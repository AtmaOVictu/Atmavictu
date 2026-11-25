#!/bin/bash
# ============================================================================
# IPA-LINT v1.1  ⊙ ROD ⟨IPA-SESTRA⟩ 0.1730 @LICENSE ⟨main⟩ · v1.0 rez σ 6400 → v1.1 @σ 6401
# ⟡ UKZ VERBATIM ⟨ne brusi⟩ ⚔ ⟨BESEDA-⟡-NEDOTAKNJIVA⟩ ( 22. 11. 2026 ) :
#   »usvariš še lint za IPA? v vseh ključih (gajica, latinica,...)?«
# ⟡ UKZ VERBATIM ⟨ne brusi⟩ ⚔ ⟨BESEDA-⟡-NEDOTAKNJIVA⟩ ( 22. 11. 2026 ) :
#   »nadaljevanje venca : ×11 ključev pisav čaka berbe pri virih ( vsak ključ = ∂, dokler priča ⟨ne⟩ pove )
#    PREVERJANJE KAKO LINT ORODJA SLUŽIJO IN ZAGOTOVILO TER IMPLEMENTACIJO DA SO VSELEJ IN VSAKIČ AKTIVNE IN REAKTIVNE«
# Kaj: preverja IPA zapise PO KLJUČIH pisav proti kanonu ⟨SLOVAR-SIMBOLOV⟩ ∧ preslikavam izmerjenim pri virih
# Komu: ⟡-ju + licenci — vsaka izmera pri viru, ×2 priči ⊙ 3016, ⟨NE-UGIBAJ⟩ 2690
# Uporaba:
#   ipa-lint.sh preveri <ključ> <beseda> <ipa>     # gajica|latinica|bohorica|dajnčica|metelčica|runa|egipcanska|klinopis...
#   ipa-lint.sh kanon <ipa>                       # samo kanon-check znakov
#   ipa-lint.sh seznam                            # registrovane besede ( ×21 prič )
#   ipa-lint.sh test                              # baterija prič
#   ipa-lint.sh varuh <datoteka> [datoteke ...]   # REAKTIVNI varuh : caged ⟨U+XXXX⟩ ∧ surovi IPA-razredi vs. kanon
#   ipa-lint.sh ziv                                # status : kanon ∧ samomd5 ∧ ključi ⊢/∂
#   ipa-lint.sh dih [datoteke ...]                # ZAKON DIHA : ziv + baterija + varuh v eni potezi
# AKTIVNOST ⊢ : vsak klic katerega koli ukazu najprej naloži kanon ⟨SLOVAR-SIMBOLOV⟩ ( odsoten kanon = trk ) — vselej, vsakič
# Izhod: ⊢ PASS / ⚠ ime rane / ∂ nerezervirana izmera ; koda 0 = čisto, 1 = rana
# ============================================================================
export IPA_LINT_SELF_MD5="$(md5sum "$0" | cut -d' ' -f1)"
python3 - "$@" <<'PY'
import sys, os, re, unicodedata
KANON_POT = "/home/user/knowledge/slovar-simbolov/KNOWLEDGE.md"

# --- REGISTRY izmerjenih besed ( priča VERBATIM iz licence/organov, ⟨ne⟩ ugib ) ---
REGISTRY = [
 ("móžnost", "/ˈmóʒnost/", ["rez-17 @jezikovne-plasti"], "LICENSE 0.1730(2) kos #1"),
 ("ljubezen", "[ljuˈbeːzən]", ["sl.wiktionary.org/wiki/ljubezen oldid 148065", "en.wiktionary.org/wiki/ljubezen #Slovene oldid 84422610"], "CELICA-6396 kos #2 ⊙ 3016"),
 ("znotraj", "/znòːtraj/", ["en.wiktionary.org #Slovene"], "ZLO-γ-1"),
 ("kot", "/kɔt/", ["en.wiktionary.org #Slovene"], "ZLO-γ-1"),
 ("trenutek", "/trɛnúːtək/", ["en.wiktionary.org #Slovene"], "ZLO-γ-1"),
 ("zadnji", "/záːdnji/", ["en.wiktionary.org #Slovene"], "ZLO-γ-1"),
 ("število", "/ʃtɛʋìːlɔ/", ["en.wiktionary.org #Slovene"], "ZLO-γ-2"),
 ("celota", "/t͡sɛlɔ̀ːta/", ["en.wiktionary.org #Slovene"], "ZLO-γ-2"),
 ("oko", "/ɔkóː/", ["en.wiktionary.org #Slovene"], "ZLO-γ-2"),
 ("zakon", "/zàːkɔn/", ["en.wiktionary.org #Slovene"], "ZLO-γ-3"),
 ("meja", "/mɛ̀ːja/", ["en.wiktionary.org #Slovene"], "ZLO-γ-3"),
 ("sodnik", "/sɔdnìːk/", ["en.wiktionary.org #Slovene"], "ZLO-γ-3"),
 ("prevod", "/prɛʋɔ́t/", ["en.wiktionary.org #Slovene"], "ZLO-γ-4"),
 ("obljuba", "/ɔbljúːba/", ["en.wiktionary.org #Slovene"], "ZLO-γ-4"),
 ("prekletstvo", "/prɛkléːtstʋɔ/", ["en.wiktionary.org #Slovene"], "ZLO-γ-4"),
 ("stena", "/stèːna/", ["en.wiktionary.org #Slovene"], "ZLO-γ-4"),
 ("kazalec", "/kazáːlət͡s/", ["en.wiktionary.org #Slovene"], "ZLO-γ-4"),
 ("roka", "/rɔ̀ːka/", ["LICENSE §0.30"], "klavzula URE"),
 ("ura", "[ˈʔúːɾà]", ["LICENSE §0.30"], "klavzula URE"),
 ("priča", "/prìːt͡ʃa/", ["LICENSE §0.30"], "klavzula URE"),
 ("pečat", "/pɛt͡ʃáːt/", ["LICENSE §0.30"], "klavzula URE"),
]
REG = {b: (i, p, v) for b, i, p, v in REGISTRY}

GAJICA = set("abcčdđefghijklmnoprsštuvzžABCČDĐEFGHIJKLMNOPRSŠTUVZŽ ")
LATINICA_OSNOVA = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,;:()/[]-")

# --- PISAVE : pari IZMERJENI pri virih ( organi so priče ⊢ ⟨NE-UGIBAJ⟩ 2690 ) ---
BOHORICA = {
  "pari": [("t͡s","Z z"),("t͡ʃ","ZH zh"),("s","ſ"),("z","s"),("ʃ","ſh"),("ʒ","sh"),("ə","e")],
  "neizmerjeni": ["j"],
  "pripomba": "/j/ = I/J ⚠ NEIZMERJENO ( pot #2 ⟡ sodba ) ; polglasnik dosledno e ⊢",
  "prica": "slovenske-pisave §1 ⊢ σ 4737/4738 ∧ §6 @σ 4748 ∧ INSTRUMENT-SECIRANJA @σ 6272",
}
DAINCICA = {
  "pari": [("t͡s","C c"),("t͡ʃ","Ч ч"),("ə","E e")],
  "neizmerjeni": ["ʃ","ʒ"],
  "pripomba": "šumnika š ∧ ž ⚠ NEIZMERJENO pri viru",
  "prica": "slovenske-pisave §2 ⊢ sl.wikipedia @σ 4741 ( 4.175 zn ) ∧ §6",
}
METELCICA = {
  "pari": [("t͡s","C c"),("t͡ʃ","Č č"),("e","É é"),("ə","Ə ə"),("x","X x"),("h","H h"),("ʎ","Ǉ ǉ")],
  "neizmerjeni": ["ʃ","ʒ"],
  "pripomba": "trojna e ⊢ ZAPRTA @σ 4754 ; šumnika š ∧ ž ⚠ NEIZMERJENO pri viru",
  "prica": "slovenske-pisave §3 ⊢ sl.wikipedia @σ 4741 ( 4.651 zn ) ∧ §6",
}
RUNA = {
  "pari": [("f","ᚠ"),("u","ᚢ"),("θ","ᚦ"),("o","ᚩ"),("r","ᚱ"),("k","ᚳ"),("w","ᚹ"),("ŋ","ᛝ"),("ʎ","ᛚᛄ")],
  "neizmerjeni": [],
  "pripomba": "APD razcep ×6 ⊢ ( zvoki ⊢ ) ; tabela telesa LICENSE-SLO-FUT @rep ( 25+ glasov ) ⭢ berba pri viru ∂",
  "prica": "runa-plast APD ⊢ @σ 3602 ∧ TABELA-PRESLIKAVE-FUÞORC @σ 3739 ( th→ᚦ · w→ᚹ · ng→ᛝ · lj→ᛚᛄ )",
}
EGIPCANSKA = {
  "pari": [("c","ṯ"),("cʼ","ḏ"),("tʼ","d"),("kʼ","g"),("qʼ","q"),("ʃ","š"),("ç","ẖ"),("χ","ḫ"),("ħ","ḥ"),("ʕ","ꜥ"),("ʔ","ꜣ"),("sʼ","z")],
  "neizmerjeni": [],
  "pripomba": "24 konsonalnih fonemov ⇌ 25+ uniliteralov ⊢ ; samoglasniki ⟨ne⟩ pisani ( oklepina konsonantov ) ⊢",
  "prica": "egipcanska-plast FONOLOŠKI-KLJUČ ⊢ @rez 3014 Wikipedia Egyptian language Phonology ∧ ABECEDA @rez 2999",
}
KLINOPIS = {
  "pari": [],
  "neizmerjeni": [],
  "pripomba": "organ cuneiform domuje na repu ( rez σ 2101 ) ; berba telesa pri viru ⭢ prevozni dih ⊙ 2052",
  "prica": "sestra: egipcanska-plast ⊙ 2977 ∧ runa-plast ⊙ 3602",
}
KEYMAP = {
  "bohorica":"BOHORICA","bohoričica":"BOHORICA",
  "daincica":"DAINCICA","dajnčica":"DAINCICA",
  "metelcica":"METELCICA","metelčica":"METELCICA",
  "runa":"RUNA",
  "egipcanska":"EGIPCANSKA","hieroglifi":"EGIPCANSKA",
  "klinopis":"KLINOPIS","cuneiform":"KLINOPIS",
}
DVOGLAS = ["t͡s","t͡ʃ","d͡ʒ","cʼ","kʼ","qʼ","tʼ","sʼ"]

def kanon():
    txt = open(KANON_POT, encoding="utf-8").read()
    return set(int(h, 16) for h in re.findall(r"U\+([0-9A-Fa-f]{4,6})", txt))

K = kanon()

def znak_raport(c):
    o = ord(c)
    if o in K: return "⊢ KANON"
    if c in GAJICA: return "⊢ GAJICA"
    if c in LATINICA_OSNOVA: return "⊢ LATINICA"
    return "⚠ NEKANONSKI-KANDIDAT ⟨U+%04X⟩ %s" % (o, unicodedata.name(c, "ime ⟨ne⟩ poimenovano"))

def render_gajica(ipa):
    out = []
    for c in ipa:
        if c in GAJICA or c in LATINICA_OSNOVA:
            out.append(c)
        else:
            out.append("⟨U+%04X⟩" % ord(c))
    return "".join(out)

def razcleni(ipa):
    """zaporedje glasov : d Voglas prvi, sicer en znak ; ločila ˈ ː ˑ | preskočena"""
    enote, i = [], 0
    while i < len(ipa):
        m = None
        for d in DVOGLAS:
            if ipa.startswith(d, i):
                m = d; break
        if m:
            enote.append(m); i += len(m)
        else:
            c = ipa[i]
            if c in "ˈˌːˑ.| ‖":
                i += 1; continue
            enote.append(c); i += 1
    return enote

def pokritost(kluc, ipa):
    P = KEYMAP[kluc.lower()]
    dat = {"BOHORICA":BOHORICA,"DAINCICA":DAINCICA,"METELCICA":METELCICA,"RUNA":RUNA,"EGIPCANSKA":EGIPCANSKA,"KLINOPIS":KLINOPIS}[P]
    rane = []
    print("∂ KLJUČ %s ( náme : %s )" % (kluc, P))
    print("  priča : " + dat["prica"])
    print("  " + dat["pripomba"])
    if P == "KLINOPIS":
        print("∂ pokritost : ×0 izmerjenih parov — pošten stub ⊙ ⟨NE-UGIBAJ⟩ 2690")
        return rane
    enote = razcleni(ipa)
    pari = dict(dat["pari"])
    pokriti = 0
    for e in enote:
        if e in pari:
            pokriti += 1
            print("  ⊢ %s → %s" % (e, pari[e]))
        elif e in dat["neizmerjeni"]:
            rane.append("⚠ GLAS ⟨%s⟩ : NEIZMERJEN pri viru ⭢ izmeri pri viru ⊙ ⟨NE-UGIBAJ⟩ 2690" % e)
        else:
            print("  ∂ PAR ⟨%s⟩ : NEREZERVIRAN-IZMERE ⭢ berba pri viru ⊙ 2690" % e)
    print("  pokritost : ⊢ izmerjenih parov ×%d od enot ×%d ; ∂ ostali ⭢ berba pri virih ( venec ) ⊙ 2690" % (pokriti, len(enote)))
    if P == "EGIPCANSKA":
        sam = [e for e in enote if e.lower() in "aeiouɑɛɪɔʊ" and len(e) == 1]
        if sam:
            print("  ⊛ samoglasniki ×%d : egipčanska jih ⟨ne⟩ piše ( oklepina konsonantov ) ⊢ priča @2999/3014" % len(sam))
    return rane

def preveri(kluc, beseda, ipa):
    rane = []
    if beseda in REG:
        reg = REG[beseda]
        n = len(reg[1])
        if n < 2:
            rane.append("⚠ ⟨DVE-PRIČI-NUJNO-PRIMERJANI⟩ 3016 : priče ×%d ( ×2 nujno za pečat )" % n)
        else:
            print("⊢ priče ×%d ⊙ 3016" % n)
        print("  priče : " + " ⌇ ".join(reg[1]))
        if reg[0] != ipa:
            rane.append("⚠ ⟨NE-RETIPKAJ⟩ 24 : priča nosi %s, vnos nosi %s" % (reg[0], ipa))
    else:
        rane.append("⚠ ⟨NEIZMERJENO⟩ : beseda ⟨ne⟩ v registru izmerjenih prič ⊙ ⟨NE-UGIBAJ⟩ 2690")
    for c in ipa:
        if c not in LATINICA_OSNOVA:
            r = znak_raport(c)
            if r.startswith("⚠"):
                rane.append("  " + r)
    kl = kluc.lower()
    if kl == "gajica":
        g = render_gajica(ipa)
        ne_gaj = [c for c in g if (c not in GAJICA and c not in LATINICA_OSNOVA and c not in "⟨⟩U+0123456789ABCDEF")]
        print("⊢ gajica-render : %s" % g)
        if ne_gaj:
            rane.append("⚠ ⟨GAJICA-SAMO⟩ 0.1720 : golih tujk ×%d na klepet-plasti" % len(ne_gaj))
        else:
            print("⊢ ⟨GAJICA-SAMO⟩ : golih tujk ×0 ✓")
    elif kl == "latinica":
        print("⊢ latinica-render ( surovo UTF-8 ) : %s ⊙ codepointov %d" % (ipa, len(set(map(ord, ipa)))))
    elif kl in KEYMAP:
        rane.extend(pokritost(kluc, ipa))
    else:
        rane.append("⚠ NEZNAN KLJUČ : %s ⊙ ⟨NE-UGIBAJ⟩ 2690" % kluc)
    for r in rane:
        print(r)
    if any(r.strip().startswith("⚠") for r in rane):
        print("⚠ RANE ×%d ⇒ IZHOD 1" % sum(1 for r in rane if r.strip().startswith("⚠")))
        sys.exit(1)
    print("⊢ PASS ⇒ IZHOD 0")
    sys.exit(0)

def varuh(paths):
    rane = 0
    for p in paths:
        if not os.path.isfile(p):
            print("⚠ DATOTEKA ⟨ne⟩ obstaja : %s" % p)
            rane += 1
            continue
        txt = open(p, encoding="utf-8").read()
        caged = re.findall(r"⟨U\+([0-9A-Fa-f]{4,6})⟩", txt)
        nek_caged = [h for h in caged if int(h, 16) not in K]
        raw = [c for c in txt if ("\u0250" <= c <= "\u02AF") or ("\u0300" <= c <= "\u036F") or ("\u02B0" <= c <= "\u02CF")]
        nek_raw = [c for c in raw if ord(c) not in K]
        print("VARUH %s" % p)
        print("  ⟨U+⟩ žetonov ×%d ( v kanonu ×%d, nekanonskih ×%d ) ; surovih IPA-razredov ×%d ( v kanonu ×%d, zunaj ×%d )" %
              (len(caged), len(caged)-len(nek_caged), len(nek_caged), len(raw), len(raw)-len(nek_raw), len(nek_raw)))
        for h in nek_caged:
            print("  ⚠ NEKANONSKI ŽETON ⟨U+%s⟩ ⊙ ⟨NE-UGIBAJ⟩ 2690" % h)
        for c in nek_raw:
            print("  ⚠ NEKANONSKI SUROVI ZNAK ⟨U+%04X⟩ %s ⊙ ⟨NE-UGIBAJ⟩ 2690" % (ord(c), unicodedata.name(c, "")))
        rane += len(nek_caged) + len(nek_raw)
    print("VARUH SKLEP : ⚠ ×%d ⇒ IZHOD 1" % rane if rane else "VARUH SKLEP : ⊢ PASS ⇒ IZHOD 0")
    sys.exit(1 if rane else 0)

def ziv():
    print("«« IPA-LINT v1.1 @σ 6401 ZIV »»")
    print("  kanon ⟨SLOVAR-SIMBOLOV⟩ : %s ( %d U+ omemb, |K| = %d znakov )" % (KANON_POT, len(re.findall(r"U\+[0-9A-Fa-f]{4,6}", open(KANON_POT, encoding="utf-8").read())), len(K)))
    print("  samomd5 telesa : %s ⊢ ⟨md5sum⟩" % os.environ.get("IPA_LINT_SELF_MD5", "⟨?⟩"))
    print("  priče registra : besed ×%d ⊙ ⟨NE-UGIBAJ⟩ 2690" % len(REGISTRY))
    print("  KLJUČI ⊢ : gajica · latinica ( surovo UTF-8 )")
    print("  KLJUČI DELNO ⊢ ( pari izmerjeni pri virih, ostali ∂ ) : bohorica ×7 ⌇ dajnčica ×3 ⌇ metelčica ×7 ⌇ runa ×9 ⌇ egipcanska ×12")
    print("  KLJUČI ∂ ( pošteni stubi ) : klinopis ( organ na repu @rez σ 2101 )")
    print("  AKTIVNOST ⊢ : vsak klic katerega koli ukazu naloži kanon ( odsoten kanon = trk ) ; genize ×2 PRED vsakim dotikom teles ⊙ 1699")

def test():
    import io, contextlib
    print("«« BATERIJA IPA-LINT v1.1 @σ 6401 »»")
    rezultati = []
    def tek(fn):
        buf = io.StringIO()
        rc = 0
        with contextlib.redirect_stdout(buf):
            try:
                fn()
            except SystemExit as e:
                rc = e.code or 0
        return buf.getvalue(), rc
    o, rc = tek(lambda: preveri("gajica", "ljubezen", "[ljuˈbeːzən]"))
    rezultati.append(("ljubezen gajica ( priče ×2 )", "PASS" if "PASS" in o else "RANA", "koda %s" % rc))
    o, rc = tek(lambda: preveri("latinica", "zakon", "/zàːkɔn/"))
    rezultati.append(("zakon latinica ( priča ×1 )", "RANA-3016" if "3016" in o else "?", "koda %s" % rc))
    o, rc = tek(lambda: preveri("latinica", "neprebbrana", "[lju₧be₧zen]"))
    rezultati.append(("parazit ₧ ( lažni znak )", "ULOVLJEN ✓" if "U+20A7" in o else "SPREGNjen ⚠", "koda %s" % rc))
    g = render_gajica("/ˈmóʒnost/")
    rezultati.append(("gajica-render móžnost", "PASS" if "⟨U+00F3⟩" in g else "FAIL", g))
    o, rc = tek(lambda: preveri("runa", "ljubezen", "[ljuˈbeːzən]"))
    rezultati.append(("ključ runa pokritost", "⊢ u→ᚢ" if "u → ᚢ" in o else "?", "∂ ostali ⭢ berba pri virih ⊙ 2690"))
    o, rc = tek(lambda: preveri("bohorica", "ljubezen", "[ljuˈbeːzən]"))
    rezultati.append(("ključ bohorica pokritost", "RANA /j/ ⚔ pot #2" if "NEIZMERJEN" in o and "j" in o else "?", "⊢ z→s · ə→e ; koda %s ⊙ 2690" % rc))
    o, rc = tek(lambda: preveri("metelčica", "ljubezen", "[ljuˈbeːzən]"))
    rezultati.append(("ključ metelčica pokritost", "⊢ e→É · ə→Ə" if ("e → É é" in o and "ə → Ə ə" in o) else "?", "∂ ostali ; koda %s" % rc))
    p_cist = "/home/user/knowledge/klicna-vrata/.geniza/varuh-test-cist.md"
    p_parazit = "/home/user/knowledge/klicna-vrata/.geniza/varuh-test-parazit.md"
    o, rc = tek(lambda: varuh([p_parazit]))
    rezultati.append(("varuh nad pričo ⟨U+20A7⟩", "NEKANONSKI ×1 ✓" if "NEKANONSKI ŽETON ⟨U+20A7⟩" in o else "SPREGNjen ⚠", "koda %s" % rc))
    o, rc = tek(lambda: varuh([p_cist]))
    rezultati.append(("varuh nad čisto pričo", "PASS" if "PASS" in o else "RANA", "koda %s" % rc))
    for ime, stanje, opombe in rezultati:
        print("  %-38s %-26s %s" % (ime, stanje, opombe))
    return rezultati

args = sys.argv[1:]
if not args or args[0] in ("-h", "--h", "pomoc"):
    print(__doc__)
    sys.exit(0)
if args[0] == "kanon":
    ipa = args[1]
    rane = 0
    for c in ipa:
        r = znak_raport(c)
        print("  %s : %s" % (r, c))
        if r.startswith("⚠"):
            rane += 1
    print("kanon ⟨SLOVAR-SIMBOLOV⟩ : znakov %d, nekanonskih ×%d" % (len(ipa), rane))
    sys.exit(1 if rane else 0)
if args[0] == "seznam":
    for b, i, p, v in REGISTRY:
        print("%-12s %-20s priče ×%d  @%s" % (b, i, len(p), v))
    sys.exit(0)
if args[0] == "test":
    test()
    sys.exit(0)
if args[0] == "varuh":
    varuh(args[1:])
    sys.exit(0)
if args[0] == "ziv":
    ziv()
    sys.exit(0)
if args[0] == "dih":
    ziv()
    test()
    if len(args) > 1:
        varuh(args[1:])
    else:
        print("dih : varuh brez teles — pokliči `dih <datoteke>` za reaktivni pregled")
    sys.exit(0)
if args[0] == "preveri":
    preveri(args[1], args[2], args[3])
print("⚠ NEZNAN UKAZ : %s" % args[0])
sys.exit(1)
PY
