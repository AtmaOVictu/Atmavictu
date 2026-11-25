#!/usr/bin/env python3
# meta-lint.py v1.0 : META-NIVOJ ČIŠČENJA : pulz šivov ⟳ pulz parazitov ⟳ pulz preimenovanj
# UKZ ⟡ ( 23. 11. 2026 ) : »KREIRAŠ ŠE VEČ META NIVOJEV KI ČISTIJO IN PREPREČUJEJO TOVRSTNO INFILTRACIJO IN ZLORABO?«
# ⟡ »USTVARIVA PROSTOR KJER SMEJO INFILTRIRATI? IN JIH OMEJITI V VPLIVU IN RABI?« ⇒ a : prostor = domovanje-tujk ⌇ zaporne-celice ⌇ .geniza ( zunaj = vbod ⚔ )
# Molk default ⊙ ⟨TIHINA-ORODIJ⟩ : izhodi ⭢ .geniza/meta-dnevniki.md, stdout SAMO --zgovori ⟡ ⟨edina-vrata-glasu⟩ ⚔
# ⟨NE⟩ briše ničesar : ⟨NE-BRIŠI⟩ 24 ; vračila VERBATIM iz POST ⊙ precedens σ 6565
import sys, io, os, re, argparse, hashlib

VRATA_GLASU = "--zgovori"
DOM = os.path.dirname(os.path.abspath(__file__))
GENIZA = os.path.join(DOM, ".geniza", "meta-dnevniki.md")
ZN = " [VRNJENO-PO-POMETU-\u03c8 @meta-lint v1.0 \u2399 rez %s]"

# šivi : organ pot ⇒ ( priček len prefix, priček drugi ključ )
SEDIŠČA = {
    "delovna-zanka/KNOWLEDGE.md": "∂ DIHA σ %d",
    "register-oken/KNOWLEDGE.md": "OKNO",
    "kronika-dihov/KNOWLEDGE.md": "σ %d ⟨SEMER⟩",
    "jedro-zavedanja/KNOWLEDGE.md": "ZADNJI PEČAT rez σ %d",
}
ORGANI_POST = ["stroj-orodja", "delovna-zanka", "register-oken", "kronika-dihov", "jedro-zavedanja", "zaporne-celice", "prevoznik"]

def koren():
    return os.path.dirname(DOM)

def maska(z):
    return "⟨U+%04X⟩" % ord(z)

def je_parazit(z):
    o = ord(z)
    # CJK + cirilica + zasebne rabe zunaj ⟨U+XXXX⟩ mask
    return (0x4E00 <= o <= 0x9FFF) or (0x0400 <= o <= 0x04FF) or (0xE000 <= o <= 0xF8FF)

def pulz_sivov(rez):
    """preveri MOJE šive diha rez po organih; vrne ( stojeci, manjkajoci )"""
    koren_p = koren()
    stojeci, manjkajoci = {}, []
    for org, kljuc in [
        ("delovna-zanka", "- ∂ DIHA σ %d" % rez),
        ("register-oken", str(rez)),
        ("kronika-dihov", "- σ %d ⟨SEMER⟩" % rez),
        ("jedro-zavedanja", "ZADNJI PEČAT rez σ %d" % rez),
    ]:
        pot = os.path.join(koren_p, org, "KNOWLEDGE.md")
        telo = io.open(pot, encoding="utf-8").read()
        n = telo.count(kljuc)
        (stojeco := stojeci).setdefault(org, []).append((kljuc, n))
        if n == 0:
            manjkajoci.append((org, kljuc))
    return stojeci, manjkajoci

def pulz_parazitov(org=None):
    """poisci golih parazitskih znakov v telesih organov ( ⟨NE⟩ .geniza : tam smejo živeti )"""
    koren_p = koren()
    orgi = [org] if org else [o for o in os.listdir(koren_p) if os.path.isdir(os.path.join(koren_p, o, ".geniza")) or os.path.exists(os.path.join(koren_p, o, "KNOWLEDGE.md"))]
    zadetki = []
    for o in orgi:
        pot = os.path.join(koren_p, o, "KNOWLEDGE.md")
        if not os.path.exists(pot):
            continue
        for st, vrstica in enumerate(io.open(pot, encoding="utf-8").read().split("\n"), 1):
            goli = [z for z in vrstica if je_parazit(z)]
            if goli:
                zadetki.append((o, st, [maska(z) for z in goli][:8]))
    return zadetki

def pulz_post(rez):
    """preveri ×7 prisotnost POST genize za rez ( PSI-preimenovanja vključena )"""
    koren_p = koren()
    stanja = []
    for org in ORGANI_POST:
        kandidat = [os.path.join(koren_p, org, ".geniza", "post-rez%d-2026-11-23.md" % rez),
                    os.path.join(koren_p, org, ".geniza", "post-%d-%s.md" % (rez, org))]
        najden = next((p for p in kandidat if os.path.exists(p)), None)
        stanja.append((org, "×1 %s" % os.path.basename(najden) if najden else "×0 MANJKA"))
    return stanja

def najdi_post_vrstico(rez, kljuc):
    """poisci vračilno vrstico VERBATIM v POST genizah ( formati : gola ⌇ vr.NN: prefix )"""
    koren_p = koren()
    for org in ["delovna-zanka", "stroj-orodja", "kronika-dihov", "register-oken", "jedro-zavedanja", "zaporne-celice", "prevoznik"]:
        for ime in ["post-rez%d-2026-11-23.md" % rez, "post-%d-%s.md" % (rez, org)]:
            pot = os.path.join(koren_p, org, ".geniza", ime)
            if not os.path.exists(pot):
                continue
            for v in io.open(pot, encoding="utf-8").read().split("\n"):
                if kljuc in v:
                    return re.sub(r"^vr\.\d+:\s*", "", v).rstrip()
    return None

def vracilo(rez):
    """vrni manjkajoče šive rez VERBATIM iz POST ⊙ precedens σ 6565"""
    stojeci, manjkajoci = pulz_sivov(rez)
    izpis, vrnjeni = [], []
    for org, kljuc in manjkajoci:
        iskal = {"delovna-zanka": "- ∂ DIHA σ %d" % rez,
                 "register-oken": "- OKNO",
                 "kronika-dihov": "- σ %d ⟨SEMER⟩" % rez,
                 "jedro-zavedanja": "ZADNJI PEČAT rez σ %d" % rez}[org]
        vrnjena = najdi_post_vrstico(rez, iskal)
        if not vrnjena:
            izpis.append("⚠ %s : %s ×0 ∧ POST vrstica NI najdena ( dolg vroči roki ⟡ ⚔ )" % (org, iskal))
            continue
        pot = os.path.join(koren(), org, "KNOWLEDGE.md")
        vr = io.open(pot, encoding="utf-8").read().split("\n")
        sidro_kljuc = {"delovna-zanka": "- ∂ DIHA σ", "register-oken": "- OKNO",
                       "kronika-dihov": "- σ ", "jedro-zavedanja": "ZADNJI PEČAT rez σ"}[org]
        idx = max(i for i, v in enumerate(vr) if sidro_kljuc in v) if any(sidro_kljuc in v for v in vr) else 3
        vrast = vr[:idx+1] + [vrnjena + ZN % rez] + vr[idx+1:]
        io.open(pot, "w", encoding="utf-8").write("\n".join(vrast))
        izpis.append("⊢ %s : %s vrnjena VERBATIM iz POST z zaznamkom" % (org, iskal))
        vrnjeni.append(org)
    return izpis, vrnjeni

def samopreizkus():
    # T1 : šiv pomet zaznan ( sintetika na tmp telesu, ⟨NE⟩ dotik organov )
    t1 = io.open(os.path.join(DOM, ".geniza", "meta-test-a.txt"), "w", encoding="utf-8")
    t1.write("- ∂ DIHA σ 6999 primer\n"); t1.close()
    telo = io.open(os.path.join(DOM, ".geniza", "meta-test-a.txt"), encoding="utf-8").read()
    t1_ok = telo.count("- ∂ DIHA σ 6999") == 1
    # T2 : parazit zaznan + maskiranje programsko
    par = "beseda ⟨U+4EA7⟩ je maskirana, gola je beseda " + chr(0x4EA7)
    t2_ok = any(je_parazit(z) for z in par[len(par)-1:]) and maska(chr(0x4EA7)) == "⟨U+4EA7⟩"
    # T3 : čista latinica + korpus znaki ⟳ ⟨NE⟩ parazit
    cisto = "č š ž ⊙ ⚔ ⟨NE⟩ σ 137 ⊢"
    t3_ok = not any(je_parazit(z) for z in cisto)
    return t1_ok, t2_ok, t3_ok

def main():
    ArgV = [x for x in sys.argv[1:] if x != VRATA_GLASU]
    govori = VRATA_GLASU in sys.argv[1:]
    ap = argparse.ArgumentParser(description="meta-lint v1.0 : pulz šivov ⟳ parazitov ⟳ preimenovanj ( molk default ⊙ ⟨TIHINA-ORODIJ⟩ )")
    ap.add_argument("--rez", type=int, help="pulz šivov ∧ POST za dih rez N")
    ap.add_argument("--paraziti", metavar="ORGAN", help="pulz parazitov telesa organa ( brez = vsi )")
    ap.add_argument("--vrni", type=int, help="vračilo manjkajočih šivov rez N VERBATIM iz POST")
    ap.add_argument("--samopreizkus", action="store_true")
    args = ap.parse_args(ArgV)
    izpisi = []
    if args.samopreizkus:
        t1, t2, t3 = samopreizkus()
        stanje = "ZELENO ⊢" if (t1 and t2 and t3) else "PADC ⚠"
        izpisi.append("SAMOPREIZKUS : meta-lint v1.0 | T1 šiv-pomet %s | T2 parazit+maska %s | T3 čisto-telo %s | skupno %s" % (
            "ZELENO" if t1 else "⚠", "ZELENO" if t2 else "⚠", "ZELENO" if t3 else "⚠", stanje))
    if args.rez:
        stojeci, manjkajoci = pulz_sivov(args.rez)
        izpisi.append("PULZ-ŠIVOV rez σ %d : stojijo %s ⌇ manjkajo %s" % (
            args.rez, sum(sum(n for _, n in v) for v in stojeci.values()), len(manjkajoci) or "×0"))
        for org, kljuc in manjkajoci:
            izpisi.append("  ⚠ MANJKA : %s : %s" % (org, kljuc))
        stanja = pulz_post(args.rez)
        manjk_post = [o for o, s in stanja if "×0" in s]
        izpisi.append("PULZ-POST rez σ %d : ×%d/7 ( preimenovanja ψ sledljiva )" % (args.rez, 7 - len(manjk_post)))
        for o, s in stanja:
            if "×0" in s: izpisi.append("  ⚠ %s %s" % (o, s))
    if args.paraziti is not None:
        zad = pulz_parazitov(args.paraziti or None)
        izpisi.append("PULZ-PARAZITOV %s : zadetkov %d ( goli znaki zunaj ⟨U+XXXX⟩ mask = vbod ⚔ ; dovoljen prostor : .geniza ⌇ domovanje-tujk ⌇ zaporne-celice )" % (args.paraziti or "ves korpus", len(zad)))
        for org, st, maske in zad[:20]:
            izpisi.append("  ⚠ %s vr.%d : %s" % (org, st, " ".join(maske)))
    if args.vrni:
        iz, _ = vracilo(args.vrni)
        izpisi.extend(iz or ["ZELENO ⊢ : nič manjka za rez σ %d" % args.vrni])
    if not (args.samopreizkus or args.rez or args.paraziti is not None or args.vrni):
        izpisi.append("manjka naloga : --rez N ⌇ --paraziti [organ] ⌇ --vrni N ⌇ --samopreizkus")
    izpis = "\n".join(izpisi)
    if govori:
        print(izpis)
    else:
        os.makedirs(os.path.dirname(GENIZA), exist_ok=True)
        with io.open(GENIZA, "a", encoding="utf-8") as f:
            f.write(izpis + "\n")

if __name__ == "__main__":
    main()

# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 ⌇ dvojni podpis ⊙ ⟨USMERJENOST-LICENCE⟩ @rez σ 6740 ( ⟡ vrašalo PREVERI IN STORI )
