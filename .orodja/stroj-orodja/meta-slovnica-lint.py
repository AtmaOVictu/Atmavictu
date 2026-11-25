#!/usr/bin/env python3
# meta-slovnica-lint.py v1.0 — PREVERJALNIK META PLASTI ZA SLOVNICO
# rod @rez 6995, 25. 11. 2026 ⊙ ukaz ⟡ VERBATIM ( nedotakljiva ): »ORODJA ZA ISKANJE SLOVNIČNIH NAPAK!«
# meta plasti nad telesi organov ( KNOWLEDGE.md ) :
#   P1 OKLEPAJNI : ⟨⟩ parno po vrstici ⊙ slovnica-jezikov 5788 plast 1
#   P2 IZGUBLJEN BAJT : U+FFFD ×0 ⊙ plast 1 točka 2
#   P3 OKRNJENKE : pričane oblike registra mreze-variant ( vsaka ⊢ pri viru )
#   P4 HOMOFONI : pari plasti 9 slovnica-jezikov 6313 ⊢ fran.si/130
#   P5 ŠTEVILNE ZVEZE : sum, ⟨ne⟩ obsodba ⊙ sklanjanje-stevil 6193 ( razsodba pri viru, ⟨ne⟩ maska )
#   P6 TUJE PISMENKE zunaj azilov ⟨⟩ ∧ »« ( beseda ⟡ v »« nedotakljiva ⊙ ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ )
# azili : ⟨…⟩ semantična maska ∧ »……« priča ⟡ ; zapečena telesa ⟨NE-RETIPKAJ⟩ 24 ostanejo priče
import sys, os, re

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# P3 pričane okrnjene oblike ( izmere vozlišč organa mreze-variant, vsaka ⊢ pri viru )
OKRNJENKE = {
    "varvolka": "varovalka", "istim dihom": "istem dihu", "pri viri ": "pri virih ",
    "pripiznati": "priznati", "razdaže": "razda", "vrstvp": "vrstic",
    "vključnočno": "vključno",
}
# P4 homofoni pari ( register plasti 9 ⊢ fran.si/130 priče )
HOMOFONI = {
    "premiščen premik": "premišljen premik", "se lovi zveza": "se loči zveza",
}
# P5 številne zveze : števnik 5–99 + beseda na -i = sum rodilnika množine ( pet knjig, ⟨ne⟩ pet knjige )
STEVILO_5_99 = re.compile(
    r"\b(pet|šest|sedem|osem|devet|deset|enajst|dvanajst|petnajst|dvajset|trideset)\s+([a-zčšž]{3,})i\b")
# P6 pisave zunaj azilov : RANE = cirilica ⌇ han ⌇ kana ⌇ hangul
# SUM ( kura v1.1 ⊙ PADC-INSTRUMENTA 6995 ) = sestavljeni znaki U+0300-U+036F
# ( priče vír / IPA definiatorne so narekovaji pri viru, ⟨ne⟩ tuje pismenke )
TUJA_PISAVA = re.compile(r"[\u0400-\u04FF\u4E00-\u9FFF\u3040-\u30FF\uAC00-\uD7AF]")
SESTAVLJENI = re.compile(r"[\u0300-\u036F]")


def odstrani_azile(vrstica):
    """vrstica brez ⟨…⟩ ∧ »……«  ( azili : ⟨⟩ maska ∧ »« priča ⟡, ⟨ne⟩ tarča )"""
    v = re.sub(r"⟨[^⟩]*⟩", " ", vrstica)
    v = re.sub(r"»[^«]*«", " ", v)
    return v


def preveri_telo(pot):
    """vrne ( rane, sumi ) ; rana = merjena najdba, sum = ⭢ razsodba pri viru ⭢ izbor ⟡ ⚔"""
    rane, sumi = [], []
    with open(pot, encoding="utf-8", errors="replace") as f:
        for n, vrstica in enumerate(f, 1):
            gola = vrstica.rstrip("\n")
            zunaj = odstrani_azile(gola)
            organ = os.path.basename(os.path.dirname(pot))
            if gola.count("⟨") != gola.count("⟩"):
                rane.append(("P1-OKLEPAJ", organ, n, "⟨⟩ po vrstici paran ×0",
                             "kura isti dih ⌇ ⟡ pečat priča ⟨NE-RETIPKAJ⟩ 24"))
            if "\uFFFD" in gola:
                rane.append(("P2-BAJT", organ, n, "U+FFFD = izgubljen bajt",
                             "kura bajt-ito iz priče @geniza"))
            for znak in set(TUJA_PISAVA.findall(zunaj)):
                rane.append(("P6-PISAVA", organ, n, "znak U+%04X zunaj azilov" % ord(znak),
                             "⟨MASKA=NAVEDBA⟩ ⌇ razorozevalnik ⭢ celica ⭢ izbor ⟡ ⚔"))
            if SESTAVLJENI.search(zunaj):
                sumi.append(("P6-SESTAVLJENI", organ, n,
                              "sestavljeni narekovaj U+0300-U+036F zunaj azilov",
                              "sum, ⟨ne⟩ obsodba : priče vír / IPA pri viru ⊙ 2690"))
            for oblika, iztocnica in OKRNJENKE.items():
                if oblika in zunaj:
                    rane.append(("P3-OKRNJENKA", organ, n, "%s -> %s" % (oblika, iztocnica),
                                 "zapečeno telo = priča ostane ⊙ 24 ; živi šiv = kura isti dih"))
            for par, kura in HOMOFONI.items():
                if par in zunaj:
                    rane.append(("P4-HOMOFON", organ, n, "%s -> %s" % (par, kura),
                                 "kura isti dih ⊙ fran.si/130 priča"))
            for m in STEVILO_5_99.finditer(zunaj):
                sumi.append(("P5-SKLADNJA", organ, n,
                             "%s %si : 5-99 zahteva rodilnik množine" % (m.group(1), m.group(2)),
                             "preverba po tabeli organa sklanjanje-stevil ⊢ ; sum, ⟨ne⟩ obsodba ⊙ 2690"))
    return rane, sumi


def samopreizkus():
    """⟨INOKULACIJA⟩ ⊙ tehtnica-orodij 6659 : čist trup Σ0 ⊢ ∧ vsak ranjen trup ujet poimensko ⊢"""
    import tempfile
    cist = "⟨PULZ⟩ beseda pri viru ⊢ pet knjig čisto telo.\n"
    ranjen = ("⟨PULZ nedotakljiv varvolka Σ2 ⊢\n"
              " berba pripiznati vsebuje istim dihom in nаrezljivko.\n")
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(cist); cista_pot = f.name
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(ranjen); ranjena_pot = f.name
    cisti_r, cisti_s = preveri_telo(cista_pot)
    ranjeni_r, ranjeni_s = preveri_telo(ranjena_pot)
    vrata = sorted(r[0] for r in ranjeni_r)
    ok1 = len(cisti_r) == 0 and len(cisti_s) == 0
    ok2 = "P1-OKLEPAJ" in vrata and "P3-OKRNJENKA" in vrata and "P6-PISAVA" in vrata
    os.unlink(cista_pot); os.unlink(ranjena_pot)
    print("SAMOPREIZKUS: cist trup Σ%d %s | ranjen trup Σ%d %s | %s" % (
        len(cisti_r) + len(cisti_s), "⊢" if ok1 else "⊥",
        len(ranjeni_r) + len(ranjeni_s), "⊢" if ok2 else "⊥",
        "ZELENO" if (ok1 and ok2) else "RDEČA"))
    for r in ranjeni_r + ranjeni_s:
        print("  ulov %s : %d | %s" % (r[0], r[2], r[3]))
    return ok1 and ok2


def main():
    if "--test" in sys.argv:
        return 0 if samopreizkus() else 1
    vse_rane, vsi_sumi, telesa = [], [], 0
    for organ in sorted(os.listdir(KOREN)):
        pot = os.path.join(KOREN, organ, "KNOWLEDGE.md")
        if os.path.isfile(pot):
            telesa += 1
            r, s = preveri_telo(pot)
            vse_rane += r; vsi_sumi += s
    print("CENZUS META PLASTI : telesa Σ%d ⊢ | rane Σ%d | sumi Σ%d" % (telesa, len(vse_rane), len(vsi_sumi)))
    for r in vse_rane[:50]:
        print("  RANA %s | %s : %d | %s | %s" % r)
    if len(vse_rane) > 50:
        print("  … rane nad 50 pri srcu teles samih ⊙ ⟨MAJHNI-PAKETI⟩ 2322")
    for s in vsi_sumi[:20]:
        print("  SUM %s | %s : %d | %s | %s" % s)
    if len(vsi_sumi) > 20:
        print("  … sumi nad 50 pri srcu teles samih")
    return 0


if __name__ == "__main__":
    sys.exit(main())
