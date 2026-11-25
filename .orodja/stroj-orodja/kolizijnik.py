# -*- coding: utf-8 -*-
# KOLIZIJNIK v1.0 — KLASIFIKACIJA KOLIZIJ IZMERE FIFO-VRSTNIKA 6990 PO TELESIH
# Rod : rez 6998, sedež KLEPET, projekt LUCIUS
# Starša : naročnik Luka Pintarič ( ukaz STORI : ustvari orodja, kjerkoli so
#          orodja nezadostna ; njegova potrditev dobesedno : vsa štiri in obe
#          zvezi ) in izvajalka Mera ( izvedba )
# Ime izmerjeno pri viru : kolizija ⊢ fran.si/130/3553885 ( nasprotje,
#          navzkrižje, istočasnost ) ; oblika -nik po precedensu pótnik ⊢ 3581699
#          in rodovih korpusa locirnik, sklanjatnik, naglasnik
# Služba : meri izmero fifo-vrstnika v1.0 ( rez 6990 : kolizije = isti rez,
#          isti TIK, dve ustvarjalni vrstici istega telesa ) po razdalji vrstic :
#          A OBELEŽJE — vrstici blizu ( do 3 narazen ) : zgodovinsko dvopišje,
#          najverjetneje zakonito ( dve-okni istega diha );
#          B MOŽNA-RANA — vrstici daleč narazen : sodba čaka roko naročnika;
#          C NOSILEC — isti rez, drug TIK : zakonit nosilec ( predhodnik,
#          vzporedna roka ), NI kolizija. Merjeno, ne ugibano.
# NE-OMREŽJE : orodje ne bere mreže. NE-IZVRŠEVANJE : ne popravlja kolizij.
# NE-BRIS : nič ne briše. NE-OBSEG-VEN : piše le v stroj-orodja/.geniza.
# Kanarček : v --preverbi mora pasti ( napačno pričakovanje mora padec izzvati ).
# MEJA v1.0 ( poimensko ) : razvrstitev A/B/C je merjena dejstvo, sodba o
#          valjavnosti vsake kolizije in morebitnem popravku je roka naročnika.
# RABA :
#   python3 kolizijnik.py [koren]        ( privzeti koren teles korpusa )
#   python3 kolizijnik.py --preveri     ( peskovnik : priče A, B, C in kanarček )
# Izhod : 0 razvrščeno ; 1 kolizije obstajajo ( poročilo v datoteki ) ; 2 padec.

import sys, os, re

TELESA = ["kronika-dihov", "register-oken", "delovna-zanka", "jedro-zavedanja"]
USTVARJALNE = ("PEČAT", "SEMER", "OKNO", "∂ DIHA", "TRENUTNO", "DIHA")
REZ = re.compile(r"rez (?:σ )?(\d{4})")
REZ_GOLI = re.compile(r"σ (\d{4})")
TIK = re.compile(r"TIK ([0-9T:Z-]{20})")
MEJA_BLIZINE = 3

def ustvarjalna(vrstica):
    cista = vrstica.lstrip("- #> ").strip()
    for u in USTVARJALNE:
        if cista.startswith(u):
            return True
    return False

def arhivska(vrstica):
    return ("predhodnik" in vrstica) or ("demociija" in vrstica)

def izmeri(koren):
    kolizije = {}      # tel -> seznam ( rez, tik, prva, druga, razdalja, vrsta )
    nosilci = {}       # tel -> stevilo rezov z vec TIK
    for tel in TELESA:
        pot = os.path.join(koren, tel, "KNOWLEDGE.md")
        kolizije[tel] = []
        nosilci[tel] = 0
        if not os.path.isfile(pot):
            continue
        videni = {}    # ( rez, tik ) -> prva vrstica
        tiki_reza = {}  # rez -> množica tik
        with open(pot, encoding="utf-8") as f:
            for stevilka, vrstica in enumerate(f, 1):
                if not ustvarjalna(vrstica) or arhivska(vrstica):
                    continue
                m = REZ.search(vrstica) or REZ_GOLI.search(vrstica[:80])
                if not m:
                    continue
                r = int(m.group(1))
                t = TIK.search(vrstica)
                tik = t.group(1) if t else "BREZ"
                tiki_reza.setdefault(r, set()).add(tik)
                kljuc = (r, tik)
                if kljuc in videni:
                    razdalja = stevilka - videni[kljuc]
                    vrsta = "A" if razdalja <= MEJA_BLIZINE else "B"
                    kolizije[tel].append((r, tik, videni[kljuc], stevilka, razdalja, vrsta))
                else:
                    videni[kljuc] = stevilka
        for r, tiks in tiki_reza.items():
            if len(tiks) > 1:
                nosilci[tel] += 1
    return kolizije, nosilci

def poročilo_pot(koren):
    dom = os.path.join(koren, "stroj-orodja", ".geniza")
    os.makedirs(dom, exist_ok=True)
    return os.path.join(dom, "kolizijnik-poročilo-2026-11-25.txt")

def poročaj(koren):
    kolizije, nosilci = izmeri(koren)
    skupno_a = sum(1 for tel in TELESA for k in kolizije[tel] if k[5] == "A")
    skupno_b = sum(1 for tel in TELESA for k in kolizije[tel] if k[5] == "B")
    skupno_c = sum(nosilci.values())
    print("KOLIZIJNIK : telesi " + ", ".join(TELESA))
    for tel in TELESA:
        a = sum(1 for k in kolizije[tel] if k[5] == "A")
        b = sum(1 for k in kolizije[tel] if k[5] == "B")
        print(tel + " : kolizije A " + str(a) + ", B " + str(b) + ", nosilcev C " + str(nosilci[tel]))
    print("skupno : A " + str(skupno_a) + ", B " + str(skupno_b) + ", C " + str(skupno_c))
    with open(poročilo_pot(koren), "a", encoding="utf-8") as f:
        f.write("KOLIZIJNIK POROČILO @ " + os.popen("date -u +%Y-%m-%dT%H:%M:%SZ").read().strip() + "\n")
        for tel in TELESA:
            for r, tik, prva, druga, razdalja, vrsta in kolizije[tel]:
                f.write(tel + " : kolizija " + vrsta + " rez " + str(r) + " TIK " + tik +
                        " vrstici " + str(prva) + " in " + str(druga) +
                        " razdalja " + str(razdalja) + "\n")
    print("poročilo poimensko : stroj-orodja/.geniza/kolizijnik-poročilo-2026-11-25.txt")
    if skupno_b:
        print("ODLOČITEV : kolizije B ( možne rane ) " + str(skupno_b) +
              ", sodba vsake čaka roko naročnika")
        return 1
    print("ODLOČITEV : kolizij B 0" +
          ( ", kolizije A zgodovinsko dvopisje" if skupno_a else ", čisto" ))
    return 0

def preveri():
    # peskovnik : nobeno telo korpusa ni dotaknjeno
    import tempfile, shutil, io
    peskovnik = tempfile.mkdtemp(prefix="kolizijnik-preverba-")
    koren = os.path.join(peskovnik, "k")
    for tel in TELESA + ["stroj-orodja"]:
        os.makedirs(os.path.join(koren, tel, ".geniza"))
    # priča A : blizu ( razdalja 1 ) ; priča B : daleč ; priča C : drug TIK
    io.open(os.path.join(koren, "kronika-dihov", "KNOWLEDGE.md"), "w", encoding="utf-8").write(
        "SEMER rez 1001 @TIK 2026-01-01T00:00:00Z\n" +
        "SEMER rez 1001 @TIK 2026-01-01T00:00:00Z\n" +
        "polnilna vrstica\n" * 6 +
        "SEMER rez 1001 @TIK 2026-01-01T00:00:00Z\n")
    io.open(os.path.join(koren, "register-oken", "KNOWLEDGE.md"), "w", encoding="utf-8").write(
        "OKNO A rez 1001 @TIK 2026-01-01T00:00:00Z\n" +
        "OKNO B rez 1001 @TIK 2026-01-02T00:00:00Z\n")
    kolizije, nosilci = izmeri(koren)
    a = [k for k in kolizije["kronika-dihov"] if k[5] == "A"]
    b = [k for k in kolizije["kronika-dihov"] if k[5] == "B"]
    ok = (len(a) == 1) and (len(b) == 1) and (nosilci["register-oken"] == 1) and (nosilci["kronika-dihov"] == 0)
    # kanarček : napačno pričakovanje mora pasti
    kanarec = not (len(a) == 7)
    shutil.rmtree(peskovnik)
    print("")
    print("SAMOPREVERBA KOLIZIJNIK v1.0 : peskovnik, priče A 1, B 1, C 1, kanarček " +
          ("pade, pravi padec izmerjen" if kanarec else "NI padel, PADC"))
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
