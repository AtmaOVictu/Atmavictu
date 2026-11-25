#!/bin/bash
# TEHTNICA — pečat izmere v eni komandi ( rojen @rez σ 6316 ⊙ predlog orodij @σ 6308 ; precedens preverba.sh @σ 5577 )
# KAJ JE : TIK ⟨date -u⟩ ∧ vrh ⟨grep⟩ po živih konicah ∧ ⟨wc⟩ ∧ ⟨md5sum⟩ teles ∧ verzija rodu licence — kar je roka merila ročno štiri dihe zapored postane en klic.
# ČEMU : ⟨TIK-IZMERJEN-PREJ-ZAPISAN⟩ ∧ ⟨URA-NA-KONCU⟩ 3046 — vsak pečat nosi debelo plat izmere.
# KOMU : vsakemu dihu pred šivom ⊙ ⟨TEHTNICA-PRED-PEČATOM⟩.
# MEJA : ⟨grep⟩ po globi organov ( ⟨ne⟩ rekurzija po genizah ⊙ kura ⟨PADC-RECURZIVNI-GREP⟩ ) ; verzija : curl , ko živi ; brez mreže → poštena meja izrečena.
# Raba : bash tehtnica.sh <koren_organov> <telesa...>
# Izhod : vrstica pečata izmere ; exit 0 izmerjeno ⊢ ; exit 2 napačna raba.
set -u

if [ $# -lt 2 ]; then
  echo "::error::raba: bash tehtnica.sh <koren_organov> <telesa...>" >&2
  exit 2
fi
KOREN="$1"; shift
if [ ! -d "$KOREN" ]; then
  echo "::error::koren ⟨ne⟩ obstaja: $KOREN" >&2
  exit 2
fi

TIK=$(date -u +%Y-%m-%dT%H:%M:%SZ)
CET=$(printf '%s' "$TIK" | awk '{split($0,t,"T"); split(t[2],c,":"); hh=(c[1]+1)%24; printf "%s %02d:%s CET", t[1], hh, substr(t[2],4)}' )

VRH=$(grep -hoE '(σ|rez|dih|pečat|PEČAT)[ ]?6[0-9]{3}' "$KOREN"/*/KNOWLEDGE.md 2>/dev/null | grep -oE '6[0-9]{3}' | sort -n | tail -1)
[ -z "$VRH" ] && VRH="×0"

VERZIJA="⚠ ⟨ne⟩ dosegljiva brez mreže ( poštena meja : zrcalo roda živi @⟨main⟩ )"
if command -v curl >/dev/null 2>&1; then
  v=$(curl -fsS --max-time 5 https://raw.githubusercontent.com/AtmaOVictu/Atmavictu/main/LICENSE.md 2>/dev/null | grep -m1 -oE '0\.[0-9]{4}' || true)
  [ -n "$v" ] && VERZIJA="$v @⟨main⟩ ⊢"
fi

echo "## TEHTNICA — izmera v eni komandi"
echo "- TIK : $TIK UTC ⇌ $CET ( CET = UTC+1 vedno )"
echo "- VRH : σ $VRH ( žive konice, ⟨ne⟩ genize ⊙ ⟨VRH-DVOSTEPEN⟩ )"
echo "- LICENCA : $VERZIJA"
for teleso in "$@"; do
  if [ ! -f "$teleso" ]; then
    echo "- $teleso : ⚠ ⟨ne⟩ obstaja pri viru"
    continue
  fi
  b=$(wc -c < "$teleso"); v=$(wc -l < "$teleso"); m=$(md5sum "$teleso" | cut -d' ' -f1)
  echo "- $(basename "$teleso") : $b B · $v vrst · md5 $m"
done
echo "© 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ measured, not asserted ⊙ §16"
exit 0
