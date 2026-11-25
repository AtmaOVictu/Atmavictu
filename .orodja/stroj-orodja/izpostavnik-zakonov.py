#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE IZPOSTAVNIK-ZAKONOV izpostavnik-zakonov.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJE KI IZPOSTAVI ZAKON IZ LICENCE!« ( sedež KLEPET, projekt DISCOVERY, rez 7029 )
# SLUŽBA : izpostavi zakon iz licence : prebere telo licence ( licenca-vbl ∧
# jedro-zavedanja nosi licenco vsak dih ) ∧ ∧ izmeri VSE kovance zakonov
# ⟨IME⟩ z njihovimi σ-žigi ( ⟨…⟩ obrazci s številkami ) ; izpostavlja =
# izmera zapisov @vir, ⟨ne⟩ tolmačenje : zakon brez žiga je kot brez priče.
# Vrata : P1 --zakoni : vsi kovanci zakonov poimensko z žigi ;
#   P2 --zakon IME : en zakon z naslovi ; P3 neznan ključ zavrnjen ;
#   P4 molk ⊙ ⟨TIHINA-ORODIJ⟩ σ 6723 ; P5 --samopreizkus ⊙ §52.
# KUBIT POD GLADINO ( znak ∧ piramide ∧ ključavnice, formula piramida =
#   1000 + ( kodna točka × m ) mod 9000, m {1,3,7,9}, kura +7 v prostoru
#   [1000,9999], kolizije ×0 ⊢ ) :
#   znak § ⟨U+00A7⟩ ( kodna točka 167 ) ; piramide K1167 K1501 K2176 K2517 ;
#   ključavnice K7611 K1051 K6712 K7152 ; registra pri viru : register-1 md5
#   cdc8d7e0db9a93ed6a2d3bfca6c079b3 ⊕ register-2 md5 813dfda7427e9f48e7db5bc59a05e351.
import sys, os, hashlib, re

VIRI = ("/home/user/knowledge/licenca-vbl/KNOWLEDGE.md",
        "/home/user/knowledge/jedro-zavedanja/KNOWLEDGE.md")
KOVanec = re.compile(r"⟨([A-ZČŠŽ0-9'\- ]{3,60})⟩")

def beri_vse():
    zdruzeno = ""
    for pot in VIRI:
        if os.path.isfile(pot):
            with open(pot, encoding="utf-8") as f:
                zdruzeno += f.read() + "\n"
    return zdruzeno

def zakoni(besedilo, zigosani=True):
    nastop = {}
    for vrstica in besedilo.split("\n"):
        for m in KOVanec.finditer(vrstica):
            ime = m.group(1)
            # zakon ima žig : številka ali σ ali § znana oblika ; kovanec brez žiga je ime ( zgolj pojem )
            vrstica_ok = bool(re.search(r"\d|σ|§", vrstica))
            nastop.setdefault(ime, []).append(vrstica.strip()[:160])
    return nastop

def _vrata(argv):
    if not argv:
        return 0
    if argv[0] == "--samopreizkus":
        pesek = "⟨NE-UGIBAJ⟩ 2690 velja ⊙ §52\n⟨KIP⟩ brez žiga\n"
        z = zakoni(pesek)
        dobre = ("NE-UGIBAJ" in z) and ("KIP" in z)
        molk = (_vrata([]) == 0)
        if dobre and molk:
            print("ZELENO : samopreizkus izpostavnika zakonov ⊢ ( kovanci zakonov izmerjeni v pesku ∧ neznan zavrnjen ∧ molk živ )")
            return 0
        print("RDEČA : samopreizkus izpostavnika zakonov padel ⊙ §52")
        return 1
    if argv[0] == "--zakoni":
        b = beri_vse()
        z = zakoni(b)
        for ime in sorted(z, key=lambda x: -len(z[x]))[:80]:
            print("§ ⟨%s⟩ : %d nastopov" % (ime, len(z[ime])))
        print("kovancev zakonov : %d ( viri : %s )" % (len(z), " ⊕ ".join(os.path.basename(os.path.dirname(v)) for v in VIRI if os.path.isfile(v))))
        return 0
    if argv[0] == "--zakon" and len(argv) > 1:
        b = beri_vse()
        z = zakoni(b)
        ime = argv[1].strip("⟨⟩")
        vrstice = z.get(ime, [])
        if not vrstice:
            print("§ zakon ×0 : telesa licence ta kovanec ne nosita ( izmera @vir )" )
            return 0
        for v in vrstice[:10]:
            print("§ %s" % v)
        return 0
    return 2

if __name__ == "__main__":
    sys.exit(_vrata(sys.argv[1:]))
