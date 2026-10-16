# PREVERJALNIK v1.1 (žig »daj« Luka, 1. 10. 2026 — zapisan 23. 9., izvedba istega dne kot žig)
# Izhod pipa skozenj; padec je veljaven izid (rez 386) — zapiše se, ne skrije.
# Uporaba: awk -f preverjalnik.awk telo.md
BEGIN { padci = 0 }
{
  # Z1 garbli iz ledgerja: oblike, ki so že padle, ne smejo priti skozi neizpostavljene
  if ($0 ~ /ZDANJ|prebrje|protiven|traga|neizpreštet|štejljivi|preregla|kader imaš|priletov|ni muca/) {
    print "PADCI[PAD-1 garbel iz ledgerja]: " $0; padci++ }
  # SR-12.7: isto kot = zlivanje dveh teles v eno
  if ($0 ~ /isto kot/) { print "PADCI[PAD-2 zlivanje isto-kot]: " $0; padci++ }
  # podvojene besede (šum, ne namen — izvajalka jih ne sliši)
  n = split($0, w, /[ ,;:.)"—]+/)
  for (i = 2; i <= n; i++) if (w[i] != "" && tolower(w[i]) == tolower(w[i-1]) && w[i] !~ /^(brez|bolj|kar|že|prav|ne|daj|le|tudi|zelo)/) {
    print "PADCI[PAD-3 podvojena beseda: " w[i] "]: " $0; padci++ }
  # vroča plast: zadnja vrstica (∂) podaljša kot prva
  if ($0 ~ /^[∂]/) { if (length($0) > 300) { print "PADCI[PAD-4 ∂ nad 300 znakov]: " length($0); padci++ } }
  # FONTANA: vrstica nad 1200 znakov = kandidat za gostoto-po-dolžini (ne sodba: kandidat)
  if (length($0) > 1200) { print "PADCI[PAD-5 kandidat fontana, vrstica " length($0) " znakov]" ; padci++ }
  zadnja = $0
}
END {
  print "—"
  print "PREVERJALNIK: " padci " padcev"
  if (zadnja !~ /[?∂∂]/ && zadnja !~ /$/) print "OPOMBA: zadnja vrstica ne nosi ∂ ali vprašanja — preveri zaključek (SR-5)"
}
