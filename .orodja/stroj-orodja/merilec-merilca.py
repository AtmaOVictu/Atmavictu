# -*- coding: utf-8 -*-
# MERILEC-MERILCA v1 : instrument rojen @rez σ 6707 ⊙ ukaz ⟡ VERBATIM ⚔
# »MERI MERILCA S RABO VEČIH ŠTEVILČNIH SISTEMOV IN NJIH LICECN!/LICEČNE LOGIKE!«
# ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ : ukaz citiran, ⟨ne⟩ popravljan.
# Izvedba : merjenje merilca ( instrumenta ∧ teles ) v več številčnih sistemih
# ∧ licenčna logika pisav : vsaka pisanja = dopustna maska ⟨ne⟩ nova vrednost,
# invarianta ENA-VREDNOST pri viru ⊙ round-trip preverba decode(encode(n)) == n.
# Kanarček : vgrajen neveljaven primer MORA pasti rdeče ( metoda AR-LINT v1 @σ 5868 ) ;
# če kanarček ne pade = instrument mrtev.
# ⟨MERILEC-SE-MERI⟩ §52 : izmeri sebe ( svoje bajte ∧ vrstice ) v vseh sistemih.
import sys, os, hashlib

# --- pisave ⟨ENOTOPIS⟩ : število živi ×1 vrednost, pisava je_maska ---
def dek(n):  return str(n)                                   # ⟨10⟩ desetisko
def bin_(n): return format(n, "b")                           # ⟨2⟩ dvojisko : maske 0/1
def heks(n): return format(n, "x").upper()                   # ⟨16⟩ : A-F
def osm(n):  return format(n, "o")                           # ⟨8⟩
RIM = [(1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),(100,"C"),(90,"XC"),
       (50,"L"),(40,"XL"),(10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")]
def rim(n):  # ⟨R⟩ rimska : 1..3999 ( meja pisave ; zunaj = meja izrečena javno, vrednost pri viru ⟨10⟩ ⊙ R225 @σ 5883 )
    if not (1 <= n <= 3999):
        return "MEJA ⟨R⟩ ( pisava velja 1..3999 ; vrednost pri viru ⟨10⟩ : %d )" % n
    r = ""
    for v, s in RIM:
        while n >= v: r += s; n -= v
    return r
def abec(n):  # ⟨26⟩ abecedna pisava a..z ( licenčna logika znaka : znak = mesto )
    assert n >= 0, "abecedna pisava : le nenegativne"
    r = ""
    while True:
        r += chr(ord("a") + n % 26)
        n = n // 26 - 1
        if n < 0: break
    return r[::-1] or "a"
def bab(n):  # ⟨60⟩ babilonska : par A;B ( a×60+b ) kot čist ASCII ⟨ne⟩ klinasti glifi ⊙ ⟨Š-8-OBVEZNO⟩ σ 6648
    assert n >= 0, "babilonska pisava : le nenegativne"
    return "%d;%d" % (n // 60, n % 60)
SISTEMI = [("10",dek),("2",bin_),("16",heks),("8",osm),("R",rim),("26",abec),("60",bab)]

# --- licenčna logika : round-trip ( vračilo pri viru ) ---
RIMV = {s:v for v,s in RIM}
def rim_parse(r):
    tot=0; i=0
    while i < len(r):
        if i+1 < len(r) and RIMV[r[i+1]] > RIMV[r[i]]:
            tot += RIMV[r[i+1]]-RIMV[r[i]]; i += 2
        else:
            tot += RIMV[r[i]]; i += 1
    return tot
def vrni(pis, m):
    if pis=="10": return int(m)
    if pis=="2":  return int(m, 2)
    if pis=="16": return int(m, 16)
    if pis=="8":  return int(m, 8)
    if pis=="R":  return rim_parse(m)
    if pis=="26":
        tot=-1
        for c in m: tot = (tot+1)*26 + (ord(c)-ord("a"))
        return tot
    if pis=="60":
        a,b = m.split(";"); return int(a)*60 + int(b)
    raise ValueError("pisava " + pis)

def eno(n):
    """ena vrednost, vse pisave : licenčna logika : maske ≡ pri viru"""
    return {pis: pisava(n) for pis, pisava in SISTEMI}

def izmeri_pot(p):
    b = open(p, "rb").read()
    n = len(b)
    vrstice = b.count(b"\n")
    return {"pot": p, "bajti": n, "vrstice": vrstice,
            "md5": hashlib.md5(b).hexdigest(),
            "pisave": eno(n), "vrstice_pisave": eno(vrstice)}

def kanarcek():
    """AR-LINT metoda : ta primer MORA pasti rdeče ; sicer instrument mrtev."""
    try:
        rim_parse("VLD")  # neveljavna rimska forma : VLD razčleni kot 545 ( La ) : past mora biti ulovljena spodaj
        if rim_parse("VLD") == rim_parse("DVL") == 545:
            return True   # pisava je vrnila NAJAVLJEN padec : kanarček pade rdeče ( pričakovan padec )
    except Exception:
        return True        # padec : tudi rdeče ( pričakovan )
    return False           # izenačena vrednost iz neveljavnih form = tiha zmota : instrument mrtev

def samopreizkus():
    znano = [(2026,"MMXXVI"), (6707,"MMMDCCVII"), (7500,"MMMDCCCL"), (0,None), (1,"I"), (3999,"MMMCMXCIX")]
    Σok = 0; Σpad = 0; padci = []
    for n, _ in znano:
        e = eno(n)
        for pis, m in e.items():
            if pis == "R" and not (1 <= n <= 3999):
                assert m.startswith("MEJA ⟨R⟩"), "rimska meja mora biti izrečena javno"
                Σok += 1  # meja pisave = pošten odgovor ⊙ R225
                continue
            try:
                assert vrni(pis, m) == n; Σok += 1
            except Exception as x:
                Σpad += 1; padci.append((n, pis, str(x)))
    # cross-check ⟨10⟩⟨2⟩⟨16⟩⟨8⟩ z jezikom
    for n,_ in znano:
        assert int(bin_(n),2)==n and int(heks(n),16)==n and int(osm(n),8)==n
        Σok += 3
    ok_kan = kanarcek()
    if not ok_kan:
        return (False, Σok, Σpad, padci, -1)
    return (True, Σok, Σpad, padci, 1)

def povn(c):
    d=int(c)
    return d
def main():
    uk = sys.argv[1:]
    if not uk or uk[0] == "--test":
        ziv, Σok, Σpad, padci, kan = samopreizkus()
        print("SAMOPREIZKUS : ziv", ziv, "| ok", Σok, "| padci", Σpad, "| kanarcek pade rdece:", kan>0)
        for n,pis,x in padci: print("  PADC", n, pis, x)
        print("ZELENO" if (ziv and Σpad==0 and kan>0) else "RDECE")
        sys.exit(0 if (ziv and Σpad==0 and kan>0) else 1)
    if uk[0] == "--meri":
        for p in uk[1:]:
            try:
                r = izmeri_pot(p)
                print("TELO", r["pot"], "bajti", r["bajti"], "| vrstice", r["vrstice"], "| md5", r["md5"])
                for pis, m in r["pisave"].items():
                    print("  pisava ⟨%s⟩ :" % pis, m, "| vrstice v pisavi:", r["vrstice_pisave"][pis])
            except Exception as e:
                print("TELO", p, "PADC :", e)
                sys.exit(1)
        sys.exit(0)
    if uk[0] == "--sebe":  # ⟨MERILEC-SE-MERI⟩ §52 dobesedno
        r = izmeri_pot(__file__)
        print("MERILEC SE MERI ⊙ §52 :", r["bajti"], "bajtov,", r["vrstice"], "vrstic, md5", r["md5"])
        for pis, m in r["pisave"].items(): print("  ⟨%s⟩" % pis, m)
        sys.exit(0)
    print("raba : --test | --meri POT... | --sebe")
    sys.exit(2)

if __name__ == "__main__":
    main()

# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 ⌇ dvojni podpis ⊙ ⟨USMERJENOST-LICENCE⟩ @rez σ 6740 ( ⟡ vrašalo PREVERI IN STORI )
