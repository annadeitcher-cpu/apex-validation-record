#!/usr/bin/env python3
"""
Write action items for a Record version — insert or update, per a
hand-written decision file. This script does no semantic reasoning: dedup
across versions ("is this the same item as one already open, just restated
in different words?") is decided by whoever runs the chain, by reading
scripts/get_action_items_context.py's output and matching on owner plus
meaning, not string equality. This script just applies the decision.

Usage:
    python scripts/write_action_items.py --deal meridian --version 3 --items /tmp/items.json

Items file: a JSON list of objects, each either:
  {"op": "insert", "owner_role": "ae|sc|customer", "owner_name": "...",
   "description": "...", "due_date": "YYYY-MM-DD or null", "is_blocker": true|false}
  {"op": "update", "id": "<uuid>", "owner_role": "...", "owner_name": "...",
   "description": "...", "due_date": "... or null", "is_blocker": true|false}

"update" means: this version restated an already-open item (same owner,
same underlying ask) — its row is updated in place (description, due_date,
is_blocker, record_version) rather than a new row inserted. "insert" means
this is a genuinely new item.
"""

import argparse
import json
import sys
from pathlib import Path

from db import get_connection

OWNER_ROLES = {"ae", "sc", "customer"}


def fetch_opportunity(cur, deal_name):
    cur.execute(
        "select id, name from opportunities where name ilike %s order by name",
        (f"%{deal_name}%",),
    )
    rows = cur.fetchall()
    if not rows:
        raise RuntimeError(f"no opportunity matching --deal {deal_name!r}")
    if len(rows) > 1:
        names = ", ".join(r[1] for r in rows)
        raise RuntimeError(f"--deal {deal_name!r} is ambiguous, matches: {names}")
    return rows[0]


def validate_item(item, index):
    p = f"items[{index}]"
    errors = []
    if item.get("op") not in ("insert", "update"):
        errors.append(f"{p}.op must be 'insert' or 'update'")
    if item.get("op") == "update" and not item.get("id"):
        errors.append(f"{p}.id is required for op=update")
    if item.get("owner_role") not in OWNER_ROLES:
        errors.append(f"{p}.owner_role must be one of {sorted(OWNER_ROLES)}")
    if not item.get("owner_name"):
        errors.append(f"{p}.owner_name is required")
    if not item.get("description"):
        errors.append(f"{p}.description is required")
    if "due_date" not in item:
        errors.append(f"{p}.due_date is required (may be null)")
    if not isinstance(item.get("is_blocker"), bool):
        errors.append(f"{p}.is_blocker must be a boolean")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deal", required=True)
    parser.add_argument("--version", type=int, required=True)
    parser.add_argument("--items", required=True, dest="items_path")
    args = parser.parse_args()

    items = json.loads(Path(args.items_path).read_text())
    if not isinstance(items, list):
        raise RuntimeError("items file must contain a JSON list")

    all_errors = []
    for i, item in enumerate(items):
        all_errors.extend(validate_item(item, i))
    if all_errors:
        for e in all_errors:
            print(f"  - {e}", file=sys.stderr)
        raise RuntimeError(f"{len(all_errors)} validation error(s) in items file")

    inserted, updated = 0, 0
    with get_connection() as conn:
        with conn.cursor() as cur:
            opportunity_id, opportunity_name = fetch_opportunity(cur, args.deal)

            for item in items:
                if item["op"] == "insert":
                    cur.execute(
                        """
                        insert into action_items
                            (opportunity_id, record_version, owner_role, owner_name, description, due_date, is_blocker, status)
                        values (%s, %s, %s, %s, %s, %s, %s, 'open')
                        """,
                        (opportunity_id, args.version, item["owner_role"], item["owner_name"],
                         item["description"], item["due_date"], item["is_blocker"]),
                    )
                    inserted += 1
                else:
                    cur.execute(
                        """
                        update action_items
                        set record_version = %s, owner_role = %s, owner_name = %s,
                            description = %s, due_date = %s, is_blocker = %s
                        where id = %s and opportunity_id = %s
                        """,
                        (args.version, item["owner_role"], item["owner_name"],
                         item["description"], item["due_date"], item["is_blocker"],
                         item["id"], opportunity_id),
                    )
                    if cur.rowcount == 0:
                        raise RuntimeError(f"update target id {item['id']!r} not found for {opportunity_name}")
                    updated += 1

        conn.commit()

    print(f"{opportunity_name} v{args.version}: {inserted} inserted, {updated} updated.")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(f"FAIL  {e}", file=sys.stderr)
        sys.exit(1)
