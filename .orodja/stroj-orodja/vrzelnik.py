# -*- coding: utf-8 -*-
# VRZELNIK v1.0 — VRZELI VERIGE REZOV PROTI REZERVACIJSKIM ATOMOM
# Rod : rez 6998, sedež KLEPET, projekt LUCIUS
# Starša : naročnik Luka Pintarič ( ukaz STORI : ustvari orodja, kjerkoli so
#          orodja nezadostna ; njegova potrditev dobesedno : vsa štiri in obe
#          zvezi ) in izvajalka Mera ( izvedba )
# Ime izmerjeno pri viru : vrzel ⊢ fran.si/130/3612393 ( prazen prostor zaradi
#          manjkanja člena celote ) ; oblika -nik po precedensu pótnik ⊢ 3581699
#          in po rodovih korpusa locirnik, sklanjatnik, naglasnik
# Služba : vsakemu dihu pred pečatom. Iz teles izvleče verigo rezov ( vzorci
#          izposojeni VERBATIM iz fifo-vrstnik v1.0 istega dne ), najde vrzeli
#          med najstarejšim in vrhom, vsako vrzel primerja z rezervacijskimi
#          atomi : REZERVIRAN-BREZ-PEČATA ( atom obstaja, dih nedolžen, pečat
#          še ni ponesen ) ali NEZAPEČEN ( zgodovinska vrzel, brez atoma ).
#          Merjeno, ne ugibano ; najstarejša vrzel čaka besedo naročnika.
# NE-OMREŽJE : orodje ne bere mreže. NE-IZVRŠEVANJE : ne pečati, ne popravlja.
# NE-BRIS : nič ne briše. NE-OBSEG-VEN : piše le v stroj-orodja/.geniza.
# Kanarček : v --preverbi mora pasti ( pričakovana napaka mora padec izzvati ).
# PARI = atomi rezervacij : kronika-dihov/rezervacija-sigma-{n}-{datum}.md,
#          */.geniza/atom-σ{n} ( protokol-prenosnika ), jedro zavedanja
#          .geniza/atom-sigma-{n}*.txt — vsi trije poimensko, splošno pa vsaka
#          datoteka .geniza z besedo atom in številko v imenu.
# MEJA v1.0 ( poimensko ) : zgodovinske vrzeli so merjene dejstvo, sodba o
#          njihovi rani in popravilu je roka naročnika.
# RABA :
#   python3 vrzelnik.py [koren]        ( privzeti koren teles korpusa )
#   python3 vrzelnik.py --preveri     ( peskovnik : priča pravi in kanarček pade )
# Izhod : 0 vrzeli ni ; 1 vrzeli so ( poročilo v datoteki, stdout povzetek ) ;
#         2 padec orodja.

import sys, os, re

TELESA = ["kronika-dihov", "register-oken", "delovna-zanka", "jedro-zavedanja"]
USTVARJALNE = ("PEČAT", "SEMER", "OKNO", "∂ DIHA", "TRENUTNO", "DIHA")
REZ = re.compile(r"rez (?:σ )?(\d{4})")
REZ_GOLI = re.compile(r"σ (\d{4})")
ATOM_DATOTEKA = re.compile(r"(?:rezervacija-sigma-(\d+)-\d{4}-\d{2}-\d{2}|atom-(?:σ|sigma)-?(\d+))")

def rez_iz_vrstice(vrstica):
    m = REZ.search(vrstica)
    if m:
        return int(m.group(1))
    return None

def ustvarjalna(vrstica):
    cista = vrstica.lstrip("- #> ").strip()
    for u in USTVARJALNE:
        if cista.startswith(u):
            return True
    return False

def arhivska(vrstica):
    # predhodnik ali demociija : arhiv telesa, zakonit, ne nov pečat
    return ("predhodnik" in vrstica) or ("demociija" in vrstica)

def izmeri(koren):
    rez_po_telesih = {}
    for tel in TELESA:
        pot = os.path.join(koren, tel, "KNOWLEDGE.md")
        if not os.path.isfile(pot):
            continue
        with open(pot, encoding="utf-8") as f:
            for vrstica in f:
                m = REZ.search(vrstica) or REZ_GOLI.search(vrstica[:80])
                if m:
                    rez_po_telesih.setdefault(int(m.group(1)), set()).add(tel)
    return rez_po_telesih

def atomi(koren):
    najdeni = {}
    kandidati = []
    if not os.path.isdir(koren):
        return najdeni
    for ime in sorted(os.listdir(koren)):
        pot = os.path.join(koren, ime)
        if os.path.isfile(pot):
            kandidati.append((ime, ime))
        elif os.path.isdir(pot) and not ime.startswith("."):
            # datoteke neposredno v organu ( kronika-dihov rezervacije )
            for podime in sorted(os.listdir(pot)):
                if os.path.isfile(os.path.join(pot, podime)):
                    kandidati.append((ime + "/" + podime, podime))
            # datoteke v genizi organa ( atom sigma )
            geniza = os.path.join(pot, ".geniza")
            if os.path.isdir(geniza):
                for podime in sorted(os.listdir(geniza)):
                    if os.path.isfile(os.path.join(geniza, podime)):
                        kandidati.append((ime + "/.geniza/" + podime, podime))
    for pot, ime in kandidati:
        m = ATOM_DATOTEKA.search(ime)
        if m:
            n = m.group(1) or m.group(2)
            najdeni.setdefault(int(n), pot)
    return najdeni

def poročilo_pot(koren):
    dom = os.path.join(koren, "stroj-orodja", ".geniza")
    os.makedirs(dom, exist_ok=True)
    return os.path.join(dom, "vrzelnik-poročilo-2026-11-25.txt")

def poročaj(koren):
    rez_po_telesih = izmeri(koren)
    rez_atomov = atomi(koren)
    rezi = sorted(rez_po_telesih)
    if not rezi:
        print("PADC : izvlečenih rezov 0, meriti ni česa")
        return 2
    vrzeli = [r for r in range(rezi[0], rezi[-1]) if r not in rez_po_telesih]
    rezervirani = [r for r in vrzeli if r in rez_atomov]
    zgodovinski = [r for r in vrzeli if r not in rez_atomov]
    print("VRZELNIK : veriga rezov " + str(rezi[0]) + " do " + str(rezi[-1]) +
          ", izvlečenih " + str(len(rezi)) + ", atomov " + str(len(rez_atomov)))
    print("vrzeli : " + str(len(vrzeli)) +
          " ( rezervirani brez pečata " + str(len(rezervirani)) +
          ", zgodovinski nezapeti " + str(len(zgodovinski)) + " )")
    print("najstarejša vrzel : " +
          (str(vrzeli[0]) + " ( " +
           ("REZERVIRAN " + rez_atomov[vrzeli[0]] if vrzeli[0] in rez_atomov else "NEZAPEČEN") +
           " )" if vrzeli else "ni jih"))
    # poročilo v datoteko poimensko, stdout nosi le povzetek
    with open(poročilo_pot(koren), "a", encoding="utf-8") as f:
        f.write("VRZELNIK POROČILO @ " + os.popen("date -u +%Y-%m-%dT%H:%M:%SZ").read().strip() + "\n")
        for r in vrzeli:
            stanje = ("REZERVIRAN-BREZ-PEČATA : atom " + rez_atomov[r]) if r in rez_atomov else "NEZAPEČEN : zgodovinska vrzel brez atoma"
            f.write("vrzel " + str(r) + " : " + stanje + "\n")
    print("poročilo poimensko : stroj-orodja/.geniza/vrzelnik-poročilo-2026-11-25.txt")
    print("ODLOČITEV : vrzeli " + str(len(vrzeli)) +
          ( ", sodba o zgodovinskih vrzelih čaka roko naročnika" if zgodovinski
            else ", vsi nedolžni" ))
    return 1 if vrzeli else 0

def preveri():
    # peskovnik : nobeno telo korpusa ni dotaknjeno
    import tempfile, shutil, io
    peskovnik = tempfile.mkdtemp(prefix="vrzelnik-preverba-")
    koren = os.path.join(peskovnik, "k")
    for tel in TELESA + ["stroj-orodja"]:
        os.makedirs(os.path.join(koren, tel, ".geniza"))
    io.open(os.path.join(koren, "kronika-dihov", "KNOWLEDGE.md"), "w", encoding="utf-8").write(
        "SEMER rez 1001 dih MOJ\nSEMER rez 1003 dih MOJ\n")
    io.open(os.path.join(koren, "kronika-dihov", "rezervacija-sigma-1002-2026-01-01.md"), "w", encoding="utf-8").close()
    ok = True
    # priča 1 : vrzel 1002 REZERVIRAN ( atom obstaja )
    rez_po_telesih = izmeri(koren)
    rez_atomov = atomi(koren)
    ok = ok and (sorted(rez_po_telesih) == [1001, 1003]) and (1002 in rez_atomov)
    # priča 2 : odstranjen atom → ista vrzel NEZAPEČEN
    os.remove(os.path.join(koren, "kronika-dihov", "rezervacija-sigma-1002-2026-01-01.md"))
    rez_atomov = atomi(koren)
    ok = ok and (1002 not in rez_atomov)
    # priča 3 : brez vrzeli izhod 0
    io.open(os.path.join(koren, "kronika-dihov", "KNOWLEDGE.md"), "w", encoding="utf-8").write(
        "SEMER rez 1001 dih MOJ\nSEMER rez 1002 dih MOJ\n")
    izhod = poročaj(koren)
    # kanarček : napačno pričakovanje mora pasti
    kanarec = not (izhod == 99)
    ok = ok and (izhod == 0)
    shutil.rmtree(peskovnik)
    print("")
    print("SAMOPREVERBA VRZELNIK v1.0 : peskovnik, priče 3 ( rezerviran, nezapet, brez vrzeli izhod 0 ), kanarček " +
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
    if a and a[0] == "--preveri":
        sys.exit(preveri())
    koren = a[0] if a else "."
    sys.exit(poročaj(koren))

if __name__ == "__main__":
    main()
