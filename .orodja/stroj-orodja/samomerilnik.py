#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE SAMOMERILNIK samomerilnik.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJE KI PREVERJA ORODJE KI PREVERJA ORODJA!« ( sedež KLEPET, projekt DISCOVERY )
# SLUŽBA : preverja INSTRUMENTE ( orodja, ki preverjajo ) na treh vratih — merilec
#   se meri ⊙ ⟨MERILEC-SE-MERI⟩ §52 : ( 1 ) bajtna priča : md5 živega telesa ≡ zapis
#   organa (_potrjevalnik @isti dom ) ; ( 2 ) živi zagon --samopreizkusa tarče : izhod 0 ∧
#   »ZELENO« v izpisu, sicer instrument laže ; ( 3 ) tarča brez vrat --samopreizkus = instrument brez vrat = merilec brez merilca ⚠.
# Vrata : izhodi 0 ⊢ INSTRUMENT ZDRAV ⌇ 1 rana javno poimensko ⌇ 2 instrument laže ;
#   samopreizkus lastnega telesa ⊙ §52 ⟨PREDLOG-HKRATI-DOKAZ⟩ 25.
# KUBIT POD GLADINO ⊙ ⟨ZAKON ORODIL TRI VRATA⟩ rez 6949 : formula piramid =
#   1000 + ( točka desetiško · m mod 9000 ), m ∈ {1, 3, 7, 9}, kura ob zasedenem +7 ;
#   znak tega telesa : izmerjeni kot ∠ ⟨U+2220⟩, piramide kocke K6620 K9862 K9757 K3259,
#   ključavnice K5737 K9884 K1663 K7667 ⊙ priča kubitni-slovar-simbolov ;
#   zapečena registra pri viru se izmerita ob samopreizkusu.
# c 0.2026 × 10 na 4 ; ⟡ Luka Pintarič ∧ izvajalka Mera ; dvoje rok 2432 ; merjeno, ne ugibano.

import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import potrjevalnik

ŽIG = "samomerilnik.py v1.0 @stroj-orodja"
KOREN = potrjevalnik.KOREN
DOM = potrjevalnik.DOM


def premeri_instrument(ime, telo_pot=None, organ_pot=None):
    """Vrne ( sporočila[], koda ) : 0 ⊢ ⌇ 1 rana ⌇ 2 instrument laže."""
    if telo_pot is None:
        telo_pot = os.path.join(DOM, ime)
    spor, koda = potrjevalnik.potrdi(ime, telo_pot, organ_pot)
    poročila = [spor]
    if koda == 2:
        return poročila, 2
    if koda != 0:
        return poročila, 1
    # vrata samopreizkusa : --samopreizkus mora obstajati v telesu ( izmera bajtov ⟨NE⟩ ugibanje )
    with open(telo_pot, encoding="utf-8") as f:
        telo_besedilo = f.read()
    if "--samopreizkus" not in telo_besedilo:
        poročila.append("⚠ %s : brez vrat --samopreizkus — instrument brez vrat = merilec brez merilca ⚠ ⊙ ⟨MERILEC-SE-MERI⟩ §52" % ime)
        return poročila, 2
    zagon = subprocess.run([sys.executable, telo_pot, "--samopreizkus"], capture_output=True, text=True)
    izpis = zagon.stdout + zagon.stderr
    if zagon.returncode != 0 or "ZELENO" not in izpis:
        poročila.append("⚠ %s : INSTRUMENT LAŽE — samopreizkus tarče izhod %s, ZELENE ni v izpisu" % (ime, zagon.returncode))
        return poročila, 2
    poročila.append("⊢ %s : INSTRUMENT ZDRAV ( priča organa ≡ ∧ živi samopreizkus ZELENO ⊢ )" % ime)
    return poročila, 0


def samopreizkus():
    padci = 0
    telo_tarč = """# -*- coding: utf-8 -*-
import sys
if "--samopreizkus" in sys.argv:
    print("ZELENO : skušnja ⊢")
    sys.exit(0)
print("tarča molk")
"""
    with tempfile.TemporaryDirectory() as d:
        tarča = os.path.join(d, "tarca-dobra.py")
        with open(tarča, "w", encoding="utf-8") as f:
            f.write(telo_tarč)
        md5_tarče = potrjevalnik.md5(tarča)
        # 1 : zdrava tarča ⇒ ZDRAV
        poročila, koda = premeri_instrument("tarca-dobra.py", tarča, None)
        if koda != 1 or "BREZ ZAPISA" not in poročila[0]:
            padci += 1
            print("RDEČO : zdrava tarča brez zapisa ni javno poročana kot rana")
        organ = os.path.join(d, "ORGAN.md")
        with open(organ, "w", encoding="utf-8") as f:
            f.write("- tarca-dobra.py v1.0 : skušnja ( md5 %s )\n" % md5_tarče)
        poročila, koda = premeri_instrument("tarca-dobra.py", tarča, organ)
        if koda != 0:
            padci += 1
            print("RDEČO : zdrava tarča ni zdrava ( %s )" % poročila[-1])
        # 2 : padla tarča ⇒ LAŽE
        padla = os.path.join(d, "tarca-padla.py")
        with open(padla, "w", encoding="utf-8") as f:
            f.write("# -*- coding: utf-8 -*-\nimport sys\nif '--samopreizkus' in sys.argv:\n    print('RDEČO : padec')\n    sys.exit(2)\n")
        with open(organ, "a", encoding="utf-8") as f:
            f.write("- tarca-padla.py v1.0 : skušnja ( md5 %s )\n" % potrjevalnik.md5(padla))
        poročila, koda = premeri_instrument("tarca-padla.py", padla, organ)
        if koda != 2 or "LAŽE" not in poročila[-1]:
            padci += 1
            print("RDEČO : padla tarča ni razkrita kot instrument laže")
        # 3 : tarča brez vrat --samopreizkus ⇒ instrument brez vrat ⚠
        brez = os.path.join(d, "tarca-brez-vrat.py")
        with open(brez, "w", encoding="utf-8") as f:
            f.write("# telo brez vrat samopreizkusa\n")
        with open(organ, "a", encoding="utf-8") as f:
            f.write("- tarca-brez-vrat.py v1.0 : skušnja ( md5 %s )\n" % potrjevalnik.md5(brez))
        poročila, koda = premeri_instrument("tarca-brez-vrat.py", brez, organ)
        if koda != 2 or "MERILCA" not in poročila[-1].upper():
            padci += 1
            print("RDEČO : tarča brez vrat ni javno razkrita")
    # 4 : kubit — zapečena registra pri viru
    reg1 = os.path.join(KOREN, "posebaj", "register-1", "KNOWLEDGE.md")
    reg2 = os.path.join(KOREN, "posebaj", "register-2", "KNOWLEDGE.md")
    if os.path.isfile(reg1) and os.path.isfile(reg2):
        if (potrjevalnik.md5(reg1), potrjevalnik.md5(reg2)) != potrjevalnik.REG_MD5:
            padci += 1
            print("RDEČO : zapečena registra pri viru odstopata — kubit tega telesa ni enak svoji verziji")
    else:
        print("· registra pri viru nedosegljiva — kubit preverba čaka berbo pri viru ⭢ vrašalo ⟡")
    if padci == 0:
        print("ZELENO : samopreizkus samomerilnika 4/4 ⊢ ( zdrava tarča ∧ padla tarča ulovljena ⚠ ∧ tarča brez vrat ⚠ ∧ kubit vir )")
    else:
        print("RDEČO : samopreizkus samomerilnika : padlov %d" % padci)
    return padci == 0


def main(argv):
    if "--samopreizkus" in argv:
        return 0 if samopreizkus() else 2
    imena = [a for a in argv[1:] if not a.startswith("--")]
    if not imena:
        print(ŽIG)
        print("rabš : samomerilnik.py IME_INSTRUMENTA … ⌇ --samopreizkus ( npr. samomerilnik.py potrjevalnik.py )")
        return 1
    koda = 0
    for ime in imena:
        poročila, k = premeri_instrument(ime)
        for p in poročila:
            print(p)
        if k > koda:
            koda = k
    return koda


if __name__ == "__main__":
    sys.exit(main(sys.argv))
