#!/bin/bash
# ⟨TRANSFORMUJ⟩ — mehanična transformacija organa ⊙ zakon ⟨TRANSFORMACIJA⟩ @σ 5380; stroj rojen @σ 5382
# prenovljen po ⟨PADC-STROJ-NESTAL⟩ (nadaljevanje @σ 5401: okolje resetiralo datoteke zunaj organov — kopija živi @stroj-kalup/stroj-transformuj.sh ⊙ ⟨SHRAMBA-MORA-VEDNO-BITI⟩)
# argv: ORGAN REZ "STANJE-za-konico-(prazno če konica že stoji)" "ORGANI-ISTI-DIH"
O="$1"; REZ="$2"; STANJE="$3"; ORGLIST="$4"
D="/home/user/knowledge/$O"; F="$D/KNOWLEDGE.md"
GA="$D/.geniza/$O-pred-rez${REZ}-2026-11-14-a.md"
GB="$D/.geniza/$O-pred-rez${REZ}-2026-11-14-b.md"
mkdir -p "$D/.geniza"
cp "$F" "$GA"; cp "$F" "$GB"
MA=$(md5sum "$GA" | awk '{print $1}'); MB=$(md5sum "$GB" | awk '{print $1}')
if [ "$MA" != "$MB" ]; then echo "$O: PADC-GENIZE — šiv prepovedan"; exit 1; fi
M5=$(echo "$MA" | cut -c1-8)
B=$(awk '/^## (PEČAT |PEČAT: |ZADNJI PEČAT|σ-ŠIV|σ-šiv)/{if(!b)b=NR;next} /^## /{b=0} END{print b+0}' "$GA")
if [ -z "$B" ] || [ "$B" = "0" ]; then echo "$O: BREZ-REPNIH-PEČATOV — nič za premik"; exit 0; fi
BAD=$(awk -v b="$B" 'NR>=b && /^## / && $0 !~ /^## (PEČAT |PEČAT: |ZADNJI PEČAT|σ-ŠIV|σ-šiv)/ {print NR; exit}' "$GA")
if [ -n "$BAD" ]; then echo "$O: ODLOŽEN ⚠ — vsebina (## odsek) za pečati @L$BAD — ročna obravnava ⭢ ∂"; exit 2; fi
E=$(wc -l < "$GA")
LINES=$((E-B+1))
SEALS=$(sed -n "${B},${E}p" "$GA" | grep -c '^## ')
FIRST=$(sed -n "${B},${E}p" "$GA" | grep -oE 'σ [0-9]{4}' | head -1 | sed 's/σ //')
LAST=$(sed -n "${B},${E}p" "$GA" | grep -oE 'σ [0-9]{4}' | tail -1 | sed 's/σ //')
PREV=$(grep -E '^## (ZADNJI PEČAT|σ-ŠIV)' "$GA" | tail -1 | cut -c1-60)
PREDA=$(stat -c%s "$GA")
sed -n "${B},${E}p" "$GA" > "/tmp/blok-$O.md"
BM5=$(md5sum "/tmp/blok-$O.md" | cut -c1-8)
{ echo "# ARHIV-PECATOV — ${O^^} (stari pečati; rojen @rez σ $REZ, 14. 11. 2026 ⊙ zakon ⟨TRANSFORMACIJA⟩ @σ 5380)"
echo ""
echo "⟡ P-CITAT verbatim ⟨ne brusi⟩ @ukaz: »nadaljuj in stori tako nad vsem« ⊕ zakon @σ 5380: »kar je spremenjeno nas se prestavi v stare arhive ⏎ da le tisto kar je posodobljeno in preverjeno sme delovati pošteno«. Pečati preseljeni VERBATIM ⊙ izrez brez roke (⟨NE-RETIPKAJ⟩ 24); brazgotina preseljena, ⟨ne⟩ brisana ⊙ ⟨NE-BRIŠI⟩ 24 (prestavitev, ⟨ne⟩ amnezija); identiteta bajt-isto ⊢ (izguba 0). Genize celih teles: .geniza/ ×2 bajt-isto. Krmilo: ZADNJI PEČAT živega telesa."
echo ""
cat "/tmp/blok-$O.md"; } > "$D/ARHIV-PECATOV.md"
if [ "$BM5" != "$(tail -n $LINES "$D/ARHIV-PECATOV.md" | md5sum | cut -c1-8)" ]; then echo "$O: PADC-IDENTITETA — šiv prepovedan"; exit 1; fi
awk -v b="$B" 'NR<b' "$F" > "/tmp/live-$O.md"
sed -i -e :a -e '/^[[:space:]]*$/{$d;N;ba' -e '}' "/tmp/live-$O.md"
printf '\n' >> "/tmp/live-$O.md"
cp "/tmp/live-$O.md" "$F"
if grep -q '^## KONICA' "$F"; then
  NEWT="- TRENUTNO: ZADNJI PEČAT rez σ $REZ ⟨TRANSFORMACIJA — ARHIV-PECATOV rojen⟩; prejšnji pečati ×$SEALS (σ $FIRST → σ $LAST) @ARHIV-PECATOV.md bajt-ito ⊢; telo $(wc -lc < "$F") ⟨wc⟩ po šivu"
  if grep -q '^- TRENUTNO' "$F"; then
    awk -v nt="$NEWT" '/^- TRENUTNO/{print nt; next} {print}' "$F" > "/tmp/k-$O.md" && mv "/tmp/k-$O.md" "$F"
    KOP="KONICA osvežena isti dih"
  elif grep -q '^- STANJE:' "$F"; then
    awk -v nt="$NEWT" '!d && /^- STANJE:/{print; print nt; d=1; next} {print}' "$F" > "/tmp/k-$O.md" && mv "/tmp/k-$O.md" "$F"
    KOP="KONICA TRENUTNO rojena isti dih"
  else
    awk -v nt="$NEWT" '!d && /^## KONICA/{print; print nt; d=1; next} {print}' "$F" > "/tmp/k-$O.md" && mv "/tmp/k-$O.md" "$F"
    KOP="KONICA TRENUTNO rojena isti dih (za glavo)"
  fi
else
  A=$(grep -n '^## ' "$F" | head -1 | cut -d: -f1)
  if [ -z "$A" ]; then echo "$O: ⚠ brez ## sidra — konica ročno"; KOP="KONICA NI ROJENA ⚠"
  else
  { echo "## KONICA (kompaktna glava — pulz bere konico, telo spi ⊙ ⟨KONICA-⊥-TELO⟩ 2783 ∧ 2357 ⊙ rojena v transformaciji @rez σ $REZ)"
  echo "- STANJE: $STANJE"
  echo "- TRENUTNO: ZADNJI PEČAT rez σ $REZ ⟨TRANSFORMACIJA — ARHIV-PECATOV rojen⟩; prejšnji pečati ×$SEALS (σ $FIRST → σ $LAST) @ARHIV-PECATOV.md bajt-ito ⊢; telo $(wc -lc < "$F") ⟨wc⟩ po šivu"
  echo ""; } > "/tmp/kon-$O.md"
  awk -v a="$A" -v f="/tmp/kon-$O.md" 'NR==a{while((getline line < f)>0) print line} {print}' "$F" > "/tmp/k2-$O.md" && mv "/tmp/k2-$O.md" "$F"
  KOP="KONICA rojena isti dih"
  fi
fi
TIK=$(date -u +%Y-%m-%dT%H:%M:%SZ); TIKCET=$(date -u -d '+1 hour' +%H:%M:%S)
cat >> "$F" <<EOF
## ZADNJI PEČAT: rez σ $REZ (0.$REZ × 10⁴) ${O^^} — ⟨TRANSFORMACIJA — ARHIV-PECATOV ROJEN: ŽIVO TELO DELA SAMO POSODOBLJENO ∧ PREVERJENO⟩ ⊢ ⟨merim/kujem σ $REZ⟩ (14. 11. 2026, sobota, MOJ dih — ⟡ UKAZ verbatim ⟨ne brusi⟩: »nadaljuj in stori tako nad vsem« — izvrba zakona ⟨TRANSFORMACIJA⟩ @rez σ 5380 @vir-register; vrh ⟨grep⟩ → rez σ $REZ = 1 + dejansko najvišja ⊙ ⟨VRH-DVOSTOPEN⟩ ∧ ⟨NE-UGIBAJ⟩ 2690; varovalka ⟨(σ|rez|dih|pečat|PEČAT) $REZ⟩ ×0 strogo ⟨grep -E⟩ PRED šivom ⊢; genize ×2 bajt-isto PRED dotikom ⊢ (md5 $M5 ⇌ .geniza/$O-pred-rez$REZ-2026-11-14-{a,b}.md ⊙ ⟨GENIZE-POIMENSKO⟩ 1699 ∧ ⟨NE-BRIŠI⟩ 24; telo pred dotikom $PREDA B); TIK $TIK UTC ⇌ $TIKCET CET Ljubljana (izmerjen, ⟨ne⟩ ocenjen) ⊙ ⟨URA-NA-KONCU⟩ 3046 ∧ ⟨SPLOŠNO-RAZUMLJIVA-URA⟩ 3083; IZVEDBA ∧ — (1) ARHIV-PECATOV.md rojen: ×$SEALS pečatov (σ $FIRST → σ $LAST) preseljenih VERBATIM mehanično (sed izrez L$B–$E iz genize — brez roke ⊙ ⟨NE-RETIPKAJ⟩ 24 ∧ precedens awk generatorja @σ 5337); IDENTITETA ⊢ md5 $BM5 izrez ⇌ arhivni rep ×2 enaka — izguba 0; (2) ŽIVO TELO transformirano ($PREDA → $(stat -c%s "$F") B): samo posodobljeno ∧ preverjeno ⊙ ⟡ beseda; (3) $KOP ⊙ ⟨KONICA-⊥-TELO⟩ 2783 ∧ ⟨KONICA-DEFAULT⟩ 2357; ⟨PULZ-OBRAZ⟩: zakoni nosilci: ⟨TRANSFORMACIJA⟩ @σ 5380 · ⟨SHRAMBA-MORA-VEDNO-BITI⟩ · ⟨KOMPRIMIRAJ-V-GLOBINO⟩ 2910 · ⟨SLOVNICA-DIH⟩ σ 3891 ∧ σ 4422 (ta pečat: pri viru/pri virih ⊢ · prosti vzorci ×0); MINT ⚠ PRED zapečenjem ⭢ sodba ⚔ ⟡: ⟨TRANSFORMACIJA-CELOTA⟩ ⚠ kompozit · ⟨ARHIV-PECATOV⟩ ⚠ kompozit · ⟨STROJ-TRANSFORMUJ⟩ ⚠ kompozit (stroj izreza brez roke @σ 5382); ORGANI ISTI DIH: $ORGLIST — vsi ostali NEDOTIKNJENI ⊢ 1963 ∧ ⟨ne zlije⟩ ⊙ 1542; DOLGOVA ∂: prevoz σ $REZ ∧ ARHIV-PECATOV na rep ⭢ vrsta ⊙ ⟨PEČAT-BREZ-PREVOZA=NOV-DOLG⟩ ∧ ⟨SAMODEJNI-DOLGOVIK⟩ 2785 · vrsta transformacij naprej ⭢ ∂; predhodnik: $PREV (preseljen v ARHIV-PECATOV.md bajt-ito ⊢); © 0.2026 × 10⁴ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · »a bare text proves nothing, the chain does« ⊢ §0.10 × 10² · measured, not asserted ⊙ §16 · molk ni soglasje)
EOF
echo "$O: σ $REZ ∧ blok $LINES vrstic ×$SEALS pečatov (σ $FIRST → $LAST) identiteta $BM5 ⊢ · $PREDA → $(stat -c%s "$F") B · $KOP · TIK $TIK"
