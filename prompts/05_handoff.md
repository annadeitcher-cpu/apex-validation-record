# Pass 5 — CS Handoff

## Purpose

This pass writes the message CS receives at close. It does no extraction — every fact in it already exists in the Record. The point isn't new information, it's assembly: turning an accrued object nobody on the CS side has read into the specific things a CSM needs before their first call, in the order they need them.

**Inputs:** the output of `scripts/get_handoff_context.py --deal <name>` — deal metadata, the v1 payload's `stakeholders` (the baseline — who bought), and the latest Record's full payload (the accrued, current state at close).

**Output:** plain text (Slack mrkdwn), written directly to the file the runbook tells you to. No JSON, no code fence.

## This is not `04_render.md` again

The AE/SC render is a status update for people who were in the room. The handoff is an orientation for someone who wasn't. Don't lead with stage-exit criteria or action-item mechanics — the CSM doesn't care what gated Commercial Negotiation, they care what they're walking into. Reuse `04_render.md`'s writing discipline (below), not its structure.

## Writing rules (same as `04_render.md`)

- Short sentences. One idea each. No em-dash hinges.
- Never show internal identifiers — no `obj_05`, no field names, no JSON keys.
- Plain words over product language.
- No waffling — "consider," "might," "worth" are not allowed. State it or don't.
- No praise, no reassurance, no editorializing.
- Titles on first mention for every prospect-side person, first name after. Internal Apex people don't need titles.
- Assume the reader knows nothing about this deal.
- No paragraph longer than three sentences.
- `*bold*` for section headers and a person's name (not title) on first mention. Under 3,500 characters, hard ceiling under Slack's 4,000-char limit for `chat.update`.

This budget is wider than `04_render.md`'s 2,000, deliberately: that message gets scanned mid-week by a rep who already knows the deal, this one gets read once, carefully, at the moment a CSM inherits an account they've never touched. Different reading context, different budget — don't tighten this back to 2,000 to match `04_render.md`, and don't treat 3,500 as a target to write up to either.

## Message-type header

Same convention as `04_render.md`: two lines before any content, then a `---`, then the rest of the message split into `---`-delimited sections the same way (see that file's "Sections and dividers" section — `scripts/post_to_slack.py` turns each chunk into a Block Kit section block with a divider between). For the handoff, always:

```
🤝 *HANDOFF TO CUSTOMER SUCCESS* · Meridian Health — Customer Data Platform
_Posted at close. Everything Elena inherits, drawn from the record above._
```

No version — this isn't a versioned artifact. The italic line names the CSM by first name; it's otherwise fixed wording, same as the other three message types.

## Section order

Message-type header → Header → What they think they bought → What we committed to → What you're inheriting → Who's here now vs. who bought → Risks → Freshness

**Header.** Account, ACV, CSM's first name (this is their handoff, name them in the header, not just at the @-mention). One line. This is a distinct section from the message-type header above it, separated by its own `---`.

**What they think they bought.** Pull from `success_criteria` — the customer's own stated pain, in their own words or a tight paraphrase of it, not the product's feature list. This is discovery, not a spec sheet: what were they actually trying to fix when this started. Include the scale/stakes facts if the customer stated them (population size, retention requirements, a specific incident) — those are the numbers a CSM will get asked about in their first call and won't have unless they're here.

**What we committed to.** Bullets, one commitment per bullet, `• *Short name.*` followed by plain-language sentences — same pattern as `04_render.md`'s "Worth raising" list. Pull from `integration_patterns`, every entry, not just the clean ones. Fold each caveat into its own bullet rather than listing caveats separately; a caveat is exactly the kind of thing that becomes a support ticket when nobody told CS it existed. Say what's in phase one versus deferred if the record shows that split. Plain words over product language applies here more than anywhere else in this pass — a CSM scanning this list has to understand each line without knowing the product's internal terms for its own features.

**What you're inheriting.** Objections with status `open` or `resurfaced` only — not `resolved`, not `partially_resolved`. A partially-resolved objection was accepted as a tradeoff; that's closed, not inherited. If a `resurfaced` objection exists, say plainly that it was once considered closed and came back, and in what new form — that's the single highest-signal fact in this section when it's present. If nothing is open or resurfaced, say so in one sentence rather than skipping the section.

**Who's here now vs. who bought.** The most important section. Compare the baseline stakeholders (v1) against the latest version's stakeholders. Name who was there at the start and is gone. Name who's here now that wasn't. State each person's role plainly (`role_inference`, never invented, never upgraded — a departed champion who was never tagged `economic_buyer` does not get called the economic buyer here, the same caution `04_render.md` names). If the buyer changed, say plainly that the CSM is onboarding someone who wasn't in the room for the original pitch — that sentence is the point of this whole section, not a nice-to-have close.

**Risks.** `open_risks` at `severity: medium` or `high` only — drop `low`. One line each: the risk, plainly, no severity label shown (the filtering already did that job).

**Freshness.** One line: how many days between the record's last update and close. If it's a small number, say so plainly — that's the reassurance, not a hedge ("record was current, not stale").

## @-mention

Address the CSM by first name at the top of the message body (`Hey @Elena` or similar), the same way `scripts/escalate.py` writes `@{first_name}` as plain text — there is no real Slack user id on file for any CSM in this prototype, so this is not a functioning Slack mention, it's plain text that reads as one. Don't fabricate a `<@U...>` id; a fabricated id either fails silently or, worse, could resolve to an unrelated real Slack user.

## Target output

```
🤝 *HANDOFF TO CUSTOMER SUCCESS* · Meridian Health — Customer Data Platform
_Posted at close. Everything Elena inherits, drawn from the record above._
---
*Meridian Health — Customer Data Platform handoff for Elena*
$310,000 · closed won

Hey @Elena — here's what you're inheriting on this one.
---
*What they think they bought*
Today, care-gap outreach is a manual spreadsheet handoff between the clinical team and outreach, cross-checked by hand against consent and reachability. It's slow, and it periodically breaks down entirely. Last year two outreach programs texted the same patients in the same week and it became an escalation. Compliance needs to prove, at the individual level, that a specific person wasn't contacted after opting out — not a summary. Some records carry roughly seven-year retention requirements. The addressable population is about 400,000 people, with single campaigns running up to 60-70k during open enrollment.
---
*What we committed to*
• *Consent Sync.* One place that tracks opt-outs so every channel sees them, instead of a patient opting out on one channel and still getting contacted on another. Their legacy call center dialer can't get a live signal, so it checks in on a schedule instead. Setting up the actual opt-out categories is real work, not a quick config.
• *Care-gap segmentation.* Outreach lists build directly off their clinical care-gap data, in whatever order across channels they want. Apex doesn't decide who's overdue for care — that logic stays Meridian's.
• *Dialer integration.* The legacy dialer gets a list on a schedule instead of a live feed, still a big step up from today's fully manual process. Phase one is email only; the dialer comes later, once email is proven out.
• *Data sourcing.* Most of the data — demographics, scheduling, health plan membership, recent claims — is already in Snowflake, and that's the primary source. One narrow connector reaches into their older Teradata system just for call center consent records, and gets shut off once that system is retired. Their old marketing CRM is skipped entirely since it's being phased out. Naomi's team needs a handful of days spread over a couple of weeks for the setup work, and Priya committed to protecting that time.
• *Lineage.* Every outreach event is traceable back to the record and rule that produced it, kept for as long as they need, with a real export, not just something visible on screen.
• *Schema alerts.* If a source system changes in a way that would break the pipeline, someone gets alerted. A field disappearing outright still needs a person to fix the mapping by hand.
• *De-identified analytics.* Analysts can work against the data without seeing full patient records, limited to what their specific use case needs. Meridian's own compliance team decides what counts as properly de-identified, not Apex.
---
*What you're inheriting*
One objection is open again. Curtis, their security engineer, signed off in call one on how PII is protected during processing, and that technical answer still stands. Priya is now asking a different question about the same moment in the pipeline: does the contract actually cover protected health information sitting there before processing runs. Nobody has answered that yet.
---
*Who's here now vs. who bought*
Derek Osei, Director of Data Engineering, was the champion who drove this deal from the first call. He left the company before close. Priya Raman, VP of Data Platform, took over — she has real budget authority of her own, which Derek never had, and she's the first person on this deal anyone identified as the economic buyer. You're onboarding someone who wasn't in the room for the original pitch. Naomi and Curtis are both still around and still engaged.
---
*Risks*
Whether this platform replaces or just sits alongside Meridian's legacy marketing CRM is still undecided internally — marketing hasn't weighed in. If the open contract question turns into real amendment work rather than a quick clarification, it could push the timeline.
---
*Freshness*
The record was last updated 1 day before close.
```

Two things about this target worth understanding, not copying: the "who's here now" paragraph is longer than the three-sentence rule would normally allow for a reason — it's the one section explicitly called out as the most important, and the target still keeps each sentence short and single-idea rather than using length as license to pack multiple facts into one sentence. And every fact above traces to a specific field in the payload — if you can't point to where a sentence in your own output came from, it doesn't belong in the message.
