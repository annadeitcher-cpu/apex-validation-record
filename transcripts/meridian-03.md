---
opportunity: Meridian Health — Customer Data Platform
call_id: meridian-03
call_type: technical_validation
day_offset: -2
duration_minutes: 74
participants:
  - name: Daniel Okafor
    role: Account Executive
    org: Apex
  - name: Marcus Webb
    role: Solutions Consultant
    org: Apex
  - name: Priya Raman
    role: VP, Data Platform
    org: Meridian Health
  - name: Naomi Fletcher
    role: Staff Data Architect
    org: Meridian Health
  - name: Curtis Nam
    role: Security Engineer
    org: Meridian Health
---

DANIEL: Morning — or afternoon, for you all, I guess. Looks like we've got a new face on the call today. Is Derek joining a little later, or —

NAOMI: Oh — no, actually, Derek's not with us anymore, he left a few weeks back. This is Priya, she's picked up the initiative from here.

CURTIS: Yeah, it's been a bit of a whirlwind couple of weeks around here, honestly.

PRIYA: [laughs] That's one word for it. Hi, I'm Priya, I run data platform here, Derek used to report up through me, so I've inherited this along with a handful of other things that were on his plate.

DANIEL: Oh — got it, well, nice to meet you, Priya. Sorry to hear about Derek, hope he's off to something good.

NAOMI: He is, yeah, he's in a good place, just wanted to be clear that's not a sad story or anything.

MARCUS: Good to hear. Hi, Priya, I'm Marcus, I'm the solutions consultant on this from Apex.

PRIYA: Good to meet you both. So, full disclosure up front — Derek gave me a hand-off briefing before he left, so I've got the broad strokes, but it was fairly high level, and I know there's been at least one call since then that I wasn't part of. So I may ask you to re-cover some ground, and I appreciate everyone's patience with that.

DANIEL: Of course, that's completely normal, and honestly it's better that you ask than nod along and have gaps surface later.

PRIYA: I appreciate that, I've sat through enough handoffs where everyone pretends the new person is fully caught up and then three meetings later it's obvious they weren't, so I'd rather just be upfront about it now.

NAOMI: That's honestly a really healthy way to start, most people try to fake it longer than they should.

CURTIS: Agreed, faking it just means we end up re-explaining things anyway, just later and more awkwardly.

PRIYA: [laughs] Exactly, may as well front-load the awkwardness.

CURTIS: Agreed, no worries at all, happy to re-explain anything.

NAOMI: Yeah, same, take whatever time you need to get oriented.

PRIYA: Appreciated. Maybe the most useful thing is if someone just gives me the state of play as of today — what's actually been agreed, what's still open — and then I can ask questions as they come up rather than derail you with a hundred questions up front.

DANIEL: Sure, happy to do that. So — high level, this started as a conversation about unifying patient and member engagement data, mainly to solve a consent and coordination problem, care gap outreach specifically was the anchor use case. Marcus walked through a piece called Consent Sync in the first session, which centralizes consent and suppression state across channels, and there was a long, pretty thorough conversation about PII handling and security that Curtis led.

CURTIS: Right, and for what it's worth, I came away satisfied on that front, we can get into the specifics if you want, but I didn't leave that call with open concerns.

PRIYA: Good to know, I'll probably still ask a couple things, just so I've heard it directly, but noted. Can you remind me, actually, what does Consent Sync do, mechanically? Derek's briefing mentioned the name but not really the substance.

MARCUS: Sure — the core idea is that consent and suppression state, so opt-outs, preference changes, that kind of thing, becomes a single unified layer that every channel reads from, rather than living separately in each downstream system the way it does today. So if someone opts out via a text reply, that propagates out to email, the call center dialer, wherever else, instead of each system only knowing about opt-outs that happened through itself.

PRIYA: Okay, and that propagation, is that fast, or is it more of a batch thing?

MARCUS: Depends on the source of the signal — a text-based opt-out is near real time, seconds to low minutes. Something coming through an older system, like your call center platform, is a bit slower, but still bounded, minutes rather than hours.

PRIYA: Got it, that's a helpful summary, thank you.

NAOMI: That's basically the same explanation from the first call, just condensed, for what it's worth, so you're not missing much by not having been there for the long version.

PRIYA: Good, that's reassuring, sounds like I got the efficient version rather than a watered-down one.

MARCUS: Of course, that's fair.

NAOMI: And then the second call was really just me presenting a mapping I put together — which systems are already migrated to Snowflake versus still on our legacy Teradata environment, since we're mid-migration and that affects what this can actually source from day one.

PRIYA: Right, Derek mentioned the migration status in the hand-off, but I don't think he got into specifics. What'd you find?

NAOMI: The good news is most of the core data — patient demographics, scheduling, health plan member data, recent claims — is already in Snowflake. The wrinkle is the call center platform, which is where opt-out and consent data from phone interactions lives, that's still on Teradata, and it wasn't on anyone's migration roadmap because nobody had connected it to this use case before.

PRIYA: Okay, and that matters because that's exactly the consent-tracking data this whole thing is supposed to fix.

NAOMI: Exactly, yeah, kind of an ironic gap.

MARCUS: The resolution we landed on is a bridge — we'd build against Snowflake for the bulk of it, and stand up one additional connector specifically against Teradata for the call center system, with the plan to re-point it once that system's eventually migrated or retired.

PRIYA: Okay. And is that connector actually as clean as "just one more integration," or is there real complexity hiding in that?

NAOMI: It's additive, not a different order of magnitude, was the conclusion — it's some incremental setup work, not a redesign. I did push on that a bit at the time, I wanted to make sure we weren't hand-waving it.

MARCUS: Yeah, Naomi asked good questions on that, we didn't just take it as settled.

PRIYA: Can I actually ask you to walk me through the plan itself, rather than just the headline? I know "Snowflake for most of it, one Teradata connector for the call center piece" is the summary, but I want to understand what happens once that system does eventually get migrated or retired, because I don't want us building something that creates its own cleanup project down the road.

NAOMI: That's actually a question I asked too, almost word for word. The answer was that retiring the connector is meant to be clean — since it's scoped narrowly to just that one source, you re-point the equivalent data at its new home in Snowflake and turn the old connector off, rather than unwinding something deeply tangled into the rest of the platform.

PRIYA: Okay, that's reassuring, I've seen "temporary bridge" solutions turn permanent before, so I wanted to make sure that wasn't quietly baked in here.

MARCUS: No, that's a fair thing to want confirmed, and it's a legitimate risk in general with bridge architectures, just not the case here specifically, or at least not by design.

NAOMI: Yeah, and for what it's worth, I pushed on that exact concern when I first heard the plan too, so you're not the only skeptic in the room.

PRIYA: Good, I like that it wasn't just me being paranoid on day one, I don't want to inherit an assumption nobody actually stress-tested.

DANIEL: That's a fair instinct, and honestly a healthy one to bring in fresh, sometimes a new set of eyes catches something everyone else had gotten used to.

PRIYA: We'll see if I catch anything, no promises.

DANIEL: Can I ask, out of curiosity, how are you finding stepping into something mid-stream like this? I imagine it's a different experience than starting an initiative from scratch.

PRIYA: Honestly, it's a bit of both good and bad. Good, in that the hard early groundwork is already done, I'm not starting from a blank page. Bad, in that I don't have the full context for why certain calls got made, so I'm partly trusting the team's judgment and partly re-deriving it myself as I go.

MARCUS: That's a pretty honest description of what taking over mid-project actually feels like, in my experience.

PRIYA: Yeah, I'd rather be honest about it than pretend I walked in with full command of every decision that's been made so far. I wasn't there, I don't have that, and pretending otherwise would just slow us down.

NAOMI: I think that's the right instinct, honestly, the pretending version usually costs more time in the long run than just asking.

PRIYA: Agreed. Okay — what else, what's the actual state of the commercial side, has a number gone out?

DANIEL: Not yet, actually — I was in the process of putting together a proposal, and I'd had it addressed to Derek specifically, since that's who I'd been working with. I should probably redirect that to you now.

PRIYA: Yeah, please, redirect it to me. I'll need to get up to speed on it before I can react to anything meaningfully, but yes, I'm the right recipient going forward.

DANIEL: Understood, I'll make sure of that.

PRIYA: What's actually in it, roughly, before I see the real thing?

DANIEL: It reflects the Snowflake-primary architecture with the one Teradata connector for the call center piece, and it also folds in a recommendation around segment ownership — Marcus had flagged that as an organizational gap, not a technical one, that came up in the second call.

PRIYA: Oh, interesting, tell me about that one, that's new to me.

MARCUS: Sure — the gist is, once this is live, someone needs to actually own building and maintaining the audience segments day to day, and right now that's ad hoc, it's whoever in marketing happens to be closest to a given campaign. Derek flagged that as a real gap, not something anyone had solved.

PRIYA: Yeah, that tracks, honestly, that's a broader pattern I've seen in a few places here, we're decent at standing up infrastructure and less disciplined about who actually owns using it well.

NAOMI: That's a very fair read of this organization, yeah.

PRIYA: [laughs] I'm allowed to say it, I live here. Okay — do you have a recommendation, or is that something you're leaving to us?

MARCUS: We'd recommend designating an accountable owner early, doesn't need to be a whole new team on day one, even just one person as the point of contact for segment quality and adoption tends to make a real difference. A lot of organizations grow that into something like a small outreach operations function over time.

PRIYA: Okay. Honestly, unlike some of what I'm going to have to research, I can actually make a call on this one faster than Derek could — I have budget flexibility to designate someone into a piece of that role now rather than waiting for a bigger org design exercise. Let me think about who, but I don't think this needs to sit open the way it did last time.

DANIEL: That's great to hear, honestly, that's exactly the kind of thing that's better resolved early.

PRIYA: Yeah, no sense in leaving an obvious gap open just because nobody forced a decision on it.

DANIEL: Can I ask, actually, roughly what's your budget authority look like relative to what Derek had? Just so I calibrate how I frame things going forward.

PRIYA: I've got real discretion at this level, more than Derek did, honestly, that's part of why this landed with me rather than getting reassigned to someone else at his level. I still answer to the CIO's office for anything genuinely large, but the range we've been circling in today wouldn't need to go beyond me for approval.

DANIEL: That's really helpful to know, thank you for being direct about that.

PRIYA: Yeah, I'd rather you know where the actual decision sits than have you guess or over-scope your ask to route around a gatekeeper that isn't really there.

MARCUS: That's a refreshing amount of clarity this early, honestly.

CURTIS: That's honestly a very different energy than the last couple calls, not a complaint, just an observation.

PRIYA: [laughs] I'll take that as a compliment. I tend to make calls I actually have authority to make rather than let them float, it's a habit.

NAOMI: No, it's a good habit, I'm not going to argue with it.

DANIEL: Should we get into the more technical agenda for today, or is there more state-of-play stuff to cover first?

PRIYA: I think I've got enough of a picture for now, let's move into whatever today was actually supposed to cover. What was on the agenda?

MARCUS: Today was meant to be more of an implementation-planning session, nailing down some remaining architecture specifics now that there's real momentum, rather than open-ended discovery.

PRIYA: Okay, that works. Before we get too deep into new territory though, I do want to go back to something — the PII handling piece Curtis mentioned. I know you said you were satisfied, Curtis, and I trust your read on the technical side, but I want to ask about it from a slightly different angle, because it's the piece I'm going to be accountable for if this ever gets scrutinized externally, and I'd rather ask now than assume.

CURTIS: Sure, go ahead, happy to have it covered again.

PRIYA: So — I guess the thing I keep turning over is less about the encryption mechanics and more about the staging layer specifically. Before normalization actually runs — before any of the transformation logic touches the data — where does it physically sit? Because there's presumably some landing zone where raw data arrives before anything happens to it, and I want to understand our business associate agreement posture during that specific window, not after processing's already been applied. That's a HIPAA question as much as it is a technical one, and it's the piece I keep coming back to.

MARCUS: That's — that's a good question, and a slightly different angle than what we covered last time, so let me actually walk through it properly rather than assume the earlier answer fully covers it.

PRIYA: I'd appreciate that, yeah.

MARCUS: So — data lands in a staging area on ingestion, that's true, there is a landing zone conceptually. But sensitive fields are encrypted as part of that same ingestion step, before the data is considered "landed" in any queryable or accessible sense. So there isn't a window where raw, identifiable data is sitting in staging in a plaintext, accessible form waiting for normalization to get to it later.

PRIYA: Okay, and when you say "as part of that same ingestion step" — is that atomic, meaning it either lands encrypted or it doesn't land at all, or is there some sequencing where it could theoretically land first and get encrypted a moment later?

MARCUS: It's designed to be atomic in the sense that encryption is applied before the data becomes accessible to anything downstream, including staging-layer access. I want to be precise though — I'd want to confirm the exact mechanics with our engineering team rather than assert "impossible" from memory on a call, because "theoretically impossible" is a strong claim and I don't want to overstate it to you the way I wouldn't want it overstated to me.

PRIYA: I appreciate that qualification, honestly, "let me confirm" is a better answer than false confidence stated with a straight face.

CURTIS: Can I jump in here? Because — I want to be straightforward, we did go through a version of this last time, pretty thoroughly, and I came away satisfied. Field-level encryption at ingestion, one-way tokenization, customer-managed keys, I saw the SOC 2 report was coming, I asked about HSMs, pen testing, breach notification timing. I'm not saying don't ask, Priya, but I don't want us to spend the whole session re-litigating something I already worked through.

PRIYA: I hear you, Curtis, and I'm not questioning your read on the technical controls, genuinely. But I think we're actually asking slightly different questions, and I want to be honest about why. You're evaluating this as a security engineer — is the data protected, are the controls sound. I have to think about it as the person who'd be representing our BAA posture and our minimum necessary standard if this ever came up in an OCR inquiry, or an internal compliance audit, or a board question. Those aren't the same lens, even when they're looking at the same system.

CURTIS: That's — okay, that's a fair distinction, actually, I wasn't thinking about it that way.

NAOMI: Yeah, I think that's a real difference, honestly, not just Priya being cautious for its own sake.

PRIYA: Right, and to be specific about what's actually still open for me — it's not "is the encryption real," I believe that it is. It's: does our BAA, as written, actually cover a third-party platform touching PHI at the staging layer specifically, even transiently and even encrypted, or does our current BAA language only contemplate PHI once it's in a processed, normalized state? Because if our BAA doesn't explicitly cover the staging window, that's a gap regardless of how good the encryption is.

MARCUS: That's — that's a genuinely sharp question, and honestly not one I can answer definitively myself, because that depends on the specific language of your existing BAA, which I haven't seen, and on how our own data processing agreement characterizes that staging step contractually. That's a legal and contracts question layered on top of the technical answer, not purely a technical one, and I'd rather say that plainly than pretend I can speak to contract language I haven't reviewed.

PRIYA: Right, that's exactly my read too.

DANIEL: We can absolutely get our legal team to work through that specifically with whoever owns your BAA language, rather than me or Marcus trying to characterize it loosely on a call. I'd rather that come from the people actually qualified to speak to it than from either of us guessing.

PRIYA: I'd want that, yeah. I don't think I can consider this fully closed until I've seen that in writing, mapped specifically to the staging layer, not just to the platform generally. A general assurance about the platform as a whole isn't the same thing as language that actually contemplates this specific window.

CURTIS: To be clear, I'm not pushing back on getting that in writing, that seems reasonable. I just don't want my earlier sign-off to get erased in the process, like the technical answer I got was somehow wrong. It wasn't wrong, it just wasn't the question Priya's asking.

PRIYA: Agreed, and I want to be clear I'm not walking back your read, Curtis, genuinely. I think you're right on the technical merits. I just carry a different kind of exposure than you do, and "the security engineer signed off" isn't going to be a complete answer if I'm ever in a room justifying our BAA posture specifically.

MARCUS: That distinction actually makes a lot of sense to me, and I don't think it needs to be resolved as "Curtis was wrong" or "Curtis was right" — it sounds like both things are true. The technical controls are sound, and there's a separate, real question about whether the paperwork explicitly contemplates this specific data flow. I don't want to paper over that by pretending it's one clean answer when it's genuinely two different, valid concerns sitting side by side.

PRIYA: That's a fair way to put it, yeah, and honestly it's a more useful framing than either of us trying to declare a winner.

DANIEL: I'll get that moving with legal as a real, tracked item, not something that gets lost. I don't want to promise a timeline I can't back up, but I'll treat it as a priority given what you've laid out, given how clearly it's tied to something you're personally accountable for.

PRIYA: Appreciated. I'm not trying to hold the whole project hostage to this, to be clear, I just don't want it quietly assumed closed when, from where I sit, it isn't yet.

DANIEL: Understood, and just so it's said plainly — nothing about today changes our commitment to getting this right, even if it means the timeline shifts a bit while legal works through it properly.

PRIYA: I appreciate you saying that, genuinely, I've had vendor conversations before where raising exactly this kind of question gets treated as friction to be managed rather than a legitimate concern to be worked through.

MARCUS: No, that's — that's not how we want this to go, if anything I'd rather you keep asking sharp questions like that one, it makes the eventual answer more trustworthy, not less.

PRIYA: Good, that's the right attitude, honestly, and it's part of why I don't feel the need to be adversarial about it, I just need it actually resolved properly rather than glossed over.

NAOMI: That seems like the right way to leave it, honestly — not pretending it's resolved, but not treating it as a blocker either. I'd rather have an honest "open" label on something than a fake "closed" one we all quietly know isn't real.

CURTIS: Yeah, agreed, I can live with "open but not blocking." I'd rather have it labeled honestly than have it come back and surprise someone in six months.

PRIYA: Good, that's exactly where I'd want it to sit for now. I'd rather leave here with an accurate picture than a falsely tidy one, even on my first real call with all of you.

MARCUS: Should I keep going with the rest of today's agenda, or is there more on this specifically?

PRIYA: No, let's keep moving, I think we've said what needs to be said on that for now.

MARCUS: Okay — one thing I did want to cover today, since we're talking about sensitive data handling, is de-identification, since I know that sometimes comes up separately from the operational consent question, especially if you ever want to use this data for analytics or reporting purposes beyond the direct outreach use case.

PRIYA: Yeah, that's actually relevant, we do have an analytics team that would love broader access to patterns in this data without needing full PHI access for every analyst.

MARCUS: Right, so there's support for generating de-identified views of the data, following a defined de-identification methodology, that analytics users could work against without touching identifiable fields directly. I want to be careful here though — de-identification methodology is something we'd need to align with your compliance team's specific standard, whether that's expert determination or safe harbor, we're not unilaterally deciding what counts as sufficiently de-identified for your organization.

PRIYA: Good, I wouldn't want a vendor making that determination for us, that's exactly the kind of thing that needs to be our call, with our own compliance sign-off.

NAOMI: Agreed, that's a real distinction, methodology ownership matters a lot there.

PRIYA: Practically, who on our side would need to be involved in defining that methodology? Is that a compliance conversation, or does it sit with Curtis's team, or somewhere else entirely?

CURTIS: I'd say it's primarily compliance's call, with security weighing in on the technical implementation once the standard's picked. I wouldn't want to be the one deciding whether we're using expert determination versus safe harbor, that's genuinely not my domain.

NAOMI: Yeah, agreed, that feels like a compliance-led decision with technical folks executing on it.

PRIYA: Okay, that's helpful, I'll make sure compliance is looped in properly from the start, rather than have this get treated as a technical detail that slips past them until it's too late to easily fix.

MARCUS: That's exactly the right instinct, we've seen de-identification treated as purely technical before and it tends to cause problems later when compliance discovers after the fact that a methodology was chosen without them.

PRIYA: Yeah, that's not a mistake I want to make on my first real decision here. Can I ask a related question — minimum necessary. If analytics only needs certain fields for a given use case, is there a way to actually enforce that at the platform level, so someone doesn't get broader access than their specific use case requires, even if de-identified?

MARCUS: Yes, access can be scoped by role and by specific dataset or view, so you could construct a narrower view that exposes only what a specific analytics use case actually needs, rather than one broad de-identified dataset that everyone gets full access to regardless of their specific need.

PRIYA: Good, that's the right shape, honestly, minimum necessary isn't just a PHI-access concept for us, we try to apply that discipline broadly, even to de-identified data, just as a matter of practice.

CURTIS: That's consistent with how I'd want that instrumented from a security standpoint too, for what it's worth.

MARCUS: Good, glad it aligns from both directions, that's usually a sign we're actually describing the same thing rather than talking past each other.

PRIYA: Can we talk about the call center connector for a second, actually, going back to that — I know Naomi said it's additive, not a redesign, but walk me through, practically, who at Meridian would need to be involved in standing that up? I want to understand the actual resourcing ask, not just the architectural shape of it.

NAOMI: That would mostly be me and maybe one other person from my team, for the mapping and validation side, plus whoever from Marcus's team handles the actual connector build.

MARCUS: That's right, it's primarily a joint effort between Naomi's team validating the schema and our team handling the connector configuration itself.

PRIYA: And timeline-wise — I know nobody wanted to commit to a hard number before, is that still where things stand, or has that firmed up at all since the last call?

NAOMI: Still roughly where it was, honestly, we said a small number of months for an initial pilot, mostly gated by the security and governance review rather than the actual configuration work, and I don't think anything's changed that estimate materially.

PRIYA: Okay, and the BAA question we just talked about — does that sit inside that timeline, or could that actually extend it if legal takes a while?

DANIEL: Honestly, it could extend it somewhat if it turns out real BAA amendment work is needed rather than just clarifying existing language. I don't want to pretend that's zero-risk to the timeline.

PRIYA: I appreciate you saying that rather than assuming it's a rounding error, that's exactly the kind of thing that quietly blows up a plan if nobody flags it early.

MARCUS: Agreed, better to have that risk named now than discovered in month two, when it's a lot more disruptive to everyone's plans.

PRIYA: Okay, and roughly how much of Naomi's time, would you estimate? I'm trying to get a sense of whether I need to protect time on her calendar explicitly or whether this is background-level effort.

NAOMI: I'd guess something like a handful of days spread over a couple weeks, not a full-time commitment, but not zero either.

PRIYA: Okay, I'll make sure that's protected time rather than something you're squeezing in around everything else, that's exactly the kind of thing that quietly slips if nobody names it explicitly.

NAOMI: I appreciate that, honestly, that's not always how it goes.

CURTIS: Can I ask, while we're on resourcing — is there budget for any additional security review time on my end, or am I expected to absorb this into my existing workload the way most things get handled here?

PRIYA: That's a fair question. I'd rather protect real time for you too, given how central the BAA and governance piece is turning out to be, rather than assume you'll just absorb it. Let me think about what that looks like practically, whether that's formal allocated hours or just me making sure your manager knows this is a priority.

CURTIS: Either would help, honestly, right now it's very much "fit it in around everything else."

PRIYA: Yeah, I don't love that model for something this consequential, I'll follow up on it separately from this call. Same instinct as with Naomi's time, honestly — if it matters this much, it should be protected, not squeezed in.

DANIEL: [laughs] I'm noticing a pattern of you just deciding things today, which, from where I sit, is a nice change of pace.

PRIYA: [laughs] Give it a few weeks, I'm sure I'll accumulate my own backlog of things I haven't decided yet, that's just how this job seems to go. Okay — what else is on today's list?

MARCUS: There was a question from last time about destination prioritization for the first phase — call center dialer, email, whatever else — that got deferred until there were real numbers to look at. I don't know if you want to touch that today or wait.

PRIYA: Let's at least talk about it directionally, even if we're not locking anything in. What were the options?

MARCUS: Broadly, email tends to be the fastest to stand up given how mature that integration typically is, the call center dialer integration is a bit heavier given the platform age we discussed, and there was also discussion of whether push or additional channels come in a later phase.

PRIYA: My instinct, without having dug into it deeply, is start with email for the first phase, prove the pattern, then bring in the dialer once we've got a working example to point to internally. Does that match what you'd have recommended anyway, or am I about to suggest something you'd have talked me out of?

MARCUS: No, that's actually right in line with what we'd typically recommend, starting with the lower-complexity destination and expanding from a proven base tends to go a lot better than trying to stand up everything simultaneously.

PRIYA: Good, glad my instinct wasn't wildly off on my first real technical opinion here, small victories.

NAOMI: [laughs] You're off to a decent start.

PRIYA: [laughs] Low bar, but I'll take it. Sorry, random tangent — is the office still doing that thing where facilities randomly reshuffles everyone's desk assignment without warning? Derek mentioned it once and I never got the full story.

NAOMI: Oh my god, yes, that happened again literally last month, I came in on a Monday and my desk was just gone, reassigned to someone else, no email, nothing.

CURTIS: I still don't understand how facilities operates, honestly, it feels like a black box nobody's ever successfully audited.

PRIYA: [laughs] That tracks with my experience of them too, though thankfully not something I have to deal with day to day anymore now that I'm mostly in the exec suite.

NAOMI: Must be nice.

PRIYA: [laughs] Don't worry, I have my own version of facilities-level chaos to deal with, just at a different altitude. Anyway, sorry, that was completely unrelated, go ahead.

DANIEL: Should we talk a little about numbers, given where things stand, or do you want to hold that until you've had more time to get oriented?

PRIYA: I think I'd rather see the actual proposal once it's redirected to me before we talk numbers live on a call, if that's alright. I don't want to react to a figure I haven't actually sat with.

DANIEL: Completely fair, I'll get that over to you directly rather than walk through it verbally today.

PRIYA: Appreciated.

CURTIS: Can I ask something separate, while we're not fully through the agenda — the SOC 2 report Marcus mentioned last time, has that actually come through, or is that still pending?

MARCUS: It should have gone out under NDA already, let me double check after this call and make sure it actually landed with the right person on your side, rather than assume it did.

CURTIS: Appreciate that, I don't think I've seen it yet, but it's possible it went to Derek's inbox and got lost in the handoff.

PRIYA: Oh, that's actually a good point, there's probably a handful of things that went to Derek's email that never made it anywhere. I should have IT do a pass on his inbox for exactly this kind of thing before it gets fully deactivated.

NAOMI: Yeah, that's a good call, there's probably more than just the SOC 2 report sitting in there.

DANIEL: We can also just resend it directly to you and Curtis both, to be safe, rather than rely on it surfacing from an old inbox.

PRIYA: Yeah, let's do that, belt and suspenders.

NAOMI: Can I ask, actually, while we're talking about things that might be stuck in Derek's inbox — is there a formal offboarding checklist for stuff like this, or is IT just going to freestyle it? I only ask because I don't want us to find out about a third missing thing a month from now.

PRIYA: That's a fair worry, and honestly I don't know the answer off the top of my head, I'll check with IT and make sure there's an actual process rather than hoping someone remembers to look.

CURTIS: Might be worth having someone specifically comb through anything vendor-related, given how many of these threads run through email.

PRIYA: Agreed, I'll ask for that specifically rather than a generic sweep.

MARCUS: Will do, I'll make sure that goes out today.

PRIYA: Can I ask one more thing before we move on from security — how does something like the pen test summary Curtis mentioned relate to the BAA question we discussed earlier? Are those totally separate tracks, or does one inform the other?

CURTIS: Mostly separate, honestly, the pen test speaks to whether the controls actually hold up under attack, the BAA question is more about whether the paperwork covers a specific data flow at all, regardless of how well-defended it is.

PRIYA: Right, that distinction makes sense, I just wanted to make sure I wasn't conflating two different assurances into one in my head.

MARCUS: That's a good instinct to check, honestly, those two things get conflated a lot, and they really are answering different questions.

PRIYA: Appreciated. What else is on the list, or are we mostly through it?

MARCUS: I think that's most of what I had flagged for today. The main open items coming out of this are: legal working through the BAA language specifically for the staging layer question, the SOC 2 report getting properly resent, and Daniel redirecting the proposal to you.

PRIYA: And the segment ownership piece, which I said I'd think about on my end.

MARCUS: Right, yes, that one too.

PRIYA: Can I ask one more thing, actually — Derek mentioned in his handoff that there was some open question about whether marketing wants to keep their existing outreach tool for campaign authoring, versus having this platform absorb that too. Is that still genuinely undecided, or has that firmed up?

NAOMI: Still undecided, as far as I know, that conversation never really got resolved, it's been sitting there since the first call.

MARCUS: Right, we've been careful not to assume either direction, since Derek was pretty clear that marketing hadn't weighed in yet.

PRIYA: Okay, I'll try to get an actual answer on that before the next real conversation, since I think it probably matters for scoping the proposal properly, and I don't want that sitting open indefinitely the way Derek left it.

DANIEL: That would be really helpful, honestly, that's one of the bigger scope questions still hanging out there.

PRIYA: Yeah, I'll talk to whoever owns that relationship on the marketing side and come back with a real answer, rather than let it keep drifting the way it apparently has been.

CURTIS: That's probably one of the more consequential things sitting on your plate honestly, out of everything we've covered today.

PRIYA: Noted, I'll prioritize it accordingly.

DANIEL: Should we get something on the calendar for a follow-up, or do you want to hold off until you've had time to actually sit with the proposal and the BAA question?

PRIYA: Let's hold off on booking something specific today, honestly, I think I need to actually read the proposal and hear back from legal before I know what the next real conversation needs to cover. I don't want to book something blind and then have it be a status-check call with nothing new to say.

DANIEL: That's completely reasonable, we'll wait to hear from you rather than force something onto the calendar.

PRIYA: I'll be in touch once I've had a chance to actually sit with everything, probably within the next couple weeks, but I don't want to commit to an exact date I might not hit given everything else that's on my plate right now. Anything else before we wrap, or is that the last of the open threads?

MARCUS: I think that's most of it, we've covered a lot of ground for a first real session with the full group.

PRIYA: Agreed, more than I expected, honestly, given I walked in only half-briefed.

DANIEL: You did better than half-briefed, for what it's worth, that recap went a lot smoother than most first sessions with a new stakeholder.

PRIYA: [laughs] I'll take the compliment, even if I suspect you say that to everyone.

DANIEL: Not everyone, no, some people take a lot longer to get oriented than you just did.

MARCUS: Understood, no pressure on our end, we'll be responsive whenever you're ready.

CURTIS: For what it's worth, this was a genuinely useful session, even with the re-covering-ground parts.

NAOMI: Agreed, good to have you fully looped in now, Priya, rather than piecing it together secondhand.

PRIYA: Thanks, both, and thank you both for your patience today, I know re-explaining things you'd already covered isn't the most exciting use of everyone's time.

DANIEL: Not at all, honestly, this was a genuinely substantive session, we covered real ground even with the recap.

PRIYA: Good. Okay, I think that's everything on my end for today.

MARCUS: Sounds good, we'll get the SOC 2 report resent, work the BAA question with legal, and get the proposal over to you directly.

PRIYA: Appreciated, thank you all.

DANIEL: Thank you, Priya, good to meet you, we'll talk soon.

NAOMI: Bye, everyone.

CURTIS: Bye, take care.

MARCUS: Bye, thanks all.
