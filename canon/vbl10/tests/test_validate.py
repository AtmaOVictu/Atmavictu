import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from canon.vbl10.validate import validate_record


TIMESTAMP = "2026-10-23T12:00:00Z"


def incident_record():
    return {
        "recordType": "incident",
        "id": "incident-1",
        "createdAt": TIMESTAMP,
        "reporter": "reporter-1",
        "claim": "A specified event was observed.",
        "status": "REPORTED",
        "evidence": [],
        "history": [
            {
                "status": "REPORTED",
                "actor": "reporter-1",
                "at": TIMESTAMP,
                "reason": "Initial report.",
                "procedure": "intake-v1",
                "evidenceRefs": [],
            }
        ],
        "limitations": ["No independent review yet."],
    }


class IncidentValidationTests(unittest.TestCase):
    def test_reported_incident_is_valid_without_claiming_confirmation(self):
        self.assertEqual(validate_record(incident_record(), Path.cwd()), [])

    def test_current_status_must_match_last_history_event(self):
        record = incident_record()
        record["status"] = "CONFIRMED"
        self.assertIn(
            "incident status must match the last history event",
            validate_record(record, Path.cwd()),
        )

    def test_transition_history_rejects_skipping_to_verified_correction(self):
        record = incident_record()
        record["status"] = "CORRECTION_VERIFIED"
        record["history"].append(
            {
                "status": "CORRECTION_VERIFIED",
                "actor": "reviewer-1",
                "at": TIMESTAMP,
                "reason": "Attempted direct transition.",
                "procedure": "review-v1",
                "evidenceRefs": [],
            }
        )
        self.assertTrue(
            any(
                "invalid incident status transition" in error
                for error in validate_record(record, Path.cwd())
            )
        )


class VerificationValidationTests(unittest.TestCase):
    def test_executor_cannot_verify_own_consequential_action(self):
        record = {
            "recordType": "verification",
            "id": "verification-1",
            "target": {"id": "action-1", "version": "1"},
            "evidenceRefs": ["evidence-1"],
            "procedure": "check-v1",
            "procedureVersion": "1",
            "result": "VERIFIED",
            "verifiedAt": TIMESTAMP,
            "executor": "agent-a",
            "verifier": "agent-a",
            "limitations": [],
        }
        self.assertIn(
            "executor cannot be the sole verifier of the same action",
            validate_record(record, Path.cwd()),
        )

    def test_unavailable_independent_review_must_not_claim_a_verifier(self):
        record = {
            "recordType": "verification",
            "id": "verification-1",
            "target": {"id": "action-1", "version": "1"},
            "evidenceRefs": ["evidence-1"],
            "procedure": "check-v1",
            "procedureVersion": "1",
            "result": "INDEPENDENT_VERIFICATION_UNAVAILABLE",
            "verifiedAt": TIMESTAMP,
            "executor": "agent-a",
            "verifier": None,
            "limitations": ["No independent verifier was available."],
        }
        self.assertEqual(validate_record(record, Path.cwd()), [])


class ReleaseValidationTests(unittest.TestCase):
    def make_release(self, root: Path, claimed_status="CANDIDATE"):
        artifact = root / "license.md"
        artifact.write_text("draft text\n", encoding="utf-8")
        register = root / "incidents.jsonl"
        register.write_text("", encoding="utf-8")
        return {
            "recordType": "release",
            "version": "10.0.0-draft.1",
            "publishedAt": TIMESTAMP,
            "predecessor": "2.6",
            "author": "author-1",
            "executor": "builder-1",
            "sourceArtifact": {
                "path": "license.md",
                "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
            },
            "tests": [],
            "registers": [
                {
                    "path": "incidents.jsonl",
                    "status": "VALID",
                    "checkedAt": TIMESTAMP,
                }
            ],
            "verification": {
                "status": "INDEPENDENT_VERIFICATION_UNAVAILABLE",
                "executor": "builder-1",
                "verifier": None,
                "evidenceRefs": [],
            },
            "limitations": ["Draft; not an active license."],
            "approval": {
                "actor": "approver-1",
                "approvedAt": TIMESTAMP,
                "decisionRef": "decision-1",
            },
            "claimedStatus": claimed_status,
        }

    def test_missing_register_fails_instead_of_becoming_an_empty_register(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = self.make_release(root)
            (root / "incidents.jsonl").unlink()
            self.assertTrue(
                any(
                    "register is missing" in error
                    for error in validate_record(record, root)
                )
            )

    def test_digest_detects_artifact_change(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = self.make_release(root)
            (root / "license.md").write_text("changed text\n", encoding="utf-8")
            self.assertIn(
                "source artifact SHA-256 digest does not match",
                validate_record(record, root),
            )

    def test_release_artifact_path_cannot_escape_manifest_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = self.make_release(root)
            record["sourceArtifact"]["path"] = "../outside.md"
            self.assertTrue(
                any(
                    "path escapes record directory" in error
                    for error in validate_record(record, root)
                )
            )

    def test_verified_release_requires_passing_tests_and_independent_review(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = self.make_release(root, claimed_status="VERIFIED")
            errors = validate_record(record, root)
            self.assertIn(
                "VERIFIED release requires at least one test result",
                errors,
            )
            self.assertIn(
                "VERIFIED release requires verified independent review",
                errors,
            )

    def test_jsonl_register_rows_are_validated(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = self.make_release(root)
            register_path = root / "incidents.jsonl"
            register_path.write_text(json.dumps({"recordType": "unknown"}) + "\n", encoding="utf-8")
            self.assertTrue(
                any(
                    "incidents.jsonl:1" in error
                    for error in validate_record(record, root)
                )
            )


if __name__ == "__main__":
    unittest.main()
