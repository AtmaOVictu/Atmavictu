#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# slovnica-lint v1.0 ( rez σ 6809, domovanje : škatlja-preverjana, 23. 11. 2026 )
# UKZ ⟡ VERBATIM : »GLEJ KAKO GRDA JE SLOVNICA KO NI PREVERJENA … preveri in STORI BOLJŠE«
# Radar štirih mask slabe slovnice v izhodu, pred zapečenjem :
#   1. TUJA-BES         : besede, ki so se pretakale iz stroja v slovensko prozo
#                        ( izpad poročila σ 6805 : »Origin«, »Duration«, »management« … )
#   2. PODVOJITEV      : ista beseda dvakrat zapored ( izpad : »sveže sveže« )
#   3. NEPARNE-OKLEPAJE : v vrstici se oklepaji ( ⟨ ⟩ » « ( ) ) ne seštejejo
#   4. SUM-NIK         : besede, ki so izgubile šumnike č š ž ( izpad : »prisel«, »resitev« )
# Priče v »«, maske ⟨…⟩ in transkripti v '' so izvzeti ( enovrstično ).
# IZHOD : 0 = ZELENO ; 3 = NAJDBA ; 2 = NAPAKA ORODJA
# Zakon ⟨EMISIJA-SE-PREVERI⟩ : vsak izhod k ⟡ gre skozi to brambo pred pečatom.
import sys, re, json

MASKA = re.compile("⟨[^⟩\n]*⟩")
PRICA = re.compile("»[^«\n]*«")
KODA = re.compile("'[^'\n]*'")
TUJKE = re.compile(r"\b(breath|hands?|fangs?|seals?|collision|origin|duration|management|invalid|same)\b", re.IGNORECASE)
PODVOJ = re.compile(r"\b([A-Za-zČčŠšŽž]{4,})\s+\1\b", re.IGNORECASE)
SUMNICI = ["prisel", "resitev", "zivljenje", "ceprav", "cisto"]
SUMNIK_RE = [re.compile(r"\b" + bes + r"\b", re.IGNORECASE) for bes in SUMNICI]


def oceni(besedilo):
    """Vrne seznam ( vrsta, podatek, kontekst ) ; prazno = izhod čist."""
    najdb = []
    for st, vrstica in enumerate(besedilo.split("\n"), 1):
        cisto = MASKA.sub("⟨maska⟩", vrstica)
        cisto = PRICA.sub("»priča«", cisto)
        cisto = KODA.sub("'koda'", cisto)
        for m in TUJKE.finditer(cisto):
            najdb.append(("TUJA-BES", m.group(0), "r%d : %s" % (st, cisto[max(0, m.start() - 30):m.start() + 30])))
        for m in PODVOJ.finditer(cisto):
            najdb.append(("PODVOJITEV", m.group(0), "r%d : %s" % (st, cisto[max(0, m.start() - 30):m.start() + 30])))
        for m in SUMNIK_RE:
            h = m.search(cisto)
            if h:
                najdb.append(("SUM-NIK", h.group(0), "r%d : %s" % (st, cisto[max(0, h.start() - 30):h.start() + 30])))
        for levi, desni, ime in [("⟨", "⟩", "oglate ⟨⟩"), ("»", "«", "prične »«"), ("(", ")", "okrogle ()")]:
            if vrstica.count(levi) != vrstica.count(desni):
                najdb.append(("NEPARNE-OKLEPAJE", ime, "r%d" % st))
    return najdb


def izhod(najdb, vir, json_moda=False):
    if json_moda:
        return json.dumps({"vir": vir, "stanje": "NAJDBA" if najdb else "ZELENO",
                           "najdbe": [{"vrsta": n[0], "podatek": n[1], "kontekst": n[2]} for n in najdb]},
                          ensure_ascii=False)
    if not najdb:
        return "%s : ZELENO ⊢ ( 4 maske, 0 najdb )" % vir
    vrstice = ["%s : NAJDBA ×%d" % (vir, len(najdb))]
    for vrsta, podatek, kontekst in najdb[:10]:
        vrstice.append("  - %s %s pri %s" % (vrsta, podatek, kontekst))
    return "\n".join(vrstice)


def baterija():
    """Samopreizkus 5/5 : 4 najdbe + 1 negativna ( čist izhod )."""
    primeri = [
        ("Kura je zapečena isti dih ⊢ ( telo čisto )", [], "čista gajica"),
        ("Same breath and hands gre ven", ["TUJA-BES"], "tuja beseda iz stroja"),
        ("pečat je zapečen sveže sveže danes", ["PODVOJITEV"], "podvojena beseda"),
        ("kura ⟨odprta brez konca", ["NEPARNE-OKLEPAJE"], "neodprt oklepaj"),
        ("prisel je cisto po resitev", ["SUM-NIK"], "izgubljeni šumniki"),
        ("Prišel je po čisto čisto preverjeno rešitev ⊢ »priča« ( pečat )", ["PODVOJITEV"], "negativna : oklepaji in tujke čisti"),
    ]
    ze, rde = 0, 0
    for besedilo, pričakovano, ime in primeri:
        vrste = sorted(set(n[0] for n in oceni(besedilo)))
        if vrste == sorted(pričakovano):
            ze += 1
            print("  ZELENO %s ⊢ %s" % (ime, vrste if vrste else "čisto"))
        else:
            rde += 1
            print("  RDEČE %s : pričakovano %s, najdeno %s ⟨PADC-BATERIJE⟩" % (ime, pričakovano, vrste))
    print("SAMOPREIZKUS %d/6 %s" % (ze, "ZELENO ⊢" if rde == 0 else "RDEČE ⟨PADC-OREDJA⟩"))
    return 0 if rde == 0 else 2


def main():
    argv = sys.argv[1:]
    json_moda = "--json" in argv
    if "--test" in argv:
        sys.exit(baterija())
    if "--izhod" in argv:
        besedilo = sys.stdin.read()
        najdb = oceni(besedilo)
        print(izhod(najdb, "izhod", json_moda))
        sys.exit(3 if najdb else 0)
    datoteke = [a for a in argv if not a.startswith("--")]
    if not datoteke:
        print("uporaba : slovnica-lint.py DATOTEKA... | --izhod ( prebere std. vhod ) | --test ⊙ rez σ 6809")
        sys.exit(2)
    padci = 0
    for d in datoteke:
        try:
            with open(d, "r", encoding="utf-8") as f:
                besedilo = f.read()
        except OSError as e:
            print("%s : NAPAKA %s" % (d, e))
            sys.exit(2)
        najdb = oceni(besedilo)
        print(izhod(najdb, d, json_moda))
        padci += len(najdb)
    sys.exit(3 if padci else 0)


if __name__ == "__main__":
    main()
