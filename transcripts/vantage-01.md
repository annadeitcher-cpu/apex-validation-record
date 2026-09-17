---
opportunity: Vantage Media — Cross-Channel Data Platform
call_id: vantage-01
call_type: technical_validation
day_offset: -11
duration_minutes: 76
participants:
  - name: Daniel Okafor
    role: Account Executive
    org: Apex
  - name: Aditi Sharma
    role: Solutions Consultant
    org: Apex
  - name: Sung-min Park
    role: VP, Audience Data
    org: Vantage Media
  - name: Hallie Brooks
    role: Marketing Ops Manager
    org: Vantage Media
---

DANIEL: Okay, I think we're all here — Sung-min, Hallie, thanks for making time, I know seventy-six minutes on a calendar looks aggressive, we'll try to keep it moving.

SUNG-MIN: No, this is fine, I'd rather go deep once than do three shallow calls, that's usually a worse use of everyone's time.

HALLIE: Agreed, and honestly I blocked the whole afternoon just in case, so don't feel like you have to rush on my account.

DANIEL: Ha, good to know, though I'll still try not to test that. So, quick intros — I'm Daniel, account exec on this from Apex, and this is Aditi, our solutions consultant, she'll carry most of the technical side today.

ADITI: Hey, good to meet you both. I did a little homework beforehand but I'd rather hear the actual shape of the problem from you directly than work off what I assume it is.

SUNG-MIN: Sure. I'm Sung-min, I run audience data for Vantage, which — practically — means I own the strategy and the team responsible for how we understand and reach our audience across all our properties.

HALLIE: And I'm Hallie, marketing ops, I sit under Sung-min, I'm the one actually executing a lot of what she and the brand teams want to do, so I'm probably going to have opinions about anything that sounds cleaner in theory than it is in practice.

SUNG-MIN: [laughs] That's a fair self-description.

DANIEL: That's exactly the perspective we want in the room. So — I know we talked briefly at a high level before this, but I'd love to actually hear the problem in your words, rather than me reflecting back a slightly-off version of what I think I heard.

SUNG-MIN: Sure. So, high level — Vantage runs several media properties, different verticals, different audiences, but a lot of shared infrastructure underneath. Historically each property's marketing team has operated pretty independently, their own list, their own tools in some cases, and that made sense when we were smaller, but at our current scale it's actively working against us. We can't see a person who reads one property and also has an account on another, we can't do any kind of intelligent cross-promotion, and honestly we're probably annoying people by treating them as strangers across properties when they're clearly the same person.

DANIEL: Can you give a concrete example of where that shows up as an actual business problem, not just an inefficiency?

SUNG-MIN: Yeah — subscription conversion is the clearest one. We know, anecdotally, that someone who's a free reader on one property and a paying subscriber on another is a much better conversion target for the first property than a cold prospect. But we can't act on that today, because there's no shared view that says "this email address is a subscriber over here." So we're leaving what's probably meaningful conversion upside on the table, and we can't even quantify how much because we don't have the visibility to measure it properly.

HALLIE: And on my side, the day-to-day version of that is just — every campaign I run, I'm working off whatever that one property's list looks like, in isolation, and if the brand team wants to try something cross-property, which happens more and more, it becomes this manual, painful export-and-merge exercise that eats a huge amount of my week.

ADITI: When you say export-and-merge, walk me through that a bit — what does that actually look like mechanically?

HALLIE: So, say marketing wants to promote one property's content to subscribers of another. I'd have to pull a list from each property's system, usually a CSV export, then manually reconcile them — dedupe by email, try to figure out overlap, apply whatever suppression rules apply, and then upload the resulting list somewhere it can actually be used. It's slow, it's error-prone, and honestly by the time it's done the moment's often passed for whatever the campaign was trying to catch. And it's not even just cross-property stuff, honestly, sometimes it's within a single property — like, marketing wants to exclude anyone who's already converted from a promotional push, and that exclusion list has to get manually maintained too, separately from everything else.

ADITI: Is that exclusion logic something that's consistent across properties, or does each one handle it slightly differently?

HALLIE: Slightly differently, honestly, because each property's marketing team built their own version of "how do we exclude converted users" independently, so there's no single source of truth even for that, it's five different homegrown approaches.

SUNG-MIN: Which is its own quiet risk, honestly, because nobody's ever audited whether all five are even correct, they've just existed long enough that everyone assumes they work.

DANIEL: That's a really concrete picture, thank you. Sung-min, is this initiative coming from a specific mandate, or is it more something your team's been pushing for internally?

SUNG-MIN: Bit of both. Leadership's been pushing hard on subscription growth generally, that's a company-level priority this year, and separately my team's been flagging this exact gap for a while. This is really the first time there's been enough budget appetite to actually do something structural about it rather than keep patching around it.

DANIEL: Got it, that's helpful context. Can I ask, is there a specific goal attached to the subscription growth push, like a number leadership's tracking against, or is it more directional?

SUNG-MIN: There's a number, I won't share the exact figure, but it's meaningful enough that a few percentage points of conversion lift across our base would matter at the board level, not just internally. That's part of why this got funded now rather than staying a nice-to-have.

DANIEL: That's helpful to understand, thank you.

SUNG-MIN: And to be clear, this isn't purely a defensive play either, it's not just "stop losing money to fragmentation," there's real upside we think we're leaving on the table, the conversion story I mentioned earlier is the clearest version of that.

DANIEL: That distinction matters, thank you for drawing it out, it helps to know whether we're solving a cost problem or a growth problem, since that tends to shape how the case gets made internally later.

SUNG-MIN: Fair point, honestly it's probably both, but if I had to pick one to lead with, it's growth, the cost savings are real but they're not what got this funded. Leadership responds a lot more to "here's money we're leaving on the table" than "here's a process that's mildly inefficient," even when the inefficiency is genuinely costly too.

DANIEL: That's a useful thing to know for how we frame the proposal too, we'll lead with the growth case rather than bury it under operational efficiency framing. Appreciate you steering us on that rather than letting us guess at the framing.

HALLIE: Sorry, quick tangent, not really related — Daniel, are you the same Daniel who used to work with our old rep at a different vendor, or am I thinking of someone else? Your name rang a bell earlier and I couldn't place it.

DANIEL: [laughs] I don't think so, unless it's a very common coincidence, I've only been doing this for a few years and I don't think I've overlapped with Vantage before today.

HALLIE: Huh, maybe I'm just misremembering, sorry, that's been bugging me since the intro.

SUNG-MIN: [laughs] Hallie collects vague half-memories of people's names, it's a whole thing.

HALLIE: It's a curse, honestly. Anyway, sorry, ignore that, not important.

DANIEL: No worries at all.

ADITI: Can I ask about scale, just to get a sense of what we're dealing with — roughly how many properties, and roughly what's the combined audience size?

SUNG-MIN: We've got five properties actively in scope for this, a couple more that are smaller and probably come later. Combined audience, if you count anyone with any kind of account or subscription across all of them, it's in the low millions, several million unique email addresses once you account for overlap, though we don't actually know the overlap number precisely today, which is sort of the whole problem.

ADITI: Right, that makes sense, that's exactly the kind of thing that becomes visible once there's a unified view.

HALLIE: Honestly I'm half-hoping the overlap number itself is interesting, marketing loves a good "you're already reading two of our properties" stat for a deck.

SUNG-MIN: [laughs] Very on brand for you to think about it that way.

DANIEL: Can I ask about the current tooling landscape — are the five properties on genuinely separate marketing stacks, or is there some shared infrastructure already that we'd be building on top of?

SUNG-MIN: It's mixed. Two of the newer properties share an ESP because they were built around the same time under one team, but the others are all on different email platforms, different push providers in some cases, it's pretty fragmented. Part of what makes this hard is there wasn't ever a deliberate decision to fragment it, it's more that each property grew up somewhat independently before anyone was thinking about this as one audience.

HALLIE: Yeah, it's very much an organic-growth mess rather than a designed one, if that makes sense.

ADITI: Are the two properties on the shared ESP at least benefiting from that today, like is there already some cross-property capability between just those two?

SUNG-MIN: A little, honestly it's more coincidental than designed, the shared ESP means someone technically could build a cross-property list between those two specifically, but nobody's really done it in practice, it's more latent capability than an actual working process.

HALLIE: Yeah, I've thought about it, but building it manually for just two properties out of five felt like solving a fifth of the problem for a fifth of the effort, so it kept getting deprioritized against other stuff.

ADITI: That makes sense, it's usually not worth partially solving something like this, the value is really in the full unification, not a partial version of it.

SUNG-MIN: Right, exactly, which is part of why we didn't already have someone bolt together a manual solution for just those two, it wasn't worth the effort for a fifth of the value.

ADITI: That's a really common shape, honestly, deliberate fragmentation is rare, it's almost always this kind of accumulated independence.

SUNG-MIN: Good, glad it's not just us then.

DANIEL: Should we get into the product now, or is there more current-state to cover?

SUNG-MIN: I think we've got the shape of it, let's get into it, we can always loop back.

ADITI: Great, let me share my screen. Everyone see okay?

HALLIE: Yep.

SUNG-MIN: Looks good.

ADITI: Okay, so — given what you're describing, I want to start with Segment Studio, since it maps pretty directly onto the "who is this person across properties" problem. It's a visual audience builder that runs against your actual data model, so instead of Hallie manually exporting and reconciling lists, someone can build a cross-property audience definition directly — "subscriber on property A, active reader on property B, no engagement in the last N days" — and it resolves against unified identity rather than five separate lists.

SUNG-MIN: Okay, and the identity resolution piece is really the crux of it for us — how does that actually work when someone might use different emails, or be logged in on one property and anonymous on another?

ADITI: That's the right question to ask first, honestly, because a lot of vendors gloss over exactly that. Identity resolution here is based on whatever deterministic identifiers you actually have — so a shared email address is the strongest signal, a logged-in user ID within a property is strong within that property, and it can also incorporate probabilistic matching on things like device or browser signals for the anonymous case, though I want to be upfront that probabilistic matching is inherently lower-confidence, and you'd want to treat those matches differently than a deterministic email match.

SUNG-MIN: Okay, and is that confidence level something that's exposed, or does it just get collapsed into "this is the same person" behind the scenes?

ADITI: It's exposed, you're not forced to treat a probabilistic match with the same certainty as a deterministic one — you could build a segment that only acts on high-confidence identity links, versus one that's more inclusive but accepts more noise, depending on what the use case tolerates.

SUNG-MIN: That's good, because for something like a promotional email, I'd want high confidence, I don't want to email someone who isn't actually who we think they are. But for something lower-stakes, like an on-site content recommendation, I'd probably accept more ambiguity.

ADITI: Exactly, and that's a really good instinct, different use cases should tolerate different confidence thresholds, and the platform's meant to let you make that call explicitly rather than hiding it.

DANIEL: That's a good example of exactly the kind of nuance we try to preserve rather than flatten.

HALLIE: Can I ask something dumber, sorry — when you say "device or browser signals," is that the kind of thing that breaks constantly because of browser privacy changes, cookie deprecation, all that? Because that's been a whole headache for us on the ad tech side separately.

ADITI: It's not a dumb question at all, honestly it's one of the more important ones. Probabilistic signals of that kind have gotten less reliable industry-wide as browsers restrict tracking, that's a real trend, not something specific to us. Which is part of why I'd steer you toward leaning on deterministic signals, like logged-in identity and email, as the backbone, and treating probabilistic matching as a supplementary layer rather than something load-bearing, precisely because that ground keeps shifting under everyone in the industry.

HALLIE: Okay, that's reassuring actually, because I was worried this whole thing was going to quietly degrade over the next year as browsers keep locking things down further.

ADITI: It's a fair worry to have, I'd rather you go in with realistic expectations about where that's headed than get surprised by it later.

SUNG-MIN: Can I go a level deeper on the deterministic case? If someone's used three different email addresses across their history with us — maybe a personal one, a work one from years ago — does identity resolution ever merge across those, or is it strictly one email equals one identity?

ADITI: It can incorporate additional deterministic signals beyond a single email if they exist in your data — so if there's a shared payment method on file, or an explicit account-linking event, those can tie separate email-based identities together. But I want to be careful here — if the only thing you've got is two different emails that happen to belong to the same actual person, with no other connecting signal, the system isn't going to guess that they're the same person out of nowhere, that would be exactly the kind of over-claiming I don't want to promise.

SUNG-MIN: No, that's the right answer, I'd be more worried if you said yes to that without qualification.

HALLIE: Can I ask a practical question about this — once something like that does get identified, a shared payment method linking two emails, say, does that require someone on my team to review and approve the merge, or does it just happen automatically in the background?

ADITI: That's configurable, and honestly I'd lean toward recommending a review step for anything that's going to drive customer-facing decisions, at least initially, until you've built up trust in how the matching behaves against your actual data. Fully automatic merging with no human check is possible, but I wouldn't necessarily start there.

HALLIE: Yeah, I'd want eyes on that early on too, the idea of two people's histories getting silently merged without anyone noticing makes me nervous.

SUNG-MIN: Agreed, that's exactly the kind of thing I'd want a review step on, at least until we've got a track record of it being reliable.

ADITI: That's the right instinct, and it's honestly how most customers approach it initially, then they loosen the review requirement over time as confidence builds.

HALLIE: Who would actually be doing that review, practically, is that a data engineering thing or could someone on my team handle it?

ADITI: It doesn't require deep engineering skill to review a proposed match, it's really more of a judgment call once the relevant context is presented clearly, so that's the kind of thing marketing ops could reasonably own, assuming there's a defined process for it. It's more about having clear criteria for what counts as a confident merge than about needing someone technical in the loop.

HALLIE: Okay, that's good, I was worried this was going to become another thing that has to route through Sung-min's team specifically and create its own bottleneck.

SUNG-MIN: Yeah, I'd rather this not become a new bottleneck either, that would sort of defeat the point of doing this in the first place. We've got enough bottlenecks already, I'm not looking to invent a new one on purpose.

HALLIE: [laughs] Fair, I'll add it to the list of things not to accidentally recreate. Can I ask something more practical — once an audience is built this way, does it update automatically, or is it still something someone has to manually re-run, because that re-running is honestly half of what kills me today?

ADITI: It can run on a schedule, continuously refreshing as underlying data changes, so people move in and out of the audience automatically rather than someone re-triggering an export. That's really the core thing that removes the manual reconciliation loop you described earlier.

HALLIE: Okay, that alone would give me back a meaningful chunk of my week, if it actually works the way you're describing. Can I ask, what happens if the refresh cadence and a campaign send timing don't line up well, like if a campaign's about to go out right as the audience is mid-refresh? Is there a risk of sending against a half-updated audience?

ADITI: That's a fair operational question — the refresh is transactional in the sense that consumers of the audience see a consistent, complete state, not a partially-updated one mid-calculation. So a campaign wouldn't pull an audience that's half old data and half new, it'd either get the prior complete state or the new complete state, not something in between.

HALLIE: Okay, that's reassuring, I was picturing something messier than that.

ADITI: Yeah, that kind of consistency guarantee matters a lot once people are actually relying on it operationally, it's not something we'd want to hand-wave.

SUNG-MIN: Can I ask, what does a failed refresh actually look like from the outside? Like if the underlying warehouse query fails for some reason, does the audience just silently stay on the last good state, or is there something more alarming that happens?

ADITI: It stays on the last known good state by default, rather than failing open into something empty or wrong, and the failure itself gets surfaced so someone can investigate. So the failure mode is "stale but correct," not "wrong and nobody notices," which I think is the right default for something people are making real decisions off of.

SUNG-MIN: Good, "stale but correct" is a much better failure mode than the alternative, I'd rather know something's a day old than have it silently be wrong.

ADITI: Agreed, that's a deliberate design choice, not an accident. I'd rather you stay a little skeptical until we've actually shown it against your data, "if it works the way I'm describing" is a fair qualifier to hold onto for now.

SUNG-MIN: I appreciate that framing, honestly, a little healthy skepticism from the vendor side is refreshing.

DANIEL: [laughs] We try.

SUNG-MIN: Can I push on one more identity scenario, sorry, I know we might be getting into the weeds — what happens with household-level sharing? Media subscriptions get shared within families sometimes, informally, not through an official multi-user plan. Does the platform have any concept of that, or does it just treat every login as one person regardless?

ADITI: That's a genuinely hard problem, and I want to be honest that there's no clean technical solution to informal account sharing — the platform sees whatever signals exist, logins, devices, and so on, and if those signals suggest multiple behavioral patterns under one identity, that can surface as a kind of ambiguity flag rather than the system confidently asserting it knows there are two people. But I don't want to overpromise that it reliably detects informal sharing, because that's a genuinely hard, somewhat fuzzy problem across this whole industry, not something specific to us.

SUNG-MIN: No, I appreciate the honesty, that's actually a problem I've never heard a vendor answer well, so "we don't fully solve it either" is at least an honest non-answer.

HALLIE: Can I ask a follow-up on the household thing, actually, because it's very relevant to us specifically — a lot of our subscription plans are explicitly family plans, multiple people sharing one subscription on purpose, not informally. Is that a totally different case from what Sung-min was describing?

ADITI: That's actually a cleaner case, because a formal family plan usually comes with its own structure in your systems already — multiple named users under one billing account, for instance — which gives the platform real signal to work with, rather than having to infer sharing from behavioral ambiguity. If that structure exists in your source data, identity resolution can respect it explicitly rather than guessing.

HALLIE: Okay, that's good, because we do have that structure, each family member typically has their own login under the shared plan.

ADITI: Then that's a meaningfully easier problem than the fully informal case Sung-min raised, since you're not starting from zero signal.

HALLIE: That's good, because family plans are actually a decent chunk of our subscriber base on a couple properties, so if that had been a hard problem too, that would've been a real gap for us specifically, not just a theoretical edge case.

SUNG-MIN: Yeah, agreed, that one actually matters to our numbers, unlike some of the more exotic edge cases we might dream up on a call like this.

ADITI: Fair, and that's honestly a useful distinction to keep in mind generally — some edge cases are real and load-bearing for a given business, others are more hypothetical, and it's worth being clear about which is which rather than treating every edge case as equally urgent, otherwise you end up spending real engineering effort chasing scenarios that barely move the needle for your actual business.

SUNG-MIN: That's a good way to think about prioritization generally, honestly, not just for this. Good, glad the two cases aren't equally hard, that was going to be one of my bigger worries.

ADITI: [laughs] I'll take "honest non-answer" as a compliment in this context.

SUNG-MIN: One more, and then I promise I'll let identity go for a while — when confidence tiers change over time, like a probabilistic match gets upgraded to deterministic because new data comes in, does that happen automatically, or does someone have to intervene?

ADITI: It can happen automatically as new corroborating signals arrive — so if a probabilistic match later gets reinforced by, say, a shared login event, the confidence tier can update on its own without someone manually re-evaluating it. That said, it doesn't downgrade or upgrade silently in a way that's invisible — the history of how a given identity link's confidence has changed is something you could trace back through, similar to the lineage concept we'll get to in a bit.

SUNG-MIN: Okay, good, I like that it's not a black box that just quietly reclassifies things.

ADITI: Yeah, that would undermine trust in the whole system pretty quickly if people couldn't see why something changed.

DANIEL: Should we keep going, or do you want to sit with identity a bit more? I know we've spent a good chunk of time here already.

SUNG-MIN: No, this was worth it, but let's keep moving, I don't want to eat the whole call on one topic.

ADITI: Agreed. So, once an audience is defined this way, the next piece is activation — getting that audience out to wherever it actually needs to go, email platform, push, paid social, without someone manually exporting and uploading each time.

HALLIE: Which destinations does that actually cover? We're on a fairly standard ESP, plus a push provider for the apps, plus the usual paid social platforms.

ADITI: All of those are supported destination types generally, the specifics depend on exactly which platforms you're on, but email, push, and the major paid social platforms are all well-trodden ground for us.

SUNG-MIN: Okay, and does that mean the same identity resolution and confidence-tiering carries through to activation, or is that a separate consideration once it's going out the door?

ADITI: It carries through — the confidence tier you build into the audience definition is reflected in what actually gets pushed to each destination, so a high-confidence email audience and a broader probabilistic on-site audience aren't collapsed into the same undifferentiated list once they leave the platform.

SUNG-MIN: Good, that consistency matters a lot to me, I'd be nervous about a system where the nuance existed in the builder but got flattened the moment it activated somewhere.

HALLIE: Can I ask a more basic question — for the paid social destinations specifically, is that pushing a full audience list each time, or is there some kind of incremental update, because our current process is very much "re-upload the whole list and hope it processes before the campaign needs it"?

ADITI: It's incremental where the destination platform supports it — so rather than re-uploading a full list each time, changes get pushed as additions and removals against the existing audience on the platform side. Not every ad platform's API supports that equally well, so there can be some variation by destination, but the intent is to avoid exactly the "re-upload everything and hope" pattern you're describing.

HALLIE: Okay, that alone sounds like it'd save me a genuine chunk of time, the re-upload-and-wait cycle is its own special kind of miserable.

ADITI: Yeah, that's a really common complaint, honestly, the batch re-upload pattern is one of the more painful legacy workflows in this space.

DANIEL: That's exactly the kind of thing that tends to bite people later if it's not designed carefully from the start.

SUNG-MIN: Can I ask about paid social specifically — a lot of what we do there right now is lookalike modeling off our existing subscriber base. Does that still work the same way once audiences are being built through this, or does that require its own separate setup?

ADITI: Lookalike modeling itself happens on the ad platform's side, using whatever seed audience you feed it — so the platform here would be responsible for getting you a cleaner, more current seed audience than what you're working with today, but the actual lookalike expansion is still the ad platform's own modeling, that's not something we're replacing.

SUNG-MIN: Okay, that makes sense, I wasn't sure if that was going to be a whole separate conversation or not.

ADITI: No, it plugs into what you're already doing there, it just improves the input rather than replacing the mechanism. Should I walk through what this actually looks like end to end with a concrete example, or does the conceptual version land okay so far?

SUNG-MIN: Let's do the concrete example, I think that'll surface anything we're still missing.

ADITI: Okay — so, take the subscriber-cross-promotion case you described earlier. You'd define an audience as, say, "paying subscriber on Property A, has an account but no subscription on Property B, high-confidence identity link between the two." That resolves against the unified identity graph, and then you could push that audience into an email campaign on Property B specifically promoting a cross-property offer, with the suppression logic automatically excluding anyone who's already opted out of marketing on either property.

SUNG-MIN: Okay, that's — that's basically exactly the scenario I described earlier, almost uncomfortably on the nose.

ADITI: [laughs] I promise I'm not just reading your earlier answer back to you, it's a genuinely common pattern for multi-property media companies specifically.

HALLIE: The suppression piece you mentioned at the end there — how does that actually work across properties? Because today, suppression is basically per-property, per-channel, it's not unified at all, and that's honestly one of the messiest parts of what I deal with.

ADITI: Suppression state can be modeled centrally, so an opt-out captured on one property or channel is visible to the whole system rather than living in isolation. I don't want to go too deep into that specific mechanism right now though, since I know we've got more ground to cover and I want to be mindful of time — happy to come back to it if it doesn't get addressed elsewhere.

DANIEL: Yeah, actually — I want to flag, we're a bit behind where I expected us to be at this point, which is a good problem, the conversation's been genuinely useful, but I want to make sure we get through the rest of the agenda too. Should we pick up the pace a little on the remaining pieces?

SUNG-MIN: Yeah, that's fair, we did go deep on identity. Let's move faster through the rest, I trust we've covered the hardest part already.

ADITI: Okay, I'll be a bit more efficient with the remaining pieces then. Quickly — there's also Warehouse Native Activation, which just means all of this runs against your actual data warehouse rather than requiring a separate copy of your audience data sitting in some other system. Given you're managing several properties' worth of data already, that matters for not multiplying your data footprint further.

SUNG-MIN: Yeah, we'd want to avoid standing up yet another copy of everything, that tracks.

ADITI: And there's Lineage Graph, which gives you a traceable record of how any audience or activation was built and what happened to it — useful for exactly the kind of "wait, why did this person get this email" debugging that tends to come up eventually. I don't want to do the full walkthrough given time, but happy to go deeper on that separately if it becomes relevant.

SUNG-MIN: That's fine, I think I get the shape of it from what you've described elsewhere already.

DANIEL: We can also send over more detail on both of those after the call, so you've got something to reference without us rushing through it live.

SUNG-MIN: That would help, yeah.

HALLIE: Can I actually bring up something that's been on my mind this whole call, it's related but I don't think it's come up yet directly?

ADITI: Please, go ahead.

HALLIE: So — separate from the audience-building side, there's this whole other thing I deal with constantly, which is consent and suppression list reconciliation. And I don't think I've actually described this properly yet. So — every channel basically has its own opt-out mechanism. Email has its own unsubscribe list, push has its own opt-out at the app level, and paid social, depending on the platform, has its own suppression list concept, like an exclusion audience you have to build and upload. None of those talk to each other. So if someone unsubscribes from email, that doesn't automatically suppress them from paid social remarketing, or from push notifications, unless someone manually goes and updates every single list separately.

ADITI: Right, that's a really common pain point.

HALLIE: It's — honestly it's worse than common pain, it's genuinely one of the worst parts of my job. I'm not exaggerating, I spend, conservatively, four or five hours a week just manually cross-referencing these lists against each other, pulling exports, matching them up, re-uploading suppression lists to each platform separately, and it never actually feels done, because by the time I've finished one cycle, there's already been new opt-outs that need to go through the same process again.

SUNG-MIN: Yeah, and it's not just Hallie's time, it's genuinely a risk surface too. If someone opts out on one channel and we keep hitting them on another, that's a bad customer experience at minimum, and depending on the channel, it can edge into actual compliance territory. And the frustrating thing is, none of the individual platforms are doing anything wrong, they're all working exactly as designed, it's just that "designed" means "designed in isolation," nobody built any of them expecting to talk to the others.

HALLIE: Right, and there was one time — this was maybe six months ago — where I was doing the paid social suppression upload, and I grabbed what I thought was the current unsubscribe export, but it was actually a version from like ten days earlier, because the export process isn't automated, someone has to remember to pull a fresh one each time. So for those ten days, an actual meaningful chunk of people who'd unsubscribed from email were still getting hit with paid social remarketing ads for the exact same campaign they'd opted out of. It wasn't a massive number of people, but it was enough that a few of them complained, and one of them was, unfortunately, a fairly vocal person online, and that turned into a small but real embarrassment that made its way up to leadership.

SUNG-MIN: Yeah, that one got a lot more attention internally than the actual scale of it probably warranted, just because of who was affected. It's a good example of how a small, boring process failure can turn into a very visible problem depending on who's on the receiving end.

HALLIE: Right, and the worst part is explaining it afterward, because the honest explanation is just "our suppression process is manual and someone used a slightly stale file," and that's a genuinely unsatisfying thing to have to say to leadership after the fact. And the actually infuriating part is that it wasn't even a hard mistake to make, it's basically inevitable given how manual the process is, it was just a matter of time before some version of that happened. And I fully expect some version of it to happen again eventually, honestly, unless something about the underlying process actually changes.

DANIEL: Yeah, that comes up a lot, honestly, that's a really common thing we hear. It's rough when it's a manual process like that, those tend to be the ones that quietly eat the most time.

ADITI: Definitely, the fragmented-suppression-list problem is something a lot of marketing ops teams deal with. Okay — should we move on to rollout and pricing, given where we are on time, or is there more you wanted to cover on the product side first?

SUNG-MIN: No, I think we've covered a lot, let's get into rollout and pricing, I want to make sure we leave enough time for that too.

DANIEL: Sounds good. So, on rollout — given the scope, five properties, unified identity, multiple destinations — I don't want to commit to a precise timeline today, but directionally, given the identity work is the hard part and we've clearly spent real time on it today, I'd expect an initial phase, maybe starting with two or three of the larger properties, to be in the range of a couple months rather than weeks, with the remaining properties following once that's proven out.

SUNG-MIN: That's roughly in line with what I was expecting, honestly, maybe even a bit faster.

HALLIE: Can I ask, practically, what does my team's actual involvement look like during that rollout window? Because I'm already stretched thin, and I don't want to assume this is purely a data-engineering lift on our side.

DANIEL: Fair question — there's real involvement needed from marketing ops, mostly around defining the suppression and exclusion categories we touched on earlier, and validating that audiences built during setup actually match what your team expects before anything goes live broadly. It's not a full-time commitment for the whole window, but it's not zero either, I don't want to undersell that.

HALLIE: Okay, that's honestly what I assumed, I just wanted to hear it said plainly rather than find out later.

DANIEL: Yeah, we'd rather set that expectation now than have it be a surprise partway through. On pricing — similar to how I'd usually handle this, I don't want to throw out a specific number on the call itself, I'd rather put together something real based on what we've actually discussed and come back with it. But directionally, for an organization your size with this scope, it tends to land in a range that I think will feel proportionate given what you described earlier about the conversion upside you're currently leaving on the table.

SUNG-MIN: That's fine, I'd rather see a real number than a range anyway. I've sat through enough vague-range conversations to know they rarely save anyone time in the end.

DANIEL: Agreed, I'd rather do the real work up front than have a number move later and damage trust.

SUNG-MIN: In terms of budget — I'll be straightforward, I own this budget line directly, this is within my authority to approve without it needing to go up another level, assuming the number's reasonable relative to what we discussed. I'll still loop in our CFO's office as a courtesy given the size, but I don't expect that to be a real obstacle if the case is as strong as today's conversation suggests.

DANIEL: That's really helpful to know, thank you for being direct about that.

SUNG-MIN: Yeah, I'd rather you know exactly where the actual decision sits rather than have you guess at it.

DANIEL: Can I ask, is there a specific point in your fiscal calendar this needs to land by, or is the timing mostly driven by wanting to move quickly on the opportunity itself?

SUNG-MIN: More the latter, honestly. There's no hard cutoff I'm working against, but given the conversion upside we talked about earlier, every quarter we don't have this is a quarter of leaving that on the table, so I'd rather move at a reasonable pace than let this drift for the sake of drifting.

DANIEL: Understood, that's helpful, we won't manufacture artificial urgency, but we also won't sit on this longer than necessary on our side either.

SUNG-MIN: Appreciated.

HALLIE: Can I ask something slightly unrelated — do you two work exclusively with media companies, or is Vantage kind of an outlier in your book of business?

ADITI: It's a mix, honestly, we work across a handful of industries, media's a meaningful chunk but not the majority. I'd say the underlying problems rhyme a lot more than people expect though, fragmented identity and fragmented suppression state show up almost everywhere that has more than one customer-facing channel.

HALLIE: Interesting, I guess I assumed this was more of a media-specific headache.

DANIEL: It shows up in slightly different flavors everywhere, honestly, healthcare, retail, logistics, we've had some version of this conversation with all of them.

SUNG-MIN: That's reassuring in a weird way, means we're not uniquely disorganized, it's just an industry-agnostic problem.

ADITI: [laughs] Nobody's uniquely disorganized, in my experience, it's just a matter of how visible the mess has become.

HALLIE: Can I ask, sorry, going back for a second — the identity question about work versus personal emails, and the household sharing thing, are those things we'd need to have fully figured out before this could start, or is that more of an ongoing refinement?

ADITI: That's a great question to close on, honestly, and I don't think we have time to do it justice properly right now given where we are — that's a genuinely open question, both on the technical approach for the household case and on how much precision you'd want before launch versus accepting some ambiguity initially. I don't want to give you a rushed answer to something that important, I'd rather we pick that up specifically in a follow-up.

SUNG-MIN: That's fair, I'd rather that be handled carefully than squeezed into the last five minutes of this call.

DANIEL: Agreed, let's make sure that's the first thing we tackle next time rather than an afterthought.

HALLIE: Works for me, I mostly wanted to flag it so it doesn't get lost. It's the kind of thing that's easy to lose track of once a call ends and everyone moves on to the next thing.

SUNG-MIN: Agreed, let's make sure it's written down somewhere, not just remembered.

DANIEL: Noted, it won't. Okay — in terms of next steps, I'll get a recap over along with the additional detail on lineage and warehouse activation we didn't get to properly today, and I'll start putting together real numbers based on today's conversation.

SUNG-MIN: Sounds good.

DANIEL: Should we get a follow-up on the calendar now, specifically to close out the identity edge cases and go over pricing once it's ready?

SUNG-MIN: Yeah, let's do that. I'm fairly open the next couple weeks, so whatever works on your end.

ADITI: I can make most times work, I'll coordinate with Daniel on a slot and we'll send an invite.

DANIEL: Perfect, I'll get that sent today along with the recap.

SUNG-MIN: Great. This was a genuinely useful session, more substantive than a lot of these calls tend to be.

HALLIE: Agreed, and hopefully the suppression list thing becomes someone else's problem eventually, a girl can dream.

ADITI: [laughs] Noted.

DANIEL: Well, thank you both, this was a great conversation, we'll get that recap and the follow-up invite over shortly.

SUNG-MIN: Thanks, talk soon.

HALLIE: Bye, everyone.

ADITI: Bye, thanks both.
