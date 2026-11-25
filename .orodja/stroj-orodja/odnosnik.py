#!/usr/bin/env python3
# ODNOSNIK v1.0 @stroj-orodja ; rod : rez σ 7031 ( 25. 11. 2026 ) ⊙ ⟡ UKZ VERBATIM »ORODJA KI DEFINIRAJO ODNOS!«
# Služba : izpiše definicije odnosov ⊢ pri viru @register-odnosov ( pet vrst σ 5859 : ⊥ antinom ⌇ ⟨ni le…tudi⟩ razcep ⌇ ∅ edin ⌇ - zveza ⌇ ⊕ več-in-manj ).
# Zakoni : ⟨NE-UGIBAJ⟩ 2690 ( definicija brana pri viru vsak zagon, nikoli iz spomina ) ⌇ ⟨MERILEC-SE-MERI⟩ §52.
# Roke : odnosnik.py [ZNAK] | --samopreizkus ; ZNAK ∈ {⊥, ∅, -, ⊕, razcep} ( brez : vseh pet ).
# Izhodi : 0 ZELENA ⌇ 1 RDECA ( organ ali znak nerodni ) ⌇ 40 roka neznana.

import os, re, sys

ORGAN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "register-odnosov", "KNOWLEDGE.md")
ZNACKE = ["⊥", "∅", "⊕", "razcep", "-"]

def beri(znak=""):
    try:
        with open(ORGAN, encoding="utf-8") as t: vrstice = t.read().splitlines()
    except OSError as r:
        return None, "⟨NAPAKA=VSE-KAR-NI-BRANO⟩ " + str(r)
    najdeni = []
    for v in vrstice:
        if len(v) < 8: continue
        if znak and znak in v and any(zn in v for zn in ZNACKE):
            najdeni.append(v.strip())
        elif not znak and any(zn in v for zn in ["⊥", "∅", "⊕", "razcep"]):
            najdeni.append(v.strip())
    return najdeni, None

def samopreizkus():
    padci = []
    if not os.path.isfile(ORGAN):
        padci.append("organ register-odnosov neroden"); return padci
    v, rana = beri()
    if rana: padci.append(rana)
    if not any("⊥" in x for x in v): padci.append("antinom ⟨⊥⟩ pri viru ×0")
    if not any("∅" in x for x in v): padci.append("edin ⟨∅⟩ pri viru ×0")
    if not any("⊕" in x for x in v): padci.append("več-in-manj ⟨⊕⟩ pri viru ×0")
    return padci

def glavni():
    if "--samopreizkus" in sys.argv[1:] or len(sys.argv) == 2 and sys.argv[1] == "--samopreizkus":
        padci = samopreizkus()
        print("SAMOPREIZKUS : preizkusi 4, padci instrumenta %d" % len(padci))
        for p in padci: print("  PADC :: " + p)
        print("SEMAFOR : " + ("ZELENA" if not padci else "RDECA"))
        return 0 if not padci else 1
    if len(sys.argv) > 2:
        print("roka neznana ; roke : [ZNAK] | --samopreizkus"); return 40
    znak = sys.argv[1] if len(sys.argv) == 2 else ""
    najdeni, rana = beri(znak)
    if rana:
        print(rana); return 1
    if not najdeni:
        print("VIDNO ⭢ znak %s pri viru ×0 ; definicija ⭢ sodba ⚔ ⟡ ⊙ ⟨NE-UGIBAJ⟩ 2690" % ("prazen" if not znak else znak))
        print("SEMAFOR : RDECA"); return 1
    print("ODNOSNIK v1.0 : definicije ⊢ pri viru @register-odnosov ( σ 5859, pet vrst )")
    for v in najdeni[:12]: print("  " + v[:240])
    print("SEMAFOR : ZELENA")
    return 0

if __name__ == "__main__":
    sys.exit(glavni())
