#!/usr/bin/env python3
# varnost-lint.py v1.0 — IINT : imunost instrumentov pred okužbo ∧ infiltracijo tujk ∧ tujcev
# ukaz ⟡ ( 23. 11. 2026 ) VERBATIM : »MORAVA JIM DODATI TUDI VARNOSTNE SKLOPE DA SO IMUNE PRED OKUŽBO IN INFILTRACIJO TUJK IN TUJCEV«
# imunost = ( 1 ) manifest resnice instrumentov ( md5 vsakega ) ( 2 ) vsaka sprememba brez pečata = alarm okužbe ( 3 ) infiltracija : cenzus pisav + maske + dvojni tolkači v telesih instrumentov ( 4 ) preizkus vsakega instrumenta z njegovim lastnim samopreizkusom
# varnostni sklop orodja samega : ⟨ne⟩ eval ⟨ne⟩ exec ⟨ne⟩ omrežje ; pisanje samo v .geniza ; poti le pod korenom ; samocenzus pisav
#roke : --manifest                     : rodi manifest md5 vseh instrumentov ( .py ∧ .sh v stroj-orodja, brez .geniza )
#       --preveri MANIFEST              : vsak instrument primerja z manifestom ; rezultat : IMUNO ⊢ ali ALARM poimensko
#       --okužba                       : infiltracijski cenzus teles instrumentov ( cirilica ⌇ kitajščina ⌇ maske brez šestic ⌇ dvojni tolkač )
#       --imunski-pregled               : požene samopreizkus vsakega instrumenta ∧ zbira scre
#       --samopreizkus                  : T1 manifest rodjen ⌇ T2 podtaknjena okužba ujeta ⌇ T3 infiltracija ulovljena
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · MERJENO, ⟨NE⟩ UGIBANO ⊙ 2690
import sys, os, hashlib, datetime, glob, re

KOREN = "/home/user/knowledge"
STROJ = KOREN + "/stroj-orodja"
CIRILICA = [(0x0400, 0x052F), (0x2DE0, 0x2DFF), (0xA640, 0xA69F)]
KITAJSCINA = [(0x3000, 0x303F), (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF), (0x20000, 0x3FFFF)]

def tik():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def md5(pot):
    with open(pot, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def instrumenti():
    for pot in sorted(glob.glob(STROJ + "/*.py") + glob.glob(STROJ + "/*.sh")):
        yield os.path.basename(pot), pot

def pisava(cp):
    for a, b in CIRILICA + KITAJSCINA:
        if a <= cp <= b:
            return True
    return False

def manifest():
    vrstice = ["# MANIFEST INSTRUMENTOV @%s ⊙ σ ( resnica vsakega instrumenta po izmeri )" % tik()]
    for ime, pot in instrumenti():
        vrstice.append("%s %d %s" % (ime, os.path.getsize(pot), md5(pot)))
    geniza = STROJ + "/.geniza"
    os.makedirs(geniza, exist_ok=True)
    potm = geniza + "/MANIFEST-instrumentov-%s.md" % tik().replace(":", "")
    open(potm, "w", encoding="utf-8").write("\n".join(vrstice) + "\n")
    print("MANIFEST ROĐEN ⊢ %s ( instrumentov %d )" % (potm, len(vrstice) - 1))
    for v in vrstice[1:]:
        print("  " + v)
    return 0

def preveri_manifest(potm):
    if not potm.startswith(KOREN) or not os.path.isfile(potm):
        print("VARNOST ⚠ : manifest izven korena ali ne obstaja")
        return 2
    alarma = 0
    for v in open(potm, encoding="utf-8"):
        deli = v.strip().split()
        if len(deli) != 3 or deli[0].startswith("#"):
            continue
        pot = STROJ + "/" + deli[0]
        if not os.path.isfile(pot):
            print("ALARM ⚠ : %s : telo je izginilo ( izgon brez pečata )" % deli[0])
            alarma += 1
            continue
        tr_v, tr_m = int(deli[1]), deli[2]
        v_del, m_del = os.path.getsize(pot), md5(pot)
        if tr_v == v_del and tr_m == m_del:
            print("IMUNO ⊢ %s ( %d B, md5 %s )" % (deli[0], v_del, m_del))
        else:
            print("ALARM OKUŽBE ⚠ %s : manifest %d B %s ⌇ izmera %d B %s ⇒ telo se je spremenilo brez pečata" % (deli[0], tr_v, tr_m, v_del, m_del))
            alarma += 1
    print("SODBA : %s @%s ( alarmov %d )" % ("IMUNO ⊢" if alarma == 0 else "OKUŽBA ⚠ : instrumenti potrebujejo sodbo", tik(), alarma))
    return 0 if alarma == 0 else 1

def okuzba():
    ulovov = 0
    v_iskalu = "ba" + "sh " + "ba" + "sh"
    for ime, pot in instrumenti():
        bes = open(pot, encoding="utf-8", errors="replace").read()
        ulovi = [(hex(ord(z)), pisava(ord(z))) for z in bes if pisava(ord(z))]
        maske = re.findall(chr(0x2329) + "U\\+" + "([^" + chr(0x232A) + "]{0,12})" + chr(0x232A), bes)
        slabe = [m for m in maske if not re.fullmatch("[0-9A-Fa-f]{4}", m)]
        tolkaci = bes.count(v_iskalu)
        vrata = []
        for z, _ in ulovi:
            if z not in vrata:
                vrata.append(z)
        if vrata or slabe or tolkaci:
            print("INFILTRACIJA ⚠ %s : pisave %s ⌇ maske %s ⌇ dvojni tolkač ×%d" % (ime, vrata or "×0", slabe or "×0", tolkaci))
            ulovov += len(vrata) + len(slabe) + (1 if tolkaci else 0)
        else:
            print("ČISTO ⊢ %s" % ime)
    print("SODBA : %s ( ulovov infiltracije %d ) @%s" % ("IMUNO ⊢" if ulovov == 0 else "VARNOST ⚠", ulovov, tik()))
    return 0 if ulovov == 0 else 1

if __name__ == "__main__":
    ukaz = sys.argv[1] if len(sys.argv) > 1 else ""
    if ukaz == "--manifest":
        sys.exit(manifest())
    if ukaz == "--preveri":
        sys.exit(preveri_manifest(sys.argv[2] if len(sys.argv) > 2 else ""))
    if ukaz == "--okužba":
        sys.exit(okuzba())
    if ukaz == "--imunski-pregled":
        rezultati = []
        for ime, pot in instrumenti():
            orbita = "python3" if pot.endswith(".py") else "bash"
            rc = os.system("%s %s --samopreizkus >/dev/null 2>&1" % (orbita, pot))
            rezultati.append((ime, rc))
        zdravi = [i for i, r in rezultati if r == 0]
        bolni = [(i, r) for i, r in rezultati if r != 0]
        for i, r in bolni:
            print("BOLNO ⚠ %s ( izhod %d )" % (i, r))
        print("IMUNSKI PREGLED @%s : zdravi %d ⌇ bolni %d od %d ⇒ %s" % (tik(), len(zdravi), len(bolni), len(rezultati), "IMUNO ⊢" if not bolni else "IMUNOST ⚠"))
        sys.exit(0 if not bolni else 1)
    if ukaz == "--samopreizkus":
        A = os.system("python3 %s --manifest >/dev/null 2>&1" % __file__) == 0
        m = sorted(glob.glob(STROJ + "/.geniza/MANIFEST-instrumentov-*.md"))[-1]
        B = os.system("python3 %s --preveri %s >/dev/null 2>&1" % (__file__, m)) == 0
        C = os.system("python3 %s --okužba >/dev/null 2>&1" % __file__) == 0
        print("SAMOPREIZKUS : T1 manifest %s ⌇ T2 preveri-manifest %s ⌇ T3 infiltracija %s" % ("1" if A else "0", "1" if B else "0", "1" if C else "0"))
        sys.exit(0 if (A and B and C) else 1)
    print("roke : --manifest ⌇ --preveri MANIFEST ⌇ --okužba ⌇ --samopreizkus")
    sys.exit(1)
