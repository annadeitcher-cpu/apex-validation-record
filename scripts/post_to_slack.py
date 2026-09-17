#!/usr/bin/env python3
"""
Post/update a Validation Record in the deal's Slack channel.

Usage:
    python scripts/post_to_slack.py --deal meridian --version 1 --message-file /tmp/v1.txt
    python scripts/post_to_slack.py --deal meridian --version 3 --message-file /tmp/v3.txt --changed-file /tmp/v3_changed.txt
    python scripts/post_to_slack.py --deal meridian --handoff --message-file /tmp/handoff.txt

This script does no content formatting — it posts exactly the text it's
given. The text is written by hand, by following prompts/04_render.md (or,
for --handoff, prompts/05_handoff.md) against the output of
scripts/get_render_context.py (or scripts/get_handoff_context.py). No field
value from the Record is templated into a message anywhere in this file.

The one thing this script does structure: hand-written text is split on
lines containing only `---` (scripts/slack_blocks.py) into Block Kit
section blocks with dividers between them, so messages don't post as a
single wall of text. That's mechanical parsing on a fixed delimiter, not a
content decision — same category as write_record.py's schema validation.
Canvas content is untouched by this, since a Canvas is markdown, not Block
Kit, and `---` already renders there as a horizontal rule.

v1 creates the object in the deal channel (canvas, falling back to a pinned
message if canvases aren't available on this workspace/plan) and stores its
identity (canvas_id or slack_ts) in `notifications`. v2+ update that same
object in place. If --changed-file is given, its text is posted as a
"what changed" channel message — or, if one was already posted for this
version, updated in place rather than duplicated.

--handoff posts the CS handoff as its own message (surface `cs_handoff` in
`notifications`) rather than updating the pinned Record — it's a
close-triggered artifact, not a version. Mutually exclusive with --version;
requires the deal to already be Closed Won (see scripts/simulate_close.py).
Re-running --handoff updates the same message in place, not a duplicate.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from db import get_connection
from slack_blocks import build_blocks, fallback_text


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


def channel_id_for(opportunity_name):
    m = re.match(r"[A-Za-z]+", opportunity_name)
    var = f"SLACK_CHANNEL_{m.group(0).upper()}"
    value = os.environ.get(var, "")
    if not value:
        raise RuntimeError(f"no {var} set in .env for deal {opportunity_name!r}")
    return value


def fetch_record_status(cur, opportunity_id, version):
    cur.execute(
        "select status from validation_records where opportunity_id = %s and version = %s",
        (opportunity_id, version),
    )
    row = cur.fetchone()
    if row is None:
        raise RuntimeError(f"no validation_records row for version {version}")
    return row[0]


def fetch_latest_version(cur, opportunity_id):
    cur.execute(
        "select version, status from validation_records where opportunity_id = %s order by version desc limit 1",
        (opportunity_id,),
    )
    row = cur.fetchone()
    if row is None:
        raise RuntimeError("no validation_records on file for this deal")
    return row


def fetch_handoff_notification(cur, opportunity_id):
    cur.execute(
        "select destination, slack_ts from notifications "
        "where opportunity_id = %s and surface = 'cs_handoff' "
        "order by sent_at desc limit 1",
        (opportunity_id,),
    )
    return cur.fetchone()


def fetch_pin_notification(cur, opportunity_id):
    cur.execute(
        "select destination, slack_ts, payload from notifications "
        "where opportunity_id = %s and surface = 'channel_pin' "
        "order by sent_at desc limit 1",
        (opportunity_id,),
    )
    return cur.fetchone()


def fetch_update_notification(cur, opportunity_id, version):
    cur.execute(
        "select destination, slack_ts from notifications "
        "where opportunity_id = %s and surface = 'channel_update' and (payload->>'version')::int = %s "
        "order by sent_at desc limit 1",
        (opportunity_id, version),
    )
    return cur.fetchone()


def insert_notification(cur, opportunity_id, surface, destination, slack_ts, payload):
    cur.execute(
        """
        insert into notifications (opportunity_id, surface, destination, slack_ts, payload, sent_at)
        values (%s, %s, %s, %s, %s, now())
        """,
        (opportunity_id, surface, destination, slack_ts, json.dumps(payload)),
    )


def create_canvas(client, channel_id, markdown):
    return client.api_call(
        "conversations.canvases.create",
        json={"channel_id": channel_id, "document_content": {"type": "markdown", "markdown": markdown}},
    )


def edit_canvas(client, canvas_id, markdown):
    return client.api_call(
        "canvases.edit",
        json={
            "canvas_id": canvas_id,
            "changes": [{"operation": "replace", "document_content": {"type": "markdown", "markdown": markdown}}],
        },
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deal", required=True)
    parser.add_argument("--version", type=int, help="required unless --handoff")
    parser.add_argument("--handoff", action="store_true", help="post the CS handoff (prompts/05_handoff.md) instead of a versioned Record update")
    parser.add_argument("--message-file", required=True, dest="message_path", help="hand-written message text, from prompts/04_render.md or prompts/05_handoff.md")
    parser.add_argument("--changed-file", dest="changed_path", help="hand-written 'what changed' text, from prompts/04_render.md — omit if there's nothing to say; not used with --handoff")
    args = parser.parse_args()

    if args.handoff and args.version:
        raise RuntimeError("--handoff and --version are mutually exclusive — the handoff isn't tied to one version")
    if not args.handoff and not args.version:
        raise RuntimeError("--version is required unless --handoff is given")
    if args.handoff and args.changed_path:
        raise RuntimeError("--changed-file isn't used with --handoff — there's no prior handoff state to diff against")

    token = os.environ.get("SLACK_BOT_TOKEN", "")
    if not token or not token.startswith("xoxb"):
        raise RuntimeError("SLACK_BOT_TOKEN missing or malformed in .env")
    client = WebClient(token=token)

    message_text = Path(args.message_path).read_text().strip()
    changed_text = Path(args.changed_path).read_text().strip() if args.changed_path else None

    with get_connection() as conn:
        with conn.cursor() as cur:
            opportunity_id, opportunity_name = fetch_opportunity(cur, args.deal)
            channel_id = channel_id_for(opportunity_name)

            if args.handoff:
                latest_version, latest_status = fetch_latest_version(cur, opportunity_id)
                existing = fetch_handoff_notification(cur, opportunity_id)
                if existing:
                    destination, slack_ts = existing
                    client.chat_update(channel=destination, ts=slack_ts, text=fallback_text(message_text), blocks=build_blocks(message_text))
                    print(f"Updated existing CS handoff message {slack_ts} in place (against v{latest_version}, {latest_status}).")
                    insert_notification(cur, opportunity_id, "cs_handoff", destination, slack_ts, {"version": latest_version})
                else:
                    resp = client.chat_postMessage(channel=channel_id, text=fallback_text(message_text), blocks=build_blocks(message_text))
                    print(f"Posted new CS handoff message {resp['ts']} in {channel_id} (against v{latest_version}, {latest_status}).")
                    insert_notification(cur, opportunity_id, "cs_handoff", channel_id, resp["ts"], {"version": latest_version})
                conn.commit()
                return

            status = fetch_record_status(cur, opportunity_id, args.version)

            if args.version == 1:
                canvas_id = None
                canvas_error = None
                try:
                    resp = create_canvas(client, channel_id, message_text)
                    canvas_id = resp.get("canvas_id")
                except SlackApiError as e:
                    canvas_error = e.response.get("error", str(e))

                if canvas_id:
                    print(f"Created canvas {canvas_id} in {channel_id}.")
                    insert_notification(cur, opportunity_id, "channel_pin", channel_id, None, {"kind": "canvas", "canvas_id": canvas_id})
                else:
                    print(f"Canvas creation failed on this plan ({canvas_error}) — falling back to a pinned message, per the fallback rule. Not fighting it.")
                    resp = client.chat_postMessage(channel=channel_id, text=fallback_text(message_text), blocks=build_blocks(message_text))
                    ts = resp["ts"]
                    client.pins_add(channel=channel_id, timestamp=ts)
                    print(f"Posted and pinned message {ts} in {channel_id}.")
                    insert_notification(cur, opportunity_id, "channel_pin", channel_id, ts, {"kind": "pinned_message"})
                conn.commit()

            else:
                prior = fetch_pin_notification(cur, opportunity_id)
                if prior is None:
                    raise RuntimeError(f"no existing pinned object for {opportunity_name} — run --version 1 first")
                destination, slack_ts, prior_payload = prior
                kind = (prior_payload or {}).get("kind")

                if kind == "canvas":
                    canvas_id = prior_payload["canvas_id"]
                    edit_canvas(client, canvas_id, message_text)
                    print(f"Updated canvas {canvas_id} in place.")
                    insert_notification(cur, opportunity_id, "channel_pin", destination, None, {"kind": "canvas", "canvas_id": canvas_id})
                else:
                    client.chat_update(channel=destination, ts=slack_ts, text=fallback_text(message_text), blocks=build_blocks(message_text))
                    print(f"Updated pinned message {slack_ts} in place.")
                    insert_notification(cur, opportunity_id, "channel_pin", destination, slack_ts, {"kind": "pinned_message"})

                if changed_text is None:
                    print("No --changed-file given — leaving the 'what changed' message alone.")
                else:
                    existing = fetch_update_notification(cur, opportunity_id, args.version)
                    if existing:
                        upd_destination, upd_ts = existing
                        client.chat_update(channel=upd_destination, ts=upd_ts, text=fallback_text(changed_text), blocks=build_blocks(changed_text))
                        print(f"Updated existing 'what changed' message {upd_ts} in place.")
                        insert_notification(cur, opportunity_id, "channel_update", upd_destination, upd_ts, {"version": args.version})
                    else:
                        resp = client.chat_postMessage(channel=channel_id, text=fallback_text(changed_text), blocks=build_blocks(changed_text))
                        print(f"Posted new 'what changed' message {resp['ts']}.")
                        insert_notification(cur, opportunity_id, "channel_update", channel_id, resp["ts"], {"version": args.version})

                conn.commit()


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, SlackApiError) as e:
        print(f"FAIL  {e}", file=sys.stderr)
        sys.exit(1)
