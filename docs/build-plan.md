# Apex Assessment — Build & Presentation Plan
**Role:** Applied AI Architect, GTM (Braze)
**Deliverable:** Technical Validation Record — an accruing deal object with four consumers, delivered in Slack

---

## 1. The Problem

**Technical Validation is the only stage that moved.** 12 → 14 → 23 avg days across three quarters. Discovery (11/12/11), Commercial Negotiation (18/17/19), and Legal (9/10/11) all held flat. A 64% expansion in one quarter, isolated to one stage.

**It is also the stage most correlated with winning.** Win rate by time in Technical Validation: 68% under 7 days, 41% at 7–14, 22% beyond 14. No other stage in the packet has a published win-rate relationship.

**The Gong data names the behavior.** Top-quartile AEs log 2.3 touches in the 14 days post-demo. Bottom quartile: 0.7. This is not a skill mystery. It is a measurable behavioral gap at a single identifiable moment.

**It compounds downstream.** Sales cycle length vs. time-to-first-customer-value correlates at r=0.71. Deals closing under 60 days reach value in 31; deals over 90 days take 68. Every day lost in validation costs roughly a day of onboarding drag.

**Six qualitative signals converge on the same seam:**

| Source | Signal |
|---|---|
| AE, Enterprise NY | No playbook for the post-technical-win moment |
| Sales Manager, Enterprise | Best reps schedule next steps before leaving the room; average reps wait |
| SC, Enterprise | Hands back to AE and never hears what happened |
| CS Manager | Longest-closing deals are the hardest onboards — expectations drift, champion changes |
| Sales Enablement Lead | Post-demo guide exists in Confluence, nobody uses it |
| Current State doc | SC summary completes ~60% of the time; nothing systematic flows to post-sales |

**Structural facts from the workflow description:** no defined playbook for the Technical Validation → Commercial Negotiation transition, and no systematic capture of objections, resolutions, open concerns, or agreed integration patterns flowing to post-sales at handoff.

### Why not the other candidate problems

**Differentiation** (Chicago AE, both SCs). Real and painful, but it's a content and positioning problem that surfaces at every stage. Hard to scope, hard to attribute impact, and PMM owns half the solution. *I am not dropping it — see §3, competitive capture.*

**Product release velocity** (SF AE, Regional Sales Manager, MM SC). Same shape. Enablement lag is a content-supply problem. *Also folded in — see §3, product relevance.*

**BDR sequencing tool breakage.** A vendor/IT problem wearing an AI costume. And BDR-sourced pipeline ($4.2M / $5.1M / $4.8M) is noise, not a trend — no decline to solve.

**Buying committee blindness** (MM AE). Real, but it's a *field* of the thing I'm building, not a system on its own.

**The line to use in the room:** "Three of these are content problems and one is a procurement problem. One is a workflow problem with a measurable behavioral gap at a specific moment, and it's the one the data says costs the most. I solved that one and pulled the best parts of the others into it."

---

## 2. The Solution in One Sentence

*When a technical validation call ends, a structured Validation Record is created for the opportunity and posted to the deal's Slack channel. It updates in place as the deal progresses. CS inherits a current record instead of a stale one. If an action item goes 72 hours past due, its owner gets a private reminder — and a public one at seven days if that goes unaddressed.*

**The architectural claim that makes this a system and not a summarizer:** the Record is scoped to the *opportunity*, not the call. It accrues. Version 1 from the technical validation and version 3 from six weeks later are different objects, and the diff between them is the deal's actual story.

---

## 3. The Validation Record — Field Spec

This is the core object. Everything else is a rendering of it.

```json
{
  "record_id": "uuid",
  "opportunity_id": "uuid",
  "version": 3,
  "source_call_ids": ["uuid", "uuid", "uuid"],
  "generated_at": "2026-09-13T14:22:00Z",
  "status": "complete | partial | failed",

  "summary": "2-3 sentences, current state of the technical evaluation",

  "stakeholders": [{
    "name": "Priya Raman",
    "title": "VP Data Platform",
    "role_inference": "economic_buyer | champion | technical_evaluator | blocker | influencer | unknown",
    "confidence": "high | medium | low",
    "first_seen_call": "uuid",
    "last_seen_call": "uuid",
    "status": "active | departed | new_this_call",
    "evidence": "verbatim line that supports the role inference"
  }],

  "objections": [{
    "objection_id": "obj_01",
    "text": "Concern about PII handling in the normalization layer",
    "category": "security | integration | pricing | data_residency | performance | procurement | other",
    "status": "resolved | open | partially_resolved | resurfaced",
    "resolution_note": "SC walked through field-level encryption; customer accepted",
    "raised_call": "uuid",
    "last_updated_call": "uuid",
    "confidence": "high | medium | low"
  }],

  "integration_patterns": [{
    "description": "Snowflake reverse-ETL via existing Fivetran instance",
    "systems": ["Snowflake", "Fivetran"],
    "agreed": true,
    "caveats": "Pending confirmation their Fivetran plan supports the connector"
  }],

  "success_criteria": [{
    "customer_words": "verbatim quote",
    "interpreted": "plain restatement",
    "metric_stated": "reduce segment build time from 3 days to same-day" 
  }],

  "competitive": [{
    "vendor": "Vendor X",
    "context_verbatim": "what the prospect actually said",
    "evaluation_status": "actively_evaluating | incumbent | mentioned_only",
    "suggested_positioning": "grounded in the stated concern, not a generic battlecard"
  }],

  "product_relevance": [{
    "need_stated": "verbatim need the customer raised",
    "relevant_release": "Release name + one line on why it applies"
  }],

  "next_step": {
    "present": true,
    "described": "Pricing review with Priya and finance",
    "owner": "AE | SC | customer",
    "date_committed": "2026-09-20 | null",
    "confidence": "high | medium | low"
  },

  "open_risks": [{
    "risk": "No economic buyer identified after three calls",
    "severity": "high | medium | low"
  }]
}
```

### Design notes worth defending

- **Every inference carries a confidence field.** The system is allowed to say "unknown." A record that admits it couldn't identify the economic buyer is more useful than one that guesses.
- **`evidence` on stakeholders and `context_verbatim` on competitive** exist so a rep can check the system's work in one glance. Traceability is what earns trust in a live workflow.
- **`status: "resurfaced"`** on objections is a distinct state from `open`. An objection that was closed and came back is the single highest-signal event in the whole system. It gets its own treatment in the diff.
- **`next_step.present: false`** is a first-class output, not a missing field. That flag is what drives the nudge.
- **Competitive and product relevance are grounded**, not retrieved-and-dumped. The system only surfaces positioning tied to something the customer actually said. This is how the differentiation and release-velocity signals get solved at the one moment they convert.

---

## 4. Data Architecture

### Production shape (describe, don't build)

Gong and Salesforce sync to Snowflake on their existing cadence. A scheduled job (every 2 hours) picks up new calls on opportunities in Technical Validation or later, joins opportunity/account/activity context, runs the extraction chain, writes a versioned record back to the warehouse, diffs against the prior version, and renders a Slack payload **only when something material changed.**

**Prompts never touch Gong.** Per-call API extraction at 300 people is expensive and rate-limited. Batch off the warehouse is cheaper, idempotent, replayable, and lets you re-run the whole corpus when you improve a prompt. *Lead with this in the room — it's the strongest credibility signal for the solutions seat on the panel.*

**Three properties to name explicitly:**
1. **Idempotent.** Reprocessing a call produces the same record version, not a duplicate.
2. **Incremental.** A five-call deal produces one pinned record and four diffs, not five records.
3. **Fails visibly.** A failed extraction writes `status: failed` and alerts. It never posts a half-empty record.

### Prototype shape (build this)

Supabase (Postgres) stands in for Snowflake. Synthetic transcripts are seeded directly into the `transcripts` table — that's where the Gong sync boundary sits, and it's a single line on the architecture slide.

**Setup (~30 min):** create a Supabase project, copy the connection string, hand it to Claude Code. Use `psycopg` scripts rather than an MCP server — simpler for this scope and gives you a rerunnable `seed.py`. **No RLS, no auth, no edge functions, no migrations tooling.** It is a table store.

### Schema

```sql
create table accounts (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  industry text,
  employee_count int,
  region text
);

create table opportunities (
  id uuid primary key default gen_random_uuid(),
  account_id uuid references accounts(id),
  name text not null,
  segment text,                    -- 'Enterprise' | 'Mid-Market'
  stage text not null,
  acv numeric,
  close_date date,
  stage_entered_at timestamptz,
  ae_name text, sc_name text, csm_name text,
  slack_channel_id text,
  created_at timestamptz default now()
);

create table calls (
  id uuid primary key default gen_random_uuid(),
  opportunity_id uuid references opportunities(id),
  gong_call_id text,
  call_type text,                  -- 'technical_validation' | 'follow_up' | 'commercial'
  occurred_at timestamptz not null,
  duration_minutes int
);

create table participants (
  id uuid primary key default gen_random_uuid(),
  call_id uuid references calls(id),
  name text, title text, email text,
  is_internal boolean default false
);

create table transcripts (
  id uuid primary key default gen_random_uuid(),
  call_id uuid references calls(id) unique,
  content text not null
);

create table validation_records (
  id uuid primary key default gen_random_uuid(),
  opportunity_id uuid references opportunities(id),
  version int not null,
  source_call_ids uuid[],
  payload jsonb not null,
  status text not null,            -- 'complete' | 'partial' | 'failed'
  generated_at timestamptz default now(),
  unique (opportunity_id, version)
);

create table record_events (
  id uuid primary key default gen_random_uuid(),
  opportunity_id uuid references opportunities(id),
  from_version int, to_version int,
  event_type text,                 -- 'objection_resurfaced' | 'stakeholder_added' |
                                   -- 'champion_changed' | 'objection_resolved' |
                                   -- 'next_step_missing' | 'competitor_introduced'
  detail jsonb,
  materiality text,                -- 'material' | 'minor'  → gates notification
  created_at timestamptz default now()
);

create table activities (
  id uuid primary key default gen_random_uuid(),
  opportunity_id uuid references opportunities(id),
  activity_type text,              -- 'email' | 'call' | 'meeting'
  actor text,
  occurred_at timestamptz,
  subject text
);

create table notifications (
  id uuid primary key default gen_random_uuid(),
  opportunity_id uuid references opportunities(id),
  surface text,                    -- 'channel_pin' | 'channel_update' | 'dm_ae' |
                                   -- 'dm_sc' | 'dm_manager'
  destination text,
  slack_ts text,                   -- enables chat.update on the pinned record
  payload jsonb,
  sent_at timestamptz default now()
);
```

`notifications.slack_ts` is load-bearing. It's how the pinned Record gets edited in place instead of reposted.

---

## 5. Synthetic Data Spec

Six opportunities. Three carry multi-call sequences. Generate with Claude Code; hand-check every transcript for the specific thing it's supposed to test.

| # | Account | Segment / ACV | Calls | What it demonstrates |
|---|---|---|---|---|
| 1 | **Meridian Health** | Ent / $310K | 3 | **The demo deal.** Objection resolved in call 1 resurfaces in call 3. Champion (Dir. Data Eng) departs between calls 2 and 3; new VP appears. Full accrual arc. |
| 2 | **Northwind Logistics** | Ent / $180K | 2 | Active competitive evaluation. Vendor X mentioned offhand mid-call. Tests grounded positioning. |
| 3 | **Calibre Financial** | Ent / $420K | 1 | **Messy transcript.** Crosstalk, an unintroduced stakeholder, an ambiguous half-commitment ("we'll probably want to loop in Marcus"). No next step agreed. Tests confidence handling and the `next_step.present: false` flag. |
| 4 | **Sightline Retail** | MM / $85K | 1 | Clean, fast, textbook. The control. Under-7-days profile. |
| 5 | **Vantage Media** | Ent / $240K | 1 | Customer states a need that a recent release addresses but nobody mentions it. Tests product relevance surfacing. |
| 6 | **Ardent Manufacturing** | Ent / $150K | 1 | Demo was 4 days ago, zero logged activity since. **The nudge demo.** |

### Transcript generation rules

- 60–90 minutes of realistic content, ~6,000–9,000 words each. Long enough that extraction is non-trivial.
- AE, SC, and 2–4 customer-side people. At least one person in Calibre who never introduces themselves.
- Bury the competitor mention in Northwind mid-transcript, phrased casually. Don't make it easy.
- In Meridian call 1, the PII objection gets a *convincing* resolution. In call 3, a new stakeholder reopens it in different words — not a keyword match. This is the case that proves semantic tracking.
- Vary quality deliberately. One transcript should be genuinely hard. When the panel asks what breaks first, you answer with something you observed.

---

## 6. Extraction Chain

Three passes. Don't do it in one prompt — you'll get shallow results on long transcripts and you won't be able to diagnose which part failed.

**Pass 1 — Segment & extract.** Chunk the transcript, pull raw candidates for each field with verbatim evidence attached. Optimized for recall; over-extraction is fine here.

**Pass 2 — Consolidate & classify.** Dedupe candidates, assign categories, make the hard calls: resolved vs. open vs. partially resolved, and stakeholder role inference. Assign confidence. This is where most of your iteration time goes.

**Pass 3 — Merge with prior version.** Input: consolidated extraction + prior record payload. Output: new version + a list of change events. This is where `resurfaced` gets detected — semantically, not by string match — and where champion departure gets inferred from a stakeholder present in versions 1–2 and absent in 3 while a new senior person appears.

### The two things that will embarrass you

**Resolved vs. open classification.** The failure mode is optimism — the model hears the SC give a confident answer and marks the objection resolved, when the customer never actually accepted it. Mitigation: require evidence of *customer* acceptance, not vendor explanation, to mark resolved. Default to `partially_resolved` when only the SC spoke.

**Stakeholder role inference.** The failure mode is title-matching — anyone with "VP" becomes the economic buyer. Mitigation: infer from behavior in the call (who asks about budget, who defers to whom, who owns the timeline), not from title. Require an evidence line. Allow `unknown`.

**Keep a running log of every correction you make to the prompts and why.** The assessment explicitly evaluates "where you had to override the AI or correct it." This log is your answer to that question and it's better than anything you can reconstruct from memory on day 5.

---

## 7. Eval Harness

Two hours of work, disproportionate payoff. It is the difference between "I wrote a prompt" and "I built a system I can tune."

Hand-label 12 transcripts with ground truth. Score the chain on:

| Metric | Target | Why |
|---|---|---|
| Objection recall | > 90% | Missing an objection is the worst failure — silent and invisible |
| Objection status accuracy | > 85% | The optimism failure mode |
| Stakeholder role accuracy (excl. `unknown`) | > 80% | |
| Next-step presence detection | > 95% | Binary, drives the nudge, must be near-perfect |
| **Hallucinated commitments** | **0** | Zero tolerance. A fabricated customer commitment in a follow-up email kills the system |

Run it after every prompt change. Quote the numbers in the presentation. When asked how you'd know output quality is degrading in production, the answer is "this harness runs weekly against a rolling labeled sample, and hallucinated commitments page someone."

---

## 8. Slack Delivery Design

Real free workspace, not a mockup. ~15 min: create workspace → create app → bot token with `chat:write`, `chat:postMessage`, `pins:write` → invite to channel. Create `#deal-meridian-health` with 2–3 fake human members so it reads as a shared space.

**Build on a pinned message updated via `chat.update`, not a canvas.** Canvas availability on free workspaces is inconsistent. Functionally identical for the demo — one durable object reflecting current truth. Mention canvas as the production form on a slide and move on.

### Routing — the judgment call to say out loud

| Surface | Content | Why |
|---|---|---|
| **Pinned message, deal channel** | The Record itself, updated in place | Shared context. CS has been watching it accrue for six weeks before handoff |
| **Channel post** | "What changed" — only on `materiality: material` | Objection resurfaced, stakeholder added, champion changed, competitor introduced |
| **DM to AE or SC, 72h** | Private reminder naming the specific missed action item and its due date | Escalation is never a surprise |
| **Channel post, 7 days** | Public escalation if the private reminder went unaddressed, names which stage-exit criterion it's gating if any | One nudge, one escalation — nags once |
| **Manager, day 7** | Surfaces in existing pipeline review | Private, low-frequency, already in the rhythm |

**The line for the room:** *"A public artifact builds shared context. A public nudge is a public shaming, and reps route around systems that embarrass them. Information is public. Accountability is private."*

That distinction is the practitioner judgment the JD is screening for. Say it deliberately.

### Hygiene philosophy

Every hygiene win comes from **removing work, not adding it.**

- SC review time drops because the Record already reflects what happened on the call, extracted from the transcript — nothing to write from scratch.
- Next steps get logged because the system extracted the one already agreed on the call and asks for confirmation.
- Missed items get caught within 72 hours by a private reminder instead of going silent for a week.

Exactly **one** nudge and **one** escalation in the entire system. *"The more this system nags, the faster it dies, so it nags once."*

---

## 9. Measurement

### 30 days — Adoption
- Coverage: % of technical validation calls producing a complete Record (target 95%)
- Record open rate in channel; AE packet open rate within 24h
- **Reminder-to-resolution rate** within 72h (the real adoption metric — passive opens don't count)
- SC summary completion: 60% → 90%
- Median hours from demo to first logged touch

### 60 days — Behavior
- Post-demo touches in 14 days, **bottom quartile: 0.7 → 1.5** (the headline behavioral number)
- Middle 50%: 1.1 → 1.8
- % of deals with a scheduled next step logged before stage exit
- % of deals with an identified economic buyer before Commercial Negotiation

### 90 days — Impact
- Avg days in Technical Validation: **23 → 16**
- Win rate, Record-covered deals vs. **holdout cohort**
- CS time-to-first-value for deals arriving with a complete Record, measured against the r=0.71 baseline
- % of closed-won deals arriving at CS with a Record < 7 days stale

### Continuous — Quality & counter-metrics
- Weekly eval harness run (§7 metrics)
- **Nudge dismissal rate** — if it climbs, the nudge is miscalibrated and gets turned down. Your own kill switch.
- Record correction rate by SCs — high correction rate means extraction is drifting

### Say this before they say it

The 68/41/22 win-rate table is **correlational.** Slow deals may simply be bad deals. Compressing time-in-stage does not automatically convert a 22% deal into a 68% deal. That's why the 90-day measure is a holdout comparison, not a before/after on the aggregate. Naming this yourself is one of the highest-signal moves available in the room.

---

## 10. What Breaks First

Have these ready. The assessment says they'll ask.

1. **False-resolved objections.** Highest-probability failure. Detection: SC correction rate on the objection block. Mitigation: require customer acceptance evidence; default to `partially_resolved`.
2. **Notification fatigue.** If materiality gating is too loose, the channel becomes noise and people mute it. Detection: mute rate, dismissal rate, declining open rate. Mitigation: tighten the materiality gate; it's a config change, not a rebuild.
3. **Silent extraction failure on atypical calls.** Multi-language, bad audio, a call that's actually a working session rather than a demo. Mitigation: `status: failed` is visible and alerts; never post a partial record silently.
4. **Adoption decays after week 3** once novelty wears off. This is the real risk and it's a product problem, not a technical one. Detection: reminder dismissal rate trend. Mitigation: the system has to be *less* work than the status quo, not more. That's why every hygiene mechanism is subtractive.

---

## 11. Five-Day Plan

**Day 1 — Data foundation**
Supabase project + schema. Generate and hand-check six deals' worth of transcripts. Seed accounts, opportunities, calls, participants, transcripts, activities. *End state: you can query realistic data.*

**Day 2 — Extraction + eval**
Build the three-pass chain. Build the eval harness with 12 labeled transcripts. Iterate on resolved/open and stakeholder inference until metrics clear targets. Keep the correction log. *End state: a record you'd show someone.*

**Day 3 — Diff + Slack**
Slack workspace and app. Pinned-record rendering, `chat.update` in place. Diff logic and materiality gating. Enforcement DM (72h private reminder). *End state: single-call flow works end to end.*

**Day 4 — Accrual + framing**
Multi-call sequence on Meridian: version 1 → 3 with resurfaced objection and champion change. Thin renderings for CS handoff, manager escalation (static/hardcoded is fine — label them as mocks). Measurement slides, failure modes. **Record the backup demo video.**

**Day 5 — Narrative**
Deck. Rehearse to 20 minutes with a timer. Q&A drills. **Send materials 24 hours ahead** (this is a stated requirement — don't miss it).

### Scope discipline — the trap list

**Do not build:**
- A web UI. Slack is the interface, Supabase's table view is your admin panel. This is the single biggest time sink and the assessment explicitly says not to polish.
- Real Gong / Salesforce / Snowflake integration. Draw the boundary on one slide.
- Cron, queues, orchestration. You trigger the job with a command; the schedule is a sentence.
- More than six deals. Volume feels productive and teaches you nothing.
- Retry logic, idempotency guards, error handling for cases the demo never hits. *Describe* them; implement only the diff logic, which is load-bearing.

**Do spend time on:** extraction quality on the hard cases, and the eval harness.

---

## 12. The 20-Minute Presentation

| Time | Section | Content |
|---|---|---|
| 0:00–4:00 | **The problem** | The stage that moved, the win-rate cliff, the 2.3 vs 0.7 gap, the r=0.71 downstream cost. The six converging quotes. Why not the other four problems — and how competitive/product got folded in rather than dropped. |
| 4:00–7:00 | **The workflow** | Walk it as the AE experiences it. Then the SC, CS, manager. Emphasize: one object, four renderings. |
| 7:00–15:00 | **Live demo** | See below. This is the centerpiece. |
| 15:00–18:00 | **Measurement** | 30/60/90 + counter-metrics. Say the correlation caveat yourself. |
| 18:00–20:00 | **What breaks first** | Top 3 failure modes, how you detect each, adoption decay as the real risk. |

### Demo beats (~8 min)

1. **Current state.** The Meridian deal channel as it exists today — AE, SC, CSM in it, and after the technical validation call, silence. That screenshot *is* the problem.
2. **Run the job.** Record posts and pins. Walk it slowly, once: objections with status, stakeholders with inferred roles and evidence, integration patterns, success criteria in the customer's words, competitive mention, next step.
3. **Enforcement.** An action item goes 72 hours past due. Its owner gets a private reminder. Say plainly: *private first, so escalation is never a surprise.*
4. **Advance three weeks. Run call 2, then call 3.** The pinned Record updates in place. New stakeholder appears. The champion is gone. **The PII objection you marked resolved is back.** Channel gets a short "what changed" post.
5. **Jump to close.** Show the CS handoff — and make the point that CS isn't *receiving* anything. They've been in the channel the whole time.
6. **Ardent Manufacturing.** Four days, no activity. The nudge, in DM, once. Deliver the line about public nudges.

**Record the full run, narrated, as backup.** Live demos fail in panel rooms for reasons unrelated to your code.

---

## 13. Q&A Prep

**"Why this over the differentiation problem?"**
Three of the five signals are content-supply problems that surface at every stage — hard to scope, hard to attribute, and PMM owns half. One is a workflow problem with a measurable behavioral gap at a specific moment. I also didn't drop differentiation: the Record surfaces competitive positioning grounded in what the prospect actually said, at the one moment it converts.

**"The win-rate table is correlation, not causation."**
Agreed, and that's why the 90-day measure is a holdout, not a before/after. Slow deals may be bad deals. What I'm confident in is the behavioral gap — 2.3 vs 0.7 touches is a behavior, not a deal-quality artifact.

**"Gong already writes call summaries. Why build this?"**
A summary is prose for one reader at one moment. This is a structured object that accrues across calls, routes to four consumers in different renderings, and writes to a warehouse I can join to outcomes. You can't query a summary, diff it, or measure against it.

**"What's this cost to run at 300 people?"**
Batch off the warehouse, not per-call API into Gong. One extraction per new call on active opportunities, roughly [X] calls/week at Apex scale. Re-runnable when prompts improve, without re-pulling from Gong.

**"Customer call content in a Slack channel — security?"**
Deal channels are internal and access-controlled, and the Record contains strictly less than what already sits in Gong, which the same people already have access to. Verbatim quotes are limited to evidence lines. If policy requires it, the channel post can carry a summary with the full record behind a link.

**"What if reps just ignore it?"**
That's the real risk, and it's why every hygiene mechanism is subtractive. SC review time drops because the Record already reflects the call, not because I added a reminder. The measure that matters is reminder-to-resolution rate, not opens. If that decays after week 3, the system isn't less work than the status quo and I'd rebuild the surface, not add nagging.

**"What would you build next?"**
The pattern library across Records: which objection-handling approaches precede advancement, which integration concerns recur by vertical, which competitor mentions correlate with stall. Framed as a shared SC asset, not an individual scorecard. It needs about a quarter of volume before the patterns are trustworthy — I wouldn't ship it on thin data.

---

## Open Items

- [ ] Confirm whether anything at Braze already occupies this surface
- [ ] Decide whether to use real Braze release names in the product-relevance field or keep everything Apex-fictional (recommend: keep it fictional, mention the Braze parallel verbally)
- [ ] Get the recruiter to confirm the exact panel roster and send time
