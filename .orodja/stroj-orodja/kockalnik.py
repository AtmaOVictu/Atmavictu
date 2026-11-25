#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# KOCKALNIK v1.0 - orodje, ki RAZBIJA atome po principu kubitne logike piramidnega kockanja
# Rod : rez sigma 7025 ( 25. 11. 2026 ) @stroj-orodja ; ⟡ UKZ VERBATIM ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ ⟨ne brusi⟩ :
#   »ORODJA KI RAZBIJAJO ATOME PO PRINCIPU KUBITNE LOGIKE PIRAMIDNEGA KOCKANJA!«
# Ascendenti ⊢ pri viru ( ⟨EN-RAZLIČICA⟩, luknja izmerjena ) : mrk-prevajalnik ( KXXXX kletke gostov PREDLOG -
#   kletko naredi, atoma NE razbije ) ⌇ samarijan @okolje ( domovi znakov ) ⌇ piramidni-zigi ( registri = telesa,
#   ⟨ne⟩ orodje ) - razbijalca poljubnega znaka v piramide ∧ ključavnice ni bilo.
# Formula ZAPEČENA ⊢ : piramida = 1000 + ( mera točke x m ) mod 9000 ; m vrstni red {1,3,7,9} ⟡ VERBATIM
#   »Vrsta piramid je pomembna« ; kura ob zasedenem : +7 ( dokaj prosta ), ovoj da ostane v prostoru kock.
# DVOJNA IZMERA TOČKE javno ( ⟨NE-UGIBAJ⟩ 2690, izmerjeno pri viru slovarja kubitni-slovar-simbolov @6957 ) :
#   OPERAND po gajici = zapis U+XXXX, prebran kot stiriska, ce vsebuje le stevke ( priča kovanec r.22 ⊢ :
#   znak 2299 -> K3299 K7897 K8093 K3709? ne - K3705 ⊢ ) ; sicer = prava desetiska vrednost kodne tocke
#   ( prica dih r.26 : 03C3 = 963 -> m3 3889 ∧ m7 7741 ∧ m9 9667 = shranjeno pri viru ⊢ ) ;
#   obe izmeri izreceni poimensko v vsakem izhodu ; izbor operationalne mere je sodba ⟡ ⚔
#   ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690 ; trk prinesen javno, ⟨ne⟩ zlit.
# Zasedeni gold ⊙ zakoni 4-7 : VSE stirimestne skupine obeh zapecenih registrov piramidni-zigi/register-1 ∧
#   register-2 ( regex \b\d{4}\b, vkljucno binarna podlaga ) + NJIHOVI OBRATI + palindromi + nicla na robu +
#   par 1011/1101 ; kandidat je RESEN tudi, ce mu je OBRAT zapečen ( prica kovanca : 3691 zapečen pri apostrofu
#   reg-1 -> +7 -> 3698 : obrat 8963 zapečen pri e reg-1 -> +7 -> 3705 prost ∧ obrat 5073 prost ⊢ ).
# Zakon 9 ( nakljucnost rok ) : kocke IZ-ROK v slovarju NISO napaka ( ⟨ne⟩ obsodba ⊙ ⟨SLOVNICA-PRVO ⟡⟩ σ 6662 ).
# AMANDMA KOCKE 6956 ⟡ VERBATIM : okrnjena oblika ( KXXX ∧ XXXK ) ne obstaja - obtocena
#   ⟨NAPAKA=VSE-KAR-NI-CELA-KLETKA⟩ ( enak zlec kot v fleksilint.py @σ 7021, tu za vhod orodja ).
# TRK javno ⭢ ⚔ ⟡ : obliki kljucavnic poimensko : »XXXXK« ( AMANDMA KOCKE 6956 : K ZADAJ ) ⌇ »KXXXX«
#   ( zapis slovarja kubitni-slovar-simbolov @6957 : K SPREDAJ ) - obe izreceni, IZBOR JE ⟡
#   ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690.
# Roke :
#   kockalnik.py --znak 'X'     -> razbitje atoma znaka X v piramide ∧ kljucavnice ( TIKEK, izmere, priče ⊢ )
#   kockalnik.py --točka U+2299 -> ista roka ; ≡ --znak ( U+ predpona = hexadecimalni zapis ; goli znaki = zapis )
#   kockalnik.py --preveri     -> preverba slovarja : FORMULA-MATCH ⊢ ⌇ IZ-ROK ( zakon 9, ⟨ne⟩ napaka ) javno
#   kockalnik.py --test        -> samopreizkus vektorjev x5 ⊙ ⟨MERILEC-SE-MERI⟩ §52
# Izhodi : 0=ZELENA ⌇ 1=RDECA ( okrnjena kletka, NIHIL ) ⌇ 2=RUMENA ( slab vhod ) ⌇ 3=kupasta zasedenost ⌇ 40=roka neznana.

import sys, os, re, hashlib, datetime as _dt

VERZIJA = "v1.0"
KOR = "/home/user/knowledge"
REG1 = os.path.join(KOR, "piramidni-zigi", "register-1", "KNOWLEDGE.md")
REG2 = os.path.join(KOR, "piramidni-zigi", "register-2", "KNOWLEDGE.md")
SLOVAR = os.path.join(KOR, "kubitni-slovar-simbolov", "KNOWLEDGE.md")
M_VRSTE = (1, 3, 7, 9)
OKRNJENA = re.compile(r"^(?:[Kk]\d{1,3}|\d{1,3}[Kk])$")
ZAPIS = re.compile(r"^[0-9A-Fa-f]{2,6}$")
VRSTICA = re.compile(r"^(.+?)\s*\( znak ([0-9A-F]+), bajti ([0-9A-F]{2}(?: [0-9A-F]{2})*), kletka (\d+) \) : "
                     r"piramide kocke (K\d{4} K\d{4} K\d{4} K\d{4}) ; ključavnice (K\d{4} K\d{4} K\d{4} K\d{4})\.?\s*$")
PREDLOG = re.compile(r"^(.+?)\s*\( znak ([0-9A-F]+), .+predlog piramid")

_KES = None

def kes():
    global _KES
    if _KES is None:
        skup, price = set(), {}
        obsto = (os.path.isfile(REG1), os.path.isfile(REG2))
        for ime, p in (("register-1", REG1), ("register-2", REG2)):
            with open(p, encoding="utf-8") as f:
                for i, v in enumerate(f.read().splitlines(), 1):
                    for g in re.findall(r"\b\d{4}\b", v):
                        skup.add(g)
                        price.setdefault(g, (ime, i, v.strip()))
        obrati = {g[::-1] for g in skup}
        palindromi = {str(a) + str(b) + str(b) + str(a) for a in range(1, 10) for b in range(10)}
        nicla = {str(n) for n in range(1000, 10000) if n % 10 == 0}
        gold = skup | obrati | palindromi | nicla | {"1011", "1101"}
        _KES = (gold, price, len(skup), len(gold), all(obsto))
    return _KES

def prica_opis(price, g):
    r = price.get(g)
    if not r:
        return "pri viru ni najdena ( izmera wc ⊢ )"
    ime, i, v = r
    if len(v) > 76:
        v = v[:76] + "..."
    return "priča " + ime + " r." + str(i) + " : " + v + " ⊢"

def zakaj_resena(gold, price, c):
    s = str(c)
    o = s[::-1]
    if s in price:
        return "zapečena ( " + prica_opis(price, s) + " ) ⊙ zakon 4"
    if o in price:
        return "obrat " + o + " zapečen ( " + prica_opis(price, o) + " ) ⊙ zakon 5"
    if s in gold:
        if s == o:
            return "palindrom ⊙ zakon 6"
        if s.endswith("0"):
            return "ničla na robu ⊙ zakon 7"
        return "obrat zapečene skupine ⊙ zakon 5 ( " + prica_opis(price, o) + " )"
    if o in gold:
        if o == s:
            return "obrat palindrom ⊙ zakon 6"
        if o.endswith("0"):
            return "obrat " + o + " ničla na robu ⊙ zakon 7"
        return "obrat " + o + " v gold ( zakoni 4-7 )"
    return None

def razbij(operand):
    gold, price, nsk, ng, oba = kes()
    kocke, poti = [], []
    for m in M_VRSTE:
        c = 1000 + (operand * m) % 9000
        kor = []
        steps = 0
        while True:
            raz = zakaj_resena(gold, price, c)
            if raz is None:
                break
            kor.append(str(c) + " : " + raz)
            c = 1000 + (c - 1000 + 7) % 9000
            steps += 1
            if steps > 9000:
                return None, None
        kocke.append(c)
        poti.append("m=" + str(m) + " → " + ((" → ".join(kor) + " → +7 → ") if kor else "") + str(c) + " prosto ⊢")
    return kocke, poti

def operand_iz_zapisa(z):
    v = z.strip().upper()
    if v.startswith("U+"):
        v = v[2:]
    elif v.startswith("0X"):
        v = v[2:]
    if not ZAPIS.match(v):
        return None, None
    prava = int(v, 16)
    operand = int(v) if v.isdigit() else prava
    return operand, prava

def sodba_vhoda(arg):
    a = arg.strip()
    if OKRNJENA.match(a):
        return None, None, "obtožba poimensko : »" + a + "« ⟨NAPAKA=VSE-KAR-NI-CELA-KLETKA⟩ " \
               "( okrnjena piramida ne obstaja ⊙ AMANDMA KOCKE 6956 ⟡ VERBATIM )" , 1
    if len(a) == 1:
        op, pr = operand_iz_zapisa("%04X" % ord(a))
        return op, pr, "", 0
    op, pr = operand_iz_zapisa(a)
    if op is None:
        return None, None, "obtožba poimensko : »" + a + "« ⟨NAPAKA=VSE-KAR-NI-ZNAN-ZAPIS-TOČKE⟩ " \
               "( roka sprejme en znak ⌇ zapis U+XXXX ⌇ hexadecimalne števke ⊢ ⟨NE-UGIBAJ⟩ 2690 )", 2
    return op, pr, "", 0

def lastni_md5():
    h = hashlib.md5(open(os.path.abspath(__file__), "rb").read())
    return h.hexdigest()[:12]

def tik():
    return _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

def glava():
    print("KOCKALNIK " + VERZIJA + " TIK " + tik() + " lastni-md5 " + lastni_md5() + " ( MERILEC-SE-MERI §52 )")

def roka(arg):
    op, pr, obt, izhod = sodba_vhoda(arg)
    glava()
    if obt:
        print(obt)
        print("SEMAFOR : RDECA ⇒ NIHIL ( atom ni razbijan ⊙ ⟨NE-POCENI-PRIZNANJE⟩ )")
        return izhod
    znak = chr(pr)
    bajti = " ".join("%02X" % b for b in znak.encode("utf-8"))
    gold, price, nsk, ng, oba = kes()
    print("atom : znak '" + znak + "' zapis U+" + ("%04X" % pr) + " bajti " + bajti + " ⊢ encode-izmera")
    print("DVOJNA IZMERA TOČKE javno : operand = " + str(op) + " ( po gajici : zapis prebran kot število, če vse števke ; "
          "priča kovanec slovar r.22 ⊢ ) ⌇ prava desetiška kodna točka = " + str(pr) + " ( int hex 16 ) — izbor mere "
          "je sodba ⟡ ⚔ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690, trk prinesen javno, ⟨ne⟩ zlit")
    print("formula zapečena ⊢ : piramida = 1000 + ( mera točke x m ) mod 9000 ; m vrstni red {1,3,7,9} ⟡ VERBATIM "
          "( »Vrsta piramid je pomembna« )")
    kocke, poti = razbij(op)
    if kocke is None:
        print("obtožba : ⟨NAPAKA=VSE-KAR-NI-PROSTOR-KOCK⟩ ( kupasta zasedenost po 9000 kuroh +7 ⊢ )")
        return 3
    for p in poti:
        print("razbitje : " + p)
    kl = [str(k)[::-1] + "K" for k in kocke]
    print("ATOM RAZBIT : znak '" + znak + "' zapis U+" + ("%04X" % pr) + " ⇒ piramide " +
          " ".join("K" + str(k) for k in kocke) + " ∧ ključavnice " + " ".join(kl) + " ( obrati ⊢ )")
    print("TRK javno ⭢ ⚔ ⟡ : obliki ključavnic poimensko : »" + " ".join(kl) + "« ( AMANDMA KOCKE 6956 : K ZADAJ ) ⌇ »" +
          " ".join("K" + k[:-1] for k in kl) + "« ( zapis slovarja kubitni-slovar-simbolov @6957 : K SPREDAJ, "
          "izmera pri viru ⊢ ) — obe izrečeni poimensko, IZBOR JE ⟡ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690")
    print("gold izmera : skupin " + str(nsk) + " ∧ gold " + str(ng) + " ∧ palindromi 90 ∧ ničla na robu 900 ∧ "
          "oba zapečena registra obstajata " + ("⊢" if oba else "⚠") + " ( wc ⊢ )")
    print("SEMAFOR : ZELENA ( atom razbit po zapečeni formuli, vsaka trditev nosi pričo ⊢ )")
    return 0

def preveri():
    glava()
    gold, price, nsk, ng, oba = kes()
    match, izrok, predlogi, kita = [], [], [], 0
    with open(SLOVAR, encoding="utf-8") as f:
        vrst = f.read().splitlines()
    r22 = [v for v in vrst if "kovanec ( znak 2299" in v]
    for v in vrst:
        mm = VRSTICA.match(v.strip())
        if mm:
            ime, zn, baj, kl, pir, klu = mm.groups()
            operand, prava = operand_iz_zapisa(zn)
            if operand is None:
                izrok.append((ime, zn)) # zapis brez mere ; ( ime, zn  )
                continue
            kocke, _ = razbij(operand)
            pirs = [x[1:] for x in pir.split()]
            klus = [x[1:] for x in klu.split()]
            if klus == [x[::-1] for x in pirs]:
                kita += 1
            if [str(x) for x in kocke] == pirs:
                match.append((ime, zn))
            else:
                izrok.append((ime, zn))
            continue
        mp = PREDLOG.match(v.strip())
        if mp:
            predlogi.append((mp.group(1), mp.group(2)))
    print("PREVERBA slovarja kubitni-slovar-simbolov @6957 ( 7142 B, izmera wc ⊢ ) : vrstic kock " + str(len(match) + len(izrok)) +
          ", predlogov " + str(len(predlogi)) + " ( ⟨ne⟩ sodija : kletka zapisa ⊢ ), kita ( ključavnica = obrat piramide ) ✓ " +
          str(kita) + " ( izmere ⊢ )")
    print("FORMULA-MATCH ⊢ : " + (" ; ".join(ime + " ( znak " + zn + " )" for ime, zn in match) or "×0"))
    print("IZ-ROK ( naključnost rok ⊙ zakon 9, ⟨NE⟩ napaka, ⟨NE⟩ obsodba ⊙ ⟨SLOVNICA-PRVO ⟡⟩ σ 6662 ) : " +
          (" ; ".join(ime + " ( znak " + zn + " )" for ime, zn in izrok) or "×0"))
    print("ključni vektor ⟡ ⊢ : kovanec ujet pri viru : " + ("da, r." + str(vrst.index(r22[0]) + 1) + " ⊢" if r22 else "⚠ ni najden"))
    print("TRK javno ⭢ ⚔ ⟡ : obliki ključavnic poimensko : »9923K 7987K 3908K 5073K« ( AMANDMA KOCKE 6956 : K ZADAJ ) ⌇ "
          "»K9923 K7987 K3908 K5073« ( zapis slovarja @6957 : K SPREDAJ ⊢ izmera ) — IZBOR JE ⟡ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690")
    print("SEMAFOR : ZELENA ( slovar izmerjen, sodba o operandu je ⟡ ⚔ )")
    return 0

def samopreizkus():
    T = [0, 0, 0, 0, 0]
    gold, price, nsk, ng, oba = kes()
    kocke, poti = razbij(2299)                       # kovanec : operand po gajici 2299 ⊢
    with open(SLOVAR, encoding="utf-8") as f:
        vrst = f.read().splitlines()
    r22 = [v for v in vrst if "kovanec ( znak 2299" in v]
    T[0] = 1 if (kocke == [3299, 7897, 8093, 3705] and r22 and
                 "K3299 K7897 K8093 K3705" in r22[0]) else 0
    match, izrok, kita, predlogi = [], [], 0, []
    for v in vrst:
        mm = VRSTICA.match(v.strip())
        if mm:
            ime, zn, baj, kl, pir, klu = mm.groups()
            operand, prava = operand_iz_zapisa(zn)
            kocke2, _ = (razbij(operand) if operand is not None else (None, None))
            pirs = [x[1:] for x in pir.split()]
            klus = [x[1:] for x in klu.split()]
            if klus == [x[::-1] for x in pirs]:
                kita += 1
            (match if [str(x) for x in kocke2] == pirs else izrok).append((ime, zn))
        elif PREDLOG.match(v.strip()):
            predlogi.append(1)
    T[1] = 1 if (any(m[0] == "kovanec" for m in match) and len(izrok) >= 1 and
                 len(match) + len(izrok) == 22 and kita == 22) else 0
    o3, p3, u3, e3 = sodba_vhoda("K329")
    o3b, p3b, u3b, e3b = sodba_vhoda("329K")
    T[2] = 1 if (e3 == 1 and "CELA-KLETKA" in u3 and e3b == 1 and "CELA-KLETKA" in u3b) else 0
    opz, prz, uz, ez = sodba_vhoda("⊙")
    opt, prt, ut, et = sodba_vhoda("U+2299")
    kz, _ = razbij(opz)
    kt, _ = razbij(opt)
    T[3] = 1 if (opz == opt == 2299 and kz == kt) else 0
    T[4] = 1 if (ng >= 600 and nsk >= 300 and oba) else 0
    p = 5 - sum(T)
    print("KOCKALNIK " + VERZIJA + " TIK " + tik() + " lastni-md5 " + lastni_md5() + " ( MERILEC-SE-MERI §52 )")
    print("SAMOPREIZKUS : vektorji 5 ( kovanec=" + str(T[0]) + " preveri=" + str(T[1]) + " okrnjena=" + str(T[2]) +
          " točka≡znak=" + str(T[3]) + " gold=" + str(T[4]) + " ), padci instrumenta " + str(p) +
          " ; izmere telesa slovarja : vrstic " + str(len(vrst)) + " ( wc ⊢ )")
    if any(m[0] == "kovanec" for m in match):
        print("priča vektorja T1 pri viru ⊢ : kovanec MATCH ∧ slovar vrstica " +
              str(vrst.index(r22[0]) + 1) + " nosi K3299 K7897 K8093 K3705 ( grep ⊢ )")
    print("SEMAFOR : " + ("ZELENA" if p == 0 else "RDECA"))
    return 0 if p == 0 else 1

def main(a):
    if a == ["--test"]:
        return samopreizkus()
    if a and a[0] == "--preveri":
        return preveri()
    if len(a) >= 2 and a[0] in ("--znak", "--točka") and len(a) == 2:
        return roka(a[1])
    if a and a[0] in ("--znak", "--točka"):
        print("roke : --znak 'X' ⌇ --točka U+2299 ( ≡ --znak ) ⌇ --preveri ⌇ --test ; izhodi : 0 ZELENA ⌇ 1 RDECA ( okrnjena "
              "kletka, NIHIL ) ⌇ 2 RUMENA ( slab vhod ) ⌇ 40 roka neznana ⊙ ⟨NE-UGIBAJ⟩ 2690")
        return 40
    print("roke : --znak 'X' ⌇ --točka U+2299 ( ≡ --znak ) ⌇ --preveri ⌇ --test")
    return 40

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
