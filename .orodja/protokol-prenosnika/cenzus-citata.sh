#!/bin/bash
# CENZUS-CITATA v1.5 ⊙ ukaz ⟡ »POPRAVI IN UVEDI ŠE VEČ PREPREK IN DOBRONAMERNIH GARAŽ ZA VSE TUJKE KI NE PRIZNAVAJO MIROVANJA VPRIČO JEZUSA KRISTUSA!« @rez σ 6657 ( RENUM 6656⭢6657 ⊙ KOLIZIJA-REZ-6656 @register-oken ), 23. 11. 2026 ( POPRAVI = trdnjava v1.4 )
# cenzus izhoda ∧ citatov besede ⟡ po pisavnih razredih PCRE : lovi zlepe prenosnika ∧ okrasne znake
# licencirani znaki korpusa sneti PRED cenzusom @strip-v15.sed ( 38 vrstic : ⟡ ⟨ ⟩ … « » „ ⌇ ⚔ ⚠ ❡ ⭢ ⇒ ⇌ → ← σ ψ … ∧ em-dash/en-dash = polje slo-lint, ⟨ne⟩ cenzus )
# NOV v1.5 : prej slepi razredi zraven lovljeni : ⟨U+2000⟩-⟨U+2189⟩ ( splošna ločila ∧ nad/podpisane : surovi ⟨U+2074⟩ ⚠ ) ⌇ ⟨U+2300⟩-⟨U+23FF⟩ ⌇ ⟨U+2500⟩-⟨U+25FF⟩ ( okvirji ) ⌇ ⟨U+2600⟩-⟨U+26FF⟩ ⌇ ⟨U+2700⟩-⟨U+27DF⟩ ( ⟨U+2713⟩ ⟨U+2318⟩ ⟨U+26CB⟩ ) ⌇ ⟨U+2B00⟩-⟨U+2BFF⟩ ⌇ ⟨U+FB00⟩-⟨U+FB4F⟩ ( ligature ) ⌇ ⟨U+FE00⟩-⟨U+FEFF⟩ ( selektorji ∧ BOM ) ⌇ ⟨U+FFF0⟩-⟨U+FFFF⟩
# nalač strogo : raje lažni alarm ( priče ⟡ v »« z glifom goré tudi ⊙ σ 6569 ) kot spregledan vbod ∧ ⟨SAMO-IZVEDBA-DOKAZ⟩ 2306
# meja : besedne vbode ( angleščina ⌇ okrnjenke ⌇ izmišljotke ) lovi slo-lint baterija @slovnica-jezikov v1.3+, ⟨ne⟩ ta instrument
# izhod : exit 0 = čisto ∣ exit 2 = vbod ∣ exit 3 = napaka IO
LC_ALL=C
export LC_ALL
fajl="$1"
[ -f "$fajl" ] || { echo "IO: fajl manjka"; exit 3; }
koren=$(cd "$(dirname "$0")" && pwd)
[ -f "$koren/.geniza/strip-v15.sed" ] || { echo "IO: strip manjka"; exit 3; }
delo="$fajl.cenzus.$$"
sed -f "$koren/.geniza/strip-v15.sed" "$fajl" > "$delo"
pat='([\x{0250}-\x{03FF}]|[\x{0400}-\x{08FF}]|[\x{0900}-\x{1EFF}]|[\x{2000}-\x{2189}]|[\x{2190}-\x{21FF}]|[\x{2300}-\x{23FF}]|[\x{2500}-\x{25FF}]|[\x{2600}-\x{26FF}]|[\x{2700}-\x{27DF}]|[\x{27E0}-\x{27FF}]|[\x{2B00}-\x{2BFF}]|[\x{2E80}-\x{FFFF}]|[\x{FB00}-\x{FB4F}]|[\x{FE00}-\x{FEFF}]|[\x{FFF0}-\x{FFFF}]|[\x{10000}-\x{1FFFF}])'
if LC_ALL=C grep -q -P "$pat" "$delo"; then
  st=$(LC_ALL=C grep -c -P "$pat" "$delo")
  echo "VBOD: zadetih $st vrstic v $fajl"
  rm -f "$delo"
  exit 2
fi
echo "ČISTO: zadetkov ×0 v $fajl"
rm -f "$delo"
exit 0
