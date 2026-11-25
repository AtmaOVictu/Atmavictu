#!/usr/bin/env python3
# LOVC-EV-ANGLESCINE ( locirnik-anglezcine ) v1.0 - lociranje angle\u0161kih besed od slovenskih
# rod @rez sigma 6991 @stroj-orodja ; ukaz naro\u010dnika VERBATIM :
# \u00bbLOCIRANJE ANGLESKIH BESED OD SLOVENSKIH!\u00ab in \u00bbUSTVARI TEMU PRIMERNA ORODJA!\u00ab
# zakoni : NE-UGIBAJ 2690 ; trditev=izmera ; MERILEC-SE-MERI par.52 ; kanon register-napak
# izhodi : EXIT 0 = najdenih 0 ; EXIT 1 = VIDNO vsaj 1 ; EXIT 2 = le MOGOCE ; EXIT 3 = padec instrumenta
# opomba : izvorna datoteka nosi le znake ascii, sumniki zapisani po \u00fcXXXX ( anti-zlep vrata )

import sys, re, datetime, hashlib, os

VERZIJA = "v1.0"
IME = "LOCIRNIK-ANGLEZCINE " + VERZIJA

SLOVENSKI = set("""
a o i on do pri za od na po v s k ki da se je bil si smo so bili bi ne tu tam zdaj sedaj test
to same more no pa ta ti le ga mid in most
""".split())

GOSTI = set("""
internet internetu internetna software hardware timeout server hosting online download quiz
""".split())

R1 = set("""
the and of to in that this these those with without from by as at into onto over under
about after between during through against was were been being am are is
has had have having does did done doing will would could should can cannot may might must
shall not no yes what which who whom whose when where why how all any both each few more
most other some such only own same than too very just also then once here there
get got make made take taken go went come came see saw seen know knew think thought
say said tell told find found give gave given work worked use used try tried need needed
""".split())

R2_KONCETA = ("ing", "tion", "sion", "ment", "ness", "ally")
R2_DVOJICE = ("th", "wh", "gh", "ck", "sh")
R2_CRKE = ("q", "w", "x")

RE_BESEDA = re.compile("[A-Za-z\\u010c\\u0160\\u017d\\u010d\\u0161\\u017e\\u0110\\u0111]+(?:'[A-Za-z]+)?")

KOVANEC_VIDNO = "\u27e8NAPAKA=VSE-KAR-NI-SLOVENSKO\u27e9"
KOVANEC_MOGOCE = "\u27e8NAPAKA=VSE-KAR-NI-PREVERJENO-SLOVENSKO\u27e9"

def tik():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def vsebina(pot):
    try:
        with open(pot, encoding="utf-8", errors="replace") as f:
            return f.read(), None
    except OSError as e:
        return None, "\u27e8NAPAKA=VSE-KAR-NI-BRANO\u27e9 " + pot + " : " + str(e)

def oceni(beseda):
    niz = beseda.strip("'").lower()
    if niz in SLOVENSKI or niz in GOSTI:
        return None, None
    if niz in R1:
        return 1, "VIDNO"
    for k in R2_KONCETA:
        if len(niz) >= 5 and niz.endswith(k):
            return 2, "MOGOCE"
    for d in R2_DVOJICE:
        if d in niz and len(niz) >= 3:
            return 2, "MOGOCE"
    for c in R2_CRKE:
        if c in niz and len(niz) >= 2:
            return 2, "MOGOCE"
    return None, None

def lociraj(pot, tekst, izhod):
    znakov = len(tekst)
    vidno = 0
    mogoce = 0
    for vrstica in tekst.splitlines():
        for m in RE_BESEDA.finditer(vrstica):
            beseda = m.group(0)
            ravnina, zanesljivost = oceni(beseda)
            if zanesljivost is None:
                continue
            stolpec = m.start() + 1
            kontekst = vrstica[max(0, m.start() - 20):m.end() + 20].strip()
            if zanesljivost == "VIDNO":
                kovanec = KOVANEC_VIDNO
                vidno += 1
            else:
                kovanec = KOVANEC_MOGOCE
                mogoce += 1
            print("LOCIRANO %s : beseda=%s ravnina=%d mesto=%s:%d kontekst=...%s..."
                  % (zanesljivost, beseda, ravnina, pot, stolpec, kontekst), file=izhod)
            print("TRDIM javno : " + kovanec + " ( izbor popravila njegov )", file=izhod)
    return znakov, vidno, mogoce

def samopreizkus():
    padci = 0
    vektorji = [
        ("Jasno nebo nad Ljubljano je cisto in mirno.", 0),
        ("To je test of the tool, jasno nebo se vidi clear.", 2),
        ("The quick brown fox jumps over the lazy dog.", 3),
        ("Internet hosting je strezba na gosti licenci.", 0),
    ]
    vsota = 0
    for tekst, pricakovano in vektorji:
        devnull = open(os.devnull, "w")
        zn, vidno, mogoce = lociraj("--test", tekst, devnull)
        devnull.close()
        vsota += vidno
        if vidno != pricakovano:
            print("\u27e8NAPAKA=VSE-KAR-NI-UJETO\u27e9 vektor ujel %d, pricakovano tocno %d : %s"
                  % (vidno, pricakovano, tekst[:40]))
            padci += 1
    return padci, vsota

def main():
    args = sys.argv[1:]
    if not args:
        print("\u27e8NAPAKA=VSE-KAR-NI-POKLICANO\u27e9 uporaba : --test | DATOTEKA ...")
        return 3
    print(IME + " TIK " + tik() +
          " lastni-md5 " + hashlib.md5(open(__file__, "rb").read()).hexdigest()[:12] +
          " ( MERILEC-SE-MERI par.52 )")
    if args == ["--test"]:
        padci, ujetih = samopreizkus()
        print("SAMOPREIZKUS : vektorji 4, ujetih skupaj %d, padci instrumenta %d" % (ujetih, padci))
        print("SEMAFOR : " + ("ZELENA" if padci == 0 else "RDECA"))
        return 0 if padci == 0 else 1
    padci_instr = 0
    vidno_sk = 0
    mogoce_sk = 0
    znakov_sk = 0
    for pot in args:
        tekst, napaka = vsebina(pot)
        if napaka:
            print(napaka)
            padci_instr += 1
            continue
        zn, vidno, mogoce = lociraj(pot, tekst, sys.stdout)
        znakov_sk += zn
        vidno_sk += vidno
        mogoce_sk += mogoce
    print("POVZETEK : znakov %d, VIDNO %d, MOGOCE %d, padci instrumenta %d"
          % (znakov_sk, vidno_sk, mogoce_sk, padci_instr))
    if padci_instr:
        print("SEMAFOR : RDECA")
        return 3
    if vidno_sk:
        print("SEMAFOR : RUMENA")
        return 1
    if mogoce_sk:
        print("SEMAFOR : RUMENA")
        return 2
    print("SEMAFOR : ZELENA ( izmerjeno 0 ; molk ni soglasje, zato receno na glas )")
    return 0

if __name__ == "__main__":
    sys.exit(main())
