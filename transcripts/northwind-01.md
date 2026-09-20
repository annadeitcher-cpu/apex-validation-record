---
opportunity: Northwind Logistics — Operational Data Unification
call_id: northwind-01
call_type: technical_validation
day_offset: -14
duration_minutes: 81
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
---

RACHEL: Okay, I think we're all set — Kenji, Lisa, can you both hear me okay? I had some echo on my end a second ago.

KENJI: Yeah, sounds fine now.

LISA: Yep, all good.

RACHEL: Great, sorry about that, might've been my headset. So, thanks for making the time — I know eighty minutes is a real chunk of a Wednesday, we'll try to be efficient about it.

KENJI: No, this is good, honestly, we'd rather do one real session than a bunch of thirty-minute check-ins where we never actually get anywhere.

RACHEL: Agreed. So, quick intros — I'm Rachel, I'm the account exec on this from Apex, and this is Marcus, our solutions consultant, he'll carry most of the technical side.

MARCUS: Hey, good to meet you both properly. I think I've seen your names on an email thread or two but this is the first time we've actually talked.

KENJI: Yeah, that's probably right. I'm Kenji, I head up data platform here — so warehouse systems, transportation, a bit of everything data-adjacent ends up on my desk eventually, whether I want it or not.

LISA: [laughs] That's generous phrasing. I'm Lisa, senior analytics engineer, I work under Kenji, I'm probably going to be the one actually building and living with whatever we end up doing here.

RACHEL: Perfect, that's exactly the right mix for today. So, I know we talked briefly on the intro call about the general shape of the problem, but I'd love to actually hear it from you two directly, in your own words, rather than me summarizing it back at you and getting it slightly wrong.

KENJI: Sure, yeah. So — high level, we're a logistics and supply chain company, we run distribution centers, we've got our own fleet plus a bunch of contracted carriers, and the core problem is that our operational data lives in, honestly, probably six different systems that don't talk to each other in any coherent way. Warehouse management system is one, transportation management is a separate system entirely, we've got telematics data coming off the trucks, there's an ERP that has its own view of inventory, and then a handful of spreadsheets that, unofficially, are load-bearing for things they really shouldn't be.

LISA: The spreadsheets are the part that keeps me up at night, honestly.

KENJI: [laughs] Fair, yeah. So the practical effect of all this is that if something goes wrong operationally — a shipment's delayed, there's a discrepancy between what the WMS says is in a facility versus what the TMS thinks got dispatched — figuring that out takes way longer than it should, because someone has to manually go stitch together data from three or four different systems to even understand what happened, let alone fix it.

MARCUS: Can you give a concrete example of that? Like an actual instance where that stitching-together process caused a real problem.

KENJI: Yeah, actually — there was one a few months back, pretty embarrassing one. We had a cross-dock delay at one of our regional facilities, and the customer found out about it before we did, because their own tracking showed the shipment sitting still for way longer than expected, and they called our ops team asking what was going on, and nobody internally could answer that question quickly. It took, I want to say, most of a day to actually piece together why it happened, and by then the customer relationship damage was already done, even though the underlying issue itself wasn't even that serious.

LISA: Yeah, and that's not a one-off, that's just the most memorable one. Smaller versions of that happen basically weekly, it's just usually not visible enough externally to become an actual incident.

RACHEL: That's a really concrete example, thank you. And when you say "figuring it out took most of a day" — is that mostly Lisa's time, or does that pull in other people too?

LISA: It pulls in a bunch of people, honestly, that's part of what makes it expensive beyond just my time — usually it's me plus someone from ops plus whoever's on-call from the warehouse side, all trying to reconstruct a timeline from systems that don't share a common view of, like, what even counts as the same shipment across each system.

KENJI: Right, there isn't a unified identifier that reliably ties a shipment across all these systems, that's honestly a big part of the technical mess underneath the operational mess.

RACHEL: Can I ask, just for scale — how many facilities are we talking about, and roughly what's the fleet size, owned versus contracted?

KENJI: We run eleven distribution centers ourselves, plus we lease space in a few more during peak season that come and go. Owned fleet is a few hundred trucks, but the contracted carrier network is way bigger than that, we're talking dozens of carriers, some of them tiny regional operators, some of them pretty large.

LISA: And that carrier diversity is actually a huge part of the mess, honestly, because every carrier's telematics setup is slightly different, some of them barely have any digital tracking at all, they're calling in updates.

KENJI: Yeah, the long tail of small regional carriers is rough. Our biggest carriers have decent telematics integrations, but the smaller ones, sometimes it's genuinely a dispatcher on the phone updating a spreadsheet, which, obviously, doesn't feed into anything automatically.

MARCUS: Okay, that heterogeneity is really useful to know, that's going to matter for how we think about ingestion sources, since it's not going to be one clean telematics feed, it's going to be a mix of qualities.

RACHEL: And Kenji, sorry, going back to the inventory discrepancy piece you mentioned — is that a frequent thing, or was that specific incident more of an outlier?

KENJI: It's not rare, unfortunately. I'd say some version of a WMS-versus-TMS mismatch happens most weeks somewhere in the network, it's just usually minor enough that it self-resolves before it becomes a customer-facing problem. It's really only the ones that compound with something else, like the ice storm thing we'll get to, or just bad timing, that turn into an actual incident.

LISA: Yeah, and honestly, we probably don't even know about most of the minor ones, because nobody's watching for them proactively, they just sort of get absorbed into the noise of a normal operating day.

MARCUS: That's a really common pattern, actually — the visible incidents are usually just the tip of a much bigger iceberg of smaller stuff that never surfaces because there's no systematic way to catch it.

KENJI: Yeah, that's a good way to put it, honestly, that's probably exactly what's happening.

MARCUS: Okay, that's really useful context. Roughly what volume are we talking, in terms of events or transactions — like how many shipments, how many telematics pings, that kind of thing, just so I have a sense of scale?

KENJI: Shipment volume's in the tens of thousands a day across the network. Telematics is way higher than that, obviously, since that's continuous positional data off every truck, that's — I don't have the exact number memorized, but it's in the millions of events a day once you add it all up.

LISA: Yeah, telematics is the one that actually strains things technically, the shipment-level stuff is comparatively tame.

RACHEL: Got it, that's helpful for scoping. Should we get into the product side now, or is there more current-state to cover first?

KENJI: I think we've covered the core of it, we can always circle back if something specific comes up.

MARCUS: Great, let me share my screen then. Can you both see okay?

LISA: Yep.

KENJI: Yeah, looks good.

MARCUS: Okay, so — given what you're describing, I want to start with a piece called Streamline Ingest, because I think it maps pretty directly onto the telematics volume problem specifically. The core idea is handling sub-minute ingestion for high-volume event streams, so rather than telematics data landing in batches on some delay, it's ingested close to real time, and it's immediately queryable alongside your other operational data, not sitting in some separate fast-moving system that's disconnected from the slower-moving warehouse and transportation data.

KENJI: Okay, when you say sub-minute, what does that actually mean in practice — like, is that end-to-end from a ping leaving a truck to it being queryable, or is that just the ingestion step, with more latency added elsewhere?

MARCUS: That's end-to-end for the ingestion and availability piece specifically — from the event landing at our ingestion layer to being queryable in your warehouse is sub-minute, typically much faster than that in practice, more like single-digit seconds for a lot of customers, but I'd rather commit to the conservative number. Obviously the actual truck-to-ingestion-layer latency depends on the telematics provider's own transmission behavior, that's outside what we control.

LISA: Given what Kenji just described about carrier heterogeneity — how does ingestion actually handle the fact that some carriers are sending clean structured telematics data and others are effectively a person typing into a form? Is that two totally different pipelines, or does it normalize somehow?

MARCUS: It can be modeled as multiple sources feeding the same underlying entity, so a structured telematics feed and a manually-entered status update can both ultimately represent "this shipment's current known location," just with very different confidence and freshness characteristics attached. The system doesn't pretend they're equally reliable — you'd want to carry some notion of source quality or recency alongside the data itself, so downstream consumers, like an activation rule, can account for that rather than treating a five-minute-old GPS ping the same as a two-hour-old phone call.

LISA: Okay, that's a good answer, because if it just blended everything together with no sense of confidence, that would honestly be worse than what we have now in some ways, at least right now a human knows to distrust the phone-call updates.

KENJI: Yeah, that's a real concern, I'm glad you asked that.

MARCUS: Yeah, it's a fair thing to push on, "unifying" data across wildly different quality tiers without preserving that distinction is a classic way to make a system feel smart while actually making decisions worse.

LISA: Okay, that's — that's actually a meaningfully different world than what we have now, our current telematics feed batches every fifteen minutes, so even the "current" position data we're looking at is stale by the time anyone sees it.

KENJI: Yeah, fifteen minutes doesn't sound like much until you're trying to explain to a customer why their shipment looked stationary on the map for longer than it actually was.

MARCUS: Right, that's exactly the kind of gap this is meant to close. And once it's ingested, that's where it becomes useful for the unification problem more broadly — because now you've got telematics, WMS, and TMS data landing in the same place, on a common timeline, rather than three separate timelines that someone has to manually reconcile after the fact.

KENJI: Okay, and the "common timeline" part — does that require us to have already solved the unified-identifier problem I mentioned, the fact that a shipment doesn't have one consistent ID across systems? Or is that something the platform helps with?

MARCUS: That's a fair question, and I don't want to overstate this — the platform doesn't magically invent a unified identifier if one doesn't exist anywhere in your source data. What it can do is apply matching logic across sources based on whatever correlating fields do exist — so if there's a shipment number, a PO reference, a trailer ID, whatever the closest thing to a shared key is across systems, that can be used to stitch records together, even if it's imperfect. But if there's genuinely no correlating field between two systems at all, that's more of a data modeling problem on your end that we'd need to work through together, not something the platform solves on its own.

KENJI: And just to make sure I'm tracking — when you say "matching logic," is that something that runs once during setup and then stays static, or does it keep adapting as new data comes in?

MARCUS: It's not a one-time thing, it can be refined over time as you learn more about which fields are reliable and which aren't, but I wouldn't call it "adapting" in some autonomous machine-learning sense either — changes to the matching logic are deliberate, someone decides to adjust the rules based on what they're observing, it's not silently reshaping itself in the background in a way that would be hard to audit later.

KENJI: Okay, good, I was worried you were going to say it's some black-box model that just figures it out, because that would make debugging a mismatch basically impossible.

MARCUS: No, definitely not, that would undermine the whole lineage and auditability story we're about to get into anyway, so it wouldn't make sense to build it that way.

LISA: Okay, that's honestly the most credible answer I could've hoped for, because I've had a vendor tell us before that their system would "automatically unify" our shipment data and it turned out to mean approximately nothing once we actually tried it.

MARCUS: [laughs] Yeah, I'd rather be upfront that this is real modeling work than let you find that out the hard way three months in.

RACHEL: Right, and to be clear, this is basically the same underlying database technology under the hood, so it's not like we're asking you to stand up a whole separate data warehouse alongside your existing one —

MARCUS: Sorry, small correction — it's not the same underlying database technology necessarily, it depends on what you're running, it's more that we're not requiring a separate copy of your warehouse, the activation and matching logic runs against whatever you've already got. Different thing than what I think you just said.

RACHEL: [laughs] Right, yes, that's what I meant, I said that wrong, thank you for catching it.

KENJI: [laughs] No worries, we figured that's what you meant.

RACHEL: That tracks with a lot of what we hear, honestly, "automatic unification" is one of those phrases that tends to fall apart under any real scrutiny.

KENJI: Yeah. Okay, well, I appreciate the honesty there, that's actually reassuring in a weird way.

LISA: Can I ask something slightly more in-the-weeds — how does this handle events that arrive out of order? Because with the smaller carriers especially, we sometimes get status updates that arrive after a later status has already come in, like a "picked up" update showing up after we've already got a "delivered" update for the same load, just because of how delayed their reporting is.

MARCUS: Yeah, that's a real scenario and it's handled by event time rather than arrival time — so the system tracks when something actually happened, based on whatever timestamp the source provides, versus when it showed up in the pipeline, and ordering and state resolution are based on the former, not the latter. So a late-arriving "picked up" event with an earlier timestamp than an already-processed "delivered" event would be recognized as out of sequence rather than just being applied naively as if it were the newest thing that happened.

LISA: Okay, and what happens practically when that's detected — does it just silently reorder, or does something flag it?

MARCUS: It reorders correctly for the purposes of state, but genuinely conflicting or suspicious sequences — like a "delivered" event followed by an earlier-timestamped "picked up" that doesn't fit any sane explanation — those can be flagged for review rather than silently resolved, since at that point it might indicate a data quality issue with the source rather than just normal latency.

LISA: Okay, that's a solid answer, that's honestly better thought through than I expected for what's kind of an edge case.

KENJI: Yeah, agreed, that's good.

LISA: One more on that — does the visual trace view work the same way for something that never fired, like, can I ask "why didn't this get flagged" the same way I could ask "why did this get flagged"? Because in my experience the missing-alert case is usually the harder one to investigate.

MARCUS: Yeah, that's supported too, and honestly you're right that it's usually the harder case — you'd be able to query against the historical state to see what the rule would have evaluated to at a given point in time, so you can distinguish "the rule correctly didn't fire because conditions weren't met" from "the rule should have fired but something upstream prevented it," which are very different failure modes to explain to someone asking why they weren't warned.

LISA: Okay, good, that's exactly the harder direction, I'm glad it's not an afterthought.

MARCUS: Should I keep going, or do you want to sit with the ingestion piece a bit more?

KENJI: No, keep going, I think we've got the core of it.

MARCUS: Okay, so the other piece I want to show is Warehouse Native Activation, and this is really about what happens once that unified operational picture exists — instead of standing up a separate reporting or alerting system that requires copying all this data somewhere else, the activation layer runs directly against your warehouse, so dashboards, alerts, whatever downstream consumption you need, reads current state directly rather than from some secondary copy that's inevitably a bit stale.

LISA: Can you give an example of what "activation" actually looks like here? Like, concretely, what's the output?

MARCUS: Sure — so, take the cross-dock delay scenario Kenji described. If you've got a rule defined, something like "flag any shipment that's been stationary at a facility longer than expected dwell time for that facility," that rule can run continuously against the unified, near-real-time data, and when it fires, it can push an alert wherever your ops team actually needs to see it — could be a dashboard, could be a Slack channel, could be pushing into whatever ticketing or ops tooling you already use.

KENJI: Okay, that's — that's basically describing the exact scenario I brought up earlier, almost uncomfortably specifically.

MARCUS: [laughs] I promise that wasn't scripted, it's just a genuinely common pattern for logistics customers specifically.

LISA: And the rule definition — is that something my team builds, or is that more of a joint thing during setup?

MARCUS: It's something your team defines and owns, we're not deciding what counts as an operationally significant delay for your network, that's domain knowledge that has to come from you. What we provide is the mechanism for that rule to run continuously against current data and route the output wherever it needs to go, not the judgment of what the rule should be.

KENJI: That's the right boundary, honestly, similar to what I'd expect — I wouldn't want a vendor guessing at our operational thresholds.

LISA: Can I ask about who actually gets to define these rules, practically — is that a single admin, or can multiple people on my team create and edit them, and if so, is there any protection against two people defining conflicting rules without realizing it?

MARCUS: Multiple people can be granted access to define rules, it's not locked to a single admin, that wouldn't scale for most teams. On the conflict question — there's visibility into existing rules so you're not working blind, you'd be able to see what's already defined before creating something new, but I'll be honest, it's not going to proactively stop two similar-but-not-identical rules from both existing if two people define them independently without checking first. That's more a process question for your team than something the tooling fully solves for you.

LISA: Okay, that's a fair answer, I'd rather know that upfront than assume it's magically prevented and then find out it isn't.

KENJI: Yeah, we'd probably want some kind of light review process for new rules regardless, just given how many hands might eventually be touching this.

MARCUS: That's a reasonable practice, a lot of customers end up doing something like that informally, a quick second pair of eyes before a new rule goes live.

LISA: Can I ask about alert fatigue, actually? Because I could see this going wrong in the opposite direction, where suddenly everyone's getting flooded with alerts because the thresholds weren't tuned well, and then people just start ignoring all of them, which honestly might be worse than the current silence.

MARCUS: Yeah, that's a really legitimate worry, and I've seen it happen with other customers when thresholds get set too aggressively out of the gate. The way we'd usually approach it is starting rules in a kind of shadow mode, where they evaluate and log what they would have flagged without actually pushing alerts anywhere yet, so you can tune thresholds against real data before anything's actually surfacing to a human. Nobody wants to be the reason the ops team starts muting a Slack channel.

LISA: Okay, that's a good answer, that shadow mode thing specifically addresses what I was worried about. I've def muted channels before because of exactly this problem with a different tool.

KENJI: [laughs] We all have. Actually, remind me to tell Lisa about the muted-Slack-channel thing later, that's basically our current life with a couple of the monitoring tools we already run.

LISA: Oh, don't get me started on that, we've got at least two channels right now that are essentially graveyards because someone set the thresholds too sensitive years ago and nobody's gone back to fix it, and at this point fixing it feels like its own project nobody has time for.

MARCUS: Yeah, it's an extremely common failure mode, honestly, over-alerting kills adoption faster than almost anything else, and it's a lot harder to win back trust in a channel once people have already tuned it out than it is to just get the thresholds reasonably close from the start.

KENJI: I guess one thing I'm wondering about, and it's maybe a bigger question than alert tuning — we've actually already got some dashboards built on top of our current, admittedly bad, data setup. Nothing amazing, but people use them. Is moving to this going to mean rebuilding all of that from scratch, or is there some path where the existing reporting layer can keep working while the underlying data gets better?

MARCUS: That's a fair thing to raise, and the honest answer is it depends on how those dashboards are built today — if they're pulling from tables or views that we can continue to populate or that map cleanly onto the new unified model, there's often a path to pointing existing dashboards at the improved data with fairly minimal rework. If they're built directly against some fragile one-off export process, that's more likely to need rebuilding regardless of what we do here, honestly, that fragility is probably going to bite you eventually either way.

KENJI: Yeah, that's fair, some of it is probably the fragile kind, if I'm being honest with myself.

LISA: Yeah, a couple of them are held together with what I'd generously call duct tape.

MARCUS: I don't want to promise "zero rework," because I don't know enough about your specific dashboards to say that honestly, but I also don't want you to assume "total rebuild" by default, it really depends on the individual case. That's something worth actually looking at together once we're further along, rather than me guessing on a call.

KENJI: Okay, that's — yeah, I think that's a fair thing to leave open for now, I don't think either of us can resolve it today anyway without actually looking at the dashboards.

RACHEL: Agreed, let's make a note to come back to that rather than guess. Should we take a quick tangent, actually — Kenji, didn't you mention on the intro call something about a facility that had a pretty rough peak season? I'm curious if that's related to any of this or a totally separate story.

KENJI: [laughs] Oh, god, yeah, that's — that's a whole other thing, that was actually a weather story more than a data story. We had a facility that got hit by a surprise ice storm during peak, and it wasn't so much that our systems failed, it's that half our contracted carriers just couldn't get trucks in or out for like two days, and there was nothing any dashboard was going to fix about that particular problem.

LISA: Yeah, that one was more "acts of God" than "acts of bad tooling." Though I will say, even then, better visibility would've at least let us communicate proactively with customers instead of them finding out from their own tracking again.

KENJI: True, fair point.

RACHEL: [laughs] Sorry, I derailed us, that wasn't really relevant, I was just curious.

KENJI: No, it's fine, honestly kind of nice to talk about something that wasn't our fault for a change.

MARCUS: Should I keep going on activation, or is there more to unpack there?

KENJI: No, let's keep moving.

MARCUS: Okay. So the other thing I want to touch on, and this ties into the unified-identifier conversation from earlier, is lineage. There's a capability called Lineage Graph that tracks, for any piece of operational data or any alert that fires, exactly what it was derived from and when — so if six months from now someone asks "why did this shipment get flagged, or why didn't it," there's an actual traceable answer rather than someone having to reconstruct it from memory or logs scattered across systems.

LISA: Okay, that's actually really relevant, because right now if a rule — well, we don't really have automated rules today, but hypothetically, if something like that existed and it misfired, or failed to fire when it should have, there'd be basically no way to diagnose why after the fact.

MARCUS: Right, exactly that scenario — the lineage record would show you what data the rule evaluated against at the time, so you could actually distinguish "the rule was wrong" from "the data was late" from "the data was wrong," which are three very different problems that currently probably all just look like "the alert didn't fire" from the outside.

KENJI: Yeah, that distinction actually matters a lot for us, because right now when something like that goes wrong, half the debugging time is just figuring out which of those three things it even was. Can I ask a follow-up on that — the lineage record itself, where does that live, is that something Lisa's team would need to build queries against, or is there a more usable interface for someone who isn't going to write SQL to trace through it?

MARCUS: There's a visual trace view for the common case — you can click into a specific alert or a specific record and see the derivation path without writing anything. For deeper investigation, the underlying lineage data is also queryable directly, if someone wants to do something more custom than the UI supports. So it's not either-or, it's a usable default with an escape hatch for when someone needs more.

LISA: Okay, that's good, because realistically most people investigating one of these issues are not going to want to write a query, they just want to click and see what happened.

KENJI: Yeah, agreed, that's the right default.

RACHEL: That's a good place to actually ask — Kenji, when you evaluated some of the reporting tooling that sits on top of your TMS a while back, was that a similar debugging problem, or was that more just about the reports themselves being clunky?

KENJI: Oh — yeah, that was, honestly a bit of both. We looked at a couple things at the time, there was a smaller add-on our TMS vendor sells, and then separately we did a brief look at Corvus, which I think does something adjacent to this, more on the visibility and tracking side specifically. Neither of those really addressed the underlying unification problem though, they were both kind of bolted onto one system's view of the world rather than actually pulling everything together, so we didn't get very far with either of them. Anyway — that's really a separate thread from what we're doing today, I don't want to get too far into old vendor history.

MARCUS: No, that's helpful context regardless, thank you. Should I keep going, or does anyone have more questions on lineage first?

LISA: No, I think that's clear, let's keep moving.

MARCUS: Okay — the last piece I want to touch on, and I think this is actually a good one to end the product walkthrough on, is really just tying all three of those together into what a day-to-day workflow looks like. So, telematics and WMS and TMS data land near-real-time through Streamline Ingest, it's modeled and matched across sources as best the available identifiers allow, activation rules run continuously against that unified picture and route alerts wherever your ops team lives, and lineage gives you the ability to debug any of it after the fact. That's really the whole loop.

KENJI: Okay. That's — that's a genuinely coherent story, I'll say that, more coherent than I was expecting walking in, honestly.

RACHEL: [laughs] I'll take that as a compliment.

KENJI: It is one, don't worry.

MARCUS: I do want to be honest about one thing before we move on, though, because I don't want to leave you with an overly rosy picture — the identifier matching piece we talked about earlier, that really is going to be the hardest part of this, harder than the ingestion or activation pieces technically. If your systems genuinely don't share good correlating keys in some places, that's real modeling work, and I'd rather flag that clearly now than have it be a surprise during implementation.

KENJI: Yeah, no, I appreciate you saying that rather than glossing over it. I think — honestly I don't know off the top of my head how bad that gap actually is across all our systems, Lisa, do you have a better sense than me?

LISA: I have a sense for WMS and TMS, those are reasonably close, there's a shipment reference that exists in both, it's just not always populated consistently. Telematics is the one I'm less sure about, that's more Kenji's historical area than mine.

KENJI: Yeah, and I'd want to actually go look rather than guess at that on a call, I don't want to give you a confident answer that turns out to be wrong.

RACHEL: That's totally fine, we don't need a precise answer today.

MARCUS: Agreed, that's honestly a really natural thing to take away as a follow-up rather than force an answer to right now.

RACHEL: Should we talk a bit about rollout and then pricing, or is there more product stuff either of you wanted to cover?

KENJI: I think we're good on product for now. Lisa, anything?

LISA: No, I'm good, I've got plenty to chew on already.

RACHEL: Great. So, on rollout — similar to what I'd tell any customer at this stage, I don't want to commit to a precise timeline until we've got a better sense of that identifier matching question, since that's really the variable that affects effort the most. But directionally, for an initial scope focused on, say, the telematics and WMS pieces first, given those seem to have the clearer path, we'd typically be talking about something in the range of a handful of weeks to get an initial version live, not months, assuming the matching logic isn't unexpectedly gnarly.

KENJI: Okay, that's — that's faster than I was expecting, honestly, given everything else about this has been a slog.

MARCUS: Yeah, the individual pieces are usually the fast part, it's really the identifier and modeling questions that can stretch things out if they're worse than expected. I don't want to overpromise before we've actually looked at your specific schemas.

KENJI: No, that's fair, I'd rather you under-promise there than over-promise and have it blow up later.

RACHEL: Before we get to pricing, one more scoping question — you mentioned the ERP as one of the systems in the mix earlier, but we haven't really talked about it since. Is that in scope for this initial phase, or more of a later addition?

KENJI: I'd say later addition, honestly. The ERP's inventory view matters, but it's the least time-sensitive of everything we've discussed, discrepancies there tend to surface on a slower cycle anyway, so it doesn't have the same urgency as the telematics and dispatch side.

LISA: Yeah, agreed, I'd rather we nail the fast-moving stuff first and bring ERP in once we've proven this works, rather than trying to boil the ocean on day one.

MARCUS: That makes sense from our side too, honestly, starting narrower and expanding tends to go a lot better than trying to unify everything simultaneously.

RACHEL: Good, that's helpful for scoping the proposal too, I'll keep initial phase focused on telematics, WMS, and TMS, with ERP flagged as a logical next phase rather than day one.

KENJI: That's right.

RACHEL: On pricing — I don't want to throw out a specific number today, I'd rather come back with something real once we've got a clearer sense of scope, especially given the telematics volume you mentioned, since that can be a meaningful input into how this gets priced. But directionally, for a company your size with this data volume, it tends to land in a range that I think you'll find reasonable relative to the cost of what you described earlier — a day of multiple people's time just to diagnose one delay, multiplied by however often that happens.

KENJI: Yeah, that framing makes sense. In terms of budget — I'll be honest, I don't fully own that conversation myself, there's a commercial and operations budget process that this would need to go through that I'm not the primary owner of. I can advocate for it, and I think the operational case is strong, but I don't want to represent that I can just greenlight a number the way maybe someone in my exact seat could at a different company.

RACHEL: That's really helpful to know, thank you for being upfront about that. Is there someone specific who'd own that side of it, or is that still to be determined?

KENJI: It's a bit to be determined, honestly. There's someone in revenue operations who typically gets involved in vendor spend decisions of this size, I just haven't looped them in yet because we weren't far enough along to justify pulling them in. I probably should soon, though, now that this is looking like it has real legs.

LISA: Yeah, that tracks with how most vendor decisions go here, RevOps tends to show up once something's serious, not before.

RACHEL: Can I ask, roughly, what that process tends to look like once RevOps is looped in — is it a quick sign-off, or a longer evaluation with other stakeholders?

KENJI: Honestly, it varies a lot depending on the size of the spend and who else has opinions. For something at this scale, I'd guess it's not a rubber stamp, there'll be real scrutiny, but it's also not going to be a six-month committee process either, from what I've seen with past vendor decisions of similar size.

LISA: Yeah, I've seen it go both quick and slow depending on who's asking questions that month, it's not super predictable from the outside.

RACHEL: That's helpful to know, thank you. We won't assume a specific timeline on that front, we'll just stay flexible as it becomes clearer.

KENJI: Appreciate that, I think that's the most honest answer I can give you today.

RACHEL: That makes sense, and honestly, whenever that makes sense on your end, we'd welcome having them in a future conversation — commercial questions tend to go smoother when the right person's actually in the room rather than relayed secondhand.

KENJI: Yeah, agreed, I'll think about the right timing for that. I don't want to pull them in too early and have them sit through a bunch of technical stuff that's not relevant to them, but I also don't want to wait so long that it becomes a bottleneck right when we're trying to close something out.

MARCUS: That's a reasonable thing to sit with, I don't think you need to solve it today.

RACHEL: Agreed, let's leave that as something to figure out before next time, rather than force it now.

KENJI: Yeah, I think that's right. I'll think about who exactly and when.

RACHEL: Okay. So, in terms of next steps — I'll get a recap over to you both after this, and Marcus, is there anything specific you'd want from Lisa's side before a follow-up, given the identifier matching question?

MARCUS: Yeah, if it's not too much trouble, if you could pull together a rough sense of what correlating fields do exist between WMS, TMS, and the telematics feed — doesn't need to be exhaustive, just enough for us to get a read on how bad the matching problem actually is.

LISA: Yeah, I can do that, I'll need a bit of time though, probably — I don't know, a week or so, depending on what else is going on.

KENJI: That's fine, no rush on our end beyond wanting to keep this moving generally.

RACHEL: Perfect. Should we pencil in a follow-up for, what, a couple weeks out, to give Lisa room on that plus a little buffer?

KENJI: Yeah, couple weeks sounds right.

MARCUS: Works for me.

RACHEL: Great, I'll send an invite. And Kenji, take whatever time you need on the RevOps question, no pressure to have that sorted before then, we can pick it up whenever it makes sense.

KENJI: Appreciated. Okay, I think — anything else before we wrap? We're coming up on time.

LISA: Nothing from me, this was useful, thanks.

MARCUS: Same, this was a good one, thank you both for being so direct about what you don't know yet, that actually makes this easier, not harder.

KENJI: [laughs] Well, good, because there was a lot of "I don't know" today.

RACHEL: Honest "I don't know" beats confident wrong answers every time, in my experience.

KENJI: Ha, fair enough.

RACHEL: One last thing, actually, before we drop — sorry, small thing, but Kenji, is there a better time of day generally for future calls, or was this slot fine? I know we booked this one a little last minute.

KENJI: This was fine, honestly, mornings are worse for us, afternoons tend to work better generally if you've got flexibility on your end.

RACHEL: Good to know, I'll try to keep future ones in the afternoon then. Alright, thanks both, talk in a couple weeks, have a good rest of your week.

MARCUS: Bye, all.

LISA: Bye.
