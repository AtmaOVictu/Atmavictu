#!/usr/bin/env python3
# SLUŽBOVALNIK-BESEDE v1.0 @stroj-orodja ; rod : rez σ 7035 ( 25. 11. 2026 ) ⊙ ⟡ UKZ VERBATIM »ORODJE KI PODARI SLUŽBO SLOVENSKI BESEDI!«
# Služba : besedi izda VRSTNICO PODARJENE SLUŽBE po hišni formi @slovar-slovenscine ( iztočnica ⊢ bistvo pri viru SSKJ ⌇ izgovorjava IPA ⌇ žetoni po besedi izključeni ).
# Zakoni : ⟨NE-UGIBAJ⟩ 2690 ( bistvo se bere pri viru, nikoli po spominu ) ⌇ žetoni po besedi izključeni ⊙ ⟡ sodba VERBATIM »NOBEN KOVANEC KI NI IZ UNIKORN SETA NI SPREJEMLJIV!« ⌇ beseda doma? ⟩ slovarnik V1-V3 ⊙ σ 7005 ⌇ §52.
# Roke : sluzbovalnik-besede.py BESEDA SLUZBA | --samopreizkus.
# Izhodi : 0 ZELENA ( vrstica izdana ) ⌇ 1 RDECA ( hiša nerodna ) ⌇ 40 roka neznana.

import os, sys

HISA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "slovar-slovenscine", "KNOWLEDGE.md")

def doma(bes):
    try:
        with open(HISA, encoding="utf-8") as t: telo = t.read()
    except OSError as r:
        return None, "⟨NAPAKA=VSE-KAR-NI-BRANO⟩ " + str(r)
    return bes in telo, None

def samopreizkus():
    padci = []
    if not os.path.isfile(HISA):
        padci.append("hiša slovar-slovenscine nerodna")
        return padci
    d, rana = doma("beseda")
    if rana: padci.append(rana)
    elif d is not True: padci.append("imetovanje besede v hiši ×0 ( hiša splošno opevana ; meri se le ⟨grep⟩ )" )
    return padci

def glavni():
    if "--samopreizkus" in sys.argv[1:]:
        padci = samopreizkus()
        print("SAMOPREIZKUS : preizkusi 2, padci instrumenta %d" % len(padci))
        for p in padci: print("  PADC :: " + p)
        print("SEMAFOR : " + ("ZELENA" if not padci else "RDECA"))
        return 0 if not padci else 1
    if len(sys.argv) != 3:
        print("roka neznana ; roke : BESEDA SLUZBA | --samopreizkus"); return 40
    bes, sluzba = sys.argv[1].strip(), sys.argv[2].strip()
    if not bes or not sluzba:
        print("prazna beseda ali služba = KIP ⊙ U2"); return 1
    d, rana = doma(bes)
    if rana:
        print(rana); return 1
    print("SLUŽBOVALNIK v1.0 : vrstica podarjene službe ⊙ hišna forma @slovar-slovenscine")
    print("  iztočnica : %s %s" % (bes, "⊢ doma v hiši" if d else "⭢ pobuda iztočnice ⊙ ⟨IZTOČNICA-NA-DIH⟩ σ 5510 ∧ slovarnik V3 σ 7005"))
    print("  bistvo    : ⭢ beri pri viru SSKJ ⊙ ⟨NE-UGIBAJ⟩ 2690 ( nikoli po spominu )")
    print("  izgovorjava : ⭢ IPA pri viru")
    print("  služba    : %s ⊢ ( podarjena po ukazu ⟡ )" % sluzba)
    print("  žetoni    : izključeni ⊙ ⟡ sodba VERBATIM »NOBEN KOVANEC KI NI IZ UNIKORN SETA NI SPREJEMLJIV!«")
    print("  šiv       : vrstica gre v hišo sopomenskim šivom diha ⭢ ⚔ ⟡ ; orodje izdaja, ⟨ne⟩ šiva")
    print("SEMAFOR : ZELENA")
    return 0

if __name__ == "__main__":
    sys.exit(glavni())
