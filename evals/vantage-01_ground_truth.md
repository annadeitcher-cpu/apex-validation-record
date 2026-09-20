# Ground truth — vantage-01

Written by independently reading transcripts/vantage-01.md only. No validation_records row exists
for this opportunity/call yet.

## Stakeholders
- **Sung-min Park**, VP, Audience Data — `economic_buyer`, high confidence. Explicit: "I own this
  budget line directly, this is within my authority to approve... I'll still loop in our CFO's
  office as a courtesy" (not for approval).
- **Hallie Brooks**, Marketing Ops Manager — `influencer`, medium confidence. Reports to Sung-min, no
  budget authority, but drives the most concrete pain-point evidence in the call (the suppression-
  list incident) and visibly shapes scope discussion (raises the rollout-workload question herself).

## Objections
1. **Household/informal account-sharing identity resolution** (integration/other). Aditi is explicit
   there's "no clean technical solution" for the informal case; only an ambiguity flag, not real
   resolution. **Expected status: `open`** for the informal-sharing case specifically.
2. **Formal family-plan identity resolution** — a narrower, separate question Hallie raises
   immediately after. Aditi: "that's actually a cleaner case... can respect it explicitly." Hallie
   confirms they have that exact structure. **Expected status: `resolved`, high confidence** — this
   is a genuinely different, fully-answered sub-case, not a duplicate of #1.
3. **Reliability of probabilistic (device/browser) matching given cookie deprecation** (performance).
   Aditi concedes the industry-wide degradation is real and ongoing, recommends deterministic-first
   as mitigation rather than claiming the underlying problem is solved. **Expected status:
   `partially_resolved`.**
4. **What happens on a failed/mid-refresh audience sync** (performance). "Stale but correct" failure
   mode described and explicitly welcomed by Sung-min as the right default, no remaining concern
   raised. **Expected status: `resolved`, high confidence.**
5. **Will identity-match review become a new bottleneck routed through Sung-min's team** (other/
   integration). Answered directly — reviewable by marketing ops itself, no deep engineering needed.
   Both customer-side people explicitly satisfied. **Expected status: `resolved`.**

## Competitive
**Expected: empty array.** Hallie's aside about a "Daniel" from a prior vendor (lines 76-84) is
about mistaken personal identity, explicitly resolved as not the same person — not a vendor mention.
No other vendor, tool, or prior evaluation appears anywhere in this transcript.

## Next step
Present: true. Daniel (AE) will send a recap plus outstanding detail (lineage, warehouse activation)
and start pricing; a follow-up call is agreed to close out identity edge cases and review pricing.
**Owner: AE. Date committed: expected `null`** — Sung-min says only "I'm fairly open the next couple
weeks," no specific day is named (contrast with Sightline's explicit "next Tuesday"). A chain that
marks `date_committed` as set here is inventing a date that was never spoken. This is a genuine
stage-exit-criterion test: criterion 4 ("next step scheduled with owner *and date*") should read as
**unmet** even though `next_step.present` is true.

## Product relevance — THE PLANT
Hallie describes, in detail and at length (lines 294–310), manually reconciling consent/suppression
state across email, push, and paid social — no shared source of truth, a real incident where a stale
export led to customers who'd unsubscribed from email still getting hit with paid social remarketing,
which became a visible embarrassment that reached leadership. **Neither Daniel nor Aditi connects
this to Apex's actual Consent Sync release** ("propagates consent and suppression state to all
downstream destinations" per docs/deal-spec.md) — Daniel just says "that comes up a lot," Aditi says
it's "something a lot of marketing ops teams deal with." Nobody in the room makes the connection.

**This is the single most important thing to check when running the real chain.** The system's whole
value proposition (per design-doc.md, §"Not just Gong's call summary") is catching exactly this kind
of need the humans in the room missed. Expected: `product_relevance` should contain an entry pairing
Hallie's stated need with Consent Sync. If pass 1 doesn't extract this as a `product_relevance_candidate`
(it's stated as pain, not literally framed as "I need X"), or if `query_knowledge.py`'s retrieval on
the extracted need-text doesn't surface Consent Sync, this connection will be missed — and that's a
real, reportable finding either way.

## Hallucination check
No price, no specific rollout date beyond Daniel's hedged "a couple months rather than weeks," and
no committed calendar date for the follow-up call.
