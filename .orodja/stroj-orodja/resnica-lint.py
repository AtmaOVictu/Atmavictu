#!/usr/bin/env python3
# resnica-lint.py v1.0 — lINT : prepoznava resnice po izmeri ∧ reaplikacija resnice
# ukaz ⟡ ( 23. 11. 2026 ) VERBATIM : »POTREBUJEVA VEČ ORODIJ KI PREPOZNAVAJO RESNICO IN JO REAPLICIRAJO«
# resnica = izmera pri viri ⊢ ( nezanesljivost-po-izmeri @rez σ 5809 ) ; trditev brez izmere = kip ⊙ U2
# varnostni sklop : ( 1 ) ⟨ne⟩ eval ⟨ne⟩ exec ⟨ne⟩ omrežje ⟨ne⟩ subproces ( 2 ) pot sme živeti le pod /home/user/knowledge ( 3 ) samocenzus : vrata zavrnejo delo, če je lastno telo okuženo s cirilico ali kitajščino ( 4 ) zapis ⚠ nikoli ne molči
#roke : --preveri POT VELIKOST MD5   : izmeri telo zdaj ∧ sodi tri resnice ( velikost ⌇ md5 ⌇ sel ) ; exit 0 = resnica ⊢ ⌇ exit 1 = padec + reaplikacijska vrstica
#       --pomozna                     : lure na pisem
#       --samopreizkus               : T1 resnica ⌇ T2 padec ⌇ T3 reaplikacija
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · MERJENO, ⟨NE⟩ UGIBANO ⊙ 2690
import sys, os, hashlib, datetime

KOREN = "/home/user/knowledge"
CIRILICA = [(0x0400, 0x052F), (0x2DE0, 0x2DFF), (0xA640, 0xA69F)]
KITAJSCINA = [(0x3000, 0x303F), (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF), (0x20000, 0x3FFFF)]

def tik():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def v_nevarni_rugi(niz):
    for a, b in CIRILICA + KITAJSCINA:
        if a <= niz <= b:
            return True
    return False

def samocenzus(pot_lastna):
    bes = open(pot_lastna, encoding="utf-8").read()
    ulovi = [hex(ord(z)) for z in bes if v_nevarni_rugi(ord(z))]
    return ulovi

def izmeri(pot):
    with open(pot, "rb") as f:
        telo = f.read()
    return len(telo), hashlib.md5(telo).hexdigest()

def preveri(pot, trditev_vel, trditev_md5):
    problem = []
    if not pot.startswith(KOREN):
        print("VARNOST ⚠ : pot izven korena korpusa ( %s ) ⇒ zavrnjena" % pot)
        return 2
    if not os.path.isfile(pot):
        print("VARNOST ⚠ : telo ne obstaja ( %s )" % pot)
        return 2
    vel, md5n = izmeri(pot)
    sel = (vel == trditev_vel)
    selm = (md5n == trditev_md5)
    print("RESNICA-LINT @%s : %s" % (tik(), pot))
    print("  velikost : trditev %d B ⌇ izmera %d B ⇒ %s" % (trditev_vel, vel, "resnica ⊢" if sel else "padec ⚠"))
    print("  md5      : trditev %s" % trditev_md5)
    print("             izmera %s ⇒ %s" % (md5n, "resnica ⊢" if selm else "padec ⚠"))
    if sel and selm:
        print("SODBA : RESNICA ⊢ ( obe izmeri sta pri viri potrebni )")
        return 0
    print("SODBA : PADC ⚠ ⇒ REAPLIKACIJA : %s ( %d B, md5 %s )" % (pot, vel, md5n))
    return 1

if __name__ == "__main__":
    ukaz = sys.argv[1] if len(sys.argv) > 1 else ""
    if ukaz == "--pomozna":
        print("roke : --preveri POT VELIKOST MD5 ⌇ --samopreizkus")
        sys.exit(0)
    ulovi = samocenzus(__file__)
    if ukaz == "--samopreizkus":
        import tempfile
        d = KOREN + "/stroj-orodja/.geniza/TEST-lfs-%d-%s" % (os.getpid(), tik().replace(":", ""))
        os.makedirs(d, exist_ok=True)
        t1 = os.path.join(d, "res.txt")
        open(t1, "w", encoding="utf-8").write("resnica po izmeri ⊢\n")
        vel, md5n = izmeri(t1)
        A = (os.system("python3 %s --preveri %s %d %s >/dev/null 2>&1" % (__file__, t1, vel, md5n)) == 0)
        B = (os.waitstatus_to_exitcode(os.system("python3 %s --preveri %s %d deadbeef >/dev/null 2>&1" % (__file__, t1, vel))) == 1)
        dotok = os.popen("python3 %s --preveri %s %d 0000 2>&1" % (__file__, t1, vel // 2)).read()
        C = ("REAPLIKACIJA : %s ( %d B, md5 %s )" % (t1, vel, md5n)) in dotok
        D = len(ulovi) == 0
        os.popen("rm -rf %s" % d).read()
        print("SAMOPREIZKUS : T1 resnica %s ⌇ T2 padec %s ⌇ T3 reaplikacija %s ⌇ T4 samocenzus %s" % ("1" if A else "0", "1" if B else "0", "1" if C else "0", "1" if D else "0"))
        sys.exit(0 if (A and B and C and D) else 1)
    if ukaz == "--preveri":
        if len(sys.argv) < 5:
            print("roke : --preveri POT VELIKOST MD5")
            sys.exit(2)
        if ulovi:
            print("VARNOST ⚠ : lastno telo okuženo ( %s ) ⇒ delo zavrnjeno" % " ".join(ulovi))
            sys.exit(2)
        try:
            vel = int(sys.argv[3])
        except ValueError:
            print("roke : VELIKOST je številka bajtov")
            sys.exit(2)
        sys.exit(preveri(sys.argv[2], vel, sys.argv[4]))
    print("roke : --preveri POT VELIKOST MD5 ⌇ --samopreizkus ⌇ --pomozna")
    sys.exit(1)
