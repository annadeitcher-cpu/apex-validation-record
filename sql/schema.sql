-- Apex Validation Record — prototype schema
-- Target: Supabase (Postgres 15+), standing in for Snowflake
-- Safe to re-run: drops and rebuilds everything.

drop table if exists knowledge cascade;
drop table if exists action_items cascade;
drop table if exists notifications cascade;
drop table if exists record_events cascade;
drop table if exists validation_records cascade;
drop table if exists activities cascade;
drop table if exists transcripts cascade;
drop table if exists participants cascade;
drop table if exists calls cascade;
drop table if exists opportunities cascade;
drop table if exists accounts cascade;

-- ---------------------------------------------------------------
-- Core CRM objects (stand-ins for Salesforce sync)
-- ---------------------------------------------------------------

create table accounts (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  industry text,
  employee_count int,
  region text
);

create table opportunities (
  id uuid primary key default gen_random_uuid(),
  account_id uuid references accounts(id) on delete cascade,
  name text not null,
  segment text,                          -- 'Enterprise' | 'Mid-Market'
  stage text not null,                   -- 'Discovery' | 'Technical Validation' |
                                         -- 'Commercial Negotiation' | 'Legal/Close' |
                                         -- 'Closed Won' | 'Closed Lost'
  acv numeric,
  close_date date,
  stage_entered_at timestamptz,          -- drives days-in-stage
  ae_name text,
  sc_name text,
  csm_name text,
  slack_channel_id text,
  created_at timestamptz default now()
);

-- ---------------------------------------------------------------
-- Call data (stand-ins for Gong sync)
-- ---------------------------------------------------------------

create table calls (
  id uuid primary key default gen_random_uuid(),
  opportunity_id uuid references opportunities(id) on delete cascade,
  gong_call_id text,
  call_type text,                        -- 'technical_validation' | 'follow_up' | 'commercial'
  occurred_at timestamptz not null,
  duration_minutes int
);

create table participants (
  id uuid primary key default gen_random_uuid(),
  call_id uuid references calls(id) on delete cascade,
  name text,
  title text,
  email text,
  is_internal boolean default false
);

create table transcripts (
  id uuid primary key default gen_random_uuid(),
  call_id uuid references calls(id) on delete cascade unique,
  content text not null
);

-- Activity log — what the 72h nudge reads.
-- Absence of rows here for a given opportunity is the signal.
create table activities (
  id uuid primary key default gen_random_uuid(),
  opportunity_id uuid references opportunities(id) on delete cascade,
  activity_type text,                    -- 'email' | 'call' | 'meeting'
  actor text,
  occurred_at timestamptz,
  subject text
);

-- ---------------------------------------------------------------
-- Reference content (release notes, competitor battlecards).
-- Static, not seeded from calls — the extraction chain retrieves
-- against this to ground product_relevance and competitive signals.
-- ---------------------------------------------------------------

create table knowledge (
  id uuid primary key,
  kind text not null,        -- 'release_note' | 'battlecard'
  title text not null,
  subject text,              -- release name, or competitor name
  content text not null,
  tags text[]
);

-- ---------------------------------------------------------------
-- The system's own objects
-- ---------------------------------------------------------------

-- Versioned. Accrual is the whole point: v1 from the technical
-- validation and v3 six weeks later are different objects, and the
-- diff between them is the deal's story.
create table validation_records (
  id uuid primary key default gen_random_uuid(),
  opportunity_id uuid references opportunities(id) on delete cascade,
  version int not null,
  source_call_ids uuid[],
  payload jsonb not null,
  status text not null,                  -- 'complete' | 'partial' | 'failed'
  generated_at timestamptz default now(),
  unique (opportunity_id, version)
);

-- Diff log between versions. materiality gates notification:
-- only 'material' events produce a channel post.
create table record_events (
  id uuid primary key default gen_random_uuid(),
  opportunity_id uuid references opportunities(id) on delete cascade,
  from_version int,
  to_version int,
  event_type text,                       -- 'objection_resurfaced' | 'objection_resolved'
                                         -- 'stakeholder_added' | 'champion_changed'
                                         -- 'next_step_missing' | 'competitor_introduced'
  detail jsonb,
  materiality text,                      -- 'material' | 'minor'
  created_at timestamptz default now()
);

-- Enforcement layer (docs/enforcement-layer-spec.md §2). Written alongside
-- each Record version. Dedupe across versions is semantic (owner + meaning),
-- decided by the model reasoning about the deal, not by string equality in
-- code — see scripts/write_action_items.py.
create table action_items (
  id uuid primary key default gen_random_uuid(),
  opportunity_id uuid references opportunities(id) on delete cascade,
  record_version int,
  owner_role text,                       -- 'ae' | 'sc' | 'customer'
  owner_name text,
  description text not null,
  due_date date,
  is_blocker boolean default false,
  status text default 'open',            -- 'open' | 'completed' | 'completed_unverified' | 'missed'
                                         -- completed_unverified: evidence found but only weakly
                                         -- corresponds to the item — see scripts/check_closure.py
  completed_at timestamptz,
  created_at timestamptz default now()
);

-- slack_ts is load-bearing: it's how the pinned Record gets edited
-- in place via chat.update instead of reposted.
create table notifications (
  id uuid primary key default gen_random_uuid(),
  opportunity_id uuid references opportunities(id) on delete cascade,
  surface text,                          -- 'channel_pin' | 'channel_update' | 'dm_ae'
                                         -- 'dm_sc' | 'dm_manager'
  destination text,
  slack_ts text,
  payload jsonb,
  sent_at timestamptz default now()
);

-- ---------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------

create index idx_opportunities_account on opportunities(account_id);
create index idx_opportunities_stage on opportunities(stage);
create index idx_calls_opportunity on calls(opportunity_id);
create index idx_calls_occurred on calls(occurred_at);
create index idx_participants_call on participants(call_id);
create index idx_activities_opportunity on activities(opportunity_id, occurred_at desc);
create index idx_records_opportunity on validation_records(opportunity_id, version desc);
create index idx_events_opportunity on record_events(opportunity_id, created_at desc);
create index idx_notifications_opportunity on notifications(opportunity_id, surface);
create index idx_action_items_opportunity on action_items(opportunity_id, status);
create index idx_action_items_due on action_items(due_date) where status = 'open';
create index idx_knowledge_kind on knowledge(kind);
create index idx_knowledge_tags on knowledge using gin(tags);
