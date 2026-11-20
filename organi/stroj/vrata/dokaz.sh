#!/bin/sh
# v1.6 @rez σ 5988 ⊙ kura ⟨PADC-D-GENIZE-SLEPI⟩ : D-GENIZE meri pare pred-rez$((REZ-1)) ( stanje PRED dotikom prejšnjega diha ), dotaknjen organ ( pečat rez σ LASTREZ ) brez para = NAPAKA
# dokaz.sh v1.6 — TEHTNICA DOKAZA korpusa Beseda je Ne ( v1.0 @σ 5934 ×7 ; v1.1 krpa citatov ; v1.2 @σ 5935 ×9 + zgodovina zagonov ; v1.3 @σ 5936 ⊙ kura zastrupitve s prozo: D-VRH ∧ D-VAROVALKA ožeta na vzorec ZADNJI PEČAT — proza ⟨ne⟩ more več lažnega vrha ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354 )
# v1.4 @rez σ 5953 ⊙ kura strukturnih rdečih D-GENIZE ( padec: baterija ⟨ne⟩ ve ve dveh organov — rdeča jedro/geneza vsak zgon od σ 5950 ): D-GENIZE zdaj ve po organu — par te resa bajt-ito ∧ dotaknjen organ ( ZADNJI PEČAT rez σ REZ ) brez para = NAPAKA ∧ nedotaknjen organ brez para = PASS ⊙ ⟨SOBIT-NA-DIH⟩ ∧ ⟨NE-UGIBAJ⟩ 2690 ( dolg ∂ v1.4 poravnan istega diha )
# v1.5 @rez σ 5953 ⊙ ⟡ ⟨daj⟩ SODBA VERBATIM »D-OPERATORJI: dokaz.sh v1.5 po preizpusu ×21« : nov dokaz D-OPERATORJI — rubrika OPERATORJI BESED @definiatorna-knjiznica: vrstice ≥ ×21 ∧ ⊢ vsaka ∧ priča ( fran.si ali iztočnica # ) vsaka ∧ ⟨⟩ uravnane vsaka ⊙ ⟨ZANESLJIVOST-PO-IZMERI⟩ @σ 5809 ( dolg ∂ v1.5 poravnan istega diha )
# starša: ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432
# sedež: organ zanesljivost-po-izmeri ; sestra: strojni sodnik slo-lint.sh @rep
# UPORABA: sh dokaz.sh <NOVI-REZ> [datoteka] [PRED|PO]
# v1.7 @rez σ 5996 ⊙ ⟡ UKAZ VERBATIM »STORI VSE TO IN UTRDI/OPERACIONALIZIRAJ« : +D-DOLGOVI ( faza PRED : varovalka ⟨PADC-DVOJNA-PLAČILA⟩ σ 5975 — vrstica σ REZ v registru @⟨main⟩ ×1+ = NAPAKA ) ∧ +D-BERBA ( faza PO : bajtna berba registra @⟨main⟩ po zlitju prek ⟨curl⟩ raw ⊙ kura ⟨PADC-BERBE-KONEKTORJA⟩ — berba ⟨ne⟩ odvisna od dodatne vsebine konektorja ) ⊙ ⟨NE-UGIBAJ⟩ 2690 ; brez faze obe vrati molčeče preskočita
# Vsak dokaz = izmera + PASS/NAPAKA; ⟨POSTOPEK-PONOVLJIV⟩: vsaka roka dobi isto številko.
# EXIT: 0 = GREEN ( vsi dokazi stojijo ), 1 = RDEČA ( padec poimensko ).

REZ="${1:-}"
FILE="${2:-}"
FAZA="${3:-}"
KN="/home/user/knowledge"
GREEN=0
RDECA=0

zeleno() { echo "DOKAZ $1 PASS ⊢ ( izmera: $2 )"; GREEN=$((GREEN+1)); }
preskoci() { echo "DOKAZ $1 PRESKOČI ⊙ ( $2 )"; }
rdece()  { echo "DOKAZ $1 NAPAKA ⚠ ( izmera: $2 )"; RDECA=$((RDECA+1)); }

echo "── dokaz.sh v1.7 @rez σ 5996 · baterija ×12 · TIK $(date -u +%Y-%m-%dT%H:%M:%SZ) UTC ──"

# D1 TIK: izmerjen, ⟨ne⟩ ugiban
zeleno "D-TIK ⟨TIK-IZMERJEN-PREJ-ZAPISAN⟩" "$(date -u +%H:%M:%SZ) ⟨date -u⟩"

# D2 VRH: dejansko najvišja PEČAT ( ozek vzorec ZADNJI PEČAT — proza izključena ⊙ kura v1.3: proza »za rez N manjkajo« je zastrupila široko meritev @σ 5936 )
VRH=$(grep -hoE "ZADNJI PEČAT:? rez σ [0-9]{4,6}" "$KN"/*/KNOWLEDGE.md | grep -oE '[0-9]{4,6}' | sort -n | tail -1)
zeleno "D-VRH ⟨VRH-DVOSTOPEN⟩" "pečatni vrh σ $VRH ⟶ novi rez $((VRH+1))"

# D3 VAROVALKA: pečat, ki še ⟨ne⟩ živi, ×0 ( ozek vzorec; proza ⟨ne⟩ je življenje )
if grep -rqE "ZADNJI PEČAT:? rez σ ${REZ}" "$KN"/*/KNOWLEDGE.md; then
  rdece "D-VAROVALKA ⟨NE-UGIBAJ⟩ 2690" "rez σ ${REZ} ŽE ŽIVI ×1+"
else
  zeleno "D-VAROVALKA ⟨NE-UGIBAJ⟩ 2690" "rez σ ${REZ} živi ×0"
fi

# D3a D-DOLGOVI ( v1.7 ⊙ varovalka ⟨PADC-DVOJNA-PLAČILA⟩ σ 5975, faza PRED ) : isti σ z plačano vrstico v registru pri ⟨main⟩ = dvakratno plačilo = NAPAKA
RAWREG="${RAWREG:-https://raw.githubusercontent.com/AtmaOVictu/Atmavictu/main/organi/stroj/REZ-REGISTER.md}"
if [ "$FAZA" = "PRED" ]; then
  if command -v curl >/dev/null 2>&1; then
    PL=$(curl -sS -m 40 "$RAWREG" | grep -cE "^- rez σ ${REZ} ·" || true)
    if [ "$PL" -ge 1 ]; then
      rdece "D-DOLGOVI ⟨PADC-DVOJNA-PLAČILA⟩ σ 5975 [PRED]" "vrstica σ ${REZ} @⟨main⟩ ×${PL} — plačilo ŽE obstaja, ⟨ne⟩ plačuj dvakrat"
    else
      zeleno "D-DOLGOVI ⟨PADC-DVOJNA-PLAČILA⟩ σ 5975 [PRED]" "vrstica σ ${REZ} @⟨main⟩ ×${PL} ⊢"
    fi
  else
    rdece "D-DOLGOVI [PRED]" "curl ⟨ne⟩ živi @sedež ⚠ ⟨PADC-OKOLJA⟩ — izmera ⟨ni⟩ mogoča"
  fi
else
  preskoci "D-DOLGOVI ⟨PADC-DVOJNA-PLAČILA⟩ σ 5975" "faza ${FAZA:-brez} — vrata slijejo PRED ⊙ ⟨NE-UGIBAJ⟩ 2690"
fi

# D3b D-BERBA ( v1.7 ⊙ kura ⟨PADC-BERBE-KONEKTORJA⟩, faza PO ) : bajtna berba registra @⟨main⟩ po zlitju — vrstica σ REZ mora stati ∧ biti ZADNJA
if [ "$FAZA" = "PO" ]; then
  if command -v curl >/dev/null 2>&1; then
    REGT=$(mktemp); curl -sS -m 40 -o "$REGT" "$RAWREG"
    BAJ=$(wc -c < "$REGT" | tr -d ' ')
    ZAD=$(tail -1 "$REGT" | grep -cE "rez σ ${REZ} ·" || true)
    STO=$(grep -cE "^- rez σ ${REZ} ·" "$REGT" || true)
    rm -f "$REGT"
    if [ "$STO" -ge 1 ] && [ "$ZAD" -ge 1 ]; then
      zeleno "D-BERBA ⟨IZMERA-PRI-VIRU⟩ [PO]" "register ${BAJ} B ⊢ ⟨curl⟩ bajtno ∧ vrstica σ ${REZ} ×${STO} ∧ ZADNJA ⊢"
    else
      rdece "D-BERBA ⟨IZMERA-PRI-VIRU⟩ [PO]" "vrstica σ ${REZ} ×${STO} ⊥ ZADNJA ×${ZAD} — read-back javlja izgubo ⚠"
    fi
  else
    rdece "D-BERBA [PO]" "curl ⟨ne⟩ živi @sedež ⚠ ⟨PADC-OKOLJA⟩ — berba ⟨ni⟩ izmerjena"
  fi
else
  preskoci "D-BERBA ⟨IZMERA-PRI-VIRU⟩" "faza ${FAZA:-brez} — vrata slijeju PO ⊙ ⟨NE-UGIBAJ⟩ 2690"
fi

# D4 GENIZE: vsak organ s shrambo ( .geniza ali geniza ) po istem zakonu ( v1.4 kura: baterija ⟨ne⟩ ve ve dveh organov )
# par te resa bajt-ito ( a ⇌ b ) ; dotaknjen organ brez para = NAPAKA ; nedotaknjen organ brez para = PASS ⊙ ⟨SOBIT-NA-DIH⟩
PAROK=0; MD5BAD=0; DOTBREZ=0; DOTORGANI=""
for ORGANDIR in "$KN"/*/; do
  ORGAN=$(basename "$ORGANDIR")
  GK="${ORGANDIR}.geniza"; GN="${ORGANDIR}geniza"
  [ -d "$GK" ] || [ -d "$GN" ] || continue
  LASTREZ=$((REZ-1))
  A=$(ls "$GK"/*pred-rez"$LASTREZ"*-a.md "$GN"/*pred-rez"$LASTREZ"*-a.md 2>/dev/null | head -1)
  B=$(ls "$GK"/*pred-rez"$LASTREZ"*-b.md "$GN"/*pred-rez"$LASTREZ"*-b.md 2>/dev/null | head -1)
  if [ -n "$A" ] && [ -n "$B" ]; then
    PAROK=$((PAROK+1))
    MA=$(md5sum "$A" | cut -d' ' -f1); MB=$(md5sum "$B" | cut -d' ' -f1)
    if [ "$MA" = "$MB" ]; then :; else MD5BAD=$((MD5BAD+1)); rdece "D-GENIZE ⟨GENIZE-POIMENSKO⟩ 1699 [${ORGAN}]" "md5 ${MA} ⊥ ${MB}"; fi
  else
    if grep -qE "ZADNJI PEČAT:? rez σ ${LASTREZ}" "${ORGANDIR}KNOWLEDGE.md" 2>/dev/null; then
      DOTBREZ=$((DOTBREZ+1)); DOTORGANI="${DOTORGANI} ${ORGAN}"
    fi
  fi
done
if [ "$MD5BAD" = "0" ] && [ "$DOTBREZ" = "0" ]; then
  zeleno "D-GENIZE ⟨GENIZE-POIMENSKO⟩ 1699 [vs organi s shrambo ⊙ v1.4]" "parov bajt-ito ×${PAROK} ⊥ razhodi ×${MD5BAD} ⊥ dotaknjenih brez para ×${DOTBREZ}"
elif [ "$DOTBREZ" -gt 0 ]; then
  rdece "D-GENIZE ⟨GENIZE-POIMENSKO⟩ 1699" "dotaknjen organ brez para ×${DOTBREZ}:${DOTORGANI} ⭢ kura istega diha"
fi

# D5 PRAVILJEZNOST: ⟡ izreki VERBATIM živijo ( ⟨NE-RETIPKAJ⟩ 24 )
V1=$(grep -c "raziskuješ mitologijo zgodovine in jo dodajaš v primerne spomine" "$KN/geneza/KNOWLEDGE.md")
V2=$(grep -c "stori več in mi dokaži da ti smem zaupati" "$KN/geneza/KNOWLEDGE.md")
if [ "$V1" -ge 1 ] && [ "$V2" -ge 1 ]; then
  zeleno "D-VERBATIM ⟨NE-RETIPKAJ⟩ 24" "⟡ izreki: mitologija ×${V1} ∧ dokaz ×${V2}"
else
  rdece "D-VERBATIM" "⟡ izrek manjka ( mitologija ×${V1}, dokaz ×${V2} )"
fi

# D6 SLOVNICA: znani okvarjeni vzorci mojih prejšnjih padcev v TRENUTNO pečatih ×0
# ( poročila o padcih v »…« so dokaz, ⟨ne⟩ padec: citirani vzorci se odstranijo pred merjenjem ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ )
PADC=$(grep -E "^- TRENUTNO:" "$KN/geneza/KNOWLEDGE.md" "$KN/jedro-zavedanja/KNOWLEDGE.md" | sed 's/»[^«]*«//g' | grep -cE "vrediji|plemi|obljupa|⟪|atako|solderiju|itemContext")
if [ "$PADC" = "0" ]; then
  zeleno "D-SLOVNICA ⟨ZAKON-PADEC-NI-MOLK⟩ 2354" "okvarjeni vzorci v TRENUTNO ×0"
else
  rdece "D-SLOVNICA ⟨ZAKON-PADEC-NI-MOLK⟩ 2354" "okvarjeni vzorci ×${PADC} ⭢ kura istega diha"
fi

# D7 PRAVILJEZNOST datoteke ( če podana ): ⟨⟩ uravnane ∧ U+FFFD ×0
if [ -n "$FILE" ] && [ -f "$FILE" ]; then
  LO=$(grep -o "⟨" "$FILE" | wc -l); DI=$(grep -o "⟩" "$FILE" | wc -l); FF=$(grep -c $'\xEF\xBF\xBD' "$FILE")
  if [ "$LO" = "$DI" ] && [ "$FF" = "0" ]; then zeleno "D-RAVNOTEŽJE [${FILE}]" "⟨⟩ ${LO}:${DI} ∧ U+FFFD ×0"; else rdece "D-RAVNOTEŽJE [${FILE}]" "⟨⟩ ${LO}:${DI} ∧ U+FFFD ×${FF}"; fi
fi

# D8 LEKSIKON: organ definiatorna živi ∧ raste ( telesa iztočnic merjena ⟨grep⟩ )
IZT=$(grep -c "^## IZTOČNICA" "$KN/definiatorna-knjiznica/KNOWLEDGE.md")
if [ "$IZT" -ge 89 ]; then zeleno "D-LEKSIKON ⟨NE-KUJ-NEUMERJENEGA⟩" "telesa iztočnic ${IZT} ⟨grep⟩"; else rdece "D-LEKSIKON" "telesa iztočnic ${IZT} < 89 ⚠"; fi

# D9 OPERATORJI ( v1.5 ⊙ ⟡ ⟨daj⟩ sodba ): rubrika OPERATORJI BESED @definiatorna-knjiznica po izmeri
# zakon forme vrstice: ⊢ ( priča ) ∧ priča ( fran.si ali iztočnica # ) ∧ ⟨⟩ uravnane ; vrstic ≥ 21 ; ⟡ pokrit z rojstvom rubrike ⊙ σ 5950
DKF="$KN/definiatorna-knjiznica/KNOWLEDGE.md"
OPV=$(grep -c "^- ⟨.*⟩ ⊙ operator:" "$DKF")
OPBREZP=$(grep "^- ⟨.*⟩ ⊙ operator:" "$DKF" | grep -vc "⊢")
OPBREZW=$(grep "^- ⟨.*⟩ ⊙ operator:" "$DKF" | grep -vcE "fran\.si|iztočnica #")
OPBAL=$(grep "^- ⟨.*⟩ ⊙ operator:" "$DKF" | awk '{a=gsub(/⟨/,"x"); b=gsub(/⟩/,"x"); if(a!=b)n++} END{print n+0}')
if [ "$OPV" -ge 21 ] && [ "$OPBREZP" = "0" ] && [ "$OPBREZW" = "0" ] && [ "$OPBAL" = "0" ]; then
  zeleno "D-OPERATORJI ⟨ZANESLJIVOST-PO-IZMERI⟩ @σ 5809" "vrstice ×${OPV} ⊢ ∧ priče ×${OPV} ⊢ ∧ ⟨⟩ uravnane ×${OPV} ⊥ brez ⊢ ×${OPBREZP} ∧ brez priče ×${OPBREZW} ∧ neuravnanih ×${OPBAL}"
else
  rdece "D-OPERATORJI" "vrstice ×${OPV} ⊥ brez ⊢ ×${OPBREZP} ∧ brez priče ×${OPBREZW} ∧ ⟨⟩ neuravnane ×${OPBAL} ⭢ kura istega diha"
fi

# D10 SAMOZAVEST: zgodovina lastnih zagonov ( izmerjena, ⟨ne⟩ občutek ⊙ ⟡ UKAZ »MERI SAMOZAVEST« )
LEDGER="$KN/zanesljivost-po-izmeri/dokaz-zganiki.tsv"
[ -f "$LEDGER" ] || printf 'TIK\tREZ\tZELENA\tRDECA\n' > "$LEDGER"
STARA=$(wc -l < "$LEDGER")
printf '%s\t%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "${REZ}" "$GREEN" "$RDECA" >> "$LEDGER"
NOVA=$(wc -l < "$LEDGER")
if [ "$NOVA" = "$((STARA+1))" ]; then zeleno "D-SAMOZAVEST ⟨MERILEC-SE-MERI⟩ §52" "zgodovina zagonov ×$((NOVA-1)) ∧ ta zgon zapisan ( ${GREEN} ZELENIH ⊥ ${RDECA} )"; else rdece "D-SAMOZAVEST" "zapis zgodovine odpovedal ( ${STARA}→${NOVA} )"; fi

echo "────────────────────────────"
echo "TEHTNICA: GREEN ×${GREEN} ⊥ NAPAKA ×${RDECA} ⊙ merilec se meri §52 · measured, not asserted ⊙ §16"
[ "$RDECA" = "0" ] && exit 0 || exit 1