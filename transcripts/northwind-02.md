---
opportunity: Northwind Logistics — Operational Data Unification
call_id: northwind-02
call_type: follow_up
day_offset: -5
duration_minutes: 46
participants:
  - name: Rachel Kim
    role: Account Executive
    org: Apex
  - name: Marcus Webb
    role: Solutions Consultant
    org: Apex
  - name: Kenji Watanabe
    role: Head of Data Platform
    org: Northwind Logistics
  - name: Lisa Ferreira
    role: Senior Analytics Engineer
    org: Northwind Logistics
  - name: Owen Brady
    role: Director, RevOps
    org: Northwind Logistics
---

RACHEL: Okay, looks like we've got a new face today — you must be Owen?

OWEN: Yep, that's me, sorry, let me just — one sec, my camera's being weird. There we go. Hey, everyone.

KENJI: Owen, this is Rachel and Marcus from Apex. Rachel, Marcus — Owen Brady, he's our director of RevOps, I mentioned last time we'd probably want to get him looped in once things were further along.

RACHEL: Right, yes, good to meet you, Owen, thanks for joining.

OWEN: Yeah, Kenji's been keeping me posted at a high level, figured it was time to actually get on a call rather than hear about it secondhand.

RACHEL: Sorry, quick aside — were you able to get parking okay? I know that building's a nightmare, someone told me about it once and I've never forgotten it.

OWEN: [laughs] Oh, I don't actually go into that office much, I'm mostly at our other site across town, this is a rare in-person day for me actually, so I lucked out.

KENJI: Owen's basically a ghost at headquarters, we joke about it.

OWEN: Hey, remote-adjacent is a lifestyle choice, I stand by it.

RACHEL: [laughs] Fair enough, sorry, unrelated, just curious.

MARCUS: Welcome. Should we do a quick recap for Owen's benefit before we get into anything new, or has Kenji already covered the ground?

OWEN: I've got the gist, honestly, don't need the full replay, but feel free to fill in gaps as we go if something doesn't make sense to me.

KENJI: That works. Actually, before we get into whatever Owen wants to cover, Lisa's got a quick update on the thing we owed you from last time, the correlating-fields mapping.

MARCUS: Great, yeah, I've been curious about that since we wrapped last time.

RACHEL: Same, go ahead, Lisa.

LISA: Yeah, quick version — I went through WMS, TMS, and the telematics feed. WMS and TMS are actually in decent shape, there's a shipment reference field in both, it's populated in something like ninety-plus percent of records, so that's a solid join key for most of the volume. Telematics is messier, there isn't a clean shipment-level identifier at all on that side, it's more tied to the vehicle and the route, so matching that back to a specific shipment is going to take some actual modeling work, roughly what you flagged as the risk last time.

MARCUS: Okay, that's really useful, and honestly not surprising given what you described about the carrier heterogeneity. Is the WMS-TMS piece clean enough that we could stand that up pretty quickly while the telematics matching gets worked out in parallel?

LISA: Yeah, I think so, that piece feels low-risk to me.

MARCUS: That ninety-plus percent number on WMS-TMS, is that consistent across all your facilities, or does it vary a lot by site?

LISA: It varies some, the newer facilities are cleaner, closer to ninety-eight, ninety-nine percent, it's really a handful of the older sites dragging the average down, I want to say low eighties for the worst one. But even the worst case is workable, it's not like it's fifty percent or something that'd make the whole approach questionable.

MARCUS: Okay, that's a manageable spread, that's good to know.

KENJI: Yeah, I'm feeling good about the technical side generally, I don't think there's anything blocking us there anymore, it's really just execution at this point.

RACHEL: That's great to hear, thank you both, that was fast turnaround.

OWEN: Can I jump in here, actually? I don't want to derail the technical stuff, but I do want to get to what I actually came prepared to talk about, if that's alright.

RACHEL: Of course, go ahead.

OWEN: So — I'll just be direct, because I think that's more useful than dancing around it. We're not only looking at you all. We've also been talking to a company called Tracewell, they do something pretty similar on the surface, and they've been pretty aggressive about it. So I want to understand, from a commercial standpoint, why we'd go with you over them, because right now I don't have a clean answer to that, and I'm the one who's going to get asked.

RACHEL: Sure, yeah, happy to talk through that. Can I ask what specifically they've put in front of you, just so I'm responding to the actual thing rather than guessing?

OWEN: Yeah — so, two things mainly. One, their number's lower. Not dramatically, but meaningfully, enough that it's going to come up in any comparison. And two, they told us three weeks to a live pilot, which is a lot faster than what I'm hearing from you all, even accounting for the identifier stuff Lisa just walked through.

RACHEL: Okay. So, on the timeline piece — I think a lot of that gap probably comes down to scope, honestly, three weeks sounds fast for something covering the same ground we've been discussing, so I'd want to understand what exactly their three weeks includes before treating that as apples to apples.

OWEN: Fair, I don't actually know the details of their scope that precisely, I'd have to go back and check. But even directionally, that's a real gap, and it's the kind of thing that's going to get asked about above my head, so I'd rather have a real answer than "probably scope."

RACHEL: That's fair. Can I ask, is Tracewell someone you sought out, or did they come to you?

OWEN: A bit of both, honestly — I'd heard the name before from a peer at another logistics company who uses them for something adjacent, and then separately their sales team reached out to us directly a few months back, before any of this was even on my radar. So it wasn't purely reactive to you all, if that's what you're asking.

RACHEL: No, that's fair, I wasn't trying to imply that, just trying to understand the shape of it.

OWEN: Yeah, no, it's a legitimate question. They've also apparently got a couple of reference customers in freight and distribution specifically, which matters to me, I'd rather not be the first logistics company figuring out someone's rough edges.

KENJI: That's a fair thing to weigh, though for what it's worth, from the little I've seen of their actual product, the reference customers might be using it for something narrower than what we'd need.

OWEN: Maybe, I haven't verified that independently, that's just what their team told me.

RACHEL: That's fair. Let me — honestly, I think the strongest thing I can point to is more on the reliability side than the speed side. Our lineage and audit capabilities are genuinely more mature, and given the kind of operational decisions you're going to be making off this data, that matters a lot more than shaving a couple weeks off setup.

OWEN: I hear you, but that's — that's a bit of a dodge, honestly, no offense. I asked about commercial terms and timeline and you're pivoting to a feature. I'm not saying the lineage thing doesn't matter, I just don't think that's actually answering my question.

RACHEL: No, that's — that's fair, sorry. Let me try again. I think part of what's happening is I don't have their number in front of me, so it's hard for me to engage with "meaningfully lower" without knowing what that actually means in dollars, and I'd rather not guess.

OWEN: That's reasonable, I'm not expecting you to have memorized their pricing, I'm more asking what your process is for responding to it once you do know.

RACHEL: Sure. Honestly, I think my instinct is usually to lead with value rather than matching a number directly, but I hear you that value framing isn't landing as an actual answer to what you asked, so let me not do that again.

OWEN: [laughs] Appreciate the self-awareness, at least.

RACHEL: No, that's — you're right, sorry, let me actually answer it. On price, I don't have their number in front of me, so I can't do a precise comparison right now, but I can come back with something concrete rather than talk in generalities.

OWEN: Okay, that's more useful. And to be transparent with you — it's not just the raw number, there's also a procurement angle. Our finance org already has a master agreement in place with Tracewell's parent company, through a completely different part of the business, a logistics-adjacent thing on the finance side. That makes the paperwork a lot easier on our end if we go with them versus standing up a brand new vendor relationship from scratch.

MARCUS: Can I ask, is that master agreement specifically with Tracewell, or with some larger parent company that Tracewell happens to be part of? Just trying to understand how directly it applies.

OWEN: It's with the parent company, Tracewell's technically a subsidiary, I think they got acquired a couple years back, so it's not like we already have paper specifically with the product team you'd be dealing with day to day, but legal treats it as the same counterparty, so from a procurement standpoint it functions the same as already having a relationship.

MARCUS: Got it, that's a meaningful distinction to understand, thank you. Does that master agreement cover data platform spend specifically, or is it more general vendor terms that would need a separate rider for something like this?

OWEN: Honestly, I don't know that level of detail off the top of my head, I'd have to check with our finance contact. It's possible it's general enough to cover this, or it's possible there's more paperwork than I'm assuming, I don't want to overstate how easy it actually is until I've confirmed it.

MARCUS: That's fair, I appreciate you not overselling your own side of it either.

OWEN: [laughs] Feels only fair given I've been asking you all not to oversell. I'll get you an answer on that once I've actually checked rather than guess at it now.

RACHEL: That's a really specific and legitimate consideration, thank you for laying that out clearly. Yeah, agreed, that's — that's a real factor, I won't pretend procurement friction doesn't matter, I know it does practically even when it's not about the product itself.

OWEN: Right, and to be clear, I'm not saying it's decided, I'm saying that's the bar you're up against, and right now the honest picture is: comparable price, faster stated timeline, and an easier procurement path on their side. So I need you to give me something that outweighs that, or I genuinely don't know what I tell my boss.

KENJI: Can I add something here, actually? Just from the technical side — I don't think the technical picture is close, for what it's worth. I haven't gone deep with Tracewell, but from what little I've seen, it didn't look like it handled the identifier matching problem with anywhere near the seriousness Marcus's team has, it looked more like a dashboard layer bolted on top, similar to some other stuff we've looked at in the past. That's not nothing, Owen, that's a real difference, even if it's not the thing you're asking about right now.

OWEN: No, that's useful, I appreciate you saying that, genuinely. I just can't take "the technical fit is better" to my boss on its own, I need the commercial side to at least not be embarrassing, even if it's not winning on price.

RACHEL: That's a completely reasonable ask. Let me be honest about where I am right now — I don't have a number in front of me that I can commit to on this call, and I don't want to make something up just to have an answer. What I can do is go back today, get real pricing pulled together with the scope we've actually discussed, and come back to you specifically with something that addresses the procurement question too, since that's clearly not just about the sticker price.

OWEN: Okay. I appreciate you not just throwing out a number to make me feel better in the moment, for what it's worth, I've had vendors do that and it's usually wrong.

RACHEL: Yeah, I'd rather come back with something real than something fast and wrong. I will say, since we're being direct with each other today — I'd rather lose this on a real gap than win it because you didn't have good information, so if Tracewell's genuinely the better fit once all this is on the table, I'd rather know that clearly than have this drag out.

OWEN: I appreciate you saying that, genuinely, that's not the kind of thing I usually hear from a vendor mid-competitive-process.

RACHEL: Well, I'd rather be the person who said that than the person who wasn't, if I'm being honest about it.

MARCUS: On the procurement piece specifically — I don't know the details of how that master agreement works structurally, but that's worth us actually looking into too, whether there's any path to something similar or at least a smoother process on our side, rather than just accepting that's automatically a point in their favor.

OWEN: Yeah, if there's anything you can do there, that would help. I'm not going to pretend it's the deciding factor on its own, but it's a real friction point, and friction points add up when someone's trying to decide between two options that are otherwise close.

RACHEL: Can I ask, out of curiosity — has anyone else at Northwind talked to Tracewell, or is this really just you at this point?

OWEN: Just me so far, on our side. I mentioned it to Kenji in passing a couple weeks ago, but this is really the first time it's being discussed with the full group.

KENJI: Yeah, first I'm hearing the specifics too, honestly, Owen mentioned the name once and I didn't think much of it at the time.

OWEN: Yeah, I wasn't trying to keep it secret, it just wasn't developed enough to be worth a whole conversation until now.

RACHEL: No, that makes sense, I appreciate you bringing it fully into the open rather than letting it sit in the background.

KENJI: Can I ask, Owen — is this actually close to a decision, or is this more you doing diligence in parallel because that's just good practice? I ask because it changes how urgently we should treat pulling this together.

OWEN: Honestly, it's not imminent-imminent, but I wouldn't call it lazy diligence either. I'd say if Apex doesn't come back with something reasonably compelling in the next little while, Tracewell starts looking like the easier path, mostly because of the procurement thing, not because anyone's decided they're better.

RACHEL: Understood, that's a clear and fair way to frame it, thank you.

LISA: Can I say something, actually, from a slightly different angle — I don't have a horse in the commercial race, but from a pure "will this actually solve our problem" standpoint, I'd be pretty disappointed if we picked a worse technical fit to save on procurement friction. That's not my call to make, obviously, I just wanted that on the record.

OWEN: Noted, and for what it's worth, that's exactly the kind of input I need to be able to weigh this properly, so thank you for saying it.

KENJI: Yeah, agreed with Lisa, though I also get that I'm not the one who has to deal with procurement, so I get why Owen's weighing it the way he is.

OWEN: I don't love being cast as the procurement guy who doesn't care about quality, for the record. If the technical gap turns out to be as real as Kenji's describing, that matters a lot to me too, I just can't be the one who ignores a legitimate cost and process difference because the demo was impressive.

LISA: No, that's fair, I didn't mean to imply otherwise, sorry if it landed that way.

OWEN: No, you're good, I'm just being a little defensive, it's a common dynamic in my job, I promise I'm not actually the villain here.

KENJI: [laughs] Nobody said villain.

OWEN: Preemptive defensiveness, my specialty. I don't love being the guy in the room pushing on price when everyone else is excited about the product, but that's kind of the job.

RACHEL: No, it's a legitimate role to play, and honestly I'd rather have this conversation directly with you now than have it happen invisibly somewhere I can't respond to it.

OWEN: Yeah, agreed, that's why I wanted to actually get on a call instead of just relaying questions through Kenji.

RACHEL: Appreciated. So, to make sure I've got this right — I'll come back with real pricing against the scope we've discussed, I'll look into whether there's anything we can do on the procurement friction side, and I'll try to get a clearer sense of what Tracewell's three-week timeline actually includes so we're comparing the same thing, if you're willing to share more detail on that as you get it.

OWEN: Yeah, I can share what I know, within reason, obviously I'm not going to hand you their proposal, but directionally I can tell you what's actually in scope versus what's implied.

RACHEL: That's fair, I wouldn't ask for the actual document anyway.

OWEN: One more thing, actually, while I'm thinking of it — is there flexibility on contract length? Because part of what makes the Tracewell number look better on paper is they're offering a shorter initial term, and I know sometimes a lower headline price comes with a longer lock-in that isn't actually better for us.

RACHEL: That's a really good question, and honestly I don't want to promise flexibility I haven't actually confirmed internally. What I can say is that's a completely fair thing to ask for, and I'll find out what's actually possible rather than assume our standard term is the only option.

OWEN: Appreciate that, that's exactly the kind of thing that's easy to overlook when you're just comparing two numbers side by side.

KENJI: Yeah, that's a good catch, I wouldn't have thought to ask that.

OWEN: It's the kind of thing that bites you a year in if nobody asks upfront.

MARCUS: I'll also put together something on the technical differentiation that's a bit more concrete than what I said a minute ago, actual specifics rather than a general claim about maturity, so Owen's got something more substantive to bring internally if it's useful.

OWEN: That would help, yeah, something I can actually point to rather than "trust us, we're better."

MARCUS: To give you a preview rather than making you wait entirely — the identifier matching approach we walked through with Kenji and Lisa last time, the event-time ordering, the confidence-tiering across data sources of different quality, that's not surface-level stuff, that's the kind of thing that only matters once you're actually running this at your volume and seeing the edge cases. A dashboard layer bolted onto one system's view doesn't have to solve any of that, because it's not actually unifying anything underneath. I'd want to verify what Tracewell's architecture actually does before saying more than that, but that's the shape of the gap I'd expect.

OWEN: Okay, that's useful, that's more specific than what I had. I don't know enough to independently verify it, but at least it's a concrete claim I can go ask them about directly, which is more useful than a vague "we're more mature."

MARCUS: That's fair, and I'd rather you go verify it and come back skeptical than just take my word for it.

OWEN: Appreciate that, that's actually a good sign in itself, vendors who want you to just trust them make me more nervous, not less. Can I ask one more thing, actually, sorry — on the identifier matching gap you mentioned, Marcus, how long would it realistically take to close that, roughly? Because if it's months, that eats into the timeline argument regardless of everything else we've talked about.

MARCUS: I don't want to give you a number I'd have to walk back, honestly, that's genuinely dependent on what Lisa finds when she digs into the telematics side specifically, which she flagged as the open piece. My rough instinct, based on similar customers, is weeks rather than months, but I'd rather confirm that against your actual data before putting it in front of you as a commitment.

OWEN: Okay, that's fair, I'd rather you say that than make something up to sound more competitive.

LISA: Yeah, I can probably have a better read on that within the same timeframe as the pricing stuff, so it doesn't have to be a separate wait.

RACHEL: That's helpful, I'll fold that into what I bring back too, so it's a complete picture rather than pricing in isolation.

KENJI: I think that's the right next step, honestly. I don't think we solve the commercial question today, and I don't think we should pretend to.

RACHEL: Agreed, I'd rather leave this genuinely open than manufacture a false resolution on the call.

OWEN: Yeah, I appreciate that too, for what it's worth. I've sat through calls where a vendor tries to close something out that obviously isn't closed, and it's not a good look.

RACHEL: Well, hopefully we're doing the opposite of that today.

OWEN: So far, yeah.

RACHEL: Okay — in terms of timing, how soon do you need something back from us to actually be useful, rather than me just picking an arbitrary date?

OWEN: I'd say sooner is better, obviously, but I'm not going to pretend there's a hard cutoff this week. If I had to put a rough boundary on it, I'd want something in hand before too much more time passes, a couple weeks out feels like it's pushing it, sooner than that would be better.

RACHEL: Understood, I'll treat that as the real constraint and try to move faster than that if I can. Can I also ask — once I come back with something, is this a conversation that happens with just you again, or does it need to go to a wider group at that point?

OWEN: Depends what you come back with, honestly. If it's genuinely compelling, I can probably carry it forward myself initially. If it's close or ambiguous, it probably needs to go up a level, to my boss and possibly whoever owns the budget on Kenji's side too.

KENJI: That would be whoever I report to, ultimately, though I haven't looped her in yet either, similar to what Owen's describing on his side.

RACHEL: Got it, that's helpful to know, I'll keep that in mind for how I frame whatever we send over.

MARCUS: Same on my end for the technical write-up.

KENJI: Good. Lisa, anything else on your side before we wrap, or are we good?

LISA: No, I'm good, I think my part's done for now until there's something new to react to.

RACHEL: Great. So, to close this out — no resolution on the competitive question today, and I don't want to pretend otherwise. I'll come back with real pricing, something on procurement, and a sharper technical comparison, and we'll go from there.

OWEN: That works for me. Appreciate you not trying to spin this into something more settled than it is.

KENJI: Yeah, agreed, this was a useful one even without a clean ending.

RACHEL: Well, thank you all, and Owen, genuinely, thanks for being direct, it's a lot more useful than vague pressure would've been. I'd much rather work a real objection than guess at one.

OWEN: Yeah, well, hopefully what you bring back makes my job easier rather than harder.

RACHEL: That's the goal.

OWEN: Yeah, no problem. Talk soon, I guess, once you've got something back to me.

RACHEL: Will do.

MARCUS: Thanks, everyone, bye all.

KENJI: Bye.

LISA: Bye.
