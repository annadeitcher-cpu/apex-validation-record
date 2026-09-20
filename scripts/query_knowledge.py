#!/usr/bin/env python3
"""
Retrieve knowledge-base rows matching a comma-separated list of terms.

Usage:
    python scripts/query_knowledge.py --terms "Tracewell,consent reconciliation"

Run this between pass 1 and pass 2, with terms pulled from pass 1's
competitor mentions and stated customer needs. Matches only against
knowledge.subject and knowledge.tags — never content, and never returns
the whole table. Prints nothing (an explicit "no match" note) rather than
everything when nothing matches; a prompt grounded in "everything" isn't
grounded in anything.
"""

import argparse
import json
import re
import sys

from db import get_connection

STOPWORDS = {
    "about", "after", "again", "their", "there", "which", "would", "could",
    "should", "where", "really", "actually", "because", "something",
    "things", "think", "thing", "these", "those", "being", "still",
    "before", "other", "every", "gonna", "wanna", "right", "point",
    "customer", "customers", "prospect",
}


def tag_tokens(term):
    # Preserve internal hyphens so compound tags like "self-serve" or
    # "audience-builder" can match — splitting on them would turn a term
    # like "self-serve" into "self"/"serve", neither of which equals the
    # actual tag string.
    words = re.findall(r"[a-zA-Z]+(?:-[a-zA-Z]+)*", term.lower())
    return [w for w in words if len(w.replace("-", "")) >= 4 and w not in STOPWORDS]


def query_knowledge(cur, terms):
    terms = [t.strip() for t in terms if t.strip()]
    if not terms:
        return []

    subjects_lower = [t.lower() for t in terms]
    tokens = sorted({tok for t in terms for tok in tag_tokens(t)})

    cur.execute(
        """
        select kind, title, subject, content, tags
        from knowledge
        where (%(subjects)s::text[] <> '{}' and lower(subject) = any(%(subjects)s))
           or (%(tokens)s::text[] <> '{}' and tags && %(tokens)s)
        order by kind, subject
        """,
        {"subjects": subjects_lower, "tokens": tokens},
    )
    return cur.fetchall()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", required=True, help="comma-separated terms")
    args = parser.parse_args()
    terms = args.terms.split(",")

    with get_connection() as conn:
        with conn.cursor() as cur:
            rows = query_knowledge(cur, terms)

    if not rows:
        print("(no matching knowledge rows)")
        return

    for kind, title, subject, content, tags in rows:
        print("=" * 70)
        print(f"kind: {kind}    subject: {subject}    title: {title}")
        print(f"tags: {', '.join(tags or [])}")
        print("-" * 70)
        print(content)
        print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"FAIL  {e}", file=sys.stderr)
        sys.exit(1)
