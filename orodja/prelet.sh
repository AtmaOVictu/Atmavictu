#!/bin/sh
# PRELET — orodje ×3 plasti korpusa Beseda je Ne — ROJENO @rez σ 5642 · PAKET-174 (16. 11. 2026)
# IZVOR: ⟡ UKAZ verbatim »več orodij ki pomagajo prepoznavati in graditi iz ter za vzorce in njih rezultate/posledice«
# RABA: sh prelet.sh <datoteka> [pot-vzorcev]  (privzeto: prelet-vzorci.tsv poleg datoteke)
# PLASTI: BESED — kanon ∧ R-razredi iz prelet-vzorci.tsv · ORODIJ — prelet na lastnem registru (zadetki = priče)
# KLASIFIKACIJA: zadetki = IZMERE; GOLI ⊥ PRIČE presoja oko ⊙ σ 5402 (instrument meri z definicijo)
# ZAKON RASTI: vsak ulov ⟡ = nova vrstica prelet-vzorci.tsv ISTI DIH ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354 — rane se ne prosijo, zapisujejo se
# ⟨ORODJE-JE-MERILEC⟩: preizkušen na test-ran pred prvo rabo ⊢ izmera @σ 5642
# BATERIJA ORODIJA (PADC-ORODJA ×3 javno ⊙ ⟨MERILEC-SE-MERI⟩ §52 — ulovljene @samopreizpus):
#   1. busybox awk: napaka večbitnih vrstic → awk izstrojen; tr ∧ uniq ∧ grep nosijo
#   2. busybox ash read: transkodira večbitne bajte (C4 8D → C3 84 C2 8D, izmera od-od) → read izstrojen; sed vrstica + cut polje
#   3. podpičje na drugi podvojeni besedi razdvoji ulov → ločila se ločijo v žetone pred primerjavo

F="$1"
[ -n "$F" ] || { echo "PRELET ⊢ raba: sh prelet.sh <datoteka>"; exit 1; }
[ -f "$F" ] || { echo "PRELET ⊢ napaka: datoteke ni: $F"; exit 1; }
D=$(dirname "$F")
V="${2:-$D/prelet-vzorci.tsv}"
G="$D/prelet-goli.$$"
sed 's/»[^»]*«//g; s/⟨[^⟩]*⟩//g' "$F" > "$G"
echo "== PRELET ⊢ $F"
echo "-- KANON (goli tekst, priče »…« ∧ imena ⟨…⟩ odstranjena):"
for p in 'pri viri[^h]' 'varvolka' 'PEÇAT'; do
  n=$(grep -c -- "$p" "$G" 2>/dev/null); [ -z "$n" ] && n=0
  echo "   $p = $n"
done
n=$(grep -cP '[\x{FFFD}\x{0410}-\x{042F}\x{0430}-\x{044F}]' "$F" 2>/dev/null); [ -z "$n" ] && n=0
echo "   U+FFFD ∧ cirilica = $n"
n=$(grep -c '  ' "$F" 2>/dev/null); [ -z "$n" ] && n=0
echo "   dvojni presledki = $n"
n=$(sed 's/;/ ; /g; s/,/ , /g; s/\. / . /g; s/·/ · /g; s/—/ — /g' "$F" | tr -s ' ' '\n' | uniq -d | grep -v -e '^×0$' -e '^∧$' | grep -cE '[A-Za-z0-9]'); [ -z "$n" ] && n=0
echo "   dvojne besede = $n"
echo "-- R-RAZREDI (iz $V):"
if [ -f "$V" ]; then
  total=$(wc -l < "$V")
  i=0
  while [ "$i" -lt "$total" ]; do
    i=$((i+1))
    row=$(sed -n "${i}p" "$V")
    case "$row" in '#'*|'') continue;; esac
    r=$(printf '%s\n' "$row" | cut -d'|' -f1)
    vz=$(printf '%s\n' "$row" | cut -d'|' -f2)
    k=$(printf '%s\n' "$row" | cut -d'|' -f3)
    [ -n "$r" ] || continue
    n=$(grep -c -- "$vz" "$G" 2>/dev/null); [ -z "$n" ] && n=0
    echo "   $r | $vz = $n | kura: $k"
  done
else
  echo "   (register vzorcev ni najden: $V — R-razredi brez izmere ⊙ ⟨NE-UGIBAJ⟩ 2690)"
fi
rm -f "$G"
echo "== konec preleta ⊢ klasifikacija GOLI/PRIČE = oko"
