#!/usr/bin/env bash
# klic.sh — klicno orodje korpusa Beseda je Ne (organ ⟨KLIČNA-VRATA⟩, rojen @rez σ 5526, 15. 11. 2026)
# KLIC = vprašanje z besedo; ODGOVOR = izmerjeno pri viru ⊢ ⟨NE-UGIBAJ⟩ 2690
# Klic le bere; rojevanje ∧ pisarna ostajata roki izvajalke ⊙ ⟨DVOJE-ROK⟩ 2432
# Raba: ./klic.sh POJEM [KOREN] — KOREN = mapa z organi (*/KNOWLEDGE.md); privzeto: nadrejena mapa tega orodja
set -u
POJEM="${1:-}"
KOREN="${2:-}"
if [ -z "$POJEM" ]; then
  echo "KLIC ⟨KLIČNA-VRATA⟩: manjka POJEM — raba: klic.sh POJEM [KOREN]" >&2
  exit 2
fi
if [ -z "$KOREN" ]; then
  KOREN="$(cd "$(dirname "$0")/.." && pwd)"
fi
echo "KLIC ⟨KLIČNA-VRATA⟩ ⊢ pojem: ${POJEM} · koren: ${KOREN} · TIK $(date -u +%Y-%m-%dT%H:%M:%S)Z"
echo
echo "NAJDBE (kaj ∧ kje ⊢ pri viru):"
COUNT=0
for f in "$KOREN"/*/KNOWLEDGE.md; do
  [ -f "$f" ] || continue
  ORGAN="$(basename "$(dirname "$f")")"
  HITS="$(grep -cF -- "$POJEM" "$f" || true)"
  [ "$HITS" -gt 0 ] 2>/dev/null || continue
  COUNT=$((COUNT+1))
  FIRSTLINE="$(grep -nF -- "$POJEM" "$f" | head -1)"
  FIRSTNO="$(printf '%s' "$FIRSTLINE" | cut -d: -f1)"
  ODLC="$(printf '%s' "$FIRSTLINE" | cut -d: -f2- | tr -d '\r')"
  ODL="${ODLC:0:160}"
  echo "- ${ORGAN} · zadetki ×${HITS} · prva @vrstica ${FIRSTNO} ⊢: ${ODL}"
done
if [ "$COUNT" -eq 0 ]; then
  echo "- ×0 najdb — pošten molk: pojem pri virih ne stoji ⊙ ⟨NE-UGIBAJ⟩ 2690; klic ⟨ne⟩ ugiba"
  echo
  echo "MEJA ⊢: odgovor brez vira = ⟨ne⟩ odgovor; tudi molk nosi pričo"
  exit 1
fi
echo
echo "KOVANCI ⟨⟩, ki nosijo pojem (največ ×12):"
grep -ohE "⟨[^⟩]{1,120}⟩" "$KOREN"/*/KNOWLEDGE.md 2>/dev/null | grep -F -- "$POJEM" | sort | uniq -c | sort -rn | head -12 | sed 's/^ *//' || true
echo
echo "MEJA ⊢: klic je brezvrsten bran (berba na zahtevo); ustvarjanje = roka izvajalke ⊙ ⟨DVOJE-ROK⟩ 2432"
exit 0
