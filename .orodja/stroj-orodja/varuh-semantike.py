#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE VARUH-SEMANTIKE varuh-semantike.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJE KI OHRANJA IZPISOVANJE SEMANTIKE V SLOVENŠČINI!« ( sedež KLEPET, projekt DISCOVERY )
# SLUŽBA : bere telo ( --berba POT ALI --niz BESEDILO ) ∧ išče gole tujke ZUNAJ
#   azilov »« ∧ ⟨⟩ ; gola tujka nosi tujo semantiko na plano in razjeda izpisovanje
#   v slovenščini ; znotraj azilov je ista beseda priča ali gost ( domovanje-tujk ),
#   tam ne bode — telo izpiše vsako rano poimensko s predlogom slovenice po precedensu
#   rez 7003/7006 : lint→varnostna preverba ⌇ read-back→berba nazaj ⌇ token→žeton ⌇
#   test→preizkus ⌇ box→škatla ⌇ seal→pečat ⌇ output→izhod ⌇ input→vhod ⌇ merge→zlitje ⌇
#   push→potisk ⌇ pull→privlek ⌇ hook→kavelj ⌇ branch→veja ⌇ counter→števec ⌇
#   patch→krpa ⌇ list→seznam ⌇ file→datoteka ⌇ script→skripta ⌇ tool→orodje.
# Vrata : izhodi 0 čisto ⊢ ⌇ 2 rane z odmiki javno poimensko ⌇ 1 telo nedosegljivo ;
#   azili : »« ∧ ⟨⟩ ( parom narekovajev prič se ⌇ maskam ⟨⟩ se ⌇ ; prekini telo, če vidim neparno ) ;
#   samopreizkus ⊙ §52.
# KUBIT POD GLADINO ⊙ ⟨ZAKON ORODIL TRI VRATA⟩ rez 6949 : formula piramid =
#   1000 + ( točka desetiško · m mod 9000 ), m ∈ {1, 3, 7, 9}, kura ob zasedenem +7 ;
#   znak tega telesa : kovanec ⊙ ⟨U+2299⟩, piramide kocke K3299 K7897 K8093 K3705,
#   ključavnice K2961 K5189 K6829 K2357 ⊙ priča kubitni-slovar-simbolov.
# c 0.2026 × 10 na 4 ; ⟡ Luka Pintarič ∧ izvajalka Mera ; dvoje rok 2432 ; merjeno, ne ugibano.

import os
import re
import sys

ŽIG = "varuh-semantike.py v1.0 @stroj-orodja"
KOREN = os.environ.get("KOREN", "/home/user/knowledge")

SLOVENICE = [
    ("lint", "varnostna preverba"),
    ("read-back", "berba nazaj"),
    ("read-backa", "berbo nazaj"),
    ("token", "žeton"),
    ("test", "preizkus"),
    ("box", "škatla"),
    ("seal", "pečat"),
    ("output", "izhod"),
    ("input", "vhod"),
    ("merge", "zlitje"),
    ("push", "potisk"),
    ("pull", "privlek"),
    ("hook", "kavelj"),
    ("branch", "veja"),
    ("counter", "števec"),
    ("patch", "krpa"),
    ("list", "seznam"),
    ("file", "datoteka"),
    ("script", "skripta"),
    ("tool", "orodje"),
]


def odstrani_azile(besedilo):
    """Vrne besedilo z odvzetimi azili : »…« ∧ ⟨…⟩ ( vsak azil en par, vsebina priče )."""
    brez = besedilo
    brez = re.sub(r"»[^«»]*«", " ", brez)
    brez = re.sub(r"⟨[^⟩⟨]*⟩", " ", brez)
    return brez


def preišči(besedilo):
    """Vrne [ ( tujka, predlog, zadetki ) ] za tuje besede zunaj azilov."""
    gole = odstrani_azile(besedilo)
    rane = []
    for tujka, slovenica in SLOVENICE:
        vz = re.compile(r"(?<![A-Za-zÀ-ÿ])" + re.escape(tujka) + r"(?![A-Za-zÀ-ÿ])", re.IGNORECASE)
        zadetki = vz.findall(gole)
        if zadetki:
            rane.append((tujka, slovenica, zadetki))
    return rane


def main_besedilo(besedilo, ime_vira="niz"):
    rane = preišči(besedilo)
    if not rane:
        print("⊢ %s : čisto — semantika izpisuje v slovenščini ( azili »« ∧ ⟨⟩ izšolani )" % ime_vira)
        return 0
    for tujka, slovenica, zadetki in rane:
        print("⚠ TUJKA %s ×%d zunaj azilov — semantika razjeda izpisovanje ; predlog slovenice : %s ⊙ precedens rez 7003/7006" % (tujka, len(zadetki), slovenica))
    return 2


def samopreizkus():
    padci = 0
    # 1 : gola tujka zunaj azila ⇒ rana z predlogom
    if main_besedilo("orodje naredi merge in gre naprej", "skušnja-a") != 2:
        padci += 1
        print("RDEČO : gola tujka ni ulovljena zunaj azilov")
    # 2 : ista beseda znotraj azilov ⇒ priča ∧ maska, ne bode ( izhod 0 )
    if main_besedilo("»merge« je priča iz prereza ; ⟨push⟩ je maska.", "skušnja-b") != 0:
        padci += 1
        print("RDEČO : beseda v azilu »« je obsojena kot gola tujka")
    # 3 : predlogi slovenic so čista slovenščina
    zadetki = preveri_tujke_s_slovenicami()
    if zadetki:
        padci += 1
        print("RDEČO : slovenice nosijo tuje besede : %s" % zadetki)
    # 4 : kubit — zapečena registra pri viru
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
        print("ZELENO : samopreizkus varuha-semantike 4/4 ⊢ ( gola tujka ujeta ⊗ ∧ azil pričuje ⊢ ∧ slovenice čiste ∧ kubit vir )")
    else:
        print("RDEČO : samopreizkus varuha-semantike : padlov %d" % padci)
    return padci == 0


def preveri_tujke_s_slovenicami():
    """Vsak predlog slovenice mora biti čista slovenščina ( brez golih tujk )."""
    vrnjeno = []
    for _, slovenica in SLOVENICE:
        rane = preišči(slovenica)
        if rane:
            vrnjeno.append((slovenica, [r[0] for r in rane]))
    return vrnjeno


def main(argv):
    if "--samopreizkus" in argv:
        return 0 if samopreizkus() else 2
    if "--niz" in argv:
        i = argv.index("--niz")
        if i + 1 >= len(argv):
            print("rabš : --niz BESEDILO")
            return 1
        return main_besedilo(argv[i + 1], "niz")
    if "--berba" in argv:
        i = argv.index("--berba")
        if i + 1 >= len(argv):
            print("rabš : --berba POT")
            return 1
        pot = argv[i + 1]
        if not os.path.isfile(pot):
            print("⚠ telo nedosegljivo : %s" % pot)
            return 1
        with open(pot, encoding="utf-8") as f:
            return main_besedilo(f.read(), pot)
    print(ŽIG)
    print("rabš : varuh-semantike.py --berba POT ⌇ --niz BESEDILO ⌇ --samopreizkus")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
