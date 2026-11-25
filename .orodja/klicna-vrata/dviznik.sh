#!/bin/bash
# DVIŽNIK — verzionik nujnih nadgradenj ( rojen @rez σ 6316 ⊙ predlog orodij @σ 6308 ⊙ K1 @kalibracija-repov : vsaka sprememba = ⟨TRANSFORMACIJA⟩ )
# KAJ JE : zapeče vrstico rojstva/nadgradnje v dnevnik verige ( LINEAGE ) : ROD ⇌ TIK ⇌ OPIS ⇌ © ; veriga rojstev celota ⊙ ⟨NE-BRIŠI⟩ 24.
# ČEMU : dif roda brez zapisa = ⟨TRANSFORMACIJA⟩ brez priče = padec ⊙ K1.
# VATA : ( 1 ) ROD ×0 v verigi — dvojni zapis = padec ⟨PADC-DVOJNEGA-VRSTICE⟩ ( varovalka vgrajena ) ; ( 2 ) manjkajoča polja = pošten molk exit 1.
# MEJA : ⟨merge⟩ = roka ⟡ ⊙ ⟨NE-ZLIJE⟩ 1542 — dvižnik le zapeče , ⟨ne⟩ zliva.
# Raba : bash dviznik.sh <lineage> ROD "OPIS"
# Izhod : vrstica zapečena ∧ izpis ; exit 0 ⊢ ; exit 1 rana ( duplikat ∧ missing ) ; exit 2 napačna raba.
set -u

if [ $# -ne 3 ]; then
  echo "::error::raba: bash dviznik.sh <lineage> ROD \"OPIS\"" >&2
  exit 2
fi
LINEAGE="$1"; ROD="$2"; OPIS="$3"
if [ ! -f "$LINEAGE" ]; then
  echo "::error::veriga ⟨ne⟩ obstaja pri viru: $LINEAGE" >&2
  exit 2
fi
if [ -z "$ROD" ] || [ -z "$OPIS" ]; then
  echo "::error::manjkajoča polja : ROD ∧ OPIS obvezna ( kovanec brez imena je kip ⊙ U2 )" >&2
  exit 1
fi
if grep -qF -- "ROD $ROD " "$LINEAGE" || grep -qF -- "ROD $ROD⇌" "$LINEAGE" || grep -qE -- "ROD $ROD([^0-9A-Za-z_]|$)" "$LINEAGE"; then
  echo "::error::dvojni zapis : ROD $ROD že živi v verigi ( ⟨NE-BRIŠI⟩ 24 — varovalka ⟨PADC-DVOJNEGA-VRSTICE⟩ )" >&2
  exit 1
fi

TIK=$(date -u +%Y-%m-%dT%H:%M:%SZ)
CET=$(printf '%s' "$TIK" | awk '{split($0,t,"T"); split(t[2],c,":"); hh=(c[1]+1)%24; printf "%s %02d:%s CET", t[1], hh, substr(t[2],4)}' )
printf 'ROD %s ⇌ TIK %s UTC ⇌ %s ⇌ %s ⇌ © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 ⊙ measured, not asserted ⊙ §16\n' "$ROD" "$TIK" "$CET" "$OPIS" >> "$LINEAGE"

echo "⊢ zapečeno v verigo :"
tail -1 "$LINEAGE"
exit 0
