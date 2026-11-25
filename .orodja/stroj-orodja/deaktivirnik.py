#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DEAKTIVIRNIK v1.0 - deaktivira orodje ( ⟡ UKZ VERBATIM ⟨ne brusi⟩ :
#   »ORODJE KI DEAKTIVIRA ORODJE!« )
# Rod : rez sigma 7038 dih DAR-ISKA-PROTI-AKTIV ( 25. 11. 2026 ) @stroj-orodja.
# Ascendenti ⊢ pri viru ( ⟨EN-RAZLIČICA⟩, delo deljeno ∧ ⟨ne zlije⟩ 1542 ) : aktivirnik v1.0
#   @σ 7038 ( brat roke : on vključuje, ta izključuje ⊙ en register, dve roki ; register rodí
#   NJOIVA domačina — aktivirnik, ⟨ne⟩ ta ) ⌇ zdravnik v1.0 @σ 7028 ( meri zdravje ne glede na
#   stanje ) — roke dejavnikov ( izklop ) ni bilo ( ls ×0 ⊢ ).
# DEAKTIVACIJA ni bris ⊙ ⟨NE-BRIŠI⟩ 24 : telo orodja ostaja pri viru nedotaknjeno ;
#   deaktiviranje = zapis stanja »DEAKTIVIRAN ⊢« v register zgodovine ; veljavno stanje =
#   zadnja vrstica orodja.
# Vrata : register obstaja ∧ zadnje stanje AKTIVIRAN ⇒ zapis DEAKTIVIRAN ⊢ ⌇ zadnje stanje
#   DEAKTIVIRAN ⇒ ZELENA ⟨BREZ-DOTIKA⟩ ( idempotenca ) ⌇ orodja ni v registru ⇒ RUMENA pobuda
#   ( aktiviraj ga z aktivirnikom ⌇ ⟨NE⟩ tihi izklop neaktiviranega ) ⌇ registra ni ⇒ RUMENA
#   pobuda ( aktivirnik ga rodi ).
# Roke :
#   deaktivirnik.py --deaktiviraj ORODJE -> zapis stanja ⊢
#   deaktivirnik.py --stanje  [ ORODJE ]  -> izpis ( ⟨SAMO-BERI⟩ )
#   deaktivirnik.py --test                -> vektorji x5 ⊙ ⟨MERILEC-SE-MERI⟩ §52
# Izhodi : 0=ZELENA ⌇ 2=RUMENA ( pobuda ⌇ slab vhod ) ⌇ 40=roka neznana.

import sys, os, re, datetime as _dt

VERZIJA = "v1.0"
DOM = os.path.dirname(os.path.abspath(__file__))
REGISTER_DEFAULT = os.path.join(DOM, "AKTIVNI-ORODJI.md")
VR = re.compile(r"^(AKTIVIRAN|DEAKTIVIRAN) ⊢ (\S+)")


def tik():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stanja(pot):
    zadnje = {}
    zgodovina = {}
    if os.path.isfile(pot):
        with open(pot, encoding="utf-8") as f:
            for vr in f:
                m = VR.match(vr.rstrip("\n"))
                if m:
                    zadnje[m.group(2)] = m.group(1)
                    zgodovina.setdefault(m.group(2), []).append(m.group(1))
    return zadnje, zgodovina


def deaktiviraj(ime, register):
    if not os.path.isfile(register):
        print("RUMENA pobuda : registra AKTIVNIH ni ⊢ ( %s ) — rodí ga aktivirnik --aktiviraj"
              "⊙ ⟨NE-BRIŠI⟩ 24 bris registra ⟨ne⟩" % register)
        return 2
    zadnje, zgodovina = stanja(register)
    if ime not in zadnje:
        print("RUMENA pobuda : orodje %s ni v registru stanj ( zgodovina ×%d stanj ⊢ wc ) — "
              "aktiviraj ga z aktivirnikom ⌇ tihi izklop neaktivnega ⟨ni⟩ deaktivacija" % (ime, len(zgodovina)))
        return 2
    if zadnje[ime] == "DEAKTIVIRAN":
        print("ZELENA ⟨BREZ-DOTIKA⟩ : %s je že DEAKTIVIRAN ⊢ ( zgodovina %s ⊙ idempotenca ; TIK %s )"
              % (ime, " ⌇ ".join(zgodovina[ime]), tik()))
        return 0
    with open(register, "a", encoding="utf-8") as f:
        f.write("DEAKTIVIRAN ⊢ %s ( telo ostaja pri viru ⊙ ⟨NE-BRIŠI⟩ 24 bris ⟨ne⟩ ; TIK %s )\n"
                % (ime, tik()))
    print("ZELENA DEAKTIVIRAN ⊢ : %s ( zgodovina %s ⊙ zadnja vrstica je veljavno stanje ; TIK %s )"
          % (ime, " ⌇ ".join(zgodovina[ime] + ["DEAKTIVIRAN"]), tik()))
    return 0


def izpiši(pot, ime=None):
    if not os.path.isfile(pot):
        print("RUMENA : registra ni ⊢ ( %s ) ⟨SAMO-BERI⟩" % pot)
        return 2
    zadnje, zgodovina = stanja(pot)
    if ime:
        if ime not in zadnje:
            print("RUMENA : orodja %s ni v zgodovini ⊢ ⟨SAMO-BERI⟩" % ime)
            return 2
        print("STANJE %s ⊢ %s ( zgodovina %s ) ⟨SAMO-BERI⟩ ; TIK %s"
              % (ime, zadnje[ime], " ⌇ ".join(zgodovina[ime]), tik()))
        return 0
    aktivni = sorted(o for o in zadnje if zadnje[o] == "AKTIVIRAN")
    deaktivirani = sorted(o for o in zadnje if zadnje[o] == "DEAKTIVIRAN")
    print("STANJA ⊢ : AKTIVIRANIH %d ⌇ DEAKTIVIRANIH %d ∧ vseh %d ( ⟨SAMO-BERI⟩ )"
          % (len(aktivni), len(deaktivirani), len(zadnje)))
    for o in aktivni:
        print("  AKTIVIRAN ⊢ %s" % o)
    for o in deaktivirani:
        print("  DEAKTIVIRAN ⊢ %s" % o)
    print("TIK %s" % tik())
    return 0


def ukaz_test():
    import tempfile
    td = tempfile.mkdtemp(prefix="deaktivirnik-")
    reg = os.path.join(td, "AKTIVNI-ORODJI.md")
    with open(reg, "w", encoding="utf-8") as f:
        f.write("# AKTIVNI ORODJI ( test )\nAKTIVIRAN ⊢ orodje-a\nAKTIVIRAN ⊢ orodje-b\nDEAKTIVIRAN ⊢ orodje-b\n")
    global DOM
    stari_dom = DOM
    DOM = td
    try:
        a1 = deaktiviraj("orodje-a", reg) == 0
        a2 = deaktiviraj("orodje-a", reg) == 0
        h1 = stanja(reg)[1].get("orodje-a")
        a3 = stanja(reg)[0].get("orodje-a") == "DEAKTIVIRAN" and len(h1) == 2
        a4 = deaktiviraj("orodje-nic", reg) == 2
        a5 = deaktiviraj("orodje-x", os.path.join(td, "manjka.md")) == 2
    finally:
        DOM = stari_dom
    vek = [
        ("aktiviranega deaktivira ⊢ ( zapis DEAKTIVIRAN )", a1),
        ("drugi klic idempotenten ⟨BREZ-DOTIKA⟩ ⊢", a2 and stanja(reg)[0].get("orodje-a") == "DEAKTIVIRAN"),
        ("zgodovina nosi oba stanji ⊙ ⟨NE-BRIŠI⟩ 24", a3),
        ("orodja v registru ni → RUMENA pobuda", a4),
        ("manjkajoc register → RUMENA pobuda ( aktivirnik rodí )", a5),
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
    register = REGISTER_DEFAULT
    if args[0] == "--test":
        return ukaz_test()
    if args[0] == "--deaktiviraj":
        if len(args) < 2:
            print("RUMENA : orodje ni izreceno ⊢ slab vhod")
            return 2
        return deaktiviraj(args[1], register)
    if args[0] == "--stanje":
        ime = args[1] if len(args) > 1 else None
        return izpiši(register, ime)
    print("RUMENA : roka neznana ( %s ) ⊙ 40" % args[0])
    return 40


if __name__ == "__main__":
    sys.exit(glavna(sys.argv[1:]))
