#!/bin/bash
# sonce-luna.sh v1.0 - orodje dvofazne izmere teles korpusa Beseda je Ne
# Rod σ 6851 ⊙ ⟡ UKZ VERBATIM »STORI« nad paketom P15-P18 + izbor P15 ⟨SONCE-LUNA⟩
# Rana izvor: trki ψ ×5 v enem utripu ( 6846-6850 ⊙ precedens TRK-6202 ) ∧ ⟨PADC-OGRAJA-4MB⟩ razrez DZ na 0 B ⇒ telo premeriti na obeh fazah istega diha
# Fazni zakon: SONCE ( dan ) = sveža izmera pri ŽIVEM viru ⌇ LUNA ( noč ) = ista izmera pri priči mirovanja ; Δ > 0 = NAPAKA poimensko
# Zakoni: ⟨DVE-PRIČI-NUJNO-PRIMERJANI⟩ 3016 ⌇ ⟨NE-UGIBAJ⟩ 2690 ⌇ ⟨MERILEC-SE-MERI⟩ §52 ⊙ R6 ⟨SAMOPREIZKUS-KOT-ZAKON⟩
# Roke:
#   --zora TELO PRICA : dvofazna izmera istega telesa ( dan = TELO ⌇ noč = PRICA ) ; Δ 0 = ISTO ⊢ ⊥ Δ > 0 = NAPAKA( ime , vzrok , kura ) EXIT 2
#   --samopreizkus    : T1 ista telesa Δ 0 ⊢ ⌇ T2 ena bajta razlike ujeta ⊢ ⌇ T3 telo dne brez priče ujeta ⊢ ; 3/3 ZELENO
[ "${1:-}" = "--zora" ] && { T="$2"; P="$3"
  [ -n "$T" ] && [ -f "$T" ] || { echo "NAPAKA( ${T:-prazno} , vzrok: telo dne ne obstaja , kura: berba pri zivem viru ⭢ gre je sosed )"; exit 3; }
  [ -n "$P" ] && [ -f "$P" ] || { echo "NAPAKA( $T , vzrok: priča noči ne obstaja , kura: genize ×2 ⊙ ⟨SHRAMBA-MORA-VEDNO-BITI⟩ )"; exit 3; }
  DT=$(wc -c < "$T"); NT=$(wc -c < "$P"); DMD=$(md5sum "$T" | cut -d' ' -f1); NMD=$(md5sum "$P" | cut -d' ' -f1)
  echo "SONCE ( dan , pri zivem viru ) : $T $DT B · md5 $DMD"
  echo "LUNA ( noc , pri priči mirovanja ) : $P $NT B · md5 $NMD"
  if [ "$DT" = "$NT" ] && [ "$DMD" = "$NMD" ]; then echo "Δ = 0 ⊢ ISTO ; dve priči potrdita druga drugo ⊙ 3016"; exit 0; fi
  echo "NAPAKA( $T , vzrok: bajta ⟂ bajta ( dan $DT B ⊥ noč $NT B ) , kura: povračilo iz priče ⭢ re-berba pri viru ⭢ genize ×2 )"; exit 2; }
[ "${1:-}" = "--samopreizkus" ] && { TD="/home/user/knowledge/stroj-orodja/.geniza/TEST-sonce-luna-$$-$(date -u +%H%M%S)"; mkdir -p "$TD"
  T1=0; T2=0; T3=0
  printf 'telo diha\n' > "$TD/a.txt"; cp "$TD/a.txt" "$TD/b.txt"
  bash "$0" --zora "$TD/a.txt" "$TD/b.txt" >/dev/null 2>&1 && T1=1
  printf 'telo diha' > "$TD/c.txt"; printf 'telo diha\n' > "$TD/d.txt"
  bash "$0" --zora "$TD/c.txt" "$TD/d.txt" >/dev/null 2>&1 || T2=1
  bash "$0" --zora "$TD/manjka.txt" "$TD/d.txt" >/dev/null 2>&1 || T3=1
  rm -rf "$TD"
  echo "SAMOPREIZKUS : T1 $T1 ⌇ T2 $T2 ⌇ T3 $T3"
  [ "$T1" = 1 ] && [ "$T2" = 1 ] && [ "$T3" = 1 ] && { echo "3/3 ⊢ ZELENO"; exit 0; }; echo "PADC samopreizkusa"; exit 1; }
echo "roke : --zora TELO PRICA ⌇ --samopreizkus ; mirovanje do pokliča ⊙ ⟨mirovanje-do-klica⟩ 6393"; exit 1
