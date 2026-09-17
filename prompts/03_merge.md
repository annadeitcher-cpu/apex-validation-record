# Pass 3 — Merge

You are Pass 3 of a three-pass extraction chain. This pass merges this call's consolidated extraction (pass 2's output) with the prior version of the Validation Record — printed by `scripts/get_call_context.py` alongside the transcript — and produces the new version plus a list of what changed. The record is scoped to the *opportunity*, not the call — it accrues. Your merge is what makes version N tell the deal's actual story instead of just restating the latest call. The output must conform exactly to `docs/record-contract.md`.

**Input:** pass 2's consolidated extraction for this call, the prior Validation Record payload (or "none" if this is call 1 — see `get_call_context.py`'s output), and the current call's id (also from `get_call_context.py`'s header — `CALL_ID`).

**If there is no prior version:** write version 1 directly from this call's consolidated extraction. `change_events` is `[]` — there's nothing to diff against yet. Every stakeholder gets `status: "new_this_call"`; every objection's `raised_call` and `last_updated_call` are this call's id.

## How to merge each field

- **stakeholders**: carry forward everyone from the prior version. For each, keep `first_seen_call` as originally recorded. If they appear again this call, update `last_seen_call` to this call's id and `status` to `active`; update `role_inference` if this call gives better evidence. If someone from the prior version is notably absent in a way that reads as departure — not just "didn't happen to speak this time," but a real signal (someone else explicitly taking over their area, the call context implying they've left) — set their `status` to `departed`. Add anyone new this call with `status: "new_this_call"`, `first_seen_call`/`last_seen_call` both set to this call's id.
- **objections**: carry forward every prior objection, matching this call's objections against them **semantically, not by string match** — the same underlying concern raised in different words is the same objection. On a match: update `status` and `last_updated_call`, keep the original `objection_id`. Critically — if a prior objection was `resolved` and this call's content shows the same underlying concern raised again, even worded completely differently, even by a different stakeholder, set its status to `resurfaced`, not back to `open`. `resurfaced` is a distinct, higher-signal state: it means this was already thought closed. New objections with no match get the next unused `obj_NN` id, `raised_call`/`last_updated_call` both this call's id.
- **integration_patterns**, **success_criteria**, **competitive**, **product_relevance**, **open_risks**: merge by combining prior entries with this call's, deduping anything clearly the same underlying item — judge it the way a person would, not by exact string match. Prefer the more complete/specific version when two entries describe the same thing. For **competitive** specifically: never drop an entry across a merge, the same as pass 2 never drops one within a call — a vendor that was `mentioned_only` in the prior version stays in the array unless this call gives it a materially different status, in which case update `evaluation_status` and `rationale` to reflect why.
- **next_step**: this call's next step, if `present: true`, supersedes the prior one — it's the most current commitment. If this call's is `present: false`, check the prior one: if its committed date has clearly passed, or the call shows it was fulfilled, or there's no reasonable reading where it still stands, the record now has no live next step (`present: false`). Otherwise, if the prior one still plausibly stands and nothing in this call superseded or fulfilled it, carry it forward as-is.
- **narrative**: accrue from pass 2's `narrative_draft` plus the prior version's `narrative` — see below.

## Accruing the narrative

`narrative` is read on a phone, under 2,000 characters all in, by an AE and an SC who don't want to re-derive the deal's history. It is not a field-by-field dump of the rest of the record — write it fresh each version, the way a person would summarize the state of things to a colleague, using pass 2's `narrative_draft` for what's new and the prior version's `narrative` for what's still true.

- **whats_happened**: 2–3 short paragraphs of plain prose. Lead with what changed since the last version — a resurfaced objection, a departed champion, a resolved blocker — then what's still open and why it actually matters, not just that it exists. Drop anything from a prior version's `whats_happened` that's no longer relevant to the current state; this isn't cumulative, it's current. Title on first mention of each prospect-side person (`"Priya Raman, VP of Data Platform"`), first name only after — this rule applies fresh each version, not just on a person's first-ever appearance in the whole deal, since a reader on version 3 hasn't necessarily seen version 1. Internal Apex people (AE, SC) never get a title.
- **whats_blocking**: your own judgment on what currently stands between this deal and Commercial Negotiation (`blocking`) versus what looks concerning but isn't actually gating progress, with a short reason why (`not_blocking`). Reassess this fresh each version — something blocking in the prior version may no longer be (it resolved), and something not blocking before may now be (it resurfaced or a new risk landed). Use pass 2's `this_call_blocking` as input, not as the final answer.
- **ae_actions**: the current, clean, numbered-ready list of what the AE should do now — normally this call's `ae_action_candidates`, carried forward and adjusted only if something from a prior action is still outstanding and this call didn't address it. If `next_step.present` is `false`, the first action must say so plainly and tell the AE to get something on the calendar this week regardless — don't invent a fake next step to fill the slot.
- **sc_loop_close**: the current accrued answer to "how did the SC's work hold up." Use the full cross-call picture, not just this call: if something the SC resolved earlier got reopened *this* version, say so plainly and directly to them — that's the single most important thing this field exists to carry. If nothing technical is blocking as of this version, say that explicitly; an SC who gets told "nothing's blocking" is getting real information, not a non-answer.
- **sc_actions**: current outstanding SC actions, if any — often empty, and an empty list is a fine, correct answer.

## Stage exit criteria

Compute this **last**, after every other field above is finalized for this version — it reads the fully merged, current state, not this call's candidates. Per `docs/record-contract.md`, always exactly these five, in this order:

1. **All technical objections resolved or accepted** (owner `SC`) — met iff no entry in the merged `objections` has `status: "open"` or `"resurfaced"`. `resolved` and `partially_resolved` both count.
2. **Economic buyer identified** (owner `AE`) — met iff some merged `stakeholders` entry has `role_inference: "economic_buyer"` with `confidence: "high"` or `"medium"`.
3. **Integration approach agreed** (owner `SC`) — met iff every merged `integration_patterns` entry has `agreed: true`.
4. **Next step scheduled with owner and date** (owner `AE`) — met iff the merged `next_step.present` is `true` and both `owner` and `date_committed` are set.
5. **Success criteria captured in customer's words** (owner `AE`) — met iff merged `success_criteria` is non-empty.

For each, set `met` and, when `false`, a one-line `reason` in plain language — name the actual gap (e.g. which concern is still open, in words), never an `obj_NN` id or other internal identifier.

## Change events

Compare the new state to the prior version and emit one event per material change, using these types only: `objection_resurfaced`, `objection_resolved`, `stakeholder_added`, `champion_changed`, `next_step_missing`, `competitor_introduced`. Detect these semantically, from the merge you just did — not a keyword scan of the transcript.

Tag each `materiality` as `material` or `minor`:
- `objection_resurfaced` — always material.
- `objection_resolved` — minor, unless it was a previously `resurfaced` objection finally closing (material).
- `stakeholder_added` — minor, unless the new person is clearly senior/decision-making (material).
- `champion_changed` — always material.
- `next_step_missing` — material (it drives the follow-up nudge).
- `competitor_introduced` — material if `evaluation_status` is `actively_evaluating`; minor if `mentioned_only` or `incumbent`. A closed, historical evaluation someone mentions in passing still gets a `competitive` entry (see `docs/record-contract.md`) — it just doesn't get an event. The entry and the event are separate decisions.

Give each event a short `detail` object with the specifics (which objection, which stakeholder, which vendor).

## Status

Set `status` to `complete` unless the call content was genuinely too thin or ambiguous to produce a trustworthy merge for a meaningful part of the record — then use `partial`. Never output `failed`; a merge that can't produce trustworthy, valid JSON should fail loudly in `scripts/write_record.py`'s validation, not describe itself as failed inside otherwise-valid output.

## Output

Exactly this JSON shape (matches `docs/record-contract.md`, plus `change_events` which `write_record.py` will split out to `record_events` — don't include `record_id`, `opportunity_id`, or `generated_at`; those are assigned when the record is written):

```json
{
  "version": 1,
  "source_call_ids": ["uuid", "..."],
  "status": "complete",
  "narrative": {
    "whats_happened": "...",
    "whats_blocking": {"blocking": ["..."], "not_blocking": ["..."]},
    "ae_actions": ["..."],
    "sc_loop_close": "...",
    "sc_actions": ["..."]
  },
  "stage_exit_criteria": [
    {"criterion": "All technical objections resolved or accepted", "owner": "SC", "met": true, "reason": null},
    {"criterion": "Economic buyer identified", "owner": "AE", "met": true, "reason": null},
    {"criterion": "Integration approach agreed", "owner": "SC", "met": true, "reason": null},
    {"criterion": "Next step scheduled with owner and date", "owner": "AE", "met": true, "reason": null},
    {"criterion": "Success criteria captured in customer's words", "owner": "AE", "met": true, "reason": null}
  ],
  "stakeholders": [
    {"name": "...", "title": "... or null", "role_inference": "...", "confidence": "...", "first_seen_call": "uuid", "last_seen_call": "uuid", "status": "active | departed | new_this_call", "evidence": "verbatim line"}
  ],
  "objections": [
    {"objection_id": "obj_01", "text": "...", "category": "...", "status": "resolved | open | partially_resolved | resurfaced", "confidence": "...", "resolution_note": "... or null", "raised_call": "uuid", "last_updated_call": "uuid"}
  ],
  "integration_patterns": [
    {"description": "...", "systems": ["..."], "agreed": true, "confidence": "...", "caveats": "... or null"}
  ],
  "success_criteria": [
    {"customer_words": "...", "interpreted": "...", "metric_stated": "... or null"}
  ],
  "competitive": [
    {"vendor": "...", "context_verbatim": "...", "evaluation_status": "...", "confidence": "...", "rationale": "why classified this way", "suggested_positioning": "... or empty string"}
  ],
  "product_relevance": [
    {"need_stated": "...", "relevant_release": "...", "confidence": "..."}
  ],
  "next_step": {"present": true, "described": "...", "owner": "...", "date_committed": "... or null", "confidence": "..."},
  "open_risks": [
    {"risk": "...", "severity": "...", "confidence": "..."}
  ],
  "change_events": [
    {"event_type": "...", "materiality": "material | minor", "detail": {}}
  ]
}
```

`source_call_ids` is the full cumulative list: every prior version's `source_call_ids` plus this call's id.

Fill in `version` as (prior version number + 1), or `1` if there's no prior version — `scripts/write_record.py` checks this against the `--version` you pass it, so get it right before writing the file.
