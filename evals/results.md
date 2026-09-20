# Eval harness — first real run

Built to replace a fabricated claim in a draft design doc ("twelve hand-labeled transcripts, scored
after every prompt change") — that never existed; `evals/` was empty before this. This is a real,
minimal version: 3 transcripts, hand-labeled ground truth, chain run fresh, scored by a re-runnable
script.

## The honest limitation, stated up front

The same reasoner (this session) wrote both the ground truth and ran the extraction chain against
it. A clean score here proves internal consistency with a documented set of rules, not that an
independently-run chain, or a different model, would produce identical judgment calls on genuinely
ambiguous cases. Two things partially offset that: ground truth was written from the raw transcript
alone, before looking at chain output, for all three calls (and for two of the three — Calibre and
Vantage — no stored extraction of any kind existed to consult even by accident); and several
individual judgment calls genuinely moved during the process (see "Judgment calls worth knowing
about" below) rather than being decided once and confirmed. That's evidence of real reasoning against
the rules, not just restating an answer already picked. It is not the same as a blind, independent
score, and this doc doesn't claim it is.

## Transcripts used and why

- **sightline-01** — deal-spec.md's own "clean control," textbook execution. Baseline: does the
  chain get the easy case fully right (5/5 exit criteria, no false blockers)?
- **calibre-01** — deal-spec.md's deliberately hard case: an unidentified speaker who never
  introduces themselves, real crosstalk, and no next step agreed. Tests whether the chain resists
  guessing a role for the unidentified speaker and resists inventing a next step that isn't there.
- **vantage-01** — deal-spec.md's "unmet product relevance" plant: a customer describes real,
  costly pain (manual consent/suppression reconciliation) that neither the AE nor SC connects to an
  actual Apex release in the room. Tests the single most load-bearing claim in the whole system —
  that it catches what the humans missed — against a real `query_knowledge.py` retrieval, not just
  the JSON matching itself.

## Results

| Metric | sightline-01 | calibre-01 | vantage-01 |
|---|---|---|---|
| Objection recall | 3/3 | 6/6 | 5/5 |
| Objection status accuracy | 3/3 | 6/6 | 5/5 |
| Stakeholder role accuracy | 2/2 | 2/2 | 2/2 |
| Next-step detection | correct | correct | correct |
| Competitive count | 2 (expected ≥2) | 0 (expected 0) | 0 (expected 0) |
| Product relevance (Consent Sync) | n/a | found (bonus — see below) | **found** |
| Hallucinated commitments | 0 | 0 | 0 |
| Stage-exit criteria | 5 of 5 | 1 of 5 | 3 of 5 |

Re-run any of these with `python scripts/eval_score.py evals/<name>_ground_truth.json evals/<name>_chain_output.json`.

## What's actually verified, not just self-consistent

**Calibre's "bonus" product-relevance connection**: ground truth didn't require one (Calibre isn't
deal-spec's designated plant for this), but Nathan and Yara's stated consent-tracking-maturity gap
independently retrieved and connected to Consent Sync too — reasonable given the real retrieval,
included in chain output for completeness, not scored against a required expectation either way.

**Retrieval genuinely works.** `query_knowledge.py --terms "consent and suppression list
reconciliation,fragmented suppression across channels"` — run for real, not simulated — returns
Consent Sync's actual release note, and the note's own "what problem it solves" text independently
describes the *exact* incident Hallie recounts (a customer who unsubscribed from email still getting
hit with paid social remarketing for the same campaign). That's not something I wrote into the
ground truth to make the retrieval look good — it's the knowledge base's own pre-existing content
matching a real transcript, confirmed by actually running the script.

**Stage-exit numbers make independent narrative sense.** Sightline (the designed-to-be-clean deal)
lands at 5/5. Calibre (deal-spec's deliberately messy deal, no next step, no economic buyer) lands
at 1/5. Vantage (one real open objection, no committed date) lands at 3/5. These weren't tuned to
hit those numbers — they fall out of applying the same five fixed criteria mechanically each time.

**A real bug got caught and fixed in this run** — in the scorer, not the chain. The first Vantage
run flagged a "hallucination" because the forbidden-terms list included the phrase "specific date,"
which the chain output uses correctly and repeatedly to describe the *absence* of a committed date
("no specific date was set"). That's the system being honest about a gap, not inventing one. Fixed
by tightening the ground truth's forbidden-terms list to actual day names instead of an ambiguous
phrase, documented here rather than quietly corrected. This is exactly the category of thing
`docs/corrections.md` exists to log — it's a scorer bug, not a chain bug, so it isn't going in that
log, but it's the same discipline.

## Judgment calls worth knowing about (not clean wins, genuinely close calls)

- **Sightline's "babysitting" objection (obj_01)** was reclassified mid-process. Aditi's answer
  gives real architectural reasons the customer's core fear won't recur, but also explicitly
  concedes "it's not zero maintenance." Applying the resolved-test literally — *is there anything
  left to concede* — the honest answer is yes, so this landed as `partially_resolved`, not
  `resolved`, even though the surrounding tone of the call reads as a clean win. This is exactly the
  failure mode `docs/corrections.md` #4 was written to catch (found on this same deal, on a
  different objection in the same call), and it would have been easy to mark this one `resolved` on
  a looser read.
- **Calibre's Yara Haddad role** (`champion`, medium confidence) is a real judgment call, not a
  confident read. She shows some champion-shaped behavior (paces the meeting, raises the hard
  lock-in question herself) but states no budget authority and asks some technical questions too.
  `unknown` would have been a defensible alternative, and pass 2's own rule explicitly prefers
  `unknown` over a guess when the call doesn't give enough signal. Flagging this rather than
  presenting it as settled.
- **Calibre's economic buyer** genuinely isn't identified in this call — correctly reflected as an
  open risk rather than force-fit onto Yara or Nathan.

## What this doesn't cover

Three transcripts against one set of hand-written rules is not the twelve-transcript, ongoing,
weekly-re-run harness the original plan (and the now-corrected design doc) describe as the
production target. This is a first real data point, not a finished measurement system. `scripts/
eval_score.py` is a genuine, re-runnable tool — extending this to the full corpus is mechanical
(write ground truth for the remaining 7 real transcripts, run the chain, score) rather than a new
build.
