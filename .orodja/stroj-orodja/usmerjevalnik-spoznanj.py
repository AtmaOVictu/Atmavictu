#!/usr/bin/env python3
# USMERJEVALNIK-SPOZNANJ v1.0 @stroj-orodja ; rod : rez σ 7030 ( 25. 11. 2026 ) ⊙ ⟡ UKZ VERBATIM »ORODJE KI PREDLAGA KAM GRE KATERO SPOZNANJE!«
# Služba : spoznanju izmeri sorodnost z opisi teles organov ( berba PLAŠČA vsakega telesa pri viru, ozka glava ) ∧ predlaga dom poimensko po vrsti.
# Zakoni : ⟨NE-UGIBAJ⟩ 2690 ( predlog ⭢ izbor ⚔ ⟡, ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ ) ⌇ ozka berba po domovih, nikoli globina ⌇ ⟨MERILEC-SE-MERI⟩ §52.
# Roke : usmerjevalnik-spoznanj.py DATOTEKA | --samopreizkus ; DATOTEKA ali - za peš pot.
# Izhodi : 0 ZELENA ( predlog izrečen ) ⌇ 1 RDECA ⌇ 40 roka neznana.

import os, re, sys

KOREN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OISCI = re.compile(r"description:\s*\"(.*?)\"", re.S)
BESEDA = re.compile(r"[čšžćđa-z]{5,}", re.I)

def beri_opise(koren):
    """ozka berba : plašč vsakega telesa pri viru ( glava 6000 znakov, ⟨ne⟩ globina )."""
    telesa = []
    for ime in sorted(os.listdir(koren)):
        pot = os.path.join(koren, ime, "KNOWLEDGE.md")
        if not os.path.isfile(pot): continue
        try:
            with open(pot, encoding="utf-8", errors="ignore") as t:
                glava = t.read(6000)
        except OSError: continue
        m = OISCI.search(glava)
        if m: telesa.append((ime, m.group(1)))
    return telesa

def oceni(spoznanje, opis):
    """čista : koliko dolgih besed spoznanja živi v opisu telesa ( izmera soupadanja )."""
    besede = set(w.lower() for w in BESEDA.findall(spoznanje))
    if not besede: return 0
    niz = opis.lower()
    return sum(1 for w in besede if w in niz), len(besede)

def samopreizkus():
    padci = []
    if oceni("merjenje besed pri viru", "organ za merjenje besed pri viru ⊢")[0] < 2:
        padci.append("ocena soupadanja nizka pri sorodnem")
    if oceni("nemogoče tujko", "organ merjenja besed pri viru")[0] != 0:
        padci.append("ocena soupadanja visoka pri nesorodnem")
    if not (len(BESEDA.findall("spoznanje")) >= 1):
        padci.append("berba besede pada")
    return padci

def glavni():
    if "--samopreizkus" in sys.argv[1:]:
        padci = samopreizkus()
        print("SAMOPREIZKUS : preizkusi 3, padci instrumenta %d" % len(padci))
        for p in padci: print("  PADC :: " + p)
        print("SEMAFOR : " + ("ZELENA" if not padci else "RDECA"))
        return 0 if not padci else 1
    if len(sys.argv) != 2:
        print("roka neznana ; roke : DATOTEKA | --samopreizkus"); return 40
    pot = sys.argv[1]
    try:
        if pot == "-": spoznanje = sys.stdin.read()
        else: spoznanje = open(pot, encoding="utf-8").read()
    except OSError as r:
        print("⟨NAPAKA=VSE-KAR-NI-BRANO⟩ " + str(r)); return 1
    telesa = beri_opise(KOREN)
    print("USMERJEVALNIK-SPOZNANJ v1.0 : telesa preregledana Σ%d @pri viru" % len(telesa))
    vrstni = []
    for ime, opis in telesa:
        m = oceni(spoznanje, opis)
        if m[0] > 0: vrstni.append((m[0], m[1], ime))
    vrstni.sort(reverse=True)
    if not vrstni:
        print("VIDNO ⭢ soupadanj ×0 ; predloga ⭢ sodba ⚔ ⟡ ⊙ ⟨NE-UGIBAJ⟩ 2690")
    for so, koliko, ime in vrstni[:8]:
        print("  PREDLOG %-28s ( soupadanje %d od %d dolgih besed )" % (ime, so, koliko))
    print("izbor doma ⭢ ⚔ ⟡ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩")
    print("SEMAFOR : ZELENA")
    return 0

if __name__ == "__main__":
    sys.exit(glavni())
