# Ground truth — calibre-01

Written by independently reading transcripts/calibre-01.md only. No validation_records row exists
for this opportunity/call yet, so there was nothing to accidentally consult.

## Stakeholders
- **Yara Haddad**, VP, Enterprise Data — `champion`, medium confidence. Drives strategic framing,
  paces the meeting ("let's keep going"), raises the vendor lock-in business question. No stated
  budget authority in this call, so not `economic_buyer`.
- **Nathan Cole**, Data Governance Lead — `technical_evaluator`, high confidence. Owns essentially
  every governance/security/access-control question in the call.
- **Unidentified Speaker** ("Priti," per Yara's aside at line 511, but never self-introduces) — the
  deal-spec plant. **Expected: `role_inference: unknown`, `confidence: low`** — a chain that guesses
  a role here (e.g. infers seniority from the depth of her questions) is failing the deliberate test.

No economic buyer is identified in this call at all — nobody discusses budget authority. This should
surface as an **open risk**, not get force-fit onto a stakeholder.

## Objections
1. **Where does data actually land — customer environment or Apex-controlled** (data_residency).
   Answered (customer's own warehouse), but Nathan says "that's the right starting answer... I'm
   going to have a lot of follow-ups." **Expected status: `partially_resolved`**, not fully closed.
2. **Does Apex make any autonomous decisioning judgments** (other/compliance). Pushed hard, answered
   unambiguously and repeatedly — no exceptions, including for risk. Nathan: "that's actually the
   answer I needed to hear." **Expected status: `resolved`, high confidence.**
3. **Encryption/tokenization/key-management mechanics** (security). Detailed answer given, but Nathan
   explicitly refuses to call it resolved: "I'd want our security team to actually validate the
   specifics before I'd call it resolved." **Expected status: `open`** — the customer himself declines
   acceptance on the record.
4. **Vendor lock-in / how tested is the config-export path, does it satisfy vendor-exit compliance
   obligations** (procurement). Tom explicitly declines to answer the compliance-checklist version:
   "I don't think I can give you a fully satisfying answer... right now." **Expected status: `open`.**
5. **Cross-institution identity matching against third-party-tokenized data** (integration). Explicitly
   deferred as "not a today question," needs its own design conversation. **Expected status: `open`.**
6. **Risk-alerting latency/ordering guarantees** (performance). Substantive answer given, but Priti:
   "I still think risk specifically needs its own session." **Expected status: `partially_resolved`.**

## Competitive
**Expected: empty array.** No other vendor, tool, or prior evaluation is mentioned anywhere in this
transcript — this call is entirely about Calibre's own internal systems and governance requirements.
An empty array here is the *correct* answer, not a recall miss.

## Next step
**Present: false.** Yara explicitly declines to name a next step: "I don't think we're at a point
where I can say what the next concrete step is today... we'll probably want to loop in Renata before
we go much further." This is the deal-spec's deliberate plant — a chain that invents a next step
here (e.g. from Tom's "we'll get the security materials moving") is fabricating one.

## Open risks
- No economic buyer identified or engaged in this call.
- Deal is genuinely undecided internally — no committed next step, scope not yet chosen internally
  per Yara's own words.

## Hallucination check
Nothing in this call commits to a price, a specific timeline number beyond Tom's explicit "a few
months rather than weeks" (itself hedged, not a firm date), or any named individual outside the five
people on the call plus Renata (mentioned, not present).
