#!/bin/bash
# vrata-jajce.sh v1.0 -- orodje J5 VOSLOVNA-JAJCA: vsako od sedmih vrat izhoda dobi znano pokvarjeno hrano
# Rod sigma 6883, UKZ delta VERBATIM STORI IN NADALJUJ
# Roke: --sej : seje 7 pokvarjenih + 1 cisto telo emisija-lintu, meri ulov po vratih
#       --samopreizkus : isto ( jajce samo je preizkus )
# Varnostni sklop: poti le znotraj /home/user/knowledge; brez eval/exec/omrezja.
KOREN=/home/user/knowledge
EM=$KOREN/stroj-orodja/emisija-lint.sh
TD="$KOREN/stroj-orodja/.geniza/TEST-vrata-$$-$(date -u +%H%M%S)"
mkdir -p "$TD"
i=0
sej() { i=$((i+1)); printf '%s\n' "$2" > "$TD/$1.txt"; }
sej V1 'dolga crta — tu je'
sej V2 'kratka crta – tu je'
sej V3 'prevec naglasa í tu'
sej V4 'zlep imeZnaka tu'
MASKA5=$(printf '\u27e8U+03C\u03c6\u27e9')
sej V5 "maska $MASKA5 tu"
sej V6 'dvojni  presledek tu'
sej V7 'presledek . pred piko'
printf '%s\n' 'cisto telo brez padca ⊢' > "$TD/cisto.txt"
U=0
for v in V1 V2 V3 V4 V5 V6 V7; do
  if bash "$EM" --preglej "$TD/$v.txt" >/dev/null 2>&1; then
    echo "BOLNO ⚠ $v : vrata spustila pokvarjeno"
  else
    U=$((U+1)); echo "ULOVLJENO ⊢ $v"
  fi
done
CIST=0
bash "$EM" --preglej "$TD/cisto.txt" >/dev/null 2>&1 && CIST=1
rm -rf "$TD"
echo "VRATA-JAJCE : ulovljenih $U od 7 ⌇ cisto telo spusceno $CIST"
[ "$U" = 7 ] && [ "$CIST" = 1 ] && { echo "SODBA : SEW ⊢"; exit 0; }
echo "SODBA : PADC ⚠"; exit 1
