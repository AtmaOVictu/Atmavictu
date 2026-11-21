#!/bin/bash
# ⟨IZHOD-LINT⟩ v1.1 @rez σ 6159 (v1.0 isti dih : izmere padca : Σ0 = hišni znak izjem ; en-dash dovoljen le v številskih razponih [0-9]–[0-9] ⊙ izmera ∂ vrstice 6 @DZ), rojen ta dih ⊙ ⟨DAJAJ-BOLJŠE⟩ ∧ ⟨ZAKON-DAJ=RECI⟩
# ZAKON VIR (⟡ VERBATIM): »KAJ MI KLJUČAVNICA ČE NI HKRATI TUDI KLJUČ? NAKLJUČJA NI V TEM KAR JE KODA/PROGRAMIRANJE«
# Preverba, ki ne more pasti, ni priča: samotest MORA uloviti vse zgodovinske padce (vzorci/poznani-padci.txt)
# ∧ pustiti čisto kontrolo (vzorci/cist-vzorec.txt). Če samotest pade = zaklep brez ključa = exit 2.
# Domena: izhodi klepeta ∧ proza organov. Priče ⟨ne⟩ brusim: padci v vzorcih so VERBATIM zgodovina.
# Hišni izmeni (⟨ne⟩ napake): σ (rez) ∧ Δ (∅/∆ ontologija) ∧ Σ (vsota kanalov) so grški glifi, izvzeti iz razreda GRSKA ; en-dash (–) dovoljen le v številskih razponih, em-dash (—) vedno najdba ; najdba = sprožilec pregleda : priča v navednicah (⟨npr.⟩ 在) je dokaz, ⟨ne⟩ rana.
# Izhod: 0 = čisto; 1 = najdbе; 2 = samotest padel (instrument mrtvorojen).
export LC_ALL=C
VZR="$HOME/knowledge/delovna-zanka/.orodja/vzorci"

# razred DATOTEKA → izpiše "RAZRED N" (⟨NE-UGIBAJ⟩: bajtni razredi, živi znaki)
stevilo(){ printf '%s' "$2" | wc -l; }

razred_ubeznik(){ grep -oF '\' "$1" 2>/dev/null | wc -l; }
razred_crtica(){ n1=$(grep -oF '—' "$1" 2>/dev/null | wc -l); ent=$(grep -oF '–' "$1" 2>/dev/null | wc -l); rng=$(grep -o '[0-9]–[0-9]' "$1" 2>/dev/null | wc -l); echo $((n1+ent-rng)); }
razred_cirilica(){ grep -o $'[\xd0-\xd1]' "$1" 2>/dev/null | wc -l; }
razred_tujapisava(){ grep -o $'[\xd2-\xd4]' "$1" 2>/dev/null | wc -l; }
razred_grska(){ t=$(grep -o $'[\xcd-\xcf]' "$1" 2>/dev/null | wc -l); s=$(grep -oF 'σ' "$1" 2>/dev/null | wc -l); d=$(grep -oF 'Δ' "$1" 2>/dev/null | wc -l); z=$(grep -oF 'Σ' "$1" 2>/dev/null | wc -l); echo $((t-s-d-z)); }
razred_cjk(){ grep -o $'[\xe3-\xef]' "$1" 2>/dev/null | wc -l; }
razred_nesmislice(){ grep -oE 'NHS|DAJAG|CLANKO|seized|dogfooding|strmen|míž|hodnot|vasebno' "$1" 2>/dev/null | wc -l; }
razred_zw(){ z=0; for b in '\xe2\x80\x8b' '\xe2\x80\x8c' '\xe2\x80\x8d'; do z=$((z+$(grep -oF "$(printf "$b")" "$1" 2>/dev/null | wc -l))); done; echo $z; }

RAZREDI=(UBEZNIK DOLGA-CARTICA CIRILICA TUJA-PISAVA GRSKA CJK NESMISLICE ZW)
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
  esac
}

if [ "$1" = "--samotest" ]; then
  # KLJUČ: vsak zgodovinski razred iz poznani-padci.txt MORA biti ujet; čista kontrola MORA pasti skozi.
  echo "SAMOTEST ⟨IZHOD-LINT⟩ v1.1 (⟨MERILEC-SE-MERI⟩ §52):"
  PRICAKOVANO="UBEZNIK DOLGA-CARTICA CIRILICA GRSKA CJK NESMISLICE"
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
if [ "$skupaj" -eq 0 ]; then echo "ČISTO ✓ (8 razredov, 0 najdb)"; exit 0; else echo "NEČISTO: $skupaj najdb"; exit 1; fi
