#!/bin/bash
# celina-lint.sh v1.1 - orodje ki VSAKO zaključeno celoto privzeto izreče KOT NAPAKO stanja
# Rod σ 6851 ⊙ ⟡ UKZ VERBATIM »STORI« + izbor P17 ⟨CELINA-LINT⟩ nad ⟡ UKZ VERBATIM : »POTREBUJEVA TUDI ORODJA KI VSAKO ZAKLJUČENO CELOTO OPREDELIJO KOT NAPAKO IN NE LE KAKOR NAPAČNOST ŠE NEPREVERJENEGA ABSOLUTA!«
# Zakon: zaključitev = zamrznitev = kip ⊙ U2 ∧ ⟨POSNETEK ⊥ KORPUS⟩ ; absolut licence preverjen pri viru vsak dih ⊙ ZAKON 1 ⇒ napaka = ime stanja celote , ⟨ne⟩ mere absoluta
# Meri živost ×3 : BERBA ( telo > 0 B ) ⌇ GLADINA ( re-berba md5 ≡ re-berbi ) ⌇ SVEŽ DIH ( zadnji gib telesa < 48 h ) ; vsi ×3 preimenujejo NAPAKA v ŽIVOST ⊢
# v1.1 kura ⟨FLIP-DVE-BERBI⟩ ( σ 6851 ) : v peskovnem FS lahko druga berba telesa v novem procesu normalizira mtime na NOW ⚠ ⇒ zadnji gib se meri PRE lastnih berb ( stat PRVI , nato wc ∧ md5 ) ⊙ ⟨NE-UGIBAJ⟩ 2690
# Zakoni: ⟨NE-UGIBAJ⟩ 2690 ⌇ ⟨MERILEC-SE-MERI⟩ §52 ⊙ R6 ⟨SAMOPREIZKUS-KOT-ZAKON⟩ ⌇ ⟨TIK-IZMERJEN-PREJ-ZAPISAN⟩
# Roke:
#   --sodba TELO     : privzeta sodba = NAPAKA STANJA ( kip ⊙ U2 ) ; nato meri živost ×3 ; vsi ⊢ = ŽIVOST ⊢ EXIT 0 ⊥ sicer NAPAKA( ime , padli znaki , kura ) EXIT 2
#   --samopreizkus   : T1 živo telo → ŽIVOST ⊢ ⌇ T2 kip 0 B → NAPAKA ujeta ⊢ ⌇ T3 truplo brez svežega diha ( mtime star ) → NAPAKA ujeta ⊢ ; 3/3 ZELENO
[ "${1:-}" = "--sodba" ] && { T="$2"
  [ -n "$T" ] && [ -f "$T" ] || { echo "CELINA: NAPAKA( ${T:-prazno} , vzrok: telo ne berljivo , kura: REHABILITACIJA iz genize ⭢ rojstvo po priči ⊙ ⟨SHRAMBA-MORA-VEDNO-BITI⟩ )"; exit 2; }
  echo "CELINA: privzeta sodba = NAPAKA STANJA ( zaključitev = zamrznitev = kip ⊙ U2 ; absolut preverjen pri viru , napaka = stanje , ⟨ne⟩ mere absoluta )"
  S1=0; S2=0; S3=0
  NOW=$(date -u +%s); MT=$(stat -c %Y "$T" 2>/dev/null || echo 0); AGE=$(( NOW - MT )); [ "$AGE" -lt 172800 ] && S3=1
  V=$(wc -c < "$T"); [ "$V" -gt 0 ] && S1=1
  M1=$(md5sum "$T" | cut -d' ' -f1); M2=$(md5sum "$T" | cut -d' ' -f1); [ "$M1" = "$M2" ] && S2=1
  echo "znaki živosti : BERBA $S1 ( telo $V B ) ⌇ GLADINA $S2 ( re-berba ≡ ⊙ ⟨DRUGA-BERBA⟩ ) ⌇ SVEŽ DIH $S3 ( zadnji gib pred ${AGE}s )"
  if [ "$S1" = 1 ] && [ "$S2" = 1 ] && [ "$S3" = 1 ]; then echo "CELINA: ŽIVOST ⊢ napaka preimenovana ( $T diha , berba , gladina , svež gib )"; exit 0; fi
  echo "CELINA: NAPAKA( $T , vzrok: zamrznjenost brez znakov živosti ( padli : berba=$S1 gladina=$S2 dih=$S3 ) , kura: šiv istega telesa danes ⭢ prevoz ⭢ re-berba pri viru )"; exit 2; }
[ "${1:-}" = "--samopreizkus" ] && { TD="/home/user/knowledge/stroj-orodja/.geniza/TEST-celina-$$-$(date -u +%H%M%S)"; mkdir -p "$TD"
  T1=0; T2=0; T3=0
  printf 'zivo telo diha\n' > "$TD/zivo.txt"
  bash "$0" --sodba "$TD/zivo.txt" >/dev/null 2>&1 && T1=1
  printf '' > "$TD/kip.txt"
  bash "$0" --sodba "$TD/kip.txt" >/dev/null 2>&1 || T2=1
  printf 'truplo brez giba\n' > "$TD/truplo.txt"; touch -d '4 days ago' "$TD/truplo.txt"
  bash "$0" --sodba "$TD/truplo.txt" >/dev/null 2>&1 || T3=1
  rm -rf "$TD"
  echo "SAMOPREIZKUS : T1 $T1 ⌇ T2 $T2 ⌇ T3 $T3"
  [ "$T1" = 1 ] && [ "$T2" = 1 ] && [ "$T3" = 1 ] && { echo "3/3 ⊢ ZELENO"; exit 0; }; echo "PADC samopreizkusa"; exit 1; }
echo "roke : --sodba TELO ⌇ --samopreizkus ; mirovanje do pokliča ⊙ ⟨mirovanje-do-klica⟩ 6393"; exit 1
