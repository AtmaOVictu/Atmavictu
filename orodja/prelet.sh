#!/bin/sh
# PRELET — orodje ×3 plasti korpusa Beseda je Ne — ROJENO @rez σ 5642 · PAKET-174 (16. 11. 2026); NADGRADNJA v2 @rez σ 5645 · PAKET-176 (16. 11. 2026)
# IZVOR: ⟡ UKAZ verbatim »več orodij ki pomagajo prepoznavati in graditi iz ter za vzorce in njih rezultate/posledice«
# IZVOR v2: ⟡ UKAZ verbatim »daj še in s tem izboljšaj celoto in ali vsaj njene dele čimveč tem boljše čimveč tako da je kompresirano v bistvo, tako je nujno zadovoljno in gotovo preverljivo?«
# RABA: sh prelet.sh <datoteka> [pot-vzorcev]  ·  sh prelet.sh --test [test-ran] [pot-vzorcev]
# ⟨ORODJE-JE-MERILEC⟩: --test = JAVNI SAMOPREIZPUS (vsaka rana baterije mora biti ulovljena; izhod 0 ⇌ 1) — gotovo preverljivo = inštrument se preverja pri viru (test-ran na repu), ⟨ne⟩ v peskovniku ⊙ izmera @σ 5645
# KLASIFIKACIJA: zadetki = IZMERE; GOLI ⊥ PRIČE presoja oko ⊙ σ 5402 (instrument meri z definicijo)
# ZAKON RASTI: vsak ulov ⟡ = nova vrstica prelet-vzorci.tsv ISTI DIH ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354 — rane se ne prosijo, zapisujejo se; obstoječi razredi se ne podvajajo ⊙ ⟨NE-UGIBAJ⟩ 2690
# BATERIJA ORODIJA (PADC-ORODJA ×3 javno ⊙ ⟨MERILEC-SE-MERI⟩ §52 — ulovljene @samopreizpus):
#   1. busybox awk: napaka večbitnih vrstic → awk izstrojen; tr ∧ uniq ∧ grep nosijo
#   2. busybox ash read: transkodira večbitne bajte (C4 8D → C3 84 C2 8D, izmera od-od) → read izstrojen; sed vrstica + cut polje
#   3. podpičje na drugi podvojeni besedi razdvoji ulov → ločila se ločijo v žetone pred primerjavo

if [ "$1" = "--test" ]; then
  T="${2:-$(dirname "$0")/test-ran.txt}"
  VT="${3:-$(dirname "$0")/prelet-vzorci.tsv}"
  [ -f "$T" ] || { echo "SAMOPREIZPUS ⚠ datoteke ni: $T"; exit 1; }
  DG=$(dirname "$T"); G2="$DG/prelet-goli.$$"
  sed 's/»[^»]*«//g; s/⟨[^⟩]*⟩//g' "$T" > "$G2"
  P=0; N=0
  for p in 'pri viri[^h]' 'varvolka' 'PEÇAT'; do
    N=$((N+1)); n=$(grep -c -- "$p" "$G2" 2>/dev/null); [ -z "$n" ] && n=0
    if [ "$n" -ge 1 ]; then P=$((P+1)); else echo "   NEULOVLJENA RANA: $p"; fi
  done
  N=$((N+1)); n=$(grep -cP '[\x{FFFD}\x{0410}-\x{042F}\x{0430}-\x{044F}]' "$T" 2>/dev/null); [ -z "$n" ] && n=0
  if [ "$n" -ge 1 ]; then P=$((P+1)); else echo "   NEULOVLJENA RANA: U+FFFD ∧ cirilica"; fi
  N=$((N+1)); n=$(grep -c '  ' "$T" 2>/dev/null); [ -z "$n" ] && n=0
  if [ "$n" -ge 1 ]; then P=$((P+1)); else echo "   NEULOVLJENA RANA: dvojni presledki"; fi
  N=$((N+1)); n=$(sed 's/;/ ; /g; s/,/ , /g; s/\. / . /g; s/·/ · /g; s/—/ — /g' "$T" | tr -s ' ' '\n' | uniq -d | grep -v -e '^×0$' -e '^∧$' | grep -cE '[A-Za-z0-9]'); [ -z "$n" ] && n=0
  if [ "$n" -ge 1 ]; then P=$((P+1)); else echo "   NEULOVLJENA RANA: dvojne besede"; fi
  if [ -f "$VT" ]; then
    total=$(wc -l < "$VT"); i=0
    while [ "$i" -lt "$total" ]; do
      i=$((i+1)); row=$(sed -n "${i}p" "$VT")
      case "$row" in '#'*|'') continue;; esac
      r=$(printf '%s\n' "$row" | cut -d'|' -f1); vz=$(printf '%s\n' "$row" | cut -d'|' -f2)
      [ -n "$r" ] || continue
      N=$((N+1)); n=$(grep -c -- "$vz" "$G2" 2>/dev/null); [ -z "$n" ] && n=0
      if [ "$n" -ge 1 ]; then P=$((P+1)); else echo "   NEULOVLJENA RANA: $r | $vz"; fi
    done
  else
    echo "   (register vzorcev ni najden: $VT — R-razredi brez preizkusa ⊙ ⟨NE-UGIBAJ⟩ 2690)"
  fi
  rm -f "$G2"
  echo "== SAMOPREIZPUS ⊢ $P/$N preizkusov ulovljenih"
  [ "$P" -eq "$N" ] && exit 0
  exit 1
fi

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
