import os
from datetime import date, datetime, timedelta, timezone

from db import get_connection

# All dates are expressed as day offsets from REFERENCE_DATE so this can be
# rerun the morning of a demo and every days-in-stage number is correct
# again. Offsets preserve the exact intervals from deal-spec.md (originally
# anchored to reference date 2026-09-13) — don't "improve" them.
#
# Defaults to today's date in UTC, not local time: Postgres's now() is UTC,
# and anchoring to local time would drift the days-in-stage math by a day
# whenever local and UTC dates disagree (e.g. evenings in US timezones).
REFERENCE_DATE = date.fromisoformat(
    os.environ.get("REFERENCE_DATE", datetime.now(timezone.utc).date().isoformat())
)


def d(offset):
    return REFERENCE_DATE + timedelta(days=offset)


ACCOUNTS = [
    {"name": "Meridian Health", "industry": "Healthcare", "employee_count": 8000, "region": "AMER"},
    {"name": "Northwind Logistics", "industry": "Logistics & Supply Chain", "employee_count": 3200, "region": "AMER"},
    {"name": "Calibre Financial", "industry": "Financial Services", "employee_count": 12000, "region": "AMER"},
    {"name": "Sightline Retail", "industry": "Retail", "employee_count": 900, "region": "AMER"},
    {"name": "Vantage Media", "industry": "Media & Entertainment", "employee_count": 2400, "region": "AMER"},
    {"name": "Ardent Manufacturing", "industry": "Manufacturing", "employee_count": 5600, "region": "AMER"},
]

OPPORTUNITIES = [
    {
        "account": "Meridian Health",
        "name": "Meridian Health — Customer Data Platform",
        "segment": "Enterprise",
        "stage": "Technical Validation",
        "acv": 310000,
        "close_date": "2026-10-30",
        "stage_offset": -23,
        "ae_name": "Daniel Okafor",
        "sc_name": "Marcus Webb",
        "csm_name": "Elena Restrepo",
        "slack_channel_id": os.environ.get("SLACK_CHANNEL_MERIDIAN") or None,
    },
    {
        "account": "Northwind Logistics",
        "name": "Northwind Logistics — Operational Data Unification",
        "segment": "Enterprise",
        "stage": "Technical Validation",
        "acv": 180000,
        "close_date": "2026-10-15",
        "stage_offset": -14,
        "ae_name": "Rachel Kim",
        "sc_name": "Marcus Webb",
        "csm_name": "Elena Restrepo",
        "slack_channel_id": None,
    },
    {
        "account": "Calibre Financial",
        "name": "Calibre Financial — Enterprise Data Activation",
        "segment": "Enterprise",
        "stage": "Technical Validation",
        "acv": 420000,
        "close_date": "2026-11-20",
        "stage_offset": -9,
        "ae_name": "Tom Brennan",
        "sc_name": "Aditi Sharma",
        "csm_name": "James Whitfield",
        "slack_channel_id": None,
    },
    {
        "account": "Sightline Retail",
        "name": "Sightline Retail — Audience Activation",
        "segment": "Mid-Market",
        "stage": "Technical Validation",
        "acv": 85000,
        "close_date": "2026-09-30",
        "stage_offset": -4,
        "ae_name": "Sofia Marchetti",
        "sc_name": "Aditi Sharma",
        "csm_name": "James Whitfield",
        "slack_channel_id": None,
    },
    {
        "account": "Vantage Media",
        "name": "Vantage Media — Cross-Channel Data Platform",
        "segment": "Enterprise",
        "stage": "Technical Validation",
        "acv": 240000,
        "close_date": "2026-10-31",
        "stage_offset": -11,
        "ae_name": "Daniel Okafor",
        "sc_name": "Aditi Sharma",
        "csm_name": "Elena Restrepo",
        "slack_channel_id": None,
    },
    {
        "account": "Ardent Manufacturing",
        "name": "Ardent Manufacturing — Operational Data Platform",
        "segment": "Enterprise",
        "stage": "Technical Validation",
        "acv": 150000,
        "close_date": "2026-11-05",
        "stage_offset": -4,
        "ae_name": "Greg Lindqvist",
        "sc_name": "Marcus Webb",
        "csm_name": "James Whitfield",
        "slack_channel_id": None,
    },
]

# Each call: opportunity, day offset, type, duration, customer participants
# (name, title), plus the AE/SC from the opportunity attend as internal
# participants.
CALLS = [
    # Meridian — champion departure (Derek in 1,2 / Priya in 3) + objection
    # resurfacing (Curtis call 1 -> Priya call 3, different language).
    {
        "opportunity": "Meridian Health — Customer Data Platform",
        "offset": -23,
        "call_type": "technical_validation",
        "duration_minutes": 88,
        "customer_participants": [
            ("Derek Osei", "Director, Data Engineering"),
            ("Naomi Fletcher", "Staff Data Architect"),
            ("Curtis Nam", "Security Engineer"),
        ],
    },
    {
        "opportunity": "Meridian Health — Customer Data Platform",
        "offset": -12,
        "call_type": "follow_up",
        "duration_minutes": 52,
        "customer_participants": [
            ("Derek Osei", "Director, Data Engineering"),
            ("Naomi Fletcher", "Staff Data Architect"),
        ],
    },
    {
        "opportunity": "Meridian Health — Customer Data Platform",
        "offset": -2,
        "call_type": "technical_validation",
        "duration_minutes": 74,
        "customer_participants": [
            ("Priya Raman", "VP, Data Platform"),
            ("Naomi Fletcher", "Staff Data Architect"),
            ("Curtis Nam", "Security Engineer"),
        ],
    },
    {
        # Meridian — BAA closes, segment owner named, 5/5 exit criteria.
        # Offset is +5 (after REFERENCE_DATE), not negative like every other
        # row here — it's ~1 week after call 3's -2, which is the deal's own
        # most recent call. On a genuine from-scratch reseed this whole
        # Meridian block should get re-anchored (all offsets shifted more
        # negative together, preserving the intervals) so this one lands
        # safely in the past again — see docs/transcript-generation-process.md.
        # Left as +5 rather than "fixed" here since it accurately reflects
        # this call's real position in the story relative to call 3, and
        # silently renumbering it would just hide the re-anchoring need.
        "opportunity": "Meridian Health — Customer Data Platform",
        "offset": 5,
        "call_type": "follow_up",
        "duration_minutes": 34,
        "customer_participants": [
            ("Priya Raman", "VP, Data Platform"),
            ("Naomi Fletcher", "Staff Data Architect"),
        ],
    },
    # Northwind — competitor mention (call 1) + stakeholder added (call 2)
    {
        "opportunity": "Northwind Logistics — Operational Data Unification",
        "offset": -14,
        "call_type": "technical_validation",
        "duration_minutes": 81,
        "customer_participants": [
            ("Kenji Watanabe", "Head of Data Platform"),
            ("Lisa Ferreira", "Senior Analytics Engineer"),
        ],
    },
    {
        "opportunity": "Northwind Logistics — Operational Data Unification",
        "offset": -5,
        "call_type": "follow_up",
        "duration_minutes": 46,
        "customer_participants": [
            ("Kenji Watanabe", "Head of Data Platform"),
            ("Lisa Ferreira", "Senior Analytics Engineer"),
            ("Owen Brady", "Director, RevOps"),
        ],
    },
    # Calibre — unidentified speaker, crosstalk, no next step
    {
        "opportunity": "Calibre Financial — Enterprise Data Activation",
        "offset": -9,
        "call_type": "technical_validation",
        "duration_minutes": 93,
        "customer_participants": [
            ("Yara Haddad", "VP, Enterprise Data"),
            ("Nathan Cole", "Data Governance Lead"),
            ("Unidentified Speaker", None),
        ],
    },
    # Sightline — clean control
    {
        "opportunity": "Sightline Retail — Audience Activation",
        "offset": -4,
        "call_type": "technical_validation",
        "duration_minutes": 58,
        "customer_participants": [
            ("Amara Diallo", "Director, Growth Analytics"),
            ("Paul Renner", "Data Engineer"),
        ],
    },
    # Vantage — unmet product relevance (Consent Sync)
    {
        "opportunity": "Vantage Media — Cross-Channel Data Platform",
        "offset": -11,
        "call_type": "technical_validation",
        "duration_minutes": 76,
        "customer_participants": [
            ("Sung-min Park", "VP, Audience Data"),
            ("Hallie Brooks", "Marketing Ops Manager"),
        ],
    },
    # Ardent — normal call, then the nudge (zero activities)
    {
        "opportunity": "Ardent Manufacturing — Operational Data Platform",
        "offset": -4,
        "call_type": "technical_validation",
        "duration_minutes": 69,
        "customer_participants": [
            ("Viktor Lang", "Director, Operations Data"),
            ("Cheryl Boateng", "Plant Systems Analyst"),
        ],
    },
]

# Ardent deliberately has zero rows here — that absence is the nudge demo.
ACTIVITIES = [
    {"opportunity": "Meridian Health — Customer Data Platform", "offset": -22, "activity_type": "email", "actor": "Daniel Okafor", "subject": "Recap + architecture doc"},
    {"opportunity": "Meridian Health — Customer Data Platform", "offset": -12, "activity_type": "meeting", "actor": "Daniel Okafor", "subject": "Follow-up session"},
    {"opportunity": "Meridian Health — Customer Data Platform", "offset": -11, "activity_type": "email", "actor": "Daniel Okafor", "subject": "Answers on tokenization"},
    {"opportunity": "Meridian Health — Customer Data Platform", "offset": -2, "activity_type": "call", "actor": "Daniel Okafor", "subject": "Second validation session"},
    {"opportunity": "Meridian Health — Customer Data Platform", "offset": 5, "activity_type": "call", "actor": "Daniel Okafor", "subject": "BAA resolution + segment owner named"},
    {"opportunity": "Meridian Health — Customer Data Platform", "offset": 6, "activity_type": "email", "actor": "Daniel Okafor", "subject": "Meeting invite for commercial conversation"},
    {"opportunity": "Northwind Logistics — Operational Data Unification", "offset": -13, "activity_type": "email", "actor": "Rachel Kim", "subject": "Recap and next steps"},
    {"opportunity": "Northwind Logistics — Operational Data Unification", "offset": -4, "activity_type": "email", "actor": "Rachel Kim", "subject": "Integration questions from Owen"},
    {"opportunity": "Calibre Financial — Enterprise Data Activation", "offset": -8, "activity_type": "email", "actor": "Tom Brennan", "subject": "Thanks + materials"},
    {"opportunity": "Sightline Retail — Audience Activation", "offset": -4, "activity_type": "email", "actor": "Sofia Marchetti", "subject": "Same-day recap"},
    {"opportunity": "Sightline Retail — Audience Activation", "offset": -2, "activity_type": "meeting", "actor": "Sofia Marchetti", "subject": "Pricing walkthrough"},
    {"opportunity": "Vantage Media — Cross-Channel Data Platform", "offset": -10, "activity_type": "email", "actor": "Daniel Okafor", "subject": "Follow-up + docs"},
]


def seed():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("truncate table accounts cascade")

            account_ids = {}
            for a in ACCOUNTS:
                cur.execute(
                    "insert into accounts (name, industry, employee_count, region) "
                    "values (%(name)s, %(industry)s, %(employee_count)s, %(region)s) returning id",
                    a,
                )
                account_ids[a["name"]] = cur.fetchone()[0]

            opportunity_ids = {}
            for o in OPPORTUNITIES:
                cur.execute(
                    """
                    insert into opportunities
                        (account_id, name, segment, stage, acv, close_date,
                         stage_entered_at, ae_name, sc_name, csm_name, slack_channel_id)
                    values
                        (%(account_id)s, %(name)s, %(segment)s, %(stage)s, %(acv)s, %(close_date)s,
                         %(stage_entered_at)s, %(ae_name)s, %(sc_name)s, %(csm_name)s, %(slack_channel_id)s)
                    returning id
                    """,
                    {**o, "account_id": account_ids[o["account"]], "stage_entered_at": d(o["stage_offset"])},
                )
                opportunity_ids[o["name"]] = cur.fetchone()[0]

            for c in CALLS:
                opp = next(o for o in OPPORTUNITIES if o["name"] == c["opportunity"])
                cur.execute(
                    """
                    insert into calls (opportunity_id, call_type, occurred_at, duration_minutes)
                    values (%s, %s, %s, %s)
                    returning id
                    """,
                    (opportunity_ids[c["opportunity"]], c["call_type"], d(c["offset"]), c["duration_minutes"]),
                )
                call_id = cur.fetchone()[0]

                for name, title in c["customer_participants"]:
                    cur.execute(
                        "insert into participants (call_id, name, title, is_internal) values (%s, %s, %s, false)",
                        (call_id, name, title),
                    )

                cur.execute(
                    "insert into participants (call_id, name, title, is_internal) values (%s, %s, %s, true)",
                    (call_id, opp["ae_name"], "Account Executive"),
                )
                cur.execute(
                    "insert into participants (call_id, name, title, is_internal) values (%s, %s, %s, true)",
                    (call_id, opp["sc_name"], "Solutions Consultant"),
                )

            for act in ACTIVITIES:
                cur.execute(
                    "insert into activities (opportunity_id, activity_type, actor, occurred_at, subject) "
                    "values (%s, %s, %s, %s, %s)",
                    (
                        opportunity_ids[act["opportunity"]],
                        act["activity_type"],
                        act["actor"],
                        d(act["offset"]),
                        act["subject"],
                    ),
                )

        conn.commit()


if __name__ == "__main__":
    seed()
    print(f"seeded against REFERENCE_DATE={REFERENCE_DATE.isoformat()}: "
          f"6 accounts, 6 opportunities, 9 calls, activities (Ardent: zero)")
