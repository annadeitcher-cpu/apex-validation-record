---
opportunity: Meridian Health — Customer Data Platform
call_id: meridian-01
call_type: technical_validation
day_offset: -23
duration_minutes: 88
participants:
  - name: Daniel Okafor
    role: Account Executive
    org: Apex
  - name: Marcus Webb
    role: Solutions Consultant
    org: Apex
  - name: Derek Osei
    role: Director, Data Engineering
    org: Meridian Health
  - name: Naomi Fletcher
    role: Staff Data Architect
    org: Meridian Health
  - name: Curtis Nam
    role: Security Engineer
    org: Meridian Health
---

DANIEL: Okay, looks like we're all here — Derek, Naomi, Curtis, thanks for carving out, what is this, an hour and a half? I know that's a big ask.

DEREK: Yeah, we figured better to do one longer session than three short ones where everyone's re-explaining context each time. So, worth it, hopefully.

DANIEL: Agreed. So for the recording — I'm Daniel, I'm the account exec on this from our side, and Marcus here is our solutions consultant, he's going to carry most of the technical part of the conversation.

MARCUS: Hey, everyone. Good to finally get on a call with the full group — I think I've only talked to Derek so far, over email.

DEREK: Yeah, and I've been sort of the bottleneck on getting the rest of the team looped in, sorry about that, it's been a chaotic few weeks on our end.

NAOMI: Hi, I'm Naomi, I'm the staff architect on the data platform side, so I'll probably be the one arguing with you about schemas.

MARCUS: [laughs] Looking forward to it, honestly, I'd rather argue about schemas now than find out about a mismatch three months into implementation.

CURTIS: And I'm Curtis, security engineering. I'll mostly be listening today, I think, unless something sets off an alarm bell.

DANIEL: [laughs] Noted. Before we get into it — Derek, did you end up making it to that health data conference you mentioned a few weeks back, or did that fall through?

DEREK: Oh — no, I ended up not going, honestly, it was right in the middle of a budget cycle crunch and I just couldn't justify being out for three days. Naomi went though, didn't you?

NAOMI: Yeah, I went, it was fine, mostly a lot of vendors I already knew about repackaging the same pitch. Though I did sit in on a session about consent management specifically that was actually somewhat relevant to today, coincidentally.

DANIEL: Oh interesting, small world. Well, hopefully we hold up okay against whatever they were pitching.

NAOMI: [laughs] We'll see.

DEREK: Okay, should we actually get into it? I'm conscious of the clock, and I know we've got a lot to cover.

DANIEL: That's exactly the kind of participation we want, honestly — better an alarm bell now than later. Okay, so, Derek, I know you and I have talked at a high level about what's driving this, but I think it'd help everyone, including us, if you just laid out the actual problem again from the top, for the group.

DEREK: Sure, yeah. So — high level, Meridian's a regional health system, we've got hospitals, a bunch of outpatient clinics, and a growing health plan side, and the problem we're trying to solve is really about patient and member engagement data being scattered across, honestly, I'd say six or seven systems that don't talk to each other well. So you've got clinical scheduling in one system, the health plan's member portal in another, our call center platform is its own thing, there's a legacy CRM that marketing uses for outreach campaigns, and none of it is unified in a way that lets us do the kind of coordinated outreach we're supposed to be doing.

MARCUS: When you say coordinated outreach, can you give a concrete example of what that looks like, or fails to look like today?

DEREK: Yeah, so — the clearest one is care gap outreach. So if someone's diabetic and they're overdue for an A1C test, ideally we want to reach them, remind them, maybe multiple channels, email, text, a call if needed. Right now what actually happens is the clinical team identifies the gap in one system, hands off a list, usually a spreadsheet, to the outreach team, who then has to manually cross-reference against — is this person actually reachable, have they opted out of texts, do we have a current phone number, is there already an active outreach happening for something else so we don't double up. And that whole handoff is slow and it's error prone, and periodically it just breaks down entirely.

NAOMI: And "breaks down" has actually meant real problems — there was a period last year where two different outreach programs were both texting the same population of patients about unrelated things within the same week, and we got complaints, and that turned into an actual escalation.

CURTIS: Yeah, and from my side, the thing that makes me nervous about the current setup isn't really any one system, it's that consent and opt-out status lives differently in like four different places, and there's no single source of truth for "has this person opted out of texts," so it's entirely possible for someone to opt out through one channel and still get contacted through another because that system never heard about it.

DANIEL: And just roughly, scale-wise — when we say the population you're trying to reach, are we talking, what, tens of thousands, hundreds of thousands of patients and members?

DEREK: It's — across the health system and the plan side combined, it's a little over four hundred thousand unique individuals we've got some kind of record for, though obviously not all of them are actively being outreached to at any given time. Any single campaign might be anywhere from a few hundred people to, during open enrollment season, upwards of sixty, seventy thousand.

NAOMI: Open enrollment is actually its own special nightmare, separate from the care gap stuff, because that's a hard deadline, everyone has to be reached before a specific cutoff, and it's the highest-volume period by far.

DANIEL: Right, that makes sense, there's no "we'll get to it eventually" option there.

DEREK: Exactly, and that's actually where some of our worst near-misses have happened, because volume is high and everyone's moving fast, which is exactly when a consent tracking gap turns into an actual incident instead of a theoretical one.

MARCUS: Yeah, that tracks with what we usually see — the failure modes show up disproportionately during the highest-pressure windows, which is unfortunate but predictable.

DEREK: One near miss specifically — this wasn't a full-blown incident, but it was close — during open enrollment last cycle, a batch of reminder calls went out to a list that hadn't been refreshed against opt-outs in about two weeks, because the refresh process at the time was manual and someone was out sick that week. Nobody outside opted out during that window as far as we can tell, we got lucky, but it was close enough that it scared people at the VP level.

CURTIS: Yeah, that's the one I was thinking of, actually, when I said "near misses." That's exactly the kind of thing that's currently held together by someone remembering to run a script.

DANIEL: Understood, that's a really concrete example, thank you for sharing it, that helps a lot in terms of understanding the actual stakes here rather than just the abstract problem.

DEREK: There's also a dumber, less dramatic version of the same problem, which is just — duplicate outreach. Not a compliance issue, just annoying and wasteful. Someone gets a care gap reminder call and an email on the same day from two different teams who didn't know the other was also reaching out, and it looks disorganized, and periodically someone complains that we're "spamming" them, which, fair, from their side it probably feels that way.

NAOMI: Yeah, and that one's honestly almost as damaging to trust as the consent issue, in a way, because it's the kind of thing patients actually notice and mention to their care team, and then it becomes a whole conversation about why the health system can't get its act together.

MARCUS: That kind of cross-channel deduping is actually a pretty direct fit for the orchestration piece I mentioned, we can circle back to exactly how that works once we get there.

DEREK: Yeah, let's get there, I don't want to front-load every pain point before you've even shown us anything.

DANIEL: [laughs] Fair, let's keep moving.

DEREK: Actually, one more piece of context that probably matters — that legacy CRM I mentioned, the one marketing uses for outreach campaigns, it's actually being sunset. Not by us choosing to replace it with this necessarily, it's more that the vendor announced end-of-life for it, I think it's got maybe another year or so of support left.

MARCUS: Oh, that's useful to know, actually — is the expectation that this platform would take over everything that CRM currently does, or just the specific consent and coordination piece we're talking about today?

DEREK: Honestly, I don't think that's been fully decided yet. I think there's an assumption forming that a lot of what that CRM does could be absorbed by whatever we land on here, but I wouldn't want to overstate that as a settled decision, because marketing hasn't weighed in on that specifically, and this conversation today has really been driven from the data and compliance side, not from marketing's side.

NAOMI: Yeah, that's a fair caveat, I could see marketing having opinions about losing a tool they're used to, even if the underlying data problem gets solved.

DANIEL: That's helpful to flag, we won't assume that scope without it actually being confirmed by whoever owns that decision.

DEREK: Yeah, good, I'd rather you not assume it, honestly, because if it turns out marketing wants to keep their CRM for campaign authoring and just wants better data flowing into it, that's a meaningfully different scope than replacing it outright.

MARCUS: Understood, we can design for either, but it's good to know that's genuinely undecided rather than assume one direction.

DANIEL: That's — yeah, that's a really common pain point actually, and it's one of the things I wanted to make sure we spent real time on today, because we do have something pretty specifically built for exactly that problem.

DEREK: Good, because that's honestly, out of everything, probably the thing leadership is most anxious about right now. Not even the outreach effectiveness piece, more the — if we get this wrong and someone who opted out gets contacted anyway, that's a real compliance exposure, that's not just an annoyance.

MARCUS: Right, understood. Okay, well, let me — should I just go ahead and share my screen and we can walk through this concretely rather than talking in the abstract?

DEREK: Yeah, please.

MARCUS: Okay, can everyone see okay?

NAOMI: Yep.

CURTIS: Yep, good.

MARCUS: Great. So there's a piece of the platform called Consent Sync, and the core idea is — instead of consent and suppression state living separately in each downstream system, it becomes a unified layer that every destination reads from before anything gets sent. So if someone opts out via a text reply, that's captured, and it propagates to every other channel and system that's wired into it, so the email system, the outreach CRM, the call center dialer, all of them would see the same current opt-out state.

DEREK: Okay, so walk me through the actual mechanics — like where does the opt-out signal originate, and how fast does it propagate?

MARCUS: So it depends on where the signal comes from — if it's a text reply, like a "STOP" keyword, that's typically near real time, we're talking seconds to low minutes depending on the messaging provider's webhook latency. If it's someone calling in and a call center rep manually marking them opted out in whatever system they're using, that's dependent on that system firing an event or us polling it, so it can be a bit slower, but still generally minutes, not hours.

NAOMI: And is that — sorry, is that push-based, like it's calling out to each destination as soon as it changes, or is each destination pulling on some interval?

MARCUS: It's push-based for supported destinations, so as soon as the state changes, it fires out to everything downstream that's subscribed. For destinations that don't support a push model, there's a fallback polling mechanism, but that's really more of an edge case for older systems.

DEREK: Our call center platform is genuinely ancient, so I'd bet money that's the polling case.

MARCUS: Yeah, that's honestly really common, a lot of call center platforms from that era are polling-only, so we'd scope for that.

CURTIS: Okay, and where does that consent state actually live? Like is it a separate database Apex hosts, or is it sitting in our warehouse alongside everything else?

MARCUS: It's modeled as a first-class object that lives in your warehouse, similar to how the segment or audience data works — the consent state itself is queryable data in your environment, we're not standing up a shadow database of consent records somewhere else that you'd have to trust independently of your own systems.

CURTIS: Okay, that's — good, that's actually a meaningfully better answer than I was expecting, honestly, because a separate consent database somewhere else is exactly the kind of thing that becomes its own audit nightmare.

DANIEL: Yeah, we hear that a lot, actually, especially from anyone who's been through an audit around consent management specifically.

DEREK: We have, unfortunately. Multiple times. Okay — Naomi, does that answer your architecture question, or do you have more?

NAOMI: I have a related one, actually — does the system distinguish between marketing consent and, like, operational or treatment-related communications? Because under HIPAA there's stuff we're allowed to send regardless of marketing opt-out, appointment reminders, that kind of thing, and I'd be worried about a system that treats "opted out" as one blanket flag and accidentally suppresses something we're actually required to send.

MARCUS: Yeah, that's an important distinction and it is modeled as separate categories rather than one flag — so consent and suppression state is tracked per communication purpose, not just per person. Someone can be opted out of marketing outreach while remaining reachable for treatment or operational messages, and those categories are configurable to match how you've defined them internally, we're not hardcoding a definition of what counts as "marketing" versus "operational" that might not match your compliance team's actual categorization.

NAOMI: Okay, good, that's — that was actually a real concern, because I've seen vendors treat opt-out as universal and it causes problems in exactly the healthcare context we're in.

CURTIS: Yeah, that would've been a dealbreaker on its own, honestly, if it was one blanket suppression flag.

MARCUS: Understood, and to be clear, getting those category definitions right during setup is real work, that's not a five minute config, but it's modeled correctly at the architecture level, it's not something bolted on after the fact.

DEREK: Okay, that's good to hear. Naomi, anything else on that for now, or should we keep moving?

NAOMI: No, that's good for now, I might have more once we get further into it.

MARCUS: That's totally fine, feel free to jump in whenever, this doesn't need to be linear.

DANIEL: Should I — actually, before we go further into the product, I want to ask something that's more just, business context. Derek, when you say leadership is anxious about this — is this coming from, like, compliance, or is there a specific incident that triggered this initiative, or is it more just a general sense that this needs to get fixed?

DEREK: It's — honestly a bit of both. There wasn't like a single catastrophic incident, thank god, but there's been enough near-misses and enough manual firefighting that our CIO basically said this needs to be solved this year, not next year. And separately, our compliance team has been raising the consent fragmentation issue independently, so those two pressures kind of converged onto this initiative.

DANIEL: Got it, that's helpful context, thank you.

DEREK: Yeah, no problem. Okay, should we keep going on the product side? I want to make sure we get to the actual data architecture piece too, because that's — Naomi and Curtis are going to have a lot more opinions about that than me.

MARCUS: Yeah, let's do that. So the other core piece, and this ties into what you were describing with the manual cross-referencing — is really the segmentation and orchestration layer, so once you've got unified consent and a unified view of, say, "who's overdue for an A1C test," you can build that population once as a live segment, similar conceptually to what a marketing team would build for a campaign, except here it's clinically driven, and it stays current automatically as people's status changes — someone gets the test done, they drop out of the segment, someone becomes newly overdue, they get added.

DEREK: Okay, and where's the source of "who's overdue" actually coming from — is that us feeding that in, or is that something the platform derives?

MARCUS: That's coming from you — we're not a clinical rules engine, we're not deciding who's overdue for what, that logic lives in whatever system already determines that today, presumably something adjacent to your clinical data. What we're providing is the layer that takes that population, once it's defined, and makes it usable for coordinated, consent-aware outreach across channels, with the deduping and suppression logic handled centrally instead of per-system.

NAOMI: Okay, that's — that's actually the right boundary, I think, we would not want a vendor deciding clinical overdue logic, that needs to stay with us and with whatever's authoritative for that.

DEREK: Yeah, agreed, that's — that's good that that's not in scope, honestly, that would've been a red flag if you said otherwise.

MARCUS: Yeah, we're pretty deliberate about that boundary, it comes up a lot with healthcare customers specifically.

DEREK: Can I ask about channel prioritization, actually — like, if someone's eligible for outreach through email, text, and a call, does the system decide which channel to use first, or is that something we configure?

MARCUS: That's configurable, it's not a black-box decision — you'd define the prioritization logic, so something like "try text first, if no response within X days escalate to a call," and the platform executes that sequencing and handles the suppression so someone doesn't get all three simultaneously unless that's actually what you want.

DEREK: Okay, and does that plug into our actual call center dialer, or does it just tell someone "this person needs a call" and a human has to do something with that?

MARCUS: That depends on the dialer's own integration capabilities — for a lot of modern platforms we can push directly into a call queue or campaign list. For older systems, and I suspect yours might fall into this category given what you said earlier —

DEREK: [laughs] Yeah, it's old.

MARCUS: — right, for those it's more likely we'd be generating a list that gets pulled into the dialer on whatever cadence that system supports, rather than a live API push. It still removes the manual cross-referencing step, it's just a slightly less real-time handoff on that specific channel.

DEREK: That's fine, honestly, even just removing the manual list-building step would be a big improvement over today.

NAOMI: Yeah, agreed, the dialer integration being slightly less elegant doesn't really move the needle on whether this is worth doing.

DANIEL: Should we talk about the data architecture piece now? I know that's been sort of hovering in the background.

DEREK: Yeah, let's get into it, because honestly this might be the thing that actually determines the shape of this whole project.

NAOMI: So — context for you both, we are mid-migration. We've been on Teradata, on-prem, for basically our entire history, and about a year and a half ago we started migrating to Snowflake. And "started" is doing a lot of work in that sentence, because it's — we're not done. We've got a chunk of our data already in Snowflake, mostly the newer analytics workloads, but a lot of our core operational data, including a lot of what would feed into this specific use case, is still living in Teradata.

MARCUS: Okay, and is there a timeline for when the rest moves over, or is it more open-ended?

NAOMI: It's — I wish I could give you a clean answer. There's a target, informally, of getting the bulk of it done by, call it, end of next year, but that target has already slipped twice, so I'd take it with a grain of salt. It's genuinely dependent on how much headcount we get allocated to the migration relative to everything else competing for the same engineers.

DEREK: We actually brought in a migration consultancy at one point to try to accelerate it, this was, I don't know, over a year ago now.

NAOMI: Oh, don't remind me.

DEREK: [laughs] Yeah, that's a whole separate story, but the short version is it did not go the way anyone hoped, and we ended up doing most of the actual migration work ourselves anyway, just with less trust in outside help than we started with.

MARCUS: Yeah, I won't pretend that's an uncommon story with warehouse migrations, unfortunately.

NAOMI: It's fine, it's mostly fine now, we just move slower than the org would like, and every quarter there's a new fire that pulls someone off the migration to go deal with something else.

DANIEL: That's a really familiar pattern, honestly, most organizations we talk to are somewhere in the middle of a multi-year migration like this, it's rarely a clean before-and-after.

DEREK: Which is, to be blunt, one of my actual open questions for this whole engagement — like, do we build this against Teradata now, knowing we're going to have to re-point it at Snowflake eventually, or do we wait and only build it against Snowflake once the relevant data's actually moved, which could be a lot longer than any of us want to wait.

MARCUS: Yeah, that's — that's a real question, and I don't think I can hand you a clean answer on the spot, honestly, because it depends on exactly which tables and how much volume we're talking about on the Teradata side.

DANIEL: We do support Teradata as a source, to be clear, so it's not that one option is off the table entirely.

MARCUS: Right, exactly, it's not a capability gap, it's more a sequencing and cost-of-rework question — like, is it worth standing up against Teradata now and then re-pointing later, versus waiting. Both are legitimate paths depending on your appetite.

DEREK: Yeah. I mean, my gut is we can't wait for the full Snowflake migration, that's — realistically that could be another year, year and a half at this rate, and leadership wants something moving well before that.

NAOMI: I'd tend to agree, though I'd want to actually look at which specific source tables this needs before committing to that, because if it turns out the critical data's actually already in Snowflake and it's really just the call center and legacy CRM stuff still on Teradata, that changes the calculus a lot.

DEREK: That's fair, I don't think we have that mapped out precisely yet, honestly.

MARCUS: Yeah, I don't think we need to solve that fully today — this feels like something worth a follow-up specifically on, once we've got a clearer picture of exactly which tables and systems are in scope.

DEREK: Can I ask, separately from the sourcing question — once we do have that sorted out, roughly what does a pilot or initial rollout actually look like timeline-wise? Like are we talking weeks, or months, for something at our scale?

MARCUS: For an organization your size with this many source systems, I'd expect an initial pilot scope — so probably one use case, likely the care gap outreach one given how concretely you've described it — to be somewhere in the range of a small number of months rather than weeks, mostly driven by the security review process and the initial data mapping, not by the product configuration itself, which is comparatively fast.

DEREK: Okay, and the security review — is that something that runs in parallel with the technical setup, or does it gate everything until it's done?

MARCUS: It can run substantially in parallel, especially since Curtis has already gotten into a lot of the substantive questions today rather than waiting until later to raise them. Usually what gates things is whichever is slower between the formal compliance sign-off and the actual data mapping work, not the platform configuration itself.

CURTIS: That's good to know, I'd rather front-load this stuff too, it's always worse when security review happens at the very end and blows up a timeline everyone thought was basically done.

DANIEL: Completely agree, and that's honestly part of why we wanted this session to include you from the start rather than bringing security in only once there's a contract on the table.

DEREK: Yeah, that's appreciated, that's not always how these vendor processes go.

DANIEL: One more thing while we're talking rollout — would it be useful at some point to talk to a reference customer, ideally another health system, who's gone through a similar rollout? Sometimes that's more convincing than anything we say ourselves.

DEREK: Yeah, that could be useful, maybe not today, but at some point before this gets finalized, I think leadership would probably want that too.

DANIEL: Understood, I'll keep that in mind for when we're further along. Agreed, let's not try to force a decision on that right now, I'd rather we get it right than get it fast.

DEREK: Yeah, that's — okay, that's fine, I just wanted to flag it early because I think it's going to end up being the thing that actually shapes the timeline more than anything else we talk about today.

NAOMI: Agreed, it's the biggest open variable, honestly.

DANIEL: Noted, we'll come back to that. Should we keep going, Marcus?

MARCUS: Yeah — so the other piece I wanted to touch on, given the compliance angle Derek mentioned, is lineage. So there's a capability called Lineage Graph, and basically, for every segment or audience that gets built and every piece of outreach that goes out based on it, there's a traceable record — this population was built from these source fields, here's when the definition changed and by whom, here's exactly what went out to whom and when. Which, for something like an audit around "did we contact someone who'd opted out," that record becomes pretty central.

CURTIS: Okay, that's — how granular is that, actually? Like if compliance comes to me six months from now and says "prove that this specific person didn't get contacted after opting out," can I actually answer that from this, or is it more of a high-level summary?

MARCUS: It's granular down to the individual record level — you'd be able to see, for that specific person, their consent state history, and cross-reference that against the outreach log to show whether any contact attempt happened after the opt-out timestamp, and if one somehow did, when and through which channel.

CURTIS: Okay. That's — that's a good answer, that's actually specifically the kind of question I get asked, so.

MARCUS: Yeah, that's exactly the scenario it's meant to support.

NAOMI: How long does that lineage history actually get retained for? Because we've got retention obligations that run pretty long for some of this, I want to say seven years in some categories, and I don't want to find out three years in that the detailed history's been rolled up into some aggregate that's no longer useful for an actual audit.

MARCUS: Retention's configurable, and it's not automatically summarized away after some default window — you'd set the retention period to match your actual compliance requirement, and the granular record-level detail persists for that full period, it's not degraded into aggregates over time unless you specifically configure it that way.

NAOMI: Okay, good, and is there an actual export mechanism, like if an external auditor needs something in a specific format, or is it locked into whatever your UI shows?

MARCUS: There's a structured export, so you're not limited to screenshots of a dashboard — you can pull the underlying records out in a format that a data team could hand to an auditor or load into another system if needed.

NAOMI: That's good, that's the right answer, honestly, I've dealt with vendors before where the "audit trail" turned out to be a UI feature with no real export path, and that's basically useless the moment an external party needs to see it independently.

DEREK: Yeah, we've been burned by that exact thing before too, actually, with a different system entirely, unrelated to any of this. [half to himself] That alone might be worth the price of admission, honestly.

DANIEL: [laughs] I'll take that as an unofficial endorsement.

DEREK: Don't quote me on that in the proposal.

DANIEL: No promises.

CURTIS: Can I — sorry, going back a bit, actually, before we move too far past the architecture piece. I guess one thing I'm wondering about, and it's maybe getting ahead of where we are, but — when data comes in from all these different source systems, and it's getting, I assume, normalized into some common structure before any of this segmentation stuff can happen — what actually happens to PII during that normalization step? Like where does it sit, in what form, while that's happening?

MARCUS: Yeah, that's a good question, and an important one, let me actually walk through that properly rather than give you a quick answer.

CURTIS: Yeah, I don't need the quick version, I'd rather hear the real one.

MARCUS: Okay, so — when source data comes in for normalization, sensitive fields, so things like name, date of birth, contact info, any identifiers, those go through field-level encryption before they're written anywhere, including in the intermediate normalized structures. So it's not that PII sits around in plaintext at any point during that process. And separately from encryption, there's tokenization for the fields that need to be used for matching and joining across sources — so if we need to match a record from your clinical scheduling system to a record from your call center platform, that matching happens on a token, a stable but non-reversible identifier, rather than on the raw PII fields themselves.

CURTIS: Okay, so — walk me through tokenization a bit more, because that word gets used pretty loosely sometimes. Is this a real one-way token, or is it something that can be reversed if someone has the right key?

MARCUS: It's a deterministic token generated via a one-way function, so the same input always produces the same token, which is what lets matching work consistently, but there's no key that reverses the token back to the original value. The mapping from raw value to token isn't stored as a reversible lookup either — it's generated algorithmically each time, not stored as a table you could dump.

CURTIS: Okay. And the encryption piece — field-level, you said. Is that encrypted at rest only, or in transit too, and who holds the keys?

MARCUS: Both at rest and in transit. In transit it's standard TLS, nothing unusual there. At rest, the field-level encryption uses keys that are — for most deployment models, customer-managed, so you'd actually control the key material, generally through a cloud KMS setup, rather than us holding a universal key that decrypts everyone's data.

CURTIS: Customer-managed keys specifically, or is that an add-on tier thing? Because I've had vendors tell me "yes we support that" and then it turns out it's a whole separate SKU.

MARCUS: [laughs] Fair skepticism. For your deployment size and the kind of data sensitivity you're describing, customer-managed keys would be part of the standard setup, not a gated add-on. I can get that confirmed explicitly in writing as part of the proposal, actually, so it's not just something I said on a call.

CURTIS: Yeah, I'd want that in writing, honestly, not because I doubt you specifically, just — that's the kind of thing that needs to be nailed down before this goes anywhere near production data.

DANIEL: That's completely fair, we'll make sure that's explicit.

CURTIS: Okay. And then — one more piece, sorry, I know I'm going deep on this one topic. During normalization itself, before tokenization and encryption are applied — is there a window where the raw data is sitting somewhere unprotected, even briefly, or is encryption applied at ingestion before anything else touches it?

MARCUS: Encryption of sensitive fields happens at ingestion, before the normalization logic operates on the data, so the normalization step itself is working against already-encrypted or already-tokenized representations for anything sensitive, not raw values. There isn't a window where it's sitting in an intermediate plaintext state waiting for a later step to protect it.

CURTIS: Okay, that's good. Two more, sorry, and then I promise I'll let this go for now — are the encryption keys held in an HSM, or software-based key management, and separately, is there a current SOC 2 report I could actually look at rather than take on faith?

MARCUS: HSM-backed for the managed key management option, and for the customer-managed KMS setup, that'd be whatever your cloud provider's HSM-backed KMS offering is, so it'd inherit whatever assurance you already have there. And yes, there's a current SOC 2 Type II report, I can get that over to you directly, that's a pretty standard ask at this stage and we're used to sharing it under NDA if needed.

CURTIS: Yeah, we'd want that under NDA, but that's fine, that's normal. And — breach notification, hypothetically, if something ever did go wrong on your end involving data that maps back to our patients, what's the actual contractual obligation on timing and who gets notified?

MARCUS: That's going to be spelled out explicitly in the data processing agreement and the BAA once we get to that stage, rather than something I want to characterize loosely on a call, just because the exact language matters a lot there and I don't want to misstate it. But directionally, it's the kind of notification timeline you'd expect for handling PHI, it's not something we'd try to negotiate down, this comes up with basically every healthcare customer we work with.

CURTIS: Fair, yeah, I'd rather see the actual contract language on that one anyway rather than a verbal summary, that's the right instinct on your part. One more, actually, sorry — how often do you all run third-party penetration testing, and is that something we'd get visibility into, or just a checkbox that says "yes we do this"?

MARCUS: Annually at minimum, sometimes more frequently around major architecture changes, and customers at your tier can typically get a summary report, not necessarily the full raw findings, but enough to see scope, severity of anything found, and remediation status, rather than just a one-line attestation.

CURTIS: Okay, that's reasonable, that's about what I'd expect from a vendor that's actually doing this seriously rather than performatively.

DANIEL: We'll make sure that's front and center whenever we get to that stage of paperwork, and we can loop in your legal team directly on the BAA specifics whenever that's useful.

CURTIS: Okay. That's — honestly that's a more thorough answer than I expected going into this, I had kind of braced for some hand-waving on this one.

MARCUS: [laughs] I figured you might, given the role. I'd rather over-explain it than have you leave this call still worried about it.

CURTIS: No, I appreciate that. I think — yeah, I think that actually addresses my concern. Field-level encryption at ingestion, one-way tokenization for matching, customer-managed keys, granular lineage for audit — that's a legitimate answer, not just a reassurance. I'm satisfied with that, for what it's worth, on the PII handling specifically.

DEREK: Good, glad we got that on the table properly instead of it lingering.

DANIEL: Yeah, agreed, that's — that's exactly the kind of thing we'd rather spend real time on now than have surface later.

MARCUS: I'll also just say, happy to set up a separate deeper session with whoever else on your security side needs to see this, if Curtis isn't the only stakeholder who needs to sign off eventually.

CURTIS: Yeah, there's — it's mostly me for the initial technical read, but this probably does need to go past our compliance team formally at some point before anything's signed, that's just how these things work here.

DANIEL: Of course, that's expected, we can support whatever documentation that process needs.

NAOMI: Can I ask about the scheduling system specifically, since that's one of the sources we haven't really touched on — appointment data. Is that treated any differently, given it's more operationally sensitive and updates pretty frequently compared to, say, claims data?

MARCUS: Not architecturally different in terms of how it's ingested and protected — same field-level encryption for sensitive fields, same tokenization for matching — but the ingestion cadence can be tuned per source, so a high-churn source like scheduling can sync more frequently than something that changes rarely, without that being a separate system to manage, it's just a configuration difference on the same pipeline.

NAOMI: Okay, and if an appointment gets rescheduled or cancelled right as some outreach is about to fire — like someone's about to get an automated reminder call for an appointment that just got cancelled ten minutes ago — is there any protection against that kind of race condition, or is that on us to handle downstream?

MARCUS: That's a real edge case worth designing for explicitly, and it's more a question of how frequently that source syncs relative to how time-sensitive the outreach is — if scheduling data syncs every few minutes, the window for that kind of collision shrinks a lot, but it's not literally zero unless the outreach trigger itself checks current status right before firing rather than relying on a snapshot from the last sync. That's something we'd want to design deliberately for the appointment reminder use case specifically, rather than assume the default sync cadence is automatically tight enough.

NAOMI: Okay, that's a fair answer, I'd rather hear "we'd need to design that carefully" than a confident "don't worry about it," honestly, because I don't fully believe the second one from anybody at this point.

DEREK: [laughs] Yeah, healthy skepticism there.

MARCUS: Noted, and agreed, that's exactly the kind of thing that sounds like a minor detail until it's the reason someone gets an annoyed phone call about a cancelled appointment they were reminded about anyway.

DEREK: Okay — should we talk about kind of what a rollout would actually look like, or is there more product stuff to cover first?

MARCUS: I think we've covered the core pieces — Consent Sync, the segmentation and orchestration side, lineage, and now the PII handling in reasonable depth. The one thing hanging out there that we didn't fully resolve is the Teradata versus Snowflake sourcing question.

DEREK: Right, yeah, that one's still open, and I don't think we're going to resolve it today, honestly. I think what we need to do is get someone from Naomi's team to actually map out which specific tables and systems this would need to pull from, and then figure out how much of that is already in Snowflake versus still on Teradata, and come back to you all with that.

NAOMI: Yeah, I can put together that mapping, it's not a huge lift, it's more that nobody's had a reason to do it yet since this use case wasn't defined until recently.

MARCUS: That would be really helpful, honestly, once we have that we can give you a much more concrete answer on sequencing rather than the "it depends" I gave you earlier.

DEREK: Yeah, I don't think there's a way around that being a bit unresolved for now. I don't love leaving it open, but I also don't think anyone in this call can actually close it out today without that mapping done first.

DANIEL: Agreed, let's not force it. We'll flag that as the open item coming out of this call and make sure it's the first thing we follow up on.

NAOMI: I can probably get that mapping done in — I don't want to promise something ridiculous, but a couple weeks feels realistic, depending on what else lands on my plate.

DEREK: That works. Let's aim for that.

DANIEL: Great, we'll plan around that then.

DEREK: Okay, on the business side — I know we haven't really talked numbers at all today, and I don't think we need to get deep into that right now, but can you give us any general sense of how pricing tends to scale for something like this, just so I'm not going in totally blind when I talk to my leadership about it?

DANIEL: Yeah, happy to give you a general shape without pinning down specifics yet, especially since the Teradata question could actually affect scope somewhat. Generally, for an organization your size with the number of source systems and destinations you're describing, this tends to land in a range that's meaningful but not, like, wildly out of step with what you'd expect for a platform replacing this much manual process and this much compliance risk. I'd rather come back with an actual number once we've got the sourcing question answered, rather than throw out a range today that ends up being wrong in either direction.

DEREK: That's fair, I'd rather have an accurate number a bit later than a rough one now anyway, especially given how this org reacts if a number moves later.

DANIEL: Understood completely, we'll wait until we have a real basis for it.

DEREK: I will say, just so you have a sense of the ceiling here — this isn't a small discretionary budget line, if the value case is clear, there's real appetite to fund this properly rather than nickel-and-dime it, given what's driving it. I don't want to say a number, but I don't want you to think we're a company that's going to balk at a serious enterprise number if the case is made well.

DANIEL: That's really helpful context, thank you, that shapes how I'll think about scoping the eventual proposal.

DEREK: Yeah, I'd rather you scope it right than scope it cheap and have it fall short of what we actually need. Okay. In terms of internal process on our end — I'm going to be the one pushing this forward day to day, but realistically this is going to need sign-off above me, probably from whoever's overseeing that end-of-year mandate I mentioned, and obviously from Curtis's side formally at some point, and probably legal given it's healthcare data.

DANIEL: That all sounds normal for something at this scope, yeah. Who would that sign-off sit with, roughly, so I have a sense of the shape of it?

DEREK: It would likely go up to our VP of Data Platform eventually, she's not been in any of these calls yet, but she's aware this is happening, I've been keeping her looped in at a summary level.

DANIEL: Got it, that's helpful to know, thank you.

DEREK: Yeah, no problem.

NAOMI: Can I ask one more architecture thing before we wrap, sorry, totally separate from the Teradata question?

MARCUS: Go for it.

NAOMI: When you're pulling from multiple source systems and normalizing them into a common structure — how do you handle schema drift over time? Like if one of our source systems changes a field type or renames something, does that silently break downstream, or is there some kind of contract or validation layer?

MARCUS: There's schema validation on ingestion, so if an incoming source deviates from the expected contract in a way that would break downstream processing, that gets flagged rather than silently passed through and potentially corrupting things. It's not going to catch every conceivable change gracefully — a genuinely breaking change, like a field disappearing entirely, is still going to require someone updating the mapping — but it won't fail silently, you'd get an alert rather than discovering it three weeks later because some segment count looks wrong.

NAOMI: Okay, that's a reasonable answer, that's basically what I was hoping to hear, honestly, silent breakage is my least favorite failure mode in any system.

MARCUS: Yeah, same, it comes up constantly in these conversations for good reason.

DEREK: Okay, I think — are we running close to time? I want to be respectful of everyone's afternoon, this has already run long.

DANIEL: We're actually right about at time, yeah. I think this was a genuinely useful session, way more substantive than I think either side was expecting going in, honestly.

DEREK: Yeah, agreed. Okay, so, to summarize where we landed — Naomi's going to put together that source system mapping for the Teradata versus Snowflake question, that's the main open item. Curtis, I think you said you're satisfied on the PII and encryption piece, pending the formal write-up Marcus mentioned.

CURTIS: Yeah, satisfied on the substance, just want it documented properly before it goes anywhere near compliance.

DEREK: Got it. And Daniel, you're going to hold off on real numbers until we've got the sourcing question answered.

DANIEL: That's right. I'll send over a recap after this along with some architecture documentation on our side that might help Naomi's mapping exercise, and once we've got a sense of the sourcing situation, we can get something on the calendar for a follow-up.

DEREK: And to be clear for everyone's sake, since I know these things sometimes go sideways after a good call and then nobody follows up for a month — I want to actually keep momentum on this, this isn't a "let's revisit next quarter" situation for me. I'll be checking in with Naomi on that mapping work directly, not just waiting for it to happen on its own.

NAOMI: [laughs] Noted, no pressure.

DEREK: Some pressure.

MARCUS: We'll make sure we're responsive on our end too, we don't want to be the reason this stalls either.

DANIEL: Agreed, we'll treat the recap and docs as a same-day thing, not a "whenever I get to it" thing.

DEREK: That sounds right. Let's plan on regrouping in — I don't know, a week and a half, two weeks, depending on how fast Naomi can turn around that mapping.

NAOMI: Yeah, that timeline works for me.

MARCUS: Great, we'll watch for that and follow up to get something scheduled once you're ready, rather than booking something blind right now.

DEREK: Perfect. Okay — anyone have anything else before we drop?

CURTIS: Nothing from me, this was more thorough than I expected, appreciated it. I'll say, going into this I expected to spend most of the call being politely stonewalled on the security questions, so this was a pleasant surprise.

MARCUS: [laughs] I'll take that as a compliment, genuinely.

NAOMI: Same, no complaints. Honestly the Teradata thing being left open is the right call rather than someone pretending to have an answer they don't have yet.

DEREK: Agreed. Okay, I think that's everything.

DANIEL: Great, well, thank you all again, this was a really substantive conversation, we'll get that recap over shortly.

DEREK: Thanks, everyone, talk soon.

MARCUS: Thanks, bye all.

NAOMI: Bye.

CURTIS: Bye.
