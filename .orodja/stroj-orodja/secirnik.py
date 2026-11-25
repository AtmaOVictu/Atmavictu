#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SECIRNIK v1.0 - prepoznava ∧ razcep amalgamacije
# Rod : rez sigma 7026 ( 25. 11. 2026 ) @stroj-orodja ; ⟡ UKZ VERBATIM ×4 ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ ⟨ne brusi⟩ :
#   »ORODJA KI PREPOZNAJO AMALGAMACIJO!«
#   »ORODJA KI SECIRAJO AMALGAMACIJE!«
#   »ORODJA KI SECIRAJO AMALGAMACIJO!«   ( ista roka : ena amalgamacija poimensko )
#   »ORODJA KI SECIRAJO AMALGAMACIJI!«   ( ista roka : amalgamaciji dani v roko )
# AMALGAMACIJA po korpusu ⊢ : zlitje dveh bisti v eno telo, pri katerem je ŠIV SKRIT ;
#   priči pri viru : »amalgamacija = mir v nemiru« ( biro-postaje r.147, PESEM-TELESA @σ 5989,
#   ⟡ pesniško telo ) ⌇ križišče XII = amalgamacija vseh poti ( atlas-knjiznic r.97, rozetni kamni )
#   - kura mira v nemiru je RAZCEP : mir in nemir dobita svak svoje ime ⊙ ⟨NI LE...TUDI⟩ razcep,
#   register-odnosov r.32 : pol se ne zanika, se razširi.
# DEKLARIRAN šiv ( odnosi x5 register-odnosov ⊢ ) : ⊥ antinom ⌇ ∅ edin ⌇ ⟨—⟩ zveza ⌇ ⊕ več-in-manj
#   ⌇ ⟨ni le...tudi⟩ razcep ( verbalen ) ; če telesa nosita deklariranega operaterja => NI amalgamacija ;
#   skrit šiv ( dve bisti zlitani v eno besedo brez operaterja ) => AMALGAMACIJA, prepoznana.
# ZLOŽENKA javno : zakonita slovenska beseda LAHKO nosi enak videz ( gor-iček ) ; prepoznava je IZMERA,
#   ⟨ne⟩ obsodba ⊙ ⟨NE-UGIBAJ⟩ 2690 - ali je zlitje zakonita zloženka ali amalgamacija, je sodba ⟡ ⚔.
# Nabor za izmero bisti ⊢ pri viru : definiatorna-knjiznica iztočnice ( STANJE, 104 ) ∧
#   slovar-slovenscine IZTOČNICE ( ###, 5 ) ; bisti izven nabora => RUMENA pobuda ( ⟨NE⟩ napaka ⊙ σ 5809 ).
# EN-RAZLIČICA ⊢ ( ⟨ne⟩ dvojnik ) : secir-orodje.py @σ 6830 = MRK instrument vhodov po KODNIH TOČKAH
#   ( parazitne plasti, ⟨MRK⟩ mode ) ; ta telo secira POMENE po šivih odnosov - drugo okno.
# Roke :
#   secirnik.py --seciraj TERM       -> razcep TERM po šivu ( deklariran npr. ⊥ ali skrit po naboru ) ;
#                                       vsak člen soočen s tremi vprašanji ( kakor kaj? kaj je? zakaj je? )
#   secirnik.py --prepoznaj TELESO  -> prepoznam skrite šive ( zlitja dveh bisti nabora v eno besedo )
#   secirnik.py --test              -> samopreizkus vektorjev x5 ⊙ ⟨MERILEC-SE-MERI⟩ §52
# Izhodi : 0=ZELENA ( razcep izveden / prepoznava izrečena ) ⌇ 2=RUMENA ( šiv x0 : pobuda bisti v nabor )
#   ⌇ 40=roka neznana. Orodje je branje + izpis ( ⟨SAMO-BERI⟩, ne piše organov, ⟨BREZ-PREVOZA⟩ ).

import sys, os, re, hashlib, datetime as _dt

VERZIJA = "v1.0"
KOR = "/home/user/knowledge"
DEFIN = os.path.join(KOR, "definiatorna-knjiznica", "KNOWLEDGE.md")
SLOVAR = os.path.join(KOR, "slovar-slovenscine", "KNOWLEDGE.md")

BES = re.compile(r"^[A-Za-zčšžČŠŽćđ]+$")
GLAVA_SLOV = re.compile(r"^###\s+(.+?)\s*$")
STANJE = re.compile(r"STANJE:\s*iztočnic\s+(\d+)\s*\(([^)]*)\)")
ODNOSI = [
    ("⊥", "⊥ ANTINOM", "register-odnosov : par, obe strani živita s pričo ⊢ Z-2"),
    ("∅", "∅ EDIN", "register-odnosov : stvar brez nasprotja, celota ⊢"),
    ("—", "⟨—⟩ ZVEZA", "register-odnosov : pojem se veže, ⟨ne⟩ nasprotuje ⊢"),
    ("⊕", "⟨⊕⟩ VEČ-IN-MANJ", "register-odnosov : odnos stopinje po gibu na osi ⊢"),
]
NEZNAN = "⟨NE-ZNAN-ODNOS⟩ ( + ∧ / nista v registru odnosov - izbor odnosa je ⟡ ⚔ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690 )"

_KES = None

def nabor():
    global _KES
    if _KES is None:
        besede, n_def, n_slo = set(), 0, 0
        with open(DEFIN, encoding="utf-8") as f:
            telo = f.read()
        m = STANJE.search(telo)
        if m:
            n_def = int(m.group(1))
            for zn in re.split(r"[·,;]", m.group(2)):
                zn = zn.strip().strip(":")
                if zn and BES.match(zn):
                    besede.add(zn.lower())
        with open(SLOVAR, encoding="utf-8") as f:
            for v in f:
                mm = GLAVA_SLOV.match(v)
                if mm:
                    n_slo += 1
                    for zn in re.split(r"[\s-]+", mm.group(1)):
                        if BES.match(zn):
                            besede.add(zn.lower())
        _KES = (besede, n_def, n_slo)
    return _KES

def lastni_md5():
    h = hashlib.md5(open(os.path.abspath(__file__), "rb").read())
    return h.hexdigest()[:12]

def tik():
    return _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

def razcepi_niz(term):
    """vrne ( levi, desni, odnos, izvor ) ali None"""
    for zn, ime, price in ODNOSI:
        if zn in term:
            levi, desni = term.split(zn, 1)
            return (levi.strip(), desni.strip(), ime, "deklariran šiv " + zn + " ⊢ " + price)
    for zn in ("+", "/"):
        if zn in term:
            levi, desni = term.split(zn, 1)
            return (levi.strip(), desni.strip(), None, "šiv " + zn + " prisoten, odnos " + NEZNAN)
    besede = nabor()[0]
    t = term.lower().strip(".,;:!?»«\"()[]")
    for k in range(2, len(t) - 1):
        levi, desni = t[:k], t[k:]
        if levi in besede and desni in besede:
            return (levi, desni, None, "skrit šiv najden po naboru ⊢ ( " + levi + " ∧ " + desni +
                    " izmerjena pri viru definiatorne ∧ slovarja, grep ⊢ )")
    return None

def vprasanja(ime, clement):
    print("  člen ⟨" + clement + "⟩ :")
    print("    1. KAKOR KAJ? - kakšen je pravi " + ime + " ⟨" + clement + "⟩ ( izrek vprašanja ⊙ 2690 )")
    print("    2. KAJ JE ⟨" + clement + "⟩? - bistvo : nabor izmerjen ( grep ⊢ ) ;"
          " neznan => pobuda iztočnice ( ⟨NE⟩ napaka ⊙ σ 5809 )")
    print("    3. ZAKAJ JE ⟨" + clement + "⟩? - svrha : vprašanje izrečeno, odgovor je ⟡ ⚔ ( ⊙ 2690 )")

def seciraj(term):
    besede, n_def, n_slo = nabor()
    print("SECIRNIK " + VERZIJA + " TIK " + tik() + " lastni-md5 " + lastni_md5() + " ( MERILEC-SE-MERI §52 )")
    print("nabor izmerjen pri viru ⊢ : definiatorna iztočnic " + str(n_def) + " ∧ slovar iztočnic " +
          str(n_slo) + " ( wc ∧ grep ⊢ ) ; telo TERM : " + str(len(term)) + " znakov ( wc ⊢ )")
    r = razcepi_niz(term)
    if r is None:
        print("šiv ×0 : bisti ⟨" + term + "⟩ nista izmerjeni v naboru ⇒ RUMENA pobuda ( RAZCEP x0, ⟨NE⟩ napaka ⊙ zanesljivost-po-izmeri σ 5809 )")
        print("SEMAFOR : RUMENA ( pobuda : met bisti v definiatorno ∧ slovar )")
        return 2
    levi, desni, odnos, izvor = r
    print("razcep izveden ⊢ : " + izvor)
    print("AMALGAMACIJA PREPOZNANA ∧ SECIRANA poimensko : " + term + " = ⟨" + levi + "⟩ ⌇ ⟨" + desni + "⟩")
    if odnos is None:
        print("odnos : " + NEZNAN)
    else:
        print("odnos : " + odnos + " ( šiv DEKLARIRAN ⇒ telo ni amalgamacija ; razcep izmerjen javno ⊢ )")
    print("priča pojmov ⊢ pri viru : amalgamacija = mir v nemiru ( biro-postaje r.147 @σ 5989 ) ⌇ "
          "križišče XII amalgamacija vseh poti ( atlas-knjiznic r.97 ) ; kura = razcep, mir in nemir poimensko ⊙ ⟨NI LE...TUDI⟩ r.32")
    vprasanja("levi člen", levi)
    vprasanja("desni člen", desni)
    print("SEMAFOR : " + ("ZELENA ( deklariran šiv, razcep javno )" if odnos else "ZELENA ( skrit šiv razcepljen, odnos ⟡ ⚔ )"))
    return 0

def prepoznaj(besedilo):
    besede, n_def, n_slo = nabor()
    print("SECIRNIK " + VERZIJA + " TIK " + tik() + " lastni-md5 " + lastni_md5() + " ( MERILEC-SE-MERI §52 )")
    print("nabor izmerjen pri viru ⊢ : definiatorna iztočnic " + str(n_def) + " ∧ slovar iztočnic " + str(n_slo) + " ( wc ⊢ )")
    kandidati, nzlozenke = [], 0
    for t in re.findall(r"[A-Za-zčšžČŠŽćđ]{6,}", besedilo):
        nzlozenke += 1
        low = t.lower()
        for k in range(2, len(low) - 1):
            levi, desni = low[:k], low[k:]
            if levi in besede and desni in besede:
                besede_kopija = True
                kandidati.append((t, levi, desni))
                break
    for t, levi, desni in kandidati:
        print("kandidat AMALGAMACIJE poimensko : " + t + " = ⟨" + levi + "⟩ ⌇ ⟨" + desni +
              "⟩ ( skrit šiv, oba člena izmerjena v naboru ⊢ grep ) ; zloženka vidi enaka, "
              "obsodba je sodba ⟡ ⚔ ⊙ ⟨NE-UGIBAJ⟩ 2690")
    print("izmera : besed " + str(nzlozenke) + " ∧ kandidatov " + str(len(kandidati)) +
          " ( wc ⊢ ) ; prepoznava je IZMERA, ⟨ne⟩ obsodba")
    print("SEMAFOR : ZELENA ( prepoznava izrečena javno ; mir v nemiru prejet : vsak šiv dobi ime ⊢ biro-postaje r.147 )")
    return 0

def samopreizkus():
    T = [0, 0, 0, 0, 0]
    r1 = razcepi_niz("napakavic")
    T[0] = 1 if (r1 and r1[0] == "napaka" and r1[1] == "vic" and r1[2] is None and
                 "skrit" in r1[3]) else 0
    e2 = prepoznaj("beseda napakavic živi med telesi ⊢") 
    T[1] = 1 if (e2 == 0 and razcepi_niz("napakavic")[0] == "napaka") else 0
    r3 = razcepi_niz("napaka⊥vic")
    T[2] = 1 if (r3 and r3[2] and "ANTINOM" in r3[2] and "deklariran" in r3[3]) else 0
    r4 = razcepi_niz("xyzqwv")
    T[3] = 1 if (r4 is None) else 0
    besede, n_def, n_slo = nabor()
    T[4] = 1 if (n_def >= 100 and n_slo >= 1 and os.path.isfile(DEFIN) and os.path.isfile(SLOVAR)) else 0
    p = 5 - sum(T)
    print("SAMOPREIZKUS : vektorji 5 ( napakavic=" + str(T[0]) + " prepoznaj=" + str(T[1]) +
          " antinom=" + str(T[2]) + " siv-x0=" + str(T[3]) + " nabor=" + str(T[4]) +
          " ), padci instrumenta " + str(p) + " ; nabor " + str(len(besede)) + " besed ( wc ⊢ )")
    print("SEMAFOR : " + ("ZELENA" if p == 0 else "RDECA"))
    return 0 if p == 0 else 1

def main(a):
    if a == ["--test"]:
        return samopreizkus()
    if len(a) >= 2 and a[0] == "--seciraj":
        return seciraj(" ".join(a[1:]))
    if len(a) >= 2 and a[0] == "--prepoznaj":
        return prepoznaj(" ".join(a[1:]))
    print("roke : --seciraj TERM ⌇ --prepoznaj TELESO ⌇ --test ; izhodi : 0 ZELENA ⌇ 2 RUMENA ( pobuda ) ⌇ 40")
    return 40

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
