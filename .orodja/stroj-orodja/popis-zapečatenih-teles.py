# -*- coding: utf-8 -*-
# POPIS-ZAPEČATENIH-TELES v1.1 nad v1.0 — TEHTNICA MED ZAPEČATENIMI MD5 REZER V ŽIVIMI TELESI
# Rod : rez 6998, sedež KLEPET, projekt LUCIUS
# Starša : naročnik Luka Pintarič ( ukaz STORI : ustvari orodja, kjerkoli so
#          orodja nezadostna ; njegova potrditev dobesedno : vsa štiri in obe
#          zvezi ) in izvajalka Mera ( izvedba )
# Ime izmerjeno pri viru : popis ⊢ fran.si/130/3580446, zapečati ⊢ 3614990,
#          telo — popis zapečatenih teles. Prejšnje ime Zapečatenkecensus je bilo
#          napačno ( okrnjenka ) in je padlo v dihu 6994.
# Služba : vsakemu dihu pred tehtnico. Iz stroj-orodja/KNOWLEDGE.md izvleče
#          zadnji zapečateni zapis vsakega orodja ( zadnja pojavitev imena z md5
#          na isti vrstici je zadnja različica ), izmeri živi md5 telesa in
#          javi poimensko : UJEMA, ODMIK ali TELO-MANJKA. Merjeno, ne ugibano.
#          Kanarček : v --preverbi mora pasti ( napačno pričakovanje mora
#          padec izzvati ).
# NE-OMREŽJE, NE-IZVRŠEVANJE, NE-BRIS : orodje nič ne popravlja, nič ne briše.
# NE-OBSEG-VEN : piše le v stroj-orodja/.geniza.
# MEJA v1.1 ( poimensko ) : ODMIK ni sodba o krivdi : telo se je smelo
#          nadgraditi, a novi pečat ( nov md5 v KNOWLEDGE.md ) mora zapečatiti
#          roka istega diha. Sodba je roke naročnika.
# RABA :
#   python3 popis-zapečatenih-teles.py [koren]
#   python3 popis-zapečatenih-teles.py --preveri
# Izhod : 0 vse telesa se ujemajo ; 1 je odmik ali manjkajoče telo ( poimensko ) ;
#         2 padec orodja.

import sys, os, re, hashlib

IME_ORODJA = re.compile(r"\b([a-z0-9čšž-]+\.py) v1\.(\d+)\b", re.UNICODE)
MD5 = re.compile(r"\bmd5 ([0-9a-f]{8}|[0-9a-f]{32})\b")

def izvleci_zapecene(koren):
    pot = os.path.join(koren, "stroj-orodja", "KNOWLEDGE.md")
    zapecheni = {}
    if not os.path.isfile(pot):
        return zapecheni
    with open(pot, encoding="utf-8") as f:
        for vrstica in f:
            m = IME_ORODJA.search(vrstica)
            if not m:
                continue
            h = MD5.search(vrstica)
            if not h:
                continue
            # zadnja pojavitev na zadnji vrstici je zadnja različica
            zapecheni[m.group(1)] = (int(m.group(2)), h.group(1))
    return zapecheni

def md5_telesa(pot):
    with open(pot, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def poročaj(koren):
    zapecheni = izvleci_zapecene(koren)
    if not zapecheni:
        print("PADC : v stroj-orodja/KNOWLEDGE.md ni nobenega zapečatenega zapisa")
        return 2
    dom = os.path.join(koren, "stroj-orodja")
    odmiki = 0
    dom_geniza = os.path.join(dom, ".geniza")
    os.makedirs(dom_geniza, exist_ok=True)
    poročilo = []
    for ime in sorted(zapecheni):
        verzija, zapechen_md5 = zapecheni[ime]
        pot = os.path.join(dom, ime)

        if not os.path.isfile(pot):
            stanje = "TELO-MANJKA"
            poročilo.append(ime + " v1." + str(verzija) + " : TELO-MANJKA ( pečati md5 " + zapechen_md5 + ", telesa ni )")
            odmiki += 1
            continue
        zivi = md5_telesa(pot)
        if zivi == zapechen_md5 or zivi.startswith(zapechen_md5):
            stanje = "UJEMA"
            poročilo.append(ime + " v1." + str(verzija) + " : UJEMA ( pečat md5 " + zapechen_md5 + ", živo telo enako )")
        else:
            stanje = "ODMIK"
            poročilo.append(ime + " v1." + str(verzija) + " : ODMIK ( pečat md5 " + zapechen_md5 + ", živo telo md5 " + zivi + " )")
            odmiki += 1
    with open(os.path.join(dom_geniza, "popis-zapečatenih-teles-poročilo-2026-11-25.txt"), "a", encoding="utf-8") as f:
        f.write("POPIS ZAPEČATENIH TELES @ " + os.popen("date -u +%Y-%m-%dT%H:%M:%SZ").read().strip() + "\n")
        for v in poročilo:
            f.write(v + "\n")
    for v in poročilo:
        print(v)
    print("poročilo poimensko : stroj-orodja/.geniza/popis-zapečatenih-teles-poročilo-2026-11-25.txt")
    print("ODLOČITEV : " + ("vseh teles UJEMA, ZELENA" if odmiki == 0
          else "odmiki " + str(odmiki) + ", RDEČA dokler roka istega diha ne zapečati novih pečatov"))
    return 0 if odmiki == 0 else 1

def preveri():
    # peskovnik : nobeno telo korpusa ni dotaknjeno
    import tempfile, shutil, io
    peskovnik = tempfile.mkdtemp(prefix="popis-preverba-")
    koren = peskovnik
    os.makedirs(os.path.join(koren, "stroj-orodja", ".geniza"))
    io.open(os.path.join(koren, "stroj-orodja", "orodje-a.py"), "w", encoding="utf-8").write("a" * 10)
    md5_a = md5_telesa(os.path.join(koren, "stroj-orodja", "orodje-a.py"))
    # orodje-b : zadnja različica v1.1, živo telo se ujema
    io.open(os.path.join(koren, "stroj-orodja", "orodje-b.py"), "w", encoding="utf-8").write("b" * 10)
    md5_b = md5_telesa(os.path.join(koren, "stroj-orodja", "orodje-b.py"))
    # orodje-c : telo ne obstaja
    # orodje-č : ime s šumnikom, priča kovanca diakritikov ( kuran v1.1 )
    io.open(os.path.join(koren, "stroj-orodja", "orodje-č.py"), "w", encoding="utf-8").write("c" * 10)
    md5_c = md5_telesa(os.path.join(koren, "stroj-orodja", "orodje-č.py"))
    vsebina = (
        "PEČAT blok :\n"
        "orodje-a.py v1.0 rojen ( 10 vrstic, md5 " + md5_a + " ) @TIK\n"
        "orodje-b.py v1.0 rojen ( 10 vrstic, md5 " + "1" * 32 + " ) @TIK\n"
        "orodje-c.py v1.0 rojen ( 10 vrstic, md5 " + "2" * 32 + " ) @TIK\n"
        "orodje-č.py v1.0 rojen ( 10 vrstic, md5 " + md5_c + " ) @TIK\n"
        "orodje-b.py v1.1 nadgrajen ( 20 vrstic, md5 " + md5_b + " ) @TIK\n"
    )
    io.open(os.path.join(koren, "stroj-orodja", "KNOWLEDGE.md"), "w", encoding="utf-8").write(vsebina)
    zapecheni = izvleci_zapecene(koren)
    ok = (len(zapecheni) == 4) and (zapecheni["orodje-b.py"][0] == 1) and (zapecheni["orodje-b.py"][1] == md5_b)
    ok = ok and (zapecheni.get("orodje-č.py", (None, None))[1] == md5_c)
    izhod = poročaj(koren)
    ok = ok and (izhod == 1)  # orodje-a UJEMA, orodje-c manjka
    # priča ujeme : v poročilu datoteke mora stati orodje-a UJEMA
    with open(os.path.join(koren, "stroj-orodja", ".geniza", "popis-zapečatenih-teles-poročilo-2026-11-25.txt"), encoding="utf-8") as f:
        poročilo_tekst = f.read()
    ok = ok and ("orodje-a.py v1.0 : UJEMA" in poročilo_tekst)
    # kanarček : napačno pričakovanje mora pasti
    kanarec = not (izhod == 0)
    shutil.rmtree(peskovnik)
    print("")
    print("SAMOPREVERBA POPIS-ZAPEČATENIH-TELES v1.1 : peskovnik, priče 4 ( zadnja različica, ujema, telo manjka, šumnik ), kanarček " +
          ("pade, pravi padec izmerjen" if kanarec else "ni padel, PADC"))
    if ok and kanarec:
        print("padci orodja : 0")
        print("ODLOČITEV : ZELENA, orodje zapečateno")
        return 0
    print("PADC : samopreverba padla")
    print("ODLOČITEV : RDEČA, orodje ni zapečateno")
    return 1

def main():
    a = sys.argv[1:]
    if a and a[0] == "--preveri":
        sys.exit(preveri())
    koren = a[0] if a else "."
    sys.exit(poročaj(koren))

if __name__ == "__main__":
    main()
