#!/usr/bin/env python3
# NASLOVNIK-PARI v1.0 - spomin prevedenih naslovov : pari izvirnik <=> prevod, append-only.
# Rod : rez sigma 7014 ( 25. 11. 2026 ) @stroj-orodja ; ukaz naro\u010dnika VERBATIM, beseda nedotakljiva :
#   "ORODJA ZA PREVAJANJE NASLOVOV V SLOVEN\u0160\u010cINO!"
# Sestra : naslovnik.py v1.0 isti rez isti dih ( sodba prevoda ) ; to telo je SPOMIN parov :
#   naslov, enkrat preveden in zape\u010den, se nikoli ve\u010d ne ugiba \u27e8NE-UGIBAJ\u27e9 2690.
# Register : naslovnik-pari.tsv @stroj-orodja, stolpci TIK \u23e7 IZVIRNIK \u23e7 PREVOD \u23e7 VIR \u23e7 PREVAJALEC,
#   append-only \u27e8NE-BRI\u0160I\u27e9 24 ; duplikat popolnoma isti = idempotent \u27e8EN-RAZLI\u010cICA\u27e9 ;
#   isti izvirnik z druga\u010dnim prevodom = spor \u23ad sodba \u27e8NE-ODLO\u010cAJ-NAMESTO-\u27e8?\u27e9\u27e9 ;
#   isti prevod dvema izvirnikoma = trk slovenskega naslova ( javno, brez \u0161iva ).
# Roke :
#   naslovnik-pari.py --dodaj IZVIRNIK PREVOD VIR [PREVAJALEC]   -> ZELENA app / idempotent / spor
#   naslovnik-pari.py --isci IZVIRNIK                            -> najde par ( prej kovan prevod \u22a2 )
#   naslovnik-pari.py --obratno PREVOD                           -> obratno iskanje
#   naslovnik-pari.py --stat                                     -> pari N, velikost, md5 \u22a2
#   naslovnik-pari.py --test                                     -> samopreizkus vektorjev \u00d75 ( \u00a752 )
# Izhodi : 0=ZELENA \u2227 1=NI-JE \u2227 2=TRK-PREVODA \u2227 3=SPOR-PREVODA \u2227 4=roka neznana.

import sys, os, hashlib, datetime as _dt

DOM = os.path.dirname(os.path.abspath(__file__))
PARI = os.environ.get("NASLOVNIK_PARI", os.path.join(DOM, "naslovnik-pari.tsv"))
VERZIJA = "v1.0"

def vedno_obstaja():
    if not os.path.exists(PARI):
        with open(PARI, "w", encoding="utf-8") as f:
            f.write("")

def pari():
    vedno_obstaja()
    with open(PARI, encoding="utf-8") as f:
        vrstice = [r.rstrip("\n").split("\t") for r in f if r.strip()]
    return [v for v in vrstice if len(v) == 5]

def md5_registra():
    vedno_obstaja()
    with open(PARI, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def tik():
    return _dt.dt_now if False else _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

def cisto(polje):
    return "\t" not in polje and "\n" not in polje and polje.strip() != ""

def dodaj(izvirnik, prevod, vir, prevajalec):
    for ime, v in (("izvirnik", izvirnik), ("prevod", prevod), ("vir", vir), ("prevajalec", prevajalec)):
        if not cisto(v):
            print("RDECA : " + ime + " nosi tab/novo vrstico ali praznino ( \u27e8NE-GRIZI\u27e9 2432 )")
            return 1
    stari = pari()
    for t, i, p, v, pr in stari:
        if i == izvirnik and p == prevod:
            print("ZELENA idempotent : par obstaja \u22a2 ( TIK " + t + " ; pri\u010da " + v + " ) \u27e8EN-RAZLI\u010cICA\u27e9")
            return 0
        if i == izvirnik and p != prevod:
            print("SPOR-PREVODA : izvirnik »" + i + "« \u017ee \u017eivi z druga\u010dnim prevodom »" + p +
                  "« ( TIK " + t + " ) \u23ad nada v roko \u2694 ; NIHIL brez \u0161iva")
            return 3
        if p == prevod and i != izvirnik:
            print("TRK-PREVODA : slovenski naslov »" + prevod + "« \u017ee \u017eivi z izvirnikom »" + i +
                  "« ( TIK " + t + " ) ; NIHIL, javno")
            return 2
    vedno_obstaja()
    with open(PARI, "a", encoding="utf-8") as f:
        f.write("\t".join((tik(), izvirnik, prevod, vir, prevajalec)) + "\n")
    n = len(pari())
    print("ZELENA app : par polo\u017een ; TIK " + tik() + " ; pari " + str(n) + " ; md5 " + md5_registra()[:12] + " \u22a2")
    return 0

def isci(izvirnik, polje_izv=1, polje_prev=2):
    for t, i, p, v, pr in pari():
        if (polje_izv == 1 and i == izvirnik) or (polje_izv == 2 and p == izvirnik):
            drugi = p if polje_izv == 1 else i
            print("NAJDEN \u22a2 : " + ("izvirnik »" + i + "« \u21c4 prevod »" + p + "«") +
                  " ; pri\u010da " + v + " ; TIK " + t + " ; prevajalec " + pr)
            return 0
    print("NI-JE \u22a2 : »" + izvirnik + "« nima para ( pobuda prevoda ; prej preveden naslov se ne ugiba znova," )
    print("         nepreveden pa \u010daka roko \u27e8PREVAJALEC-POIMENOVAN\u27e9 \u27e8NE-UGIBAJ\u27e9 2690 )")
    return 1

def stat():
    vedno_obstaja()
    n = len(pari())
    b = os.path.getsize(PARI)
    print("STAT \u22a2 : pari " + str(n) + " ; telo " + str(b) + " B ; md5 " + md5_registra() + " ; pot " + PARI)
    return 0

def samopreizkus():
    import tempfile
    td = tempfile.mkdtemp(prefix="TEST-pari-", dir=os.path.join(DOM, ".geniza"))
    reg = os.path.join(td, "p.tsv")
    os.environ["NASLOVNIK_PARI"] = reg
    global PARI
    PARI = reg
    T = [0, 0, 0, 0, 0]
    T[0] = 1 if dodaj("On Love", "Ljub\u00e9zen", "v1", "izvajalka Mera") == 0 else 0
    T[1] = 1 if isci("On Love") == 0 else 0
    T[2] = 1 if dodaj("On Love", "Ljub\u00e9zen", "v1", "izvajalka Mera") == 0 and len(pari()) == 1 else 0
    T[3] = 1 if dodaj("On Love", "Drugi prevod", "v1", "izvajalka Mera") == 3 and len(pari()) == 1 else 0
    T[4] = 1 if isci("Ljub\u00e9zen", 2, 1) == 0 else 0
    n = len(pari())
    import shutil
    shutil.rmtree(td, ignore_errors=True)
    p = 5 - sum(T)
    print("SAMOPREIZKUS : vektorji 5 ( app=" + str(T[0]) + " isci=" + str(T[1]) + " idempotent=" + str(T[2]) +
          " spor=" + str(T[3]) + " obratno=" + str(T[4]) + " ), pari-ostanek " + str(n) +
          ", padci instrumenta " + str(p))
    print("SEMAFOR : " + ("ZELENA" if p == 0 else "RDECA"))
    return 0 if p == 0 else 1

def main(argv):
    a = argv[1:]
    if not a:
        print("roka neznana ; roke : --dodaj | --isci | --obratno | --stat | --test")
        return 4
    if a[0] == "--test":
        return samopreizkus()
    if a[0] == "--stat":
        return stat()
    if a[0] == "--isci" and len(a) == 2:
        return isci(a[1], 1, 2)
    if a[0] == "--obratno" and len(a) == 2:
        return isci(a[1], 2, 1)
    if a[0] == "--dodaj" and len(a) in (4, 5):
        return dodaj(a[1], a[2], a[3], a[4] if len(a) == 5 else "izvajalka Mera")
    print("roka neznana ; roke : --dodaj | --isci | --obratno | --stat | --test")
    return 4

if __name__ == "__main__":
    sys.exit(main(sys.argv))
