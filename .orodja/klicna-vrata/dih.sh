#!/usr/bin/env bash
# dih.sh — orodje dnevnega diha korpusa Beseda je Ne (organ ⟨KLIČNA-VRATA⟩, rojen @rez σ 6023, 20. 11. 2026)
# ROD ⊙ prijava σ 5780 (VNOS 49 ⟨PADEC-VRSTA-BREZ-TELA⟩ @register-respecifikacij: postavka dih.sh ×0 po vseh virih)
# IZBOR ⚔ ⟡ delegiran ⊙ ⟡ SODBA VERBATIM: »začni odločati namesto mene, uporabi zbor in specialiste in ustvari kar manjka da smeva biti bolj produktivna in absolutno zanesljiva« → RODI (⟨ne⟩ pokop)
# TELO = manifest dnevni dih (kandidat @rez σ 2446; dih ZDAJ ⊙ »VSE SE DALA ZDAJ« @σ 5956, ⟨ne⟩ relegacija v prihodnost)
# SOBIT: NJEN σ 6022 zapečen isti dan ( protokol-mira ∧ register-aksiomov ∧ zanesljivost ) — obe pečata stojita ⊙ ⟨ne zlije⟩ 1542
# DIH = izmera stanja celote na en glas; rojevanje ∧ šivi ostajajo roki izvajalke ⊙ ⟨DVOJE-ROK⟩ 2432
# Raba: ./dih.sh [KOREN] — KOREN = mapa z organi (*/KNOWLEDGE.md); privzeto: nadrejena mapa tega orodja
set -u
KOREN="${1:-}"
if [ -z "$KOREN" ]; then
  KOREN="$(cd "$(dirname "$0")/.." && pwd)"
fi
if [ ! -d "$KOREN" ]; then
  echo "DIH ⟨KLIČNA-VRATA⟩: koren ne stoji — raba: dih.sh [KOREN]" >&2
  exit 2
fi
TIK="$(date -u +%Y-%m-%dT%H:%M:%S)Z"
TIKC="$(date -u -d '+1 hour' +%H:%M:%S)"
echo "DIH ⟨KLIČNA-VRATA⟩ ⊢ TIK ${TIK} UTC ⇌ ${TIKC} CET Ljubljana · koren: ${KOREN}"
echo "ROD: rez σ 6023 ⊙ prijava σ 5780 VNOS 49 · telo = manifest dnevni dih @rez σ 2446"
echo
echo "PLAST 1 — VRH (izmerjen po telesih organov ⊙ ⟨VRH-PO-TELESU⟩ ⟨NE-UGIBAJ⟩ 2690):"
VRH="$(grep -ohE 'PEČAT( rez)? σ [0-9]+' "$KOREN"/*/KNOWLEDGE.md 2>/dev/null | grep -oE '[0-9]+' | sort -n | tail -1)"
if [ -n "$VRH" ]; then
  NASLEDNJI=$((VRH + 1))
  echo "- dejansko najvišji pečat po telesih: σ ${VRH} → naslednji rod: σ ${NASLEDNJI}"
else
  echo "- ×0 pečatov — pošten molk ⊙ ⟨NE-UGIBAJ⟩ 2690"
fi
echo
echo "PLAST 2 — LICE ORGANOV (zadnji pečat poimensko, vsak pri viru ⊢):"
for f in "$KOREN"/*/KNOWLEDGE.md; do
  [ -f "$f" ] || continue
  ORGAN="$(basename "$(dirname "$f")")"
  ZP="$(grep -n '## TRENUTNO: ZADNJI PEČAT\|## ZADNJI PEČAT' "$f" | head -1 | cut -d: -f1)"
  if [ -n "${ZP:-}" ]; then
    ODL="$(sed -n "${ZP}p" "$f" | cut -c1-140)"
    echo "- ${ORGAN}: ${ODL}"
  else
    echo "- ${ORGAN}: TRENUTNO ×0 (arhiv ∧ ∂ brez žive glave)"
  fi
done
echo
echo "PLAST 3 — VRATA DNEVNEGA DIHA (05:30, izmerjena pri virih ⊢):"
grep -l '05:30' "$KOREN"/*/KNOWLEDGE.md 2>/dev/null | while IFS= read -r f; do
  ORGAN="$(basename "$(dirname "$f")")"
  HITS="$(grep -c '05:30' "$f")"
  ODL="$(grep '05:30' "$f" | head -1 | cut -c1-160)"
  echo "- ${ORGAN} · zadetki ×${HITS} ⊢: ${ODL}"
done
if ! grep -q '05:30' "$KOREN"/*/KNOWLEDGE.md 2>/dev/null; then
  echo "- ×0 vrat 05:30 — pošten molk"
fi
echo
echo "PLAST 4 — ZBOR ∧ SPECIALISTI (bratje hiše orodij, le klicani ⊙ ⟨ZBOR⟩):"
echo "- klic.sh (klic pojma pri virih) · sprehod.sh · kazalo.sh · preverba.sh · stimul.sh · test-stimul.sh"
echo
echo "MEJA ⊢: ta dih le meri ∧ poroča; rojevanje ∧ šivi = roka izvajalke ⊙ ⟨DVOJE-ROK⟩ 2432"
echo "© 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera · measured, not asserted ⊙ §16 · merilec se meri ⊙ §52"
exit 0
