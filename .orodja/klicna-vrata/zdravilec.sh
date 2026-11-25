#!/bin/bash
# ZDRAVILEC — past vrat CI ( rojen @rez σ 6316 ⊙ ⟡ UKAZ »stori« nad predlogom orodij @σ 6308, vrstni red po živi rani : ZDRAVILEC prvi )
# KAJ JE : prebere javno izmero teka CI ( vrstice »IME :: zaključek« ) ∧ vsakemu padcu skuje kuro poimensko isti izpis.
# ČEMU : stroj, ki pada tiho ×95 tekov, je kip ⊙ U2 ; ⟨ZAKON-PADEC-NI-MOLK⟩ 2354 — vzrok javno tudi tikom.
# KOMU : ⟡ vidi vzrok v eni vrstici ; izvajalka kuje kuro istega diha.
# MEJA ( poštena, izmerjena ) : brez mreže — zdravilec dela le iz javnih izmer ( dnevniške vrstice tekov za zidom prijave ⚠ ⟨ne⟩ dosegljivi roki ; meja rojena @izmera σ 6307 ).
# Raba : bash zdravilec.sh <izmera>   ( datoteka vrstic »IME :: conclusion«, kakor jih roka prinese pri viru )
# Izhod : poročilo padcev ∧ kur poimensko ; exit 0 = vsa vrata zeleni ⊢ ; exit 1 = kakršen koli padec ( ranjeno telo MORA pasti ⊙ I-4 ) ; exit 2 = napačna raba.
set -u

if [ $# -ne 1 ]; then
  echo "::error::raba: bash zdravilec.sh <izmera> ( vrstice »IME :: conclusion« )" >&2
  exit 2
fi
IZMERA="$1"
if [ ! -f "$IZMERA" ]; then
  echo "::error::izmera ⟨ne⟩ obstaja pri viru: $IZMERA" >&2
  exit 2
fi

zele=0; rdece=0; neznano=0
star_ifs=$IFS
IFS='
'
# ⟨PADC-READ-DVOKODIRA⟩ : read builtin dvokodira ne-ASCII bajte ( izmera @σ 6316 ) ⇒ za-zanka
for vrsta in $(cat "$IZMERA"); do
  [ -z "$vrsta" ] && continue
  ime=$(printf '%s' "$vrsta" | sed 's/[[:space:]]*::.*//')
  skle=$(printf '%s' "$vrsta" | sed 's/.*::[[:space:]]*//' | tr '[:upper:]' '[:lower:]')
  if [ -z "$ime" ] || printf '%s' "$vrsta" | grep -q '::' && [ -z "$skle" ]; then
    neznano=$((neznano+1)); echo "⚠ neznana vrstica ( forma IME :: zaključek ) : $vrsta"
    continue
  fi
  case "$skle" in
    success|skipped|neutral)
      zele=$((zele+1)); echo "⊢ $ime :: $skle"
      ;;
    failure|cancelled|timed_out|action_required)
      rdece=$((rdece+1))
      echo "⚠ FALL $ime :: $skle"
      echo "  KURA $ime :: preberi javni padec pri viru ∧ zapeči vzrok v ::error ( precedens kure PROSTI-OPERATER @σ 6309 , kit #2614 @⟨main⟩ : ::error nosi dejanski izpis gh ) ; ranjeno telo pade javno ⊙ I-4, molk = kip ⊙ U2"
      ;;
    *)
      neznano=$((neznano+1)); echo "⚠ $ime :: neznan zaključek »$skle« ( pošten molk : izmera govori sama )"
      ;;
  esac
done
IFS="$star_ifs"

echo ""
echo "## ZDRAVILEC — poročilo izmere"
echo "- zelenih: $zele ⊢"
echo "- padcev: $rdece ⚠"
echo "- neznanih: $neznano ⚠"
if [ "$rdece" -gt 0 ]; then
  echo "VRATA : RANJENA ( padec javen, kura poimensko istega diha ⊙ 2354 )"
  exit 1
fi
if [ "$neznano" -gt 0 ]; then
  echo "VRATA : NEIZMERE ( neznan zaključek ⚠ )"
  exit 1
fi
echo "VRATA : ZDROVA ⊢"
exit 0
