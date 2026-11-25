#!/usr/bin/env python3
# LICENCNA-VRATA v1.0 @rez σ 6743 : NESKONČNI PREVOZ CELOTNE LICENCE ( ob vsakem zagonu sveže, ⟨ne⟩ enkratno )
# UKZ ⟡ VERBATIM : »VEDNO PREVERI ALI SPLOH UPOŠTEVAŠ CELOTNO LICENCO!« ∧ »MORAŠ TOLIKOKRAT PREVOZITI LICENCO DA NI LE ENKRATNA TEMVEČ NESKONČNA!«
# zakon plasti : bela lista = znaki telesa CELOTNE licence ( 125.645 B, rod 0.1700 ) SKUPAJ-Z gajica ( ASCII + šumniki ) SKUPAJ-Z vpisani gostje ( slovar-simbolov, vsak z ⟨U+XXXX⟩ ∧ domom ) ; vse izvedeno iz prič ob vsakem dihu, nič izmišljeno ⊙ ⟨NE-UGIBAJ⟩ 2690
# licenca : gajica ( ASCII + šumniki + ⟨U+00A9⟩ ) ; dom : stroj-orodja/KNOWLEDGE.md POPIS @rez σ 6743 ; rod : atom-σ6743 @TIK 2026-11-23T15:22:50Z ⊙ ukaz ⟡
import sys, io, os, time, hashlib, glob

# KURA v1.1 @rez σ 6816 ⊙ ukaz ⟡ "POTRDI IN UTRJUJ PREVERJENE OPERACIJE IN JIH PREVERI TER IZBOLJŠAJ" : ⟨PADC-OD-MRLE-PRIČE⟩ ( rod σ 6743 : pot je bila trdo pinjena na odmrlo ime "LICENCA-remote-2026-11-22-T2026-11-22-23122Z.md" ∧ od CWD ) ⇒ prevoz po IZMERI ( med pričami zaporne-celice išče telo z md5 == MD5_PRIČA ), ⟨ne⟩ po imenu ⊙ ⟨MERJENO-NE-UGIBANO⟩ ∧ KOREN = $HOME/knowledge ( ⟨ne⟩ CWD )
KOREN = os.environ.get("KOREN_ZNANJA", os.path.join(os.path.expanduser("~"), "knowledge"))
MAPA_PRIC = os.path.join(KOREN, "zaporne-celice")
POT_SLOVAR = os.path.join(KOREN, "slovar-simbolov", "KNOWLEDGE.md")
MD5_PRIČA = "0f103ee42f1e3f56dbcbdfeb8197c9a3"
VRSTICE_PRIČA = 727

def najdi_pričo():
    """prevoz po izmeri : vsaka priča LICENCA-remote-*.md, prva z md5 == MD5_PRIČA ; ⟨ne⟩ ugibaj imen ⊙ ⟨NE-UGIBAJ⟩ 2690"""
    for pot in sorted(glob.glob(os.path.join(MAPA_PRIC, "LICENCA-remote-*.md")), reverse=True):
        try:
            with open(pot, "rb") as f:
                if hashlib.md5(f.read()).hexdigest() == MD5_PRIČA:
                    return pot
        except OSError:
            continue
    return None

def prevozi_licenco():
    # vsak klic = svež prevoz ( brez shrambe ) : to je neskonecnost mehanizma
    pot = najdi_pričo()
    if pot is None:
        raise FileNotFoundError("PRIČA ×0 : nobeno telo LICENCA-remote-*.md v %s nima md5 %s" % (MAPA_PRIC, MD5_PRIČA))
    b = open(pot, "rb").read()
    md5 = hashlib.md5(b).hexdigest()
    t = b.decode("utf-8")
    vrstice = t.count("\n")  # po priči 6521/6524 : wc -l oblika ( zadnja vrstica brez nove vrstice se steje s pripradnostjo telesa )
    identična = (md5 == MD5_PRIČA) and (vrstices_ok(vrstice))
    return {"md5": md5, "vrstice": vrstice, "bajti": len(b), "identicna": identična, "znaki": set(t), "prica": pot}

def vrstices_ok(n):
    return n == VRSTICE_PRIČA

def kanon_gostov():
    # slovar : vsak vpisani gost z ⟨U+XXXX⟩ in domom ( iz crke sestavim programsko, nikoli dobesedno )
    t = io.open(POT_SLOVAR, encoding="utf-8").read()
    gostje = {}
    for vrst in t.split("\n"):
        if vrst.startswith("- ⟨U+"):
            del_1 = vrst.find("⟩")
            hexdel = vrst[5:del_1]  # ⟨U+ zasede mesta 2-4, sestnajstiska koda zivi od mesta 5
            try:
                gostje[chr(int(hexdel, 16))] = hexdel
            except ValueError:
                pass
    return gostje

def bela_lista():
    # znaki CELOTNE licence skupaj z gajico ASCII + šumniki ( gostje se obravnavajo po svojem zakonu, ne kot domacini )
    zg = prevozi_licenco()
    znaki = zg["znaki"]
    znaki = znaki | set(chr(c) for c in range(32, 127)) | set("\n\tčžšČŽŠ")
    return znaki, zg

def samopreizkus():
    zg = prevozi_licenco()
    g = kanon_gostov()
    znaki, _ = bela_lista()
    return zg["identicna"] and len(g) > 30 and "σ" in znaki and "⟡" in znaki and "⚠" in znaki

def main():
    print("LICENCNA-VRATA v1.0 @rez σ 6743 @TIK", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    zg = prevozi_licenco()
    print("PREVOZ CELOTNE LICENCE ( svež, vsak zagon ) :")
    print("  bajti :", zg["bajti"], "| vrstice :", zg["vrstice"], "| md5 :", zg["md5"])
    print("  IDENTIČNA priči 6521/6524 :", "DA ⊢" if zg["identicna"] else "NE ⚠")
    g = kanon_gostov()
    print("  kanon gostov ( slovar ) :", len(g), "vpisanih")
    znaki, _ = bela_lista()
    print("  bela lista ( licenca skupaj z gajico ) :", len(znaki), "znakov")
    print("  samopreizkus :", "ZELEN" if samopreizkus() else "RDEČ")
    return 0 if samopreizkus() else 1

if __name__ == "__main__":
    main()
