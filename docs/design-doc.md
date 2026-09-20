# Mushu: AI System Design and Prototype

**Applied AI Architect, GTM — Assessment Requirement 3**

This covers who uses the system, when, what triggers it, what it outputs, what data it needs, the
decisions behind it, and what I actually built.

*A note on naming: the project is called Mushu.*

---

## 1. Who uses it

- **The AE** — reads `ae_actions` in the deal's record, posted straight to the deal's Slack
  channel. Gets a private DM if an action item they own passes its due date with no evidence it
  happened.
- **The SolCon** — reads `sc_actions` and `sc_loop_close`: whether their prior technical
  resolutions held up in the next call, or got reopened. The packet's own SolCon quote is
  *"I almost never hear how it goes after that."* This is that.
- **The CSM** — inherits the record at close, having watched it build in-channel the whole time
  rather than getting a cold handoff.
- **The sales manager** — no new surface to check. The day-7 escalation and the adherence
  dashboard both show up inside the pipeline review they already run.

There's no approval step anywhere. The record posts directly after each call. Nothing waits on a
human to sign off before the deal team sees it — an approval step is more work, and the whole
point is less.

## 2. When

Active from the first Technical Validation call. Quiet through Commercial Negotiation and Legal.
Wakes once at close for the CS handoff.

Technical Validation is the only stage whose duration moved — 12 to 14 to 23 days over three
quarters, while Discovery, Commercial Negotiation, and Legal all held flat. Six separate
qualitative signals land in the same window: an AE with no playbook after the demo, a SolCon who
never learns if their answer held, a CS manager inheriting drifted expectations and a changed
champion, a sales manager watching average reps wait, an enablement lead whose guide is dead in
Confluence, and the packet's own note that SolCon summaries complete about 60% of the time.

## 3. What triggers it

Nothing manual. Three event types:

| Trigger | What happens |
|---|---|
| A new call transcript lands | The three-pass chain runs; the record updates in place in the pinned Slack message via `chat.update`; a separate "what changed" post fires only if something material happened — an objection reopened, a stakeholder changed, a champion left |
| An action item's due date passes with no evidence it happened | Private DM to the owner, once |
| That reminder goes unaddressed for 7 days | Public post in the deal channel, naming the item and which stage-exit criterion it's gating, once |

In production the first trigger is a scheduled batch job — roughly every 2 hours, reading new
calls off the warehouse. The prototype runs that step by hand (§9).

These three run independently. Nothing chains them together.

```
AFTER EVERY CALL
────────────────────────────────────────────────────────────
  Gong call syncs to warehouse
        │
        ▼  batch job picks up new transcripts (~2 hrs)
  Three-pass chain
        │   pass 2 also joins SFDC opportunity/activity for context
        ▼
  Versioned record written
        │
        ▼
  Pinned Slack message updated in place  (chat.update)
        │
        ▼
  Action items written to action_items    (deduped against prior versions)
        │
        ├── material change?  ──yes──▶  "what changed" post
        └──────────────────────no──────▶  nothing else posts


IF AN ACTION ITEM GOES OVERDUE
────────────────────────────────────────────────────────────
  Item in action_items passes its due date
        │
        ▼  checked against evidence:
           AE items       → SFDC activity history
           SolCon items   → record field state changed
           customer items → SFDC stage-history (did the stage move)
        │
        ├── evidence found ──▶ marked complete, nothing happens
        │
        └── no evidence ──▶ private DM to the owner  (once)
                                  │
                                  ▼  still open at 7 days?
                            public post in the deal channel  (once)
                            names the item + the criterion it gates


WHEN THE DEAL IS READY TO ADVANCE
────────────────────────────────────────────────────────────
  After each record update: all 5 exit criteria met?
        │
        ├── no  ──▶ record shows "X of 5", blockers named in plain language
        │
        └── yes ──▶ stage advances
                    record goes quiet through Negotiation and Legal
                    wakes once at close for the CS handoff
```

## 4. What the output looks like

One record per opportunity, updated in place as the deal moves. Not one per call. Version 1 from
the first call and version 3 from six weeks later are different objects, and the diff between them
is the deal's actual story.

**The narrative block:**
- `whats_happened` — 2–3 short paragraphs of plain prose: what changed since last version, what's
  open, why it matters. No field labels, no quote dumps.
- `whats_blocking` — split into `blocking` and `not_blocking`, so something that looks concerning
  but isn't actually gating progress doesn't read as a false alarm.
- `ae_actions` — synthesized from the record, not copy-pasted from the transcript.
- `sc_loop_close` — prose to the SolCon: did their prior resolutions hold, did anything they
  handled get reopened. If nothing technical is blocking, it says so — that's feedback a SolCon
  otherwise never gets.
- `sc_actions` — optional, can be empty.

**Five stage-exit criteria**, always present, same order, computed after the full merge (pass 3)
rather than from one call in isolation — only the fully accrued record knows whether an objection
resolved two versions ago is still resolved:

1. All technical objections resolved or accepted (SolCon)
2. Economic buyer identified, confidence high or medium (AE)
3. Integration approach agreed (SolCon)
4. Next step scheduled with owner and date (AE)
5. Success criteria captured in the customer's own words (AE)

Each carries a `met` boolean and a one-line `reason` when unmet, written in plain language, never
an internal ID.

**Underneath:**

- **`stakeholders`** — name, title, inferred role, confidence, and a verbatim `evidence` line so a
  rep can check the reasoning at a glance. Roles come from behavior in the call — who asks about
  budget, who defers to whom, who owns the timeline. Not from title.
- **`objections`** — text, category, and status: `resolved | open | partially_resolved |
  resurfaced`. `resurfaced` is its own status, separate from `open`. An objection that was closed
  and came back in different words is the most important thing this catches, and it can't collapse
  back into an undifferentiated "open."
- **`competitive`** — every vendor, tool, or prior-evaluation mention gets a row, including unnamed
  and historical ones. A throwaway mention is marked `mentioned_only` with a `rationale` for why
  it's immaterial. An empty array has to mean nothing was mentioned, never that something was
  mentioned and judged away — you can't tell those apart later without re-reading the transcript.
- **`next_step`** — always fully populated, even when nothing was agreed. `present: false` with
  every other field explicitly `null`, not omitted. That flag is what the 72-hour reminder reads.
- **`open_risks`**, **`integration_patterns`**, **`success_criteria`**, **`product_relevance`** —
  each carries `confidence` where it's a judgment call rather than a transcription.

**Real example**, Meridian Health v3: exit criteria at 3 of 5, with the unmet technical-objections
criterion reading *"A patient-data protection objection is open again — now a contract-coverage
question, not a technical one."*

## 5. What data it needs

- **Call transcripts** (Gong in production) — the raw extraction input.
- **CRM opportunity and activity data** — stage, stage-entry date, logged AE/SolCon activity. Two
  jobs: context for extraction, and the evidence closure-tracking checks against when an item's
  due date passes.
- **Internal knowledge base** — release notes and battlecards, tagged. Only used to ground
  `product_relevance` and `competitive.suggested_positioning` in something the customer actually
  said. Nothing invented: if nothing retrieves, the field stays empty.

---

## 6. Design philosophy: hygiene through subtraction

Every mechanism removes work rather than adding a step. The SolCon's review burden drops because
the record already reflects the call — nothing to write from scratch. Next steps get logged
because the system pulls the one already agreed on the call, not because someone fills out a form.
A missed item gets caught in 72 hours instead of going silent for a week, and escalates exactly
once. A system that nags constantly gets muted; a system with no consequence gets ignored.

---

## 7. Decisions and tradeoffs

### Slack, not a web app

A web app would be more elegant. It would also be a place people have to remember to go, and the
packet already documents what happens to those: the enablement lead built a post-demo follow-up
guide, it lives in Confluence, and by her own account nobody knows it exists. That's the failure
mode I'm designing against.

AEs and SolCons already live in the deal channel. The record shows up where the conversation about
the deal is already happening, in the same thread as the human back-and-forth about it. That's
worth more than a better interface nobody opens.

The tradeoff is real. Slack constrains formatting badly, a pinned message is a clumsy container
for a structured object, and I give up any real interaction model. I took that trade on purpose.

### Not just Gong's call summary

Gong writes a good summary. But a summary is prose, written once, for one reader, about one call.
Four differences that matter:

- **Structured, so it's queryable.** You can't ask a summary how many deals in the pipeline have
  an open security objection. You can ask this, because it writes to a warehouse table you can
  join against outcomes.
- **It accrues across calls.** Gong summarizes call three. It can't tell you that an objection
  resolved in call one came back in call three in different words, raised by someone who wasn't
  there the first time, with no vocabulary overlap. That comparison needs an object that persists
  between calls.
- **Grounded in our own material.** Classification runs against our stage-exit criteria, our
  battlecards, our release notes. A generic summarizer doesn't know what "economic buyer
  identified" means for our process, or that a competitor's name should pull a specific
  positioning response. I can tune recall on the things we care about, and measure that tuning
  (§8).
- **Cheaper and more controlled.** Batch extraction off the warehouse, re-runnable when prompts
  improve, instead of per-call API calls at 300 people. When quality drifts I see it in the eval
  harness and fix the prompt, rather than filing a ticket with a vendor.

### Scoped to the opportunity, not the call

A per-call object would be simpler to build and would never need a merge step. It also can't do
the one thing this exists for. Resurfacing, champion departure, and stakeholder drift are all
comparisons between two points in time — they only exist if something persists across calls. The
merge pass is the expensive part of the design and it's the part that earns the rest.

### Three passes, not one prompt

One prompt over a 60–90 minute transcript gives shallow results, and when it's wrong you can't
tell which part failed. Splitting it means each pass has one job — recall, then classification,
then comparison against prior state — and when something breaks I can isolate it. Corrections #3
and #6 were both found this way: the output looked fine, and tracing which pass should have
handled the input is what surfaced the gap.

### Batch off the warehouse, never per-call API calls into Gong

Cheaper at 300 people, idempotent, and replayable — the whole corpus can be re-run after a prompt
improvement without re-pulling anything. This is the one architectural choice I'd keep in any
environment.

---

## 8. Quality and failure handling

**How I know the output is any good.** A real eval harness, not a plan for one — hand-written
ground truth from three transcripts, read independently before looking at any chain output, scored
against a fresh run of the actual chain by a re-runnable script (`scripts/eval_score.py`,
`evals/results.md`):

| Metric | sightline-01 | calibre-01 | vantage-01 |
|---|---|---|---|
| Objection recall | 3/3 | 6/6 | 5/5 |
| Objection status accuracy | 3/3 | 6/6 | 5/5 |
| Stakeholder role accuracy | 2/2 | 2/2 | 2/2 |
| Next-step detection | correct | correct | correct |
| Product relevance (Consent Sync) | n/a | found | found |
| **Hallucinated commitments** | **0** | **0** | **0** |
| Stage-exit criteria | 5 of 5 | 1 of 5 | 3 of 5 |

The three transcripts were chosen for coverage, not for a clean result: `sightline-01` is the
designed-to-be-clean control; `calibre-01` is the deliberately hard case (unidentified speaker,
crosstalk, no next step); `vantage-01` is the "unmet product relevance" plant — a customer
describes real pain that nobody in the room connects to an actual release, testing the single most
load-bearing claim in the system against a real `query_knowledge.py` retrieval, not just JSON
matching.

**The honest limit, stated plainly:** the same reasoner wrote the ground truth and ran the chain,
so a clean score here proves internal rule-consistency, not independent validation. Two things
partially offset that — ground truth was written from the raw transcript alone before any chain
output existed to consult, and several judgment calls genuinely moved mid-process rather than
being decided once and confirmed (`evals/results.md` documents each one, including a real
reclassification that reproduces the exact failure mode `docs/corrections.md` #4 was written to
catch, found on the same deal, on a different objection). This is a first real data point on three
transcripts, not the ongoing, twelve-transcript, weekly-re-run harness that's still the production
target — extending it to the rest of the corpus is mechanical, not a new build.

In production this would run weekly against a rolling labeled sample. A hallucinated commitment
pages someone.

**When extraction fails.** The record carries a `status` of `complete`, `partial`, or `failed`.
`partial` means one section was genuinely too thin for a trustworthy merge but the rest is usable
— a flagged limitation, not a failure. `failed` means malformed output or a broken merge, set by
`write_record.py` on validation failure. A failed extraction never posts a half-empty record; it
writes `failed` and alerts.

**Idempotency.** Reprocessing a call produces the same record version, not a duplicate. A
five-call deal produces one pinned record and four diffs, not five separate records. The whole
corpus can be re-run when a prompt improves, without re-pulling anything from Gong.

---

## 9. What I built

All of this runs. The data's synthetic; the code isn't.

- **Live schema in Supabase**, standing in for the warehouse: `accounts`, `opportunities`, `calls`,
  `participants`, `transcripts`, `validation_records` (versioned), `record_events`, `activities`,
  `action_items`, `notifications`.
- **Ten synthetic call transcripts**, generated and hand-QA'd across six deals. Two are
  deliberately hard: one with an unidentified speaker who contributes substantively but never
  introduces themselves, real crosstalk, and no next step agreed; one with a historical,
  already-rejected competitor mention that has to classify as `mentioned_only` and must not fire a
  false `competitor_introduced` event.
- **The prompt chain** (below), run against all of it.
- **Real Slack workspace and bot**, updating the pinned record via `chat.update`.
- **The Meridian arc end to end**: a PII objection explicitly accepted by the customer in call 1
  comes back in call 3, after the champion leaves and a new VP arrives, in completely different
  vocabulary — PHI, staging layer, BAA against the original encryption, tokenization, HSM. That's
  the case that proves it's tracking meaning, not keywords.
- **`docs/corrections.md`** — seven cases where I caught and fixed the system's own output,
  including one limitation I found and deliberately left unfixed (§11).

### How the chain actually runs

Five prompts, each a separate file in `prompts/` so they can be iterated independently. Three do
the extraction; two do the rendering.

**`01_extract.md` — extract.** Full transcript, no chunking; the longest is about 52k characters
and fits in context. Biased toward recall — over-extraction is fine here, because pass 2
consolidates. Every candidate carries a verbatim evidence quote. This pass ignores the record
contract's enums entirely; its only job is not to miss things.

**Retrieval, between passes 1 and 2 — code, not a prompt.** A script pulls the competitor names
and unmet needs out of pass 1's output, queries the `knowledge` table on subject and tags, and
passes only the matching rows into pass 2. The model never searches for itself, which is what makes
"grounded in retrieved content only, never invented" enforceable rather than aspirational. With
only 8 knowledge rows, keyword lookup is the right call and vector search would be
over-engineering — the interface is the same either way.

**`02_consolidate.md` — consolidate, retrieve, classify.** Dedupes candidates, assigns categories
and confidence, and makes the two hard calls: objection status (resolved / open /
partially_resolved) and stakeholder role inference from behavior rather than title. Grounds
`competitive` and `product_relevance` in the retrieved rows only. This pass sees one call in
isolation and nothing else.

**`03_merge.md` — merge.** Takes pass 2's output for the current call plus the prior version's
full payload, and emits the new version plus change events. The only pass that produces something
matching the full contract, and the only place `resurfaced`, `champion_changed`, and the other
change events get detected — semantically, not by string match. Stage-exit criteria are computed
here, after the merge, because only the fully accrued record knows current standing.

**`04_render.md` and `05_handoff.md` — rendering.** Turn the merged record into the Slack message
and, at close, the CS handoff. Kept separate from extraction so the record's content and its
presentation iterate independently. `04_render.md` carries the grounding rule that caught
correction #7.

`scripts/write_record.py` is the only place the contract is mechanically enforced; a payload that
fails validation is written `failed` rather than posted.

In the prototype the passes are hand-run against these files per `scripts/run_chain.md` — there's
no orchestrator. In production this is the scheduled job described below.

### Prototype vs. production

| | Prototype | Production |
|---|---|---|
| Warehouse | Supabase (Postgres) | Snowflake, on Gong/Salesforce's existing sync |
| Orchestration | Hand-run per call | Scheduled batch job, ~every 2 hours |
| Transcripts | 10 synthetic, hand-QA'd | Real Gong calls |
| Slack surface | Pinned message, `chat.update` | Canvas — chose a pinned message here because canvas access is inconsistent on free workspaces |
| Stage tracking | Current state only, relative date offsets | Real Salesforce stage-history timestamps |
| Dashboard | Static HTML from a query | Live |

This one I'd keep either way: **batch off the warehouse, never per-call API calls into Gong.**
Cheaper at 300 people, idempotent, replayable.

If SFDC and Gong both land in warehouse tables including historical stage-change tables,
production could plausibly run this as a Snowflake Cortex Agent instead of custom orchestration —
text-to-SQL against structured SFDC data plus document search against transcripts, in one governed
environment. That changes the execution layer, not the design. The record contract, the
classification rules, and the stage-exit logic are the contribution regardless of what runs them.

---

## 10. Security and data handling

Deal channels are internal and access-controlled. The record contains strictly less than what's
already sitting in Gong, which the same people can already see. Verbatim quotes are limited to
evidence lines — one per stakeholder inference, one per competitive mention — not transcript
excerpts.

If policy required it, the channel post could carry a summary with the full record behind a link,
so the sensitive content sits behind whatever access control the warehouse already enforces rather
than in the message itself.

The prototype uses 100% synthetic data. No real customer content anywhere in the repo.

**Cost at scale.** One extraction per new call on opportunities in Technical Validation or later.
Because it batches off the warehouse rather than calling Gong per-call, cost scales with new calls
on active deals, not with total corpus size — and re-running the corpus after a prompt improvement
costs model time only, not re-ingestion.

---

## 11. Corrections log

Full detail in `docs/corrections.md`. In the order found:

1. **A spec defect I caught in my own reconciliation.** My build plan stated the principle — every
   judgment-call field carries `confidence` — and then didn't follow it in its own example.
   Missing from four fields. Fixed when I formalized the plan into the contract.
2. **A silent retrieval bug.** The tag tokenizer stripped hyphens, so a compound tag like
   `self-serve` could never match. Nothing about the output would've looked wrong — a groundable
   need would just quietly fail to retrieve, and pass 2 would correctly drop the ungrounded
   candidate rather than invent one.
3. **A downstream fix that was never actually tested.** I improved pass 2's competitive
   classification logic, but pass 1 had never extracted the unnamed competitor mention it was
   meant to judge. The fix looked complete and was untestable. Check whether the responsible stage
   ran on the relevant input, not just whether the final output looks right.
4. **A classification rule that needed tightening.** "The customer accepted the answer" wasn't
   enough to mark an objection `resolved`. The sharper test: did the answer make the concern
   untrue, or did the customer just accept its cost as a standing tradeoff? Only the first is
   `resolved`.
5. **A limitation I found and deliberately didn't fix.** The AE closure rule counts any logged
   activity after an item's creation as evidence it happened. That produced a false positive — an
   item almost certainly still outstanding came back `completed` on unrelated activity. I flagged
   it rather than quietly re-seeding the data to avoid the awkward result. Absence of evidence is
   a strong, conservative signal. Presence of evidence under this heuristic is a weak one, and
   anything built on top of closure tracking shouldn't treat `completed` with the same confidence
   as `missed`.
6. **A second recall gap with the same shape as #3.** Commercial and procurement pushback tied to a
   competitor's name landed only in `competitive`, never as an `objections` entry — invisible to
   stage-exit criteria and action items, which only read `objections`. Same root cause: real
   content sitting one inferential step from every worked example already in the prompts, with
   nothing telling the system to look for it.
7. **An operator error the system's own rule caught.** I told it a departed champion had also been
   economic buyer. The record's own v1 data said otherwise. The grounding rule — write to verified
   data, never a tidier narrative — was written to stop the model inventing a cleaner story, and it
   happened to also catch a wrong premise from me.

---

## 12. What breaks first

- **False-resolved objections.** A confident SolCon answer gets read as resolution even when the
  underlying concern is still true — the customer accepted its cost, not that it went away. This
  already happened once in testing, on the Sightline control deal — caught it, added the explicit
  test for whether the concern itself became untrue, not just whether the customer reacted well
  (§11.4). It happened again independently while building the eval harness (§8), on the same deal,
  on a different objection — this is a real, recurring failure mode, not a one-off. Detection in
  production: SolCon correction rate on the objection block.
- **Objections mis-filed as competitive mentions.** Pricing or procurement pushback tied to a
  competitor's name gets filed only as a competitor note, making it invisible to exit criteria and
  action items. Also already happened, on Northwind — caught and fixed (§11.6).
- **Adoption decay after week three.** No correction to point to here, which is the point — I
  don't have evidence either way, and five days of synthetic deals can't produce it. It's a
  product problem, not a technical one: the system has to be less work than the status quo. What
  I'd watch is whether reminder-to-resolution rate holds or declines. If it decays, I'd rebuild
  the surface rather than add more reminders.
