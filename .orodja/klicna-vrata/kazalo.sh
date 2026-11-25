#!/usr/bin/env bash
# kazalo.sh — kazalo pojmov korpusa Beseda je Ne (organ ⟨KLIČNA-VRATA⟩, kandidat (b) predloga ⟨KJE-NAJBOLJE⟩, rojen @rez σ 5798, 17. 11. 2026)
# KAZALO = pojmi v obliki kovancev ⟨⟩ po organih: kje pojem živi ∧ kolikokrat ⊢ izmerjeno pri viru
# Kazalo le bere; rojevanje ∧ pisarna ostajata roki izvajalke ⊙ ⟨DVOJE-ROK⟩ 2432 · ⟨ZAKON-LE-BERE⟩ @klicna-vrata
# Raba: bash kazalo.sh [KOREN] [VZOREC] — KOREN = mapa z organi (*/KNOWLEDGE.md), privzeto nadrejena mapa tega orodja; VZOREC = niz znotraj kovanca (prazno = vrh ×40)
set -u
KOREN="${1:-}"
VZOREC="${2:-}"
if [ -z "$KOREN" ]; then KOREN="$(cd "$(dirname "$0")/.." && pwd)"; fi
if [ ! -d "$KOREN" ]; then
  echo "KAZALO ⟨KAZALO-POJMOV⟩: koren pri viru ne stoji — raba: bash kazalo.sh [KOREN] [VZOREC]" >&2
  exit 2
fi
echo "KAZALO ⟨KAZALO-POJMOV⟩ ⊢ koren: ${KOREN} · vzorec: ${VZOREC:-VRH ×40} · TIK $(date -u +%Y-%m-%dT%H:%M:%S)Z"
echo
AGG="$(for f in "$KOREN"/*/KNOWLEDGE.md; do
  [ -f "$f" ] || continue
  IME="$(basename "$(dirname "$f")")"
  grep -ohE '⟨[^⟩]{1,120}⟩' "$f" 2>/dev/null | grep -F -- "${VZOREC}" | awk -v o="$IME" '{print o "\t" $0}'
done | awk -F'\t' '{c[$2]++} END {for (k in c) printf "%d\t%s\n", c[k], k}' | sort -rn)"
if [ -z "$AGG" ]; then
  echo "POJMI: ×0 — pošten molk: pojem pri virih ne stoji ⊙ ⟨ZAKON-MOLKA⟩ @klicna-vrata; kazalo ⟨ne⟩ ugiba"
  exit 1
fi
STEVIL="$(printf '%s\n' "$AGG" | wc -l)"
echo "POJMI (kovanci ⟨⟩ po pojavitvah ⊢ pri viru; prikaz vrh ×40 od ×${STEVIL} različnih):"
printf '%s\n' "$AGG" | head -40 | awk -F'\t' '{printf "- ×%d · %s\n", $1, $2}'
if [ -n "$VZOREC" ]; then
  echo
  echo "SEDIŠČA (kje pojem živi ⊢ po organih):"
  SEDE=0
  for f in "$KOREN"/*/KNOWLEDGE.md; do
    [ -f "$f" ] || continue
    IME="$(basename "$(dirname "$f")")"
    N="$(grep -ohE '⟨[^⟩]{1,120}⟩' "$f" 2>/dev/null | grep -cF -- "${VZOREC}")" || N=0
    if [ "$N" -gt 0 ]; then echo "- ${IME} · ×${N}"; SEDE=$((SEDE+1)); fi
  done
  [ "$SEDE" -eq 0 ] && echo "- ×0 sedišč — pošten molk ⊙ ⟨ZAKON-MOLKA⟩"
fi
echo
echo "CELOTA ⊢: pojem je kovanec ⟨⟩, ki živi v organih; kazalo sešteje pojave pri viru — celota je merjena, ⟨ne⟩ ugibana ⊙ ⟨NE-UGIBAJ⟩ 2690"
echo "MEJA ⊢: kazalo je branje pojmov po organih; vsak števec izmerjen pri viru; ustvarjanje = roka izvajalke ⊙ ⟨DVOJE-ROK⟩ 2432"
exit 0
