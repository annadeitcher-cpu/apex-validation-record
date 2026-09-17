---
opportunity: Ardent Manufacturing — Operational Data Platform
call_id: ardent-01
call_type: technical_validation
day_offset: -4
duration_minutes: 69
participants:
  - name: Greg Lindqvist
    role: Account Executive
    org: Apex
  - name: Marcus Webb
    role: Solutions Consultant
    org: Apex
  - name: Viktor Lang
    role: Director, Operations Data
    org: Ardent Manufacturing
  - name: Cheryl Boateng
    role: Plant Systems Analyst
    org: Ardent Manufacturing
---

GREG: Okay, I think that's everyone — Viktor, Cheryl, thanks for hopping on. How's the week treating you both?

VIKTOR: Can't complain, busy but the normal kind of busy.

CHERYL: Same, honestly, nothing exciting to report.

GREG: [laughs] I'll take nothing exciting, that's usually the good kind of week.

VIKTOR: Yeah, honestly the most exciting thing this week was a forklift battery dying in the middle of a shift, which, believe it or not, counts as excitement around here.

CHERYL: [laughs] That was a whole thing, we don't need to relive it.

VIKTOR: It's fine, it's fine, nobody got hurt, it was just annoying.

GREG: [laughs] Well, glad it wasn't anything worse. So, quick intros for the recording — I'm Greg, account exec on this from Apex, and this is Marcus, our solutions consultant, he'll do most of the technical talking today.

MARCUS: Hey, good to meet you both. I saw the notes from the intro call, but I'd rather hear the current-state picture directly from you than work off secondhand notes.

VIKTOR: Sure, happy to. I'm Viktor, I head up operations data here, so plant systems, production reporting, that whole world reports up through me eventually.

CHERYL: And I'm Cheryl, plant systems analyst, I'm more in the weeds day to day, I'm the one who actually touches most of the systems Viktor's about to describe at a high level.

GREG: Perfect, that's a good mix. Viktor, want to just walk us through the shape of the problem as you see it?

VIKTOR: Sure. So, high level — we run several manufacturing facilities, and each one's got its own mix of plant-floor systems, PLCs, SCADA, that kind of thing, feeding into a manufacturing execution system, and then separately there's a maintenance system, and an ERP that has its own view of production and inventory. None of that's unified today. If I want to understand overall equipment effectiveness across the network, or get ahead of a maintenance issue before it causes downtime, that's mostly manual work, pulling reports from each system separately and stitching them together.

MARCUS: Can you give a concrete example of where that manual stitching actually shows up as a real cost?

VIKTOR: Sure — monthly OEE reporting is the clearest one. Cheryl basically spends the better part of a week every month pulling numbers from each facility's systems and reconciling them into one network-level view. It's not glamorous work, and it's very much "here's what happened last month" rather than anything that could help us react faster.

CHERYL: Yeah, it's a lot of exports and spreadsheet work, honestly. Each facility's systems report things slightly differently, so there's always some amount of judgment calls involved in reconciling it, which isn't great from a consistency standpoint either.

MARCUS: And is that OEE reporting the main use case, or are there other things layered on top of that?

VIKTOR: Mainly that, plus we'd like better visibility into maintenance patterns, being able to see, across facilities, which equipment types are failing more often than expected, that kind of cross-facility pattern is basically invisible to us today because everything's siloed per facility.

CHERYL: Right, today if a specific type of pump keeps failing at one facility, nobody necessarily notices that the same thing's happening at two other facilities too, because there's no shared view.

MARCUS: Are there other use cases beyond OEE and maintenance patterns, or are those really the two anchors for this?

VIKTOR: Those are the two big ones. There's a smaller third thing — inventory reconciliation between what the ERP thinks we've got on hand versus what's actually on the floor, but that's more of a nice-to-have, it's not the main driver.

CHERYL: Yeah, the inventory mismatch thing is annoying but it's not — it doesn't cause the kind of pain the OEE reporting does, it's more of a background irritation.

MARCUS: Got it, that's helpful to know what's core versus secondary.

GREG: How big's the team that's dealing with this day to day — is it really just you two, or is there more headcount involved?

VIKTOR: It's mostly Cheryl doing the hands-on work, I've got two other analysts who help with different pieces, but Cheryl's the one who owns the network-level rollup specifically.

CHERYL: Yeah, the facility-level reporting is spread across a few people, but somebody — currently me — has to pull it all together at the network level.

GREG: Got it, that's helpful context.

MARCUS: That makes sense, that's a pretty common pattern actually, cross-facility visibility tends to be one of the first things that becomes possible once data's unified that wasn't possible before.

GREG: How many facilities are we talking about, roughly, just so I've got a sense of scale?

VIKTOR: Six currently, a seventh coming online early next year that we'd want to fold in eventually too.

GREG: Got it, that's helpful.

MARCUS: And is the seventh facility, the new one, going to be on the same systems as the newer existing facilities, or is that still being decided?

VIKTOR: Same systems, yeah, we standardized on that stack a couple years back for new builds, so at least going forward things get simpler, it's really the older facilities that are the long tail of inconsistency.

CHERYL: Right, every new facility going forward should be easier to onboard than the old ones, that part's at least trending the right direction already.

MARCUS: That's good, it means the problem's actually shrinking over time on its own, even before this conversation, which is a nice thing to be able to say.

VIKTOR: Yeah, I hadn't really framed it that way, but that's true, I guess.

MARCUS: And the underlying systems, are they the same across facilities, or does each one have its own setup?

VIKTOR: Bit of both, honestly. The newer facilities are on a more modern, standardized stack, but a couple of the older ones are running systems that have been there for a decade or more, with their own quirks.

CHERYL: Yeah, the oldest facility's SCADA system is genuinely ancient, I don't think it's had a meaningful upgrade in years.

MARCUS: That's useful to know, that kind of heterogeneity is pretty normal for manufacturing environments honestly, it's rare that everything's on one clean stack.

VIKTOR: Yeah, I figured as much, we're definitely not unique in that regard.

MARCUS: What's the ERP you're running, if you don't mind me asking, just so I have a sense of the overall landscape?

VIKTOR: It's a fairly standard mid-market ERP, nothing exotic, been in place for a while now, it's honestly the most stable piece of the whole picture.

CHERYL: Yeah, the ERP's fine, it's really the plant-floor-to-MES-to-ERP chain that's the mess, not any one piece in isolation.

MARCUS: That's a helpful distinction, it's usually the seams between systems that cause the pain, not the systems themselves.

VIKTOR: Right, exactly, nothing's really broken, it's just disconnected.

GREG: And the maintenance system, is that a dedicated CMMS, or is that folded into something else?

VIKTOR: Dedicated CMMS, separate system entirely, it's actually pretty decent on its own, work orders and asset history are tracked reasonably well within it, it's just isolated from everything else.

CHERYL: Yeah, the CMMS data is good quality, it's just sitting in its own silo, same as everything else.

VIKTOR: Can I ask, does connecting the CMMS require the same kind of setup work as the plant-floor systems, or is that a lighter lift since it's already fairly clean?

MARCUS: It's generally a lighter lift when the source data's already well-structured, since a lot of the setup effort goes into handling messiness, and a clean, well-maintained CMMS tends not to have much of that. The connection itself is still real work, but the mapping and cleanup portion is usually shorter.

VIKTOR: Good, that's one less thing to worry about then.

CHERYL: Yeah, if anything's going to be the easy part of this, I'd bet on the CMMS being it.

GREG: Should we get into the product now, or is there more to cover on the current state first?

VIKTOR: I think we've covered the main shape of it, let's get into it.

MARCUS: Great, let me share my screen. Everyone see okay?

CHERYL: Yep.

VIKTOR: Looks good.

MARCUS: Okay, so — given what you're describing, the piece I want to start with is Streamline Ingest, since it's built for exactly this kind of high-volume operational event data, sub-minute ingestion so that plant-floor and machine data lands close to real time rather than in the kind of batch exports you're doing today.

VIKTOR: Okay, and does that require us to standardize the older facility's SCADA system first, or can it work against what's there today?

MARCUS: It can work against what's there, we're not requiring you to modernize infrastructure before this becomes useful. The ingestion layer adapts to whatever the source system can actually provide, so an older SCADA system with more limited connectivity options would still be a viable source, just potentially with different latency characteristics than a newer one.

VIKTOR: Okay, that's good, I was a little worried this was going to turn into a "upgrade everything first" conversation.

MARCUS: No, definitely not, that would be a pretty unreasonable ask given how normal it is for manufacturing environments to have a real mix of system ages.

VIKTOR: Okay, and what about latency for the older system specifically — if it's genuinely legacy, sub-minute might not be realistic, right?

MARCUS: That's fair, sub-minute is what's achievable when the source system itself can push data promptly. For something genuinely legacy with more limited connectivity, we might be looking at more like a few minutes rather than sub-minute, depending on exactly what interfaces it exposes. I'd want to actually look at the specific system before committing to a number.

VIKTOR: That's fine, even a few minutes would be a massive improvement over "once a month," so I'm not going to quibble over minutes versus seconds.

CHERYL: Yeah, agreed, we're not exactly starting from a high bar here.

MARCUS: [laughs] Fair, that does lower the bar for what counts as a win.

VIKTOR: Can I ask, is there a difference in how you'd approach the historian versus a live PLC connection? I know those are technically different things even though people sometimes talk about them interchangeably.

MARCUS: Good distinction to draw out — a historian's already collecting and storing time-series data over time, so that's often a more straightforward source to connect to, since the collection and retention logic already exists there. A live PLC connection is closer to the raw source, which can give you lower latency but usually means more setup work to define what's actually being captured versus relying on whatever the historian's already configured to retain.

VIKTOR: Okay, we've got historians at most facilities, so that's probably the more realistic starting point rather than going straight to the PLCs.

CHERYL: Yeah, agreed, the historians are already doing the hard part of collection, it'd be silly to bypass that and reinvent it.

MARCUS: That's usually the right call, honestly, leaning on an existing historian rather than building a parallel collection path tends to be both faster and lower-risk.

VIKTOR: Are there facilities where we don't have a historian at all, would that just mean we're starting from a live PLC connection there by necessity?

CHERYL: I think all six current facilities have some form of historian, even the old one, it's just an older version of the software. The new seventh facility will too, obviously, since it's on the modern stack.

MARCUS: Good, that simplifies things, it means we're not looking at a from-scratch live-PLC build for any facility, which would be a meaningfully bigger lift.

VIKTOR: Yeah, I'm glad that's not a problem we have to solve, honestly, that would've changed the whole shape of this conversation. Can I ask about tag naming, actually — one thing that's bitten us before is each facility using slightly different naming conventions for what's essentially the same piece of equipment. Does that cause problems here?

MARCUS: It's a real thing to plan for, yeah. The mapping from your facility-specific naming into a common model is part of the setup work, similar to how we'd handle any cross-source modeling — it's not something that resolves itself automatically, someone needs to define that mapping once per facility. But once it's defined, it's a one-time cost per facility rather than an ongoing translation problem.

VIKTOR: Okay, that tracks with what I'd expect, I wasn't hoping for magic there.

CHERYL: Yeah, the naming inconsistency across facilities is very much a known problem for us already, it's not a surprise.

MARCUS: Good, it's usually easier when a customer's already aware of it rather than discovering it partway through setup.

VIKTOR: Can I ask one more thing on the technical side — what happens if a facility loses connectivity temporarily, like a network outage on the plant floor? Does data just get lost for that window, or is there some kind of buffering?

MARCUS: Depends on the source system's own behavior during an outage — if it buffers locally and catches up once connectivity's restored, that gets picked up on reconnect. If the source itself drops data during an outage, that's a limitation of the source, not something ingestion can retroactively recover, we can't pull data that was never captured anywhere.

VIKTOR: Okay, that makes sense, I wasn't expecting you to solve for data that never existed in the first place.

CHERYL: Yeah, most of our systems buffer locally for at least a short outage, it's really only a prolonged one that'd cause actual gaps, and that's already a known risk regardless of what we do here.

MARCUS: Right, that risk exists independent of this project, so it's not something this changes for better or worse, it just inherits whatever your source systems already do.

VIKTOR: Fair enough, that's a reasonable way to think about it.

CHERYL: Can I ask a more practical question — once data's flowing in from all these systems, does it require someone technical to actually build the OEE calculations, or is there something more accessible for that?

MARCUS: The underlying data ingestion is a technical setup, that part does need someone with the right access and understanding of your systems, but once the data's flowing, calculations like OEE can be defined once and then reused, rather than someone rebuilding the reporting logic by hand every month. So the heavy lift is really at setup, not in the ongoing monthly cycle.

CHERYL: Okay, that would be a big change from what I do today, since right now it really is a rebuild-by-hand cycle every single month.

MARCUS: Yeah, that's exactly the kind of recurring manual cost this is meant to remove.

CHERYL: Can I ask, once the OEE calculation's defined, does it run the same way for every facility, or do I need to define it separately per facility given how different some of the source systems are?

MARCUS: The calculation logic itself is defined once, conceptually — "OEE equals availability times performance times quality," or however you define it specifically — but it draws from each facility's mapped data, so as long as the underlying mapping's in place per facility, the same calculation applies consistently across all of them. You're not redefining OEE six different ways, you're mapping six different sources into one consistent calculation.

CHERYL: Okay, that's actually a big deal, because right now every facility's OEE number is calculated slightly differently by whoever happens to be pulling it that month, so even the "same" metric isn't really comparable across facilities today.

VIKTOR: Yeah, that's actually a bigger problem than I usually give it credit for, the inconsistency between facilities undermines a lot of the cross-facility comparisons we'd like to make.

MARCUS: That's a really common hidden cost, honestly, "the same metric calculated differently" causes more confusion than people expect until it's pointed out directly.

VIKTOR: Can I ask, is the OEE formula itself something you'd want us to define exactly, down to how we're counting planned downtime versus unplanned, or is there a standard version most customers just use?

MARCUS: There's a fairly standard industry formula most manufacturing customers start from, but the specifics of what counts as planned versus unplanned downtime, or how you treat changeover time, tend to vary by company, sometimes even by facility. So we'd want to nail down your specific definitions rather than assume a generic one applies cleanly.

VIKTOR: Yeah, we've actually got some internal disagreement about that already, honestly, a couple facilities count changeover time differently than others.

CHERYL: That's true, actually, I've noticed that discrepancy before but never had a reason to force a resolution on it.

MARCUS: That's actually a really common byproduct of a project like this, it forces a conversation that probably should have happened already but never had a forcing function behind it.

VIKTOR: [laughs] Fair, I guess this'll be the forcing function then. Can I ask, once it's set up, how often does the OEE view actually refresh — is that near real-time too, or is that more of a daily rollup given it's a monthly reporting cadence anyway?

MARCUS: It can be as current as the underlying data allows, so technically near real-time, but you could also choose to only look at it on whatever cadence makes sense operationally, the platform doesn't force you to consume it more frequently than you want to. Some customers do like having it available in near real-time even if the formal reporting cadence stays monthly, just because it lets them catch a bad trend early rather than waiting for the month-end number.

VIKTOR: Yeah, that would actually be useful, catching a bad trend mid-month instead of finding out after the fact would be a real improvement.

CHERYL: Agreed, right now by the time I've pulled the monthly number, whatever caused it is ancient history, there's no way to react to it in the moment.

MARCUS: Yeah, that's really the core value unlock once something moves from monthly-batch to available-whenever-you-want-it, it's not really about the numbers being different, it's about being able to act on them sooner.

VIKTOR: Can I ask about historical backfill — if we wanted to look at trends going back a year or two, is that something that's possible, or does this only really capture data going forward from whenever we turn it on?

MARCUS: If historical data exists in your source systems already, that can generally be backfilled, it's not limited to only-forward-looking data. The historian data specifically tends to have a good amount of history already sitting there, so that's often a reasonable source for backfill without needing anything special.

VIKTOR: Okay, that's good, having a year or two of trend data from day one would make this a lot more useful immediately rather than having to wait a year to build up a comparable baseline.

CHERYL: Yeah, agreed, waiting a year to have anything meaningful to compare against would be a pretty rough start.

MARCUS: Right, and that's part of why backfill matters so much for something like OEE trending specifically, a single month of forward-only data isn't nearly as useful as having real historical context to compare it against.

VIKTOR: Does the backfilled data go through the same mapping and cleanup as new data going forward, or is that treated differently since it's historical?

MARCUS: Same mapping logic applies, so once a facility's mapping is defined, it applies consistently to both the historical backfill and anything new coming in going forward, rather than historical data getting some separate, lower-quality treatment.

VIKTOR: Good, I'd be annoyed if the old data was somehow second-class compared to what comes in after setup.

CHERYL: Yeah, agreed, that would be a pretty frustrating asterisk to discover after the fact.

MARCUS: Understood, and that's not how it's designed to work, consistency across historical and current data is really the whole point.

VIKTOR: One more on backfill, actually — is there a practical limit on how far back we could go, or does that really just depend on what the historians happen to have retained?

MARCUS: It really comes down to source retention, if a historian's only kept two years of data because of its own storage limits, that's the practical ceiling, not something we can pull from thin air. Whatever's genuinely available in the source is what's available to backfill.

VIKTOR: That's fair, I think our historians go back at least three or four years at most facilities, so that shouldn't be a real constraint for us.

CHERYL: Yeah, retention hasn't been an issue for us historically, it's really just been about nobody having unified it before now.

MARCUS: Good, that's honestly one less variable to worry about then.

GREG: That sounds like it'd give you a lot of time back, Cheryl.

CHERYL: [laughs] I could think of worse things to do with a week a month, yeah.

MARCUS: Should I keep going, or do you want to sit with that for a second?

VIKTOR: No, keep going, this is good so far.

MARCUS: Okay, so the other piece I want to touch on is Warehouse Native Activation, which is really about what happens once the unified data exists — rather than standing up a separate reporting system that needs its own copy of everything, dashboards and alerts run directly against your data as it sits, so the OEE view, or a maintenance pattern alert, reflects current state rather than a stale copy.

VIKTOR: Okay, and the alerting piece — is that something we'd define, or does the platform come with some default set of manufacturing alerts baked in?

MARCUS: You'd define what actually matters to you, we're not going to assume we know your specific thresholds for what counts as a meaningful deviation at a given facility, that has to come from your team's domain knowledge. What we provide is the mechanism for that rule to run continuously and route wherever it needs to go, not the judgment of what the rule should be.

VIKTOR: That's the right answer, honestly, I'd be skeptical of a vendor claiming to know our thresholds better than we do.

MARCUS: Yeah, that boundary comes up a lot, and for good reason.

VIKTOR: Can I ask, does the alerting distinguish between severity levels, or is everything treated the same once it crosses a threshold?

MARCUS: Severity is something you'd define as part of the rule, so a minor deviation and a genuinely serious one don't have to look identical when they show up, you could route them differently, or just flag them with different urgency, depending on what makes sense for your team.

VIKTOR: Good, that matters, a wall of undifferentiated alerts is basically as useless as no alerts at all.

CHERYL: Yeah, agreed, if everything looks equally urgent, people stop trusting any of it pretty quickly.

MARCUS: Exactly, that's a really common failure mode, and it's part of why severity being configurable rather than flattened matters as much as the alerting existing in the first place.

VIKTOR: Can I ask about access — who'd actually be able to see these dashboards once they exist? Is that something IT has to manage carefully, or is it more self-serve for whoever needs it?

MARCUS: Access is configurable by role, so you could have plant-level staff seeing their facility's view and network-level folks like yourself seeing the rollup, without it being all-or-nothing. It's not something IT has to hand-manage user by user indefinitely, but there is an initial setup of who sees what.

VIKTOR: Okay, that's what I'd expect, I just wanted to make sure it wasn't either "everyone sees everything" or "only three people in the company can look at it."

MARCUS: [laughs] No, it's meant to sit comfortably in between those two extremes.

CHERYL: Is there a mobile view, or something usable from the plant floor? A lot of our plant staff aren't sitting at a desk with two monitors, they're walking the floor.

MARCUS: Yeah, the dashboards are accessible from a browser on a mobile device, it's not a dedicated native app, but it's usable from the floor, it's not desktop-only.

CHERYL: Okay, that matters more than people might expect, honestly, if it's not usable from a phone or tablet on the floor, plant staff just won't engage with it, full stop.

VIKTOR: Yeah, that's been a real lesson for us with other tools in the past, desktop-only stuff just doesn't get used by the people actually on the floor.

MARCUS: That's really common feedback, yeah, and it's part of why that's designed to be accessible that way rather than an afterthought.

VIKTOR: Can I ask about notifications specifically — if an alert fires, does that show up as, like, a push notification, an email, or does someone have to be actively looking at the dashboard to see it?

MARCUS: It's configurable, most customers set it up so alerts push out through whatever channel their team already lives in, email or a messaging tool, rather than requiring someone to be staring at a screen waiting for something to happen.

VIKTOR: Okay, that's good, because realistically nobody's just sitting there watching a dashboard all day, that's not how plant staff work.

CHERYL: Right, if it doesn't come to us, we're not going to go looking for it proactively, same as the pattern-detection thing we talked about earlier.

MARCUS: Yeah, that's a consistent theme across a lot of what we've covered today, honestly — the value's less in the data existing and more in it actually reaching the right person at the right moment without them having to go hunting for it.

CHERYL: Can I ask, practically — once this is running, would I still be the one building new reports as people ask for them, or does it shift who does that?

MARCUS: It can shift some of that, especially for straightforward requests, since a lot of what people ask for ends up being some variation of an existing view once the underlying data's unified. For anything genuinely new, someone would still need to define it, but the amount of from-scratch, manual reconciliation work should drop a lot once the base layer exists.

CHERYL: Okay, that's good to hear, I get a lot of ad hoc requests that currently take way longer than they should because I'm starting from scratch each time.

MARCUS: Yeah, that's a really common pattern, the marginal cost of each new request tends to drop a lot once there's a real foundation underneath it.

VIKTOR: Can I ask something slightly off to the side — how does this actually get set up initially, is that mostly your team doing the work, or is it more collaborative with Cheryl's team?

MARCUS: It's collaborative — our team handles the platform configuration itself, but we need input from whoever knows the source systems best, which sounds like it'd be Cheryl for a lot of this, to validate that mappings are correct and that the numbers coming out match what you'd expect from the existing manual process.

CHERYL: Okay, so I'd be involved in setup, not just receiving something finished at the end.

MARCUS: Right, exactly, we wouldn't want to hand you something at the end that you haven't had a chance to sanity-check along the way.

VIKTOR: That's good, I'd be nervous about a black-box setup where we just get handed numbers at the end with no visibility into how they got there.

CHERYL: Yeah, same, I've been burned by that before with a different tool, numbers just showed up and didn't match what I expected, and there was no way to trace back why.

MARCUS: Yeah, that's a really common frustration, and it's part of why the setup process is meant to involve your team's validation along the way, not just at the very end.

VIKTOR: What does that validation actually look like practically, is that a formal sign-off step, or more informal?

MARCUS: It can be as formal or informal as you want, some customers like a defined checkpoint per facility where someone signs off that the numbers match, others prefer a more continuous back-and-forth as things get built. We'd adapt to whatever fits how your team actually likes to work rather than impose one rigid process.

VIKTOR: I think a checkpoint per facility makes sense for us, gives us a clear point to catch anything before it compounds across the rest of the rollout.

CHERYL: Yeah, agreed, I'd rather catch a mapping issue on facility one than discover it's been wrong across all six by the time anyone notices.

MARCUS: That's a smart way to sequence it, catching issues early and containing them to one facility before they propagate is exactly the kind of thing a per-facility checkpoint is good for. We'd probably start with whichever facility's cleanest, honestly, to prove the pattern out before tackling the messier ones.

VIKTOR: That makes sense, start with the easy win and build confidence before the harder facilities.

GREG: Should we talk a bit about lineage too, or is that not as relevant here?

MARCUS: I think it's worth a quick mention — there's a capability called Lineage Graph that gives you a traceable record of how any given number was derived, which can matter if someone questions an OEE figure months later and you need to actually show your work rather than just assert it's right.

VIKTOR: Yeah, that would be useful, honestly, we've had situations where a number gets questioned and nobody can fully reconstruct how it was calculated at the time.

CHERYL: That's happened to me more than once, someone asks "where did this number come from" and I have to go reconstruct my own spreadsheet logic from months ago.

MARCUS: Yeah, that's exactly the kind of thing this is meant to prevent, having an actual traceable record rather than relying on someone's memory of their own spreadsheet.

VIKTOR: That's a nice-to-have for us, I don't think it's the main driver, but it's a good thing to have alongside everything else.

CHERYL: Can I ask a maintenance-specific question, actually — for the cross-facility pattern detection you mentioned earlier, like the pump example, how would that actually surface to someone? Is that a report I'd have to go look at, or does it proactively flag something?

MARCUS: It can be proactive — similar to the OEE alerting concept, you could define a rule like "flag if the same equipment type has more than N failures across facilities within some window," and that would surface as an alert rather than requiring someone to remember to go looking for the pattern.

CHERYL: Okay, that's good, because realistically nobody's going to proactively go hunting for cross-facility patterns on a regular basis, there's just not time for that kind of open-ended investigation.

VIKTOR: Right, if it's not surfaced to us, it's not going to get found, that's just the reality of how much bandwidth anyone has for that kind of exploratory digging.

MARCUS: Yeah, that's exactly why the alerting model matters as much as the underlying data itself, unified data that nobody looks at doesn't actually solve anything on its own.

VIKTOR: That's a fair point, honestly, having the data available isn't the same as anyone actually noticing something useful in it.

CHERYL: Can I ask about false positives, though — if we set thresholds too aggressively, do we end up getting flooded with alerts nobody acts on?

MARCUS: That's a real risk if thresholds aren't tuned carefully, yeah. Most customers start a bit conservative and tighten over time as they get a feel for what's actually meaningful versus noise, rather than starting aggressive and immediately drowning people in alerts.

CHERYL: Okay, that seems like the right approach, better to start quiet and add more than start loud and have people tune it out.

MARCUS: Agreed, that's generally the safer direction to err in.

GREG: Makes sense. Should we open it up for any other questions, or do you feel like we've covered the main ground?

VIKTOR: I think we've covered it pretty well, honestly. Cheryl, anything you wanted to ask that we haven't gotten to?

CHERYL: I don't think so, this has been pretty thorough already.

MARCUS: Happy to go deeper on anything specific if something comes up later too, this doesn't have to be the only conversation.

VIKTOR: Appreciate that.

GREG: Cheryl, since you're the one who's going to be living in this day to day — anything on your mind that we haven't touched on?

CHERYL: Let me think — I guess the one thing is, how disruptive is the initial setup to my actual day job? Like, am I going to be pulled off my normal work for weeks at a time, or is it more incremental alongside what I'm already doing?

MARCUS: It's meant to be incremental rather than a full-time pull, especially since it's collaborative rather than something dropped entirely on your plate. There'd be periods where your input's needed more heavily, validating mappings for a given facility, for instance, but it's not designed to require you to set aside your regular responsibilities for an extended stretch.

CHERYL: Okay, that's reassuring, because I genuinely don't have slack in my schedule for a multi-week full-time project on top of everything else.

VIKTOR: Yeah, that's a fair concern, Cheryl's already stretched as it is.

MARCUS: Understood, and that's exactly the kind of thing worth being explicit about during actual planning, not just assumed.

VIKTOR: Can I ask, roughly, how long does a setup like this usually take end to end, for something our size?

MARCUS: For six facilities with the kind of variation you've described, I'd expect something in the range of a couple months for the initial rollout, though the newer, more standardized facilities would likely come online faster than the older ones individually. I don't want to commit to a precise number without actually looking at your systems more closely, but that's a reasonable ballpark.

VIKTOR: That's roughly what I was expecting, honestly, nothing about that surprises me.

CHERYL: Yeah, that seems reasonable given everything we've talked about today.

VIKTOR: One more from me, actually — data residency, does everything stay within a specific region, or is that not really a concern for something like this?

MARCUS: For your case, unless there's a specific regulatory requirement driving it, it's usually not a major concern, but if there is a preference or requirement around where data's processed, that's something we can accommodate, it's just good to know upfront if it matters to you specifically.

VIKTOR: No, I don't think we have a hard requirement there, I was mostly just checking since it comes up in other contexts for us.

MARCUS: Understood, good to confirm either way.

CHERYL: One more from me — training. Once this is live, is there formal training for the plant-level staff who'd actually be using the dashboards, or is it more self-explanatory?

MARCUS: There's typically a short training session for whoever's going to be actively using it day to day, it's not meant to require extensive ramp-up, but we wouldn't just hand people a link and assume it's self-explanatory either, especially for staff who might not be used to this kind of tool at all.

CHERYL: Okay, that's good, some of our plant staff aren't especially tech-forward, so a little hand-holding upfront would go a long way.

VIKTOR: Yeah, agreed, I'd rather over-invest in that training than have adoption stall because people didn't feel comfortable with it.

MARCUS: That's a really sensible instinct, adoption problems are a lot more often about comfort and habit than about the tool itself being hard to use.

VIKTOR: Can I ask one more thing, actually — is there any way for plant staff to give feedback if a number looks wrong to them, or is it purely one-directional, data flows out and that's it?

MARCUS: There's typically a way to flag something for review, so it's not purely one-directional, if someone on the floor thinks a number looks off, that can get routed back to whoever owns the data quality side rather than just being silently ignored or silently trusted.

VIKTOR: That's good, our plant staff generally have really good instincts for when something looks wrong, even if they can't always explain exactly why technically, so I wouldn't want to lose that signal.

CHERYL: Yeah, agreed, some of our best catches over the years have come from someone on the floor just saying "that doesn't look right" and being correct.

MARCUS: That kind of frontline intuition is honestly one of the most valuable things a system like this can capture if it's set up to actually listen for it, rather than assume the data's always right and the human's always wrong.

VIKTOR: That's a good way to put it, I like that framing.

GREG: On the business side — I don't want to get too deep into pricing today, but directionally, for a company your size with six facilities, this tends to land in a range that I think is going to feel reasonable given what you've described about the reporting time cost alone.

VIKTOR: Yeah, that sounds about right, I don't think price is going to be the sticking point here, assuming it's in a normal range for something like this.

GREG: Good to hear. I'll put together something more concrete and send it over.

VIKTOR: Sounds good.

CHERYL: This was a genuinely useful session, I feel like I understand this a lot better than from the intro call.

GREG: Glad to hear it. Well, I think that's probably a good place to leave it for today, unless there's anything else.

VIKTOR: No, I think we're good. This was helpful.

MARCUS: Agreed, thanks for walking us through the current state so clearly, that made this a lot easier to have a real conversation about.

GREG: Yeah, we should probably touch base again at some point, keep this moving.

VIKTOR: Yeah, for sure, let's do that.

CHERYL: Sounds good to me.

GREG: Great. Well, thanks again, both of you, this was a good one.

VIKTOR: Thanks, Greg, talk soon.

CHERYL: Bye, everyone.

MARCUS: Bye, thanks both.
