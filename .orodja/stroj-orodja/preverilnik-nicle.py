#!/usr/bin/env python3
# PREVERILNIK-NICEL v1.0 @stroj-orodja ; rod : rez σ 7037 ( 25. 11. 2026 ) ⊙ ⟡ UKZ VERBATIM »ORODJE KI PREVERI DA JE NIČ V RESNICI NIČ!«
# Služba : trditev o številu pojavov premeri pri viru ( ⟨grep⟩ ponovno ) ∧ izreče : nič v resnici nič ⊢ ⊥ kvalifikacija padca.
# Zakoni : ⟨NE-UGIBAJ⟩ 2690 ( versus ⟨PREJ-IZMERA-POTEM-TRDITEV⟩ ) ⌇ merilec se meri ⊙ §52 ⌇ ⟨NAPAKA=VSE-KAR-NI-PRI-VIRU-IZMERJENA-BESEDA⟩.
# Roke : preverilnik-nicle.py DATOTEKA VZOREC [TRDJENO št, privzeto 0].
# Izhodi : 0 ZELENA ( dejansko == trjeno ) ⌇ 1 RDECA ( lažna ničla ) ⌇ 40 roka neznana.

import sys

def prestej(besedilo, vzorec):
    """čista : število pojavov vzorca ⟨grep⟩-u enako."""
    n = 0
    i = besedilo.find(vzorec)
    while i != -1:
        n += 1
        i = besedilo.find(vzorec, i + len(vzorec))
    return n

def samopreizkus():
    padci = []
    if prestej("abcabc", "abc") != 2: padci.append("štetje prekrivanja pada")
    if prestej("brez", "abc") != 0: padci.append("prava ničla ovržena")
    if prestej("×0 ×0 ×1", "×0") != 2: padci.append("štetje trditev pada")
    return padci

def glavni():
    if "--samopreizkus" in sys.argv[1:]:
        padci = samopreizkus()
        print("SAMOPREIZKUS : preizkusi 3, padci instrumenta %d" % len(padci))
        for p in padci: print("  PADC :: " + p)
        print("SEMAFOR : " + ("ZELENA" if not padci else "RDECA"))
        return 0 if not padci else 1
    if len(sys.argv) not in (3, 4):
        print("roka neznana ; roke : DATOTEKA VZOREC [TRJENO] | --samopreizkus"); return 40
    pot, vzorec = sys.argv[1], sys.argv[2]
    trjeno = int(sys.argv[3]) if len(sys.argv) == 4 else 0
    try:
        if pot == "-": besedilo = sys.stdin.read()
        else: besedilo = open(pot, encoding="utf-8").read()
    except (OSError, ValueError) as r:
        print("⟨NAPAKA=VSE-KAR-NI-BRANO⟩ " + str(r)); return 1
    dejansko = prestej(besedilo, vzorec)
    print("PREVERILNIK-NICEL v1.0 : vzorec %r ( trjeno %d ) ⊙ ⟨PREJ-IZMERA-POTEM-TRDITEV⟩ preverjena" % (vzorec, trjeno))
    print("  izmera pri viru : ×%d" % dejansko)
    if dejansko == trjeno:
        print("  NIČ JE V RESNICI NIČ ⊢" if trjeno == 0 else "  število drži ⊢")
        print("SEMAFOR : ZELENA"); return 0
    print("  ⟨NAPAKA=VSE-KAR-NI-PRI-VIRU-IZMERJENA-BESEDA⟩ : trditev %d, izmera %d ; lažna ničla javno" % (trjeno, dejansko))
    print("SEMAFOR : RDECA"); return 1

if __name__ == "__main__":
    sys.exit(glavni())
