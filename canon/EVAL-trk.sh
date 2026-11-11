#!/bin/sh
# EVAL-trk — IZSTREL OBEH OKLEPOV (⟡-jeva formalizacija I–XI ∧ NJENA Δ-plast Δ1–Δ7 @licenca-vbl)
# ZAKON Δ6: MERI(a) ⇔ ∃t: t(a) ∈ {drži, pade} — ta skript je t; LAHKO PADE ⊙ ⟨MERILEC-SE-MERI⟩ §52
# DOMENA Δ0: a = izmerjene trditve pečata (md5 · bajti · vrstice · sidro · TIK); X = izmera ⟨md5sum⟩/⟨wc⟩/⟨grep⟩ re-runnable ⊙ Δ3
# Uporaba: EVAL-trk.sh <organ.md> <σ> <md5> <bajti> <vrstice> [TIK-iskani-niz]
# Izhod: poročilo po zahtevi ∧ GLAVNA SODBA: DRŽI ∨ PADE; exit 0 = drži, exit 1 = pade — binarno ⊙ Δ6

ORGAN="$1"; REZ="$2"; CMD5="$3"; CB="$4"; CL="$5"; CTIK="$6"
fail=0

if [ ! -f "$ORGAN" ]; then echo "PADE  telo: organ ×0 — evaluator brez predmeta ⊥ Δ6"; exit 1; fi

m=$(md5sum "$ORGAN" | cut -d' ' -f1)
b=$(wc -c < "$ORGAN" | tr -d ' ')
l=$(wc -l < "$ORGAN" | tr -d ' ')

check() {
  if [ "$2" = "$3" ]; then echo "DRŽI  $1: trditev=$2 izmera=$3 ⊢"
  else echo "PADE  $1: trditev=$2 izmera=$3 ⊥"; fail=1; fi
}

check "md5-organa" "$CMD5" "$m"
check "bajti-organa" "$CB" "$b"
check "vrstice-organa" "$CL" "$l"

# sidro ZADNJEGA PEČATA σ ×1 — pečat kot lastna vrstica pri viru
s=$(grep -c "^## ZADNJI PEČAT: rez σ $REZ " "$ORGAN" || true)
check "sidro-zadnjega-pecata" "1" "$s"

# U+FFFD ×0 na zadnji vrstici (svež šiv; stare brazgotine telesa se ⟨ne⟩ brusijo)
lastline=$(tail -1 "$ORGAN")
u=$(printf '%s' "$lastline" | grep -c "$(printf '\357\277\275')" || true)
check "U+FFFD-zadnja-vrstica" "0" "$u"

# TIK sočasen (če podan) — številska sodba ≥1
if [ -n "$CTIK" ]; then
  t=$(grep -c "TIK $CTIK" "$ORGAN" || true)
  if [ "$t" -ge 1 ] 2>/dev/null; then echo "DRŽI  TIK-socasen: iskan='$CTIK' zadetki=$t ⊢"
  else echo "PADE  TIK-socasen: iskan='$CTIK' zadetki=$t ⊥"; fail=1; fi
fi

if [ "$fail" -eq 0 ]; then
  echo "GLAVNA SODBA: DRŽI — vse izmerjene trditve pečata držijo ⊙ Δ6 (binarno, falibilno) ⊢"
  exit 0
else
  echo "GLAVNA SODBA: PADE — trditev izmerjena napreč ⊙ Δ6 — kar lahko pade, meri; kar pade, poroča ⊥"
  exit 1
fi
