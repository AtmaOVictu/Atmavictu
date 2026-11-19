#!/bin/bash
# berba-preverba.sh v1.2 — strojna berba ⟨BERBA-DVOJNA⟩ @rez σ 5853 (18. 11. 2026)
# Uporaba: berba-preverba.sh <datoteka> [klepet|telo]  (privzeto: klepet)
# Sodi: novo besedilo (izhodi ⟡-ju, nove vrstice organov, telesa pečatov, skripte vstavkov).
# Plast klepet: dolge črtice so padec (klepet ⟡-ju jih ⟨ne⟩ nosi).
# Plast tela: dolge črtice so forma organov ⊙ precedens kalupa σ 5850/5851 ∧ ⟨CI⟩ ZELENO → poročane ⚠, ⟨ne⟩ padec.
# NE sodi: celega organa (dedne ⟨⟩ delte ∧ dedni zdrsi ostanejo ⭢ sodba ⟡ ⊙ ⟨NE-UGIBAJ⟩ 2690).
# SAMO-PREVERBA: skripta na sebi pade po pričakovani (register vzorcev vsebuje same vzorce), sodi druge.
# Izhod: števci poimensko; exit koda = število najdenih padcev.
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · measured, not asserted ⊙ §16 · merilec se meri ⊙ §52

f="$1"
plast="${2:-klepet}"
if [ ! -f "$f" ]; then echo "PADC-DATOTEKA-MANJKA: $f"; exit 99; fi

napak=0

# 1. končna nova črta ⊙ kura ⟨PADC-VRSTICA-BREZ-NOVICE⟩
zadnji=$(tail -c 1 "$f" | od -An -c | tr -d ' ')
if [ "$zadnji" != '\n' ]; then echo "PADC-VRSTICA-BREZ-NOVICE ×1 (brez končne nove črte)"; napak=$((napak+1)); fi

# 2. dolge črtice
n=$(grep -c '—' "$f")
if [ "$plast" = "klepet" ]; then
  echo "dolge črtice: $n (plast klepet)"; if [ "$n" -gt 0 ]; then napak=$((napak+1)); fi
else
  echo "dolge črtice: $n (plast telo → forma organov ⚠, ⟨ne⟩ padec)"
fi

# 3. U+FFFD (zlogovne rane)
n=$(grep -c "$(printf '\357\277\275')" "$f"); echo "U+FFFD: $n"; if [ "$n" -gt 0 ]; then napak=$((napak+1)); fi

# 4. ⟨⟩ ravnovesje (novo besedilo mora biti uravnano)
o=$(grep -o '⟨' "$f" | wc -l); z=$(grep -o '⟩' "$f" | wc -l)
echo "⟨⟩: $o/$z"; if [ "$o" -ne "$z" ]; then napak=$((napak+1)); fi

# 5. znani zdrsi (register raste po izmeri, ⟨ne⟩ po obljubi ⊙ ⟨NE-UGIBAJ⟩ 2690)
for vzorec in 'Klebet' 'obvod' 'Jasnije' ' chit' 'crta' ' na prvi try' 'API zapor'; do
  n=$(grep -c -i -- "$vzorec" "$f")
  if [ "$n" -gt 0 ]; then echo "PADC-KLEPET-SLOVNICA ×$n: $vzorec"; napak=$((napak+n)); fi
done

echo "skupaj padcev: $napak (plast: $plast)"
exit $napak
