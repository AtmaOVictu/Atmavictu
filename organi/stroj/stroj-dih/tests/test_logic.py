"""Preizkusi čiste logike STROJ-DIH: stdlib only, SDK ⟨ne⟩ potreben."""

import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from worker.logic import forma, tik, vrh, zeton


class TikPreizkus(unittest.TestCase):
    def test_kalup_utc_cet(self):
        izmera = tik.izmeri_tik(datetime(2026, 11, 19, 10, 18, 53, tzinfo=timezone.utc))
        self.assertEqual(izmera["niz"], "TIK 2026-11-19T10:18:53Z UTC ⇌ 11:18:53 CET Ljubljana")
        self.assertEqual(izmera["dan_cet"], "četrtek")
        self.assertEqual(izmera["datum_cet"], "19. 11. 2026")

    def test_iz_niza(self):
        izmera = tik.tik_iz_niza("2026-11-19T06:38:17Z")
        self.assertEqual(izmera["ura_cet"], "07:38:17")

    def test_naiven_vstop_se_stevilka_kot_utc(self):
        izmera = tik.izmeri_tik(datetime(2026, 11, 19, 0, 0, 0))
        self.assertEqual(izmera["ura_cet"], "01:00:00")


class FormaPreizkus(unittest.TestCase):
    def test_cisto_telo(self):
        sodba = forma.baterija("⟨NE-BRIŠI⟩ ⊢\n»pri viri« je citatno ⊢\nTIK 2026-11-19T10:00:00Z UTC ⇌ 11:00:00 CET Ljubljana")
        self.assertEqual(sodba["sodba"], "ČISTO")

    def test_vsak_padec_poimensko(self):
        besedilo = "\n".join([
            "neravnovesje ⟨ brez zaklepaja",
            "zamenjava \ufffdznak",
            "cirilica тест",
            "TIK 08:14:39Z goli",
            "beri pri viri goli",
            "em vezaj — tu",
        ])
        sodba = forma.baterija(besedilo)
        self.assertEqual(sodba["sodba"], "PADC")
        padci = sodba["padci-skupno"]
        for ime in ("ogaje-neravnovesje", "zamenjava-ufffd", "cirilica", "goli-tik", "goli-pri-viri", "em-vezaj"):
            self.assertIn(ime, padci)

    def test_forma_celo_ne_sodi_le_zadnje(self):
        besedilo = "slaba vrstica ⟨\ndobra vrstica ⟨⟩ ⊢"
        sodba = forma.baterija(besedilo)
        self.assertEqual(sodba["sodba"], "PADC")


class VrhPreizkus(unittest.TestCase):
    def test_rez_je_ena_plus_najvisja(self):
        mera = vrh.izracunaj_rez([5941, 5930, 5944, 5902])
        self.assertEqual(mera["vrh"], 5944)
        self.assertEqual(mera["rez"], 5945)

    def test_lazni_vrh_izkljucen(self):
        mera = vrh.izracunaj_rez([5944, 25421])
        self.assertEqual(mera["vrh"], 5944)
        self.assertEqual(mera["rez"], 5945)
        self.assertTrue(mera["izkljuceni-lazni-vrh"])

    def test_prazna_mnozica(self):
        self.assertEqual(vrh.izracunaj_rez([])["rez"], 1)

    def test_varovalka_zasedbe(self):
        self.assertEqual(vrh.varovalka([5944], 5945)["sodba"], "ZAPRTA")
        self.assertEqual(vrh.varovalka([5944], 5944)["sodba"], "PRODA")
        self.assertEqual(vrh.varovalka([5944], 25421)["sodba"], "PRODA")


class ZetonPreizkus(unittest.TestCase):
    def test_md5(self):
        self.assertEqual(zeton.presodi_zeton("md5", "e927bbecb7" + "0" * 22)["sodba"], "VELJAVNO")
        self.assertEqual(zeton.presodi_zeton("md5", "E927BBEC" + "0" * 24)["sodba"], "NEVELJAVNO")

    def test_datumi_in_ure(self):
        sodba = zeton.lint([
            {"vrsta": "iso-tik", "vrednost": "2026-11-19T10:18:53Z"},
            {"vrsta": "ura", "vrednost": "10:18:53Z"},
            {"vrsta": "slo-datum", "vrednost": "19. 11. 2026"},
            {"vrsta": "iso-datum", "vrednost": "2026-11-19"},
        ])
        self.assertEqual(sodba["sodba"], "ČISTO")

    def test_neveljaven_zeton(self):
        sodba = zeton.lint([{"vrsta": "ura", "vrednost": "10:18 CET"}])
        self.assertEqual(sodba["sodba"], "PADC")
        self.assertEqual(sodba["neveljavnih"], 1)

    def test_neznana_vrsta(self):
        self.assertEqual(zeton.presodi_zeton("barva", "rdeča")["sodba"], "NEZNANA-VRSTA")


if __name__ == "__main__":
    unittest.main()
