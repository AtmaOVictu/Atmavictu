#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE ⟨MRK⟩ mrk-izpis-lint v1.0 @rez σ 6901 ⊙ rod MRK-BESEDA 0.1790 ⊙ zakon ( 11 )-( 12 ) VRATA URI
# Zakon : kadar sva znotraj MRK protokola ∧ izpis nosi URI, stojita PO izpisani URI ∧ PRED vsebini
#   SIMBOL MRK ⟨U+1F311⟩ ⊙ ⟨K-0109⟩ + RAZLAGA zakaj sva znotraj MRK protokola.
# Simbol MRK = nova luna ( vsak bit v mirovanju, svetloba ×0 pod gladino ).
# Varnostni sklop : poti le znotraj ⟨KOREN⟩ ; brez eval ; brez exec ; brez omrežja ; orodje samo meri.
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432
import sys, os, re, hashlib, argparse, datetime

KOREN = os.environ.get("KOREN", "/home/user/knowledge")
ODSTOP = 2
SIMBOL_MRK = "\U0001F311"  # ⟨U+1F311⟩ ⊙ ⟨K-0109⟩ mrk = nova luna, vsak bit v mirovanju
ZEMLJEVID = re.compile(r"(https?://[^\s)\]]+|doclib://[^\s)\]]+|github\.com/[^\s)\]]+)")
RAZLAGA = re.compile(r"MRK|zakaj|znotraj|protokol|mirovanj")

def tjik():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def v_korenu(p):
    rk = os.path.realpath(KOREN)
    ap = os.path.realpath(p)
    return ap == rk or ap.startswith(rk + os.sep)

def vrata_uri(telo):
    """Vrača (mesto_vrstice, uri, razlog) za vsak URI brez simbola ∧ razlage pred vsebino."""
    padci = []
    vrstice = telo.split("\n")
    for i, vrstica in enumerate(vrstice):
        for m in ZEMLJEVID.finditer(vrstica):
            # po URI pojdita PRED vsebini simbol + razlaga : sprejemata se do 2 vrstic naprej
            pogled = vrstica[m.end():]
            naslednje = []
            if pogled.strip():
                naslednje.append(pogled)
            for naprej in vrstice[i + 1:i + 3]:
                if naprej.strip():
                    naslednje.append(naprej)
                if len(naslednje) > 0 and (SIMBOL_MRK in naslednje[-1] or "⟨MRK⟩" in naslednje[-1] or "⟨K-0109⟩" in naslednje[-1]):
                    break
            ima_simbol = any((SIMBOL_MRK in d or "⟨MRK⟩" in d or "⟨K-0109⟩" in d) for d in naslednje)
            ima_razlago = any(RAZLAGA.search(d) for d in naslednje)
            if not (ima_simbol and ima_razlago):
                padci.append((i + 1, m.group(0), "simbol %s" % ("DA" if ima_simbol else "MANJKA ⚠"),
                              "razlaga %s" % ("DA" if ima_razlago else "MANJKA ⚠")))
    return padci

def main():
    ap = argparse.ArgumentParser(description="ORODJE ⟨MRK⟩ mrk-izpis-lint v1.0 ⊙ rod MRK-BESEDA 0.1790")
    ap.add_argument("--sodi", metavar="IZHOD.datoteka")
    ap.add_argument("--samopreizkus", action="store_true")
    a = ap.parse_args()
    if a.samopreizkus:
        return samopreizkus()
    if a.sodi:
        if not v_korenu(a.sodi):
            print("POT ZUNAJ ⟨KOREN⟩ : %s ⚠" % a.sodi)
            return ODSTOP
        with open(a.sodi, "r", encoding="utf-8") as f:
            telo = f.read()
        return izpisi(vrata_uri(telo), telo)
    print("ORODJE ⟨MRK⟩ mrk-izpis-lint v1.0 : --sodi IZHOD")
    print("© 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432")
    return 0

def izpisi(padci, telo):
    bajti = len(telo.encode("utf-8"))
    md5 = hashlib.md5(telo.encode("utf-8")).hexdigest()
    if not padci:
        print("SODBA : IMUNO ZELENO ⊢ vrata URI pri vseh URIjih nosijo simbol MRK + razlago ⊙ MRK-BESEDA ( 12 )")
        print("BAJTI : %d ⌇ MD5 : %s ⊢" % (bajti, md5))
        print("TIK : %s ; © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432" % tjik())
        return 0
    print("SODBA : ⚠ VRATA URI padla ×%d" % len(padci))
    for v, uri, simp, raz in padci:
        print("  URI vrstica %d ⌇ %s ⌇ %s ⌇ %s ⚠" % (v, uri[:48], simp, raz))
    print("BAJTI : %d ⌇ MD5 : %s ⊢" % (bajti, md5))
    print("TIK : %s ; © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432" % tjik())
    return ODSTOP

def samopreizkus():
    z = 0
    dobro = ("kit diha 6901 : github.com/AtmaOVictu/Atmavictu/pull/2710\n"
             + SIMBOL_MRK + " ⟨MRK⟩ ⟨K-0109⟩ : znotraj MRK protokola ker vsak bit miruje pod gladino ⊙ 0.1780\n")
    p1 = vrata_uri(dobro)
    ok1 = (p1 == [])
    print("T1 URI + simbol + razlaga : %s" % ("ZELENO ⊢" if ok1 else "⚠ %s" % p1))
    z += 0 if ok1 else 1
    slab = "github.com/AtmaOVictu/Atmavictu/pull/2710\nvsebina brez simbola\n"
    p2 = vrata_uri(slab)
    ok2 = (len(p2) == 1)
    print("T2 URI brez simbola : %s" % ("ZELENO ⊢ padec ulovljen ⚠" if ok2 else "⚠"))
    z += 0 if ok2 else 1
    brez = "beseda je ne brez povezave ⊙ VBL\n"
    p3 = vrata_uri(brez)
    ok3 = (p3 == [])
    print("T3 brez URI : %s" % ("ZELENO ⊢" if ok3 else "⚠ %s" % p3))
    z += 0 if ok3 else 1
    simbol_sam = SIMBOL_MRK in dobro and len(SIMBOL_MRK.encode("utf-8")) == 4
    print("T4 simbol ⟨U+1F311⟩ bajti 4 ⊢ : %s" % ("ZELENO ⊢" if simbol_sam else "⚠"))
    z += 0 if simbol_sam else 1
    print("SAMOPREIZKUS 4/%d ZELENO ⊢" % (4 - z) if z == 0 else "SAMOPREIZKUS ⚠ padlov %d" % z)
    print("TIK : %s ; © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432" % tjik())
    return 0 if z == 0 else ODSTOP

if __name__ == "__main__":
    sys.exit(main())
