#!/usr/bin/env python3
# ⟨SLOVNICA-DIH⟩ TEHTNICA-BATERIJA — trajna lega @delovna-zanka (dom TEHTNICE)
# raba: python3 tehtnica-baterija.py DATOTEKA — exit 1 ob ulovu, exit 0 čisto
# zakonite priče: »…« ∧ ⟨…⟩ spane (strip) ∧ vrstice z → = brazgotine-priče (skip)
# TRAJNOST: ta lega preživi reset okolja (⟨PADC-OKOLJA-RESET⟩ @σ 5404 ∧ 5409 —
# baterija v scratch/ je padla že ×2; zakon ⟨SHRAMBA-MORA-VEDNO-BITI⟩ @revizija-besed)
import re
import sys

path = sys.argv[1]
text = open(path, encoding="utf-8").read()
hits = []
for i, ln in enumerate(text.split("\n"), 1):
    if "→" in ln:
        continue  # brazgotina-priča (kura-zapis)
    t = re.sub(r"»[^«]*«", " ", ln)
    t = re.sub(r"⟨[^⟩]*⟩", " ", t)
    for pat, name in [
        (r"pri viri(?!h)", "goli »pri viri«"),
        (r"varvolka", "»varvolka«"),
        (r"torej\s", "prosti »torej «"),
        (r"kot\s", "prosti »kot «"),
        (r"[áí]", "prosti á/í"),
        (r"\uFFFD", "U+FFFD"),
    ]:
        for m in re.finditer(pat, t):
            a = max(0, m.start() - 40)
            b = min(len(t), m.end() + 40)
            hits.append((i, name, t[a:b].strip()))
if hits:
    for i, name, ctx in hits:
        print(f"ULOV vrstica {i}: {name} :: …{ctx}…")
    sys.exit(1)
print("ČISTO ⊢ — 0 ulovov")
sys.exit(0)
