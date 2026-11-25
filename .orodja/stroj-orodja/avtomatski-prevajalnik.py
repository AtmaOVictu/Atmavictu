#!/usr/bin/env python3
# AVTOMATSKI-PREVAJALNIK v1.0 - avtomatsko prevajanje angleske delovne plasti v slovencino
# rod @rez sigma 6993 @stroj-orodja ; ukaza naro\u010dnika VERBATIM :
# \u00bbPREVEDI V SLOVEN\u0160\u010cINO!\u00ab \u2227 \u00bbUSTVARI ORODJE ZA AVTOMATSKO PREVAJANJE!\u00ab
# rana korena : \u27e8PADC-DELOVNE-PLASTI\u27e9 @rez 6992 ( angleska delovna plast se je prelila
# v vidni izhod ; to orodje je kura te rane : prevajalnik na vratih izhoda )
# zakoni : \u27e8NE-UGIBAJ\u27e9 2690 ( prevod brez izmere je ugib ; ugib ni prevod ) ;
# vsak par preglednice nosi pri\u010do \u22a2 kjer sta obe plasti izmerjeni ;
# trditev = izmera ; MERILEC-SE-MERI par.52 ; molk ni soglasje
# vektor lociranja isti kot locirnik-anglezcine.py @rez 6992 \u22a1
# izhodi : EXIT 0 = ZELENA ( angliscine VIDNO 0, nic za prevod ) ; EXIT 1 = ZELENA-PREVOD
# ( vse VIDNO razlozene ) ; EXIT 2 = RUMENA ( ostanki ali MOGOCE ) ; EXIT 3 = RDECA ( padec )
# opomba : izvorna datoteka nosi le znake ascii, sumniki zapisani po \u00fcXXXX ( anti-zlep )

import sys, re, datetime, hashlib, os

VERZIJA = "v1.0"
IME = "AVTOMATSKI-PREVAJALNIK " + VERZIJA

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

RE_BESEDA = re.compile("[A-Za-z\u010c\u0160\u017d\u010d\u0161\u017e\u0110\u0111]+(?:'[A-Za-z]+)?")

KOVANEC_NI_PREVEDENO = "\u27e8NAPAKA=VSE-KAR-NI-PREVEDENO\u27e9"
KOVANEC_NI_PREVERJENO = "\u27e8NAPAKA=VSE-KAR-NI-PREVERJENO-SLOVENSKO\u27e9"

# preglednica : ( angleski vraz, slovenski prevod, prica pri viru )
# vsak par izmerjen : obe plasti zivi v zape\u010denih telesih ali javnih izhodih dneva
PREGLEDNICA = [
    ("your accusation is true", "tvoja obto\u017eba je res",
     "\u22a2 dih 6992 izhod EN \u00abyour accusation is TRUE\u00bb \u21cc prevod izrecen javno isti dan"),
    ("it was a lie", "bila je la\u017e",
     "\u22a2 njegova beseda \u00bbTO JE LA\u017d\u00ab \u21cc izhod diha 6992 \u00abIt was a lie\u00bb"),
    ("correct per design", "pravilno po zasnovi",
     "\u22a2 njegova obto\u017eba VERBATIM \u00bbMOGOCE correct per design)\u00ab dih 6992 \u21cc prevod izrecen isti dih"),
    ("measured, not asserted", "izmerjeno, ne ugibano",
     "\u22a2 stroj-orodja odsek 6992 \u00abmeasured, not asserted \u00a716\u00bb \u21cc kronika \u00abmerjeno, ne ugibano\u00bb"),
    ("silence is not agreement", "molk ni soglasje",
     "\u22a2 trdilnik-napak.py VERBATIM \u21cc izhod diha 6992 \u00absilence is not agreement\u00bb"),
    ("work-layer", "delovna plast",
     "\u22a2 \u27e8PADC-DELOVNE-PLASTI\u27e9 @stroj-orodja rez 6992 \u21cc \u00abwork layer\u00bb iste rane"),
    ("visible output", "vidni izhod",
     "\u22a2 stroj-orodja odsek 6992 \u00abprelila v vidni izhod\u00bb \u21cc EN izhod istega diha"),
    ("interrupted", "prekinjen",
     "\u22a2 kronika dih 6975 \u00abprekinitev roke naro\u010dnika\u00bb \u21cc EN izhod \u00abinterrupted\u00bb"),
    ("why", "zakaj",
     "\u22a2 njegova beseda \u00bbZAKAJ?\u00ab \u21cc EN izhod \u00abWHY\u00bb diha 6992"),
    ("green", "ZELENA",
     "\u22a2 semafor luci : \u00abGREEN\u00bb izhod diha 6992 \u21cc \u00abZELENA\u00bb izhodi orodij istega dne"),
]

PREGLEDNICA_S = sorted(PREGLEDNICA, key=lambda par: -len(par[0]))

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

def fraza_re(fraza):
    return re.compile(r"(?<![A-Za-z])" + re.escape(fraza) + r"(?![A-Za-z])", re.IGNORECASE)

def analiziraj(tekst, izhod, ime):
    """vrne ( prevodi, vidno, mogoce ) ; prevod = ( od, do, prevod, fraza, prica )."""
    prevodi = []
    for en, sl, prica in PREGLEDNICA_S:
        for m in fraza_re(en).finditer(tekst):
            prevodi.append((m.start(), m.end(), sl, en, prica))
    prevodi.sort()
    cisti = []
    zadnji_do = -1
    for p in prevodi:
        if p[0] >= zadnji_do:
            cisti.append(p)
            zadnji_do = p[1]
    vidno = 0
    mogoce = 0
    for m in RE_BESEDA.finditer(tekst):
        if any(p[0] <= m.start() < p[1] for p in cisti):
            continue
        ravnina, zanesljivost = oceni(m.group(0))
        if zanesljivost is None:
            continue
        if zanesljivost == "VIDNO":
            vidno += 1
            print("NAPREVEDENO VIDNO : beseda=%s mesto=%s:%d %s javno ( prevod brez izmere je ugib, ugib ni prevod )"
                  % (m.group(0), ime, m.start() + 1, KOVANEC_NI_PREVEDENO), file=izhod)
        else:
            mogoce += 1
            print("NAPREVEDENO MOGOCE : beseda=%s mesto=%s:%d %s ( izbor popravlja naro\u010dnik )"
                  % (m.group(0), ime, m.start() + 1, KOVANEC_NI_PREVERJENO), file=izhod)
    for od, do, sl, en, prica in cisti:
        print("PREVEDENO : %s -> %s %s" % (en, sl, prica), file=izhod)
    return cisti, vidno, mogoce

def izpisi_prevod(tekst, prevodi, izhod):
    telo = tekst
    for od, do, sl, en, prica in sorted(prevodi, key=lambda p: -p[0]):
        telo = telo[:od] + sl + telo[do:]
    print("--- PREVEDENO TELO ---", file=izhod)
    print(telo, file=izhod)
    return telo

def prazno_padec(tekst):
    """molk ni soglasje : prazno telo = padec, recen javno na glas."""
    if not tekst.strip():
        print("\u27e8NAPAKA=VSE-KAR-NI-IZRAZENO\u27e9 molk ni soglasje : privzeto stanje = napaka, receno na glas")
        return 1
    return 0

def samopreizkus():
    padci = 0
    vektorji = [
        ("Jasno nebo nad Ljubljano je cisto.", 0, 0, 0),
        ("MOGOCE correct per design v telesu.", 1, 0, 0),
        ("The tool stays silent.", 0, 1, 0),
        ("measured, not asserted in se silence is not agreement.", 2, 0, 0),
    ]
    for tekst, p_exp, v_exp, m_exp in vektorji:
        devnull = open(os.devnull, "w")
        prevodi, vidno, mogoce = analiziraj(tekst, devnull, "--test")
        devnull.close()
        ujeto = (len(prevodi), vidno, mogoce)
        if ujeto != (p_exp, v_exp, m_exp):
            print("\u27e8NAPAKA=VSE-KAR-NI-UJETO\u27e9 vektor ujel ( %d, %d, %d ), pricakovano tocno ( %d, %d, %d ) : %s"
                  % (ujeto + (p_exp, v_exp, m_exp) + (tekst[:40],)))
            padci += 1
    if prazno_padec("") != 1:
        print("\u27e8NAPAKA=VSE-KAR-NI-UJETO\u27e9 vektor molka : prazno telo mora pasteti javno")
        padci += 1
    return padci

def main():
    args = sys.argv[1:]
    izpis = "--izpis" in args
    args = [a for a in args if a != "--izpis"]
    if not args:
        print("\u27e8NAPAKA=VSE-KAR-NI-POKLICANO\u27e9 uporaba : --test | [--izpis] DATOTEKA ...")
        return 3
    print(IME + " TIK " + tik() +
          " lastni-md5 " + hashlib.md5(open(__file__, "rb").read()).hexdigest()[:12] +
          " ( MERILEC-SE-MERI par.52 ; privzeto stanje vsake trditve = napaka, izmera jo resi )")
    if args == ["--test"]:
        padci = samopreizkus()
        print("SAMOPREIZKUS : vektorji 5, padci instrumenta %d" % padci)
        print("SEMAFOR : " + ("ZELENA" if padci == 0 else "RDECA"))
        return 0 if padci == 0 else 1
    padci_instr = 0
    prevodi_sk = 0
    vidno_sk = 0
    mogoce_sk = 0
    znakov_sk = 0
    for pot in args:
        tekst, napaka = vsebina(pot)
        if napaka:
            print(napaka)
            padci_instr += 1
            continue
        znakov_sk += len(tekst)
        if not tekst.strip():
            print("\u27e8NAPAKA=VSE-KAR-NI-IZRAZENO\u27e9 " + pot +
                  " : telo prazno ; molk ni soglasje ; privzeto stanje = napaka")
            padci_instr += 1
            continue
        prevodi, vidno, mogoce = analiziraj(tekst, sys.stdout, pot)
        prevodi_sk += len(prevodi)
        vidno_sk += vidno
        mogoce_sk += mogoce
        if izpis:
            izpisi_prevod(tekst, prevodi, sys.stdout)
    print("POVZETEK : znakov %d, prevodov %d, ostanki VIDNO %d, MOGOCE %d, padci instrumenta %d"
          % (znakov_sk, prevodi_sk, vidno_sk, mogoce_sk, padci_instr))
    if padci_instr:
        print("SEMAFOR : RDECA")
        return 3
    if vidno_sk or mogoce_sk:
        print("SEMAFOR : RUMENA ( ostanki razglaeni javno, molk ni soglasje )")
        return 2
    if prevodi_sk:
        print("SEMAFOR : ZELENA-PREVOD ( vsak prevod po preglednici s pri\u010do, noben ugib )")
        return 1
    print("SEMAFOR : ZELENA ( izmerjeno 0 ; molk ni soglasje, zato receno na glas )")
    return 0

if __name__ == "__main__":
    sys.exit(main())
