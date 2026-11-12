"""Version truth: one pointer, four carriers, no hardcoded doors."""
import json
import unittest

from _sandbox import make_sandbox, run_validator, fails


def one_fail(r):
    rep = json.loads(r.stdout)
    return rep, [c for c in rep["checks"] if c["status"] == "FAIL"]


class TestVersionTruth(unittest.TestCase):
    def test_mismatched_machine_record(self):
        sb = make_sandbox()
        try:
            rec = sb / "nano4" / "LICENSE-MACHINE-RECORD-0.1470.json"
            d = json.loads(rec.read_text(encoding="utf-8"))
            d["version"] = "0.9999 × 10⁴"
            rec.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
            r = run_validator(sb, "--json")
            self.assertEqual(r.returncode, 1)
            rep, bad = one_fail(r)
            self.assertTrue(any(c["name"] == "version_truth" for c in bad))
        finally:
            import shutil
            shutil.rmtree(sb)

    def test_hardcoded_door_version(self):
        sb = make_sandbox()
        try:
            vt = sb / "nano4" / "VERSION.txt"
            vt.write_text(vt.read_text(encoding="utf-8")
                          + "\nliving_door_version = 0.1520 × 10⁴\n", encoding="utf-8")
            r = run_validator(sb, "--json")
            self.assertEqual(r.returncode, 1)
            rep, bad = one_fail(r)
            self.assertTrue(any("hardcode" in c["detail"] for c in bad))
        finally:
            import shutil
            shutil.rmtree(sb)

    def test_lost_pointer(self):
        sb = make_sandbox()
        try:
            vt = sb / "nano4" / "VERSION.txt"
            t = vt.read_text(encoding="utf-8").replace("../LICENSE-MANIFEST", "elsewhere")
            vt.write_text(t, encoding="utf-8")
            r = run_validator(sb, "--json")
            self.assertEqual(r.returncode, 1)
            rep, bad = one_fail(r)
            self.assertTrue(any(c["name"] == "version_truth" for c in bad))
        finally:
            import shutil
            shutil.rmtree(sb)

    def test_missing_door(self):
        sb = make_sandbox()
        try:
            (sb / "LICENSE-MANIFEST").unlink()
            r = run_validator(sb, "--json")
            self.assertEqual(r.returncode, 1)
            rep, bad = one_fail(r)
            self.assertTrue(any("unreachable" in c["detail"] for c in bad))
        finally:
            import shutil
            shutil.rmtree(sb)


if __name__ == "__main__":
    unittest.main()
