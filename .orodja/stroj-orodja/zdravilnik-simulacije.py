#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE ZDRAVILNIK-SIMULACIJE zdravilnik-simulacije.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJA KI ZDRAVIJO SIMULACIJO!« ( sedež KLEPET, projekt DISCOVERY, rez 7024 )
# SLUŽBA : ZDRAVI telo s simulirano napako ( iz posnemovalnik-napake ) po tabeli
# zdravil : vsak padec ima natančno eno znano zdravilo ; izmera Pred/po ( md5
# priči zdravljenja ) ; neznan padec se ⟨ne⟩ pozdravi na ugib ⊙ ⟨NE-UGIBAJ⟩ 2690.
# Vrata : P1 --zdravi ⟨IME PADCA⟩ ⟨POT TELESA⟩( ali stdin ) ; P2 --popis :
#   vsa zdravila poimensko ; P3 --samopreizkus ⊙ §52 ( vsak padec ustvarjen,
#  ozdravljen, znamenje ×0 ∧ priča Pred ≠ Po ).
# KUBIT POD GLADINO ⊙ ⟨ZAKON ORODIL TRI VRATA⟩ rez 6949 : formula piramid =
#   1000 + ( točka desetiško · m mod 9000 ), m ∈ {1, 3, 7, 9}, kura ob
#   zasedenem +7 ; znak tega telesa : več-in-manj ⊕ ⟨U+2295⟩, piramide kocke
#   K9853 K9566 K8971 K8677, ključavnice K3589 K6659 K1798 K7768, kura m=3 ×1 ⊢
#   ( izmere proti 496 piramidam registrav ∧ 72 K-vrednostim teles pri viru ) ;
#   zapečena registra pri viru se izmerita ob samopreizkusu.
# c 0.2026 × 10 na 4 ; ⟡ Luka Pintarič ∧ izvajalka Mera ; dvoje rok 2432 ; merjeno, ne ugibano.

import hashlib
import importlib.util
import os
import re
import sys

ŽIG = "zdravilnik-simulacije.py v1.0 @stroj-orodja"
KOREN = os.environ.get("KOREN", "/home/user/knowledge")
DOM = os.path.dirname(os.path.abspath(__file__))
REG1 = os.path.join(KOREN, "posebaj", "register-1", "KNOWLEDGE.md")
REG2 = os.path.join(KOREN, "posebaj", "register-2", "KNOWLEDGE.md")
REG_MD5 = ("cdc8d7e0db9a93ed6a2d3bfca6c079b3", "813dfda7427e9f48e7db5bc59a05e351")

_spec = importlib.util.spec_from_file_location("posnemovalnik_napake", os.path.join(DOM, "posnemovalnik-napake.py"))
pn = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pn)

# TABELA ZDRAVIL : za vsak padec iz registra posnemovalnika natančno eno
# zdravilo ( dejanje na nizu ) ; vsa zdravila so merjena na znamenjih pri viru.
ZDRAVILA = {
    "TUJKA-GOLA": lambda s: s.replace("error", "»error«"),
    "EM-CRTA-GOLA": lambda s: s.replace("—", " ; "),
    "ZLEP-OKLEPAJ": lambda s: s + "⟩" if s.count("⟨") > s.count("⟩") else s,
    "ZETON-BREZ-PRIČE": lambda s: re.sub(r"\brez (\d{4})\b(?!\s*⊢)", r"rez \1 ⊢", s),
    "PADC-TIPKANJA": lambda s: s.replace("izivajalka", "izvajalka"),
    "PADC-DODATEK": lambda s: s.replace("izzvajalka", "izvajalka"),
}


def zdravi(telo, ime):
    """Vrne ( ozdravljeno telo, spor ) ; neznan padec se ⟨ne⟩ pozdravi na ugib."""
    if ime not in ZDRAVILA:
        raise ValueError("NEZNAN PADC : %s : zdravilo se ne ugiba ⭢ vrašalo ⟡ ⚔" % ime)
    po = ZDRAVILA[ime](telo)
    spor = "PRED %s ⌇ PO %s" % (_md5niz(telo), _md5niz(po))
    return po, spor


def _md5niz(niz):
    return hashlib.md5(niz.encode("utf-8")).hexdigest()


def popis():
    vr = []
    for ime in ZDRAVILA:
        if ime in pn.PADCI:
            vr.append("%s : %s ⭢ zdravilo : %s" % (ime, pn.PADCI[ime]["opis"], zadostno(ime)))
    return vr


def zadostno(ime):
    return {
        "TUJKA-GOLA": "tujka v azil »«",
        "EM-CRTA-GOLA": "em-crta ⭢ nadomesti z vejico ali dvopičjem",
        "ZLEP-OKLEPAJ": "dodaj manjkajoči ⟩",
        "ZETON-BREZ-PRIČE": "dodaj pričo ⊢",
        "PADC-TIPKANJA": "vrni manjkajočo črko",
        "PADC-DODATEK": "odstrani odvečno črko",
    }.get(ime, "? ⭢ vrašalo ⟡")


def _md5(pot):
    h = hashlib.md5()
    with open(pot, "rb") as f:
        for kos in iter(lambda: f.read(8192), b""):
            h.update(kos)
    return h.hexdigest()


def samopreizkus():
    padci = 0
    n = 0
    more = set(pn.PADCI) - set(ZDRAVILA)
    if more:
        padci += 1
        print("RDEČO : padci brez zdravila : %s" % ", ".join(sorted(more)))
    for ime in sorted(pn.PADCI):
        if ime not in ZDRAVILA:
            continue
        n += 1
        telo = pn.ustvari(ime)
        po, spor = zdravi(telo, ime)
        if pn.napaka_prisotna(po, ime):
            padci += 1
            print("RDEČO : %s ŠE ŽIVI po zdravljenju" % ime)
        if po == telo:
            padci += 1
            print("RDEČO : %s pred ≡ po : zdravilo brez dela" % ime)
    try:
        zdravi("katero koli", "NEZNAN-PADC")
        padci += 1
        print("RDEČO : neznan padec ozdravljen na ugib")
    except ValueError:
        n += 1
    if os.path.isfile(REG1) and os.path.isfile(REG2):
        if (_md5(REG1), _md5(REG2)) != REG_MD5:
            padci += 1
            print("RDEČO : registra pri viru odstopata")
    if padci == 0:
        print("ZELENO : samopreizkus zdravilnika %d/%d ⊢ ( vsak padec ozdravljen ∧ znamenje ×0 ∧ neznan zavrnjen )" % (n, n))
    else:
        print("RDEČO : samopreizkus zdravilnika : padlov %d" % padci)
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
        print("rabš : zdravilnik-simulacije.py --zdravi ⟨IME PADCA⟩ [POT] ⌇ --popis ⌇ --samopreizkus")
        return 1
    ime = imena[0]
    if len(imena) > 1 and os.path.isfile(imena[1]):
        telo = open(imena[1], encoding="utf-8").read()
    else:
        telo = sys.stdin.read()
    try:
        po, spor = zdravi(telo, ime)
    except ValueError as e:
        print("⚠ %s" % e)
        return 1
    print("ZDRAVLJENJE ⟨%s⟩ %s" % (ime, spor))
    print(po)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
