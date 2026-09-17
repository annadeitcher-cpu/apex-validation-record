# Apex Assessment — Handoff

**Context for a fresh conversation.** I'm an internal Braze candidate for Applied AI Architect, GTM. Final round is a 60-minute panel: 20 min presentation, 40 min discussion. Panel is a Senior AVP of Technical Solutions (internal solutions, not SC org leadership), a VP of Competitive and Monetization Strategy, a sales VP, and the person heading the new Applied AI team.

**Assessment ask:** analyze a fictional B2B SaaS company (Apex), pick a problem from the scenario packet, design an AI solution, build a working prototype, and define measurement. Materials due 24 hours before the session.

**Where I am:** Day 1 complete. Day 2 starting — the extraction chain.

---

## The problem I chose

**The post-technical-validation dead zone.**

- Technical Validation is the only stage that moved: 12 → 14 → 23 avg days over three quarters. Discovery, Commercial Negotiation, and Legal all held flat.
- It's the stage most correlated with winning: 68% win rate under 7 days, 41% at 7–14, 22% past 14.
- The behavioral gap is measurable: top-quartile AEs make 2.3 touches in the 14 days post-demo, bottom quartile 0.7.
- It compounds downstream: sales cycle length vs. time-to-first-value correlates at r=0.71.
- Six qualitative signals converge: AE with no playbook for that moment, manager watching average reps wait, SC who never hears how it went, CS manager inheriting drifted expectations, enablement lead whose guide is dead in Confluence, plus the packet's own note that SC summaries complete ~60% of the time and nothing flows to post-sales.

**Deprioritized:** differentiation (content problem, spans all stages, PMM owns half), product release velocity (same shape), BDR sequencing tool (procurement problem; BDR pipeline is flat — 4.2/5.1/4.8 is noise), buying committee blindness (a field of the solution, not a system).

**But not dropped** — differentiation and release velocity are folded into the solution via grounded competitive positioning and product relevance, surfaced at the moment they convert. That's the answer to "why didn't you solve differentiation," and it's a working example rather than an argument.

---

## The solution

**The Validation Record** — a structured deal object, scoped to the **opportunity** (not the call), that accrues across calls and renders to four consumers in Slack.

One object, four renderings:
- **Pinned canvas/message in the deal channel** — the Record itself, updated in place as the deal progresses
- **Channel post** — "what changed," only on material events
- **AE DM** — drafted follow-up email (drafts only, never sends), recommended next step, open risks
- **SC DM** — pre-drafted summary doc to approve/correct, plus a loop-close when the deal advances
- **CS** — inherits a current Record at handoff, having watched it accrue in-channel for weeks
- **Manager** — one escalation at day 7, surfaced in the existing pipeline review

**Key design positions to defend:**
- **Information public, accountability private.** The artifact is public in the deal channel; the nudge is a DM. A public nudge is a public shaming and reps route around systems that embarrass them.
- **Hygiene through subtraction.** SC completion goes 60% → 90% because the doc arrives pre-drafted, not because of reminders. Every hygiene win comes from deleting work, not adding it.
- **One nudge, one escalation.** The more this nags, the faster it dies, so it nags once.
- **Batch off the warehouse, not per-call Gong API calls.** Cheaper, idempotent, replayable, re-runnable when prompts improve. Supabase stands in for Snowflake.
- **Accrual is what makes this a system, not a summarizer.** Gong already writes summaries. A summary is prose for one reader at one moment; this is a structured object that accrues, routes to four consumers, and joins to outcomes.

---

## Build state

**Repo:** `~/apex`. Supabase project `whnrhddhpzrsgseonhmc`. Personal Claude Code with Supabase MCP.

### Done
- Schema applied: `accounts`, `opportunities`, `calls`, `participants`, `transcripts`, `validation_records` (versioned), `record_events` (diff log with materiality gating), `activities`, `notifications`, `knowledge`
- `seed_structure.py` — six opportunities, idempotent, **deterministic uuid5 IDs** derived from natural keys
- **Nine transcripts** generated, QA'd, loaded, verified. 22k–51k chars each.
- `seed_knowledge.py` — 8 rows: 5 Apex release notes (Streamline Ingest, Segment Studio 2.0, Lineage Graph, Consent Sync, Warehouse Native Activation), 3 battlecards (Tracewell, Corvus, Anchorpoint Systems)
- `qa_transcript.py` — automated transcript QA (escaping, frontmatter, word count vs. duration, absolute dates, consecutive-speaker turns, hedge/interruption density)
- Slack workspace + app created. Bot token and `#deal-meridian-health` channel ID in `.env`. **Smoke test not yet confirmed run.**

### The date thing (important)
All dates in `seed_structure.py` are **relative offsets from a `REFERENCE_DATE`** env var, not absolute dates. Reason: Meridian must read exactly 23 days in Technical Validation on demo day, because 23 is Apex's Q3 average and the line "twenty-three days" is in the presentation. If dates were absolute they'd drift.

UUIDs are deterministic (uuid5 on natural keys) specifically so re-seeding with a new `REFERENCE_DATE` doesn't orphan the `validation_records`, `record_events`, and `notifications` generated against the old IDs.

**Action required the morning of the panel:** re-run `seed_structure.py` with `REFERENCE_DATE` set to that day, then re-run `load_transcripts.py`, then regenerate the Records. Verify Meridian reads 23 days and Ardent reads 4 with a null `last_activity`.

Also: **no absolute calendar dates, months, years, or quarters appear in any transcript dialogue** — people say "next Tuesday," "end of the month." This was deliberate so re-anchoring never contradicts the transcripts.

### Next (Day 2)
1. Three-pass extraction chain — prompts in `prompts/` as separate `.md` files so they're iterable
2. Retrieval step in pass 2 — query `knowledge` on extracted competitor names and unmet needs
3. Run on Sightline first (the control), read by eye, then iterate
4. Eval harness against hand labels
5. Full corpus run, check the trap cases

### Then
- **Day 3:** diff/materiality logic, Slack rendering. Try canvas first (`canvases:write`, `conversations.canvases.create`); if it 403s on the free plan, fall back to a pinned message with `chat.update`. Build the renderer format-agnostic with two thin adapters so the swap costs nothing.
- **Day 4:** Meridian accrual sequence end to end, thin renderings for SC/CS/manager (hardcoded mocks are fine, label them as such in the deck), measurement slides, failure modes, **recorded backup demo**.
- **Day 5:** deck, rehearse to 20 min, send materials 24h ahead.

---

## The demo — four commands and a Slack channel

```bash
python scripts/run_extraction.py --deal meridian --through-call 1   # Record v1 posts + pins; AE gets drafted email
python scripts/run_extraction.py --deal meridian --through-call 2   # v2 — pin updates IN PLACE; "what changed" post
python scripts/run_extraction.py --deal meridian --through-call 3   # v3 — objection resurfaced + champion changed; SC loop-close
python scripts/run_nudge.py                                        # finds Ardent, DMs the AE once
```

Demo order: show the channel silent after the technical validation (that screenshot *is* the problem) → run call 1, walk the Record slowly → show the AE's drafted email, note it never auto-sends → advance three weeks, run calls 2 and 3, watch the pin change → jump to close, show CS inherited a current record → Ardent nudge, deliver the public-vs-private line.

---

## The synthetic corpus — what each transcript tests

| Deal | Calls | Purpose |
|---|---|---|
| **Meridian Health** ($310K, Ent, 23 days in stage) | 3 | **The demo arc.** Curtis Nam raises a PII concern in call 1 and **explicitly accepts** the resolution. Call 3: Derek Osei (champion) has left, **Priya Raman** (VP Data Platform) arrives cold and reopens the same concern in **entirely different vocabulary** — PHI, staging layer, BAA, HIPAA vs. Curtis's encryption, tokenization, HSM. Curtis pushes back that it was settled. Tests semantic tracking, not string matching. Call 2 resolves a Teradata/Snowflake sourcing question with a wrinkle preserved. |
| **Northwind Logistics** ($180K, Ent) | 2 | Call 1: **Corvus** mentioned — solicited, historical, already rejected. **False-positive trap**: should classify `mentioned_only`, must NOT trigger `competitor_introduced`. Call 2: **Owen Brady** (RevOps) arrives with **active competitive pressure — Tracewell**, lower price, 3-week pilot, and an existing master agreement between Northwind's finance org and Tracewell's parent that eases procurement. Rachel Kim pivots to a feature answer, gets called on the dodge, course-corrects. This is the Chicago AE's problem in dialogue. **Material: `competitor_introduced`. Minor: `stakeholder_added`.** Tracewell's battlecard contains the answer Rachel didn't have. |
| **Calibre Financial** ($420K, Ent) | 1 | **The hard case.** An `UNIDENTIFIED:` speaker who contributes substantively but never introduces themselves (→ `role_inference: unknown`, low confidence). Genuine crosstalk. **No next step** — ends on "we'll probably want to loop in Renata," no owner, no date (→ `next_step.present: false`). Two or three objections in genuinely arguable states. |
| **Sightline Retail** ($85K, MM, 4 days in stage) | 1 | **The control.** Clean execution, 68%-win-rate profile. Amara Diallo is `economic_buyer` by **behavior** (has allocated budget, VP is a courtesy). Traps: Deepa (VP Mktg) and Marcus (IT) are mentioned but never attend — must not be promoted to attendees. An unnamed prior vendor → `mentioned_only`. |
| **Vantage Media** ($240K, Ent) | 1 | **The product-relevance plant.** Hallie Brooks describes 4–5 hrs/week manually reconciling consent and suppression lists across email, push, and paid social, including a stale-export incident that reached leadership. **Daniel and Aditi never connect it to Consent Sync** — they're compressing the agenda after running long. Sung-min Park is `economic_buyer` (owns the budget line, CFO is courtesy). Reads as a natural miss under time pressure, not incompetence. |
| **Ardent Manufacturing** ($150K, Ent, 4 days in stage) | 1 | **The nudge.** An ordinary call that goes fine. Next step discussed but never lands — no owner, no date. Greg Lindqvist is competent but passive. **Zero rows in `activities`** — that absence is the entire demo beat. |

**Note on execution variance:** Marcus Webb demos Consent Sync competently at Meridian while Aditi Sharma misses it at Vantage. This is deliberate — it's Apex's stated problem ("execution varies significantly across the team"), not an inconsistency.

---

## Extraction chain design

Three passes, prompts as separate files so they're iterable. `claude-sonnet-4-6`.

**Pass 1 — extract.** Full transcript + participant list. **No chunking** — longest is 51k chars / ~13k tokens, fits in context. Bias toward recall. Every candidate carries a verbatim evidence quote.

**Pass 2 — consolidate, retrieve, classify.** Code pulls competitor names and unmet needs out of pass 1, queries `knowledge` on subject/tags, passes only matching rows into the prompt. Then: dedupe, categorize, classify objection status, infer stakeholder roles, ground competitive and product_relevance in retrieved content only.

Two rules that matter most:
- **Resolved requires customer acceptance on the record.** A confident vendor answer is not resolution. SC-only → `partially_resolved`.
- **Roles from behavior, not title.** Who asks about budget, who defers to whom, who owns timeline. `unknown` is valid and preferred over a guess.

Every inference carries a confidence field.

**Pass 3 — merge.** Consolidated extraction + prior version → new version + change events. Detect **semantically**: `objection_resurfaced`, `objection_resolved`, `stakeholder_added`, `champion_changed`, `next_step_missing`, `competitor_introduced`. Tag each `material` or `minor`.

**On retrieval scale:** 8 knowledge rows means keyword lookup is correct and vector search would be over-engineering. The interface is the same either way — that's the answer if asked.

---

## Eval harness

12 hand-labeled transcripts, scored on:

| Metric | Target |
|---|---|
| Objection recall | > 90% |
| Objection status accuracy | > 85% |
| Stakeholder role accuracy (excl. `unknown`) | > 80% |
| Next-step presence detection | > 95% |
| **Hallucinated commitments** | **0 — zero tolerance** |

**Status: labels not yet written.** Needs doing, ideally alongside reading each Record.

If Day 2 runs long, score objection recall and hallucinated commitments only. Two real numbers beat five aspirational ones.

---

## Measurement framework

**30 days — adoption:** coverage (% of TV calls producing a complete Record), **edit-and-send rate on the drafted email within 48h** (the real adoption metric — opens don't count), SC summary completion 60% → 90%, median hours demo → first logged touch.

**60 days — behavior:** post-demo touches, **bottom quartile 0.7 → 1.5** (the headline number), middle 50% 1.1 → 1.8, % of deals exiting TV with a logged next step, % with an identified economic buyer before Commercial Negotiation.

**90 days — impact:** avg days in TV **23 → 16**, win rate for Record-covered deals **vs. a holdout cohort**, CS time-to-first-value against the r=0.71 baseline, % of closed-won arriving at CS with a Record < 7 days stale.

**Continuous:** weekly eval harness run; **nudge dismissal rate** as a counter-metric (climbs → the nudge is miscalibrated and gets turned down — own kill switch); SC correction rate on Records.

**Say unprompted:** the 68/41/22 table is **correlational**. Slow deals may simply be bad deals. Compressing time-in-stage doesn't convert a 22% deal into a 68% deal. That's why the 90-day measure is a holdout, not a before/after. Naming this before the panel does is the highest-credibility move available.

---

## What breaks first

1. **False-resolved objections** — highest probability. Detection: SC correction rate on the objection block. Mitigation: require customer acceptance evidence; default to `partially_resolved`.
2. **Notification fatigue** — materiality gate too loose → channel gets muted. Detection: mute rate, dismissal rate, declining opens. Mitigation: tighten the gate, a config change not a rebuild.
3. **Silent extraction failure** on atypical calls (multi-language, bad audio, a working session rather than a demo). Mitigation: `status: failed` is visible and alerts; never post a partial silently.
4. **Drafted email sent unedited and wrong.** Mitigation: drafts only, hallucinated-commitment counter at zero.
5. **Adoption decay after week 3** — the real risk, and a product problem not a technical one. Detection: edit-and-send rate trend. Mitigation: the system must be *less* work than the status quo. That's why every hygiene mechanism is subtractive.

---

## Q&A positions

**"Gong already writes summaries."** A summary is prose for one reader at one moment. This is a structured object that accrues across calls, routes to four consumers in different renderings, and writes to a warehouse I can join to outcomes. You can't query a summary, diff it, or measure against it.

**"Cost at 300 people?"** Batch off the warehouse, one extraction per new call on active opportunities. Re-runnable when prompts improve without re-pulling from Gong.

**"Customer call content in Slack — security?"** Deal channels are internal and access-controlled. The Record contains strictly less than what's already in Gong, which the same people can already see. Verbatim quotes limited to evidence lines. If policy requires, the channel post can carry a summary with the full record behind a link. The prototype itself uses **100% synthetic data — no real customer content anywhere.**

**"What if reps ignore it?"** The real risk. Every hygiene mechanism is subtractive — the SC doc gets done because I deleted the work, not because I added a reminder. The metric that matters is edit-and-send rate, not opens. If it decays after week 3, the system isn't less work than the status quo and I'd rebuild the surface, not add nagging.

**"What would you build next?"** The pattern library across Records — which objection-handling approaches precede advancement, which integration concerns recur by vertical, which competitor mentions correlate with stall. Framed as a **shared SC asset, not an individual scorecard.** Needs about a quarter of volume before the patterns are trustworthy; I wouldn't ship it on thin data.

---

## Scope guardrails

**Do not build:** a web UI (Slack is the interface, Supabase's table view is the admin panel — this is the single biggest time sink and the assessment explicitly says not to polish); real Gong/Salesforce/Snowflake integration (draw the boundary on one slide); cron or orchestration (trigger by command, the schedule is a sentence); retry logic or idempotency guards for cases the demo never hits (*describe* them; implement only the diff logic, which is load-bearing).

**Compressions available if time runs short:** build only the pinned Record and AE DM properly — SC loop-close, CS handoff, and manager escalation can be one hardcoded example each, labeled as mocks. Score only objection recall and hallucinated commitments in the eval.

**Do not compress:** Meridian 3's accrual demo, extraction quality iteration, the recorded backup demo.

---

## Correction log

Keep this current — the assessment explicitly evaluates "where you had to override the AI or correct it." Entries so far:

- **Refactored all dates to relative offsets.** Absolute dates would have drifted past the reference date before the panel, breaking the "23 days matches Apex's Q3 average" line.
- **Made UUIDs deterministic (uuid5).** Runtime UUIDs meant re-seeding on demo morning would orphan every generated Record.
- **Forced an open thread into Meridian 1.** The first two transcripts resolved every objection cleanly, which would have left the extraction chain with no `open` or `partially_resolved` examples to calibrate against.
- **Caught Sightline resolving 5-for-5** and required subsequent transcripts to leave threads open.
- **Moved Northwind's competitive plant from call 1 to call 2.** The call-1 Corvus mention came out solicited and historical rather than casual and active, leaving the corpus with two historical-vendor cases and zero active competition — which would have left the differentiation demo beat with nothing to run on. Kept call 1 as a deliberate false-positive trap instead of regenerating.
- **Skipped chunking in pass 1.** Transcripts fit in context; chunking would have added complexity for no benefit. Noted as a production consideration.
- **Insisted on real retrieval over context-stuffing** despite only 8 knowledge rows, because the interface is what generalizes.
- **Required Vantage's miss to have a visible cause.** Without the time-pressure setup the transcript reads as a strawman and the demo beat loses force.
- **Fixed consecutive-same-speaker turns** across the first three transcripts — a recurring generation artifact that passes structural checks but can confuse speaker attribution.

---

## Files in the repo

```
apex/
├── docs/
│   ├── build-plan.md                      # full plan: field spec §3, architecture §4, chain §6
│   ├── deal-spec.md                       # the six deals, what each tests
│   ├── transcript-generation-process.md    # standing rules, per-deal fills, QA checklist
│   ├── day1-setup.md
│   ├── corrections.md                      # the log above
│   └── Applied_AI_Architect__GTM_Assessment.pdf   # the scenario packet — NEEDS ADDING
├── sql/schema.sql
├── scripts/
│   ├── db.py
│   ├── seed_structure.py
│   ├── seed_knowledge.py
│   ├── load_transcripts.py
│   ├── qa_transcript.py
│   └── slack_check.py                      # written? smoke test not confirmed
├── transcripts/     # 9 files
├── prompts/         # Day 2
└── evals/           # labels not yet written
```

---

## Immediate next actions

1. **Confirm the Slack smoke test ran** — `chat.update` and `pins.add` working is a hard Day 3 dependency
2. **Add the assessment PDF to `docs/`** — Claude Code has never seen the source scenario packet, only my derived spec
3. **Write eval labels** for the six transcripts already read, before memory fades
4. **Build the extraction chain**, run on Sightline, read against labels, iterate
