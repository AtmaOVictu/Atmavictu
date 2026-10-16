# PREVERJALNIK SINTAKSE BJS (v1, rez 818) — velja za vrstice ZAKON/REZ/∂/UTRIP
# Raba: awk -f preverjalnik-sintakse.awk DATOTEKA
# Padec je veljaven izid (rez 386) — izpiše se, ne skrije.

# ZAKON:  Z(id) :: POZITIVNI IZREK [— negacija šele nato] ⊢ vir
/^Z\([^)]*\) *::/ {
  z++; if ($0 !~ /⊢/) { print "FAIL [ZAKON brez ⊢ vira]: " substr($0,1,80); fz++ }
  else if ($0 !~ /⚠|ŽIG|⊢ [A-ZŠČŽ]/) { print "WARN [ZAKON: vir neimenovan s telesom?]: " substr($0,1,80); wz++ }
  next
}
# REZ:    R(n) NASLOV | AKTIVATOR | OS | ... | K(γ,ost,tal,o) | VEZI… | ∂…
/^R\([0-9]+\) / { r++; if ($0 !~ /∂/) { print "WARN [REZ brez ∂ odprtja]: " substr($0,1,80); wr++ } next }
# ∂:      ∂(id)@vir : VPRAŠANJE ? NASLOVNIK [rok]
/^∂\([^)]*\)@[^ ]* *:/ {
  d++; rok = ($0 ~ /\[[^]]+\]/) ? 1 : 0
  nas = ($0 ~ /\?/) ? 1 : 0
  if (!rok || !nas) { print "FAIL [∂ brez naslovnika ali roke (PREMER-4)]: " substr($0,1,90); fd++ }
  next
}
# UTRIP:  T(datum) ORGAN : IZVEDBA ~ sled
/^T\([0-9.]+\) [^:]*:/ { t++; if ($0 !~ /~/) { print "WARN [UTRIP brez sledi ~]: " substr($0,1,80); wt++ } next }
# kanonične zanke v skladu (Z1..Z12) — telo s pričo (597)
/^Z[0-9]+ [^ ]+ ::/ {
  k++; if ($0 !~ /⊢/) { print "FAIL [zanka brez ⊢ priče]: " substr($0,1,80); fk++ } next
}
END {
  print "---- PREVERJALNIK SINTAKSE ----"
  printf "ZAKON %d (fail %d) | REZ %d (warn %d) | ∂ %d (fail %d) | UTRIP %d (warn %d) | zanke %d (fail %d)\n", z, fz+0, r, wr+0, d, fd+0, t, wt+0, k, fk+0
  if (fz+fd+fk > 0) print "SKLEP: telo pada — padci zapisani, ne skriti (Z6)."
  else print "SKLEP: sintaksa drži ⊢ (do naslednje izmere, Z10)."
}
