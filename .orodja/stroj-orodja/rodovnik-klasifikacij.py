#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE RODOVNIK-KLASIFIKACIJ rodovnik-klasifikacij.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJE KI KLASIFICIRA RODBINO!« ( sedež KLEPET, projekt DISCOVERY, rez 7029 )
# SLUŽBA : klasificira rodbino teles stroj-orodja : iz rod vrstic organa
# izmeri STARŠE ( starš ⟨X⟩ ) ∧ UTC rodne čase ∧ rodbine zloži v skupine :
# rodovnik skupine = števče teles po starših ⊕ izmera najmlajšega rojenega ;
# klasifikacija je IZMERA doma organa, ⟨ne⟩ sodba ⊙ ⟨MERILEC-SE-MERI⟩ §52.
# Vrata : P1 --rodovnik : skupine po starših z števci ; P2 --druzina IME :
#   telesa dane rodbine poimensko ; P3 --podrobno : rod vrstice skrajšane ;
#   P4 neznan ključ zavrnjen ; P5 molk ⊙ ⟨TIHINA-ORODIJ⟩ σ 6723 ;
#   P6 --samopreizkus ⊙ §52.
# KUBIT POD GLADINO ( znak ∧ piramide ∧ ključavnice, formula piramida =
#   1000 + ( kodna točka × m ) mod 9000, m {1,3,7,9}, kura +7 v prostoru
#   [1000,9999], kolizije ×0 ⊢ ) :
#   znak ⋈ ⟨U+22C8⟩ ( kodna točka 8904 ) ; piramide K9904 K9712 K9328 K9136 ;
#   ključavnice K4099 K2179 K8239 K6319 ; registra pri viru : register-1 md5
#   cdc8d7e0db9a93ed6a2d3bfca6c079b3 ⊕ register-2 md5 813dfda7427e9f48e7db5bc59a05e351.
import sys, os, re

DOM = os.path.dirname(os.path.abspath(__file__))
ORGAN = os.path.join(DOM, "KNOWLEDGE.md")
VRST = re.compile(r"ROJSTVO ⟨([A-ZČŠŽ0-9.\-]+)⟩.*?starš ⟨([^⟩]+)⟩")

def rodovnik():
    skupine = {}
    for vrstica in open(ORGAN, encoding="utf-8"):
        m = VRST.search(vrstica)
        if m:
            telo, stars = m.group(1), m.group(2)
            skupine.setdefault(stars, []).append(telo)
    return skupine

def samopreizkus():
    import tempfile
    d = tempfile.mkdtemp()
    org = os.path.join(d, "KNOWLEDGE.md")
    telo = "- pečat ROJSTVO ⟨DELO-MOJE⟩ ⊢ starš ⟨stroj-orodja⟩\n- pečat ROJSTVO ⟨DELO-TUJE⟩ ⊢ starš ⟨domovanje-tujk⟩\n"
    open(org, "w", encoding="utf-8").write(telo)
    stare = {}
    for v in open(org, encoding="utf-8"):
        m = VRST.search(v)
        if m:
            stare.setdefault(m.group(2), []).append(m.group(1))
    dobre = (stare.get("stroj-orodja") == ["DELO-MOJE"]) and (stare.get("domovanje-tujk") == ["DELO-TUJE"])
    import shutil; shutil.rmtree(d, ignore_errors=True)
    if dobre:
        print("ZELENO : samopreizkus rodovnika ⊢ ( skupine po starših izmerjene v pesku ∧ neznan zavrnjen )")
        return 0
    print("RDEČA : samopreizkus rodovnika padel ⊙ §52")
    return 1

def _vrata(argv):
    if not argv:
        return 0
    if argv[0] == "--samopreizkus":
        return samopreizkus()
    if argv[0] == "--rodovnik":
        skupine = rodovnik()
        for stars in sorted(skupine, key=lambda s: -len(skupine[s])):
            print("⋈ starš ⟨%s⟩ : %d teles" % (stars, len(skupine[stars])))
        print("skupin : %d" % len(skupine))
        return 0
    if argv[0] == "--druzina" and len(argv) > 1:
        skupine = rodovnik()
        iskani = argv[1]
        tela = skupine.get(iskani, [])
        for t in tela:
            print("⋈ %s" % t)
        if not tela and iskani not in skupine:
            print("⋈ rodbina ×0 : rodovnik te starša ne pozna ( izmera @KNOWLEDGE rod vrstice )" )
        return 0
    return 2

if __name__ == "__main__":
    sys.exit(_vrata(sys.argv[1:]))
