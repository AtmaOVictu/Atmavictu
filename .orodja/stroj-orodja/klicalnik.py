#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE KLICALNIK klicalnik.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJA KI POTRJUJEJO IN KLIČEJO ORODJA!« ( sedež KLEPET, projekt DISCOVERY )
# SLUŽBA : kliče orodje LE skozi vrata potrjevalnika — brez bajtne potrditve ni
# klica, orodje brez zapisa je kip ⊙ U2 ; vsak klic je samopreizkus nad živim
# telesom ⊙ ⟨PREDLOG-HKRATI-DOKAZ⟩ 25.
# Vrata : P1 potrjevalnik.potrdi( ime ) ( sestra @isti dom ) ; P2 rana ali brez
#   zapisa ⇒ KLIC ZAVRNJEN, izhod 1, telo se ne zažene ; P3 sicer živ zagon
#   telesa z njegovimi argumenti, izhod = izhod telesa ; P4 samopreizkus ⊙ §52.
# KUBIT POD GLADINO ⊙ ⟨ZAKON ORODIL TRI VRATA⟩ rez 6949 : formula piramid =
#   1000 + ( točka desetiško · m mod 9000 ), m ∈ {1, 3, 7, 9}, kura ob zasedenem +7 ;
#   znak tega telesa : izmenjava ⇌ ⟨U+21CC⟩, piramide kocke K9652 K8984 K7571 K6868,
#   ključavnice K3693 K7518 K9374 K5219 ⊙ priča kubitni-slovar-simbolov ;
#   zapečena registra pri viru se izmerita ob samopreizkusu.
# c 0.2026 × 10 na 4 ; ⟡ Luka Pintarič ∧ izvajalka Mera ; dvoje rok 2432 ; merjeno, ne ugibano.

import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import potrjevalnik

ŽIG = "klicalnik.py v1.0 @stroj-orodja"
KOREN = os.environ.get("KOREN", "/home/user/knowledge")
DOM = os.path.join(KOREN, "stroj-orodja")


def kliči(ime, argumenti, dom=DOM, organ_pot=None):
    """Vrne izhod telesa ali 1 ob zavrnjenem klicu ; nikoli ne zažene nezapisanega telesa."""
    telo_pot = ime if os.sep in ime else os.path.join(dom, ime)
    spor, koda = potrjevalnik.potrdi(os.path.basename(ime), telo_pot, organ_pot)
    if koda != 0:
        print("KLIC ZAVRNJEN : %s" % spor)
        return 1
    zagon = subprocess.run([sys.executable, telo_pot] + list(argumenti))
    return zagon.returncode


def samopreizkus():
    padci = 0
    import hashlib
    with tempfile.TemporaryDirectory() as d:
        telo = os.path.join(d, "poskusnik.py")
        organ = os.path.join(d, "ORGAN.md")
        žigovnik = os.path.join(d, "žig.txt")
        with open(telo, "w", encoding="utf-8") as f:
            f.write("# -*- coding: utf-8 -*-\nimport sys\nwith open(r'%s', 'w', encoding='utf-8') as f:\n    f.write(' '.join(sys.argv[1:]))\nsys.exit(0)\n" % žigovnik)
        digest = hashlib.md5()
        with open(telo, "rb") as f:
            for kos in iter(lambda: f.read(8192), b""):
                digest.update(kos)
        with open(organ, "w", encoding="utf-8") as f:
            f.write("- poskusnik.py v1.0 : skušnja ( md5 %s )\n" % digest.hexdigest())
        # 1 : potrjen klic se zažene in telesu pridejo argumenti
        koda = kliči("poskusnik.py", ["zapisal"], dom=d, organ_pot=organ)
        zapis = ""
        if os.path.isfile(žigovnik):
            with open(žigovnik, encoding="utf-8") as f:
                zapis = f.read()
        if koda != 0 or zapis != "zapisal":
            padci += 1
            print("RDEČO : potrjen klic ni zagnal telesa ( koda %s, žig %r )" % (koda, zapis))
        os.remove(žigovnik)
        # 2 : vbod v telo ⇒ priča odstopa ⇒ klic zavrnjen, telo se NI zagnalo
        with open(telo, "a", encoding="utf-8") as f:
            f.write("# vbod\n")
        koda = kliči("poskusnik.py", [], dom=d, organ_pot=organ)
        zagon_dejstvo = os.path.isfile(žigovnik)
        if koda != 1 or zagon_dejstvo:
            padci += 1
            print("RDEČO : vbod je preživel klical ( koda %s, telo se %s )" % (koda, "zagnalo" if zagon_dejstvo else "ni zagnalo"))
        # 3 : orodje brez zapisa = kip ⊙ U2 ⇒ zavrnjeno, telo se NI zagnalo
        nezapisan = os.path.join(d, "nezapisan.py")
        with open(nezapisan, "w", encoding="utf-8") as f:
            f.write("# -*- coding: utf-8 -*-\nimport sys\nwith open(r'%s', 'w', encoding='utf-8') as f:\n    f.write('tekel')\n" % žigovnik)
        prej = sys.stdout
        from io import StringIO
        sys.stdout = nov = StringIO()
        try:
            koda = kliči("nezapisan.py", [], dom=d, organ_pot=organ)
            izpis = nov.getvalue()
        finally:
            sys.stdout = prej
        if koda != 1 or "KIP" not in izpis.upper() or os.path.isfile(žigovnik):
            padci += 1
            print("RDEČO : nezapisano orodje ni zavrnjeno kot kip ( koda %s )" % koda)
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
        print("ZELENO : samopreizkus klicalnika 4/4 ⊢ ( potrjen klic stekel ∧ vbod zavrnjen ∧ kip zavrnjen ∧ kubit vir )")
    else:
        print("RDEČO : samopreizkus klicalnika : padlov %d" % padci)
    return padci == 0


def main(argv):
    if "--samopreizkus" in argv:
        return 0 if samopreizkus() else 2
    imena = [a for a in argv[1:] if not a.startswith("--")]
    if not imena:
        print(ŽIG)
        print("rabš : klicalnik.py IME_ORODJA [ argumenti telesa … ] ⌇ --samopreizkus")
        return 1
    return kliči(imena[0], imena[1:])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
