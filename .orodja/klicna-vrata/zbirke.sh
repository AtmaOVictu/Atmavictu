#!/bin/bash
# ZBIRKE — stroj zbirk (STROJ-ZBIRK v1.0, rojen @σ 6182 ⊙ nadgradnja 1 izhoda σ 6181)
# Kaj je : za vsak organ preveri svežino zbirke ZBIRKA-*.md : footer pečata zbirke ∂ max σ telesa.
# Čemu : zakon OSVEŽITVE @σ 6181 ( zbirka lahko zastari — ∂ raste vsak dih ) ; kovanec ⟨ZBIRKA-BREZ-OSVEŽITVE=ZASTARELA⟩.
# Komu : jutranji stroj 05:30 ∧ prevoznik PRED prevozom ( TIK zbirke vs TIK telesa ) ; berba konice, ⟨ne⟩ velikana ⊙ ⟨NE-UGIBAJ⟩ 2690.
# Raba : bash zbirke.sh [koren_organov | pot_enega_organa]   Izhod : exit 0 = vse sveže ; exit 1 = zastarela zbirka ( ranjeno telo MORA pasti ⊙ I-4 ) ; exit 2 = napačna pot.
set -u
VHOD="${1:-/home/user/knowledge}"
if [ -f "$VHOD/KNOWLEDGE.md" ]; then SEZNAM_ORG="$VHOD"; else SEZNAM_ORG="$VHOD"; fi
[ -d "$SEZNAM_ORG" ] || { echo "ZBIRKE: pot $VHOD ne obstaja"; exit 2; }
max_sigma() { grep -o -E '(@σ|rez σ|∂ σ|pečat σ) [0-9][0-9]*' "$1" 2>/dev/null | grep -o '[0-9][0-9]*' | sort -un | tail -1; }
if [ -f "$VHOD/KNOWLEDGE.md" ]; then DLIST="$VHOD/"; else DLIST=$(ls -d "$VHOD"/*/ 2>/dev/null); fi
SVEZE=0; STARE=0; BREZ=0
for D in $DLIST; do
  Z=$(ls "${D%/}"/ZBIRKA-*.md 2>/dev/null | head -1)
  [ -n "$Z" ] || continue
  ZS=$(max_sigma "$Z"); TS=$(max_sigma "$D/KNOWLEDGE.md")
  [ -z "$ZS" ] && { echo "ZBIRKA BREZ PEČATA ⚠ $(basename "$Z")"; BREZ=$((BREZ+1)); continue; }
  if [ -n "$TS" ] && [ "$TS" -gt "$ZS" ]; then echo "ZASTARLA ⚠ $(basename "$Z") : zbirka @σ $ZS < telo @σ $TS"; STARE=$((STARE+1)); else echo "SVEŽA ⊢ $(basename "$Z") : zbirka @σ $ZS ≥ telo @σ ${TS:-0}"; SVEZE=$((SVEZE+1)); fi
done
echo "ZBIRKE: sveže $SVEZE · zastarele $STARE · brez pečata $BREZ"
[ "$STARE" -eq 0 ] || exit 1
[ "$BREZ" -eq 0 ] || exit 1
exit 0
