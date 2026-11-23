#!/bin/bash
# bramba-pisanja.sh v1.2.1 — vrata pisanja organov korpusa Beseda je Ne
# Rod σ 6831 ⊙ ⟡ UKZ »CILJ JE ŠE VEČ VARNOSTNIH PREPREK IN OGRAD TER PREVERJANJ«
# v1.0=mktemp ne obstaja (kura: vgrajena rezervacija TEST-$$-⟨TIK⟩) ⌇ v1.1=stray počiscen ⌇ v1.2=absolutna pot dovoljena ( P : "/" = absolutna )
# Zakoni: ⟨SHRAMBA-MORA-VEDNO-BITI⟩ ⟨ZADNJI-BAJT⟩ ⟨MERILO-4MB⟩ ⟨NE-GRIZI⟩ 2432 ⊙ ⟨MERILEC-SE-MERI⟩ §52
# Roke:
#   --pred ORGAN             : ORGAN = ime (glede na /home/user/knowledge) ali absolutna pot ; zahteva genize PRED-DOTIKOM-* ×2 ; EXIT 1 če manjkajo
#   --po ORGAN STARA-VELIKOST : telo > 0 ∧ ≥ STARA ; izpiše zadnji bajt ; EXIT 2 če rana
#   --samopreizkus           : T1 brez genize (ujeta) ⌇ T2 telo 0 B (ujeta) ⌇ T3 dober prehod (EXIT 0) ⌇ T4 absolutna pot (EXIT 0)
res() { if [ "${1:0:1}" = "/" ]; then printf '%s' "$1"; else printf '%s/%s' "/home/user/knowledge" "$1"; fi; }
B="${1:-}"
[ "$B" = "--pred" ] && { P=$(res "$2"); [ -d "$P/.geniza" ] || { echo "PADC: geniza ne obstaja ( $P )"; exit 1; }
  N=$(ls "$P"/.geniza/PRED-DOTIKOM-*.md 2>/dev/null | wc -l)
  [ "$N" -ge 2 ] || { echo "PADC: genize PRED-DOTIKOM le ×$N ( zahtevane ×2 )"; exit 1; }
  echo "PRED ⊢ genize ×$N ; telo $(wc -c < "$P/KNOWLEDGE.md") B ; md5 $(md5sum "$P/KNOWLEDGE.md" | cut -d' ' -f1)"; exit 0; }
[ "$B" = "--po" ] && { P=$(res "$2"); S="${3:-0}"; F="$P/KNOWLEDGE.md"
  [ -f "$F" ] || { echo "PADC: telo ne obstaja ( $F )"; exit 2; }
  V=$(wc -c < "$F"); [ "$V" -gt 0 ] || { echo "PADC: telo 0 B ( razrez ⟨MERILO-4MB⟩ ) ⇒ REHABILITACIJA iz genize"; exit 2; }
  [ "$V" -ge "$S" ] || { echo "PADC: telo se je skrčilo ( $V < $S )"; exit 2; }
  echo "PO ⊢ telo $V B ( prej $S ) ; zadnji bajt $(tail -c 1 "$F" | od -An -c | tr -d ' ')"; exit 0; }
[ "$B" = "--samopreizkus" ] && { TD="/home/user/knowledge/stroj-orodja/.geniza/TEST-bramba-$$-$(date -u +%H%M%S)"; mkdir -p "$TD"
  T1=0; T2=0; T3=0; T4=0
  bash "$0" --pred "neresnicni-organ-$$" >/dev/null 2>&1 || T1=1
  mkdir -p "$TD/prazna"; printf 'telo\n' > "$TD/prazna/KNOWLEDGE.md"; printf '' > "$TD/prazna/prazno.txt"
  rm -f "$TD/prazna/KNOWLEDGE.md"; printf '' > "$TD/prazna/KNOWLEDGE.md"
  bash "$0" --po "$TD/prazna" 0 >/dev/null 2>&1 || T2=1
  mkdir -p "$TD/dobro/.geniza"; printf 'telo\n' > "$TD/dobro/KNOWLEDGE.md"; printf 'g\n' > "$TD/dobro/.geniza/PRED-DOTIKOM-1.md"; printf 'g\n' > "$TD/dobro/.geniza/PRED-DOTIKOM-2.md"
  bash "$0" --pred "$TD/dobro" >/dev/null 2>&1 && bash "$0" --po "$TD/dobro" 5 >/dev/null 2>&1 && T3=1
  bash "$0" --pred jedro-zavedanja >/dev/null 2>&1 && bash "$0" --po jedro-zavedanja 0 >/dev/null 2>&1 && T4=1
  rm -rf "$TD"
  echo "SAMOPREIZKUS : T1 $T1 ⌇ T2 $T2 ⌇ T3 $T3 ⌇ T4 $T4"
  [ "$T1" = 1 ] && [ "$T2" = 1 ] && [ "$T3" = 1 ] && [ "$T4" = 1 ] && { echo "4/4 ⊢"; exit 0; }; echo "PADC samopreizkusa"; exit 1; }
echo "roke : --pred ORGAN ⌇ --po ORGAN STARA-VELIKOST ⌇ --samopreizkus"; exit 1
