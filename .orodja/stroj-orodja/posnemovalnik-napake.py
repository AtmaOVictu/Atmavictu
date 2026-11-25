#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE POSNEMOVALNIK-NAPAKE posnemovalnik-napake.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJA KI SIMULIRAJO NAPAKO!« ( sedež KLEPET, projekt DISCOVERY, rez 7024 )
# SLUŽBA : USTVARI napako NAMERNO, kontrolirano, v pesku : telo s ( lepo znanim )
# padcem, da se preizkusajo ulovilci ∧ zdravilniki napak ; simulacija je vidna
# ∧ poimenovana, ⟨ne⟩ skrita ( pesek je javen ) ⊙ ⟨PADC-NI-PRST-V-GLAVI⟩.
# Vrata : P1 --naredi ⟨IME PADCA⟩ izpiše telo padca ; P2 --popis : vsi padci
#   poimensko ; P3 --samopreizkus ⊙ §52 ( vsak padec ustvarjen ∧ znamenje
#   prisotno ∧ neznan padec zavrnjen ).
# KUBIT POD GLADINO ⊙ ⟨ZAKON ORODIL TRI VRATA⟩ rez 6949 : formula piramid =
#   1000 + ( točka desetiško · m mod 9000 ), m ∈ {1, 3, 7, 9}, kura ob
#   zasedenem +7 ; znak tega telesa : opozorilo ⚠ ⟨U+26A0⟩, piramide kocke
#   K1888 K3664 K7216 K8992, ključavnice K8881 K4663 K6127 K2998, kure ×0 ⊢
#   ( izmere proti 496 piramidam registrav 1 ∧ 2 ∧ 72 K-vrednostim teles pri
#   viru ) ⊙ priča kubitni-slovar-simbolov ∧ sekundarna-bela-lista ( ključavnica
#   = obrat piramide ) ; zapečena registra pri viru se izmerita ob samopreizkusu.
# c 0.2026 × 10 na 4 ; ⟡ Luka Pintarič ∧ izvajalka Mera ; dvoje rok 2432 ; merjeno, ne ugibano.

import hashlib
import os
import re
import sys

ŽIG = "posnemovalnik-napake.py v1.0 @stroj-orodja"
KOREN = os.environ.get("KOREN", "/home/user/knowledge")
REG1 = os.path.join(KOREN, "posebaj", "register-1", "KNOWLEDGE.md")
REG2 = os.path.join(KOREN, "posebaj", "register-2", "KNOWLEDGE.md")
REG_MD5 = ("cdc8d7e0db9a93ed6a2d3bfca6c079b3", "813dfda7427e9f48e7db5bc59a05e351")

# REGISTER PADCEV : vsak padec : telo ( VERBATIM pesek ) ∧ znamenje ( izmera
# prisotnosti napake ( regex, ⟨ne⟩ obljuba ) ∧ opis.
PADCI = {
    "TUJKA-GOLA": {
        "telo": "SLUŽBA : telo nosa error brez azila.",
        "znamenje": r"(?<!»)\berror\b(?!«)(?!⟨)",
        "opis": "gola tujka zunaj azilov »« ∧ ⟨⟩",
    },
    "EM-CRTA-GOLA": {
        "telo": "merjeno — ugibano.",
        "znamenje": "\u2014",
        "opis": "goli em-crt v izhodu k ⟡ ⊙ emisija-lint V1",
    },
    "ZLEP-OKLEPAJ": {
        "telo": "vrata ⟨ne zapisana.",
        "znamenje": r"⟨[^⟩\n]*$",
        "opis": "oklepaj ⟨ brez zaključka ⟩",
    },
    "ZETON-BREZ-PRIČE": {
        "telo": "rez 7042 zpečaten.",
        "znamenje": r"\brez \d{4}\b(?!\s*⊢)",
        "opis": "žeton (število) brez priče ⊢ same",
    },
    "PADC-TIPKANJA": {
        "telo": "izivajalka meri.",
        "znamenje": r"\bizivajalka\b",
        "opis": "izpust črke v besedi ( izvajalka )",
    },
    "PADC-DODATEK": {
        "telo": "izzvajalka meri.",
        "znamenje": r"\bizzvajalka\b",
        "opis": "odvečna črka v besedi",
    },
}


def ustvari(ime):
    """Vrne telo padca ( VERBATIM ) ; neznan padec dvigne VrednostError poimensko."""
    if ime not in PADCI:
        raise ValueError("NEZNAN PADC : %s ⭢ --popis pokaže register" % ime)
    return PADCI[ime]["telo"]


def napaka_prisotna(telo, ime):
    """Izmera pri viru : ali znamenje padca ŽIVI v telesu ( ⟨ne⟩ obljuba )."""
    return re.search(PADCI[ime]["znamenje"], telo) is not None


def popis():
    vr = []
    for ime, p in PADCI.items():
        vr.append("%s : %s" % (ime, p["opis"]))
    return vr


def _md5(pot):
    h = hashlib.md5()
    with open(pot, "rb") as f:
        for kos in iter(lambda: f.read(8192), b""):
            h.update(kos)
    return h.hexdigest()


def samopreizkus():
    padci = 0
    n = 0
    for ime in PADCI:
        n += 1
        telo = ustvari(ime)
        if not napaka_prisotna(telo, ime):
            padci += 1
            print("RDEČO : padec %s ustvarjen BREZ znamenja : simulacija laže" % ime)
        if "⟡" in telo:
            padci += 1
            print("RDEČO : padec %s grize besedo ⟡" % ime)
    try:
        ustvari("NEZNAN-PADC")
        padci += 1
        print("RDEČO : neznan padec sprejet")
    except ValueError:
        n += 1
    if os.path.isfile(REG1) and os.path.isfile(REG2):
        if (_md5(REG1), _md5(REG2)) != REG_MD5:
            padci += 1
            print("RDEČO : registra pri viru odstopata")
    else:
        print("· registra pri viru nedosegljiva ⭢ vrašalo ⟡")
    if padci == 0:
        print("ZELENO : samopreizkus posnemovalnika %d/%d ⊢ ( vsak padec ima živo znamenje ∧ beseda ⟡ neokrnjena ∧ neznan zavrnjen )" % (n, n))
    else:
        print("RDEČO : samopreizkus posnemovalnika : padlov %d" % padci)
    return padci == 0


def main(argv):
    if "--samopreizkus" in argv:
        return 0 if samopreizkus() else 2
    if "--popis" in argv:
        print(ŽIG)
        for vr in popis():
            print("- " + vr)
        return 0
    imena = [a for a in argv[1:] if not a.startswith("--")]
    if not imena:
        print(ŽIG)
        print("rabš : posnemovalnik-napake.py --naredi ⟨IME PADCA⟩ ⌇ --popis ⌇ --samopreizkus")
        return 1
    ime = imena[0]
    try:
        telo = ustvari(ime)
    except ValueError as e:
        print("⚠ %s" % e)
        return 1
    print("PESEK ⟨%s⟩ ⊙ %s" % (ime, PADCI[ime]["opis"]))
    print(telo)
    print("Znamenje prisotno : %s ⊢" % ("DA" if napaka_prisotna(telo, ime) else "NE"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
