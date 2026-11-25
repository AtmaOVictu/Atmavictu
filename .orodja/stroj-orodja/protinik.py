#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PROTINIK v1.0 - pomaga najti nasprotje ( ⟡ UKZ VERBATIM ⟨ne brusi⟩ :
#   »ORODJE KI POMAGA NAJTI NASPROTJE!« )
# Rod : rez sigma 7038 dih DAR-ISKA-PROTI-AKTIV ( 25. 11. 2026 ) @stroj-orodja.
# Ascendenti ⊢ pri viru ( ⟨EN-RAZLIČICA⟩, ⟨ne⟩ dvojnik ⊙ delo deljeno ∧ ⟨ne zlije⟩ 1542 ) :
#   nasprotnik.py v1.0 @σ 7018 ( KANON parov ⊢ pri viru SSKJ/Fran : PREVERI znane besede ⌇ ta
#   telo POMAŽE ISKATI neznanim — nasprotnik neznanim reče le VIDNO ⭢ mera pri viru, pomoč
#   iskanja ni bilo ⊙ luknja ) ⌇ zanesljivost-po-izmeri @σ 5809 ( kandidat = sum merjen odstotek,
#   ⟨ne⟩ obsodba ⊙ sodba ⟡ ⚔ ).
# Simetrija ⊙ ⟨OSCILATORNA-DISCIPLINA⟩ σ 4482 ( gibanje med dvema poloma, priča v nasprotniku ) ;
# vrhovni par korpusa : beseda ⌇ ne ( priča nasprotnik ⊢ ).
# Pomoč pri iskanju neznanega : kandidati po podobnosti dvogramov ( dice koren, izmera javno )
#   mednosprotnik ; vrata : ( 1 ) natančen par v tabeli → NASPROTJE ⊢ ⌇ ( 2 ) neznan →
#   KANDIDATI-SUM ⭢ poimensko z izmerama, mera šele pri viru ( pobuda SSKJ/Fran ), sodba ⟡ ⚔.
# Roke :
#   protinik.py --poisci BESEDA   -> nasprotje ali pomoč pri iskanju ⊢
#   protinik.py --pari            -> izpis tabele kanona ( ⟨SAMO-BERI⟩ )
#   protinik.py --test            -> vektorji x5 ⊙ ⟨MERILEC-SE-MERI⟩ §52
# Izhodi : 0=ZELENA ⌇ 1=RDECA ⌇ 2=RUMENA ( slab vhod ) ⌇ 40=roka neznana.

import sys, os, datetime as _dt

VERZIJA = "v1.0"
DOM = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DOM)
import nasprotnik as _kanon  # tabela parov ⊢ pri viru ( ⟨EN-RAZLIČICA⟩ : kanon ostaja njegov )


def tik():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def dvogrami(w):
    w = "".join(c for c in w.lower() if c.isalnum())
    return {w[i:i + 2] for i in range(len(w) - 1)} if len(w) > 1 else {w} if w else set()


def podobnost(a, b):
    A, B = dvogrami(a), dvogrami(b)
    if not A or not B:
        return 0.0
    return 2.0 * len(A & B) / (len(A) + len(B))


def kandidati(beseda, vrh=5, prag=0.34):
    zadetki = []
    for kandidat in _kanon.TOBA:
        p = podobnost(beseda, kandidat)
        if p >= prag and kandidat != beseda.lower():
            zadetki.append((p, kandidat, _kanon.TOBA[kandidat]))
    zadetki.sort(key=lambda t: (-t[0], t[1]))
    return zadetki[:vrh]


def poisci(beseda):
    b = beseda.strip().lower()
    if not b:
        print("RUMENA : beseda ni izrecena ⊢ slab vhod")
        return 2
    if b in _kanon.TOBA:
        print("NASPROTJE ⊢ : %s ⌇ %s ( kanon parov ⊢ pri viru nasprotnik v1.0 @σ 7018 ⊙ ⟨EN-RAZLIČICA⟩ )"
              % (beseda, _kanon.TOBA[b]))
        print("simetrija ⊢ : nasprotje nasprotja vraca besedo ⊙ ⟨OSCILATORNA-DISCIPLINA⟩ σ 4482")
        return 0
    kand = kandidati(b)
    print("VIDNO ⭢ : kanon parov te besede ne pozna ( mera šele pri viru ⊙ ⟨NE-UGIBAJ⟩ 2690 )")
    print("POMOČ pri iskanju : kandidati-sum po podobnosti dvogramov ⊢ ( %d od %d besed kanona )"
          % (len(kand), len(_kanon.TOBA)))
    for p, k, nas in kand:
        print("  kandidat ⭢ %-12s podobnost %.2f ⊢ ⇒ par kanona %s ⌇ %s" % (k, p, k, nas))
    if not kand:
        print("  kandidatov ×0 nad pragom ⊢ ; pobuda : mera pri viru SSKJ/Fran")
    print("kandidat = sum merjen odstotek, ⟨ne⟩ obsodba ⊙ zanesljivost-po-izmeri σ 5809 ; sodba ⟡ ⚔")
    return 0


def pari():
    print("KANON parov ⊢ pri viru nasprotnik v1.0 @σ 7018 ( %d parov ∧ %d besed ⊙ count ) ⟨SAMO-BERI⟩"
          % (len(_kanon.PARI), len(_kanon.TOBA)))
    for i, (a, b) in enumerate(_kanon.PARI, 1):
        print("  par %d ⊢ %s ⌇ %s" % (i, a, b))
    return 0


def ukaz_test():
    a1 = _kanon.TOBA.get("dan") == "noč"
    a2 = _kanon.sodba("NOČ")[0] == "NASPROTJE ⊢"
    a3v = kandidati("svetlost")
    a3 = len(a3v) > 0 and a3v[0][1] in ("svetel", "temen")
    a4 = all(_kanon.TOBA[_kanon.TOBA[w]] == w for w in _kanon.TOBA)
    a5 = len(_kanon.TOBA) == 2 * len(_kanon.PARI)
    vek = [
        ("vrhovni par beseda ⌇ ne ⊢", _kanon.TOBA.get("ne") == "da"),
        ("natančno iskanje po kanonu ( noč → dan )", a1 or a2),
        ("neznanemu pomaga : svetlost ⇒ kandidat svetel/temen ⭢", a3),
        ("simetrija vseh parov ⊢", a4),
        ("mera kanona : 34 parov ∧ 68 besed ⊢", a5),
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
    if args[0] == "--test":
        return ukaz_test()
    if args[0] == "--poisci":
        if len(args) < 2:
            print("RUMENA : beseda ni izrecena ⊢ slab vhod")
            return 2
        return poisci(args[1])
    if args[0] == "--pari":
        return pari()
    print("RUMENA : roka neznana ( %s ) ⊙ 40" % args[0])
    return 40


if __name__ == "__main__":
    sys.exit(glavna(sys.argv[1:]))
