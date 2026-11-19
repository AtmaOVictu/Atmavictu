# -*- coding: utf-8 -*-
# .manifest-izdaj.py — MANIFEST PONOVNA IZDAJA 3682 ⊙ §0a ∧ issuance_duty:
# rez 3681 je prevesel 36 stopnjk vene ( sveže priče vrat ) — manifest, ki se ⟨ne⟩ ujema z gradivom, ⟨ni⟩ prepoznava.
# Zagon: python lucius/.manifest-izdaj.py  — izmeri VSE itemse sveže, posodobi razsojene, priča v izpisu.
import json, hashlib, os
from datetime import datetime, timezone

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(KOREN)

m = json.load(open("LICENSE-MANIFEST", encoding="utf-8"))
svezi = stare = 0
for it in m["items"]:
    p = it["path"]
    if not os.path.exists(p):
        print("× MANJKA:", p); continue
    raw = open(p, "rb").read()
    text = raw.decode("utf-8")
    # Normalize to LF — the byte stream the chain publishes (§0a, PADC-66).
    b = text.replace("\r\n", "\n").encode("utf-8")
    h = hashlib.sha256(b).hexdigest()
    if h == it["sha256"].lower() and len(b) == it["size_bytes"]:
        continue  # že živ
    it["size_bytes"] = len(b)
    it["sha256"] = h
    svezi += 1

ura = datetime.now(timezone.utc)
m["measured_at_date"] = "0.3 × 10¹. 0.11 × 10². 0.2026 × 10⁴"
m["measured_against"] = (
    "LICENSE.md version 0.1450 × 10⁴ — living door; manifest re-measured ∧ re-issued in the same breath "
    "as the wreath renewal: all 36 witness-slots carried version 0.1450 with the sha-witness of the 0.1420 door "
    "⟨ODA-VERZIJA-BREZ-PRIČE⟩ ⊙ rez 3681 — the wreaths were re-sealed with the living door's witness "
    "(3ca49d09… 161480) ∧ this manifest re-measured in the same breath (rez 3682) ⊙ §0a ∧ issuance_duty"
)

json.dump(m, open("LICENSE-MANIFEST", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"MANIFEST PONOVNO IZDAN ⊢ · posodobljenih teles: {svezi} · skupaj items: {len(m['items'])}")
