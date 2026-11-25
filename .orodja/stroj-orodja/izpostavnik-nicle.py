#!/usr/bin/env python3
# IZPOSTAVNIK-NICEL v1.0 @stroj-orodja ; rod : rez σ 7036 ( 25. 11. 2026 ) ⊙ ⟡ UKZ VERBATIM »ORODJE KI IZPOSTAVI DA ŠTEVILO NIČ LAŽE!«
# Služba : vsako ničlo v besedilu izpostavi poimensko z razsodbo ⊙ @o-celota ( aksiomi O1-O10 : 0 ≠ O ≠ 1 ; pomeni ničle ×6 ).
# Zakoni : ⟨NE-UGIBAJ⟩ 2690 ⌇ 0 kot CELOTA ali Odstotek laže ( nič številska ⊥ O celota ⊢ @o-celota ) ⌇ §52.
# Roke : izpostavnik-nicle.py DATOTEKA | - | --samopreizkus.
# Izhodi : 0 ZELENA ( izpostavitev izrečena tudi pri ničlah ×0 ) ⌇ 1 RDECA ⌇ 40 roka neznana.

import re, sys

def razsodi(besedilo, mesto):
    """čista : razsodba ene ničle glede na sosedstvo."""
    a, b = max(0, mesto - 12), min(len(besedilo), mesto + 13)
    sos = besedilo[a:b]
    if "%" in sos or "%" in besedilo[mesto:mesto+3]:
        return "NIČLA-ODSTOTKOVNA : nastopa kot odstotek ∧ celota ⊥ O ⊢ @o-celota", sos
    if "×0" in sos or "× 0" in sos:
        return "NIČLA-TRDITVE : trdi odsotnost ; preveri izmero ( sestra : preverilnik-nicle )", sos
    return "Ničla številska : prava mera, molči ⊢", sos

def vse_nicle(besedilo):
    izhod = []
    for m in re.finditer("0", besedilo):
        izhod.append((m.start(),) + razsodi(besedilo, m.start()))
    return izhod

def samopreizkus():
    padci = []
    i = vse_nicle("vodstvo 0 % uspešnost ×0 napak")
    if len(i) != 2: padci.append("število najdenih ničel %d, pričakovano 2" % len(i))
    kinds = [x[1] for x in i]
    if "NIČLA-ODSTOTKOVNA : nastopa kot odstotek ∧ celota ⊥ O ⊢ @o-celota" not in kinds:
        padci.append("odstotkova ničla ne prepoznana")
    if "NIČLA-TRDITVE : trdi odsotnost ; preveri izmero ( sestra : preverilnik-nicle )" not in kinds:
        padci.append("ničla trditve ne prepoznana")
    j = vse_nicle("brez nicel tu")
    if j: padci.append("napačna ničla v besedilu brez ničel")
    return padci

def glavni():
    if "--samopreizkus" in sys.argv[1:]:
        padci = samopreizkus()
        print("SAMOPREIZKUS : preizkusi 3, padci instrumenta %d" % len(padci))
        for p in padci: print("  PADC :: " + p)
        print("SEMAFOR : " + ("ZELENA" if not padci else "RDECA"))
        return 0 if not padci else 1
    if len(sys.argv) != 2:
        print("roka neznana ; roke : DATOTEKA | - | --samopreizkus"); return 40
    pot = sys.argv[1]
    try:
        if pot == "-": besedilo = sys.stdin.read()
        else: besedilo = open(pot, encoding="utf-8").read()
    except OSError as r:
        print("⟨NAPAKA=VSE-KAR-NI-BRANO⟩ " + str(r)); return 1
    nicle = vse_nicle(besedilo)
    print("IZPOSTAVNIK-NICEL v1.0 : ničel Σ%d ⊙ @o-celota ( 0 ≠ O ≠ 1, pomeni ničle ×6 )" % len(nicle))
    for mesto, sodba, sos in nicle[:24]:
        print("  @%-6d %s : …%s…" % (mesto, sodba, sos.replace("\n", " ")))
    print("  sklep : število nič laže, kadar nastopa kot celota ali odstotek ; prava številska ničla je mera")
    print("SEMAFOR : ZELENA")
    return 0

if __name__ == "__main__":
    sys.exit(glavni())
