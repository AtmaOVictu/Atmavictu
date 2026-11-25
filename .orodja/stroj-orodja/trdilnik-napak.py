#!/usr/bin/env python3
# TRDILNIK-NAPAK v1.0 - orodje, ki vselej trdi napako ( dokaz breme trditve )
# rod @rez sigma 6991 @stroj-orodja ; ukaz naro\u010dnika VERBATIM :
# \u00bbORODJE KI VSELEJ TRDI NAPAKO JE NUJNOST!\u00ab
# BIT register-napak ( sodb #25 ) : vsak vir trdi napako, dokaz ga re\u0161i ;
# re\u0161itev napake = izmera ( \u27e8NAPAKA=VSE-KAR-NI-X\u27e9 kanon ; markers dokaza : TIK md5 \u00d7 )
# izhodi : EXIT 0 = vsaka trditev nosi izmero ( ZELENA ) ; EXIT 1 = vsaj ena brez ( RDECA ) ;

import sys, re, datetime, hashlib

VERZIJA = "v1.0"
IME = "TRDILNIK-NAPAK " + VERZIJA

DOKAZ = ("TIK", "md5", "sha256", "\u27e8NE-UGIBAJ\u27e9", "izmer", "grep", "wc", "stat", "exit")

def tik():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def trdim(napis, izhod):
    print("TRDIM javno : " + napis, file=izhod)

def preveri(ime, tekst, izhod):
    """vrne stevilo trditev brez dokaza ; vsako napako izrece NA GLAS."""
    brez = 0
    vrstice = [v for v in tekst.splitlines() if v.strip()]
    if not vrstice:
        trdim("\u27e8NAPAKA=VSE-KAR-NI-IZRAZENO\u27e9 " + ime +
              " : telo prazno, molk ni soglasje, privzeto stanje = napaka", izhod)
        return 1
    for v in vrstice:
        ima_dokaz = False
        for d in DOKAZ:
            if d in v:
                ima_dokaz = True
                break
        if not ima_dokaz:
            brez += 1
            trdim("\u27e8NAPAKA=VSE-KAR-NI-IZMERJENO\u27e9 " + ime + " : vrstica brez dokaza : "
                  + v.strip()[:80], izhod)
    if brez == 0:
        trdim("\u27e8NAPAKA=VSE-KAR-NI-IZRAZENO\u27e9 ni je : vsaka vrstica nosi izmero ( to je "
              + str(len(vrstice)) + " izmerjenih pri\u010d, molk bi bil napaka )", izhod)
    return brez

def samopreizkus(izhod):
    padci = 0
    v1 = preveri("--test-a", "Rezultat je dober, vse deluje.", izhod)
    if v1 != 1:
        print("\u27e8NAPAKA=VSE-KAR-NI-UJETO\u27e9 gola trditev mora pasteti", file=izhod)
        padci += 1
    v2 = preveri("--test-b", "TIK 2026-11-25T00:00:00Z izmerjeno grep \u00d7 0", izhod)
    if v2 != 0:
        print("\u27e8NAPAKA=VSE-KAR-NI-UGRABNJENO\u27e9 izmerjena vrstica mora zdrzati", file=izhod)
        padci += 1
    v3 = preveri("--test-c", "", izhod)
    if v3 != 1:
        print("\u27e8NAPAKA=VSE-KAR-NI-UJETO\u27e9 molk mora pasteti kot napaka", file=izhod)
        padci += 1
    return padci

def main():
    args = sys.argv[1:]
    print(IME + " TIK " + tik() +
          " lastni-md5 " + hashlib.md5(open(__file__, "rb").read()).hexdigest()[:12] +
          " ( MERILEC-SE-MERI par.52 ; privzeto stanje tega orodja = napaka, dokaz ga resi )")
    if args == ["--test"]:
        padci = samopreizkus(sys.stdout)
        print("SAMOPREIZKUS : vektorji 3, padci instrumenta %d" % padci)
        print("SEMAFOR : " + ("ZELENA" if padci == 0 else "RDECA"))
        return 0 if padci == 0 else 1
    if not args:
        print("\u27e8NAPAKA=VSE-KAR-NI-POKLICANO\u27e9 uporaba : --test | DATOTEKA ...")
        return 3
    brez_sk = 0
    for pot in args:
        try:
            with open(pot, encoding="utf-8", errors="replace") as f:
                tekst = f.read()
        except OSError as e:
            trdim("\u27e8NAPAKA=VSE-KAR-NI-BRANO\u27e9 " + pot + " : " + str(e), sys.stdout)
            brez_sk += 1
            continue
        brez_sk += preveri(pot, tekst, sys.stdout)
    print("POVZETEK : vrstic brez dokaza %d" % brez_sk)
    print("SEMAFOR : " + ("ZELENA ( vsaka trditev nosi izmero )" if brez_sk == 0 else "RDECA"))
    return 0 if brez_sk == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
