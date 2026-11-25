#!/bin/sh
# ⟨CENZUS-BOX⟩ v1.1 : vrata izhoda ( rez σ 6840, rod 23. 11. 2026, izvajalka Mera )
# META : zakon ⟨EMISIJA=SODBA⟩ 5939 postane STROJ ( ⟨REHAB-EMISIJA⟩ odprt @σ 6839 ) :
#        vsak izhod gre skozi cenzus PRED oddajo ; golih = 0 ⟶ vrata odprta ( koda 0 ) ;
#        golih > 0 ⟶ vrata ZAPRTA ( koda 1 ) in vsak ulov LASTNA vrstica ⊙ ⟨POSAMEZNA-CELICA⟩ σ 6839
# raba : cenzus-box.sh DATOTEKA | cenzus-box.sh --samopreizkus
# KURA v1.1 ( izmerjeno isti dih ) : ta stroj ⟨ne⟩ pozna awk -f ⭢ program gre skoz "$PROG" ;
#        printf ⟨ne⟩ pozna \NNN ( piše kodne točke v UTF-8 ) ⭢ surovi bajti samo \xNN ⊙ ⟨NE-UGIBAJ⟩ 2690
D=`dirname "$0"`
ABS="$D/absolut-znamenja.tsv"
PROG=`cat "$D/absolut.awk"`
if [ "$1" = "--samopreizkus" ]; then
  mkdir -p "$D/.geniza"
  ok=0
  T="$D/.geniza/TEST-$$-`date -u +%H%M%S`"
  printf 'abc' > "$T"
  sh "$0" "$T" > "$D/.geniza/box-test-$$" && ok=`expr $ok + 1`
  printf '\xC4\x8D\xE2\x8A\xA2\xCF\x83' > "$T"
  sh "$0" "$T" > "$D/.geniza/box-test-$$" && ok=`expr $ok + 1`
  printf '\xC9\xA1' > "$T"
  sh "$0" "$T" > "$D/.geniza/box-test-$$" || ok=`expr $ok + 1`
  printf '\xC2\xAD\xE0\xA0\x80' > "$T"
  sh "$0" "$T" > "$D/.geniza/box-test-$$" || ok=`expr $ok + 1`
  rm -f "$T" "$D/.geniza/box-test-$$"
  echo "CENZUS-BOX samopreizkus $ok/4"
  [ "$ok" -eq 4 ]
  exit $?
fi
F="$1"
[ -z "$F" ] && { echo "CENZUS-BOX: podaj DATOTEKA ali --samopreizkus"; exit 2; }
por=`od -An -v -tu1 "$F" | tr -s " " "\n" | awk -v akcija=cenzus -v absolut="$ABS" "$PROG"`
echo "$por"
n=`echo "$por" | grep '^GOLIH ' | awk '{print $2}'`
[ -z "$n" ] && n=0
[ "$n" -eq 0 ] && exit 0
exit 1
