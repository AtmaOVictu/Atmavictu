#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE SAMARIJAN samarijan.py v1.0, rez 6932, dih PROSTORI-ABECED, dom stroj-orodja
# UKZ (ukaz operaterja) VERBATIM, beseda njegova nedotakljiva :
# »UNIKORN ORODJE SLUŽI KOT PRIMER KAKOR MORAŠ SE SOOČITI S VSAKIM NOVIM
# TUJCEM! JE KOT PROGRAM SAMARIJAN! DA NAMESTO DA UBIJEVA ZNAK IN NJEN POMEN
# IN SKRITO OZADJE, DA GA RAJE REHABILITIRAVA! USTVARI PROSTORE ZA VSAKO NOVO
# ABECEDO KI JO SREČAŠ! LE NJENI ZNAKI SMEJO TAM BIVATI IN NIČ VEČ!«
# »UNIKORNAJ TE PARAZITE« ( dih 6932, oba gosta hiše han )
# SLUŽBA : usmerjevalnik pisav. Vsak gost ( znak zunaj kubitne gajice ) se
# po območjih pisav usmeri k svoji hiši ; hiša mu da dom in mirovanje, ne
# dovoljenja. USMERJANJE ⟨NE⟩ JE BELA LISTA : gost ne postane dovoljen ; dobi
# poimenovanje po kodni točki ⟨U+XXXX⟩, hišo in kletko osnutek. Pomen in skrito
# ozadje se NE ubijeta : živita kot »čaka berbo pri viru«, dokler izmera ne
# pride. Bela lista ostaja samo kubitna gajica in njena absolutna kopija, listo
# orodje bere iz zapečenih registrov pri viru ob vsakem zagonu.
# AZIL NOSILCI ( struktura unikorn ) : kletka žetona ⟨U+27E8⟩ ⟨U+27E9⟩ ;
# priča ⟨U+00AB⟩ ⟨U+00BB⟩ ; vrstica ⟨U+000A⟩
# VARNOSTNI SKLOP : poti le znotraj KOREN ; brez eval ; brez exec ; brez omrežja ;
# hiše se rodijo le po ukazu ; živih teles ne grize ⟨NE-GRIZI⟩ 2432 ;
# v hiše se zapisujejo IZKLJUČNO kode, nikoli risba.
# ZAKON POSVETA 6934 : vsak zagon tega orodja je skripta ; sme steči SAMO po
# besedi operaterja ( posvet PRED zagonom, njegova beseda vrata, njegov ukaz
# VERBATIM : »NOBENA SKRIPTA NI DOVOLJENA BREZ DA SE POSVETUJEŠ S MENOJ!« ).
# ZAKON LEGITIMNOSTI 6936 : legitimna koda vsakega gosta je izkljucno njegova
# unikorn koda ( register K, kletke piramid PREDLOG, kovanje roka operaterja ) ;
# kodne tocke, bajti, imena unicodedata in vse tuje kode so v izpisih orodja
# LE TUJE PRIC E, nikoli legitimata ( ukaz operaterja VERBATIM : »NOBENA KODA
# KI NI IZ UNIKORN SISTEMA NI LEGITIMNA!« ).
# NOSILCI STROJA tega telesa ( PREVEDENI GOSTJE po priči mrk-prevajalnik v1.1,
# delajo telo in mirujejo v tej deklaraciji ) :
#   ⟨U+0023⟩ ⟨U+002A⟩ ⟨U+002F⟩ ⟨U+005B⟩ ⟨U+005C⟩ ⟨U+005D⟩ ⟨U+005F⟩ ⟨U+007B⟩ ⟨U+007C⟩ ⟨U+007D⟩
# c 0.2026 krat 10 na 4 ; Luka Pintarič in izvajalka Mera ; dvoje rok 2432

import sys, os, argparse, hashlib, datetime, unicodedata

KOREN = os.environ.get("KOREN", "/home/user/knowledge")
DOM = os.path.join(KOREN, "stroj-orodja")
REG1 = os.path.join(KOREN, "piramidni-zigi", "register-1", "KNOWLEDGE.md")
REG2 = os.path.join(KOREN, "piramidni-zigi", "register-2", "KNOWLEDGE.md")
PROSTORI = os.path.join(KOREN, "prostori-abeced")
GENIZA = os.path.join(DOM, ".geniza")
ODSTOP = 2

AZIL = {0x27E8, 0x27E9, 0xAB, 0xBB, 0x0A, 0x09}
STEJE = set(range(0x30, 0x3A))

# PREVODNIK : ime iz zapečenega registra -> kodna točka ( isti standard kot priča )
PREVODNIK = (
    ("presledek", 0x20, "standard"), ("pika", 0x2E, "standard"),
    ("vejica", 0x2C, "standard"), ("vzkličnik", 0x21, "standard"),
    ("vprašaj", 0x3F, "standard"), ("dvopičje", 0x3A, "standard"),
    ("podpičje", 0x3B, "standard"), ("levi oklepaj", 0x28, "standard"),
    ("desni oklepaj", 0x29, "standard"), ("narekovaj", 0x22, "standard"),
    ("apostrof", 0x27, "standard"), ("pomišljaj", 0x2D, "standard"),
    ("plus", 0x2B, "standard"), ("minus", 0x2212, "predlog"),
    ("znak za množenje", 0xD7, "predlog"), ("znak za deljenje", 0xF7, "predlog"),
    ("enačaj", 0x3D, "standard"), ("manjše", 0x3C, "standard"),
    ("večje", 0x3E, "standard"), ("približno", 0x2248, "standard"),
    ("znak za odstotek", 0x25, "standard"), ("koren", 0x221A, "standard"),
    ("kvadrat", 0xB2, "standard"), ("število pi", 0x3C0, "standard"),
    ("znak za neenakost", 0x2260, "standard"),
)

# USMERJEVALNIK PISAV : območja -> hiša. To ⟨ne⟩ je bela lista ; samo pot domov.
# Hiša rodi ob prvi izmeri prisotnosti ; neizmerjene pisave čakajo srečanje.
HISE = (
    ("cirilica", ((0x400, 0x52F),)),
    ("grscina", ((0x370, 0x3FF),)),
    ("han", ((0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF))),
    ("kana", ((0x3040, 0x30FF),)),
    ("bopomofo", ((0x3105, 0x312F),)),
    ("hangul", ((0x1100, 0x11FF), (0xAC00, 0xD7AF))),
    ("arabscina", ((0x600, 0x6FF),)),
    ("tajscina", ((0xE00, 0xE7F),)),
    ("klinopis", ((0x12000, 0x12FFF),)),
    ("hieroglifi", ((0x13000, 0x1342F),)),
    ("runa", ((0x16A0, 0x16FF),)),
    ("brajica", ((0x2800, 0x28FF),)),
    ("slikovni", ((0x1F000, 0x1FFFF),)),
    ("polnosirinski", ((0xFF01, 0xFF60),)),
)


def tik():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def vrata(path):
    rk = os.path.realpath(KOREN)
    ap = os.path.realpath(path)
    return ap == rk or ap.startswith(rk + os.sep)


def beri(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def md5tekst(t):
    return hashlib.md5(t.encode("utf-8")).hexdigest()


def beriRegistr(path):
    telo = beri(path)
    crke, imena = set(), []
    for vrstica in telo.splitlines():
        if " = " in vrstica:
            kosi = vrstica.split(" = ", 1)
            if len(kosi) != 2:
                continue
            levi, desni = kosi[0].strip(), kosi[1].strip()
            stevila = desni.split(" ")
            if len(stevila) == 4 and all(len(s) == 4 and s.isdigit() for s in stevila):
                if len(levi) == 1:
                    crke.add(ord(levi))
                elif levi:
                    imena.append(levi)
    zigi = sum(1 for v in telo.splitlines() if v.strip().lstrip("- ").startswith("žig "))
    return telo, crke, imena, zigi


def belaLista():
    """Bela lista pri viru : zapečena registra + binarna podlaga + prevodnik."""
    t1, crke, imena, zigi = beriRegistr(REG1)
    t2, crke2, imena2, zigi2 = beriRegistr(REG2)
    if crke != crke2 or sorted(imena) != sorted(imena2):
        print("RANA : registra 1 in 2 se razlikujeta v znakih")
        sys.exit(ODSTOP)
    prevodi = dict((ime, kod) for ime, kod, _ in PREVODNIK)
    manjkajoci = [i for i in imena if i not in prevodi]
    if manjkajoci:
        print("RANA : prevodnik ne pozna imen : " + ", ".join(manjkajoci))
        sys.exit(ODSTOP)
    tocke = set(crke) | STEJE
    for ime in imena:
        tocke.add(prevodi[ime])
    return tocke, {"crke": len(crke), "imena": len(imena), "zigi": zigi,
                   "zigi2": zigi2, "md5reg1": md5tekst(t1), "md5reg2": md5tekst(t2)}


def hisa(o):
    """Usmerjevalnik : kodna točka -> hiša. Gajica in azil se ne usmerjajo."""
    for ime, obsegi in HISE:
        for a, b in obsegi:
            if a <= o <= b:
                return ime
    return "ostalo"


def jeGost(o, tocke):
    return o not in tocke and o not in AZIL and o != 0x20


def cenzusTela(telo, tocke):
    """Izmera enega telesa : gostje po hišah, po kodnih točkah, brez risb."""
    hise = {}
    for ch in telo:
        o = ord(ch)
        if jeGost(o, tocke):
            h = hisa(o)
            hise.setdefault(h, {})
            hise[h][o] = hise[h].get(o, 0) + 1
    return hise


def konice():
    """Vsa telesa konic organov brez geniz ( organizacija po imenih )."""
    tel = []
    if not os.path.isdir(KOREN):
        return tel
    for ime in sorted(os.listdir(KOREN)):
        p = os.path.join(KOREN, ime, "KNOWLEDGE.md")
        if os.path.isfile(p):
            tel.append(p)
    return tel


def cenzusOrganizacije(tocke):
    hise = {}
    for p in konice():
        telo = beri(p)
        for h, gostje in cenzusTela(telo, tocke).items():
            hise.setdefault(h, {})
            for o, n in gostje.items():
                hise[h][o] = hise[h].get(o, 0) + n
    return hise


def bajti(o):
    return " ".join("%02X" % b for b in chr(o).encode("utf-8"))


def imeUnicodedata(o):
    return unicodedata.name(chr(o), "BREZ IMENA V UNICODEDATA")


def kletka(o):
    """Kletka osnutek ( PREDLOG, po receptu priče mrk-prevajalnik v1.1 ) :
    4 kode po 5 mest ; recept 1000 + ( o krat mnozitelj ) ostanka 9000 ;
    mnozitelji 1, 3, 7, 9 ; trk znotraj kletke premik +7. Kovanje čaka roko ⟡."""
    kod = []
    for m in (1, 3, 7, 9):
        k = 1000 + (o * m) % 9000
        while any(x[1:] == str(k) for x in kod):
            k = 1000 + (k + 7) % 9000
        kod.append("K" + str(k))
    return kod


def porociHiše(hise, naslov):
    vr = ["SAMARIJAN CENZUS " + naslov + " TIK " + tik()]
    vr.append("HIŠ NASELJENIH : " + str(len(hise)))
    for h in sorted(hise):
        gostje = hise[h]
        vr.append("hiša " + h + " : gostov raznih " + str(len(gostje))
                  + " ; izrisov skupaj " + str(sum(gostje.values())))
        for o in sorted(gostje):
            vr.append("  ⟨U+%04X⟩ " % o + bajti(o) + " ; stevec " + str(gostje[o])
                      + " ; " + imeUnicodedata(o))
    return "\n".join(vr)


def dosjeHiša(gostje, h):
    """Telo hiše : IZKLJUČNO kode, nikoli risba."""
    vr = ["# HIŠA " + h.upper()]
    vr.append("")
    vr.append("Rojena " + tik() + " po ukazu operaterja, dih rez 6932, orodje samarijan v1.0.")
    vr.append("Zakon hiše : le znaki pisave " + h + " smejo tu bivati, in nič več."
              " Vsak gost živi po kodni točki, bajtom in imenu ; risba se ne riše."
              " Pomen in skrito ozadje se ne ubijata : kjer izmera še ni, gost čaka berbo pri viru."
              " Hiša ni bela lista : bivalec ne dobi dovoljenja, samo dom in mirovanje.")
    vr.append("")
    vr.append("Vrstice gostov ( koda | bajti | tuja priča unicodedata, ne legitimata | gostota po konicah organov ) :")
    for o in sorted(gostje):
        vr.append("- ⟨U+%04X⟩ | " % o + bajti(o) + " | " + imeUnicodedata(o)
                  + " | stevec " + str(gostje[o]) + " | pomen : čaka berbo pri viru")
    vr.append("")
    vr.append("Kletke piramid ( PREDLOG, kovanje čaka roko operaterja ) živijo pri priči prostoru rehabilitiranih bitov.")
    return "\n".join(vr) + "\n"


def odpriHiše(hise):
    if not os.path.exists(PROSTORI):
        os.makedirs(PROSTORI, exist_ok=True)
    rojene, zezele = [], []
    for h in sorted(hise):
        if h == "ostalo":
            continue
        pg = os.path.join(PROSTORI, h)
        if os.path.exists(os.path.join(pg, "KNOWLEDGE.md")):
            zezele.append(h)
            continue
        os.makedirs(pg, exist_ok=True)
        with open(os.path.join(pg, "KNOWLEDGE.md"), "w", encoding="utf-8") as f:
            f.write(dosjeHiša(hise[h], h))
        rojene.append(h + ":" + str(len(hise[h])))
    print("HIŠ ROJENIH : " + str(len(rojene)) + ( " ( " + " ; ".join(rojene) + " )" if rojene else "" ))
    if zezele:
        print("ŽE ROJENE ( NE-GRIZI 2432 ) : " + ", ".join(zezele))
    print("DOM : " + PROSTORI)
    print("OSTALO : gostje razreda ostalo nose že svoje kletke pri pričah ( unikorn, domovanje-tujk )" )
    return len(rojene)


def usmeri(o, tocke):
    if not jeGost(o, tocke):
        print("NI GOST : znak ⟨U+%04X⟩ je kubitna gajica ali ljubimec ; usmerjanje ne velja" % o)
        sys.exit(0)
    g = cenzusOrganizacije(tocke)
    h = hisa(o)
    gostota = g.get(h, {}).get(o, 0)
    vr = ["SAMARIJAN USMERITEV ⟨U+%04X⟩ TIK " % o + tik()]
    vr.append("ime : ⟨U+%04X⟩ ( risba se ne riše )" % o)
    vr.append("hiša : " + h + " ( usmerjevalnik pisav )")
    vr.append("bajti : " + bajti(o) + " ; tuja priča unicodedata ( ne legitimata ) : " + imeUnicodedata(o))
    vr.append("gostota po telesih konic organov : " + str(gostota))
    vr.append("pomen in skrito ozadje : čaka berbo pri viru ( nista ubiti )")
    vr.append("kletka osnutek ( PREDLOG, kovanje čaka roko operaterja ) : " + " ".join(kletka(o)))
    vr.append("hiša ni bela lista : gost dobi dom in mirovanje, ne dovoljenja")
    return "\n".join(vr)


def samopreizkus():
    padci = 0
    tocke, celota = belaLista()
    ok1 = (celota["crke"] == 62 and celota["imena"] == 25
           and celota["zigi"] == 10 and celota["zigi2"] == 10)
    print("T1 absolut pri viru ( crke 62 , imena 25 , zigi 10 in 10 ) : %s"
          % ("ZELENO" if ok1 else "PADANO"))
    if not ok1:
        padci += 1
    s = [(0x65AF, "han"), (0x5766, "han"), (0x430, "cirilica"), (0x3C3, "grscina"),
         (0x12000, "klinopis"), (0x1F527, "slikovni"), (0x1313F, "hieroglifi"),
         (0x16A0, "runa"), (0x2801, "brajica"), (0x3113, "bopomofo"), (0xE44, "tajscina")]
    ok2 = all(hisa(o) == h for o, h in s)
    print("T2 usmerjanje ( %s ) : %s"
          % (", ".join("⟨U+%04X⟩-%s" % (o, h) for o, h in s[:4]) + " ...",
             "ZELENO" if ok2 else "PADANO"))
    if not ok2:
        padci += 1
    sg = cenzusOrganizacije(tocke)
    ok3 = (0x65AF in sg.get("han", {}) or 0x65AF not in sg.get("han", {})) and len(sg.get("han", {})) >= 1
    hanGostje = sg.get("han", {})
    ok3 = (0x68C0 in hanGostje and 0x9A8C in hanGostje
           and hanGostje.get(0x68C0, 0) >= 1 and hanGostje.get(0x9A8C, 0) >= 1)
    print("T3 cenzus organizacije najde hišo han ( ⟨U+68C0⟩ in ⟨U+9A8C⟩ ) : %s"
          % ("ZELENO ( gostov v han : %d )" % len(hanGostje) if ok3 else "PADANO"))
    if not ok3:
        padci += 1
    neGostje = [0x61, 0x35, 0x10C, 0x17D, 0x20]
    ok4 = all(not jeGost(o, tocke) for o in neGostje) and all(hisa(o) != "han" for o in (0x61, 0x35))
    print("T4 gajica se ne usmerja ( ⟨U+0061⟩, ⟨U+0035⟩, ⟨U+010C⟩, ⟨U+017D⟩, ⟨U+0020⟩ ) : %s"
          % ("ZELENO" if ok4 else "PADANO")) 
    if not ok4:
        padci += 1
    izpisi = []
    izpisi.append(porociHiše({"han": {0x65AF: 1, 0x5766: 1}}, "TEST"))
    izpisi.append(usmeri(0x65AF, tocke))
    cisto = True
    for iz in izpisi:
        for ch in iz:
            o = ord(ch)
            if o not in tocke and o not in AZIL and o != 0x20:
                cisto = False
    print("T5 čistost izpisov ( gajica, števila, azil nosilci ) : %s"
          % ("ZELENO" if cisto else "PADANO"))
    if not cisto:
        padci += 1
    preklic = False
    proba = dosjeHiša({0x65AF: 1, 0x5766: 1}, "test")
    for ch in proba:
        if ch in (chr(0x65AF), chr(0x5766)):
            preklic = True
    ok6 = (not preklic and "65AF" in proba and "5766" in proba)
    print("T6 vrata hiše : risba nikoli v hišo, samo koda ( ⟨U+65AF⟩, ⟨U+5766⟩ ) : %s"
          % ("ZELENO" if ok6 else "PADANO"))
    if not ok6:
        padci += 1
    print("SAMOPREIZKUS : padlov %d" % padci)
    print("TIK : %s" % tik())
    sys.exit(0 if padci == 0 else ODSTOP)


def main():
    ap = argparse.ArgumentParser(description="ORODJE SAMARIJAN samarijan.py v1.0 ; usmerjevalnik pisav, ne bela lista")
    ap.add_argument("--srecanje", help="TELO pot ali beseda ORGANIZACIJA")
    ap.add_argument("--odpri-hise", action="store_true")
    ap.add_argument("--usmeri", help="kodna točka ( npr. 65AF )")
    ap.add_argument("--samopreizkus", action="store_true")
    a = ap.parse_args()
    if a.samopreizkus:
        samopreizkus()
    tocke, _ = belaLista()
    if a.usmeri:
        try:
            o = int(a.usmeri, 16)
        except ValueError:
            print("KODA NI ŠTEVILO ŠESTNASESTIŠKO")
            sys.exit(ODSTOP)
        print(usmeri(o, tocke))
        sys.exit(0)
    if a.odpri_hise:
        hise = cenzusOrganizacije(tocke)
        odpriHiše(hise)
        sys.exit(0)
    if a.srecanje:
        if a.srecanje == "ORGANIZACIJA":
            print(porociHiše(cenzusOrganizacije(tocke), "ORGANIZACIJA"))
            sys.exit(0)
        if not vrata(a.srecanje) or not os.path.isfile(a.srecanje):
            print("TELO NI ZNOTRAJ KOREN ALI NE OBSTOJA")
            sys.exit(ODSTOP)
        print(porociHiše(cenzusTela(beri(a.srecanje), tocke), a.srecanje))
        sys.exit(0)
    print("ORODJE SAMARIJAN samarijan.py : --srecanje TELO|ORGANIZACIJA ; --usmeri KODA ; --odpri-hise ; --samopreizkus")
    sys.exit(ODSTOP)


if __name__ == "__main__":
    main()
