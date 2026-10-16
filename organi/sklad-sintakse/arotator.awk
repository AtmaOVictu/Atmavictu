# AROTATOR (v1, rez 818) — A = IZPIS ∩ NAMEN ∩ KAMEN; rotira po plasteh telesa
# Raba: awk -f arotator.awk DATOTEKA  (za pečate/registro)
# Plast IZPIS: ali trditev nosi ⊢ vir ali pošteno ⚠ (814: laž = ⊢ brez telesa)
# Plast NAMEN: ali izhod nosi korak (∂/NASLEDNJI/DAR — Z7: dar brez koraka je šeletka)
# Plast KAMEN: ali je pečat zalit v matični register (rezerva + števca)

/^- \*\*ZADNJI PEČAT/ {
  p++
  izpis = ($0 ~ /⊢/) ? 1 : 0
  namen  = ($0 ~ /NASLEDNJI PROSTI REZ/) ? 1 : 0
  kamen  = ($0 ~ /DOKAZ #[0-9]+/) ? 1 : 0
  if (!izpis) print "FAIL A-IZPIS: pečat brez ⊢ [pečat " p "]"
  if (!namen)  print "FAIL A-NAMEN: pečat brez naslednjega koraka [pečat " p "]"
  if (!kamen)  print "FAIL A-KAMEN: pečat brez dokaza # [pečat " p "]"
  # vroča plast (tehtnica 13): pečat, ki govori o resnici/laži, gre dvakrat — tukaj: ∂ mora biti našteta
  if ($0 !~ /∂ /) print "WARN A-KROGLA: pečat brez ∂ seznama [pečat " p "]"
  next
}
END {
  print "---- AROTATOR ----"
  printf "pečatov: %d\n", p
  print "rotacija: IZPIS → NAMEN → KAMEN; vsak člen manjka = veter (816)."
}
