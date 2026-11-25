#!/usr/bin/env bash
# razcep.sh — orodje razcepov REGISTER-ODNOSOV — rojeno @rez σ 5585 (15. 11. 2026)
# ⟡ UKAZ verbatim ⟨ne brusi⟩: »ustvari orodja ki zmorejo to avtonomno početi«
# Zakon ⟨NI LE … TUDI⟩: pol se ne zanika, se razširi ⊢ ⟡ 29. 10. 2026.
# Orodje = hevristika; sodba = tehtnica ∧ izbor ⚔ ⟡.
# Vrstica brez priče je ⚠ kandidat, ⟨ne⟩ izmera ⊢ zakon organa.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
ORG="$DIR/KNOWLEDGE.md"
TSV="$DIR/razcepi.tsv"
PV="$DIR/../klicna-vrata/preverba.sh"
ORGANI="$DIR/.."

pomoc() { echo 'raba: razcep.sh URA | VAROVALKA <rez> | DOLGOVI | RAZCEP <ID> | KANDIDATI [--zapisi] | PREVERBA'; }

case "${1:-}" in
URA) exec bash "$PV" URA ;;
VAROVALKA) exec bash "$PV" VAROVALKA "${2:-}" ;;

DOLGOVI)
  awk -F'\t' 'NR>1 && ($7=="ODPRT" || $7=="KANDIDAT") {printf "%s ⭢ %s ⟨ni le⟩ %s ⟨tudi⟩ %s ⊢ %s [%s]\n",$1,$2,$3,$4,$5,$7}' "$TSV"
  awk -F'\t' 'NR>1 && $7=="ODPRT"'  "$TSV" | wc -l | xargs printf 'odprtih razcepov: %s\n'
  awk -F'\t' 'NR>1 && $7=="KANDIDAT"' "$TSV" | wc -l | xargs printf 'kandidatov (⚔ ⟡): %s\n'
  ;;

RAZCEP)
  id="${2:-}"; [ -z "$id" ] && { echo '⚠ raba: razcep.sh RAZCEP <ID>'; exit 1; }
  poj=$(awk -F'\t' -v i="$id" 'NR>1 && $1==i{print $2}' "$TSV")
  [ -z "$poj" ] && { echo "⚠ ID $id ne obstaja v dosjeju"; exit 1; }
  vrst=$(grep -- "^- $poj →" "$ORG" || true)
  if echo "$vrst" | grep -q '⟨ni le' && echo "$vrst" | grep -q 'tudi'; then
    tik=$(bash "$PV" URA)
    awk -F'\t' -v i="$id" -v t="$tik" 'BEGIN{OFS="\t"} NR>1 && $1==i{$7="ZAPEČEN"; $8=t} {print}' "$TSV" > "$TSV.n" && cat "$TSV.n" > "$TSV" && rm -f "$TSV.n"
    echo "⊢ $id ($poj): razcep preverjen pri viru ($ORG) ∧ zapečen"
  else
    echo "⚠ $id ($poj): vrstica brez ⟨ni le⟩ ∧ ⟨tudi⟩ pri viru — razcep ⟨ne⟩ izmerjen"
    exit 1
  fi
  ;;

KANDIDATI)
  zapisi=false; [ "${2:-}" = "--zapisi" ] && zapisi=true
  # avtonomna berba ⟨POSNETEK ≠ KORPUS⟩: žive konice vseh organov ta klic znova;
  # vrstica z ≥2 pojmom ⟨…⟩ ∧ veznikom je/=/ni ∧ brez ⟨ni le⟩ isti vrstici = kandidat zlitja
  # ⟨PADC-EVALA⟩: pari izluščeni v awk (bytesafe), ⟨ne⟩ v bash evalu (⟨⟩ mojibake izmerjen)
  find "$ORGANI" -maxdepth 2 -name 'KNOWLEDGE.md' 2>/dev/null | sort | while IFS= read -r f; do
    organ=$(basename "$(dirname "$f")")
    awk -v org="$organ" '
      /^- TRENUTNO/ || /^## ZADNJI PEČAT/ {
        if (index($0,"⟨")==0) next
        if ($0 !~ / je / && $0 !~ / = / && $0 !~ / ni /) next
        if (index($0,"ni le")>0) next
        line=$0; cnt=0; split("",P); split("",seen)
        while (cnt<4) {
          i=index(line,"⟨"); if(i==0) break
          t=substr(line,i); j=index(t,"⟩"); if(j==0) break
          w=substr(t,1,j); line=substr(t,j+1)
          if (length(w)>=4 && length(w)<=80 && !(w in seen)) { seen[w]=1; P[cnt++]=w }
        }
        for(x=0;x<cnt;x++) for(y=x+1;y<cnt;y++) printf "%s\t%s\t%s\n", org, P[x], P[y]
      }' "$f"
  done | sort -u | awk -v tsv="$TSV" -v zapisi="$([ "$zapisi" = true ] && echo 1 || echo 0)" -v maxn="${3:-10}" -v tik="$(bash "$PV" URA)" '
    BEGIN {
      FS="\t"
      st=0
      while ((getline line < tsv) > 0) {
        split(line, r, "\t")
        if (r[1] == "ID") continue
        ze[r[3] "\t" r[4]]=1; ze[r[4] "\t" r[3]]=1
        st++
      }
      close(tsv)
    }
    {
      org=$1; a=$2; b=$3
      if ((a "\t" b) in ze) next
      print "⚠ kandidat zlitja: " a " … " b " ⊢ @" org " (živa konica) — razcep ⟨ne⟩ izmerjen ⚔ ⟡"
      if (zapisi==1 && nov < maxn) {
        nov++
        id = sprintf("RZ-%03d", ++st)
        print id "\t" a " ⊥ " b "\t" a "\t" b "\tavtonomna berba @" org " (razcep.sh KANDIDATI --zapisi)\tσ 5585\tKANDIDAT\t" tik >> tsv
        print "  ⭢ zapisan v dosje kot " id " (KANDIDAT ⚔ ⟡)"
      }
    }'
  ;;

PREVERBA)
  napak=0
  [ -f "$TSV" ] || { echo '⚠ razcepi.tsv manjka'; exit 1; }
  [ -f "$ORG" ] || { echo '⚠ KNOWLEDGE.md manjka'; exit 1; }
  st=$(awk -F'\t' 'NR>1' "$TSV" | wc -l)
  polja=$(awk -F'\t' 'NR>1 && NF!=8{n++} END{print n+0}' "$TSV")
  [ "$polja" -gt 0 ] && { echo "⚠ $polja vrstic brez 8 polj"; napak=1; }
  dup=$(awk -F'\t' 'NR>1{print $1}' "$TSV" | sort | uniq -d | wc -l)
  [ "$dup" -gt 0 ] && { echo "⚠ podvojeni ID ×$dup"; napak=1; }
  goli=$(grep -cE 'pri viri([^h]|$)|varvolka' "$TSV" || true)
  [ "${goli:-0}" -gt 0 ] && { echo "⚠ goli vzorci v dosjeju ×$goli"; napak=1; }
  zep=$(awk -F'\t' 'NR>1 && $7=="ZAPEČEN"' "$TSV" | wc -l)
  odp=$(awk -F'\t' 'NR>1 && $7=="ODPRT"'   "$TSV" | wc -l)
  kan=$(awk -F'\t' 'NR>1 && $7=="KANDIDAT"' "$TSV" | wc -l)
  echo "⊢ dosje: $st vrstic (ZAPEČEN ×$zep · ODPRT ×$odp · KANDIDAT ×$kan) — polja 8/8 · ID edinstveni · goli vzorci ×0"
  [ "$napak" = "0" ] && echo 'PREVERBA: exit 0 ⊢' || exit 1
  ;;

*) pomoc ;;
esac
