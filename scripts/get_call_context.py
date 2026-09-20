#!/usr/bin/env python3
"""
Print everything needed to run pass 1 + pass 3 on one call, by hand.

Usage:
    python scripts/get_call_context.py --deal meridian --call 1
    python scripts/get_call_context.py --deal "Sightline" --call 1

Prints, in order: call metadata, the participant list for that call (from
the database — the authoritative roster, per prompts/01_extract.md), the
full transcript, and the prior Validation Record payload (version = call
number - 1) if one exists. This is I/O only — it does no extraction and
calls no model. Read its output, then follow prompts/01_extract.md.
"""

import argparse
import json
import sys

from db import get_connection


def fetch_opportunity(cur, deal_name):
    cur.execute(
        """
        select o.id, o.name, a.name, o.acv, o.ae_name, o.sc_name, o.stage, o.stage_entered_at,
               date_part('day', now() - o.stage_entered_at)::int as days_in_stage
        from opportunities o
        join accounts a on a.id = o.account_id
        where o.name ilike %s order by o.name
        """,
        (f"%{deal_name}%",),
    )
    rows = cur.fetchall()
    if not rows:
        raise RuntimeError(f"no opportunity matching --deal {deal_name!r}")
    if len(rows) > 1:
        names = ", ".join(r[1] for r in rows)
        raise RuntimeError(f"--deal {deal_name!r} is ambiguous, matches: {names}")
    return rows[0]


def fetch_call(cur, opportunity_id, call_number):
    cur.execute(
        "select id, call_type, occurred_at, duration_minutes from calls "
        "where opportunity_id = %s order by occurred_at asc",
        (opportunity_id,),
    )
    calls = cur.fetchall()
    if call_number < 1 or call_number > len(calls):
        raise RuntimeError(
            f"--call {call_number} out of range — this opportunity has {len(calls)} call(s)"
        )
    return calls[call_number - 1]


def fetch_participants(cur, call_id):
    cur.execute(
        "select name, title, is_internal from participants "
        "where call_id = %s order by is_internal desc, name",
        (call_id,),
    )
    return cur.fetchall()


def fetch_transcript(cur, call_id):
    cur.execute("select content from transcripts where call_id = %s", (call_id,))
    row = cur.fetchone()
    if row is None:
        raise RuntimeError(f"no transcript for call {call_id}")
    return row[0]


def fetch_prior_record(cur, opportunity_id, call_number):
    prior_version = call_number - 1
    if prior_version < 1:
        return None
    cur.execute(
        "select payload from validation_records where opportunity_id = %s and version = %s",
        (opportunity_id, prior_version),
    )
    row = cur.fetchone()
    return row[0] if row else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deal", required=True, help="substring match against opportunity name")
    parser.add_argument("--call", type=int, required=True, dest="call_number")
    args = parser.parse_args()

    with get_connection() as conn:
        with conn.cursor() as cur:
            (opportunity_id, opportunity_name, account_name, acv, ae_name, sc_name,
             stage, stage_entered_at, days_in_stage) = fetch_opportunity(cur, args.deal)
            call_id, call_type, occurred_at, duration = fetch_call(cur, opportunity_id, args.call_number)
            participants = fetch_participants(cur, call_id)
            transcript = fetch_transcript(cur, call_id)
            prior_payload = fetch_prior_record(cur, opportunity_id, args.call_number)

    print("=" * 70)
    print(f"ACCOUNT       {account_name}")
    print(f"OPPORTUNITY   {opportunity_name}")
    print(f"OPPORTUNITY_ID {opportunity_id}")
    print(f"ACV           ${acv:,.0f}" if acv is not None else "ACV           (not set)")
    print(f"AE / SolCon   {ae_name} / {sc_name}")
    print(f"STAGE         {stage} — entered {stage_entered_at.date()} ({days_in_stage} days ago, as of now)")
    print(f"CALL #{args.call_number}  ({call_type}, {occurred_at}, {duration} min)")
    print(f"CALL_ID        {call_id}")
    print("=" * 70)

    print("\n--- PARTICIPANTS (from participants table) ---\n")
    if participants:
        for name, title, is_internal in participants:
            side = "internal (AE/SolCon)" if is_internal else "customer-side"
            print(f"- {name} — {title or 'title unknown'} ({side})")
    else:
        print("(no participant rows on file for this call)")

    print("\n--- PRIOR VALIDATION RECORD ---\n")
    if prior_payload is not None:
        print(f"(version {args.call_number - 1} — feed this to prompts/03_merge.md as the prior payload)\n")
        print(json.dumps(prior_payload, indent=2))
    else:
        print(f"(none — this is call #{args.call_number}; no version {args.call_number - 1} exists. "
              f"If this is call 1, write version 1 with no prior and no change events.)")

    print("\n--- TRANSCRIPT ---\n")
    print(transcript)


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(f"FAIL  {e}", file=sys.stderr)
        sys.exit(1)
