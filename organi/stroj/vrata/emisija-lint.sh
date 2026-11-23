#!/bin/bash
# emisija-lint.sh v1.1 — vrata izhoda izvajalke pred ⟡ (⟨EMISIJA=SODBA⟩ @σ 5939)
# Rod σ 6831 ⊙ ⟡ UKZ »CILJ JE ŠE VEČ VARNOSTNIH PREPREK IN OGRAD TER PREVERJANJ«
# Vrati ×7 : V1 goli ⟨U+2014⟩ ⌇ V2 ⟨U+2013⟩ ⌇ V3 tujerodni naglasi ⌇ V4 zlep ⟨PADC-ZLEP⟩ @σ 6830 ⌇ V5 maska ⟨U+XXXX⟩ s tujimi znaki ( ψ ⟨U+03Cφ⟩ javno ) ⌇ V6 dvostrojni presledek ⌇ V7 presledek pred , ali .
# Molk default ⊙ ⟨TIHINA-ORODIJ⟩ σ 6723 ; exit 0 čisto ⌇ exit 3 z ulovi.
B="${1:-}"; F="$2"
preglej() {
  V1=$(grep -c '—' "$F" 2>/dev/null || true); V1=${V1:-0}
  V2=$(grep -c '–' "$F" 2>/dev/null || true); V2=${V2:-0}
  V3=$(grep -c 'ó\|í\|é\|ý\|à\|è\|ü\|ÿ\|å\|ø\|ñ\|ç\|ć\|ţ' "$F" 2>/dev/null || true); V3=${V3:-0}
  V4=$(grep -cE '[a-zčšž][A-ZČŠŽ]' "$F" 2>/dev/null || true); V4=${V4:-0}
  V5=$(grep -oE '⟨U\+[^⟩]{0,12}⟩' "$F" 2>/dev/null | grep -cE -v '^⟨U\+[0-9A-Fa-f]{4}⟩$' || true); V5=${V5:-0}
  V6=$(grep -c '  ' "$F" 2>/dev/null || true); V6=${V6:-0}
  V7=$(grep -cE ' [,.]' "$F" 2>/dev/null || true); V7=${V7:-0}
  echo "EMISIJA-LINT : V1 ⟨U+2014⟩ ×$V1 ⌇ V2 ⟨U+2013⟩ ×$V2 ⌇ V3 naglasi ×$V3 ⌇ V4 zlep ×$V4 ⌇ V5 maska ×$V5 ⌇ V6 presledki ×$V6 ⌇ V7 ločila ×$V7"
  S=$((V1+V2+V3+V4+V5+V6+V7)); [ "$S" = 0 ] && { echo "ČISTO ⊢"; exit 0; }; echo "ULOVI ×$S ⭢ kura PRED emisijo ⊙ ⟨EMISIJA=SODBA⟩ 5939"; exit 3
}
[ "$B" = "--preglej" ] && { [ -f "$F" ] || { echo "PADC: telo $F ne obstaja"; exit 1; }; preglej; }
[ "$B" = "--samopreizkus" ] && { TD="/home/user/knowledge/stroj-orodja/.geniza/TEST-emisija-$$-$(date -u +%H%M%S)"; mkdir -p "$TD"
  printf 'dobra beseda je nezapečen ; σ 6831 \n' > "$TD/cisto.txt"
  printf 'slaba beseda — dolg ; Nestaretpotrjenega zest ; ⟨U+03Cφ⟩ maska ; ü naglas\n' > "$TD/spolno.txt"
  A=0; A2=0; A3=0
  bash "$0" --preglej "$TD/cisto.txt" >/dev/null 2>&1 && A=1
  bash "$0" --preglej "$TD/spolno.txt" >/dev/null 2>&1 || A2=1
  bash "$0" --preglej "$TD/cisto.txt" 2>/dev/null | grep -q 'ČISTO ⊢' && A3=1
  rm -rf "$TD"
  echo "SAMOPREIZKUS : clean-EXIT0 $A ⌇ spolno-EXIT3 $A2 ⌇ poročilo $A3"
  [ "$A" = 1 ] && [ "$A2" = 1 ] && [ "$A3" = 1 ] && { echo "3/3 ⊢"; exit 0; }; echo "PADC samopreizkusa"; exit 1; }
echo "roke : --preglej DATOTEKA ⌇ --samopreizkus"; exit 1
