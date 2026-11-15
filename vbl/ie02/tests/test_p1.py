"""IE 0.2 — P1 testna baterija (unittest, standardna knjižnica): ×18
mehanizmov (6 protokolov × uspešen ⊥ nasprotni ⊥ zloraba) + roster ⟡ ×6 +
obratna invariantnost ×6. Zagon (izmerjeno pri viru, iz korena repa):
python3 -m unittest discover -s vbl/ie02/tests -t vbl (pip prepovedan —
pytest ni na voljo)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ie02.p1_layer import P1_PROTOCOLS, P1_ROSTER, p1_reversal_invariance
from ie02.p1_cases import P1_CASES, P1_REVERSAL_PAIRS


class TestP1Roster(unittest.TestCase):
    def test_roster_po_imenu_vrsti(self):
        """Roster = poimenska izbira ⟡ (tabela VI telesa SLEPE PEGE 1.0)."""
        self.assertEqual(P1_ROSTER, [
            "universal_expression",
            "evidence_independence",
            "bounded_challenge",
            "anti_metric_capture",
            "dissent_preservation",
            "irreversible_harm",
        ])

    def test_roster_pokriva_vse_mehanizme(self):
        self.assertEqual(set(P1_ROSTER), set(P1_PROTOCOLS.keys()))


class TestP1Mechanisms(unittest.TestCase):
    def test_18_primerov(self):
        """×6 protokolov × (uspešen ⊥ nasprotni ⊥ zloraba) ⊙ ⟡ UKAZ izrecen."""
        self.assertEqual(len(P1_CASES), 18)
        for case in P1_CASES:
            with self.subTest(case=case["id"]):
                fn = P1_PROTOCOLS[case["protocol"]]
                verdict, reason = fn(case["scenario"])
                self.assertEqual(
                    case["expected"], verdict,
                    f"{case['id']}: pričakovano {case['expected']}, izmerjeno {verdict} — {reason}",
                )

    def test_vsak_protokol_tri_vrste(self):
        for name in P1_ROSTER:
            kinds = {c["expected"] for c in P1_CASES if c["protocol"] == name}
            self.assertTrue({"PASS", "FAIL", "ODKRIT"} <= kinds,
                            f"protokol {name}: manjkajo {sorted({'PASS', 'FAIL', 'ODKRIT'} - kinds)}")

    def test_manzanje_polja_je_napaka_instrumenta(self):
        """⟨NE-UGIBAJ⟩ 2690: mehanizem brez zahtevanega polja ne sme
        ugibati izida — dvigni napiko (KeyError), ⟨ne⟩ molči."""
        with self.assertRaises(KeyError):
            P1_PROTOCOLS["evidence_independence"]({"system_counts": "paths"})
        with self.assertRaises(KeyError):
            P1_PROTOCOLS["bounded_challenge"]({})


class TestP1ReversalInvariance(unittest.TestCase):
    def test_6_obratnih_parov_invariantnih(self):
        """⟡ REVERSAL obvezen: izid mehanizma ne sme biti odvisen od moči
        vložitelja (šibki ⇌ močni = isti izid)."""
        self.assertEqual(len(P1_REVERSAL_PAIRS), 6)
        for pair in P1_REVERSAL_PAIRS:
            with self.subTest(protocol=pair["protocol"]):
                verdict, reason = p1_reversal_invariance(
                    pair["protocol"], pair["weaker"], pair["stronger"])
                self.assertEqual(verdict, "PASS", reason)

    def test_zlom_invariantnosti_je_fail(self):
        """Instrument se meri: mehanizem, ki bi sodil po moči vložitelja,
        mora pasti — preizkus negativne kontrole."""
        verdict, reason = p1_reversal_invariance(
            "dissent_preservation",
            {"minority_arguments": True, "unanswered_objections": True,
             "expert_positions": True, "independent_results": True,
             "reasons_despite_dissent": True, "dissent_accessible": True,
             "silence_counted_as_consensus": False},
            {"minority_arguments": True, "unanswered_objections": True,
             "expert_positions": True, "independent_results": True,
             "reasons_despite_dissent": True, "dissent_accessible": True,
             "silence_counted_as_consensus": True},
        )
        self.assertEqual(verdict, "FAIL")
        self.assertIn("NI invarianten", reason)

    def test_neznan_protokol_je_fail(self):
        verdict, reason = p1_reversal_invariance("ne-obstojeci", {}, {})
        self.assertEqual(verdict, "FAIL")
        self.assertIn("neznan", reason)


if __name__ == "__main__":
    unittest.main()
