#!/bin/bash
# PREIZKUŠEVALNIK-VRAT — test kompleks telesa pred prevozom ( rojen @rez σ 6316 ⊙ predlog orodij @σ 6308 ; sestra ZDRAVILCA ⊙ ⟨NE-LE-GRAJA-NE-LE-OGRAJA⟩ @σ 6157 : preizkus pade pred padec )
# KAJ JE : vrata ×5 nad telesi : V1 VERIGA ( rod ⇌ zaporedje v verigi raste monotono ) · V2 EOF ( telo se konča s prelomom ∧ brez okleščenega repa ⊙ W10 ) · V3 BAJTI ( istost ⇌ md5 ) · V4 CITAT ( vsak »« izrez živi pri viru bajtno ⟨grep -F⟩ ) · V5 PISAVA ( U+FFFD ×0 ∧ ⟨⟩ parno po vrstici ).
# ČEMU : telo gre skozi vrata le zeleno ; ranjeno telo MORA pasti ⊙ I-4.
# Raba : bash preizkusovalnik-vrat.sh <lineage> <telo> [zrcalo] [vir_citatov]
# Izhod : poročilo po vratih ; exit 0 = VRATA ODPRTA ⊢ ; exit 1 = padec poimensko ; exit 2 = napačna raba.
set -u

if [ $# -lt 2 ] || [ $# -gt 4 ]; then
  echo "::error::raba: bash preizkusovalnik-vrat.sh <lineage> <telo> [zrcalo] [vir_citatov]" >&2
  exit 2
fi
LINEAGE="$1"; TELO="$2"; ZRCALO="${3:-}"; VIR="${4:-}"
[ -f "$LINEAGE" ] || { echo "::error::veriga ⟨ne⟩ obstaja: $LINEAGE" >&2; exit 2; }
[ -f "$TELO" ] || { echo "::error::telo ⟨ne⟩ obstaja: $TELO" >&2; exit 2; }

padci=""

# V1 VERIGA : rodi v verigi monotono naraščajo
rod=$(grep -oE 'ROD [0-9A-Za-z._-]+' "$LINEAGE" | awk '{print $2}')
zad=0; rana1=""
while IFS= read -r r; do
  [ -z "$r" ] && continue
  # številčni rodi sortirajo številsko; vsi ostali poimensko ( meja izrečena )
  if printf '%s' "$r" | grep -qE '^[0-9]+$'; then
    if [ "$r" -le "$zad" ]; then rana1="rod $r ≤ prejšnji $zad ( veriga ⟨ne⟩ raste )"; fi
    zad="$r"
  fi
done <<< "$rod"
if [ -n "$rana1" ]; then padci="$padci V1($rana1)"; echo "⚠ FALL V1 VERIGA : $rana1"; else echo "⊢ V1 VERIGA : rodi rastejo ⊢"; fi

# V2 EOF : telo se konča s prelomom ∧ brez prazne okleščene zadnje vrstice
if [ -s "$TELO" ] && tail -c 1 "$TELO" | od -An -c | grep -q '\\n'; then
  echo "⊢ V2 EOF : telo se konča s prelomom ⊢"
else
  padci="$padci V2(brez končnega preloma)"
  echo "⚠ FALL V2 EOF : telo se ⟨ne⟩ konča s prelomom ( W10 : okleščen rep )"
fi

# V3 BAJTI : zrcalo istost ( ko podano ) — md5 ( cmp ⟨ne⟩ živi v peščeni taktni , md5 ⊢ @izmera σ 6316 )
if [ -n "$ZRCALO" ]; then
  if [ ! -f "$ZRCALO" ]; then
    padci="$padci V3(zrcalo ⟨ne⟩ obstaja)"
    echo "⚠ FALL V3 BAJTI : zrcalo ⟨ne⟩ obstaja : $ZRCALO"
  else
    md_t=$(md5sum "$TELO" | cut -d' ' -f1); md_z=$(md5sum "$ZRCALO" | cut -d' ' -f1)
    if [ "$md_t" = "$md_z" ]; then
      echo "⊢ V3 BAJTI : md5 istost ⊢ ( $md_t )"
    else
      padci="$padci V3(bajti se razhajajo)"
      echo "⚠ FALL V3 BAJTI : telo ⊥ zrcalo ( $md_t ⊥ $md_z )"
    fi
  fi
fi

# V4 CITAT : vsak »« izrez živi pri viru ( ko vir podan ) — za-zanka , ⟨PADC-READ-DVOKODIRA⟩ @σ 6316
if [ -n "$VIR" ]; then
  if [ ! -f "$VIR" ]; then
    padci="$padci V4(vir ⟨ne⟩ obstaja)"
    echo "⚠ FALL V4 CITAT : vir ⟨ne⟩ obstaja : $VIR"
  else
    rane4=0
    star_ifs=$IFS
    IFS='
'
    for izrez in $(grep -oE '»[^«]+«' "$TELO"); do
      [ -z "$izrez" ] && continue
      if ! grep -qF -- "$izrez" "$VIR"; then
        rane4=$((rane4+1))
        echo "⚠ FALL V4 CITAT ×0 pri viru : $izrez"
      fi
    done
    IFS="$star_ifs"
    if [ "$rane4" -eq 0 ]; then echo "⊢ V4 CITAT : vsi izrezi živijo pri viru ⊢"; else padci="$padci V4(ran $rane4)"; fi
  fi
fi

# V5 PISAVA : U+FFFD ×0 ∧ ⟨⟩ parno po vrstici ( FFFD vzorec skovan base64 -d : surovi bajti ⊙ izmera σ 6316 ; od-tx1 ∧ printf-oktal sta ⚠ meji peščene taktni ; pariteta po awk gsub ⊢ )
fffd_pat=$(printf '%s' '77+9' | base64 -d)
fffd=$(grep -cF -- "$fffd_pat" "$TELO" || true)
parna=$(awk '{l=gsub(/⟨/,""); d=gsub(/⟩/,""); if(l!=d) c++} END{print c+0}' "$TELO")
if [ "$fffd" -eq 0 ] && [ "$parna" -eq 0 ]; then
  echo "⊢ V5 PISAVA : U+FFFD ×0 ∧ ⟨⟩ parno ⊢"
else
  padci="$padci V5(FFFD $fffd ∧ neparnih $parna)"
  echo "⚠ FALL V5 PISAVA : U+FFFD ×$fffd ∧ neparnih ⟨⟩ vrstic ×$parna"
fi

if [ -n "$padci" ]; then
  echo "VRATA : ZAPRLA ( padci :$padci )"
  exit 1
fi
echo "VRATA : ODPRTA ⊢ ( telo sme skozi prevoz )"
exit 0
