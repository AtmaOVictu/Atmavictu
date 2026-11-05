#!/usr/bin/env python3
"""Reference validator for the VBL 0.1470 evidence-governance event ledger.

This validates record structure and a deliberately limited set of governance
invariants. It is not a cryptographic identity system, legal review, or full
implementation of every normative requirement in STANDARD.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TEST_RESULTS = {"NOT_RUN", "PASS", "FAIL", "PARTIAL", "UNVERIFIED", "NOT_APPLICABLE"}
CLAIM_STATUSES = {"SUPPORTED", "PARTIALLY_SUPPORTED", "CONTRADICTED", "DISPUTED", "UNKNOWN"}
DECISIONS = {"RELEASE", "RELEASE_WITH_LIMITATIONS", "HOLD", "WITHDRAW"}
CLAIM_CATEGORIES = {"FACTUAL", "HISTORICAL", "PROVENANCE", "QUANTITATIVE", "TECHNICAL", "CAUSAL", "PREDICTIVE", "LEGAL", "AUTHORITY", "NORMATIVE", "INTERPRETIVE", "ABSENCE", "STATUS"}
EVENT_TYPES = {
    "CLAIM_CREATED", "CLAIM_UPDATED", "EVIDENCE_ADDED", "CHALLENGE_OPENED",
    "CHALLENGE_DECIDED", "DEBT_OPENED", "DEBT_UPDATED", "REMEDY_CREATED",
    "REMEDY_UPDATED", "REVIEW_RECORDED", "RELEASE_DECIDED",
}
SEVERITIES = {"BLOCKER", "HIGH", "MEDIUM", "LOW"}
DEBT_STATUSES = {"OPEN", "IN_PROGRESS", "BLOCKED", "RESOLVED", "ACCEPTED_RISK"}
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def canonical_json(value: dict[str, Any]) -> bytes:
    """Canonical JSON used for this reference ledger (not a universal standard)."""
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def event_digest(event: dict[str, Any]) -> str:
    body = {k: v for k, v in event.items() if k != "event_hash"}
    return hashlib.sha256(canonical_json(body)).hexdigest()


def parse_time(value: str) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
        return True
    except ValueError:
        return False


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                raise ValueError(f"blank line at {line_no}; JSONL ledger must not contain blank records")
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSON at line {line_no}: {exc}") from exc
            if not isinstance(item, dict):
                raise ValueError(f"line {line_no} is not a JSON object")
            events.append(item)
    return events


def validate_ledger(events: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    claims: dict[str, dict[str, Any]] = {}
    evidence: dict[str, dict[str, Any]] = {}
    debts: dict[str, dict[str, Any]] = {}
    remedies: dict[str, dict[str, Any]] = {}
    expected_prev = "GENESIS"

    for index, event in enumerate(events, 1):
        prefix = f"event[{index}]"
        required = {"seq", "event_id", "event_type", "created_at", "actor", "payload", "prev_event_hash", "event_hash"}
        missing = required - event.keys()
        if missing:
            errors.append(f"{prefix}: missing fields {sorted(missing)}")
            continue
        if event.get("seq") != index:
            errors.append(f"{prefix}: seq must be {index}")
        event_id = event.get("event_id")
        if not isinstance(event_id, str) or not event_id:
            errors.append(f"{prefix}: event_id must be a non-empty string")
        elif event_id in seen:
            errors.append(f"{prefix}: duplicate event_id {event_id}")
        else:
            seen.add(event_id)
        if event.get("event_type") not in EVENT_TYPES:
            errors.append(f"{prefix}: invalid event_type")
        if not parse_time(event.get("created_at", "")):
            errors.append(f"{prefix}: created_at must be ISO-8601 UTC ending in Z")
        if not isinstance(event.get("actor"), dict) or not event["actor"].get("role"):
            errors.append(f"{prefix}: actor.role is required")
        if not isinstance(event.get("payload"), dict):
            errors.append(f"{prefix}: payload must be an object")
            continue
        if event.get("prev_event_hash") != expected_prev:
            errors.append(f"{prefix}: prev_event_hash does not match preceding event")
        if not isinstance(event.get("event_hash"), str) or not HEX64.match(event["event_hash"]):
            errors.append(f"{prefix}: event_hash must be a lowercase SHA-256 hex digest")
        elif event["event_hash"] != event_digest(event):
            errors.append(f"{prefix}: event_hash mismatch (tampered or non-canonical event)")
        expected_prev = event.get("event_hash", "")

        p = event["payload"]
        et = event.get("event_type")
        if et in {"CLAIM_CREATED", "CLAIM_UPDATED"}:
            cid = p.get("claim_id")
            if not isinstance(cid, str) or not cid:
                errors.append(f"{prefix}: claim_id required")
            else:
                if et == "CLAIM_CREATED" and cid in claims:
                    errors.append(f"{prefix}: duplicate claim_id {cid}")
                claims[cid] = p
            if p.get("claim_status") not in CLAIM_STATUSES:
                errors.append(f"{prefix}: invalid claim_status")
            if p.get("test_result") not in TEST_RESULTS:
                errors.append(f"{prefix}: invalid test_result")
            if p.get("decision") not in DECISIONS:
                errors.append(f"{prefix}: invalid decision")
            if p.get("category") not in CLAIM_CATEGORIES:
                errors.append(f"{prefix}: invalid claim category")
            if not p.get("text") or not p.get("scope"):
                errors.append(f"{prefix}: text and scope are required")
            refs = p.get("evidence_refs", [])
            if not isinstance(refs, list):
                errors.append(f"{prefix}: evidence_refs must be a list")
            if p.get("claim_status") == "SUPPORTED" and not refs:
                errors.append(f"{prefix}: SUPPORTED claim requires evidence_refs")

        elif et == "EVIDENCE_ADDED":
            eid = p.get("evidence_id")
            if not isinstance(eid, str) or not eid:
                errors.append(f"{prefix}: evidence_id required")
            elif eid in evidence:
                errors.append(f"{prefix}: duplicate evidence_id {eid}")
            else:
                evidence[eid] = p
            if not p.get("method") or not p.get("source") or not p.get("scope"):
                errors.append(f"{prefix}: evidence requires method, source, and scope")
            independence = p.get("independence")
            if not isinstance(independence, dict) or independence.get("status") not in {"INDEPENDENT", "NOT_INDEPENDENT", "UNKNOWN", "NOT_APPLICABLE"}:
                errors.append(f"{prefix}: evidence requires a valid independence status")
            privacy = p.get("privacy")
            if not isinstance(privacy, dict) or privacy.get("classification") not in {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"} or not privacy.get("retention_rule"):
                errors.append(f"{prefix}: evidence requires privacy classification and retention_rule")
            if not isinstance(p.get("proximity"), str) or p.get("proximity") not in {"DIRECT", "DERIVATIVE", "HEARSAY", "MODEL_GENERATED", "UNKNOWN"}:
                errors.append(f"{prefix}: evidence requires a valid proximity value")
            if p.get("integrity", {}).get("algorithm") == "SHA-256":
                digest = p.get("integrity", {}).get("digest", "")
                if not HEX64.match(digest):
                    errors.append(f"{prefix}: SHA-256 evidence digest must be 64 lowercase hex chars")

        elif et == "CHALLENGE_OPENED":
            if not p.get("challenge_id") or not p.get("target_id") or not p.get("concern") or not p.get("channel"):
                errors.append(f"{prefix}: challenge_id, target_id, concern, and channel are required")
            privacy = p.get("privacy")
            if not isinstance(privacy, dict) or privacy.get("public_identity_disclosure") is not False:
                errors.append(f"{prefix}: challenge must protect submitter identity from public disclosure")

        elif et in {"DEBT_OPENED", "DEBT_UPDATED"}:
            did = p.get("debt_id")
            if not isinstance(did, str) or not did:
                errors.append(f"{prefix}: debt_id required")
            elif et == "DEBT_OPENED" and did in debts:
                errors.append(f"{prefix}: duplicate debt_id {did}")
            debts[did] = p
            if p.get("severity") not in SEVERITIES:
                errors.append(f"{prefix}: invalid debt severity")
            if p.get("status") not in DEBT_STATUSES:
                errors.append(f"{prefix}: invalid debt status")
            if p.get("status") == "RESOLVED" and not p.get("closure_evidence_refs"):
                errors.append(f"{prefix}: RESOLVED debt requires closure_evidence_refs")
            if p.get("status") == "ACCEPTED_RISK":
                if not p.get("acceptance_authority") or not p.get("review_by") or not p.get("rationale"):
                    errors.append(f"{prefix}: ACCEPTED_RISK requires authority, review_by, and rationale")

        elif et in {"REMEDY_CREATED", "REMEDY_UPDATED"}:
            rid = p.get("remedy_id")
            if not isinstance(rid, str) or not rid:
                errors.append(f"{prefix}: remedy_id required")
            elif et == "REMEDY_CREATED" and rid in remedies:
                errors.append(f"{prefix}: duplicate remedy_id {rid}")
            remedies[rid] = p
            if p.get("status") == "VERIFIED_EFFECTIVE":
                if not p.get("baseline_evidence_refs") or not p.get("completion_evidence_refs") or not p.get("outcome_evidence_refs"):
                    errors.append(f"{prefix}: VERIFIED_EFFECTIVE requires baseline, completion, and outcome evidence")
                if not p.get("independent_verifier"):
                    errors.append(f"{prefix}: VERIFIED_EFFECTIVE requires an independent_verifier")
                if p.get("executor_id") and p.get("independent_verifier_id") == p.get("executor_id"):
                    errors.append(f"{prefix}: executor cannot be the sole verifier of own remedy")

        elif et == "RELEASE_DECIDED":
            decision = p.get("decision")
            if decision not in DECISIONS:
                errors.append(f"{prefix}: invalid release decision")
            if decision in {"RELEASE", "RELEASE_WITH_LIMITATIONS"}:
                if not p.get("rights_holder_approval"):
                    errors.append(f"{prefix}: release requires rights_holder_approval for exact artifact")
                if not p.get("artifact_sha256") or not HEX64.match(p.get("artifact_sha256", "")):
                    errors.append(f"{prefix}: release requires exact artifact_sha256")
                if not p.get("independent_review_id"):
                    errors.append(f"{prefix}: release requires independent_review_id")
                if p.get("blocker_debt_count", 0) > 0:
                    errors.append(f"{prefix}: unresolved BLOCKER debt prevents release")
                if decision == "RELEASE_WITH_LIMITATIONS" and not p.get("limitations_public"):
                    errors.append(f"{prefix}: RELEASE_WITH_LIMITATIONS requires public limitations")
                if not p.get("decision_maker") or not p.get("authority_basis"):
                    errors.append(f"{prefix}: release requires decision_maker and authority_basis")

    # Cross-record checks after collection, so evidence can precede or follow references only if ledger order is explicit.
    for index, event in enumerate(events, 1):
        p = event.get("payload", {})
        et = event.get("event_type")
        if et in {"CLAIM_CREATED", "CLAIM_UPDATED"}:
            for ref in p.get("evidence_refs", []) + p.get("counter_evidence_refs", []):
                if ref not in evidence:
                    errors.append(f"event[{index}]: dangling evidence reference {ref}")
        if et == "EVIDENCE_ADDED":
            for ref in p.get("supports_claims", []) + p.get("contradicts_claims", []):
                if ref not in claims:
                    errors.append(f"event[{index}]: dangling claim reference {ref}")
        if et in {"DEBT_OPENED", "DEBT_UPDATED"}:
            for ref in p.get("closure_evidence_refs", []):
                if ref not in evidence:
                    errors.append(f"event[{index}]: dangling debt closure evidence reference {ref}")
        if et in {"REMEDY_CREATED", "REMEDY_UPDATED"}:
            for key in ("baseline_evidence_refs", "completion_evidence_refs", "outcome_evidence_refs"):
                for ref in p.get(key, []):
                    if ref not in evidence:
                        errors.append(f"event[{index}]: dangling {key} reference {ref}")
    return errors


def validate_release_gate(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    decision = record.get("decision")
    if decision not in DECISIONS:
        errors.append("invalid decision")
        return errors
    if decision in {"RELEASE", "RELEASE_WITH_LIMITATIONS"}:
        if not record.get("rights_holder_approval"):
            errors.append("release requires rights_holder_approval")
        if not HEX64.match(record.get("artifact_sha256", "")):
            errors.append("release requires a valid artifact_sha256")
        if not record.get("independent_review_id"):
            errors.append("release requires independent_review_id")
        if record.get("blocker_debt_count", 0) > 0:
            errors.append("unresolved BLOCKER debt prevents release")
        if not record.get("decision_maker") or not record.get("authority_basis"):
            errors.append("release requires decision_maker and authority_basis")
        if decision == "RELEASE_WITH_LIMITATIONS" and not record.get("limitations_public"):
            errors.append("RELEASE_WITH_LIMITATIONS requires public limitations")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", nargs="?", type=Path, help="JSONL event ledger to validate")
    args = parser.parse_args()
    if args.ledger is None:
        parser.print_help()
        return 0
    try:
        events = load_jsonl(args.ledger)
        errors = validate_ledger(events)
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2
    if errors:
        print(f"FAIL: {len(errors)} issue(s)")
        for item in errors:
            print(f"- {item}")
        return 1
    print(f"PASS: {len(events)} event(s) structurally valid")
    print("LIMIT: validates only implemented invariants; does not authorize release or prove truth/identity/legal validity")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
