# Enforcement Layer — Build Spec

Four additions, in priority order. If time runs out, the dashboard is the one to mock rather than build.

---

## 1. Stage exit criteria (cheapest, build first)

Turns "what's blocking us" from prose into a gate. All five criteria are already derivable from the Record payload.

**Criteria for Technical Validation → Commercial Negotiation:**

| Criterion | Owner | Derived from |
|---|---|---|
| All technical objections resolved or accepted | SC | `objections` — none `open` or `resurfaced` |
| Economic buyer identified | AE | a stakeholder with `role_inference: economic_buyer`, confidence high or medium |
| Integration approach agreed | SC | every `integration_patterns` entry has `agreed: true` |
| Next step scheduled with owner and date | AE | `next_step.present` true, owner and `date_committed` both set |
| Success criteria captured in customer's words | AE | `success_criteria` non-empty |

**Render in the pinned record**, above "What's blocking us":

```
*Exit criteria — 2 of 5*
✅ Integration approach agreed — Marcus
✅ Success criteria captured — Daniel
❌ Technical objections resolved — Marcus · 1 open (BAA coverage)
❌ Economic buyer identified — Daniel · Priya inferred, unconfirmed
❌ Next step scheduled — Daniel · no date committed
```

Add a `stage_exit_criteria` block to the Record payload so the dashboard can aggregate it without recomputing. Store: criterion, owner role, met boolean, and a one-line reason when unmet.

**Why this matters more than it looks:** it gives the manager view something countable, it makes every action item traceable to a gate rather than a suggestion, and it's the honest answer to "who's enforcing this" — the criteria are, and the dashboard reports on them.

---

## 2. Action-item closure tracking

The enforcement primitive. Everything else reads from this.

**New table:**

```sql
create table action_items (
  id uuid primary key default gen_random_uuid(),
  opportunity_id uuid references opportunities(id) on delete cascade,
  record_version int,
  owner_role text,              -- 'ae' | 'sc' | 'customer'
  owner_name text,
  description text not null,
  due_date date,
  is_blocker boolean default false,
  status text default 'open',   -- 'open' | 'completed' | 'missed'
  completed_at timestamptz,
  created_at timestamptz default now()
);
```

`write_action_items.py` writes action items when a Record version is written. Dedupe across versions — an item restated in v3 that was already open in v2 is the same item, not a new one. Match on owner plus a semantic comparison of the description, not string equality.

**`scripts/check_closure.py`** runs against `action_items` where `due_date <= today` and `status = 'open'`, and resolves each against evidence:

- AE items → a matching row in `activities` after the item was created
- SC items → the corresponding Record field changed state
- Customer items → stage advanced, or the blocking objection resolved

No evidence by the due date → `missed`. This is deliberately conservative: absence of logged evidence is the same signal the packet's touch data is built on.

---

## 3. Two-stage escalation

**Stage 1 — private, 72 hours.** DM to the owner. Names the specific item, the date, and days-in-stage. Once only.

**Stage 2 — public, 7 days.** Posted to the deal channel, @-mentioning the owner. Names the item, that a private reminder was already sent, and the stage-exit criterion it's gating.

```
⚠️ @daniel — open 7 days past due
BAA position from Apex legal · due Wed Sep 16 · reminded Sep 17
Gating: technical objections resolved
Meridian is 30 days in Technical Validation. Average is 12.
```

**The line to use when challenged:** *"The private nudge comes first, so the escalation is never a surprise. It posts to the deal channel — the AE, the SC, the CSM — not a sales-wide channel. That's a working team, not an audience. A nudge with no escalation is a nudge with no teeth, and that's how the Confluence guide died."*

Nudge dismissal rate stays a counter-metric. If escalations climb, the thresholds are wrong and they get tuned down.

---

## 4. Adherence dashboard

**Build it as a static HTML file generated from a query.** `scripts/build_dashboard.py` queries Supabase, writes `dashboard.html`, you open it in a browser. No server, no auth, no live refresh, no interactivity. It demos identically to a real dashboard and costs a fraction of the time.

Two panels, and the distinction between them is the important part.

### Panel A — adherence (real data)

Computed from your actual records and action items:

- Action items committed vs. completed, by owner role
- On-time completion rate, per AE and per SC
- Open items past due, with days overdue
- Deals past stage average with no next step scheduled
- Exit criteria met, per deal — a 5-column grid across all deals
- Record coverage: % of technical validation calls with a complete Record
- Median hours from call to Record generation

### Panel B — outcome correlation (the instrument, clearly labeled)

Structure the panel, populate it with placeholder data, and **label it explicitly**: `Awaiting volume — 90-day holdout design`.

- Days in Technical Validation: deals with all exit criteria met vs. not
- Win rate: record-covered vs. holdout cohort
- CS time-to-first-value: against the r=0.71 baseline
- Post-demo touches by AE quartile: 0.7 → 1.5 target for bottom quartile

**Say this out loud during the demo:** *"Panel A is real, computed from the records in this database. Panel B is the instrument, not a finding — I'm not going to claim an adherence-to-velocity correlation on nine synthetic deals. The 90-day measure is a holdout comparison for exactly that reason."*

That sentence is worth more than any chart on the page. Volunteering the limit of your own evidence is the highest-credibility move available, and it preempts the question.

### Who opens it, and when

The dashboard isn't a thing managers are asked to visit. It's the artifact behind the existing pipeline review — the one meeting where this conversation already happens. Frame it that way and it stops being a fourth tab nobody checks.

---

## Time and sequencing

| Item | Effort | Priority |
|---|---|---|
| Exit criteria in the Record + render | ~45 min | 1 — cheapest, highest demo value |
| `action_items` table + closure tracking | ~1 hr | 2 — everything else reads from it |
| Two-stage escalation | ~30 min | 3 — small once closure exists |
| CS handoff rendering | ~1 hr | 4 — most documented pain |
| Northwind through the chain | ~30 min | 5 — the differentiation payoff |
| Static dashboard | ~90 min | 6 — mock it if time runs out |

**If the dashboard slips:** one screenshot of the layout with placeholder numbers, clearly labeled as a mock, is a completely acceptable deliverable. The assessment says not to over-index on polish, and the design is the point. What you cannot fake is the exit criteria and the closure tracking, because those are the answer to "who's enforcing this."

---

## What this changes in the pitch

The system now has four layers rather than two, and the fourth is the one the panel will push on:

1. **Capture** — the Record, accruing across calls
2. **Delivery** — Slack surfaces per consumer
3. **Prompting** — drafted email, nudge, escalation
4. **Verification** — exit criteria, closure tracking, adherence reporting

Layer 4 is the JD's language almost directly: *creates feedback loops that surface where execution can improve*. Before this, the system observed and suggested. Now it verifies.

Worth adding to the corrections log: this was a gap you identified yourself late in the build — the system prompted but nothing checked whether anything happened, which meant every action item was a suggestion. Naming a hole you found in your own design, and what you did about it, is a strong answer to "what would you change."
