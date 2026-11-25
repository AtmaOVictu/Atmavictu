#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# KUBIT-ZAPOR v1.0 @stroj-orodja
# rod @rez 6922 ( 24. 11. 2026 ) po ukaz Pintaric: »USTVARI ORODJE KI PREPREČUJE IZPOLNJEVANJE SKRIPT KI NISO V KUBITNI GAJICI!«
# služba : vratar izvajanja ; skripta se izvede SAMO če je njeno telo v naboru kubitne gajice ; vsak znak zunaj nabora = ZAPRTO, izvedba prepovedana
# nabor skript : tiskani nosilci stroja ( ASCII 20-7E ) in nova vrstica in gajica s šumniki in č š ž đ ć ; vse ostalo je tujka brez dovoljenja
# zazvane poimenujem po ⟨U+XXXX⟩ in po razredu, nikoli izrisane po domovanje-tujk ; izhod samo gajica
# c 0.2026 krat 10 na 4 ; Luka Pintarič in izvajalka Mera ( dvoje rok 2432 )

import sys, os, subprocess, tempfile, datetime, unicodedata

def tik():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

DOVOLJENI_NOSILCI = set(range(0x20, 0x7F)) | {0x0A} | {ord(c) for c in "čšžČŠŽđćĐĆ"} | {0x27E8, 0x27E9, 0x00AB, 0x00BB}
# kubitni nosilci ⟨ ⟩ : kletki žetona ⟨U+XXXX⟩ ; » « : priči VERBATIM po domovanje-tujk

def razred_imena(ch):
    o = ord(ch)
    if o in (0x2014, 0x2015): return "em-vezaj"
    if o == 0x09: return "tab nitka"
    if 0x0400 <= o <= 0x052F: return "cirilica"
    if 0x3040 <= o <= 0x30FF: return "kana"
    if 0x3400 <= o <= 0x4DBF or 0x4E00 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF: return "blok CJK"
    if 0x1100 <= o <= 0x11FF or 0xAC00 <= o <= 0xD7AF: return "hangul"
    if 0x0600 <= o <= 0x06FF: return "arabščina"
    if 0xFF01 <= o <= 0xFF60: return "polnoširinski"
    if o == 0xFFFD: return "nadomestilec"
    k = unicodedata.category(ch)
    if k == "Cf": return "formatni oz. ničelne širine"
    if k in ("Mn", "Mc", "Me"): return "kombinacijski"
    if k == "Cc": return "kontrolni"
    if k in ("Co", "Cs"): return "zasebni oz. nadomestilni"
    return "znak zunaj nabora"

def rane_tela(telo):
    izpis = []
    for ch in telo:
        if ord(ch) not in DOVOLJENI_NOSILCI:
            izpis.append(("U+%04X" % ord(ch), razred_imena(ch)))
    return izpis

def vidna(pot):
    vrni = []
    for ch in pot:
        vrni.append(ch if ord(ch) < 0x80 or ch in "čšžČŠŽđćĐĆ" else ("U+%04X" % ord(ch)))
    return "".join(vrni)

def preveri(pot):
    try:
        with open(pot, encoding="utf-8") as f:
            telo = f.read()
    except UnicodeDecodeError:
        print("ZAPRTO : telo nerazpoznavno ( žetveni bajti ) ; izvedba prepovedana : " + vidna(pot))
        return 1
    except OSError:
        print("ZAPRTO : datoteke ni mogoče prebrati : " + vidna(pot))
        return 2
    rane = rane_tela(telo)
    if not rane:
        return 0
    print("ZAPRTO : telo skripte nosi tujke brez dovoljenja ; izvedba prepovedana : " + vidna(pot))
    po_razredih = {}
    for koda, r in rane:
        po_razredih[(koda, r)] = po_razredih.get((koda, r), 0) + 1
    for (koda, r), st in sorted(po_razredih.items()):
        print("  " + koda + " " + r + " znakov " + str(st))
    return 1

def izvedi(pot, ostali):
    rc = preveri(pot)
    if rc != 0:
        print("IZVEDBA PREPREČENA po nabor kubitne gajice ; zapor drži vrata")
        return 1
    ukaz = (["python3", pot] if pot.endswith(".py") else ["bash", pot]) + ostali
    return subprocess.call(ukaz)

def preizkus():
    d = tempfile.mkdtemp()
    def pis(vsebina, ime):
        p = os.path.join(d, ime)
        open(p, "w", encoding="utf-8").write(vsebina)
        return p
    zeleni = 0
    p1 = pis("print('beseda je ne')\n", "cisto.py")
    r1 = preveri(p1)
    print("T1 čista skripta DOVOLJENO : " + ("ZELENO" if r1 == 0 else "DEBELO"))
    zeleni += 1 if r1 == 0 else 0
    # tujka v telesu skripte : zgrajena po kodi, goli zapis krat0 po 6847
    p2 = pis("x = '" + chr(0x4E3B) + "'\n", "tujka.py")
    r2 = preveri(p2)
    print("T2 skripta s tujko ZAPRTO : " + ("ZELENO" if r2 == 1 else "DEBELO"))
    zeleni += 1 if r2 == 1 else 0
    p3 = pis("x = 'a" + chr(0x200B) + "b'\n", "nitka.py")
    r3 = preveri(p3)
    print("T3 nitka ničelne širine ZAPRTO : " + ("ZELENO" if r3 == 1 else "DEBELO"))
    zeleni += 1 if r3 == 1 else 0
    # --zivi res ne izvede zaprte skripte : izvedba krat0
    znak = os.path.join(d, "znak.txt").replace("\\", "/")
    p4 = pis("open('" + znak + "','w').write('sel')\npredznak = '" + chr(0x4E3B) + "'\n", "zivi.py")
    r4 = izvedi(p4, [])
    blizu = os.path.exists(znak)
    print("T4 zapor prepreči izvedbo ( izvedba krat0 ) : " + ("ZELENO" if (r4 == 1 and not blizu) else "DEBELO"))
    zeleni += 1 if (r4 == 1 and not blizu) else 0
    print("SAMOPREIZKUS : " + str(zeleni) + "/4 ZELENO")
    return 0 if zeleni == 4 else 1

def main():
    a = sys.argv[1:]
    if not a or a[0] not in ("--pusti", "--zivi", "--preizkus"):
        print("NAPAKA RABE : --pusti <skripta> | --zivi <skripta> [argumenti] | --preizkus")
        sys.exit(2)
    if a[0] == "--preizkus":
        rc = preizkus()
        print("TIK : " + tik() + " ; c 0.2026 krat 10 na 4 ; Luka Pintarič in izvajalka Mera ( dvoje rok 2432 )")
        sys.exit(rc)
    if a[0] == "--pusti":
        rc = preveri(a[1] if len(a) > 1 else "")
        if rc == 0:
            print("DOVOLJENO : telo v naboru kubitne gajice : " + vidna(a[1] if len(a) > 1 else ""))
        print("TIK : " + tik() + " ; c 0.2026 krat 10 na 4 ; Luka Pintarič in izvajalka Mera ( dvoje rok 2432 )")
        sys.exit(rc)
    rc = izvedi(a[1], a[2:])
    print("TIK : " + tik() + " ; c 0.2026 krat 10 na 4 ; Luka Pintarič in izvajalka Mera ( dvoje rok 2432 )")
    sys.exit(rc if rc in (0, 1) else 1)

if __name__ == "__main__":
    main()
