# -*- coding: utf-8 -*-
# VRATAR v1.0 — DNEVNIK VRATIŠČ VIROV, KJER ŽIVIJO BERBE IZMER
# Rod : rez 6998, sedež KLEPET, projekt LUCIUS
# Starša : naročnik Luka Pintarič ( ukaz STORI : ustvari orodja, kjerkoli so
#          orodja nezadostna ; njegova potrditev dobesedno : vsa štiri in obe
#          zvezi ) in izvajalka Mera ( izvedba )
# Ime izmerjeno pri viru : vratar ⊢ fran.si/130/3611971 ( kdor poklicno
#          nadzoruje vstopanje in izstopanje skozi vhodna vrata ) — beseda
#          pri viru, ne kovanec
# Služba : vsaka meritev vira ( dostop, zapor, preusmeritev ) dobi vrstico
#          dnevnika : TIK, vir, stanje, priča. Orodje samo zapisuje ( zakon
#          tehtnice-orodij : roka meri mrežo, orodje zapisuje stanje, NE-OMREŽJE ).
#          Stanja : ZADIHA ( vir je odgovoril ), ZAPOR ( vir je odgovoril ne :
#          izhod 000, pretekel pogoj ), PREUSMERITEV ( vir je dejal drugamo ).
# ZAPEČENA VRATA sklanjatnika ( dih 6994, priče dostop 25. 11. 2026 ) :
#          zveza en-ena-eno ( SSKJ geslo en, rodilnik ženske oblike ene izmerjen
#          v celotnem besedilu, zadetkov 262 ), zveza dva-dve-oba-obe ( SSKJ
#          glavi gesel dva in oba, SSS glavni števniki ).
# ODPRTA VRATA sklanjatnika : i-tvor ( miš oblike : Sloleks, kdor diha ),
#          pridevniške tabele ( ucko in Sloleks, kdor diha ).
# NE-OMREŽJE : orodje samo ne bere mreže, stanja nosi roka.
# NE-BRIS : dnevnik se vedno samo dopolnjuje. NE-OBSEG-VEN : piše le
#          stroj-orodja/.geniza. NE-IZVRŠEVANJE : ne odpira vrat, ne zapečuje.
# Kanarček : v --preverbi mora pasti ( napačno pričakovanje mora padec izzvati ).
# RABA :
#   python3 vratar.py zapis VIR STANJE [PRIČA ...]   ( TIK izmeri orodje )
#   python3 vratar.py stanja                        ( zadnje stanje vsakega vira )
#   python3 vratar.py --preveri                     ( peskovnik + kanarček )
# Izhod : 0 v redu ; 1 je zapis o zaporu ( trenutek pozornosti ) ; 2 padec.

import sys, os

ZAPISNIK = os.path.join(".", "stroj-orodja", ".geniza", "vratar-zapisnik.tsv")

def zapis(vir, stanje, prica):
    dom = os.path.dirname(ZAPISNIK)
    os.makedirs(dom, exist_ok=True)
    tik = os.popen("date -u +%Y-%m-%dT%H:%M:%SZ").read().strip()
    with open(ZAPISNIK, "a", encoding="utf-8") as f:
        f.write("\t".join([tik, vir, stanje, prica]) + "\n")
    print("VRATAR : zapisano " + tik + " " + vir + " " + stanje)
    if stanje == "ZAPOR":
        print("trenutek pozornosti : vir v zaporu")
        return 1
    return 0

def zadnje(koren):
    pot = os.path.join(koren, ZAPISNIK)
    if not os.path.isfile(pot):
        print("VRATAR : dnevnik še ne obstaja, nobena vrata še niso zapisana")
        return 0
    zadnji = {}
    with open(pot, encoding="utf-8") as f:
        for vrstica in f:
            deli = vrstica.rstrip("\n").split("\t")
            if len(deli) >= 3:
                zadnji[deli[1]] = (deli[0], deli[2], "\t".join(deli[3:]))
    if not zadnji:
        print("VRATAR : dnevnik prazen")
        return 0
    for vir in sorted(zadnji):
        tik, stanje, prica = zadnji[vir]
        print(vir + " : " + stanje + " ( " + tik + " " + prica + " )")
    print("ZAPEČENA VRATA sklanjatnika : zveza en-ena-eno, zveza dva-dve-oba-obe ( rez 6998 )")
    print("ODPRTA VRATA : i-tvor ( Sloleks ), pridevniške tabele ( ucko, Sloleks )")
    return 0

def preveri():
    # peskovnik : pravi dnevnik ni dotaknjen ( ZAPISNIK je relativna pot )
    import tempfile, shutil, io
    peskovnik = tempfile.mkdtemp(prefix="vratar-preverba-")
    prej = os.getcwd()
    os.chdir(peskovnik)
    ok = True
    # priča 1 : zapis treh stanj
    os.makedirs(os.path.join("stroj-orodja", ".geniza"), exist_ok=True)
    i1 = zapis("vir-preverba", "ZADIHA", "peskovnik priča")
    i2 = zapis("vir-preverba", "ZAPOR", "peskovnik priča")
    i3 = zapis("vir-drugi", "ZADIHA", "peskovnik priča")
    ok = ok and (i1 == 0) and (i2 == 1) and (i3 == 0)
    with open(ZAPISNIK, encoding="utf-8") as f:
        vrstice = f.read().strip().split("\n")
    ok = ok and (len(vrstice) == 3) and all(len(v.split("\t")) >= 3 for v in vrstice)
    # priča 2 : zadnje stanje je zadnji zapis istega vira
    zadnji = {}
    for v in vrstice:
        d = v.split("\t")
        zadnji[d[1]] = d[2]
    ok = ok and (zadnji["vir-preverba"] == "ZAPOR") and (zadnji["vir-drugi"] == "ZADIHA")
    # kanarček : napačno pričakovanje mora pasti
    kanarec = not (zadnji["vir-preverba"] == "ZADIHA")
    os.chdir(prej)
    shutil.rmtree(peskovnik)
    print("")
    print("SAMOPREVERBA VRATAR v1.0 : peskovnik, priči 2 ( zapis tri, zadnje stanje ), kanarček " +
          ("pade, pravi padec izmerjen" if kanarec else "ni padel, PADC"))
    if ok and kanarec:
        print("padci orodja : 0")
        print("ODLOČITEV : ZELENA, orodje zapečeno")
        return 0
    print("PADC : samopreverba padla")
    print("ODLOČITEV : RDEČA, orodje ni zapečeno")
    return 1

def main():
    a = sys.argv[1:]
    if not a:
        print("RABA : zapis VIR STANJE [PRIČA] | stanja | --preveri")
        sys.exit(2)
    if a[0] == "--preveri":
        sys.exit(preveri())
    if a[0] == "stanja":
        sys.exit(zadnje("."))
    if a[0] == "zapis" and len(a) >= 3:
        sys.exit(zapis(a[1], a[2], " ".join(a[3:])))
    print("PADC : neznan ukaz " + a[0])
    sys.exit(2)

if __name__ == "__main__":
    main()
