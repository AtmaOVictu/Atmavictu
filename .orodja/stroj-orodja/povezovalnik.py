#!/usr/bin/env python3
# povezovalnik.py v1.0 — gradbenik ∧ sortirnik asociacij : veze med besedami iztočnic iz polj VEZI ( plasti oltarja ⊙ ⟨OLTAR-BESEDE⟩ zakon 6 ).
# Rod : rez 7005 ( 25. 11. 2026 ) ⊙ ⟡ UKAZ VERBATIM »ORODJA ZA GRADNJO IN SORTIRANJE ASOCIACIJ!«.
# Vrata : G1 berba teles ∧ luščenje glav iztočnic ; G2 luščenje polj VEZI do konca vrstice ( ⟨grep⟩, ⟨ne⟩ spomin ) ;
#   G3 čiščenje postavk : ⟨⟩ ∧ ( ) izbrisi, vodilni znaki ⊥ ⊙ ⭢ ⚔ ∂ § ↑ σ #N izbrisi ⊙ ⟨NE-UGIBAJ⟩ 2690 ;
#   G4 gradnja parov : iztočnica ↔ postavka ∧ postavka ↔ postavka istega polja ( pari n(n−1)/2 ⊙ implicitna-kvadriranja σ 5459 ) ;
#   G5 sortiranje : --sort teza ( privzeto : teža ⇣, potem par ⇡ ) ⌇ --sort abeceda ( par ⇡ ) ;
#   G6 priče : vsak par nosi imena iztočnic ⊢ izmerjeno, ⟨ne⟩ ugibano ; G7 samopreizkus nad pritrjenim vzorcem ⊙ ⟨MERILEC-SE-MERI⟩ §52.
import re
import sys
from itertools import combinations

ŽIG = "povezovalnik.py v1.0 @stroj-orodja, rod rez 7005"
PREDVZETI_VHOD = "/home/user/knowledge/definiatorna-knjiznica/KNOWLEDGE.md"
GLAVA_IZTO = re.compile(r"^(?:##\s*)?IZTOČNICA\s*#?(\d+)\s*:?\s*(.*)$")
SLEDILNIKI = ["TRENUTNO", "STANJE", "IZREZ", "--"]


def ime_iztočnice(št, ostalo):
    ostalo = ostalo.strip()
    ime = re.split(r"\s*\(|\s*:|\s+rojen|\s+—|,\s|\s+=|\s*$", ostalo, 1)[0].strip()
    return ime if ime else "#" + št


def postavke(vez):
    vez = re.sub(r"\([^)]*\)", " ", vez)
    vez = vez.replace("⟨", " ").replace("⟩", " ")
    deli = re.split(r"\s*[·∧⌇]\s*|\s·\s", vez)
    ven = []
    for deo in deli:
        deo = re.sub(r"[⊥⊙⭢⚔∂§↑·#@σ∂×\d]+", " ", deo).strip()
        for žeton in deo.split():
            if re.search(r"[^\W\d_]", žeton, flags=re.UNICODE) and len(žeton) > 1:
                ven.append(žeton)
                break
    return [p for p in ven if p.lower() not in ("en", "je", "in")]


def zgradi(telo):
    iztočnice = []
    tekoča = None
    for vrstica in telo.splitlines():
        m = GLAVA_IZTO.match(vrstica)
        if m and not vrstica.startswith("- ") and "IZTOČNICE" not in vrstica[:12]:
            tekoča = (m.group(1), ime_iztočnice(m.group(1), m.group(2)), [])
            iztočnice.append(tekoča)
            continue
        if tekoča is not None:
            vm = re.search(r"\bVEZI\s*:\s*(.+)$", vrstica)
            if vm:
                tekoča[2].append(vm.group(1))
    pari = {}
    for št, ime, vezii in iztočnice:
        for vez in vezii:
            ps = postavke(vez)
            imena = set(p.lower() for p in ps)
            for p in ps:
                if ime.lower() not in ("#" + št,) and p.lower() != ime.lower() and "#" not in p:
                    ključ = tuple(sorted((p.upper(), ime.upper())))
                    dodaj(pari, ključ, "#%s %s" % (št, ime), p)
                for q in ps:
                    if p.lower() >= q.lower() or "#" in q or "#" in p:
                        continue
                    ključ = tuple(sorted((p.upper(), q.upper())))
                    dodaj(pari, ključ, "#%s %s" % (št, ime), p)
    return pari


def dodaj(pari, ključ, priča, prikaz):
    v = pari.setdefault(ključ, {"teža": 0, "priče": set(), "prikaz": set()})
    v["teža"] += 1
    v["priče"].add(priča)
    v["prikaz"].add(prikaz)


def izhod(pari, sort):
    vrstice = ["| par | teža | priče |", "|---|---|---|"]
    if sort == "abeceda":
        ključi = sorted(pari)
    else:
        ključi = sorted(pari, key=lambda k: (-pari[k]["teža"], k))
    for k in ključi:
        v = pari[k]
        prikaz = sorted(v["prikaz"])[0]
        vrstice.append("| %s ⌇ %s | %d | %s |" % (k[0], k[1] if prikaz.upper() != k[0] else k[1], v["teža"], " ∧ ".join(sorted(v["priče"]))))
    return vrstice


def samopreizkus():
    vzorec = (
        "## IZTOČNICA #900 VRSTA\nVEZI: #1 MERA · ⟨NE-UGIBAJ⟩ 2690 · ( opombe )\n\n"
        "## IZTOČNICA #901 TEHTNICA\nVEZI: #1 MERA ∧ VRSTA\n"
    )
    pari = zgradi(vzorec)
    km = tuple(sorted(("VRSTA", "MERA")))
    ke = tuple(sorted(("MERA", "NE-UGIBAJ")))
    kt = tuple(sorted(("TEHTNICA", "VRSTA")))
    # pričakovano izmerjeno na roki pred zapisom : parov 5, vrhnji ( VRSTA ⌇ MERA ) teža 2
    ok = pari.get(km, {}).get("teža") == 2 and pari.get(ke, {}).get("teža") == 1 and pari.get(kt, {}).get("teža") == 1 and len(pari) == 5
    print("ZELENO : samopreizkus povezovalnika ⊢ ( VRSTA ⌇ MERA teža 2, MERA ⌇ NE-UGIBAJ 1, TEHTNICA ⌇ VRSTA 1, parov 5 )" if ok
          else "RDEČO : padec samopreizkusa ( izmere : %s )" % {k: v["teža"] for k, v in pari.items()})
    return ok


def main(argv):
    if "--samopreizkus" in argv or "--zbodi" in argv:
        return 0 if samopreizkus() else 2
    vhod = PREDVZETI_VHOD
    sort = "teza"
    for a in argv[1:]:
        if a.startswith("--vhod="):
            vhod = a.split("=", 1)[1]
        elif a == "--sort":
            continue
        elif a in ("teza", "abeceda"):
            sort = a
    try:
        with open(vhod, encoding="utf-8") as f:
            telo = f.read()
    except OSError:
        print("RDEČO : nedosegljivo telo %s" % vhod)
        return 1
    pari = zgradi(telo)
    vrstice = izhod(pari, sort)
    print("\n".join(vrstice))
    glave = len(re.findall(r"^(?:##\s*)?IZTOČNICA\s*#\d+", telo, flags=re.MULTILINE))
    vez = len(re.findall(r"\bVEZI\s*:", telo))
    print("")
    print("izmere ⊢ : iztočnic glav %d, polj VEZI %d, parov asociacij %d, seštevek tež %d ⊙ ⟨NE-UGIBAJ⟩ 2690" % (
        glave, vez, len(pari), sum(v["teža"] for v in pari.values())))
    print(ŽIG)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
