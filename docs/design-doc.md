# Mushu: AI System Design and Prototype

**Applied AI Architect, GTM — Assessment Requirement 3**

This document describes the AI-powered solution — who uses it, when, what triggers it, what the
output looks like, and what data it needs — and then describes what was actually built as a
working prototype, not just designed. It reconciles `docs/build-plan.md` (the original plan),
`docs/record-contract.md` (the authoritative schema), and `docs/enforcement-layer-spec.md` (the
verification layer) into one narrative. Where those documents disagree, `record-contract.md` and
`enforcement-layer-spec.md` are treated as ground truth, since they were written to reconcile and
correct the original plan.

---

## 1. Who uses it

- **The AE** — reads `ae_actions` in the deal's living record, posted directly to the deal's Slack
  channel. Receives a private DM if an action item they own passes its due date with no evidence
  it happened.
- **The SC** — reads `sc_actions` and `sc_loop_close` in the same record: whether their prior
  technical resolutions held up in the next call, or got reopened. This is the direct answer to
  the assessment packet's own SC quote — *"I almost never hear how it goes after that."*
- **The CSM** — inherits the record at deal close, having watched it accrue in-channel for the
  life of the deal rather than receiving a cold handoff.
- **The sales manager** — doesn't get a new surface to check. A day-7 escalation and the adherence
  dashboard both surface inside the existing pipeline review, not as a fourth tab nobody opens.

There is no draft-and-approve step anywhere in the system. The record posts directly to the
channel after each call; nothing waits on a human to review or approve it before the deal team
sees it. This is a deliberate design choice under the "hygiene through subtraction" philosophy
(§6) — every mechanism in the system is meant to remove work, not add a review step.

## 2. When

Active from the first Technical Validation call. Goes quiet through Commercial Negotiation and
Legal. Wakes once at close for the CS handoff.

This scope is deliberate, not accidental. It is the specific fourteen-day window that the
quantitative data (Technical Validation is the only stage whose duration moved: 12 → 14 → 23 days
across three quarters, while Discovery, Commercial Negotiation, and Legal all held flat) and six
independent qualitative signals — an AE with no playbook for the post-demo moment, an SC who never
learns if their answer held up, a CS manager inheriting drifted expectations and a changed
champion, a sales manager watching average reps "wait," an enablement lead whose guide is dead in
Confluence, and the packet's own note that SC summaries complete only ~60% of the time — all
converge on. The system does not attempt to manage the whole deal lifecycle; it targets the
specific gap the data and the field both point at.

## 3. What triggers it

Nothing manual. Three independent event types drive the system:

| Trigger | What happens |
|---|---|
| A new call transcript lands | The three-pass extraction chain runs; the record updates in place in the pinned Slack message (`chat.update`, not a new post); a separate "what changed" post fires only if something material happened (an objection reopened, a stakeholder changed, a champion left) |
| An action item's due date passes with no evidence it happened | A private DM to the owner — once |
| That reminder goes unaddressed for 7 days | A public post in the deal channel, naming the specific item and which stage-exit criterion it's gating — once |

In production, the first trigger is driven by a scheduled batch job (roughly every 2 hours)
reading new calls off the warehouse, not a person running a command. The prototype triggers this
step by hand, and that boundary is named explicitly in §7 below.

## 4. What the output looks like

One record per opportunity, updated in place as the deal progresses — not one record per call.
Version 1 from the first Technical Validation call and version 3 from six weeks later are
different objects, and the diff between them is the deal's actual story. The record has two main
parts.

**A plain-language narrative:**
- `whats_happened` — 2–3 short paragraphs of prose describing what changed since the last version
  and what's open and why it matters. No field labels, no evidence quotes dumped in.
- `whats_blocking` — split explicitly into `blocking` and `not_blocking`, so an item that looks
  concerning but isn't actually gating progress doesn't read as a false alarm.
- `ae_actions` — synthesized, ready-to-act items derived from the record, not copy-pasted from the
  transcript.
- `sc_loop_close` — prose addressed to the SC: did their prior resolutions hold up this version, or
  did something they handled get reopened. If nothing technical is blocking, this says so
  explicitly — that is the feedback an SC otherwise never gets.
- `sc_actions` — optional, may be empty.

**Five fixed stage-exit criteria**, always present, in this exact order, computed only after the
full merge (pass 3) rather than from a single call in isolation — because only the fully accrued
record knows whether an objection resolved two versions ago is still resolved:

1. All technical objections resolved or accepted (owner: SC)
2. Economic buyer identified, confidence high or medium (owner: AE)
3. Integration approach agreed (owner: SC)
4. Next step scheduled with owner and date (owner: AE)
5. Success criteria captured in the customer's own words (owner: AE)

Each criterion carries a `met` boolean and a one-line, plain-language `reason` naming the specific
gap when unmet (e.g. which objection is still open, described in plain language — never by an
internal ID).

Underneath the narrative and the exit criteria, the record tracks:

- **`stakeholders`** — name, title, inferred role (`economic_buyer | champion | technical_evaluator
  | blocker | influencer | unknown`), a `confidence` level, and a verbatim `evidence` line so a rep
  can check the system's reasoning in one glance. Roles are inferred from behavior in the call —
  who asks about budget, who defers to whom, who owns the timeline — never from title alone.
- **`objections`** — text, category, and a status of `resolved | open | partially_resolved |
  resurfaced`. `resurfaced` is a distinct status from plain `open`: an objection that was closed
  and later comes back in different words is the single highest-signal event in the system, and it
  must not collapse back into an undifferentiated "open."
- **`competitive`** — every flagged vendor, tool, or prior-evaluation mention gets a row, including
  unnamed and purely historical ones. A closed or throwaway mention is marked
  `evaluation_status: "mentioned_only"` with a `rationale` explaining why it's immaterial — it is
  never simply dropped. An empty `competitive` array must mean nothing was mentioned, never that
  something was mentioned and judged away; those two cases have to be distinguishable from the
  record alone, without re-reading the transcript.
- **`next_step`** — always a fully populated object, even when nothing was agreed. When
  `present: false`, every other field (`described`, `owner`, `date_committed`, `confidence`) is
  explicitly `null`, not omitted — because this flag is exactly what the 72-hour reminder logic
  reads.
- **`open_risks`**, **`integration_patterns`**, **`success_criteria`**, **`product_relevance`** —
  each carries a `confidence` field where it involves a judgment call rather than a transcription
  (see the corrections log, §8.1, for how this principle was actually enforced).

**A real example**, from the Meridian Health deal at version 3: exit criteria at 3 of 5, with the
`reason` field for the unmet "technical objections resolved" criterion reading *"A patient-data
protection objection is open again — now a contract-coverage question, not a technical one"* —
naming the specific gap in plain language, not a generic status.

## 5. What data it needs

- **Call transcripts** (Gong, in production) — the raw input to the extraction chain.
- **CRM opportunity and activity data** — stage, stage-entry date, and logged AE/SC activity. This
  serves two purposes: context for the extraction chain, and the evidence the closure-tracking
  logic checks against when an action item's due date passes.
- **An internal knowledge base** — product release notes and competitive battlecards, tagged. Used
  only to ground `product_relevance` and `competitive.suggested_positioning` in something the
  customer actually said. Nothing is invented: if nothing relevant retrieves, the field is left
  empty rather than filled with generic content.

---

## 6. Design philosophy: hygiene through subtraction

Every mechanism in the system is built to remove work from a human, not add a step for them to do.
The SC's review burden drops because the record already reflects what happened on the call,
extracted from the transcript — there is nothing to write from scratch. Next steps get logged
because the system extracts the one already agreed on the call, not because someone is asked to
fill out a form. A missed action item is caught within 72 hours by a private reminder instead of
going silent for a week, and it escalates exactly once if unaddressed — because a system that nags
repeatedly gets muted, and a system with no consequence at all gets ignored. This is also why there
is no draft-and-approve step: an approval gate is a step to do, and the entire design principle is
to have fewer of those, not more.

---

## 7. The prototype — built, not just described

This is a working system, run against real (synthetic) input, not a set of mocked screenshots.

- **A live schema in Supabase**, standing in for the production warehouse: `accounts`,
  `opportunities`, `calls`, `participants`, `transcripts`, `validation_records` (versioned),
  `record_events` (a separate change-event log with materiality tagging), `activities`,
  `action_items`, and `notifications`.
- **Nine full synthetic call transcripts**, generated and hand-QA'd, covering six deals — including
  a deliberately hard case (an unidentified speaker who contributes substantively but never
  introduces themselves, genuine crosstalk, no next step agreed) and a deliberate false-positive
  trap (a historical, already-rejected competitor mention that must classify as `mentioned_only`
  and must not fire a false `competitor_introduced` event).
- **A real three-pass extraction chain**, actually run against this synthetic input:
  - **Pass 1 — extract.** Full transcript, no chunking (transcripts fit in context). Biased toward
    recall; over-extraction here is acceptable, since pass 2 will consolidate.
  - **Pass 2 — consolidate, retrieve, classify.** Dedupes candidates, queries the knowledge base on
    extracted competitor names and unmet needs, assigns categories and confidence, and makes the
    hard classification calls (resolved vs. open vs. partially resolved; stakeholder role
    inference from behavior, not title).
  - **Pass 3 — merge.** Consolidated extraction plus the prior version's full payload produces the
    new version and a list of change events. This is the only pass that ever produces something
    matching the full record contract, and the only place `resurfaced` and `champion_changed`
    events get detected — semantically, not by string matching.
- **A real Slack workspace and bot**, posting and updating the pinned record in an actual deal
  channel via `chat.update`, not a screenshot mockup.
- **The Meridian Health accrual arc, run end to end**: an objection resolved in call 1 (a PII
  concern, explicitly accepted by the customer) resurfaces in call 3 — after the original champion
  departs and a new VP arrives — in entirely different vocabulary (PHI, staging layer, BAA vs. the
  original encryption, tokenization, HSM). This proves the system tracks meaning across calls, not
  keywords.
- **A documented corrections log** (`docs/corrections.md`) — seven real cases where the system's
  own output was caught and corrected during the build, including one limitation that was
  identified and deliberately left unfixed, with the reasoning for that choice made explicit (see
  §8 below).

### What I built vs. what I'd build in production

| | Prototype | Production |
|---|---|---|
| Warehouse | Supabase (Postgres) | Snowflake, on Gong/Salesforce's existing sync cadence |
| Orchestration | Hand-run per call | Scheduled batch job (~every 2 hours) |
| Transcripts | 9 synthetic, hand-QA'd | Real Gong calls |
| Slack surface | Pinned message, `chat.update` | Canvas (attempted first in the prototype; falls back to a pinned message on free-workspace limits) |
| Stage tracking | Current state only; dates as relative offsets from a reference date | Real Salesforce stage history |
| Dashboard | Static HTML generated from a query | Live, refreshing |

One architectural choice is defended regardless of environment: **batch extraction off the
warehouse, never per-call API calls into Gong.** At 300 people this is cheaper, idempotent
(reprocessing a call produces the same version, not a duplicate), incremental (a five-call deal
produces one record and four diffs, not five separate records), and replayable — the whole corpus
can be re-run when a prompt improves without re-pulling anything from Gong.

---

## 8. Corrections log — where the system was overridden or corrected

Full detail in `docs/corrections.md`. Summary, in the order found:

1. **A spec defect caught in my own reconciliation.** The original plan's stated design
   principle — every judgment-call field carries a `confidence` value — wasn't actually followed
   in its own example. Missing from four fields (`integration_patterns.agreed`,
   `competitive.evaluation_status`, `product_relevance`, `open_risks.severity`). Fixed when the
   plan was formalized into the authoritative contract.
2. **A silent retrieval bug.** The knowledge-base tag tokenizer stripped hyphens, so a compound tag
   like `self-serve` could never match. This is the dangerous kind of bug: the record would read as
   complete and confident while quietly missing a field it should have populated, because a
   groundable need would simply fail to retrieve and pass 2 would (correctly) drop the ungrounded
   candidate rather than invent something.
3. **A downstream fix that was never actually tested.** Pass 2's classification logic for
   competitive mentions was correctly improved, but pass 1 had never extracted the unnamed
   competitor mention it was meant to judge in the first place — so the fix looked complete but was
   untested against real input. The general lesson: check whether the responsible stage actually
   ran on the relevant input, not just whether the final output looks right.
4. **A classification rule that needed tightening.** "The customer accepted the answer" was not
   sufficient evidence to mark an objection `resolved`. The sharper test: did the answer make the
   underlying concern no longer true, or did the customer just accept its cost as a standing
   tradeoff? Only the former is `resolved`; the latter is `partially_resolved`.
5. **A limitation identified and deliberately not fixed.** The AE closure-tracking rule — any
   logged activity by that AE after an item's creation counts as evidence it was done — produced a
   false positive: an action item that is very likely still outstanding came back `completed` on
   unrelated activity. This was flagged rather than quietly re-seeded away, with an explicit note
   that absence of evidence is a strong, conservative signal, while presence of evidence under this
   heuristic is a weak one — and anything built on top of closure tracking (the dashboard,
   escalation) should not treat "completed" with the same confidence as "missed."
6. **A second, structurally identical recall gap.** Commercial and procurement pushback tied to a
   named competitor was captured only as a `competitive` entry, never as an `objections` entry —
   making it invisible to the stage-exit criteria and action items, which only ever read
   `objections`. Same root cause as #3: a category of real content that no explicit instruction
   pointed at, sitting one inferential step away from every worked example already in the system.
7. **An operator error the system's own rule caught.** A build instruction stated as fact that a
   departed champion had also been the deal's economic buyer. The record's own verified data said
   otherwise. The existing grounding rule — write to verified data, never a tidier narrative — was
   written to guard against a model inventing a cleaner story, but it happened to also catch a
   confidently wrong premise supplied by the human operator, and surfaced the discrepancy back
   rather than silently complying with it.

---

## 9. What breaks first

- **False-resolved objections.** The highest-probability failure mode: a customer's grudging
  acceptance of a limitation gets misread as the concern being genuinely settled. Detected via SC
  correction rate on the objection block; mitigated by requiring explicit customer acceptance
  evidence and defaulting to `partially_resolved` when only the SC spoke.
- **Notification fatigue.** If the materiality gate on the "what changed" post is too loose, the
  channel becomes noise and gets muted. This is a config change (tightening the gate), not a
  rebuild.
- **Adoption decay after week three**, once novelty wears off. This is the real risk, and it is a
  product problem, not a technical one — the system has to be less work than the status quo, not
  more. Detected via the reminder-to-resolution rate trend over time; if it decays, the fix is
  rebuilding the surface, not adding more reminders.
