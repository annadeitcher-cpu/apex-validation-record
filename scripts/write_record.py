#!/usr/bin/env python3
"""
Validate a Validation Record payload against docs/record-contract.md and
write it to the database.

Usage:
    python scripts/write_record.py --deal Sightline --version 1 --payload /tmp/rec.json
    python scripts/write_record.py --deal Sightline --version 2 --payload /tmp/rec.json --events /tmp/events.json

Idempotent per (opportunity, version): rerunning with the same version
overwrites that row rather than duplicating it (matches production
behavior described in build-plan.md §4 — reprocessing produces the same
record version, not a duplicate).

On a malformed payload (missing keys, bad enum values, wrong types), this
writes status: "failed" for that version with the validation errors
attached, and exits non-zero. It never writes a payload under
status: "complete"/"partial" that didn't pass validation.
"""

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from db import get_connection

STATUSES = {"complete", "partial", "failed"}
ROLES = {"economic_buyer", "champion", "technical_evaluator", "blocker", "influencer", "unknown"}
CONFIDENCE = {"high", "medium", "low"}
STAKEHOLDER_STATUS = {"active", "departed", "new_this_call"}
OBJECTION_CATEGORY = {"security", "integration", "pricing", "data_residency", "performance", "procurement", "other"}
OBJECTION_STATUS = {"resolved", "open", "partially_resolved", "resurfaced"}
EVAL_STATUS = {"actively_evaluating", "incumbent", "mentioned_only"}
NEXT_STEP_OWNER = {"AE", "SC", "customer"}
SEVERITY = {"high", "medium", "low"}
EVENT_TYPES = {
    "objection_resurfaced", "objection_resolved", "stakeholder_added",
    "champion_changed", "next_step_missing", "competitor_introduced",
}
MATERIALITY = {"material", "minor"}

REQUIRED_TOP_LEVEL = {
    "record_id", "opportunity_id", "version", "source_call_ids", "generated_at",
    "status", "narrative", "stage_exit_criteria", "stakeholders", "objections",
    "integration_patterns", "success_criteria", "competitive", "product_relevance",
    "next_step", "open_risks",
}
REQUIRED_NARRATIVE_KEYS = {"whats_happened", "whats_blocking", "ae_actions", "sc_loop_close", "sc_actions"}
REQUIRED_BLOCKING_KEYS = {"blocking", "not_blocking"}
STAGE_EXIT_CRITERIA_TEXT = (
    "All technical objections resolved or accepted",
    "Economic buyer identified",
    "Integration approach agreed",
    "Next step scheduled with owner and date",
    "Success criteria captured in customer's words",
)
STAGE_EXIT_OWNER = {"AE", "SC"}


class ValidationErrors(list):
    def add(self, msg):
        self.append(msg)


def validate_payload(payload, expected_version):
    errors = ValidationErrors()

    if not isinstance(payload, dict):
        return ["payload is not a JSON object"]

    missing = REQUIRED_TOP_LEVEL - payload.keys()
    if missing:
        errors.add(f"missing top-level keys: {sorted(missing)}")
        return errors  # nothing else is safe to check

    if payload.get("status") not in STATUSES:
        errors.add(f"status must be one of {sorted(STATUSES)}, got {payload.get('status')!r}")

    if payload.get("version") != expected_version:
        errors.add(f"payload version {payload.get('version')!r} does not match --version {expected_version}")

    narrative = payload.get("narrative")
    if not isinstance(narrative, dict):
        errors.add("narrative must be an object")
    else:
        missing_narrative = REQUIRED_NARRATIVE_KEYS - narrative.keys()
        if missing_narrative:
            errors.add(f"narrative missing keys: {sorted(missing_narrative)}")
        if not isinstance(narrative.get("whats_happened"), str) or not narrative["whats_happened"].strip():
            errors.add("narrative.whats_happened must be a non-empty string")
        blocking = narrative.get("whats_blocking")
        if not isinstance(blocking, dict) or (REQUIRED_BLOCKING_KEYS - blocking.keys()):
            errors.add("narrative.whats_blocking must be an object with 'blocking' and 'not_blocking' lists")
        if not isinstance(narrative.get("ae_actions"), list) or not narrative["ae_actions"]:
            errors.add("narrative.ae_actions must be a non-empty list")
        if not isinstance(narrative.get("sc_loop_close"), str) or not narrative["sc_loop_close"].strip():
            errors.add("narrative.sc_loop_close must be a non-empty string")
        if not isinstance(narrative.get("sc_actions"), list):
            errors.add("narrative.sc_actions must be a list (may be empty)")

    criteria = payload.get("stage_exit_criteria")
    if not isinstance(criteria, list) or len(criteria) != 5:
        errors.add("stage_exit_criteria must be a list of exactly 5 entries")
    else:
        seen_text = []
        for i, c in enumerate(criteria):
            p = f"stage_exit_criteria[{i}]"
            if not isinstance(c, dict):
                errors.add(f"{p} is not an object")
                continue
            seen_text.append(c.get("criterion"))
            if c.get("owner") not in STAGE_EXIT_OWNER:
                errors.add(f"{p}.owner must be one of {sorted(STAGE_EXIT_OWNER)}, got {c.get('owner')!r}")
            if not isinstance(c.get("met"), bool):
                errors.add(f"{p}.met must be a boolean")
            elif c["met"] is False and not (isinstance(c.get("reason"), str) and c["reason"].strip()):
                errors.add(f"{p}.reason is required (non-empty string) when met is false")
            elif c["met"] is True and c.get("reason") is not None:
                errors.add(f"{p}.reason must be null when met is true")
        if tuple(seen_text) != STAGE_EXIT_CRITERIA_TEXT:
            errors.add(
                "stage_exit_criteria must be exactly these five criteria, in this order: "
                + json.dumps(STAGE_EXIT_CRITERIA_TEXT)
            )

    if not isinstance(payload.get("source_call_ids"), list) or not payload["source_call_ids"]:
        errors.add("source_call_ids must be a non-empty list")

    for i, s in enumerate(payload.get("stakeholders", [])):
        p = f"stakeholders[{i}]"
        if not isinstance(s, dict):
            errors.add(f"{p} is not an object")
            continue
        if not s.get("name"):
            errors.add(f"{p}.name is required")
        if s.get("role_inference") not in ROLES:
            errors.add(f"{p}.role_inference invalid: {s.get('role_inference')!r}")
        if s.get("confidence") not in CONFIDENCE:
            errors.add(f"{p}.confidence invalid: {s.get('confidence')!r}")
        if s.get("status") not in STAKEHOLDER_STATUS:
            errors.add(f"{p}.status invalid: {s.get('status')!r}")
        if not s.get("evidence"):
            errors.add(f"{p}.evidence (verbatim quote) is required")
        if not s.get("first_seen_call") or not s.get("last_seen_call"):
            errors.add(f"{p} missing first_seen_call/last_seen_call")

    for i, o in enumerate(payload.get("objections", [])):
        p = f"objections[{i}]"
        if not isinstance(o, dict):
            errors.add(f"{p} is not an object")
            continue
        if not o.get("objection_id"):
            errors.add(f"{p}.objection_id is required")
        if not o.get("text"):
            errors.add(f"{p}.text is required")
        if o.get("category") not in OBJECTION_CATEGORY:
            errors.add(f"{p}.category invalid: {o.get('category')!r}")
        if o.get("status") not in OBJECTION_STATUS:
            errors.add(f"{p}.status invalid: {o.get('status')!r}")
        if o.get("confidence") not in CONFIDENCE:
            errors.add(f"{p}.confidence invalid: {o.get('confidence')!r}")
        if not o.get("raised_call") or not o.get("last_updated_call"):
            errors.add(f"{p} missing raised_call/last_updated_call")

    for i, ip in enumerate(payload.get("integration_patterns", [])):
        p = f"integration_patterns[{i}]"
        if not isinstance(ip, dict):
            errors.add(f"{p} is not an object")
            continue
        if not isinstance(ip.get("agreed"), bool):
            errors.add(f"{p}.agreed must be a boolean")
        if ip.get("confidence") not in CONFIDENCE:
            errors.add(f"{p}.confidence invalid: {ip.get('confidence')!r}")
        if not isinstance(ip.get("systems"), list):
            errors.add(f"{p}.systems must be a list")

    for i, sc in enumerate(payload.get("success_criteria", [])):
        p = f"success_criteria[{i}]"
        if not isinstance(sc, dict) or not sc.get("customer_words") or not sc.get("interpreted"):
            errors.add(f"{p} missing customer_words/interpreted")

    for i, c in enumerate(payload.get("competitive", [])):
        p = f"competitive[{i}]"
        if not isinstance(c, dict):
            errors.add(f"{p} is not an object")
            continue
        if not c.get("vendor"):
            errors.add(f"{p}.vendor is required")
        if not c.get("context_verbatim"):
            errors.add(f"{p}.context_verbatim (verbatim quote) is required")
        if c.get("evaluation_status") not in EVAL_STATUS:
            errors.add(f"{p}.evaluation_status invalid: {c.get('evaluation_status')!r}")
        if c.get("confidence") not in CONFIDENCE:
            errors.add(f"{p}.confidence invalid: {c.get('confidence')!r}")
        if not c.get("rationale"):
            errors.add(f"{p}.rationale is required — why this was classified this way")
        if "suggested_positioning" not in c:
            errors.add(f"{p}.suggested_positioning is required (empty string if ungrounded)")

    for i, pr in enumerate(payload.get("product_relevance", [])):
        p = f"product_relevance[{i}]"
        if not isinstance(pr, dict) or not pr.get("need_stated") or not pr.get("relevant_release"):
            errors.add(f"{p} missing need_stated/relevant_release")
        elif pr.get("confidence") not in CONFIDENCE:
            errors.add(f"{p}.confidence invalid: {pr.get('confidence')!r}")

    ns = payload.get("next_step")
    if not isinstance(ns, dict) or "present" not in ns:
        errors.add("next_step must be an object with a 'present' key")
    else:
        if ns["present"] is True:
            if not ns.get("described"):
                errors.add("next_step.described is required when present is true")
            if ns.get("owner") not in NEXT_STEP_OWNER:
                errors.add(f"next_step.owner invalid: {ns.get('owner')!r}")
            if ns.get("confidence") not in CONFIDENCE:
                errors.add(f"next_step.confidence invalid: {ns.get('confidence')!r}")
        elif ns["present"] is False:
            for field in ("described", "owner", "date_committed", "confidence"):
                if ns.get(field) is not None:
                    errors.add(f"next_step.{field} must be null when present is false")
        else:
            errors.add("next_step.present must be a boolean")

    for i, r in enumerate(payload.get("open_risks", [])):
        p = f"open_risks[{i}]"
        if not isinstance(r, dict) or not r.get("risk"):
            errors.add(f"{p}.risk is required")
        else:
            if r.get("severity") not in SEVERITY:
                errors.add(f"{p}.severity invalid: {r.get('severity')!r}")
            if r.get("confidence") not in CONFIDENCE:
                errors.add(f"{p}.confidence invalid: {r.get('confidence')!r}")

    return errors


def validate_events(events):
    errors = ValidationErrors()
    if not isinstance(events, list):
        return ["events file must contain a JSON list"]
    for i, e in enumerate(events):
        p = f"events[{i}]"
        if not isinstance(e, dict):
            errors.add(f"{p} is not an object")
            continue
        if e.get("event_type") not in EVENT_TYPES:
            errors.add(f"{p}.event_type invalid: {e.get('event_type')!r}")
        if e.get("materiality") not in MATERIALITY:
            errors.add(f"{p}.materiality invalid: {e.get('materiality')!r}")
        if "detail" not in e:
            errors.add(f"{p}.detail is required (may be {{}})")
    return errors


def fetch_opportunity(cur, deal_name):
    cur.execute(
        "select id, name from opportunities where name ilike %s order by name",
        (f"%{deal_name}%",),
    )
    rows = cur.fetchall()
    if not rows:
        raise RuntimeError(f"no opportunity matching --deal {deal_name!r}")
    if len(rows) > 1:
        names = ", ".join(r[1] for r in rows)
        raise RuntimeError(f"--deal {deal_name!r} is ambiguous, matches: {names}")
    return rows[0]


def existing_record_id(cur, opportunity_id, version):
    cur.execute(
        "select id from validation_records where opportunity_id = %s and version = %s",
        (opportunity_id, version),
    )
    row = cur.fetchone()
    return row[0] if row else uuid.uuid4()


def write_row(cur, record_id, opportunity_id, version, source_call_ids, payload, status):
    cur.execute(
        """
        insert into validation_records (id, opportunity_id, version, source_call_ids, payload, status, generated_at)
        values (%s, %s, %s, %s, %s, %s, now())
        on conflict (opportunity_id, version) do update set
            source_call_ids = excluded.source_call_ids,
            payload = excluded.payload,
            status = excluded.status,
            generated_at = now()
        """,
        (record_id, opportunity_id, version, source_call_ids, json.dumps(payload), status),
    )


def write_events(cur, opportunity_id, from_version, to_version, events):
    cur.execute(
        "delete from record_events where opportunity_id = %s and to_version = %s",
        (opportunity_id, to_version),
    )
    for e in events:
        cur.execute(
            """
            insert into record_events (opportunity_id, from_version, to_version, event_type, detail, materiality)
            values (%s, %s, %s, %s, %s, %s)
            """,
            (opportunity_id, from_version, to_version, e["event_type"], json.dumps(e["detail"]), e["materiality"]),
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deal", required=True)
    parser.add_argument("--version", type=int, required=True)
    parser.add_argument("--payload", required=True, dest="payload_path")
    parser.add_argument("--events", dest="events_path")
    args = parser.parse_args()

    payload = json.loads(Path(args.payload_path).read_text())
    events = json.loads(Path(args.events_path).read_text()) if args.events_path else []

    with get_connection() as conn:
        with conn.cursor() as cur:
            opportunity_id, opportunity_name = fetch_opportunity(cur, args.deal)
            record_id = existing_record_id(cur, opportunity_id, args.version)

            # record_id, opportunity_id, and generated_at are assigned here,
            # not produced by pass 3 (see prompts/03_merge.md) — inject them
            # before validating so the contract's full shape is checked
            # against the object that actually gets stored.
            if isinstance(payload, dict):
                payload.setdefault("record_id", str(record_id))
                payload.setdefault("opportunity_id", str(opportunity_id))
                payload.setdefault("generated_at", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

            payload_errors = validate_payload(payload, args.version)
            event_errors = validate_events(events)
            all_errors = list(payload_errors) + list(event_errors)

            if all_errors:
                raw_call_ids = payload.get("source_call_ids", []) if isinstance(payload, dict) else []
                safe_call_uuids = []
                for c in raw_call_ids:
                    try:
                        safe_call_uuids.append(uuid.UUID(c))
                    except (ValueError, TypeError, AttributeError):
                        pass  # malformed call id — exactly the kind of thing that got us here
                error_payload = {
                    "record_id": str(record_id),
                    "opportunity_id": str(opportunity_id),
                    "version": args.version,
                    "source_call_ids": [str(c) for c in safe_call_uuids],
                    "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "status": "failed",
                    "validation_errors": all_errors,
                }
                write_row(
                    cur, record_id, opportunity_id, args.version,
                    safe_call_uuids, error_payload, "failed",
                )
                conn.commit()
                print(f"FAILED validation for {opportunity_name} v{args.version}:", file=sys.stderr)
                for err in all_errors:
                    print(f"  - {err}", file=sys.stderr)
                print("\nWrote status: failed. No events were written.", file=sys.stderr)
                sys.exit(1)

            payload["record_id"] = str(record_id)
            payload["opportunity_id"] = str(opportunity_id)

            source_call_uuids = [uuid.UUID(c) for c in payload["source_call_ids"]]
            write_row(
                cur, record_id, opportunity_id, args.version,
                source_call_uuids, payload, payload["status"],
            )
            from_version = args.version - 1 if args.version > 1 else None
            write_events(cur, opportunity_id, from_version, args.version, events)
            conn.commit()

    print(f"Wrote {opportunity_name} v{args.version} — status: {payload['status']}, {len(events)} event(s).")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"FAIL  {e}", file=sys.stderr)
        sys.exit(1)
