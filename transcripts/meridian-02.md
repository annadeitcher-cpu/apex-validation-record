---
opportunity: Meridian Health — Customer Data Platform
call_id: meridian-02
call_type: follow_up
day_offset: -12
duration_minutes: 52
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
---

DANIEL: Okay, I think it's just the four of us today — Curtis said he'd sit this one out, right?

DEREK: Yeah, he didn't think there was anything new for him this round, said to loop him back in once there's something worth his time.

DANIEL: Makes sense, we'll keep him posted separately. How's everyone doing, it's been, what, a week and a half since we last talked?

DEREK: Yeah, about that. It's been a week, honestly, budget season is still not over, I don't know why I thought it would be by now.

MARCUS: [laughs] Does budget season ever actually end, or does it just sort of fade into the next one?

DEREK: Fair point. Naomi, you got the short end of the stick this round, you actually had real work to do between calls.

NAOMI: [laughs] Yeah, thanks for that, by the way. No, it was fine, honestly, it was less painful than I expected, mostly because a lot of the mapping already existed in fragments, I just had to actually assemble it into one place instead of it living in three people's heads.

MARCUS: How'd the rest of your week go, other than budget stuff?

DEREK: Honestly fine, mostly heads-down. Naomi, anything exciting on your end, or was it all mapping spreadsheets?

NAOMI: [laughs] Mostly mapping spreadsheets, if I'm being honest. Though I did get pulled into an unrelated fire on Tuesday, someone's dashboard broke because a field got renamed upstream, which, ironically, is exactly the kind of thing we talked about last time with the schema drift question.

MARCUS: Oh no. Well, at least it's topical.

NAOMI: Very topical. Anyway, that ate half a day I didn't plan on losing, but I still got the mapping done.

DEREK: Yeah, she's downplaying it, I know it wasn't nothing.

DANIEL: Well, we're looking forward to hearing it. Do you want to just dive in, or is there anything else first?

DEREK: No, let's get into it, this is really the whole point of today. Naomi, take it away.

NAOMI: Okay, so — I went through, table by table, source system by source system, everything we'd talked about needing for the care gap and consent use case, and mapped each one to whether it's currently in Snowflake or still on Teradata. And the good news, genuinely, is it's better than I expected going in.

DEREK: Yeah, tell them the actual breakdown.

NAOMI: So — patient demographics, that's fully in Snowflake, that migrated pretty early because it's used by a bunch of analytics workloads already. Clinical scheduling data, also in Snowflake, migrated maybe eight months ago. Health plan member data, also there, that one moved as part of a separate initiative on the plan side that had its own funding, so it got prioritized ahead of a lot of other stuff.

MARCUS: Okay, that's — that's actually a lot of the core stuff already in place.

NAOMI: Right, and claims data, which I wasn't sure about going in, is also mostly in Snowflake — there's a small subset of older historical claims, I want to say anything older than about three years, that's still Teradata-only, but for the actual use case we're talking about, recent claims history is what matters, and that part's already migrated.

DEREK: Which honestly surprised me too, I thought claims was going to be the bad news.

MARCUS: That's a really strong starting position, honestly, a lot of what I'd normally expect to be the long pole is already done.

DANIEL: Naomi, how'd you actually go about confirming what's migrated versus not — was that you checking each system directly, or was there existing documentation you could lean on?

NAOMI: Bit of both. There's a migration tracker that's supposed to be kept current, but I've learned not to fully trust it, so for anything load-bearing I actually queried both environments directly to confirm row counts and freshness matched what I expected, rather than just taking the tracker's word for it.

MARCUS: That's a smart instinct, honestly, migration trackers drift out of date constantly, especially on long-running projects like this.

NAOMI: Yeah, and I actually caught one discrepancy doing that — the tracker said scheduling data was "fully migrated," but when I checked, there was a subset, I think it was a handful of specialty clinics that onboarded more recently, whose scheduling data was still landing in Teradata because their integration predates the migration cutover for that source.

DEREK: Oh, I didn't know about that one.

NAOMI: Yeah, it's small, volume-wise it's maybe two or three percent of total scheduling records, but I didn't want to gloss over it just because it's small, since "fully migrated" turned out to not quite be true.

MARCUS: I appreciate you catching that, honestly, that's exactly the kind of small gap that causes confusing bugs three months in if nobody flags it up front.

DANIEL: Agreed, that's a good habit, verifying rather than trusting a tracker that might be stale.

DEREK: Yeah, that's Naomi for you, she doesn't take anything at face value, it's occasionally annoying and mostly extremely useful.

NAOMI: [laughs] I'll take that as a compliment too, apparently this is a day for backhanded compliments. Yeah. So — here's the part that's not fully resolved, and I want to be upfront about it rather than bury it. Two things are still on Teradata only. One is the legacy CRM data, which — Derek mentioned last time that system's being sunset anyway, so I don't think anyone's rushing to build fresh integration against it regardless of what we do here.

DEREK: Right, no, I don't think we should invest in a clean Teradata connection to a system that's got a year of life left. If anything that's an argument for skipping it and just handling that gap manually during the transition period, or accepting it as a known limitation for now.

MARCUS: That seems reasonable, honestly, building a robust pipeline against a system that's actively being decommissioned isn't usually a great use of anyone's time.

NAOMI: Agreed. The second one is more annoying, though, and I want to flag it clearly because it's the one that actually matters — the call center platform's data, including the opt-out and consent records that get logged there when someone calls in and asks to be removed from outreach — that's still Teradata-only. It hasn't moved, and it's not actually on anyone's migration roadmap in the near term, because until this conversation, nobody upstream really flagged it as high priority, it was just sort of assumed to be low-value operational data.

DEREK: Which is, obviously, more than a little ironic, given that's exactly the data that matters most for the thing we're trying to fix.

MARCUS: Yeah — I mean, that's — that is a real wrinkle, I won't pretend otherwise. The one source that's still on the legacy system happens to be the one most directly tied to the consent problem.

DANIEL: Is there a reason it wasn't prioritized, or was it really just an oversight?

NAOMI: Kind of both — the migration prioritization was driven by what analytics and reporting teams needed for their existing dashboards, and call center opt-out logs weren't feeding any of that, so they just fell to the bottom of a very long backlog. Nobody was being careless, it just wasn't visible as important until we started looking at it through this specific lens.

DEREK: Right, and to be fair to past-us, this whole initiative didn't exist when that prioritization got made, so it's not like anyone dropped the ball on a known requirement.

MARCUS: Sure, that makes sense, priorities shift once you're looking at a new use case that didn't exist before. Okay — practically, this doesn't block things the way I was worried it might when Naomi said "two things." Since we do support Teradata as a source, we could stand up a connector specifically against that one system, the call center platform, while everything else sources from Snowflake. It's not architecturally elegant, having two source systems instead of one clean warehouse, but it's a well-supported pattern, we do it for other customers who are mid-migration.

DEREK: Okay, and is that meaningfully more setup work, having one Teradata connector alongside the Snowflake ones, or is it basically the same lift?

MARCUS: It's some incremental work, it's not zero, but it's not a different order of magnitude either — it's one additional connection to configure and validate, not a fundamentally different project. I'd want to actually look at that system's schema before committing to a specific estimate, but directionally it's additive, not a blocker.

DEREK: And just to poke at it a bit more — the call center system, since it's on the polling side rather than push, like Marcus mentioned last time for older platforms — does that polling limitation get worse when it's also the source system, not just a destination? Like, is there additional lag stacking up because it's Teradata and polling-based?

MARCUS: It's additive in the sense that you've got the polling interval on top of whatever the normal processing latency is, but it's not compounding in a runaway way — realistically you're looking at something in the minutes-to-tens-of-minutes range for that specific consent signal to propagate, versus the near-real-time we talked about for modern push-based sources. It's slower, but it's a known, bounded slowness, not an open-ended one.

DEREK: Okay, and is minutes-to-tens-of-minutes acceptable, practically, for a consent signal? Like, is there a real-world scenario where that lag actually matters versus being a rounding error?

NAOMI: I think realistically it matters most for exactly the near-miss scenario we described last time — high volume, fast-moving campaign, someone calls in right as a batch is about to go out. Tens of minutes probably would have prevented what almost happened, but it's not instantaneous the way the text-based opt-out is.

MARCUS: That's a fair characterization. It's a meaningful improvement over the current fully-manual process, but I don't want to oversell it as identical to the push-based case, because it isn't, and I'd rather you go in with accurate expectations.

DEREK: No, I appreciate that, I'd rather know it's "much better, not perfect" than have it framed as flawless and then be disappointed later.

DANIEL: Naomi, do you have a rough sense of volume on that call center opt-out data, just so Marcus can sanity check the connector scoping? Is it a high-frequency stream or more of a trickle?

NAOMI: It's not huge, honestly, compared to some of the other sources — I want to say low hundreds of opt-out or preference-change events on a typical day, spiking somewhat during open enrollment, but nothing like the volume on, say, scheduling data, which is constant throughout the day across every clinic.

MARCUS: Okay, that's helpful, that's a manageable volume for a polling-based connector, it's not going to strain anything even at open enrollment peak.

DEREK: Good, that's one less thing to worry about then.

NAOMI: Yeah, if it had been a firehose I'd have been more nervous about the connector holding up, but at that volume I'm not worried.

DANIEL: That's reassuring to hear, honestly, low-volume-but-high-importance is a much easier engineering problem than high-volume-and-high-importance.

MARCUS: Agreed, this is very much in the manageable category.

NAOMI: That's good to hear, honestly, because my worry going into today was that this wrinkle was going to reopen the whole "do we wait for the migration" conversation from last time, and it sounds like it doesn't have to.

DEREK: Yeah, agreed, that's a relief. So — to state it plainly, because I want to make sure I'm not glossing over the actual implication here — the plan would be, build against Snowflake for the bulk of it, stand up one Teradata connector specifically for the call center consent data, and then when that system eventually gets pulled into Snowflake, or gets replaced, whichever happens first, we re-point that one connector and simplify down to a single source. Does that track?

MARCUS: That tracks exactly, yeah.

DANIEL: That's a really clean way to phrase where we landed, honestly, thank you for laying that out.

DEREK: Well, I want to make sure everyone in this call, and everyone I report to afterward, actually understands the shape of it, rather than it turning into a vague "it's mostly fine" that falls apart under scrutiny later.

NAOMI: Yeah, agreed, I'd rather over-explain the wrinkle now than have it surface as a surprise during actual implementation.

MARCUS: Completely agree, and for what it's worth, I think this is actually a pretty good outcome relative to where we were two weeks ago — we went from "we don't know how much of this is even feasible against current infrastructure" to "here's a specific, bounded piece of extra work, and here's exactly why it exists."

DEREK: Yeah, no, I think this is good news, genuinely, even with the wrinkle. I was bracing for something worse.

DANIEL: Does this change anything about which use case makes sense to pilot first? I know last time care gap outreach came up as the likely starting point.

DEREK: I don't think so, actually — if anything this makes me more confident starting with care gap outreach, since that's the use case most dependent on data that's already fully in Snowflake, minus the consent signal piece which we've now got a real plan for. If we'd started with something more dependent on the call center data specifically, this wrinkle would matter a lot more.

NAOMI: Agreed, care gap outreach is still the right starting point, this doesn't change that.

MARCUS: That's good alignment, and it also means the pilot doesn't have to wait on the Teradata connector being fully polished, we could sequence that connector work slightly behind the initial Snowflake setup if needed, since it's additive rather than a hard dependency for getting started.

DEREK: Oh, that's actually a good point, I hadn't thought about sequencing it that way.

MARCUS: Yeah, we don't have to solve everything on day one, we can phase it so you're seeing value sooner rather than waiting for every piece to be perfect.

DEREK: I like that, that's a much more palatable story to bring to leadership than "everything ships at once in three months."

DANIEL: Should we talk timeline implications, or is there more to unpack on the mapping itself first?

DEREK: I think that's the core of it. Naomi, anything else in the mapping worth flagging, or was that the headline?

NAOMI: That was really the headline. There's some smaller stuff, like a couple of reference tables — product catalog equivalents, category lookups, that kind of thing — that are duplicated in both systems right now because of the incomplete migration, and eventually someone needs to decide which one's authoritative, but that's a much smaller problem, and it doesn't block anything here.

DEREK: Yeah, that one we can sort out ourselves separately from this project.

MARCUS: Agreed, that's not something that needs to shape scope here.

DANIEL: Just out of curiosity, since you mentioned duplicated reference tables — does that ever cause a mismatch where, say, a category exists in one system's version but not the other, or are they at least consistent with each other even if duplicated?

NAOMI: Mostly consistent, from what I've seen, they're kept in sync through an existing nightly job, it's just that job is itself kind of a relic of the migration that nobody's bothered to retire yet. So it's more an annoyance than an actual risk right now.

MARCUS: Okay, good, that's the kind of thing that matters if it's actually causing drift, but if it's staying in sync it's really just tech debt cleanup rather than something that affects us.

NAOMI: Right, exactly, it's on my list, just not a today problem.

DEREK: Naomi's list is very long, for the record.

NAOMI: [laughs] It really is.

DANIEL: Okay. So — given this is a lot more resolved than where we were, do you want me to start putting together an actual proposal now, or is there anything else you'd want nailed down first?

DEREK: I think you can start. I don't think we need to wait on anything else structural. There is one thing I wanted to raise today, actually, that's separate from all of this, and it's less technical, more just — an organizational gap I noticed while we were prepping for this call.

DANIEL: Sure, go ahead.

DEREK: So — assuming this all moves forward, someone's actually going to own building and maintaining the segments day to day, the actual audience definitions, once the platform's live. And right now, honestly, that's not clearly anyone's job. It's sort of assumed it'll be "marketing, or maybe outreach ops," but there isn't a defined role or team for it currently, it's been ad hoc because the tooling's been ad hoc.

NAOMI: Yeah, and that's not really a data engineering problem, that's more of an org design question, but it's relevant here because if nobody owns it clearly, we could end up in a situation where the platform's live and capable, and it still doesn't get used well, because there's no clear owner driving adoption.

MARCUS: That's a fair thing to flag, and honestly it's not unique to you, this comes up with a lot of customers — the technical rollout succeeds and then adoption lags because ownership wasn't sorted out ahead of time.

DANIEL: Can I ask, roughly, what does that ownership tend to look like at other health systems you've worked with, or does it really vary a lot?

MARCUS: It varies, but there's a common pattern — a lot of organizations end up creating something like a small "outreach operations" function that sits between clinical, marketing, and IT, and that team owns the actual segment definitions and campaign orchestration day to day, while the underlying data and platform infrastructure stays with data engineering. It's usually one to three people depending on organization size, not a huge team.

DEREK: Interesting. We don't have anything like that today, it's really just whoever in marketing happens to be closest to a given campaign, plus me getting pulled in when it's technical.

NAOMI: Which honestly sounds like most of our current problems trace back to that exact gap, now that I say it out loud.

DEREK: Yeah, that's — that's probably not a coincidence.

MARCUS: It often isn't. I'd say the organizations that get the most value fastest tend to be the ones that at least designate someone as the accountable owner early, even if it's not a full new team on day one, even just "this one person is the point of contact for segment quality and adoption" makes a real difference.

DEREK: That's useful, actually, having a lighter-weight version of that to propose internally feels a lot more achievable than "let's create a new department."

DANIEL: Yeah, we can definitely frame it that way in the proposal, a phased ownership model rather than an all-or-nothing org change.

DEREK: That would help a lot, honestly, that's a much easier conversation to have with my VP than what I was picturing. Right, and I don't have an answer for you today, this genuinely isn't something I can resolve on this call, it's more a conversation I need to have with whoever oversees outreach operations and probably with my VP, about whether this becomes a defined role, or gets absorbed into an existing team's mandate.

DANIEL: That's totally fair, and honestly, useful to know now rather than have it become a surprise gap later in the process. We can build some recommendations into the proposal around what a healthy ownership model tends to look like for other customers, if that would help you make the internal case.

DEREK: Yeah, that would actually be helpful, having something concrete to point to when I raise it internally, rather than just me saying "someone should own this" without backup.

NAOMI: Agreed, that would help.

DEREK: But I want to be clear, that's a genuinely open thing on our side, I'm not going to pretend I have a plan for it today just to make this call feel more resolved than it is.

DANIEL: Understood, we'll leave it exactly as open as it actually is, and just note it as something to revisit.

MARCUS: I'll add a note about it to my internal recap too, so it doesn't get lost between now and the next call.

DEREK: Appreciate that.

DANIEL: Okay, so — given where we've landed, do you want me to put together real numbers now? I think we're at the point where I can scope this properly, including the Teradata connector piece for the call center system.

DEREK: Yeah, let's do that. I think leadership's going to want to see an actual number soon regardless, and I'd rather bring them something concrete than keep saying "still scoping." Honestly, I got asked about this again yesterday, informally, and "still scoping" is starting to sound like I'm stalling even though I'm not.

DANIEL: Understood, we don't want you to be in that position. Who's asking, out of curiosity, is that the CIO directly or is it filtering down through someone else?

DEREK: It's filtering down, mostly, my VP gets asked by the CIO's office and then it lands on me. It's not adversarial, everyone's being reasonable about it, but there's definitely a clock running that I don't fully control.

NAOMI: Yeah, I've felt that pressure too, secondhand, it's part of why I didn't want to drag my feet on the mapping.

DEREK: Which I appreciate, for the record.

NAOMI: [laughs] Duly noted.

DANIEL: Well, that's helpful to understand, it'll shape how quickly I try to turn the proposal around too. Understood. I'll put together a proposal that reflects the Snowflake-primary architecture with the one Teradata connector, and I'll build in some flexibility given that connector might simplify down the road once that system's migrated or replaced.

DEREK: That makes sense.

DANIEL: I'll also fold in the phased ownership recommendation Marcus described, so it's not just a pricing document, it's something you can actually bring to your VP as a fuller picture of what a rollout looks like, not just a number. Should I address that specifically to you, or is there someone else who should be the named recipient given it might get forwarded upward?

DEREK: Address it to me, I'll be the one walking my VP through it in person rather than just forwarding a document, I think it lands better that way than her reading it cold.

DANIEL: Makes sense, I'll keep that in mind for how I frame the language too, since it's meant to support you presenting it, not stand alone.

DEREK: Yeah, that's — honestly that's more useful to me than just a quote would be. The number matters, obviously, but I've learned that if I bring my VP just a price without the "here's how this actually gets adopted" story, I get sent back to go get that story anyway.

MARCUS: [laughs] That's a very relatable executive move.

DEREK: It's a whole genre of executive move, yeah.

DANIEL: Noted, we'll make sure the proposal tells the full story, not just the commercial piece.

DEREK: Appreciated. Should we talk at all about which of the destinations from last time — the call center dialer, the email side, whatever else — actually gets prioritized in a first phase, or is that premature until you've seen the proposal?

MARCUS: I think that's reasonable to nail down once we're looking at real numbers together, since the phasing might actually affect the shape of the pricing a bit, depending on how many destinations are in scope for phase one versus later.

DEREK: Fair, let's hold that for next time then.

DANIEL: In terms of timing, how does — I want to say a couple weeks out feel for getting back together once you've had a chance to actually sit with a real proposal?

DEREK: That works. Naomi, are you going to need to be in that one too, or is that more of a business conversation by that point?

NAOMI: I'd guess mostly business, unless something in the proposal raises a technical question, in which case pull me in. I don't think I need to be there by default.

MARCUS: That's fair, we can keep it lighter on our side too then, unless something comes up that needs a deeper technical answer.

DANIEL: Should we loop Curtis back in for that one, or is he still sitting it out until there's something new for him?

DEREK: I think he'd want to be looped in once there's an actual number and an actual timeline, even if it's not a technical conversation, just so he's not surprised later. I'll make sure he's aware regardless of whether he needs to be live on the call. Knowing Curtis, he'll probably want at least a heads-up on the Teradata connector too, even though it's not a new PII surface, just so it's not news to him later that there are now two source systems instead of one.

MARCUS: That's a good instinct, we can include a short technical note in the recap that covers the connector at a summary level, so he's got something in writing even if he's not live on the call.

DEREK: That would help, yeah, he prefers having something to read over than being told verbally secondhand through me, understandably.

DANIEL: That works for us.

DEREK: And honestly, depending on how the proposal lands, I could see us wanting one more technical session after that, more to nail down implementation specifics once there's real commitment, rather than more open architecture questions. We'll see how it goes.

MARCUS: Sounds good, we'll stay flexible on that.

NAOMI: One more question actually, sorry, before we move on — the Teradata connector for the call center system, once that system eventually gets retired or migrated, is un-hooking that connector a clean thing to do, or does it turn into its own little migration project down the line?

MARCUS: It's meant to be clean — since the connector's scoped narrowly to that one source, retiring it is mostly a matter of re-pointing the equivalent data at its new home in Snowflake and turning the old connector off, rather than unwinding something deeply entangled with the rest of the platform. It's not zero effort, you'd still want to validate the cutover, but it's not a project on the scale of the original migration.

NAOMI: Okay, good, that's what I was hoping to hear, I didn't want us solving today's problem by creating a smaller version of the same problem for future-us.

DEREK: Future-us has enough problems already, we don't need to gift them another one.

MARCUS: [laughs] Understandable instinct.

DANIEL: Great. So, to recap where we're landing — Naomi's mapping resolves most of the sourcing question, Snowflake for the bulk of it, one Teradata connector for the call center consent data as a bridge until that system's migrated or replaced. The segment ownership question is a real open item on your side that we'll factor into the proposal as a recommendation rather than something we're solving for you. And I'll get a real proposal together and we'll reconvene in a couple weeks.

DEREK: That's right, that's a good summary.

NAOMI: Yeah, that all sounds right to me.

DEREK: I really appreciate the mapping work turning out as clean as it did, Naomi, given how much worse this could have gone.

NAOMI: [laughs] Low bar, but I'll take the compliment.

DEREK: Take the win.

DANIEL: Well, this was a genuinely productive one, even shorter than last time. Thank you both.

NAOMI: Yeah, thanks, this was easier than I expected walking in.

DEREK: Agreed. Talk again once there's a real number to look at.

DANIEL: Sounds good. And Derek, good luck surviving the rest of budget season.

DEREK: [laughs] I'm going to need it, honestly, I think there's at least one more round of "can we cut this by ten percent" coming before it's actually over.

NAOMI: There's always one more round.

MARCUS: For what it's worth, once you've got a real number in hand, if it helps to have something to point to for the value side of that ten-percent conversation, we can put together a rough before-and-after on the manual effort side too — hours saved, that kind of thing — not just the platform cost in isolation.

DEREK: That would actually help a lot, honestly, "here's what it costs" lands very differently next to "here's what we're currently spending in people-hours to do this badly."

DANIEL: We'll build that in as well then.

DEREK: Appreciated. Okay, thanks again, both of you, this was a good use of forty-five minutes, or whatever we ended up at.

MARCUS: Happy to hear it. Talk soon.

DANIEL: Take care, everyone.

DEREK: Bye.

NAOMI: Bye, all.
