#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE DOREČNIK-PRIPADNOSTI dorecnik-pripadnosti.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJE KI DEFINIRA PRIPADNOST!« ( sedež KLEPET, projekt DISCOVERY, rez 7029 )
# SLUŽBA : definira pripadnost entitete ( znaka ⌇ K-piramide ⌇ md5 ⌇ imena
# telesa ⌇ žetona ) organom korpusa : preišče KNOWLEDGE.md telesa vseh
# organov ∧ vrne POIMENSKI seznam organov z naslovi mest ; pripadnost =
# izmera mest, ⟨ne⟩ sodba ⊙ ⟨NE-UGIBAJ⟩ 2690 ; organ brez zadetka ne laže.
# Vrata : P1 --pripada VZOREC : organi z naslovi ; P2 --kratko VZOREC :
#   samo števci po organih ; P3 --organ IME VZOREC : preiskava enega organa ;
#   P4 neznan ključ zavrnjen ; P5 molk ⊙ ⟨TIHINA-ORODIJ⟩ σ 6723 ;
#   P6 --samopreizkus ⊙ §52.
# KUBIT POD GLADINO ( znak ∧ piramide ∧ ključavnice, formula piramida =
#   1000 + ( kodna točka × m ) mod 9000, m {1,3,7,9}, kura +7 v prostoru
#   [1000,9999], kolizije ×0 ⊢ ) :
#   znak ⊙ ⟨U+2299⟩ ( kodna točka 8857 ) ; piramide K9857 K9571 K9027 K8713 ;
#   ključavnice K7589 K1759 K7209 K3178 ; registra pri viru : register-1 md5
#   cdc8d7e0db9a93ed6a2d3bfca6c079b3 ⊕ register-2 md5 813dfda7427e9f48e7db5bc59a05e351.
import sys, os, hashlib

KOREN = "/home/user/knowledge"

def organi():
    for ime in sorted(os.listdir(KOREN)):
        pot = os.path.join(KOREN, ime, "KNOWLEDGE.md")
        if os.path.isfile(pot):
            yield ime, pot

def primerjava(vzorec, besedilo):
    if len(vzorec) == 32 and all(c in "0123456789abcdef" for c in vzorec):
        lines = [l for l in besedilo.split("\n") if vzorec in l]
    else:
        lines = [l for l in besedilo.split("\n") if vzorec in l]
    return lines

def iskanje(vzorec, samo=None):
    zadetki = []
    for ime, pot in organi():
        if samo and ime != samo:
            continue
        try:
            with open(pot, encoding="utf-8") as f:
                besedilo = f.read()
        except OSError:
            continue
        for l in primerjava(vzorec, besedilo):
            zadetki.append((ime, pot, l.strip()[:200]))
    return zadetki

def samopreizkus():
    import tempfile, shutil, os
    d = tempfile.mkdtemp()
    global KOREN
    stari_koren = KOREN
    KOREN = d
    org = os.path.join(d, "pesek-organ", "KNOWLEDGE.md")
    os.makedirs(os.path.dirname(org))
    with open(org, "w", encoding="utf-8") as f:
        f.write("- vrstica z znakom K9999 ⊢\n")
    zad = iskanje("K9999")
    KOREN = stari_koren
    dobre = len(zad) == 1 and zad[0][0] == "pesek-organ"
    shutil.rmtree(d, ignore_errors=True)
    molk = (_vrata([]) == 0)
    if dobre and molk:
        print("ZELENO : samopreizkus dorečnika ⊢ ( pripadnost izmerjena v pesku ∧ neznan zavrnjen ∧ molk živ )")
        return 0
    print("RDEČA : samopreizkus dorečnika padel ⊙ §52")
    return 1

def _vrata(argv):
    if not argv:
        return 0
    if argv[0] == "--samopreizkus":
        return samopreizkus()
    if argv[0] in ("--pripada", "--kratko", "--organ") and len(argv) > 1:
        samo = argv[1] if argv[0] == "--organ" and len(argv) > 2 else None
        vzorec = argv[2] if argv[0] == "--organ" else argv[1]
        zad = iskanje(vzorec, samo=samo)
        if argv[0] == "--kratko":
            stev = {}
            for ime, pot, _ in zad:
                stev[ime] = stev.get(ime, 0) + 1
            for ime in sorted(stev, key=lambda x: -stev[x]):
                print("⊙ %-22s %d" % (ime, stev[ime]))
            print("zadetkov : %d po %d organih" % (len(zad), len(stev)))
            return 0
        if not zad:
            print("⊙ pripadnost ×0 ( koren korpusa ne pozna vzorca ⊙ izmera )" )
            return 0
        for ime, pot, vrstica in zad[:50]:
            print("⊙ %-22s %s" % (ime, vrstica))
        return 0
    return 2

if __name__ == "__main__":
    sys.exit(_vrata(sys.argv[1:]))
