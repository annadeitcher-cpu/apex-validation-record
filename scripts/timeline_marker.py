#!/usr/bin/env python3
"""
Prints a boxed on-screen banner showing where a deal sits in the pipeline
right now, for a screen-recorded demo — run it before each beat so the
terminal carries the state the narration alone can't over a long recording.

Usage:
    python scripts/timeline_marker.py --deal meridian --day 22 --call 3

--day is a narrative label, not a database value — you choose it to match
wherever the recording currently is in the story. Everything else in the
banner (stage, days-in-stage, exit criteria) is read live from the
database at the moment this runs, never hardcoded — which means the
database itself has to actually be in the state you're narrating when you
call this. In particular, `opportunities.stage`/`stage_entered_at` have no
history table, so showing "Technical Validation" at one beat and
"Commercial Negotiation" at a later one means the deal's actual stage row
has to have been advanced for real between those two calls, not just
implied by --day changing.

Exit criteria are read from the Record version matching --call, not
simply "the latest version" — so a beat narrating call 3 correctly shows
call 3's exit-criteria state even if call 4's Record already exists in the
database (as it usually will, once the full chain's been run once). This
assumes the deal's calls and Record versions accrue 1:1, which is how
every deal in this system is built. If that version doesn't exist yet, or
exists but predates `stage_exit_criteria` being part of the contract (true
for some early seed data), the banner reads "no record" rather than
guessing or erroring.
"""

import argparse
import sys

from db import get_connection


def fetch_opportunity(cur, deal_name):
    cur.execute(
        "select o.id, o.name, o.acv, o.stage, o.stage_entered_at "
        "from opportunities o where o.name ilike %s",
        (f"%{deal_name}%",),
    )
    rows = cur.fetchall()
    if not rows:
        raise RuntimeError(f"no opportunity matching --deal {deal_name!r}")
    if len(rows) > 1:
        raise RuntimeError(f"--deal {deal_name!r} is ambiguous, matches: {[r[1] for r in rows]}")
    return rows[0]


def fetch_total_calls(cur, opportunity_id):
    cur.execute("select count(*) from calls where opportunity_id = %s", (opportunity_id,))
    return cur.fetchone()[0]


def fetch_days_in_stage(cur, opportunity_id):
    cur.execute(
        "select greatest(date_part('day', now() - stage_entered_at)::int, 0) "
        "from opportunities where id = %s",
        (opportunity_id,),
    )
    return cur.fetchone()[0]


def fetch_exit_criteria(cur, opportunity_id, call_number):
    """(met, total) for the Record version matching this call, or None if
    there's nothing usable — no such version, or a version old enough to
    predate stage_exit_criteria in the contract."""
    cur.execute(
        "select payload->'stage_exit_criteria' from validation_records "
        "where opportunity_id = %s and version = %s",
        (opportunity_id, call_number),
    )
    row = cur.fetchone()
    if row is None or row[0] is None:
        return None
    criteria = row[0]
    return sum(1 for c in criteria if c["met"]), len(criteria)


def render(day, opportunity_name, acv, stage, days_in_stage, call_number, total_calls, exit_criteria):
    acv_str = f"${acv:,.0f}" if acv is not None else "(ACV not set)"
    criteria_str = f"{exit_criteria[0]} of {exit_criteria[1]}" if exit_criteria else "no record"

    lines = [
        f"DAY {day} · {opportunity_name} · {acv_str}",
        f"Stage: {stage.upper()} ({days_in_stage} day{'s' if days_in_stage != 1 else ''})",
        f"Call {call_number} of {total_calls} · Exit criteria: {criteria_str}",
    ]

    width = max(len(l) for l in lines) + 4
    border = "═" * width
    print(border)
    for l in lines:
        print(f"  {l}")
    print(border)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deal", required=True)
    parser.add_argument("--day", type=int, required=True, help="simulated day number for the narration — a label, not a DB value")
    parser.add_argument("--call", type=int, required=True, help="which call this beat represents")
    args = parser.parse_args()

    with get_connection() as conn:
        with conn.cursor() as cur:
            opportunity_id, opportunity_name, acv, stage, stage_entered_at = fetch_opportunity(cur, args.deal)
            total_calls = fetch_total_calls(cur, opportunity_id)
            days_in_stage = fetch_days_in_stage(cur, opportunity_id)
            exit_criteria = fetch_exit_criteria(cur, opportunity_id, args.call)

    render(args.day, opportunity_name, acv, stage, days_in_stage, args.call, total_calls, exit_criteria)


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(f"FAIL  {e}", file=sys.stderr)
        sys.exit(1)
