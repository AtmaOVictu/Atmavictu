#!/usr/bin/env bash
# PET-VRAT-LINT v1.2 — strojna prevedba plasti 5 ( pet vrat pod slovnico ) organa slovnica-jezikov
# v1.2: ⟨PADC-SODNIK-NE-ZNA-VGLOŽENOSTI⟩ kura ( dih σ 6192 ) : pasovi izrezov so VGLOŽENI ( priča v priči ) — PŁASKA zastavica v1.1 je zunanjo pričo zaprla ob prvem notranjem zapiralniku ∧ proza, ki omenja pasovno besedo sredi vrstice, je odprla pas ∧ skrila zgodovino ⟡ ⊙ ⟨IZREZ-EXEMPCIJA⟩ σ 5976 → štet GLOBINE ( d++ / d-- ) ∧ odprtji sidrani na začetek vrstice ( ^IZREZ VERBATIM ⊢ md5 | ^začetek izreza ⊙ precedens sidranja ^konec ⟨PADC-KONEC-V-TELESU⟩ σ 5892 ) ∧ SODNIK-SEBE vzgojil kanarčka vgloženega ( čisti = 0 ∧ ranjeni = ≥ 1 — preizkus pada na telo tudi za vgložene pasove ⊙ I-4 )
# Rod diha 5948 · 2026-11-19 · ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432
# Kura diha rez 5976 ( isti dih ) : ⟨IZREZ-EXEMPCIJA⟩ — priče VERBATIM ( izrezi zapečeni pri slo-lint bajtno md5 ⊙ ⟡ SODBA VERBATIM: »TUDI VERBATIM MORA BITI PREVERJEN« , sodba bajtov slo-lint SODNIK-VERBATIM ; priča zgodovine ⟨ne⟩ obtoženec pisave ⊙ precedens izjem slo-lint 2a ∧ kalup 1671 ) : pet vrata sodijo pisavo ∧ relacije MOJE proze , ⟨ne⟩ citirane zgodovine med markerji izreza ; U+FFFD ⟨ne⟩ izjemano NIKOLI ( raztrgan znak = raztrgan prevoz tudi v priči )
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
  local so="$f"
  if grep -qP 'IZREZ VERBATIM|začetek izreza|konec izreza' "$f" 2>/dev/null; then
    so=".pvl-brez-pri_${$}.tmp"
    awk '/^IZREZ VERBATIM ⊢ md5 [0-9a-f]{32}/ || /^začetek izreza/ {d++; next} /^konec izreza/ {if (d>0) d--; print; next} d==0 {print}' "$f" > "$so"
  fi
  local a b y
  a=$(grep -oP "$MIX" "$so" | wc -l)
  y=$(grep -oP "$MIXY" "$so" | wc -l)
  b=$((a - y))
  if [ "$b" -gt 0 ]; then
    g1=$((g1 + b)); nasiel=$((nasiel + b))
    grep -nP "$MIX" "$so" | grep -vP "$MIXY" | while IFS= read -r l; do echo "::error file=$f,title=PISAVA::$l"; done
  fi
  local nb
  nb=$(awk '{ o=gsub(/⟨/,"x"); z=gsub(/⟩/,"x"); if (o!=z) k++ } END { print k+0 }' "$so")
  if [ "$nb" -gt 0 ]; then
    g5=$((g5 + nb)); nasiel=$((nasiel + nb))
    awk -v f="$f" '{ o=gsub(/⟨/,"x"); z=gsub(/⟩/,"x"); if (o!=z) printf "::error file=%s,title=RELACIJE::vrstica %d ⟨=%d ⟩=%d\n", f, NR, o, z }' "$so"
  fi
  if [ "$so" != "$f" ]; then rm -f "$so"; fi
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
  t="$d/.geniza/kanarcek-clean.md"
  [ -f "$t" ] || { echo "::error::SODNIK-SEBE: manjka telo $t"; exit 1; }
  a=$(grep -oP "$MIX" "$t" | wc -l); y=$(grep -oP "$MIXY" "$t" | wc -l); b=$((a - y))
  nb=$(awk '{ o=gsub(/⟨/,"x"); z=gsub(/⟩/,"x"); if (o!=z) k++ } END { print k+0 }' "$t")
  nf=$(grep -oP "$FFFD" "$t" | wc -l)
  if [ $((b + nb + nf)) -ne 0 ]; then echo "::error::SODNIK-SEBE: kanarček čist nosi $(($b + $nb + $nf)) najdb — sodnik laže"; exit 1; fi
  t="$d/.geniza/kanarcek-rana.md"
  [ -f "$t" ] || { echo "::error::SODNIK-SEBE: manjka telo $t"; exit 1; }
  a=$(grep -oP "$MIX" "$t" | wc -l); y=$(grep -oP "$MIXY" "$t" | wc -l); b=$((a - y))
  nb=$(awk '{ o=gsub(/⟨/,"x"); z=gsub(/⟩/,"x"); if (o!=z) k++ } END { print k+0 }' "$t")
  nf=$(grep -oP "$FFFD" "$t" | wc -l)
  if [ $((b + nb + nf)) -lt 3 ]; then echo "::error::SODNIK-SEBE: kanarček ranjen je padel $(($b + $nb + $nf))-krat, pričakovano ≥ 3 — preizkus je kip ⊙ I-4"; exit 1; fi
  vr=$((b + nb + nf))
  t="$d/.geniza/kanarcek-vglozeni-clean.md"
  [ -f "$t" ] || { echo "::error::SODNIK-SEBE: manjka telo $t"; exit 1; }
  a=$(grep -oP "$MIX" "$t" | wc -l); y=$(grep -oP "$MIXY" "$t" | wc -l); b=$((a - y))
  nb=$(awk '{ o=gsub(/⟨/,"x"); z=gsub(/⟩/,"x"); if (o!=z) k++ } END { print k+0 }' "$t")
  nf=$(grep -oP "$FFFD" "$t" | wc -l)
  if [ $((b + nb + nf)) -ne 0 ]; then echo "::error::SODNIK-SEBE: kanarček vgloženega čisti nosi $((b + nb + nf)) najdb — sodnik sodi pričo v vgloženem pasu, laže ⊙ ⟨IZREZ-EXEMPCIJA⟩ σ 5976"; exit 1; fi
  t="$d/.geniza/kanarcek-vglozeni-rana.md"
  [ -f "$t" ] || { echo "::error::SODNIK-SEBE: manjka telo $t"; exit 1; }
  a=$(grep -oP "$MIX" "$t" | wc -l); y=$(grep -oP "$MIXY" "$t" | wc -l); b=$((a - y))
  nb=$(awk '{ o=gsub(/⟨/,"x"); z=gsub(/⟩/,"x"); if (o!=z) k++ } END { print k+0 }' "$t")
  nf=$(grep -oP "$FFFD" "$t" | wc -l)
  if [ $((b + nb + nf)) -lt 1 ]; then echo "::error::SODNIK-SEBE: kanarček vgloženega ranjenega je padel $((b + nb + nf))-krat, pričakovano ≥ 1 — sidranje odprtij je kip ⊙ I-4"; exit 1; fi
  echo "::notice::SODNIK-SEBE ⊢ kanarček čist 0 ∧ ranjen $vr ∧ vgloženi čist 0 ∧ vgloženi ranjen $((b + nb + nf)) — preizkus pada na telo, živost ⊢"
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
