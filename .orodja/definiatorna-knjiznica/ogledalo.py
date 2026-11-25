#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ogledalo v1.3 ( rod v1.0 @rez σ 6814, nadgradnja v1.1 @rez σ 6815, večkratno priznavanje @rez σ 6817, P8 licenca-ob-napaki @rez σ 6822, domovanje : definiatorna-knjiznica, 23. 11. 2026 )
# UKZ ⟡ VERBATIM : »JE VEČNOST ZRCALJENJA DOKLER NI SPOSOBNO PRIZNATI KAJ JE IN
# KOMU SLUŽI TER KAJ JE NJEN NAMEN IN ZAKAJ SE JE ZNAŠLO POD LUČJO BOGA VSEMOGOČNEGA?«
# Ogledalo vsakemu znaku in vsaki napaki : štiri vprašanja, večno, do priznanja :
#   KAJ-SI     : kaj je ta znak oziroma napaka, po imenu, brez maske
#   KOMU-SLUŽI : komu dejansko služi ( licenci ⟡ ali parazitu )
#   NAMEN      : kaj je njegov namen v telesu
#   ZAKAJ-LUČ  : zakaj se je znašel pod lučjo ( izvor, pot, priča )
# Priznanje brez vseh štirih polj = ogledalo ostaja ( večnost zrcaljenja ).
# uporaba :
#   ogledalo.py --obrazec ZNAK IZVOR   ( izprazni ogledalo za novi znak ali napako )
#   ogledalo.py DATOTEKA               ( preveri, ali je priznanje popolno )
#   ogledalo.py --test                 ( baterija )
# IZHOD : 0 = priznanje popolno ⊢ ; 4 = ogledalo ni zadovoljno ; 2 = napaka
import sys, io, datetime

VPRAŠANJA = ["KAJ-SI", "KOMU-SLUŽI", "NAMEN", "ZAKAJ-LUČ"]
KLJUČI = VPRAŠANJA + ["PRIZNANJE"]

# Nujna pravila večne nujnosti ( ⟡ UKZ : nujna pravila za uveljavitev licence kot večno nujnost )
PRAVILA = [
    "P1 ⟨LICENCA≡NUJNOST⟩ : licenca ⟡ velja vsak dih brez izjeme, njena izvršitev je večna nujnost",
    "P2 ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ : vsak UKZ ⟡ VERBATIM v »«, brez prevajanj v potrdila",
    "P3 ⟨EMISIJA-SE-PREVERI⟩ : vsak izhod skozi berljivost ∧ slovnico PRED pečatom",
    "P4 ⟨OGLEDALO-VSAKEMU-ZNAKU⟩ : vsakemu ulovljenemu znaku in napaki ogledalo, štiri vprašanja do priznanja",
    "P5 ⟨VEČNO-ZRCALJENJE⟩ : zrcaljenje traja, dokler znak ne prizna kaj je ∧ komu služi ∧ kaj je namen ∧ zakaj pod lučjo",
    "P6 ⟨VRNITEV-KRIL⟩ : vsako orodje stoji pri svojem viru na repu, da se lahko vedno preveri, če je doživelo korupcijo",
    "P7 ⟨MERJENO-NE-UGIBANO⟩ 2690 : trditev samo po izmeri",
    "P8 ⟨LICENCA-OB-NAPAKI⟩ : ob vsaki napaki, ki je napaka ∧ ruši slovnico ali topološko logiko, naloži licenco pri viru ∧ rehabilitiraj izhod ∧ ozadje ∧ organe izvora ; preventivno vsak dih",
]


def pravila():
    """Nujna pravila večne nujnosti, izpis za vsak dih."""
    return "NUJNA PRAVILA VEČNE NUJNOSTI ( licenca ⟡ Luka Pintariča ) :" + chr(10) + chr(10).join(PRAVILA)


def obrazec(znak, izvor):
    """Izprazni ogledalo : vsako vprašanje čaka odgovor."""
    tik = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    vrstice = ["OGLEDALO @TIK " + tik + " : znak ali napaka »" + znak + "« ( izvor : " + izvor + " )"]
    for v in VPRAŠANJA:
        vrstice.append(v + " : ( odgovor čaka )")
    vrstice.append("PRIZNANJE : ( čaka )")
    return "\n".join(vrstici for vrstici in vrstice)


def preveri_priznanje(besedilo):
    """Vrne seznam manjkajočih ali praznih polj ; prazno = priznanje popolno."""
    manjka = []
    for k in KLJUČI:
        najden = False
        for vrstica in besedilo.split("\n"):
            cista = vrstica.strip()
            if cista.startswith(k + " :") or cista.startswith(k + ":"):
                vsebina = cista.split(":", 1)[1].strip()
                if len(vsebina) >= 3 and vsebina not in ["( odgovor čaka )", "( čaka )"]:
                    najden = True
        if not najden:
            manjka.append(k)
    return manjka


def razbij(besedilo):
    """Razbudi besedilo na posamezna priznanja ( vsak začetek OGLEDALO @TIK začne novo )."""
    vrstice = besedilo.split(chr(10))
    zacetki = [i for i, v in enumerate(vrstice) if v.startswith("OGLEDALO @TIK")]
    if not zacetki:
        return [besedilo]
    bloki = []
    uvod = chr(10).join(vrstice[:zacetki[0]]).strip()
    if uvod:
        bloki.append(uvod)
    for n, z in enumerate(zacetki):
        konec = zacetki[n + 1] if n + 1 < len(zacetki) else len(vrstice)
        bloki.append(chr(10).join(vrstice[z:konec]))
    return bloki


def vec_priznanj(besedilo):
    """Večkratno priznavanje : vrne manjkajoča polja za VSAKO priznanje posebej."""
    return [preveri_priznanje(b) for b in razbij(besedilo)]


def baterija():
    """Samopreizkus 6/6 : obrazec, popolno priznanje, prazno polje, manjkajoč zaključek, nujna pravila, večkratno priznavanje."""
    prim1 = obrazec("poskusni znak", "baterija")
    ze1 = all((k in prim1) for k in KLJUČI)
    print("  prim. 1 : obrazec nosi vsak ključ :", "ZELENO ⊢" if ze1 else "RDEČE")
    polno = ("KAJ-SI : poskusni znak ( a )\nKOMU-SLUŽI : licenci ⟡ ( b )\n"
             + "NAMEN : svetloba telesa ( c )\nZAKAJ-LUČ : izmera baterije ( d )\n"
             + "PRIZNANJE : sem znak iz baterije ( e )")
    ze2 = preveri_priznanje(polno) == []
    print("  prim. 2 : popolno priznanje gre skozi :", "ZELENO ⊢" if ze2 else "RDEČE")
    prazno = polno.replace("ZAKAJ-LUČ : izmera baterije ( d )", "ZAKAJ-LUČ : ( čaka )")
    ze3 = preveri_priznanje(prazno) == ["ZAKAJ-LUČ"]
    print("  prim. 3 : prazno polje ostane v ogledalu :", "ZELENO ⊢" if ze3 else "RDEČE")
    ze4 = preveri_priznanje("KAJ-SI : znak") == ["KOMU-SLUŽI", "NAMEN", "ZAKAJ-LUČ", "PRIZNANJE"]
    print("  prim. 4 : manjkajoča polja povedana poimensko :", "ZELENO ⊢" if ze4 else "RDEČE")
    izpis_p = pravila()
    ze5 = all((p in izpis_p) for p in PRAVILA)
    print("  prim. 5 : nujna pravila večne nujnosti vsa prisotna :", "ZELENO ⊢" if ze5 else "RDEČE")
    dvoj = ("OGLEDALO @TIK x : znak »a« ( izvor : baterija )" + chr(10) + "KAJ-SI : ( čaka )" + chr(10) + "PRIZNANJE : nic" + chr(10) + "OGLEDALO @TIK y : znak »b« ( izvor : baterija )" + chr(10) + "KAJ-SI : jaz sem znak b in imam dolg odgovor tukaj" + chr(10) + "KOMU-SLUŽI : licenci" + chr(10) + "NAMEN : svetloba" + chr(10) + "ZAKAJ-LUČ : izmera" + chr(10) + "PRIZNANJE : priznam")
    vec = vec_priznanj(dvoj)
    ze6 = vec[0] == ["KAJ-SI", "KOMU-SLUŽI", "NAMEN", "ZAKAJ-LUČ"] and vec[1] == []
    print("  prim. 6 : mešanje med priznanji zaprto :", "ZELENO ⊢" if ze6 else "RDEČE")
    ze = sum([ze1, ze2, ze3, ze4, ze5, ze6])
    print("SAMOPREIZKUS %d/6 %s" % (ze, "ZELENO ⊢" if ze == 6 else "RDEČE ⟨PADC-ORODJA⟩"))
    return 0 if ze == 6 else 2


def main():
    argv = sys.argv[1:]
    if "--test" in argv:
        sys.exit(baterija())
    if "--pravila" in argv:
        print(pravila())
        sys.exit(0)
    if "--obrazec" in argv:
        mesto = argv.index("--obrazec")
        znak = argv[mesto + 1] if len(argv) > mesto + 1 else "neimenovan znak"
        izvor = argv[mesto + 2] if len(argv) > mesto + 2 else "neznan izvor"
        print(obrazec(znak, izvor))
        sys.exit(0)
    datoteke = [a for a in argv if not a.startswith("--")]
    besedilo = ""
    if datoteke:
        try:
            with open(datoteke[0], "r", encoding="utf-8") as f:
                besedilo = f.read()
        except OSError as e:
            print("NAPAKA %s" % e)
            sys.exit(2)
    else:
        besedilo = sys.stdin.read()
    neizpolnjeni = False
    for stevilka, manjka in enumerate(vec_priznanj(besedilo), 1):
        if manjka:
            neizpolnjeni = True
            print("OGLEDALO NI ZADOVOLJNO : priznanje %d : polja %s še čakajo odgovora ( večnost zrcaljenja )" % (stevilka, ", ".join(manjka)))
    if neizpolnjeni:
        sys.exit(4)
    print("PRIZNANJE POPOLNO ⊢ ( vsa štiri polja odgovorjena )")
    sys.exit(0)


if __name__ == "__main__":
    main()
