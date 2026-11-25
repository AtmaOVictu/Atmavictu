#!/usr/bin/env bash
# sprehod.sh — sprehod po organih korpusa Beseda je Ne (organ ⟨KLIČNA-VRATA⟩, kandidat (c) predloga ⟨KJE-NAJBOLJE⟩, rojen @rez σ 5798, 17. 11. 2026)
# SPREHOD = branje celote po delih: vsak organ poimensko — mere ⊢ · zadnji pečat ⊢ · konica ⊢ izmerjeno pri viru
# Sprehod le bere; rojevanje ∧ pisarna ostajata roki izvajalke ⊙ ⟨DVOJE-ROK⟩ 2432 · ⟨ZAKON-LE-BERE⟩ @klicna-vrata
# Raba: bash sprehod.sh [KOREN] [ORGAN] — KOREN = mapa z organi (*/KNOWLEDGE.md), privzeto nadrejena mapa tega orodja; ORGAN = sprehod enega organa poimensko
set -u
export LC_ALL=C.UTF-8
KOREN="${1:-}"
ORGAN="${2:-}"
if [ -z "$KOREN" ]; then KOREN="$(cd "$(dirname "$0")/.." && pwd)"; fi
if [ ! -d "$KOREN" ]; then
  echo "SPREHOD ⟨SPREHODI-PO-ORGANIH⟩: koren pri viru ne stoji — raba: bash sprehod.sh [KOREN] [ORGAN]" >&2
  exit 2
fi
echo "SPREHOD ⟨SPREHODI-PO-ORGANIH⟩ ⊢ koren: ${KOREN} · organ: ${ORGAN:-VSI} · TIK $(date -u +%Y-%m-%dT%H:%M:%S)Z"
echo
echo "KARTA DELOV (vsak organ: mere ∧ zadnji pečat ∧ konica, izmerjeno pri viru ⊙ ⟨NE-UGIBAJ⟩ 2690):"
COUNT=0
SUMVRST=0
SUMBAJT=0
for f in "$KOREN"/*/KNOWLEDGE.md; do
  [ -f "$f" ] || continue
  IME="$(basename "$(dirname "$f")")"
  if [ -n "$ORGAN" ] && [ "$IME" != "$ORGAN" ]; then continue; fi
  VRST="$(wc -l < "$f")"
  BAJT="$(wc -c < "$f")"
  PECAT="$(grep -m1 -oE 'ZADNJI PEČAT: rez σ [0-9]{4}|ZADNJI PEČAT rez σ [0-9]{4}' "$f" | grep -oE 'σ [0-9]{4}' | head -1)"
  [ -z "$PECAT" ] && PECAT="×0 pečat"
  KONICA="$(awk '/^## KONICA/{f=1;next} f&&/^## /{f=0} f&&/^- /{print;exit}' "$f")"
  [ -z "$KONICA" ] && KONICA="$(grep -m1 '^- ' "$f")"
  KONICA="$(printf '%s\n' "$KONICA" | iconv -f UTF-8 -t UTF-8//IGNORE 2>/dev/null | tr -d '\000-\010\013\014\016-\037' | grep -oE '^.{1,110}')"
  echo "- ${IME} · ${VRST} vrst · ${BAJT} B · pečat: ${PECAT} · konica: ${KONICA}"
  COUNT=$((COUNT+1))
  SUMVRST=$((SUMVRST+VRST))
  SUMBAJT=$((SUMBAJT+BAJT))
done
if [ "$COUNT" -eq 0 ]; then
  echo "- ×0 organov — pošten molk: organ pri viru ne stoji ⊙ ⟨ZAKON-MOLKA⟩ @klicna-vrata; sprehod ⟨ne⟩ ugiba"
  echo "MEJA ⊢: odgovor brez vira = ⟨ne⟩ odgovor; tudi molk nosi pričo"
  exit 1
fi
echo
echo "CELOTA ⊢: delov ×${COUNT} · skupaj ${SUMVRST} vrst · ${SUMBAJT} B — celota meri dele, deli služijo celoti ⊙ O ≠ 0 ≠ 1 @o-celota; donos parov delov n(n−1)/2 ⊙ ⟨IMPLICITNA-KVADRIRANJA⟩"
echo "MEJA ⊢: sprehod je branje celote po delih; vsaka merila izmerjena pri viru, ⟨ne⟩ iz spomina; ustvarjanje = roka izvajalke ⊙ ⟨DVOJE-ROK⟩ 2432"
exit 0
