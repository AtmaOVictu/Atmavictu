#!/bin/sh
# ⟨PREIZKUS-NADMOČI⟩ v1.6 rojen @rez σ 6066 ⊙ ukaz ⟡ ⟨stori⟩ nad ( 6 )( iv )
# kure roda : spomin ( berba po datoteki ) ; čas ( obseg 56 glavnih teles ) ; razcep besed ( cele oblike, POSIX temp ) ; digesti ( dedupe po md5 )
# ⟨SODNIK-SEBE⟩ ta roda : digestni zagon ima ČASOVNO varovalo ( v1.5 bajtno je padlo : 280s smrt nad 7,78 GB ⊙ ⟨PADEC-ČASA⟩ javno ) ∧ nadaljevalni manifest ( naslednji dih koplje dalje ⟨ne⟩ od začetka )
D="$(dirname "$0")"; KROOT="${1:-/home/user/knowledge}"; MODE="${2:-}"
TMP="${TMPDIR:-/tmp}/nadmoči-oblike.$$"
MAND="${D}/nadmoči-genize-manifest.tsv"
awk -F'\t' 'NR>4 && $1!~/^#/ && $1!="" {print $1}' "$D/tipokujec-slovar.tsv" > "$TMP"
if [ "$MODE" = "--genize" ]; then
  LIMIT="${3:-90}"; T0=$(date +%s)
  LIST="${TMP}.list"
  [ -f "$MAND" ] || printf '# pot\tmd5 ( nadaljevalni manifest dige )\n' > "$MAND"
  find "$KROOT"/*/.geniza -type f 2>/dev/null | sort > "$LIST"
  VSE=$(grep -c . "$LIST" 2>/dev/null || true); VSE=${VSE:-0}
  PREJ=$(tail -n +2 "$MAND" | cut -f1 | sort -u)
  N=0; STOP=0
  while IFS= read -r F; do
    if echo "$PREJ" | grep -qxF "$F"; then continue; fi
    if [ $(( $(date +%s) - T0 )) -ge "$LIMIT" ]; then STOP=1; break; fi
    M=$(md5sum "$F" 2>/dev/null | cut -d' ' -f1) || continue
    [ -n "$M" ] && printf '%s\t%s\n' "$F" "$M" >> "$MAND"
    N=$((N+1))
  done < "$LIST"
  KOPAL=$(tail -n +2 "$MAND" | cut -f1 | sort -u | grep -c . 2>/dev/null || true); KOPAL=${KOPAL:-0}
  POKOR=$(( KOPAL * 100 / (VSE>0?VSE:1) ))
  echo "== ⟨PREIZKUS-NADMOČI⟩ v1.6 digestni zagon : teles geniz $VSE ; pokopanih skupaj $KOPAL ( ta dih $N, varovalo ${LIMIT}s, stop $STOP ) ; pokora $POKOR %"
  tail -n +2 "$MAND" | cut -f2 | sort -u > "${TMP}.uniq"
  UNIQ=$(grep -c . "${TMP}.uniq" 2>/dev/null || true); UNIQ=${UNIQ:-0}
  awk 'NR>1 && !seen[$2]++ {print $1}' "$MAND" 2>/dev/null | sed 's/$//' > "${TMP}.repra"
  : > "${TMP}.hits" || true
  tr '\n' '\0' < "${TMP}.repra" | xargs -0 -r -n 128 grep -lF -f "$TMP" 2>/dev/null >> "${TMP}.hits" || true
  ZADETKI=$(grep -c . "${TMP}.hits" 2>/dev/null || true); ZADETKI=${ZADETKI:-0}
  ULOV=0
  while IFS= read -r BEZ; do
    [ -z "$BEZ" ] && continue
    N1=0
    if [ "$ZADETKI" -gt 0 ]; then N1=$(grep -hF -- "$BEZ" $(cat "${TMP}.hits") 2>/dev/null | wc -l | tr -d ' '); fi
    ULOV=$((ULOV+N1))
    echo "   oblika »$BEZ« : pojavnic $N1 ( po enotnih telesih z zadetkom $ZADETKI )"
  done < "$TMP"
  echo "== izmera : enotnih digestov $UNIQ ; dedupe $(( (KOPAL-UNIQ)*100 / (KOPAL>0?KOPAL:1) )) % ; ulovi $ULOV ; preostanek ⭢ ∂ ( naslednji dih koplje dalje istega manifesta ) =="
  rm -f "$TMP" "${TMP}".* ; exit 0
fi
echo "== ⟨PREIZKUS-NADMOČI⟩ v1.6 @rez σ 6066 : fiksen korpus : glavna telesa 56 organov ( genize ⭢ digestni način --genize ) =="
ULOV=0; ST=0
while IFS= read -r BEZ; do
  [ -z "$BEZ" ] && continue
  N=$(grep -ho -F -- "$BEZ" "$KROOT"/*/KNOWLEDGE.md 2>/dev/null | wc -l | tr -d ' ')
  ST=$((ST+1)); ULOV=$((ULOV+N))
  echo "   oblika »$BEZ« : pojavnic $N"
done < "$TMP"
rm -f "$TMP"
echo "== ulovi po slovarju vnosov $ST : zgornja meja ( šteje tudi priče v »« ) = $ULOV"
if [ "$ULOV" -gt 0 ]; then echo "== preizkus živ: vrata I8 ( rod @dih σ 6052 ⊢ ) obsegajo prejšnja ⊙ ⟨MERILEC-SE-MERI⟩ §52 =="; else echo "== delta 0 = nadmoč NEDOKAZANA ⊙ ⟨NE-TRDI-PAČ⟩ σ 5475 =="; fi
