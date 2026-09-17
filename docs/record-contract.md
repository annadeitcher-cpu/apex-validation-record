# Validation Record — Contract

Authoritative schema for the object stored in `validation_records.payload` and validated by `scripts/write_record.py`. This reconciles `docs/build-plan.md` §3 — it is not a rewrite. Read that section first for the *why*; this doc is the *exactly what*.

## Reconciliation note

§3's own design principle is: **"Every inference carries a confidence field. The system is allowed to say 'unknown.'"** But §3's JSON example only puts `confidence` on `stakeholders`, `objections`, and `next_step` — it's missing from `integration_patterns.agreed`, `competitive.evaluation_status`, `product_relevance`, and `open_risks.severity`, which are inferences too (whether the customer actually agreed to a pattern, whether a mention is live competitive risk, whether a need is truly the same thing a release addresses, how severe a risk is). This contract adds `confidence` to those four so the principle actually holds everywhere it should, per the JSON below. `success_criteria` is intentionally excluded — it's closer to a verbatim-plus-restatement than a judgment call, so no confidence field applies there.

Everything else below is unchanged from §3.

## The five things that must survive any future edit to this file

1. `confidence` on every field that involves a judgment call, not just a transcription.
2. `evidence` (verbatim) on every stakeholder; `context_verbatim` (verbatim) on every competitive mention.
3. `resurfaced` as an objection status distinct from `open` — a closed objection coming back is the highest-signal event in the system and must not collapse back into `open`.
4. `next_step.present: false` as a fully-specified object (not a missing/null field) — this is what the 72h nudge reads.
5. `status: "complete" | "partial" | "failed"` on the record itself — a failed extraction must never look like a complete one.

## Schema

```json
{
  "record_id": "uuid",
  "opportunity_id": "uuid",
  "version": 1,
  "source_call_ids": ["uuid"],
  "generated_at": "2026-09-13T14:22:00Z",
  "status": "complete | partial | failed",

  "narrative": {
    "whats_happened": "2-3 short paragraphs of plain prose — what changed since the last version, what's open and why it matters. No field labels, no evidence quotes. Each prospect-side person gets their title on first mention ('Priya Raman, VP of Data Platform'), first name only after. Internal Apex people never get titles.",
    "whats_blocking": {
      "blocking": ["explicit items standing between this deal and Commercial Negotiation"],
      "not_blocking": ["items that could look concerning but aren't actually gating progress, with why"]
    },
    "ae_actions": ["numbered-ready action derived from next_step, synthesized not copy-pasted"],
    "sc_loop_close": "Prose, addressed to the SC: did their prior resolutions hold up this version, did anything they handled get reopened. If nothing technical is blocking, say so explicitly — that's the feedback an SC otherwise never gets.",
    "sc_actions": ["optional — may be an empty list"]
  },

  "stage_exit_criteria": [
    {"criterion": "All technical objections resolved or accepted", "owner": "SC", "met": true, "reason": null},
    {"criterion": "Economic buyer identified", "owner": "AE", "met": true, "reason": null},
    {"criterion": "Integration approach agreed", "owner": "SC", "met": true, "reason": null},
    {"criterion": "Next step scheduled with owner and date", "owner": "AE", "met": true, "reason": null},
    {"criterion": "Success criteria captured in customer's words", "owner": "AE", "met": true, "reason": null}
  ],

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
    "confidence": "high | medium | low",
    "resolution_note": "SC walked through field-level encryption; customer accepted (or null if unresolved)",
    "raised_call": "uuid",
    "last_updated_call": "uuid"
  }],

  "integration_patterns": [{
    "description": "Snowflake reverse-ETL via existing Fivetran instance",
    "systems": ["Snowflake", "Fivetran"],
    "agreed": true,
    "confidence": "high | medium | low",
    "caveats": "Pending confirmation their Fivetran plan supports the connector (or null)"
  }],

  "success_criteria": [{
    "customer_words": "verbatim quote",
    "interpreted": "plain restatement",
    "metric_stated": "reduce segment build time from 3 days to same-day (or null)"
  }],

  "competitive": [{
    "vendor": "Vendor X",
    "context_verbatim": "what the prospect actually said",
    "evaluation_status": "actively_evaluating | incumbent | mentioned_only",
    "confidence": "high | medium | low",
    "rationale": "why this classification — live vs. historical, named vs. not; not the same as suggested_positioning",
    "suggested_positioning": "grounded in retrieved knowledge only — empty string if nothing was retrieved, never invented"
  }],

  "product_relevance": [{
    "need_stated": "verbatim need the customer raised",
    "relevant_release": "Release name + one line on why it applies",
    "confidence": "high | medium | low"
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
    "severity": "high | medium | low",
    "confidence": "high | medium | low"
  }]
}
```

### `stage_exit_criteria`

Per `docs/enforcement-layer-spec.md` §1. Always exactly these five entries, in this fixed order — never add, drop, or reorder them per-deal:

1. **All technical objections resolved or accepted** (owner `SC`) — met iff no entry in `objections` has `status: "open"` or `status: "resurfaced"`. `resolved` and `partially_resolved` both count as accepted; `partially_resolved` means the customer explicitly accepted a tradeoff, which is a real accept, not a gap.
2. **Economic buyer identified** (owner `AE`) — met iff some `stakeholders` entry has `role_inference: "economic_buyer"` with `confidence: "high"` or `"medium"`. A `low`-confidence guess doesn't count.
3. **Integration approach agreed** (owner `SC`) — met iff every entry in `integration_patterns` has `agreed: true`.
4. **Next step scheduled with owner and date** (owner `AE`) — met iff `next_step.present` is `true` and both `owner` and `date_committed` are set (non-null).
5. **Success criteria captured in customer's words** (owner `AE`) — met iff `success_criteria` is non-empty.

`reason` is a one-line, plain-language explanation when `met` is `false` (naming the specific gap, e.g. which objection is still open — never an `obj_NN` identifier), and `null` when `met` is `true`.

**Computed in pass 3, after the merge, not pass 2.** Every criterion above reads a field on the *fully accrued* Record (this version's complete `objections`, `stakeholders`, `integration_patterns`, `next_step`, `success_criteria`) — not one call's consolidated candidates. Pass 2 only ever sees a single call in isolation and has no way to know whether an objection resolved two versions ago is still resolved; only pass 3, after assembling the merged state, actually knows the deal's current standing.

### `competitive` — every flagged mention gets a row, never dropped

If the extraction chain noticed a vendor, tool, or prior-evaluation reference at all, it produces a `competitive` entry — including unnamed and purely historical mentions. `evaluation_status: "mentioned_only"` plus a `rationale` explaining why it's immaterial is the correct outcome for a closed, historical, or throwaway mention; a missing entry is not. An empty `competitive` array must mean "nothing was mentioned," never "something was mentioned and got judged away" — those two cases have to be distinguishable from the record alone, without re-reading the transcript.

### `next_step` when nothing was agreed

Not an omitted key — a fully populated object with `present: false`:

```json
{
  "next_step": {
    "present": false,
    "described": null,
    "owner": null,
    "date_committed": null,
    "confidence": null
  }
}
```

### `status`

- `complete` — every section was extractable with reasonable confidence.
- `partial` — the call content was genuinely too thin or ambiguous for a trustworthy merge on some section, but something usable was still produced. Not a failure; a flagged limitation.
- `failed` — malformed model output, a broken merge, or anything that means the payload can't be trusted. `write_record.py` sets this itself on validation failure; the merge step should never claim `failed` inside otherwise-valid JSON (if the output is that broken, it isn't valid JSON to begin with, and `write_record.py` catches it).

## Change events (`record_events`, not part of the Record payload)

Produced by pass 3 alongside the new version, written to a separate table so the payload stays a clean snapshot of current state:

```json
{
  "event_type": "objection_resurfaced | objection_resolved | stakeholder_added | champion_changed | next_step_missing | competitor_introduced",
  "materiality": "material | minor",
  "detail": { "...": "whatever specifics matter for this event type" }
}
```

Materiality gates notification (§8) — only `material` events produce a channel post. Guidance on tagging lives in `prompts/03_merge.md`.

## Field ownership across passes

Not part of the contract itself, but useful context: nothing in this file is produced whole by one pass. Pass 1 (`prompts/01_extract.md`) produces raw, ungrounded, unclassified candidates with verbatim evidence — recall-optimized, ignore this contract's enums entirely. Pass 2 (`prompts/02_consolidate.md`) is where the enums, confidence levels, and grounding get assigned for *this call only*. Pass 3 (`prompts/03_merge.md`) is the only pass that ever produces something matching this contract exactly — it merges pass 2's output for the current call against the prior version's full payload (already in this shape) and emits the new version plus change events. `scripts/write_record.py` is the only place this contract is mechanically enforced.
