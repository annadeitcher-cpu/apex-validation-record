"""
Seed real Apex historical baseline metrics into `baselines`, per
docs/dashboard-build-spec.md — this is genuine case-packet data, not
synthetic. Every number here is what makes the baseline column on the
dashboard's Panel B charts real, while the treatment/holdout columns
wait for actual rollout volume.

Idempotent: deterministic uuid5 ids keyed on (metric, segment, period),
upsert on conflict. Never truncates — additive only, same convention as
scripts/seed_knowledge.py. Safe to re-run any time.

Usage:
    python scripts/seed_baselines.py
"""

import uuid

from db import get_connection

NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "apex.baselines")


def bid(key):
    return str(uuid.uuid5(NAMESPACE, key))


# Stage duration by quarter, in days. Three values per stage are Q1/Q2/Q3
# in order — Q3 is the most recent quarter and is the baseline column
# Panel B chart 1 compares treatment against.
STAGE_DURATION = {
    "Discovery": [11, 12, 11],
    "Technical Validation": [12, 14, 23],
    "Commercial Negotiation": [18, 17, 19],
    "Legal/Close": [9, 10, 11],
}

# Win rate by days spent in Technical Validation.
WIN_RATE_BY_TV_DAYS = [
    ("<7 days", 68),
    ("7-14 days", 41),
    (">14 days", 22),
]

# CS time to first value (days), by deal cycle-length bucket.
CS_TTFV = [
    ("<60 days", 31),
    ("60-90 days", 47),
    (">90 days", 68),
]
CS_TTFV_CORRELATION = 0.71  # cycle length vs. time-to-first-value, r

# Post-demo touches in the 14 days following a technical validation call,
# by AE performance quartile.
POST_DEMO_TOUCHES = [
    ("top", 2.3),
    ("middle", 1.1),
    ("bottom", 0.7),
]

SC_SUMMARY_COMPLETION_PCT = 60  # "~60%" in the packet — approximate, not exact


def upsert(cur, metric, segment, metric_period, value, unit, note=None):
    key = f"{metric}:{segment}:{metric_period}"
    cur.execute(
        """
        insert into baselines (id, metric, segment, metric_period, value, unit, note)
        values (%s, %s, %s, %s, %s, %s, %s)
        on conflict (id) do update set
            value = excluded.value,
            unit = excluded.unit,
            note = excluded.note
        """,
        (bid(key), metric, segment, metric_period, value, unit, note),
    )


def seed():
    with get_connection() as conn:
        with conn.cursor() as cur:
            for stage, values in STAGE_DURATION.items():
                for i, days in enumerate(values, start=1):
                    period = f"Q{i}"
                    note = "Baseline quarter (most recent)." if i == len(values) else None
                    upsert(cur, "stage_duration", stage, period, days, "days", note)

            for bucket, pct in WIN_RATE_BY_TV_DAYS:
                upsert(cur, "win_rate_by_tv_days", bucket, None, pct, "pct")

            for bucket, days in CS_TTFV:
                upsert(cur, "cs_ttfv", bucket, None, days, "days")
            upsert(
                cur, "cs_ttfv_correlation", None, None, CS_TTFV_CORRELATION, "ratio",
                note="Correlation between cycle length and time to first value.",
            )

            for quartile, touches in POST_DEMO_TOUCHES:
                upsert(cur, "post_demo_touches", quartile, None, touches, "count")

            upsert(
                cur, "sc_summary_completion", None, None, SC_SUMMARY_COMPLETION_PCT, "pct",
                note="Stated as approximate (~60%) in the source packet.",
            )
        conn.commit()

    print("Seeded baselines: 12 stage_duration rows, 3 win_rate_by_tv_days, "
          "3 cs_ttfv + 1 correlation, 3 post_demo_touches, 1 sc_summary_completion.")


if __name__ == "__main__":
    seed()
