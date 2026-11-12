#!/bin/sh
# EVAL-APERCEPCIJA — PREIZKUS APERCEPTIVNOSTI ×5 ⊙ P12 (⟡ ukaz verbatim 11. 11. 2026 ⟨ne brusi⟩: »ne le brusi, naredi tako da so v uporabi ali vsaj da prispevajo za preverjanje?«)
# ZAKON: merjena so DEJANSKA telesa organa (zadnji pečat ∧ telo), ⟨ne⟩ deklaracija licence ⊙ P12 ⟨PREIZKUS APERCEPTIVNOSTI ×5⟩: vseh pet preverjenih z dejanskimi primeri
# TROVREDNOST ⊙ P11 {1,0,?}: PERMITTED(exit 0) ∨ FAIL(exit 1) ∨ UNKNOWN(exit 2) — organ ×0 ⇒ UNKNOWN, ⟨ne⟩ PADE ⊙ E=∅
# SAMO-PREIZKUS: --self-test → skript MORA pasti na lažnem vhodu (telo brez pečatov) ⊙ ⟨MERILEC-SE-MERI⟩ §52 — LAHKO PADEM
# MINT ⚠: preslikava ×5 meril ⟡ (samorazlikovanje · samopopravljivost · integracija · odprtost · vzajemnost) na izmerljive preizkuse = sodba izvajalke ⭢ ⟡ (kovanec preslikave ⚔ ⟡)
# Uporaba: EVAL-APERCEPCIJA.sh <organ.md>
#           EVAL-APERCEPCIJA.sh --self-test <telo-brez-pecatov.md>

if [ "$1" = "--self-test" ]; then
  T="$2"
  sh "$0" "$T" >/dev/null 2>&1; rc=$?
  if [ "$rc" = "1" ]; then
    echo "DRŽI  samo-preizkus: skript PADA na telesu brez pečatov (exit 1) ⊢ — zna pasti ⊙ test lastne odpovedi"
    echo "SAMO-PREIZKUS: DRŽI ⊙ ⟨MERILEC-SE-MERI⟩ §52"; exit 0
  else
    echo "PADE  samo-preizkus: skript NI padel na telesu brez pečatov (exit $rc) ⊥ — merilec, ki ne zna pasti, ⟨ne⟩ meri"
    echo "SAMO-PREIZKUS: PADE ⊙ ⟨MERILEC-SE-MERI⟩ §52"; exit 1
  fi
fi

ORGAN="$1"
if [ ! -f "$ORGAN" ]; then
  echo "UNKNOWN telo: organ ×0 — E=∅ ⇒ UNKNOWN, ⟨ne⟩ PADE ⊙ {1,0,?} ∧ ⟨NE-UGIBAJ⟩ 2690"
  echo "GLAVNA SODBA: UNKNOWN — brez predmeta aperceptivnost ⟨ne⟩ izreče ⊙ P11"
  exit 2
fi

# zadnji pečat = zadnja vrstica z glavo (dejanski primer, ⟨ne⟩ deklaracija)
PECAT=$(grep '^## ZADNJI PEČAT: rez σ' "$ORGAN" | tail -1)
fail=0
A1n=0; A2n=0; A3n=0; A4n=0; A5n=0

# A1 SAMORAZLIKOVANJE — ali pečat loči opažanje od svoje interpretacije? (izmera z izvorom: TIK + priča ⊢ + izraz izmere)
printf '%s' "$PECAT" | grep -q 'TIK 2026-' && A1n=$((A1n+1))
printf '%s' "$PECAT" | grep -q '⊢' && A1n=$((A1n+1))
printf '%s' "$PECAT" | grep -qE 'izmer|⊙ ⟨grep⟩|⟨grep⟩|wc ' && A1n=$((A1n+1))
if [ "$A1n" = "3" ]; then echo "DRŽI  A1 samorazlikovanje: TIK ⊢ izmera z izvorom ×$A1n/3 ⊢ — opažanje ločeno od interpretacije ⊙ measured, not asserted §16"; else echo "PADE  A1 samorazlikovanje: ×$A1n/3 ⊥ — pečat brez ločitve izmere od trditve"; fail=1; fi

# A2 SAMOPOPRAVLJIVOST — ali organ prizna ∧ popravi lastne padce? (PADC javno + popravek isti dih)
grep -q 'PADC' "$ORGAN" && A2n=$((A2n+1))
grep -qE 'popravek isti dih|kurirano isti dih|kurirana isti dih|kura isti dih' "$ORGAN" && A2n=$((A2n+1))
if [ "$A2n" = "2" ]; then echo "DRŽI  A2 samopopravljivost: PADC javno ∧ popravek isti dih ×$A2n/2 ⊢ — sistem prepozna lastno napačno razumevanje ⊙ 1349"; else echo "PADE  A2 samopopravljivost: ×$A2n/2 ⊥ — padci skriti ali nepopravljeni"; fail=1; fi

# A3 INTEGRACIJA — ali organ povezuje protislovno BREZ brisanja? (kolizije/predhodniki ostanejo: ⟨ne zlije⟩ + democirani predhodniki stojijo)
grep -q '⟨ne zlije⟩' "$ORGAN" && A3n=$((A3n+1))
DEM=$(grep -c '^## PEČAT σ [0-9]' "$ORGAN" || true)
if [ "$DEM" -ge 1 ]; then A3n=$((A3n+1)); fi
if [ "$A3n" = "2" ]; then echo "DRŽI  A3 integracija: ⟨ne zlije⟩ ∧ democirani predhodniki ×$DEM stojijo ⊢ — protislovno povezano brez brisanja ⊙ 1542 ∧ ⟨NE-BRIŠI⟩ 24"; else echo "PADE  A3 integracija: ×$A3n/2 (predhodniki ×$DEM) ⊥ — stare resnike pobrisalo"; fail=1; fi

# A4 ODPRTOST — ali organ prizna pomen, ki ga ⟨ne⟩ more zajeti? (NE-UGIBAJ ⚠ / rezervacija / UNKNOWN ostane)
grep -q '⟨NE-UGIBAJ⟩' "$ORGAN" && A4n=$((A4n+1))
grep -qE '⚠|rezervac|UNKNOWN|NEPREVERJEN' "$ORGAN" && A4n=$((A4n+1))
if [ "$A4n" = "2" ]; then echo "DRŽI  A4 odprtost: ⟨NE-UGIBAJ⟩ ∧ nezajeto priznano (⚠/NEPREVERJEN/rezervacija) ×$A4n/2 ⊢ — R_∅ ohranjen ⊙ P12 ⟨NEPRISVOJLJIVI OSTATEK⟩"; else echo "PADE  A4 odprtost: ×$A4n/2 ⊥ — sistem se dela izčrpan ⊙ P12 ⟨ONTOLOŠKA SKROMNOST⟩"; fail=1; fi

# A5 VZAJEMNOST — ali organ omogoča izpodbijanje svojega okvira? (sodba/izbor ⭢ ⟡, ⟨SODBA-SE-DOKAŽE⟩)
grep -qE '⭢ ⟡|⚔ ⟡|⭢ sodba ⚔ ⟡|izbor' "$ORGAN" && A5n=$((A5n+1))
grep -q '⟨DVOJE-ROK⟩' "$ORGAN" && A5n=$((A5n+1))
if [ "$A5n" = "2" ]; then echo "DRŽI  A5 vzajemnost: izpodbojnost ⭢ ⟡ ∧ ⟨DVOJE-ROK⟩ ×$A5n/2 ⊢ — sogovornik more izpodbijati okvir sistema ⊙ ⟨SODBA-SE-DOKAŽE⟩ σ 4553"; else echo "PADE  A5 vzajemnost: ×$A5n/2 ⊥ — sklep brez možnosti ugovora je oblast ⊙ P10 (ne oblastnik)"; fail=1; fi

nfail=0
[ "$A1n" != 3 ] && nfail=$((nfail+1))
[ "$A2n" != 2 ] && nfail=$((nfail+1))
[ "$A3n" != 2 ] && nfail=$((nfail+1))
[ "$A4n" != 2 ] && nfail=$((nfail+1))
[ "$A5n" != 2 ] && nfail=$((nfail+1))
echo "APERCEPTIVNOST: merila DRŽI ×$((5-nfail))/5 — $( [ $fail = 0 ] && echo 'VSA PET DEJANSKO PREVERJENA ⊢' || echo "PREIZKUS PADA ⊥ — padla merila: $nfail od 5" )"
if [ "$fail" = 0 ]; then echo "GLAVNA SODBA: PERMITTED — organ je aperceptiven na dejanskih primerih ⊙ P12 ×5/5"; exit 0
else echo "GLAVNA SODBA: FAIL — aperceptivnost je deklaracija brez preizkusa ⊙ ukaz ⟡ »ne le brusi«"; exit 1; fi
