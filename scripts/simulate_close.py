#!/usr/bin/env python3
"""
Advance a deal to Closed Won, so the CS handoff (--handoff on
post_to_slack.py) has a real close moment to compute freshness against,
rather than hand-editing the database.

Usage:
    python scripts/simulate_close.py --deal meridian

Sets opportunities.stage = 'Closed Won' and stage_entered_at = now() — the
same column every other stage transition already uses to mean "when did we
enter the current stage," so "days in stage" and "days since close" are the
same computation the rest of the system already does, not a new concept.
Logs one activities row as a light audit trail. Does not touch calls,
transcripts, or validation_records — closing a deal doesn't rewrite its
history.
"""

import argparse
import sys

from db import get_connection


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
    args = parser.parse_args()

    with get_connection() as conn:
        with conn.cursor() as cur:
            opportunity_id, opportunity_name, stage = fetch_opportunity(cur, args.deal)

            if stage == "Closed Won":
                print(f"{opportunity_name} is already Closed Won — nothing to do.")
                return

            cur.execute(
                "update opportunities set stage = 'Closed Won', stage_entered_at = now() where id = %s",
                (opportunity_id,),
            )
            cur.execute(
                "insert into activities (opportunity_id, activity_type, actor, occurred_at, subject) "
                "values (%s, 'meeting', 'system', now(), 'Deal closed won (simulated)')",
                (opportunity_id,),
            )
        conn.commit()

    print(f"{opportunity_name}: {stage} -> Closed Won.")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(f"FAIL  {e}", file=sys.stderr)
        sys.exit(1)
