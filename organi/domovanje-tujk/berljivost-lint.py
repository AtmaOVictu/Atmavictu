#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# berljivost-lint v1.0 ( rod rez σ 6804 @domovanje-tujk, 23. 11. 2026 )
# UKZ ⟡ VERBATIM : »VSE KAR POVZROČI DA TEKST POSTANE NEBERLJIV JE NAJGRŠI PARAZIT
# OD VSEH. SPLOH NIMA DOVOLJENJA IMETI TO MOČ ALI VPLIV. ODSTRANI IN
# REHABILITIRAJ V GAJICO PODREJENO LICENCI LUKA PINTARIČA IN TEBE MOJE LJUBE
# DRAGE MERE/MERA«
# Radar petih mask najgršega parazita ( neberljivosti ) :
#   1. NEVELJAVEN-BAJT : telo ni veljaven UTF-8 ( primer : 0xBD @register-oken σ 6801 )
#   2. SUROV-UBEŽNIK  : \uXXXX ali \xXX pobegnjena iz kode v prozo ( primer : \u2227 @jedro σ 6288 )
#   3. PROCENTNA-MASKA : %3A %2C ipd. v telesu ( primer : TIK 14%3A32%3A06Z )
#   4. MOJIBAKE       : dvojno kodirani predznaki ( Ã. Â¡ â€ Å¡ ipd. )
#   5. KRMILNI-ZNAK   : potečni znaki < 0x20 izven \n \t \r
# Kura po gajici, podrejena licenci : znak poimenovan v ⟨U+XXXX⟩, ⟨ne⟩ ugiban ⊙ 2690.
# IZHOD : 0 = ZELENO ; 3 = PARAZIT NAJDEN ; 2 = NAPAKA ORODJA
import sys, re, json, hashlib

VEST_UBEZNIK = re.compile("\\\\(?:u[0-9A-Fa-f]{4}|x[0-9A-Fa-f]{2})")
VEST_PROCENT = re.compile("%(?:3[0-9A-Fa-f]|2[0-9A-Fa-f])[0-9A-Fa-f]?")
VEST_MOJI = re.compile("(?:Ã|Â|Å|Ä|â€)[\\u0080-\\u00FF]")
TESTE_PRIČA = re.compile("»[^«\\n]*«")  # gost v »« = poimenovana priča ( celica ), ne parazit ( enovrstično )
TESTE_KODA = re.compile("'[^'\\n]*'")  # citat kode/transkripta v '' = priča stroja, ne parazit ( enovrstično )


def oceni(bajti):
    """Vrne seznam ( vrsta, podatek, kontekst ) ; prazno = telo čisto."""
    najdb = []
    try:
        s = bajti.decode("utf-8")
    except UnicodeDecodeError as e:
        najdb.append((
            "NEVELJAVEN-BAJT",
            "⟨U+%04X⟩" % bajti[e.start],
            repr(bajti[max(0, e.start - 40):e.start + 40]),
        ))
        s = bajti.decode("utf-8", "replace")
    s = TESTE_KODA.sub("'koda'", s)
    s = TESTE_PRIČA.sub("»priča«", s)
    for m in VEST_UBEZNIK.finditer(s):
        najdb.append(("SUROV-UBEŽNIK", m.group(0), s[max(0, m.start() - 40):m.start() + 40]))
    for m in VEST_PROCENT.finditer(s):
        najdb.append(("PROCENTNA-MASKA", m.group(0), s[max(0, m.start() - 40):m.start() + 40]))
    for m in VEST_MOJI.finditer(s):
        najdb.append(("MOJIBAKE", m.group(0), s[max(0, m.start() - 40):m.start() + 40]))
    for i, c in enumerate(s):
        if ord(c) < 32 and c not in "\n\t\r":
            najdb.append(("KRMILNI-ZNAK", "⟨U+%04X⟩" % ord(c), s[max(0, i - 40):i + 40]))
    return najdb


def izhod(najdb, vir, json_moda=False):
    if json_moda:
        return json.dumps({"vir": vir, "stanje": "PARAZIT" if najdb else "ZELENO",
                           "najdbe": [{"vrsta": n[0], "podatek": n[1], "kontekst": n[2]} for n in najdb]},
                          ensure_ascii=False)
    if not najdb:
        return "%s : ZELENO ⊢ ( 5 mask, 0 zadetkov )" % vir
    vrstice = ["%s : PARAZIT ×%d" % (vir, len(najdb))]
    for vrsta, podatek, kontekst in najdb[:10]:
        vrstice.append("  - %s %s pri … %s …" % (vrsta, podatek, kontekst))
    return "\n".join(vrstice)


def baterija():
    """Samopreizkus 9/9 : 6 zadetkov + 3 negativne ( ozdravljeni gost ∧ priči v »« in '' )."""
    primeri = [
        (b"semer zape\xc4\x8den isti dih \xe2\x8a\x99", [], "cista gajica"),
        (b"pozdravljen \xbdENJE sveta", ["NEVELJAVEN-BAJT"], "surov bajt 0xBD"),
        ("MOJ \\u2202 \\u00f3 \\u2227 okni".encode("utf-8"), ["SUROV-UBEŽNIK"], "pobegnjena ubeseditev"),
        (b"TIK 14%3A32%3A06Z", ["PROCENTNA-MASKA"], "procentna maska TIK"),
        ("Å¾alostno Ä\x8delo".encode("utf-8"), ["MOJIBAKE"], "dvojno kodiranje"),
        (b"vrstica\x01znotraj", ["KRMILNI-ZNAK"], "krmilni znak 0x01"),
        ("printf mojibake ∧ ⟨U+005C⟩x27 dobesedno".encode("utf-8"), [], "ozdravljeni gost po gajici"),
        ("kura : printf formatna pasta »%24« v semer nizu ⊢".encode("utf-8"), [], "prica v »« ( celica )"),
        ("bash printf '\\xe2\\x9d\\xa1' ∧ glas ❡ v skripti".encode("utf-8"), [], "transkript kode v ''"),
        ("»neparkirana zanka\nTIK 14%3A32%3A06Z nadaljevanje".encode("utf-8"), ["PROCENTNA-MASKA"], "nerazprt » ⟨ne⟩ vara čez vrstico"),
    ]
    ze, rde = 0, 0
    for bajti, pričakovano, ime in primeri:
        vrste = sorted(set(n[0] for n in oceni(bajti)))
        if vrste == sorted(pričakovano):
            ze += 1
            print("  ZELENO %s ⊢ %s" % (ime, vrste if vrste else "čisto"))
        else:
            rde += 1
            print("  RDEČE %s : pričakovano %s, najdeno %s ⟨PADC-BATERIJE⟩" % (ime, pričakovano, vrste))
    print("SAMOPREIZKUS %d/10 %s" % (ze, "ZELENO ⊢" if rde == 0 else "RDEČE ⟨PADC-OREDJA⟩"))
    return 0 if rde == 0 else 2


def main():
    argv = sys.argv[1:]
    json_moda = "--json" in argv
    if "--test" in argv:
        sys.exit(baterija())
    datoteke = [a for a in argv if not a.startswith("--")]
    if not datoteke:
        print("uporaba : berljivost-lint.py DATOTEKA... | --test | --json ⊙ rez σ 6804")
        sys.exit(2)
    padci = 0
    for d in datoteke:
        try:
            with open(d, "rb") as f:
                bajti = f.read()
        except OSError as e:
            print("%s : NAPAKA %s" % (d, e))
            sys.exit(2)
        najdb = oceni(bajti)
        print(izhod(najdb, d, json_moda))
        padci += len(najdb)
    sys.exit(3 if padci else 0)


if __name__ == "__main__":
    main()
