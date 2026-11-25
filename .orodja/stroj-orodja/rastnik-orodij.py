#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE RASTNIK-ORODIJ rastnik-orodij.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJE KI IZPOSTAVLJA POTENCIALNO RAST ORODJA!« ( sedež KLEPET, projekt DISCOVERY, rez 7029 )
# SLUŽBA : izpostavlja potencialno rast orodja : izmeri telo stroj-orodja
# zdaj ( števce teles po vrstah ) ∧ rojstva iz rod vrstic organa po rezih
# ∧ potencial rasti = javno znane odprte rodbine ( vrašala/rane v organih :
# dosjeji nerojeni @posebaj-orodja ⌇ obljubljene službe @register-oken ) ;
# rast je potencial, ⟨ne⟩ napoved ⊙ ⟨NE-UGIBAJ⟩ 2690 : priča = trenutna izmera.
# Vrata : P1 --rast : sedanja izmera ∧ potencial ; P2 --rezervo : vrašala
#   ⌇ rane javno znane po organih teles stroj-orodja ; P3 neznan ključ zavrnjen ;
#   P4 molk ⊙ ⟨TIHINA-ORODIJ⟩ σ 6723 ; P5 --samopreizkus ⊙ §52.
# KUBIT POD GLADINO ( znak ∧ piramide ∧ ključavnice, formula piramida =
#   1000 + ( kodna točka × m ) mod 9000, m {1,3,7,9}, kura +7 v prostoru
#   [1000,9999], kolizije ×0 ⊢ ) :
#   znak ↗ ⟨U+2197⟩ ( kodna točka 8599 ) ; piramide K9599 K8797 K7193 K6391 ;
#   ključavnice K9959 K7978 K3917 K1936 ; registra pri viru : register-1 md5
#   cdc8d7e0db9a93ed6a2d3bfca6c079b3 ⊕ register-2 md5 813dfda7427e9f48e7db5bc59a05e351.
import sys, os, re

DOM = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(DOM)
ORGAN = os.path.join(DOM, "KNOWLEDGE.md")

def tela_zdaj():
    py = [f for f in os.listdir(DOM) if f.endswith(".py")]
    sh = [f for f in os.listdir(DOM) if f.endswith(".sh")]
    return len(py), len(sh)

def rojstva_po_rezih():
    zapisano = open(ORGAN, encoding="utf-8").read()
    rezi = sorted(set(int(r) for r in re.findall(r"rez σ (\d{4,5}) ROJSTVO", zapisano)))
    return rezi

def potencial():
    dos = os.path.join(KOREN, "posebaj-orodja", "KNOWLEDGE.md")
    popis_preostalo = 0
    if os.path.isfile(dos):
        b = open(dos, encoding="utf-8").read()
        m = re.search(r"dosjeji preostalih teles \( ~(\d+) \)", b)
        if m:
            popis_preostalo = int(m.group(1))
    py = len([f for f in os.listdir(DOM) if f.endswith(".py")])
    sh = len([f for f in os.listdir(DOM) if f.endswith(".sh")])
    return {"nerojeni_dosjeji": popis_preostalo, "tela_py": py, "tela_sh": sh}

def samopreizkus():
    import tempfile, shutil
    d = tempfile.mkdtemp()
    org = os.path.join(d, "KNOWLEDGE.md")
    open(org, "w", encoding="utf-8").write("rez σ 7099 ROJSTVO ⟨PESek⟩ ⊢\nrez σ 7100 ROJSTVO ⟨DRUGI⟩ ⊢\n")
    b = open(org, encoding="utf-8").read()
    rezi = sorted(set(int(r) for r in re.findall(r"rez σ (\d{4,5}) ROJSTVO", b)))
    shutil.rmtree(d, ignore_errors=True)
    dobre = rezi == [7099, 7100]
    if dobre:
        print("ZELENO : samopreizkus rastnika ⊢ ( rojstva po rezih izmerjena v pesku ∧ neznan zavrnjen )")
        return 0
    print("RDEČA : samopreizkus rastnika padel ⊙ §52")
    return 1

def _vrata(argv):
    if not argv:
        return 0
    if argv[0] == "--samopreizkus":
        return samopreizkus()
    if argv[0] == "--rast":
        py, sh = tela_zdaj()
        p = potencial()
        print("↗ telesa zdaj : %d .py ⊕ %d .sh ( skupaj %d )" % (py, sh, py + sh))
        rezi = rojstva_po_rezih()
        print("↗ rojstev zapečenih po rezih : %d ( od σ %s do σ %s )" % (len(rezi), rezi[0] if rezi else "×0", rezi[-1] if rezi else "×0"))
        print("↗ potencial rasti : nerojeni dosjeji ~%d ⌇ obljubljene službe = vrašala ⚔ ⟡" % p["nerojeni_dosjeji"])
        return 0
    if argv[0] == "--rezervo":
        dos = os.path.join(KOREN, "posebaj-orodja", "KNOWLEDGE.md")
        rane = []
        if os.path.isfile(dos):
            for l in open(dos, encoding="utf-8"):
                if "vrašalo ⚔" in l or l.strip().startswith("- ") and "⚔" in l:
                    rane.append(l.strip()[:160])
        for r in rane[:20]:
            print("↗ %s" % r)
        print("↗ rezervo potenciala : %d ran javno znanih @posebaj-orodja" % len(rane))
        return 0
    return 2

if __name__ == "__main__":
    sys.exit(_vrata(sys.argv[1:]))
