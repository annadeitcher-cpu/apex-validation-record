# Apex — Deal Specification (seed data)

Six opportunities. Reference date: **2026-09-13**. All dates anchored to it.

Every detail below that looks arbitrary is load-bearing for a demo beat. Don't "improve" the dates or drop participants — the accrual arc and the nudge both read directly off this data.

---

## Apex product releases (last two quarters)

Needed for the product-relevance field. Keep these fictional; the Braze parallel is something you say out loud, not something you hardcode.

| Release | Shipped | What it does |
|---|---|---|
| Streamline Ingest | Q1 | Sub-minute ingestion for high-volume event streams |
| Segment Studio 2.0 | Q1 | Self-serve audience builder, no SQL required |
| Lineage Graph | Q2 | Column-level lineage across ingestion and activation |
| **Consent Sync** | Q2 | Propagates consent and suppression state to all downstream destinations |
| Warehouse Native Activation | Q2 | Activate directly from the customer's warehouse without copying data |

---

## 1. Meridian Health — THE DEMO DEAL

**Account:** Meridian Health · Healthcare · 8,000 employees · AMER
**Opportunity:** Meridian Health — Customer Data Platform · Enterprise · **$310,000** · Technical Validation
**stage_entered_at:** `2026-08-21` (23 days — matches the Q3 average, makes the problem visible in the data)
**close_date:** `2026-10-30`
**Internal:** AE Daniel Okafor · SC Marcus Webb · CSM Elena Restrepo
**Slack:** real channel ID

### Calls

| # | Date | Type | Duration | Customer participants |
|---|---|---|---|---|
| 1 | 2026-08-21 | technical_validation | 88 | Derek Osei (Director, Data Engineering) · Naomi Fletcher (Staff Data Architect) · Curtis Nam (Security Engineer) |
| 2 | 2026-09-01 | follow_up | 52 | Derek Osei · Naomi Fletcher |
| 3 | 2026-09-11 | technical_validation | 74 | **Priya Raman (VP, Data Platform)** · Naomi Fletcher · Curtis Nam |

Daniel Okafor and Marcus Webb attend all three.

### The two plants

**Champion departure.** Derek Osei appears in calls 1 and 2 and is absent from call 3. Priya Raman appears only in call 3. The `participants` table encodes this structurally — but the *transcript* must independently support it. Someone in call 3 should reference Derek having left, obliquely, the way people actually do. The system should infer champion change from behavior and be confirmable against the table, not read it off the table.

**Objection resurfacing.** Call 1: Curtis Nam raises a concern about PII handling in the normalization layer. Marcus Webb walks through field-level encryption and tokenization. **Curtis explicitly accepts** — this is what makes it legitimately `resolved`, not `partially_resolved`. Call 3: Priya Raman reopens the same underlying concern in **entirely different language** — she asks what happens to protected health information sitting in the staging layer before normalization runs, and raises their BAA posture.

> This is the single most important detail in the seed data. If call 3 reuses call 1's phrasing, you've built a keyword matcher and your best demo beat is theater. Different words, same underlying concern, escalated because a new senior stakeholder is asking.

### Activities

| Date | Type | Actor | Subject |
|---|---|---|---|
| 2026-08-22 | email | Daniel Okafor | Recap + architecture doc |
| 2026-09-01 | meeting | Daniel Okafor | Follow-up session |
| 2026-09-02 | email | Daniel Okafor | Answers on tokenization |
| 2026-09-11 | call | Daniel Okafor | Second validation session |

---

## 2. Northwind Logistics — competitive pressure

**Account:** Northwind Logistics · Logistics & Supply Chain · 3,200 · AMER
**Opportunity:** Northwind Logistics — Operational Data Unification · Enterprise · **$180,000** · Technical Validation
**stage_entered_at:** `2026-08-30` (14 days) · **close_date:** `2026-10-15`
**Internal:** AE Rachel Kim · SC Marcus Webb · CSM Elena Restrepo

| # | Date | Type | Duration | Customer participants |
|---|---|---|---|---|
| 1 | 2026-08-30 | technical_validation | 81 | Kenji Watanabe (Head of Data Platform) · Lisa Ferreira (Senior Analytics Engineer) |
| 2 | 2026-09-08 | follow_up | 46 | Kenji Watanabe · Lisa Ferreira · **Owen Brady (Director, RevOps)** |

**The plant, call 1:** in the middle third, Kenji mentions **Corvus** casually — a past, closed evaluation of a narrower TMS-reporting add-on, brought up in passing while answering a question about lineage/debugging, not as a "how are you different" question. He explicitly frames it as old vendor history he doesn't want to get into. This should **not** read as live competitive risk — it's a false-positive trap for `competitor_introduced`, not a real one.

**The plant, call 2:** Owen Brady (Director, RevOps) joins for the first time and immediately raises real, active competitive pressure — Northwind is genuinely evaluating **Tracewell** in parallel. This is materially different from the Corvus mention: Tracewell is live, named with specifics (a lower price, a stated three-week pilot timeline, and an existing master services agreement between Northwind's finance org and Tracewell's parent company that eases procurement), and it is **not resolved by end of call**. Rachel handles it imperfectly — she initially pivots to a technical/value argument when Owen is asking a commercial question, gets called on it, and course-corrects. She commits to coming back with real pricing, a procurement-friction answer, and a sharper technical comparison, but none of that lands on this call. This should register as a `competitor_introduced` event with `materiality: material`, and the record's `next_step` for this deal should reflect real, unresolved commercial risk, not a closed loop.

Owen's arrival is *also* a `stakeholder_added` event (minor on its own), but it's the competitive content of what he brings that matters here, not just his presence — don't let the two events collapse into one under-weighted signal.

**Activities:** email `2026-08-31` (Rachel Kim, "Recap and next steps"), email `2026-09-09` (Rachel Kim, "Integration questions from Owen").

---

## 3. Calibre Financial — the messy one

**Account:** Calibre Financial · Financial Services · 12,000 · AMER
**Opportunity:** Calibre Financial — Enterprise Data Activation · Enterprise · **$420,000** · Technical Validation
**stage_entered_at:** `2026-09-04` (9 days) · **close_date:** `2026-11-20`
**Internal:** AE Tom Brennan · SC Aditi Sharma · CSM James Whitfield

| # | Date | Type | Duration | Customer participants |
|---|---|---|---|---|
| 1 | 2026-09-04 | technical_validation | 93 | Yara Haddad (VP, Enterprise Data) · Nathan Cole (Data Governance Lead) · **one unidentified speaker** |

**The plants:**
- A fourth voice who **never introduces themselves.** Seed them in `participants` as `Unidentified Speaker` with a null title. The system should surface them as a stakeholder with `role_inference: unknown` and `confidence: low` rather than guessing.
- **Genuine crosstalk** — two people talking over each other at least twice, with the transcript reflecting it.
- **No next step agreed.** The call ends with Yara saying something like *"we'll probably want to loop in Renata before we go much further"* — no owner, no date, no commitment. `next_step.present` must come back `false`. A careful human would also hesitate here; that's the bar.

**Activities:** one email 2026-09-05 (Tom Brennan, "Thanks + materials"). Deliberate — Calibre should *not* trigger the nudge, so only Ardent does.

---

## 4. Sightline Retail — the clean control

**Account:** Sightline Retail · Retail · 900 · AMER
**Opportunity:** Sightline Retail — Audience Activation · **Mid-Market** · **$85,000** · Technical Validation
**stage_entered_at:** `2026-09-09` (4 days — the under-7-day, 68% win-rate profile) · **close_date:** `2026-09-30`
**Internal:** AE Sofia Marchetti · SC Aditi Sharma · CSM James Whitfield

| # | Date | Type | Duration | Customer participants |
|---|---|---|---|---|
| 1 | 2026-09-09 | technical_validation | 58 | Amara Diallo (Director, Growth Analytics) · Paul Renner (Data Engineer) |

**The plant:** none. This is the control — textbook execution, clear next step with an owner and a date, objections raised and cleanly resolved, economic buyer identified. It exists so you can show the Record on a healthy deal and so your eval set isn't all edge cases. Generate it **first**; it calibrates length and texture for everything else.

**Activities:** email 2026-09-09 (Sofia Marchetti, same-day recap), meeting 2026-09-11 (Sofia Marchetti, "Pricing walkthrough").

---

## 5. Vantage Media — unmet product relevance

**Account:** Vantage Media · Media & Entertainment · 2,400 · AMER
**Opportunity:** Vantage Media — Cross-Channel Data Platform · Enterprise · **$240,000** · Technical Validation
**stage_entered_at:** `2026-09-02` (11 days) · **close_date:** `2026-10-31`
**Internal:** AE Daniel Okafor · SC Aditi Sharma · CSM Elena Restrepo

| # | Date | Type | Duration | Customer participants |
|---|---|---|---|---|
| 1 | 2026-09-02 | technical_validation | 76 | Sung-min Park (VP, Audience Data) · Hallie Brooks (Marketing Ops Manager) |

**The plant:** Hallie describes, at some length and with visible frustration, manually reconciling consent and suppression lists across email, push, and paid social — a recurring multi-hour task. **Nobody on the Apex side connects it to Consent Sync.** The AE and SC move past it. The system should surface it under `product_relevance`, which is the release-velocity signal solved at the moment it converts.

**Activities:** email 2026-09-03 (Daniel Okafor, "Follow-up + docs").

---

## 6. Ardent Manufacturing — the nudge

**Account:** Ardent Manufacturing · Manufacturing · 5,600 · AMER
**Opportunity:** Ardent Manufacturing — Operational Data Platform · Enterprise · **$150,000** · Technical Validation
**stage_entered_at:** `2026-09-09` (4 days) · **close_date:** `2026-11-05`
**Internal:** AE Greg Lindqvist · SC Marcus Webb · CSM James Whitfield

| # | Date | Type | Duration | Customer participants |
|---|---|---|---|---|
| 1 | 2026-09-09 | technical_validation | 69 | Viktor Lang (Director, Operations Data) · Cheryl Boateng (Plant Systems Analyst) |

**The plant: zero activity rows.** The call went fine — a perfectly normal validation, next step even loosely discussed — and then nothing. Four days of silence.

> **Ardent must have no rows in `activities`.** That absence is the entire nudge demo. Verify it explicitly after seeding.

---

## Post-seed verification

```sql
select o.name, o.segment, o.acv, o.stage,
       date_part('day', now() - o.stage_entered_at)::int as days_in_stage,
       count(distinct c.id) as calls,
       max(a.occurred_at) as last_activity
from opportunities o
left join calls c on c.opportunity_id = o.id
left join activities a on a.opportunity_id = o.id
group by o.id, o.name, o.segment, o.acv, o.stage, o.stage_entered_at
order by o.name;
```

Expect:

| Deal | days_in_stage | calls | last_activity |
|---|---|---|---|
| Ardent Manufacturing | 4 | 1 | **NULL** |
| Calibre Financial | 9 | 1 | 2026-09-05 |
| Meridian Health | 23 | 3 | 2026-09-11 |
| Northwind Logistics | 14 | 2 | 2026-09-09 |
| Sightline Retail | 4 | 1 | 2026-09-11 |
| Vantage Media | 11 | 1 | 2026-09-03 |

If Ardent's `last_activity` isn't null, the nudge won't fire and you'll lose a demo beat.

---

## Transcript generation order

1. **Sightline** — clean control, calibrates everything
2. **Meridian 1 → 2 → 3** — in sequence, each with prior transcripts as context so continuity holds
3. **Northwind 1 → 2**
4. **Vantage**
5. **Ardent**
6. **Calibre** — last, once you know what "normal" looks like in your own corpus

Nine transcripts total. 6,000–9,000 words each. Read the first one in full before generating any others.
