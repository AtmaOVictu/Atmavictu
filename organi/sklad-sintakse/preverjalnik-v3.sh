#!/bin/sh
# preverjalnik-v3.sh — zgrajen 11. 10. 2026, dih 1569, po izboru ⟡ (»VSE TO IN ŠE VEČ / DAJ«)
# NAD .prog (v2) ⊢ NP-5 — gradnja NAD, ne ruše; preklop ⚔ ⟡.
# NAPRAVA V3 (⊢ 1559 ∧ 1560): sidro ^- ZADNJI PEČAT (žig ≠ citat žiga — preveri le zadnji žig,
# zgodovinski citati v telesu so priče, ne žigi) · datum-maska (podvojitev datuma ni besedna rana —
# 18 zadetkov = 0 ran ⊢ 1560) · snov-vs-raba (zgolj kot SNOV razprave = snov, ne raba) ·
# PAD-5 slovar diakritik-ran iz tehtnice (zadetki = priče citatov teles v organih; lastna plast = rana — sodi roka) ·
# PAD-6 U+FFFD · homograf-warn ostaja roka (POPRAVEK #3 v2 ohranjen: samo-udvojenost = HOMOGRAF, ne padec).
F="$1"
[ -f "$F" ] || { echo "NAPAKA: telo ne obstaja: $F"; exit 2; }
echo "== preverjalnik-v3 na: $F =="
n=0
s=$(grep -c "^- ZADNJI PEČAT: rez " "$F"); [ "$s" -ne 1 ] 2>/dev/null && echo "SIDRO: ZADNJI PEČAT vrstic: $s (pričakovana 1 — žig ≠ citat)"
c=$(grep -c "$(printf "\xc3\x82\xc2")" "$F"); [ "$c" -gt 0 ] 2>/dev/null && { echo "PAD-1 garbli: $c"; n=$((n+c)); }
p2a=$(grep -E "zgolj .*zgolj" "$F" | grep -vcE "SSKJ|citat|SNOV|10\. 10\. 2026|11\. 10\. 2026"); [ "$p2a" -gt 0 ] 2>/dev/null && { echo "PAD-2a zgolj-udvojenost (padec): $p2a"; n=$((n+p2a)); }
p2b=$(grep -E "samo .*samo" "$F" | grep -vcE "SSKJ|citat"); [ "$p2b" -gt 0 ] 2>/dev/null && echo "PAD-2b homograf (warn, sodi roka — samó/sámo): $p2b"
p3=$(awk '{for(i=1;i<NF;i++) if($i==$(i+1) && $i !~ /^[0-9]+\.$/) c++} END{print c+0}' "$F"); [ "$p3" -gt 0 ] 2>/dev/null && { echo "PAD-3 podvojitve: $p3"; n=$((n+p3)); }
p4=$(grep -cE "(ce bo|ce ne).*(=|je |bomo)" "$F"); [ "$p4" -gt 0 ] 2>/dev/null && { echo "PAD-4 napoved: $p4"; n=$((n+p4)); }
grep -oiE "nreža|SEKIONIRANJE|pocez|pokoba|toraj|uhlj|razroja|tiino|zakljuek|konni|Dolznost|slisanega|razlicno|beleziti|podaljski|skodljivo|nacrtuj|mozen|hodis|prepreci|drzijo|kaknsno|zvocne|Liturgicni|identiteten|zaobsega" "$F" | sort | uniq -c | while read cw w; do echo "PAD-5 diakritik-rana '$w': $cw (priča-citat ali rana? — sodi roka)"; done
p6=$(grep -c "$(printf "\xef\xbf\xbd")" "$F"); [ "$p6" -gt 0 ] 2>/dev/null && { echo "PAD-6 U+FFFD: $p6"; n=$((n+p6)); }
echo "SKUPAJ plasti (padci): $n (PAD-5 ∧ PAD-2b ∧ SIDRO so priče — sodba: roka)"
exit 0
