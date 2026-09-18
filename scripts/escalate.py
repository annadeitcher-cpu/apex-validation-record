#!/usr/bin/env python3
"""
Two-stage escalation on missed action items, per docs/enforcement-layer-spec.md §3.

Usage:
    python scripts/escalate.py --deal meridian

Stage 1 — private, >=72 hours (3 days) past due. Names the item, the due
date, and days-in-stage. Sent once — recorded in `notifications` so it
never repeats.

Real delivery, when a real Slack user id is on file: if `SLACK_USER_<FIRST
NAME>` (e.g. `SLACK_USER_DANIEL`) is set in .env for the target's first
name, this actually opens a DM via `conversations.open` and posts there via
`chat.postMessage` — not simulated. Falls back to the old print-only,
not-actually-delivered behavior for anyone without a real id on file (still
true for the SC in this prototype). `opportunities.ae_name`/`sc_name`
themselves stay plain text either way; the id is looked up separately by
first name, not stored on the opportunity.

Stage 2 — public, >=7 days past due, posted to the deal channel. Opens with
the ⚠️ OVERDUE message-type header (see prompts/04_render.md's "Message-type
header" section — the same convention applies here), then names the item,
notes that a private reminder already went out (and when), and names the
stage-exit criterion it's gating, if it's a formal blocker. Idempotent like
every other posting script in this system — re-running it updates the same
message in place (via `notifications`) rather than posting a duplicate.
Only fires if stage 1 has already been recorded (it may be recorded in this
same run, for an item that's already well past both thresholds — private
always precedes public, even when catching up on a backlog). Stage 1
doesn't carry the ⚠️ OVERDUE message-type header even when it's really
delivered — that convention (see prompts/04_render.md) is for messages
posted to the shared deal channel, not a 1:1 DM; a DM doesn't need a
"what is this and why does it exist" banner the way a channel post read
cold does.

Customer-owned items escalate to the AE, never to the customer — nothing in
this system ever messages anyone outside Apex. There is no code path here
that resolves a Slack destination from `owner_role == "customer"`.

Both messages are short, compact, structured alerts (not narrative prose,
unlike the Record itself) — composed directly here rather than through a
model pass, since there's no judgment involved, only known facts assembled
into a fixed, scannable format. That's a deliberate, narrow exception to
"no string templating," not a walk-back of it: nothing here required
reasoning about the deal, only arithmetic on dates already known.
"""

import argparse
import json
import os
import re
from datetime import date, timedelta

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from db import get_connection
from slack_blocks import build_blocks, fallback_text

TV_AVG_DAYS = 12
STAGE1_DAYS = 3   # 72 hours
STAGE2_DAYS = 7

OWNER_ROLE_TO_CRITERION_KEYWORDS = {
    "sc": ("resolved", "agreed"),       # objections resolved / integration approach agreed
    "ae": ("economic buyer", "next step", "success criteria"),
}


def fetch_opportunities(cur, deal_name):
    cur.execute(
        """
        select o.id, o.name, o.ae_name, o.sc_name, o.stage,
               date_part('day', now() - o.stage_entered_at)::int as days_in_stage
        from opportunities o where o.name ilike %s
        """,
        (f"%{deal_name}%",),
    )
    rows = cur.fetchall()
    if not rows:
        raise RuntimeError(f"no opportunity matching --deal {deal_name!r}")
    if len(rows) > 1:
        raise RuntimeError(f"--deal {deal_name!r} is ambiguous, matches: {[r[1] for r in rows]}")
    return rows[0]


def real_user_id_for(first_name):
    """A real Slack user id for this first name, if .env has one on file — else empty string."""
    return os.environ.get(f"SLACK_USER_{first_name.upper()}", "")


def channel_id_for(opportunity_name):
    m = re.match(r"[A-Za-z]+", opportunity_name)
    var = f"SLACK_CHANNEL_{m.group(0).upper()}"
    value = os.environ.get(var, "")
    if not value:
        raise RuntimeError(f"no {var} set in .env for deal {opportunity_name!r}")
    return value


def fetch_missed_items(cur, opportunity_id):
    cur.execute(
        "select id, owner_role, owner_name, description, due_date, is_blocker "
        "from action_items where opportunity_id = %s and status = 'missed' order by due_date",
        (opportunity_id,),
    )
    return cur.fetchall()


def escalation_target(owner_role, owner_name, ae_name, sc_name):
    """Customer items always redirect to the AE. Never the customer — see module docstring."""
    if owner_role == "customer":
        return "ae", ae_name
    if owner_role == "sc":
        return "sc", sc_name
    return "ae", ae_name


def already_sent(cur, item_id, surface):
    cur.execute(
        "select sent_at from notifications where surface = %s and (payload->>'action_item_id') = %s "
        "order by sent_at desc limit 1",
        (surface, str(item_id)),
    )
    row = cur.fetchone()
    return row[0] if row else None


def fetch_escalation_notification(cur, item_id):
    cur.execute(
        "select destination, payload->>'slack_ts' from notifications "
        "where surface = 'channel_escalation' and (payload->>'action_item_id') = %s "
        "order by sent_at desc limit 1",
        (str(item_id),),
    )
    return cur.fetchone()


def record_notification(cur, opportunity_id, surface, destination, item_id, extra=None):
    payload = {"action_item_id": str(item_id)}
    if extra:
        payload.update(extra)
    cur.execute(
        "insert into notifications (opportunity_id, surface, destination, slack_ts, payload, sent_at) "
        "values (%s, %s, %s, %s, %s, now())",
        (opportunity_id, surface, destination, None, json.dumps(payload)),
    )


def find_gating_criterion(cur, opportunity_id, target_role, is_blocker):
    if not is_blocker:
        return None
    cur.execute(
        "select payload from validation_records where opportunity_id = %s order by version desc limit 1",
        (opportunity_id,),
    )
    row = cur.fetchone()
    if row is None:
        return None
    criteria = row[0].get("stage_exit_criteria", [])
    owner_tag = "AE" if target_role == "ae" else "SC"
    for c in criteria:
        if c["owner"] == owner_tag and not c["met"]:
            return c["criterion"]
    return None


def stage1_text(description, due_date, days_in_stage, opportunity_name, stage):
    if stage == "Technical Validation":
        stage_line = f"{opportunity_name} is {days_in_stage} days into Technical Validation — the Apex average is {TV_AVG_DAYS}."
    else:
        # Same fix as stage2_text: once the deal has moved on, a live "days in stage" figure
        # measures the wrong stage entirely (and can go negative if stage_entered_at is now
        # in the future relative to today, e.g. a simulated close date) — not just stale.
        stage_line = f"{opportunity_name} has since moved to {stage} — this item was still open at that point."
    return f"Reminder: \"{description}\" was due {due_date.strftime('%a %b %-d')} and hasn't been marked done.\n{stage_line}"


def stage2_text(owner_name, description, due_date, days_late, stage1_sent_at, gating, opportunity_name, days_in_stage, stage):
    first_name = owner_name.split()[0]
    header = (
        f"⚠️ *OVERDUE* · {opportunity_name}\n"
        f"_Second reminder. Private DM sent to {first_name} on {stage1_sent_at.strftime('%b %-d')}._"
    )
    if stage == "Technical Validation":
        stage_line = f"{opportunity_name} is {days_in_stage} days in Technical Validation. Average is {TV_AVG_DAYS}."
    else:
        # The deal moved on (e.g. closed) after this item was created — a live "days in stage"
        # figure would be measuring the wrong stage entirely, not just a stale number.
        stage_line = f"{opportunity_name} has since moved to {stage} — this item was still open at that point."
    body = [
        f"@{first_name} — open {days_late} days past due",
        f"{description} · due {due_date.strftime('%a %b %-d')} · private reminder sent {stage1_sent_at.strftime('%a %b %-d')}",
        f"Gating: {gating}" if gating else "Not tied to a formal stage-exit blocker — flagged for visibility regardless.",
        stage_line,
    ]
    return header + "\n---\n" + "\n".join(body)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deal", required=True)
    args = parser.parse_args()

    token = os.environ.get("SLACK_BOT_TOKEN", "")
    if not token or not token.startswith("xoxb"):
        raise RuntimeError("SLACK_BOT_TOKEN missing or malformed in .env")
    client = WebClient(token=token)

    today = date.today()

    with get_connection() as conn:
        with conn.cursor() as cur:
            opportunity_id, opportunity_name, ae_name, sc_name, stage, days_in_stage = fetch_opportunities(cur, args.deal)
            channel_id = channel_id_for(opportunity_name)
            items = fetch_missed_items(cur, opportunity_id)

            if not items:
                print(f"{opportunity_name}: no missed items — nothing to escalate.")
                return

            for item_id, owner_role, owner_name, description, due_date, is_blocker in items:
                days_late = (today - due_date).days
                target_role, target_name = escalation_target(owner_role, owner_name, ae_name, sc_name)
                dm_surface = f"dm_{target_role}"

                stage1_sent_at = already_sent(cur, item_id, dm_surface)

                if days_late >= STAGE1_DAYS and stage1_sent_at is None:
                    text = stage1_text(description, due_date, days_in_stage, opportunity_name, stage)
                    first_name = target_name.split()[0]
                    real_uid = real_user_id_for(first_name)

                    if real_uid:
                        dm_channel = client.conversations_open(users=[real_uid])["channel"]["id"]
                        resp = client.chat_postMessage(channel=dm_channel, text=text)
                        print(f"\n--- STAGE 1 (private DM, delivered to {target_name} via conversations.open) ---")
                        print(text)
                        record_notification(
                            cur, opportunity_id, dm_surface, dm_channel, item_id,
                            {"slack_ts": resp["ts"], "delivered": True, "user_id": real_uid},
                        )
                    else:
                        print(f"\n--- STAGE 1 (private, would-be DM to {target_name}) ---")
                        print(text)
                        print(
                            f"[not actually delivered — no SLACK_USER_{first_name.upper()} on file in .env. "
                            f"Recorded as sent so it never repeats.]"
                        )
                        record_notification(cur, opportunity_id, dm_surface, target_name, item_id, {"delivered": False})

                    conn.commit()
                    stage1_sent_at = today

                if days_late >= STAGE2_DAYS and stage1_sent_at is not None:
                    gating = find_gating_criterion(cur, opportunity_id, target_role, is_blocker)
                    text = stage2_text(
                        target_name, description, due_date, days_late,
                        stage1_sent_at if isinstance(stage1_sent_at, date) else stage1_sent_at.date(),
                        gating, opportunity_name, days_in_stage, stage,
                    )
                    existing = fetch_escalation_notification(cur, item_id)
                    if existing is None:
                        print(f"\n--- STAGE 2 (public, posting to #{opportunity_name.split()[0].lower()}-deal channel) ---")
                        print(text)
                        resp = client.chat_postMessage(channel=channel_id, text=fallback_text(text), blocks=build_blocks(text))
                        record_notification(cur, opportunity_id, "channel_escalation", channel_id, item_id, {"slack_ts": resp["ts"]})
                        conn.commit()
                    else:
                        destination, slack_ts = existing
                        print(f"\n--- STAGE 2 (public, updating existing message {slack_ts} in place) ---")
                        print(text)
                        client.chat_update(channel=destination, ts=slack_ts, text=fallback_text(text), blocks=build_blocks(text))
                        record_notification(cur, opportunity_id, "channel_escalation", destination, item_id, {"slack_ts": slack_ts})
                        conn.commit()


if __name__ == "__main__":
    import sys
    try:
        main()
    except (RuntimeError, SlackApiError) as e:
        print(f"FAIL  {e}", file=sys.stderr)
        sys.exit(1)
