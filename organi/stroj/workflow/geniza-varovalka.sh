#!/usr/bin/env bash
# W13 GENIZE-VAROVALKA ⊙ dih σ 6235 — strojna preverba, ⟨ne⟩ obljuba ⊙ §16 measured, not asserted
# : zunanjih url v telesu LICENSE-ZLO-IPA.md ×0 ⊙ ⟡ beseda VERBATIM »sovražim linke do zunanjih url povezav, saj niso absolutno zanesljive. a ne da niso?«
# : priče genize obstoje ∧ velikosti bajtno točne ⊙ MANIFEST.json ∧ reference telesa prisotne
set -euo pipefail
ROOT="${1:-.}"
TELO="$ROOT/LICENSE-ZLO-IPA.md"
MAN="$ROOT/geniza/virov-zlo-ipa/MANIFEST.json"
[ -f "$TELO" ] || { echo "W13 ⚠ manjka telo : $TELO"; exit 1; }
[ -f "$MAN" ] || { echo "W13 ⚠ manjka manifest : $MAN"; exit 1; }
Z=$(grep -cE 'https?://[a-zA-Z0-9]' "$TELO" || true)
if [ "$Z" != "0" ]; then echo "W13 ⚠ zunanjih url v telesu : $Z ( pričakovano 0 )"; exit 1; fi
python3 - "$ROOT" << 'PYKONEC'
import json, os, sys
root = sys.argv[1]
man = json.load(open(os.path.join(root, "geniza/virov-zlo-ipa/MANIFEST.json"), encoding="utf-8"))
telo = open(os.path.join(root, "LICENSE-ZLO-IPA.md"), encoding="utf-8").read()
p = man.get("priče", [])
napake = []
if len(p) < 40: napake.append("prič " + str(len(p)) + " ⊥ 40")
for x in p:
    d = x["datoteka"]
    pot = os.path.join(root, d)
    if not os.path.isfile(pot):
        napake.append("manjka : " + d)
        continue
    v = os.path.getsize(pot)
    if v != x["velikost_bajtov"]: napake.append("velikost ⚠ " + d + " : " + str(v) + " ⊥ " + str(x["velikost_bajtov"]))
    if ("( " + d + " )") not in telo: napake.append("prijča ni v telesu : " + d)
if napake:
    print("W13 ⚠ : " + " ; ".join(napake))
    sys.exit(1)
print("W13 GENIZE-VAROVALKA ⊢ : zunanjih url ×0 ; prič " + str(len(p)) + " velikosti bajtno točne ; reference telesa prisotne")
PYKONEC
