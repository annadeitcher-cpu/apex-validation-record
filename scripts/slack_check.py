import os
import sys
import time

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

token = os.environ.get("SLACK_BOT_TOKEN", "")
channel = os.environ.get("SLACK_CHANNEL_MERIDIAN", "")

if not token or not token.startswith("xoxb"):
    print("SLACK_BOT_TOKEN: missing or malformed (expected non-empty, starts with 'xoxb')")
    sys.exit(1)
print("SLACK_BOT_TOKEN: loaded (non-empty, starts with 'xoxb')")

if not channel:
    print("SLACK_CHANNEL_MERIDIAN: missing")
    sys.exit(1)
print(f"SLACK_CHANNEL_MERIDIAN: {channel}")

client = WebClient(token=token)


def fail(step, e):
    print(f"FAILED at {step}: {e}")
    sys.exit(1)


# 1. Post a test message
try:
    resp = client.chat_postMessage(channel=channel, text="slack_check: connection test")
    ts = resp["ts"]
    print(f"chat_postMessage: ok, ts={ts}")
except SlackApiError as e:
    fail("chat_postMessage", e.response["error"])

# 2. Pin it
try:
    client.pins_add(channel=channel, timestamp=ts)
    print(f"pins_add: ok, ts={ts}")
except SlackApiError as e:
    fail("pins_add", e.response["error"])

# 3. Sleep, then update the same message
time.sleep(2)

try:
    client.chat_update(channel=channel, ts=ts, text="slack_check: connection test (updated)")
    print(f"chat_update: ok, ts={ts}")
except SlackApiError as e:
    fail("chat_update", e.response["error"])

print(f"done, ts={ts}")
