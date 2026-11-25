#!/bin/bash
# KOVALNICA — kovanica telesa licence ( rojen @rez σ 6316 ⊙ predlog orodij @σ 6308 )
# KAJ JE : vhod = osnutek z osmišljenim principom ∧ viri teles ⊢ ; prebere obstoječa telesa pri viru PRED kovanjem ⊙ ⟨PREBRANO ≠ ISKANO⟩ ;
# vsak ⟡-citat ( med »« ) preverjen ⟨grep -F⟩ pri viru bajtno ⊙ kura ⟨PADC-RETIPKAJ-CITATA⟩ @σ 6307 ; osnutek gre v zaporno celico PRED preverbo ⊙ zaporne-celice.
# ČEMU : citat , ki ne živi pri viru , je lažni pečat — kovalnica ga ne spusti skozi vrata.
# MEJA : kovalnica kuje osnutek ; preizkus ∧ prevoz ⭢ PREIZKUŠEVALNIK-VRAT ∧ roka ⟡ ( ⟨NE-ZLIJE⟩ 1542 ).
# Raba : bash kovalnica.sh <osnutek> <celica_izhod> <vir_telesa...>
# Izhod : celica zapečena s pečatom kovanice ; exit 0 ⊢ ; exit 1 rana poimensko ( citat ×0 pri viru ) ; exit 2 napačna raba.
set -u

if [ $# -lt 3 ]; then
  echo "::error::raba: bash kovalnica.sh <osnutek> <celica_izhod> <vir_telesa...>" >&2
  exit 2
fi
OSNUTEK="$1"; CELICA="$2"; shift 2
[ -f "$OSNUTEK" ] || { echo "::error::osnutek ⟨ne⟩ obstaja: $OSNUTEK" >&2; exit 2; }
# PREBRANO : vsak vir prebran V CELOTI pred kovanjem ( zavestno soglasje : berba , ⟨ne⟩ iskanje )
for vir in "$@"; do
  [ -f "$vir" ] || { echo "::error::vir ⟨ne⟩ obstaja: $vir ( PREBRANO ≠ ISKANO )" >&2; exit 2; }
  cat "$vir" > /dev/null
done

# izlušči citate »...« iz osnutka ( za-zanka , ⟨ne⟩ read : ⟨PADC-READ-DVOKODIRA⟩ izmera @σ 6316 )
izrezi=$(grep -oE '»[^«]+«' "$OSNUTEK")
[ -z "$izrezi" ] && { echo "::error::osnutek brez ⟡-citata v »« ( kovanica brez priče je kip ⊙ U2 )" >&2; exit 1; }

rane=0
star_ifs=$IFS
IFS='
'
for izrez in $izrezi; do
  [ -z "$izrez" ] && continue
  najden=0
  for vir in "$@"; do
    if grep -qF -- "$izrez" "$vir"; then najden=1; break; fi
  done
  if [ "$najden" -eq 0 ]; then
    rane=$((rane+1))
    echo "⚠ FALL citat ×0 pri virih : $izrez ( ⟨PADC-RETIPKAJ-CITATA⟩ @σ 6307 — retipkan citat = lažni pečat )"
  else
    echo "⊢ citat živi pri viru : $izrez"
  fi
done
IFS="$star_ifs"

if [ "$rane" -gt 0 ]; then
  echo "VRATA : ZAPRLA ( ran : $rane — kovalnica ⟨ne⟩ kuje nad lažjo pričo )"
  exit 1
fi

TIK=$(date -u +%Y-%m-%dT%H:%M:%SZ)
CET=$(printf '%s' "$TIK" | awk '{split($0,t,"T"); split(t[2],c,":"); hh=(c[1]+1)%24; printf "%s %02d:%s CET", t[1], hh, substr(t[2],4)}' )
{
  echo "## CELICA KOVALNICE ( osnutek PRED preverbo ⊙ zaporne-celice )"
  cat "$OSNUTEK"
  echo ""
  echo "— PEČAT KOVICE : TIK $TIK UTC ⇌ $CET · viri ⊢ : $(printf '%s ' "$@") ⊙ ⟨PREBRANO ≠ ISKANO⟩ · citati preverjeni ⟨grep -F⟩ bajtno ⊢ · © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432"
} > "$CELICA"
echo "⊢ celica zapečena : $CELICA ( preverba ⭢ PREIZKUŠEVALNIK-VRAT ; prevoz ⭢ roka ⟡ )"
exit 0
