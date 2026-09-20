"""
Turn hand-written, `---`-delimited Slack mrkdwn text into Block Kit blocks:
one section block per chunk, a divider block between each pair. This is the
shared convention behind the message-type header + section-divider format
in prompts/04_render.md, prompts/05_handoff.md, and scripts/escalate.py.

Used by scripts/post_to_slack.py and scripts/escalate.py for every
chat.postMessage / chat.update call. Not used for canvases — a Canvas
document is markdown, not Block Kit, and a bare `---` line already renders
there as a horizontal rule, so canvas content passes through unchanged.
"""

SECTION_TEXT_LIMIT = 2900  # Slack's real per-block cap is 3000 — leave margin


def build_blocks(message_text):
    lines = message_text.strip("\n").split("\n")
    chunks = [[]]
    for line in lines:
        if line.strip() == "---":
            chunks.append([])
        else:
            chunks[-1].append(line)
    parts = ["\n".join(c).strip() for c in chunks if "\n".join(c).strip()]

    if not parts:
        raise RuntimeError("message has no content after splitting on '---' dividers")

    blocks = []
    for i, part in enumerate(parts):
        if len(part) > SECTION_TEXT_LIMIT:
            raise RuntimeError(
                f"section {i + 1} is {len(part)} chars, over the {SECTION_TEXT_LIMIT}-char "
                f"Block Kit section limit — split or trim it, don't let Slack silently reject it"
            )
        if i > 0:
            blocks.append({"type": "divider"})
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": part}})
    return blocks


def fallback_text(message_text):
    """Plain-text fallback for notifications/search — same content, '---' markers dropped."""
    return "\n".join(line for line in message_text.split("\n") if line.strip() != "---").strip()
