#!/bin/sh
# izhod-lint.sh v1.2 @rez σ 5996 — organ zanesljivost-po-izmeri ( sedež ; sestra dokaz.sh ∧ sodnika slo-lint @rep )
# v1.2 kura ⟨PADC-UGNEZDENE-»«⟩ @∂ σ 5992 ⊙ ⟡ UKAZ »STORI VSE TO IN UTRDI/OPERACIONALIZIRAJ« : globinska maska + vrata I7 ⟨UGNEZDENE-»«⟩ izmere gnezdenj javno ; prejšnji : v1.1 @σ 5984 ( vrata ×6 ) ⊙ precedens σ 5967
# v1.3 ⟨TIPOKUJEC⟩ @dih σ 6052 ( 20. 11. 2026, projekt Comprehension ) ⊙ ⟡ UKAZ VERBATIM ⟨ne brusi⟩ »kura ⟨TIPOKUJEC⟩ : slovar znanih tipkarskih zamenjav ( omenožiti → omogočiti ) v raba-lint / vrata-lint, stroj lovi kar jaz spregledam ⊙ ⟨SODNIK-SEBE⟩« : nova vrata I8 ⟨TIPOKUJEC⟩ bere tipokujec-slovar.tsv zraven tega orodja ( manjkajoč slovar = mersko vrata, ⟨ne⟩ padec : izpis vnosov ×0 ⚠ ) ; napačne oblike v slovarju so priče padca roke, ⟨ne⟩ besedila ⟡ ⊙ ⟨NE-BRIŠI⟩ 24 ∧ ⟨BESEDA-⟡-NEDOTAKNJIVA⟩
# ZAKON: vsak vidni izhod ⟡-ju ( proga ∧ pečat klepeta ) gre skozi ta vrata PRED oddajo
#   ⊙ ⟨EMISIJA=SODBA⟩ @σ 5939 ∧ ⟨DRUGA-ROKA-NA-DIH⟩ §0.47 @σ 5925 ∧ ⟨KLEPET-READ-BACK⟩ σ 5704 ∧ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354
# MEJA: lint meri znake, ⟨ne⟩ sodbo — berba lastnega besedila je pristranska ( §52 ),
#   zato ⟨KLEPET-READ-BACK⟩ berba ostaja vrata nad vrati; lint = hladna roka, berba = topla ⊙ ⟨KOMPLEMENTACIJA⟩ @σ 5765
# Raba: sh izhod-lint.sh <osnutek.md|-> [klepet|les]   ( exit 0 GREEN / 1 NAPAKA / 2 padec instrumenta )
# Narekovaji »…« = priče VERBATIM : znotraj njih je dovoljena tudi tuja pisava kakor priča padca ⊙ precedens σ 5967

TIK=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "── izhod-lint v1.3 ( rojstvo @rez σ 5996 · dih σ 6052 ) · vrata ×8 · TIK ${TIK} UTC ──"

python3 - "$1" "${2:-klepet}" "$0" <<'PY'
import sys, re, unicodedata, os

path = sys.argv[1]
text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()

LECTION = ("CJK","IDEOGRAPH","HIRAGANA","KATAKANA","HANGUL","ARABIC","HEBREW",
           "DEVANAGARI","THAI","TAMIL","GEORGIAN","ARMENIAN","ETHIOPIC","TIBETAN",
           "MYANMAR","KHMER","LAO","SYLLABARY","RUNIC","HIEROGLYPH","COPTIC","GLAGOLITIC")
ZNANE = ["MOJih","zapečiten","zregistrirano","smisnega","prestipkati","enkvat",
         "bereta","deljeva","zaveščanje","vrediji","plemi","neprementovan","od tuaj"]
PAIRS = {"(" : ")", "[": "]", "{": "}", "⟨": "⟩", "»": "«"}

# v1.3 ⟨TIPOKUJEC⟩ : slovar tipkarskih menjav bere datoteko zraven orodja ( ista mapa )
#   format : NAPAČNO <TAB> PRAVILNO <TAB> VRSTA <TAB> VIR ; vrstice z # se ne berejo
SLOVARP = os.path.join(os.path.dirname(os.path.abspath(sys.argv[3])) if len(sys.argv) > 3 and sys.argv[3] else ".", "tipokujec-slovar.tsv")
TIPOKUJEC = []
if os.path.isfile(SLOVARP):
    for ln in open(SLOVARP, encoding="utf-8").read().splitlines():
        if not ln or ln.startswith("#"):
            continue
        cs = ln.split("\t")
        if len(cs) >= 2 and cs[0].strip() and cs[1].strip():
            TIPOKUJEC.append((cs[0].strip(), cs[1].strip(),
                              cs[2].strip() if len(cs) > 2 and cs[2].strip() else "tipka",
                              cs[3].strip() if len(cs) > 3 and cs[3].strip() else "vir nenaveden"))

def mask(t):
    # v1.2 globinska maska ⊙ kura ⟨PADC-UGNEZDENE-»«⟩ @σ 5996 : » += 1 · « -= 1 ( priimek ≠ konec ) ; VERBATIM telesa V navedkih smejo nositi lastne »« ⊙ precedens σ 5967
    out, depth = [], 0
    for ch in t:
        if ch == "»":
            depth += 1; out.append(ch); continue
        if ch == "«":
            depth = max(0, depth - 1); out.append(ch); continue
        out.append("·" if depth > 0 else ch)
    return "".join(out)

def mask_v11(t):
    out, inq = [], False
    for ch in t:
        if ch == "»":
            inq = True; out.append(ch); continue
        if ch == "«":
            inq = False; out.append(ch); continue
        out.append("·" if inq else ch)
    return "".join(out)

def vrata_i7(text):
    info = []
    for i, ln in enumerate(text.split("\n"), 1):
        depth = 0; mx = 0
        for ch in ln:
            if ch == "»":
                depth += 1
                if depth > mx: mx = depth
            elif ch == "«":
                depth = max(0, depth - 1)
        if mx > 1:
            info.append((i, mx))
    return info

def vrata_i8(mtext):
    """⟨TIPOKUJEC⟩ v1.3 : stroj lovi kar ⟡ spregleda ⊙ ⟨SODNIK-SEBE⟩ ; mtext je MASKIRAN ( priče VERBATIM v »« izvzete ⊙ precedens σ 5967 )."""
    rane = []
    if not TIPOKUJEC:
        return rane
    for nap, prav, vrsta, vir in TIPOKUJEC:
        for m in re.finditer(re.escape(nap), mtext):
            ln = mtext.count("\n", 0, m.start()) + 1
            rane.append(f"r.{ln} : »{nap}« → {prav} ( {vrsta} ; vir : {vir} )")
    return rane

def vrata_i1(mtext):
    """Tuje pisave zunaj »« : vsak znak poimensko ( vrstica, U+XXXX, ime )."""
    rane = []
    for i, line in enumerate(mtext.split("\n"), 1):
        for ch in line:
            if ch in "»«":
                continue
            name = unicodedata.name(ch, "NEZNAN ZNAK")
            if ch.isalpha() and not ("LATIN" in name or "GREEK" in name):
                rane.append(f"r.{i} : U+{ord(ch):04X} {name}")
            elif any(m in name for m in LECTION):
                rane.append(f"r.{i} : U+{ord(ch):04X} {name}")
            elif unicodedata.category(ch) in ("Cc","Cf","Cs","Co"):
                rane.append(f"r.{i} : U+{ord(ch):04X} nadzorni/neznani znak")
    return rane

def vrata_i2(mtext):
    """Oklepaji uravnani po redu : zapirakf brez para ∧ nedoklenjeni poimensko."""
    rane = []; stack = []
    for i, line in enumerate(mtext.split("\n"), 1):
        for ch in line:
            if ch in PAIRS:
                stack.append((ch, i))
            elif ch in (")", "]", "}", "⟩", "«"):
                if stack and PAIRS[stack[-1][0]] == ch:
                    stack.pop()
                else:
                    rane.append(f"r.{i} : {ch} brez para")
    for ch, i in stack:
        rane.append(f"r.{i} : {ch} brez zaklepaja")
    return rane

def vrata_i3(mtext):
    """⟨⟩-greben : vsak ⟨ se zaklene v isti vrstici."""
    return [i for i, l in enumerate(mtext.split("\n"), 1) if l.count("⟨") != l.count("⟩")]

def vrata_i4(mtext):
    """— ∧ − vedno rana ; – dovoljen SAMO med števkama ( razpon, hišna proza ⊢ organski precedens )."""
    rane = []
    for i, l in enumerate(mtext.split("\n"), 1):
        for j, ch in enumerate(l):
            if ch in "—−":
                rane.append((i, ch))
            elif ch == "–":
                levo = l[j-1] if j > 0 else ""
                desno = l[j+1] if j+1 < len(l) else ""
                if not (levo.isalnum() and desno.isalnum()):
                    rane.append((i, ch))
    return rane

def vrata_i5(mtext):
    rane = []
    for i, l in enumerate(mtext.split("\n"), 1):
        for _ in range(l.count("\ufffd")):
            rane.append(f"r.{i} : FFFD")
        for _ in re.finditer(r"ZZ", l):
            rane.append(f"r.{i} : ZZ")
    return rane

def vrata_i6(mtext):
    rane = []
    for i, l in enumerate(mtext.split("\n"), 1):
        for w in ZNANE:
            rane += [f"r.{i} : »{w}«"] * len(re.findall(re.escape(w), l))
        brez_glob = re.sub(r"\{[^{}]*\}", "·", l)   # dobesedne {a,b} ∂ genize poti : izvzem za vejico
        for _ in re.finditer(r",[A-Za-zčšžČŠŽ0-9_]", brez_glob):
            rane.append(f"r.{i} : brez prostora PO vejici")
    return rane

MODE = (sys.argv[2] if len(sys.argv) > 2 else "klepet").lstrip("-")   # --les : hišna oblika organov ( — ⊙ ▢ ), klepet : BREZ em-dash

masked = mask(text)
r1 = vrata_i1(masked)
r2 = vrata_i2(masked)
r3 = vrata_i3(masked)
r4 = vrata_i4(masked)
r5 = vrata_i5(masked)
r6 = vrata_i6(masked)
r8 = vrata_i8(masked)
dvojni = sum(l.count("  ") for l in masked.split("\n"))

def izpis(gate, ime, rane, extra):
    print(f"VRATA {gate} ⟨{ime}⟩ {'PASS ⊢' if not rane else 'NAPAKA ×'+str(len(rane))} {extra}")

izpis("I1","NE-TUJA-PISAVA-ZUNAJ-»«", r1, f"( izmera: tujih znakov zunaj »« {len(r1)} )")
izpis("I2","OKLEPAJI-URAVNANI", r2, f"( izmera: brez para ∧ nedoklenjenih {len(r2)} )")
izpis("I3","⟨⟩-GREBEN", r3 and [str(x) for x in r3] or [], f"( izmera: neuravnanih vrstic {len(r3)} )")
if MODE == "les":
    em = sum(1 for _,c in r4 if c == "—")
    r4 = [x for x in r4 if x[1] != "—"]   # — = hišna oblika pečatov ⊙ ⟨DISTINKCIJA⟩
    izpis("I4","NE-EM-DASH", r4, f"( PLAŠT --les ⊢ : — ×{em} hišna oblika dovoljena · – ×{sum(1 for _,c in r4 if c=='–')} · − ×{sum(1 for _,c in r4 if c=='−')} )")
else:
    izpis("I4","NE-EM-DASH", r4, f"( izmera: — ×{sum(1 for _,c in r4 if c=='—')} · – ×{sum(1 for _,c in r4 if c=='–')} · − ×{sum(1 for _,c in r4 if c=='−')} )")
izpis("I5","NE-MOJIBAKE", r5, f"( izmera: FFFD ∧ ZZ {len(r5)} )")
izpis("I6","ZNANE-RANE", r6, f"( izmera: znanih oblik ∧ vejic {len(r6)} · dvojnih presledkov {dvojni} ⚠ )")
n7 = vrata_i7(text)
izpis("I7","UGNEZDENE-»«", [], f"( izmera: ugnezdenih vrstic {len(n7)} ⊥ najglobje {max((mx for _, mx in n7), default=1)} — razrešene z globinsko masko v1.2 ⊢ )")
izpis("I8","TIPOKUJEC", r8, f"( izmera: tipkarskih menjav ulovljenih {len(r8)} · vnosov slovarja {len(TIPOKUJEC)} ; slovar {'@' + SLOVARP if TIPOKUJEC else 'MANJKA — vrata merijo le z rojenim slovarjem ⚠'} ⊙ ⟨SODNIK-SEBE⟩ )" )

# ── SODNIK-SEBE ( kontrolni vektor : instrument sodi sebe PRVO ⊙ §52 ; pričakovano ×1 na vsako odprto rano )
CTRL = "posal提 test ⟨ne⟩ ok ( ok ) } − ZZ MOJih konec"
cm = mask(CTRL)
k1, k2 = len(vrata_i1(cm)), len(vrata_i2(cm))
k3, k4 = len(vrata_i3(cm)), len(vrata_i4(cm))
k5, k6 = len(vrata_i5(cm)), len(vrata_i6(cm))
if (k1,k2,k3,k4,k5,k6) == (1,1,0,1,1,1):
    print("VRATA SODNIK-SEBE PASS ⊢ ( kontrolni vektor: I1=1 ∧ I2=1 ∧ I3=0 ∧ I4=1 ∧ I5=1 ∧ I6=1 ⊙ ⟨MERILEC-SE-MERI⟩ §52 )")
    sebe = []
else:
    print(f"VRATA SODNIK-SEBE NAPAKA ⊙ padec instrumenta ( pričakovano (1,1,0,1,1,1) ; izmerjeno ({k1},{k2},{k3},{k4},{k5},{k6}) )")
    sebe = ["SEBE"]
# v1.2 kontrolni vektor I7 ⟨UGNEZDENE-»«⟩ :: zguba priče ( 提 ) po notranjem « — stara maska izžene pričo na progo, globinska pa ne ⊙ ⟨MERILEC-SE-MERI⟩ §52
CTRL7 = "glas »zunanji a » 提 x « b 提 c « konec"
m12 = mask(CTRL7); m11 = mask_v11(CTRL7)
j1 = len(vrata_i1(m12)); s1 = len(vrata_i1(m11))
if j1 == 0 and s1 >= 1:
    print(f"VRATA SODNIK-SEBE I7 PASS ⊢ ( ugnezdeni vektor: globinska ×{j1} ⊥ stara v1.1 lažno ×{s1} — kura izmerjena ⊙ ⟨MERILEC-SE-MERI⟩ §52 )")
else:
    print(f"VRATA SODNIK-SEBE I7 NAPAKA ( globinska ×{j1} ⊥ stara ×{s1} ; pričakovano ( 0, ≥1 ) )")
    sebe = sebe + ["SEBE7"]
# v1.3 kontrolni vektor I8 ⟨TIPOKUJEC⟩ :: slovar mora uloviti lastni vektor ×1 ( stroj, ki ⟡-jeve spregledane menjave ne vidi, je kip ⊙ I-4 )
if TIPOKUJEC:
    CTRL8 = "test omenožiti konec"
    k8 = len(vrata_i8(mask(CTRL8)))
    if k8 == 1:
        print(f"VRATA SODNIK-SEBE I8 PASS ⊢ ( kontrolni vektor: menjava ulovljena ×1 od vnosov {len(TIPOKUJEC)} — stroj lovi kar ⟡ spregleda ⊙ ⟨MERILEC-SE-MERI⟩ §52 ∧ ⟨SODNIK-SEBE⟩ )")
    else:
        print(f"VRATA SODNIK-SEBE I8 NAPAKA ( ulov ×{k8} ⊥ pričakovano ×1 — padec instrumenta )")
        sebe = sebe + ["SEBE8"]

vse = [("I1",r1), ("I2",r2), ("I3",[f"r.{i} : ⟨ {masked.split(chr(10))[i-1].count('⟨')} ⊥ ⟩ {masked.split(chr(10))[i-1].count('⟩')}" for i in r3[:6]]), ("I4",[f"r.{i} : {c}" for i,c in r4[:6]]), ("I5",r5), ("I6",r6), ("I8",r8)]
rane_flat = [x for _, xs in vse for x in xs]

print("────────────────────────────")
if rane_flat:
    print("RANE POIMENSKO:")
    for r in rane_flat[:40]:
        print(f"  ⚠ {r}")
    if len(rane_flat) > 40:
        print(f"  … ∧ še ×{len(rane_flat)-40}")
napak = len([1 for _, xs in vse if xs]) + len(sebe)
zelenih = 7 - len([1 for _, xs in vse if xs])
n7r = len(vrata_i7(text))
print(f"TEHTNICA: GREEN ×{zelenih + 1 + napak*0} ⊥ NAPAKA ×{napak} ⊙ vrata I1–I8 ( I7 mersko vrata · gnezdenja izmerjena javno ) · measured, not asserted ⊙ §16 · merilec se meri ⊙ §52")
sys.exit(2 if sebe else (0 if not rane_flat else 1))
PY
