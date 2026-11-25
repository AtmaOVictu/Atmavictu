#!/bin/sh
# ⟨MEDUZA⟩ v1.1 : prostor zamrznitve ( rez σ 6840, rod 23. 11. 2026, izvajalka Mera )
# META : ⟨ZAMRZNI-ŽIVI-GLIF⟩ σ 6836 postane PROSTOR, ⟨ne⟩ le pojav : vsak živi glif se
#        kameni v ⟨U+XXXX⟩ žeton PRED berbo ; telo VERBATIM ostaja priča v .geniza ;
#        pri Meduzi okeymeni gledalec, tu se kameni DOTIK sam ⊙ kovanec iz besede ⟡ ( ⚔ ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ )
# raba : meduza.sh DATOTEKA            ( zamrznjeno telo na izhod )
#        meduza.sh --census DATOTEKA   ( poročilo ulovov, vsak LASTNA vrstica )
#        meduza.sh --samopreizkus
# KURA v1.1 ( izmerjeno isti dih ) : ta stroj ⟨ne⟩ pozna awk -f ⭢ program gre skoz "$PROG" ;
#        printf ⟨ne⟩ pozna \NNN ( piše kodne točke v UTF-8 ) ⭢ surovi bajti samo \xNN ⊙ ⟨NE-UGIBAJ⟩ 2690
D=`dirname "$0"`
ABS="$D/absolut-znamenja.tsv"
PROG=`cat "$D/absolut.awk"`
AK="zamrznitev"
[ "$1" = "--census" ] && { AK="cenzus"; shift; }
if [ "$1" = "--samopreizkus" ]; then
  mkdir -p "$D/.geniza"
  T="$D/.geniza/TEST-$$-`date -u +%H%M%S`"
  printf '\xC7\xAB\xE2\x8A\xA2\xC9\xA1' > "$T"
  ok=0
  izh=`od -An -v -tu1 "$T" | tr -s " " "\n" | awk -v akcija=zamrznitev -v absolut="$ABS" "$PROG"`
  [ "$izh" = "ǫ⊢⟨U+0261⟩" ] && ok=`expr $ok + 1`
  c=`od -An -v -tu1 "$T" | tr -s " " "\n" | awk -v akcija=cenzus -v absolut="$ABS" "$PROG" | grep -c '^⟨U+0261⟩ 1$'`
  [ "$c" -eq 1 ] && ok=`expr $ok + 1`
  rm -f "$T"
  echo "MEDUZA samopreizkus $ok/2"
  [ "$ok" -eq 2 ]
  exit $?
fi
F="$1"
[ -z "$F" ] && { echo "MEDUZA: podaj DATOTEKA ali --census DATOTEKA ali --samopreizkus"; exit 2; }
od -An -v -tu1 "$F" | tr -s " " "\n" | awk -v akcija="$AK" -v absolut="$ABS" "$PROG"
exit 0
