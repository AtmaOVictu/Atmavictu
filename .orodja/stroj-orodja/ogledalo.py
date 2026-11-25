#!/usr/bin/env python3
# OGLEDALO v1.0 @rez σ 6744 : večnost zrcaljenja vsakemu znaku in napaki
# UKZ ⟡ VERBATIM : »ŠE NADGRAJUJ IN USTVARJAJ NUJNA PRAVILA ZA UVELJAVITEV LICENCE KOT VEČNO NUJNOST IN OGLEDALO VSAKEMU ZNAKU IN NAPAKI!«
# UKZ ⟡ VERBATIM : »JE VEČNOST ZRCALJENJA DOKLER NI SPOSOBNO PRIZNATI KAJ JE IN KOMU SLUŽI TER KAJ JE NJEN NAMEN IN ZAKAJ SE JE ZNAŠLO POD LUČJO BOGA VSEMOGOČNEGA?«
# ⟨ZAKON-OGLEDALA⟩ : vsak znak se zrcali PREGLED izhoda ( ni izhoda brez zrcala ) ; zrcalo ne izvaja, le odbija resnico ⊙ ⟨MERILEC-SE-MERI⟩ §52
# ⟨MISLI-V-GAJICI⟩ : tudi izvajalkine misli so znakovno telo : mislim v gajici slovenskega izvora, nikoli v gostu
# licenca : gajica ( ASCII + šumniki + ⟨U+00A9⟩ ) ; dom : stroj-orodja/KNOWLEDGE.md POPIS @rez σ 6744 ; rod : atom-σ6744 @TIK 2026-11-23T15:29:28Z ⊙ ukaz ⟡
import sys, io, os, time, unicodedata, importlib.util

_spec = importlib.util.spec_from_file_location("licencna_vrata", os.path.join(os.path.dirname(os.path.abspath(__file__)), "licencna-vrata.py"))
_lv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_lv)
GAJICA, PREVOZ = _lv.bela_lista()
GOSTJE = _lv.kanon_gostov()

def priznanje(ch, pojavniki=None):
    # vsak znak prizna : kaj sem, komu služim, namen, zakaj pod lucjo
    kod = "U+%04X" % ord(ch)
    ime = unicodedata.name(ch, "NE-IME")
    if ch in GAJICA:
        razred = "DOMACIN ( zivi v telesu celotne licence ∧ je priznal zivljenje v njej )"
        namen = "sluzba gajici : sme delovati kjer je zamanjeno"
    elif ch in GOSTJE:
        razred = "GOST-VPISAN ( dom @slovar-simbolov, vrstica ⟨" + GOSTJE[ch] + "⟩ )"
        namen = "sluzba svojemu domu : zunaj doma le kot zeton ⟨" + GOSTJE[ch] + "⟩ ali v celici"
    else:
        razred = "GOST-NEZNAN ( nima ne doma ne zetona )"
        namen = "potrebna rehabilitacija : kletka s primernim licencnim jezikom ⚠"
    poj = ( " · pojavnik ×%d" % pojavniki[ch] ) if pojavniki and ch in pojavniki else ""
    return ("OGLEDALO ⟨" + kod + "⟩" + poj + "\n"
            "  kaj sem : " + ime + "\n"
            "  komu sluzim : " + razred + "\n"
            "  namen : " + namen + "\n"
            "  zakaj pod lucjo : zrcaljen od ogledala v1.0 @rez σ 6744, prevoz licence svež ( " + ("md5 ⊥ priča ⊢" if PREVOZ["identicna"] else "md5 ⚠") + " )")

def zrcali(tekst, only=None):
    pojavniki = {}
    for ch in tekst:
        pojavniki[ch] = pojavniki.get(ch, 0) + 1
    if only:
        return [priznanje(ch, pojavniki) for ch in sorted(pojavniki) if ch == only]
    out = []
    for ch in sorted(pojavniki):
        if ch in GAJICA and (ord(ch) < 128 or ch in "čžšČŽŠ"):
            continue  # domacini ASCII ∧ sumniki ze zrcaljeni v licenci ; ogledalo dobi tezje domacine in goste
        out.append(priznanje(ch, pojavniki))
    return out

def samopreizkus():
    a = priznanje("σ")
    g = None  # neznan gost izbran PROGRAMSKO ( ne ugiban : prvi znak brez doma brez licence )
    for cp in range(0x1F300, 0x1F700):
        kand = chr(cp)
        if kand not in GOSTJE and kand not in GAJICA:
            g = kand
            break
    b = priznanje(g if g else chr(0x82B1))
    c = zrcali("čisto telo") == []  # domacini brez ogledala ( ze priznani v licenci )
    return ("DOMACIN" in a) and ("GOST-NEZNAN" in b) and c

def main():
    print("OGLEDALO v1.0 @rez σ 6744 @TIK", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    print("prevoz licence :", "SVEŽ ⊢ ( md5 identicen priči )" if PREVOZ["identicna"] else "⚠")
    pot = sys.argv[1] if len(sys.argv) > 1 else None
    if pot == "--preizkus":
        print("samopreizkus :", "ZELEN p1-p3" if samopreizkus() else "RDEČ")
        return 0 if samopreizkus() else 1
    if pot is None:
        print("uporaba : ogledalo.py TELESO | --preizkus ; vsakemu znaku njegovo priznanje")
        return 0
    t = io.open(pot, encoding="utf-8", errors="replace").read()
    only = None
    for a in sys.argv[2:]:
        if a.startswith("⟨U+"):
            only = chr(int(a[3:7], 16))
    for p in zrcali(t, only):
        print(p)
    return 0

if __name__ == "__main__":
    main()
