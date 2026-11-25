"""ORODJE MRK mrk-prevajalnik v1.4 rez 6939 ( osnova azilnih nosilcev : poroci steje azilne nosilce javno ; ukaz operaterja : vsak ki trdi azil mora imeti novo kodificirano osnovo ), prejsnja v1.3 rez 6935 ( preroditev ⟨U+0023⟩ : ni nosilec stroja, temveč parazit po sodbi operaterja ), dih MRK-PREVAJALNIK, dom stroj-orodja
UKZ (ukaz operaterja) VERBATIM, beseda njegova nedotakljiva :
»naredi MRK« in »vse kar ni iz kubitne gajice je sovražnik ki zahteva
REHABILITACIJO V NOV JEZIK IN STRUKTURO UNIKORN SISTEMA!«
»KARKOLI KAR ZAHTEVA WHITE LIST JE PARAZIT! EDINI DOVOLJEN WHITE LIST JE
KUBIT GAJICA IN NJENA ABSOLUTNA KOPIJA NA GITHUBU! KARKOLI KAR SKUŠA SEBE
WHITELISTAT MORA PRVO BITI PREVEDENO SKOZI UNIKORN SISTEM!«
SLUŽBA : vsak znak zunaj kubitne gajice je SOVRAŽNIK ; orodje ga poimenuje
izključno po kodni točki ⟨U+XXXX⟩, mu skuje kletko unikorn (PREDLOG, roka
operaterja), napise osnutek dosjeja 16 polj in preveri mirovanje
(moc 0, izvedba 0). Orodje lastne bele liste ne nosi : listo bere iz
zapečenih registrov pri viru ob vsakem zagonu po zakonu ⟨SAMO-KUBIT-LISTA⟩
po zakonu merjeno, ne ugibano 2690.
AZIL NOSILCI ( struktura unikorn po kubit-zapor 6922 ; domovanje-tujk po sodbi operaterja ) :
  kletka žetona ⟨U+27E8⟩ ⟨U+27E9⟩ ; priča ⟨U+00AB⟩ ⟨U+00BB⟩ ; vrstica ⟨U+000A⟩
NOSILCI STROJA tega telesa (PREVEDENO SKOZI UNIKORN : gostje brez moči) :
  ⟨U+002A⟩ ⟨U+002F⟩ ⟨U+005B⟩ ⟨U+005C⟩ ⟨U+005D⟩ ⟨U+005F⟩ ⟨U+007B⟩ ⟨U+007C⟩ ⟨U+007D⟩
OSNOVA AZILNIH NOSILCEV ( v1.4 dih 6939 ; ukaz operaterja : vsak ki trdi azil mora imeti novo kodificirano osnovo ) :
  azilna nosilca ⟨U+27E8⟩ ⟨U+27E9⟩ rojena kot gostja unikorn ( K2216 K4648 K9512 K2944 ; K2217 K4651 K9519 K2953 ) ;
  kovanec ⟨U+00D7⟩ odtežen v gajico besede, rojen kot gost ( K1215 K1645 K2505 K2935 ) ;
  poroci vsakega azilnega nosilca steje javno ; merilec svojih azilcev več ne skriva
PRERODITEV ⟨U+0023⟩ ( dih 6935 ) : po sodbi operaterja ni nosilec stroja, temveč parazit ;
  rojen kot gost unikorn, piramide K1035 K1105 K1245 K1315 ; v tem telesu na nič.
PREVODNIK : ime iz zapečenega registra v kodno točko ; standard univerzalna postavitev tipkovnic ; predlogi operaterja.
VARNOSTNI SKLOP : poti le znotraj KOREN ; brez eval ; brez exec ; brez omrežja ;
  živih organov ne grize ⟨NE-GRIZI⟩ 2432 ; rojstva ODIH v mapi dneva dnevne-genize ( geniza nima pravice rodit ).
c 0.2026 krat 10 na 4 ; Luka Pintarič in izvajalka Mera ; dvoje rok 2432
"""

import sys, os, argparse, hashlib, datetime, unicodedata

KOREN = os.environ.get("KOREN", "/home/user/knowledge")
DOM = os.path.join(KOREN, "stroj-orodja")
REG1 = os.path.join(KOREN, "piramidni-zigi", "register-1", "KNOWLEDGE.md")
REG2 = os.path.join(KOREN, "piramidni-zigi", "register-2", "KNOWLEDGE.md")
UNIKORNT = os.path.join(KOREN, "unikorn", "KNOWLEDGE.md")
DAN = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
GENIZA = os.path.join(KOREN, "dnevne-genize", DAN)
POPIS = os.path.join(GENIZA, "POPIS-DNEVA.md")
CELICE = os.path.join(GENIZA, "mrk-celice")
ODSTOP = 2

NOSILCI_TELA = {0x2A, 0x2F, 0x5B, 0x5C, 0x5D, 0x5F, 0x7B, 0x7C, 0x7D}

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

AZIL = {0x27E8, 0x27E9, 0xAB, 0xBB, 0x0A, 0x09}
STEJE = set(range(0x30, 0x3A))
STROJNE_PONE = {"py", "sh", "json", "yml", "tsv", "ts", "js", "awk"}


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
    manjkajoci = []
    tocke = set(crke) | STEJE
    decoding = {}
    for ime in imena:
        if ime not in prevodi:
            manjkajoci.append(ime)
        else:
            decoding[ime] = prevodi[ime]
            tocke.add(prevodi[ime])
    if manjkajoci:
        print("RANA : prevodnik ne pozna imen : " + ", ".join(manjkajoci))
        sys.exit(ODSTOP)
    celota = {"crke": len(crke), "imena": len(imena), "zigi": zigi,
              "zigi2": zigi2, "toccke": len(tocke),
              "predlogi": sum(1 for _, _, fl in PREVODNIK if fl == "predlog"),
              "md5reg1": md5tekst(t1), "md5reg2": md5tekst(t2),
              "decoding": decoding}
    return tocke, decoding, celota


def razred(ch, o):
    if o in (0x2014, 0x2015):
        return "dolga crtica"
    if 0x0400 <= o <= 0x052F:
        return "cirilica"
    if 0x0300 <= o <= 0x036F:
        return "sestavljeni naglas"
    if 0x0370 <= o <= 0x03FF:
        return "grski"
    if (0x3400 <= o <= 0x4DBF) or (0x4E00 <= o <= 0x9FFF) or (0xF900 <= o <= 0xFAFF):
        return "han"
    if 0x3040 <= o <= 0x30FF:
        return "kana"
    if 0x3105 <= o <= 0x312F:
        return "zhuyin"
    if 0x2FF0 <= o <= 0x2FF2:
        return "ideografska sestava"
    if (0x1100 <= o <= 0x11FF) or (0xAC00 <= o <= 0xD7AF):
        return "hangul"
    if 0x0600 <= o <= 0x06FF:
        return "arabski"
    if 0x0E00 <= o <= 0x0E7F:
        return "tajski"
    if 0xFF01 <= o <= 0xFF60:
        return "polnosirinski"
    if o == 0xFFFD:
        return "nadomestilni"
    if o >= 0x1F000:
        return "slikovni"
    k = unicodedata.category(ch)
    if k == "Cf":
        return "formatni"
    if k in ("Mn", "Mc", "Me"):
        return "kombinacijski"
    if k == "Cc":
        return "kontrolni"
    if k in ("Co", "Cs"):
        return "zasebni"
    if k in ("Sm", "So", "Sc", "Sk"):
        return "simbol"
    return "znak zunaj nabora"


def kletka(o):
    """Kletka unikorn : PREDLOG, 4 kode po 4 stevilke, vse unikatne.
    Recept : koda i = 1000 + ( o krat mnozitelj i ) ostanka 9000 ;
    mnozitelji 1, 3, 7, 9 ; pri trku znotraj kletke premik +7.
    Kovani kod rodi izkljucno roka operaterja ; trki se merijo proti unikorn."""
    kod = []
    for m in (1, 3, 7, 9):
        k = 1000 + (o * m) % 9000
        while any(x[1:] == str(k) for x in kod):
            k = 1000 + (k + 7) % 9000
        kod.append("K" + str(k))
    return kod


def obstojeciKod():
    telo = beri(UNIKORNT)
    kod = set()
    for v in telo.splitlines():
        for beseda in v.split():
            if len(beseda) == 5 and beseda.startswith("K") and beseda[1:].isdigit():
                kod.add(beseda)
    return kod


def jeStrojno(path):
    return os.path.splitext(path)[1].lstrip(".").lower() in STROJNE_PONE


def cenzusTela(telo, tocke, strojno):
    """Izmera : vsak znak ; goli znak zunaj azila = SOVRAZNIK ; azilni nosilci stejejo javno."""
    sovraz, imen, nos, azil = {}, {}, {}, {}
    kletkaOdprta = False
    pricaOdprta = False
    vrstica = 1
    for ch in telo:
        o = ord(ch)
        if o == 0x0A:
            vrstica += 1
        if o in AZIL:
            if o == 0x27E8:
                kletkaOdprta = True
            elif o == 0x27E9:
                kletkaOdprta = False
            elif o == 0xBB:
                pricaOdprta = True
            elif o == 0xAB:
                pricaOdprta = False
            if o in (0x27E8, 0x27E9, 0xAB, 0xBB):
                azil[o] = azil.get(o, 0) + 1
            continue
        if o in tocke or o in STEJE or o == 0x20:
            continue
        if kletkaOdprta or pricaOdprta:
            imen[o] = imen.get(o, 0) + 1
            continue
        if strojno and 0x20 <= o < 0x7F:
            nos[o] = nos.get(o, 0) + 1
        else:
            st, prva = sovraz.get(o, (0, vrstica))
            sovraz[o] = (st + 1, prva)
    return sovraz, imen, nos, azil


def cenzus(path, tocke):
    telo = beri(path)
    return telo, cenzusTela(telo, tocke, jeStrojno(path))


def poroci(sovraz, imen, nos, azil, path):
    vrstice = ["MRK CENZUS " + path + " TIK " + tik()]
    vrstice.append("SOVRAZNIKOV RAZNOVRSNIH : " + str(len(sovraz)))
    for o in sorted(sovraz):
        st, prva = sovraz[o]
        vrstice.append("SOVRAZNIK ⟨U+%04X⟩ razred : %s ; stevec : %d ; prva vrstica : %d" % (o, razred(chr(o), o), st, prva))
    vrstice.append("GOSTOV IMENOVANIH V AZILU : " + str(len(imen)))
    vrstice.append("AZILNIH NOSILCEV (GOSTJE AZILNE SLUZBE, STEJNI JAVNO) : " + str(sum(azil.values())))
    for o in sorted(azil):
        vrstice.append("AZILNI NOSILEC ⟨U+%04X⟩ stevec : %d" % (o, azil[o]))
    vrstice.append("NOSILCEV STROJA (PREVEDENI GOSTJE) : " + str(len(nos)))
    for o in sorted(nos):
        vrstice.append("NOSILEC ⟨U+%04X⟩ stevec : %d" % (o, nos[o]))
    return "\n".join(vrstice)


def dosje(o, stevec, prva, path, obst):
    kod = kletka(o)
    trki = [k for k in kod if k in obst]
    vrstice = [
        "ime : ⟨U+%04X⟩" % o,
        "razred : " + razred(chr(o), o),
        ("razlog vpisa : gol znak zunaj azila pri viru ( %s , vrstica %d , stevec %d )" % (path, prva, stevec)),
        "nasprotje : PREDLOG operaterja ( par po osi razreda )",
        "kategorija : gost, ki terji azil",
        "matematicna funkcija : brez lastne enote ; razmerje do nosilca",
        "ontomatematika : identiteta le po kodni tocki ; moc 0",
        "zeton : %04X , DEAKTIVIRAN" % o,
        "dom : osnutek celice v mapi dneva ; rojstni dom unikorn SAMO beseda operaterja",
        "pot : ukaz operaterja diha 6931 ( MRK ) ; prevod skozi unikorn",
        "izgovorjava : brez glasu v zapisu ; po razredu bloka",
        "moc : samo opisana ; izvedba 0",
        "nemoc : brez azila ne stopi na povrsje",
        ("kletka : %s ( PREDLOG operaterja ; trki z registrom unikorn : %d )" % (" ".join(kod), len(trki))),
        "uporabnost : imenovanje ⟨U+XXXX⟩ izkljucno ; priča v »« ; risba 0",
        "price : ukaz operaterja VERBATIM ( MRK dih 6931 )",
        "testi : sest testov mirovanja ; moc 0 ; izvedba 0 ; MIROVANJE",
    ]
    return "\n".join(vrstice)


def preliv(telo, tocke):
    levo, desno = chr(0x27E8), chr(0x27E9)
    nov = []
    kletkaOdprta = False
    pricaOdprta = False
    for ch in telo:
        o = ord(ch)
        if o in AZIL:
            if o == 0x27E8:
                kletkaOdprta = True
            elif o == 0x27E9:
                kletkaOdprta = False
            elif o == 0xBB:
                pricaOdprta = True
            elif o == 0xAB:
                pricaOdprta = False
            nov.append(ch)
            continue
        if ((not kletkaOdprta and not pricaOdprta) and o not in tocke
                and o not in STEJE and o != 0x20):
            nov.append(levo + "U+%04X" % o + desno)
        else:
            nov.append(ch)
    return "".join(nov)


def popis(vrstica):
    """Dnevnik dneva : vsako rojstvo orodja poimensko isti cas."""
    with open(POPIS, "a", encoding="utf-8") as f:
        f.write(vrstica + "\n")


def rehabilitiraj(path, tocke, izhod):
    telo, (sovraz, imen, nos, azil) = cenzus(path, tocke)
    obst = obstojeciKod()
    os.makedirs(CELICE, exist_ok=True)
    for o in sorted(sovraz):
        st, prva = sovraz[o]
        ime = os.path.join(CELICE, "mrk-celica-U%04X-%s.md" % (o, tik().replace(":", "")))
        with open(ime, "w", encoding="utf-8") as f:
            f.write(dosje(o, st, prva, path, obst) + "\n")
    if izhod is None:
        izhod = os.path.join(GENIZA, ("mrk-prevod-" + os.path.basename(path) + "-" + tik().replace(":", "") + ".md"))
    if os.path.basename(os.path.realpath(izhod)) == "KNOWLEDGE.md":
        print("VRATA ZAPRTA : organ ni tarča postopka ⟨NE-GRIZI⟩ 2432")
        sys.exit(ODSTOP)
    if not vrata(izhod):
        print("POT ZUNAJ KOREN")
        sys.exit(ODSTOP)
    with open(izhod, "w", encoding="utf-8") as f:
        f.write(preliv(telo, tocke))
    popis("mrk-prevajalnik v1.4 TIK " + tik() + " : preliv " + os.path.basename(izhod) + " ; osnutkov dosjejev " + str(len(sovraz)))
    return izhod, len(sovraz)


def samopreizkus():
    padci = 0
    tocke, decoding, celota = belaLista()
    ok1 = (celota["crke"] == 62 and celota["imena"] == 25
           and celota["zigi"] == 10 and celota["zigi2"] == 10)
    print("T1 bela lista pri viru ( crke 62 , imena 25 , zigi 10 in 10 ) : %s" % ("ZELENO" if ok1 else "PADANO"))
    if not ok1:
        padci += 1
    os.makedirs(GENIZA, exist_ok=True)
    trup = os.path.join(GENIZA, "TEST-mrk-trup-6931.txt")
    with open(trup, "w", encoding="utf-8") as f:
        f.write("beseda je ne 123\n")
    _, (s2, i2, n2, a2) = cenzus(trup, tocke)
    ok2 = (len(s2) == 0)
    print("T2 cisto telo : %s" % ("ZELENO ( mirovanje )" if ok2 else "PADANO"))
    if not ok2:
        padci += 1
    with open(trup, "w", encoding="utf-8") as f:
        f.write("cisti trup z golim ⟨U+2699⟩ : " + chr(0x2699) + " in " + chr(0x0430) + "\n")
    _, (s3, i3, n3, a3) = cenzus(trup, tocke)
    ok3 = (s3.get(0x2699, (0, 0))[0] == 1 and s3.get(0x430, (0, 0))[0] == 1 and len(s3) == 2)
    print("T3 gol trup : %s" % ("ZELENO ( ⟨U+2699⟩ in ⟨U+0430⟩ poimensko )" if ok3 else "PADANO"))
    if not ok3:
        padci += 1
    izhod, n4 = rehabilitiraj(trup, tocke, os.path.join(GENIZA, "TEST-mrk-prevod-6931.txt"))
    _, (s4, i4, n4b, a4) = cenzus(izhod, tocke)
    telo4 = beri(izhod)
    ok4 = (len(s4) == 0 and n4 == 2 and "U+2699" in telo4 and "U+0430" in telo4)
    print("T4 preliv skozi unikorn : %s" % ("ZELENO ( mirovanje izhoda ; 2 gosta poimensko v kletki )" if ok4 else "PADANO"))
    if not ok4:
        padci += 1
    with open(__file__, "r", encoding="utf-8") as f:
        lastno = f.read()
    s5, i5, n5, a5 = cenzusTela(lastno, tocke, True)
    ok5 = (set(n5) == NOSILCI_TELA and len(s5) == 0 and 0x27E8 in a5 and 0x27E9 in a5)
    print("T5 lastno telo merjeno s seboj : %s" % (
        "ZELENO ( nosilci prijavljeni : " + " ".join(sorted("⟨U+%04X⟩" % o for o in n5)) + " ; goli 0 )"
        if ok5 else
        "PADANO ( izmerjeno : " + " ".join(sorted("⟨U+%04X⟩" % o for o in set(n5) | set(s5))) + " )"))
    if not ok5:
        padci += 1
    kod = kletka(0x2699)
    ok6 = (len(kod) == 4 and len(set(kod)) == 4 and all(k.startswith("K") and len(k) == 5 and k[1] != "0" for k in kod))
    trki = [k for k in kod if k in obstojeciKod()]
    print("T6 kletka ⟨U+2699⟩ : %s ( %s ; trki z registrom unikorn : %d )" % (
        "ZELENO" if ok6 else "PADANO", " ".join(kod), len(trki)))
    if not ok6:
        padci += 1
    print("SAMOPREIZKUS : padlov %d" % padci)
    print("TIK : %s" % tik())
    sys.exit(0 if padci == 0 else ODSTOP)


def main():
    ap = argparse.ArgumentParser(description="ORODJE MRK mrk-prevajalnik v1.4")
    ap.add_argument("--gajica", action="store_true")
    ap.add_argument("--izmeri")
    ap.add_argument("--mir")
    ap.add_argument("--rehabilitiraj")
    ap.add_argument("--izhod")
    ap.add_argument("--samopreizkus", action="store_true")
    a = ap.parse_args()
    if a.samopreizkus:
        samopreizkus()
    if a.gajica:
        tocke, decoding, celota = belaLista()
        print("BELA LISTA PRI VIRU")
        print("register 1 : crke 62 ; imena 25 ; zigi binarne podlage %d ; md5 %s" % (celota["zigi"], celota["md5reg1"]))
        print("register 2 : isti znaki ; zigi %d ; md5 %s" % (celota["zigi2"], celota["md5reg2"]))
        print("prevodnik : dekodiranih imen 25 ( predlogov operaterja : %d )" % celota["predlogi"])
        for ime in sorted(decoding):
            fl = [f for nme, _, f in PREVODNIK if nme == ime][0]
            print("  %s = ⟨U+%04X⟩%s" % (ime, decoding[ime], " ( PREDLOG )" if fl == "predlog" else ""))
        print("celotna lista kodnih tock : %d" % celota["toccke"])
        sys.exit(0)
    if a.izmeri or a.mir:
        pot = a.izmeri if a.izmeri else a.mir
        if not vrata(pot) or not os.path.isfile(pot):
            print("TELO NI ZNOTRAJ KOREN ALI NE OBSTOJA")
            sys.exit(ODSTOP)
        tocke, _, _ = belaLista()
        telo, (sovraz, imen, nos, azil) = cenzus(pot, tocke)
        print(poroci(sovraz, imen, nos, azil, pot))
        if a.mir:
            if sovraz:
                print("MIROVANJE : NE ; goli sovrazniki cakajo sodbo operaterja")
                sys.exit(1)
            print("MIROVANJE : DA PO MRK ; moc 0 ; izvedba 0")
            sys.exit(0)
        sys.exit(1 if sovraz else 0)
    if a.rehabilitiraj:
        if not vrata(a.rehabilitiraj) or not os.path.isfile(a.rehabilitiraj):
            print("TELO NI ZNOTRAJ KOREN ALI NE OBSTOJA")
            sys.exit(ODSTOP)
        tocke, _, _ = belaLista()
        izhod, n = rehabilitiraj(a.rehabilitiraj, tocke, a.izhod)
        print("PREVOD SKOZI UNIKORN : dosje osnutkov %d ; izhod : %s" % (n, izhod))
        sys.exit(0)
    print("ORODJE MRK mrk-prevajalnik : --gajica ; --izmeri TELO ; --mir TELO ; --rehabilitiraj TELO --izhod DAT ; --samopreizkus")
    sys.exit(ODSTOP)


if __name__ == "__main__":
    main()
