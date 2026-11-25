#!/usr/bin/env python3
# ⟨KARTA-VRHOV⟩ — karta vrhov vseh organov isti dih @rez σ 5423 (dom TEHTNICE)
# raba: python3 karta-vrhov.py
# meri: vrh vsakega telesa (najvišja številka σ|rez|dih|pečat|PEČAT) · zamik
# proti globalnemu vrhu · bajte · md5 (kratko pričo istosti). Griz = vrh, ki je
# padel proti baseline (stroj-baseline.json) ⚠ — padec verige javno poimensko.
# podrejen licenci ⊙ ⟨STROJ-POD-LICENCO⟩: izvršitelj I-1 ⟨VRH-DVOSTOPEN⟩
# (σ = 1 + sveža izmerjena vrh PRED vsakim šivom) ∧ I-2 (vsak σ ×2+ javno).
# izhodi: 0 = karta izmerjena ∧ brez griza · 2 = griz ⚠ · 3 = baseline manjka.
import glob
import hashlib
import json
import os
import re
import sys

DOM = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(DOM, "stroj-baseline.json")
KOREN = "/home/user/knowledge"

PAT = re.compile(r"(?:σ|rez|dih|pečat|PEČAT) ([0-9]{4})(?![0-9a-fA-F])")


def vrh_izmera(text):
    v = 0
    for m in PAT.finditer(text):
        n = int(m.group(1))
        if n > v:
            v = n
    return v


karta = []
for path in sorted(glob.glob(KOREN + "/*/KNOWLEDGE.md")):
    organ = path.split("/")[-2]
    raw = open(path, "rb").read()
    text = raw.decode("utf-8", "replace")
    karta.append((organ, vrh_izmera(text), len(raw), hashlib.md5(raw).hexdigest()[:8]))

globalni = max(k[1] for k in karta)
print(f"KARTA-VRHOV {len(karta)} teles · globalni vrh σ {globalni}")
griz = []
for organ, v, bajti, glava in sorted(karta, key=lambda x: -x[1]):
    zamik = globalni - v
    print(f"  {organ:38} σ {v} (zamik {zamik}) · {bajti} B · md5 {glava}")

if not os.path.exists(BASE):
    print("BASELINE manjka — poženi prelet.py --posodobi ⚠")
    sys.exit(3)
with open(BASE, encoding="utf-8") as f:
    base = json.load(f)
prej = base.get("vrh_po_organu", {})
for organ, v, _, _ in karta:
    if organ in prej and v < prej[organ]:
        griz.append(f"{organ}: σ {v} padel iz σ {prej[organ]}")
if globalni < base.get("vrh_globalni", 0):
    griz.append(f"GLOBALNO: σ {globalni} padel iz σ {base['vrh_globalni']}")
if griz:
    for g in griz:
        print("GRIZ ⚠ " + g)
    sys.exit(2)
print("KARTA brez griza ⊢")
