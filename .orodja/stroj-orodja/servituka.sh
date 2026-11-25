#!/bin/sh
# ⟨SERVITUKA⟩ v1.2 : dodeljevalec služb jetnikom ( rez σ 6840, rod 23. 11. 2026, izvajalka Mera )
# META : ⟨SERVITUT-ZNAKA⟩ σ 6669 : služba ali izbris ; ⟨IZ-PEPELU-BOLJŠA-ORODJA⟩ ∧
#        ⟨UČENJE-OD-PARAZITOV⟩ σ 6700 : vsak ujeti znak postane TESTNI VEKTOR samopreizkusov
# raba : servituka.sh CELICA          ( izpise SLUŽBA v celico + vektor v testni-vektorji.tsv )
#        servituka.sh --samopreizkus
# KURA v1.2 ( izmerjeno isti dih ) : vektor se zapiše SAMO, če žeton še ⟨ni⟩ v registru ( ⟨SEKIRA-DUPLIKATOV⟩ ) ;
#        samopreizkus gre skoz lasten preizkusni register ( ⟨ne⟩ onesnaža živega ) ⊙ ⟨NE-UGIBAJ⟩ 2690
D=`dirname "$0"`
VEC="${VEC:-$D/testni-vektorji.tsv}"
if [ "$1" = "--samopreizkus" ]; then
  mkdir -p "$D/.geniza"
  T="$D/.geniza/serv-test-$$-`date -u +%H%M%S`"
  V="$D/.geniza/serv-test-vec-$$"
  rm -f "$V"
  printf '# testni register σ 6840\n' > "$V"
  printf '# CELICA ⟨U+0261⟩ test\n- ulov : ⟨U+0261⟩ × 1\n' > "$T"
  VEC="$V" sh "$0" "$T" > /dev/null
  v=`grep -c '^⟨U+0261⟩' "$V"`
  grep -q 'SLUŽBA' "$T" && ok=1 || ok=0
  VEC="$V" sh "$0" "$T" > /dev/null
  v2=`grep -c '^⟨U+0261⟩' "$V"`
  rm -f "$T" "$V"
  [ "$v2" -eq 1 ] && dup=1 || dup=0
  echo "SERVITUKA samopreizkus $ok-$v-$dup/3"
  [ "$ok" -eq 1 ] && [ "$v" -eq 1 ] && [ "$dup" -eq 1 ]
  exit $?
fi
C="$1"
[ -z "$C" ] && { echo "SERVITUKA: podaj CELICA"; exit 2; }
tok=`grep -m 1 -o '⟨U+[0-9A-Fa-f][0-9A-Fa-f]*⟩' "$C"`
[ -z "$tok" ] && { echo "SERVITUKA: v celici ni žetona ulova"; exit 3; }
mkdir -p "$D/.geniza"
if ! grep -qF "$tok" "$VEC" 2>/dev/null; then
  awk -v t="$tok" -v dat="$VEC" 'BEGIN { printf "%s\tULOV\t%s\n", t, strftime("%Y-%m-%dT%H:%M:%SZ", systime(), 1) >> dat; close(dat) }' 2>/dev/null || \
  printf '%s\n' "$tok	ULOV	`date -u +%Y-%m-%dT%H:%M:%SZ`" >> "$VEC"
fi
if ! grep -q 'SLUŽBA :' "$C" 2>/dev/null; then
  printf '%s\n' "- SLUŽBA : testni vektor absoluta ( $tok pričakovan ulov cenzusa ) ⊙ ⟨SERVITUT-ZNAKA⟩ σ 6669 · rod σ 6840 · sad spoznanja = služba" >> "$C"
fi
echo "SERVITUKA : služba dodeljena $tok"
exit 0
