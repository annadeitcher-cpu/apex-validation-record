import uuid

from db import get_connection

# Stable namespace for deterministic ids — re-running with the same `key`
# always produces the same row id, which is what makes this idempotent.
NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "apex.knowledge")


def kid(key):
    return str(uuid.uuid5(NAMESPACE, key))


RELEASE_NOTES = [
    {
        "key": "release_note:streamline-ingest",
        "title": "Streamline Ingest",
        "subject": "Streamline Ingest",
        "tags": ["release", "q1", "ingestion", "logistics", "manufacturing", "retail"],
        "content": """
What shipped: A new ingestion layer for customers with continuous, high-volume
operational or behavioral event data — telematics, POS, plant-floor sensors,
transaction streams. Previously, high-volume sources landed in batch windows,
often fifteen minutes or more; Streamline Ingest brings that down to
sub-minute, typically single-digit seconds, from event arrival to queryable
state in the customer's own warehouse.

Who it's for: Customers whose core pain is "we found out too late" — logistics
and manufacturing ops teams reacting to disruptions after the fact, retail
teams needing near-real-time inventory visibility, any account where a batch
delay directly costs money or trust. Less relevant for low-volume, low-frequency
sources like a weekly HR export — don't lead with this for a customer whose
data doesn't actually move fast.

What problem it solves: Legacy batch pipelines mean decisions get made on
stale data. The gap between "something happened" and "someone found out" is
where cost and risk accumulate — a delayed shipment nobody notices until the
customer calls, a stockout that isn't visible until next-day reporting, a
maintenance issue that's been building for a week before anyone sees the
pattern.

How to position it: Lead with the business cost of the current delay, not the
spec sheet. Ask what the customer's current batch cadence actually is and
what breaks because of it — "sub-minute" only lands once they've named their
own number and felt the gap themselves. Let the SC go deep on event-time
ordering, late-arriving-data windows, and source heterogeneity once the
prospect is engaged; as an AE, stop at "your data is usable within seconds of
happening, not fifteen minutes or a day later."

Common misconception: this is not a warehouse or a BI tool. It's the
ingestion layer underneath a warehouse the customer already owns — never let
a prospect walk away thinking this replaces Snowflake. It feeds it.
""".strip(),
    },
    {
        "key": "release_note:segment-studio-2",
        "title": "Segment Studio 2.0",
        "subject": "Segment Studio 2.0",
        "tags": ["release", "q1", "audience-builder", "marketing", "self-serve"],
        "content": """
What shipped: A visual, no-code audience and segment builder that lets
non-technical users — marketing ops, growth analysts, RevOps — construct and
maintain audience definitions directly against the customer's warehouse. No
SQL, no ticket to a data engineer. Segments can be one-time exports or
continuously refreshing, and they push to standard destinations without a
manual re-upload each time something changes.

Who it's for: Marketing, growth, or ops teams where every segment request
currently routes through a data engineer or analyst, creating a queue and an
iteration tax on every campaign. The clearest fit is any account where the
current process is "someone technical writes a query against a plain-English
description someone non-technical gave them," with a multi-day turnaround per
request.

What problem it solves: The bottleneck was never that the underlying queries
are hard — it's the translation layer between what marketing wants and what
gets built, and the fact that every iteration re-enters that same queue.
Segment Studio 2.0 collapses that loop: the person who knows what they want
builds it directly, against live category and attribute values pulled from
the actual data model, so a segment can't reference something that doesn't
exist in the first place.

How to position it: This is the single easiest before/after story in the
platform. Ask for their current segment-request turnaround (usually measured
in days) and how often a first draft comes back wrong and has to re-enter the
queue. Both collapse toward zero. Don't oversell it as fully zero-maintenance
for engineering, though — initial data modeling, defining what a "customer,"
a "purchase," a "session" actually is, is real work, done once, by someone
technical. What becomes self-serve is everything built on top of that
foundation. Reps who promise "your data team never touches this again" will
get corrected by the SC on the next call — don't set that expectation.
""".strip(),
    },
    {
        "key": "release_note:lineage-graph",
        "title": "Lineage Graph",
        "subject": "Lineage Graph",
        "tags": ["release", "q2", "lineage", "audit", "governance", "compliance", "healthcare", "financial-services"],
        "content": """
What shipped: A traceable, queryable record of how any derived data — a
segment, an audience, an activation, an alert — was built: source fields,
definition-change history with who changed what and when, and, for anything
that triggered a downstream action, exactly what went out, to whom, and
through which channel. Retention is configurable per customer to match actual
compliance requirements rather than a fixed default, and there's a structured
export, not just a UI view — an auditor can work with the output directly.

Who it's for: Any regulated or audit-sensitive customer — healthcare,
financial services, anything touching consent or PII/PHI — plus any customer
who's been burned by "why did this happen and nobody can explain it"
debugging. This is also the single most durable answer to a security or
procurement review's questions about auditability.

What problem it solves: Two distinct failure modes. First, debugging: today,
when a number looks wrong or an alert didn't fire, nobody can quickly tell
"the rule was wrong" from "the data was late" from "the data was wrong" —
Lineage Graph turns that into a lookup instead of a forensic exercise.
Second, audit: "prove this specific person wasn't contacted after they opted
out six months ago" needs to be an answerable question at the individual
record level, not something reconstructed from memory or a summary
dashboard.

How to position it: For a buyer with a governance or compliance stakeholder
in the room, raise this proactively — it's frequently the deciding factor
once security gets involved, not a feature to hold in reserve. For less
regulated buyers, lead with the operational debugging story instead: "why did
this happen" answered in seconds, not a week of Slack archaeology. One
caution — don't conflate this with a SOC 2 report or a penetration test
summary. Lineage Graph proves what the platform did with a customer's data;
it doesn't attest to the platform's own security posture. Those are separate
documents, and a security stakeholder will notice if you blur them together.
""".strip(),
    },
    {
        "key": "release_note:consent-sync",
        "title": "Consent Sync",
        "subject": "Consent Sync",
        "tags": ["release", "q2", "consent", "suppression", "marketing", "healthcare", "cross-channel"],
        "content": """
What shipped: A unified consent and suppression layer that sits above every
outbound channel — email, push, paid social, SMS, call center — so an
opt-out captured on one channel is enforced on all of them, not just the one
it came in through. Consent state is modeled per communication purpose
(marketing versus transactional or treatment-related, for example) rather
than as a single blanket flag, so a marketing opt-out can't accidentally
suppress a message the customer is actually required to send. Propagation is
near-real-time for push-capable destinations and bounded, minutes rather than
hours, for polling-only legacy systems.

Who it's for: Any customer running outreach across more than one channel with
today's suppression lists living separately per platform — this is close to
universal in marketing and growth organizations, and load-bearing in
regulated verticals like healthcare and financial services, where a missed
suppression is a compliance event, not just an annoyance.

What problem it solves: this is the single most common unprompted pain point
we hear in discovery, and the one reps most often fail to connect to an
actual fix. Ask any marketing ops or growth stakeholder how they reconcile
consent and suppression lists across channels today, and you'll usually hear
the same story: manual CSV exports per platform, hours a week of
cross-referencing by hand, and a specific incident — someone who unsubscribed
on email still getting hit with a paid social remarketing ad for the exact
campaign they opted out of. This rarely arrives as a labeled objection. It
shows up as a tangent, a complaint, a "we've been burned by this before"
story, told with real frustration. If a prospect describes this pain, in any
words, connect it to Consent Sync in that same conversation — don't let it
pass as sympathetic small talk.

How to position it: Lead with the manual-reconciliation cost — hours per
week, a real story if they have one — before the compliance angle. The
operational pain is what people volunteer unprompted, and it's the more
relatable entry point even when compliance risk is the bigger reason the deal
ultimately closes. Get specific: how many channels, who owns building the
suppression list today, has there been an incident. Then walk through the
per-purpose consent model so a compliance stakeholder isn't left worrying
that a required message could get blanket-suppressed along with marketing.
""".strip(),
    },
    {
        "key": "release_note:warehouse-native-activation",
        "title": "Warehouse Native Activation",
        "subject": "Warehouse Native Activation",
        "tags": ["release", "q2", "architecture", "activation", "security", "vendor-lock-in"],
        "content": """
What shipped: The activation and orchestration layer — audiences, alerts,
dashboards, downstream pushes — runs directly against the customer's own
warehouse rather than requiring a separate, Apex-managed copy of the data. A
scoped service account, read access against source schemas, narrow write
access to designated output tables or views, handles execution. Nothing is
duplicated into a shadow database the customer has to trust independently of
their own systems.

Who it's for: Every customer, functionally — this is closer to a core
architectural property of the platform than a discrete feature, but it's
worth naming explicitly because it directly answers the two questions every
technical buyer eventually asks: where does our data actually live, and what
happens to it if we ever leave. It matters most, and should be raised
proactively, with security- or governance-heavy buyers and with anyone who's
been burned by a previous vendor's separate data copy going stale or becoming
its own audit liability.

What problem it solves: Vendor lock-in anxiety and audit surface. A separate,
vendor-controlled copy of customer data is both a stale-data risk, two
systems drifting apart, and a governance liability, a second store that's a
second thing to secure, audit, and eventually delete. Running natively
against the customer's own warehouse means the data never leaves their
control, and if the relationship ever ends, there's no separate copy to
extract or fight about.

How to position it: This is the direct answer to "how locked in are we,
really" — a question senior and VP-level buyers ask more often than
individual contributors, and one AEs sometimes fumble by pivoting to a
feature pitch instead of answering the actual question. Answer it directly:
the data stays in their warehouse, and configuration, segment and rule
definitions, has a real, exercised export path. Be honest about the edge of
that claim, though — the export mechanism being technically real does not
automatically mean it satisfies a specific customer's vendor-exit compliance
checklist. That's a legal and contracts question layered on top of a
technical one, and it should be routed there rather than answered casually,
in the room, on the spot.
""".strip(),
    },
]

BATTLECARDS = [
    {
        "key": "battlecard:tracewell",
        "title": "Battlecard: Tracewell",
        "subject": "Tracewell",
        "tags": ["competitor", "battlecard", "tracewell", "pricing", "procurement", "logistics"],
        "content": """
Who they are: A subsidiary of a larger logistics-adjacent holding company,
acquired roughly two years ago. Positions as visibility and tracking tooling
for logistics — shipment and asset tracking dashboards on top of a
customer's existing TMS or WMS, not a data unification platform.

Where they win: Price — they consistently undercut on the headline number,
often meaningfully. Speed-to-pilot — they quote aggressive timelines, we've
seen three weeks quoted, for narrow visibility use cases. Procurement — their
parent company frequently already holds a master services agreement with a
prospect's finance org from an unrelated business line, making paperwork
dramatically faster on the buyer's side. Real, legitimate advantage, not a
myth — treating it as one costs you credibility. They can also point to named
reference customers in freight and distribution.

Where they lose: In every technical evaluation we're aware of, Tracewell does
not attempt real cross-system identity resolution — it's a dashboard layer
bolted onto one system's view, typically a TMS, not a platform unifying WMS,
TMS, telematics, and ERP into one queryable model. If the prospect's actual
problem is "these systems don't talk to each other," Tracewell gives a nicer
view of one piece of it, not a fix. Their quoted pilots are almost always
narrower in scope than ours; ask what a three-week pilot actually includes
before treating it as comparable. No meaningful lineage or audit story, and
not built for regulated-data use cases, where the prospect has real
governance requirements, this is where the gap is largest.

Objection: "Your number's higher than Tracewell's."
Don't pivot to a feature comparison — "our lineage is more mature" — without
first answering the commercial question; that reads as a dodge because it is
one. Instead: ask what's actually in scope for their number, since a narrower
pilot isn't the same purchase as a real unification project; name the
architecture gap by asking whether their evaluation tested identifier-matching
depth the way ours did (usually it wasn't); and if price is genuinely close
once scope is normalized, that's a fair comparison — don't manufacture a gap
that isn't real.

Objection: "Their parent company already has a master agreement with our
finance org, so it's an easier procurement path."
Don't dismiss this as minor — real procurement friction is a real cost, and
waving it away reads as tone-deaf. Instead: acknowledge it as a legitimate
advantage; ask your own deal desk whether an accelerated procurement path
exists for this account before assuming there's nothing to offer, increasingly
there is; and reframe to total friction over the relationship's life, not
just signature friction — a fast signature on a platform that doesn't solve
the underlying problem just moves the real procurement cycle later. Only use
that reframe if it's actually true for this prospect's use case.

Bottom line: a real commercial threat on price and procurement friction, not
a technical one for a prospect whose real problem is unification rather than
visibility. Find out which one applies before deciding how worried to be.
""".strip(),
    },
    {
        "key": "battlecard:corvus",
        "title": "Battlecard: Corvus",
        "subject": "Corvus",
        "tags": ["competitor", "battlecard", "corvus", "visibility", "logistics"],
        "content": """
Who they are: A point solution focused on shipment and asset visibility and
tracking, adjacent to but narrower than Tracewell — typically evaluated as an
add-on to an existing TMS rather than a platform play. Most often shows up as
"we looked at this a while back" — closed, historical vendor history rather
than an active competitive threat.

Where they win: Cheap and fast to stand up for a single, narrow tracking or
visibility use case, with low commitment and minimal setup. If a prospect's
entire stated need is better shipment-tracking dashboards and genuinely
nothing more, Corvus is a reasonable, low-risk choice for that scope, and
it's not our job to talk them out of a fit that's actually fine for what they
need.

Where they lose: No data unification story at all — it's explicitly a
visibility layer sitting on top of one system, not an attempt to solve
cross-system identity or fragmented data. No activation layer, no lineage, no
governance depth, and no real ingestion architecture underneath it. It simply
does not scale to "we have several systems that don't talk to each other" —
that's out of scope for what the product does, not a close call.

Common objection: "We already looked at Corvus, we don't need to re-evaluate
that."
Response: You almost never need to argue against Corvus directly. By the time
we're in a real technical validation, the prospect has usually already
self-selected out of it, because their actual problem, unification, was
never what Corvus does in the first place. Don't manufacture a competitive
threat that isn't live. If it comes up, ask what they were solving for when
they looked at it, confirm that was a narrower need than what's on the table
now, and move on. Treating a closed, historical evaluation as active
competition wastes the prospect's time and signals you weren't listening to
what they actually told you.

Common objection: "Isn't what you're describing basically the same as
Corvus?"
Response: No, and the clearest way to show that rather than assert it is to
ask the prospect to describe what Corvus actually showed them, then map that
against the specific unification problem they described in discovery. The
gap — one system's view versus a genuinely unified model across systems —
usually becomes obvious from their own description without you having to
argue the point.

Bottom line: Corvus is rarely a real head-to-head competitive situation by
the time we're deep in a deal. Confirm it's already been ruled out for scope
reasons rather than assuming that, and don't spend real call time re-litigating
a comparison the prospect has likely already made for themselves.
""".strip(),
    },
    {
        "key": "battlecard:large-incumbent",
        "title": "Battlecard: Large Incumbent Platforms",
        "subject": "Anchorpoint Systems",
        "tags": ["competitor", "battlecard", "incumbent", "enterprise", "procurement", "brand-risk"],
        "content": """
Who they are: A representative profile for the established, well-resourced
enterprise data platform vendors we run into most often — Anchorpoint Systems
here stands in for that category. Broad brand recognition, a large
enterprise sales, CS, and professional-services organization, and a long
feature checklist that covers most of what any RFP asks for on paper. The
default "safe choice" name that shows up in enterprise evaluations regardless
of actual fit, because procurement and legal already have a comfort level
with them.

Where they win: Brand and risk aversion — "nobody gets fired for buying the
big name" is a real force in enterprise procurement, especially with
risk-averse buyers or committees without a strong technical champion in the
room. Broad platform coverage on paper, even where depth varies across
individual capabilities. Existing relationships — many large enterprises
already run some other product from the same vendor, creating an easier
procurement story, structurally similar to the advantage Tracewell gets from
its parent company's master agreement. Larger implementation and CS
organizations, which appeals to buyers nervous about being under-supported.

Where they lose: Price and total cost — enterprise incumbents are almost
always the most expensive option once professional services and
implementation are included, not just license price. Implementation speed —
heavier, longer, more services-dependent rollouts; buyers who need speed to a
first working use case are usually disappointed. Consultative depth — because
they sell breadth, their reps and SCs are frequently generalists relative to
any one specific use case, and prospects who've sat through their demo often
describe it as feature-driven rather than outcome-driven. Product velocity —
larger platforms tend to iterate more slowly, and their own field teams often
can't clearly explain newer capabilities either, the same enablement gap we
have to actively guard against ourselves.

Objection: "Nobody gets in trouble for going with the bigger name."
Response: Don't attack the brand directly — that reads as insecure and
rarely moves anyone. Instead, shift the risk conversation to actual project
risk: a slower, heavier implementation is its own risk, time-to-value,
adoption risk, cost overrun, and it's worth asking the buyer directly what
"safe" means to them. Safe from being blamed for the vendor choice, or safe
as in the project actually works and lands on time. Those are different
kinds of safety, and naming the distinction usually resonates with anyone
who's lived through a slow enterprise rollout before.

Objection: "Their feature checklist covers more than yours."
Response: Ask what, specifically, on that checklist maps to a real, named use
case for this deal, not a hypothetical one. Breadth without depth on the two
or three things that matter to this buyer is weaker than it looks on paper.
Offer a reference customer who chose depth over checklist breadth, if one
exists for this vertical.

Bottom line: a brand and risk-aversion fight, not a capability fight, in most
real evaluations. Don't let it turn into a feature-for-feature shootout —
that plays to their breadth instead of our depth.
""".strip(),
    },
]


def upsert(cur, kind, item):
    cur.execute(
        """
        insert into knowledge (id, kind, title, subject, content, tags)
        values (%s, %s, %s, %s, %s, %s)
        on conflict (id) do update set
            title = excluded.title,
            subject = excluded.subject,
            content = excluded.content,
            tags = excluded.tags
        """,
        (kid(item["key"]), kind, item["title"], item["subject"], item["content"], item["tags"]),
    )


def seed():
    with get_connection() as conn:
        with conn.cursor() as cur:
            for item in RELEASE_NOTES:
                upsert(cur, "release_note", item)
            for item in BATTLECARDS:
                upsert(cur, "battlecard", item)
        conn.commit()
    print(f"seeded {len(RELEASE_NOTES)} release notes, {len(BATTLECARDS)} battlecards")


if __name__ == "__main__":
    seed()
