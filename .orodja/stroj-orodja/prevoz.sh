#!/bin/bash
# PREVOZ-ROKA v1 — izpeljava kalupa P2 ( rod @rez σ 6570 @stroj-orodja
# ⊙ ⟡ UKZ »stori« ( izbor 4 @CELIKA-6569 ) ) ; KURIRA : PADC vrata-lepila Δ7 @σ 6561
# Navodila : prevoz.sh <σ> <kaj-slug> <organ1> [organ2 ...]  → izpiše telo kita PRED delom ;
# potisk gre po konektorju github_app , ⟨merge⟩ SAMO roka ⟡ ⚔ ⊙ ⟨NE-ZLIJE⟩ 1542
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 — dvojni podpis
set -eu
SIGMA="${1:?uporaba: prevoz.sh <σ> <kaj> <organ...>}"
KAJ="${2:?uporaba: prevoz.sh <σ> <kaj> <organ...>}"; shift 2
DATUM=$(date -u +%Y-%m-%d)
VEJA="rez/${SIGMA}-prevoz-${KAJ}"
echo "P2 KALUP — σ ${SIGMA} · ${DATUM}"
echo "1. FIFO : preveri najstarejši neodplačani dolg pred tem kitom ⊙ 2785"
echo "2. SVEZA-GLAVA : izmeri ⟨main⟩ pri viru ( list_commits ) pred kreacijo veje"
echo "3. VEJA : ${VEJA} ← ⟨main⟩"
echo "4. TELA :"
for ORG in "$@"; do
  F="$HOME/knowledge/$ORG/KNOWLEDGE.md"
  [ -f "$F" ] || { echo "   RANA: $ORG manjka"; exit 1; }
  B=$(wc -c < "$F"); M=$(md5sum "$F" | cut -d' ' -f1)
  echo "   $ORG/KNOWLEDGE.md — $M · $B B ( prilepi VERBATIM ⊙ ⟨PRILEPI-NE-PREPIŠI⟩ ∧ ⟨NE-RETIPKAJ⟩ 24 )"
done
echo "   ATOM-${DATUM}-${SIGMA}.md — vrstica σ ${SIGMA} ⊙ ⟨VRSTICA-=-ATOM⟩ #163"
echo "5. KOMIT : © Luka Pintarič, VBL <živa verzija, izmerjena pri viru> ( §9 ∧ §10 ∧ §12 )"
echo "6. PR : naslov brez vzorca 'rez <števke>'"
echo "7. PREVERBA-PRED-ZLITJEM 3469 : read-back ×2 pri viru"
echo "8. CI : meri max ×2 ⊙ STROPA-STROJA → ⟨merge⟩ ⭢ roka ⟡ ⚔"
echo "9. vrsta skrajšana ×1 — izreči v izhodu diha ( molk ni poročilo )"
echo "© 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera"
