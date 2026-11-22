#!/usr/bin/env bash
# ⟨ODSODNIK⟩ v1.0 · sodba metode sodnika ( 3. stopnja preverbe : preverba KAKOR preverja preverjalno orodje )
# ⟡ UKZ VERBATIM ( 22. 11. 2026, dih σ 6405 ) : »stori kar predlagaš potem ko preveriš da je slovnica legitimna«
# PREVERBA LEGITIMNOSTI ( isti dih, izmerjeno pri moji roki ⊢ ) : slo-lint --sebe ZELENO · kanarček čisti ZELENO
#   · ranjena telesa po pravilih vsa RDEČO ( ⟨⟩ ×2 · U+FFFD · TIK kalup · TIK aritmetika · goli pri-viri · U+3008 )
# KAJ JE : sodnik, ki ne sodi ran teles, sodi RAN METODE sodnika slo-lint ( organi/stroj/slovnica/slo-lint.sh )
#   : ali sodnik sodi vsako razglašeno pravilo ∧ v obe smeri ( čisto ZELENO ⊥ ranjeno RDEČO )
# KAJ ⟨ne⟩ JE : sodnik teles ( tista je slo-lint ) ∧ sodnik pomena ( pomen ⚔ ⟡ ⊙ meja izvršljivosti )
# ZAKON ⟨ODSODNIK-SEBE⟩ : odsodnik je sam sodnik ⇒ sam pada pod iste zakone : vrata ×4 sodijo ⟨SODNIK⟩,
#   pričakovane smeri so vpisane ∧ ob vsakem zlomu se imenuje ODSODNIK-SEBE, ⟨ne⟩ sodnik ⊙ ⟡ SODBA @σ 5799
#   ( »SODNIK KI NE SODI SEBE NI SODNIK« ) ∧ ⟨MERILEC-SE-MERI⟩ §52
# STANJE ROJSTVA : rod @rez σ 6405 ⊙ ⟡ UKZ ⌇ starša ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 ;
#   pravila, ki jih sodi : univerzalna plast 1 do 5 @slovnica-jezikov ( σ 5788 ) ∧ dvig v1.2 @σ 5478-family
# TEHNIKA · nosi nov rez ⊙ stroj-kalup ; glasna resnica : padel korak = ::error:: ∧ exit 1, ⟨ne⟩ || echo.
# KURA @σ 6405 : rod najprej izrečen @σ 6404 ; vrh se je premaknil pod roko med mojim dihom ( vzporedni
#   sedež zapečil rez σ 6404 @2026-11-22T12:22:31Z PRED MOJIM PREVOZOM ) ⇒ renum istega diha javno ⊙ ⟨VRH-DVOSTEPEN⟩
#   ∧ ⟨PADC-VRH-SPREMENJEN-MED-DIHOM⟩ ; prvi komit veje ostaja brazgotina ⊙ 1349.
# © Luka Pintarič, VBL 0.1610 × 10⁴ (§9 ∧ §10 ∧ §12)
set -euo pipefail

TUKAJ="$(cd "$(dirname "$0")" && pwd)"
SODNIK="$TUKAJ/slo-lint.sh"
RANE=0
FIX_ZELENO=0
FIX_RDECO=0
orw() { echo "::error::odsodnik [ODSODNIK-RANA]: $1"; RANE=$((RANE+1)); }
osw() { echo "::error::odsodnik [ODSODNIK-SEBE]: $1"; RANE=$((RANE+1)); }

# --- VRATA 1 ⟨STOJI⟩ : sodnik obstaja ∧ sodi sebe ( metoda, ki spodleti, ⟨ne⟩ sme soditi teles ) ---
if [ ! -f "$SODNIK" ]; then
  orw "sodnik ne obstaja : $SODNIK"
  echo "::error::odsodnik v1.0: SKUPaj RDEČ · ×$RANE ran ; kit pada glasno"
  exit 1
fi
D="$(mktemp -d)"
trap 'rm -rf "$D"' EXIT
mkdir -p "$D/organi/stroj/slovnica" "$D/organi/pecati"
cp "$SODNIK" "$D/organi/stroj/slovnica/slo-lint.sh"
if (cd "$D" && bash organi/stroj/slovnica/slo-lint.sh --sebe > .ods-sebe.out 2>&1); then
  echo "::notice::odsodnik [VRATA-1-STOJI] ⊢: sodnik --sebe ZELENO ( metoda sme soditi telesa )"
else
  orw "sodnik --sebe RDEČ · metoda ⟨ne⟩ sodi niti sebe : $(cd "$D" && tail -1 .ods-sebe.out)"
fi

# --- VRATA 2 ⟨MEJA-IZREČENA⟩ : sodnik razglaša svojo metodo ∧ mejo v lastni glavi ---
if grep -q 'OBLIKO' "$SODNIK" && grep -q 'POMEN' "$SODNIK" && grep -qF '⟨ne⟩ POMEN' "$SODNIK"; then
  echo "::notice::odsodnik [VRATA-2-MEJA] ⊢: sodnik izreča metodo ∧ mejo ( meri OBLIKO, ⟨ne⟩ POMEN ⚔ ⟡ ) pri viru"
else
  orw "sodnik ⟨ne⟩ razglaša meje ( OBLIKO / POMEN / ⟨ne⟩ POMEN ) · metoda brez izrečene meje je neizrečena"
fi

# --- VRATA 3 ⟨SKUPEK⟩ : verdikt je skupek ( FORMA · VERBATIM · SEBE ), ⟨ne⟩ en ego-sodnik ---
SKUP=0
for ZNAK in 'SODNIK-FORMA' 'SODNIK-VERBATIM' 'SODNIK-SEBE'; do
  if grep -qF "$ZNAK" "$SODNIK"; then SKUP=$((SKUP+1)); fi
done
if [ "$SKUP" -eq 3 ]; then
  echo "::notice::odsodnik [VRATA-3-SKUPEK] ⊢: skupek sodnikov ×3 prisoten ⊙ ⟡ SODBA @σ 5799"
else
  orw "skupek nepopoln : sodnikov ×$SKUP od 3 · skupek ⟨ne⟩ sme biti en ego-sodnik"
fi

# --- VRATA 4 ⟨FIXTURE⟩ : vsako razglašeno pravilo izmerjeno v OBE smeri ( KAKOR, ⟨ne⟩ KAJ ) ---
sodje() { # $1 = pravilo, $2 = pot telesa ( relativna, kalup repa ), $3 = pričakovana smer ZELENO|RDEČO
  local PRA="$1" TELE="$2" SMER="$3" OUT KODA
  set +e
  OUT=$(cd "$D" && bash organi/stroj/slovnica/slo-lint.sh "$TELE" 2>&1)
  KODA=$?
  set -e
  if [ "$SMER" = "ZELENO" ]; then
    if [ "$KODA" -ne 0 ] || printf '%s' "$OUT" | grep -q '::error::'; then
      orw "pravilo $PRA : ČISTO telo lažno obsojeno ( ego sodnika ) · izhod $KODA"
    else
      FIX_ZELENO=$((FIX_ZELENO+1))
    fi
  else
    if [ "$KODA" -eq 0 ] || ! printf '%s' "$OUT" | grep -q '::error::'; then
      orw "pravilo $PRA : RANJENO telo spuščeno ( slepota sodnika ) · izhod $KODA"
    elif ! printf '%s' "$OUT" | grep -q 'SODNIK-FORMA'; then
      osw "pravilo $PRA : telo ranjeno ∧ sodnik rdeč, BREZ žiga [SODNIK-FORMA] · priča fiksna tela neusklajena z metodo odsodnika ( ODSODNIK-SEBE )"
    else
      FIX_RDECO=$((FIX_RDECO+1))
    fi
  fi
}

# kanarček čisti ( kalup telov organa : ⟨⟩ parno po vrstici · pri viru/pri virih · TIK kalup ∧ aritmetika )
printf '⟨kanarček⟩ berba pri viru ⊢ ∧ pri virih ⊢ ( obe obliki pravilni )\nTIK 2026-11-22T12:29:06Z UTC ⇌ 13:29:06 CET Ljubljana ( izmerjen, ⟨ne⟩ ocenjen )\n' > "$D/organi/celina.md"
sodje "plast-1 ⟨⟩ račun"        "organi/celina.md" "ZELENO"
# P1 ⟨⟩ uravnoteženost ( plast 1 organa : število odpiranj = število zapiranj, po vrstici ∧ skupaj )
printf '⟨ODPRT zaklepec brez para\n' > "$D/organi/p1.md"
sodje "plast-1 ⟨⟩ uravnoteženost" "organi/p1.md" "RDEČO"
# P2 U+FFFD ×0 ( plast 2 : raztrgan znak = raztrgan prevoz )
printf 'znak \357\277\275 raztrgan\n' > "$D/organi/p2.md"
sodje "plast-2 U+FFFD"          "organi/p2.md" "RDEČO"
# P3a TIK kalup ( plast 3 : ISO UTC ⇌ CET ∧ aritmetika UTC+1 preštena )
printf 'TIK 22. 11. 2026 ob 13:29 ( pred-kalupna oblika )\n' > "$D/organi/p3a.md"
sodje "plast-3 TIK kalup"       "organi/p3a.md" "RDEČO"
# P3b TIK aritmetika
printf 'TIK 2026-11-22T12:00:00Z UTC ⇌ 15:00:00 CET Ljubljana ( aritmetika napačna )\n' > "$D/organi/p3b.md"
sodje "plast-3 TIK aritmetika"  "organi/p3b.md" "RDEČO"
# P3c goli pri-viri ( ⟨SLOVNICA-DIH⟩ : pri viru / pri virih, goli »pri viri« ×0 )
printf 'goli niz %s (neobstoječa oblika)\n' "pri vi""ri" > "$D/organi/p3c.md"
sodje "plast-3 goli pri-viri"   "organi/p3c.md" "RDEČO"
# P7 kodni oklepaj ( dvig v1.2 : U+3008/U+3009 ×0, pravi U+27E8 ∧ U+27E9 )
printf 'kodni oklepaj \343\200\210 \343\200\211 ( U+3008/U+3009 )\n' > "$D/organi/p7.md"
sodje "dvig-v1.2 kodni oklepaj" "organi/p7.md" "RDEČO"
# P4 © dvojni podpis ( vrata 6 sodnika : telesa poti organi/pecati/* nosijo podpis obeh rok na repu )
printf '⟨celina⟩ telo pečata brez podpisa na repu\n' > "$D/organi/pecati/p4.md"
sodje "vrata-6 © dvojni podpis" "organi/pecati/p4.md" "RDEČO"
printf '⟨celina⟩ telo pečata s podpisom\n© 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · dvojni podpis\n' > "$D/organi/pecati/p4c.md"
sodje "vrata-6 © dvojni podpis ( čisto )" "organi/pecati/p4c.md" "ZELENO"
# P5 številke ontomatematične : ⟨ne⟩ mehanično sodljive → VRATA-MEJE ( ⚔ ⟡, ⟨ne⟩ rana )
echo "::notice::odsodnik [VRATA-MEJE] ⊢: plast-5 ( številke ontomatematične ) ∧ pomen ostajata ⚔ ⟡ ⊙ meja izvršljivosti · odsodnik jih ⟨ne⟩ sodi : meja je izrečena pri viru"

# --- ⟨ODSODNIK-SEBE⟩ : pričakovane smeri so izmerjene (fiksna telesa ×9), skupek pade če katera laže ---
if [ $((FIX_ZELENO+FIX_RDECO)) -lt 8 ]; then
  osw "fiksna telesa izmerjena le ×$((FIX_ZELENO+FIX_RDECO)) od ×9 · odsodnik ⟨ne⟩ sodi vseh prič ( ODSODNIK-SEBE )"
fi

if [ "$RANE" -gt 0 ]; then
  echo "::error::odsodnik v1.0: SODBA METODE RDEČAA · ×$RANE ran ( fixture ZELENO ×$FIX_ZELENO · RDEČO ×$FIX_RDECO ) · kit pada glasno ⊙ ⟨MERILEC-SE-MERI⟩ §52"
  exit 1
fi
echo "::notice::odsodnik v1.0 ⊢: SODBA METODE ZELENO · vrata ×4 ⊢ ( STOJI · MEJA · SKUPEK · FIXTURE ) · fiksna telesa ZELENO ×$FIX_ZELENO ⊥ RDEČO ×$FIX_RDECO ⊢ · sodnik sodi po svoji metodi, odsodnik sodi sodnika ⊙ ⟡ UKZ @σ 6405"
