"""Candidate gate: one home, fail-closed, honest emptiness."""
import json
import unittest

from _sandbox import make_sandbox, run_validator, fails


def candidate_fails(r):
    rep = json.loads(r.stdout)
    return [c for c in rep["checks"]
            if c["name"] == "candidate_gate" and c["status"] == "FAIL"]


class TestCandidateGate(unittest.TestCase):
    def test_empty_candidate_is_honest(self):
        sb = make_sandbox()
        try:
            r = run_validator(sb, "--json")
            self.assertEqual(r.returncode, 0, r.stdout)
            rep = json.loads(r.stdout)
            na = [c for c in rep["checks"]
                  if c["name"] == "candidate_gate" and c["status"] == "NOT_APPLICABLE"]
            self.assertTrue(na, "an empty candidate must read NOT_APPLICABLE, not PASS")
        finally:
            import shutil
            shutil.rmtree(sb)

    def test_orphan_candidate(self):
        sb = make_sandbox()
        try:
            (sb / "nano4" / "candidate" / "LICENSE-draft.txt").write_text(
                "orphan", encoding="utf-8")
            r = run_validator(sb, "--json")
            self.assertEqual(r.returncode, 1)
            self.assertTrue(any("orphan" in c["detail"] for c in candidate_fails(r)))
        finally:
            import shutil
            shutil.rmtree(sb)

    def test_unsafe_path_in_register(self):
        sb = make_sandbox()
        try:
            cand = sb / "nano4" / "candidate"
            (cand / "LICENSE-draft.txt").write_text("x", encoding="utf-8")
            (cand / "PACKAGE-MANIFEST.json").write_text(json.dumps({
                "status": "CANDIDATE",
                "files": [{"path": "../../outside.txt", "sha256": "0" * 64}],
            }), encoding="utf-8")
            r = run_validator(sb, "--json")
            self.assertEqual(r.returncode, 1)
            self.assertTrue(any("unsafe" in c["detail"] for c in candidate_fails(r)))
        finally:
            import shutil
            shutil.rmtree(sb)

    def test_stale_hash(self):
        sb = make_sandbox()
        try:
            import hashlib
            cand = sb / "nano4" / "candidate"
            body = cand / "LICENSE-draft.txt"
            body.write_text("snov", encoding="utf-8")
            (cand / "PACKAGE-MANIFEST.json").write_text(json.dumps({
                "status": "CANDIDATE",
                "files": [{"path": "LICENSE-draft.txt",
                           "sha256": hashlib.sha256(b"other").hexdigest()}],
            }), encoding="utf-8")
            r = run_validator(sb, "--json")
            self.assertEqual(r.returncode, 1)
            self.assertTrue(any("stale hash" in c["detail"] for c in candidate_fails(r)))
        finally:
            import shutil
            shutil.rmtree(sb)

    def test_malformed_register(self):
        sb = make_sandbox()
        try:
            cand = sb / "nano4" / "candidate"
            (cand / "PACKAGE-MANIFEST.json").write_text("{not json", encoding="utf-8")
            r = run_validator(sb, "--json")
            self.assertEqual(r.returncode, 1)
            self.assertTrue(any("malformed" in c["detail"] for c in candidate_fails(r)))
        finally:
            import shutil
            shutil.rmtree(sb)


if __name__ == "__main__":
    unittest.main()
