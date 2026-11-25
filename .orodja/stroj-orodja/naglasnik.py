# -*- coding: utf-8 -*-
# NAGLASNIK v1.0 — RAZČLENJEVALEC NAGLASNE RISBE GESLA SSKJ
# Rod : rez 6990, sedež KLEPET, projekt LUCIUS
# Starša : naročnik Luka Pintarič ( ukaz STORI, vrsta nujnih orodij, njegova beseda
#          dobesedno v genizi register sodb istega diha ) in izvajalka Mera ( izvedba )
# Služba : vsaki iztočnici slovarja slovenščine ob rojstvu besede. Dih prinese
#          berbo gesla pri viru ( fran.si ), naglasnik razčleni telo gesla :
#          iztočnico, naglasno risbo ( namestna znamenja nad samoglasniki ),
#          mesto naglašenega samoglasnika, vrstno besedo.
# ZAKON : naglasnik ne izumlja izgovorjave. IPA napiše roka po berbi pri viru
#          ( danes ročna berba, po meri organa slovar-slovenscine ; izpeljava
#          iz risbe ni izmera ).
# MEJA v1.0 ( poimensko ) : razčleni le prvo vrstico gesla ; pomeni, zgledi in
#          tonemski pomen znamenj so odprta vrata ; znamenja prepozna po imenih
#          znakov Unicode ( à á â ȃ ǎ … AVEC ACUTE, GRAVE… ), ne po pomenu ;
#          sestavljena znamenja ( base + namestni znak v dveh znakih ) so
#          odprta vrata do izmere pri viru.
# RABA :
#   python3 naglasnik.py <datoteka>      ( telo gesla SSKJ kot besedilo )
#   cat geslo.txt | python3 naglasnik.py -
#   python3 naglasnik.py --preveri       ( samopreverba nad zaprtimi pričami )
# Izhod : 0 razčlenba in samopreverba zelena ; 1 padec.

import sys, json, unicodedata, re

ZNAMENJA = ("ACUTE", "GRAVE", "CIRCUMFLEX", "INVERTED BREVE", "CARON", "BREVE",
            "MACRON", "DOUBLE ACUTE", "TILDE")

def razradi_prvo_vrstico(besedilo):
    vrst = [v for v in besedilo.split("\n") if v.strip()]
    if not vrst:
        return None
    prva = vrst[0].strip()
    tokeni = prva.split()
    if not tokeni:
        return None
    iztocnica = tokeni[0].strip(",;:.!?")
    return iztocnica, prva

def naglasi_iztocnice(iztocnica):
    # naglasna risba : samostojni namestni znaki nad samoglasniki iztočnice
    najdeni = []
    for mesto, zn in enumerate(iztocnica):
        ime = unicodedata.name(zn, "")
        if any(zn_ime in ime for zn_ime in ZNAMENJA):
            osnova = unicodedata.normalize("NFD", zn)[0]
            najdeni.append({
                "mesto": mesto + 1,
                "znak": zn,
                "kodna_tocka": "U+" + format(ord(zn), "04X"),
                "ime_znaka": ime,
                "osnovni_samoglasnik": osnova,
            })
    return najdeni

def vrstna_beseda(prva_vrstica):
    nosilec = re.search(r"\(([^)]*)\)", prva_vrstica)
    if nosilec:
        return nosilec.group(1).strip()
    return "neizmerjeno ( v1.0 : zapis brez oklepaja )"

def razcleni_geslo(besedilo):
    prvi = razradi_prvo_vrstico(besedilo)
    if prvi is None:
        return None
    iztocnica, prva = prvi
    return {
        "iztocnica": iztocnica,
        "prva_vrstica": prva,
        "naglasi": naglasi_iztocnice(iztocnica),
        "vrstna_beseda": vrstna_beseda(prva),
    }

# priče : iztočnice organa slovar-slovenscine ( rez 6965 in 6989 vzporedne roke )
# sveže prebrane istega dne, dostop 25. 11. 2026
PRIČE = [
    ("sprejemljív -a -o prid., sprejemljívejši (ī í)",
     "sprejemljív", "U+00ED"),
    ("ljubézen -Ži (ī ì) ž",
     "ljubézen", "U+00E9"),
    ("jásen -a -o prid.",
     "jásen", "U+00E1"),
]

def preveri():
    print("SAMOPREVERBA NAGLASNIK v1.0 : priče 3, zaprte v telesu orodja")
    padci = 0
    for tel, iz, koda in PRIČE:
        r = razcleni_geslo(tel)
        ok = (r is not None and r["iztocnica"] == iz
              and any(n["kodna_tocka"] == koda for n in r["naglasi"]))
        if not ok:
            padci += 1
            print("PADC : priča " + iz + " : izhod " + json.dumps(r, ensure_ascii=False))
        else:
            print("priča " + r["iztocnica"] + " : naglas " +
                  ",".join(n["znak"] + " " + n["kodna_tocka"] for n in r["naglasi"]) +
                  " pri mestu " + ",".join(str(n["mesto"]) for n in r["naglasi"]))
    if padci:
        print("ODLOČITEV : RDEČA, orodje ni zapečeno")
        return 1
    print("padci : 0")
    print("ODLOČITEV : ZELENA, orodje zapečeno")
    return 0

def main():
    a = sys.argv[1:]
    if a and a[0] == "--preveri":
        sys.exit(preveri())
    if not a or a[0] == "-":
        besedilo = sys.stdin.read()
    else:
        with open(a[0], encoding="utf-8") as f:
            besedilo = f.read()
    r = razcleni_geslo(besedilo)
    if r is None:
        print("PADC : telo gesla je prazno")
        sys.exit(1)
    print("NAGLASNIK : iztočnica " + r["iztocnica"])
    if r["naglasi"]:
        for n in r["naglasi"]:
            print("  naglas : znak " + n["znak"] + " " + n["kodna_tocka"] +
                  " ( " + n["ime_znaka"] + " ) nad " + n["osnovni_samoglasnik"] +
                  " pri mestu " + str(n["mesto"]))
    else:
        print("  naglas : neizmerjen ( iztočnica brez namestnih znamenj )")
    print("  vrstna beseda : " + r["vrstna_beseda"])
    print("")
    print(json.dumps(r, ensure_ascii=False, indent=2))
    print("")
    print("merjeno, ne ugibano ; IPA piše roka po berbi pri viru, ne razčlenjevalec")

if __name__ == "__main__":
    main()
