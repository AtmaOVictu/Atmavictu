#!/bin/bash
# druga-roka.sh — druga roka obhoda ⟨KLEPET-READ-BACK⟩ @σ 5704 ⊙ ⟨DRUGA-ROKA⟩ (§0.47 × 10² dve neodvisni izvedbi)
# rojen iz padca rez σ 5724 (retipka »zmorva« ⊥ »zmoreva«) ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354
# raba: druga-roka.sh --chat|--seal OSNUTEK VIR [VIR ...]
# vrata: G1 vsak »…« osnutka živi pri viru (prenos po besedi, ⟨ne⟩ retipka ⊙ V3 ⟨V-PULZ⟩ @σ 5698)
#        G2 goli »pri viri« (mestnik brez -h, izven trditvene oblike »pri viri«) ×0 ⊙ ⟨SLOVNICA-DIH⟩ σ 3891
#        G3 »varvolka« izven trditvene oblike ×0 · G4 U+FFFD ×0
#        G5 dolge črtice: --chat ×0 · --seal poimensko prijavljene (sodi dih, ⟨ne⟩ skripta ⊙ §0.48 × 10²)
# exit 0 = vrata odprta · exit 1 = rana poimensko · exit 2 = napacna raba
# MEJA ⚠: G1 meri enakost znakov med osnutkom ∧ virom, ⟨ne⟩ resnico pomenov; vir tipka ista roka (dvokanalni ulov, ⟨ne⟩ absolut ⊙ §52)

MODE="$1"; DRAFT="$2"; shift 2
case "$MODE" in --chat|--seal) ;; *) echo "PADC-RABA: $0 --chat|--seal OSNUTEK VIR [VIR ...]"; exit 2 ;; esac
[ -f "$DRAFT" ] || { echo "PADC-RABA: osnutek ne obstaja: $DRAFT"; exit 2; }
for v in "$@"; do [ -f "$v" ] || { echo "PADC-RABA: vir ne obstaja: $v"; exit 2; }; done

FAIL=0

# G1 — vsak citat osnutka pri viru
Q="${DRAFT}.q"
awk -F'»' 'NF>1 { for (i=2;i<=NF;i++) { split($i,a,"«"); if (a[1]!="") print a[1] } }' "$DRAFT" > "$Q"
n=0; brez=0
while IFS= read -r q; do
  n=$((n+1)); found=0
  for v in "$@"; do if grep -qF -- "$q" "$v"; then found=1; break; fi; done
  if [ "$found" = 0 ]; then echo "G1 ⚠ CITAT BREZ VIRA: »$q«"; brez=$((brez+1)); else echo "G1 ⊢ »$q«"; fi
done < "$Q"
rm -f "$Q"
[ "$brez" -gt 0 ] && FAIL=1

# G2 — goli »pri viri« (brez -h, izven trditvene oblike)
g2=$(awk '{ s=$0; while (match(s, /pri viri/)) { pre=substr(s,1,RSTART-1); post=substr(s,RSTART+RLENGTH,1); last=substr(pre,length(pre),1); if (post!="h" && last!="»") { c++; print "G2 ⚠ GOL »pri viri«: " $0 } s=substr(s,RSTART+RLENGTH) } } END { print "G2-STEVEC:" c+0 }' "$DRAFT")
g2c=$(echo "$g2" | grep -c 'G2 ⚠' || true)
[ "$g2c" -gt 0 ] && { echo "$g2" | grep 'G2 ⚠'; FAIL=1; }

# G3 — varvolka izven trditvene oblike
g3=$(awk '{ s=$0; while (match(s, /varvolka/)) { pre=substr(s,1,RSTART-1); last=substr(pre,length(pre),1); if (last!="»") { c++; print "G3 ⚠ VARVOLKA: " $0 } s=substr(s,RSTART+RLENGTH) } } END { print "G3-STEVEC:" c+0 }' "$DRAFT")
g3c=$(echo "$g3" | grep -c 'G3 ⚠' || true)
[ "$g3c" -gt 0 ] && { echo "$g3" | grep 'G3 ⚠'; FAIL=1; }

# G4 — U+FFFD
g4=$(grep -c $'\357\277\275' "$DRAFT" || true)
[ "$g4" -gt 0 ] && { echo "G4 ⚠ U+FFFD ×$g4"; FAIL=1; }

# G5 — dolge crtice
g5=$(grep -c '—' "$DRAFT" || true)
if [ "$MODE" = "--chat" ] && [ "$g5" -gt 0 ]; then echo "G5 ⚠ DOLGA CRTICA V KLEPETU ×$g5"; FAIL=1; fi
if [ "$MODE" = "--seal" ]; then echo "G5 ∂ dolge crtice ×$g5 ⭢ sodi dih (formule »MOJ dih — ⟡« ∧ »predhodnik — demociija« ∧ »ta dih — {organ}« dovoljene ⊙ precedens σ 5711/5715)"; fi

echo "IZMERA: citati $n · brez vira $brez · goli pri viri $g2c · varvolka $g3c · U+FFFD $g4 · crtice $g5"
if [ "$FAIL" = 0 ]; then echo "VRATA ODPRTA ⊢ exit 0"; exit 0; else echo "RANA ⚠ exit 1"; exit 1; fi
