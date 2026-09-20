#!/usr/bin/env python3
"""
Resolve open action items against evidence, for every item with
due_date <= today. No evidence by the due date means status: missed.

Usage:
    python scripts/check_closure.py            # all deals
    python scripts/check_closure.py --deal meridian

Evidence rules, per owner type (docs/enforcement-layer-spec.md §2). These
are deliberately simple, prototype-level heuristics, not precise semantic
matching — noted inline where that matters:

  AE items:       an `activities` row for the opportunity, same actor as
                   the owner, dated on or after the item's creation and on
                   or before ~7 days past due — AND whose subject plausibly
                   corresponds to the item's description (shared significant
                   words). Strong correspondence (2+ shared words) ->
                   completed. Weak correspondence (exactly 1 shared word) ->
                   completed_unverified — evidence exists but doesn't clearly
                   match, so it's not claimed as verified. No corresponding
                   activity at all, regardless of word overlap -> no
                   evidence. This still isn't proof the specific action
                   happened (a real system would tie an activity to the item
                   explicitly), but it no longer credits any unrelated
                   activity as evidence the way "any activity after
                   creation" did — that produced a real false positive
                   (see docs/corrections.md #5) before this fix.
  SolCon items:   a newer Record version exists than the one that logged
                   the item (the SolCon had another checkpoint to act), and if
                   the item is a blocker, the latest version's stage exit
                   criteria are fully met.
  Customer items: the opportunity's stage has advanced past Technical
                   Validation, or — for a blocking item — the latest
                   Record's stage exit criteria are fully met.

No evidence found and due_date <= today: status -> missed. This never
degrades silently: completed_unverified is a distinct, visibly weaker
status precisely so a dashboard built on this can report verified and
unverified separately rather than conflating them with real confirmation.
"""

import argparse
import re
from datetime import date, timedelta

from db import get_connection

STOPWORDS = {
    "about", "after", "again", "their", "there", "which", "would", "could",
    "should", "where", "really", "actually", "because", "something",
    "things", "think", "thing", "these", "those", "being", "still",
    "before", "other", "every", "with", "from", "that", "this", "will",
    "send", "have", "into", "your", "over",
}


def _significant_words(text):
    return {w for w in re.findall(r"[a-zA-Z]+", (text or "").lower()) if len(w) >= 4 and w not in STOPWORDS}


def fetch_opportunities(cur, deal_name):
    if deal_name:
        cur.execute("select id, name, stage from opportunities where name ilike %s", (f"%{deal_name}%",))
    else:
        cur.execute("select id, name, stage from opportunities")
    return cur.fetchall()


def fetch_due_open_items(cur, opportunity_id):
    cur.execute(
        "select id, owner_role, owner_name, description, due_date, is_blocker, record_version, created_at "
        "from action_items where opportunity_id = %s and status = 'open' and due_date <= %s",
        (opportunity_id, date.today()),
    )
    return cur.fetchall()


def latest_version_and_criteria(cur, opportunity_id):
    cur.execute(
        "select version, payload from validation_records where opportunity_id = %s order by version desc limit 1",
        (opportunity_id,),
    )
    row = cur.fetchone()
    if row is None:
        return None, None
    version, payload = row
    return version, payload.get("stage_exit_criteria")


def check_ae(cur, opportunity_id, owner_name, description, created_at, due_date):
    window_end = due_date + timedelta(days=7)
    cur.execute(
        "select subject from activities "
        "where opportunity_id = %s and actor ilike %s "
        "and occurred_at >= %s and occurred_at <= %s",
        (opportunity_id, owner_name, created_at, window_end),
    )
    item_words = _significant_words(description)
    best_overlap = 0
    for (subject,) in cur.fetchall():
        overlap = len(item_words & _significant_words(subject))
        best_overlap = max(best_overlap, overlap)

    if best_overlap >= 2:
        return "completed"
    if best_overlap == 1:
        return "completed_unverified"
    return None


def check_sc(cur, opportunity_id, record_version, is_blocker):
    latest_version, criteria = latest_version_and_criteria(cur, opportunity_id)
    if latest_version is None or latest_version <= record_version:
        return None
    if is_blocker:
        resolved = bool(criteria) and all(c["met"] for c in criteria)
    else:
        resolved = True
    return "completed" if resolved else None


def check_customer(cur, opportunity_id, stage, record_version, is_blocker):
    if stage != "Technical Validation":
        return "completed"
    latest_version, criteria = latest_version_and_criteria(cur, opportunity_id)
    if is_blocker:
        resolved = bool(criteria) and all(c["met"] for c in criteria)
    else:
        resolved = latest_version is not None and latest_version > record_version
    return "completed" if resolved else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deal", help="omit to check every deal")
    args = parser.parse_args()

    with get_connection() as conn:
        with conn.cursor() as cur:
            opportunities = fetch_opportunities(cur, args.deal)
            if not opportunities:
                print(f"no opportunity matching --deal {args.deal!r}" if args.deal else "no opportunities found")
                return

            counts = {"completed": 0, "completed_unverified": 0, "missed": 0}
            for opportunity_id, opportunity_name, stage in opportunities:
                items = fetch_due_open_items(cur, opportunity_id)
                if not items:
                    continue
                print(f"=== {opportunity_name} ===")
                for item_id, owner_role, owner_name, description, due_date, is_blocker, record_version, created_at in items:
                    if owner_role == "ae":
                        result = check_ae(cur, opportunity_id, owner_name, description, created_at, due_date)
                    elif owner_role == "sc":
                        result = check_sc(cur, opportunity_id, record_version, is_blocker)
                    else:
                        result = check_customer(cur, opportunity_id, stage, record_version, is_blocker)

                    status = result or "missed"
                    completed_at = "now()" if status == "completed" else "null"
                    cur.execute(
                        f"update action_items set status = %s, completed_at = {completed_at} where id = %s",
                        (status, item_id),
                    )
                    counts[status] += 1
                    label = {"completed": "completed", "completed_unverified": "UNVERIFIED", "missed": "MISSED"}[status]
                    print(f"  {label:<11}[{owner_role}] {description[:65]} (due {due_date})")
            conn.commit()

    print(f"\n{counts['completed']} completed, {counts['completed_unverified']} unverified, {counts['missed']} missed.")


if __name__ == "__main__":
    main()
