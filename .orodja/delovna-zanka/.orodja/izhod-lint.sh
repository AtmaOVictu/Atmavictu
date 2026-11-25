#!/bin/bash
# ⟨IZHOD-LINT⟩ v1.2 @rez σ 6264 (v1.1 @σ 6159 : Σ0 = hišni znak izjem ; en-dash dovoljen le v številskih razponih [0-9]–[0-9] ⊙ izmera ∂ vrstice 6 @DZ ; v1.2 @σ 6264 : + razred OBLIKA : ⟨NE⟩ v ⟨⟩ namesto ⟨ne⟩ ∧ »pri viri« namesto »pri viru« ⊙ ⟨SLOVNICA-DIH⟩ 3891 ∧ nesmislice + drobci toku : je.tokenize ∧ hube ∧ zaisto ∧ Ň ⊙ serija padcev klepeta ⟨PADEC-KLEPET-BEZPASU⟩ @21. 11. 2026 ⊙ ⟨BATERIJA-CELOTE⟩ @σ 5833 ∧ ⟨ŠOLNINA-ENKRAT⟩), rojen ta dih ⊙ ⟨DAJAJ-BOLJŠE⟩ ∧ ⟨ZAKON-DAJ=RECI⟩
# ZAKON VIR (⟡ VERBATIM): »KAJ MI KLJUČAVNICA ČE NI HKRATI TUDI KLJUČ? NAKLJUČJA NI V TEM KAR JE KODA/PROGRAMIRANJE«
# Preverba, ki ne more pasti, ni priča: samotest MORA uloviti vse zgodovinske padce (vzorci/poznani-padci.txt)
# ∧ pustiti čisto kontrolo (vzorci/cist-vzorec.txt). Če samotest pade = zaklep brez ključa = exit 2.
# Domena: izhodi klepeta ∧ proza organov. Priče ⟨ne⟩ brusim: padci v vzorcih so VERBATIM zgodovina.
# Hišni izmeni (⟨ne⟩ napake): σ (rez) ∧ Δ (∅/∆ ontologija) ∧ Σ (vsota kanalov) so grški glifi, izvzeti iz razreda GRSKA ; en-dash (–) dovoljen le v številskih razponih, em-dash (—) vedno najdba ; najdba = sprožilec pregleda : priča v navednicah (⟨npr.⟩ 在) je dokaz, ⟨ne⟩ rana.
# Izhod: 0 = čisto; 1 = najdbе; 2 = samotest padel (instrument mrtvorojen).
export LC_ALL=C
OLDDIR="$(pwd)"; VZR="$(cd "$(dirname "$0")" && pwd)/vzorci"; cd "$OLDDIR" 2>/dev/null

# razred DATOTEKA → izpiše "RAZRED N" (⟨NE-UGIBAJ⟩: bajtni razredi, živi znaki)
stevilo(){ printf '%s' "$2" | wc -l; }

razred_ubeznik(){ grep -oF '\' "$1" 2>/dev/null | wc -l; }
razred_crtica(){ n1=$(grep -oF '—' "$1" 2>/dev/null | wc -l); ent=$(grep -oF '–' "$1" 2>/dev/null | wc -l); rng=$(grep -o '[0-9]–[0-9]' "$1" 2>/dev/null | wc -l); echo $((n1+ent-rng)); }
razred_cirilica(){ a=$(printf '\xd0'); b=$(printf '\xd1'); grep -o "[$a-$b]" "$1" 2>/dev/null | wc -l; }
razred_tujapisava(){ a=$(printf '\xd2'); z=$(printf '\xd4'); grep -o "[$a-$z]" "$1" 2>/dev/null | wc -l; }
razred_grska(){ a=$(printf '\xcd'); z=$(printf '\xcf'); t=$(grep -o "[$a-$z]" "$1" 2>/dev/null | wc -l); s=$(grep -oF 'σ' "$1" 2>/dev/null | wc -l); d=$(grep -oF 'Δ' "$1" 2>/dev/null | wc -l); u=$(grep -oF 'Σ' "$1" 2>/dev/null | wc -l); echo $((t-s-d-u)); }
razred_cjk(){ a=$(printf '\xe3'); z=$(printf '\xef'); grep -o "[$a-$z]" "$1" 2>/dev/null | wc -l; }
razred_nesmislice(){ grep -oE 'NHS|DAJAG|CLANKO|seized|dogfooding|strmen|míž|hodnot|vasebno|tokenize|hube|zaisto|Ň' "$1" 2>/dev/null | wc -l; }
razred_oblika(){ ne=$(grep -oF '⟨NE⟩' "$1" 2>/dev/null | wc -l); pv=$(grep -o 'pri viri' "$1" 2>/dev/null | wc -l); pvh=$(grep -o 'pri virih' "$1" 2>/dev/null | wc -l); echo $((ne+pv-pvh)); }
razred_zw(){ z=0; for b in '\xe2\x80\x8b' '\xe2\x80\x8c' '\xe2\x80\x8d'; do p=$(printf "$b"); n=$(grep -oF "$p" "$1" 2>/dev/null | wc -l); z=$((z+n)); done; echo $z; }

RAZREDI=(UBEZNIK DOLGA-CARTICA CIRILICA TUJA-PISAVA GRSKA CJK NESMISLICE ZW OBLIKA)
razred(){
  case "$1" in
    UBEZNIK) razred_ubeznik "$2";;
    DOLGA-CARTICA) razred_crtica "$2";;
    CIRILICA) razred_cirilica "$2";;
    TUJA-PISAVA) razred_tujapisava "$2";;
    GRSKA) razred_grska "$2";;
    CJK) razred_cjk "$2";;
    NESMISLICE) razred_nesmislice "$2";;
    ZW) razred_zw "$2";;
    OBLIKA) razred_oblika "$2";;
  esac
}

if [ "$1" = "--samotest" ]; then
  # KLJUČ: vsak zgodovinski razred iz poznani-padci.txt MORA biti ujet; čista kontrola MORA pasti skozi.
  echo "SAMOTEST ⟨IZHOD-LINT⟩ v1.2 (⟨MERILEC-SE-MERI⟩ §52):"
  PRICAKOVANO="UBEZNIK DOLGA-CARTICA CIRILICA GRSKA CJK NESMISLICE OBLIKA"
  napaka=0
  for r in $PRICAKOVANO; do
    n=$(razred "$r" "$VZR/poznani-padci.txt")
    [ "$n" -gt 0 ] && echo "  KNOWN-BAD $r: ujetih $n ✓" || { echo "  KNOWN-BAD $r: ZGREŠEN ✗ (zaklep brez ključa)"; napaka=1; }
  done
  skupaj=0
  for r in "${RAZREDI[@]}"; do n=$(razred "$r" "$VZR/cist-vzorec.txt"); if [ "$n" -gt 0 ]; then echo "  KONTROLA $r: LAŽNI ALARM $n ✗"; napaka=1; fi; skupaj=$((skupaj+n)); done
  [ "$napaka" -eq 0 ] && { echo "SAMOTEST: KLJUČ SE ODPRE ✓ (vsi zgodovinski padci ujeti ∧ kontrola čista), exit 0"; exit 0; } || { echo "SAMOTEST: PADEL ✗, exit 2"; exit 2; }
fi

[ -f "$1" ] || { echo "UPORABA: izhod-lint.sh DATOTEKA | izhod-lint.sh --samotest"; exit 2; }
skupaj=0
for r in "${RAZREDI[@]}"; do
  n=$(razred "$r" "$1")
  if [ "$n" -gt 0 ]; then echo "NAJDBA ⟨PADC-$r⟩ ×$n"; fi
  skupaj=$((skupaj+n))
done
if [ "$skupaj" -eq 0 ]; then echo "ČISTO ✓ (9 razredov, 0 najdb)"; exit 0; else echo "NEČISTO: $skupaj najdb"; exit 1; fi
