---
opportunity: Calibre Financial — Enterprise Data Activation
call_id: calibre-01
call_type: technical_validation
day_offset: -9
duration_minutes: 93
participants:
  - name: Tom Brennan
    role: Account Executive
    org: Apex
  - name: Aditi Sharma
    role: Solutions Consultant
    org: Apex
  - name: Yara Haddad
    role: VP, Enterprise Data
    org: Calibre Financial
  - name: Nathan Cole
    role: Data Governance Lead
    org: Calibre Financial
  - name: Unidentified Speaker
    role: null
    org: Calibre Financial
---

TOM: Okay, I think we're at time — Yara, Nathan, thanks for making room for this, I know ninety minutes is a big ask on a Thursday.

YARA: No, this is the right amount of time for what we need to cover, better than trying to squeeze it into thirty.

NATHAN: Agreed, and we've got a couple more people who might be joining partway through, fair warning, so don't be alarmed if a name you don't recognize pops up.

TOM: No problem, we'll roll with whoever shows up. Before we dive in — Yara, did you end up making it out to that industry conference you mentioned a few weeks back, or did that fall through?

YARA: Oh — no, that got bumped, honestly, budget season ate the travel approval, so that's a next-year thing now.

NATHAN: Yeah, I heard about that, seemed like a bummer, I know you were looking forward to a couple of the sessions.

YARA: [laughs] It's fine, there's always next year, and honestly I've been buried enough that missing three days of travel wasn't the worst outcome.

TOM: [laughs] Silver linings. Okay, quick intros to kick things off properly — I'm Tom, account exec on this from Apex, and this is Aditi, our solutions consultant, she'll carry most of the technical conversation.

ADITI: Hey, good to meet you both properly. I know we did a shorter scoping call a few weeks back with someone from your architecture team, but I'd rather hear the shape of the problem fresh from you two.

YARA: Sure, happy to set the stage. I'm Yara, I lead enterprise data here, so across retail banking, wealth management, and our risk organization, I own the strategy for how customer and account data actually gets used, not just stored.

NATHAN: And I'm Nathan, I lead data governance, so access controls, audit, lineage, all the stuff that has to be airtight before anything Yara's team wants to do can actually go live.

TOM: Perfect, that's exactly the right pairing for a conversation like this.

YARA: So — high level, the problem is that we've got customer and account data spread across a lot of systems, core banking, wealth management platforms, risk and fraud systems, and historically each of those has operated in its own lane. What we want to get to is the ability to actually activate that data — real-time engagement, proactive risk alerts, personalized offers — rather than just having it sit there for quarterly reporting.

ADITI: Can you give a concrete example of what "activate" looks like in practice, something you'd want to be able to do that you can't today?

YARA: Sure — say a customer's spending pattern suggests they might be a good fit for a product they don't currently have, or conversely, their behavior suggests early signs of financial distress that risk would want to know about. Today, neither of those signals reaches anyone in a timely way, because the systems that would need to talk to each other don't.

NATHAN: And to be clear up front, because this is going to shape a lot of today's conversation — anything touching customer financial data here is under real regulatory scrutiny. We're not a company that can move fast and figure out governance later, governance has to be designed in from the start or this doesn't get anywhere near production.

TOM: Understood, and that's exactly why we wanted Nathan in this conversation from day one rather than bringing governance in at the end.

NATHAN: Appreciated, that's not always how vendors approach it, so noted.

ADITI: Should I go ahead and get into the product, or is there more current-state to cover first?

YARA: Let's get into it, I think we've set the stage well enough.

ADITI: Great, let me share my screen. Everyone see okay?

NATHAN: Yep.

YARA: Looks good.

ADITI: Okay, so — given what you're describing, I want to start with the data foundation piece, Streamline Ingest, since a lot of what you're describing depends on getting data from these source systems into a unified, current state quickly. It's built for high-volume event ingestion, sub-minute, so transaction and account activity data lands close to real time rather than on some batch delay.

NATHAN: Before we go further — where does that data actually land? Is that in our environment, or somewhere Apex controls?

ADITI: It runs against your environment, your warehouse specifically — we're not pulling your data into a separate Apex-controlled store. The ingestion and processing happen against infrastructure you control, which matters a lot given what you just said about regulatory scrutiny.

NATHAN: Okay, that's the right starting answer. I'm going to have a lot of follow-ups on exactly what "your environment" means in practice, but that's the right direction.

ADITI: I'd expect that, and I'd rather get into the specifics properly than give you a surface-level answer you'll just have to re-ask later.

YARA: Can I ask a business-side question before we go deeper technical — the real-time engagement use case I mentioned, personalized offers based on spending pattern, does that require us to have already solved for cross-system identity, like knowing a retail banking customer and a wealth management customer are the same person?

ADITI: It does depend on identity resolution to some degree, yes, though the depth required depends on the specific use case — a same-system pattern, like spending behavior within retail banking alone, doesn't need cross-system identity, but connecting retail and wealth management activity for one person would.

YARA: Okay, and how mature does that need to be before we could realistically launch even a narrow first use case?

ADITI: For a narrow first use case within one system, you could move relatively quickly, since you're not solving the hardest identity problem first. Cross-system use cases would be a later phase once that muscle's built. I wouldn't recommend starting with the hardest version of the problem.

YARA: Can I ask a follow-up — within retail banking alone, how much of that spending-pattern use case is genuinely deliverable versus how much still depends on things we haven't built yet, like the offer eligibility logic itself?

ADITI: The eligibility logic itself — deciding who's actually a good fit for a given product — is squarely on your side, that's domain and often compliance-sensitive judgment that has to come from you, similar to what Nathan flagged earlier about decisioning. What we'd provide is the mechanism to act on that eligibility logic once it's defined, and to keep the underlying population current as behavior changes.

YARA: Okay, so realistically the honest scope for a first use case is: we bring the eligibility logic, you handle keeping it current and operational.

ADITI: That's exactly right, yes.

YARA: That's a sensible sequencing, honestly, I was half-expecting you to tell us we need to solve everything before we can do anything.

ADITI: No, that would be a pretty rough way to start a relationship with a new platform, honestly.

TOM: [laughs] We try to avoid that particular flavor of bad advice.

YARA: Can I ask, since we're talking sequencing — is there a typical order customers in financial services specifically tend to start with, retail versus wealth versus risk, or does it vary a lot?

ADITI: It varies, but retail banking tends to be a common starting point for customers with a structure like yours, mainly because the data tends to be more standardized and higher volume, which makes the initial win easier to demonstrate. Risk tends to come later, once there's trust built up, given how much more scrutiny that use case draws.

YARA: That tracks with my instinct too, honestly, I wasn't going to suggest starting with risk regardless of what you said.

NATHAN: [laughs] Good, that would've been a hard no from me on day one. Can I go back to the environment question? When you say it runs against our environment — does that mean a service account with access, similar to what we'd grant any analytics tool, or is there something more involved?

ADITI: It's a service account model, yes, scoped to specific schemas or views rather than broad access. A lot of customers in regulated industries specifically build a dedicated view layer that exposes only what's needed for activation, and grant the service account access to just that layer, keeping the blast radius small.

NATHAN: Can I ask — the service account itself, does it have write access anywhere, or is it strictly read against the source data?

ADITI: It depends on the destination side — reading from your warehouse for the unified view is generally read-only against source systems, but there are write operations involved when activation results get written somewhere, like a computed segment or a derived table. Those writes are scoped to specifically designated output locations, not broad write access across your environment.

NATHAN: Okay, so reads are broad-ish within the scoped view, writes are narrow and specific to designated outputs.

ADITI: That's a good summary, yes.

NATHAN: And is there logging on everything that service account touches, reads and writes both?

ADITI: Yes, all activity through that account is logged, which feeds into the same lineage and audit story we'll get into more later.

NATHAN: Good, I'll want to see what that logging actually looks like in practice, not just hear that it exists.

ADITI: Completely fair, we can arrange that.

NATHAN: Okay, and who defines what's in that view layer — is that entirely on us, or is there a recommended pattern you bring to that conversation?

ADITI: Both — we've got patterns from other financial services customers that we can bring as a starting point, but ultimately your team defines what's actually exposed, since you know your data classification and sensitivity levels better than we do.

NATHAN: Good, I wouldn't want a vendor telling us what our own sensitivity classifications should be.

ADITI: Agreed, that has to come from you.

YARA: Can we talk about the activation side now, or do you want to stay on ingestion a bit longer?

ADITI: I think we've covered the core of ingestion, let's move to activation. So — once data's unified and current, the activation layer is what actually does something with it. Take the spending-pattern example — you'd define a rule or a model output that identifies the pattern, and that population becomes actionable, whether that's triggering an offer, an alert to a relationship manager, whatever the actual next action is.

YARA: And the "define a rule or a model output" piece — does that mean we bring our own models, or is there something built in?

ADITI: You'd bring your own models for anything predictive, we're not shipping a proprietary risk or propensity model, that's exactly the kind of thing that should come from your own data science work, given the regulatory sensitivity around anything resembling a credit or risk decision. What we provide is the layer that takes a model's output, or a simpler rule-based definition, and makes it operational — routed to the right destination, whether that's a relationship manager's queue, a marketing channel, or a risk system.

NATHAN: That's an important distinction, and I want to make sure it's actually true rather than marketing language — you're not making any decisioning judgments yourselves, anywhere in this pipeline?

ADITI: No, we're not, and I want to be precise about that because it matters a lot in your context — decisioning logic, whether that's a model or a rule, is defined and owned by you. We're the operational layer that executes on a decision already made, not the layer making the decision.

NATHAN: Can I push on that boundary a bit more, actually? Because "we don't make decisioning judgments" can mean a lot of things depending on how narrowly you define "decisioning." Does the platform do any kind of ranking, prioritization, or scoring of its own, even something that stops short of a full decision?

ADITI: That's a fair distinction to draw out. The platform can apply logic you've defined, including something like a prioritization order across multiple eligible actions, but that logic is authored by you, it's not the platform independently inferring or generating a ranking on its own. If you wanted, say, "email before push notification," that ordering is something you configure, not something the platform decides based on its own judgment.

NATHAN: Okay, so even prioritization logic, as long as it's platform behavior, is still something you wrote the rules for, not something inferred.

ADITI: Correct, nothing in this pipeline is making an inference about a customer on its own initiative, everything traces back to logic your team defined.

NATHAN: Okay, that's — that's actually the answer I needed to hear, because if that boundary were blurry, this wouldn't be a conversation we could keep having.

YARA: Agreed, that boundary is non-negotiable for us.

TOM: Understood completely, and I'd rather lose a deal than misrepresent that boundary, honestly, that's not the kind of thing you can walk back later.

YARA: Can I ask something adjacent while we're on this — for the risk-alerting side specifically, does the same "we don't decide, we execute" boundary hold, or is risk treated any differently given the regulatory weight there?

ADITI: Same boundary, no exceptions, if anything the boundary matters even more for risk given the regulatory scrutiny you'd expect there, not less. We wouldn't want to be in a position where a regulator asks who made a risk-relevant call and the honest answer involves a black box on our side.

YARA: Good, that's exactly the answer I needed to hear on that specifically, given how much scrutiny that particular use case would draw internally.

NATHAN: Agreed, risk is genuinely the highest-stakes version of this conversation for us, so I'm glad the answer's consistent rather than "mostly, except for risk."

[The door opens off-screen; a fourth voice joins partway through, unannounced.]

UNIDENTIFIED: Sorry, sorry — got pulled out of another call, didn't mean to walk in mid-sentence. Please continue, I'll catch up.

YARA: No worries, we're mid-conversation about the decisioning boundary, Aditi was just confirming Apex doesn't make any decisioning judgments itself, it's purely operational once a decision's already been made upstream.

UNIDENTIFIED: Good, that's the right boundary. Can I ask a follow-up on that once you're done with this thread?

ADITI: Of course, go ahead whenever's natural.

NATHAN: I think we're basically done with this specific thread, so — go ahead.

UNIDENTIFIED: Okay — so if the operational layer is executing on a decision already made, what happens when that decision needs to be revoked or reversed after the fact? Say a model output gets flagged as wrong after some actions have already been triggered off it.

ADITI: That's a good question. The lineage record would show exactly what was triggered based on that specific output, so you'd be able to identify and unwind the affected actions rather than that being a manual forensic exercise. It doesn't automatically reverse real-world actions that have already happened, like an offer that's already been sent, but it gives you the trace to know exactly what needs remediation.

UNIDENTIFIED: Okay, that's reasonable. I'd want to see that in practice rather than just hear it described, but conceptually that's the right shape.

TOM: We can absolutely walk through that more concretely in a follow-up if that would help.

UNIDENTIFIED: Yeah, that'd be useful.

NATHAN: While we're on remediation — if something needs to be unwound, does that require engineering effort each time, or is there a repeatable mechanism for it?

ADITI: It's meant to be repeatable rather than a bespoke engineering exercise each time — since the lineage record identifies the affected population precisely, unwinding or suppressing further downstream action against that population is a defined operation, not something someone has to hand-build from scratch every incident.

NATHAN: Okay, that's good, because if every remediation were its own mini-project, that would get old fast, and probably wouldn't actually get done consistently under time pressure.

UNIDENTIFIED: Agreed, consistency under pressure is exactly when ad hoc processes tend to fail.

ADITI: Yeah, that's really the point of making it a repeatable mechanism rather than relying on someone being careful and thorough during what's usually already a stressful moment.

NATHAN: Can I ask, is there a way to simulate or dry-run a remediation before actually executing it, or is it act-first, verify-after?

ADITI: There's a preview step, yes, you'd see what a remediation would affect before committing to it, rather than being forced to execute blind and hope the scope was right.

NATHAN: Good, that matters a lot, I would not want to find out after the fact that a remediation touched a broader population than intended.

UNIDENTIFIED: Agreed, that's exactly the kind of thing that turns a contained incident into a bigger one, a remediation that overcorrects.

ADITI: Right, and that's really the whole reason a preview step exists, remediation shouldn't introduce its own new risk in the process of fixing something else.

YARA: Can I ask something for my own understanding — the lineage piece, is that something Nathan's team would be the primary owner of, or is that more broadly useful?

NATHAN: It's primary for us, honestly, but I could see risk and even some of the business teams wanting visibility into it too, depending on what's being traced.

ADITI: Yeah, access to lineage is configurable by role, so it's not an all-or-nothing thing, different teams can see the slice that's relevant to them.

YARA: Can I ask about the export format for something like an internal audit request — does that come out in something an auditor could actually work with, or is it more of a UI-only view?

ADITI: There's a structured export, not just a UI view, so it's not limited to screenshots or manual transcription for an auditor, the underlying records can be pulled in a format your team could hand off or load elsewhere.

YARA: Good, I've dealt with tools before where the "audit trail" turned out to be a dashboard feature with no real export, and that's basically useless the moment an actual examiner asks for something concrete.

NATHAN: Yeah, that's happened to us before too, unfortunately, with a system I won't name.

ADITI: [laughs] I've heard some version of that story from almost every regulated customer we work with, it's a really common gap in this space.

NATHAN: Retention on the lineage data itself — is that indefinite, or does it also get purged on some schedule?

ADITI: Configurable, same as the audit trail retention we'll get into shortly — you'd set it to match whatever your actual obligations are rather than it defaulting to some arbitrary window that may or may not align with what you're required to hold.

NATHAN: Okay, good. And one more — if someone with legitimate access looks at a record, is that itself logged, like an access log on top of the data log?

ADITI: Yes, access is logged separately from the data lineage itself, so you'd have both "what happened to this data" and "who looked at it and when" as distinct, traceable records.

NATHAN: Good, that's actually important for us specifically, we get asked about access patterns almost as often as we get asked about the data itself.

YARA: Yeah, agreed, "who looked at this" is its own recurring audit question for us, separate from "what happened to it."

ADITI: That's a really common pairing of requirements in financial services specifically, so that distinction being modeled explicitly isn't an afterthought.

UNIDENTIFIED: Can I ask, is the access log itself immutable, or could someone with sufficient privilege alter it after the fact?

ADITI: It's designed to be append-only, so entries aren't editable or deletable after the fact, even by someone with elevated privilege, which matters a lot for exactly the scenario you're describing, an audit log that can be quietly altered isn't really an audit log.

UNIDENTIFIED: Good, that's the right answer, a mutable audit log is close to worthless from an audit standpoint.

NATHAN: Agreed, that's a hard requirement for us, not a nice-to-have. And more generally, that's the right model overall, I wouldn't want lineage data itself to become its own uncontrolled sprawl.

UNIDENTIFIED: Can I ask, does role-based access here integrate with our existing identity provider, or is that a separate user directory we'd have to maintain in parallel?

ADITI: It integrates with standard identity providers via SSO, so it's not a separate directory you're maintaining in parallel, access and roles are managed through the same identity system you're already using for everything else.

UNIDENTIFIED: Good, a parallel user directory would've been an immediate no from me, honestly, that's exactly the kind of thing that quietly becomes a security liability over time as it drifts out of sync with the real directory.

NATHAN: Agreed, that's happened to us before with a different tool, a shadow user list nobody was maintaining properly.

ADITI: Yeah, that's a really common failure mode, and it's part of why SSO integration isn't optional here, it's the default expectation for anything touching access control.

NATHAN: Can I ask, does that include multi-factor enforcement too, or is that something layered on separately through the identity provider itself?

ADITI: That's inherited from your identity provider's own MFA policy, we're not maintaining a separate authentication path that could bypass whatever MFA requirements you've already got configured there.

NATHAN: Good, that's exactly what I'd want, one consistent authentication surface rather than a second door that might be weaker than the front one.

YARA: Yeah, "a second door that's weaker than the front one" is a pretty good way to describe exactly the kind of gap that gets found in a penetration test the hard way.

ADITI: [laughs] Unfortunately accurate, yeah, that's a really common way these things get discovered.

YARA: Can we get into the governance and access control side more directly now? I think that's going to be the thing that actually determines whether this is viable for us.

ADITI: Yeah, let's do that, that's probably the most important part of today honestly, given everything Nathan's flagged.

NATHAN: So — I guess one thing I'm wondering about, and it's the big one — for fields that are genuinely sensitive, account numbers, SSNs, anything that would be considered high-sensitivity under our data classification framework, what actually happens to those during ingestion and processing?

ADITI: Sensitive fields go through field-level encryption at ingestion, before any processing touches them, and for anything needed for matching or joining across sources, that happens via tokenization rather than operating on raw values. The pattern's similar to what we'd do for any regulated customer, though the specific field classifications would need to map to your framework specifically, not some generic one.

NATHAN: Okay, walk me through tokenization a bit more — is that reversible by design, or genuinely one-way?

ADITI: One-way, deterministic — same input always produces the same token, which is what makes matching work, but there's no key that reverses a token back to the original value, and the mapping isn't stored as a reversible lookup table either.

NATHAN: And the encryption keys — who holds those?

ADITI: For most deployment models, customer-managed, through your own KMS setup, rather than us holding a universal key.

NATHAN: Okay. I think — I think that's directionally right, but I'd want our security team to actually validate the specifics before I'd call it resolved. It sounds right on paper, I just don't want to say "yes, that's fine" on a call and have it turn out there's a gap once someone actually digs in.

ADITI: That's completely fair, I wouldn't want you to sign off on my say-so alone either, honestly.

NATHAN: Can I ask about key rotation, actually, since we're on encryption — if keys get rotated, does that break anything downstream, existing tokens, existing encrypted values?

ADITI: Rotation is designed to not break existing encrypted data — there's a defined process for re-encrypting under a new key without losing access to historical data, rather than rotation being a destructive event. I'd want to walk your security team through the specific mechanics rather than summarize it loosely here, since that's exactly the kind of detail that matters a lot in practice and less in theory.

NATHAN: Yeah, I'd want that in writing too, honestly, "designed to not break things" is the kind of sentence that sounds great until it isn't true under some edge case nobody thought of.

UNIDENTIFIED: Can I ask, has rotation ever actually caused a customer-facing issue in practice, or is this genuinely theoretical at this point?

ADITI: I don't have an incident to point to off the top of my head, but I don't want to claim perfection on the spot either, I'd rather check and give you an accurate answer than assert "never" from memory on a call.

UNIDENTIFIED: Appreciate that, "let me check" is a better answer than a confident "never" that turns out to be wrong.

NATHAN: Agreed, that's the right instinct.

ADITI: Fair, and I'd rather you hold that skepticism until it's actually demonstrated than take it as settled based on a description.

NATHAN: Appreciated. One more on this thread — data residency. Is everything processed within a specific region, or does that vary?

ADITI: That's configurable to match your requirements, we don't force processing into a specific region regardless of what you need, but I'd want to understand your specific residency requirements before claiming we definitely satisfy them, since "configurable" isn't the same as "already validated against your specific obligations."

NATHAN: That's a fair distinction. I don't think residency is our sharpest edge case, honestly, most of what we're discussing today stays domestic, but I wanted to ask regardless.

ADITI: Good to know, that simplifies at least that piece of it.

UNIDENTIFIED: Can I ask a follow-up on encryption at rest specifically — is that applied uniformly across all data, or only to the fields flagged as sensitive?

ADITI: Field-level encryption is targeted at flagged sensitive fields specifically, not applied uniformly to everything, since encrypting non-sensitive fields the same way would add overhead without a corresponding benefit. That said, the underlying storage itself is also encrypted at rest more broadly, so there's a layered approach, targeted field-level plus broader storage-level.

UNIDENTIFIED: Okay, that's a reasonable layered approach, that's roughly what I'd expect from a mature system.

NATHAN: Agreed, that matches what I'd want to see, defense in depth rather than relying on one single control.

YARA: Can I ask —

UNIDENTIFIED: — sorry, go ahead, Yara, I was going to ask something similar —

YARA: No, go, you probably had the sharper version of it.

UNIDENTIFIED: I was just going to ask whether the tokenization approach holds up specifically for cross-institution matching, since a decent chunk of what we'd eventually want touches data that originated outside our own systems, like third-party enrichment data.

ADITI: That's — that's a good question, and I want to be honest that cross-institution matching introduces complexity beyond what I described for internal sources, since you're dealing with data that was tokenized, if at all, under someone else's scheme. That would likely need its own dedicated design conversation rather than an answer I give you right now.

NATHAN: Yeah, agreed, that's not a today question.

UNIDENTIFIED: Fair, I figured as much, just wanted to flag it before we move too far past governance.

YARA: Good flag. Can I ask, while we're on third-party data — does the same field-level encryption approach apply to enrichment data that comes in from an outside vendor, or does that get treated separately since we didn't originate it?

ADITI: Same treatment at ingestion, sensitive fields get encrypted regardless of whether the data originated internally or from a third party, the protection isn't conditional on data provenance.

YARA: Good, that's what I'd hope, I wouldn't want a gap just because something came from outside our walls.

NATHAN: Agreed, third-party data isn't automatically lower-sensitivity just because we didn't generate it ourselves, sometimes it's the opposite.

ADITI: Exactly, and that's really the right instinct, provenance shouldn't determine protection level, sensitivity should.

NATHAN: Can I push on one more piece — audit. If a regulator or internal audit comes asking "show me every time this customer's data was used for a decision in the last year," can we actually answer that from this?

ADITI: Yes, that's what the lineage and audit trail is built for — every activation, what data fed into it, when, and through what rule or model, is traceable at the individual record level, not just a high-level summary.

NATHAN: Retention on that — configurable to match our actual regulatory retention requirements, or is there some default that doesn't fit financial services timelines?

ADITI: Configurable, it's not degraded into aggregates or purged on some default schedule that ignores your actual requirements, you'd set retention to match what you're obligated to hold.

NATHAN: Okay. That's — I think that's a reasonable answer. I'm not going to pretend I've fully stress-tested it, but nothing in what you've described is raising a flag for me right now.

UNIDENTIFIED: Can I add one thing here, actually, before we move on — has this specific architecture, the encryption and tokenization approach, actually been through a third-party penetration test, or is that something still in progress?

ADITI: It has, yes, that's part of our standard SOC 2 Type II process, and we'd share the relevant summary under NDA as part of your security review.

UNIDENTIFIED: Good, I'd want to see that directly rather than take the description at face value, no offense.

ADITI: None taken, honestly, I'd be more worried if nobody asked to see it directly.

YARA: That's about as strong an endorsement as you'll get out of Nathan on a first pass, for what it's worth.

NATHAN: [laughs] Fair, accurate.

ADITI: I'll take "no flags raised" as a genuine win, honestly.

YARA: Can I ask one more governance question before we move on — internally, who at Apex actually has access to a customer's raw data during support or troubleshooting? Because that's always a question I get asked, "who at the vendor can see our data."

ADITI: Support access is scoped and logged as well, it's not broad internal access by default, someone would need a specific reason and it would go through an access request process, not just ambient visibility for anyone on our side.

YARA: Okay, and is that access logging visible to us, or purely internal to Apex?

ADITI: That's something we can expose to you as part of the audit trail, yes, vendor-side access to your data being invisible to you would undermine a lot of what we've talked about today.

YARA: Good, that's the right answer, I'd have been a lot more skeptical of everything else we discussed if that one came back wrong.

NATHAN: Agreed, that's honestly one of the first things our security review would flag if it were missing.

YARA: Can I ask, is there a limit on how granular that support-access approval can be, like scoped to one specific account versus broader access to troubleshoot a systemic issue?

ADITI: It can be scoped narrowly, down to what's actually needed for the specific issue being investigated, rather than defaulting to broad access just because it's more convenient on our side. Broader access would require a correspondingly broader justification, not just a default setting.

YARA: Good, that's the right default, convenience shouldn't be the reason access is broader than it needs to be.

NATHAN: Agreed, "it was more convenient" is not a justification we'd accept internally either, so it's good that's not the default here.

TOM: Should we take a quick beat, or keep going? I know we've been deep in governance for a while.

YARA: Let's keep going, I think we're making good progress and I don't want to lose momentum.

ADITI: Okay — one more governance-adjacent thing worth covering, since we touched on cross-institution data a second ago — consent and permissible use. For any data that's subject to customer consent or specific permissible-use restrictions, is that something your systems already track in a structured way, or is that more ad hoc today?

NATHAN: It's tracked, but not uniformly, honestly — retail banking has a reasonably mature consent framework, wealth management's is less mature, and I'd call risk's approach to permissible use more policy-based than systematized.

YARA: Yeah, that unevenness is real, and it's honestly one of the things I'd want this to help us get in front of rather than just inherit.

ADITI: Understood, that's useful to know, because the platform can model consent and permissible-use state centrally similar to how we handle other governance metadata, but it's going to reflect whatever maturity exists in each source, it's not going to retroactively fix an ungoverned source on its own.

NATHAN: Can I ask, practically, who at your company would we be working with if we needed to escalate a governance question during implementation — is that Aditi directly, or is there a dedicated governance contact on your side for customers like us?

ADITI: For customers with governance requirements at this depth, there's typically a dedicated point of contact beyond just the SC relationship, someone who specifically handles the ongoing compliance and security conversation, not just initial sales. I can get you specifics on exactly who that'd be for an account like yours.

NATHAN: That would help, I'd rather have a named person than a generic support queue for something this sensitive.

YARA: Agreed, that matters a lot to me too, honestly, generic support queues are where governance questions go to die.

ADITI: [laughs] Fair, and understood, we'll make sure that's clear before anything's signed, not after.

NATHAN: Right, that makes sense, I wasn't expecting it to fix wealth management's consent tracking for us, that's on us regardless.

YARA: Agreed, that's a separate workstream from this specifically, even if it's related.

NATHAN: Can I ask, practically — once consent state is modeled centrally, does that flow both ways, like could we use this to actually surface where our consent tracking has gaps, or is it purely a pass-through of whatever exists today?

ADITI: It can surface gaps, actually — if a source system has no consent record at all for a given population, that absence is visible rather than silently defaulting to some assumption, so it can become a useful diagnostic for exactly the unevenness you described, not just a pass-through.

NATHAN: That's actually more useful than I expected, honestly, I was picturing something that just reflects our mess back at us without adding value.

YARA: Yeah, agreed, visibility into the gap itself is worth something on its own, even before we've fixed anything.

ADITI: That's a common secondary benefit customers mention, actually, the diagnostic value of unification sometimes matters as much as the activation use case itself, at least early on.

NATHAN: Can I ask, does surfacing a gap like that create any liability on our end, like are we now on the hook for something we weren't formally aware of before?

ADITI: That's really a legal and policy question more than a technical one, I don't want to give you a confident answer on liability implications, that's genuinely outside what I can responsibly speak to.

NATHAN: Fair, that's probably a conversation for our legal team regardless of what this platform does or doesn't surface.

YARA: Agreed, that's not something we resolve on this call either way. Can I ask, is there a way to actually quantify that gap, like a report that says "X percent of this population has no recorded consent," or is it more of a qualitative flag?

ADITI: It can be quantified, yes, that kind of coverage reporting is a natural byproduct of modeling consent state as structured data rather than something buried in each source system's own format.

YARA: That would actually be useful for a completely separate conversation I've been trying to have internally about wealth management's consent maturity specifically, having a real number instead of an anecdote would change that conversation a lot.

NATHAN: Yeah, agreed, "we think it's less mature" lands very differently than an actual coverage percentage in front of leadership.

ADITI: That's a really common pattern, honestly, having a number instead of an impression tends to unlock internal conversations that had been stuck on anecdote versus anecdote.

UNIDENTIFIED: Can I ask something adjacent — does that coverage reporting extend to permissible-use restrictions too, or is it specifically a consent-opt-out thing?

ADITI: It can extend to permissible-use metadata as well, since that's modeled similarly to consent state, structured rather than buried in each source's own format. The specific categories you'd track are configurable to match however your policy actually defines permissible use.

UNIDENTIFIED: Good, because those are related but not identical concepts in our world, and I've seen tools conflate them before in ways that caused real confusion.

NATHAN: Yeah, agreed, permissible use and consent get treated as synonyms more often than they should be, and that's caused us actual problems before.

ADITI: That's a really important distinction to preserve, and it's good that you're both flagging it now rather than us discovering it's conflated somewhere downstream.

TOM: Understood, we won't assume that's in scope unless you tell us otherwise.

UNIDENTIFIED: Can I ask something slightly different — performance, actually, not governance. For the risk-alerting use case specifically, what's the actual latency from a transaction happening to a risk signal being available downstream? Because for some of what risk would want, minutes matters a lot more than it would for, say, a marketing offer.

ADITI: For transaction-level events feeding through Streamline Ingest, we're talking sub-minute from ingestion to queryable, similar to what I'd describe for any high-volume event stream. The end-to-end latency including whatever model or rule evaluation happens on top of that depends on how that logic is architected on your side, that's not purely an ingestion question.

UNIDENTIFIED: Okay, and is there any guarantee around ordering for something like a sequence of transactions that risk logic depends on, or is that something we'd need to design for explicitly?

ADITI: Similar to how we'd handle it for any event stream — ordering is based on event time rather than arrival time, so a late-arriving event doesn't get treated as more current than an earlier one just because it showed up later. For something as sensitive as risk logic specifically, I'd want to actually work through your exact requirements rather than assume a general answer fully covers a use case with this much on the line.

UNIDENTIFIED: Can I ask one more thing on this before we move off it — you mentioned event-time ordering, does that mean the system waits for some window to close before considering data "final," or can a value change after it's already been acted on?

ADITI: There's a defined lateness window you'd configure, so the system waits a bounded amount of time for late-arriving events before treating a given window as settled, rather than either acting instantly on possibly-incomplete data or waiting indefinitely. If something arrives after that window closes, it's flagged as a late correction rather than silently changing something that's already been acted on.

UNIDENTIFIED: Okay, and is that lateness window something we'd tune per use case, or is it a global setting?

ADITI: Per use case, yes, a marketing use case and a risk use case could have very different tolerance for that tradeoff, and the configuration reflects that rather than forcing one global setting on everything.

UNIDENTIFIED: Okay, that's — that's a reasonable architecture. I still think risk specifically needs its own session, but this is a more thought-through answer than I expected, I'll say that.

ADITI: [laughs] I'll take that, genuinely.

NATHAN: Agreed, risk logic specifically probably needs its own conversation with our risk architecture folks in the room.

ADITI: That's completely reasonable, I'd rather flag that as needing deeper treatment than give you a general answer and have it turn out to be insufficient for something this consequential.

YARA: Can I bring up something from the business side while we're partway through? I want to make sure we get to it before we run out of time.

TOM: Of course, go ahead.

YARA: I guess the thing I keep coming back to is — this is a lot of our customer and account data becoming dependent on one vendor's platform for activation. If something happened, if Apex had a major outage, or if we needed to walk away from this relationship for some reason down the road, how locked in are we, practically?

TOM: That's a fair and important question. On the technical side, since everything runs against your own warehouse rather than a separate Apex-controlled store, your underlying data isn't trapped anywhere, it's still sitting in your environment regardless of what happens with us. On the configuration side — the rules, the mappings, the activation logic you build — there's an export mechanism for that, so it's not purely proprietary lock-in either.

YARA: Okay, and how tested is that export path, practically? Is that a real, exercised thing, or a theoretical capability nobody's actually used?

ADITI: I'd want to give you a precise answer on how frequently that's actually exercised in practice rather than —

NATHAN: — sorry, actually, before you answer that, I want to add something to Yara's question, because I think there's a compliance angle too, not just a technical one —

ADITI: — no, go ahead, that's a fair thing to fold in —

NATHAN: — right, because even if the export mechanism works technically, there's a separate question of whether the exported configuration would actually satisfy an internal audit requirement around vendor exit planning, which is its own checklist we'd have to run.

YARA: Right, that's exactly what I was getting at too, it's not just "can we get the data out," it's "would getting the data out actually satisfy what we're obligated to be able to do."

TOM: That's a really fair distinction, and I don't think I can give you a fully satisfying answer to the compliance-checklist version of that question right now, honestly. I can tell you the technical export capability is real and used by other customers, but whether it maps cleanly onto your specific vendor-exit obligations is something I'd want to actually look into properly rather than guess at.

YARA: Yeah, I'd rather you say that than give me a confident answer that turns out to be wrong later.

NATHAN: Agreed, this is exactly the kind of thing that needs a real answer, not a reassuring one.

ADITI: Understood, we'll take that as a real follow-up item rather than something we handle in the room.

TOM: Noted, I'll make sure that's tracked properly.

UNIDENTIFIED: For what it's worth, this is a pretty common gap in my experience, vendors rarely have a crisp answer to the compliance-checklist version of that question, so I wouldn't read too much into Apex specifically not having one on the spot.

YARA: That's fair, thank you, Priti, that's a useful frame.

NATHAN: Yeah, agreed.

TOM: We're coming up on the hour and a half mark, I want to be mindful of everyone's afternoon. Should we start thinking about wrapping, or is there more you wanted to cover?

YARA: I think there's a bit more, but let's move a little faster through what's left.

ADITI: Sure — quickly, on rollout, given everything we've discussed, especially the governance depth, I'd expect an initial narrow use case, something within one system rather than cross-institution, to be a meaningful project, not a trivial one, given the sensitivity of what we're handling. I don't want to throw out a specific timeline without more clarity on exactly which use case you'd start with.

YARA: That's fair, I don't think we've even fully decided that internally yet, honestly.

NATHAN: Yeah, that's still genuinely open on our side.

YARA: Can I ask, practically, how does the retail-banking-first sequencing you mentioned earlier actually interact with the cross-institution question we raised before? Like, does starting narrow now make the harder cross-system work easier later, or are those genuinely independent tracks?

ADITI: Starting narrow does tend to make the harder work easier later, mainly because you build real operational muscle, trust in the outputs, a track record of the governance model actually holding up, before layering on the added complexity of cross-institution matching. It's not that the narrow use case technically unlocks the harder one, but organizationally it tends to set you up much better for it.

YARA: That's a reasonable way to think about sequencing, honestly, prove it out narrow, then earn the harder problem.

NATHAN: Agreed, and honestly, if the narrow version doesn't hold up under our governance requirements, that's important to know before we've invested in the harder version anyway.

YARA: Can I ask, roughly, how long would you expect the narrow first use case to take, start to finish, given everything we've discussed today?

TOM: I don't want to commit to a precise number given how much is still open, particularly around the risk-architecture conversation and the vendor-exit compliance question, but directionally, for a narrow, single-system use case at your scale, I'd expect something in the range of a few months rather than weeks, mostly driven by the governance validation work, not the platform configuration itself.

YARA: That's roughly in line with what I was expecting, honestly, nothing about that surprises me given the depth of what we've covered.

NATHAN: Agreed, and frankly I'd be more worried if you told me it could move faster than that, given everything we've just spent an hour and a half establishing needs real scrutiny.

TOM: [laughs] Understood, we're not going to try to rush something that shouldn't be rushed. And more broadly, we won't force a scope decision today either.

YARA: On pricing — I don't expect a number today, but directionally, given the scope, I assume we're talking about something meaningfully north of what a smaller engagement would look like.

TOM: That's fair to assume, yes, I'd rather come back with something real once we've got more clarity on scope, especially given the governance depth might affect what's actually included.

YARA: That makes sense.

NATHAN: Can I ask one more thing before we run out of time — the SOC 2 report, pen testing cadence, the usual security-attestation package, is that something you can share ahead of a deeper security review?

ADITI: Yes, all of that's available, typically under NDA, I can get that started on our side right after this call.

NATHAN: Appreciated, that'll help our security team get a head start rather than waiting for a formal review to even begin looking at it.

TOM: We'll get that moving today.

UNIDENTIFIED: Can I ask one more thing, unrelated to security — the model risk management function, does that typically get involved in a conversation like this at some point, or is that a separate track from what we're discussing?

YARA: That's a good question, honestly. Model risk would get involved once we're actually bringing a specific model into this, since the platform itself isn't the model, it's what operationalizes a model's output. So probably not day one, but definitely before anything with real model output goes near production.

NATHAN: Agreed, that's downstream of today's conversation, but it's on the list of stakeholders that'll need to weigh in eventually.

TOM: Good to know, we'll keep that in mind for how we think about the eventual rollout sequencing.

UNIDENTIFIED: Just wanted to flag it now rather than have it be a surprise gate later.

YARA: Appreciated, that's a fair thing to get ahead of.

NATHAN: Can I ask one more thing before we're totally out of time — is there a customer reference in financial services specifically we could talk to at some point, ideally someone who's gone through a governance review as deep as this one's shaping up to be?

TOM: Yeah, we've got a couple of financial services customers who'd likely be willing to talk, I don't want to commit a specific name without checking with them first, but that's something I can arrange.

NATHAN: Appreciated, that would genuinely help internally, hearing from a peer tends to carry more weight than anything we say ourselves.

TOM: Completely understand, we'll get that lined up once it's useful timing-wise.

YARA: One more small thing before we actually wrap — is there a way to get a written summary of everything we covered today specifically, not just a generic recap, given how much ground we went over?

ADITI: Yes, I can put together something that actually reflects the specific threads we covered, the decisioning boundary, the governance and access model, the open items, rather than a generic template recap.

YARA: That would help a lot, honestly, given how much is still open, I'd rather have something concrete to reference than rely on everyone's memory of a ninety-minute call.

NATHAN: Agreed, that'll help whoever else needs to get read in on this internally, so they're not starting from nothing.

YARA: Okay — I think, given everything we've covered, and given how much is still genuinely open — the risk-latency piece, the vendor-exit compliance question, the actual use case we'd start with — I don't think we're at a point where I can say what the next concrete step is today. I think we'll probably want to loop in Renata before we go much further, she owns a lot of the cross-functional prioritization on our side and none of this should move without her weighing in.

NATHAN: Yeah, agreed, this touches enough open threads that I don't think we should manufacture a tidy next step just for the sake of having one.

TOM: That's completely fair, and I'd rather we leave this accurately unresolved than pretend otherwise.

ADITI: Agreed, there's real substance to follow up on regardless of whether there's a formal next step defined today.

UNIDENTIFIED: For what it's worth, I thought this was a genuinely substantive session, more than I expected going in.

YARA: Agreed, thank you both, this was useful even without a clean bow on it.

NATHAN: Yeah, appreciated the directness today, on both sides.

TOM: Thank you all, we'll get the security materials moving and stay available for whenever you're ready to pick this back up.

YARA: Sounds good, talk soon.

NATHAN: Bye, everyone.

ADITI: Thanks, bye all.
