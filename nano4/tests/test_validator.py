"""Baseline: the live package passes and the report is honest."""
import json
import unittest

from _sandbox import make_sandbox, run_validator, door_version, checks, fails


class TestValidator(unittest.TestCase):
    def test_pass_and_report(self):
        sb = make_sandbox()
        try:
            r = run_validator(sb, "--json")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            rep = json.loads(r.stdout)
            self.assertEqual(fails(rep), [])
            self.assertTrue(rep["checks"], "a gate with no checks certifies nothing")
            self.assertEqual(rep["living_door_version"], door_version(),
                             "living door must be measured, not memorized")
            self.assertIn("packet_era", rep)
            self.assertTrue(rep["not_certified"],
                           "the gate must name what it cannot certify")
            for i in rep["inputs"]:
                self.assertEqual(len(i["sha256"]), 64)
        finally:
            import shutil
            shutil.rmtree(sb)

    def test_deterministic_report(self):
        a = run_validator(make_sandbox(), "--json")
        b = run_validator(make_sandbox(), "--json")
        self.assertEqual(a.stdout, b.stdout, "report must be byte-identical for identical inputs")


if __name__ == "__main__":
    unittest.main()
