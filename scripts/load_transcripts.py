import re
import sys
from pathlib import Path

from db import get_connection

TRANSCRIPTS_DIR = Path(__file__).resolve().parent.parent / "transcripts"

# Known generation artifact (see docs/transcript-generation-process.md) —
# backslash-escaped markdown that breaks frontmatter parsing if left in.
ESCAPE_RE = re.compile(r"\\([-_\[\]])")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def strip_escaped_markdown(text):
    return ESCAPE_RE.sub(r"\1", text)


def parse_frontmatter(text):
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError("no parseable YAML frontmatter")
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.strip().startswith("-"):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm, text[m.end():]


def call_sequence(call_id):
    m = re.match(r"^[a-z]+-(\d+)$", call_id)
    if not m:
        raise ValueError(f"call_id {call_id!r} doesn't match the expected <slug>-<NN> pattern")
    return int(m.group(1))


def load():
    files = sorted(TRANSCRIPTS_DIR.glob("*.md"))
    if not files:
        print("No transcript files found in transcripts/.")
        return

    loaded = []
    with get_connection() as conn:
        with conn.cursor() as cur:
            for path in files:
                text = strip_escaped_markdown(path.read_text())
                fm, body = parse_frontmatter(text)

                for field in ("opportunity", "call_id", "call_type", "duration_minutes"):
                    if field not in fm:
                        raise ValueError(f"{path.name}: frontmatter missing '{field}'")

                opportunity_name = fm["opportunity"]
                call_id_slug = fm["call_id"]
                seq = call_sequence(call_id_slug)

                cur.execute("select id from opportunities where name = %s", (opportunity_name,))
                row = cur.fetchone()
                if row is None:
                    raise RuntimeError(
                        f"{path.name}: call_id {call_id_slug!r} does not match anything in the "
                        f"database — no opportunity named {opportunity_name!r}"
                    )
                opportunity_id = row[0]

                cur.execute(
                    "select id, call_type, duration_minutes from calls "
                    "where opportunity_id = %s order by occurred_at asc",
                    (opportunity_id,),
                )
                calls = cur.fetchall()
                if seq < 1 or seq > len(calls):
                    raise RuntimeError(
                        f"{path.name}: call_id {call_id_slug!r} does not match anything in the "
                        f"database — implies call #{seq} for {opportunity_name!r}, but that "
                        f"opportunity only has {len(calls)} call(s)"
                    )
                call_row_id, db_call_type, db_duration = calls[seq - 1]

                if db_call_type != fm["call_type"]:
                    print(f"  WARN  {path.name}: call_type mismatch (file: {fm['call_type']!r}, db: {db_call_type!r})")
                try:
                    file_duration = int(fm["duration_minutes"])
                except ValueError:
                    file_duration = None
                if file_duration is not None and file_duration != db_duration:
                    print(f"  WARN  {path.name}: duration_minutes mismatch (file: {file_duration}, db: {db_duration})")

                cur.execute(
                    """
                    insert into transcripts (call_id, content)
                    values (%s, %s)
                    on conflict (call_id) do update set content = excluded.content
                    """,
                    (call_row_id, body.strip()),
                )
                loaded.append(path.name)
                print(f"  ok    {path.name} -> {opportunity_name} call #{seq}")

            cur.execute(
                """
                select o.name, c.call_type, c.occurred_at
                from calls c
                join opportunities o on o.id = c.opportunity_id
                left join transcripts t on t.call_id = c.id
                where t.id is null
                order by o.name, c.occurred_at
                """
            )
            missing = cur.fetchall()

        conn.commit()

    print(f"\nLoaded {len(loaded)} transcript(s).")
    if missing:
        print(f"\n{len(missing)} call(s) in the database with no transcript:")
        for name, call_type, occurred_at in missing:
            print(f"  - {name} ({call_type}, {occurred_at})")
    else:
        print("\nEvery call in the database has a transcript.")


if __name__ == "__main__":
    try:
        load()
    except (ValueError, RuntimeError) as e:
        print(f"\nFAIL  {e}", file=sys.stderr)
        sys.exit(1)
