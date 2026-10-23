#!/usr/bin/env python3
"""Validate VBL 10.0.0 draft records and release evidence."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "schemas" / "records.schema.json"
STATUSES = {
    "REPORTED",
    "UNDER_REVIEW",
    "UNVERIFIED",
    "CONFIRMED",
    "DISPUTED",
    "CORRECTION_PROPOSED",
    "CORRECTION_VERIFIED",
    "CLOSED_WITH_LIMITATIONS",
}
TRANSITIONS = {
    "REPORTED": {"UNDER_REVIEW", "UNVERIFIED", "DISPUTED"},
    "UNDER_REVIEW": {
        "UNVERIFIED",
        "CONFIRMED",
        "DISPUTED",
        "CLOSED_WITH_LIMITATIONS",
    },
    "UNVERIFIED": {"UNDER_REVIEW", "DISPUTED", "CLOSED_WITH_LIMITATIONS"},
    "CONFIRMED": {"CORRECTION_PROPOSED", "DISPUTED", "CLOSED_WITH_LIMITATIONS"},
    "DISPUTED": {"UNDER_REVIEW", "UNVERIFIED", "CONFIRMED", "CLOSED_WITH_LIMITATIONS"},
    "CORRECTION_PROPOSED": {
        "CORRECTION_VERIFIED",
        "DISPUTED",
        "CLOSED_WITH_LIMITATIONS",
    },
    "CORRECTION_VERIFIED": {"CLOSED_WITH_LIMITATIONS"},
    "CLOSED_WITH_LIMITATIONS": set(),
}


def schema_validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def schema_errors(record: dict[str, Any]) -> list[str]:
    validator = schema_validator()
    return [
        f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: "
        f"{error.message}"
        for error in sorted(
            validator.iter_errors(record),
            key=lambda item: tuple(str(part) for part in item.absolute_path),
        )
    ]


def resolve_record_path(base_dir: Path, relative_path: str) -> Path:
    path = (base_dir / relative_path).resolve()
    if not path.is_relative_to(base_dir.resolve()):
        raise ValueError(f"path escapes record directory: {relative_path}")
    return path


def semantic_errors(record: dict[str, Any], base_dir: Path) -> list[str]:
    errors: list[str] = []
    record_type = record.get("recordType")

    if record_type == "incident":
        history = record.get("history", [])
        if history and history[-1].get("status") != record.get("status"):
            errors.append("incident status must match the last history event")
        if history and history[0].get("status") != "REPORTED":
            errors.append("incident history must begin with REPORTED")
        evidence_ids = {item.get("id") for item in record.get("evidence", [])}
        for index, event in enumerate(history):
            unknown = set(event.get("evidenceRefs", [])) - evidence_ids
            if unknown:
                errors.append(
                    f"history[{index}] references unknown evidence: "
                    + ", ".join(sorted(unknown))
                )
            if index:
                previous = history[index - 1].get("status")
                current = event.get("status")
                if current not in TRANSITIONS.get(previous, set()):
                    errors.append(
                        f"invalid incident status transition at history[{index}]: "
                        f"{previous} -> {current}"
                    )

    if record_type == "verification":
        verifier = record.get("verifier")
        if verifier is not None and verifier == record.get("executor"):
            errors.append("executor cannot be the sole verifier of the same action")
        if record.get("result") == "INDEPENDENT_VERIFICATION_UNAVAILABLE" and verifier is not None:
            errors.append(
                "verifier must be null when independent verification is unavailable"
            )
        if record.get("result") == "VERIFIED" and verifier is None:
            errors.append("VERIFIED requires an independent verifier")

    if record_type == "correction":
        remedies = record.get("remedies", {})
        completed = [
            name
            for name, state in remedies.items()
            if state == "COMPLETED"
        ]
        if completed and not record.get("evidenceRefs"):
            errors.append("completed remedies require evidence references")
        if completed and not record.get("verifiedAt"):
            errors.append("completed remedies require a verifiedAt timestamp")
        if record.get("acceptanceResult") == "PASSED" and not record.get("verifiedAt"):
            errors.append("passed acceptance criteria require a verifiedAt timestamp")

    if record_type == "release":
        claimed_status = record.get("claimedStatus")
        artifact = record.get("sourceArtifact", {})
        try:
            artifact_path = resolve_record_path(base_dir, artifact.get("path", ""))
        except ValueError as error:
            errors.append(str(error))
        else:
            if not artifact_path.is_file():
                errors.append(f"source artifact is missing: {artifact.get('path', '')}")
            else:
                digest = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
                if digest != artifact.get("sha256"):
                    errors.append("source artifact SHA-256 digest does not match")

        for register in record.get("registers", []):
            try:
                path = resolve_record_path(base_dir, register.get("path", ""))
            except ValueError as error:
                errors.append(str(error))
                continue
            if not path.is_file():
                errors.append(f"register is missing: {register.get('path', '')}")
                continue
            if register.get("status") != "VALID":
                errors.append(
                    f"register is not marked VALID: {register.get('path', '')} "
                    f"({register.get('status')})"
                )
            errors.extend(validate_jsonl(path))

        if claimed_status == "VERIFIED":
            tests = record.get("tests", [])
            if not tests:
                errors.append("VERIFIED release requires at least one test result")
            for test in tests:
                if test.get("status") != "PASSED":
                    errors.append(
                        f"VERIFIED release has non-passing test: "
                        f"{test.get('id')} ({test.get('status')})"
                    )
            if not record.get("registers"):
                errors.append("VERIFIED release requires explicit register results")
            if record.get("verification", {}).get("status") != "VERIFIED":
                errors.append("VERIFIED release requires verified independent review")
            if (
                record.get("verification", {}).get("verifier")
                in {
                    record.get("author"),
                    record.get("executor"),
                    record.get("approval", {}).get("actor"),
                }
            ):
                errors.append("release verifier must be distinct from author, executor, and approver")
            if record.get("approval", {}).get("actor") in {
                record.get("author"),
                record.get("executor"),
            }:
                errors.append("release approver must be distinct from author and executor")

    return errors


def validate_record(record: Any, base_dir: Path) -> list[str]:
    if not isinstance(record, dict):
        return ["record must be a JSON object"]
    errors = schema_errors(record)
    if errors:
        return errors
    return semantic_errors(record, base_dir)


def validate_jsonl(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        return [f"cannot read register {path}: {error}"]
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            errors.append(f"{path}:{number}: blank JSONL rows are not allowed")
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            errors.append(f"{path}:{number}: invalid JSON: {error.msg}")
            continue
        row_errors = validate_record(record, path.parent)
        errors.extend(f"{path}:{number}: {message}" for message in row_errors)
    return errors


def main(arguments: list[str]) -> int:
    if len(arguments) != 1:
        print("Usage: python canon/vbl10/validate.py <record.json | register.jsonl>", file=sys.stderr)
        return 2

    path = Path(arguments[0]).resolve()
    if not path.is_file():
        print(f"Input is missing: {path}", file=sys.stderr)
        return 1

    if path.suffix.lower() == ".jsonl":
        errors = validate_jsonl(path)
    else:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            print(f"Cannot read JSON record: {error}", file=sys.stderr)
            return 1
        errors = validate_record(record, path.parent)

    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1

    print("VALID: record structure and implemented semantic checks passed.")
    print("LIMITATION: this is a draft validator, not proof of legal or ethical correctness.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
