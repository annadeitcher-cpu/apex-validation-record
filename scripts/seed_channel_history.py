#!/usr/bin/env python3
"""
Seed #deal-meridian-health with a scripted "before Baton" backstory: real
Slack chatter from the weeks leading up to the demo, posted as Marcus Webb
and Elena Restrepo via chat.postMessage's username/icon_emoji override
(requires the chat:write.customize scope). Naomi Fletcher never posts
herself — she's Meridian's employee, not Apex's — her updates only ever
surface secondhand, inside a message from Marcus or Elena.

Usage:
    python scripts/seed_channel_history.py            # post the backstory
    python scripts/seed_channel_history.py --reset    # wipe all prior bot
                                                        # messages in the
                                                        # channel, then stop

This is deliberately the opposite of every other posting script in this
repo: it does no structuring, no summarizing, no field values, nothing
templated from the Record. It's what the channel looked like *before* the
system existed — the record has nothing to add here because nobody in this
conversation is doing the record's job. Real people react, schedule, and
go quiet.

Slack's chat.postMessage has no way to backdate a timestamp for a normal
bot token, so these all land with today's real timestamp regardless of
which "week" a message represents in the story — the elapsed-time feel
comes from the content and the pauses between clusters, not from Slack's
own metadata. Don't rely on the channel's date dividers to sell the
six-week arc; the copy has to do that work.

--reset removes every message this app has ever posted in the channel —
not just this script's backstory, but also anything post_to_slack.py or
escalate.py posted earlier (the pinned Record, "what changed" messages,
the CS handoff, the escalation). It scans the full channel history via
conversations.history (paginated) and deletes anything whose bot_id
matches this app's own bot_id, via chat.delete — a real human message
(including one posted from your own renamed "Daniel Okafor" account) is
never touched, since it won't carry this app's bot_id. If you want the
Record/handoff/escalation back after a reset, that means re-running
post_to_slack.py and escalate.py for this deal, not just this script.
"""

import argparse
import os
import sys
import time

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

# (display name, icon_emoji, message text). Index 0 of each cluster is
# marked below in CLUSTER_STARTS so a pause gets inserted before it —
# that pause is standing in for the silence between real-world clusters,
# since Slack won't let a bot token backdate a timestamp.
CONVERSATION = [
    # Setup before the first call
    ("Marcus Webb (SC)", ":man:", "calendly link is out for the 22nd, they took the 10am slot"),
    ("Marcus Webb (SC)", ":man:", "curtis nam (security) is joining too apparently, sent him the encryption one-pager just in case"),
    ("Elena Restrepo (CSM)", ":woman:", "not mine yet right, just lurking"),
    ("Marcus Webb (SC)", ":man:", "yeah still TV, i'll tag you if/when"),

    # Short exchange after the technical validation call — Curtis's questions
    ("Marcus Webb (SC)", ":man:", "that ran long lol. curtis had like 20 min of questions on tokenization/encryption"),
    ("Elena Restrepo (CSM)", ":woman:", "ooh what specifically did curtis push back on? want to flag it if it's a pattern"),
    ("Marcus Webb (SC)", ":man:", "nothing major tbh, just wanted the details on how it all works, not really objections"),
    ("Marcus Webb (SC)", ":man:", "think it landed ok, he said he was satisfied by the end"),
    ("Marcus Webb (SC)", ":man:", "soc2 going out under nda today"),

    # Naomi's mapping comes back, a couple weeks later
    ("Marcus Webb (SC)", ":man:", "naomi sent the snowflake/teradata mapping over. mostly clean, one gap on the call center system"),
    ("Marcus Webb (SC)", ":man:", "not on their migration roadmap apparently lol, gonna need a connector for that one"),
    ("Marcus Webb (SC)", ":man:", "2nd call today, fine, nothing new really"),

    # Derek's departure surfaces informally
    ("Marcus Webb (SC)", ":man:", "did we know derek left meridian?? just found out from naomi"),
    ("Marcus Webb (SC)", ":man:", "someone named priya raman taking over, she's his old boss i think"),
    ("Marcus Webb (SC)", ":man:", "guess we'll find out more thursday"),

    # Elena asks about timing
    ("Elena Restrepo (CSM)", ":woman:", "saw the thread re: derek lol. rough"),
    ("Elena Restrepo (CSM)", ":woman:", "any sense of timing on this one yet? trying to plan headcount for q"),
    ("Marcus Webb (SC)", ":man:", "tbh not really, still getting the new person up to speed"),
]

CLUSTER_STARTS = {4, 9, 12, 15}  # indices where a new cluster begins (0 excluded, nothing to pause before)
CLUSTER_PAUSE_SECONDS = 4


def get_bot_id(client):
    return client.auth_test()["bot_id"]


def channel_id():
    ch = os.environ.get("SLACK_CHANNEL_MERIDIAN", "")
    if not ch:
        raise RuntimeError("SLACK_CHANNEL_MERIDIAN missing in .env")
    return ch


def seed(client, channel):
    for i, (username, icon, text) in enumerate(CONVERSATION):
        if i in CLUSTER_STARTS:
            time.sleep(CLUSTER_PAUSE_SECONDS)
        resp = client.chat_postMessage(channel=channel, username=username, icon_emoji=icon, text=text)
        print(f"  [{resp['ts']}] {username}: {text}")
    print(f"\nseeded {len(CONVERSATION)} message(s).")


def fetch_all_history(client, channel):
    messages = []
    cursor = None
    while True:
        kwargs = {"channel": channel, "limit": 200}
        if cursor:
            kwargs["cursor"] = cursor
        resp = client.conversations_history(**kwargs)
        messages.extend(resp["messages"])
        cursor = (resp.get("response_metadata") or {}).get("next_cursor")
        if not cursor:
            break
    return messages


def reset(client, channel):
    bot_id = get_bot_id(client)
    messages = fetch_all_history(client, channel)
    to_delete = [m["ts"] for m in messages if m.get("bot_id") == bot_id]
    skipped_human = len(messages) - len(to_delete)

    print(f"found {len(messages)} message(s) total, {len(to_delete)} from this app (bot_id={bot_id}), {skipped_human} left untouched.")

    failures = []
    deleted = 0
    for ts in to_delete:
        try:
            client.chat_delete(channel=channel, ts=ts)
            deleted += 1
        except SlackApiError as e:
            failures.append((ts, e.response.get("error", str(e))))

    print(f"deleted {deleted}/{len(to_delete)} message(s).")

    if failures:
        print("\nFAILED to delete:", file=sys.stderr)
        for ts, err in failures:
            print(f"  ts={ts}: {err}", file=sys.stderr)
        raise RuntimeError(f"{len(failures)} message(s) could not be deleted — see above, nothing else was skipped silently")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="delete every message this app has posted in the channel, then stop (does not reseed)")
    args = parser.parse_args()

    token = os.environ.get("SLACK_BOT_TOKEN", "")
    if not token or not token.startswith("xoxb"):
        raise RuntimeError("SLACK_BOT_TOKEN missing or malformed in .env")
    client = WebClient(token=token)
    channel = channel_id()

    if args.reset:
        reset(client, channel)
    else:
        seed(client, channel)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, SlackApiError) as e:
        print(f"FAIL  {e}", file=sys.stderr)
        sys.exit(1)
