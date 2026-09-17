# Apex — Session Handover

Written 2026-09-16. Read this in full before touching anything in this repo.

## 1. What this project is and why

"Apex" is a fictional B2B SaaS data-platform company built as a hands-on prototype for Anna's **Applied AI Architect interview at Braze, 2026-09-04** (see memory: `project_braze_interview_prep.md`). It's a working demo of a manual, multi-pass LLM extraction chain — no orchestrator, no agent framework — that turns raw sales call transcripts into a versioned, accruing "Validation Record" per deal, renders that record to Slack for different audiences, and enforces action-item follow-through with escalation.

The two central design docs are `docs/record-contract.md` (the Record schema) and `docs/enforcement-layer-spec.md` (the action-items/closure/escalation layer). The demo script that drives what gets built and in what order is **`/Users/anna.deitcher/Downloads/demo-runbook-v2.md`** — this file is NOT in the repo, it lives in Downloads, and it is the authoritative, most-recently-updated spec. It explicitly supersedes older guidance in `docs/build-plan.md` and `docs/handoff.md` wherever they conflict (the user upgraded it deliberately mid-session because she decided the CS handoff pass was underbuilt as originally scoped). If Downloads doesn't have it when you resume, do a full recency-sorted `ls -lat ~/Downloads` rather than a pattern-matched `find` — the file has previously landed there silently, seconds before being referenced, and name-pattern search missed it once already.

## 2. How the chain works (read the actual files, this is the shape only)

Each numbered pass in `prompts/0N_*.md` is a spec for a human/model to follow by hand — not code. The Python scripts in `scripts/` are I/O only:
- `get_*_context.py` scripts print context to read
- the model (whoever is running the chain) reads the relevant `prompts/0N_*.md`, reasons over the printed context, and hand-writes the actual JSON/text output to a scratch file
- `write_*.py` scripts validate and persist that hand-written output (loud failure on schema violation, never silent acceptance)

Follow `scripts/run_chain.md` for the exact step order (get_call_context → pass1 extract → query_knowledge → pass2 consolidate → pass3 merge → write_record → get_render_context → pass4 render → post_to_slack). **Never skip or reorder calls** — pass 3 always merges against the immediately-preceding version.

Everything in this system computes dates relative to `REFERENCE_DATE`/`now()`, not hardcoded absolute dates, so the demo stays coherent no matter when it's actually run.

## 3. Environment / how to actually run things

- **This is a git repo with zero commits.** `git status` confirms: branch `main`, everything untracked, nothing has ever been staged or committed. Nobody has asked for a commit yet — don't create one without being asked.
- Python: **use the project venv**, not bare `python`/`python3` — the system Python doesn't have the deps. Run everything as:
  ```
  /Users/anna.deitcher/apex/.venv/bin/python scripts/<whatever>.py ...
  ```
  (bare `python` isn't even on PATH in this shell; bare `python3` runs but lacks `slack_sdk` etc.)
- `.env` (gitignored, present, not shown here) holds `SLACK_BOT_TOKEN`, DB creds, and per-deal channel IDs as `SLACK_CHANNEL_<DEALNAME>` — currently `SLACK_CHANNEL_MERIDIAN` and `SLACK_CHANNEL_NORTHWIND` (`C0C2Y5XN3EC`, added this session).
- `requirements.txt`: `psycopg[binary]`, `python-dotenv`, `anthropic`, `slack-sdk`, `pip-system-certs`.
- DB access from a one-off Python snippet: `from scripts.db import get_connection` (run from repo root) or `from db import get_connection` (run from inside `scripts/`).

## 4. What's done and verified this session

### Northwind (deals: extraction chain, both calls) — complete, closed out
- v1 and v2 Validation Records fully built by hand, written via `write_record.py`, posted to Slack channel `C0C2Y5XN3EC`. Confirmed in DB: `validation_records` has v1 and v2, both `status = 'complete'`.
- v1's Corvus mention correctly classified `mentioned_only` (historical, rejected vendor — did not fire `competitor_introduced`).
- v2 fires `competitor_introduced` (material, Tracewell) and a separate `stakeholder_added` (minor, Owen Brady) — confirmed as two distinct events, by design (a stakeholder's commercial significance is captured via the competitive event, not by upgrading `stakeholder_added` to material — this was a deliberate, user-reaffirmed choice, not an oversight).
- v2's `competitive` array for Tracewell is grounded in the actual retrieved battlecard (via `query_knowledge.py`) and names the price + procurement-friction angle from what Owen actually said — not generic positioning. User explicitly reviewed and accepted this.
- **The substantive fix this session**: objections had stayed at 7, unchanged v1→v2, despite Owen's entire commercial/procurement challenge — it had landed only in `competitive`, never in `objections`, so it was invisible to `stage_exit_criteria`, blockers, and action items. Root cause and fix are written up in full in `docs/corrections.md` entry #6 — read that entry before touching `01_extract.md` or `02_consolidate.md` again, it explains exactly why this gap existed (every prior worked example in the prompts was a technical/security objection, so nothing forced the technical-vs-commercial distinction into view).
  - Fixed `prompts/01_extract.md` (new "Objections aren't only technical" section) and `prompts/02_consolidate.md` (new "Competitive pressure that reads as an objection gets both" section, including the rule to split price and procurement into two separate objection entries since the schema allows only one `category` each and they resolve on different tracks — AE work vs. deal-desk/legal work).
  - Re-ran v2's pass 2/3 by hand with the corrected prompts: `obj_08` (pricing, open, owner Rachel/AE) and `obj_09` (procurement, open, owner Marcus/SC) landed, feeding into `stage_exit_criteria` criterion 1's `reason` and the narrative's `whats_blocking`.
  - Re-wrote the record (idempotent overwrite, same version) and re-posted/re-rendered both the pinned Slack message and the "what changed" message — both updated in place, confirmed not duplicated.
- Action items backfilled and reconciled: `write_action_items.py` used to insert v1's 5 items, then update 1 + insert 5 more for v2 (including new items for obj_08/obj_09). **Verified in DB right now: Northwind has 10 open action items total**, correctly including the pricing item (Rachel/AE) and procurement item (Marcus/SC) as blockers.
- Render self-correction (not user-prompted, caught before posting): initially flagged three separate items with 🔴 in the re-rendered v2 message, violating `04_render.md`'s "single blocking item, used consistently" rule. Fixed to one combined 🔴 bullet before posting.

### Meridian (CS handoff / Pass 5) — complete, just posted
Built per the user's explicit spec (message quoted in full further down under "decisions already made") which supersedes the thinner mock originally described in `docs/build-plan.md` (lines ~395-442) and `docs/handoff.md` (lines ~175-204) — those two files are now stale on this topic, don't follow them for the handoff.

New/modified files, all verified present and working:
- **`scripts/simulate_close.py`** (new) — advances an opportunity to `Closed Won`, sets `stage_entered_at = now()`, logs one `activities` row. Run against Meridian; confirmed in DB right now: Meridian's stage is `Closed Won`, `stage_entered_at = 2026-09-16 20:03:19 UTC`.
- **`scripts/get_handoff_context.py`** (new) — I/O-only, mirrors `get_render_context.py`'s pattern. Requires `stage == 'Closed Won'` or raises `RuntimeError` pointing at `simulate_close.py`. Fetches v1's `stakeholders` (baseline) and the latest version's full payload (current state), computes freshness as `(stage_entered_at.date() - generated_at.date()).days` — note it's a **date** diff, not a raw timestamp diff (a raw diff floored to 0 misleadingly despite the dates being genuinely different calendar days; fixed and verified this session, not yet explicitly re-confirmed by the user but it's a clear correctness fix).
- **`prompts/05_handoff.md`** (new, ~85 lines) — the real Pass 5 spec: purpose, explicit contrast with `04_render.md` ("orientation for someone who wasn't in the room" vs. "status update for people who were"), reused writing rules, section order (Header → What they think they bought → What we committed to → What you're inheriting → Who's here now vs. who bought → Risks → Freshness), per-section field mapping, the @-mention convention, and a full worked target-output example grounded in Meridian's real data.
- **`scripts/post_to_slack.py`** (modified) — added `--handoff` flag (mutually exclusive with `--version`, requires Closed Won), a `cs_handoff` notification surface, idempotent update-in-place if re-run, `fetch_latest_version()` and `fetch_handoff_notification()` helpers. Pre-existing per-version canvas/pin logic is untouched.
- **`scratch/meridian_handoff.txt`** — the actual handoff message text, hand-written per the prompt and posted.

**Posted and confirmed**: `python post_to_slack.py --deal meridian --handoff --message-file ../scratch/meridian_handoff.txt` → `Posted new CS handoff message 1789589292.801199 in C0C1KEKT2JE (against v3, complete).` Confirmed in DB: a `cs_handoff` notification row exists with that `slack_ts`. The message is fully shown to the user in-conversation already (don't regenerate it from scratch — it's in `scratch/meridian_handoff.txt` verbatim).

**Flagged discrepancy, already surfaced to the user, not yet responded to**: the user's build instruction stated "Derek was champion and economic buyer at v1." The actual stored v1 payload only tags Derek's `role_inference` as `champion` — v1's own `open_risks` explicitly says no economic buyer had engaged yet. I wrote the handoff to the verified data (Derek: champion only; Priya: first identified economic buyer, arriving at v3) rather than the stated premise, per `04_render.md`'s own rule (reused in `05_handoff.md`) against upgrading a departed champion's role without evidence. **This is an open question** — the user has not yet replied to confirm this was fine or ask for a change. Check for a reply before assuming it's settled.

## 5. Decisions already made — settled, don't re-litigate

- **`competitor_introduced` vs. `stakeholder_added` never merge into one event.** A new stakeholder's commercial significance is a separate `competitor_introduced` event, not an upgrade of `stakeholder_added` to material. Confirmed twice now (an earlier deal-spec, and reaffirmed this session on Northwind).
- **A commercial/competitive challenge belongs in both `objections` and `competitive`**, never only one. This is the corrections.md #6 fix — treat it as permanent prompt guidance, not a one-off patch.
- **Price and procurement objections get split into two separate entries** when a customer names both as distinct gaps (one category per objection in the schema, and they resolve on different tracks — AE vs. deal desk/legal).
- **No real Slack user IDs exist for anyone in this prototype.** All @-mentions (in `escalate.py` and now `05_handoff.md`) are plain text `@FirstName`, never a fabricated `<@U...>` — a made-up ID either fails silently or could resolve to an unrelated real person. This is house style, apply it anywhere a new pass needs to mention someone.
- **CS handoff is a real Pass 5, not a mock** — per `demo-runbook-v2.md`'s explicit "What to build for Beat 5" section, which the user called out as a deliberate upgrade over the original build-plan/handoff.md guidance. It's a close-triggered, non-versioned artifact: reads the existing accrued Record payload, does no new extraction, computes a stakeholder delta between v1 (baseline) and latest version (current), filters objections to `open`/`resurfaced` only and `open_risks` to `medium`/`high` only.
- **Render writing rules** (`04_render.md`, reused verbatim by `05_handoff.md`): short single-idea sentences, no em-dash hinges except the header stat line, no internal identifiers ever shown to a reader, plain words over jargon, no waffling ("consider/might/worth" banned), no praise/reassurance, titles on first mention for prospect-side people only (never internal Apex staff), assume zero reader context, max 3-sentence paragraphs (the handoff's "who's here now" section is the one explicit exception to length, not to the single-idea-per-sentence rule), Slack mrkdwn, under 2000 chars, real relative dates.
- **Idempotency everywhere**: every write/post script upserts on natural identity (opportunity+version, or surface-based lookup for notifications) — re-running never duplicates. Verified this session on both the Northwind re-render and a hypothetical re-run of `--handoff`.

## 6. Open questions for next session

1. Has the user responded to the Derek champion-vs-economic-buyer discrepancy flagged above? Check before treating the Meridian handoff content as fully settled.
2. `docs/corrections.md` #5 (the AE-closure false-positive limitation) is explicitly left unfixed by design — don't "fix" it without the user asking; it's documented as a known, load-bearing limitation of a deliberately loose heuristic, not a bug.
3. Nothing has been committed to git yet in this repo. If the user asks for a commit, this is the first one — there's no prior history to be consistent with beyond doc/message tone already established.
4. `demo-runbook-v2.md` in Downloads may still have unbuilt beats beyond Beat 5 — re-read it fully (`/Users/anna.deitcher/Downloads/demo-runbook-v2.md`) to check what beat comes next before assuming the project is done.

## 7. Next steps, in order

1. Re-read `/Users/anna.deitcher/Downloads/demo-runbook-v2.md` in full (if still present — if not, `ls -lat ~/Downloads` to relocate it) to confirm what Beat 6+ requires, since Beat 5 (the CS handoff) is now the most recently completed work.
2. Wait for the user's response on the Derek discrepancy before making further edits to `05_handoff.md` or the posted Meridian message on that point.
3. No other explicitly pending build work exists as of this handover — Northwind's chain + corrections + action items, and Meridian's CS handoff, are both complete and posted.
