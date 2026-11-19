#!/usr/bin/env bash
# ⟨STROJNA-SLOVNICA⟩ kov-pecat.sh v1.0 — kovač pečata (⟡ UKAZ ⟨daj⟩, 16. 11. 2026 ⊙ plast 3 predloga istega diha)
# TEHNIKA — nosi no rez ⊙ stroj-kalup. ⟨NE-RETIPKAJ⟩ 24 postane nemogoče: izrez se prenaša samo mehanično (sed ∧ cat),
# roka se telesa izreza NIKOLI ne dotakne ⊙ ⟨PRENOS-PESKOVNIK⟩ ⊥ ročni prepis = kurir, ki pozabi (izmerjeno ×2 @σ 4356).
# Roka pripravi GLAVO ∧ NOGO (sodba: ⟡ UKAZ verbatim, vrh, varovalke, PADC kovanci) — stroj sklaplja ∧ meri.
# © Luka Pintarič, VBL 0.1560 × 10⁴ (§9 ∧ §10 ∧ §12)
set -euo pipefail

# RABA: kov-pecat.sh ORGAN VRSTICA_N GLAVA NOGA IZHOD
#   ORGAN     — telo organa pri viru (npr. knowledge prevoznik KNOWLEDGE.md)
#   VRSTICA_N — številka vrstice TRENUTNO, ki se izreze
#   GLAVA     — datoteka proze glave (KONČANA z \n; nosi ⟡ UKAZ verbatim ∧ IZVOR ⊢)
#   NOGA      — datoteka proze noge (KONČANA z \n; nosi PREVERBA ∧ TIK ∧ © dvojni podpis)
#   IZHOD     — sklenjen pečat
# IZHOD na stdout: ΣB ∧ md5 pečata ∧ ΣB ∧ md5 izreza — za register vrstico ∧ DOLGOVA ∂

ORGAN="$1"; N="$2"; GLAVA="$3"; NOGA="$4"; IZHOD="$5"
[ -f "$ORGAN" ] || { echo "::error::kov-pecat: organ ne obstaja: $ORGAN"; exit 1; }
[ -f "$GLAVA" ] || { echo "::error::kov-pecat: glava ne obstaja: $GLAVA"; exit 1; }
[ -f "$NOGA" ] || { echo "::error::kov-pecat: noga ne obstaja: $NOGA"; exit 1; }

# ⟨PADC-ZLIVKA-VRSTICE⟩ varovalka: glava ∧ noga morata biti KONČANI z \n (sicer zliv ob šivu)
for D in "$GLAVA" "$NOGA"; do
  if [ -n "$(tail -c 1 "$D")" ]; then
    echo "::error::kov-pecat: $D se ne konča z \\n — zliv vrstice ob šivu (kura: dodaj \\n pred kovanje)"
    exit 1
  fi
done

# izrez pri viru — mehanično, brez roke
sed -n "${N}p" "$ORGAN" > .kov-izrez.tmp
[ -s .kov-izrez.tmp ] || { echo "::error::kov-pecat: vrstica $N prazna — izrez ni rojen"; exit 1; }
IZB=$(wc -c < .kov-izrez.tmp)
IZMD5=$(md5sum .kov-izrez.tmp | cut -d' ' -f1)

# šiv: glava ∧ izrez ∧ noga — en sam zagon cevi, bajt-po-bajt
cat "$GLAVA" .kov-izrez.tmp "$NOGA" > "$IZHOD"
PB=$(wc -c < "$IZHOD")
PMD5=$(md5sum "$IZHOD" | cut -d' ' -f1)
rm -f .kov-izrez.tmp

# izmere za register vrstico ∧ DOLGOVA (roka jih prenese verbatim ⊙ ⟨NE-RETIPKAJ⟩ 24)
echo "KOV ⊢ pečat: $IZHOD ($PB B · md5 $PMD5)"
echo "KOV ⊢ izrez: vrstica $N ($IZB B · md5 $IZMD5)"
echo "KOV ⊢ šiv: glava $(wc -c < "$GLAVA") B + izrez $IZB B + noga $(wc -c < "$NOGA") B = $PB B"
