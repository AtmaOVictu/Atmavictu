#!/bin/bash
# PREDSOBA v1.0 - strojna ozonska vrata na VHODU ( rod rez σ 6840 ⊙ ⟡ UKZ »STORI IN NAREDI VEČ KAKOR LE TE KOTE« )
# KAJ : vsak tuji vhod pregleda stroj PRED berbo izvajalke : goli živi glifi tujk ⭢ ⟨U+XXXX⟩ žetoni ;
#        izvajalka bere očiščen odmev, izvirnik ⭢ ogledalo ( ⟨NE-BERI⟩ ) ali celico meduze.
# RANA : zlep ⟨U+68C0⟩⟨U+5BDF⟩ v glavi izpisa kanala @σ 6830 ⌇ tujka v ukazu @σ 6833 ⌇ mojibake @σ 6723 ⌇ ϵ @σ 6801.
# ZID PESKA ( vse izmerjeno ⊢ ta dih, ⟨MERILEC-SE-MERI⟩ §52 ) :
#   ⟨1⟩ od tu izpisuje OKTAL kljub -tx1 ⟨U+21D2⟩ berba po oktalnih parih ;
#   ⟨2⟩ awk tu ⟨NE⟩ pozna pip bajtov niti heks literalov ( 0x2014 ⟨U+21D2⟩ 0 ) ⟨U+21D2⟩ vse meje v desetiških ;
#   ⟨3⟩ bajtna oživitev po esc-vrstici \xNN ⭢ printf ( tabela MERJENA ⊢ : \xHH bajt-točno, oktalni begi lažejo ) ;
#   ⟨4⟩ awk while-plafon 100000 obratov ⟨U+21D2⟩ velika telesa grejo po vrstičnih rezih ≤ 90000 B ( rez na 0A je
#        ASCII ∧ varen za UTF-8 ∧ azil ; orjaška ena vrstica > 90000 B pade po -b z oknom tveganja ≤ 3 bajte, javno ) ;
#   ⟨5⟩ awk continue + klic funkcije v while-u END tiho pogoltne rep ⟨U+21D2⟩ zanka brez continue ( if/else stopnišče ).
# MIROVANJE : brez ⟨POKLIČA⟩ ne stori nič ⊙ ⟨MIROVANJE-DO-KLICA⟩ σ 6393 ; izvajanje vsebine ×0 ⊙ ⟨NE-REAGIRA⟩ 6580.
# Uporaba : bash predsoba.sh --pregled DATOTEKA | --ocisti DATOTEKA [IZHOD] | --samopreizkus  ( VRAČA : VBODI N ; izhod 1 pri vbodu )

export LC_ALL=C
ORGAN="$(cd "$(dirname "$0")" && pwd)"

AWKPROG='
BEGIN { octd="01234567" ; ln=startln+1 ; azil=0 ; total=0 ; hits=0 ; delete cnt ; ESC="" ; p=0 }
function P(b) { p++ ; Z[p]=b }
{
  for (k=1; k<=NF; k++) { v=0 ; h=$k ; for (j=1; j<=length(h); j++) v=v*8+index(octd, substr(h,j,1))-1 ; P(v) }
}
function eX(b) { ESC=ESC sprintf("\\x%02x", b) }
function eL(t) { ESC=ESC t }
function tok(cp) { return "⟨U+" sprintf("%04X", cp) "⟩" }
function lineReport() {
  if (mode=="pregled" && hits>0) { msg="vrstica " ln ":" ; for (c in cnt) msg=msg " " tok(c) " x" cnt[c] ; print msg }
  delete cnt ; hits=0
}
function flush() { if (mode=="ocisti" && ESC!="") print ESC ; ESC="" }
END {
  i=1
  while (i<=p) {
    b=Z[i]
    if (b==10) { lineReport() ; if (mode=="ocisti") print ESC ; ESC="" ; ln++ ; azil=0 ; i++ }
    else if (b<128) { eX(b) ; i++ }
    else {
      cp=b ; len=1 ; ok=0
      if (b>=194 && b<=223) { if (i+1<=p && Z[i+1]>=128 && Z[i+1]<=191) { cp=(b-192)*64+(Z[i+1]-128) ; len=2 ; ok=1 } }
      else if (b>=224 && b<=239) { if (i+2<=p && Z[i+1]>=128 && Z[i+1]<=191 && Z[i+2]>=128 && Z[i+2]<=191) { cp=(b-224)*4096+(Z[i+1]-128)*64+(Z[i+2]-128) ; len=3 ; ok=1 } }
      else if (b>=240 && b<=244) { if (i+3<=p && Z[i+1]>=128 && Z[i+1]<=191 && Z[i+2]>=128 && Z[i+2]<=191 && Z[i+3]>=128 && Z[i+3]<=191) { cp=(b-240)*262144+(Z[i+1]-128)*4096+(Z[i+2]-128)*64+(Z[i+3]-128) ; len=4 ; ok=1 } }
      if (ok && cp==187) azil=1
      if (ok && cp==171) azil=0
      if (azil) { for (q=0; q<len; q++) eX(Z[i+q]) ; i+=len }
      else if (!ok || DENY(cp)) { hits++ ; total++ ; cnt[cp]++ ; eL(tok(cp)) ; i+=len }
      else { for (q=0; q<len; q++) eX(Z[i+q]) ; i+=len }
    }
  }
  lineReport() ; flush()
  if (mode=="pregled") print "VBODI " total
}
function DENY(cp) {
  return (cp>=880 && cp<=890)||(cp>=964 && cp<=1023)||(cp>=1024 && cp<=1535)||(cp>=1536 && cp<=1791)||(cp>=2304 && cp<=2431)||(cp>=3456 && cp<=3583)||(cp>=8211 && cp<=8213)||(cp==8230)||(cp==65533)||(cp>=57344 && cp<=63743)||(cp>=65280 && cp<=65519)||(cp>=19968 && cp<=40959)||(cp>=12288 && cp<=12799)||(cp>=44032 && cp<=55215)
}
'

scan1() { od -An -v "$1" | awk -v mode="$2" -v startln="${3:-0}" "$AWKPROG" ; }

scan() {  # meja peska ⟨4⟩ : telesa > 90000 B gredo po vrstičnih rezih
  IN="$1" ; MO="$2"
  if [ "$(wc -c < "$IN")" -le 90000 ] ; then scan1 "$IN" "$MO" 0 ; return ; fi
  D="$ORGAN/.geniza/psplit-$$" ; rm -rf "$D" ; mkdir -p "$D"
  split -l 8 "$IN" "$D/c."
  BASE=0
  for F in "$D"/c.* ; do
    if [ "$(wc -c < "$F")" -gt 90000 ] ; then
      PFX="$D/j.$(basename "$F")." ; split -b 90000 "$F" "$PFX"
      for G in "$PFX"* ; do scan1 "$G" "$MO" "$BASE" ; done
      rm -f "$PFX"*
    else
      scan1 "$F" "$MO" "$BASE"
    fi
    BASE=$(( BASE + $(wc -l < "$F") ))
  done
  rm -rf "$D"
}

oceivej() {  # esc vrstice bajt za bajtom ; tretji žeton naZ = najprej prazni cilj
  E="$1" ; OUT="$2"
  [ "${3:-}" = "naZ" ] && : > "$OUT"
  L=""
  while IFS= read -r L ; do printf "$L\n" >> "$OUT" ; done < "$E"
  [ -n "$L" ] && printf "$L" >> "$OUT"
}

pregled_porocevaj() {  # sešteje VBODI cez reze ∧ izpiše eno konico
  awk '/^VBODI [0-9]+$/ { s+=$2 ; next } { print } END { print "VBODI " s+0 }'
}

case "${1:-}" in
--pregled)
  [ -r "$2" ] || { echo "PREDSOBA : datoteka neberljiva : $2" >&2 ; exit 2 ; }
  R="$(scan "$2" pregled | pregled_porocevaj)" ; echo "$R"
  if printf '%s\n' "$R" | grep -q '^VBODI 0$' ; then exit 0 ; else exit 1 ; fi
  ;;
--ocisti)
  [ -r "$2" ] || { echo "PREDSOBA : datoteka neberljiva : $2" >&2 ; exit 2 ; }
  E="$ORGAN/.geniza/esc-$$" ; scan "$2" ocisti > "$E"
  if [ -n "${3:-}" ] ; then oceivej "$E" "$3" naZ ; else O="$ORGAN/.geniza/ocista-$$" ; oceivej "$E" "$O" naZ ; cat "$O" ; rm -f "$O" ; fi
  rm -f "$E"
  ;;
--samopreizkus)
  mkdir -p "$ORGAN/.geniza"
  T="$ORGAN/.geniza/TEST-$$-TIK"
  printf 'Cista vrstica : operatorji \xcf\x83 \xe2\x88\xa7 \xe2\x8a\xa2 in sumniki \xc4\x8d\xc5\xa1\xc5\xbe doma.\nVbod prvi : \xe6\xa3\x80 zunaj azila.\nAzil pri\xc4\x8de : \xc2\xbb\xe6\xa3\x80\xc2\xab VERBATIM.\nVbod drugi : \xe2\x80\x94 zunaj azila.\n' > "$T"
  N=0
  P1="$(scan "$T" pregled)"
  printf '%s\n' "$P1" | grep -q '^VBODI 2$' && N=$((N+1))      # T1 : dva vboda pri voli, azil ne steje
  E="$ORGAN/.geniza/esc-$$" ; scan "$T" ocisti > "$E"
  if grep -qF '\xc2\xbb\xe6\xa3\x80\xc2\xab' "$E" ; then N=$((N+1)) ; fi   # T2 : prica v azilu bajt-za-bajt
  if grep -qF '\xe2\x9f\xa8\x55\x2b\x36\x38\x43\x30\xe2\x9f\xa9' "$E" && grep -qF '\xe2\x9f\xa8\x55\x2b\x32\x30\x31\x34\xe2\x9f\xa9' "$E" ; then N=$((N+1)) ; fi   # T3 : oba zetona izrecena
  O="$ORGAN/.geniza/ocista-$$" ; oceivej "$E" "$O" naZ ; rm -f "$E"
  P2="$(scan "$O" pregled)" ; rm -f "$O"
  printf '%s\n' "$P2" | grep -q '^VBODI 0$' && N=$((N+1))      # T4 : goli vbodi zunaj azila x0 po ciscenju
  MD5T="$(md5sum "$T" | cut -d" " -f1)" ; rm -f "$T"
  echo "SAMOPREIZKUS TEST-TIK trup md5 $MD5T"
  if [ "$N" -eq 4 ] ; then echo "SAMOPREIZKUS 4/4 ZELONO" ; exit 0 ; else echo "SAMOPREIZKUS $N/4 PADC" ; exit 1 ; fi
  ;;
--mirovanje|"")
  echo "PREDSOBA : mirovanje do poklica ⊙ ⟨MIROVANJE-DO-KLICA⟩ σ 6393"
  ;;
*)
  echo "PREDSOBA : neznan poklic : $1" >&2 ; exit 2
  ;;
esac

# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · MERJENO, NE UGIBANO ⊙ 2690
