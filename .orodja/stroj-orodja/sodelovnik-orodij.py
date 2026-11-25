#!/usr/bin/env python3
# SODELOVNIK-ORODIJ v1.0 - izmera sodelovanja podobnih teles : rodovine po imenskih korenih, verige po skupnih pričah.
# Rod : rez sigma 7026 ( 25. 11. 2026 ) @stroj-orodja ; ukaz naročnika VERBATIM, beseda nedotakljiva :
#   »ORODJA KI SODELUJEJO MED SEBOJ KER SO PODOBNA!« ( devet bratskih ukazov istega diha je pokritih z
#   živečimi telesi s pričami — popis pokritja živi v atomu diha @protokol-prenosnika/.geniza )
# Luknja izmerjena pri viru ( ⊢ ) : telo, ki bi merilo podobnost teles ∧ njihovo sodelovanje, ×0 ;
#   standard diha 7015 nosi dosje vsakega orodja ( ČEMU ⌇ ZAKAJ ⌇ KDAJ UDELEŽENO ), a ne izmeri sorodnosti —
#   to orodje je kura te luknje.
# Zakoni : ⟨NE-UGIBAJ⟩ 2690 ( imena in telesa se berejo pri viru ob vsakem zagonu, nikoli iz spomina )
#   ⌇ ⟨MERILEC-SE-MERI⟩ §52 ( samopreizkus čistih funkcij ) ⌇ ⟨PADC-ŠIROKA-BRBA⟩ ( berba le poimensko
#   po domovih teles, ena mapa, nikoli po celem prostoru ).
# Roke :
#   sodelovnik-orodij.py               -> izmera rodovin ∧ verig @stroj-orodja, izpis v slovenščini
#   sodelovnik-orodij.py --samopreizkus -> preizkus čistih funkcij na izmisljenih imenih
# Izhodi : EXIT 0 = ZELENA ( izmera prosta padcev ) ⌇ 1 = RDECA ( padec instrumenta ) ⌇ 40 = roka neznana.

import os, re, sys

VERZIJA = "v1.0"
DOM = os.path.dirname(os.path.abspath(__file__))

# rodovine po korenu imena ( kanon korenov, izmere pri viru ) : podobna telesa nosijo sorodna imena
RODOVINE = [
    ("PREVAJALSKA", ("prevajalnik", "naslovnik", "locirnik", "prevod", "slovarnik")),
    ("CENZUSNA", ("cenzus",)),
    ("PREGLEDALNA", ("lint", "varuh")),
    ("TEHTNIČNA", ("tehtnica", "sodnik", "vratar")),
    ("OSCILATORNA", ("oscilnik",)),
    ("ŠTEVILSKA", ("stevilo", "stevilovrstnik")),
    ("POPRAVILNA", ("popravenik", "izpostavnik", "rehabilitac")),
    ("SIMBOLNA", ("znak", "gajica", "simbol", "kletk")),
]

NAVERIGE = "verige sodelovanja ( skupne priče : dve ali več teles bereta isto telo-pričo )"


def rodovine_imen(imena):
    """čista : dane imena razvrsti v rodovine po korenu ; nepojavljena imena ostanejo pri POIMENSKO prostih."""
    razdelitev = []
    for ime_rodovine, koreni in RODOVINE:
        cleni = []
        for ime in imena:
            niz = ime.lower()
            if any(koren in niz for koren in koreni):
                cleni.append(ime)
        if cleni:
            razdelitev.append((ime_rodovine, cleni))
    prosta = [i for i in imena if not any(k in i.lower() for _, ks in RODOVINE for k in ks)]
    return razdelitev, prosta


def priče_teles(karta_telem_pric):
    """čista : iz karte telo -> množica prič vrne navzkrižne priče ( priča -> telesa ) s številom ≥ 2."""
    from collections import defaultdict
    prica_telesa = defaultdict(list)
    for telo, price in karta_telem_pric.items():
        for prica in price:
            prica_telesa[prica].append(telo)
    return {p: sorted(t) for p, t in prica_telesa.items() if len(t) >= 2}


def izmera(dom=DOM):
    """berba poimenska po enem domu : telesa ∧ njihovi sklepi na priče ( .tsv .json .md .awk v istem domu )."""
    imena = []
    karta = {}
    for ime in sorted(os.listdir(dom)):
        pot = os.path.join(dom, ime)
        if not os.path.isfile(pot) or not (ime.endswith(".py") or ime.endswith(".sh")):
            continue
        imena.append(ime)
        sodelavniki = set()
        try:
            with open(pot, encoding="utf-8", errors="ignore") as telo:
                vsebina = telo.read()
        except OSError:
            return None, None, "pocena telesa :: " + ime
        for zadetek in re.findall(r"[\w.-]+\.(?:tsv|json|md|awk)", vsebina):
            if zadetek != ime and os.path.isfile(os.path.join(dom, zadetek)):
                sodelavniki.add(zadetek)
        karta[ime] = sorted(sodelavniki)
    return imena, karta, None


def samopreizkus():
    """preizkus čistih funkcij na izmisljenih imenih ( MERILEC-SE-MERI §52 )."""
    izmisljena = ["avtomatski-prevajalnik.py", "naslovnik.py", "gajica-sodnik.py",
                  "oscilnik-besede.py", "zustvar.py"]
    razdelitev, prosta = rodovine_imen(izmisljena)
    rodovine = dict(razdelitev)
    padci = []
    if rodovine.get("PREVAJALSKA") != ["avtomatski-prevajalnik.py", "naslovnik.py"]:
        padci.append("rodovina prevajalska napacna")
    if rodovine.get("OSCILATORNA") != ["oscilnik-besede.py"]:
        padci.append("rodovina oscilatorna napacna")
    if prosta != ["zustvar.py"]:
        padci.append("prosta imena napacna")
    karta = {"a.py": ["skupna.tsv", "samo-a.tsv"], "b.py": ["skupna.tsv"], "c.py": []}
    verige = priče_teles(karta)
    if set(verige) != {"skupna.tsv"} or verige["skupna.tsv"] != ["a.py", "b.py"]:
        padci.append("veriga skupne price napacna")
    return padci


def glavni():
    if "--samopreizkus" in sys.argv[1:]:
        padci = samopreizkus()
        print("SAMOPREIZKUS : preizkusi 4, padci instrumenta %d" % len(padci))
        for p in padci:
            print("  PADC :: " + p)
        print("SEMAFOR : " + ("ZELENA" if not padci else "RDECA"))
        return 0 if not padci else 1
    if sys.argv[1:] not in ([], ["--izpis"]):
        print("roka neznana ; roke : ( prazna ) | --samopreizkus")
        return 40
    imena, karta, rana = izmera()
    if imena is None:
        print("⟨NAPAKA=VSE-KAR-NI-BRANO⟩ " + rana)
        return 1
    print("SODELOVNIK-ORODIJ %s : telesa izmerjena pri viru Σ%d" % (VERZIJA, len(imena)))
    razdelitev, prosta = rodovine_imen(imena)
    for ime_rodovine, cleni in razdelitev:
        print("  RODOVINA %-13s ×%d : %s" % (ime_rodovine, len(cleni), ", ".join(cleni)))
    print("  POIMENSKO PROSTA     ×%d ( brez korena kanona ; ⟨NE-UGIBAJ⟩ 2690 : ne sodim )" % len(prosta))
    verige = priče_teles(karta)
    print(NAVERIGE + " : ×%d" % len(verige))
    for prica in sorted(verige):
        print("  PRIČA %-28s : %s" % (prica, ", ".join(verige[prica])))
    print("SEMAFOR : ZELENA")
    return 0


if __name__ == "__main__":
    sys.exit(glavni())
