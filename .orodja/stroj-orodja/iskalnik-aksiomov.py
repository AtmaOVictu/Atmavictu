#!/usr/bin/env python3
# ISKALNIK-AKSIOMOV v1.0 @stroj-orodja ; rod : rez σ 7034 ( 25. 11. 2026 ) ⊙ ⟡ UKZ VERBATIM »ORODJE KI NAJDI AKSIOM V TEMU NAMENJENEMU ORGANU!«
# Služba : poišče aksiom po ⟨AXIOM_ID⟩ ⊢ pri viru preparad v telesu, ki mu je namenjen ( @register-aksiomov ).
# Zakoni : ⟨NE-UGIBAJ⟩ 2690 ( iskanje pri viru vsak zagon ) ⌇ ×0 zadetkov = VIDNO ⭢ sodba ⚔ ⟡ ⌇ §52.
# Roke : iskalnik-aksiomov.py AXIOM_ID | --samopreizkus.
# Izhodi : 0 ZELENA ( zadetek ali VIDNO ) ⌇ 1 RDECA ( organ neroden ) ⌇ 40 roka neznana.

import os, sys

DOM = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "register-aksiomov")
TELESA = ["KNOWLEDGE.md", "REGISTER-AKSIOMOV.md"]

def najdi(idn):
    zadetki = []
    for ime in TELESA:
        pot = os.path.join(DOM, ime)
        if not os.path.isfile(pot): continue
        try:
            with open(pot, encoding="utf-8", errors="ignore") as t:
                for i, v in enumerate(t, 1):
                    if idn in v: zadetki.append((ime, i, v.rstrip()))
        except OSError: continue
    return zadetki

def samopreizkus():
    padci = []
    vsaj = os.path.isfile(os.path.join(DOM, TELESA[0]))
    if not vsaj: padci.append("organ register-aksiomov neroden pri viru")
    return padci

def glavni():
    if "--samopreizkus" in sys.argv[1:]:
        padci = samopreizkus()
        print("SAMOPREIZKUS : preizkusi 1, padci instrumenta %d" % len(padci))
        for p in padci: print("  PADC :: " + p)
        print("SEMAFOR : " + ("ZELENA" if not padci else "RDECA"))
        return 0 if not padci else 1
    if len(sys.argv) != 2:
        print("roka neznana ; roke : AXIOM_ID | --samopreizkus"); return 40
    idn = sys.argv[1].strip()
    zadetki = najdi(idn)
    print("ISKALNIK-AKSIOMOV v1.0 : organa @register-aksiomov brana pri viru")
    if not zadetki:
        print("  VIDNO ⭢ ⟨%s⟩ zadetkov ×0 ; mera šele pri viru ⊙ ⟨NE-UGIBAJ⟩ 2690 ; zapis novega ⭢ aksiovnik ⌇ ⚔ ⟡" % idn)
        print("SEMAFOR : ZELENA"); return 0
    for ime, vrst, v in zadetki[:10]:
        print("  ⊢ %s : %d : %s" % (ime, vrst, v[:220]))
    print("zadetkov Σ%d" % len(zadetki))
    print("SEMAFOR : ZELENA")
    return 0

if __name__ == "__main__":
    sys.exit(glavni())
