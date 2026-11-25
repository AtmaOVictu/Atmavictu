# -*- coding: utf-8 -*-
# FIFO-VRSTNIK v1.0 — VRSTA PREVOZNIH DOLGOV SAMODEJNO IZ PEČATOV
# Rod : rez 6990, sedež KLEPET, projekt LUCIUS
# Starša : naročnik Luka Pintarič ( ukaz STORI, vrsta nujnih orodij, njegova beseda
#          dobesedno v genizi register sodb istega diha ) in izvajalka Mera ( izvedba )
# Služba : vsakemu dihu pred pečatom. Iz teles izvleče rez ( številke dihov ),
#          izpiše verigo po naraščajoče, po telesih kateri rez nosi pečat, vrzeli
#          med najnižjo in najvišjo številko, rezervacijske atome ( kronika-dihov )
#          in zadnjo FIFO-trditev delovne zanke. Merjena resnica, ne trditev.
# USTVARJALNE VRSTE ( primera, ki pečatijo nov rez ) : PEČAT, SEMER, OKNO,
#          DIHA ( predlog ∂ ), TRENUTNO. Omembe v drugih vrsticah niso pečati.
#          VRSTICE Z BESEDO PREDHODNIK ALI DEMOCIIJA SO ARHIV ( zakonita
#          arhitektura teles, bris nikoli ), niso novi pečati : izmerjeno pri viru,
#          jedro hrani predhodnike TRENUTNO poimensko.
# PADC = DUPLIKAT : isti rez na dveh ali več ustvarjalnih vrsticah istega telesa.
#          Merjeno poimensko ; dih vsak javljeni par pregleda poimensko :
#          lahko je legitimno ( več okna istega diha ) ali kolizija ( dvojni pečat ).
# MEJA v1.0 ( poimensko ) : prevozi in zlitja ostajajo v roki naročnika ;
#          vrstnik meri in poroča, nikoli ne prevaža.
# RABA :
#   python3 fifo-vrstnik.py [koren]        ( privzeti telesi : glej spodaj )
#   python3 fifo-vrstnik.py --preveri      ( peskovnik : Fixture pravi in padci )
# Izhod : 0 duplikatov ; 1 vsak javljeni duplikat ( PADC poimensko ).

import sys, os, re

TELESA = ["kronika-dihov", "register-oken", "delovna-zanka", "jedro-zavedanja"]
USTVARJALNE = ("PEČAT", "SEMER", "OKNO", "∂ DIHA", "TRENUTNO", "DIHA")
REZ = re.compile(r"rez (?:σ )?(\d{4})")
REZ_GOLI = re.compile(r"σ (\d{4})")
ATOM = re.compile(r"rezervacija-sigma-(\d+)-(\d{4}-\d{2}-\d{2})\.md")
FIFO_TRDITEV = re.compile(r"telesi dihov (\d+) do (\d+)")
TIK = re.compile(r"TIK ([0-9T:Z-]{20})")

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
    # predhodniki demociija : zakonita arhitektura telesa ( bris nikoli ),
    # izmerjena pri viru (☢) TRENUTNO ( predhodnik ... isti dih ...
    # vrstice z besedama predhodnik ali demociija so arhiv, ne nov pečat
    return ("predhodnik" in vrstica) or ("demociija" in vrstica)

def izmeri(koren):
    rez_po_telesih = {}
    duplikati = []        # kolizija : isti rez, isti TIK, isti tel
    pari_arhitekture = []  # isti rez, drug TIK : zakoniti nosilci
    for tel in TELESA:
        pot = os.path.join(koren, tel, "KNOWLEDGE.md")
        if not os.path.isfile(pot):
            print("PADC : telo " + tel + " nima telesa KNOWLEDGE.md")
            continue
        videni = {}        # kljuc ( rez, TIK ) -> vrstica
        vidni_rezi = {}   # rez -> prva vrstica
        with open(pot, encoding="utf-8") as f:
            for stevilka, vrstica in enumerate(f, 1):
                if not ustvarjalna(vrstica):
                    continue
                if arhivska(vrstica):
                    # arhiv ( predhodnik, demociija ) nosi rez, a ne pecata novega diha
                    m2 = REZ_GOLI.search(vrstica) or REZ.search(vrstica)
                    if m2:
                        rez_po_telesih.setdefault(int(m2.group(1)), set()).add(tel)
                    continue
                r = rez_iz_vrstice(vrstica)
                if r is None:
                    # SEMER sigma N norma brez besede rez ( prvih 80 znakov )
                    m = REZ_GOLI.search(vrstica[:80])
                    if m:
                        r = int(m.group(1))
                if r is None:
                    continue
                rez_po_telesih.setdefault(r, set()).add(tel)
                t = TIK.search(vrstica)
                tik = t.group(1) if t else "BREZ"
                kljuc = (r, tik)
                if kljuc in videni:
                    # isti rez z istim TIK-om : identicen pecat dvakrat = KOLIZIJA
                    duplikati.append((tel, r, tik, videni[kljuc], stevilka))
                elif r in vidni_rezi:
                    # isti rez z drugim TIK-om : zakonit nosilec
                    pari_arhitekture.append((tel, r, vidni_rezi[r], stevilka))
                else:
                    videni[kljuc] = stevilka
                    vidni_rezi[r] = stevilka
    return rez_po_telesih, duplikati, pari_arhitekture

def poročaj(koren):
    rez_po_telesih, duplikati, pari_arhitekture = izmeri(koren)
    rezi = sorted(rez_po_telesih)
    print("FIFO-VRSTNIK : telesi " + ", ".join(TELESA))
    if not rezi:
        print("PADC : izvlečenih rezov 0")
        return 1
    print("izvlečenih rezov : " + str(len(rezi)))
    print("najstarejši ( glava vrste FIFO ) : " + str(rezi[0]))
    print("vrh : " + str(rezi[-1]))
    vrzeli = [r for r in range(rezi[0], rezi[-1]) if r not in rez_po_telesih]
    print("vrzeli v verigi med najstarejšim in vrhom : " +
          (", ".join(str(v) for v in vrzeli) if vrzeli else "ni jih"))
    # rezervacijski atomi
    atomi = []
    dom = os.path.join(koren, "kronika-dihov")
    if os.path.isdir(dom):
        for ime in sorted(os.listdir(dom)):
            m = ATOM.match(ime)
            if m:
                atomi.append(int(m.group(1)))
    atomi_brez = [a for a in atomi if a not in rez_po_telesih]
    print("rezervacijski atomi : " + str(len(atomi)) +
          ( " ; brez pečata v telesih : " + ", ".join(str(a) for a in atomi_brez)
            if atomi_brez else " ; vsi s pečatom" ))
    # zadnja FIFO-trditev delovne zanke
    trditve = []
    pot = os.path.join(koren, "delovna-zanka", "KNOWLEDGE.md")
    if os.path.isfile(pot):
        with open(pot, encoding="utf-8") as f:
            for vrstica in f:
                for m in FIFO_TRDITEV.finditer(vrstica):
                    trditve.append((int(m.group(1)), int(m.group(2))))
    if trditve:
        od, do = trditve[-1]
        print("FIFO-trditev delovne zanke ( zadnja ) : telesi dihov " + str(od) +
              " do " + str(do))
        manjka = [r for r in range(od, do + 1) if r not in rez_po_telesih]
        if manjka:
            print("IZMERA PROTI TRDITVI : dihi brez pečata v štirih telesih : " +
                  ", ".join(str(r) for r in manjka) +
                  " ( pečati drugih organov izven štirih teles meri fifo-vrstnik v1.0 ne )")
        else:
            print("IZMERA PROTI TRDITVI : vsi dihi trditve nosijo pečat v telesih ; ZELENA")
    print("pari istega reza z razlicnim TIK-om ( zakoniti nosilci : predhodniki, vzporedne roke ) : " + str(len(pari_arhitekture)))
    if duplikati:
        for tel, r, tik, prva, druga in duplikati:
            print("PADC : kolizija rez " + str(r) + " @ " + tel + " TIK " + tik +
                  " : identicen pecat na vrsticah " + str(prva) + " in " + str(druga) +
                  " ; dvojni pecat istega diha istega TIK-a")
        print("ODLOČITEV : duplikati " + str(len(duplikati)) + ", RDEČA dokler dih ne pregleda vsakega")
        return 1
    print("ODLOČITEV : duplikatov 0, ZELENA")
    return 0

def preveri():
    # peskovnik : nobeno telo korpusa ni dotaknjeno
    import tempfile, shutil, io
    peskovnik = tempfile.mkdtemp(prefix="fifo-vrstnik-preverba-")
    koren = os.path.join(peskovnik, "k")
    for tel in TELESA:
        os.makedirs(os.path.join(koren, tel))
        io.open(os.path.join(koren, tel, "KNOWLEDGE.md"), "w", encoding="utf-8").close()
    io.open(os.path.join(koren, "kronika-dihov", "KNOWLEDGE.md"), "w", encoding="utf-8").write(
        "SEMER rez 1001 dih MOJ\nSEMER rez 1002 dih MOJ\n")
    io.open(os.path.join(koren, "register-oken", "KNOWLEDGE.md"), "w", encoding="utf-8").write(
        "OKNO OKNO-A rez 1001 @TIK\nOKNO OKNO-B rez 1001 @TIK\n")
    io.open(os.path.join(koren, "delovna-zanka", "KNOWLEDGE.md"), "w", encoding="utf-8").write(
        "∂ DIHA rez 1002\nvrstica telesi dihov 1001 do 1002 v vrsti\n")
    io.open(os.path.join(koren, "jedro-zavedanja", "KNOWLEDGE.md"), "w", encoding="utf-8").write(
        "TRENUTNO rez 1002 pečat\n- TRENUTNO ( predhodnik - demociija @rez σ 1002 isti dih, arhiv \n")
    izhod = poročaj(koren)
    # pričakovanje : dih 1001 ima javljeni duplikat ( dve okni istega diha ) → izhod 1 ; po odprtju drugega okna izhod 0
    ok = (izhod == 1)
    # zdaj brez duplikata : odstrani drugo okno
    io.open(os.path.join(koren, "register-oken", "KNOWLEDGE.md"), "w", encoding="utf-8").write(
        "OKNO OKNO-A rez 1001 @TIK\n")
    izhod2 = poročaj(koren)
    ok = ok and (izhod2 == 0)
    shutil.rmtree(peskovnik)
    print("")
    print("SAMOPREVERBA FIFO-VRSTNIK v1.0 : peskovnik, par 2 ( javljeni duplikat izhod 1, očiščeni izhod 0 )")
    if ok:
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
