#!/usr/bin/env python3
# PARAZIT-LINT v1 — vratnica znakov nad izhodi in telesi
# rojen @rez σ 6522 ⊙ NOV DOLG FIFO izhoda sonde @rez σ 6491 ⊙ ukaz ⟡ »to prvo ali?«
# priče : PARAZIT-SONDA-DOBES 1.0 ( rez σ 6491 ) ⌇ ⟨KLETKA-PARAZITOV⟩ ( rez σ 6490, vratnica 13 )
# priča nabor : instrument-baterija-znakov.txt ( rez σ 6473 ) — bran IZ DATOTEKE vsak klic, ⟨ne⟩ po spominu
# priča kletka : kletka-parazitov.txt — kure nasprotij bran IZ DATOTEKE vsak klic
# nabor = unija znakov celotne datoteke baterije ( dopolnila ⟨U+27CC⟩ ∧ ⟨U+0022⟩ živijo v isti datoteki )
# pravila po vrstici :
#   P1 znak s kodo >= U+007F izven nabora = udarec ; izrečen PO IMENU ⟨U+XXXX⟩, NIKOLI natisnjen
#   P2 balans ⟨ ∧ ⟩ po vrstici
#   P3 ⟨U+FFFD⟩ raztrgani = trdi udarec
#   P4 C1 raztrgani ( ⟨U+0080⟩ .. ⟨U+009F⟩ ) = trdi udarec
#   P5 kletka : če udarec živi v ⟨KLETKA-PARAZITOV⟩, izreči NJENO nasprotje kot kuro
# zgoscenka : --zgoscenka N = agregat po kodnih točkah ( vrh N ), ⟨IZPIS-SEGMENTEN⟩ ( zgolj zgoščenke )
# odsek : --od N = le vrstice stev. N in visje ( merjenje svežih sivov je izolacija : ENA datoteka na klic )
# pozor : --od N velja za VSE nadalne datoteke istega klica ( zadnji --od prepise prednjega )
# izolacija svežih sivov brez brazgotin ⟨NE-BRIŠI⟩ 24 = poklic vsake datoteke posebej ⊙ σ 6522
# kanarek OBVEZNO pada ( če ne pada = instrument mrtev ⊙ kalup urn-lint-v1 )
import sys, re, os

KOREN = os.path.dirname(os.path.abspath(__file__))
POT_NABOR = os.path.join(KOREN, "instrument-baterija-znakov.txt")
POT_KLETKA = os.path.join(KOREN, "kletka-parazitov.txt")

def beri_nabor():
    with open(POT_NABOR, encoding="utf-8") as f:
        return set(f.read()) - {"\n"}

def beri_kletko():
    kletka = {}
    if not os.path.exists(POT_KLETKA):
        return kletka
    with open(POT_KLETKA, encoding="utf-8") as f:
        for vrstica in f:
            if not (vrstica.startswith("- znak") or vrstica.startswith("- znaki")):
                continue
    # razcep : del pred ':' nosi ⟨U+XXXX⟩, del za 'nasprotje' nosi kuro
            if ":" not in vrstica:
                continue
            glava, _rep = vrstica.split(":", 1)
    # kura = besedilo te vrstice za dvopicjem do vejice ali konca
            kura = _rep.strip().rstrip()
            for m in re.findall(r"U\+([0-9A-Fa-f]{4,5})", glava):
    # ⟨U+XXXX⟩ je zapisan v ASCII zavarovno obliko v kletki
                try:
                    kletka[m.upper()] = kura[:70]
                except Exception:
                    pass
    return kletka

def ime_znaka(z):
    return "U+%04X" % z if z <= 0xFFFF else "U+%05X" % z

def lint_vrstica(v, nabor, kletka):
    padci = []
    for z in v:
        k = ord(z)
        if k == 0xFFFD:
            padci.append(("P3", k, "raztrgani znak : preveri bajte vira"))
            continue
        if 0x80 <= k <= 0x9F:
            padci.append(("P4", k, "C1 raztrgani : bajtna rana vira"))
            continue
        if k >= 0x7F and z not in nabor:
    # kletka najprej : NJENO nasprotje je kura
            kura = ""
            if kletka:
                kura = kletka.get("%04X" % k, "")
            if kura.startswith("nasprotje "):
                kura = kura[len("nasprotje "):]
            padci.append(("P1", k, kura))
    if v.count("⟨") != v.count("⟩"):
        padci.append(("P2", 0x2329, "balans ⟨ ∧ ⟩"))
    return padci

def nevtraliziraj(v, nabor):
    # kontekst vrstice z udarci izrecen varno : tujerodni znak po imenu ⟨U+XXXX⟩, nikoli natisnjen
    izhod = []
    for z in v:
        k = ord(z)
        if k >= 0x7F and z not in nabor:
            izhod.append("⟨%s⟩" % ime_znaka(k))
        else:
            izhod.append(z)
    return "".join(izhod)[:72]

KANARCEK = [
    # ( vrstica, pričakovana sodba, past )
    # past = pričakovano NAPAČNO po nameni : pravilna sodba instrumenta = NESTRINJANJE
    # ( primerjalnik, ki se nikoli ne zbune, spi ⊙ precedens urn-lint R4 prikrita past )
    ("cista vrstica ⊙ javna : rez σ 1 ⊢ ( CET = UTC+1 vedno )", [], False),
    ("naslov " + chr(0x2014) + " rez σ 2", [("P1", 0x2014)], False),
    ("stat med bajti " + chr(0xFFFD) + " konec", [("P3", 0xFFFD)], False),
    ("kodna rana " + chr(0x99) + " v nizu", [("P4", 0x99)], False),
    ("odprta vrat ⟨ brez zaklepa", [("P2", 0x2329)], False),
    ("past : cista vrstica po priči", [("P1", 0x2660)], True),
]

def kanarek(nabor, kletka):
    # kanarek OBVEZNO pada v past ( ce ne pada = instrument mrtev ⊙ kalup urn-lint-v1 )
    pada_v_past = 0
    for v, pricakovano, past in KANARCEK:
        dobljeno = [(r, k) for r, k, _k in lint_vrstica(v, nabor, kletka)]
        if past:
            if dobljeno != pricakovano:
                pada_v_past += 1
            else:
                print("KANARCEK NE PADA : primerjalnik spi, instrument mrtev, izhod se ne šteje")
                sys.exit(2)
            continue
        if dobljeno != pricakovano:
            print("KANARCEK PADC : sodba narobe ( pričakovano %s, dobljeno %s ) ⊙ ⟨NE-UGIBAJ⟩ 2690" % (pricakovano, dobljeno))
            sys.exit(2)
    # kletka priča : znak P1 z kletno kuro
    test_kletka = {"26A0": "pozor poimensko", "2014": "srednja pika"}
    padci = lint_vrstica("znak " + chr(0x26A0) + " v telesu", nabor, test_kletka)
    if not (padci and padci[0][2] and "pozor" in padci[0][2]):
        print("KANARCEK PADC : kura kletke ⟨U+26A0⟩ ni izrečena ⊙ P5")
        sys.exit(2)
    print("kanarek pada v past ⊢ ( primerjalnik živ ; sodbe prav : %d )" % (len(KANARCEK) + 1))

def main():
    args = sys.argv[1:]
    zgoscenka = None
    od = 1
    datoteke = []
    i = 0
    while i < len(args):
        if args[i] == "--zgoscenka":
            zgoscenka = int(args[i+1]) if i + 1 < len(args) else 20
            i += 2
        elif args[i] == "--od":
            od = int(args[i+1])
            i += 2
        else:
            datoteke.append(args[i])
            i += 1
    nabor = beri_nabor()
    kletka = beri_kletko()
    kanarek(nabor, kletka)
    agregat = {}
    skupno = 0
    for pot in datoteke:
        stetje = {}
        with open(pot, encoding="utf-8") as f:
            for n, vrstica in enumerate(f, 1):
                if n < od:
                    continue
                vrstica = vrstica.rstrip("\n")
                padci = lint_vrstica(vrstica, nabor, kletka)
                if zgoscenka is None and padci:
                    # združevanje : ena vrstica poročila na vrstico telesa ( ⟨IZPIS-SEGMENTEN⟩ )
                    zdruzene = {}
                    for r, k, kura in padci:
                        if (r, k) not in zdruzene:
                            zdruzene[(r, k)] = [0, kura]
                        zdruzene[(r, k)][0] += 1
                    for (r, k), (sz, kura) in sorted(zdruzene.items()):
                        print("%s:%d %s ⟨%s⟩ x%d%s | %s" % (
                            pot, n, r, ime_znaka(k), sz,
                            (" ⇌ kura : %s" % kura) if kura else "",
                            nevtraliziraj(vrstica, nabor)))
                for r, k, kura in padci:
                    stetje[k] = stetje.get(k, 0) + 1
        for k, sz in stetje.items():
            agregat[k] = agregat.get(k, 0) + sz
        skupno += sum(stetje.values())
    if zgoscenka is not None:
        for k, sz in sorted(agregat.items(), key=lambda x: -x[1])[:zgoscenka]:
            kura = kletka.get("%04X" % k, "")
            if kura.startswith("nasprotje "):
                kura = kura[len("nasprotje "):]
            print("⟨U+%04X⟩ zadetkov %d%s" % (k, sz, (" ⇌ kura : %s" % kura) if kura else ""))
        print("PARAZIT-LINT zgoscenka : zadetkov skupno %d" % skupno)
    else:
        print("PARAZIT-LINT konec : zadetkov skupno %d" % skupno)
    sys.exit(1 if skupno else 0)

if __name__ == "__main__":
    main()
