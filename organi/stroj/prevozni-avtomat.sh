#!/bin/sh
# prevozni-avtomat.sh v1.1 @rez σ 6046 ⊙ ⟡ mandat »vse, ali vsaj kolikor maksimalno zmoreš«
# ⚔ PREVOZNI-AVTOMAT : skrči ročni prevozni dih iz ~20 operacij na eno izvedbo ( kosanje + read-back ).
# ⟨PADEC-MEJA-BERBE⟩ izmerjen ta dih : read_file meja je po BAJTIH ⇒ kos ≤ 58.000 B ⊙ ⟨NE-UGIBAJ⟩ 2690.
# ZAKON: meri, ⟨ne⟩ obljublja. Raba: sh prevozni-avtomat.sh <režim> <datoteka> [raw-URL]
#   kosi <datoteka> → kosi-avto/KOS-*.txt ( po vrsticah, vsak ≤ 58 kB, vsak konča ⏎, join == telo )
#   readback <lokalna> <raw-URL> → cmp bajtnito + md5
set -eu
REZIM="${1:-}"
case "$REZIM" in
kosi)
  F="$2"
  python3 - "$F" <<'PY'
import sys, os
src = open(sys.argv[1], encoding='utf-8').read()
lines = src.splitlines(keepends=True)
kosi, cur, cur_b = [], [], 0
for ln in lines:
    b = len(ln.encode('utf-8'))
    if cur and cur_b + b > 58000:
        kosi.append(''.join(cur)); cur, cur_b = [], 0
    cur.append(ln); cur_b += b
if cur: kosi.append(''.join(cur))
os.makedirs('kosi-avto', exist_ok=True)
for i, k in enumerate(kosi, 1):
    open(f'kosi-avto/KOS-{i:02d}.txt', 'w', encoding='utf-8').write(k)
print(f'kosov={len(kosi)} bajtov-max={max(len(k.encode("utf-8")) for k in kosi)} join-ok={"".join(kosi)==src}')
PY
  ;;
readback)
  LOK="$2"; URL="$3"
  curl -s "$URL" -o /tmp/rb-avto.md
  L_MD5=$(md5sum "$LOK" | cut -d' ' -f1); R_MD5=$(md5sum /tmp/rb-avto.md | cut -d' ' -f1)
  if cmp -s "$LOK" /tmp/rb-avto.md; then echo "READBACK ⊢ BAJTNITO · md5 $L_MD5 · $(wc -c < "$LOK") B"; else
    echo "READBACK ⚠ RAZLIKA · lokal $L_MD5 · pri viru $R_MD5"; exit 1; fi
  ;;
*)
  echo "Raba: sh prevozni-avtomat.sh kosi <datoteka> | readback <lokalna> <raw-URL>"; exit 2;;
esac
