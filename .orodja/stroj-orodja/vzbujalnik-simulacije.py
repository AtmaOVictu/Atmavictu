#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE VZBUJALNIK-SIMULACIJE vzbujalnik-simulacije.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJA KI STIMULIRAJO SIMULACIJO!« ( sedež KLEPET, projekt DISCOVERY, rez 7024 )
# SLUŽBA : STIMULIRA simulacijo s številkami : čez cel register padcev ×3
# ponovitve poganja posnemovalnika ∧ zdravilnika, izmeri pokritost ( vsak padec
# ustvarjen ∧ vsak ozdravljen ) ∧ izpiše izmero ; večkrat na več načinov ⊙
# sestra veckrat-verifikator ( rez 6710 ).
# Vrata : P1 --stimuliraj ( cel register ×3 ) ; P2 --padec ⟨IME⟩ ( en stimulus ) ;
#   P3 --samopreizkus ⊙ §52 ( pokritost 100 % ∧ izmera podvojena preverba ).
# KUBIT POD GLADINO ⊙ ⟨ZAKON ORODIL TRI VRATA⟩ rez 6949 : formula piramid =
#   1000 + ( točka desetiško · m mod 9000 ), m ∈ {1, 3, 7, 9}, kura ob
#   zasedenem +7 ; znak tega telesa : pulz ⟳ ⟨U+27F3⟩, piramide kocke
#   K2227 K4681 K9589 K3043, ključavnice K7222 K1864 K9859 K3403, kure ×0 ⊢
#   ( izmere proti 496 piramidam registrav ∧ 72 K-vrednostim teles pri viru ) ;
#   zapečena registra pri viru se izmerita ob samopreizkusu.
# c 0.2026 × 10 na 4 ; ⟡ Luka Pintarič ∧ izvajalka Mera ; dvoje rok 2432 ; merjeno, ne ugibano.

import hashlib
import importlib.util
import os
import sys

ŽIG = "vzbujalnik-simulacije.py v1.0 @stroj-orodja"
KOREN = os.environ.get("KOREN", "/home/user/knowledge")
DOM = os.path.dirname(os.path.abspath(__file__))
REG1 = os.path.join(KOREN, "posebaj", "register-1", "KNOWLEDGE.md")
REG2 = os.path.join(KOREN, "posebaj", "register-2", "KNOWLEDGE.md")
REG_MD5 = ("cdc8d7e0db9a93ed6a2d3bfca6c079b3", "813dfda7427e9f48e7db5bc59a05e351")
PONOVITVE = 3


def _naloži(ime):
    pot = os.path.join(DOM, ime + ".py")
    spec = importlib.util.spec_from_file_location(ime.replace("-", "_"), pot)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def stimuliraj(ime_padca=None, ponovitve=PONOVITVE):
    """Vrne izmero : vrstice ( ime ⌇ ponovitev ⌇ ustvarjeno ⌇ ozdravljeneno ) ; preorderjevanje ⟨ne⟩ ugibanja."""
    pn = _naloži("posnemovalnik-napake")
    zd = _naloži("zdravilnik-simulacije")
    imena = [ime_padca] if ime_padca else sorted(pn.PADCI)
    vr = []
    for ime in imena:
        if ime not in pn.PADCI:
            raise ValueError("NEZNAN PADC : %s ⭢ --popis pri posnemovalniku" % ime)
        ust = ozd = 0
        for _ in range(ponovitve):
            telo = pn.ustvari(ime)
            if pn.napaka_prisotna(telo, ime):
                ust += 1
            po, _spor = zd.zdravi(telo, ime)
            if not pn.napaka_prisotna(po, ime):
                ozd += 1
        vr.append((ime, ponovitve, ust, ozd))
    return vr


def izmera(vr):
    skupaj = sum(r[2] for r in vr)
    pok = sum(r[3] for r in vr)
    return skupaj, pok


def _md5(pot):
    h = hashlib.md5()
    with open(pot, "rb") as f:
        for kos in iter(lambda: f.read(8192), b""):
            h.update(kos)
    return h.hexdigest()


def samopreizkus():
    padci = 0
    vr = stimuliraj()
    sk, pk = izmera(vr)
    cilj = len(vr) * PONOVITVE
    if sk != cilj or pk != cilj:
        padci += 1
        print("RDEČO : pokritost %d/%d ustvarjenih ⌇ %d/%d ozdravljenih" % (sk, cilj, pk, cilj))
    vr2 = stimuliraj()
    sk2, pk2 = izmera(vr2)
    if (sk, pk) != (sk2, pk2):
        padci += 1
        print("RDEČO : izmera se podvaja : (%d,%d) ⌇ (%d,%d) : stimulus ni ponovljiv" % (sk, pk, sk2, pk2))
    try:
        stimuliraj("NEZNAN-PADC")
        padci += 1
        print("RDEČO : neznan padec sprejet v stimulacijo")
    except ValueError:
        pass
    if os.path.isfile(REG1) and os.path.isfile(REG2):
        if (_md5(REG1), _md5(REG2)) != REG_MD5:
            padci += 1
            print("RDEČO : registra pri viru odstopata")
    if padci == 0:
        print("ZELENO : samopreizkus vzbujalnika ⊢ ( pokritost %d/%d ∧ podvojena izmera ista ∧ neznan zavrnjen )" % (sk, cilj))
    else:
        print("RDEČO : samopreizkus vzbujalnika : padlov %d" % padci)
    return padci == 0


def main(argv):
    if "--samopreizkus" in argv:
        return 0 if samopreizkus() else 2
    ime = None
    if "--padec" in argv:
        i = argv.index("--padec")
        if i + 1 < len(argv):
            ime = argv[i + 1]
    try:
        vr = stimuliraj(ime)
    except ValueError as e:
        print("⚠ %s" % e)
        return 1
    print(ŽIG)
    for ime, pon, ust, ozd in vr:
        print("STIMULUS ⟨%s⟩ ×%d : ustvarjeno %d ⊢ ⌇ ozdravljeneno %d ⊢" % (ime, pon, ust, ozd))
    sk, pk = izmera(vr)
    print("IZMERA : %d stimulusov, pokritost %d/%d ⊢ ⊙ ⟨VEČKRAT-PREVERJENO⟩" % (sk, pk, sk))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
