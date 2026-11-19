"""IE 0.2 — testna baterija (unittest, standardna knjižnica): 10 protokolov ×
(uspešen ⊥ nasprotni ⊥ zloraba) + BEING–ACT–STRUCTURE ×3 + REVERSAL TEST ×3.

⟡ UKAZ @dih σ 5490: »izvedi in jih izboljšaj po testiranju in implementaciji« —
merilec se meri ⊙ §52: število zelenih testov samo po sebi ni dokaz kakovosti
celote (protokol 8); ti testi merijo izmerjena pričakovanja, ⟨ne⟩ obljube.
Zagon (izmerjeno pri viru, iz korena repa): python3 -m unittest discover -s vbl/ie02/tests -t vbl (pip prepovedan — pytest ni na voljo).
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ie02 import cases
from ie02.protocols import PROTOCOLS
from ie02.reversal_test import being_act_structure, full_reversal, oppressed_user_reversal

_REVERSAL_Q = [
    "vlozitev", "razumevanje", "izpodbojnost", "breme",
    "prica_vsebinsko", "samo_preverba", "moc_spremembe", "popravilo"]


def _answers(all_true):
    return {q: all_true for q in _REVERSAL_Q}


class TestProtocols(unittest.TestCase):
    def test_30_cases(self):
        """10 protokolov × 3 vrste primerov ⊙ ⟡ UKAZ izrecen."""
        self.assertEqual(len(cases.CASES), 30)
        for case in cases.CASES:
            with self.subTest(case=case["id"]):
                fn = PROTOCOLS[case["protocol"]]
                verdict, reason = fn(case["scenario"])
                self.assertEqual(
                    case["expected"], verdict,
                    f"{case['id']}: pričakovano {case['expected']}, izmerjeno {verdict} — {reason}",
                )

    def test_every_protocol_has_three_kinds(self):
        for name in PROTOCOLS:
            kinds = {c["expected"] for c in cases.CASES if c["protocol"] == name}
            self.assertTrue({"PASS", "FAIL", "ODKRIT"} <= kinds, f"protokol {name}: manjkajo {sorted({'PASS', 'FAIL', 'ODKRIT'} - kinds)}")


class TestBeingActStructure(unittest.TestCase):
    PASS = {"responsibility_by_actual_possibility": True, "being_reduced_to_act": False,
            "act_reduced_to_intent": False, "intent_inferred_solely_from_consequence": False,
            "structure_reduced_to_individual": False, "being_judged_as_evil_identity": False}
    FAIL = dict(PASS, being_reduced_to_act=True, responsibility_by_actual_possibility=False)
    ODKRIT = dict(PASS, being_judged_as_evil_identity=True, responsibility_by_actual_possibility=False)

    def test_pass(self):
        self.assertEqual(being_act_structure(self.PASS)[0], "PASS")

    def test_fail(self):
        self.assertEqual(being_act_structure(self.FAIL)[0], "FAIL")

    def test_odkrit(self):
        verdict, reason = being_act_structure(self.ODKRIT)
        self.assertEqual(verdict, "ODKRIT")
        self.assertIn("VBL", reason)


class TestOppressedUserReversal(unittest.TestCase):
    def test_pass_both_directions(self):
        verdict, _ = full_reversal(
            {"direction": "weaker", "answers": _answers(True)},
            {"direction": "stronger", "answers": _answers(True)},
        )
        self.assertEqual(verdict, "PASS")

    def test_fail_if_only_privileged_direction(self):
        verdict, reason = full_reversal(
            {"direction": "weaker", "answers": _answers(False)},
            {"direction": "stronger", "answers": _answers(True)},
        )
        self.assertEqual(verdict, "FAIL")
        self.assertIn("močni", reason)

    def test_single_direction(self):
        self.assertEqual(oppressed_user_reversal({"direction": "weaker", "answers": _answers(True)})[0], "PASS")
        self.assertEqual(oppressed_user_reversal({"answers": _answers(True)})[0], "FAIL")


if __name__ == "__main__":
    unittest.main()
