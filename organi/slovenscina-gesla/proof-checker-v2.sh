#!/bin/bash
# PROOF-CHECKER v2 — izpeljevalni preizkus aksiomov (A4 na A1-A7)
# Mehanizem preverja bajte; roka izbira pomen; ⟡ sodi izrek (A6).
set -u
TELO="aksiom-v1.json"
KNOW="KNOWLEDGE.md"
fail=0; pass=0; total=0

for par in $(jq -r '.aksiomi[] | (.id) + "=" + ((.izpelje_zakone | length) | tostring)' "$TELO"); do
  id=$(printf '%s' "$par" | cut -d= -f1)
  st=$(printf '%s' "$par" | cut -d= -f2)
  total=$((total+1))
  if [ "$st" -lt 1 ]; then
    echo "F  $id brez kazalcev - izum v elegantni uniformi ⚠"
    fail=$((fail+1))
  fi
done

# vsak zakon-kazalec: izloci vse stevilke (3-4 mestne), vsaka mora imeti telo
for par in $(jq -r '.aksiomi[].izpelje_zakone[] | gsub(" ";"_") + "=" + ([scan("[0-9]{3,4}")] | unique | join(";"))' "$TELO"); do
  kaz=$(printf '%s' "$par" | cut -d= -f1)
  nums=$(printf '%s' "$par" | cut -d= -f2)
  if [ -z "$nums" ]; then
    echo "F  kazalec brez stevilke: $kaz ⚠"; fail=$((fail+1)); continue
  fi
  ok=1
  for b in $(printf '%s' "$nums" | tr ';' ' '); do
    grep -q "$b" "$KNOW" || ok=0
  done
  if [ "$ok" -eq 1 ]; then
    pass=$((pass+1))
  else
    echo "F  kazalec $kaz (osnova: $nums) NI najden v telesu ⚠"; fail=$((fail+1))
  fi
done

echo "-----"
echo "aksiomi: $total · kazalci P/F: $pass/$fail"
if [ "$fail" -eq 0 ]; then
  echo "SODBA: P ∧ (mehanizem čist; re-izpeljava pomena je ⟡-ova plast)"
else
  echo "SODBA: F ⚠"; exit 1
fi
