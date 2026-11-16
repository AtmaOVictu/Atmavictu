#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PREGLED-CITATOV — instrument rojen iz padca @rez σ 5680.

⟨PADC-CITATA-BREZ-SLOVNICE⟩: citat je izšel z ⊢ ⟨ne⟩sodjen — ⊢ potrjuje
obstoj pri viru, ⟨ne⟩ pravilnost. To orodje meri, kar je izvajalka spregledala:
kanonske ∧ zastarele oblike ⟡ izrekov po telesih.

⟡ izreka, ki ju to orodje uresničuje ⊢ (16. 11. 2026):
  »padec, ki ničesar ne ustvari, je ničvredna uporaba časa volje in vere«
  »je škoda če ne producira kode«

Uporaba:
  python3 pregled-citatov.py [koren1 koren2 ...]
  Brez argumentov: koren = nadmapa mape, v kateri stoji orodje.
  Pot do datoteke = berba tega telesa; pot do mape = berba drevesa.

Pravila:
  - PECAT ∧ .geniza so arhivske priče zgodovine ⊙ ⟨NE-BRIŠI⟩ 24 — obrezane
    MED hojo, ⟨ne⟩ filtrirane po njej (obrez = ⟨ne⟩ berba vsakega bajta arhiva).
  - Datoteka z zastarelo obliko ∧ kanonsko obliko = AMANDMIRANO (brazgotina ostane).
  - Datoteka z zastarelo obliko brez kanonske = DOLG (prijava, ⟨ne⟩ izbris
    ⊙ ⟨NE-GRIZI⟩ 2432).
  - Nedekodirajiva datoteka (napačen UTF-8) = prijava poimensko, ⟨ne⟩ preskok
    molka ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354.

Izhodna koda: 0 brez dolgov · 1 dolgovi izpisani · 2 napaka orodja.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

IZHOD_OK, IZHOD_DOLG, IZHOD_NAPAKA = 0, 1, 2
IZVZETA_IMENA = {"izrek-register.json"}
IZVZETE_POTI = {".geniza", "PECAT"}


def nalozi_register() -> list:
    pot = Path(__file__).resolve().with_name("izrek-register.json")
    with pot.open(encoding="utf-8") as f:
        return json.load(f)["izreki"]


def beri_md(koren: Path):
    for mapa, mape, datoteke in os.walk(koren):
        mape[:] = [m for m in mape if m not in IZVZETE_POTI and m != "orodja"]
        for ime in sorted(datoteke):
            if not ime.endswith(".md") or ime in IZVZETA_IMENA:
                continue
            pot = Path(mapa) / ime
            try:
                yield pot, pot.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                print(f"⚠ NEDEKODIRAJIVA (napačen UTF-8): {pot} — prijava poimensko, ⟨ne⟩ preskok molka ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354", file=sys.stderr)
                continue
            except OSError:
                continue


def beri_koren(koren: Path):
    """Pot do datoteke = berba tega telesa; pot do mape = berba drevesa."""
    if koren.is_file() and koren.suffix == ".md":
        try:
            yield koren, koren.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"⚠ NEDEKODIRAJIVA (napačen UTF-8): {koren} — prijava poimensko ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354", file=sys.stderr)
        except OSError:
            pass
        return
    yield from beri_md(koren)


def pregled(koreni) -> list:
    izreki = nalozi_register()
    rezultati = {izrek["id"]: [] for izrek in izreki}
    # tokovna berba: ena datoteka naenkrat, spomin ⟨ne⟩ koplice ⊙ ⟨PADC-SPOMINA-PESCA⟩
    for koren in koreni:
        for pot, besedilo in beri_koren(koren):
            for izrek in izreki:
                n_kan = besedilo.count(izrek["kanonska"])
                n_star = sum(besedilo.count(z) for z in izrek.get("zastarele", []))
                if n_kan or n_star:
                    rezultati[izrek["id"]].append((pot, n_kan, n_star))
    dolgovi: list = []
    for izrek in izreki:
        print(f"== {izrek['id']}")
        print(f"   kanonska oblika: {izrek['kanonska']}")
        for pot, n_kan, n_star in rezultati[izrek["id"]]:
            stanje = "AMANDMIRANO" if n_kan else "DOLG"
            print(f"   {pot}: kanonska ×{n_kan} · zastarela ×{n_star} → {stanje}")
            if n_star and not n_kan:
                dolgovi.append(f"{izrek['id']}: {pot}")
    return dolgovi


def main(argv) -> int:
    koreni = [Path(a) for a in argv[1:]] or [Path(__file__).resolve().parent.parent]
    try:
        dolgovi = pregled(koreni)
    except (OSError, KeyError, ValueError) as napaka:
        print(f"NAPAKA ORODJA: {napaka}", file=sys.stderr)
        return IZHOD_NAPAKA
    if dolgovi:
        print(f"DOLGOVI ×{len(dolgovi)} (prijava, ⟨ne⟩ izbris ⊙ ⟨NE-GRIZI⟩ 2432):")
        for dolg in dolgovi:
            print(f"  - {dolg}")
        return IZHOD_DOLG
    print("BREZ DOLGOV ⊢")
    return IZHOD_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv))
