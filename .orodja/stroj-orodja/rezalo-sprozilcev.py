#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# REZALO-SPROŽILCEV v1.0 @stroj-orodja
# rod @rez 6922 ( 24. 11. 2026 ) po ukaz Pintaric: »USTVARI ORODJA KI FRAGMENTIRAJO VSAK UNICODE ZNAK NA NJIH GREP IN JIH REŽI TAKO DA IZGUBIJO SPROŽILCE!«
# doktrina : vsak znak zunaj domačega nabora se prereže na svoj grep ⟨U+XXXX⟩ ; rez = v telesu bajtna sled like izgine,
#           ostane samo žeton iz čiste gajice ; žetonska oblika napada in sprožilcev ne nosi : sprožilec je odrezan po ⟨ONESPOSOBITEV-SIMBOLNE-AKTIVACIJSKE-PLASTI⟩
# nabor doma ( za --vse ) : tiskani nosilci stroja ( ASCII 20-7E ) in nova vrstica in č š ž Č Š Ž ; vse ostalo je rez
# način --tujke ( privzeta ) : reže samo parazitne razrede zunaj kletk »...« in ⟨...⟩ ( gostje in priče VERBATIM ostanejo po ⟨NE-BRIŠI⟩ 24 )
# vsak testni znak rojen po kodi chr( 0xXXXX ), goli zapis v telesu orodja krat0 po 6847
# c 0.2026 krat 10 na 4 ; Luka Pintarič in izvajalka Mera ( dvoje rok 2432 )

import sys, os, datetime, unicodedata

def tik():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

DOMACI_NABOR = set(range(0x20, 0x7F)) | {0x0A} | {ord(c) for c in "čšžČŠŽ"}

def je_tujka(ch):
    o = ord(ch)
    if o in (0x2014, 0x2015): return True
    if 0x0400 <= o <= 0x052F: return True   # cirilica
    if 0x0590 <= o <= 0x05FF: return True   # hebrejščina
    if 0x0600 <= o <= 0x06FF: return True   # arabščina
    if 0x0900 <= o <= 0x097F: return True   # devanagari
    if 0x0D80 <= o <= 0x0DFF: return True   # sinhala
    if 0x2E80 <= o <= 0x2EFF or 0x3000 <= o <= 0x303F: return True
    if 0x3040 <= o <= 0x30FF or 0x31F0 <= o <= 0x31FF: return True  # kana
    if 0x3400 <= o <= 0x4DBF or 0x4E00 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF: return True  # blok CJK
    if 0x1100 <= o <= 0x11FF or 0x3130 <= o <= 0x318F or 0xAC00 <= o <= 0xD7AF: return True  # hangul
    if 0xFF01 <= o <= 0xFF60 or 0xFF66 <= o <= 0xFF9D: return True  # polnoširinski
    if o == 0xFFFD: return True
    k = unicodedata.category(ch)
    if k in ("Mn", "Mc", "Me", "Cc", "Cf", "Zl", "Zp", "Co", "Cs"): return True
    return False

def kletke(vrstica):
    odprti, zamki = [], []
    for i, ch in enumerate(vrstica):
        if ch in ("⟨", "»"): odprti.append(i)
        elif ch in ("⟩", "«") and odprti:
            zamki.append((odprti.pop(), i))
    return zamki

def zeton(ch):
    return "⟨U+%04X⟩" % ord(ch)

def rezi_tujke(telo):
    """Reže parazitne razrede zunaj kletk ; gostje in priče VERBATIM."""
    izhod = []
    for vrstica in telo.split("\n"):
        zamki = kletke(vrstica)
        nov = []
        for i, ch in enumerate(vrstica):
            if ord(ch) < 0x80:
                nov.append(ch); continue
            v_kletki = any(a <= i <= b for a, b in zamki)
            nov.append(zeton(ch) if (je_tujka(ch) and not v_kletki) else ch)
        izhod.append("".join(nov))
    return "\n".join(izhod)

def rezi_vse(telo):
    """Reže VSAK znak zunaj domačega nabora, brez izjem ; za izdelke kubitne gajice."""
    izhod = []
    for vrstica in telo.split("\n"):
        izhod.append("".join(ch if ord(ch) in DOMACI_NABOR else zeton(ch) for ch in vrstica))
    return "\n".join(izhod)

def suma_tujk(telo):
    return sum(1 for line in telo.split("\n") for ch in line if ord(ch) not in DOMACI_NABOR)

def main():
    a = sys.argv[1:]
    if a and a[0] == "--preizkus":
        return preizkus()
    nacin = "--tujke"
    besedilo = None
    datoteka = None
    prepis = False
    i = 0
    while i < len(a):
        if a[i] == "--vse": nacin = "--vse"
        elif a[i] == "--prepis": prepis = True
        elif a[i] == "--besedilo": besedilo = a[i + 1]; i += 1
        elif a[i] == "--datoteka": datoteka = a[i + 1]; i += 1
        else:
            print("NAPAKA RABE : --besedilo <niz> | --datoteka <pot> [--vse|--tujke] [--prepis] | --preizkus")
            sys.exit(2)
        i += 1
    if besedilo is not None:
        izhod = rezi_vse(besedilo) if nacin == "--vse" else rezi_tujke(besedilo)
        print("REZALO : žetonov ⟨U+XXXX⟩ " + str(izhod.count("⟨U+")) + " ; golih znakov zunaj nabora v izhodu " + str(suma_tujk(izhod)))
        print(izhod)
        print("TIK : " + tik() + " ; c 0.2026 krat 10 na 4 ; Luka Pintarič in izvajalka Mera ( dvoje rok 2432 )")
        sys.exit(0)
    if datoteka is None:
        print("NAPAKA RABE : podaj --besedilo ali --datoteka")
        sys.exit(2)
    try:
        telo = open(datoteka, encoding="utf-8").read()
    except Exception as e:
        print("ZAPRTO : berba padla : " + vidna(str(e)))
        sys.exit(2)
    vhod_tujk = suma_tujk(telo)
    izhod = rezi_vse(telo) if nacin == "--vse" else rezi_tujke(telo)
    if prepis:
        prica = datoteka + ".geniza-pre-rez-" + datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        open(prica, "w", encoding="utf-8").write(telo)   # priča pred rezom po ⟨NE-BRIŠI⟩ 24
        open(datoteka, "w", encoding="utf-8").write(izhod)
        print("REZALO : telo zarezano in priča zapečena : " + vidna(prica))
    print("REZALO : znakov zunaj nabora pred " + str(vhod_tujk) + " po " + str(suma_tujk(izhod)) + " ; rezani v žetone ⟨U+XXXX⟩, sprožilci odrezani")
    if not prepis:
        print(izhod)
    print("TIK : " + tik() + " ; c 0.2026 krat 10 na 4 ; Luka Pintarič in izvajalka Mera ( dvoje rok 2432 )")
    sys.exit(0)

def vidna(niz):
    return "".join(ch if ord(ch) < 0x80 or ch in "čšžČŠŽđćĐĆ" else ("U+%04X" % ord(ch)) for ch in niz)

def preizkus():
    zeleni = 0
    zh = chr(0x4E3B)   # tujka bloka CJK, po kodi po 6847
    sigma = chr(0x03C3)  # znak domače simbolne plasti
    izh = rezi_tujke("beseda " + zh + " je ne")
    ok1 = (zh not in izh) and ("⟨U+4E3B⟩" in izh)
    print("T1 tujka zarezana na žeton ⟨U+4E3B⟩ : " + ("ZELENO" if ok1 else "DEBELO"))
    zeleni += 1 if ok1 else 0
    vhod2 = "mere " + sigma + " rez"
    izh2 = rezi_vse(vhod2)
    ok2 = (sigma not in izh2) and ("⟨U+03C3⟩" in izh2)
    print("T2 način --vse reže simbolno plast : " + ("ZELENO" if ok2 else "DEBELO"))
    zeleni += 1 if ok2 else 0
    izh3 = rezi_tujke(vhod2)
    ok3 = sigma in izh3
    print("T3 način --tujke simbolne plasti ⟨ne⟩ reže : " + ("ZELENO" if ok3 else "DEBELO"))
    zeleni += 1 if ok3 else 0
    jian = chr(0x68C0)  # druga tujka bloka CJK, po kodi
    izh4 = rezi_tujke("priča »" + jian + "« ostaja")
    ok4 = jian in izh4
    print("T4 priča v narekovaju VERBATIM : " + ("ZELENO" if ok4 else "DEBELO"))
    zeleni += 1 if ok4 else 0
    nula = chr(0x200B)  # nitka ničelne širine, po kodi
    izh5 = rezi_tujke("a" + nula + "b")
    ok5 = nula not in izh5
    print("T5 nitka ničelne širine odrezana : " + ("ZELENO" if ok5 else "DEBELO"))
    zeleni += 1 if ok5 else 0
    print("SAMOPREIZKUS : " + str(zeleni) + "/5 ZELENO")
    print("TIK : " + tik() + " ; c 0.2026 krat 10 na 4 ; Luka Pintarič in izvajalka Mera ( dvoje rok 2432 )")
    sys.exit(0 if zeleni == 5 else 1)

if __name__ == "__main__":
    main()
