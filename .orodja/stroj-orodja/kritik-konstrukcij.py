#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE KRITIK-KONSTRUKCIJ kritik-konstrukcij.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJA KI KRITIZIRAJO KONSTRUKCIJO KI NI V SLOVENŠČINI!« ( sedež KLEPET, projekt DISCOVERY, rez 7027 )
# SLUŽBA : kritizira konstrukcije, ki niso v slovenščini ( v telesih ∧ izhodih
# korpusa ) : tujke zunaj azilov »«, tuje pisave ( cirilica ) zunaj azilov,
# tujkne zveze ; vsaka kritika poimensko z ZAKAJ ∧ KURO ( slovenski predlog ) ;
# ⟨ne⟩ popravlja, ⟨ne⟩ sodi : kritik izmeri, roka ⟡ odloča ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690.
# Vrata : P1 --preveri DATOTEKA izpiše kritike poimensko z vrsticami ;
#   P2 --popis izpiše register kritik ; P3 azili »« ⟨ne⟩ kritizirani ( tujka v
#   azilu je gost pod domačo licenco @domovanje-tujk ) ; P4 neznan ključ zavrnjen ;
#   P5 molk brez ključa ⊙ ⟨TIHINA-ORODIJ⟩ σ 6723 ( izhod 0, beseda ×0 ) ;
#   P6 --samopreizkus v živo ⊙ §52 ( pesek : vsaka kritika najdena ∧ kura
#   predlagana ∧ azil spoštovan ∧ neznan zavrnjen ) ; P7 out = izhod 0, rana = 1.
# KUBIT POD GLADINO ( rezerviran znak ∧ piramide ∧ ključavnice, formula piramida =
#   1000 + ( kodna točka × m ) mod 9000, m vrstni red {1,3,7,9}, kura +7 ob
#   zasedenosti ∧ kolizije preverjene proti 869 pričam registrov pri viru ⊢ ) :
#   znak ≠ ⟨U+2260⟩ ( kodna točka 8800 ) ; piramide K9807 K9414 K8607 K8207 ;
#   ključavnice K7089 K4149 K7068 K7028 ; registra pri viru : register-1 md5
#   cdc8d7e0db9a93ed6a2d3bfca6c079b3 ⊕ register-2 md5 813dfda7427e9f48e7db5bc59a05e351.
import sys, re, unicodedata

REGISTER = [
    # par : ( ujeta , vzorec , kura , zakaj ) : tujke živijo kot predmet peska v »«
    ("»update«",   r"\bupdate\b",   "posodobitev", "angleška tujka zunaj azila"),
    ("»file«",     r"\bfile\b",     "datoteka",    "angleška tujka zunaj azila"),
    ("»print«",    r"\bprint\b",    "natis",       "angleška tujka zunaj azila"),
    ("»default«",  r"\bdefault\b", "privzeto",    "angleška tujka zunaj azila"),
    ("»start«",    r"\bstart\b",    "zagon",       "angleška tujka zunaj azila"),
    ("»end«",      r"\bend\b",      "konec",       "angleška tujka zunaj azila"),
    ("»help«",     r"\bhelp\b",     "pomoč",       "angleška tujka zunaj azila"),
    ("»input«",    r"\binput\b",    "vhod",        "angleška tujka zunaj azila"),
    ("»output«",   r"\boutput\b",   "izhod",       "angleška tujka zunaj azila"),
    ("»error«",    r"\berror\b",    "napaka",      "angleška tujka zunaj azila"),
    ("»tool«",     r"\btool\b",     "orodje",      "angleška tujka zunaj azila"),
    ("»queue«",    r"\bqueue\b",    "vrsta",       "angleška tujka zunaj azila"),
]
CIRILICA = re.compile(r"[\u0400-\u04FF]+")   # zveza znakov = ena kritika, ne znak po znak
PISAVA_ZAKAJ = "cirilska pisava zunaj azila, prevedi v gajico"

def molk_stroja(besedilo):
    """plasta stroja ( P8 ) : navednice podatkov ∧ ukazi print( = slovnica
    pythona, ⟨ne⟩ konstrukcija korpusa : te igra molka"""
    obsegi = []
    for m in re.finditer(r'"(?:[^"\\]|\\.)*"', besedilo):
        obsegi.append((m.start(), m.end()))
    for m in re.finditer(r"'(?:[^'\\]|\\.)*'", besedilo):
        obsegi.append((m.start(), m.end()))
    for m in re.finditer(r"\bprint\s*\(", besedilo):
        obsegi.append((m.start(), m.end()))
    return obsegi

def azili(besedilo):
    """vrsti obsege azilov »...« — tujka znotraj azila je gost ⊙ @domovanje-tujk"""
    obsegi = []
    for m in re.finditer(r"»[^»]*«", besedilo):
        obsegi.append((m.start(), m.end()))
    return obsegi

def v_azilu(i, obsegi):
    return any(a <= i < b for a, b in obsegi)

def kritike(besedilo, stroj=False):
    """izmeri vse kritike : ( vrstica , ujeta , kura , zakaj ) ; stroj=True
    uposti plasto molka stroja ( P8 )"""
    obsegi = azili(besedilo)
    if stroj:
        obsegi = obsegi + molk_stroja(besedilo)
    vis = []
    for ujeta, vzorec, kura, zakaj in REGISTER:
        for m in re.finditer(vzorec, besedilo):
            if not v_azilu(m.start(), obsegi):
                vrstica = besedilo.count("\n", 0, m.start()) + 1
                vis.append((vrstica, ujeta, kura, zakaj))
    for m in CIRILICA.finditer(besedilo):
        if not v_azilu(m.start(), obsegi):
            vrstica = besedilo.count("\n", 0, m.start()) + 1
            vis.append((vrstica, "cirilica", "gajica", PISAVA_ZAKAJ))
    return sorted(vis)

def samopreizkus():
    # pesek : ( besedilo , pričakovano št. kritik ) : tujka v azilu = gost, ne kritika
    pesek = [
        ("posodobi »update« telesa", 0),
        ("update telesa", 1),
        ("print docela v glavi", 1),
        ("vrsta queue teče", 1),
        ("file in output skupaj", 2),
        ("mir, brez tujk", 0),
        ("ожила je beseda zunaj", 1),
        ("»ожила« v azilu", 0),
    ]
    dobre = True
    for besedilo, pričakovano in pesek:
        najdeno = len(kritike(besedilo))
        if najdeno != pričakovano:
            dobre = False
    # neznan ključ zavrnjen ( P4 ) : izhod 2, molk ( P5 ) : izhod 0 brez besede
    neznan = (_vrata(["--neznankljuc"]) == 2)
    molk = (_vrata([]) == 0)
    if dobre and neznan and molk:
        print("ZELENO : samopreizkus kritika konstrukcij ⊢ ( vsaka kritika izmerjena ∧ azili spoštovani ∧ neznan zavrnjen ∧ molk živ )")
        return 0
    print("RDEČA : samopreizkus kritika padel ⊙ §52")
    return 1

def _vrata(argv):
    if len(argv) == 0:
        return 0                       # molk ⊙ σ 6723
    klj = argv[0]
    if klj == "--samopreizkus":
        return samopreizkus()
    if klj == "--popis":
        for ujeta, vzorec, kura, zakaj in REGISTER:
            print("- %s → %s ( %s )" % (ujeta, kura, zakaj))
        print("- cirilica → gajica ( %s )" % PISAVA_ZAKAJ)
        return 0
    if klj == "--preveri" and len(argv) > 1:
        try:
            with open(argv[1], encoding="utf-8") as f:
                besedilo = f.read()
        except OSError as e:
            print("rana pri berbi :", e)
            return 1
        stroj = argv[1].endswith(".py")
        vis = kritike(besedilo, stroj=stroj)
        for vrstica, ujeta, kura, zakaj in vis:
            print("≠ r.%d : %s → %s ( %s )" % (vrstica, ujeta, kura, zakaj))
        print("kritike : %d" % len(vis))
        return 0
    return 2                           # neznan zavrnjen ( P4 )

if __name__ == "__main__":
    sys.exit(_vrata(sys.argv[1:]))
