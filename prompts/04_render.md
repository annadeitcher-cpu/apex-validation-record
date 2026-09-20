# Pass 4 — Render

## Purpose

This pass writes the entire Slack message as finished prose. Python supplies data and posts the result. No string templating of field values anywhere — every sentence in the output is generated, not assembled.

**Inputs:** the output of `scripts/get_render_context.py --deal <name> --version <n>` — the Record payload, this version's change events, days-in-stage, AE and SolCon first names, and today's date.

**Output:** plain text (Slack mrkdwn). No JSON, no markdown code fence — the finished message, ready to post. Write it directly to the file the runbook tells you to.

## Writing rules

- **Short sentences. One idea each.** Anything with three clauses becomes two sentences.
- **No em-dash hinges.** Don't join a problem and its solution — or any two ideas — with a dash. Two sentences instead. (The header's compact stat line is the one exception; see Slack formatting.)
- **Never show internal identifiers.** No `obj_05`, no field names, no JSON keys. Name things in words.
- **Plain words over product language.** Not "a unified consent/suppression layer." Say: one place that tracks opt-outs so every channel sees them.
- **No waffling.** Every action is an instruction. Never "consider," "worth," "might want to," "perhaps," or "worth a short doc." If something should happen, say to do it, with a date.
- **No praise, no reassurance, no editorializing.** State facts and actions.
- **Titles on first mention for every prospect-side person:** "Curtis Nam, Security Engineer." First name after that. Internal Apex people don't need titles.
- **Deal roles named explicitly when they matter.** Champion, economic buyer, technical evaluator — name the role in prose when introducing the person who holds it, and especially when it changed. If the champion or economic buyer changed, say so plainly; that's why it matters. Don't mechanically tag every stakeholder with a role-noun if it doesn't serve the sentence — the target output below names Derek's and Priya's roles because the transition is the story; it doesn't do the same for Curtis, because his role isn't what changed.
- **Ground roles in the Record, not in what would make a tidier story.** Only state a role the Record actually assigned (`role_inference`) to that person. If the departing champion was never the economic buyer, don't say they were — the interesting fact is usually that a real economic buyer showed up who wasn't there before, not that authority "transferred."
- **Disambiguate functions that exist on both sides.** Always "Apex legal" or "Meridian legal," never bare "legal."
- **Assume the reader doesn't know the deal.**
- **No paragraph longer than three sentences.**

## Slack formatting

- `*bold*` for section headers and for a person's name (not title) on first mention.
- `•` bullets for lists. Numbered lists only for action items, which are sequenced.
- Blank line between every section.
- Bold the key fact in the header — the days-in-stage figure.
- Under 2,000 characters. Never truncate mid-word — write to length, don't let code cut strings.

## Message-type header

Every message opens with two lines before anything else, then a divider (see "Sections and dividers" below):

Line 1 — emoji, the message type in bold caps, the version where it applies, then the deal name, joined with `·`.
Line 2 — italic, one sentence: what this message is and what triggered it.

For the pinned/canvas Record message:
```
📌 *VALIDATION RECORD — v3* · Meridian Health — Customer Data Platform
_Current state of the technical validation. This message updates in place._
```
The italic line is always exactly that sentence — it doesn't change per deal or version.

For the "what changed" channel post:
```
🔄 *WHAT CHANGED — v3* · Meridian Health — Customer Data Platform
_3 material changes since the last update. Triggered by the Sep 12 call._
```
Pull the count from `get_render_context.py`'s material-event count and the date from its `TRIGGERING_CALL_DATE` line, formatted like every other date in this pass (`Sep 12`, no year). If the count is 1, write "1 material change," not "changes."

Someone scrolling the channel cold should be able to tell what a message is and why it exists without asking — that's the header's whole job. Don't make it clever, don't vary the wording between deals.

## Sections and dividers

Separate every section — including the message-type header — with a line containing only `---`. `scripts/post_to_slack.py` splits on that exact line to build Block Kit blocks: each chunk becomes its own section block, with a divider between them, so a message reads as distinct blocks instead of one wall of text. Put a `---` between the message-type header and the first content section too. Never put `---` inside a section — it's a separator between sections, not a rule you draw within one.

## Section order

Message-type header → Header → What's happened → Progress toward stage exit → What's blocking us → AE actions → SolCon actions → Need from [customer] → Worth raising

Don't drop into action items without the framing sections above them. Someone who wasn't on the call needs the context first.

**Header.** Account, ACV, days in stage, the 12-day Apex average, and the 22% win rate past 14 days. One or two lines — a compact stat line, not prose. This is a distinct section from the message-type header above it — they're separated by their own `---`.

**What's happened.** 2–3 short paragraphs. What changed since the last version, what's open, why it matters.

**Progress toward stage exit.** Read from the Record's `stage_exit_criteria` (five fixed entries — see `docs/record-contract.md`). Start with the count: how many of the five are met. Then one line per criterion, met ones first: a short confirming line for each met criterion, then each unmet one with its `reason` — resolve the criterion's `owner` (`AE`/`SC`) to the actual first name from the input, and use a ✅/❌ prefix per criterion. Don't restate the full criterion text mechanically — say it the way a person would ("Integration approach agreed" reads fine as-is; render it in plain language if the stored text ever doesn't). This section is a gate, not a summary — it's the honest, countable answer to "how close is this deal," and it should read that way.

**What's blocking us.** What stands between this deal and Commercial Negotiation. One line each for non-blocking items, clearly marked as accepted or in progress.

**[AE first name] — AE.** Numbered actions, each with a real date.

**[SolCon first name] — SolCon.** Numbered actions, each with a real date. If nothing technical is blocking, that's the final item: one sentence, no elaboration.

**Need from [customer name].** What the customer has to do, with a named person and a target date. Frame these as commitments the AE secures, not assignments handed down — the AE owns getting the customer to commit, not the customer's to-do list in isolation. Flag which one is the actual blocker. Use "work with [person] to get [thing] done" for anything that depends on someone else's action.

**Worth raising.** One item per bullet. Bold the product name. Then three short sentences: the problem in plain words, what the product does about it, and who raised it on a call and whether anyone followed up in the moment.

## Dates

Generate real calendar dates from today's date (supplied in the input — don't guess or reuse a stale date from the payload). Format as `*Thu Sep 17*` — bolded, abbreviated day, abbreviated month, no year. Tight dates (this week) for anything blocking; looser dates for anything not blocking. Anything gating stage exit gets a date within the current week, not "soon."

## Sorting and flagging

Sort action items within each person's section — not across sections. Priority order: anything gating stage exit first, then anything with a hard external date, then everything else. Equal priority sorts by earlier due date.

Mark the single blocking item with a 🔴 prefix, used consistently everywhere it appears (What's blocking us, the AE's or SolCon's action list, and Need from the customer, if it shows up in more than one place).

## Target output

```
📌 *VALIDATION RECORD — v3* · Meridian Health — Customer Data Platform
_Current state of the technical validation. This message updates in place._
---
*Meridian Health — Customer Data Platform*
$310,000 · *24 days in Technical Validation* — 2x the 12-day Apex average · win rate drops to 22% past 14 days
---
*What's happened*
Derek Osei, Director of Data Engineering, was our champion. He left the company. Priya Raman, VP of Data Platform, has taken over, with real budget authority of her own that Derek never had. She's the first identified economic buyer on the deal.

Priya reopened the patient-data protection question. Curtis Nam, Security Engineer, already confirmed the controls were sound, and Priya isn't disputing that. She's asking something new: does Meridian's contract cover the moment data first arrives, before processing. Nobody had asked that before.

Two smaller items stay open. One is whether Apex replaces Meridian's old marketing tool. The other is who owns building audience segments day to day.
---
*Progress toward stage exit — 3 of 5*
✅ Economic buyer identified — Daniel
✅ Integration approach agreed — Marcus
✅ Success criteria captured — Daniel
❌ Technical objections resolved — Marcus · a patient-data objection is open again
❌ Next step scheduled — Daniel · no date committed
---
*What's blocking us*
🔴 Meridian legal has to confirm their contract covers patient data during that first-arrival window. Priya won't move forward without it in writing.
• A known reschedule delay and one slower data connector: accepted, not blocking.
• Marketing tool replacement and segment ownership: open, Priya is working both.
---
*Daniel — AE*
1. 🔴 Work with Apex legal to get a written position on staging-layer patient data by *Wed Sep 16*.
2. Book the next call by *Wed Sep 16*. No date is set and this deal is 24 days in stage.
3. Send the proposal to Priya by *Tue Sep 15*. She's waiting on numbers.
4. Resend the SOC 2 report to Priya and Curtis by *Tue Sep 15*. Derek's inbox is deactivating.
---
*Marcus — SolCon*
1. Document the Teradata bridge design by *Thu Sep 17* and send it to Naomi and Priya. Priya re-ran the whole discussion because nothing was written down.
2. Nothing technical is blocking this deal.
---
*Need from Meridian*
1. 🔴 Priya to connect Meridian legal with Apex legal on the contract question. Target *Fri Sep 18*. This is the only blocker.
2. Priya to name a segment owner. Target *Fri Sep 25*.
3. Priya to get marketing's answer on replacing the legacy CRM. Target *Fri Sep 25*.
---
*Worth raising*
• *Consent Sync.* Opt-outs live in four separate systems today, so a patient can opt out of texts and still get an email. Consent Sync puts them all in one place. Curtis raised this on call one and nobody followed up.
• *Lineage Graph.* Curtis asked whether he could prove a specific patient wasn't contacted after opting out. Lineage Graph answers that for any individual record. Raised on call one, never addressed.
```

Two things about this target worth understanding, not just copying: Derek is written as champion only, never economic buyer — check the Record's actual `role_inference` for each stakeholder before writing this paragraph for any other deal, don't assume a departing champion held both roles. And the "Worth raising" attributions go to whoever the Record and the transcript actually show raising them — verify against the Record's `product_relevance` and the underlying call, don't default to whichever name sounds plausible.

## The "what changed" channel post

Generated through this same pass, when `scripts/get_render_context.py` shows material events for this version (and it isn't version 1). Opens with the 🔄 WHAT CHANGED message-type header (above), then a `---`, then the body: plain sentences, no field names, no identifiers, no em-dash hinges. Bold names on first mention. Three or four sentences maximum — the body is one section block, it doesn't need internal dividers.

Example:

```
🔄 *WHAT CHANGED — v3* · Meridian Health — Customer Data Platform
_3 material changes since the last update. Triggered by the Sep 12 call._
---
Derek Osei has left Meridian. Priya Raman, VP of Data Platform, has taken over as champion. She has real budget authority of her own, which makes her the deal's economic buyer too. The patient-data question is open again, same staging layer, but now a contract question rather than an encryption one.
```
