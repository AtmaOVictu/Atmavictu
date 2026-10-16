# PREVERJALNIK SINTAKSE V2 (rez 825) — išče po SNOVI, ne po imenih (izmerjena vrzel 824:
# izvedba brez imena je nepreverjiva izvedba; V2 preverja obrazce snovi)
# Raba (peskovna lua brez -f): awk '…ta program…' DATOTEKA
# Preverja: (V2a) pečat: Z-INDEKS prisoten od 825; (V2b) DAR nosi korak (NASLEDNJI);
# (V2c) vezi po snovi (⊢ na vsakem ZADNJI PEČAT — arotator-Logic); (V2d) ∂ z roko v LEDGER;
# (V2e) NE-vrstica v kaskadi (Z5): pečat z AKTIVATOR "daj" mora nositi KAJ-BI-PADLO ali izbiro kanala.

# --- V2a+V2c: zadnji pečati ---
/PEČAT \(rez 8[2-9][0-9]/ || /PEČAT \(rez [9-9][0-9][0-9]/ {
  p++
  if ($0 !~ /⊢/) { print "FAIL V2c [pečat brez ⊢]"; fc++ }
  if ($0 !~ /NASLEDNJI PROSTI REZ/) { print "FAIL V2b [pečat brez NASLEDNJI koraka]"; fb++ }
  if (p > 1 && $0 !~ /Z-INDEKS/) { print "WARN V2a [pečat 825+ brez Z-INDEKSA]"; fa++ }
  if ($0 ~ /AKTIVATOR Luka[^:]*: »daj«/) {
    if ($0 !~ /KANAL|najživej|∂|izbor|izbira/) { print "WARN V2e [kaskadni daj brez NE-preverbe/kanala]"; fe++ }
  }
  next
}
# --- V2d: ∂ vrstice z roko ---
/^∂/ || /∂-[^ ]* [∂⚠⊢]/ {
  d++
  if ($0 !~ /\?|korak|rok|žig|branj|izmer|čaka/) { print "FAIL V2d [∂ brez roke]"; fd++ }
  next
}
END {
  print "---- PREVERJALNIK V2 (snov) ----"
  printf "pečatov %d (⊢-fail %d, korak-fail %d, Z-indeks-warn %d, NE-warn %d) | ∂ %d (rok-fail %d)\n", p, fc+0, fb+0, fa+0, fe+0, d, fd+0
  if (fc+fb+fd == 0) print "SNOV DRŽI: vsak pečat nosi ⊢ + korak; ∂ z rokami ⊢ (do naslednje izmere Z10)."
}
