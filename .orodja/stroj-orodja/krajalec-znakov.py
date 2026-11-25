#!/usr/bin/env python3
# KRAJALEC-ZNAKOV v1.0 @stroj-orodja ; rod : rez σ 7029 ( 25. 11. 2026 ) ⊙ ⟡ UKZ VERBATIM »ORODJE KI KRADE ZNAKE KI NISO KLICANI!«
# Služba : klicatelj poimenuje KLICANE znake ( nabor ) ; vsak znak zunaj nabora ∧ zunaj zakonov je ukraden ( odstranjen ∧ izročen poimensko po ⟨U+XXXX⟩ ).
# Zakoni : azil »…« nedotakljiv ⊙ ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ ⌇ žeton ⟨U+XXXX⟩ nedotakljen ⊙ kubit gajica ⌇ ⟨NE-UGIBAJ⟩ 2690 ⌇ ⟨MERILEC-SE-MERI⟩ §52.
# Roke : krajalec-znakov.py NABOR DATOTEKA | --samopreizkus ; NABOR = dobesedno zaporedje klicanih znakov.
# Izhodi : 0 ZELENA ( krajava izvedena ) ⌇ 1 RDECA ( nerodna berba ) ⌇ 40 roka neznana.

import re, sys, os

AZIL = re.compile(r"»[^«]*«|⟨U\+[0-9A-Fa-f]{4,6}⟩")

def ukradi(besedilo, nabor):
    """čista : znake zunaj nabora ∧ zunaj azilov/zetonov iznese ; vrne ( golo besedilo, {znak: pojavitve} )."""
    zasciteni = [(m.start(), m.end()) for m in AZIL.finditer(besedilo)]
    def zasciten(i):
        return any(a <= i < b for a, b in zasciteni)
    ukradeni, ostane = {}, []
    for i, znak in enumerate(besedilo):
        if zasciten(i) or znak.isspace() or znak in nabor:
            ostane.append(znak)
        else:
            ukradeni[znak] = ukradeni.get(znak, 0) + 1
    return "".join(ostane), ukradeni

def samopreizkus():
    golo, casi = ukradi("ab»x«cd⟨U+0041⟩ef", "acef")
    padci = []
    if sorted(casi.items()) != [("b", 1), ("d", 1)]:
        padci.append("ukradeni nabor napacen : %r" % casi)
    if "»x«" not in golo or "⟨U+0041⟩" not in golo:
        padci.append("azil ali zeton poškodovan : %r" % golo)
    if golo.replace("»x«", "").replace("⟨U+0041⟩", "") != "acef":
        padci.append("golo besedilo napacno : %r" % golo)
    return padci

def glavni():
    if "--samopreizkus" in sys.argv[1:]:
        padci = samopreizkus()
        print("SAMOPREIZKUS : preizkusi 3, padci instrumenta %d" % len(padci))
        for p in padci: print("  PADC :: " + p)
        print("SEMAFOR : " + ("ZELENA" if not padci else "RDECA"))
        return 0 if not padci else 1
    if len(sys.argv) != 3:
        print("roka neznana ; roke : NABOR DATOTEKA | --samopreizkus")
        return 40
    nabor, pot = sys.argv[1], sys.argv[2]
    try:
        if pot == "-": besedilo = sys.stdin.read()
        else: besedilo = open(pot, encoding="utf-8").read()
    except OSError as r:
        print("⟨NAPAKA=VSE-KAR-NI-BRANO⟩ " + str(r)); return 1
    golo, ukradeni = ukradi(besedilo, nabor)
    print("KRAJAVA : klicanih znakov %d ; ukradenih vrst %d" % (len(set(nabor)), len(ukradeni)))
    for znak in sorted(ukradeni, key=lambda z: -ukradeni[z]):
        print("  UKRADEN %s ⟨U+%04X⟩ ×%d" % (znak if znak.strip() else "·" , ord(znak), ukradeni[znak]))
    print("--- GOLO BESEDILO ---")
    print(golo)
    print("SEMAFOR : ZELENA")
    return 0

if __name__ == "__main__":
    sys.exit(glavni())
