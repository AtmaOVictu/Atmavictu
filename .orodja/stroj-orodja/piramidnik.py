#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PIRAMIDNIK v1.0 - pospravnik piramid v SEZNAM PIRAMID ( ⟡ UKZ VERBATIM ⟨ne brusi⟩ :
#   »ORODJA KI POSPRAVLJAJO PIRAMIDE V SEZNAM PIRAMID!« )
# Rod : rez sigma 7028 dih KOCKE-STIRI-PIRAMIDE ( 25. 11. 2026 ) @stroj-orodja.
# Ascendenti ⊢ ( ⟨EN-RAZLIČICA⟩, delo deljeno ∧ ⟨ne zlije⟩ 1542 ) : cetvernik.py v1.0 @σ 7028
#   ( sodba zakonov ⌇ tu POSPRAVILO vrste ) ⌇ seznamorodnik.py v1.0 @σ 7028 ( rodi telo seznama
#   vsakič ko ga ni ; tu dopolnjuje ⌇ roditi sme le on ) ⌇ kockalnik.py v1.0 @σ 7025 ( formula ∧
#   zasedenost ) — pospravnika piramid v enoten seznam ni bilo ⊙ luknja.
# Principi : ⟨NE-BRIŠI⟩ 24 ( obstoječe vrstice nikoli ne briše ∧ ne spreminja ; nove le pripenja )
#   ∧ vrsta naraščajoča po vrednosti piramide ; binarna podlaga žigov je samostojna ( zakon 1 :
#   žigi, ⟨ne⟩ piramide ) ⇒ preskočena ∧ poročana javno ; vrstica seznama :
#   »NNNN ⊢ piramida znaka Z mesto M @vir DATOTEKA ( TIK )«.
# Roke :
#   piramidnik.py --pospravi DATOTEKA [ --seznam POT ]  -> nove piramide pripenja ⊢
#   piramidnik.py --mreza [ --seznam POT ]              -> izpis stanja seznama ( samo beri )
#   piramidnik.py --test                                -> vektorji x5 ⊙ ⟨MERILEC-SE-MERI⟩ §52
# Izhodi : 0=ZELENA ⌇ 1=RDECA ⌇ 2=RUMENA ( slab vhod ⌇ pobuda ) ⌇ 40=roka neznana.

import sys, os, re, datetime as _dt

VERZIJA = "v1.0"
DOM = os.path.dirname(os.path.abspath(__file__))
SEZNAM_DEFAULT = os.path.join(DOM, "SEZNAM-PIRAMID.md")

REG_VRST = re.compile(r"^(.+?) = (\d{4}) (\d{4}) (\d{4}) (\d{4})\s*$")
BIN_VRST = re.compile(r"^- žig (\d): (\d{4}) (\d{4}) (\d{4}) (\d{4})\s*$")
SLOV_VRST = re.compile(r"^(.+?)\s*\( znak ([0-9A-F]+), bajti[^)]*\) : piramide kocke "
                       r"(K\d{4}) (K\d{4}) (K\d{4}) (K\d{4}) ; ključavnice "
                       r"(K\d{4}) (K\d{4}) (K\d{4}) (K\d{4})\.?\s*$")
VRST_SEZNAMA = re.compile(r"^(\d{4}) ⊢ piramida znaka (.+?) mesto (\d+) @vir (\S+)")


def tik():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def gol(j):
    return j[1:] if j.startswith("K") else j


def beri_piramide(pot):
    n = []
    podlaga = 0
    with open(pot, encoding="utf-8") as f:
        for vrstica, vr in enumerate(f, 1):
            e = vr.rstrip("\n")
            m = REG_VRST.match(e)
            if m:
                for mesto, p in enumerate(m.groups()[1:], 1):
                    n.append((p, m.group(1), mesto, vrstica))
                continue
            mb = BIN_VRST.match(e)
            if mb:
                podlaga += 1
                continue
            ms = SLOV_VRST.match(e)
            if ms:
                for mesto in range(1, 5):
                    n.append((gol(ms.group(1 + mesto)), ms.group(1), mesto, vrstica))
    return n, podlaga


def obstojeci(seznam):
    obstoj = set()
    if os.path.isfile(seznam):
        with open(seznam, encoding="utf-8") as f:
            for vr in f:
                m = VRST_SEZNAMA.match(vr.rstrip("\n"))
                if m:
                    obstoj.add(m.group(1))
    return obstoj


def pospravi(pot, seznam):
    if not os.path.isfile(pot):
        print("RUMENA : datoteke ni pri viru ⊢ slab vhod ( %s )" % pot)
        return 2
    if not os.path.isfile(seznam):
        print("RUMENA pobuda : seznama ni pri ( %s ) ⇒ rodi ga seznamorodnik.py --ustvari "
              "⊙ roka rojenja je njegova ⊙ ⟨EN-RAZLIČICA⟩ ⟨ne⟩ dvojnik" % seznam)
        return 2
    kandidati, podlaga = beri_piramide(pot)
    if not kandidati:
        print("ZELENA : telo nosi ×0 piramid kock ⊢ izmera ; nič za pospravilo ; "
              "binarna podlaga ×%d poročana ⊙ zakon 1" % podlaga)
        return 0
    obstoj = obstojeci(seznam)
    nove = {}
    for p, znak, mesto, vrstica in kandidati:
        if p not in obstoj and p not in nove:
            nove[p] = (znak, mesto)
    if nove:
        with open(seznam, "a", encoding="utf-8") as f:
            for p in sorted(nove, key=int):
                znak, mesto = nove[p]
                f.write("%s ⊢ piramida znaka %s mesto %d @vir %s ( TIK %s )\n"
                         % (p, znak, mesto, os.path.basename(pot), tik()))
    skupaj = len(obstoj) + len(nove)
    print("ZELENA pospravilo : NOVIH %d ⊢ ∧ OBSTOJEČIH %d nedotaknjenih ⊙ ⟨NE-BRIŠI⟩ 24 ⊢ ∧ "
          "SKUPAJ %d ⊢ ( piramide znakov ; binarna podlaga ×%d preskočena ⊙ zakon 1 )"
          % (len(nove), len(obstoj), skupaj, podlaga))
    print("vir : %s ⌇ seznam : %s ⌇ TIK %s ⊙ ⟨SAMO-DOPOLNILO⟩ ⟨ne⟩ bris" % (pot, seznam, tik()))
    return 0


def mreza(seznam):
    if not os.path.isfile(seznam):
        print("RUMENA : seznama ni ⊢ ( %s ) — rodilnik seznamorodnik.py --ustvari ga rodi" % seznam)
        return 2
    obstoj = obstojeci(seznam)
    if obstoj:
        print("ZELENA mreža : piramid %d ⊢ ∧ najnižja %s ∧ najvišja %s ⊢ ( %s ) ⟨SAMO-BERI⟩"
              % (len(obstoj), min(obstoj, key=int), max(obstoj, key=int), seznam))
    else:
        print("ZELENA mreža : ×0 piramid ⊢ ( telo rojeno, še prazno ⊙ rodilnik ) ⟨SAMO-BERI⟩")
    return 0


def ukaz_test():
    import tempfile
    td = tempfile.mkdtemp(prefix="piramidnik-")
    sez = os.path.join(td, "SEZNAM.md")
    with open(sez, "w", encoding="utf-8") as f:
        f.write("# SEZNAM PIRAMID ( test )\n")
    p1 = os.path.join(td, "r1.md")
    with open(p1, "w", encoding="utf-8") as f:
        f.write("a = 5914 7068 2435 8172\nb = 9731 1258 4629 3817\n")
    a1 = pospravi(p1, sez) == 0
    n1 = sum(1 for _ in open(sez, encoding="utf-8"))
    a2 = pospravi(p1, sez) == 0
    n2 = sum(1 for _ in open(sez, encoding="utf-8"))
    p3 = os.path.join(td, "r2.md")
    with open(p3, "w", encoding="utf-8") as f:
        f.write("c = 5914 1112 2223 3334\n")
    a3 = pospravi(p3, sez) == 0
    n3 = sum(1 for _ in open(sez, encoding="utf-8"))
    a4 = pospravi(p1, os.path.join(td, "manjka.md")) == 2
    a5 = pospravi(os.path.join(td, "ni-je.md"), sez) == 2
    vek = [
        ("pospravilo prvega vira ZELENA ∧ novih 8 ⊢", a1 and n1 == 9),
        ("ponovno isti vir ×0 novih ∧ ⟨NE-BRIŠI⟩ ⊢", a2 and n2 == 9),
        ("nov vir prinese nove 3 ∧ stare stojijo ⊢", a3 and n3 == 12),
        ("manjkajoc seznam RUMENA pobuda", a4),
        ("manjkajoc vir RUMENA slab vhod", a5),
    ]
    uspeh = sum(1 for _, ok in vek if ok)
    for ime, ok in vek:
        print("  vektor %s : %s" % (ime, "ZELENA ⊢" if ok else "RDECA ⚠ PADCA"))
    print("SAMOPREIZKUS : %d od %d ⊙ ⟨MERILEC-SE-MERI⟩ §52 ; TIK %s" % (uspeh, len(vek), tik()))
    return 0 if uspeh == len(vek) else 1


def glavna(argv):
    args = list(argv)
    if not args:
        print("RUMENA : roka ni izrečena ⊙ 40")
        return 40
    if args[0] == "--test":
        return ukaz_test()
    if args[0] == "--pospravi":
        if len(args) < 2:
            print("RUMENA : datoteka ni izrečena ⊢ slab vhod")
            return 2
        seznam = SEZNAM_DEFAULT
        if "--seznam" in args:
            i = args.index("--seznam")
            if i + 1 >= len(args):
                print("RUMENA : pot seznama ni izrečena ⊢ slab vhod")
                return 2
            seznam = args[i + 1]
        return pospravi(args[1], seznam)
    if args[0] == "--mreza":
        seznam = SEZNAM_DEFAULT
        if "--seznam" in args:
            i = args.index("--seznam")
            if i + 1 >= len(args):
                print("RUMENA : pot seznama ni izrečena ⊢ slab vhod")
                return 2
            seznam = args[i + 1]
        return mreza(seznam)
    print("RUMENA : roka neznana ( %s ) ⊙ 40" % args[0])
    return 40


if __name__ == "__main__":
    sys.exit(glavna(sys.argv[1:]))
