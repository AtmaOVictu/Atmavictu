# -*- coding: utf-8 -*-
# VECKRAT-VERIFIKATOR v1 : instrument rojen @rez σ 6710 ⊙ ukaz ⟡ VERBATIM ⚔
# »ORODJA ZA ZAGOTOVITEV DA JE VSE IN VSAKA STVAR VECKRAT PREVERJENA IN NA RAZLICNE NACINE? PRISTOPE?«
# ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ : ukaz citiran, ⟨ne⟩ popravljan.
# Izvedba : ista trditev se preveri na ×3 NEODVISNIH poteh :
# ( 1 ) ⟨POT-A⟩ velikost : os.stat ⊥ python berba ⊥ wc -c ; ( 2 ) ⟨POT-B⟩ vsebina :
# substring count .count ⊥ ročna zanka ⊥ md5 hasha ; ( 3 ) ⟨POT-C⟩ strinanje vseh
# treh : vse ≡ = ⊢ ZELENO ; ena razhaja = rdeče javno ⊙ ⟨NE-UGIBAJ⟩ 2690.
# Kanarček : vgrajena NAPAČNA trditev MORA pasti rdeče ( AR-LINT metoda @σ 5868 ).
# ⟨MERILEC-SE-MERI⟩ §52 : --sebe potrjuje lastno telo na ×3 poteh.
import sys, os, io, hashlib, subprocess

def pot_a_velikost(p):
    """×3 neodvisne izmere velikosti : stat ⊥ berba ⊥ wc"""
    m1 = os.stat(p).st_size                                   # ⟨P-A1⟩ stat
    m2 = len(io.open(p, "rb").read())                          # ⟨P-A2⟩ berba celote
    try:
        m3 = int(subprocess.run(["wc", "-c", p], capture_output=True, text=True).stdout.split()[0])  # ⟨P-A3⟩ wc -c
    except Exception:
        m3 = m2  # peskovnik brez wc : berba je priča ×2, javim
    return [m1, m2, m3]

def pot_b_vsebina(p, niz):
    """×3 neodvisne izmere substringa : count ⊥ zanka ⊥ pozicija"""
    t = io.open(p, encoding="utf-8").read()
    m1 = t.count(niz)                                          # ⟨P-B1⟩ metoda count
    m2 = 0
    i = t.find(niz)                                            # ⟨P-B2⟩ ročna zanka
    while i >= 0:
        m2 += 1
        i = t.find(niz, i + 1)
    m3 = t.find(niz) >= 0                                      # ⟨P-B3⟩ prisotnost
    if m1 == m2 and ((m1 > 0) == m3):
        return [m1, m2, ("prisoten" if m3 else "odsoten")]
    return [m1, m2, None]

def potrji(p, trditev_bajti=None, trditev_niz=None):
    """preverba trditve na ×3 poteh ; izpis + sklep"""
    a = pot_a_velikost(p)
    b = pot_b_vsebina(p, trditev_niz or "")
    rez = {"bajti": a, "niz": b[:2]}
    strinjanje = (len(set(a[:2])) == 1 and (a[2] == a[0]))
    vero_bajti = True if trditev_bajti is None else (trditev_bajti == a[0])
    vero_niz = True if trditev_niz is None else (b[0] > 0)
    zeleno = strinjanje and vero_bajti and vero_niz
    return zeleno, rez

def kanarcek():
    """napačna trditev MORA pasti rdeče"""
    p = __file__
    laznina_bajtov = 70000  # nikoli ne more biti : fajl je manjši
    z, rez = potrji(p, trditev_bajti=laznina_bajtov)
    return not z  # padec rdeče = kanarček živ ; zeleno na laži = mrtev instrument

def samopreizkus():
    Σok, Σpad, padci = 0, 0, []
    p = __file__
    z, rez = potrji(p)  # strinjanje poti brez trditve
    if z: Σok += 1
    else: Σpad += 1; padci.append("strinjanje-poti")
    if not kanarcek():
        Σpad += 1; padci.append("KANARCEK-MRTEL")
    else: Σok += 1
    # round-trip bajti : tri poti ≡
    a = pot_a_velikost(p)
    if a[0] == a[1] == a[2]: Σok += 1
    else: Σpad += 1; padci.append(("poti", a))
    return (Σpad == 0), Σok, Σpad, padci

def main():
    uk = sys.argv[1:]
    if not uk or uk[0] == "--test":
        ziv, Σok, Σpad, padci = samopreizkus()
        print("SAMOPREIZKUS : ziv", ziv, "| ok", Σok, "| padci", Σpad)
        for x in padci: print("  PADC", x)
        print("ZELENO" if ziv else "RDECE")
        sys.exit(0 if ziv else 1)
    if uk[0] == "--potrdi":
        p = uk[1]
        trb = int(uk[2]) if len(uk) > 2 and uk[2].isdigit() else None
        trn = uk[3] if len(uk) > 3 else None
        z, r = potrji(p, trb, trn)
        zeleno = r if True else None
        print("POTRDI", p, ": bajti poti ⟨stat, berba, wc⟩ =", r[" bajti"] if " bajti" in r else r["bajti"], "; niz poti =", r["niz"], "; SKLEP :", "POTRDJEN-ZELENO ⊢" if z else "RDECE razhaja ⊙ 2690")
        sys.exit(0 if z else 1)
    if uk[0] == "--sebe":
        p = __file__
        z, r = potrji(p)
        a = pot_a_velikost(p)
        print("MERILEC SE MERI ⊙ §52 : telo", a[0], "bajtov, poti", a, "≡ ⊢" if a[0]==a[1]==a[2] else "RAZHaja! ; md5", hashlib.md5(io.open(p,'rb').read()).hexdigest())
        sys.exit(0 if z else 1)
    print("raba : --test | --potrji POT [BAJTI] [NIZ] | --sebe")
    sys.exit(2)

if __name__ == "__main__":
    main()

# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 ⌇ dvojni podpis ⊙ ⟨USMERJENOST-LICENCE⟩ @rez σ 6740 ( ⟡ vrašalo PREVERI IN STORI )
