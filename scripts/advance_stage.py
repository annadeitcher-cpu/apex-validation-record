#!/usr/bin/env python3
"""
Advance a deal to a new pipeline stage, live, for a demo beat — e.g. the
moment Technical Validation's exit criteria all land and the deal should
visibly move to Commercial Negotiation. General version of the same
one-column update scripts/simulate_close.py does specifically for Closed
Won; use that one instead if Closed Won is genuinely what you want (it has
its own purpose-specific docstring and is what the CS handoff pass checks
for).

Usage:
    python scripts/advance_stage.py --deal meridian --stage "Commercial Negotiation"

Sets opportunities.stage and stage_entered_at = now() — the same column
every stage transition in this system uses for "when did we enter the
current stage," so scripts/timeline_marker.py's live days-in-stage number
reflects it immediately. Logs one activities row as a light audit trail.
Refuses a stage name outside the fixed enum in sql/schema.sql rather than
writing a typo into the pipeline silently.
"""

import argparse
import sys

from db import get_connection

VALID_STAGES = {
    "Discovery",
    "Technical Validation",
    "Commercial Negotiation",
    "Legal/Close",
    "Closed Won",
    "Closed Lost",
}


def fetch_opportunity(cur, deal_name):
    cur.execute(
        "select id, name, stage from opportunities where name ilike %s order by name",
        (f"%{deal_name}%",),
    )
    rows = cur.fetchall()
    if not rows:
        raise RuntimeError(f"no opportunity matching --deal {deal_name!r}")
    if len(rows) > 1:
        raise RuntimeError(f"--deal {deal_name!r} is ambiguous, matches: {[r[1] for r in rows]}")
    return rows[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deal", required=True)
    parser.add_argument("--stage", required=True)
    args = parser.parse_args()

    if args.stage not in VALID_STAGES:
        raise RuntimeError(f"--stage {args.stage!r} isn't one of {sorted(VALID_STAGES)}")

    with get_connection() as conn:
        with conn.cursor() as cur:
            opportunity_id, opportunity_name, stage = fetch_opportunity(cur, args.deal)

            if stage == args.stage:
                print(f"{opportunity_name} is already {args.stage} — nothing to do.")
                return

            cur.execute(
                "update opportunities set stage = %s, stage_entered_at = now() where id = %s",
                (args.stage, opportunity_id),
            )
            cur.execute(
                "insert into activities (opportunity_id, activity_type, actor, occurred_at, subject) "
                "values (%s, 'meeting', 'system', now(), %s)",
                (opportunity_id, f"Stage advanced to {args.stage} (simulated)"),
            )
        conn.commit()

    print(f"{opportunity_name}: {stage} -> {args.stage}.")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(f"FAIL  {e}", file=sys.stderr)
        sys.exit(1)
