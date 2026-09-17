#!/usr/bin/env python3
"""
Print everything needed to write the Slack message for one Validation
Record version, by hand, per prompts/04_render.md.

Usage:
    python scripts/get_render_context.py --deal meridian --version 3

Prints the Record payload, this version's change events (from
record_events), and deal metadata — account, ACV, AE/SC first names,
days in Technical Validation, and how that compares to the Apex-wide
average. All of it computed here, not guessed at render time. This is
I/O only — it writes no prose and calls no model.
"""

import argparse
import json
import uuid
from datetime import date

from db import get_connection

TV_AVG_DAYS = 12
WIN_RATE_PAST_14_DAYS = 22


def fetch_opportunity(cur, deal_name):
    cur.execute(
        """
        select o.id, a.name, o.name, o.acv, o.ae_name, o.sc_name,
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
        names = ", ".join(r[2] for r in rows)
        raise RuntimeError(f"--deal {deal_name!r} is ambiguous, matches: {names}")
    return rows[0]


def fetch_record(cur, opportunity_id, version):
    cur.execute(
        "select payload from validation_records where opportunity_id = %s and version = %s",
        (opportunity_id, version),
    )
    row = cur.fetchone()
    if row is None:
        raise RuntimeError(f"no validation_records row for version {version}")
    return row[0]


def fetch_events(cur, opportunity_id, version):
    cur.execute(
        "select event_type, materiality, detail from record_events "
        "where opportunity_id = %s and to_version = %s order by id",
        (opportunity_id, version),
    )
    return cur.fetchall()


def fetch_triggering_call_date(cur, source_call_ids):
    """source_call_ids is cumulative (03_merge.md) — the last id is this version's own call."""
    if not source_call_ids:
        return None
    cur.execute("select occurred_at from calls where id = %s", (uuid.UUID(source_call_ids[-1]),))
    row = cur.fetchone()
    return row[0].date() if row else None


def _first_name(full_name):
    return (full_name or "").split()[0] if full_name else "(unassigned)"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deal", required=True)
    parser.add_argument("--version", type=int, required=True)
    args = parser.parse_args()

    with get_connection() as conn:
        with conn.cursor() as cur:
            opportunity_id, account_name, opportunity_name, acv, ae_name, sc_name, days_in_stage = fetch_opportunity(cur, args.deal)
            payload = fetch_record(cur, opportunity_id, args.version)
            events = fetch_events(cur, opportunity_id, args.version)
            triggering_call_date = fetch_triggering_call_date(cur, payload.get("source_call_ids", []))

    pct_over_avg = round((days_in_stage - TV_AVG_DAYS) / TV_AVG_DAYS * 100)
    ae_first, sc_first = _first_name(ae_name), _first_name(sc_name)
    material_events = [(t, m, d) for t, m, d in events if m == "material"]

    print("=" * 70)
    print(f"TODAY             {date.today().isoformat()} ({date.today().strftime('%A')})")
    print(f"ACCOUNT           {account_name}")
    print(f"OPPORTUNITY       {opportunity_name}")
    print(f"ACV               ${acv:,.0f}" if acv is not None else "ACV               (not set)")
    print(f"AE_FIRST_NAME     {ae_first}")
    print(f"SC_FIRST_NAME     {sc_first}")
    print(f"DAYS_IN_STAGE     {days_in_stage}")
    print(f"TV_AVG_DAYS       {TV_AVG_DAYS}")
    print(f"PCT_OVER_AVG      {pct_over_avg}%  (this deal has spent {pct_over_avg}% more time in Technical Validation than the Apex average)")
    print(f"WIN_RATE_PAST_14  {WIN_RATE_PAST_14_DAYS}%")
    print("=" * 70)

    print(f"\n--- CHANGE EVENTS (v{args.version}) ---\n")
    call_date_str = triggering_call_date.strftime("%b %-d") if triggering_call_date else "(unknown)"
    print(f"TRIGGERING_CALL_DATE  {call_date_str}  (this version's own call — use it in the 'what changed' header)")
    if not events:
        print("(none — this is version 1, or nothing changed)")
    else:
        for event_type, materiality, detail in events:
            print(f"[{materiality}] {event_type}: {json.dumps(detail)}")
        print(f"\n({len(material_events)} material event(s) — a 'what changed' message is only warranted if this is >0 and version > 1)")

    print("\n--- RECORD PAYLOAD ---\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        import sys
        print(f"FAIL  {e}", file=sys.stderr)
        sys.exit(1)
