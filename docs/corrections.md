# Corrections log

Running log of every correction made to the prompts, the contract, or the pipeline code, and why. Kept per `docs/build-plan.md` §6: *"the assessment explicitly evaluates 'where you had to override the AI or correct it.'"*

---

## 1. Spec defect — `confidence` missing from four contract fields

**Found:** during reconciliation of `docs/build-plan.md` §3 into `docs/record-contract.md`.

§3 states the design principle explicitly: *"Every inference carries a confidence field. The system is allowed to say 'unknown.'"* But §3's own JSON example only puts `confidence` on `stakeholders`, `objections`, and `next_step` — it's missing from `integration_patterns.agreed`, `competitive.evaluation_status`, `product_relevance`, and `open_risks.severity`, all of which are judgment calls, not transcriptions.

**Fix:** added `confidence` to those four fields in `docs/record-contract.md` so the stated principle actually holds everywhere it should. `success_criteria` was left without one — it's closer to a verbatim-plus-restatement than a judgment call.

---

## 2. Retrieval bug — hyphenated tags could never match

**Found:** while building `scripts/query_knowledge.py`, before it had been run against real data.

The tag tokenizer stripped punctuation before matching (`re.findall(r"[a-zA-Z]+", term.lower())`), so a term containing a hyphenated word — e.g. `self-serve` — was split into separate tokens (`self`, `serve`), neither of which equals the actual tag string in `knowledge.tags` (`"self-serve"`, `"audience-builder"`, and similar compound tags are stored as single hyphenated strings). Retrieval against any compound tag would silently return nothing.

This is a system-level failure, not a content-level one, and the more dangerous kind: nothing about the output would have looked wrong. Pass 2 is instructed to ground `product_relevance`/`competitive` only in what's actually retrieved and to drop ungrounded candidates rather than invent — so with retrieval silently empty, a real, groundable need would just quietly disappear from the record instead of erroring. The record would read as complete and confident while actually missing a field it should have populated.

**Fix:** rewrote the tokenizer to preserve internal hyphens (`re.findall(r"[a-zA-Z]+(?:-[a-zA-Z]+)*", term.lower())`), so a term like `"self-serve segment builder"` now produces the token `self-serve` intact instead of two fragments.

---

## 3. Recall gap — pass 1 missed an unnamed competitor mention; pass 2's reasoning was never actually tested

**Found:** reviewing Sightline v1's `competitive: []` output. The transcript contains an unnamed prior vendor Amara describes ("we tried a 'self-serve' tool a few years back, different vendor") — a real competitive candidate, closed/historical but genuinely present in the call.

The record read as if the system had correctly judged this mention immaterial. It hadn't judged it at all: pass 1 never extracted it as a `competitive_mentions` candidate in the first place, because `01_extract.md` framed the field around `"vendor": "name as spoken"` and nothing told pass 1 to flag a vendor reference that came with no name attached. Pass 2 received nothing to reason about, and its (separately, correctly) improved judgment — evaluate a mention on its own merits, never by consulting `docs/deal-spec.md` — was consequently never exercised on real input. A downstream fix looked complete but was untestable, because the candidate it was meant to judge had already been silently dropped one stage earlier. The lesson: when an output looks right, check whether the stage responsible actually ran on the relevant input, not just whether the final field looks correct.

**Fix:** `01_extract.md` now explicitly instructs pass 1 to extract any reference to another vendor, tool, or prior evaluation — named or not, current or historical — using a description in place of a name when none is given. Classification stays pass 2's job; pass 1's job is to not miss it.

---

## 4. Classification rule tightened — `resolved` requires the concern to be closed, not just accepted

**Found:** re-reviewing Sightline's obj_04 (whether the visual builder handles genuinely complex segment logic) after fixing #3 above and re-running the chain.

The original `resolved` rule only tested for customer acceptance ("did the customer react and agree?"). That's necessary but not sufficient. In obj_04, Aditi concedes a real, standing limitation — genuine edge cases (e.g. rolling-window comparisons) still need someone technical — and Paul explicitly accepts that as a workable tradeoff ("it's not call Paul every time"). Customer acceptance is unambiguous, but the underlying concern (does this fall back to needing someone technical?) is still true; Paul agreed to live with it, not that it isn't so. Under the original rule this classified as `resolved`. It should be `partially_resolved`: acceptance of a conceded limitation is a different thing from the concern itself becoming untrue.

**Fix:** `02_consolidate.md`'s resolved-vs-partially_resolved rule now asks explicitly: did the answer make the original concern no longer true, or did it make the concern's cost acceptable? Only the former is `resolved`. Re-running the chain with this rule reclassified obj_04 as `partially_resolved`, while obj_01–03 (where the vendor's answer genuinely negated the underlying fear, not just its cost) correctly stayed `resolved`.

---

## 5. Closure-tracking limitation — the AE evidence rule produces a false positive

**Found:** running `scripts/check_closure.py` for real against Meridian's seeded action items, not pre-rigging the outcome.

The AE closure rule (`docs/enforcement-layer-spec.md` §2's own wording: "a matching row in `activities` after the item was created") is intentionally loose — any logged activity by that AE after the item's creation counts as evidence, not a check that the *specific* action happened. Meridian's "redirect the proposal to Priya" item (created 2026-09-02, restated in v3) came back `completed`, but the qualifying evidence was an unrelated tokenization-question email (Sep 3) and the call 3 transcript itself (Sep 12) — neither is proof the proposal was actually sent. It's very likely still outstanding. The adjacent "resend the SOC 2 report" item, created same-day (v3, Sep 15), correctly came back `missed` — nothing dated after it exists yet.

**Not fixed.** This is a genuine, load-bearing limitation of the simple heuristic, not a bug — the spec's own rule is this loose by design, and tightening it (e.g., requiring the activity's `subject` to match the item, or occur after `due_date` rather than `created_at`) needs either a real subject-matching step or a different evidence model than "any row exists." Flagging it here rather than quietly re-seeding data to avoid the awkward result: **absence of evidence is a strong, conservative signal (correctly drove the SOC 2 item to `missed`); presence of evidence is a weak one, and the dashboard/escalation layers built on top of this should not treat "completed" as certain** the way "missed" can be.

---

## 6. Recall gap — commercial/procurement pushback was captured as competitive context only, never as an objection

**Found:** reviewing Northwind v2 by hand. Owen Brady's challenge — Tracewell's lower price, an existing master services agreement through their parent company easing Northwind's procurement, and Rachel's first answer dodging the actual question — produced a rich `competitive` entry for Tracewell (correctly classified `actively_evaluating`, correctly grounded in the retrieved battlecard) but zero `objections` entries. Objections stayed at 7, unchanged from v1, across a call whose entire second half was a customer directly and repeatedly saying some version of "give me a commercial reason to pick you over them, or I don't know what I tell my boss."

That's the deal's actual blocker as of v2, and it was invisible to `stage_exit_criteria`, `whats_blocking`, and the action items — all of which read `objections`, not `competitive`. A reader of the record would see "3 of 5 stage exit criteria met, integration approach agreed, economic buyer identified" and a competitive mention buried in prose, not a tracked, open, customer-articulated concern.

Root cause was structural, not a one-off misjudgment: neither `01_extract.md`'s `objections` recall guidance nor `02_consolidate.md`'s `competitive` field guidance ever said a commercial challenge tied to a competitor's name belongs in *both* fields. Every worked example already in the system (Meridian's PII/BAA thread, Sightline's tool-burn skepticism) was a technical or security concern, so nothing forced the distinction between "a competitor was mentioned" and "the customer has an unresolved concern, which happens to be about a competitor" into view. This is the same shape as correction #3 (pass 1 missing an unnamed vendor mention because nothing told it to look) — a category of real content with no explicit instruction pointing at it, sitting one inferential step away from every example the prompts already contained.

**Fix:** `01_extract.md` gained an "Objections aren't only technical" section instructing pass 1 to extract a commercial/competitive challenge as an `objections` candidate in addition to a `competitive_mentions` candidate, not instead of one. `02_consolidate.md` gained a "Competitive pressure that reads as an objection gets both" section making the same point at the classification stage, including the instruction to split price and procurement friction into two separate objections when the customer named both as distinct gaps, since they resolve on different tracks (AE pricing work versus deal-desk/legal procurement work) and the schema only allows one `category` per objection. Re-ran Northwind v2's pass 2 and pass 3 with the corrected prompts: two new objections landed (`obj_08` pricing, `obj_09` procurement), both `open`, both feeding `stage_exit_criteria` criterion 1's `reason` and `whats_blocking` directly instead of living only in prose.

---

## 7. Operator error — the build instruction for Meridian's handoff misstated v1's stakeholder data, the grounding rule caught it

**Found:** building `prompts/05_handoff.md` (Pass 5, CS handoff) against Meridian. The build instruction stated as given fact that "Derek was champion and economic buyer at v1." The actual v1 record does not support that: Derek's `role_inference` is `champion` only, and v1's own `open_risks` explicitly notes no economic buyer had engaged with the deal at that point. The premise wasn't a judgment call gone wrong upstream in the chain — it was simply incorrect input at the instruction level, stated with the same confidence as the rest of the spec.

This is a different failure class from corrections #3 and #6 above (a category of real content the prompts never told a pass to look for). Here the content existed, was already correctly captured in the Record, and the risk was purely that a confidently stated instruction would override verified data rather than the other way around. `04_render.md`'s existing rule — ground every role in the Record's actual `role_inference`, never upgrade a departed champion to economic buyer without evidence — was written for a different purpose (don't let a tidier narrative override the data) but happened to be exactly the rule that also protects against a wrong human-supplied premise. `05_handoff.md` reuses that same rule verbatim for this reason.

**Fix:** none needed to the prompts or the pipeline — the rule that caught this was already in place. The handoff was written to the verified v1 data (Derek: champion only; Priya: the first person on the deal anyone identified as economic buyer, arriving at v3) and the discrepancy was surfaced back to the operator rather than silently corrected or silently complied with. Logging this because it's worth having on record as a case where the grounding discipline did its job against bad input from the human side of the process, not just against a model's own drift.
