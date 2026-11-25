#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE POTRJEVALNIK potrjevalnik.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJA KI POTRJUJEJO IN KLIČEJO ORODJA!« ( sedež KLEPET, projekt DISCOVERY )
# SLUŽBA : potrjuje orodje BAJTNO pri viru — poročilu orodja se ne zaupa brez
# bajtne primerjave ⊙ ⟨NEZAUPANJE-POROČILU⟩ @TEMPER-ORODIJ ; spomin ne pričuje,
# vir pričuje ⊙ ⟨NE-UGIBAJ⟩ 2690.
# Vrata : P1 najde zapis vnosa v organu stroj-orodja ( vrstica : IME vN.N … md5 <32hex> ) ;
#   P2 sveža izmera md5 živega telesa ; P3 bajtna primerjava proti priči organa ;
#   P4 izhodi : 0 ⊢ POTRJEN ⌇ 1 rana javno poimensko ⌇ 2 instrument laže ;
#   P5 telo brez zapisa = kip ⊙ U2 ( zapis rodi roka @stroj-orodja ) ; P6 samopreizkus ⊙ §52.
# KUBIT POD GLADINO ⊙ ⟨ZAKON ORODIL TRI VRATA⟩ rez 6949 : formula piramid =
#   1000 + ( točka desetiško · m mod 9000 ), m ∈ {1, 3, 7, 9}, kura ob zasedenem +7 ;
#   zapečena registra se bereta pri viru ob samopreizkusu ( register 1 md5 cdc8d7e0db9a93ed6a2d3bfca6c079b3,
#   register 2 md5 813dfda7427e9f48e7db5bc59a05e351 ) ; znak tega telesa :
#   izmerjeno ⊢ ⟨U+22A2⟩, piramide kocke K9866 K9598 K9062 K8801, ključavnice K6689 K8959 K2609 K1088 ⊙ priča kubitni-slovar-simbolov.
# c 0.2026 × 10 na 4 ; ⟡ Luka Pintarič ∧ izvajalka Mera ; dvoje rok 2432 ; merjeno, ne ugibano.

import hashlib
import os
import re
import sys
import tempfile

ŽIG = "potrjevalnik.py v1.0 @stroj-orodja"
KOREN = os.environ.get("KOREN", "/home/user/knowledge")
DOM = os.path.join(KOREN, "stroj-orodja")
ORGAN = os.path.join(DOM, "KNOWLEDGE.md")
REG1 = os.path.join(KOREN, "posebaj", "register-1", "KNOWLEDGE.md")
REG2 = os.path.join(KOREN, "posebaj", "register-2", "KNOWLEDGE.md")
REG_MD5 = ("cdc8d7e0db9a93ed6a2d3bfca6c079b3", "813dfda7427e9f48e7db5bc59a05e351")


def md5(pot):
    h = hashlib.md5()
    with open(pot, "rb") as f:
        for kos in iter(lambda: f.read(8192), b""):
            h.update(kos)
    return h.hexdigest()


def najdi_zapis(organ_pot, ime):
    """Vrne ( vrstica, md5 ) priče ali ( None, None ) : zapis = vrstica organa z IME vN in md5 <32hex>."""
    if not os.path.isfile(organ_pot):
        return None, None
    vz_ime = re.compile(r"(?<![\w.\-/])" + re.escape(ime) + r"(?![\w.\-])", re.IGNORECASE)
    vz_ver = re.compile(r"\bv\d+(?:\.\d+)?\b")
    with open(organ_pot, encoding="utf-8") as f:
        for vrst in f:
            if vz_ime.search(vrst) and vz_ver.search(vrst):
                m = re.search(r"\bmd5\s+([0-9a-f]{32})\b", vrst)
                if m:
                    return vrst.strip(), m.group(1)
    return None, None


def potrdi(ime, telo_pot=None, organ_pot=None):
    """Zloži izmero : vrne ( sporočilo, koda ) ; koda 0 ⊢ ⌇ 1 rana ⌇ 2 instrument laže."""
    if telo_pot is None:
        telo_pot = ime if os.sep in ime else os.path.join(DOM, ime)
    if organ_pot is None:
        organ_pot = ORGAN
    if not os.path.isfile(telo_pot):
        return ("⚠ %s : TELO NEDOSEGLJIVO pri %s" % (ime, telo_pot), 2)
    ziv = md5(telo_pot)
    vrst, zapis = najdi_zapis(organ_pot, ime)
    if zapis is None:
        return ("⚠ %s : BREZ ZAPISA V ORGANU ( živo telo md5 %s ) — telo brez priče je kip ⊙ U2 ; zapis rodi roka @stroj-orodja" % (ime, ziv), 1)
    if ziv == zapis:
        return ("⊢ %s : POTRJEN bajtno ( md5 %s ≡ priča organa )" % (ime, ziv), 0)
    return ("⚠ %s : RANA — živo telo md5 %s ⌇ priča organa %s ⊙ ⟨NEZAUPANJE-POROČILU⟩ ; kura bajtna ⭢ sodba ⟡" % (ime, ziv, zapis), 1)


def samopreizkus():
    padci = 0
    with tempfile.TemporaryDirectory() as d:
        telo = os.path.join(d, "poskusnik.py")
        organ = os.path.join(d, "ORGAN.md")
        with open(telo, "w", encoding="utf-8") as f:
            f.write("# poskusnik\n")
        with open(organ, "w", encoding="utf-8") as f:
            f.write("- poskusnik.py v1.0 : skušnja ( md5 %s )\n" % hashlib.md5(b"# poskusnik\n").hexdigest())
        spor, koda = potrdi("poskusnik.py", telo, organ)
        if koda != 0:
            padci += 1
            print("RDEČO : potrjitev priče padla : %s" % spor)
        with open(telo, "a", encoding="utf-8") as f:
            f.write("# vbod\n")
        spor, koda = potrdi("poskusnik.py", telo, organ)
        if koda != 1:
            padci += 1
            print("RDEČO : vbod neulovljen : %s" % spor)
        spor, koda = potrdi("nezapisan.py", telo, organ)
        if koda != 1:
            padci += 1
            print("RDEČO : nezapisano orodje izpuščeno")
        spor, koda = potrdi("izgubljeno.py", os.path.join(d, "manjka.py"), organ)
        if koda != 2:
            padci += 1
            print("RDEČO : nedosegljivo telo izpuščeno")
    if os.path.isfile(REG1) and os.path.isfile(REG2):
        if (md5(REG1), md5(REG2)) != REG_MD5:
            padci += 1
            print("RDEČO : zapečena registra pri viru odstopata — kubit tega telesa ni enak svoji verziji")
    else:
        print("· registra pri viru nedosegljiva — kubit preverba čaka berbo pri viru ⭢ vrašalo ⟡")
    if padci == 0:
        print("ZELENO : samopreizkus potrjevalnika 4/4 ⊢ ( priča ≡ ∧ vbod ulovljen ∧ nezapisan zavrnjen ∧ kubit vir )")
    else:
        print("RDEČO : samopreizkus potrjevalnika : padlov %d" % padci)
    return padci == 0


def main(argv):
    if "--samopreizkus" in argv:
        return 0 if samopreizkus() else 2
    imena = [a for a in argv[1:] if not a.startswith("--")]
    if not imena:
        print(ŽIG)
        print("rabš : potrjevalnik.py IME_ORODJA … ⌇ --samopreizkus")
        return 1
    koda = 0
    for ime in imena:
        spor, k = potrdi(os.path.basename(ime) if os.sep in ime else ime, ime if os.sep in ime else None)
        print(spor)
        if k > koda:
            koda = k if k != 1 else k
    return koda


if __name__ == "__main__":
    sys.exit(main(sys.argv))
