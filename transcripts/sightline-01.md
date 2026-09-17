---
opportunity: Sightline Retail — Audience Activation
call_id: sightline-01
call_type: technical_validation
day_offset: -4
duration_minutes: 58
participants:
  - name: Sofia Marchetti
    role: Account Executive
    org: Apex
  - name: Aditi Sharma
    role: Solutions Consultant
    org: Apex
  - name: Amara Diallo
    role: Director, Growth Analytics
    org: Sightline Retail
  - name: Paul Renner
    role: Data Engineer
    org: Sightline Retail
---

SOFIA: Okay, I think — are we all good? Amara, I see you, Paul, you're there too, great. I think we're just waiting on — no, actually, I think that's everybody. Should we just get going?

AMARA: Yeah, let's do it. Paul might have his camera off for a sec, he said something about his kid needing the good chair, but he's on audio.

PAUL: Yeah, I'm here, sorry, one sec — okay. Hi, everyone.

SOFIA: No worries. So, thanks for making time, I know it's — what is it, like four something for you guys?

AMARA: Four fifteen, yeah, we're fine, this was actually a good slot, everything before this was just internal stuff I was dreading anyway.

SOFIA: Ha, love that, glad we could rescue you. So, quick intros for the recording — I'm Sofia, I'm the account exec on the Apex side, and this is Aditi, who's our solutions consultant, she's going to do most of the actual talking today because she's the one who can speak to the technical stuff without me getting it wrong.

ADITI: Hi, yeah — hey, Amara, hey Paul, good to properly meet you both. We did a shorter intro call a couple weeks back with, I think it was your VP of Marketing and someone from IT?

AMARA: Right, that was more of a — yeah, that was Deepa and, um, one of our IT guys, Marcus, I don't think he's involved day to day, he was just there to make sure nothing insane was happening.

ADITI: Makes sense, that tracks. So today's really meant to be more hands-on, get into the actual mechanics of how this would work for you all, and I know Sofia sent over an agenda but I want to just sanity check it's still the right one — the plan was, you two walk us through kind of the current state, where the pain is, and then we get into the product and see where it actually maps to what you're dealing with. Sound right?

PAUL: Yeah, that's — I mean, that's what I was expecting, yeah.

AMARA: Yeah, no, that's good. I'd actually love to start there because I feel like every time I try to explain this internally I end up like three tangents deep and nobody remembers the original point, so.

SOFIA: Ha, go for it, we've got the full hour.

AMARA: Okay so — high level, we're a retail company, obviously, we've got the e-commerce side and then like two hundred and something physical stores, and marketing — my team specifically — we own audience strategy across email, push, paid social, all of it. And the actual data lives in Snowflake, Paul's team owns that, and my team's job is basically to say "okay, we want to target people who bought X but not Y in the last 30 days" or whatever the segment is, and then get that audience out to whatever channel needs it.

PAUL: And the "get that audience out" part is where it currently, um — that's the bottleneck, basically.

AMARA: Right, right, that's — go ahead, actually, you should probably describe that part, because it's more your world than mine.

PAUL: Sure, yeah. So right now the flow is, someone on Amara's team — could be Amara, could be one of her analysts — they'll come to me, usually over Slack, sometimes it's a ticket, depends how organized they're feeling that week —

AMARA: Rude.

PAUL: — no offense — and they'll describe the segment in kind of plain English, like "customers who bought from the outdoor category in the last quarter and haven't opened an email in three weeks" or whatever, and then I have to translate that into a SQL query against our warehouse, run it, export it, usually as a CSV, and then depending on where it's going, either upload it directly into like the ESP or hand it to whoever manages the paid social side to upload into their platform.

ADITI: Got it. And how long does that whole loop take, roughly, start to finish?

PAUL: I mean it depends. If I'm not slammed, a simple one, maybe same day, few hours. But if it's a more complex segment, or if I'm mid-sprint on something else, which, let's be honest, is most of the time — it can be, I don't know, two, three days? Sometimes longer if there's back and forth on the definition.

AMARA: And that back and forth is its own thing, because a lot of times what happens is I'll ask for a segment, Paul builds it, sends it over, and then I look at the count and I'm like, that doesn't seem right, that's way too big or way too small, and then we have to go figure out where the logic diverged from what I actually meant. And every one of those cycles is another day, basically.

SOFIA: Yeah, that iteration cost is — I mean that's exactly the thing we hear a lot, that the definition of the segment lives kind of half in someone's head and half in a query, and there's no shared place to actually see it.

ADITI: Can I ask, roughly how many of these requests come in, in a given week? Just trying to get a sense of volume.

AMARA: Um — it varies a lot, honestly. A slow week might be three or four. Around a launch or a promo push it can be, I don't know, ten, twelve? And it's not just me asking, it's really anyone on my team, I've got — what, four analysts plus myself, and then there's the paid social specialist who sits under me but kind of works semi-independently, and she has her own list of asks too that go through Paul.

PAUL: Yeah, and it's not always the same shape of request either, that's part of what makes it hard to just, like, template. Some of it's a one-off "give me this list for this one campaign," some of it's "can you refresh the VIP list," which is supposed to happen monthly but realistically happens whenever someone remembers.

SOFIA: And what's the actual destination tooling right now — like what ESP are you on, and is paid social going straight into the ad platforms, or is there something in between?

AMARA: We're on Klaviyo for email, that's not going anywhere, we like it fine, it's really more the getting-data-into-Klaviyo part that's the problem, not Klaviyo itself. And paid social is direct uploads into Meta and Google, mostly Meta, Google's a smaller piece of our spend.

PAUL: Yeah so today, for Klaviyo, I'm exporting a CSV and someone uploads it as a static list, which then has to get manually refreshed. For Meta it's similar, it's a custom audience upload, also static, also manual.

ADITI: Okay, that's useful, both of those are already supported destinations on our side, so that's not going to be new integration work, that part should be pretty plug and play.

SOFIA: And sorry, one more scoping question while we're here — is there a CRM or loyalty system in the mix too, or is it really just the warehouse as the single source?

AMARA: Just the warehouse, everything funnels into Snowflake first — loyalty program data, POS data from the stores, e-commerce events, all of it lands there before anything happens with it. Which I think is actually good for you guys, right? Like that's kind of the ideal setup for what you're describing.

ADITI: Yeah, exactly, that's the best case scenario architecturally, honestly, a lot of the friction we see with other companies is when the data's fragmented across five systems and nothing's actually consolidated yet. You've already done that part.

PAUL: Yeah, that consolidation was its own multi-year slog, so I'll take the small win of it being useful for something else now.

AMARA: Yes. Exactly that. And look, Paul's great, this isn't a — I'm not complaining about Paul specifically —

PAUL: I mean, a little bit you are, but it's fine.

AMARA: — a little bit, sure — but it's not sustainable, is the thing, especially because we're trying to do more personalized, more frequent campaigns, and every one of those needs a slightly different cut of the audience, and Paul does not have infinite time, he has like, real infrastructure work he's supposed to be doing.

PAUL: Yeah, the segment requests are maybe, I don't know, twenty, twenty five percent of what I do in a given week? Which doesn't sound like much when I say it out loud but it's — it's a lot of context switching, is really the issue. It's not that any one query is hard.

ADITI: That context-switching cost is real, yeah. Okay, that's really helpful, actually, because it maps pretty directly onto — so let me pull up, I want to actually show you the audience builder piece, because I think that's the most direct answer to what you're describing.

SOFIA: Actually, before you dive in — Amara, sorry, I just want to ask, when you say "personalized, more frequent" — is that like a mandate from higher up, or is that more your team's own initiative?

AMARA: Bit of both, honestly. Our CMO has been pretty vocal about wanting to move away from batch-and-blast, which, fine, everyone says that. But also we did see, our best performing campaigns last year were the more targeted ones by like a wide margin, so there's actual data behind wanting to do more of it, it's not just a vibe.

SOFIA: Got it, that's helpful context, thank you. Okay, go ahead, Aditi.

ADITI: Yeah so — can everyone see my screen okay?

PAUL: Yep.

AMARA: Yep, looks good.

ADITI: Great. So this is what we call Segment Studio — this is actually pretty recent for us, this shipped, I want to say, beginning of this year. And the idea is exactly what you were describing, Amara — instead of that request going to Paul and getting translated into SQL by a human, someone on your team builds the segment directly, using this kind of — it's a visual builder, so you're picking attributes and behaviors off the actual underlying data model, and it compiles down to a query against your warehouse. But nobody on the marketing side is writing or seeing SQL, they're just clicking through conditions.

AMARA: Okay, so — like, can I try an example, like the one Paul described?

ADITI: Yeah, please, that's exactly what I want.

AMARA: Okay so, purchased from outdoor category in the last, let's say, ninety days, and — no email open in the last three weeks.

ADITI: Okay so let's build that. So first condition — I'll go to purchase behavior, category equals — and you can see it's actually pulling the live category values from your product catalog, so it already knows "Outdoor" is a category, this isn't me typing in a string and hoping it matches.

PAUL: Oh, that's — okay, that's actually the thing I was wondering about, because half our bugs historically have been someone fat-fingering a category name that's slightly off from what's actually in the table.

ADITI: Right, exactly, so this is reading directly off the values that exist in the underlying table, live, so you can't select something that isn't real. Okay, so category equals Outdoor, and then purchase date — within the last, and I'll put ninety days. And then I'll add a second condition, and this one's going to be an engagement one — email, last open, and I'll say — is more than 21 days ago, or, no opens at all, actually let's do it properly, no opens in the last 21 days.

AMARA: Right, right, that's the — yeah, that's the segment.

ADITI: And then down here, it's showing you the count live as you build it, so as soon as I add that second condition, you can see the number updates — that's a live query against the actual data, this isn't a cached estimate from yesterday.

AMARA: Oh nice, okay, that's — how live is live, like is that hitting the warehouse right now?

ADITI: It is, yeah, it's running against — well, actually, this is a good segue into the other piece, because the way it's live without being slow is that it's running directly against your warehouse, so there's no separate copy of your data sitting in some other system getting stale. Which, Paul, I imagine you have opinions about data copies floating around.

PAUL: Yeah, no, I mean — that's actually a huge thing for us, we've had — we tried a tool a couple years back, I wasn't here yet but I've heard the stories, where it was constantly out of sync with the warehouse and marketing was targeting people based on data that was like a week stale, and it caused a whole thing with a customer getting an email about a product they'd already returned.

AMARA: Oh my god, yes, the return thing, that was — that was a whole ordeal, we still get asked about it sometimes actually, like "are we sure this won't happen again."

SOFIA: Yeah, that's — I mean that's a really common scar tissue thing, honestly, we hear some version of that a lot.

ADITI: Yeah, and I think that's actually the core architectural thing that's different here, and it's worth spending a minute on because it's not just marketing speak — we don't ingest and copy your data into an Apex-owned database. Everything runs directly against your warehouse. So when Segment Studio shows you a count, or when the audience gets pushed out, it's reading current state, whatever's true in Snowflake right this second modulo maybe a few minutes of pipeline lag, not a snapshot from whenever we last synced.

PAUL: Okay, and how does that actually work mechanically, like are you running a job on a schedule against our warehouse, or —

ADITI: So we have a — there's a piece called Warehouse Native Activation, that's actually the newer of the two things I want to show you today, and that's exactly the layer that handles it. So the segment definition lives in Apex, but the execution — the actual query, the actual "who's in this audience right now" — that gets pushed down and run as a query in your warehouse, using a service account with scoped permissions, and then only the result — so like the actual list of customer IDs or email addresses or whatever the destination needs — that gets pulled out and sent to wherever it's going. The underlying behavioral and transactional data never leaves your environment.

PAUL: Okay, that's — that answers basically my first question, which was going to be, like, are you guys ingesting our whole customer table into some Apex cloud thing, because that's a whole security review I did not want to have to run.

ADITI: No, exactly, and actually, I don't know if it matters for you specifically, but for customers in healthcare or finance that's often the whole ballgame, because it means there isn't a second copy of sensitive data sitting somewhere that needs its own security posture.

AMARA: We're not quite that regulated but I appreciate not having a second copy of, you know, everyone's purchase history sitting in some other vendor's cloud regardless.

SOFIA: Right, less surface area generally, yeah.

PAUL: Can I ask, like, a slightly more in-the-weeds question?

ADITI: Please, that's what I'm here for.

PAUL: So the service account you mentioned — what does that actually need permission-wise? Because our warehouse has, like, there's PII tables that only a few roles can touch, and I don't want to be in a position where I'm granting some broad read-all role just so this works.

ADITI: Yeah, no, good question — it's scoped to specific schemas or even specific views, so a lot of customers actually build a dedicated view layer that exposes only what's needed for activation, and grant the service account access to just that layer. It doesn't need account-admin or anything close to it. I can send over the actual permission set after this if that's useful, it's pretty short, it's like four or five grants.

PAUL: Yeah, that'd be good, I'd want to loop in — we don't really have a formal security team, it's more like our IT lead does a pass on stuff like this, but he's not going to be deep in the weeds, so having the actual list would help me just answer his questions directly instead of going back and forth.

ADITI: Yeah, for sure, I'll get that to you.

SOFIA: I'll make a note to send that along with the recap, actually, so it doesn't get lost.

AMARA: So — okay, going back to the segment thing for a second, because I want to make sure I'm not getting ahead of myself here — once I've built that segment, what actually happens with it? Like, does it just sit there as a saved thing, or —

ADITI: So you can save it, and then you can either export it as a one-time pull, or — and this is I think the more interesting piece for what you described earlier with the personalization push — you can set it to sync on a schedule, so it just continuously refreshes and pushes to whatever destination you've connected, so people are added and removed from the audience automatically as their behavior changes, without anyone re-running anything.

AMARA: Oh, that's — okay, that's actually kind of a big deal for us, because right now every one of these is a one-off ask, there's no like, "ongoing" version of it, it's always someone remembering to ask Paul again next month.

PAUL: Yeah, the recurring ones are honestly worse for me than the one-offs, because I've got like three or four segments I'm supposed to be re-running on some cadence and half the time I forget until someone pings me like "hey did that go out."

ADITI: Yeah, this would take that off your plate entirely, basically — you'd set the refresh cadence once, and it just runs.

PAUL: That's — yeah, okay, that's genuinely useful, not gonna lie.

SOFIA: I feel like that's the first unprompted compliment I've heard from an engineer on one of these calls, I'm going to remember this moment.

PAUL: [laughs] Don't get used to it.

AMARA: He's usually the skeptical one, so.

PAUL: I mean, I'm not wrong to be skeptical, most of the time. This is — okay, no, this is actually landing for me so far.

ADITI: I'll take it. Okay, should I keep going, or do you guys want to sit with that for a sec?

AMARA: No, keep going, I have — well, I have one thing, but it can maybe wait until you're done with this part, it's more of a — it's a slightly separate concern.

ADITI: Sure, we can come back to it, or go now, whatever's easier.

AMARA: No, it's fine, finish your thought, I don't want to derail.

ADITI: Okay — so, the other piece, and this is maybe less flashy but I think actually matters a lot for the ongoing maintenance question, is lineage. So once you've got a bunch of these segments running, especially the recurring ones, six months from now someone's going to ask "wait, why is this person in this audience" or "this segment's definition changed at some point, who changed it and when," and instead of that being an archaeology project through Slack history, there's an actual lineage view — this segment was built on these fields, here's the history of changes to the definition, here's every place downstream that's consuming it.

PAUL: Oh, that's — okay, that's actually something we've hit before too, like someone changes a segment definition slightly and doesn't tell anyone, and then a totally different campaign that was relying on the old definition breaks in a confusing way.

AMARA: Oh my god, the loyalty tier thing.

PAUL: Yeah, the loyalty tier thing, exactly.

AMARA: [to Sofia and Aditi] Sorry, inside reference, there was an incident, I won't bore you with it, but yes, that's a very real problem for us.

ADITI: Yeah, that's — I mean that's exactly the scenario this is meant to prevent, so.

SOFIA: [laughing] Now I kind of want to hear the loyalty tier story.

AMARA: It's not that interesting, honestly, it's just — someone tightened the definition of what counted as "gold tier" for a loyalty campaign, didn't tell the team running a separate win-back campaign that was also filtering on loyalty tier, and the win-back campaign just quietly stopped reaching anyone for like three weeks before someone noticed the numbers looked weird.

PAUL: The worst part was it took forever to even figure out that was the cause, because on the surface nothing had "broken," the segment still ran, it just returned almost nobody, and everyone assumed that was just, like, the market being weird that month.

ADITI: Yeah, that's a really common failure mode actually, silent-but-wrong is so much worse than an outright error, because at least an error gets noticed.

AMARA: Right, exactly. Anyway — that's the loyalty tier story, it's very boring in the retelling but it was a whole thing internally.

SOFIA: Should we — I know we're coming up on the halfway mark roughly, do you want to get to Amara's other thing now, or keep going on product?

AMARA: Yeah, let's — I'll just say it now actually, because I think it's relevant to what we've been talking about. So — I guess one thing I'm wondering about, and this isn't a dealbreaker exactly, it's just — we tried a "self-serve" tool a few years back, different vendor, and it was marketed exactly like this, marketing team builds their own segments, no engineering needed, and what actually happened was it required so much configuration and troubleshooting on the backend that Paul ended up basically babysitting it full time anyway, and we didn't get any of the promised speed benefit, we just moved the bottleneck around instead of removing it.

PAUL: Yeah, that's — I mean, I wasn't here for that either, but I've heard about it enough times that I'm sort of primed to expect it, honestly. Like every "no code" thing eventually needs someone technical holding it together behind the scenes.

ADITI: That's a completely fair thing to be worried about, and honestly it's the right question to ask, because a lot of tools in this space do end up that way. Can I ask, do you know what specifically broke down with that other tool? Like was it the segment logic itself, or more the destination integrations, or something else?

PAUL: I think it was mostly — from what I understand, it was two things. One, the underlying data model it needed was really rigid, so any time our schema changed even slightly, someone had to go remap things on the backend, and that someone was always me. And two, it had its own weird sync issues with the destinations, so audiences would just silently fail to update sometimes and nobody would notice until a campaign went out with an empty audience or something.

ADITI: Okay, that's — yeah, I can speak to both of those directly, actually. On the schema piece — because we're querying your warehouse directly rather than requiring data to be pre-shaped into some fixed model on ingest, when your schema evolves, the segment builder reflects that pretty much immediately, because it's reading the live schema, not a static mapping someone configured once. It's not zero maintenance — if you rename a column that a segment definition depends on, that segment's going to need updating, that's just true of any system — but it's not requiring an engineer to remap an entire data model every time something shifts.

PAUL: Okay, that's — that's actually a meaningfully different architecture than what I think we had before, if I'm understanding it right.

ADITI: Yeah, and on the sync failures — so destination syncs have monitoring and alerting built in, so if a sync fails, it's not silent, there's a notification, and there's a status view where you can see, for any given audience, last successful sync time, record count delivered, any errors. So the failure mode isn't "nobody notices until the campaign goes out empty," it's "someone gets an alert and can go look at exactly what happened."

AMARA: Okay, and who would that alert go to, practically? Like is that a thing my team sees, or does it have to route through Paul?

ADITI: It's configurable, but most customers set it up so the marketing team gets the day-to-day sync status, since they're the ones who'd notice if a campaign audience looked wrong, and then there's a separate, more technical error log for actual failures that would go to whoever's the technical owner — so Paul, in your case, presumably.

PAUL: Yeah, that seems right, I don't need to see every successful sync, I just need to know if something's actually broken.

AMARA: Yeah, that would already be better than what we have now, which is just — nothing, until someone complains.

ADITI: To be fair to your concern though — I don't want to just say "it's different, trust me," because I think you're right to be skeptical based on your history. The honest answer is there's still some setup work up front — connecting your warehouse, setting up that permission scoping Paul was asking about, defining the initial data model mappings for things like "what is a customer," "what is a purchase event." That's real work, it's usually measured in days not months for a warehouse like Snowflake, but it's not zero. What it's not, though, is ongoing babysitting every time marketing wants a new segment — that part genuinely becomes self-serve after the initial setup.

PAUL: Okay. Yeah, that — I mean, I appreciate you not just saying "no, none of that will happen to you," because that's exactly what the other vendor said and then it happened anyway.

AMARA: [laughs] Yeah, that tracks with what I remember of that pitch too, actually, now that you mention it.

ADITI: Yeah, I'd rather be straight about the up-front lift than have you find out about it after signing, that's not a great way to start a relationship.

AMARA: No, I appreciate that, honestly. Okay — no, I think that actually does address it, the initial setup being on Paul but the ongoing stuff being on us, that's the model I was hoping for, I just wanted to actually hear it rather than assume it.

PAUL: Yeah, I think — as long as the up-front lift isn't insane, which it sounds like it isn't for a Snowflake setup, I think that's a reasonable trade. Like I'd much rather spend a week doing setup once than keep getting pulled into ad hoc segment requests indefinitely.

ADITI: Yeah, that's exactly the trade it's designed to be.

PAUL: Can I push on one more piece of it though, sorry — what about when segments get genuinely complicated, like joining across purchase history and loyalty tier and, I don't know, store visit data if we ever pipe that in. Does the visual builder actually handle that, or does it fall over past a certain complexity and you're back to needing someone technical anyway?

ADITI: It handles joins across your modeled entities, so as long as those relationships are defined once — like "a purchase belongs to a customer, a store visit belongs to a customer" — the builder can traverse those without someone writing a join manually each time. Where it can get genuinely gnarly is if you want something like a rolling window comparison, "this month versus the same month last year," that kind of thing — some of that's supported natively, but the real edge cases sometimes do need a custom field defined once by someone technical, and then marketing can use that custom field like any other attribute going forward.

PAUL: Okay, so worst case, I define a weird calculated field once, and then it's reusable, it's not "call Paul every time."

ADITI: Exactly, that's the pattern — anything genuinely custom gets built once, and then it's a building block anyone can use, it doesn't recreate the original bottleneck.

PAUL: Okay. Yeah, no, that's — I think that's a fair answer, that's basically what I was hoping to hear.

AMARA: Does that also apply to, like, if we eventually want store visit data in the mix? Because that's not in Snowflake yet, that's still kind of a mess on our side.

ADITI: If it's not in your warehouse yet, that's really a separate project on your end before it'd be usable here — we're not an ingestion tool for getting store visit data into Snowflake in the first place, that's more upstream of what we do. But once it lands there in some reasonably modeled form, it becomes available the same way everything else is.

AMARA: Yeah, that's fair, that's kind of always been true regardless of what tool we use downstream, so.

SOFIA: Amara, does that land for you too, or is there more underneath that one?

AMARA: No, I think that's — that was really the core of it. I think I feel a lot better having actually heard the specifics rather than just the marketing version, so — yeah, I think that's resolved, for me anyway.

SOFIA: Great, good to hear.

ADITI: I can also, if it's useful, just talk through roughly what week one, week two of setup actually looks like, so it's not an abstract "a few days," if that would help you plan around it.

PAUL: Yeah, that'd be helpful actually, at some point, doesn't have to be right now.

ADITI: Yeah, let's do that separately, I don't want to eat the rest of the call on implementation planning before we've even — well, before we've gotten there. But happy to send something over.

SOFIA: We're at like — we've got maybe fifteen, twenty minutes left, I want to be respectful of your time. Should we talk pricing and next steps, or is there more product stuff you wanted to cover?

AMARA: I think — Paul, anything else on your list?

PAUL: I had a question about, like, historical data — like if we wanted a segment based on lifetime purchase behavior, not just recent, is that any different technically?

ADITI: No, it's the same mechanism, it's really just a matter of what's in your warehouse and how far back it goes — the query can reach as far back as your data does, there's no separate "recent data" versus "historical data" system, it's all just querying the same tables.

PAUL: Okay, good, that answers that.

AMARA: Okay, then I think we're good on product for now, we can always follow up with more questions.

SOFIA: Perfect. So on pricing — I don't want to get too deep into numbers on this call, honestly, because I think it makes more sense for me to put together an actual proposal based on what we've talked about today, rather than throw ranges around live. But directionally, for a company your size with the two connectors you'd need — email and paid social, is that right, or is there a third destination I'm missing?

AMARA: Email, paid social, and then eventually push notifications, though push is more of a nice-to-have for phase one, I don't want to overcomplicate the initial scope.

SOFIA: Got it, that's helpful, I'll scope the proposal around email and paid social as the primary destinations then, with push noted as a fast-follow. Directionally, for that footprint, we're usually in a range that I think is going to feel reasonable relative to what you're describing as the current cost of Paul's time, but let me actually put real numbers in front of you rather than hand-wave it.

AMARA: Yeah, that's fine, I'd rather see the real number anyway. In terms of, like, budget — I'll just be upfront, I do have budget allocated for something in this category for this fiscal year, it's not infinite, but it's real, and honestly this is one of the top priorities for my team right now, so if the number's in a reasonable range I don't anticipate this being a hard internal sell. I'd probably still loop in our VP just as a courtesy, but I don't think I need, like, a big justification exercise, this pain is already well understood at that level.

SOFIA: That's really helpful to know, thank you for being direct about that.

AMARA: Yeah, no, I'd rather be efficient about it than play games with the budget conversation, that's not useful for either of us.

SOFIA: Totally agree. And just so I scope the proposal right — is this fiscal year budget something that needs to be used by a certain point, or is it more flexible than that?

AMARA: It's technically available through end of quarter, so there's some mild time pressure, but I'm not going to pretend it's a hard cutoff, it's more that I'd rather not let it slip into next fiscal year and have to re-justify it from scratch. So sooner is better, but I'm not going to make you feel like there's a gun to anyone's head.

SOFIA: Understood, that's helpful to know regardless. And one more thing while we're on the practical side — typically contracts here run annual, is that going to be workable on your end, or is there a procurement quirk I should know about upfront?

AMARA: Annual's fine, that's how basically everything else in our stack is set up, I don't think procurement's going to blink at that.

SOFIA: Great, good to know. Okay, so let me — I'll put together the proposal, I'm thinking I can get that to you by end of week, does that work?

AMARA: Yeah, end of week is great.

SOFIA: And then, once you've had a chance to look it over — should we get something on the calendar now for that follow-up, or do you want to review it first and then reach out?

AMARA: Let's just get it on the calendar now, honestly, otherwise it'll slip. How about — next Tuesday? That gives me a few days with it plus the weekend if I want to dig in.

SOFIA: Tuesday works on my end. Aditi, are you around Tuesday, in case there's technical follow-up?

ADITI: Yeah, Tuesday's fine for me.

PAUL: I should be around too, assuming nothing's on fire, but I'll try to actually block the time.

AMARA: [laughs] Please do, don't let me get ghosted by a production incident.

PAUL: No promises, but I'll try.

SOFIA: And just to set expectations on the implementation side, roughly — assuming we get through Tuesday and things keep moving, what does the actual timeline look like from signature to Paul doing the warehouse setup to your team actually building live segments?

ADITI: Yeah, so typically it's — week one is the warehouse connection and permission scoping we talked about, plus defining the core entities, customer, purchase, that kind of thing. Week two is usually connecting the destinations, so Klaviyo and Meta in your case, and doing a validation pass to make sure counts and records match what you'd expect versus your existing manual process. And then there's usually a short training session for Amara's team on the builder itself, that's typically like an hour, hour and a half, it's not a heavy lift because the interface is meant to be pretty intuitive once you've seen it once.

AMARA: Okay, that's — so realistically, what, three weeks from signature to my team actually running their own segments?

ADITI: That's roughly right, yeah, give or take depending on how quickly Paul's able to prioritize the setup work against whatever else is going on for him.

PAUL: [laughs] No comment on my current backlog, but noted.

AMARA: We'll make it a priority, don't worry.

SOFIA: We can get into the specifics of that timeline in the proposal too, so you've got something concrete to plan around rather than just what we said out loud on a call. Okay, I'll send an invite for Tuesday, same time, and I'll include the proposal beforehand so you both have time to look at it before we talk. And Aditi, you were going to send Paul that permissions list separately?

ADITI: Yep, I'll get that over today or tomorrow.

PAUL: Appreciate it, that'll help me get ahead of the IT conversation before it becomes a blocker.

SOFIA: Perfect. Anything else either of you wanted to raise before we wrap? Any concerns, anything that's nagging at you that we haven't covered?

AMARA: No, I think — honestly this was one of the more useful vendor calls I've sat through in a while, so thank you both. I feel like I actually understand how this would work now versus just having a vague sense of it.

PAUL: Yeah, agreed, this was — this was good. Thanks for actually answering the annoying detailed questions instead of redirecting to sales talking points.

ADITI: Ha, that's the job, honestly, glad it was useful.

SOFIA: Great, well, thank you both again for the time, we'll get that proposal over by end of week, and we'll talk Tuesday. Have a good rest of your week.

AMARA: You too, thanks guys.

PAUL: Yeah, thanks, bye.

ADITI: Bye, everyone.
