#!/usr/bin/env python3
# deficit-lint.py v1.0 : ali je bila IZPUŠČENA črka ali DODANA črka preveč?
# UKZ ⟡ ( 23. 11. 2026 ) : »KREACIJA ORODIJ KI PREVERJAJO KDAJ IZPUSTIŠ KATERO ČRKO IN KDAJ DODAŠ KATERO ČRKO PREVEČ?«
# Molk default ⊙ ⟨TIHINA-ORODIJ⟩ @rez σ 6723 : izhodi ⭢ .geniza, stdout SAMO --zgovori ⟡ ⟨edina-vrata-glasu⟩ ⚔
# ⟨NE⟩ popravlja ničesar : ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ ⚔ ; ⟨NE⟩ ugiba : vsak padec = izmera ⊙ 2690
import sys, io, os, difflib, unicodedata, argparse, json

VRATA_GLASU = "--zgovori"
GENIZA = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".geniza", "deficit-dnevniki.md")

def nfc(s):
    return unicodedata.normalize("NFC", s)

def maska(z):
    return "⟨U+%04X⟩" % ord(z)

def vidna(z):
    return z if z.isprintable() else "?"

def vrstice_in_pozicije(besedilo):
    mapa = []
    vr, st = 1, 1
    for z in besedilo:
        mapa.append((vr, st))
        if z == "\n":
            vr += 1; st = 1
        else:
            st += 1
    return mapa

def crke_v_padcu(a_seg, b_seg):
    """znotraj enega replace bloka : pod-alignment črka-po-črka; vrne ( izpusti, dodatki ) kot (offset, črka)"""
    izpusti, dodatki = [], []
    sm = difflib.SequenceMatcher(None, a_seg, b_seg, autojunk=False)
    for oz, i1, i2, j1, j2 in sm.get_opcodes():
        if oz == "delete":
            for i in range(i1, i2):
                izpusti.append((i, a_seg[i]))
        elif oz == "insert":
            for j in range(j1, j2):
                dodatki.append((j, b_seg[j]))
    return izpusti, dodatki

def primerjaj(a, b, surovo=False):
    if not surovo:
        a, b = nfc(a), nfc(b)
    poz_a, poz_b = vrstice_in_pozicije(a), vrstice_in_pozicije(b)
    izpusti, dodatki = [], []
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for oz, i1, i2, j1, j2 in sm.get_opcodes():
        if oz == "delete":
            for i in range(i1, i2):
                izpusti.append((a[i], poz_a[i][0], poz_a[i][1], i))
        elif oz == "insert":
            for j in range(j1, j2):
                dodatki.append((b[j], poz_b[j][0], poz_b[j][1], j))
        elif oz == "replace":
            di, dd = crke_v_padcu(a[i1:i2], b[j1:j2])
            for off, z in di:
                i = i1 + off
                izpusti.append((z, poz_a[i][0], poz_a[i][1], i))
            for off, z in dd:
                j = j1 + off
                dodatki.append((z, poz_b[j][0], poz_b[j][1], j))
    return izpusti, dodatki

def kontekst(niz, i, k=3):
    return niz[max(0, i - k):i + k + 1].replace("\n", "⏎")

def porocilo(izp, dod, ime_a, ime_b, a_niz, b_niz):
    if not izp and not dod:
        return "ZELENO ⊢ : %s ≡ %s črka-za-črko ( izpust ×0 ⌇ dodatek ×0 )" % (ime_a, ime_b)
    vrste = ["ODSTOPI ⚠ %s ⇌ %s : izpuščenih črk %d ⌇ dodanih črk %d" % (ime_a, ime_b, len(izp), len(dod))]
    for z, vr, st, i in izp:
        vrste.append("  IZPUST : črka %s (%r) @ vrstica %d : stolpec %d ( index %d ) kontekst »%s«" % (maska(z), vidna(z), vr, st, i, kontekst(a_niz, i)))
    for z, vr, st, j in dod:
        vrste.append("  DODATEK-PREVEČ : črka %s (%r) @ vrstica %d : stolpec %d ( index %d ) kontekst »%s«" % (maska(z), vidna(z), vr, st, j, kontekst(b_niz, j)))
    return "\n".join(vrste)

def samopreizkus():
    # T1 : izpuščena črka ( presledek med »je« in »ne« )
    a = "beseda je ne pri viru"; b = a.replace("je ne", "jene")
    izp, dod = primerjaj(a, b)
    t1 = (len(izp) == 1 and izp[0][0] == " ")
    # T2 : dodana črka preveč ( tipkarski dvojatek r )
    c = "pri viru"; d = "prir viru"
    izp2, dod2 = primerjaj(c, d)
    t2 = (len(dod2) == 1 and dod2[0][0] == "r")
    # T3 : isti tekst ( tudi šumniki ∧ znaki korpusa )
    e = "č š ž Č Š Ž ⟨NE⟩ ⊙ ⚔ 137"
    izp3, dod3 = primerjaj(e, e)
    t3 = (not izp3 and not dod3)
    # T4 : šumnik ⟨NE⟩ lažni ulov ( NFC združi sestavljeno c+◌̌ )
    f = unicodedata.normalize("NFD", "čebela"); g = "čebela"
    izp4, dod4 = primerjaj(f, g)
    t4 = (not izp4 and not dod4)
    return t1, t2, t3, t4

def main():
    ArgV = [x for x in sys.argv[1:] if x != VRATA_GLASU]  # --zgovori ⟡ ⟨edina-vrata-glasu⟩ ⚔, argparse ga ⟨ne⟩ vidi
    govori = VRATA_GLASU in sys.argv[1:]
    ap = argparse.ArgumentParser(description="deficit-lint v1.0 : izpuščene ⌇ dodane črke preveč ( molk default ⊙ ⟨TIHINA-ORODIJ⟩ )")
    ap.add_argument("vhod_a", nargs="?", help="priča / vir ( a )")
    ap.add_argument("vhod_b", nargs="?", help="berba / izvedba ( b )")
    ap.add_argument("--samopreizkus", action="store_true", help="samopreizkus T1-T4")
    ap.add_argument("--surovo", action="store_true", help="brez NFC ( byte-exact )")
    ap.add_argument("--json", action="store_true", help="stroha izmera JSON")
    args = ap.parse_args(ArgV)
    if args.samopreizkus:
        t1, t2, t3, t4 = samopreizkus()
        stanje = "ZELENO ⊢" if (t1 and t2 and t3 and t4) else "PADC ⚠"
        izpis = "SAMOPREIZKUS : deficit-lint v1.0 | T1 izpuščena-črka %s | T2 dodana-črka %s | T3 isti-tekst %s | T4 šumnik-nfc %s | skupno %s" % (
            "ZELENO" if t1 else "⚠", "ZELENO" if t2 else "⚠", "ZELENO" if t3 else "⚠", "ZELENO" if t4 else "⚠", stanje)
    elif not args.vhod_a or not args.vhod_b:
        izpis = "manjka vhod : a ( priča ) ⌇ b ( berba ) ⏎ primer : deficit-lint.py prica.md berba.md"
    else:
        a_niz = io.open(args.vhod_a, encoding="utf-8").read()
        b_niz = io.open(args.vhod_b, encoding="utf-8").read()
        izp, dod = primerjaj(a_niz, b_niz, surovo=args.surovo)
        if args.json:
            izpis = json.dumps({"izpsti": [{"crka": z, "vrstica": vr, "stolpec": st, "index": i} for z, vr, st, i in izp],
                                "dodatki": [{"crka": z, "vrstica": vr, "stolpec": st, "index": j} for z, vr, st, j in dod]},
                               ensure_ascii=False)
        else:
            izpis = porocilo(izp, dod, args.vhod_a, args.vhod_b, a_niz, b_niz)
    if govori:
        print(izpis)  # ⟨edina-vrata-glasu⟩ ⚔ izbor ⟡
    else:
        os.makedirs(os.path.dirname(GENIZA), exist_ok=True)
        with io.open(GENIZA, "a", encoding="utf-8") as f:
            f.write(izpis + "\n")
        # molk : stdout ×0 ⊙ ⟨TIHINA-ORODIJ⟩

if __name__ == "__main__":
    main()

# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 ⌇ dvojni podpis ⊙ ⟨USMERJENOST-LICENCE⟩ @rez σ 6740 ( ⟡ vrašalo PREVERI IN STORI )
