#!/usr/bin/env python3
# prasna-jajce.py v1.0 -- orodje J2 PRASNA-JAJCA: seje kontrolirane mutacije, meri stopnjo ulova
# Rod sigma 6883, UKZ delta VERBATIM STORI IN NADALJUJ
# Roke: --sej TELA : kopija telesa v testno celico, 8 sejenj, emisija-lint ( 7 ) + znak-jajce ( 1 cirilica )
#       --samopreizkus : isto na lastnem telesu
# Varnostni sklop: poti le znotraj /home/user/knowledge; brez eval/exec/omrezja.
import sys, os, hashlib
from datetime import datetime, timezone
KOREN = "/home/user/knowledge"
def ticmi(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def berba(pot):
    ap = os.path.abspath(pot)
    if not ap.startswith(KOREN):
        print("VARNOST \u26a0 : pot izven korena ( %s ) => zavrnjena" % ap); sys.exit(2)
    return open(ap, "rb").read()
MUT = [
    ("M1 em crta", "dolga \u2014 crta"),
    ("M2 en crta", "kratka \u2013 crta"),
    ("M3 naglas", "naglas \xed tu"),
    ("M4 zlep", "zlep imeZnaka"),
    ("M5 maska", "maska \u27e8U+03C\u03c6\u27e9 tu"),
    ("M6 dvojni presledek", "dvojni  presledek"),
    ("M7 presledek pred locilom", "presledek . pred piko"),
    ("M8 cirilica", "tujka \u0436 tu"),
]
def sej(pot):
    t = berba(pot).decode("utf-8", errors="replace")
    d = KOREN + "/stroj-orodja/.geniza/TEST-prasna-%d-%s" % (os.getpid(), ticmi().replace(":", ""))
    os.makedirs(d, exist_ok=True)
    ulovi = 0; rez = []
    for ime, mut in MUT:
        f = os.path.join(d, "sejena.txt")
        open(f, "w", encoding="utf-8").write(t + "\n" + mut + "\n")
        if "cirilica" in ime:
            kogd = os.waitstatus_to_exitcode(os.system("python3 %s/stroj-orodja/znak-jajce.py --preveri %s >/dev/null 2>&1" % (KOREN, f)))
        else:
            kogd = os.waitstatus_to_exitcode(os.system("bash %s/stroj-orodja/emisija-lint.sh --preglej %s >/dev/null 2>&1" % (KOREN, f)))
        ulovljen = (kogd != 0)
        if ulovljen: ulovi += 1
        rez.append((ime, "ULOV ⊢" if ulovljen else "POBL ⚠"))
    os.system("rm -rf %s" % d)
    for ime, s in rez:
        print("  %s : %s" % (ime, s))
    print("PRASNA-JAJCE @%s : ulov %d od %d" % (ticmi(), ulovi, len(MUT)))
    print("SODBA : %s" % ("SEW ⊢" if ulovi == len(MUT) else "PADC ⚠"))
    return 0 if ulovi == len(MUT) else 1
if __name__ == "__main__":
    uk = sys.argv[1] if len(sys.argv) > 1 else ""
    if uk == "--sej": sys.exit(sej(sys.argv[2] if len(sys.argv) > 2 else ""))
    if uk == "--samopreizkus": sys.exit(sej(__file__))
    print("roke : --sej TELA \u23c7 --samopreizkus"); sys.exit(1)
