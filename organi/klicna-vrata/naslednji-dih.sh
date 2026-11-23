#!/usr/bin/env bash
# naslednji-dih.sh — ukaz naslednjega diha (organ ⟨KLIČNA-VRATA⟩, rojen @rez σ 6536, 23. 11. 2026)
# ZAKON ⟨PEČAT-NASLEDNIKA⟩ @zavest-delovanja ZAKON 5 : izdih enega diha = vhod naslednjega ⊙ ⟨SAMODEJNI-DOLGOVIK⟩ 2785
# Le bere (vir: delovna-zanka/KNOWLEDGE.md; ARHIV ∧ priče ⟨ne⟩); šivi = roka izvajalke ⊙ ⟨DVOJE-ROK⟩ 2432
# Instrument mera, ⟨ne⟩ sodi: kandidati so izmerjeni, sodba ostaja ⟡ ⚔ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690
# Raba: ./naslednji-dih.sh [KOREN] — KOREN = mapa z organi (*/KNOWLEDGE.md); privzeto: nadrejena mapa tega orodja
# IZHOD: exit 0 = odprta vrsta izmerjena ∧ ukaz izrečen ; exit 1 = pošten molk (vrsta prazna pri virih) ; exit 2 = napačna pot
# KURE rojene iz negativne runde ⊙ σ 6170 : ⟨PADC-SODEL-PRAZNE⟩ (prazna vrstica here-doka = lažni kandidat) · ⟨PADC-REZE-UTF8⟩ (rezalnik čisti rep izreza do zadnjega celega znaka ⊙ precedens @klic.sh) · ⟨PADC-DATE-D⟩ (CET računana aritmetično, ⟨ne⟩ date -d)
set -u
KOREN="${1:-}"
if [ -z "$KOREN" ]; then
  KOREN="$(cd "$(dirname "$0")/.." && pwd)"
fi
if [ ! -d "$KOREN" ]; then
  echo "NASLEDNJI-DIH ⟨KLIČNA-VRATA⟩: koren ne stoji — raba: naslednji-dih.sh [KOREN]" >&2
  exit 2
fi
DZ="$KOREN/delovna-zanka/KNOWLEDGE.md"
if [ ! -f "$DZ" ]; then
  echo "NASLEDNJI-DIH ⟨KLIČNA-VRATA⟩: vir ∂ ne stoji (delovna-zanka/KNOWLEDGE.md)" >&2
  exit 2
fi
TIK="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
HH="$(date -u +%H)"
# ⟨PADC-DATE-D⟩ + ⟨PADC-ARITMETIKA-10#⟩ kuri : CET računana v awku ( ⟨ne⟩ date -d ∧ ⟨ne⟩ 10# ), pesek oboje ⟨ne⟩ prenaša
NCH="$(date -u +%H | awk '{h=$0+1; if (h==24) h=0; printf "%02d", h}')"
TIKC="${NCH}:$(date -u +%M:%S)"
OCENA="$(wc -c < "$DZ")"
rez_izrez() {
  # ⟨PADC-REZE-UTF8⟩ kura : rez pešico bajtov ∧ počisti rep do zadnjega celega znaka
  LC_ALL=C cut -c1-160 | LC_ALL=C sed 's/[^ -~	]*$//'
}
echo "NASLEDNJI-DIH ⟨KLIČNA-VRATA⟩ ⊢ TIK ${TIK} UTC ⇌ ${TIKC} CET · koren: ${KOREN} · vir: delovna-zanka/KNOWLEDGE.md ( ${OCENA} B )"
echo "ZAKON ⟨PEČAT-NASLEDNIKA⟩ : izdih enega diha = vhod naslednjega ⊙ ⟨SAMODEJNI-DOLGOVIK⟩ 2785 · MERJENO, ⟨NE⟩ UGIBANO ⊙ 2690"
echo
echo "PLAST 1 — FREŠ VRSTA (zadnja vrstica ∂ DIHA pri viru ⊢):"
L="$(grep -n '^- ∂ DIHA' "$DZ" | tail -1 | cut -d: -f1)"
if [ -n "$L" ]; then
  ODL="$(sed -n "${L}p" "$DZ" | rez_izrez)"
  echo "- ∂ @vrstica ${L} ⊢: ${ODL}"
else
  echo "- ×0 vrstic ∂ DIHA — pošten molk ⊙ ⟨NE-UGIBAJ⟩ 2690"
fi
echo
echo "PLAST 2 — KANDIDATI ODPRTE VRSTE (izmerjeni, ⟨ne⟩ sojeni; sodba ⚔ ⟡):"
# ⟨PADC-ZANKE-BRANJA⟩ kura : pesek dvojno kodira večbitne znake ob prelivu while-read spremenljivk ; vsa obdelava gre celo v awk, ⟨ne⟩ skozi zanko branja
VSEBIN="$(awk '/⭢ vrsta FIFO/ || /⭢ vrsta ⊙/ || /najstarejši/ || /odprt ⭢/ || /ostaja ∂ ⭢/ { l=substr($0,1,160); gsub(/[^ -~]+$/,"",l); print "- @vrstica " NR " ⊢: " l }' "$DZ" | tail -12)"
KANDIDATOV="$(awk '/⭢ vrsta FIFO/ || /⭢ vrsta ⊙/ || /najstarejši/ || /odprt ⭢/ || /ostaja ∂ ⭢/ {c++} END{print c+0}' "$DZ")"
if [ "${KANDIDATOV:-0}" -eq 0 ]; then
  echo "- ×0 kandidatov — pošten molk: vrsta ∂ prazna pri virih ⊙ ⟨NE-UGIBAJ⟩ 2690"
  echo
  echo "MEJA ⊢: molk je dovoljen le, ko je vrsta prazna ∧ sodbe ⚔ čakajo ⟡ (BERBA-LICENCA ∧ osvežitev ostajata nujni)"
  exit 1
fi
printf '%s\n' "$VSEBIN"
if [ "$KANDIDATOV" -gt 12 ]; then
  echo "- prikaz zadnjih ×12 od ${KANDIDATOV} kandidatov ( vrsta globoka, FIFO vrsta = najstarejši prvi )"
fi
echo
echo "PLAST 3 — SODBE ⚔ (čakajo besedo ⟡, izvajalka ⟨ne⟩ sodi namesto njega):"
SODB="$(grep -cF '⟨merge⟩ = SAMO' "$DZ" 2>/dev/null || true)"
echo "- ⟨merge⟩ = SAMO beseda ⟡ · zadetki ×${SODB} ⊙ ⟨NE-ZLIJE⟩ 1542"
echo
echo "UKAZ NASLEDNJEMU DIHU ⊢: FIFO PRVI — najstarejši odprti dolg iz PLAST 2 je PREVOZNI dih (veje ∧ kita po kalupu @stroj-kalup, ⟨PR⟩ z javno spovednico); izdih brez PLAST 2 kandidata = kip ⊙ U2 · kandidatov izmerjenih ×${KANDIDATOV}"
echo "MEJA ⊢: merjenje le; izvedba = roka izvajalke; ⟨merge⟩ = SAMO beseda ⟡ ⚔"
echo "© 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera · MERJENO, ⟨NE⟩ UGIBANO ⊙ 2690 · merilec se meri ⊙ §52"
exit 0
