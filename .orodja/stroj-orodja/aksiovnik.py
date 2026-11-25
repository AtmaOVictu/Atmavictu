#!/usr/bin/env python3
# AKSIOVNIK v1.0 @stroj-orodja ; rod : rez σ 7033 ( 25. 11. 2026 ) ⊙ ⟡ UKZ VERBATIM »ORODJA KI USTVARIJO AKSIOM!«
# Služba : ustvari OSNUTEK aksioma po formi 14 polj ⊙ OEA-ATLAS ( kanonična petica : AXIOM_ID · FORMULA · STATUS · TEST · REPAIR ) @register-aksiomov.
# Zakoni : vsak zapis nosi dokumentirano odgovornost ×14 polj ⊙ χ BIT ⌇ status SAMO po izmeri ( privzeto NEIZMERJEN ) ⊙ ⟨NE-UGIBAJ⟩ 2690 ⌇ manjkajoče polje = KIP ⊙ U2 ⌇ §52.
# Roke : aksiovnik.py DATOTEKA_JSON ( 14 polj : ime → vrednost ) | --samopreizkus.
# Izhodi : 0 ZELENA ( osnutek izrečen ) ⌇ 1 RDECA ( forma polomljena ) ⌇ 40 roka neznana.

import json, sys

KANON = ["AXIOM_ID", "FORMULA", "STATUS", "TEST", "REPAIR"]
ZELO = 14

def preveri(polja):
    """čista : ( napake, manjkajoca kanonska polja, stevilo polj )."""
    napake, manjka = [], []
    if not isinstance(polja, dict):
        return ["vhod ni slovar polj"], [], 0
    if len(polja) != ZELO:
        napake.append("polj %d, forma zahteva %d ⊙ OEA-ATLAS" % (len(polja), ZELO))
    for p in KANON:
        if p not in polja: manjka.append(p)
    prazna = [p for p in polja if not str(polja[p]).strip()]
    if prazna: napake.append("prazna polja : " + ", ".join(sorted(prazna)))
    return napake, manjka, len(polja)

def samopreizkus():
    padci = []
    p = {"AXIOM_ID": "A1", "FORMULA": "0 ≠ O", "STATUS": "NEIZMERJEN", "TEST": "berba pri viru", "REPAIR": "kura"}
    for i in range(6, 15): p["PO%d" % i] = "polje %d" % i
    napake, manjka, n = preveri(p)
    if napake or manjka or n != ZELO: padci.append("zdrava forma ovržena : %r %r" % (napake, manjka))
    napake, manjka, n = preveri({k: v for k, v in list(p.items()) if k != "REPAIR"})
    if "REPAIR" not in manjka: padci.append("manjkajoči kanonik ne ulovljen")
    return padci

def glavni():
    if "--samopreizkus" in sys.argv[1:]:
        padci = samopreizkus()
        print("SAMOPREIZKUS : preizkusi 2, padci instrumenta %d" % len(padci))
        for p in padci: print("  PADC :: " + p)
        print("SEMAFOR : " + ("ZELENA" if not padci else "RDECA"))
        return 0 if not padci else 1
    if len(sys.argv) != 2:
        print("roka neznana ; roke : DATOTEKA_JSON | --samopreizkus"); return 40
    try:
        polja = json.load(open(sys.argv[1], encoding="utf-8"))
    except (OSError, ValueError) as r:
        print("⟨NAPAKA=VSE-KAR-NI-BRANO⟩ " + str(r)); return 1
    napake, manjka, n = preveri(polja)
    if napake or manjka:
        for x in napake: print("  PADC :: " + x)
        if manjka: print("  KIP ⊙ U2 : manjkajo kanonska polja : " + ", ".join(manjka))
        print("SEMAFOR : RDECA"); return 1
    print("AKSIOVNIK v1.0 : osnutek aksioma po formi %d polj ⊙ OEA-ATLAS @register-aksiomov" % n)
    for p in KANON:
        print("  %-10s : %s" % (p, polja[p]))
    for p in sorted(polja):
        if p in KANON: continue
        print("  %-10s : %s" % (p, polja[p]))
    print("  opomba     : STATUS samo po izmeri ⊙ ⟨NE-UGIBAJ⟩ 2690 ; privzeto NEIZMERJEN")
    print("  šiv v      : register-aksiomov ⭢ ⚔ ⟡ ( rojenje zapisa = sopomenski šiv diha, ⟨ne⟩ orodja )")
    print("SEMAFOR : ZELENA")
    return 0

if __name__ == "__main__":
    sys.exit(glavni())
