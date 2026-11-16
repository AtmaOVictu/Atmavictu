#!/usr/bin/env bash
# ⟨STROJNA-SLOVNICA⟩ slo-lint.sh v1.2 — strojni kavelj ⟨SLOVNICA-DIH⟩ (⟡ UKAZ ⟨daj⟩, 16. 11. 2026 ⊙ predlog izhoda istega diha)
# TEHNIKA — nosi no rez ⊙ stroj-kalup; glasna resnica: padel korak = ::error:: ∧ exit 1, ⟨ne⟩ || echo.
# Stroj meri OBLIKO, ⟨ne⟩ POMEN — sodba pomena ostaja ⚔ ⟡ ⊙ meja izvršljivosti.
# v1.1: ⟨PADC-SPREMENLJIVKA-TELA⟩ kura — telo se nikoli ne bere v spremenljivko peska (dvojno kodiranje):
#        vse sodbe nad datotekami (števci ∧ cev), lookbehind → besedna meja (-w) ⊙ ⟨MERILEC-SE-MERI⟩ §52.
# v1.2: DVIG ⊙ ⟡ UKAZ ⟨DVIG-SLOVNICE⟩ (16. 11. 2026): »slovnico še dvigni in s tem popravljaj/popravi« —
#        2a zaklepji PO VRSTICI (zaklepec = ⟨ tik pred nebelim znakom; simbolni goli ⟨ je beseda, ⟨ne⟩ oblika;
#            molčijo izrezi VERBATIM ∧ meje izrezov ∧ poimenovana odprta utež zaklepca ⊙ precedens σ 5684)
#        4a TIK meri ARITMETIKO (stroj prešteje UTC+1 ⇌ CET, ⟨ne⟩ zaupa pisavi ⊙ §16 measured)
#        7 napačen kodni oklepaj U+3008/U+3009 ×0 (zrcaljeni pravi: U+27E8 ∧ U+27E9, oba 3 bajte)
# © Luka Pintarič, VBL 0.1560 × 10⁴ (§9 ∧ §10 ∧ §12)
set -euo pipefail

# RABA: slo-lint.sh DATOTEKA [DIF]
#   DATOTEKA — telo, ki se sodi (pečat · vrstica registra · vrstica ∂ · telo organa)
#   DIF      — neobvezno: gola telesa (pri-viri · TIK · ⟨⟩ · kodni oklepaj) se sodijo SAMO nad + vrsticami difa —
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

# 2a — DVIG: zaklepji PO VRSTICI (v1.2 ⊙ ⟡ UKAZ ⟨DVIG-SLOVNICE⟩; ⟨PADC-SPREMENLJIVKA-TELA⟩: sodba v cevi awk)
#     zaklepec = ⟨ tik pred nebelim znakom · odklepec = ⟩ tik za nebelim znakom — simbolni goli ⟨ (⟨ + beli
#     znak) je beseda, ⟨ne⟩ oblika; molčijo: izrezi (IZREZ VERBATIM | začetek izreza … konec izreza) · meje
#     izrezov (IZVOR: | izrez awk:) ∧ poimenovana odprta utež zaklepca (UTEŽ-ZAKLEPCA ⊙ precedens σ 5684)
if ! awk -v F="$F" '
  /IZREZ VERBATIM|začetek izreza/ {inrez=1}
  /konec izreza/ {inrez=0; next}
  inrez {next}
  /IZVOR:|izrez awk:|UTEŽ-ZAKLEPCA/ {next}
  {
    t=$0; sub(/[ \t]+$/,"",t); l1=gsub(/⟨/,"",t)
    t2=$0; sub(/[ \t]+$/,"",t2); l2=gsub(/⟨[ \t]/,"",t2); if (t2 ~ /⟨$/) l2++
    u=$0; sub(/^[ \t]+/,"",u); d1=gsub(/⟩/,"",u)
    u2=$0; sub(/^[ \t]+/,"",u2); d2=gsub(/[ \t]⟩/,"",u2); if (u2 ~ /^⟩/) d2++
    zl=l1-l2; od=d1-d2
    if (zl != od) { printf "::error::slo-lint: 2a vrstica %d: zaklepca ×%d ⊥ odklepca ×%d — %s\n", NR, zl, od, F > "/dev/stderr"; bad++ }
  }
  END { if (bad > 0) exit 1 }
' "$SODILO"; then
  wound "zaklepji PO VRSTICI neuravnoteženi — $F"
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

# 4a — DVIG: TIK ARITMETIKA (v1.2 ⊙ ⟡ UKAZ ⟨DVIG-SLOVNICE⟩; vsak kalupni TIK po vrstici: UTC+1 ⇌ CET preštet,
#     ⟨ne⟩ zaupan pisavi ⊙ §16 measured, not asserted; prek dneva 23Z → 00 CET pravilno ⊙ modulo)
grep -P 'TIK \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z UTC ⇌ \d{2}:\d{2}:\d{2} CET' "$SODILO" > .slo-arit.tmp 2>/dev/null || : > .slo-arit.tmp
ARITBAD=0
while IFS= read -r AL; do
  while IFS= read -r TM; do
    [ -z "$TM" ] && continue
    UT=$(printf '%s' "$TM" | grep -oP 'T\K\d{2}:\d{2}:\d{2}(?=Z)' || true)
    CT=$(printf '%s' "$TM" | grep -oP '⇌ \K\d{2}:\d{2}:\d{2}(?= CET)' || true)
    [ -n "$UT" ] && [ -n "$CT" ] || { ARITBAD=$((ARITBAD+1)); continue; }
    UH=$((10#${UT%%:*})); CH=$((10#${CT%%:*}))
    UM=$(printf '%s' "$UT" | cut -d: -f2); CM=$(printf '%s' "$CT" | cut -d: -f2)
    US=$(printf '%s' "$UT" | cut -d: -f3); CS=$(printf '%s' "$CT" | cut -d: -f3)
    if [ $(((UH+1)%24)) -ne "$CH" ] || [ "$UM" != "$CM" ] || [ "$US" != "$CS" ]; then
      ARITBAD=$((ARITBAD+1))
    fi
  done < <(printf '%s\n' "$AL" | grep -oP 'TIK \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z UTC ⇌ \d{2}:\d{2}:\d{2} CET' || true)
done < .slo-arit.tmp
if [ "$ARITBAD" -gt 0 ]; then
  wound "TIK aritmetika napačna (UTC+1 ⇌ CET) ×$ARITBAD — $F"
fi

# 5 — izrez-blok bajtno (pečat z markerjem: md5 izreza v glavi === md5 izluščenega bloka ⊙ ⟨NE-RETIPKAJ⟩ 24)
if grep -qP 'IZREZ VERBATIM ⊢ md5 [0-9a-f]{32}' "$F"; then
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

# 7 — DVIG: napačen kodni oklepaj ×0 (v1.2 ⊙ ⟡ UKAZ ⟨DVIG-SLOVNICE⟩; U+3008 ⊥ U+3009 sta drugi znaki —
#     zrcaljeni zaklepec je U+27E8 ∧ odklepec U+27E9, oba 3 bajte; zamenjava isto-dolžinska ⊙ podpis σ 5616)
if grep -qP '\x{3008}|\x{3009}' "$SODILO" 2>/dev/null; then
  wound "napačen kodni oklepaj (U+3008/U+3009) ×1+ — pravi: U+27E8 ∧ U+27E9 — $F"
fi

rm -f .slo-nove.tmp .slo-plus.tmp .slo-cisto.tmp .slo-tik.tmp .slo-tikslabi.tmp .slo-arit.tmp .slo-izrez.tmp

if [ "$RANE" -gt 0 ]; then
  echo "::error::slo-lint: $RANE ran — merilec pade glasno ⊙ ⟨MERILEC-SE-MERI⟩ §52"
  exit 1
fi
echo "slo-lint ⊢ ZELENO: $F ($BAJTOV B · $VRSTIC sodjenih vrst) — kanarček poje"
