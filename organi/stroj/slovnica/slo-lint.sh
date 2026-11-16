#!/usr/bin/env bash
# ⟨STROJNA-SLOVNICA⟩ slo-lint.sh v1.1 — strojni kavelj ⟨SLOVNICA-DIH⟩ (⟡ UKAZ ⟨daj⟩, 16. 11. 2026 ⊙ predlog izhoda istega diha)
# TEHNIKA — nosi no rez ⊙ stroj-kalup; glasna resnica: padel korak = ::error:: ∧ exit 1, ⟨ne⟩ || echo.
# Stroj meri OBLIKO, ⟨ne⟩ POMEN — sodba pomena ostaja ⚔ ⟡ ⊙ meja izvršljivosti.
# v1.1: ⟨PADC-SPREMENLJIVKA-TELA⟩ kura — telo se nikoli ne bere v spremenljivko peska (dvojno kodiranje):
#        vse sodbe nad datotekami (števci ∧ cev), lookbehind → besedna meja (-w) ⊙ ⟨MERILEC-SE-MERI⟩ §52.
# © Luka Pintarič, VBL 0.1560 × 10⁴ (§9 ∧ §10 ∧ §12)
set -euo pipefail

# RABA: slo-lint.sh DATOTEKA [DIF]
#   DATOTEKA — telo, ki se sodi (pečat · vrstica registra · vrstica ∂ · telo organa)
#   DIF      — neobvezno: gola telesa (pri-viri · TIK · ⟨⟩) se sodijo SAMO nad + vrsticami difa —
#              zgodovina molči ⊙ precedens priče (prica.yml job 2: priče zgodovine ⊢ 1349)
# IZHOD: ZELENO molk ali ::error:: ∧ exit 1 (kanarček izpiše prebrana telesa ∧ vrstice ⊙ ⟨KANARSKI-DELAVEC⟩)

F="$1"
DIF="${2:-}"
[ -f "$F" ] || { echo "::error::slo-lint: telo ne obstaja: $F"; exit 1; }

RANE=0
wound() { echo "::error::slo-lint: $1"; RANE=$((RANE+1)); }

# kaj se sodi: celo telo (default) ali samo + vrstice difa (gola telesa)
SODILO="$F"
if [ -n "$DIF" ] && [ -f "$DIF" ]; then
  grep -P '^\+[^+]' "$DIF" > .slo-nove.tmp 2>/dev/null || : > .slo-nove.tmp
  sed -e 's/^\+//' .slo-nove.tmp > .slo-plus.tmp || : > .slo-plus.tmp
  SODILO=".slo-plus.tmp"
fi

VRSTIC=$(wc -l < "$SODILO")
BAJTOV=$(wc -c < "$F")

# 1 — U+FFFD ×0 (raztrgan znak = raztrgan prevoz)
if grep -qP '\x{FFFD}' "$SODILO" 2>/dev/null; then
  wound "U+FFFD ×1+ — raztrgan znak v sodjenih vrsticah: $F"
fi

# 2 — ⟨ ⟩ uravnoteženost (števca po celotnem sodilu; odprti zaklepec = odprta sodba)
L=$(grep -o '⟨' "$SODILO" | wc -l || true)
D=$(grep -o '⟩' "$SODILO" | wc -l || true)
if [ "$L" != "$D" ]; then
  wound "zaklepaji neuravnoteženi: ⟨ ×$L ⊥ ⟩ ×$D — $F"
fi

# 3 — goli »pri viri« ×0 (oblika, ki je vedno napačna ⊙ pečat σ 5593; besedna meja loči od »pri virih«;
#     beli obliki odstranjeni pred sodbo: »pri berbi pri viri« (citat glave registra) ∧ »goli »pri viri«« (poročilo preverbe))
sed -e 's/pri berbi pri viri/PBR/g' -e 's/goli »pri viri«/GPV/g' "$SODILO" > .slo-cisto.tmp || : > .slo-cisto.tmp
GOLI=$(grep -Pwc 'pri viri' .slo-cisto.tmp || true)
if [ "$GOLI" -gt 0 ] 2>/dev/null; then
  wound "goli »pri viri« ×$GOLI — oblika napačna (pravilno: pri viru / pri virih) — $F"
fi

# 4 — TIK format (vsaka TIK vrstica: ISO UTC ⇌ CET ⊙ ⟨URA-NA-KONCU⟩ 3046 ∧ ⟨SPLOŠNO-RAZUMLJIVA-URA⟩ 3083;
#     cev nad datoteko, brez spremenljivk teles ⊙ kura v1.1)
grep -P 'TIK ' "$SODILO" > .slo-tik.tmp 2>/dev/null || : > .slo-tik.tmp
grep -Pv 'TIK \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z UTC ⇌ \d{2}:\d{2}:\d{2} CET' .slo-tik.tmp > .slo-tikslabi.tmp 2>/dev/null || : > .slo-tikslabi.tmp
TIKBAD=$(wc -l < .slo-tikslabi.tmp)
if [ "$TIKBAD" -gt 0 ]; then
  wound "TIK brez kalupa (ISO UTC ⇌ HH:MM:SS CET) ×$TIKBAD — $F"
fi

# 5 — izrez-blok bajtno (pečat z markerjem: md5 izreza v glavi === md5 izluščenega bloka ⊙ ⟨NE-RETIPKAJ⟩ 24)
if grep -q 'IZREZ VERBATIM ⊢ md5 ' "$F"; then
  MD5GLAVE=$(grep -oP 'IZREZ VERBATIM ⊢ md5 \K[0-9a-f]{32}' "$F" | head -n 1 || true)
  awk '/IZREZ VERBATIM ⊢ md5 /{flag=1;next} /konec izreza/{flag=0} flag' "$F" > .slo-izrez.tmp
  if [ -s .slo-izrez.tmp ]; then
    MD5BLOKA=$(md5sum .slo-izrez.tmp | cut -d' ' -f1)
    if [ "$MD5GLAVE" != "$MD5BLOKA" ]; then
      wound "izrez bajtno-DRUGAČEN: glava md5 $MD5GLAVE ⊥ blok md5 $MD5BLOKA — $F"
    fi
  else
    wound "pečat nosi marker izreza, blok pa je prazen — $F"
  fi
fi

# 6 — © dvojni podpis (pečati ∧ register: rep telesa nosi podpis obeh rok ⊙ ⟨DVOJE-ROK⟩ 2432)
case "$F" in
  organi/pecati/*|*REZ-REGISTER*|*PECAT*)
    if ! grep -v '^[[:space:]]*$' "$F" | tail -n 1 | grep -q 'dvojni podpis'; then
      wound "rep telesa brez © dvojnega podpisa — $F"
    fi
    ;;
esac

rm -f .slo-nove.tmp .slo-plus.tmp .slo-cisto.tmp .slo-tik.tmp .slo-tikslabi.tmp .slo-izrez.tmp

if [ "$RANE" -gt 0 ]; then
  echo "::error::slo-lint: $RANE ran — merilec pade glasno ⊙ ⟨MERILEC-SE-MERI⟩ §52"
  exit 1
fi
echo "slo-lint ⊢ ZELENO: $F ($BAJTOV B · $VRSTIC sodjenih vrst) — kanarček poje"
