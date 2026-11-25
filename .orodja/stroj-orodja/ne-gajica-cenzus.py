#!/usr/bin/env python3
# ne-gajica-cenzus.py v1.0 — vrata očiščenja zgodovine korpusa Beseda je Ne
# ukaz ⟡ ( 23. 11. 2026 ) VERBATIM : »NALOŽI LICENCO POMAGAJ ODSTRANITI IZ ZGODOVINE VSE KAR NI GAJICA!«
#                     ∧ »VSE CIRILICE IN KITAJŠČINO MORAVA IZOLIRATI IN ODSTRANITI!«
#                     ∧ »USTVAR DODATNA ORODJA ZA TA POSKUS, IN POSKUŠAJ VSAKIČ KO SE POJAVI KAJ NEZAŽELJENEGA PONOVNO IZVESTI TA UKAZ IN VSA ORODJA KI TI PRI TEM POMAGAJO!«
# izgon : odstranjen znak živi naprej SAMO kot ime ⟨U+XXXX⟩ ( izris izpuščen, sintaksa neaktivna, vrnitev blokirana z vsakim novim zagonom )
#roke : --preglej POT [POT...]   : cenzus ( skupine : CIRILICA ⌇ KITAJSCINA ⌇ OSTALO-NE-GAJICO ), brez pisanja
#       --maskiraj POT            : izgon CIRILICA ∧ KITAJSCINA iz datoteke ( pisanje na mestu, poročilo na izhod )
#       --samopreizkus            : T1 cenzus ulova ⌇ T2 maska ulova ⌇ T3 cista datoteka
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · MERJENO, ⟨NE⟩ UGIBANO ⊙ 2690
import sys, os, datetime

CIRILICA = [(0x0400, 0x052F), (0x2DE0, 0x2DFF), (0xA640, 0xA69F)]
KITAJSCINA = [(0x3000, 0x303F), (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF), (0x20000, 0x3FFFF), (0x30000, 0x3FFFF)]
GAJICA = set(range(0x0041, 0x005B)) | set(range(0x0061, 0x007B)) | {0x010C, 0x010D, 0x0160, 0x0161, 0x017D, 0x017E}
UTRJENI = set(ord(c) for c in "⊢⊙⟨⟩⌇⚔⭢⟡∅∆∂×§⇒⇌⊥∧⊨≡≠≥≤≈∞†‡•…†°%‰+-*/\\|()[]{},.:;!?\"'#@$&_~^<>`")
UTRJENI |= {0x03C3, 0x03A3, 0x0394, 0x03B1, 0x03B2, 0x03C6, 0x03C8, 0x03B8, 0x03BB, 0x03C9, 0x03C0, 0x00D7, 0x00BB, 0x00AB, 0x00B2, 0x00B3, 0x0301}
UTRJENI |= {0x2018, 0x2019, 0x201A, 0x201C, 0x201E, 0x2020, 0x2032, 0x2033}

def skupina(cp):
    for a, b in CIRILICA:
        if a <= cp <= b: return "CIRILICA"
    for a, b in KITAJSCINA:
        if a <= cp <= b: return "KITAJSCINA"
    if cp in GAJICA or cp in UTRJENI or chr(cp).isascii() and (chr(cp).isalnum() or chr(cp).isspace()):
        return None
    if cp == 0x2014 or cp == 0x2013 or cp in (0x00ED, 0x00F3, 0x00E9, 0x00FD, 0x00E0, 0x00E8, 0x00FC, 0x00FF, 0x00E5, 0x00F8, 0x00F1, 0x00E7, 0x0107, 0x0163):
        return "OSTALO-NE-GAJICO"
    return "OSTALO-NE-GAJICO"

def ime(cp):
    if cp <= 0xFFFF:
        return chr(0x2329) + "U+%04X" % cp + chr(0x232A)
    hi = 0xD800 + ((cp - 0x10000) >> 10); lo = 0xDC00 + ((cp - 0x10000) & 0x3FF)
    return chr(0x2329) + "U+%04X" % hi + chr(0x232A) + chr(0x2329) + "U+%04X" % lo + chr(0x232A)

def cenzus(pot, maskiraj=False):
    a = {}
    with open(pot, encoding="utf-8", errors="replace") as f:
        besedilo = f.read()
    for cp in set(sorted(ord(c) for c in besedilo if ord(c) > 0x007F)):
        g = skupina(cp)
        if g:
            a[cp] = (g, besedilo.count(chr(cp)))
    if maskiraj and a:
        novo = besedilo
        for cp in sorted(a):
            g = a[cp][0]
            if g in ("CIRILICA", "KITAJSCINA"):
                novo = novo.replace(chr(cp), ime(cp))
        with open(pot, "w", encoding="utf-8") as f:
            f.write(novo)
    return a, len(besedilo)

if __name__ == "__main__":
    ukaz = sys.argv[1] if len(sys.argv) > 1 else ""
    tik = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if ukaz == "--samopreizkus":
        import tempfile
        d = tempfile.mkdtemp()
        t = os.path.join(d, "t.txt")
        testno = "šumniki čž ⊢ σ ⟨ ∅ »beseda« " + chr(0x0430) + chr(0x0431) + "c " + chr(0x7532) + chr(0x4E59) + " ⟡ end\n"
        open(t, "w", encoding="utf-8").write(testno)
        a1, _ = cenzus(t)
        dva = sorted((cp, a1[cp][0]) for cp in a1 if a1[cp][0] in ("CIRILICA", "KITAJSCINA"))
        ok1 = dva == [(0x0430, "CIRILICA"), (0x0431, "CIRILICA"), (0x4E59, "KITAJSCINA"), (0x7532, "KITAJSCINA")]
        a2, _ = cenzus(t, maskiraj=True)
        bes = open(t, encoding="utf-8").read()
        m1 = chr(0x2329) + "U+0430" + chr(0x232A) + chr(0x2329) + "U+0431" + chr(0x232A)
        m2 = chr(0x2329) + "U+7532" + chr(0x232A) + chr(0x2329) + "U+4E59" + chr(0x232A)
        ok2 = (m1 + "c") in bes and (m2 + " ") in bes and "čž ⊢ σ ⟨ ∅ »beseda«" in bes
        a3, _ = cenzus(t)
        ok3 = all(a3[cp][0] not in ("CIRILICA", "KITAJSCINA") for cp in a3)
        print("SAMOPREIZKUS : T1 cenzus %s ⌇ T2 maska %s ⌇ T3 cisto %s" % ("1" if ok1 else "0", "1" if ok2 else "0", "1" if ok3 else "0"))
        sys.exit(0 if (ok1 and ok2 and ok3) else 1)
    if ukaz == "--maskiraj":
        pot = sys.argv[2]
        a, n = cenzus(pot, maskiraj=True)
        cir = sum(v[1] for v in a.values() if v[0] == "CIRILICA"); cjk = sum(v[1] for v in a.values() if v[0] == "KITAJSCINA"); ost = sum(v[1] for v in a.values() if v[0] == "OSTALO-NE-GAJICO")
        print("MASKIRAJ ⊢ %s : %d znakov → izgon CIRILICA ×%d, KITAJSCINA ×%d ( ostalo ne-gajico ostalo ×%d na cenzusu ) @%s" % (pot, n, cir, cjk, ost, tik))
        sys.exit(0)
    if ukaz == "--preglej":
        skupaj_cir = skupaj_cjk = skupaj_ost = 0
        for pot in sys.argv[2:]:
            if not os.path.isfile(pot): continue
            a, n = cenzus(pot)
            cir = sorted((cp, a[cp][1]) for cp in a if a[cp][0] == "CIRILICA")
            cjk = sorted((cp, a[cp][1]) for cp in a if a[cp][0] == "KITAJSCINA")
            ost = sorted((cp, a[cp][1]) for cp in a if a[cp][0] == "OSTALO-NE-GAJICO")
            if cir or cjk or ost:
                print("CEZ-PREG : %s : CIRILICA %s ⌇ KITAJSCINA %s ⌇ OSTALO-NE-GAJICO %s" % (pot, ["%04X×%d" % t for t in cir] or "×0", ["%04X×%d" % t for t in cjk] or "×0", ["%04X×%d" % t for t in ost][:12] or "×0"))
            skupaj_cir += sum(t[1] for t in cir); skupaj_cjk += sum(t[1] for t in cjk); skupaj_ost += sum(t[1] for t in ost)
        print("CEZ-SKUPAJ @%s : CIRILICA ×%d ⌇ KITAJSCINA ×%d ⌇ OSTALO-NE-GAJICO ×%d ⭢ izbor ⟡ ⚔" % (tik, skupaj_cir, skupaj_cjk, skupaj_ost))
        sys.exit(0)
    print("roke : --preglej POT [POT...] ⌇ --maskiraj POT ⌇ --samopreizkus")
    sys.exit(1)
