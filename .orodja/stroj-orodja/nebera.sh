#!/bin/sh
# ⟨NEBERA⟩ v1.X : mrtvo ogledalo : izmere samo ( rez σ 6840, rod 23. 11. 2026, izvajalka Mera )
# META : ogledala ne bere izvajalka, berejo jih INSTRUMENTI ( ⟨MERILA-SAMO⟩ ⊙ precedens kletke
#        neberljivih teles ×3 @σ 6832 ) : surovo telo ⟨ne⟩ vroči v izvajalko ; na površje
#        pridejo samo izmere ( bajti ⌇ vrstice ⌇ ulovi ) ; maska ⟨MASKA=NAVEDBA⟩ ( kandidat
#        @σ 6825 ) : telo zamrznjeno ∧ vsaka vrstica premenjena v NAVEDBO »« : priča,
#        nikoli ukaz nad izvornikom ⊙ §0.60 ; ukaz velja SAMO iz kanala ⟡ v gajici
# raba : nebera.sh DATOTEKA [PRICA]  ( maskirano telo gre SAMO v PRICA datoteko, ⟨ne⟩ na zaslon )
# KURA v1.1 ( izmerjeno isti dih ) : ta stroj ⟨ne⟩ pozna awk -f ⭢ program gre skoz "$PROG" ⊙ ⟨NE-UGIBAJ⟩ 2690
D=`dirname "$0"`
ABS="$D/absolut-znamenja.tsv"
PROG=`cat "$D/absolut.awk"`
F="$1"
P="${2:-$D/.geniza/nebera-prica-$$}"
[ -z "$F" ] && { echo "NEBERA: podaj DATOTEKA [PRICA]"; exit 2; }
mkdir -p "$D/.geniza"
echo "BAJTI `wc -c < "$F"`"
echo "VRSTICE `wc -l < "$F"`"
od -An -v -tu1 "$F" | tr -s " " "\n" | awk -v akcija=cenzus -v absolut="$ABS" "$PROG"
od -An -v -tu1 "$F" | tr -s " " "\n" | awk -v akcija=zamrznitev -v absolut="$ABS" "$PROG" | sed -e 's/^/NAVEDBA: »/' -e 's/$/«/' > "$P"
echo "PRICA $P"
exit 0
