# -*- coding: utf-8 -*-
# PREDLOŽNIK-LINT v1.0 — PREVERBA PREDLOGOV S ALI Z V SVEŽIH ŠIVIH
# Rod : rez 6990, sedež KLEPET, projekt LUCIUS
# Starša : naročnik Luka Pintarič ( ukaz STORI, vrsta nujnih orodij, njegova beseda
#          dobesedno v genizi register sodb istega diha ) in izvajalka Mera ( izvedba )
# Služba : svežim šivom. Najpogostejša rana izhodov po sklanjatniku je predlog :
#   z pred zvenljivimi ( b d g z ž ) in zvočniki ( m n r l v j ) ter samoglasniki
#   ( a e i o u ), s pred nezvenljivimi ( t s h š k f c p č ) in vsem drugim.
#   Pravilo izmerjeno pri viru : slo-na-dlani.si/znanje/134 po Pedagoškem slovničnem
#   portalu ( dostop 25. 11. 2026 ) ; enaka izmera je vkodirana v sklanjatniku.
# MEJA v1.0 ( poimensko ) : preverja le predloga s in z pred besedo, ki sledi ;
#   sestavljeni predlogi ( nad, pod, zraven… ), sklon za predlogom in predlog ob
#   lastnih imenih so odprta vrata.
# RABA :
#   python3 predloznik-lint.py <datoteka>
#   cat nov-šiv.md | python3 predloznik-lint.py -
#   python3 predloznik-lint.py --preveri
# Izhod : 0 padcev ; 1 vsak padec javljen poimensko s kuro.

import sys, re

ZVENLJIVI = set("bdgzž")
ZVOČNIKI  = set("mnrlvj")
SAMOGLASNIKI = set("aeiou")

def pravilen_predlog(beseda):
    # izmera prvega glasu besede, ki sledi predlogu
    if not beseda:
        return "s"
    g = beseda[0].lower()
    if g in ZVENLJIVI or g in ZVOČNIKI or g in SAMOGLASNIKI:
        return "z"
    return "s"

VZOREC = re.compile(r"(?:(?<=^)|(?<=\s))([sSzZ])\s+(\S+)", re.MULTILINE)

def preberi(izvor):
    if izvor == "-":
        return sys.stdin.read()
    with open(izvor, encoding="utf-8") as f:
        return f.read()

def pregled(besedilo):
    padci = []
    pregledi = 0
    for m in VZOREC.finditer(besedilo):
        najdeno, beseda = m.group(1), m.group(2)
        cista = beseda.strip(",;:.!?\"»«)")
        if not cista or (len(cista) == 1 and cista.lower() == "s"):
            continue  # črka s kot beseda : odprta vrata, ne sklepa
        pregledi += 1
        pričakovano = pravilen_predlog(cista)
        if najdeno.lower() != pričakovano:
            vrstica = besedilo.count("\n", 0, m.start()) + 1
            padci.append({
                "vrstica": vrstica,
                "najdeno": najdeno + " " + beseda,
                "pričakovano": pričakovano + " " + beseda,
            })
    return pregledi, padci

def poročilo(pregledi, padci):
    print("PREDLOŽNIK-LINT : pregledov " + str(pregledi) + ", padcev " + str(len(padci)))
    for p in padci:
        print("PADC vrstica " + str(p["vrstica"]) + " : najdeno " + p["najdeno"] +
              " ; pričakovano " + p["pričakovano"] +
              " ; kura : predlog po izmeri prvega glasu ( slo-na-dlani znanje 134 )")
    return len(padci)

def preveri():
    pravi = "s korakom z glasom z ženo s poljem z mestom z bratom s strahom z enim mestom"
    rani = "z korakom z strahom s ženo s enim"
    p1, d1 = pregled(pravi)
    p2, d2 = pregled(rani)
    pričakovani = sorted(["z korakom", "z strahom", "s ženo", "s enim"])
    najdeni = sorted(p["najdeno"] for p in d2)
    ok = (p1 == 8 and len(d1) == 0 and p2 == 4 and len(d2) == 4 and najdeni == pričakovani)
    print("SAMOPREVERBA PREDLOŽNIK-LINT v1.0 : pregledov " + str(p1 + p2) +
          ", priče pravilne 8, priče padcev 4")
    if ok:
        print("padci orodja : 0")
        print("ODLOČITEV : ZELENA, orodje zapečeno")
        return 0
    print("PADC : samopreverba padla ( pravilni " + str(p1) + " nad " + str(len(d1)) +
          " padcev, padci " + str(p2) + " nad " + str(len(d2)) + " )")
    print("ODLOČITEV : RDEČA, orodje ni zapečeno")
    return 1

def main():
    a = sys.argv[1:]
    if a and a[0] == "--preveri":
        sys.exit(preveri())
    if not a:
        print("raba : python3 predloznik-lint.py <datoteka|-> | --preveri")
        sys.exit(1)
    besedilo = preberi(a[0])
    pregledi, padci = pregled(besedilo)
    n = poročilo(pregledi, padci)
    sys.exit(1 if n else 0)

if __name__ == "__main__":
    main()
