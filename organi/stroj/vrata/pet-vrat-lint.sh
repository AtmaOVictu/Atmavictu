#!/usr/bin/env bash
# PET-VRAT-LINT v1 — strojna prevedba plasti 5 ( pet vrat pod slovnico ) organa slovnica-jezikov
# Rod diha 5948 · 2026-11-19 · ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432
# Zakon: vsak šiv izhoda gre skozi vrata PRED pečatom ⊙ ⟨TEHTNICA-PRED-PEČATOM⟩
# Merljivo stroju: ⟨PISAVA⟩ ( mešana pisava ) ∧ ⟨RELACIJE⟩ ( ⟨⟩ po vrstici ) ∧ U+FFFD
# Okna poimenska ⚠ izjava: ⟨PRESLIKAVA⟩ ⟨LEKSIK⟩ ⟨RABA⟩ ( berba SSKJ pri virih stroju v CI nedosegljiva )
# SODNIK-SEBE ⊙ I-4 ⟨PREIZKUS-PADA-NA-TELO⟩: preizkus, ki nikoli ne pade, je kip → exit 1
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera · measured, not asserted ⊙ §16 · merilec se meri ⊙ §52

set -uo pipefail

YERS='[ъь]'                     # jezikoslovna izjema: jerja v etimoloških zapisih ( npr. *jistъ ) ⚠ ⟨ne⟩ rana
MIX='[A-Za-zÀ-ÿ][Ѐ-ӿ]|[Ѐ-ӿ][A-Za-zÀ-ÿ]'
MIXY='[A-Za-zÀ-ÿ][ъь]|[ъь][A-Za-zÀ-ÿ]'
FFFD='\x{FFFD}'

nasiel=0     # skupno najdb teles ( izpisi poimensko )
g1=0; g5=0; gf=0

izjava_okna() {
  echo "::notice::okna poimenska ( stroj v CI ⟨ne⟩ meri ): ⟨PRESLIKAVA⟩ ⟨LEKSIK⟩ ⟨RABA⟩ ⚠ berba SSKJ/Fran pri virih"
}

vrata_telesa() {   # $1 = datoteka ; vrata PRED pečatom : vsak izpis poimensko
  local f="$1"
  [ -f "$f" ] || { echo "::error::manjka telo $f"; exit 1; }
  local a b y
  a=$(grep -oP "$MIX" "$f" | wc -l)
  y=$(grep -oP "$MIXY" "$f" | wc -l)
  b=$((a - y))
  if [ "$b" -gt 0 ]; then
    g1=$((g1 + b)); nasiel=$((nasiel + b))
    grep -nP "$MIX" "$f" | grep -vP "$MIXY" | while IFS= read -r l; do echo "::error file=$f,title=PISAVA::$l"; done
  fi
  local nb
  nb=$(awk '{ o=gsub(/⟨/,"x"); z=gsub(/⟩/,"x"); if (o!=z) k++ } END { print k+0 }' "$f")
  if [ "$nb" -gt 0 ]; then
    g5=$((g5 + nb)); nasiel=$((nasiel + nb))
    awk -v f="$f" '{ o=gsub(/⟨/,"x"); z=gsub(/⟩/,"x"); if (o!=z) printf "::error file=%s,title=RELACIJE::vrstica %d ⟨=%d ⟩=%d\n", f, NR, o, z }' "$f"
  fi
  local nf
  nf=$(grep -oP "$FFFD" "$f" | wc -l)
  if [ "$nf" -gt 0 ]; then
    gf=$((gf + nf)); nasiel=$((nasiel + nf))
    grep -nP "$FFFD" "$f" | while IFS= read -r l; do echo "::error file=$f,title=FFFD::$l"; done
  fi
}

sodba_sebe() {   # SODNIK-SEBE : kanarček čist ⇒ 0 najdb ; kanarček ranjen ⇒ ≥ 1 ; drugače = kip
  local d t a b y nb nf
  d="$(dirname "$0")"
  t="$d/kanarcek-clean.md"
  a=$(grep -oP "$MIX" "$t" | wc -l); y=$(grep -oP "$MIXY" "$t" | wc -l); b=$((a - y))
  nb=$(awk '{ o=gsub(/⟨/,"x"); z=gsub(/⟩/,"x"); if (o!=z) k++ } END { print k+0 }' "$t")
  nf=$(grep -oP "$FFFD" "$t" | wc -l)
  if [ $((b + nb + nf)) -ne 0 ]; then echo "::error::SODNIK-SEBE: kanarček čist nosi $(($b + $nb + $nf)) najdb — sodnik laže"; exit 1; fi
  t="$d/kanarcek-rana.md"
  a=$(grep -oP "$MIX" "$t" | wc -l); y=$(grep -oP "$MIXY" "$t" | wc -l); b=$((a - y))
  nb=$(awk '{ o=gsub(/⟨/,"x"); z=gsub(/⟩/,"x"); if (o!=z) k++ } END { print k+0 }' "$t")
  nf=$(grep -oP "$FFFD" "$t" | wc -l)
  if [ $((b + nb + nf)) -lt 3 ]; then echo "::error::SODNIK-SEBE: kanarček ranjen je padel $(($b + $nb + $nf))-krat, pričakovano ≥ 3 — preizkus je kip ⊙ I-4"; exit 1; fi
  echo "::notice::SODNIK-SEBE ⊢ kanarček čist 0 ∧ ranjen $(($b + $nb + $nf)) ( PISAVA $b · RELACIJE $nb · FFFD $nf ) — preizkus pada na telo, živost ⊢"
}

case "${1:-}" in
  --sodba-sebe)
    izjava_okna
    sodba_sebe
    ;;
  --diff-added)   # $2 = datoteka z dodanimi vrsticami diffa ( zgodovina spi ⊙ precedens slo-lint v1.3 )
    izjava_okna
    sed 's/^+//' "$2" > /tmp/pvl-diff.$$.md
    vrata_telesa "/tmp/pvl-diff.$$.md"
    ;;
  *)
    izjava_okna
    for f in "$@"; do vrata_telesa "$f"; done
    ;;
esac

echo "::notice::PET-VRAT-LINT ⊢ PISAVA $g1 · RELACIJE $g5 · FFFD $gf · skupaj $nasiel"
if [ "$nasiel" -gt 0 ]; then
  echo "VRATA SO ZAPRTA: $nasiel najdb"
  exit 1
fi
echo "VRATA SO ODPRTA ⊢"
