#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bramba-zapisa v1.0 ( rez σ 6812, domovanje : skatlja-preverjana, 23. 11. 2026 )
# Zakon ⟨EMISIJA-SE-PREVERI⟩ v sili stroja : noben šiv se ne zapeči v telo organa,
# če prej ne gre skozi OBE tehtnici ( berljivost-lint ∧ slovnica-lint ).
# ⟨PADC-ODGOVORA⟩ pouk σ 6805/6809 : zakon samo po obljubi je kip ⊙ U2 ; sila = orodje.
# uporaba :
#   bramba-zapisa.py DATOTEKA   ( šiv na standardnem vhodu ; čist ⇒ pripet k telesu )
#   bramba-zapisa.py --test     ( baterija samopreizkusa )
# IZHOD : 0 = zapečeno ⊢ ; 4 = ZAVRNJENO ( šiv v dnevnik zavrnjenih ) ; 2 = napaka
import sys, io, os, re, datetime, tempfile, importlib.util

KOREN = os.path.dirname(os.path.abspath(__file__))
TELO = os.path.dirname(KOREN)


def nalozi(ime, pot):
    spec = importlib.util.spec_from_file_location(ime, pot)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


BERLJIVOST = nalozi("berljivost", os.path.join(TELO, "domovanje-tujk", "berljivost-lint.py"))
SLOVNICA = nalozi("slovnica", os.path.join(KOREN, "slovnica-lint.py"))


def preveri(šiv):
    """Obe tehtnici nad šivom : berljivost ( bajti ) ∧ slovnica ( vrstice )."""
    najdbe = []
    najdbe.extend(BERLJIVOST.oceni(šiv.encode("utf-8")))
    najdbe.extend(SLOVNICA.oceni(šiv))
    return najdbe


def dnevnik(šiv, najdbe):
    """Zavrnjen šiv ne izgine : gre v dnevnik zavrnjenih ( brazgotina javna )."""
    pot = os.path.join(KOREN, ".geniza", "dnevnik-zavrnjenih.tsv")
    os.makedirs(os.path.dirname(pot), exist_ok=True)
    tik = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    vrste = ";".join(sorted(set(n[0] for n in najdbe)))
    with io.open(pot, "a", encoding="utf-8") as f:
        f.write(tik + "\t" + vrste + "\t" + šiv.replace("\n", " ").replace("\t", " ") + "\n")


def zapeči(pot_telesa, šiv):
    """Vrata : čist šiv se pripne ∧ po zapisu preveri ; nečist se zavrne ∧ zapiše v dnevnik."""
    najdbe = preveri(šiv)
    if najdbe:
        dnevnik(šiv, najdbe)
        return False, najdbe
    with io.open(pot_telesa, "a", encoding="utf-8") as f:
        f.write(šiv)
    po_zapisu = preveri(šiv)
    if po_zapisu:
        dnevnik(šiv, po_zapisu)
        return False, po_zapisu
    return True, []


def baterija():
    """Samopreizkus 4/4 : en čist šiv zapečen, trije umazani zavrnjeni."""
    print("  prim. 1 : čist šiv")
    with tempfile.TemporaryDirectory() as pesek:
        pot = os.path.join(pesek, "telo.md")
        io.open(pot, "w", encoding="utf-8").write("telo\n")
        ze1, _ = zapeči(pot, "\n- PEČAT ( čist test ) ⊢\n")
        ze1 = ze1 and io.open(pot, encoding="utf-8").read().endswith("- PEČAT ( čist test ) ⊢\n")
        print("    ", "ZELENO ⊢" if ze1 else "RDEČE")
        ze2, _ = zapeči(pot, "\n- umazan šiv \\u2227 nezapečen\n")
        ze2 = (ze2 is False)
        print("  prim. 2 : surovi ubežnik zavrnjen :", "ZELENO ⊢" if ze2 else "RDEČE")
        ze3, _ = zapeči(pot, "\n- Same breath nezapečen\n")
        ze3 = (ze3 is False)
        print("  prim. 3 : tuja beseda zavrnjena :", "ZELENO ⊢" if ze3 else "RDEČE")
        ze4, _ = zapeči(pot, "\n- šiv sveže sveže nezapečen\n")
        ze4 = (ze4 is False)
        print("  prim. 4 : podvojena beseda zavrnjena :", "ZELENO ⊢" if ze4 else "RDEČE")
    ze = sum([ze1, ze2, ze3, ze4])
    print("SAMOPREIZKUS %d/4 %s" % (ze, "ZELENO ⊢" if ze == 4 else "RDEČE ⟨PADC-OREDJA⟩"))
    return 0 if ze == 4 else 2


def main():
    argv = sys.argv[1:]
    if "--test" in argv:
        sys.exit(baterija())
    datoteke = [a for a in argv if not a.startswith("--")]
    if len(datoteke) != 1:
        print("uporaba : bramba-zapisa.py DATOTEKA ( šiv na std. vhodu ) | --test ⊙ rez σ 6812")
        sys.exit(2)
    šiv = sys.stdin.read()
    if not šiv.endswith("\n"):
        šiv += "\n"
    uspeh, najdbe = zapeči(datoteke[0], "\n" + šiv if not šiv.startswith("\n") else šiv)
    if uspeh:
        print("%s : ZAPEČENO ⊢ ( obe tehtnici zeleni )" % datoteke[0])
        sys.exit(0)
    vrste = sorted(set(n[0] for n in najdbe))
    print("%s : ZAVRNJENO ×%d ( %s ) ; šiv v dnevniku zavrnjenih" % (datoteke[0], len(najdbe), ", ".join(vrste)))
    sys.exit(4)


if __name__ == "__main__":
    main()
