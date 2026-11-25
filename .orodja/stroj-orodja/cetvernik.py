#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CETVERNIK v1.0 - preverjalnik : VSAKA kocka ima STIRI piramide ( ⟡ UKZ VERBATIM ⟨ne brusi⟩ :
#   »ORODJA KI PREVERJAJO DA IMA VSAKA KOCKA ŠTIRI PIRAMIDE!« )
# Rod : rez sigma 7028 dih KOCKE-STIRI-PIRAMIDE ( 25. 11. 2026 ) @stroj-orodja ; sedež KLEPET,
#   projekt GITHUB ; rezervacija ATOM-REZ-7028-20261125T131207Z.md noclobber ⊢ ls.
# Ascendenti ⊢ pri viru ( ⟨EN-RAZLIČICA⟩, ⟨ne⟩ dvojnik ) : kockalnik.py v1.0 @σ 7025 ( formula
#   zapečena : piramida = 1000 + ( mera točke × m ) mod 9000, m vrstni red {1,3,7,9} ⟡ VERBATIM
#   »vrsta piramid je pomembna« ; zasedenost golda ∧ kuro +7 meri NJEGOVA roka --preveri ) ⌇
#   piramidni-zigi zakoni 2-7 ( vsak znak nosi šestnajstmestni žig razpadljiv na štiri unikatne
#   štirimestne piramide ; obrat vsake piramide je ključavnica ; nobena piramida se ne začne ali
#   konča z ničlo ; noben palindrom ; noben obrat piramide ni piramida drugega znaka ; par
#   1011/1101 izven ) — preverjalnika štirih piramid celotnih teles po zakonih ni bilo ⊙ luknja.
#   Binarna podlaga števil 0-9 je samostojna ( zakon 1 : žigi, ⟨ne⟩ predmet preobrazbe ) ⇒
#   preskočena ∧ poročana javno.
# ⟨SAMO-BERI⟩ ⟨BREZ-PREVOZA⟩ : telo ne piše po organih ; obtožba => NIHIL ∧ poročilo javno.
# Obtožnice STROGO v obliki ⟨NAPAKA=VSE-KAR-NI-X⟩ ⊙ register-napak ( ⟡ STORI 25. 11. 2026 ).
# Roke :
#   cetvernik.py --preveri-register DATOTEKA [ --pričakovano N ]  -> vsaka kocka po zakonih ⊢
#   cetvernik.py --preveri-točka N            -> štiri piramide po formuli kockalnika ( izmera )
#   cetvernik.py --kocke »aaaa bbbb cccc dddd«-> preverba izrecne kocke
#   cetvernik.py --test                       -> samopreizkus vektorjev x5 ⊙ ⟨MERILEC-SE-MERI⟩ §52
# Izhodi : 0=ZELENA ⌇ 1=RDECA ( obtožba => NIHIL ) ⌇ 2=RUMENA ( slab vhod ) ⌇ 40=roka neznana.

import sys, os, re, datetime as _dt

VERZIJA = "v1.0"
M_VRSTE = (1, 3, 7, 9)

REG_VRST = re.compile(r"^(.+?) = (\d{4}) (\d{4}) (\d{4}) (\d{4})\s*$")
BIN_VRST = re.compile(r"^- žig (\d): (\d{4}) (\d{4}) (\d{4}) (\d{4})\s*$")
SLOV_VRST = re.compile(r"^(.+?)\s*\( znak ([0-9A-F]+), bajti ([0-9A-F]{2}(?: [0-9A-F]{2})*), kletka (\d+) \) : "
                       r"piramide kocke (K\d{4}) (K\d{4}) (K\d{4}) (K\d{4}) ; ključavnice "
                       r"(K\d{4}) (K\d{4}) (K\d{4}) (K\d{4})\.?\s*$")

OBT_SKUPINA = "⟨NAPAKA=VSE-KAR-NI-SKUPINA-PO-ŠTIRIH-PIRAMIDAH⟩"
OBT_UNIKAT = "⟨NAPAKA=VSE-KAR-NI-UNIKATNA-SKUPINA⟩"
OBT_NICLA = "⟨NAPAKA=VSE-KAR-NI-PIRAMIDA-BREZ-NIČLE-NA-ROBU⟩"
OBT_PALINDROM = "⟨NAPAKA=VSE-KAR-NI-NEPALINDROMNA-PIRAMIDA⟩"
OBT_PAR = "⟨NAPAKA=VSE-KAR-NI-TUJA-OD-PARJA-1011-1101⟩"
OBT_KLJUC = "⟨NAPAKA=VSE-KAR-NI-PROSTA-KLJUČAVNICA⟩"
OBT_POLN = "⟨NAPAKA=VSE-KAR-NI-POLN-REGISTER⟩"


def tik():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def gol(j):
    return j[1:] if j.startswith("K") else j


def obrat(s):
    return s[::-1]


def preveri_kocko(ime, piramide, kljucavnice=None):
    ob = []
    n = len(piramide)
    if n != 4:
        ob.append((ime, OBT_SKUPINA, "merjeno piramid %d, pasalo je %d" % (n, 4)))
        return ob
    if len(set(piramide)) != 4:
        dvoj = sorted({p for p in piramide if piramide.count(p) > 1})
        ob.append((ime, OBT_UNIKAT, "dvojnik %s" % " ".join(dvoj)))
    for mesto, p in enumerate(piramide, 1):
        if p[0] == "0" or p[-1] == "0":
            ob.append((ime, OBT_NICLA, "piramida %s mesto %d" % (p, mesto)))
        if p == obrat(p):
            ob.append((ime, OBT_PALINDROM, "piramida %s mesto %d" % (p, mesto)))
        if p in ("1011", "1101"):
            ob.append((ime, OBT_PAR, "piramida %s mesto %d" % (p, mesto)))
    for i in range(4):
        for j in range(4):
            if i != j and obrat(piramide[i]) == piramide[j]:
                ob.append((ime, OBT_KLJUC, "obrat %s piramide %s ( mesto %d ) je piramida mesta %d"
                           % (obrat(piramide[i]), piramide[i], i + 1, j + 1)))
    if kljucavnice is not None:
        if len(kljucavnice) != 4:
            ob.append((ime, OBT_SKUPINA, "ključavnic %d, pasalo je %d" % (len(kljucavnice), 4)))
        else:
            for i in range(4):
                if kljucavnice[i] != obrat(piramide[i]):
                    ob.append((ime, OBT_KLJUC, "ključavnica %s mesta %d ni obrat piramide %s"
                               % (kljucavnice[i], i + 1, piramide[i])))
    return ob


def beri_kocke(pot):
    kocke = []
    podlaga = 0
    slovar = 0
    with open(pot, encoding="utf-8") as f:
        for vrstica, vr in enumerate(f, 1):
            e = vr.rstrip("\n")
            m = REG_VRST.match(e)
            if m:
                kocke.append((m.group(1), [m.group(i) for i in range(2, 6)], None, vrstica))
                continue
            m = BIN_VRST.match(e)
            if m:
                podlaga += 1
                continue
            m = SLOV_VRST.match(e)
            if m:
                kocke.append((m.group(1), [gol(m.group(i)) for i in range(6, 10)],
                              [gol(m.group(i)) for i in range(10, 14)], vrstica))
                slovar += 1
    return kocke, podlaga, slovar


def ukaz_pregister(pot, pricakovano=None):
    if not os.path.isfile(pot):
        print("RUMENA : datoteke ni pri viru ⊢ slab vhod ( %s )" % pot)
        return 2
    kocke, podlaga, slovar = beri_kocke(pot)
    ob = []
    lastnosti = {}
    for ime, pir, klj, vr in kocke:
        for p in pir:
            lastnosti.setdefault(p, ime)
        ob += preveri_kocko(ime, pir, klj)
    for p in sorted(lastnosti):
        if obrat(p) in lastnosti:
            ob.append((lastnosti[p], OBT_KLJUC,
                       "obrat %s piramide %s je piramida znaka %s ⊙ zakon 6"
                       % (obrat(p), p, lastnosti[obrat(p)])))
    if pricakovano is not None and len(kocke) != pricakovano:
        ob.append(("<register>", OBT_POLN, "znakov %d, pričevanih %d" % (len(kocke), pricakovano)))
    piramid = sum(len(pir) for _, pir, _, _ in kocke)
    kljucavnic = sum(len(kljj) if kljj else 0 for _, _, kljj, _ in kocke)
    if ob:
        cisto = sorted(set((i, o, v) for i, o, v in ob))
        print("RDECA NIHIL : kocke telesa niso čiste ⊢ obtožbe javno ×%d :" % len(cisto))
        for ime, obt, vzrok in cisto:
            print("  %s ( %s : %s )" % (ime, obt, vzrok))
        print("izmere : kock %d ∧ piramid %d ∧ ključavnic %d ∧ podlag preskočenih %d ⊙ zakon 1"
              % (len(kocke), piramid, kljucavnic, podlaga))
        print("NIHIL : nič ni zapečeno ; sodba ⟡ ⚔ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690 ; TIK %s" % tik())
        return 1
    print("ZELENA : VSAKA kocka ima štiri piramide ⊢")
    print("izmere : kock %d ∧ vsaka po štiri ⇒ piramid %d ⊢ ∧ unikatne ⊢ ∧ ničel na robu ×0 ∧ "
          "palindromov ×0 ∧ obratov med piramidami ×0 ⊙ izmera zakonov 2-7"
          % (len(kocke), piramid))
    print("ključavnic %d ( obrati pri viru ⊙ zakon 6 ) ∧ binarna podlaga ×%d preskočena ⊙ zakon 1 "
          "( samostojni žigi, ⟨ne⟩ piramide )" % (kljucavnic, podlaga))
    print("TIK %s ; ⟨SAMO-BERI⟩ ⟨BREZ-PREVOZA⟩ ; sodba ⟡ ⚔" % tik())
    return 0


def ukaz_ptocka(arg):
    try:
        n = int(arg)
    except ValueError:
        print("RUMENA : točka ni številka ⊢ slab vhod ( %r )" % arg)
        return 2
    piramide = ["%d" % (1000 + (n * m) % 9000) for m in M_VRSTE]
    print("formula zapečena ⊢ pri viru kockalnika : piramida = 1000 + ( mera točke × m ) mod 9000 ; "
          "m vrstni red {1,3,7,9}")
    for m, p in zip(M_VRSTE, piramide):
        print("  m%d ⇒ %s" % (m, p))
    print("vrsta piramid izrecena ⊢ ⟡ VERBATIM » vrsta piramid je pomembna « ( zakon 2 )")
    ob = preveri_kocko("<točka %s>" % arg, piramide)
    if ob:
        print("RDECA NIHIL : obtožbe javno ×%d" % len(ob))
        for ime, obt, vzrok in ob:
            print("  %s ( %s : %s )" % (ime, obt, vzrok))
        print("sodba ⟡ ⚔ ; TIK %s" % tik())
        return 1
    print("ZELENA : kocka točke %s ima štiri piramide ⊢ ∧ ključavnic ( obrati ) prostih ⊢" % arg)
    print("zasedenost golda ( zakoni 4-7 ) meri KOCKALNIK --preveri ⊙ ⟨EN-RAZLIČICA⟩ ⟨ne⟩ dvojnik")
    return 0


def ukaz_kocke(arg):
    piramide = []
    for z in arg.split():
        p = gol(z)
        if not (len(p) == 4 and p.isdigit()):
            print("RUMENA : okrnjena ali tuja oblika ⊢ slab vhod ( %s ) ⊙ AMANDMA KOCKE 6956" % z)
            return 2
        piramide.append(p)
    ob = preveri_kocko("<izrecna kocka>", piramide)
    if ob:
        print("RDECA NIHIL : obtožbe javno ×%d" % len(ob))
        for ime, obt, vzrok in ob:
            print("  %s ( %s : %s )" % (ime, obt, vzrok))
        print("sodba ⟡ ⚔ ; TIK %s" % tik())
        return 1
    print("ZELENA : izrecna kocka ima štiri piramide ⊢ ( %s )" % " ".join(piramide))
    return 0


def ukaz_test():
    import tempfile
    td = tempfile.mkdtemp(prefix="cetvernik-")
    p1 = os.path.join(td, "register.md")
    with open(p1, "w", encoding="utf-8") as f:
        f.write("# test\na = 5914 7068 2435 8172\nb = 9731 1258 4629 3817\n")
    vek = [
        ("cist register ZELENA", ukaz_pregister(p1, 2) == 0),
        ("pet piramid RDECA", glavna(["--kocke", "2311 2222 3333 4444 5555"]) == 1),
        ("dvojnik RDECA", glavna(["--kocke", "5914 5914 2435 8172"]) == 1),
        ("nicla na robu RDECA", glavna(["--kocke", "0914 5914 2435 8172"]) == 1),
        ("obratni par v kocki RDECA", glavna(["--kocke", "1234 4321 5678 8716"]) == 1),
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
    if args[0] == "--preveri-register":
        if len(args) < 2:
            print("RUMENA : datoteka ni izrečena ⊢ slab vhod")
            return 2
        pric = None
        if "--pričakovano" in args:
            i = args.index("--pričakovano")
            try:
                pric = int(args[i + 1])
            except (IndexError, ValueError):
                print("RUMENA : pričakovano ni številka ⊢ slab vhod")
                return 2
        return ukaz_pregister(args[1], pric)
    if args[0] == "--preveri-točka":
        if len(args) < 2:
            print("RUMENA : točka ni izrečena ⊢ slab vhod")
            return 2
        return ukaz_ptocka(args[1])
    if args[0] == "--kocke":
        if len(args) < 2:
            print("RUMENA : kocka ni izrečena ⊢ slab vhod")
            return 2
        return ukaz_kocke(args[1])
    print("RUMENA : roka neznana ( %s ) ⊙ 40" % args[0])
    return 40


if __name__ == "__main__":
    sys.exit(glavna(sys.argv[1:]))
