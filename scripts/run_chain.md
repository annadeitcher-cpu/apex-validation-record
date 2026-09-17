# Extraction chain — manual runbook

No orchestrator. This is a manual sequence: the model (whoever/whatever is running this — Claude Code, or you by hand on demo day) reads each prompt file and does the extraction; the Python scripts only move data in and out of Supabase. Per call:

1. **Get context.**
   ```
   python scripts/get_call_context.py --deal meridian --call 1
   ```
   Prints the call metadata, the participant roster, the prior Validation Record payload (if any — none for call 1), and the full transcript.

2. **Pass 1 — extract.** Follow `prompts/01_extract.md` against the transcript and roster from step 1. Produces candidates (stakeholders, objections, integration patterns, success criteria, competitive mentions, product-relevance candidates, a next-step candidate, open-risk candidates), each with verbatim evidence.

3. **Retrieve knowledge.** Pull the vendor names and customer-stated needs out of the candidates from step 2, then:
   ```
   python scripts/query_knowledge.py --terms "Tracewell,consent reconciliation"
   ```
   Comma-separated, one call, all terms from this call at once. Prints matching battlecards/release notes, or `(no matching knowledge rows)` if nothing matched — that's a valid, expected result, not an error.

4. **Pass 2 — consolidate.** Follow `prompts/02_consolidate.md` against step 2's candidates and step 3's retrieved rows. Produces this call's consolidated extraction: deduped, categorized, classified, roles inferred, competitive/product content grounded only in what step 3 actually retrieved.

5. **Pass 3 — merge.** Follow `prompts/03_merge.md` against step 4's consolidated extraction and the prior Validation Record from step 1. Produces the new version's full payload plus a list of change events, per `docs/record-contract.md`.

6. **Write it.** Save the payload from step 5 to a JSON file (minus `change_events`) and, if there are any, the events array to a second file:
   ```
   python scripts/write_record.py --deal meridian --version 1 --payload /tmp/rec.json --events /tmp/events.json
   ```
   Validates against the contract, writes `validation_records` and `record_events`. On a malformed payload it writes `status: failed` for that version and exits non-zero — fix the payload and rerun rather than pushing through. Idempotent per (opportunity, version): rerunning the same version overwrites it, not duplicates it.

## Posting to Slack

7. **Get render context.**
   ```
   python scripts/get_render_context.py --deal meridian --version 3
   ```
   Prints the written Record payload, this version's change events, and deal metadata (account, ACV, AE/SC first names, days in stage, and how that compares to the Apex-wide average) — everything pass 4 needs, computed once, deterministically, rather than guessed at write time.

8. **Pass 4 — render.** Follow `prompts/04_render.md` against step 7's output. Write the finished pinned-message prose to a file. If step 7 showed material events for this version (and it isn't version 1), also write the short "what changed" prose to a second file, per the same prompt's rules.

9. **Post it.**
   ```
   python scripts/post_to_slack.py --deal meridian --version 3 --message-file /tmp/v3.txt --changed-file /tmp/v3_changed.txt
   ```
   `--changed-file` is optional — omit it if step 8 didn't produce one. Posts exactly the text it's given; no field value from the Record is templated into a message anywhere in this script. v1 creates the pinned object (canvas, falling back to a pinned message on this workspace); v2+ update it in place. If a "what changed" message already exists for this version, it's updated in place too, not duplicated.

## Multi-call deals

Repeat steps 1–6 per call, in order, starting from call 1. Step 1 on call 2 will print call 1's just-written record as the prior version automatically — that's the accrual working. Don't skip a call or run them out of order; pass 3's merge logic depends on the prior version actually being the immediately preceding call.

## If something fails

`write_record.py` exiting non-zero with `status: failed` written means: stop, read the validation errors it printed, fix the payload (usually a missed field or a bad enum value — check it against `docs/record-contract.md`), and rerun `write_record.py` on the corrected file. Don't re-run passes 1–3 unless the problem is actually in the extraction, not just the JSON shape.
