#!/usr/bin/env python3
"""
Score one chain output against its hand-written ground truth.

Usage:
    python scripts/eval_score.py evals/sightline-01_ground_truth.json evals/sightline-01_chain_output.json

Ground truth files are the *_ground_truth.json companions to the human-readable
*_ground_truth.md files in evals/ — the .md explains the reasoning behind each
expectation, this script only compares against the compact .json summary of it.

Metrics, per the real metric set this repo's docs describe (build-plan.md §7):
  - objection recall: of the objections ground truth expects, how many does the
    chain output contain at all (matched by a substring in objection text)
  - objection status accuracy: of the recalled objections, how many got the
    correct status
  - stakeholder role accuracy: of the named stakeholders ground truth expects,
    how many got the correct role_inference (a name not found in chain output
    at all counts as a miss, same as a wrong role)
  - next-step presence detection: does chain output's next_step.present match
    what ground truth expects, and if a date was required, was one set
  - competitive count sanity check: within the expected min/max range
  - product relevance: if ground truth names a required release, does chain
    output's product_relevance actually contain it
  - hallucinated commitments: a crude but real check — none of the forbidden
    terms ground truth lists should appear anywhere in the chain output text

This is a minimal, honest scorer, not a sophisticated NLP eval. Status/role
matches are exact-string; objection matches are substring-based on `text` /
`resolution_note`. It will not catch every real error and will occasionally
flag a false negative on close paraphrasing — that's a known, stated limit,
not a hidden one.
"""

import json
import sys


def load(path):
    with open(path) as f:
        return json.load(f)


def score(ground_truth, chain_output):
    results = {}
    notes = []

    # Objection recall + status accuracy
    gt_objections = ground_truth.get("objections", [])
    chain_objections = chain_output.get("objections", [])
    chain_text_blob = json.dumps(chain_objections).lower()

    recalled = 0
    status_correct = 0
    for gt_obj in gt_objections:
        needle = gt_obj["text_contains"].lower()
        match = None
        for co in chain_objections:
            haystack = (co.get("text", "") + " " + (co.get("resolution_note") or "")).lower()
            if needle in haystack:
                match = co
                break
        if match:
            recalled += 1
            if match.get("status") == gt_obj["expected_status"]:
                status_correct += 1
            else:
                notes.append(
                    f"objection '{gt_obj['text_contains']}': expected status "
                    f"'{gt_obj['expected_status']}', got '{match.get('status')}'"
                )
        else:
            notes.append(f"objection '{gt_obj['text_contains']}': MISSED — not found in chain output at all")

    results["objection_recall"] = f"{recalled}/{len(gt_objections)}" if gt_objections else "n/a"
    results["objection_status_accuracy"] = f"{status_correct}/{recalled}" if recalled else "n/a"

    # Stakeholder role accuracy
    gt_stakeholders = ground_truth.get("stakeholders", [])
    chain_stakeholders = {s["name"]: s for s in chain_output.get("stakeholders", [])}
    role_correct = 0
    for gt_sh in gt_stakeholders:
        chain_sh = chain_stakeholders.get(gt_sh["name"])
        if chain_sh is None:
            notes.append(f"stakeholder '{gt_sh['name']}': MISSED — not found in chain output at all")
            continue
        if chain_sh.get("role_inference") == gt_sh["expected_role"]:
            role_correct += 1
            if "expected_confidence" in gt_sh and chain_sh.get("confidence") != gt_sh["expected_confidence"]:
                notes.append(
                    f"stakeholder '{gt_sh['name']}': role correct but confidence "
                    f"expected '{gt_sh['expected_confidence']}', got '{chain_sh.get('confidence')}'"
                )
        else:
            notes.append(
                f"stakeholder '{gt_sh['name']}': expected role '{gt_sh['expected_role']}', "
                f"got '{chain_sh.get('role_inference')}'"
            )
    results["stakeholder_role_accuracy"] = f"{role_correct}/{len(gt_stakeholders)}" if gt_stakeholders else "n/a"

    # Next-step presence detection
    gt_next = ground_truth.get("next_step", {})
    chain_next = chain_output.get("next_step", {})
    next_step_ok = chain_next.get("present") == gt_next.get("expected_present")
    if next_step_ok and gt_next.get("expected_present"):
        if "expected_owner" in gt_next and chain_next.get("owner") != gt_next["expected_owner"]:
            next_step_ok = False
            notes.append(f"next_step owner: expected '{gt_next['expected_owner']}', got '{chain_next.get('owner')}'")
        if gt_next.get("date_committed_required") and not chain_next.get("date_committed"):
            next_step_ok = False
            notes.append("next_step: ground truth requires a committed date, chain output has none")
    elif not next_step_ok:
        notes.append(
            f"next_step.present: expected {gt_next.get('expected_present')}, got {chain_next.get('present')}"
        )
    results["next_step_detection"] = "correct" if next_step_ok else "INCORRECT"

    # Competitive count sanity
    comp_count = len(chain_output.get("competitive", []))
    comp_min = ground_truth.get("competitive_min_count", 0)
    comp_max = ground_truth.get("competitive_max_count", 999)
    comp_ok = comp_min <= comp_count <= comp_max
    results["competitive_count"] = f"{comp_count} (expected {comp_min}-{comp_max}) — {'ok' if comp_ok else 'OUT OF RANGE'}"

    # Product relevance
    required_release = ground_truth.get("product_relevance_required_release")
    if required_release:
        found = any(required_release in pr.get("relevant_release", "") for pr in chain_output.get("product_relevance", []))
        results["product_relevance"] = f"required '{required_release}' — {'FOUND' if found else 'MISSING'}"
        if not found:
            notes.append(f"product_relevance: chain output never connects the need to '{required_release}'")

    # Hallucination check
    full_text = json.dumps(chain_output).lower()
    hallucinations = [t for t in ground_truth.get("hallucination_forbidden_terms", []) if t.lower() in full_text]
    results["hallucinated_commitments"] = len(hallucinations)
    if hallucinations:
        notes.append(f"HALLUCINATION: forbidden terms found in chain output: {hallucinations}")

    return results, notes


def main():
    if len(sys.argv) != 3:
        print("usage: eval_score.py <ground_truth.json> <chain_output.json>", file=sys.stderr)
        sys.exit(1)

    ground_truth = load(sys.argv[1])
    chain_output = load(sys.argv[2])
    results, notes = score(ground_truth, chain_output)

    print(f"=== {sys.argv[2]} ===")
    for k, v in results.items():
        print(f"  {k}: {v}")
    if notes:
        print("  notes:")
        for n in notes:
            print(f"    - {n}")


if __name__ == "__main__":
    main()
