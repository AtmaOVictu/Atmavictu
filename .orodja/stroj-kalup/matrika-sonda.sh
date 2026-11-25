#!/bin/sh
# MATRIKA-SONDA v0.1.2 — presoja odločitvene matrike O(x) = (p1..p8), pi ∈ [0,1]
# Rod: ⟡ UKAZ verbatim ⟨ne brusi⟩: »ne le po en dih če mogoče — daj več in s tem boljše različice in nadgraditve« (15. 11. 2026) — rojena @rez σ 5507; kure isti dih: 0.1 skladnjska rana parserja → case; 0.1.1 ⟨PADC-ŠTEVKE⟩ (vhod ×9 ⊥ 8 dimenzij — varovalka števke) ∧ ⟨PADC-STRTIME⟩ (awk strftime ×0 v okolju → date -u) ∧ imena s šumniki obnovljena ⊙ ⟨SLOVNICA-DIH⟩
# Zakoni nosilke: AX-ONISUMA (O ≠ Σx) @register-aksiomov · MERILEC-%-ZAUPANJA rez 2181 (most vrednost ⊥ status po dimenziji ⚠ MINT) · ⟨D,B,R,M,T,U⟩ · ⟨NE-UGIBAJ⟩ 2690
# Raba: sh matrika-sonda.sh CILJ p1 p2 p3 p4 p5 p6 p7 p8 — pi: "0.87" (izmerjeno) | "x" (∂ neizmerjeno → U-vrstica); več kot 8 dimenzij = napaka vhoda
set -u
CILJ="$1"
shift
if [ $# -gt 8 ]; then
  echo "⚠ PADC-ŠTEVKE: vhodnih dimenzij $# ⊥ 8 — odvečne zavrnjene; prva osmica meri"
fi
names="pokritost-obsega definicijska-določenost dokazna-pokritost procesna-neodvisnost operativna-robustnost dostopnost-razumevanja obravnava-nasprotij preverjenost-popravkov"
i=0
VALS=""
for v in "$@"
do
  i=$((i+1))
  [ $i -gt 8 ] && break
  ime=$(echo "$names" | cut -d" " -f$i)
  case "$v" in
    x)
      echo "  p$i $ime : ∂ neizmerjeno ⚠ (gre v U-vrstico, ⟨ne⟩ v povprečje)"
      ;;
    *)
      st=$(awk -v n="$v" "BEGIN{if(n>0.9)print \"⊢ (>90 % nosi izmero pri viru)\"; else if(n<0.6)print \"⚠ (<60 % brez izmere)\"; else print \"∂ (sredina — izmeri še)\"}")
      echo "  p$i $ime : $v $st"
      VALS="$VALS $v"
      ;;
  esac
done
awk -v vals="$VALS" "BEGIN{
  n=split(vals,a,\" \"); min=2; sum=0; m=0
  for(k=1;k<=n;k++){ if(a[k]!=\"\"){ m++; sum+=a[k]; if(a[k]+0<min) min=a[k]+0 } }
  avg=(m>0)?sum/m:0
  printf(\"U: %d/8 dimenzij ∂ (neznano prikazano, ⟨ne⟩ prekrito)\n\", 8-m)
  printf(\"min-koordinata: %.2f ⊥ povprečje-skalarizacija: %.2f — AX-ONISUMA: povprečje prikrije U ∧ šibke dimenzije\n\", min, avg)
}"
echo "T: $(date -u +%Y-%m-%dT%H:%M:%SZ) (izmerjeno, ⟨ne⟩ zamrznjeno)"
echo "CILJ: $CILJ · sodba ⚔ ⟡ (orodje meri, ⟨ne⟩ sodi)"
