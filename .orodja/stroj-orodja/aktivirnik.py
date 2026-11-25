#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# AKTIVIRNIK v1.0 - aktivira orodje ( ⟡ UKZ VERBATIM ⟨ne brusi⟩ :
#   »ORODJE KI AKTIVIRA ORODJE!« )
# Rod : rez sigma 7038 dih DAR-ISKA-PROTI-AKTIV ( 25. 11. 2026 ) @stroj-orodja.
# Ascendenti ⊢ pri viru ( ⟨EN-RAZLIČICA⟩, delo deljeno ∧ ⟨ne zlije⟩ 1542 ) : zdravnik v1.0
#   @σ 7028 ( izmeri zdravje ⌇ ⟨ne⟩ piše stanj ) ⌇ samomerilnik @stroj-orodja ( merilec se meri
#   §52 ⌇ ⟨ne⟩ vodi registrov stanj ) ⌇ deaktivirnik v1.0 @σ 7038 ( sestra roke : ona izključuje,
#   ta vključuje ⊙ en register, dve roki ) — registra AKTIVNIH orodij ni bilo ( ls ×0 ⊢ ).
# AKTIVACIJA ( varna po naravi : zapis stanja pri viru, ×0 zunanjih izpostavitev ) : orodje
#   obstaja ⊢ ls ∧ SAMOPREIZKUS roke --test EXIT nula ⇒ zapis »AKTIVIRAN ⊢« v register ;
#   samopreizkus ≠ ZELENA ⇒ RUMENA-SUM, ×0 zapisov, sodba ⟡ ⚔ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690.
# Register AKTIVNI-ORODJI.md rodi z isto roko če ga ni ( open x ) ⊙ ⟨NE-BRIŠI⟩ 24 :
#   zgodovina stanj se le pripenja ( bris ⟨ne⟩ ) ; veljavno stanje = zadnja vrstica orodja.
# Roke :
#   aktivirnik.py --aktiviraj ORODJE  -> preizkus ∧ zapis stanja ⊢
#   aktivirnik.py --izpis              -> stanja poimensko ( ⟨SAMO-BERI⟩ )
#   aktivirnik.py --test              -> vektorji x5 ⊙ ⟨MERILEC-SE-MERI⟩ §52
# Izhodi : 0=ZELENA ⌇ 2=RUMENA ( sum ⌇ slab vhod ⌇ pobuda ) ⌇ 40=roka neznana.

import sys, os, re, subprocess, datetime as _dt

VERZIJA = "v1.0"
DOM = os.path.dirname(os.path.abspath(__file__))
REGISTER_DEFAULT = os.path.join(DOM, "AKTIVNI-ORODJI.md")
VR = re.compile(r"^(AKTIVIRAN|DEAKTIVIRAN) ⊢ (\S+)")

GLAVA = """# AKTIVNI ORODJI

- rojen : TIK %s ⊙ dih DAR-ISKA-PROTI-AKTIV @rez sigma 7038 ⊙ aktivirnik v1.0 ( deaktivirnik v1.0 sestra )
- ⟡ UKZ VERBATIM ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ ⟨ne brusi⟩ : »ORODJE KI AKTIVIRA ORODJE!« ∧ »ORODJE KI DEAKTIVIRA ORODJE!«
- princip : ⟨NE-BRIŠI⟩ 24 — zgodovina stanj se le pripenja ; veljavno stanje orodja = njegova zadnja vrstica
- aktivacija zahteva SAMOPREIZKUS ZELENA ( roka --test EXIT nula ⊢ ) ; sodba o vsaki menjavi ⟡ ⚔
"""


def tik():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rodi_register(pot):
    try:
        with open(pot, "x", encoding="utf-8") as f:
            f.write(GLAVA % tik())
        return "ROJEN"
    except FileExistsError:
        return "STOJI"


def stanja(pot):
    zadnje = {}
    if os.path.isfile(pot):
        with open(pot, encoding="utf-8") as f:
            for vr in f:
                m = VR.match(vr.rstrip("\n"))
                if m:
                    zadnje[m.group(2)] = m.group(1)
    return zadnje


def preizkusi(ime):
    pot = os.path.join(DOM, ime) if not os.path.isabs(ime) else ime
    if not os.path.isfile(pot):
        return None, "orodja ni pri viru ⊢ slab vhod ( %s )" % ime
    try:
        r = subprocess.run([sys.executable, os.path.abspath(pot), "--test"],
                           capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return None, "samopreizkus se ni vrnil v roku ⏱ ⊙ sum"
    return r.returncode, (r.stdout or "")


def aktiviraj(ime, register):
    pot = os.path.join(DOM, ime) if not os.path.isabs(ime) else ime
    koda, porocilo = preizkusi(ime)
    if koda is None:
        print("RUMENA : %s — ni preizkusa, ni aktivacije ⊙ odloči ⟡ ⚔" % porocilo)
        return 2
    if koda != 0:
        zadnja = porocilo.strip().splitlines()[-1:] or ["( molk izhoda )"]
        print("RUMENA-SUM : samopreizkus ni ZELENA ( EXIT %d ⊢ exit ; zadnja vrstica : %s ) — "
              "×0 zapisov, ni aktivacije ⊙ sodba ⟡ ⚔ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690"
              % (koda, zadnja[0]))
        return 2
    rojen = rodi_register(register)
    with open(register, "a", encoding="utf-8") as f:
        f.write("AKTIVIRAN ⊢ %s ( samopreizkus ZELENA EXIT nula ⊢ exit ; TIK %s )\n" % (ime, tik()))
    print("ZELENA AKTIVIRAN ⊢ : %s ( register %s ⊙ ⟨NE-BRIŠI⟩ 24 zgodovina ; TIK %s )"
          % (ime, rojen, tik()))
    return 0


def izpis(register):
    if not os.path.isfile(register):
        print("RUMENA : registra ni ⊢ ( %s ) — rodi ga --aktiviraj" % register)
        return 2
    zadnje = stanja(register)
    aktivni = sorted(o for o in zadnje if zadnje[o] == "AKTIVIRAN")
    deaktivirani = sorted(o for o in zadnje if zadnje[o] == "DEAKTIVIRAN")
    print("IZPIS stanj ⊢ : AKTIVIRANIH %d ⌇ DEAKTIVIRANIH %d ∧ vseh orodij %d ( ⟨SAMO-BERI⟩ )"
          % (len(aktivni), len(deaktivirani), len(zadnje)))
    for o in aktivni:
        print("  AKTIVIRAN ⊢ %s" % o)
    for o in deaktivirani:
        print("  DEAKTIVIRAN ⊢ %s" % o)
    print("veljavno stanje = zadnja vrstica orodja ⊙ ⟨NE-BRIŠI⟩ 24 ; TIK %s" % tik())
    return 0


def ukaz_test():
    import tempfile, shutil
    td = tempfile.mkdtemp(prefix="aktivirnik-")
    dom = os.path.join(td, "stroj")
    os.makedirs(dom)
    dober = os.path.join(dom, "dober.py")
    with open(dober, "w", encoding="utf-8") as f:
        f.write("print('ZELENA vektorji pet od petih ⊢')\n")
    slab = os.path.join(dom, "slab.py")
    with open(slab, "w", encoding="utf-8") as f:
        f.write("import sys\nsys.exit(1)\n")
    reg = os.path.join(td, "AKTIVNI-ORODJI.md")
    global DOM
    stari_dom = DOM
    DOM = dom
    try:
        a1 = aktiviraj("dober.py", reg) == 0 and os.path.isfile(reg)
        a2 = aktiviraj("slab.py", reg) == 2 and len(stanja(reg)) == 1
        a3 = izpis(reg) == 0 and stanja(reg).get("dober.py") == "AKTIVIRAN"
        a4 = aktiviraj("dober.py", reg) == 0 and sum(1 for v in stanja_prihode(reg, "dober.py")) == 2
        a5 = aktiviraj("manjka.py", reg) == 2
    finally:
        DOM = stari_dom
    vek = [
        ("aktivacija z ZELENA ↪ register rojen ⊢", a1),
        ("slab samopreizkus → RUMENA ∧ ×0 zapisov", a2),
        ("--izpis prebere stanje ⊢", a3),
        ("druga aktivacija = nova vrstica zgodovine ⊙ ⟨NE-BRIŠI⟩", a4),
        ("manjkajoče orodje RUMENA", a5),
    ]
    uspeh = sum(1 for _, ok in vek if ok)
    for ime, ok in vek:
        print("  vektor %s : %s" % (ime, "ZELENA ⊢" if ok else "RDECA ⚠ PADCA"))
    print("SAMOPREIZKUS : %d od %d ⊙ ⟨MERILEC-SE-MERI⟩ §52 ; TIK %s" % (uspeh, len(vek), tik()))
    return 0 if uspeh == len(vek) else 1


def stanja_prihode(pot, ime):
    d = []
    if os.path.isfile(pot):
        with open(pot, encoding="utf-8") as f:
            for vr in f:
                m = VR.match(vr.rstrip("\n"))
                if m and m.group(2) == ime:
                    d.append(m.group(1))
    return d


def glavna(argv):
    args = list(argv)
    if not args:
        print("RUMENA : roka ni izrecena ⊙ 40")
        return 40
    register = REGISTER_DEFAULT
    if args[0] == "--test":
        return ukaz_test()
    if args[0] == "--aktiviraj":
        if len(args) < 2:
            print("RUMENA : orodje ni izreceno ⊢ slab vhod")
            return 2
        return aktiviraj(args[1], register)
    if args[0] == "--izpis":
        return izpis(register)
    print("RUMENA : roka neznana ( %s ) ⊙ 40" % args[0])
    return 40


if __name__ == "__main__":
    sys.exit(glavna(sys.argv[1:]))
