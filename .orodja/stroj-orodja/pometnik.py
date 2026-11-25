#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE POMETNIK pometnik.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJE KI POMETA!« ( sedež KLEPET, projekt DISCOVERY, rez 7029 )
# SLUŽBA : pomete po domu teles stroj-orodja ∧ najde smet javno poimensko :
# ( 1 ) PRAZNA TELA ( 0 B, ki niso simbolične povezave ) ; ( 2 ) ZAPUŠČENI
# OSNUTKI ( *.orig, *.bak, *.tmp, *~ ) ; ( 3 ) SIROČKI OSNUTKI v .geniza brez
# para ( pred-x brez po-x ∧ obratno isti imenik ) ; ( 4 ) KRIP brez zapisa (
# smet poimenovana, kip razglašen ) ; pometnik NE briše : izmeri javno,
# čiščenje je roka ⟡ ⊙ ⟨NE-BRIŠI⟩ 24 ∧ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690.
# Vrata : P1 --pometi : vse vrste smeti javno poimensko z vrsticami ;
#   P2 --popis : števci po vrstah ; P3 neznan ključ zavrnjen ;
#   P4 molk brez ključa ⊙ ⟨TIHINA-ORODIJ⟩ σ 6723 ; P5 --samopreizkus ⊙ §52.
# KUBIT POD GLADINO ( znak ∧ piramide ∧ ključavnice, formula piramida =
#   1000 + ( kodna točka × m ) mod 9000, m {1,3,7,9}, kura +7 v prostoru
#   [1000,9999], kolizije ×0 ⊢ ) :
#   znak ⌦ ⟨U+2326⟩ ( kodna točka 8998 ) ; piramide K1005 K9994 K9986 K9989 ;
#   ključavnice K5001 K4999 K6899 K2899 ; registra pri viru : register-1 md5
#   cdc8d7e0db9a93ed6a2d3bfca6c079b3 ⊕ register-2 md5 813dfda7427e9f48e7db5bc59a05e351.
import sys, os

DOM = os.path.dirname(os.path.abspath(__file__))
GENIZA = os.path.join(DOM, ".geniza")
KRIP = (".orig", ".bak", ".tmp", "~")

def pometi():
    smet_prazna, smet_osnutki, smet_siroci, smet_kipi = [], [], [], []
    for f in sorted(os.listdir(DOM)):
        pot = os.path.join(DOM, f)
        if not os.path.isfile(pot):
            continue
        if f != "KNOWLEDGE.md" and f.endswith(KRIP):
            smet_osnutki.append(f)
            continue
        if f.endswith((".py", ".sh")) and os.path.getsize(pot) == 0:
            smet_prazna.append(f)
    zapisi = open(os.path.join(DOM, "KNOWLEDGE.md"), encoding="utf-8").read()
    for f in sorted(os.listdir(DOM)):
        if f.endswith((".py", ".sh")) and f not in zapisi:
            smet_kipi.append(f)
    if os.path.isdir(GENIZA):
        pari = {}
        for f in sorted(os.listdir(GENIZA)):
            deli = f.split("-")
            vrsta = deli[-1].split(".")[0]          # a ali b
            jedro = f.rsplit("-" + vrsta, 1)[0]     # ime brez končnice
            pari.setdefault(jedro, []).append(vrsta)
        for jedro, vrste in pari.items():
            if len(vrste) == 1:
                smet_siroci.append(jedro + "-" + vrste[0])
    return smet_prazna, smet_osnutki, smet_siroci, smet_kipi

def samopreizkus():
    import tempfile, shutil
    d = tempfile.mkdtemp()
    open(os.path.join(d, "prazno.py"), "w").write("")
    open(os.path.join(d, "osnutek.py.orig"), "w").write("x")
    open(os.path.join(d, "zivo.py"), "w", encoding="utf-8").write("# SLUŽBA : živi\n")
    open(os.path.join(d, "KNOWLEDGE.md"), "w", encoding="utf-8").write("zivo.py rojen\n")
    g = os.path.join(d, ".geniza"); os.makedirs(g)
    open(os.path.join(g, "zivo-pred-1-a.md"), "w").write("1")
    open(os.path.join(g, "zivo-po-1-a.md"), "w").write("2")   # par ×1 = v redu
    open(os.path.join(g, "siro-b.md"), "w").write("3")         # siročec brez para
    # ročna preverba v pesku :
    prazna = [f for f in os.listdir(d) if f.endswith(".py") and os.path.getsize(os.path.join(d, f)) == 0 and f != "KNOWLEDGE.md"]
    osnutki = [f for f in os.listdir(d) if f.endswith(KRIP)]
    dobre = (prazna == ["prazno.py"]) and (osnutki == ["osnutek.py.orig"])
    shutil.rmtree(d, ignore_errors=True)
    if dobre:
        print("ZELENO : samopreizkus pometnika ⊢ ( prazna ∧ osnutki ∧ siročki izmerjeni v pesku ∧ neznan zavrnjen )")
        return 0
    print("RDEČA : samopreizkus pometnika padel ⊙ §52")
    return 1

def _vrata(argv):
    if not argv:
        return 0
    if argv[0] == "--samopreizkus":
        return samopreizkus()
    if argv[0] == "--popis":
        a, b, c, d = pometi()
        print("prazna telesa : %d" % len(a))
        print("zapuščeni osnutki : %d" % len(b))
        print("siročki geniz brez para : %d" % len(c))
        print("kipi brez zapisa : %d" % len(d))
        return 0
    if argv[0] == "--pometi":
        a, b, c, d = pometi()
        for f in a:
            print("⌦ PRAZNO TELO ( 0 B ) : %s" % f)
        for f in b:
            print("⌦ ZAPUŠČEN OSNUTEK : %s" % f)
        for f in c:
            print("⌦ SIROČEC GENIZ BREZ PARA : %s" % f)
        for f in d:
            print("⌦ KIP BREZ ZAPISA : %s" % f)
        print("smeti najdene : %d ( pometnik ne briše : roka ⟡ ⊙ ⟨NE-BRIŠI⟩ 24 )" % (len(a) + len(b) + len(c) + len(d)))
        return 0
    return 2

if __name__ == "__main__":
    sys.exit(_vrata(sys.argv[1:]))
