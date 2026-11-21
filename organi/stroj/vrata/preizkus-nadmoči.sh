#!/bin/sh
# ⟨PREIZKUS-NADMOČI⟩ v1.7 — kure padcev stene v1.6 @MOJ dih rez σ 6073 ( ⟨PADEC-STENE-300S⟩ ∧ ⟨PADEC-STENE-240S⟩ javno ⊙ 2354 )
# kura 1 : PREJ enopasovni comm ( prej : grep po datoteki ×11 tis. = ≈35 s+m )
# kura 2 : postdig mejnik nad NOVIMI digesti TEGA kosa ( prej : grepi nad vsemi 952 repci 605 MB ×7 )
# manifest format nespremenjen ( pot TAB md5, nadaljevalni ) ∧ namere prej brane iz istega manifesta ⊙ ⟨NE-UGIBAJ⟩ 2690
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
  tail -n +2 "$MAND" | cut -f1 | sort -u > "${TMP}.prej"
  comm -23 "$LIST" "${TMP}.prej" > "${TMP}.novi"
  NOVIH=$(grep -c . "${TMP}.novi" 2>/dev/null || true); NOVIH=${NOVIH:-0}
  tail -n +2 "$MAND" | cut -f2 | sort -u > "${TMP}.predkop"
  N=0; STOP=0
  while IFS= read -r F; do
    if [ $(( $(date +%s) - T0 )) -ge "$LIMIT" ]; then STOP=1; break; fi
    M=$(md5sum "$F" 2>/dev/null | cut -d' ' -f1) || continue
    [ -n "$M" ] && printf '%s\t%s\n' "$F" "$M" >> "$MAND"
    N=$((N+1))
  done < "${TMP}.novi"
  KOPAL=$(tail -n +2 "$MAND" | cut -f1 | sort -u | grep -c . 2>/dev/null || true); KOPAL=${KOPAL:-0}
  POKOR=$(( KOPAL * 100 / (VSE>0?VSE:1) ))
  echo "== ⟨PREIZKUS-NADMOČI⟩ v1.7 digestni zagon : teles geniz $VSE ( nekopanih $NOVIH ) ; pokopanih skupaj $KOPAL ( ta dih $N, varovalo ${LIMIT}s, stop $STOP ) ; pokora $POKOR %"
  tail -n +2 "$MAND" | cut -f2 | sort -u > "${TMP}.unik"
  UNIQ=$(grep -c . "${TMP}.unik" 2>/dev/null || true); UNIQ=${UNIQ:-0}
  DEDU=$(( (KOPAL-UNIQ)*100 / (KOPAL>0?KOPAL:1) ))
  comm -13 "${TMP}.predkop" "${TMP}.unik" > "${TMP}.novdig"
  NDIG=$(grep -c . "${TMP}.novdig" 2>/dev/null || true); NDIG=${NDIG:-0}
  awk -F'\t' 'NR==FNR{d[$1]=1;next} (d[$2]==1) && !s[$2]++{print $1}' "${TMP}.novdig" "$MAND" > "${TMP}.nrepa"
  : > "${TMP}.nhits" || true
  tr '\n' '\0' < "${TMP}.nrepa" | xargs -0 -r -n 128 grep -lF -f "$TMP" 2>/dev/null >> "${TMP}.nhits" || true
  ZADETKI=$(grep -c . "${TMP}.nhits" 2>/dev/null || true); ZADETKI=${ZADETKI:-0}
  ULOV=0
  while IFS= read -r BEZ; do
    [ -z "$BEZ" ] && continue
    N1=0
    if [ "$ZADETKI" -gt 0 ]; then N1=$(grep -hF -- "$BEZ" $(cat "${TMP}.nhits") 2>/dev/null | wc -l | tr -d ' '); fi
    ULOV=$((ULOV+N1))
    echo "   oblika »$BEZ« : pojavnic $N1 ( po novih telesih kosa z zadetkom $ZADETKI )"
  done < "$TMP"
  echo "== izmera v1.7 : enotnih digestov skupaj $UNIQ ; dedupe $DEDU % ; novih digestov tega kosa $NDIG ; ulovi $ULOV ( le nad novimi telesi kosa ⊙ kura 2 ) ; preostanek ⭢ ∂ ( naslednji dih koplje dalje istega manifesta ) =="
  rm -f "${TMP}.list" "${TMP}.prej" "${TMP}.novi" "${TMP}.predkop" "${TMP}.unik" "${TMP}.novdig" "${TMP}.nrepa" "${TMP}.nhits" 2>/dev/null || true
else
  echo "raba : sh preizkus-nadmoči.sh <koren> --genize <varovalo_s>"
fi
