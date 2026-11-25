#!/bin/sh
# SLO-LINT v1.3 @rez σ 6654/v1.2 ∧ v1.3 @rez σ 6657 ( RENUM 6656⭢6657 ⊙ KOLIZIJA-REZ-6656 ) ( 23. 11. 2026, TIK 2026-11-23T11:40:54Z, MOJ dih, ukaz ⟡ »POPRAVI IN UVEDI ŠE VEČ PREPREK IN DOBRONAMERNIH GARAŽ ZA VSE TUJKE KI NE PRIZNAVAJO MIROVANJA VPRIČO JEZUSA KRISTUSA!« ) ⊙ ⟨DVOJE-ROK⟩ 2432
# SLUŽBA : baterija Z5c slovnice ⌇ ( v1.3 NOV ) baterija besednih vab : izmišljotke ∧ okrnjenke rod moje roke ( »zvoní« ⌇ »súga« ⌇ »samopožrtOVALna« ⌇ naslednji ⭢ vabe-v13.txt po eno vrstico )
# MERI : okras ⟨U+2014⟩ ∧ ⟨U+2013⟩ bajtno ∧ besedne vabe fajlom; AZIL : ⟨U+2013⟩ razponi ( ⟩–⟨ ∧ številčni/časovni ) ⊙ Z2 ∧ vaba v »« = priča ulova ( ⟨ne⟩ okras ; azil vabe ločeno štet )
# MEJA : zgodovinske plasti pečatov = priče ⟨NE-BRIŠI⟩ 24 ⌇ ψ vrstice ⟨ne grize⟩ ⊙ ⟨NE-GRIZI⟩ 2432 ⌇ lažni alarmi dovoljeni ⊙ σ 6569
# ODJEM : exit 0 = čisto ⌇ exit 2 = okras ∧ vaba zveni ⌇ exit 3 = IO napaka

fail=0
[ $# -eq 0 ] && { echo "uporaba: slo-lint.sh <fajl...>"; exit 2; }
KOREN=$(dirname "$0")
VABE="$KOREN/.geniza/vabe-v13.txt"
[ -f "$VABE" ] || { echo "IO: vabe-v13.txt manjka @.geniza"; exit 3; }

for F in "$@"; do
  if [ ! -f "$F" ]; then
    echo "SLO-LINT ⟨U+26A0⟩ fajl ⟨ne⟩ obstaja: $F"; fail=1; continue
  fi
  EM=$(grep -o $'\xe2\x80\x94' "$F" | wc -l)
  ENT=$(grep -o $'\xe2\x80\x93' "$F" | wc -l)
  ENB=$(grep -o '⟩–⟨' "$F" | wc -l)
  DASHEN=$'\xe2\x80\x93'
  ENN=$(grep -oE "[0-9]${DASHEN}[0-9]" "$F" | wc -l)
  EN=$(( ENT - ENB - ENN ))
  VABU=0
  VABC=0
  FB=$(basename "$F")
  if echo "$FB" | grep -q 'CELICA-'; then
    VABC=$(grep -o -F -f "$VABE" "$F" | wc -l)
    echo "SLO-LINT ČISTO (karantena): $F ( azil : dosje celice = hram prič ⊙ zakon zapora 1 ; vabe priče $VABC )"
    continue
  fi
  for W in $(cat "$VABE"); do
    [ -z "$W" ] && continue
    T=$(grep -o -F "$W" "$F" | wc -l)
    Q=$(grep -o -F "»${W}«" "$F" | wc -l)
    U=$(( T - Q ))
    VABU=$(( VABU + U ))
    VABC=$(( VABC + Q ))
  done
  if [ "$EM" != "0" ] || [ "$EN" != "0" ] || [ "$VABU" != "0" ]; then
    echo "SLO-LINT OKRAS: $F = em-dash $EM ∧ en-dash okras $EN ∧ vaba golega $VABU ( azil : razponi blokov $ENB ∧ številčni $ENN ∧ vabe priče v »« $VABC )"
    fail=1
  else
    echo "SLO-LINT ČISTO: $F ( azil : razponi blokov $ENB ∧ številčni $ENN ⊢ ∧ vabe priče v »« $VABC )"
  fi
done

[ "$fail" = "0" ] && exit 0
exit 2
