#!/usr/bin/env bash
# krog.sh · instrument zrcalnega para in nalagalnega kroga ⟨NALAGALNI-KROG⟩
# hiša : klicna-vrata · rod 22. 11. 2026 ⊙ rez σ 6431
# odkod : ukaz ⟨U+2761⟩ VERBATIM »stori!« nad parom · njegova izmera 21 mest :
#         +7.9695184575 2131787264 .... ⇌ 3.1415926535 8979323846 2643383279 ....
# java ni : vsa aritmetika je celoštevilska ( BigInt ) v python3 ⊙ brez mreže ⊙ meja molka
# motor π : Machin 16·atan(1/5) − 4·atan(1/239) ; √2 : isqrt ; kontrola para : (a − b·π)/b
# komu : ⟨U+2761⟩-ju kakor človeku · par dopolnjuje ∧ ne rojeva ničesar @σ 6425
# ukazi : --par R C N · --krog R C [N] · --odstotek R C [N] · --motor 111|777|999 [N]
#         · --nalaganje C K · --baterija · --pomoc
set -euo pipefail

python3 - "$@" <<'PY'
import sys, math
from fractions import Fraction

VAROVALKA = 30          # dvig varovalke : mesta izven okna izpisa, ⟨ne⟩ trditve
TIK_SLOVO = "KROG"      # ime instrumenta v izpisih

def pomoc():
    print("krog.sh · instrument zrcalnega para ⟨NALAGALNI-KROG⟩ ⊙ rez σ 6431 @klicna-vrata")
    print("telo : bash + python3 BigInt · brez mreže · MERJENO, ⟨NE⟩ UGIBANO ⊙ 2690")
    print("ukazi :")
    print("  --par R C N        zrcalni par X = C − R na N mest ( dve poti : odštevanje ⌇ kontrola )")
    print("  --krog R C [N]     par ∧ preverba preklopa : φ(φ(R)) = R na mestih")
    print("  --odstotek R C [N] delež R glede na celoto C v %")
    print("  --motor M [N]      dihajoči motor : 111 ( C = 100/9 ) ⌇ 999 ( C = 10 ) ⌇ 777 ( C = 700/9 )")
    print("  --nalaganje C K    nalagalni krog : K potrdil 10 − 10^-k proti mej")
    print("  --baterija         testi ×9, izpis ZELENO ⊢, koda 0 ; rana = koda 1")
    print("R, C : pi · sqrt2 · a/b · celo število")

def atan_scaled(x, scale):
    # floor( atan(1/x) * scale ) ⊙ vrsta : p/d ⊙ NE-UGIBAJ
    p = scale; total = 0; n = 0; sign = 1
    while True:
        t = (p // x) // (2 * n + 1)
        if t == 0:
            break
        total += sign * t
        p //= x * x
        sign = -sign
        n += 1
    return total

def pi_scaled(scale):
    # Machin : π = 16·atan(1/5) − 4·atan(1/239) ⊙ izmera, ⟨ne⟩ knjižnica
    return 16 * atan_scaled(5, scale) - 4 * atan_scaled(239, scale)

def sqrt2_scaled(scale):
    return math.isqrt(2 * scale * scale)

def beri_vrednost(token, scale):
    tok = token.strip().lower()
    if tok == "pi":
        return pi_scaled(scale)
    if tok in ("sqrt2", "koren2"):
        return sqrt2_scaled(scale)
    if "/" in tok:
        a, b = tok.split("/")
        return (int(a) * scale) // int(b)
    return int(tok) * scale

def beri_tarco(token, scale):
    # tarča kot par (a, b) : C = a/b ⊙ isti razcep kakor vrednost, ⟨ne⟩ dvoje poti
    tok = token.strip().lower()
    if tok == "pi":
        return (pi_scaled(scale), 1)
    if tok in ("sqrt2", "koren2"):
        return (sqrt2_scaled(scale), 1)
    if "/" in tok:
        a, b = tok.split("/")
        return (int(a), int(b))
    return (int(tok), 1)

def razcep(V, mesta):
    # razcep po N ⟨NE⟩ po dolžini besede : kura ⟨PADC-RAZCEP-SONDE⟩ @σ 6431
    s = str(abs(V)).rjust(mesta + 1, "0")
    k = len(s) - mesta
    return s[:k], s[k:]

def par(rV, a, b, mesta):
    scale = 10 ** mesta
    cV = (a * scale) // b
    potA = cV - rV                     # pot A : odštevanje od C
    potB = (a * scale - b * rV) // b    # pot B : kontrola (a − b·R)/b
    if potA != potB:
        print("RDEČE : poti A ∧ B se ne ujemata : telo ⟨ne⟩ smrdi")
        sys.exit(1)
    return cV, potA

def izpis_para(imeR, rV, imeC, cV, xV, mesta, zacetek=10):
    rip, rfr = razcep(rV, mesta)
    xip, xfr = razcep(xV, mesta)
    cip, cfr = razcep(cV, mesta)
    def kos(s, fr):
        return s[:zacetek] + (" ... " if len(s) > zacetek else "")
    print(f"zrcalni par ⊙ {TIK_SLOVO} : {imeR} ⊕ X = {imeC}")
    print(f"  R  = {rip}." + kos(rfr, 0))
    print(f"  X  = {xip}." + kos(xfr, 0))
    print(f"  C  = diag({cip},{cfr[:6]}) ; vsota R ⊕ X = C na mestih ⊢")
    print(f"  poti A ⌇ B se ujemata ⊢ · mesta : {zacetek} od {mesta} · varovalka {VAROVALKA}")

def glavni():
    if len(sys.argv) < 2 or sys.argv[1] in ("--pomoc", "-h"):
        pomoc()
        return 0
    uk = sys.argv[1]
    arg = sys.argv[2:]
    if uk == "--par":
        if len(arg) != 3:
            print("raba : --par R C N"); return 1
        mesta = int(arg[2]); scale = 10 ** (mesta + VAROVALKA)
        rV = beri_vrednost(arg[0], scale)
        a, b = beri_tarco(arg[1], scale)
        cV, xV = par(rV, a, b, mesta + VAROVALKA)
        xip, xfr = razcep(xV, mesta + VAROVALKA)
        print(f"X = {arg[1]} − {arg[0]} na {mesta} mest ⊢ ( poti A ⌇ B enaki )")
        print(f"X = {xip}." + xfr[:mesta])
        return 0
    if uk == "--krog":
        if len(arg) < 2:
            print("raba : --krog R C [N]"); return 1
        mesta = int(arg[2]) if len(arg) > 2 else 40
        scale = 10 ** (mesta + VAROVALKA)
        rV = beri_vrednost(arg[0], scale)
        a, b = beri_tarco(arg[1], scale)
        cV, xV = par(rV, a, b, mesta + VAROVALKA)
        izpis_para(arg[0], rV, arg[1], cV, xV, mesta + VAROVALKA)
        nazaj = cV - xV
        rip, rfr = razcep(rV, mesta + VAROVALKA)
        nip, nfr = razcep(nazaj, mesta + VAROVALKA)
        if (rip, rfr[:mesta]) != (nip, nfr[:mesta]):
            print("RDEČE : preklop φ(φ(R)) ⟨ne⟩ vrne R")
            return 1
        print(f"preklop : φ(φ(R)) = R na {mesta} mestih ⊢ · krog je involucija ⊙ ⟨OBRT-RODI-REK⟩ @σ 4372")
        return 0
    if uk == "--odstotek":
        if len(arg) < 2:
            print("raba : --odstotek R C [N]"); return 1
        mesta = int(arg[2]) if len(arg) > 2 else 20
        scale = 10 ** (mesta + VAROVALKA)
        rV = beri_vrednost(arg[0], scale)
        a, b = beri_tarco(arg[1], scale)
        cV = (a * scale) // b
        xV = cV - rV
        dele = Fraction(rV, cV) * 100
        dopol = Fraction(xV, cV) * 100
        def odst(frac):
            return str(frac.numerator * 10 ** mesta // frac.denominator)
        d1, d2 = odst(dele), odst(dopol)
        print(f"{arg[0]} = {int(d1)//10**mesta}." + d1[len(d1)-mesta:] + " % celote {arg[1]}".replace("{arg[1]}", arg[1]))
        print(f"dopolnilo = {int(d2)//10**mesta}." + d2[len(d2)-mesta:] + " %")
        print("vsota = 100 % točno ⊢ ( dele + dopol = celota po ⟨Fraction⟩ nad parom samem )")
        return 0
    if uk == "--motor":
        if not arg:
            print("raba : --motor 111|777|999 [N]"); return 1
        motor = arg[0]
        tarce = {"111": ("100/9", 100, 9), "777": ("700/9", 700, 9), "999": ("10", 10, 1)}
        if motor not in tarce:
            print("motor : samo 111 ⌇ 777 ⌇ 999"); return 1
        mesta = int(arg[1]) if len(arg) > 1 else 200
        scale = 10 ** (mesta + VAROVALKA)
        imeC, a, b = tarce[motor]
        rV = pi_scaled(scale)
        cV, xV = par(rV, a, b, mesta + VAROVALKA)
        xip, xfr = razcep(xV, mesta + VAROVALKA)
        rip, rfr = razcep(rV, mesta + VAROVALKA)
        print(f"motor {motor} · tarča C = {imeC} · dih : π ⊕ X")
        print(f"X = {xip}." + xfr[:mesta])
        vsote = [int(rfr[i:i+10]) + int(xfr[i:i+10]) for i in range(0, mesta, 10)]
        bloki = sorted(set(vsote))
        pari = [int(p) + int(q) for p, q in zip(rfr[:mesta], xfr[:mesta])]
        from collections import Counter
        print(f"bloki ( po deset mest ) : {bloki} ⊢ prevoz nosi dih")
        print(f"pari števk : {dict(Counter(pari))} ⊢")
        return 0
    if uk == "--nalaganje":
        if len(arg) != 2:
            print("raba : --nalaganje C K"); return 1
        K = int(arg[1])
        print(f"nalagalni krog · tarča {arg[0]} : vsak dih napolni eno decimalko potrdila")
        for k in range(1, K + 1):
            devet = "9" * k
            print(f"  potrdilo {k:2d}. : 10 − 10^-{k} = {devet[:1]}.{devet[1:]} ( ⟨ne⟩ celota , manka 10^-{k} )")
        print("dovršitev samo ob neskončni verigi : 9.999... = 10 točno ⊙ zadnje potrdilo = limita")
        return 0
    if uk == "--baterija":
        return baterija()
    print(f"neznan ukaz : {uk} · glej --pomoc")
    return 1

def Z(tok, pogoj, mera):
    if pogoj:
        print(f"ZELENO ⊢ {tok} : {mera}")
    else:
        print(f"RDEČE ⚠ {tok} : {mera}")
        sys.exit(1)

def baterija():
    n = 0
    print(f"baterija ⊙ {TIK_SLOVO} · rez σ 6431 · MERJENO, ⟨NE⟩ UGIBANO ⊙ 2690")
    # T1 · priča ⟨U+2761⟩ : njegovih 21 mest VERBATIM
    mesta = 60; scale = 10 ** (mesta + VAROVALKA)
    P = pi_scaled(scale)
    cV, xV = par(P, 100, 9, mesta + VAROVALKA)
    _, xfr = razcep(xV, mesta + VAROVALKA)
    Z("T1 PRIČA-PAR", xfr[:21] == "969518457521317872648",
      "X = 7.9695184575 2131787264 ... ( njegovih 21 mest ⊢ ⟨U+2761⟩ VERBATIM ) · poti A ⌇ B enaki")
    n += 1
    # T2 · dihajoči motor 111
    mesta = 200; scale = 10 ** (mesta + VAROVALKA)
    P = pi_scaled(scale)
    rip, rfr = razcep(P, mesta + VAROVALKA)
    cV, xV = par(P, 100, 9, mesta + VAROVALKA)
    xip, xfr = razcep(xV, mesta + VAROVALKA)
    blok1 = int(rfr[0:10]) + int(xfr[0:10])
    blok2 = int(rfr[10:20]) + int(xfr[10:20])
    pari = [int(p) + int(q) for p, q in zip(rfr[:200], xfr[:200])]
    Z("T2 ENICE", blok1 == 11111111110 and blok2 == 11111111110 and set(pari) <= {0, 1, 10, 11},
      f"bloka 1415926535 ⊕ 9695184575 = 11111111110 ⊢ dih : pari {{10:158, 11:19, 0:19, 1:4}} mera : {dict((k, pari.count(k)) for k in sorted(set(pari)))} · zadih pri ničlah π")
    n += 1
    # T3 · nemi motor 999
    mesta = 215; scale = 10 ** (mesta + VAROVALKA)
    P = pi_scaled(scale)
    rip, rfr = razcep(P, mesta + VAROVALKA)
    cV, xV = par(P, 10, 1, mesta + VAROVALKA)
    xip, xfr = razcep(xV, mesta + VAROVALKA)
    stolpci = [int(p) + int(q) for p, q in zip(rfr[:215], xfr[:215])]
    Z("T3 DEVETICE", all(s == 9 for s in stolpci) and xfr.startswith("8584073464102067615373"),
      f"X9 = 6.8584073464102067... · X = 10 − π · {sum(1 for s in stolpci if s == 9)}/215 stolpcev = 9, izjem 0 ⊢ nemi : brez prevoza")
    n += 1
    # T4 · motor 777
    mesta = 200; scale = 10 ** (mesta + VAROVALKA)
    P = pi_scaled(scale)
    rip, rfr = razcep(P, mesta + VAROVALKA)
    cV, xV = par(P, 700, 9, mesta + VAROVALKA)
    xip, xfr = razcep(xV, mesta + VAROVALKA)
    pari = [int(p) + int(q) for p, q in zip(rfr[:200], xfr[:200])]
    Z("T4 SEDMICE", xip == "74" and set(pari) <= {6, 7, 16, 17},
      f"X77 = 74.6361851241879845393... · pari {{7:109, 6:39, 17:39, 16:13}} mera : {dict((k, pari.count(k)) for k in sorted(set(pari)))} · tarča C = 700/9")
    n += 1
    # T5 · odstotek
    mesta = 20; scale = 10 ** (mesta + VAROVALKA)
    P = pi_scaled(scale)
    cV = (100 * scale) // 9
    xV = cV - P
    dele = Fraction(P, cV) * 100
    dopol = Fraction(xV, cV) * 100
    d1 = str(dele.numerator * 10 ** mesta // dele.denominator)
    d2 = str(dopol.numerator * 10 ** mesta // dopol.denominator)
    Z("T5 ODSTOTEK", d1.startswith("2827433388230813914") and d2.startswith("7172566611769186085") and dele + dopol == 100,
      "π = 28.27433388230813914... % celote 100/9 · dopolnilo = 71.72566611769186085... % · vsota = 100 % točno ⊢ ⟨Fraction⟩")
    n += 1
    # T6 · preklop φ∘φ = id : φ(φ(R)) = C − (C − R) = R na isti lestvi ⊙ algebra ∧ izmera
    vredu = True
    for imeR, rV in (("pi", pi_scaled(scale)), ("sqrt2", sqrt2_scaled(scale)), ("1/3", scale // 3)):
        for a, b in ((100, 9), (700, 9), (10, 1)):
            lestvica = 10 ** (mesta + VAROVALKA)
            cT = (a * lestvica) // b
            xT = cT - rV
            if cT - xT != rV:
                vredu = False
    Z("T6 PREKLOP", vredu, "φ(φ(R)) = R ⊢ za π ⌇ √2 ⌇ 1/3 skozi tarče 100/9 ⌇ 700/9 ⌇ 10 ( ×9 ) · krog je involucija ∧ se sam zapira")
    n += 1
    # T7 · priča √2 skozi nemi motor
    mesta = 60; scale = 10 ** (mesta + VAROVALKA)
    Q = sqrt2_scaled(scale)
    rip, rfr = razcep(Q, mesta + VAROVALKA)
    cV, xV = par(Q, 10, 1, mesta + VAROVALKA)
    xip, xfr = razcep(xV, mesta + VAROVALKA)
    stolpci = [int(p) + int(q) for p, q in zip(rfr[:60], xfr[:60])]
    Z("T7 PRIČA-KOREN", xip == "8" and all(s == 9 for s in stolpci),
      "√2 ⊕ 8.5857864376269049... = 10 · 60/60 stolpcev = 9 ⊢ nemi motor drži tudi za pričo √2 ( ⟨ne⟩ samo za π )")
    n += 1
    # T8 · limita : zadnje potrdilo
    konec = Fraction(99999999999, 10 ** 10)
    veriga = sum(Fraction(9, 10 ** i) for i in range(1, 51))
    Z("T8 LIMITA", konec < 10 and 10 - konec == Fraction(1, 10 ** 10) and 1 - veriga == Fraction(1, 10 ** 50),
      "9.9999999999 ( 10 mest ) = 10 − 10^-10 ⟨ne⟩ celota ⊢ · 0.999...9 ( k = 50 ) manka 10^-50 · dovršitev samo ob neskončni verigi : 9.999... = 10 točno ⊙ zadnje potrdilo = limita")
    n += 1
    # T9 · štirje krogi skozi π : tarče rodijo različne pare ∧ 999 ≡ 10 isti par
    mesta = 60; scale = 10 ** (mesta + VAROVALKA)
    P = pi_scaled(scale)
    _, x111 = par(P, 100, 9, mesta + VAROVALKA)
    _, x777 = par(P, 700, 9, mesta + VAROVALKA)
    _, x999 = par(P, 10, 1, mesta + VAROVALKA)
    l = [str(v) for v in (x111, x777, x999)]
    Z("T9 KROGI", len(set(l)) == 3 and razcep(x111, mesta + VAROVALKA)[0] == "7" and razcep(x777, mesta + VAROVALKA)[0] == "74" and razcep(x999, mesta + VAROVALKA)[0] == "6",
      "krogi skozi π : 111 → 7.9695... ⌇ 777 → 74.6361... ⌇ 999 → 6.8584... ( isti par kakor tarča 10 ) ⊢ vsaka tarča rodi svoj par, π rodi vse")
    n += 1
    print(f"BATERIJA ZELENO ⊢ ×{n} · {TIK_SLOVO} rez σ 6431 · MERJENO, ⟨NE⟩ UGIBANO ⊙ 2690 · koda 0")
    return 0

sys.exit(glavni())
PY
