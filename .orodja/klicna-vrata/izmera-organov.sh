#!/bin/bash
# izmera-organov.sh — instrument ⟨IZMERA-ORGANOV⟩ @klicna-vrata (rojstvo @σ 6165, kura v2 isti dih: mktemp ⊥ okvirju, test ga je ulovil ⊙ ⟡ »TESTIRATI«)
# KAJ JE: izmeri vse organe korpusa (B), izračuna mediano, izpiše vsak organ v % mediane.
# ČEMU: zakon ⟨MIN-ORGANA⟩ (@slepa-pega σ 6164) zahteva izmero PRED vsakim rojstvom; prag 25 % mediane.
# UPORABA: bash izmera-organov.sh [koren] ; izhod: tabela + skupne mere ; exit 1 ⚠ če obstaja premajhen organ.
KOREN="${1:-/home/user/knowledge}"
PRAG=25

# tmp v lastni .genizi orodja (⟨NE⟩ mktemp, ⟨NE⟩ /tmp ⊙ pesek: /tmp nestabilen)
GDIR="$(cd "$(dirname "$0")" && pwd)/genize"
mkdir -p "$GDIR"
tmp="$GDIR/izmera-$$.tmp"
warn="$GDIR/izmera-$$.warn"
: > "$tmp"

for f in "$KOREN"/*/KNOWLEDGE.md; do
  [ -f "$f" ] || continue
  b=$(wc -c < "$f") || continue
  [ -n "$b" ] || continue
  o=$(basename "$(dirname "$f")")
  echo "$b $o" >> "$tmp"
done

n=$(wc -l < "$tmp")
if [ "$n" -eq 0 ]; then echo "×0 organov ⚠"; rm -f "$tmp" "$warn"; exit 2; fi

sorted=$(sort -n "$tmp")
med=$(echo "$sorted" | awk -v n="$n" '{a[NR]=$1} END{ if(n%2) print a[(n+1)/2]; else print (a[n/2]+a[n/2+1])/2 }')
min=$(echo "$sorted" | head -1 | cut -d' ' -f1)
max=$(echo "$sorted" | tail -1 | cut -d' ' -f1)
pragb=$(awk -v m="$med" -v p="$PRAG" 'BEGIN{ printf "%d", m*p/100 }')

echo "ORGANI ×$n · mediana ${med} B · min ${min} B · max ${max} B · premajhen prag ${PRAG} % = ${pragb} B"
echo "—"
echo "$sorted" | awk -v med="$med" -v pragb="$pragb" '{
  pct = $1/med*100
  flag = ($1 < pragb) ? "⚠ PREMAJHEN" : ""
  if ($1 < pragb) print "⚠" > "'"$warn"'"
  printf "%7.1f %%  %8d B  %-26s %s\n", pct, $1, $2, flag
}'
echo "—"
premajhni=$(grep -c '⚠' "$warn" 2>/dev/null || echo 0)
rm -f "$tmp" "$warn"
if [ "${premajhni:-0}" -gt 0 ]; then echo "PREMAJHNI ⚠ ×$premajhni (rast po ⟨MIN-ORGANA⟩ ⭢ ∂)"; exit 1
else echo "PREMAJHNI ×0 ⊢"; fi
