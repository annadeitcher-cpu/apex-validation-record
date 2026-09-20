---
opportunity: Meridian Health — Customer Data Platform
call_id: meridian-04
call_type: follow_up
day_offset: 5
duration_minutes: 34
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
---

DANIEL: Morning, both — I kept this one short on purpose, so if we actually wrap in thirty, I'm not going to be offended.

PRIYA: I appreciate the optimism. Curtis says hi, by the way, he couldn't make it today, some internal thing came up on his end, nothing to do with any of this.

DANIEL: No worries at all, appreciate the heads up. Naomi, morning.

NAOMI: Morning. I'll flag anything security-adjacent to Curtis after, if it comes up, so he's not out of the loop.

DANIEL: Sounds good. Before we get into it — quick unrelated thing, did either of you end up going to that data platform conference a few weeks back, the one everyone's badge photo was floating around on the internal Slack?

NAOMI: [laughs] I saw the photos, I did not go, I heard the coffee situation was genuinely a disaster though.

PRIYA: I went for half a day, honestly barely remember any of the actual sessions, mostly remember standing in a very long line for a bag that had a broken zipper.

DANIEL: [laughs] That tracks with every conference bag I've ever gotten, honestly, they never survive past the first zip.

NAOMI: I feel like conference swag quality has just been declining for years, across the board, not just that one.

PRIYA: [laughs] We could do a whole session on that, but let's not, we have actual things to cover. Sorry, go ahead.

DANIEL: No, that's fair, that one's on me for bringing it up. So — I think the headline reason we're here is the BAA question, Priya, you said you had an update.

PRIYA: I do, and it's a good one, so let's lead with that. Legal came back to me — actually came back faster than I expected, which almost never happens with them.

MARCUS: [laughs] I'll take faster-than-expected legal news any day.

PRIYA: Right? So, the short version — our existing BAA language, the way it's actually written, covers third-party processing broadly enough that it doesn't need a full renegotiation. What it needs is a short amendment, specifically naming the staging-layer window, since that's the piece I said wasn't explicitly contemplated.

DANIEL: That's — that's great news, honestly, I was bracing for something heavier than that.

PRIYA: Same, if I'm honest. I think I'd mentally prepared for a multi-week contract fight and instead I got a two-paragraph amendment.

NAOMI: That's a nice surprise for once, given how these things usually go around here.

PRIYA: I made sure legal mapped it specifically to what I asked for, too, not just a general assurance about the platform. I didn't want to accept "the BAA covers this generally" the way I pushed back on last time. I asked them directly — does the amendment language name the pre-normalization staging window specifically, not just processing broadly — and they confirmed yes, that's exactly what it does.

MARCUS: That's exactly the right thing to have checked, honestly, because a generic amendment wouldn't actually have closed the gap you were describing last time.

PRIYA: That's what I thought too. So I can say, at this point, what Curtis said back on the first call — I came away satisfied. I know that's a bit of a callback, but it felt like the right way to close the loop on it, given how much I leaned on the distinction between his answer and mine.

DANIEL: I noticed that too, actually — nice symmetry.

PRIYA: [laughs] Wasn't intentional when I said it, but I'll take credit for it anyway.

NAOMI: I'll make sure Curtis hears that directly, he'll appreciate it, honestly, I think he was a little worried his original answer was going to look wrong in hindsight, even though nobody said that.

PRIYA: No, and I want to be really clear about that, because I was clear about it at the time too — his answer was never wrong. The encryption, the tokenization, none of that changed. This was purely a paperwork gap, not a technical one, and I don't want that distinction to get lost now that it's resolved.

MARCUS: Right, and just to close that loop from my side too — the atomic-ingestion answer I gave last time still stands, nothing about the amendment changes any of the technical mechanics we walked through. This was always going to be a contracts fix, not an engineering one, which is basically what I said at the time, just nice to have it actually confirmed rather than left as a prediction.

PRIYA: Right, that's exactly how I understood it, and it's nice to have that confirmed cleanly rather than muddied by legal deciding they also wanted to touch something technical.

DANIEL: So where does that leave us, practically — is the amendment signed, or still in motion?

PRIYA: Still in motion, technically, but it's with our legal team for signature now, not sitting in a queue waiting on your side or mine to do anything further. I'd call it a formality at this point rather than an open question.

DANIEL: Got it. Do you have a rough sense of turnaround on their end?

PRIYA: Honestly, not precisely — legal doesn't really give me a number I'd trust enough to repeat to you. I'd guess a week, maybe a little less, but I don't want to commit you to a date I made up.

DANIEL: That's completely fair, I'd rather have your honest guess than a confident-sounding number that's wrong. I've definitely learned that lesson the hard way before.

PRIYA: [laughs] I appreciate that self-awareness. Either way, from where I sit, I'm not treating this as open anymore. It's resolved on the substance, it's just waiting on ink at this point.

MARCUS: That's a fair way to characterize it, yeah, substance and paperwork are two different clocks.

DANIEL: Good, I'll make sure that's reflected accurately on our side too — resolved, not just "in progress," since those read pretty differently to us internally.

PRIYA: Appreciated, I'd rather it be recorded accurately than optimistically.

MARCUS: Can I ask, actually — does the amendment need to go back through any kind of governance review on your side, or is it purely a legal signature at this point? Only asking because sometimes those things pick up an extra approval step nobody expects.

PRIYA: That's a fair question. As far as I know it's purely a legal signature, it's a narrow enough change that it shouldn't need to go back through governance the way a brand new BAA would. But I'll double check that assumption rather than just assert it confidently and be wrong.

MARCUS: Appreciate that, no need to chase it down urgently, just wanted to make sure nothing was quietly going to add another few weeks.

PRIYA: Good instinct, honestly, that's exactly the kind of thing that sneaks up on people. I'll confirm and let you know if I'm wrong about it being that simple.

DANIEL: Sorry, actually — before we move off this, can I ask, was that the same tool Curtis needed a security review on, or is that a totally different thread?

PRIYA: No, that's a different thing entirely — you might be thinking of the analytics access piece we talked through with Curtis, the de-identification conversation. This is just the BAA and the staging layer, totally separate track.

DANIEL: Ah, got it, my mistake, I was conflating two different threads there for a second.

MARCUS: Easy to do, they came up around roughly the same period and both involve Curtis in some capacity.

PRIYA: No worries, happens constantly with how much we've covered across these calls, I do the same thing internally more than I'd like to admit.

DANIEL: Okay — next thing on my list, segment ownership. I believe you said you'd decide on someone rather than let that sit open the way it had been.

PRIYA: I did, and I have an answer. Dana Whitfield, from marketing ops.

NAOMI: Oh, good, I don't think I know her directly, but the name's familiar.

PRIYA: She already does a version of this informally, honestly, she was the one people quietly routed segment questions to anyway, so it felt more like formalizing something real than inventing a new role out of nothing.

DANIEL: That's great, that's exactly the kind of thing that's better resolved with someone who's already doing the work than someone brand new to it.

PRIYA: That's what I thought too. I talked to her manager, it's official as of this week, she's the named point of contact for segment quality and adoption going forward, not just informally the person people happen to ask.

NAOMI: That's a relief, honestly, I think that's been sitting open since the very first call we had.

PRIYA: It had, yeah, and there wasn't a good reason for it to keep sitting there once I actually had the budget discretion to just decide it myself.

MARCUS: Good, I'll make a note that Dana's the right contact going forward for anything related to segment definitions or the outreach-ops side of things, rather than routing that through you or Naomi by default.

PRIYA: That's right, loop her in whenever that's relevant, she'll be expecting it, I already gave her a heads up that you all might reach out.

NAOMI: Does she need anything from us to get oriented, or is that more of a "she'll ask when she needs it" situation?

PRIYA: Probably the latter, honestly, she's not shy. If she needs a briefing document or something more formal, I'll ask, but my guess is she'll just start showing up to the relevant threads.

MARCUS: Practically speaking, once she's looped in, does she own the actual definitions going forward, or is she more the point of contact while the definitions themselves still get built jointly with your team?

PRIYA: Good question — point of contact and eventual owner of quality and adoption, I'd say, rather than someone hand-building every segment herself from day one. I don't think we've fully drawn that line yet, honestly, but that's roughly the shape of it.

MARCUS: That's a totally normal way for that role to start, for what it's worth, it tends to sharpen on its own once there's something live to actually own.

PRIYA: That's what I'm assuming too, I don't want to over-design the role before there's anything for her to actually do.

DANIEL: Works for us either way. Naomi, anything on the connector side worth flagging today, or is that just quietly proceeding?

NAOMI: Quietly proceeding, honestly, nothing dramatic to report. We're partway into the mapping work, on pace for the timeline we talked about last time, nothing's surfaced that changes that estimate.

PRIYA: Good, no news is good news on that one, I was half-expecting you to tell me something had gotten more complicated.

NAOMI: No, if anything it's been a little more straightforward than I braced for. The schema's messier than I'd like in a couple of spots, but nothing that's actually blocking progress, just the normal amount of annoying.

PRIYA: When you say messier, is that a "this will cost us extra days" kind of messy, or a "mildly irritating but absorbed into the existing estimate" kind of messy?

NAOMI: The second one, honestly. Field naming's inconsistent in a couple of places, nothing structural. It's the kind of thing where I mutter to myself for twenty minutes and then it's fine.

DANIEL: [laughs] That's a very relatable description of most data work, honestly.

NAOMI: It really is, I don't think that's unique to us.

MARCUS: That tracks with what we've seen on our side too, nothing's come up that changes the connector design we walked through last time.

NAOMI: I'll flag it if that changes, but right now it's genuinely just execution, not something that needs a conversation on a call like this.

PRIYA: Good, that's exactly the kind of update I want — either it's fine and quick to say so, or it's not and I want to know early. Nothing in between.

DANIEL: Sounds like a healthy way to run it, honestly.

PRIYA: Good. Okay, before I forget — I do want to give you an honest update on the other thing I said I'd chase, which is the legacy marketing tool question. And the honest update is: I don't have an answer yet.

DANIEL: That's alright, no rush on our end.

PRIYA: I did actually go talk to marketing about it, for what it's worth, I didn't just let it sit. But their answer was basically "we're mid-way through a totally unrelated tooling evaluation right now and don't want to make this decision in isolation from that." Which, fair, honestly, but it means I still can't give you a real answer today.

NAOMI: That tracks, marketing's been heads-down on something else for a few weeks now, I'd heard the same thing secondhand from a friend over there.

PRIYA: Yeah. So it's still genuinely open, not resolved, not close to resolved, I don't want to pretend otherwise just because I've been able to close out everything else on today's list.

DANIEL: I appreciate you being straight about that rather than papering over it to keep the call feeling tidy.

PRIYA: Does it block anything on our end, practically, or is it more of a later-scoping thing?

MARCUS: I don't think it blocks anything, no. Nothing we've architected assumes either outcome — whether this eventually absorbs campaign authoring too, or that tool stays in place indefinitely alongside it. It's fine to leave that genuinely open for now.

PRIYA: Good, that's what I thought, but I wanted to say it out loud rather than let it quietly vanish from the conversation just because everything else moved today.

DANIEL: Appreciate that, honestly — that's the kind of thing that's easy to let slide once the bigger items clear off the list.

PRIYA: Yeah, I've seen that happen before, the one open thing that never gets a real answer because nothing's forcing anyone to revisit it. I'd rather it stay visible, even unresolved, than disappear quietly.

NAOMI: That's a good instinct, for what it's worth, I've watched exactly that kind of thing get forgotten here more than once.

PRIYA: I believe it. Anyway — I'll keep chasing it, I just don't want to promise a timeline I don't actually have visibility into.

DANIEL: Completely reasonable. Before I get to the last item — can I ask where you landed with the proposal? I know you wanted to sit with it properly before reacting live on a call.

PRIYA: I've read through it, yeah. I don't want to get into numbers today, since that wasn't really the plan for this call, but nothing in it surprised me structurally, it matches what you all described verbally. I've got a couple of questions, but nothing I'd call a concern at this point.

DANIEL: Good, happy to walk through those questions whenever works, live or over email, whichever you'd prefer.

PRIYA: Let's save the specifics for the commercial conversation itself, honestly, so we're not splitting the same discussion across two calls.

DANIEL: That works. Also, small thing — did the SOC 2 report and the resend land alright, or is that still floating somewhere?

PRIYA: It landed, yes, both Curtis and I got it directly this time, no Derek's-inbox detour required. I did have IT sweep his inbox too, for what it's worth, nothing else important turned up, so that particular worry turned out to be smaller than I'd braced for.

NAOMI: Good, one less loose thread.

PRIYA: Agreed, small win, but I'll take it.

DANIEL: Completely reasonable. Okay — last real item on my list, and I think it's the good one: can we get a next step on the calendar? Something with an actual commercial conversation attached, now that the BAA piece is basically closed out.

PRIYA: Yes, let's do that. I don't want to leave this drifting the way the last one did, where I kept saying "in the next couple weeks" without committing to anything real.

DANIEL: I noticed that, no judgment at all, you were still getting oriented at that point.

PRIYA: [laughs] Fair, but I'm oriented now, so let's actually put a day on it. How does a week from this coming Thursday work for you both — that gives me enough runway to have the signed amendment in hand and to have actually sat with the numbers properly, rather than reacting live.

DANIEL: Let me just double check I'm not double-booked that day — give me one second.

PRIYA: Take your time.

DANIEL: Okay, no, that's clear on my end, Thursday works.

MARCUS: Hang on, actually — I think I might have something that morning, let me check. Yeah, I've got an internal thing that morning, but I should be free by early afternoon your time.

PRIYA: Afternoon's totally fine on my end, I don't have a preference between morning and afternoon that day.

DANIEL: Works for me too either way. Let's say afternoon, then, and I'll put a placeholder time and we can nudge it if it's awkward for anyone once it's actually on the calendar.

PRIYA: That works. I'd rather have Marcus there than force an earlier slot and have him half-present anyway.

MARCUS: Appreciate that, yeah, happy to join if there's anything technical worth walking through live, otherwise I'm fine being on standby in case something comes up.

PRIYA: I think it's mostly commercial at that point, but I'd rather have you there than not, in case something technical comes up in the conversation naturally, the way it has basically every other call.

MARCUS: Sounds good, I'll block it either way, better to be there and not needed than needed and not there.

DANIEL: Great, I'll get that on the calendar today and send an invite with an agenda attached, so it doesn't turn into an unstructured status check with nothing new to actually decide.

PRIYA: Appreciated, structure helps, especially since I want to actually make a decision in that conversation, not just have another round of information gathering the way today sort of started before we got moving.

DANIEL: Understood, that's the goal on our end too, we'd rather come with something concrete than another recap.

PRIYA: Good. Okay, I think that's genuinely everything on my list for today, which is a nice feeling after the last couple of calls.

NAOMI: Agreed, this one felt almost easy by comparison, no offense to how the last one went.

DANIEL: [laughs] None taken, I'll take "almost easy," we've earned a shorter one after that last session.

PRIYA: We really have. Thank you both, genuinely, for how you handled the BAA piece — I know it would've been easy to treat that as friction to be managed rather than a real question, and nobody did that.

MARCUS: That was never going to be our approach, honestly, glad it landed the way it did for everyone.

DANIEL: Agreed, and for what it's worth, questions like that one tend to make the eventual answer more trustworthy, not less, same thing I said to you the first time it came up.

PRIYA: [laughs] You did say that, I remember. I'll try not to make a habit of testing that theory every call, though.

DANIEL: [laughs] No complaints here if you do, honestly, it's better than the alternative.

NAOMI: I'll second that, I'd rather work through sharp questions now than discover something the hard way later.

PRIYA: Well, hopefully Thursday week is a little more routine, purely commercial, nothing this eventful.

DANIEL: I wouldn't bet on routine with this group at this point, but we can hope.

PRIYA: [laughs] Fair enough.

DANIEL: Alright, I think we're actually done early, which might be a first for this deal.

PRIYA: Don't get used to it, I'm sure I'll find something to keep open next time. I'll see you both Thursday week.

NAOMI: Bye, everyone, I'll go find Curtis and give him the good news in person.

MARCUS: Bye, thanks all.

DANIEL: Thanks, Priya, talk soon.
