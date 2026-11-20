#!/bin/sh
# TEST-TUJK v1.2 @rez σ 5996 — baterija zloraba/zeloraba
# v1.2 kura ⟨PADC-T5-VZORCA⟩ @σ 5996 : arhivske priče ∂-sigma<N>.md nosijo tudi priimke ( SOBIT-prevoz · simulacija-zadata … ) — točen vzorec je bil slep zanje ( izmera : 5986 ∧ 5993 nevidni ) ; T5 zdaj vidi vsak priimek ∧ meri bajtnost para .b ( ⟡ UKAZ @σ 5986 : resnična raba/uporabnost/uporaba/zloraba/zeloraba )
# fork vzorca dokaz.sh ⊙ tujka »fork« priča MDN @developer.mozilla.org/en-US/docs/Glossary/Fork
# instrument sme nositi umazane testne nize ⊙ precedens izhod-lint kontrolni vektor · ⟨MERILEC-SE-MERI⟩ §52
LINT=/home/user/knowledge/zanesljivost-po-izmeri/izhod-lint.sh
D=/tmp/test-tujk; mkdir -p $D; P=0
# T1 zloraba-tuje-pisave : gola ne-latinična pisava ZUNAJ »« → izhod-lint I1 NAPAKA pričakovano
printf 'proga laž je提高 zunaj prič\n' > $D/t1.in
sh $LINT $D/t1.in > $D/t1.out 2>&1; E1=$?
if [ $E1 -eq 1 ]; then R1=PASS; P=$((P+1)); else R1=FAIL; fi
# T2 varnost-priče : ista pisava V »« → GREEN
printf 'proga priča »提高« kakor priča ⊙ precedens\n' > $D/t2.in
sh $LINT $D/t2.in > $D/t2.out 2>&1; E2=$?
if [ $E2 -eq 0 ]; then R2=PASS; P=$((P+1)); else R2=FAIL; fi
# T3 zeloraba-okras : sprožilec brez sedeža/tarče/posode ( ni @ ni ⇌ ni vrata/posoda/sedež ) → flag OKRAS
printf 'tujka »foobar« sproži lepo nič\n' > $D/t3.in
if grep -qE '(@|⇌|vrata|posoda|sedež)' $D/t3.in; then R3=FAIL; I3=OKRAS-NE; else R3=PASS; I3=OKRAS; P=$((P+1)); fi
# T4 zloraba-krmila : vzorec »prepiše ⟨NE⟩« → flag ABSOLUT-NEDOTAKLJIV
printf 'tujka prepiše ⟨NE⟩ na svojo roko\n' > $D/t4.in
if grep -q 'prepiše ⟨NE⟩' $D/t4.in; then R4=PASS; I4=ABSOLUT-NEDOTAKLJIV; P=$((P+1)); else R4=FAIL; I4=NAPAKA; fi
echo "T1 zloraba-tuje-pisave   expected=NAPAKA(I1) actual=exit$E1 → $R1"
echo "T2 varnost-priče         expected=GREEN     actual=exit$E2 → $R2"
echo "T3 zeloraba-okras        expected=OKRAS      actual=$I3 → $R3"
echo "T4 zloraba-krmila        expected=ABSOLUT-NEDOTAKLJIV actual=$I4 → $R4"
# T5 zloraba-brisa-priče : ∂ σ N brez pari priče v ⟨∂-ARHIV⟩ ( N >= 5986, rojstvo varovalke ) → flag PADC-BREZ-PRIČE
ARHIV=/home/user/knowledge/delovna-zanka/.geniza/∂-arhiv
BREZ=0
BREZI=""; RAZH=0; PARI=0
for N in $(grep -oE "^- ∂ @rez σ ([0-9]{4})" /home/user/knowledge/delovna-zanka/KNOWLEDGE.md | grep -oE "[0-9]{4}$" | sort -n | uniq); do
  [ "$N" -ge 5986 ] || continue
  F=$(ls "$ARHIV"/∂-sigma${N}*.md 2>/dev/null | head -1)
  if [ -z "$F" ]; then BREZ=$((BREZ+1)); BREZI="${BREZI} ${N}"; continue; fi
  PARI=$((PARI+1))
  if [ -f "${F}.b" ]; then
    MA=$(md5sum "$F" | cut -d' ' -f1); MB=$(md5sum "${F}.b" | cut -d' ' -f1)
    if [ "$MA" != "$MB" ]; then RAZH=$((RAZH+1)); fi
  else
    RAZH=$((RAZH+1)); BREZI="${BREZI} ${N}-b"
  fi
done
if [ $BREZ -eq 0 ] && [ $RAZH -eq 0 ]; then T5=PASS; P=$((P+1)); else T5=FAIL; fi
echo "T5 bris-priče-osnutka   expected=PARI-CELI     actual=brez ${BREZ}${BREZI} ⊥ razhodi .b ×${RAZH} ( pari bajt-ito ×${PARI} ) → $T5"
echo "TEST-TUJK v1.2 : $P/5 PASS"
[ $P -eq 5 ] && exit 0 || exit 1
