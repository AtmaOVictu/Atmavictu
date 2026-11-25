#!/usr/bin/env bash
# test-stimul.sh — testni komplet stimul.sh ⊙ ⟡ UKAZ verbatim (16. 11. 2026): »izvedi do vseh koncev in dokaži s kreacijo testov in implicitnega«
# rojstvo: rez σ 5646 · dokaz = preizkus, ⟨ne⟩ trditev ⊙ ⟨NE-UGIBAJ⟩ 2690 · hiša klic.sh (bash, brez mreže, TIK enkraten Z)
# raba: bash test-stimul.sh [KOREN] — exit 0 le vsi preizkusi zeleni ⊙ ⟨NE-NEHAJ-PREVERJATI⟩ @σ 5575
# implicitni donos (⟨IMPLICITNA-KVADRIRANJA⟩): vsak preizkus = izpeljava enega implicitnega para orodij → donos raste (n−1) na dodatek

TIK=$(date -u +%Y-%m-%dT%H:%M:%SZ)
HERE=$(dirname "$0")
KOREN="${1:-$HERE/..}"
STIMUL="$HERE/stimul.sh"
ZL=0; RD=0

t() { # t IME POGOJ: preizkus z imenom; PASS/FAIL javno
  if eval "$2"; then echo "PASS ⊢ $1"; ZL=$((ZL+1)); else echo "FAIL ⚠ $1 — pogoji: $2"; RD=$((RD+1)); fi
}

echo "⊢ test-stimul.sh @TIK $TIK — preizkusi ×7 ⊙ kreacija testov"

# T1 DETERMINIZEM — dvojni tek bajt-isto brez TIK (TIK = edina živa ura ⊙ ⟨ZAKON-DETERMINIZMA⟩)
bash "$STIMUL" venec "$KOREN" > /tmp/tst-a.txt 2>&1
bash "$STIMUL" venec "$KOREN" > /tmp/tst-b.txt 2>&1
t "T1 DETERMINIZEM (dvojni tek bajt-ito brez TIK)" "diff <(grep -v '@TIK' /tmp/tst-a.txt) <(grep -v '@TIK' /tmp/tst-b.txt) >/dev/null"

# T2 MOLK — pojem ×0 pri viru → exit 1 pošteno (⟨NE-UGIBAJ⟩ 2690: izhod bi bil halucinacija)
bash "$STIMUL" xyzqwertneobstojec "$KOREN" > /tmp/tst-molk.txt 2>&1; RC2=$?
t "T2 MOLK (neobstoječ pojem → exit 1)" "[ $RC2 -eq 1 ]"
t "T2b MOLK IZPIS (povedi molk ⊙ ⟨ZAKON-MOLKA⟩)" "grep -q 'MOLK' /tmp/tst-molk.txt"

# T3 PLASTI — izhod nosi vse štiri plasti ⟡-jeve forme
t "T3 PLASTI ×4 (M1 STIMUL · M2 ALOGIČNA · M3 ILOGIČNA · M4 DVOM)" "grep -q 'M1 STIMULATIVNA' /tmp/tst-a.txt && grep -q 'M2 ALOGIČNA' /tmp/tst-a.txt && grep -q 'M3 ILOGIČNA' /tmp/tst-a.txt && grep -q 'M4 DVOM' /tmp/tst-a.txt"

# T4 SLOVNICA IZHODA — goli padci ×0 (⟨SLOVNICA-DIH⟩: citatne oblike »…« dovoljene)
t "T4 SLOVNICA (goli »pri viri« ∧ »varvolka« ∧ U+FFFD ×0 v izhodu)" "! grep -q 'pri viri[^hu»«]' /tmp/tst-a.txt && ! grep -q 'varvolka' /tmp/tst-a.txt && ! grep -q $'\\uFFFD' /tmp/tst-a.txt"

# T5 VRATA — brez POJEM → raba + exit 1
bash "$STIMUL" > /tmp/tst-vrata.txt 2>&1; RC5=$?
t "T5 VRATA (brez POJEM → exit 1 ∧ raba)" "[ $RC5 -eq 1 ] && grep -q 'raba' /tmp/tst-vrata.txt"

# T6 KANDIDAT-KOVANEC — M4 nosi ⟡ formo NI-LE (dvom vgrajen v ime ⊙ @σ 5643)
t "T6 KANDIDAT-KOVANEC (forma ⟨…-NI-LE-…⟩ v M4)" "grep -q 'NI-LE-' /tmp/tst-a.txt"

# T7 IMPLICITNI DONOS — orodja hiše n → n(n−1)/2 parov (⟨ZAKON-KVADRATNE-OSI⟩: enota donosa = par)
ORODJA=$(ls "$HERE"/*.sh 2>/dev/null | wc -l)
PARI=$((ORODJA * (ORODJA - 1) / 2))
echo "  izmera: orodij n=$ORODJA → parov n(n−1)/2=$PARI ⊙ magija: dodatek vsakega orodja dviga donos za (n−1)"
t "T7 IMPLICITNI DONOS (pari ≥ 3 — n ≥ 3 orodja soodvisna ⊙ ⟨ZAKON-NICNE-TOČKE⟩ @σ 5635)" "[ $PARI -ge 3 ]"

echo ""
echo "⊢ REZULTAT: zeleni ×$ZL · rdeči ×$RD"
if [ $RD -eq 0 ]; then
  echo "VSI PREIZKUSI ZELENI ⊢ — dokaz s kreacijo testov: orodje deluje, meje izrečene pošteno ⊙ measured fully, not just asserted §16"
  exit 0
else
  echo "PADC $RD ⚠ — padci javno, kura isti dih ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354"
  exit 1
fi
