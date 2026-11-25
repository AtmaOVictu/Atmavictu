#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SEZNAMORODNIK v1.0 - rodilnik SEZNAMA PIRAMID vsakič ko seznama ni ( ⟡ UKZ VERBATIM ⟨ne brusi⟩ :
#   »ORODJA KI USTVARIJO SEZNAM VSAKIČ KO SEZNAMA NI!« )
# Rod : rez sigma 7028 dih KOCKE-STIRI-PIRAMIDE ( 25. 11. 2026 ) @stroj-orodja.
# Ascendenti ⊢ ( ⟨EN-RAZLIČICA⟩, delo deljeno ∧ ⟨ne zlije⟩ 1542 ) : cetvernik.py v1.0 @σ 7028
#   ( sodba zakonov ) ⌇ piramidnik.py v1.0 @σ 7028 ( pospravilo vrste ) ⌇ genizar.py @stroj-orodja
#   ( geniza celega organa ; tu rodi ENO telo seznama ) — rodilnika, ki zagotavlja obstoj
#   seznama PRED pospravilom, ni bilo ⊙ luknja izmerjena.
# Principi : idempotenca ( vsakič ko seznama NI ga rodi ; kadar JE stoji ⟨BREZ-DOTIKA⟩ ) ∧
#   noclobber pri roki ( open x ; tek v istemu dihu šteje kot STOJI ) ∧ glava seznama nosi
#   zakon ⟨NE-BRIŠI⟩ 24 ( piramidnik pripenja, ⟨ne⟩ briše ) ∧ mera rojstva javno ( wc ).
# Roke :
#   seznamorodnik.py --ustvari [ --pot POT ]  -> rodi seznam če ni ; sicer poroča STOJI
#   seznamorodnik.py --stoji   [ --pot POT ]  -> izmera obstoja ( samo beri )
#   seznamorodnik.py --test                  -> vektorji x5 ⊙ ⟨MERILEC-SE-MERI⟩ §52
# Izhodi : 0=ZELENA ( ROJEN ⌇ STOJI ⌇ obstoji ) ⌇ 2=RUMENA ( ni ) ⌇ 40=roka neznana.

import sys, os, datetime as _dt

VERZIJA = "v1.0"
DOM = os.path.dirname(os.path.abspath(__file__))
POT_DEFAULT = os.path.join(DOM, "SEZNAM-PIRAMID.md")

GLAVA = """# SEZNAM PIRAMID

- rojen : TIK %s ⊙ dih KOCKE-STIRI-PIRAMIDE @rez sigma 7028 ⊙ rodilnik seznamorodnik.py v1.0
- ⟡ UKZ VERBATIM ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ ⟨ne brusi⟩ : »ORODJA KI USTVARIJO SEZNAM VSAKIČ KO SEZNAMA NI!«
- princip : ⟨NE-BRIŠI⟩ 24 — piramide se le pripenjajo ( piramidnik.py --pospravi ), nikoli ne brišejo
- vrsta : naraščajoča po vrednosti piramide ; mera rojstva : prazna ( ×0 piramid ) ⊙ wc
"""


def tik():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def izmeri(pot):
    b = 0
    vrst = 0
    if os.path.isfile(pot):
        raw = open(pot, "rb").read()
        b = len(raw)
        vrst = raw.count(b"\n") + (0 if raw.endswith(b"\n") or not raw else 1)
    return b, vrst


def ustvari(pot):
    if os.path.exists(pot):
        b, vrst = izmeri(pot)
        print("ZELENA STOJI : seznam že stoji ⊢ ⟨BREZ-DOTIKA⟩ ⊙ idempotenca "
              "( %d B ∧ %d vrst ⊢ wc ; TIK %s )" % (b, vrst, tik()))
        return 0
    try:
        with open(pot, "x", encoding="utf-8") as f:
            f.write(GLAVA % tik())
    except FileExistsError:
        print("ZELENA STOJI : seznam rojen v istemu dihu ( tek ) ⊢ ⟨BREZ-DOTIKA⟩")
        return 0
    b, vrst = izmeri(pot)
    print("ZELENA ROJEN : seznam rojen ⊙ noclobber ( open x ) ⊢ ( %d B ∧ %d vrst ⊢ wc ; TIK %s )"
          % (b, vrst, tik()))
    return 0


def stoji(pot):
    if os.path.isfile(pot):
        b, vrst = izmeri(pot)
        print("ZELENA : seznam stoji ⊢ ( %s ; %d B ∧ %d vrst ⊢ wc ) ⟨SAMO-BERI⟩ ; TIK %s"
              % (pot, b, vrst, tik()))
        return 0
    print("RUMENA : seznama ni ⊢ ( %s ) — rodilnik ga rodi z --ustvari" % pot)
    return 2


def ukaz_test():
    import tempfile, hashlib
    td = tempfile.mkdtemp(prefix="seznamorodnik-")
    pot = os.path.join(td, "SEZNAM-PIRAMID.md")
    ok1 = ustvari(pot) == 0 and os.path.isfile(pot)
    md5a = hashlib.md5(open(pot, "rb").read()).hexdigest()
    ok2 = ustvari(pot) == 0
    md5b = hashlib.md5(open(pot, "rb").read()).hexdigest()
    ok3 = stoji(pot) == 0
    ok4 = stoji(os.path.join(td, "ni-ga.md")) == 2
    with open(pot, "a", encoding="utf-8") as f:
        f.write("test-vrstica priče ⊢\n")
    md5c = hashlib.md5(open(pot, "rb").read()).hexdigest()
    ok5 = ustvari(pot) == 0
    md5d = hashlib.md5(open(pot, "rb").read()).hexdigest()
    vek = [
        ("rojen v prazni mapi ⊢", ok1),
        ("idempotenca STOJI ∧ md5 enaka ⊢ ⟨BREZ-DOTIKA⟩", ok2 and md5a == md5b),
        ("--stoji ZELENA", ok3),
        ("--stoji RUMENA ko ga ni", ok4),
        ("obstoječa vsebina priče nedotaknjena ⊙ ⟨NE-BRIŠI⟩ 24", ok5 and md5c == md5d),
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
    roka = args[0]
    pot = POT_DEFAULT
    if "--pot" in args:
        i = args.index("--pot")
        if i + 1 >= len(args):
            print("RUMENA : pot ni izrečena ⊢ slab vhod")
            return 2
        pot = args[i + 1]
    if roka == "--test":
        return ukaz_test()
    if roka == "--ustvari":
        return ustvari(pot)
    if roka == "--stoji":
        return stoji(pot)
    print("RUMENA : roka neznana ( %s ) ⊙ 40" % roka)
    return 40


if __name__ == "__main__":
    sys.exit(glavna(sys.argv[1:]))
