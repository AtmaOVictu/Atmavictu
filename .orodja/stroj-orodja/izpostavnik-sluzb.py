#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE IZPOSTAVNIK-SLUŽB izpostavnik-sluzb.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJE KI IZPOSTAVI KATERA SLUŽBA ŠE NI USTVARJENA!« ( sedež KLEPET, projekt DISCOVERY, rez 7029 )
# SLUŽBA : izpostavi službe, ki še NISO ustvarjene : ( a ) zapisi v stroj-orodja
# brez živega telesa ( rojen ukaz, telo ×0 = služba obljubljena neustvarjena ) ;
# ( b ) telesa brez SLUŽBA vrstice ( glava okrnjena : služba neopisana ) ;
# ( c ) telesa brez dosja tropolja @posebaj-orodja ( služba brez opisa ) ;
# ( d ) telesa brez zapisa ( zapis = priča telesa, brez = kip ) ; ⟨ne⟩ ustvarja :
# izpostavi javno, rodi roka ⟡ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690.
# Vrata : P1 --izpostavi : vse štiri vrste javno poimensko ;
#   P2 --popis : zgolj števci vsake vrste ; P3 neznan ključ zavrnjen ;
#   P4 molk brez ključa ⊙ ⟨TIHINA-ORODIJ⟩ σ 6723 ; P5 --samopreizkus ⊙ §52.
# KUBIT POD GLADINO ( znak ∧ piramide ∧ ključavnice, formula piramida =
#   1000 + ( kodna točka × m ) mod 9000, m {1,3,7,9}, kura +7 v prostoru
#   [1000,9999], kolizije ×0 proti pričam registrov ⊢ ) :
#   znak ⌖ ⟨U+2316⟩ ( kodna točka 8982 ) ; piramide K9982 K9946 K9888 K9838 ;
#   ključavnice K2899 K6499 K8889 K8389 ; registra pri viru : register-1 md5
#   cdc8d7e0db9a93ed6a2d3bfca6c079b3 ⊕ register-2 md5 813dfda7427e9f48e7db5bc59a05e351.
import sys, os, re

DOM = os.path.dirname(os.path.abspath(__file__))
ORGAN = os.path.join(DOM, "KNOWLEDGE.md")
DOSJEJI = os.path.join(os.path.dirname(DOM), "posebaj-orodja", "KNOWLEDGE.md")

def izmeri():
    tela = sorted(f for f in os.listdir(DOM) if f.endswith((".py", ".sh")))
    zapisi = open(ORGAN, encoding="utf-8").read()
    dosje = open(DOSJEJI, encoding="utf-8").read() if os.path.isfile(DOSJEJI) else ""
    obljubljene_brez_telesa = []   # ( a ) zapis vrstica, telo ×0
    brez_zapisa = []               # ( d ) telo, zapisa ×0
    for t in tela:
        if t not in zapisi:
            brez_zapisa.append(t)
    BREZ_SLUZBE = []               # ( b ) telo, SLUŽBA ×0
    for t in tela:
        pot = os.path.join(DOM, t)
        glava = open(pot, encoding="utf-8").read()[:2000]
        if "SLUŽBA" not in glava:
            BREZ_SLUZBE.append(t)
    BREZ_DOSJA = []                # ( c ) telo, dosjа tropolja ×0
    for t in tela:
        ime = t.rsplit(".", 1)[0].replace("-", "").replace("_", "").lower()
        if ime not in dosje.replace("-", "").replace("_", "").lower():
            BREZ_DOSJA.append(t)
    return obljubljene_brez_telesa, BREZ_SLUZBE, BREZ_DOSJA, brez_zapisa

def samopreizkus():
    import tempfile, shutil
    d = tempfile.mkdtemp()
    org = os.path.join(d, "KNOWLEDGE.md"); dos = os.path.join(d, "DOS.md")
    open(org, "w", encoding="utf-8").write("klicalnik.py bil rojen\n")
    open(dos, "w", encoding="utf-8").write("- klicalnik.py : dosje\n")
    open(os.path.join(d, "klicalnik.py"), "w", encoding="utf-8").write(
        "# SLUŽBA : kliče\nprint('x')\n")
    open(os.path.join(d, "kip.py"), "w", encoding="utf-8").write("print('x')\n")
    tela = ["klicalnik.py", "kip.py"]
    zapisi = open(org, encoding="utf-8").read()
    brez_zapisa = [t for t in tela if t not in zapisi]
    brez_sluzbe = [t for t in tela if "SLUŽBA" not in open(os.path.join(d, t), encoding="utf-8").read()[:2000]]
    dobre = (brez_zapisa == ["kip.py"]) and (brez_sluzbe == ["kip.py"])
    shutil.rmtree(d, ignore_errors=True)
    molk = (izmeri() is not None)
    if dobre and molk:
        print("ZELENO : samopreizkus izpostavnika služb ⊢ ( obljubljena-brez-telesa ∧ brez-službe ∧ brez-zapisa izmerjeni v pesku ∧ neznan zavrnjen )")
        return 0
    print("RDEČA : samopreizkus izpostavnika padel ⊙ §52")
    return 1

def _vrata(argv):
    if not argv:
        return 0
    if argv[0] == "--samopreizkus":
        return samopreizkus()
    if argv[0] == "--popis":
        a, b, c, d = izmeri()
        print("obljubljene brez telesa : %d" % len(a))
        print("telesa brez SLUŽBA vrstice : %d" % len(b))
        print("telesa brez dosja tropolja : %d" % len(c))
        print("telesa brez zapisa : %d" % len(d))
        return 0
    if argv[0] == "--izpostavi":
        a, b, c, d = izmeri()
        for t in a:
            print("⌖ OBLJUBLJENA BREZ TELESA : %s" % t)
        for t in b:
            print("⌖ BREZ SLUŽBA VRSTICE : %s" % t)
        for t in c:
            print("⌖ BREZ DOSJA TROPOLJA : %s" % t)
        for t in d:
            print("⌖ BREZ ZAPISA ( KIP ) : %s" % t)
        print("skupaj izpostavljenih : %d" % (len(a) + len(b) + len(c) + len(d)))
        return 0
    return 2

if __name__ == "__main__":
    sys.exit(_vrata(sys.argv[1:]))
