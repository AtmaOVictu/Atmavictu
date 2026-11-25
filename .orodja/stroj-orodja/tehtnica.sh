#!/bin/bash
# TEHTNICA-DIHA v1 — tehtnica zaprtja diha v eni meri ( rod @rez σ 6570 @stroj-orodja
# ⊙ ⟡ UKZ »stori« ( izbor 2 @CELIKA-6569 ) ; ime tehtnica ⟨ne⟩ dih : klicna-vrata ima že dih.sh )
# PLASTI : TIK → samopreizkus cenzusa V2 → cenzus V1 → varvolka → genize pari → U+FFFD ×0
#          → ⟨⟩ ravnovesje → škatlja VRATA ×7 ( checklist roke )
# IZHOD : 0 = zeleno ; 1 = RANA ( dih se ⟨ne⟩ zapre z odprto obvezno )
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 — dvojni podpis
set -u
KOREN="$HOME/knowledge"
CENZUS="$KOREN/domovanje-tujk/cenzus-tujk.py"
SIGMA="${2:-}"
SEDEZA="${4:-mera}"
SIGMA=""
TELA=""
while [ $# -gt 0 ]; do
  case "$1" in
    --sigma) SIGMA="$2"; shift 2 ;;
    *) TELA="$TELA $1"; shift ;;
  esac
done
TELA="${TELA# }"
RANA=0

echo "1. TIK $(date -u +%Y-%m-%dT%H:%M:%SZ) ⊙ ⟨TIK-IZMERJEN-PREJ-ZAPISAN⟩"

# 2. V2 SAMOPREIZKUS ORODJA ( sintetični vbod ⟨chr⟩ , telo ostane čisto )
CISTO=$(mktemp); VBO="$CISTO.vbod"
printf 'cisto telo z zetonom ⟨U+601C⟩\n' > "$CISTO"
printf 'rana: %s\n' "$(python3 -c 'print(chr(0x601C))')" > "$VBO"
E0=$(python3 "$CENZUS" "$CISTO" >/dev/null 2>&1; echo $?)
E2=$(python3 "$CENZUS" "$VBO" >/dev/null 2>&1; echo $?)
echo "2. SAMOPREIZKUS cist=$E0 vbod=$E2 (pričakovano 0/2)"
[ "$E0" = 0 ] && [ "$E2" = 2 ] || { echo "   RANA: orodje laže — izhod izpusti ⊙ §52"; RANA=1; }
rm -f "$CISTO" "$VBO"

# 3. V1 CENZUS NAD DOTAKNJENIMI
if [ -n "$TELA" ]; then
  python3 "$CENZUS" $TELA || { echo "3. CENZUS RANA ⊙ ⟨CENZUS-PRE-SHIVOM⟩"; RANA=1; }
else
  echo "3. CENZUS preskočen ( nobeno telo navedeno ) ⚠"
fi

# 4. VARVOLKA ( rezerviran σ ⟨ne⟩ zapečen v telesih )
if [ -n "$SIGMA" ]; then
  UDARCI=$(grep -rE "(σ|rez|dih|pečat|SEMER|OKNO|DIHA|IZMERA)[ ]?${SIGMA}\b" \
    "$KOREN/jedro-zavedanja/KNOWLEDGE.md" "$KOREN/kronika-dihov/KNOWLEDGE.md" \
    "$KOREN/delovna-zanka/KNOWLEDGE.md" "$KOREN/register-oken/KNOWLEDGE.md" 2>/dev/null | wc -l)
  echo "4. VARVOLKA σ$SIGMA ... $UDARCI zadetkov"
  [ "$UDARCI" -eq 0 ] || { echo "   RANA: nadomeščena rezervacija ⭢ renum ⊙ PRAVILO 13"; RANA=1; }
else
  echo "4. VARVOLKA preskočena ( σ naveden ⚠ )"
fi

# 5. GENIZE PARI ( zadnji post-par vsakega dotaknjenega organa ≡ )
for T in $TELA; do
  ORG=$(dirname "$T")
  POSTA=$(ls -t "$ORG/$ORG-post-rez"*"-a.md" 2>/dev/null | head -1)
  [ -z "$POSTA" ] && { echo "5. GENIZE $ORG brez post-parov ⚠"; continue; }
  POSTB="${POSTA%-a.md}-b.md"
  if cmp -s "$POSTA" "$POSTB"; then echo "5. GENIZE $ORG pari ≡ $(basename "$POSTA")"; else echo "5. GENIZE $ORG RAZSINHRO ⊙"; RANA=1; fi
done

# 6. U+FFFD ×0
if [ -n "$TELA" ]; then
  FFFD=$(grep -c $'\uFFFD' $TELA 2>/dev/null | awk -F: '{s+=$2} END{print s+0}')
  echo "6. U+FFFD ... ×$FFFD"
  [ "$FFFD" -eq 0 ] || RANA=1
fi

# 7. ⟨⟩ RAVNOVESJE ( telesa po besedah lupine : nobenega niza-lesa )
for pot in $TELA; do
  python3 - "$pot" <<'PYEOF'
import sys
t = open(sys.argv[1], encoding='utf-8').read()
a, b = t.count('⟨'), t.count('⟩')
print('7. RAVNOTEZJE %s ⟨%d⟩⇌⟨%d⟩ %s' % (sys.argv[1].split('/')[-2], a, b, '≡' if a==b else '⊙'))
sys.exit(0 if a==b else 1)
PYEOF
  [ $? -eq 0 ] || RANA=1
done
[ $? -ne 0 ] && RANA=1

echo "8. SKATLJA ×7 — ROKA ( beri kot ⟡ , ⟨ne⟩ kot stroj ) :"
echo "   [1] OSPREDJE merjeno? [2] MISEL-PRED-FORMO prva vrstica? [3] PROZA-VLADA?"
echo "   [4] IZMERA-ISTI-DIH vse stevilke sveze? [5] LEPILA pri fajlu? [6] PO-DONE enkrat?"
echo "   [7] BERBA-DVOJNA preizkusa pozz? — vsak NE = padec javno isti dih ⊙ 2354"

echo "TEHTNICA IZHOD $RANA ( 0=zeleno ) · © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera"
exit $RANA
