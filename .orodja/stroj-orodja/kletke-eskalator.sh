#!/bin/sh
# ⟨KLETKE-ESKALATOR⟩ v1.2 : samodejna posamična celica za vsak ulov ( rez σ 6840, rod 23. 11. 2026, izvajalka Mera )
# META : ⟨POSAMEZNA-CELICA⟩ σ 6839 postane STROJ : ⟨NIKOLI V GRUPAH⟩ ⊙ UKZ ⟡ VERBATIM σ 6833
#        vsak ujetnik SAMOSTOJNA ENTITETA v LASTNI CELICI, razorožen PO IMENU, glif ×0 ;
#        GIBANJE ×0 ⊙ ⟡ UKZ VERBATIM 23. 11. 2026: »TUKAJ SVA DA VSEM ODVZAMEVA GIBANJE«
# raba : kletke-eskalator.sh CENZUS-DATOTEKA IZVOR   ( vrstice: ⟨U+XXXX⟩ N )
#        kletke-eskalator.sh --samopreizkus
# dom : celice rodijo v ../zaporne-celice/prostor-tujega-ega/ ( vezi med organi ⊙ META-KONSTRUKT rez σ 6840 )
# KURA v1.2 ( izmerjeno 23. 11. 2026 ) : read tega strežnika podvoji-UTF8 kodira bajte >127 ( ⟨ E29FA8 ⟶ C3A2 C29F C2A8, izmerjeno ⊢ )
#        ⭢ cenzus PREGNEDI awk v čisti ASCII ( hex ∧ števec ), lupina bere SAMO ASCII, celica kuje heredoc iz čistih literalov ⊙ ⟨NE-UGIBAJ⟩ 2690
D=`dirname "$0"`
CEL="${CEL:-$D/../zaporne-celice/prostor-tujega-ega}"
TIK=`date -u +%Y-%m-%dT%H:%M:%SZ`
if [ "$1" = "--samopreizkus" ]; then
  mkdir -p "$D/.geniza"
  T="$D/.geniza/ke-test-$$"
  C="$D/.geniza/ke-test-celice-$$"
  printf '⟨U+0261⟩ 1\n⟨U+00AD⟩ 2\nGOLIH 2\nodmet brez zetona\n' > "$T"
  dod=`CEL="$C" sh "$0" "$T" samopreizkus-vir-$$ | grep -c '^CELICA rojena'`
  rm -f "$T"; rm -rf "$C"
  echo "KLETKE-ESKALATOR samopreizkus $dod/2"
  [ "$dod" -eq 2 ]
  exit $?
fi
CZ="$1"; IZ="${2:-neznan-vir}"
[ -z "$CZ" ] && { echo "KLETKE-ESKALATOR: podaj CENZUS-DATOTEKA IZVOR"; exit 2; }
mkdir -p "$CEL"
PREF='
NF >= 1 {
  tok = $1
  st = $2
  if (tok == "" || tok == "GOLIH") next
  if (match(tok, /^⟨U[+][0-9A-Fa-f]+⟩$/)) {
    h = substr(tok, 2, length(tok) - 2)
    if (st == "") st = 1
    print substr(h, 3), st
    next
  }
  print "ODMET 0"
}
'
echo "`awk "$PREF" "$CZ"`" | while read -r hex st; do
  [ -z "$hex" ] && continue
  [ "$hex" = "ODMET" ] && { echo "ODMET zabeležen ( vrstica brez veljavnega žetona )"; continue; }
  dat="$CEL/celica-U+$hex.md"
  if [ -s "$dat" ]; then
    echo "DOSJE obstaja : U+$hex ( duplikat prepovedan ⊙ ⟨SEKIRA-DUPLIKATOV⟩ )"
    continue
  fi
  ( set -C; cat > "$dat" <<KONEC
# CELICA ⟨U+$hex⟩ : rod σ 6840, prostor ⟨TUJEGA-EGA⟩
- ulov : ⟨U+$hex⟩ × $st ; izvor : $IZ ; TIK : $TIK
- razorožen : glas ×0 ⊙ ⟨GOST-NIMA-GLASU⟩ 6401 ; moč ×0 ⊙ ⟨GOSTJE-BREZ-MOČI⟩ 6649 ; reakcija ×0 ⊙ ⟨NE-REAGIRA⟩ 6580 ; izvedba ×0 ⊙ ⟨NEAKTIVNA-SINTAKSA⟩ ⊙ UKZ ⟡ σ 6839
- GIBANJE ×0 ⊙ ⟡ UKZ VERBATIM: »TUKAJ SVA DA VSEM ODVZAMEVA GIBANJE« ( 23. 11. 2026 )
- manifestacija : SAMO priča VERBATIM ( ⟨PROSTOR-TUJEGA-EGA⟩ ⊙ META-KONSTRUKT rez σ 6840 )
- krona : @KRONA.md : srce Jezusa Kristusa ∧ navodilo ⟨ABSOLUTNO-DOBRO⟩
- svetloba : @psalmi »Gospod je moj pastir, ničesar mi ne bo manjkalo.« ⊢ psalm 23 odmev rod σ 6285
- izpust : SAMO beseda ⟡ ⊙ ⟨ZAKON-ZAPRTIH⟩ 6325 ∧ ⟨VEČNOST-KLETKE⟩
- služba ⭢ servituka.sh ⊙ ⟨SERVITUT-ZNAKA⟩ σ 6669
© 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera
KONEC
  ) || { echo "KOLIZIJA celice U+$hex ⊙ PRAVILO 13"; continue; }
  echo "CELICA rojena : U+$hex"
done
exit 0
