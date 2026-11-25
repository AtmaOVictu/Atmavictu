#!/bin/bash
# trk-jajce.sh v1.0 -- orodje J4 TRK-JAJCA: dve rezervaciji na isti rez, natanko ena zmagovalka
# Rod sigma 6883, UKZ delta VERBATIM STORI IN NADALJUJ
# Roke: --sej KROGI : KROGI x vzporedni noclobber dvojini na isti atom
#       --samopreizkus : 5 krogov, vsak natanko 1 zmagovalka
# Varnostni sklop: poti le znotraj /home/user/knowledge; brez eval/exec/omrezja.
KOREN=/home/user/knowledge
TD="$KOREN/stroj-orodja/.geniza/TEST-trk-$$-$(date -u +%H%M%S)"
mkdir -p "$TD"
KROGI="${2:-5}"
[ "$1" = "--samopreizkus" ] && KROGI=5
dobri=0
k=0
while [ "$k" -lt "$KROGI" ]; do
  k=$((k+1))
  ATO="$TD/atom-sigma-TEST-$k.txt"
  ( set -C; : > "$ATO" ) & p1=$!
  ( set -C; : > "$ATO" ) & p2=$!
  wait "$p1"; r1=$?
  wait "$p2"; r2=$?
  zm=$(( (r1 == 0) + (r2 == 0) ))
  [ "$zm" = 1 ] && dobri=$((dobri+1))
  echo "krog $k : zmagovalk $zm ( $r1 ⏇ $r2 ) $([ "$zm" = 1 ] && echo '⊢' || echo '⚠')"
done
rm -rf "$TD"
echo "TRK-JAJCE : krogov natanko-1-zmagovalka $dobri od $KROGI"
[ "$dobri" = "$KROGI" ] && { echo "SODBA : SEW ⊢"; exit 0; }
echo "SODBA : PADC ⚠"; exit 1
