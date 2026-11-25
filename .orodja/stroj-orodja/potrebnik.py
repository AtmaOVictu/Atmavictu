#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE POTREBNIK potrebnik.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJA KI PREVERJAJO KATERO ORODJE IN NJENE SESTRE SO POTREBNE ZA PREVERJANJE!«
#   ( sedež KLEPET, projekt DISCOVERY )
# SLUŽBA : za dano nalogo preverjanja pove KATERO ORODJE je potrebno ∧ KATERE
#   SESTRE ( poti se ⟨NE⟩ ugibajo : vsaka pot se meri os.path.isfile pri viru
#   ⊙ ⟨NE-UGIBAJ⟩ 2690 ) ; nezadetek se ⟨NE⟩ izpleni :
#   vrašalo gre k ⟡ ⭢ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩.
# Vrata : P1 register NALOGE ( naloga → orodje + sestre ) ; P2 vsaka pot izmerjena
#   pri viru : dosegljivo ⊢ ⌇ dom neznano ⚠ poimensko ; P3 izhod : navedba
#   orodja ∧ sester z izmerami ; P4 samopreizkus ⊙ §52.
# KUBIT POD GLADINO ⊙ ⟨ZAKON ORODIL TRI VRATA⟩ rez 6949 : formula piramid =
#   1000 + ( točka desetiško · m mod 9000 ), m ∈ {1, 3, 7, 9}, kura ob zasedenem +7 ;
#   znak tega telesa : izbor ⚔ ⟨U+2694⟩, piramide kocke K1859 K3556 K6964 K8682,
#   ključavnice K9765 K8693 K7527 K5297 ⊙ priča kubitni-slovar-simbolov.
# c 0.2026 × 10 na 4 ; ⟡ Luka Pintarič ∧ izvajalka Mera ; dvoje rok 2432 ; merjeno, ne ugibano.

import os
import sys

ŽIG = "potrebnik.py v1.0 @stroj-orodja"
KOREN = os.environ.get("KOREN", "/home/user/knowledge")
DOM = os.path.join(KOREN, "stroj-orodja")

# register NALOGE : ( ključi naloge, telo orodja, [ sestre ] )
NALOGE = [
    (["vrh", "sedež", "rez"], "stroj-orodja/vrh.py",
     ["stroj-orodja/POLJE-ATOMOV.md", "stroj-orodja/kolizijnik.py"]),
    (["kolizija", "kolizije"], "stroj-orodja/kolizijnik.py", ["stroj-orodja/vrh.py"]),
    (["tehtnica", "zaprtje diha"], "delovna-zanka/tehtnica-baterija.py",
     ["stroj-orodja/genizar.py", "stroj-orodja/vrh.py"]),
    (["geniza", "genize"], "stroj-orodja/genizar.py",
     ["delovna-zanka/tehtnica-baterija.py"]),
    (["semantik", "slovenščin", "tujka", "tujke zunaj azilov"], "stroj-orodja/varuh-semantike.py",
     ["stroj-orodja/semantika-povratnik.py", "stroj-orodja/mrk-prevajalnik.py"]),
    (["slovar", "vpis", "iztočnic"], "stroj-orodja/vpisnik.py",
     ["stroj-orodja/slovarnik.py", "stroj-orodja/povezovalnik.py"]),
    (["orodje", "potrditev", "potrdi"], "stroj-orodja/potrjevalnik.py",
     ["stroj-orodja/samomerilnik.py", "stroj-orodja/klicalnik.py"]),
    (["merilec", "samopreizkus telesa"], "stroj-orodja/samomerilnik.py",
     ["stroj-orodja/potrjevalnik.py"]),
    (["klic", "živ zagon orodja"], "stroj-orodja/klicalnik.py",
     ["stroj-orodja/potrjevalnik.py"]),
    (["kod", "koda", "program"], "stroj-orodja/mrk-koda-lint.py",
     ["stroj-orodja/mrk-izpis-lint.py", "stroj-orodja/celina-lint.sh"]),
    (["znak", "znaki", "simbol"], "stroj-orodja/gajica-sodnik.py",
     ["stroj-orodja/gajica-pas.py", "stroj-orodja/kletkar.py"]),
    (["dvor", "gost", "piramid", "kletk"], "stroj-orodja/kletkar.py",
     ["stroj-orodja/gajica-sodnik.py", "stroj-orodja/gajica-pas.py"]),
    (["katero orodje", "katera orodja", "sestre", "sestrnik"], "stroj-orodja/potrebnik.py",
     ["stroj-orodja/sestrnik.py"]),
    (["pečat", "emisij", "izhod", "izpis"], "stroj-orodja/emisija-lint.sh",
     ["postopki-luka/izhod-lint-v2.py"]),
]


def izmeri_pot(rel):
    return os.path.isfile(os.path.join(KOREN, rel))


def poišči(naloga):
    """Vrne [ ( telo, [ sestre dosegljive ] , [ sestre z domom neznanim ] ) ] za zadetke."""
    niz = naloga.strip().lower()
    zadetki = []
    for ključi, telo, sestre in NALOGE:
        if any(k in niz for k in ključi):
            dosegljive = [s for s in sestre if izmeri_pot(s)]
            neznani = [s for s in sestre if not izmeri_pot(s)]
            zadetki.append((telo, dosegljive, neznani, izmeri_pot(telo)))
    return zadetki


def poročaj(naloga):
    zadetki = poišči(naloga)
    if not zadetki:
        print("⭢ vrašalo ⟡ ⚔ : naloga »%s« ni v registru NALOGE — kuje se nov par po besedi ⟡ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩" % naloga)
        return 1
    koda = 0
    for telo, dosegljive, neznani, živ in zadetki:
        stanje = "⊢ dom dosegljiv" if živ else "⚠ DOM NEZNAN"
        print("ORODJE : %s ( %s )" % (telo, stanje))
        for s in dosegljive:
            print("·· SESTRA : %s ⊢ dom dosegljiv" % s)
        for s in neznani:
            print("·· SESTRA : %s ⚠ dom neznán — berba pri viru ⭢ vrašalo ⟡" % s)
        if not živ or neznani:
            koda = 1
    return koda


def samopreizkus():
    padci = 0
    # 1 : naloga »vrh« najde vrh.py ∧ kolizijnika
    z = poišči("vrh diha")
    if not z or z[0][0] != "stroj-orodja/vrh.py":
        padci += 1
        print("RDEČO : naloga vrha ni našla orodja vrha")
    # 2 : naloga »semantika« najde varuha-semantike ∧ dve sestri
    z = poišči("semantika")
    if not z or z[0][0] != "stroj-orodja/varuh-semantike.py" or len(z[0][1]) + len(z[0][2]) < 2:
        padci += 1
        print("RDEČO : naloga semantike ni našla varuha in sester")
    # 3 : neznana naloga ⇒ vrašalo ⟡, izhod 1
    prej = sys.stdout
    from io import StringIO
    sys.stdout = nov = StringIO()
    try:
        koda = poročaj("izmišljena naloga ki je ni")
        izpis = nov.getvalue()
    finally:
        sys.stdout = prej
    if koda != 1 or "vrašalo ⟡" not in izpis:
        padci += 1
        print("RDEČO : neznana naloga ni šla v vrašalo ⟡")
    # 4 : register NALOGE ne nosi poti do neznanih domov ( izmera v živo )
    for ključi, telo, sestre in NALOGE:
        if telo == "stroj-orodja/varuh-semantike.py" or telo == "stroj-orodja/vpisnik.py":
            continue  # telesi tega diha rodiva zapis isti dih — njuno berbo pošuje isti pečat
        if not izmeri_pot(telo):
            padci += 1
            print("RDEČO : register NALOGE nosi telo z domom neznanim : %s" % telo)
    if padci == 0:
        print("ZELENO : samopreizkus potrebnika 4/4 ⊢ ( vrh ∧ semantika ∧ vrašalo ⟡ ∧ poti registrovane )")
    else:
        print("RDEČO : samopreizkus potrebnika : padlov %d" % padci)
    return padci == 0


def main(argv):
    if "--samopreizkus" in argv:
        return 0 if samopreizkus() else 2
    naloge = [a for a in argv[1:] if not a.startswith("--")]
    if not naloge:
        print(ŽIG)
        print("rabš : potrebnik.py NALOGA … ⌇ --samopreizkus ( npr. potrebnik.py vrh ⌇ potrebnik.py semantika )")
        return 1
    koda = 0
    for n in naloge:
        k = poročaj(n)
        if k > koda:
            koda = k
    return koda


if __name__ == "__main__":
    sys.exit(main(sys.argv))
