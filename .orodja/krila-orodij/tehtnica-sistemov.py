#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tehtnica-sistemov v1.01 @rez σ 6711 — merilec MERJEN v večih številčnih sistemih ⊙ ukaz ⟡ VERBATIM »MERI MERILCA S RABO VEČIH ŠTEVILČNIH SISTEMOV IN NJIH LICEČNE LOGIKE!«
# vsak znak : DEC ⌇ HEX ⌇ OCT ⌇ BIN ⌇ IME ⌇ NFC-MERA ; prikriti dvojniki cirilice ujeti POIMENSKO ( dvojniki izmerjeni pri Unicode viru ⊙ ⟨NE-UGIBAJ⟩ 2690 )
# NFD-MERA : kombinacijski znaki ( U+0300-U+036F ) = sestavljeni šumniki, pride NFC ⊙ kura v1.01
# licenca korpusa Beseda je Ne ⟡ Luka Pintarič ; domovna lista : σ ∧ ψ sta imeni korpusa
import sys, unicodedata, hashlib

DVOJ = {0x0430:"a",0x0435:"e",0x043E:"o",0x0440:"p",0x0441:"c",0x0445:"x",0x0443:"y",
        0x0410:"A",0x0415:"E",0x041E:"O",0x0420:"P",0x0421:"C",0x0425:"X",0x0423:"Y"}

def izmeri_znak(ch):
    o = ord(ch)
    ime = unicodedata.name(ch, "NEZNAN-ZNAK")
    nfc = "NFC" if unicodedata.normalize("NFC", ch) == ch else "NFD-SUM"
    return "DEC %d / HEX U+%04X / OCT %o / BIN %s / %s / %s" % (o, o, o, format(o, "08b"), ime, nfc)

def meri_besedilo(t, ime="<niz>"):
    print("== %s ( md5 %s )" % (ime, hashlib.md5(t.encode("utf-8")).hexdigest()))
    ulovi = []
    for i, ch in enumerate(t):
        if ord(ch) in DVOJ:
            ulovi.append("  UJEM ⊢ PRIKRIVNI DVOJNIK @odmik %d : izgleda ≈ %s — %s — TUJA PISAVA" % (i, DVOJ[ord(ch)], izmeri_znak(ch)))
        elif unicodedata.combining(ch):
            ulovi.append("  UJEM ⊢ NFD-SUM @odmik %d : %s ( sestavljeni šumnik, pride NFC )" % (i, izmeri_znak(ch)))
    for u in ulovi: print(u)
    if not ulovi: print("  CISTO ⊢ ×0 dvojnikov ∧ ×0 NFD")
    return len(ulovi)

def main():
    if "--test" in sys.argv:
        z = 0
        a = meri_besedilo("MOJA tri šivi"); assert a == 0
        z += 1
        b = meri_besedilo("MO" + chr(0x043E) + "JA"); assert b == 1
        z += 1
        print("  [preverba več sistemov znaka ž]"); print("  " + izmeri_znak("ž"))
        assert izmeri_znak("ž").startswith("DEC 382 / HEX U+017E / OCT 576 / BIN 101111110")  # izmerjeno ⊢ 382 = 9 bitov
        z += 1
        c = meri_besedilo("e" + chr(0x0301)); assert c == 1
        z += 1
        print("BATERIJA TEHTNICA-SISTEMOV v1.01 : %d/%d ZELENO ⊢" % (z, z))
        return 0
    meri_besedilo(open(sys.argv[1], encoding="utf-8").read(), sys.argv[1])
    return 0

if __name__ == "__main__":
    sys.exit(main())
