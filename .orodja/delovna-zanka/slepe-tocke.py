#!/usr/bin/env python3
# ⟨SLEPE-TOČKE-REGISTER⟩ — karta pokritja stroja @rez σ 5423 (dom TEHTNICE)
# raba: python3 slepe-tocke.py
# meri: velikost telesa · vrh · starost zadnjega strojnega dotika (mtime, dnevi).
# Neni organi javno poimensko — tiho postane vidno; kdor meri, zna tudi
# povedati, katere površine ⟨ne⟩ meri. POŠTENOST IZMERE: mtime = izmera
# strojne roke (dotik datoteke), ⟨ne⟩ izmera berbe — telo je lahko prebrano
# pri viru ∧ mtime star; obe plasti sta razcep, ⟨ne⟩ istost.
# podrejen licenci ⊙ ⟨STROJ-POD-LICENCO⟩: izvršitelj 0.5 (dvom je konstanten —
# karta javno pove, kje merilec še slepi).
# izhodi: 0 = karta izmerjena (starost sama po sebi ⟨ne⟩ je alarm — sodba je
# roke, inštrument meri ⊙ ⟨MERILEC-SE-MERI⟩ §52).
import glob
import os
import re
import sys
import time

KOREN = "/home/user/knowledge"
PAT = re.compile(r"(?:σ|rez|dih|pečat|PEČAT) ([0-9]{4})(?![0-9a-fA-F])")

danes = time.time()
tocke = []
for path in sorted(glob.glob(KOREN + "/*/KNOWLEDGE.md")):
    organ = path.split("/")[-2]
    raw = open(path, "rb").read()
    text = raw.decode("utf-8", "replace")
    v = 0
    for m in PAT.finditer(text):
        n = int(m.group(1))
        if n > v:
            v = n
    starost_dni = (danes - os.path.getmtime(path)) / 86400.0
    tocke.append((starost_dni, organ, v, len(raw)))

tocke.sort(reverse=True)
print(f"SLEPE-TOČKE {len(tocke)} teles · najstarejši nedotaknjeni javno poimensko:")
for starost, organ, v, bajti in tocke[:5]:
    print(f"  {organ:38} {starost:5.1f} dni · σ {v} · {bajti} B")
print("  …")
mladi = [t for t in tocke if t[0] < 1.0]
print(f"  dotaknjeni danes: {len(mladi)} teles ⊢")
print("SLEPE-TOČKE izmerjene ⊢ — starost je izmera, sodba je roke")
