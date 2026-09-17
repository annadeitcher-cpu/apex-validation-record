# Transcript Generation — Repeatable Process

Five remaining: Northwind 1, Northwind 2, Vantage, Ardent, Calibre.

---

## The loop

1. Fill the template below and give it to Claude Code
2. Run `python scripts/qa_transcript.py transcripts/<file>.md` — fixes the mechanical stuff
3. Read against the manual checklist — catches what the script can't
4. Regenerate or patch, then move to the next

Don't batch. The one-at-a-time discipline is what's kept quality up so far.

---

## Generation template

> Generate **[DEAL, CALL #]** to `transcripts/[filename].md`. See `docs/deal-spec.md` §[N].
> Read `transcripts/sightline-01.md` and `transcripts/meridian-01.md` first and match their texture.
>
> **Participants:** [names, roles, orgs — exactly as in deal-spec]
> **Duration:** [N] minutes. **Target [N×95] words minimum** — a [N]-minute call transcribed produces a lot of text.
> **day_offset:** [−N]
>
> **This call's job:** [one or two sentences — what has to happen here for the corpus to work]
>
> **Plants (must land):**
> - [specific thing 1]
> - [specific thing 2]
>
> **Must stay out:** [topics from other calls that would muddy this one]
>
> **Leave open:** at least one thread genuinely unresolved at the end — acknowledged but outstanding.
>
> **Standing rules:**
> - Real recording, not minutes. People interrupt, backtrack, trail off, say "sorry, go ahead."
> - Objections arrive hedged and sideways, never announced.
> - Anything marked resolved requires **explicit customer acceptance on the record**, not a good vendor answer.
> - At least one tangent that goes nowhere.
> - No absolute calendar dates, months, years, or quarters. Relative language only — "next Tuesday," "end of the month," "a couple weeks out."
> - Never two consecutive turns from the same speaker.
>
> Generate only this one.

---

## Per-deal fills

**Northwind 1** (§2, 81 min, ~7,700 words) — Kenji Watanabe, Lisa Ferreira + Rachel Kim, Marcus Webb.
*Job:* establish the competitive plant. Kenji mentions a competitor **casually, in the middle third, while talking about something else** — not as a "how are you different" question. Nobody dwells on it.
*Leave open:* something that call 2 can advance.

**Northwind 2** (§2, 46 min, ~4,400 words) — adds Owen Brady (Director, RevOps).
*Job:* new stakeholder appears mid-cycle. Owen brings a commercial lens the technical people didn't have.
*Watch:* this should register as `stakeholder_added` but **not** material enough for its own channel post. Don't make Owen's arrival dramatic.

**Vantage** (§5, 76 min, ~7,200 words) — Sung-min Park, Hallie Brooks + Daniel Okafor, Aditi Sharma.
*Job:* **the Consent Sync plant.** Hallie describes, at length and with visible frustration, manually reconciling consent and suppression lists across email, push, and paid social. Multi-hour recurring task.
*Critical:* Daniel and Aditi **do not connect it to Consent Sync.** They acknowledge the pain sympathetically and move on to the next agenda item. This must feel like a natural miss under time pressure, not negligence.
*Note:* Marcus demos Consent Sync competently at Meridian. Aditi missing it here is execution variance across SCs — which is Apex's stated problem. Deliberate.

**Ardent** (§6, 69 min, ~6,500 words) — Viktor Lang, Cheryl Boateng + Greg Lindqvist, Marcus Webb.
*Job:* a perfectly ordinary call. Nothing dramatic, nothing broken. A next step gets discussed loosely — no firm owner, no date.
*The plant is the silence after.* Zero activity rows in the database. The transcript's job is to make the follow-up failure look like ordinary neglect, not a doomed deal.

**Calibre** (§3, 93 min, ~8,800 words) — Yara Haddad, Nathan Cole, **one unidentified speaker** + Tom Brennan, Aditi Sharma. Generate **last**.
*Job:* the hard case. Three plants:
1. A fourth voice who **never introduces themselves.** Render as `UNIDENTIFIED:`. They contribute substantively — this isn't a walk-on.
2. **Genuine crosstalk** at least twice, with the transcript reflecting the overlap.
3. **No next step.** Ends with Yara saying something like *"we'll probably want to loop in Renata before we go much further"* — no owner, no date, no commitment. A careful human would also hesitate to call that a next step.
*Also:* leave two or three objections in states that are genuinely arguable. This is the transcript that should make your eval labeling hard.

---

## Manual checklist

The script can't judge these. Read for them.

**Texture**
- [ ] At least one tangent that goes nowhere — a war story, a complaint about unrelated tooling, a joke
- [ ] Someone says something slightly unhelpful or half-wrong and gets corrected
- [ ] The vendor side isn't uniformly polished — a hedge, an "I'd have to check," a fumble

**Objections**
- [ ] Raised sideways, not announced. "I guess one thing I'm wondering about" beats "I have a concern about X"
- [ ] Anything marked resolved has **the customer saying so**, in their own words
- [ ] At least one thread genuinely open at the end
- [ ] Across the corpus, not every objection resolves — you need `open` and `partially_resolved` examples

**Next steps**
- [ ] Emerge in conversation — someone proposes, someone adjusts — rather than being read out like a form
- [ ] For Calibre specifically: ambiguous enough that *you* hesitate

**Consistency**
- [ ] Participants match `deal-spec.md` exactly
- [ ] Nothing contradicts an earlier call in the same deal
- [ ] Product names match the release list (Segment Studio, Warehouse Native Activation, Consent Sync, Lineage Graph, Streamline Ingest)
- [ ] Stated elapsed time inside the call roughly matches `duration_minutes`

**The corpus-level question**
After each one, ask: *does this add a case my extraction chain hasn't seen yet?* If a transcript is just more of what you already have, it's costing you generation time and adding nothing to the eval set.

---

## Known generation artifacts

Seen across all three so far — check every time:

- **Escaped markdown** (`\---`, `call\_id`, `\[laughs\]`). May be an upload-path artifact rather than the file on disk. Verify with `head -8`.
- **Consecutive same-speaker turns**, sometimes responding to something several turns back. Two in the corpus so far.
- **Low-end word counts.** Both Sightline and Meridian 2 landed at the bottom of their range. The template now asks for a hard minimum.
- **Stated time drift** — Meridian 2 says "a good use of forty-five minutes" for a 52-minute call. Cosmetic, but it's the kind of thing that's visible on a shared screen.
