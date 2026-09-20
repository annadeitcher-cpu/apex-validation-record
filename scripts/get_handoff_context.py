#!/usr/bin/env python3
"""
Print everything needed to write the CS handoff message, by hand, per
prompts/05_handoff.md.

Usage:
    python scripts/get_handoff_context.py --deal meridian

Prints: deal metadata (account, ACV, CSM name), the latest Validation
Record's payload (the accrued, current state — success_criteria,
integration_patterns, objections, open_risks), the v1 payload's
stakeholders only (the baseline this call needs for the delta), and a
freshness figure (days between the latest record's generated_at and the
close moment). This is I/O only — it does no writing and calls no model.

Requires the deal to actually be Closed Won (see scripts/simulate_close.py)
— the handoff is a close-triggered artifact, not something that fires
mid-deal.
"""

import argparse
import json
import sys
from datetime import datetime, timezone

from db import get_connection


def fetch_opportunity(cur, deal_name):
    cur.execute(
        """
        select o.id, a.name, o.name, o.acv, o.ae_name, o.sc_name, o.csm_name,
               o.stage, o.stage_entered_at
        from opportunities o join accounts a on a.id = o.account_id
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


def fetch_v1_stakeholders(cur, opportunity_id):
    cur.execute(
        "select payload -> 'stakeholders' from validation_records "
        "where opportunity_id = %s and version = 1",
        (opportunity_id,),
    )
    row = cur.fetchone()
    if row is None:
        raise RuntimeError("no version 1 record on file — the handoff needs a baseline to diff against")
    return row[0]


def fetch_latest_record(cur, opportunity_id):
    cur.execute(
        "select version, payload, generated_at from validation_records "
        "where opportunity_id = %s order by version desc limit 1",
        (opportunity_id,),
    )
    row = cur.fetchone()
    if row is None:
        raise RuntimeError("no validation_records on file for this deal")
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deal", required=True)
    args = parser.parse_args()

    with get_connection() as conn:
        with conn.cursor() as cur:
            (opportunity_id, account_name, opportunity_name, acv, ae_name, sc_name,
             csm_name, stage, stage_entered_at) = fetch_opportunity(cur, args.deal)

            if stage != "Closed Won":
                raise RuntimeError(
                    f"{opportunity_name} is in stage {stage!r}, not 'Closed Won' — the handoff is a "
                    f"close-triggered artifact. Run scripts/simulate_close.py --deal {args.deal!r} first."
                )

            v1_stakeholders = fetch_v1_stakeholders(cur, opportunity_id)
            latest_version, latest_payload, generated_at = fetch_latest_record(cur, opportunity_id)

    freshness_days = (stage_entered_at.date() - generated_at.date()).days

    print("=" * 70)
    print(f"ACCOUNT           {account_name}")
    print(f"OPPORTUNITY       {opportunity_name}")
    print(f"ACV               ${acv:,.0f}" if acv is not None else "ACV               (not set)")
    print(f"AE / SolCon / CSM     {ae_name} / {sc_name} / {csm_name}")
    print(f"CLOSED            {stage_entered_at.date().isoformat()}")
    print(f"LATEST VERSION    v{latest_version}  (generated {generated_at.date().isoformat()})")
    print(f"FRESHNESS         record last updated {freshness_days} day(s) before close")
    print("=" * 70)

    print("\n--- V1 STAKEHOLDERS (baseline — \"who bought\") ---\n")
    print(json.dumps(v1_stakeholders, indent=2))

    print(f"\n--- LATEST RECORD PAYLOAD (v{latest_version} — the accrued, current state) ---\n")
    print(json.dumps(latest_payload, indent=2))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(f"FAIL  {e}", file=sys.stderr)
        sys.exit(1)
