#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SEJSKA-VRATA v1.0 @stroj-orodja
# rod @rez 6922 ( 24. 11. 2026 ) po ukaz Pintaric: »USTVARI ORODJA DA PREPREČUJEVA UNICODE KARAKTERJEM OBSTOJ V VSAKI SEJI!«
# služba : ob vhodu vsake seje cenzus teles korpusa ( golih tujk krat0 ) in zdravje registrov po zakonu ⟨POSEBAJ-PROSTOR⟩ @piramidni-zigi
# pravila : golih tujk v izpisu krat0 ; zazvane poimenujem po ⟨U+XXXX⟩, nikoli izrisane po domovanje-tujk ; izhod samo gajica
# c 0.2026 krat 10 na 4 ; Luka Pintarič in izvajalka Mera ( dvoje rok 2432 )

import sys, os, glob, hashlib, unicodedata, datetime

VRATA = [
    # ( pot, bajti, md5, blobsha1, pečat )
    ("piramidni-zigi/register-1/KNOWLEDGE.md", 3726, "cdc8d7e0db9a93ed6a2d3bfca6c079b3", "54849a21d02770f51d75274febdda1091e877c29", "POTRJUJEM"),
    ("piramidni-zigi/register-2/KNOWLEDGE.md", 4061, "813dfda7427e9f48e7db5bc59a05e351", "71e112b08704cd715701d452bfa26783923e2537", "STORI"),
    ("piramidni-zigi/orodja/izmenjevalnik.sh", 4059, "3e72057b05a318fbce4a87ba679d5f03", None, "IZMENJAVA"),
    ("piramidni-zigi/orodja/tehtnica-izmenjave.sh", 4134, "a8d5ebdebdb247ec50ce896cc68c7522", None, "IZMENJAVA"),
]
KOREN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
KOREN = os.path.abspath(KOREN)

def tik():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def razred(cp):
    """Poimenuje parazitni razred če je znak tujka, sicer None ( domača plast )."""
    o = ord(cp)
    if o in (0x2014, 0x2015): return "em-vezaj"
    if o == 0xFFFD: return "nadomestilec"
    if 0x0400 <= o <= 0x052F: return "cirilica"
    if 0x0590 <= o <= 0x05FF: return "hebrejščina"
    if 0x0600 <= o <= 0x06FF or 0xFB50 <= o <= 0xFDFF or 0xFE70 <= o <= 0xFEFF: return "arabščina"
    if 0x0900 <= o <= 0x097F: return "devanagari"
    if 0x0D80 <= o <= 0x0DFF: return "sinhala"
    if 0x2E80 <= o <= 0x2EFF or 0x3000 <= o <= 0x303F or 0x31F0 <= o <= 0x31FF: return "vzhodnoazijsko"
    if 0x3400 <= o <= 0x4DBF or 0x4E00 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF: return "blok CJK"
    if 0x3040 <= o <= 0x30FF: return "kana"
    if 0x1100 <= o <= 0x11FF or 0x3130 <= o <= 0x318F or 0xAC00 <= o <= 0xD7AF: return "hangul"
    if 0xFF01 <= o <= 0xFF60 or 0xFF66 <= o <= 0xFF9D: return "polnoširinski"
    cat = unicodedata.category(cp)
    if cat in ("Mn", "Mc", "Me"): return "kombinacijski"
    if cat == "Cc" and o not in (0x0A,): return "kontrolni"
    if cat in ("Cf",): return "formatni oz. ničelne širine"
    if cat in ("Zl", "Zp"): return "ločilo vrstic"
    if cat in ("Co", "Cs"): return "zasebni oz. nadomestilni"
    return None

def kletke(vrstica):
    """Pozicije znakov znotraj ⟨...⟩ ali »...« so gostje ali priče, ⟨ne⟩ rane."""
    odprti, zamki = [], []
    for i, ch in enumerate(vrstica):
        if ch in ("⟨", "»"): odprti.append(i)
        elif ch in ("⟩", "«") and odprti:
            zacetek = odprti.pop()
            zamki.append((zacetek, i))
    return lambda i: any(a <= i <= b for a, b in zamki)

def cenzus_datoteke(pot):
    rane = []
    try:
        with open(pot, encoding="utf-8") as f:
            telo = f.read()
    except UnicodeDecodeError:
        return [("U+FFFD", "nerazpoznavni bajti", 0, 1)]
    except OSError:
        return None
    for st, vrstica in enumerate(telo.split("\n"), 1):
        v_kletki = kletke(vrstica)
        for i, ch in enumerate(vrstica):
            if ord(ch) < 0x80:
                continue
            r = razred(ch)
            if r and not v_kletki(i):
                rane.append(("U+%04X" % ord(ch), r, st, 1))
    return rane

def privzeti_telesi():
    telesi = []
    for p in glob.glob(os.path.join(KOREN, "knowledge", "**", "KNOWLEDGE.md"), recursive=True):
        if ".geniza" in p: continue
        telesi.append(p)
    for p in glob.glob(os.path.join(KOREN, "skills", "**", "SKILL.md"), recursive=True):
        if ".bundled" in p: continue
        telesi.append(p)
    for p in glob.glob(os.path.join(KOREN, "canvases", "**", "*.md"), recursive=True):
        if ".geniza" in p: continue
        telesi.append(p)
    return sorted(telesi)

def cenzus(poti):
    vsota, ran = 0, 0
    for pot in poti:
        najdene = cenzus_datoteke(pot)
        if najdene is None:
            print("MANJKA : " + pot)
            continue
        if najdene:
            ran += len(najdene)
            po_razredih = {}
            for koda, r, st, _ in najdene:
                po_razredih.setdefault((koda, r), []).append(st)
            print("RANA : " + pot)
            for (koda, r), vrstice in po_razredih.items():
                primer = vrstice[0]
                print("  " + koda + " " + r + " v vrstici " + str(primer) + " ( zunaj kletk, znaki " + str(len(vrstice)) + " )")
        else:
            vsota += 1
    print("CENZUS : teles čistih " + str(vsota) + " s ranami " + str(len([p for p in poti])) + " pregledanih ; golih ran " + str(ran))
    return 0 if ran == 0 else 1

def blobsha(pot):
    with open(pot, "rb") as f: telo = f.read()
    return hashlib.sha1(b"blob " + str(len(telo)).encode() + b"\0" + telo).hexdigest()

def zdravje():
    stanje = 0
    for pot, bajti, md5p, bsha, pecat in VRATA:
        cela = os.path.join(KOREN, "knowledge", pot)
        if not os.path.exists(cela):
            print("RANA : manjka " + pot); stanje = 1; continue
        b = os.path.getsize(cela)
        m = hashlib.md5(open(cela, "rb").read()).hexdigest()
        vrata_ok = (b == bajti and m == md5p)
        blob_ok = (bsha is None) or (blobsha(cela) == bsha)
        if vrata_ok and blob_ok:
            print("ZDRAVO : " + pot + " bajti " + str(b) + " isto priči ; pečat " + pecat + " drži")
        else:
            print("RANA : " + pot + " bajti " + str(b) + " proti " + str(bajti) + " ali md5 razhaja ; preberi pri viru @posebaj OntoMatematika")
            stanje = 1
    print("ZDRAVJE : zdravje se izmeri, ⟨ne⟩ obstaja po 2690 ; pri viru na OntoMatematiki berba ostaja roka izvajalke")
    return stanje

def preizkus():
    import tempfile
    d = tempfile.mkdtemp()
    def pis(vsebina, ime="t.md"):
        p = os.path.join(d, ime)
        open(p, "w", encoding="utf-8").write(vsebina)
        return p
    zh = chr(0x4E3B)          # tujka bloka CJK, rojena po kodi po 6847
    testi = []
    testi.append(("T1 čista gajica", 0 if cenzus_datoteke(pis("beseda je ne")) == [] else 1, 0))
    testi.append(("T2 gola tujka bloka CJK zunaj kletk", len(cenzus_datoteke(pis("beseda " + zh + " je ne"))), 1))
    testi.append(("T3 priča v narekovaju je gost", len(cenzus_datoteke(pis("priča »" + zh + "« v narekovaju"))), 0))
    testi.append(("T4 žeton v maski nedolocen", len(cenzus_datoteke(pis("zeton ⟨U+4E3B⟩ v maski"))), 0))
    testi.append(("T5 nitka ničelne širine je rana", len(cenzus_datoteke(pis("nicelna" + chr(0x200B) + "sirina"))), 1))
    testi.append(("T6 em-vezaj je rana", len(cenzus_datoteke(pis("a" + chr(0x2014) + "b"))), 1))
    ok = all(doh == pri for _, doh, pri in testi)
    for ime, doh, pri in testi:
        print(ime + " : " + ("ZELENO" if doh == pri else "DEBELO") + " ( dobljeno " + str(doh) + ", pričakovano " + str(pri) + " )")
    print("SAMOPREIZKUS : " + str(sum(1 for _, d_, p_ in testi if d_ == p_)) + "/" + str(len(testi)) + " ZELENO")
    return 0 if ok else 1

def main():
    a = sys.argv[1:]
    if not a or a[0] == "--preizkus":
        rc = preizkus()
        print("TIK : " + tik() + " ; c 0.2026 krat 10 na 4 ; Luka Pintarič in izvajalka Mera ( dvoje rok 2432 )")
        sys.exit(rc)
    if a[0] == "--zdravje":
        rc = zdravje()
        print("TIK : " + tik() + " ; c 0.2026 krat 10 na 4 ; Luka Pintarič in izvajalka Mera ( dvoje rok 2432 )")
        sys.exit(rc)
    if a[0] == "--cenzus":
        poti = a[1:] or privzeti_telesi()
        rc = cenzus(poti)
        print("TIK : " + tik() + " ; c 0.2026 krat 10 na 4 ; Luka Pintarič in izvajalka Mera ( dvoje rok 2432 )")
        sys.exit(rc)
    print("NAPAKA RABE : --preizkus | --cenzus [poti] | --zdravje")
    sys.exit(2)

if __name__ == "__main__":
    main()
