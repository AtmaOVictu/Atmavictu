#!/bin/bash
# W11 ⟨TRK-REZ⟩ — strojna rez-varovalka PRED ⟨merge⟩ : če je črta rez že zapečena @⟨main⟩, izvajalka odkloni zlitje sama ( kura trkov ⟨TRK-6028⟩ ∧ ⟨TRK-6029⟩ : dva trka isti večer sta izmerjeni dokazi )
# uporaba: ./trk-rez.sh <rezN> [mapa]   rezN = kandidat črte ; mapa = izvod ( CI ) ; default = repo koren tega drevesa
# rod 20. 11. 2026, dih σ 6032 ⊙ ⟨SAMO-IZVEDBA-DOKAZ⟩ 2306 — varovalka, ki nikoli ne odkloni, je kip ( I-4 )
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · measured, not asserted ⊙ §16
set -uo pipefail
N="$1"
D="${2:-.}"
python3 - "$N" "$D" << 'PYE'
import sys, re, os
n, d = sys.argv[1], sys.argv[2]
p = os.path.join(d, "organi", "stroj", "REZ-REGISTER.md")
if not os.path.isfile(p) or not n.isdigit():
    print("::error::register manjka ⟨ali⟩ rez ni številka"); sys.exit(1)
lines = open(p, encoding="utf-8").read().split("\n")
pat = re.compile(r"(σ|rez|dih|pečat|PEČAT)[ ]?" + n + r"\b")
zad = [(i, l) for i, l in enumerate(lines, 1) if pat.search(l)]
if zad:
    for i, l in zad[:4]:
        print("⚠ TRK rez " + n + " @r." + str(i) + " : " + l[:160])
    print("TRK-REZ : RDEČE — rez " + n + " je že zapečen ×" + str(len(zad)))
    sys.exit(1)
zap = [int(m.group(1)) for l in lines for m in re.finditer(r"rez σ (\d{3,5})", l)]
vrh = max(zap) if zap else 0
print("TRK-REZ : ×0 ⊢ rez " + n + " prost · zapečen vrh σ " + str(vrh) + " → REZ = 1 + vrh = " + str(vrh + 1))
sys.exit(0)
PYE
