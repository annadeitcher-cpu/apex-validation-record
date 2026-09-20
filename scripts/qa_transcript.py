#!/usr/bin/env python3
"""
QA check for generated transcripts.

Usage:
    python scripts/qa_transcript.py transcripts/meridian-03.md
    python scripts/qa_transcript.py transcripts/*.md

Catches the mechanical problems so you can spend your reading attention
on the things only a human can judge (see the manual checklist below).
"""

import re
import sys
from pathlib import Path

MONTHS = r"january|february|march|april|june|july|august|september|october|november|december"
HEDGE_MARKERS = [
    "i guess", "i mean", "sort of", "kind of", "maybe", "i don't know",
    "honestly", "i'm not sure", "i wonder", "one thing i'm wondering",
]
INTERRUPT_MARKERS = ["—", "sorry", "go ahead", "wait", "actually, ", "no, "]

# Expected word-count band by call duration. Roughly 95 words/minute of
# transcribed conversation, with generous tolerance.
def expected_words(duration_minutes):
    return int(duration_minutes * 80), int(duration_minutes * 125)


def parse_frontmatter(text):
    """Returns (frontmatter_dict, body) or (None, text) if no frontmatter."""
    stripped = text.replace("\\", "")
    m = re.match(r"\s*---\s*\n(.*?)\n\s*---\s*\n", stripped, re.DOTALL)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.strip().startswith("-"):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm, stripped[m.end():]


def speaker_turns(body):
    """Returns list of (speaker, text) in order."""
    turns = []
    for line in body.splitlines():
        m = re.match(r"^([A-Z][A-Z\s\.'-]{1,30}):\s*(.*)$", line)
        if m:
            turns.append((m.group(1).strip(), m.group(2)))
    return turns


def check(path):
    text = Path(path).read_text()
    issues, warnings, notes = [], [], []

    # --- escaping ------------------------------------------------------
    if re.search(r"\\[-_\[\]]", text):
        issues.append(
            "Escaped markdown present (\\-, \\_, \\[). Will break frontmatter "
            "parsing. Strip before loading to the database."
        )

    # --- frontmatter ---------------------------------------------------
    fm, body = parse_frontmatter(text)
    if fm is None:
        issues.append("No parseable YAML frontmatter.")
        fm, body = {}, text
    else:
        for field in ("opportunity", "call_id", "call_type", "day_offset", "duration_minutes"):
            if field not in fm:
                issues.append(f"Frontmatter missing: {field}")

    # --- length --------------------------------------------------------
    words = len(body.split())
    if "duration_minutes" in fm:
        try:
            dur = int(re.sub(r"\D", "", fm["duration_minutes"]))
            lo, hi = expected_words(dur)
            if words < lo:
                issues.append(f"{words} words for a {dur}-min call — thin (expected {lo}–{hi}).")
            elif words > hi:
                warnings.append(f"{words} words for a {dur}-min call — long (expected {lo}–{hi}).")
            else:
                notes.append(f"{words} words for {dur} min — in band.")
        except ValueError:
            warnings.append("Couldn't parse duration_minutes.")

    # --- absolute dates ------------------------------------------------
    date_hits = re.findall(rf"\b({MONTHS}|20\d\d|Q[1-4]\b)", body, re.IGNORECASE)
    if date_hits:
        issues.append(f"Absolute date references found: {sorted(set(date_hits))[:5]}. "
                      "Breaks re-anchoring — use relative language.")

    # --- turn structure ------------------------------------------------
    turns = speaker_turns(body)
    if not turns:
        issues.append("No speaker turns detected — check the SPEAKER: format.")
    else:
        notes.append(f"{len(turns)} speaker turns.")
        consecutive = [
            (i, turns[i][0]) for i in range(1, len(turns))
            if turns[i][0] == turns[i - 1][0]
        ]
        if consecutive:
            warnings.append(
                f"{len(consecutive)} consecutive same-speaker turns "
                f"(first: {consecutive[0][1]}, turn {consecutive[0][0]}). "
                "Known generation artifact — can confuse speaker attribution."
            )

        # speaker balance
        counts = {}
        for s, _ in turns:
            counts[s] = counts.get(s, 0) + 1
        quiet = [s for s, c in counts.items() if c < len(turns) * 0.05]
        if quiet:
            warnings.append(f"Near-silent participants: {quiet}. Intentional?")

    # --- texture -------------------------------------------------------
    lower = body.lower()
    hedges = sum(lower.count(h) for h in HEDGE_MARKERS)
    if hedges < 15:
        warnings.append(f"Only {hedges} hedge markers — dialogue may read too clean.")
    else:
        notes.append(f"{hedges} hedge markers.")

    interrupts = sum(lower.count(m.lower()) for m in INTERRUPT_MARKERS)
    if interrupts < 20:
        warnings.append(f"Only {interrupts} interruption markers — may read as minutes, not a recording.")
    else:
        notes.append(f"{interrupts} interruption markers.")

    # --- report --------------------------------------------------------
    print(f"\n{'=' * 70}\n{path}\n{'=' * 70}")
    for i in issues:
        print(f"  FAIL   {i}")
    for w in warnings:
        print(f"  WARN   {w}")
    for n in notes:
        print(f"  ok     {n}")
    if not issues:
        print("\n  No blocking issues. Now read it — see the manual checklist.")
    return len(issues)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    total = sum(check(p) for p in sys.argv[1:])
    sys.exit(1 if total else 0)
