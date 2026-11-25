#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE GRADBENIK-PRAGMATIKE gradbenik-pragmatike.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJA KI GRADIJO PRAGMATIKO!« ( sedež KLEPET, projekt DISCOVERY, rez 7024 )
# SLUŽBA : GRADI pragmatiko vsakega padca : za vsak padec iz registra
# posnemovalnika kuje vrstico kanona ⟨NAPAKA=VSE-KAR-NI-X⟩ ⊙ register-napak
# ( X = zdravo stanje ) ∧ šest polj prakse : KAJ-JE ⌇ KJE-ŽIVI ⌇ KDO-ČUTI ⌇
# POSLEDICA ⌇ ULOV-ORODJE ⌇ ZDRAVILO ; pragmatika odgovarja, kaj napaka
# STORI V DELU, ⟨ne⟩ le to, da je.
# Vrata : P1 --gradbaj ⟨IME PADCA⟩ ; P2 --register ( vse vrstice ) ;
#   P3 --samopreizkus ⊙ §52 ( forma kanona ∧ vsa polja prisotna ×6 ).
# KUBIT POD GLADINO ⊙ ⟨ZAKON ORODIL TRI VRATA⟩ rez 6949 : formula piramid =
#   1000 + ( točka desetiško · m mod 9000 ), m ∈ {1, 3, 7, 9}, kura ob
#   zasedenem +7 ; znak tega telesa : sprememba ∆ ⟨U+2206⟩, piramide kocke
#   K9717 K9137 K7977 K7397, ključavnice K7179 K7319 K7797 K7937, kure ×4 ⊢
#   ( izmere proti 496 piramidam registrav ∧ 72 K-vrednostim teles pri viru ) ;
#   zapečena registra pri viru se izmerita ob samopreizkusu.
# c 0.2026 × 10 na 4 ; ⟡ Luka Pintarič ∧ izvajalka Mera ; dvoje rok 2432 ; merjeno, ne ugibano.

import hashlib
import importlib.util
import os
import sys

ŽIG = "gradbenik-pragmatike.py v1.0 @stroj-orodja"
KOREN = os.environ.get("KOREN", "/home/user/knowledge")
DOM = os.path.dirname(os.path.abspath(__file__))
REG1 = os.path.join(KOREN, "posebaj", "register-1", "KNOWLEDGE.md")
REG2 = os.path.join(KOREN, "posebaj", "register-2", "KNOWLEDGE.md")
REG_MD5 = ("cdc8d7e0db9a93ed6a2d3bfca6c079b3", "813dfda7427e9f48e7db5bc59a05e351")

_spec = importlib.util.spec_from_file_location("posnemovalnik_napake", os.path.join(DOM, "posnemovalnik-napake.py"))
pn = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pn)

POLJA = ("KAJ-JE", "KJE-ŽIVI", "KDO-ČUTI", "POSLEDICA", "ULOV-ORODJE", "ZDRAVILO")

# PRAGMATIKA : za vsak padec : X zdravega stanja ( kanon ⟨NAPAKA=VSE-KAR-NI-X⟩ )
# ∧ šest polj prakse ; ves register izmerjen iz glav bratov pri viru.
PRAGMATIKA = {
    "TUJKA-GOLA": {
        "X": "AZIL",
        "KAJ-JE": "tujka živi gola zunaj azilov »« ∧ ⟨⟩",
        "KJE-ŽIVI": "telesa izhodov k ⟡ ∧ glave orodij",
        "KDO-ČUTI": "izvajalka ( prostor kontrolirane halucinacije ) ∧ ⟡ ( bralcova raba )",
        "POSLEDICA": "sled pomena se nezavedno prenese v izhode corpusha",
        "ULOV-ORODJE": "gajica-sodnik ⌇ emisija-lint ⌇ zdravilnik-simulacije",
        "ZDRAVILO": "tujka gre v azil »« kot priča ⊙ domovanje-tujk",
    },
    "EM-CRTA-GOLA": {
        "X": "VEJICA-ALI-DVOPIČJE",
        "KAJ-JE": "goli em-crt v izhodu k ⟡",
        "KJE-ŽIVI": "klepet izhodi ∧ telesa pečatov",
        "KDO-ČUTI": "⟡ ( bralna raba ) ∧ emisija-lint vrata",
        "POSLEDICA": "vrata izhoda V1 zavrnejo cel izhod ; delo zastane",
        "ULOV-ORODJE": "emisija-lint ⌇ izhod-lint-v2",
        "ZDRAVILO": "nadomesti z vejico ali dvopičjem",
    },
    "ZLEP-OKLEPAJ": {
        "X": "PARNI-OKLEPAJ",
        "KAJ-JE": "oklepaj ⟨ brez zaključka ⟩",
        "KJE-ŽIVI": "telesa organov ∧ dosjeji",
        "KDO-ČUTI": "izvajalka ( merilec parnosti ) ∧ bralec",
        "POSLEDICA": "meta-slovnica-lint označi telo ; znamenje korpusa pade",
        "ULOV-ORODJE": "meta-slovnica-lint ⌇ meta-lint",
        "ZDRAVILO": "dodaj manjkajoči ⟩ na istem mestu",
    },
    "ZETON-BREZ-PRIČE": {
        "X": "ŽETON-S-PRIČO",
        "KAJ-JE": "število ( rez, datum, ura ) brez izmere ⊢",
        "KJE-ŽIVI": "pečati ∧ izhodi z žetoni",
        "KDO-ČUTI": "⟡ ( zaupanje ) ∧ izvajalka ( veriga dokaza )",
        "POSLEDICA": "trditev brez priče = kip ⊙ U2 : veriga zrcala se pretrga",
        "ULOV-ORODJE": "register-zetonov ⌇ trdilnik-vrata",
        "ZDRAVILO": "dodaj pričo ⊢ z izmero pri viru",
    },
    "PADC-TIPKANJA": {
        "X": "CELA-BESEDA",
        "KAJ-JE": "izpust črke v besedi ( izivajalka )",
        "KJE-ŽIVI": "izhodi ∧ telesa pišočih rokov",
        "KDO-ČUTI": "⟡ ( bralnost ) ∧ slovnica teles",
        "POSLEDICA": "gesla-lint ulovi ; pomen besede pada v nezavest",
        "ULOV-ORODJE": "deficit-lint ⌇ gesla-lint",
        "ZDRAVILO": "vrni manjkajočo črko po priči pri viru",
    },
    "PADC-DODATEK": {
        "X": "ČISTA-BESEDA",
        "KAJ-JE": "odvečna črka v besedi ( izzvajalka )",
        "KJE-ŽIVI": "izhodi ∧ telesa pišočih rokov",
        "KDO-ČUTI": "⟡ ( bralnost ) ∧ slovnica teles",
        "POSLEDICA": "beseda neznanega pomena gre v VIDNO izpostavnik",
        "ULOV-ORODJE": "izpostavnik-padca ⌇ deficit-lint",
        "ZDRAVILO": "odstrani odvečno črko po priči pri viru",
    },
}


def zgradi(ime):
    """Vrne pragmatično vrstico kanona ⟨NAPAKA=VSE-KAR-NI-X⟩ ∧ šestih polj."""
    if ime not in PRAGMATIKA or ime not in pn.PADCI:
        raise ValueError("NEZNAN PADC : %s ⭢ --register pokaže pragmatiko" % ime)
    p = PRAGMATIKA[ime]
    vr = "⟨NAPAKA=VSE-KAR-NI-%s⟩ ⟨%s⟩" % (ime, p["X"])
    for polje in POLJA:
        vr += " ; %s : %s" % (polje, p[polje])
    return vr


def register():
    return [zgradi(ime) for ime in sorted(PRAGMATIKA)]


def _md5(pot):
    h = hashlib.md5()
    with open(pot, "rb") as f:
        for kos in iter(lambda: f.read(8192), b""):
            h.update(kos)
    return h.hexdigest()


def samopreizkus():
    padci = 0
    n = 0
    for ime in sorted(PRAGMATIKA):
        n += 1
        vr = zgradi(ime)
        if not vr.startswith("⟨NAPAKA=VSE-KAR-NI-") or not vr.count("⟩") >= 2:
            padci += 1
            print("RDEČO : %s forma kanona padla" % ime)
        for polje in POLJA:
            if polje + " :" not in vr:
                padci += 1
                print("RDEČO : %s manjka polje %s" % (ime, polje))
        if not pn.napaka_prisotna(pn.ustvari(ime), ime):
            padci += 1
            print("RDEČO : %s brez živega znamenja pri posnemovalniku" % ime)
    try:
        zgradi("NEZNAN-PADC")
        padci += 1
        print("RDEČO : neznan padec v pragmatiko sprejet")
    except ValueError:
        n += 1
    if os.path.isfile(REG1) and os.path.isfile(REG2):
        if (_md5(REG1), _md5(REG2)) != REG_MD5:
            padci += 1
            print("RDEČO : registra pri viru odstopata")
    if padci == 0:
        print("ZELENO : samopreizkus gradbenika %d/%d ⊢ ( forma kanona ∧ vsa polja ×6 ∧ neznan zavrnjen )" % (n, n))
    else:
        print("RDEČO : samopreizkus gradbenika : padlov %d" % padci)
    return padci == 0


def main(argv):
    if "--samopreizkus" in argv:
        return 0 if samopreizkus() else 2
    if "--register" in argv:
        print(ŽIG)
        for vr in register():
            print("- " + vr)
        return 0
    imena = [a for a in argv[1:] if not a.startswith("--")]
    if not imena:
        print(ŽIG)
        print("rabš : gradbenik-pragmatike.py --gradbaj ⟨IME PADCA⟩ ⌇ --register ⌇ --samopreizkus")
        return 1
    try:
        print(zgradi(imena[0]))
    except ValueError as e:
        print("⚠ %s" % e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
