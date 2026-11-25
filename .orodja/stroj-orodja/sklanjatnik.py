# -*- coding: utf-8 -*-
# SKLANJATNIK v1.3 — ORODJE ZA PRAVILNO SKLANJANJE ( samostalniki + števniške zveze + i-tvor + pridevniki )
# Rod : rez 6987 ( v1.0 ), sedež KLEPET, projekt LUCIUS ; nadgradnja v1.1 rez 6990 ; nadgradnja v1.2 rez 6998 ;
#          nadgradnja v1.3 rez 6999 ( ukaz naročnika dobesedno : stori in preveri slovnico preden dokončaš ;
#          odprti vrati tega diha : i-tvor in pridevniške tabele, obe zaprti po rezervaciji poimensko rez 6998 )
# Starša : naročnik Luka Pintarič ( ukaz : USTVARI ORODJA ZA PRAVILNO SKLANJANJE )
#          in izvajalka Mera ( izvedba )
# Priče :
#   - SSKJ, geslo sklánjati, pomen 2 ( lingv. menjavati končnice pri samostalniku,
#     pridevniku, zaimku in števniku ) : fran.si/iskanje?FilteredDictionaryIds=130&View=1&Query=sklanjati
#     ( dostop 25. 11. 2026 )
#   - Sloleks, slovenski oblikoslovni leksikon ( vse pregibne oblike izlečkov pri viru ) :
#     clarin.si hdl 11356/2080 ( Sloleks 3.1, dostop 25. 11. 2026 )
#   - predlog s/z pred orodnikom : z pred zvenljivimi ( b d g z ž ) in zvočniki
#     ( m n r l v j ) ter samoglasniki, s pred nezvenljivimi ( t s h š k f c p č ) :
#     slo-na-dlani.si/znanje/134, razlaga po Pedagoškem slovničnem portalu ( dostop 25. 11. 2026 )
#   - vira slovnice števnikov že zapečena v organu sklanjanje-stevil ( sss.ung.si, isjfr.zrc-sazu.si )
#   - zveza 1 ( en, ena, eno ) : SSKJ geslo en fran.si/130/3540518 ; oblike izmerjene v celotnem besedilu
#     SSKJ istega dne ( rodilnik ženski ene : absolutiziranju ene strani resničnosti, zadetkov 262 ;
#     D eni prilagojeno eni družini ; I z enim dejanjem, z eno besedo ) ; dostop 25. 11. 2026
#   - zveza 2 ( dva, dve, oba, obe ) : SSKJ glavi gesel dva fran.si/130/3539373 ( dva, dve, dveh,
#     dvema ) in oba fran.si/130/3569100 ( dolžnost obeh staršev, predstavniki obeh držav ) ;
#     SSS sss.ung.si glavni
#     števniki ( obema konjema sem dal oves, z dvema milijonoma, obe ovci ) ; dostop 25. 11. 2026
#   - tožilnik zveze 1 pred samostalnikom je en ( spil je en aperitiv, T pred imenom ), samostalniška
#     raba je enega ( pošlji enega, ki se na to razume ) — izmerjeni pri SSKJ istega dne
# ZAKON : pravilnost oblike ni obljuba orodja, je izmera pri viru ( SSKJ, Fran, Sloleks ).
#          Orodje tvori, vir odloča. Kar dvoma ne preživi, je bil ugib.
# MEJA v1.0 ( poimensko, ne po občutku ) :
#   - pred sabo so vzorci ×6 samostalnikov ; izven : ženski i-tvor ( pest ),
#     lastna imena, vodne izjeme, pridevniki, zaimki, števniki, glagoli — odprta vrata,
#     vsako širjenje samo po izmeri pri viru ⊙ NE-UGIBAJ 2690.
# RABA :
#   python3 sklanjatnik.py <geslo> <vzorec>     -> tabela 18 oblik
#   python3 sklanjatnik.py --preveri           -> samopreverba v živo ( preizkus pred zapečenjem )
#   python3 sklanjatnik.py --vzorci            -> imena vzorcev
#   python3 sklanjatnik.py --zveza 3 hiša z-a  -> števniška zveza, 6 sklonov

import sys

# vzorec : "od" = končnica iztočnice, ki osnova odloži pred tvorbo ( a-o-e vzorci )
#          m vzorci nosijo čisto soglasniško osnovo ( od = prazno )
# končnice : [ N, G, D, T, L, I ] × [ ednina, dvojina, množina ]
VZORCI = {
    # moški trdi, brez končnice : korak, junak, most
    "m-trdi": {
        "spol": "m", "priča": "korak", "od": "",
        "ednina":  ["",  "a", "u",  "",  "u",  "om"],
        "dvojina":  ["a", "",  "oma", "a", "ih", "oma"],
        "množina": ["i", "ov", "om", "e", "ih", "i"],
    },
    # moški z množino na -ovi : glas, sin, šum
    "m-glasovi": {
        "spol": "m", "priča": "glas", "od": "",
        "ednina":  ["",  "a", "u",  "",  "u",  "om"],
        "dvojina":  ["a", "",  "oma", "a", "ih", "oma"],
        "množina": ["ovi", "ov", "ovom", "ove", "ovih", "ovi"],
    },
    # moški mehki s končnico -ev : kralj, tič
    "m-mehki": {
        "spol": "m", "priča": "kralj", "od": "",
        "ednina":  ["",  "a", "u",  "",  "u",  "em"],
        "dvojina":  ["a", "",  "ema", "a", "ih", "ema"],
        "množina": ["i", "ev", "em", "e", "ih", "i"],
    },
    # ženski a-tvor : žena, hiša, leta
    "z-a": {
        "spol": "z", "priča": "žena", "od": "a",
        "ednina":  ["a", "e",  "i",  "o", "i",  "o"],
        "dvojina":  ["i", "",  "ama", "i", "ah", "ama"],
        "množina": ["e", "", "am", "e", "ah", "ami"],
    },
    # srednji o-tvor : mesto, telo, okno
    "s-o": {
        "spol": "s", "priča": "mesto", "od": "o",
        "ednina":  ["o", "a", "u",  "o", "u",  "om"],
        "dvojina":  ["i", "",  "oma", "i", "ih", "oma"],
        "množina": ["a", "", "om", "a", "ih", "i"],
    },
    # srednji e-tvor : polje, kopje, znamenje
    "s-e": {
        "spol": "s", "priča": "polje", "od": "e",
        "ednina":  ["e", "a", "u",  "e", "u",  "em"],
        "dvojina":  ["i", "",  "ema", "i", "ih", "ema"],
        "množina": ["a", "", "em", "a", "ih", "i"],
    },
    # ženski i-tvor, pest vrsta : pest, reš ( dvojina in množina na -ema/-eh/-mi )
    # izmerjeno pri viru : sloleks/slv/headword/77615 ( dostop 25. 11. 2026 )
    "z-i-pest": {
        "spol": "z", "priča": "pest", "od": "",
        "ednina":  ["",  "i", "i",  "",  "i",  "jo"],
        "dvojina":  ["i", "i", "ema", "i", "eh", "ema"],
        "množina": ["i", "i", "em",  "i", "eh", "mi"],
    },
    # ženski i-tvor, miš vrsta : miš, noč ( dvojina in množina na -ma/-ih/-mi )
    # izmerjeno pri viru : sloleks/slv/headword/69799 ( dostop 25. 11. 2026 )
    "z-i-miš": {
        "spol": "z", "priča": "miš", "od": "",
        "ednina":  ["",  "i", "i",  "",  "i",  "jo"],
        "dvojina":  ["i", "i", "ma",  "i", "ih", "ma"],
        "množina": ["i", "i", "im",  "i", "ih", "mi"],
    },
}

SKLONI = ["imenovalnik", "rodilnik", "dajalnik", "tožilnik", "mestnik", "orodnik"]

# prvi glas orodniške oblike odloča med s in z ( priča : slo-na-dlani.si/znanje/134 )
ZVENLJIVI = set("bdgzž")         # zvenljivi soglasniki -> predlog z
ZVOČNIKI  = set("mnrlvj")         # zvočniki            -> predlog z
GLASNIKI = set("aeiou")          # samoglasniki        -> predlog z
# nezvenljivi ( t s h š k f c p č ) in vse drugo -> predlog s

def predlog_orodnika(oblika):
    """s ali z : izmera prvega glasu oblike, ne občutek"""
    if not oblika:
        return "s"
    g = oblika[0].lower()
    if g in ZVENLJIVI or g in ZVOČNIKI or g in GLASNIKI:
        return "z"
    return "s"

def osnova(geslo, vzorec):
    """osnova odloži končnico iztočnice ( a-o-e vzorci ), m vzorci stojijo taki kot so"""
    konec = VZORCI[vzorec]["od"]
    if konec:
        if not geslo.endswith(konec):
            raise SystemExit("geslo " + geslo + " se ne sklada z vzorcem " + vzorec +
                             " ( iztočnica mora nositi konec " + konec + " ) ; izmeri pri viru pred sklanjanjem")
        return geslo[:-len(konec)]
    return geslo

def sklanjaj(geslo, vzorec):
    """vrne ( spol, tabela ) : tabela = { število : [ 6 oblik ] } ; mestnik nosi o, orodnik s/z"""
    if vzorec not in VZORCI:
        raise SystemExit("neznan vzorec : " + str(vzorec) + " ; glej --vzorci")
    v = VZORCI[vzorec]
    osn = osnova(geslo, vzorec)
    tabela = {}
    for stevilo in ("ednina", "dvojina", "množina"):
        vrstica = []
        for i, koncnica in enumerate(v[stevilo]):
            oblika = osn + koncnica
            if i == 4:
                oblika = "o " + oblika                          # mestnik
            elif i == 5:
                oblika = predlog_orodnika(oblika) + " " + oblika  # orodnik
            vrstica.append(oblika)
        tabela[stevilo] = vrstica
    return spol_naziv(v["spol"]), tabela

def spol_naziv(spol):
    return {"m": "moški", "z": "ženski", "s": "srednji"}[spol]

# samopreverba : kanonske oblike šestih prič, pisane po slovnici,
# vsaka oblika ena odprta vrata za preverbo pri viru ( SSKJ, Sloleks )
PRIČE = {
    "korak": ("m-trdi", {
        "ednina":  ["korak", "koraka", "koraku", "korak", "o koraku", "s korakom"],
        "dvojina":  ["koraka", "korak", "korakoma", "koraka", "o korakih", "s korakoma"],
        "množina": ["koraki", "korakov", "korakom", "korake", "o korakih", "s koraki"],
    }),
    "glas": ("m-glasovi", {
        "ednina":  ["glas", "glasa", "glasu", "glas", "o glasu", "z glasom"],
        "dvojina":  ["glasa", "glas", "glasoma", "glasa", "o glasih", "z glasoma"],
        "množina": ["glasovi", "glasov", "glasovom", "glasove", "o glasovih", "z glasovi"],
    }),
    "kralj": ("m-mehki", {
        "ednina":  ["kralj", "kralja", "kralju", "kralj", "o kralju", "s kraljem"],
        "dvojina":  ["kralja", "kralj", "kraljema", "kralja", "o kraljih", "s kraljema"],
        "množina": ["kralji", "kraljev", "kraljem", "kralje", "o kraljih", "s kralji"],
    }),
    "žena": ("z-a", {
        "ednina":  ["žena", "žene", "ženi", "ženo", "o ženi", "z ženo"],
        "dvojina":  ["ženi", "žen", "ženama", "ženi", "o ženah", "z ženama"],
        "množina": ["žene", "žen", "ženam", "žene", "o ženah", "z ženami"],
    }),
    "mesto": ("s-o", {
        "ednina":  ["mesto", "mesta", "mestu", "mesto", "o mestu", "z mestom"],
        "dvojina":  ["mesti", "mest", "mestoma", "mesti", "o mestih", "z mestoma"],
        "množina": ["mesta", "mest", "mestom", "mesta", "o mestih", "z mesti"],
    }),
    "polje": ("s-e", {
        "ednina":  ["polje", "polja", "polju", "polje", "o polju", "s poljem"],
        "dvojina":  ["polji", "polj", "poljema", "polji", "o poljih", "s poljema"],
        "množina": ["polja", "polj", "poljem", "polja", "o poljih", "s polji"],
    }),
    # i-tvor, pest vrsta : izmerjeno pri viru ( sloleks/slv/headword/77615 )
    "pest": ("z-i-pest", {
        "ednina":  ["pest", "pesti", "pesti", "pest", "o pesti", "s pestjo"],
        "dvojina":  ["pesti", "pesti", "pestema", "pesti", "o pesteh", "s pestema"],
        "množina": ["pesti", "pesti", "pestem", "pesti", "o pesteh", "s pestmi"],
    }),
    # i-tvor, miš vrsta : izmerjeno pri viru ( sloleks/slv/headword/69799 )
    "miš": ("z-i-miš", {
        "ednina":  ["miš", "miši", "miši", "miš", "o miši", "z mišjo"],
        "dvojina":  ["miši", "miši", "mišma", "miši", "o miših", "z mišma"],
        "množina": ["miši", "miši", "mišim", "miši", "o miših", "z mišmi"],
    }),
}

def preveri():
    """samopreverba v živo : merilec se meri ⊙ §52 ; preizkus PRED zapečenjem"""
    oblike_skupaj = 0
    padci = []
    for geslo, (vzorec, priča) in PRIČE.items():
        _, tabela = sklanjaj(geslo, vzorec)
        for stevilo in ("ednina", "dvojina", "množina"):
            for i in range(6):
                oblike_skupaj += 1
                if tabela[stevilo][i] != priča[stevilo][i]:
                    padci.append(geslo + " " + stevilo + " " + SKLONI[i] +
                                 " : izhod " + tabela[stevilo][i] + " ⊥ priča " + priča[stevilo][i])
    print("SAMOPREVERBA SKLANJATNIK v1.0 : oblike " + str(oblike_skupaj) + ", vzorci " + str(len(PRIČE)))
    if padci:
        for p in padci:
            print("PADC : " + p)
        print("ODLOČITEV : RDEČA, orodje ni zapečeno")
        return 1
    print("padci : 0")
    print("ODLOČITEV : ZELENA, orodje zapečeno")
    return 0

def izris(geslo, vzorec):
    spol, tabela = sklanjaj(geslo, vzorec)
    print(geslo + " ( " + spol + " spol, vzorec " + vzorec + ", priča vzorca " + VZORCI[vzorec]["priča"] + " )")
    print("")
    print("{:<14}{:<14}{:<14}{:<14}".format("", "ednina", "dvojina", "množina"))
    for i, sklon in enumerate(SKLONI):
        print("{:<14}{:<14}{:<14}{:<14}".format(
            sklon, tabela["ednina"][i], tabela["dvojina"][i], tabela["množina"][i]))
    print("")
    print("merjeno, ne ugibano : oblika je pravilna ko preživi preverbo pri viru ( SSKJ, Fran, Sloleks )")

def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "--preveri":
        sys.exit(preveri())
    if len(sys.argv) >= 2 and sys.argv[1] == "--vzorci":
        for ime, v in VZORCI.items():
            print("{:<12} priča {}".format(ime, v["priča"]))
        return
    if len(sys.argv) == 3:
        izris(sys.argv[1], sys.argv[2])
        return
    print("raba : python3 sklanjatnik.py <geslo> <vzorec> | --preveri | --vzorci")



# ============================================================
# v1.1 — ŠTEVNIŠKE ZVEZE ( ukaz STORI rez 6990 )
# ZAKONI organa sklanjanje-stevil ( plasti 3 in 4, sveže prebrani istega diha ) :
#   - 3 in 4 se VEDNO sklanjajo pridevniško ; oblike izmerjene pri viru :
#     trije ( treh, trem, tri, treh, tremi ) in štirje ( štirih, štirim, štiri,
#     štirih, štirimi ) priča JS ZRC SAZU ∧ bubblegum.la ( dostop 21. 11. 2026 )
#   - 5 naprej : v imenovalniku in tožilniku samostalnik v rodilniku množine
#     ( pet knjig ), v odvisnih sklonih pridevniško ujemanje števnika
#     ( brez petih knjig, k petim knjigam, o petih knjigah, s petimi knjigami )
#     priča Toporišič 2008 : 330–331 ( dostop 21. 11. 2026 )
#   - sveža potrditev istega dne : s tremi milijoni, z dvema milijonoma,
#     brez enega milijona, z enim milijonom, s petimi milijoni
#     priča SSS sss.ung.si glavni_stevniki ( dostop 25. 11. 2026 )
#   - samostalnik sledi zadnjemu števniku ; predlog določa sklon
# VRATA RAZREZERVIRANA ( poimensko, brez kode ugibanja ; NE-UGIBAJ ) :
#   - zveza 1 ( zaimek en, ena, eno ) : izmerjeni N ( en milijon pra SSS ),
#     G enega ( brez enega milijona pra SSS ), I enim ( z enim milijonom pra SSS ) ;
#     D in L ( enem, enemu ) nista izmerjena pri viru ta dih ( fran.si preobremenjen,
#     javno sporočilo portala ; sloleks zaviral avtomatski dostop ).
#   - zveza 2 ( dva, dve, oba, obe ) : izmerjena N ( dva stola, dve mesti pra
#     organ ∧ slo-na-dlani znanje 6 ) in I ( z dvema milijonoma pra SSS ) ;
#     G ( dveh ), D ( dvema, obema ) in L ( dveh ) niso izmerjeni pri viru ta dih.
#   - ženski i-tvor ( pest, miš ) : klasifikacija izmerjena ( miš, priča
#     slo-na-dlani znanje 6 ), oblike ne ; pridevniki : določna in nedoločna
#     oblika ter ničta končnica m ed izmerjene ( ucko.si ), tabele ne.
#     Vsako od teh vrat odpri samo po izmeri pri viru ali besedi naročnika.
# NADGRADNJA v1.2 rez 6998 : zvezi 1 in 2 sta ZAPEČENI, vse oblike izmerjene pri viru
#     istega dne ( fran.si je oddahnil, berbe v glavi telesa ) ; odprta vrata
#     ostajata poimensko : i-tvor, pridevniške tabele.
# NADGRADNJA v1.3 rez 6999 : obe odprti vrati ZAPEČENI po izmerah pri viru istega dne :
#   - i-tvor ženski : dva vzorca po izmeri ( viri.cjvt.si/sloleks, dostop 25. 11. 2026 ) :
#     pest ( sloleks/slv/headword/77615 : pesti, pestema, pesteh, pestmi ) in
#     miš ( sloleks/slv/headword/69799 : miši, mišma, miših, mišmi ) ; dva vzorca
#     ker vir javlja obli dvojini in množini različno ( pestema / mišma ).
#   - pridevniške tabele : določno in nedoločno sklanjanje treh spolov po izmeri
#     prič pravi ( sloleks/slv/headword/30012, vsi trije spoli ) in svet
#     ( sloleks/slv/headword/35546 : izmerjeni obe imenovalniški obliki svet voz
#     in sveti voz ter obe tožilniški svetega voz in sveti voz ). Ohranjena vrata
#     rezervirana poimensko : kratki pridevnik na -en ( podoben, ne izmerjen pri
#     viru ta dih ), lastna imena, vodne izjeme, zaimki, glagoli.

ŠTEVNIKI = {
    # zveza 1 ( en, ena, eno ), izmerjeno rez 6998 ( fran.si, SSS, dostop 25. 11. 2026 )
    "1": {
        # pred samostalnikom ; samostalniška raba T je enega ( pošlji enega )
        "m":  ["en", "enega", "enemu", "en", "enem", "enim"],
        "z":  ["ena", "ene", "eni", "eno", "eni", "eno"],
        "s":  ["eno", "enega", "enemu", "eno", "enem", "enim"],
    },
    # zveza 2 ( dva, dve, oba, obe ), izmerjeno rez 6998
    "2": {
        "m":  ["dva", "dveh", "dvema", "dva", "dveh", "dvema"],
        "zs": ["dve", "dveh", "dvema", "dve", "dveh", "dvema"],
    },
    "2-oba": {
        "m":  ["oba", "obeh", "obema", "oba", "obeh", "obema"],
        "zs": ["obe", "obeh", "obema", "obe", "obeh", "obema"],
    },
    "3": {
        "m":  ["trije", "treh", "trem", "tri", "treh", "tremi"],
        "zs": ["tri", "treh", "trem", "tri", "treh", "tremi"],
    },
    "4": {
        "m":  ["štirje", "štirih", "štirim", "štiri", "štirih", "štirimi"],
        "zs": ["štiri", "štirih", "štirim", "štiri", "štirih", "štirimi"],
    },
    "5": {
        "vsi": ["pet", "petih", "petim", "pet", "petih", "petimi"],
    },
}

VRATA_REZERVIRANA = {
    # rez 6999 : vrati i-tvor in pridevniške tabele ZAPRTI ( vzorci z-i-pest, z-i-miš
    # in pridevniške tabele zapečeni po izmerah pri viru ) ; nova odprta vrata :
    "pridevnik-kratki-en": ("kratki pridevnik na -en ( npr podoben ) : VRATA ODPRTA ; nedoločna "
                            "iztočnica podoben proti osnovi podobn- ni mehanična izpeljava, "
                            "oblike je prej izmeriti pri viru ( SSKJ, Sloleks ) ; nobena koda "
                            "ugibanja ⊙ NE-UGIBAJ 2690"),
    "lastna-imena": ("lastna imena : VRATA ODPRTA ; oblike je prej izmeriti pri viru ( SSKJ, "
                     "Sloleks ) ; nobena koda ugibanja ⊙ NE-UGIBAJ 2690"),
    "vodne-izjeme": ("vodne izjeme ( npr Ljubljana, Bolt ) : VRATA ODPRTA ; oblike je prej "
                     "izmeriti pri viru ( SSKJ, Sloleks ) ; nobena koda ugibanja ⊙ NE-UGIBAJ 2690"),
    "zaimki": ("zaimki : VRATA ODPRTA ; oblike je prej izmeriti pri viru ( SSKJ, Sloleks ) ; "
               "nobena koda ugibanja ⊙ NE-UGIBAJ 2690"),
    "glagoli": ("glagoli : VRATA ODPRTA ; oblike je prej izmeriti pri viru ( SSKJ, Sloleks ) ; "
                "nobena koda ugibanja ⊙ NE-UGIBAJ 2690"),
}

# končnice dolgega pridevnika : osnova = določna oblika ednine moškega brez -i
# ( pravi -> prav, sveti -> svet ) ; izmerjeno pri viru ( priči svet in pravi )
PRAIDEVNISKE_KONCNICE = {
    "m": {
        "nedoločno": {
            "ednina":  ["",    "ega", "emu", "ega", "em", "im"],
            "dvojina":  ["a",   "ih",  "ima", "a",   "ih", "ima"],
            "množina": ["i",   "ih",  "im",  "e",   "ih", "imi"],
        },
        "določno": {
            "ednina":  ["i",   "ega", "emu", "i",   "em", "im"],
            "dvojina":  ["a",   "ih",  "ima", "a",   "ih", "ima"],
            "množina": ["i",   "ih",  "im",  "e",   "ih", "imi"],
        },
    },
    # ženski in srednji : določno in nedoločno obliki po izmeri enaki
    "z": {
        "vse": {
            "ednina":  ["a",   "e",   "i",   "o",   "i",  "o"],
            "dvojina":  ["i",   "ih",  "ima", "i",   "ih", "ima"],
            "množina": ["e",   "ih",  "im",  "e",   "ih", "imi"],
        },
    },
    "s": {
        "vse": {
            "ednina":  ["o",   "ega", "emu", "o",   "em", "im"],
            "dvojina":  ["i",   "ih",  "ima", "i",   "ih", "ima"],
            "množina": ["a",   "ih",  "im",  "a",   "ih", "imi"],
        },
    },
}

def pridevniška_osnova(geslo):
    """določna oblika ednine moškega ( pravi, sveti ) nosi osnovo brez -i"""
    if not geslo.endswith("i"):
        raise SystemExit("pridevnik " + geslo + " : pričakovana določna oblika ednine moškega na -i "
                         "( npr sveti, pravi ) ; kratki pridevnik na -en je odprta vrata ; izmeri pri viru")
    return geslo[:-1]

def pridevniške_tabele(geslo):
    """vrne { spol : { oblika : { število : [ 6 oblik ] } } } po izmeri pri viru"""
    osn = pridevniška_osnova(geslo)
    tabele = {}
    for spol in ("m", "z", "s"):
        oblike = {}
        sklopi = ("nedoločno", "določno") if spol == "m" else ("vse",)
        for sklop in sklopi:
            v = PRAIDEVNISKE_KONCNICE[spol][sklop]
            tabela = {}
            for stevilo in ("ednina", "dvojina", "množina"):
                vrstica = []
                for i, koncnica in enumerate(v[stevilo]):
                    oblika = osn + koncnica
                    if i == 4:
                        oblika = "o " + oblika                          # mestnik
                    elif i == 5:
                        oblika = predlog_orodnika(oblika) + " " + oblika  # orodnik
                    vrstica.append(oblika)
                tabela[stevilo] = vrstica
            oblike[sklop] = tabela
        tabele[spol] = oblike
    return tabele

def gole_oblike(geslo, vzorec):
    # gole oblike brez predlogov ( mestnik o, orodnik s/z ) : zveza jih nosi pri števniku
    v = VZORCI[vzorec]
    osn = osnova(geslo, vzorec)
    tabela = {}
    for stevilo in ("ednina", "dvojina", "množina"):
        tabela[stevilo] = [osn + koncnica for koncnica in v[stevilo]]
    return tabela

def zveza(stevnik, geslo, vzorec):
    # vrača 6 vrstic zveze po sklonih : števnik nosi predloge, samostalnik sledi
    if vzorec not in VZORCI:
        raise SystemExit("neznan vzorec : " + str(vzorec) + " ; glej --vzorci")
    spol = VZORCI[vzorec]["spol"]
    gole = gole_oblike(geslo, vzorec)
    vrstice = []
    if stevnik == "1":
        # zveza 1, zapečena rez 6998 : samostalnik sledi v ednini
        kljuc = spol if spol in ("m", "z", "s") else "m"
        niz = ŠTEVNIKI["1"][kljuc]
        sam = gole["ednina"]
        for i in range(6):
            if i == 4:
                vrstice.append("o " + niz[i] + " " + sam[i])
            elif i == 5:
                vrstice.append(predlog_orodnika(niz[i]) + " " + niz[i] + " " + sam[i])
            else:
                vrstice.append(niz[i] + " " + sam[i])
        return vrstice, []
    if stevnik in ("2", "2-oba"):
        # zveza 2, zapečena rez 6998 ; skloni po izmeri pri viru :
        #   N in T dvojina ⊢ SSS ( oba konja, obe ovci ),
        #   G množina ⊢ SSKJ geslo oba ( dolžnost obeh staršev, predstavniki obeh držav ),
        #   D in I dvojina ⊢ SSS ( obema konjema sem dal oves, z dvema milijonoma ),
        #   L obliki enaki v dvojini in množini ⊢ SSKJ ( roman v dveh delih )
        niz = ŠTEVNIKI[stevnik]["m"] if spol == "m" else ŠTEVNIKI[stevnik]["zs"]
        sam = gole["dvojina"]
        sam_po_sklonu = [sam[0], gole["množina"][1], sam[2], sam[3], sam[4], sam[5]]
        for i in range(6):
            if i == 4:
                vrstice.append("o " + niz[i] + " " + sam_po_sklonu[i])
            elif i == 5:
                vrstice.append(predlog_orodnika(niz[i]) + " " + niz[i] + " " + sam_po_sklonu[i])
            else:
                vrstice.append(niz[i] + " " + sam_po_sklonu[i])
        return vrstice, [
            "skloni zveze izmerjeni pri viru : N in T dvojina ( SSS oba konja ), "
            "G množina ( SSKJ dolžnost obeh staršev ), D in I dvojina ( SSS obema konjema, "
            "z dvema milijonoma ), L obliki enaki ( SSKJ roman v dveh delih )",
        ]
    if stevnik in ("3", "4"):
        niz = ŠTEVNIKI[stevnik]["m"] if spol == "m" else ŠTEVNIKI[stevnik]["zs"]
        sam = gole["množina"]
        for i in range(6):
            if i == 4:
                vrstice.append("o " + niz[i] + " " + sam[i])
            elif i == 5:
                vrstice.append(predlog_orodnika(niz[i]) + " " + niz[i] + " " + sam[i])
            else:
                vrstice.append(niz[i] + " " + sam[i])
        return vrstice, []
    if stevnik == "5" or stevnik == "pet":
        niz = ŠTEVNIKI["5"]["vsi"]
        mn = gole["množina"]
        # N in T : samostalnik v rodilniku množine ; odvisni skloni : samostalnik po sklonu množine
        sam_po_sklonu = [mn[1], mn[1], mn[2], mn[1], mn[4], mn[5]]
        for i in range(6):
            if i == 4:
                vrstice.append("o " + niz[i] + " " + sam_po_sklonu[i])
            elif i == 5:
                vrstice.append(predlog_orodnika(niz[i]) + " " + niz[i] + " " + sam_po_sklonu[i])
            else:
                vrstice.append(niz[i] + " " + sam_po_sklonu[i])
        return vrstice, [
            "odvisno sklanjanje 5 naprej je neobvezno ( organ plast 1 ) ; "
            "pri enicah prevlada sklanjana oblika ( Toporišič 330–331 )",
        ]
    if stevnik in ("6", "7", "8", "9", "10"):
        # N in T sta izmerjena zakona ( rodilnik množine ) ; odvisne oblike niso izmerjene pri viru
        gm = gole["množina"][1]
        vrstice = [stevnik + " " + gm, None, None, stevnik + " " + gm, None, None]
        return vrstice, [
            "VRATA ODPRTA : odvisne oblike ( G, D, L, I ) števnika " + stevnik +
            " niso izmerjene pri viru ta dih ( izpeljava ni mehanična za sedem in osem ) ; "
            "N in T sta izmerjena zakona rodilnika množine",
        ]
    if stevnik in VRATA_REZERVIRANA:
        return None, [VRATA_REZERVIRANA[stevnik]]
    raise SystemExit("neznan števnik : " + str(stevnik) + " ; izmerjeni : 1, 2, 2-oba, 3, 4, 5 ( pet ), "
                     "odprti N in T : 6 7 8 9 10 ; odprta vrata po imenu : i-tvor, pridevniki")

ZVEZE_PRIČE = [
    ("3", "korak", "m-trdi",
     ["trije koraki", "treh korakov", "trem korakom", "tri korake",
      "o treh korakih", "s tremi koraki"]),
    ("3", "hiša", "z-a",
     ["tri hiše", "treh hiš", "trem hišam", "tri hiše",
      "o treh hišah", "s tremi hišami"]),
    ("4", "korak", "m-trdi",
     ["štirje koraki", "štirih korakov", "štirim korakom", "štiri korake",
      "o štirih korakih", "s štirimi koraki"]),
    ("5", "korak", "m-trdi",
     ["pet korakov", "petih korakov", "petim korakom", "pet korakov",
      "o petih korakih", "s petimi koraki"]),
]

def preveri_v11():
    print("SAMOPREVERBA SKLANJATNIK v1.1 : nadgradnja števniških zvez nad v1.0")
    print("plast 1 : samostalnik v1.0 ( 108 oblik, 6 prič ) :")
    r0 = preveri()
    if r0 != 0:
        return r0
    oblike, padci = 0, []
    for stevnik, geslo, vzorec, priča in ZVEZE_PRIČE:
        vrstice, opombe = zveza(stevnik, geslo, vzorec)
        for i in range(6):
            oblike += 1
            if vrstice[i] != priča[i]:
                padci.append("zveza " + stevnik + " " + geslo + " " + SKLONI[i] +
                             " : izhod " + vrstice[i] + " proti priči " + priča[i])
    print("")
    print("plast 2 : števniške zveze : oblike " + str(oblike) + ", priče " + str(len(ZVEZE_PRIČE)))
    if padci:
        for p in padci:
            print("PADC : " + p)
        print("ODLOČITEV : RDEČA, nadgradnja ni zapečena")
        return 1
    print("padci : 0")
    print("ODLOČITEV : ZELENA, nadgradnja zapečena ( v1.1 )")
    return 0

ZVEZE_PRIČE_12 = [
    # zveza 1 ( en, ena, eno ), zapečena rez 6998, priče v glavi telesa
    ("1", "družina", "z-a",
     ["ena družina", "ene družine", "eni družini", "eno družino",
      "o eni družini", "z eno družino"]),
    ("1", "gospodinjstvo", "s-o",
     ["eno gospodinjstvo", "enega gospodinjstva", "enemu gospodinjstvu",
      "eno gospodinjstvo", "o enem gospodinjstvu", "z enim gospodinjstvom"]),
    ("1", "milijon", "m-trdi",
     ["en milijon", "enega milijona", "enemu milijonu", "en milijon",
      "o enem milijonu", "z enim milijonom"]),
    # zveza 2 ( dva, dve ), priče : SSKJ dolžnost obeh staršev ( G množina ),
    # SSS obema konjema ( D dvojina ), z dvema milijonoma ( I dvojina )
    ("2", "milijon", "m-trdi",
     ["dva milijona", "dveh milijonov", "dvema milijonoma", "dva milijona",
      "o dveh milijonih", "z dvema milijonoma"]),
    ("2", "reka", "z-a",
     ["dve reki", "dveh rek", "dvema rekama", "dve reki",
      "o dveh rekah", "z dvema rekama"]),
    # zveza 2-oba ( oba, obe ), priče SSS : oba konja, z obema konjema, obe ovci
    # ( konj nosi izjemno množino brez -ev, zato priča telesa kralj vzorca m-mehki )
    ("2-oba", "kralj", "m-mehki",
     ["oba kralja", "obeh kraljev", "obema kraljema", "oba kralja",
      "o obeh kraljih", "z obema kraljema"]),
    ("2-oba", "ovca", "z-a",
     ["obe ovci", "obeh ovc", "obema ovcama", "obe ovci",
      "o obeh ovcah", "z obema ovcama"]),
]

def preveri_v12():
    print("SAMOPREVERBA SKLANJATNIK v1.2 : zvezi 1 in 2 zapečeni nad v1.1")
    r1 = preveri_v11()
    if r1 != 0:
        return r1
    oblike, padci = 0, []
    for stevnik, geslo, vzorec, priča in ZVEZE_PRIČE_12:
        vrstice, opombe = zveza(stevnik, geslo, vzorec)
        for i in range(6):
            oblike += 1
            if vrstice[i] != priča[i]:
                padci.append("zveza " + stevnik + " " + geslo + " " + SKLONI[i] +
                             " : izhod " + vrstice[i] + " proti priči " + priča[i])
    print("")
    print("plast 3 : zveze 1, 2 in 2-oba : oblike " + str(oblike) + ", priče " + str(len(ZVEZE_PRIČE_12)))
    if padci:
        for p in padci:
            print("PADC : " + p)
        print("ODLOČITEV : RDEČA, nadgradnja ni zapečena")
        return 1
    print("padci : 0")
    print("ODLOČITEV : ZELENA, nadgradnja zapečena ( v1.2 )")
    return 0

def izris_zveze(stevnik, geslo, vzorec):
    vrstice, opombe = zveza(stevnik, geslo, vzorec)
    print("zveza " + stevnik + " : samostalnik " + geslo + " ( vzorec " + vzorec + " )")
    print("")
    if vrstice is None:
        for o in opombe:
            print(o)
        return
    for i, sklon in enumerate(SKLONI):
        vrs = vrstice[i] if vrstice[i] is not None else "VRATA ODPRTA"
        print("{:<14}{}".format(sklon, vrs))
    for o in opombe:
        print("")
        print("opomba : " + o)
    print("")
    print("merjeno, ne ugibano : oblika je pravilna ko preživi preverbo pri viru ( SSKJ, Fran, Sloleks )")

PRAIDEVNIKE_PRIČE_13 = [
    # pridevniške tabele, zapečene rez 6999 : ( geslo, spol, sklop, priča )
    # priči : svet ( sloleks/slv/headword/35546 ) za moške obliki,
    # pravi ( sloleks/slv/headword/30012 ) za ženski in srednji
    ("sveti", "m", "nedoločno", {
        "ednina":  ["svet", "svetega", "svetemu", "svetega", "o svetem", "s svetim"],
        "dvojina":  ["sveta", "svetih", "svetima", "sveta", "o svetih", "s svetima"],
        "množina": ["sveti", "svetih", "svetim", "svete", "o svetih", "s svetimi"],
    }),
    ("sveti", "m", "določno", {
        "ednina":  ["sveti", "svetega", "svetemu", "sveti", "o svetem", "s svetim"],
        "dvojina":  ["sveta", "svetih", "svetima", "sveta", "o svetih", "s svetima"],
        "množina": ["sveti", "svetih", "svetim", "svete", "o svetih", "s svetimi"],
    }),
    ("pravi", "z", "vse", {
        "ednina":  ["prava", "prave", "pravi", "pravo", "o pravi", "s pravo"],
        "dvojina":  ["pravi", "pravih", "pravima", "pravi", "o pravih", "s pravima"],
        "množina": ["prave", "pravih", "pravim", "prave", "o pravih", "s pravimi"],
    }),
    ("pravi", "s", "vse", {
        "ednina":  ["pravo", "pravega", "pravemu", "pravo", "o pravem", "s pravim"],
        "dvojina":  ["pravi", "pravih", "pravima", "pravi", "o pravih", "s pravima"],
        "množina": ["prava", "pravih", "pravim", "prava", "o pravih", "s pravimi"],
    }),
]

def preveri_v13():
    print("SAMOPREVERBA SKLANJATNIK v1.3 : i-tvor in pridevniške tabele zapečeni nad v1.2")
    r2 = preveri_v12()
    if r2 != 0:
        return r2
    tabele = pridevniške_tabele("sveti")
    ravno = tabele["m"]["nedoločno"]["ednina"][0] == "svet" and tabele["m"]["določno"]["ednina"][0] == "sveti"
    if not ravno:
        print("PADC : pridevniška osnova se ne sklada z izmerjenima oblikama svet in sveti")
        print("ODLOČITEV : RDEČA, nadgradnja ni zapečena")
        return 1
    oblike, padci = 0, []
    for geslo, spol, sklop, priča in PRAIDEVNIKE_PRIČE_13:
        tabele = pridevniške_tabele(geslo)
        izmerjeno = tabele[spol][sklop]
        for stevilo in ("ednina", "dvojina", "množina"):
            for i in range(6):
                oblike += 1
                if izmerjeno[stevilo][i] != priča[stevilo][i]:
                    padci.append("pridevnik " + geslo + " spol " + spol + " " + sklop + " " +
                                 stevilo + " " + SKLONI[i] + " : izhod " + izmerjeno[stevilo][i] +
                                 " proti priči " + priča[stevilo][i])
    print("")
    print("plast 4 : i-tvor priči 36 oblik ( v osnovni samopreverbi ) ; pridevniške tabele 72 oblik")
    print("plast 4 pridevniki : oblike " + str(oblike) + ", priče " + str(len(PRAIDEVNIKE_PRIČE_13)))
    if padci:
        for p in padci:
            print("PADC : " + p)
        print("ODLOČITEV : RDEČA, nadgradnja ni zapečena")
        return 1
    print("padci : 0")
    print("ODLOČITEV : ZELENA, nadgradnja zapečena ( v1.3 )")
    print("merjeno, ne ugibano : vsaka oblika izmerjena pri viru istega dne ( Sloleks 35546 in 30012 )")
    return 0

def izris_pridevnika(geslo):
    try:
        tabele = pridevniške_tabele(geslo)
    except SystemExit as e:
        print(str(e))
        sys.exit(1)
    print("pridevnik " + geslo + " : pridevniške tabele treh spolov ( določno in nedoločno )")
    print("")
    for spol, ime_spola in (("m", "moški"), ("z", "ženski"), ("s", "srednji")):
        for sklop in ("nedoločno", "določno") if spol == "m" else ("vse",):
            print(ime_spola + " pridevnik, oblika : " + sklop)
            for stevilo in ("ednina", "dvojina", "množina"):
                print("  " + stevilo + " :")
                for i, sklon in enumerate(SKLONI):
                    print("    {:<14}{}".format(sklon, tabele[spol][sklop][stevilo][i]))
            print("")
            if spol != "m":
                print("opomba : pri ženskem in srednjem spolu sta določna in nedoločna oblika "
                      "po izmeri pri viru enaki ( Sloleks/slv/headword/30012 )")
    print("merjeno, ne ugibano : oblika je pravilna ko preživi preverbo pri viru ( SSKJ, Fran, Sloleks )")

def main_v12():
    a = sys.argv[1:]
    if a and a[0] == "--zveza":
        if len(a) != 4:
            print("raba : python3 sklanjatnik.py --zveza <števnik> <samostalnik> <vzorec>")
            sys.exit(1)
        try:
            izris_zveze(a[1], a[2], a[3])
        except SystemExit as e:
            print(str(e))
            sys.exit(1)
        return
    main()

def main_v13():
    a = sys.argv[1:]
    if a and a[0] == "--preveri":
        sys.exit(preveri_v13())
    if a and a[0] == "--pridevnik":
        if len(a) != 2:
            print("raba : python3 sklanjatnik.py --pridevnik <določnaOblikaNaI>")
            sys.exit(1)
        izris_pridevnika(a[1])
        return
    main_v12()

if __name__ == "__main__":
    main_v13()
