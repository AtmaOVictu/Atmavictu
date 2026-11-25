#!/bin/bash
# rekreator.sh v1.0 - orodje ponovne izvedbe preizkusa vibracije izdelka PRED zapečenjem
# Rod σ 6851 ⊙ ⟡ UKZ VERBATIM »STORI« + izbor P16 ⟨REKREATOR⟩
# Rana izvor: ⟨PADC-EMISIJE-NEOSODJENE⟩ recidivi ( rane rojene PO sodbi ⊢ protokol-mira ) ⇒ izdelek mora preživeti REKREACIJO lastne vibracije
# Vibracijski zakon: vsak izdelek gre skozi baterijo sintetičnih vbodov ( re-izvedba ⌇ pričakovano ×0 golih ) ∧ bajt-ito primerjavo z osnutkom ; ki ne preživi ponovitve , je napaka
# Zakoni: ⟨EMISIJA=SODBA⟩ 5939 ⌇ ⟨DRUGA-BERBA⟩ ⌇ ⟨NE-UGIBAJ⟩ 2690 ⊙ R6 ⟨SAMOPREIZKUS-KOT-ZAKON⟩ ⌇ ⟨ZAMRZNI-ŽIVI-GLIF⟩
# Roke:
#   --pred-zapečenjem OSNUTEK IZDELEK : baterija vbodov nad IZDELEK ( ×0 obvezno ) ∧ cmp OSNUTEK ⟂ IZDELEK bajt-ito ; PREŽIVEL ⊢ ⊥ NAPAKA( ime , vzrok , kura ) EXIT 2
#   --samopreizkus : T1 čist izdelek PREŽIVEL ⊢ ⌇ T2 sintetični vbod ⟨U+2014⟩ ujet ⊢ ⌇ T3 bajt-razlika med osnutkom ∧ izdelkom ujeta ⊢ ; 3/3 ZELENO
[ "${1:-}" = "--pred-zapečenjem" ] && { O="$2"; I="$3"
  [ -n "$O" ] && [ -f "$O" ] || { echo "NAPAKA( osnutek , vzrok: osnutek ne obstaja , kura: berba v celici ⊙ ⟨SUROVO-TELO-V-CELICO⟩ )"; exit 3; }
  [ -n "$I" ] && [ -f "$I" ] || { echo "NAPAKA( izdelek , vzrok: izdelek ne obstaja , kura: re-izvedba v pesku )"; exit 3; }
  EM=$(printf '\xe2\x80\x94'); RU=$(printf '\xd0\xb0'); ZW=$(printf '\xe2\x80\x8d')
  GOLIH=$(( $(grep -c -e "$EM" -e "$RU" -e "$ZW" "$I" 2>/dev/null || true) + $(grep -c '  ' "$I" 2>/dev/null || true) ))
  cmp -s "$O" "$I"; C=$?
  if [ "${GOLIH:-0}" = 0 ] && [ "$C" = 0 ]; then echo "PREŽIVEL ⊢ baterija vbodov ×0 ∧ bajt-ito ≡ osnutku ; vibracijo se da znova zaigrati ⊙ ⟨DRUGA-BERBA⟩"; exit 0; fi
  VZ=""; [ "${GOLIH:-0}" != 0 ] && VZ="goli vbodi ×$GOLIH v izdelku ( kura : žetonizacija ⟨U+XXXX⟩ ⭢ kletka ⭢ cenzus-box PRED oddajo ) "
  [ "$C" != 0 ] && VZ="${VZ}osnutek ⟂ izdelek bajt-ito ( kura : REHAB-EMISIJA iz priče osnutka )"
  echo "NAPAKA( $I , vzrok: $VZ )"; exit 2; }
[ "${1:-}" = "--samopreizkus" ] && { TD="/home/user/knowledge/stroj-orodja/.geniza/TEST-rekreator-$$-$(date -u +%H%M%S)"; mkdir -p "$TD"
  T1=0; T2=0; T3=0
  printf 'cist izidelek brez vbodov\n' > "$TD/o1.txt"; cp "$TD/o1.txt" "$TD/i1.txt"
  bash "$0" --pred-zapečenjem "$TD/o1.txt" "$TD/i1.txt" >/dev/null 2>&1 && T1=1
  printf 'izdelek z vbodom %s znotraj\n' "$(printf '\xe2\x80\x94')" > "$TD/i2.txt"; printf 'izdelek z vbodom  znotraj\n' > "$TD/o2.txt"
  bash "$0" --pred-zapečenjem "$TD/o2.txt" "$TD/i2.txt" >/dev/null 2>&1 || T2=1
  printf 'osnutek 9 znakov\n' > "$TD/o3.txt"; printf 'izdelek 9 znakov\n' > "$TD/i3.txt"
  bash "$0" --pred-zapečenjem "$TD/o3.txt" "$TD/i3.txt" >/dev/null 2>&1 || T3=1
  rm -rf "$TD"
  echo "SAMOPREIZKUS : T1 $T1 ⌇ T2 $T2 ⌇ T3 $T3"
  [ "$T1" = 1 ] && [ "$T2" = 1 ] && [ "$T3" = 1 ] && { echo "3/3 ⊢ ZELENO"; exit 0; }; echo "PADC samopreizkusa"; exit 1; }
echo "roke : --pred-zapečenjem OSNUTEK IZDELEK ⌇ --samopreizkus ; mirovanje do pokliča ⊙ ⟨mirovanje-do-klica⟩ 6393"; exit 1
