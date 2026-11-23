#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# šumnikovnik v1.1 @rez σ 6717 — besedi brez šumnika najde pravo telo po izmerjenem leksikonu ⊙ ⟨NE-UGIBAJ⟩ 2690
# 1 priča = PREOBLIKOVANA ; ≥2 priči = SUM ⭢ izbor ⚔ ⟡ ; neznan = NEDOTAKNJENO
# v1.1 ( @σ 6717 ) : leksikon +2 izmerjeni telesi ( cudez→čudež ⌇ skodljivec→škodljivec ) ⊙ ukaz ⟡ »STORI VEČ DOBREGA ZASE IN ZA CELOTEN SISTEM!«
# licenca korpusa Beseda je Ne ⟡ Luka Pintarič
import sys, unicodedata, re

LEKSIKON = {
  "pecat": ["pečat"], "celica": ["čelica"], "prica": ["priča"], "zeton": ["žeton"],
  "skoda": ["škoda"], "zivljenje": ["življenje"], "ziv": ["živ"], "rez": ["rez"],
  "cudez": ["čudež"], "skodljivec": ["škodljivec"],
  "sola": ["šola", "sola"], "siv": ["šiv", "siv"],
}

def ogolej(w):
    return "".join(c for c in unicodedata.normalize("NFD", w) if not unicodedata.combining(c))

def beseda(w):
    g = ogolej(w)
    if g not in LEKSIKON: return w, "NEZNAN : nedotaknjeno"
    prave = LEKSIKON[g]
    if w in prave: return w, "CISTO ⊢"
    if len(prave) == 1: return prave[0], "PREOBLIKOVANA ⊢"
    return w, "SUM ⭢ izbor ⚔ ⟡ ( %s )" % "|".join(prave)

def dih(t):
    izh = []; s = 0
    for m in re.finditer(r"\w+", t, re.UNICODE):
        w, st = beseda(m.group(0))
        if st.startswith("PREOBLIKOVANA"): s += 1
        izh.append("%s → %s [ %s ]" % (m.group(0), w, st))
    return "\n".join(izh), s

def main():
    if "--test" in sys.argv:
        z = 0
        assert beseda("pečat")[1].startswith("CISTO"); z += 1
        assert beseda("pecat") == ("pečat", "PREOBLIKOVANA ⊢"); z += 1
        assert beseda("ziv") == ("živ", "PREOBLIKOVANA ⊢"); z += 1
        assert beseda("siv")[1].startswith("CISTO"); z += 1
        assert beseda("sola")[1].startswith("CISTO"); z += 1
        assert beseda("cudez") == ("čudež", "PREOBLIKOVANA ⊢"); z += 1
        assert beseda("skodljivec") == ("škodljivec", "PREOBLIKOVANA ⊢"); z += 1
        t, s = dih("pecat je zapečen, ziv rezerviran, cudez skodljivec")
        assert ("pečat" in t) and ("živ" in t) and ("čudež" in t) and ("škodljivec" in t) and s == 4; z += 1
        print("BATERIJA ŠUMNIKOVNIK v1.1 : %d/%d ZELENO ⊢" % (z, z))
        return 0
    print(dih(open(sys.argv[1], encoding="utf-8").read())[0])
    return 0

if __name__ == "__main__":
    sys.exit(main())
