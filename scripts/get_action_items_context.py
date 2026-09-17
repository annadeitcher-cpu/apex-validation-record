#!/usr/bin/env python3
"""
Print all open action items for a deal, so a decision can be made about
which ones this version's new/restated items match (semantic dedup),
before writing scripts/write_action_items.py's input file.

Usage:
    python scripts/get_action_items_context.py --deal meridian
"""

import argparse
import json
from datetime import date

from db import get_connection


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deal", required=True)
    args = parser.parse_args()

    with get_connection() as conn:
        with conn.cursor() as cur:
            opportunity_id, opportunity_name = fetch_opportunity(cur, args.deal)
            cur.execute(
                "select id, owner_role, owner_name, description, due_date, is_blocker, "
                "record_version, status, created_at from action_items "
                "where opportunity_id = %s order by status, due_date nulls last, created_at",
                (opportunity_id,),
            )
            rows = cur.fetchall()

    print(f"TODAY  {date.today().isoformat()}")
    print(f"DEAL   {opportunity_name}  ({opportunity_id})")
    print()
    if not rows:
        print("(no action items on file yet for this deal)")
        return

    for r in rows:
        (id_, owner_role, owner_name, description, due_date, is_blocker, record_version, status, created_at) = r
        flag = " [BLOCKER]" if is_blocker else ""
        print(f"[{status}] {id_}{flag}")
        print(f"  owner: {owner_role} — {owner_name}")
        print(f"  description: {description}")
        print(f"  due: {due_date}   from version: {record_version}   created: {created_at.date()}")
        print()


if __name__ == "__main__":
    import sys
    try:
        main()
    except RuntimeError as e:
        print(f"FAIL  {e}", file=sys.stderr)
        sys.exit(1)
