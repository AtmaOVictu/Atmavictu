#!/bin/bash
# GENIZE-PROVERBA — instrument resnice »izguba 0 ( genize ×2 bajt-isto )« (rojstvo σ 6170 ⊙ ⟨TEST-×2⟩)
# Kaj je : preveri vsak .geniza par vsakega organa ( konvenciji g1/g2 ∧ -a/-b ) bajt-po-bajt ( md5 ) ;
# par brez para ∧ različna bajta = padec izgube, izpis javen. PESKA.net cmp ⟨ne⟩ obstaja tu ⚠ → md5sum.
# Čemu : ⟨GENIZA-AVTOMAT⟩ 2785 zahteva ×2 bajt-ito, doslej merjeno ročno ⚠ — resnica dobi telo.
# Komu : vsakemu dihu pred šivom ( genize PRED ) ∧ po šivu ( genize POST ) ⊙ zrcalo-kanarec.
# Raba : bash genize-proverba.sh [koren_organov | pot_enega_organa] [-p]
#   KOREN privzeto /home/user/knowledge ( koren ) ; če pot vsebuje KNOWLEDGE.md = en organ ( peska.net : 30 s meja, .geniza @DZ = 4 GB ⚠ prebera po organih )
#   -p : plast POST : najnovejši par vsakega organa primerja z ŽIVO konico ⟹ SVEŽ/ZASTAREL ( poročilo, ⟨ne⟩ sodba )
# Izhod : exit 0 = vsi pari bajt-ito ; exit 1 = padec ( nabojev + parcev > 0 ) ; exit 2 = napačna pot.
set -u
POST=""
VHOD="${1:-/home/user/knowledge}"
[ "${2:-}" = "-p" ] && POST=1
if [ "${1:-}" = "-p" ]; then VHOD="/home/user/knowledge"; POST=1; fi
md5_f() { md5sum "$1" 2>/dev/null | cut -d' ' -f1; }
if [ -f "$VHOD/KNOWLEDGE.md" ]; then SEZNAM_ORG="$VHOD/.."; else SEZNAM_ORG="$VHOD"; fi
[ -d "$SEZNAM_ORG" ] || { echo "GENIZE-PROVERBA: pot $VHOD ne obstaja"; exit 2; }
PARI=0; NABOJI=0; PARCI=0
if [ -f "$VHOD/KNOWLEDGE.md" ]; then set -- "$VHOD/"; else set -- "$VHOD"/*/; fi
for D in "$@"; do
  G="$D/.geniza"; ORG=$(basename "$D")
  [ -d "$G" ] || continue
  for F1 in "$G"/*g1*; do
    [ -e "$F1" ] || continue
    F2=${F1//g1/g2}
    if [ ! -e "$F2" ]; then echo "PARC SAMOTEN G1 ⚠ @${ORG}: $(basename "$F1") brez para"; PARCI=$((PARCI+1)); continue; fi
    if [ "$(md5_f "$F1")" != "$(md5_f "$F2")" ]; then echo "NABOJ ⚠ @${ORG}: $(basename "$F1") ⊥ $(basename "$F2")"; NABOJI=$((NABOJI+1)); fi
    PARI=$((PARI+1))
  done
  for F1 in "$G"/*-a.md "$G"/*-a.sh; do
    [ -e "$F1" ] || continue
    F2=$(echo "$F1" | sed 's/-a\.\([^.]*\)$/-b.\1/')
    if [ ! -e "$F2" ]; then echo "PARC SAMOTEN A ⚠ @${ORG}: $(basename "$F1") brez para $(basename "$F2")"; PARCI=$((PARCI+1)); continue; fi
    if [ "$(md5_f "$F1")" != "$(md5_f "$F2")" ]; then echo "NABOJ ⚠ @${ORG}: $(basename "$F1") ⊥ $(basename "$F2")"; NABOJI=$((NABOJI+1)); fi
    PARI=$((PARI+1))
  done
  if [ "$POST" = "1" ]; then
    NOV=$(ls -t "$G"/*g2* "$G"/*-b.md 2>/dev/null | head -1)
    if [ -n "$NOV" ] && [ -f "$D/KNOWLEDGE.md" ]; then
      if [ "$(md5_f "$NOV")" = "$(md5_f "$D/KNOWLEDGE.md")" ]; then echo "POST SVEŽ ⊢ @${ORG}"; else echo "POST ZASTAREL ⚠ @${ORG} ( konica rasla po genizi — pošteno poročilo, ⟨ne⟩ padec )"; fi
    fi
  fi
done
echo "GENIZE-PROVERBA: parov ${PARI} · nabojev ${NABOJI} · parcev ${PARCI}"
[ "$((NABOJI+PARCI))" -eq 0 ] && exit 0 || exit 1
