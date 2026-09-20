#!/usr/bin/env python3
"""
Single command to put a deal back into a clean, repeatable state before
recording another take.

Usage:
    python scripts/reset_demo.py --deal meridian
    python scripts/reset_demo.py --deal meridian --stage "Technical Validation" --days 23

Does three things, in order:
  1. Channel reset — wipes every message this app has ever posted in the
     deal's Slack channel (backstory from seed_channel_history.py, plus
     any pinned Record/what-changed/handoff/escalation from
     post_to_slack.py and escalate.py). Same scan-and-delete-by-bot_id
     logic as `seed_channel_history.py --reset`; a real human message is
     never touched.
  2. Stage reset — sets opportunities.stage and stage_entered_at to a
     fixed narrative starting point (`--stage`/`--days` ago), so whatever
     stage a prior take's advance_stage.py run left the deal in doesn't
     leak into the next one.
  3. Notification reset — deletes this deal's `dm_sc`/`dm_ae`/
     `channel_escalation` rows from `notifications`, since escalate.py
     checks those to avoid re-sending and will otherwise stay silent on a
     re-run even though nothing else about the deal changed.

Also does a fourth thing: DM reset. escalate.py's Stage 1 reminder is a
real, delivered Slack DM for any target with a SLACK_USER_<FIRST NAME> on
file (currently just Daniel) — that DM lands in a 1:1 channel the deal
channel's own history never touches, so neither this script's channel
reset nor seed_channel_history.py --reset ever sees it. This app's Slack
token doesn't have the im:history scope, so it can't list a DM channel's
history to find what to delete — instead this reads the delivered DM's
own slack_ts straight out of the notifications row escalate.py already
wrote (surface dm_ae/dm_sc, payload.delivered == true) and calls
chat.delete directly against that. Only deletes DMs this app can prove it
sent; never lists or touches anything else in that 1:1 channel.

Does NOT touch action_items.status or validation_records — check_closure.py
re-evaluates action items against the same underlying activities/records
each time and will land on the same statuses, so there's nothing stateful
there to reset. Also doesn't reseed the channel backstory or repost the
Record/handoff/escalation — run seed_channel_history.py and
post_to_slack.py/escalate.py afterward for that, per your usual take setup.
"""

import argparse
import os
import re
import sys

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from db import get_connection
from seed_channel_history import get_bot_id, fetch_all_history

load_dotenv()

ESCALATION_SURFACES = ["dm_sc", "dm_ae", "channel_escalation"]


def channel_id_for(opportunity_name):
    m = re.match(r"[A-Za-z]+", opportunity_name)
    var = f"SLACK_CHANNEL_{m.group(0).upper()}"
    value = os.environ.get(var, "")
    if not value:
        raise RuntimeError(f"no {var} set in .env for deal {opportunity_name!r}")
    return value


def fetch_opportunity(cur, deal_name):
    cur.execute("select id, name from opportunities where name ilike %s", (f"%{deal_name}%",))
    rows = cur.fetchall()
    if not rows:
        raise RuntimeError(f"no opportunity matching --deal {deal_name!r}")
    if len(rows) > 1:
        raise RuntimeError(f"--deal {deal_name!r} is ambiguous, matches: {[r[1] for r in rows]}")
    return rows[0]


def reset_dms(client, cur, opportunity_id):
    cur.execute(
        "select destination, payload->>'slack_ts' from notifications "
        "where opportunity_id = %s and surface in ('dm_ae', 'dm_sc') "
        "and payload->>'delivered' = 'true'",
        (opportunity_id,),
    )
    rows = cur.fetchall()
    failures = []
    deleted = 0
    for destination, slack_ts in rows:
        if not destination or not slack_ts:
            continue
        try:
            client.chat_delete(channel=destination, ts=slack_ts)
            deleted += 1
        except SlackApiError as e:
            failures.append((slack_ts, e.response.get("error", str(e))))
    print(f"  dms: deleted {deleted}/{len(rows)} delivered reminder(s).")
    if failures:
        raise RuntimeError(f"{len(failures)} DM message(s) could not be deleted: {failures}")


def reset_channel(client, channel):
    bot_id = get_bot_id(client)
    messages = fetch_all_history(client, channel)
    to_delete = [m["ts"] for m in messages if m.get("bot_id") == bot_id]
    failures = []
    deleted = 0
    for ts in to_delete:
        try:
            client.chat_delete(channel=channel, ts=ts)
            deleted += 1
        except SlackApiError as e:
            failures.append((ts, e.response.get("error", str(e))))
    print(f"  channel: deleted {deleted}/{len(to_delete)} bot message(s).")
    if failures:
        raise RuntimeError(f"{len(failures)} channel message(s) could not be deleted: {failures}")


def reset_stage(cur, opportunity_id, opportunity_name, stage, days):
    cur.execute(
        "update opportunities set stage = %s, stage_entered_at = now() - (%s || ' days')::interval where id = %s",
        (stage, str(days), opportunity_id),
    )
    print(f"  stage: {opportunity_name} -> {stage} ({days} days ago).")


def reset_notifications(cur, opportunity_id):
    cur.execute(
        "delete from notifications where opportunity_id = %s and surface = any(%s)",
        (opportunity_id, ESCALATION_SURFACES),
    )
    print(f"  notifications: cleared {cur.rowcount} escalation row(s) ({', '.join(ESCALATION_SURFACES)}).")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deal", required=True)
    parser.add_argument("--stage", default="Technical Validation")
    parser.add_argument("--days", type=int, default=23, help="days ago for stage_entered_at")
    args = parser.parse_args()

    token = os.environ.get("SLACK_BOT_TOKEN", "")
    if not token or not token.startswith("xoxb"):
        raise RuntimeError("SLACK_BOT_TOKEN missing or malformed in .env")
    client = WebClient(token=token)

    with get_connection() as conn:
        with conn.cursor() as cur:
            opportunity_id, opportunity_name = fetch_opportunity(cur, args.deal)
            channel = channel_id_for(opportunity_name)

            print(f"Resetting {opportunity_name}...")
            reset_channel(client, channel)
            reset_dms(client, cur, opportunity_id)
            reset_stage(cur, opportunity_id, opportunity_name, args.stage, args.days)
            reset_notifications(cur, opportunity_id)
        conn.commit()

    print("Done. Re-run seed_channel_history.py for the backstory, and post_to_slack.py/escalate.py for the Record/handoff/escalation, before this take.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, SlackApiError) as e:
        print(f"FAIL  {e}", file=sys.stderr)
        sys.exit(1)
