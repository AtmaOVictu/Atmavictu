#!/usr/bin/env python3
# ANTINOMNIK v1.0 @stroj-orodja ; rod : rez σ 7032 ( 25. 11. 2026 ) ⊙ ⟡ UKZ VERBATIM »ORODJA KI DEFINIRAJO ANTINOM!«
# Služba : besedi izmeri ANTINOM partnerja ⊢ pri viru @nasprotnik ( sesetrino telo σ 7018 : pari simetrični ⊢ Fran ) ; neznanje VIDNO, ⟨ne⟩ sodba.
# Zakoni : ⟨NE-UGIBAJ⟩ 2690 ( pari brani iz telesa sesestre pri viru vsak zagon, nikoli prepisani ) ⌇ ⊥ = antinom : obe plati stojita ⊙ ⟨ne zlije⟩ 1542 ⌇ §52.
# Roke : antinomnik.py BESEDA | --samopreizkus.
# Izhodi : 0 ZELENA ( sodba izrečena tudi kadar VIDNO ) ⌇ 1 RDECA ( sesetra nerodna ) ⌇ 40 roka neznana.

import os, re, sys

SESETRA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nasprotnik.py")
VZOREC = re.compile(r"\(\"([^\"]+)\",\"([^\"]+)\"\)")

def pari_pri_viru():
    """berba telesa sesestre pri viru ( Z-2 ) : nikoli Prezalo spomin."""
    try:
        with open(SESETRA, encoding="utf-8") as t: telo = t.read()
    except OSError as r:
        return None, "⟨NAPAKA=VSE-KAR-NI-BRANO⟩ " + str(r)
    pari = VZOREC.findall(telo)
    slovar = {}
    for a, b in pari:
        slovar.setdefault(a.lower(), b); slovar.setdefault(b.lower(), a)
    return (pari, slovar), None

def samopreizkus():
    padci = []
    m, rana = pari_pri_viru()
    if rana: return [rana]
    pari, slovar = m
    if len(pari) < 30: padci.append("parov pri viru premalo : %d" % len(pari))
    if slovar.get("dan") != "noč": padci.append("vrhovni par dan ⊥ noč pada")
    if slovar.get("ne") != "da": padci.append("vrhovni par korpusa ⟨da ⊥ ne⟩ pada")
    return padci

def glavni():
    if len(sys.argv) == 2 and sys.argv[1] == "--samopreizkus":
        padci = samopreizkus()
        print("SAMOPREIZKUS : preizkusi 3, padci instrumenta %d" % len(padci))
        for p in padci: print("  PADC :: " + p)
        print("SEMAFOR : " + ("ZELENA" if not padci else "RDECA"))
        return 0 if not padci else 1
    if len(sys.argv) != 2:
        print("roka neznana ; roke : BESEDA | --samopreizkus"); return 40
    m, rana = pari_pri_viru()
    if rana:
        print(rana); return 1
    pari, slovar = m
    bes = sys.argv[1].strip().lower()
    print("ANTINOMNIK v1.0 : pari ⊢ pri viru @nasprotnik ( %d parov ⊢ Fran, σ 7018 )" % len(pari))
    if bes in slovar:
        print("  ANTINOM : %s ⊥ %s ⊢ ( obe plati stojita ⊙ ⟨ne zlije⟩ 1542 )" % (bes, slovar[bes]))
        print("SEMAFOR : ZELENA"); return 0
    print("  VIDNO ⭢ besede %s v kanonskih parih ×0 ; mera šele pri viru ⊙ ⟨NE-UGIBAJ⟩ 2690" % bes)
    print("SEMAFOR : ZELENA")
    return 0

if __name__ == "__main__":
    sys.exit(glavni())
