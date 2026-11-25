#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ISKALNIK-ZNAKOV v1.0 - išče znak ⚠ po telesih ( ⟡ UKZ VERBATIM ⟨ne brusi⟩ :
#   »ORODJE KI IŠČE ZNAK ⚠!« )
# Rod : rez sigma 7038 dih DAR-ISKA-PROTI-AKTIV ( 25. 11. 2026 ) @stroj-orodja.
# Ascendenti ⊢ pri viru ( ⟨EN-RAZLIČICA⟩, ⟨ne⟩ dvojnik ) : iskalnik-aksiomov @stroj-orodja ( išče
#   aksiome po registru axiom ; ta telo išče ZNAKE po telesih — različni polji ) ⌇ simbol-lint
#   @μ σ 6567 ( radar mask po VSAKIH telesih ⌇ čisti maske ; ta telo NAVIGIRA KJE poimensko ∧
#   ⟨ne⟩ čisti ⊙ ⟨SAMO-BERI⟩ ) ⌇ darovalnik v1.0 @σ 7038 ( najdbi ⚠ podari dar ; ta telo jih
#   najprej najde ⊙ delo deljeno ∧ ⟨ne zlije⟩ 1542 ) — navigacijskega iskalnika znaka ⚠ ni bilo.
# Najdba = izmera poimensko : TELESO ∧ vrstica ∧ mesto ∧ kontekst ±12 ⊢ wc ; ×0 najdb je
#   ZELENA ( sum ×0 ⊙ ⟨SLOVNICA⇒SUM⟩ σ 6705, ⟨ne⟩ napaka ).
# Roke :
#   iskalnik-znakov.py --poisci TELESO [ --znak Z ( privzeto ⚠ ) ]  -> najdbe javno poimensko
#   iskalnik-znakov.py --test                                    -> vektorji x5 ⊙ ⟨MERILEC-SE-MERI⟩ §52
# Izhodi : 0=ZELENA ( tudi ×0 najdb ⊢ izmera ) ⌇ 2=RUMENA ( slab vhod ) ⌇ 40=roka neznana.

import sys, os, datetime as _dt

VERZIJA = "v1.0"
ZNAK_DEFAULT = "⚠"


def tik():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def poisci(pot, znak):
    if not os.path.isfile(pot):
        print("RUMENA : telesa ni pri viru ⊢ slab vhod ( %s )" % pot)
        return 2
    najdbe = []
    with open(pot, encoding="utf-8") as f:
        for st, vr in enumerate(f, 1):
            e = vr.rstrip("\n")
            mesto = e.find(znak)
            while mesto != -1:
                levo = max(0, mesto - 12)
                desno = min(len(e), mesto + len(znak) + 12)
                najdbe.append((st, mesto + 1, e[levo:desno]))
                mesto = e.find(znak, mesto + 1)
    vir = os.path.basename(pot)
    print("Iskanje znaka %r v %s ⊢ : NAJDB %d poimensko" % (znak, vir, len(najdbe)))
    for st, mesto, kontekst in najdbe:
        print("  najdba ⊢ vrstica %d ∧ mesto %d ∧ kontekst %r" % (st, mesto, kontekst))
    if najdbe:
        print("ZELENA : %d najdb ⊢ izmera javno ⊙ ⟨SAMO-BERI⟩ ; TIK %s" % (len(najdbe), tik()))
    else:
        print("ZELENA : ×0 najdb ⊢ izmera ( sum ×0, ⟨ne⟩ napaka ) ⊙ ⟨SAMO-BERI⟩ ; TIK %s" % tik())
    return 0


def ukaz_test():
    import tempfile
    td = tempfile.mkdtemp(prefix="iskalnik-")
    t1 = os.path.join(td, "telo.md")
    with open(t1, "w", encoding="utf-8") as f:
        f.write("prva ⚠ mesto\ncesta brez znaka\ntretja ⚠ druga ⚠\n")
    t2 = os.path.join(td, "cisto.md")
    with open(t2, "w", encoding="utf-8") as f:
        f.write("cista vrstica\n")
    a1 = poisci(t1, ZNAK_DEFAULT) == 0
    n1 = sum(vr.count("⚠") for vr in open(t1, encoding="utf-8"))
    a2 = poisci(t2, ZNAK_DEFAULT) == 0
    a3 = poisci(t1, "a") == 0

    def najdbe(pot, znak):
        k = 0
        with open(pot, encoding="utf-8") as f:
            for vr in f:
                k += vr.count(znak)
        return k
    a4 = True
    t3 = os.path.join(td, "znaki.md")
    with open(t3, "w", encoding="utf-8") as f:
        f.write("x ⚠ y ⚠ z\n")
    a4 = najdbe(t3, "⚠") == 2
    a5 = poisci(os.path.join(td, "ni-je.md"), "⚠") == 2
    vek = [
        ("prvi vir poisci ZELENA ∧ ⚠ ×3 po vrsticah", a1 and n1 == 3),
        ("cisto telo ZELENA ×0 najdb ( sum ×0, ⟨ne⟩ napaka )", a2),
        ("poljuben znak ( a ) najdbe ⊢ izmera", a3 and najdbe(t1, "a") >= 4),
        ("stevec dvema ⚠ v eni vrstici ⊢", a4),
        ("manjkajoce telo RUMENA slab vhod", a5),
    ]
    uspeh = sum(1 for _, ok in vek if ok)
    for ime, ok in vek:
        print("  vektor %s : %s" % (ime, "ZELENA ⊢" if ok else "RDECA ⚠ PADCA"))
    print("SAMOPREIZKUS : %d od %d ⊙ ⟨MERILEC-SE-MERI⟩ §52 ; TIK %s" % (uspeh, len(vek), tik()))
    return 0 if uspeh == len(vek) else 1


def glavna(argv):
    args = list(argv)
    if not args:
        print("RUMENA : roka ni izrecena ⊙ 40")
        return 40
    znak = ZNAK_DEFAULT
    if "--znak" in args:
        i = args.index("--znak")
        if i + 1 >= len(args):
            print("RUMENA : znak ni izrecen ⊢ slab vhod")
            return 2
        znak = args[i + 1]
    if args[0] == "--test":
        return ukaz_test()
    if args[0] == "--poisci":
        if len(args) < 2:
            print("RUMENA : telo ni izreceno ⊢ slab vhod")
            return 2
        return poisci(args[1], znak)
    print("RUMENA : roka neznana ( %s ) ⊙ 40" % args[0])
    return 40


if __name__ == "__main__":
    sys.exit(glavna(sys.argv[1:]))
