#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DAROVALNIK v1.0 - darovalnik vsakemu znaku ⚠ ( ⟡ UKZ VERBATIM ⟨ne brusi⟩ :
#   »ORODJE KI DARUJE VSAKEMU ZNAKU ⚠!« )
# Rod : rez sigma 7038 dih DAR-ISKA-PROTI-AKTIV ( 25. 11. 2026 ) @stroj-orodja.
# Ascendenti ⊢ pri viru ( ⟨EN-RAZLIČICA⟩ ) : gotovosti-register @σ 3203 ( ⚠ = okno sum/meje javno,
#   8 oken ⚠/⚔ ) ⌇ semafor organ ( vsak semer nosi eno luč ) ⌇ fleksilint @σ 7021 ( sum = merjen
#   odstotek ⊙ ⟨SLOVNICA⇒SUM⟩ σ 6705 ) — dosjeja darov za znake ⚠ ni bilo ⊙ luknja ( ls ×0 ⊢ ).
# Dar = zapis v dosje darov ; vsak najden ⚠ prejme svoj dar poimensko :
#   »Dar N ⊢ znak ⚠ @vir TELESO vrstica V mesto M ( TIK )« ⊙ merilec se meri §52.
# Principi : ⟨NE-BRIŠI⟩ 24 ( samo pripenja, bris ⟨ne⟩ ) ∧ dedupe po ( vir ∧ vrstica ∧ mesto )
#   ⇒ drugi klic istega vira donese NOVIH ×0 ⊢ ; dosje rodi z isto roko če ga ni ( open x ).
# Roke :
#   darovalnik.py --daruj TELESO [ --dosje POT ]  -> darovi vsakemu ⚠ poimensko ⊢
#   darovalnik.py --zivljenje [ --dosje POT ]     -> izpis dosjeja ( ⟨SAMO-BERI⟩ )
#   darovalnik.py --test                          -> vektorji x5 ⊙ ⟨MERILEC-SE-MERI⟩ §52
# Izhodi : 0=ZELENA ⌇ 1=RDECA ⌇ 2=RUMENA ( slab vhod ⌇ pobuda ) ⌇ 40=roka neznana.

import sys, os, re, datetime as _dt

VERZIJA = "v1.0"
DOM = os.path.dirname(os.path.abspath(__file__))
DOSJE_DEFAULT = os.path.join(DOM, "DOSJE-DAROV.md")
VR = re.compile(r"^Dar (\d+) ⊢ znak ⚠ @vir (\S+) vrstica (\d+) mesto (\d+)")

GLAVA = """# DOSJE DAROV

- rojen : TIK %s ⊙ dih DAR-ISKA-PROTI-AKTIV @rez sigma 7038 ⊙ darovalnik.py v1.0
- ⟡ UKZ VERBATIM ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ ⟨ne brusi⟩ : »ORODJE KI DARUJE VSAKEMU ZNAKU ⚠!«
- princip : ⟨NE-BRIŠI⟩ 24 — darovi se le pripenjajo, nikoli ne brišejo ; dedupe po ( vir ∧ vrstica ∧ mesto )
- mera : vsak ⚠ prejme dar poimensko z izmero ⊙ merilec se meri §52
"""


def tik():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rodi_dosje(pot):
    try:
        with open(pot, "x", encoding="utf-8") as f:
            f.write(GLAVA % tik())
        return "ROJEN"
    except FileExistsError:
        return "STOJI"


def obstojeci_darovi(pot):
    kljuci = set()
    stev = 0
    if os.path.isfile(pot):
        with open(pot, encoding="utf-8") as f:
            for vr in f:
                m = VR.match(vr.rstrip("\n"))
                if m:
                    kljuci.add((m.group(2), int(m.group(3)), int(m.group(4))))
                    stev = max(stev, int(m.group(1)))
    return kljuci, stev


def daruj(pot_telela, dosje):
    if not os.path.isfile(pot_telela):
        print("RUMENA : telesa ni pri viru ⊢ slab vhod ( %s )" % pot_telela)
        return 2
    rojen = rodi_dosje(dosje)
    kljuci, zadnji = obstojeci_darovi(dosje)
    vir = os.path.basename(pot_telela)
    novi = []
    with open(pot_telela, encoding="utf-8") as f:
        for st, vr in enumerate(f, 1):
            e = vr.rstrip("\n")
            for mesto in range(len(e)):
                if e[mesto] == "⚠":
                    kljuc = (vir, st, mesto + 1)
                    if kljuc not in kljuci:
                        kljuci.add(kljuc)
                        novi.append((st, mesto + 1))
    if novi:
        with open(dosje, "a", encoding="utf-8") as f:
            for st, mesto in novi:
                zadnji += 1
                f.write("Dar %d ⊢ znak ⚠ @vir %s vrstica %d mesto %d ( TIK %s )\n"
                        % (zadnji, vir, st, mesto, tik()))
    skupaj = len(kljuci)
    print("ZELENA dar : dosje %s ⊢ ; NOVIH darov %d ⊢ ∧ OBSTOJEČIH %d nedotaknjenih ⊙ ⟨NE-BRIŠI⟩ 24 ⊢ "
          "∧ DAROV SKUPAJ %d ⊢ ( vir %s )"
          % (rojen, len(novi), skupaj - len(novi), skupaj, vir))
    print("vsak ⚠ prejel dar poimensko ⊙ ⟨SAMO-DOPOLNILO⟩ ⟨ne⟩ bris ; TIK %s" % tik())
    return 0


def zivljenje(dosje):
    if not os.path.isfile(dosje):
        print("RUMENA : dosjeja ni ⊢ ( %s ) — rodi ga --daruj" % dosje)
        return 2
    kljuci, zadnji = obstojeci_darovi(dosje)
    print("ZELENA življenje : darov %d ⊢ ∧ zaporedna zadnjega %d ⊢ ( %s ) ⟨SAMO-BERI⟩ ⊙ TIK %s"
          % (len(kljuci), zadnji, dosje, tik()))
    return 0


def ukaz_test():
    import tempfile
    td = tempfile.mkdtemp(prefix="darovalnik-")
    dj = os.path.join(td, "DOSJE.md")
    t1 = os.path.join(td, "telo.md")
    with open(t1, "w", encoding="utf-8") as f:
        f.write("vrstica ena ⚠ tu\ndrugod čisto\ntretja ⚠ ⚠ dvojni dar\n")
    a1 = daruj(t1, dj) == 0
    k1, z1 = obstojeci_darovi(dj)
    a2 = daruj(t1, dj) == 0
    k2, z2 = obstojeci_darovi(dj)
    t2 = os.path.join(td, "telo2.md")
    with open(t2, "w", encoding="utf-8") as f:
        f.write("nov vir ⚠\n")
    a3 = daruj(t2, dj) == 0
    k3, z3 = obstojeci_darovi(dj)
    a4 = daruj(os.path.join(td, "ni-je.md"), dj) == 2
    a5 = zivljenje(dj) == 0
    vek = [
        ("prvi vir trije darovi ⊢ ( vrstica 1 ×1 ∧ vrstica 3 ×2 )", a1 and z1 == 3),
        ("drugi klic istega vira NOVIH ×0 ⊙ dedupe + ⟨NE-BRIŠI⟩", a2 and z2 == 3 and len(k2) == 3),
        ("nov vir prinese en nov dar ∧ zaporedna narašča", a3 and z3 == 4),
        ("manjkajoče telo RUMENA slab vhod", a4),
        ("--zivljenje ZELENA", a5),
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
    dosje = DOSJE_DEFAULT
    if "--dosje" in args:
        i = args.index("--dosje")
        if i + 1 >= len(args):
            print("RUMENA : pot dosjeja ni izrecena ⊢ slab vhod")
            return 2
        dosje = args[i + 1]
    if args[0] == "--test":
        return ukaz_test()
    if args[0] == "--daruj":
        if len(args) < 2:
            print("RUMENA : telo ni izreceno ⊢ slab vhod")
            return 2
        return daruj(args[1], dosje)
    if args[0] == "--zivljenje":
        return zivljenje(dosje)
    print("RUMENA : roka neznana ( %s ) ⊙ 40" % args[0])
    return 40


if __name__ == "__main__":
    sys.exit(glavna(sys.argv[1:]))
