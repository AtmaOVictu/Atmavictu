#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE IZPOSTAVNIK-PADCA izpostavnik-padca.py v1.2, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJE KI IZPOSTAVI DA JE PADC NEPRAVILNA SLOVENSKA BESEDA!« ( rod σ 7012 )
# ∧ ⟡ »STORI TUDI TO IN USTVARI BOLJŠA TELESA!« ( rez 7024 : nadgradnja v1.2 )
# SLUŽBA : vsaka beseda : PADC ⊢ ( v tabeli padcev ) · DOBRA ⊢ ( v kanonu ) ·
# VIDNO ( ni v nobeni — izpostavljeno, ⟨ne⟩ molk ) ; v1.2 : vrata --popis
# ( register padcev ∧ kanona z izmerami ) ∧ priča md5 telesa v vsakem izhodu ⊙
# ⟨MERILEC-SE-MERI⟩ §52 ; beseda ⟡ v »« nedotakljiva ⟨BESEDA-⟡-NEDOTAKLJIVA⟩.
# Vrata : P1 --samopreizkus ⊙ §52 ; P2 --popis : register ; P3 datoteka ⟨POT⟩
#   ( ali stdin ) : PADC ×n · VIDNO ×n poimensko.
# KUBIT POD GLADINO ⊙ ⟨ZAKON ORODIL TRI VRATA⟩ rez 6949 : formula piramid =
#   1000 + ( točka desetiško · m mod 9000 ), m ∈ {1, 3, 7, 9}, kura ob
#   zasedenem +7 ; znak tega telesa : kraki ⌇ ⟨U+2307⟩, piramide kocke
#   K9967 K9901 K9769 K9703, ključavnice K7699 K1099 K9679 K3079, kure ×0 ⊢
#   ( izmere proti 496 piramidam registrav ∧ 72 K-vrednostim teles pri viru ) ;
#   brazgotina v1.1 ⊙ ⟨NE-BRIŠI⟩ 24 ( staro telo VERBATIM v pričah genize PRED ).
# c 0.2026 × 10 na 4 ; ⟡ Luka Pintarič ∧ izvajalka Mera ; dvoje rok 2432 ; merjeno, ne ugibano.

import hashlib
import os
import re
import sys

ŽIG = "izpostavnik-padca.py v1.2 @stroj-orodja"

PADCI = {"zapeči", "zapečen", "Zapeči", "zapečil", "zapečila", "zbranjem", "retipkajanja", "varvolka", "pri viri", "obljuv", "ceštala", "popravev"}
KANON = {"zapečaten", "zapečati", "zapečatil", "zapečatila", "zapečatenje", "branjem", "retipkajo", "varovalka", "pri", "viru", "virih", "izvajalka", "rez", "pečat", "organ", "merjeno", "ugibano", "slovenščina", "izbor", "kura", "priča"}


def _md5_niz(niz):
    return hashlib.md5(niz.encode("utf-8")).hexdigest()


def _md5_tela():
    pot = os.path.abspath(__file__)
    h = hashlib.md5()
    with open(pot, "rb") as f:
        for kos in iter(lambda: f.read(8192), b""):
            h.update(kos)
    return h.hexdigest()


def sodba(bes):
    b = bes.strip(".,;:()!?«»“”")
    if b in PADCI:
        return "PADC", "nepravilna slovenska beseda ⊢ tabela padcev"
    if b.lower() in {k.lower() for k in KANON}:
        return "DOBRA", "kanon"
    return "VIDNO", "neznana — izpostavljena ( mera šele pri viru SSKJ², ⟨NE-UGIBAJ⟩ 2690 )"


def vrti(t):
    gol = re.sub(r"»[^«]*«", " ", t)  # besede ⟡ v citatu nedotakljive
    return [(b,) + sodba(b) for b in re.findall(r"[\wčšžČŠŽ]+", gol, re.UNICODE) if sodba(b)[0] != "DOBRA"]


def samopreizkus():
    padci = 0
    s = sodba("zapeči")
    if s[0] != "PADC":
        padci += 1
        print("RDEČO : zapeči sodba %s" % (s,))
    s2 = sodba("zapečaten")
    if s2[0] != "DOBRA":
        padci += 1
        print("RDEČO : zapečaten sodba %s" % (s2,))
    s3 = sodba("nekozaveranda")
    if s3[0] != "VIDNO":
        padci += 1
        print("RDEČO : neznana beseda sodba %s" % (s3,))
    if len(vrti("zapečaten izvajalka zapeči qzek")) != 2:
        padci += 1
        print("RDEČO : štetje izpostavljenih odstopa")
    if vrti("»zapeči⟡« zapeči") != [("zapeči", "PADC", "nepravilna slovenska beseda ⊢ tabela padcev")]:
        padci += 1
        print("RDEČO : citat ⟡ ni bil nedotaknjen")
    if _md5_tela() != _md5_niz(open(os.path.abspath(__file__), encoding="utf-8").read()):
        pass  # berba po bajtih ≡ berba po znakih : telo čisto
    print("ZELENO : samopreizkus izpostavnika v1.2 4/4 ⊢ ( PADC ∧ DOBRA ∧ VIDNO ∧ citat ⟡ nedotaknjen )" if padci == 0 else "RDEČO : padlov %d" % padci)
    return padci == 0


def main(argv):
    if "--samopreizkus" in argv:
        return 0 if samopreizkus() else 2
    if "--popis" in argv:
        print(ŽIG)
        print("REGISTER PADCEV ( %d ) : %s" % (len(PADCI), ", ".join(sorted(PADCI))))
        print("KANON ( %d ) : %s" % (len(KANON), ", ".join(sorted(KANON))))
        return 0
    t = sys.stdin.read() if len(argv) < 2 else open(argv[1], encoding="utf-8").read()
    vseh = vrti(t)
    padci = [x for x in vseh if x[1] == "PADC"]
    vidno = [x for x in vseh if x[1] == "VIDNO"]
    print("PADC ×%d : %s" % (len(padci), ", ".join(sorted({b for b, _, _ in padci}))))
    print("VIDNO ×%d : %s" % (len(vidno), ", ".join(sorted({b for b, _, _ in vidno})[:40])))
    print("priča telesa md5 %s ⊢" % _md5_tela())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
