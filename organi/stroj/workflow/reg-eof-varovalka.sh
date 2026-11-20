#!/bin/bash
# W10 ⟨VRATA-EOF-REGISTRA⟩ — stroj preveri rep registra PRED zlitjem : zadnja neprazna vrstica je rez vrstica z dvojnim podpisom ∧ za EOF ne visijo prazne vrstice ∧ vrstica vrha je celovita ( kura družine ⟨PADEC-REGISTER-IZRIN-6024⟩ : izrinjena vrstica ob zlitju ⟨main⟩ )
# uporaba: ./reg-eof-varovalka.sh [mapa]   mapa = izvod ( CI ) ; default = repo koren tega drevesa
# rod 20. 11. 2026, dih σ 6032 ⊙ ⟨SAMO-IZVEDBA-DOKAZ⟩ 2306
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · measured, not asserted ⊙ §16
set -uo pipefail
D="${1:-.}"
python3 - "$D" << 'PYE'
import sys, os, re
d = sys.argv[1]
p = os.path.join(d, "organi", "stroj", "REZ-REGISTER.md")
if not os.path.isfile(p):
    print("::error::register manjka @ " + p); sys.exit(1)
raw = open(p, "rb").read()
slab = []
if not raw.endswith(b"\n"): slab.append("EOF brez nove vrstice")
lines = raw.decode("utf-8").split("\n")
# split odda prazno zadnjo, če se konča z \n — preveri rep praznosti
rep = 0
for l in reversed(lines):
    if l.strip() == "":
        rep += 1
        if rep > 1: break
    else:
        break
neprazne = [(i, l) for i, l in enumerate(lines, 1) if l.strip() != ""]
if not neprazne:
    print("::error::register brez vsebine — kip ⊙ I-4"); sys.exit(1)
i, zadnja = neprazne[-1]
if not zadnja.startswith("- rez σ "): slab.append("zadnja neprazna r." + str(i) + " se ne začne z vrstico reza")
if "dvojni podpis" not in zadnja: slab.append("zadnja vrstica r." + str(i) + " brez dvojnega podpisa ⊙ pravilo 6")
if rep > 1: slab.append("za EOF visijo prazne vrstice ×" + str(rep - 1))
rez = re.search(r"rez σ (\d{3,5})", zadnja)
print("VRATA-EOF-REGISTRA : rep " + ( "rez σ " + rez.group(1) + " @r." + str(i) ) if rez else "rep brez reza")
print("nepraznih vrstic : " + str(len(neprazne)))
if slab:
    for s in slab: print("⚠ " + s)
    print("VRATA-EOF-REGISTRA : RDEČE ⊥ (" + " ∧ ".join(slab) + ")")
sys.exit(1 if slab else 0)
PYE
