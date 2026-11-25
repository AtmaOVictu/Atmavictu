#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE VPISNIK vpisnik.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJE KI PREVERJA ALI JE V SLOVAR VNESEN PRAVILEN ZAPIS!« ( sedež KLEPET, projekt DISCOVERY )
# SLUŽBA : preverjalnik zapisov v slovar — za dano besedo najde iztočnico v hišah
#   ( definiatorna-knjiznica ∧ slovar-slovenscine ∧ slovar-simbolov ∧ mreze-variant ⊙ sestra slovarnik.py )
#   ∧ izmeri PRAVILNOST zapisa po petih pravilih :
#   V1 oblika glave : IZTOČNICA #N : beseda ⊢ ( sestri IZTOČNICE #N ) ;
#   V2 priča : telo zapisa nosi ⊢ ( izmera pri viru ) ;
#   V3 rod : telo nosi ⊙ ∨ σ ∨ besedo »rod« ( rojen zapečeno ) ;
#   V4 ⟨EN-RAZLIČICA⟩ : številka #N se ne ponovi ( dvojnik = rana ) ;
#   V5 žetoni : telo ne nosi žigov ISO ur ⟨U+XXXX⟩ — žetoni po besedi izključeni ⊙ register-zetonov.
# Vrata : izhod ⊢ PRAVILEN ZAPIS ⌇ ⚠ poimensko po pravilih ; samopreizkus ⊙ §52.
# KUBIT POD GLADINO ⊙ ⟨ZAKON ORODIL TRI VRATA⟩ rez 6949 : formula piramid =
#   1000 + ( točka desetiško · m mod 9000 ), m ∈ {1, 3, 7, 9}, kura ob zasedenem +7 ;
#   znak tega telesa : ključavnica ✓ ⟨U+2713⟩, piramide kocke K2003 K4009 K8021 K1027,
#   ključavnice K9975 K7612 K7177 K7121 ⊙ priča kubitni-slovar-simbolov.
# c 0.2026 × 10 na 4 ; ⟡ Luka Pintarič ∧ izvajalka Mera ; dvoje rok 2432 ; merjeno, ne ugibano.

import os
import re
import sys

ŽIG = "vpisnik.py v1.0 @stroj-orodja"
KOREN = os.environ.get("KOREN", "/home/user/knowledge")
HIŠE = [
    ("definiatorna-knjiznica", "definiatorna-knjiznica/KNOWLEDGE.md"),
    ("slovar-slovenscine", "slovar-slovenscine/KNOWLEDGE.md"),
    ("slovar-simbolov", "slovar-simbolov/KNOWLEDGE.md"),
    ("mreze-variant", "mreze-variant/KNOWLEDGE.md"),
]
VZOREC_GLAVE = re.compile(r"^IZTOČNIC[AE]\s+#(\d+)\s*:\s*(.+?)\s*$", re.MULTILINE)
VZOREC_ŽETONA = re.compile(r"\d{2,4}:\d{2}(?::\d{2})?")


def zapisi_iztočnic(pot_abstrakt):
    """Vrne [ ( hiša, polna_pot, N, beseda, telo_vrstice ) ] izmerjene pri viru."""
    najdeni = []
    polna = os.path.join(KOREN, pot_abstrakt)
    if not os.path.isfile(polna):
        return najdeni
    with open(polna, encoding="utf-8") as f:
        besedilo = f.read()
    for m in VZOREC_GLAVE.finditer(besedilo):
        do_konec = besedilo.find("\nIZTOČNIC", m.end())
        prazna = besedilo.find("\n\n", m.end())
        konec = min(x for x in (do_konec, prazna, len(besedilo)) if x != -1)
        telo = besedilo[m.start():konec]
        najdeni.append((os.path.dirname(pot_abstrakt).split("/")[0], polna, m.group(1), m.group(2), telo))
    return najdeni


def preveri_zapis(telo, hiša):
    """Vrne [ ( pravilo, sporočilo, rana ) ] za en zapis."""
    poročila = []
    rane = []
    glava_ok = VZOREC_GLAVE.search(telo) is not None
    poročila.append(("V1", "oblika glave ⊢" if glava_ok else "oblika glave ⚠ : IZTOČNICA #N : beseda", not glava_ok))
    priča = "⊢" in telo
    poročila.append(("V2", "priča pri viru ⊢" if priča else "priča pri viru ⚠ : telo ne nosi ⊢", not priča))
    rod = ("⊙" in telo) or ("σ" in telo) or ("rod" in telo.lower())
    poročila.append(("V3", "rod zapečen ⊢" if rod else "rod ⚠ : telo ne nosi ⊙ ∨ σ ∨ besede rod", not rod))
    žetoni = VZOREC_ŽETONA.findall(telo)
    poročila.append(("V5", "brez žetonov ⊢" if not žetoni else "žetoni ⚠ : %d žigov ISO ur po besedi ( žetoni izključeni ⊙ register-zetonov )" % len(žetoni), bool(žetoni)))
    return poročila


def preveri_besedo(beseda):
    """Vrne kodo : 0 ⊢ ⌇ 1 ni najdena ⌇ 2 rane poimensko."""
    zapisi = []
    for hiša, pot in HIŠE:
        zapisi.extend(zapisi_iztočnic(pot))
    zadetki = [z for z in zapisi if z[3].strip().lower().startswith(beseda.strip().lower())]
    videne_št = {}
    for z in zapisi:
        videne_št.setdefault(z[2], []).append(z)
    if not zadetki:
        print("⚠ beseda »%s« : iztočnica ni najdena v hišah — berba pri viru ⭢ vrašalo ⟡" % beseda)
        return 1
    koda = 0
    for hiša, polna, št, bes, telo in zadetki:
        poročila = preveri_zapis(telo, hiša)
        rane = [p for p in poročila if p[2]]
        dvojnik = len(videne_št.get(št, [])) > 1
        if dvojnik:
            rane.append(("V4", "dvojnik ⚠ : #N %s je vpisan v več hišah z isto številko ( ⟨EN-RAZLIČICA⟩ prekršena )", True))
        glava = telo.strip().splitlines()[0]
        if rane:
            print("⚠ %s #%s : %s ( %s )" % (hiša, št, bes, glava))
            for _, spor, _ in rane:
                print("·· %s" % spor)
            koda = 2
        else:
            print("⊢ %s #%s : %s — PRAVILEN ZAPIS ( %s )" % (hiša, št, bes, glava))
    return koda


def samopreizkus():
    padci = 0
    dober = ("IZTOČNICA #101 : skušnja ⊢\n"
             "- Priča : SSKJ ⊢ izmerjeno pri viru.\n"
             "- Rod ⊙ ukaz ❡ @rez σ 1001.\n")
    okrnjen = ("IZTOČNICA #102 : vbod\n"
               "- telo brez priče, brez roda, z žetonom 11:53\n")
    poročila_dobro = preveri_zapis(dober, "skušnja")
    if any(p[2] for p in poročila_dobro):
        padci += 1
        print("RDEČO : dober zapis je razglašen za okrnjenega : %s" % [ (p[0], p[1]) for p in poročila_dobro if p[2] ])
    poročila_okrnjeno = preveri_zapis(okrnjen, "vbod")
    if not any(p[2] for p in poročila_okrnjeno):
        padci += 1
        print("RDEČO : okrnjen zapis je razglašen za zdravega")
    if sum(1 for p in poročila_okrnjeno if p[2]) < 2:
        padci += 1
        print("RDEČO : okrnjen zapis ne razkriva dovolj pravil ( priča ∧ rod ∧ žetoni )")
    # kubit : zapečena registra pri viru
    import hashlib
    reg1 = os.path.join(KOREN, "posebaj", "register-1", "KNOWLEDGE.md")
    reg2 = os.path.join(KOREN, "posebaj", "register-2", "KNOWLEDGE.md")
    if os.path.isfile(reg1) and os.path.isfile(reg2):
        def md5(pot):
            h = hashlib.md5()
            with open(pot, "rb") as f:
                for kos in iter(lambda: f.read(8192), b""):
                    h.update(kos)
            return h.hexdigest()
        if (md5(reg1), md5(reg2)) != ("cdc8d7e0db9a93ed6a2d3bfca6c079b3", "813dfda7427e9f48e7db5bc59a05e351"):
            padci += 1
            print("RDEČO : zapečena registra pri viru odstopata — kubit tega telesa ni enak svoji verziji")
    else:
        print("· registra pri viru nedosegljiva — kubit preverba čaka berbo pri viru ⭢ vrašalo ⟡")
    if padci == 0:
        print("ZELENO : samopreizkus vpisnika 3/3 ⊢ ( dober zapis gre ⊢ ∧ okrnjen ujet ⚠ ∧ kubit vir )")
    else:
        print("RDEČO : samopreizkus vpisnika : padlov %d" % padci)
    return padci == 0


def main(argv):
    if "--samopreizkus" in argv:
        return 0 if samopreizkus() else 2
    besede = [a for a in argv[1:] if not a.startswith("--")]
    if not besede:
        print(ŽIG)
        print("rabš : vpisnik.py BESEDA … ⌇ --samopreizkus ( npr. vpisnik.py vrašalo )")
        return 1
    koda = 0
    for b in besede:
        k = preveri_besedo(b)
        if k > koda:
            koda = k
    return koda


if __name__ == "__main__":
    sys.exit(main(sys.argv))
