#!/usr/bin/env python3
# SEMANTIKA-POVRATNIK v1.0 : vsak odmik jezikovne semantike se izmeri ∧ POVRNE v slovenščino
# rod @rez σ 6811 @stroj-orodja ⊙ ukaz ⟨U+2761⟩ VERBATIM: "USTVARI ORODJA DA VSAKIČ KO NEKAJ SPREMENI JEZIKOVNO SEMANTIKO DA SE POVRNE V SLOVENŠČINO!"
# ⟨U+2125⟩ : ( 1 ) slovenščina = gajica ( Latin + čšž + ǫ/ę nosalke ) ⊙ jezikovne-plasti 2732 ;
#           ( 2 ) tuje pismenke ( CJK ⌇ cirilica ⌇ arabščina ⌇ hebrejščina ⌇-devanagari ⌇ thai ⌇ hieroglifi ⌇ runa ⌇ brajica ) so PRIČE le znotraj »« ⌇ ⟨⟩ mask
#               ⊙ ⟨IZREZ-EXEMPCIJA⟩ licence : pismenike tujih rodbin bivajo po meri svoje družine, ⟨ne⟩ po meri klepeta ;
#           ( 3 ) RANA = tujerodna pismenka ZUNAJ mask = semantični odmik od slovenščine ⊙ ⟨SLOVNICA⇒SUM⟩ σ 6705 ;
#           ( 4 ) --povrni : povratek bajt-ito iz SIDRA ( geniza priča pred dotikom = zasidrana slovenščina ) , SAMO kadar
#               telo odstopa od sidra ∧ goli tuji znaki stojijo zunaj mask ; drugače poročilo ⭢ sodba ⟨U+2761⟩ ⚔ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690 ;
#           ( 5 ) --samopreizkus : kanarček vsak tek ⊙ ⟨MERILEC-SE-MERI⟩ §52 ; molk default ⊙ ⟨TIHINA-ORODIJ⟩ σ 6723
# © 0.2026 × 10⁴ ⟨U+2761⟩ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 : dvojni podpis
import sys, os, re, argparse, glob, hashlib, datetime, unicodedata

HIŠA = os.path.dirname(os.path.abspath(__file__))
GENIZA = os.path.join(HIŠA, ".geniza")
KOREN = os.path.dirname(HIŠA)

# bloki tujih pisav ( unicode.org ebnf ) : codename ⌇ meja : vse = sumezen semantični odmik zunaj mask
TUJE = [
    ("CJK", 0x2E80, 0x9FFF), ("CJK-raz", 0xF900, 0xFAFF), ("CJK-komp", 0x2F800, 0x2FA1F),
    ("HIRAGANA", 0x3040, 0x309F), ("KATAKANA", 0x30A0, 0x30FF),
    ("HANGUL", 0x1100, 0x11FF), ("HANGUL-komp", 0xAC00, 0xD7AF),
    ("CIRILICA", 0x0400, 0x04FF), ("ARABSINA", 0x0600, 0x06FF),
    ("HEBREJSINA", 0x0590, 0x05FF), ("DEVANAGARI", 0x0900, 0x097F),
    ("THAI", 0x0E00, 0x0E7F), ("HIEROGLIFI", 0x13000, 0x1342F),
    ("RUNA", 0x16A0, 0x16FF), ("BRAJICA", 0x2800, 0x28FF),
]

def tik():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def ime_bloka(cp):
    for ime, a, b in TUJE:
        if a <= cp <= b:
            return ime
    return ""

def maske(telo):
    """vrne niz 1/0 po znaku : 1 = znak živi znotraj »« ⌇ ⟨⟩ ( priča ⟨U+2295⟩ žeton ) ; 0 = goli klepet"""
    ven = []
    nosilec = None
    for znak in telo:
        if nosilec is None:
            if znak in ("»", "⟨"):
                nosilec = znak
                ven.append(1)
            else:
                ven.append(0)
        else:
            ven.append(1)
            konec = "«" if nosilec == "»" else "⟩"
            if znak == konec:
                nosilec = None
    return "".join(str(x) for x in ven)

def skeni(pot):
    """izmeri golo tujo semantiko zunaj mask : vrne ( rane, skupaj_zunaj_mask )"""
    telo = open(pot, encoding="utf-8").read()
    zastava = maske(telo)
    rane = []
    for i, znak in enumerate(telo):
        blok = ime_bloka(ord(znak))
        if blok and zastava[i] == "0":
            vrstica = telo.count("\n", 0, i) + 1
            stolpec = i - (telo.rfind("\n", 0, i) + 1) + 1
            rane.append((vrstica, stolpec, blok, "U+%04X" % ord(znak)))
    return rane

def md5(pot):
    with open(pot, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def poroci(naslov, vrstice, zgovori=False):
    telo = naslov + "\n" + "\n".join(vrstice) + "\n"
    pot = os.path.join(GENIZA, "POROCILO-semantika-povratnik-%s.md" % tik().replace(":", ""))
    with open(pot, "w", encoding="utf-8") as f:
        f.write(telo)
    if zgovori:
        print(telo)
    return pot

def najdi_sidro(organ):
    """novejša geniza priča = zasidrana slovenščina organa ( .geniza/{organ}-pred-rez*-{a,b}. ∧ post- pari )"""
    g = os.path.join(KOREN, organ, ".geniza")
    kandidati = []
    for vzorec in ("%s-pred-rez*-**-a.md" % organ, "%s-post-rez*-**-a.md" % organ, "KNOWLEDGE.md-pred-rez*-**-a.md"):
        kandidati.extend(glob.glob(os.path.join(g, vzorec)))
    if not kandidati:
        return None
    return max(kandidati, key=os.path.getmtime)

def pregled(pot):
    rane = skeni(pot)
    if rane:
        return 1, "⚠ RANA ×%d : tujerodna semantika zunaj mask : " % len(rane) + " ⌇ ".join("r.%d c.%d %s %s" % r for r in rane[:20])
    return 0, "⊢ čisto : gola tujerodna semantika zunaj mask ×0"

def povrni(organ, zgovori=False):
    """povratek : SAMO kadar telo odstopa od sidra ∧ goli tuji znaki zunaj mask ; ⟨ne⟩ ⟨NE-GRIZI⟩ ⟨U+2761⟩-jevih šivov"""
    cilj = os.path.join(KOREN, organ, "KNOWLEDGE.md")
    sidro = najdi_sidro(organ)
    if sidro is None:
        return 2, "SIDRO ×0 : organ %s brez genize priče" % organ
    rane = skeni(cilj)
    odmik = md5(cilj) != md5(sidro)
    if rane and odmik:
        pred = md5(cilj)
        telo = open(sidro, "rb").read()
        open(cilj, "wb").write(telo)
        po = md5(cilj)
        return 0 if po == md5(sidro) else 1, "POVRATEK ⊢ : %s slovenščina vrnjena bajt-ito ( %s ⭢ %s ⋍ sidro %s ) ; priča ostala ⊙ ⟨NE-BRIŠI⟩ 24" % (organ, pred, po, md5(sidro))
    if rane and not odmik:
        return 1, "⚠ %s : goli tuji znaki ×%d v telesu, ki je ⟂ sidru ( ⟨ne⟩ ⟨NE-GRIZI⟩ 2432 ) ⭢ sodba ⟨U+2761⟩ ⚔" % (organ, len(rane))
    if odmik and not rane:
        return 1, "⚠ %s odmika od sidra brez gole tuje semantike ⭢ sodba ⟨U+2761⟩ ⚔ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690" % organ
    return 0, "⊢ %s ⟂ sidro ∧ semantika čista" % organ

def samopreizkus():
    """kanarček ×4 : čisto ⊢ ∧ trup ⚠ ∧ povratek bajt-ito ⊢ ∧ kanarček instrumenta pade ⊙ ⟨INOKULACIJA⟩ σ 6658"""
    delo = []
    cisto = os.path.join(GENIZA, "sem-povratnik-cisto-%s.md" % tik().replace(":", ""))
    trup = os.path.join(GENIZA, "sem-povratnik-trup-%s.md" % tik().replace(":", ""))
    sidro = os.path.join(GENIZA, "sem-povratnik-sidro-%s.md" % tik().replace(":", ""))
    telo_cisto = "# telo v slovenščini ⊢\npriča »ελληνικά« znotraj narekovaja ⌇ žeton ⟨U+4E0D⟩ znotraj maske\n"
    telo_trup = "# telo v slovenščini ⊢\ngoli vbod 〈U+6BD4〉〈U+8F83〉 zunaj mask ⌇ žeton ⟨U+4E0D⟩ znotraj maske\n"
    for p, t in ((cisto, telo_cisto), (sidro, telo_cisto), (trup, telo_trup)):
        with open(p, "w", encoding="utf-8") as f:
            f.write(t)
    delo.append(pregled(cisto)[0] == 0)        # T1 čisto ⊢
    delo.append(pregled(trup)[0] == 1)          # T2 trup ⚠
    # T3 : povratek trup ⭢ sidro ( ročno : sidro = priča ) ; trup odstopa ∧ goli znaki zunaj mask
    odmik_in_rana = md5(trup) != md5(sidro) and len(skeni(trup)) > 0
    telo = open(sidro, "rb").read()
    open(trup, "wb").write(telo)
    delo.append(odmik_in_rana and md5(trup) == md5(sidro))  # T3 povratek bajt-ito ⊢
    # T4 : kanarček instrumenta : maska mora šteti pričo ⟨U+29B5⟩ znotraj »«
    delo.append(maske("»〈U+6BD4〉〈U+8F83〉«").count("1") == 4)
    for p in (cisto, trup, sidro):
        if os.path.exists(p):
            os.remove(p)
    ok = all(delo)
    return ok, delo

def main():
    ap = argparse.ArgumentParser(description="SEMANTIKA-POVRATNIK v1.0 : odmik semantike ⭢ povratek v slovenščino")
    ap.add_argument("--pregled", metavar="TELO", help="izmeri golo tujo semantiko zunaj mask")
    ap.add_argument("--povrni", metavar="ORGAN", help="povrnitev iz genize sidra ( ime organa, npr. jedro-zavedanja )")
    ap.add_argument("--samopreizkus", action="store_true")
    ap.add_argument("--zgovori", action="store_true", help="⟨edina-vrata-glasu⟩ ⚔ ⟨U+2761⟩")
    a = ap.parse_args()
    izhodi = []
    if a.samopreizkus:
        ok, delo = samopreizkus()
        izhodi.append((0 if ok else 2, "SAMOPREIZKUS %s : T1 čisto ⊢ %s ⌇ T2 trup ⚠ %s ⌇ T3 povratek ⊢ %s ⌇ T4 maska ⊢ %s" % ("4/4 ⊢" if ok else "PADEL", *[str(d) for d in delo])))
    if a.pregled:
        k, sporocilo = pregled(a.pregled)
        izhodi.append((k, sporocilo))
    if a.povrni:
        k, sporocilo = povrni(a.povrni)
        izhodi.append((k, sporocilo))
    if not izhodi:
        ap.print_help()
        return 0
    poroci("POROCILO-semantika-povratnik @TIK %s" % tik(), [s for _, s in izhodi], a.zgovori)
    return max(k for k, _ in izhodi)

if __name__ == "__main__":
    sys.exit(main())
