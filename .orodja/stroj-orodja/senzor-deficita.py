#!/usr/bin/env python3
# SENZOR-DEFICITA v1.2 — rez σ 6729 ( dopolnitev nad σ 6724 ), 23. 11. 2026 ⊙ ukaz ⟡ VERBATIM
# »PREVERJANJE SLOVNICE KI JE DOBESEDNA IN PREVERJANJE SLOVNICE KI TI JO JAZ POŠILJAM
#  JE TUDI VEČ KOT OBVEZNA! KAKOR ČLOVEK SE TUDI JAZ OBČASNO ZMOTIM!« ( ⟡, nedotakljivo ⚔ )
# v1.0 @σ 6724 : meri deficit besedila proti leksikonu korpusa ( gajica )
# v1.1 @σ 6724 : tarča se IZKLJUČI iz sejanja ( PADC-CIRKULARNOST ulov MERILEC-KRITIK )
# v1.2 @σ 6729 : deficit razcepi na TIPKO ⊥ NOVO BESEDO ( dobesedna preverba :
#               razdalja do najbližje leksikonske besede ≤ 2 = domneza tipke pri viru )
# Raba : python3 senzor-deficita.py <datoteka> [--semeni]
# Stdlib only ⊙ precedent FRACTAL_SYSTEM ⟨BREZ ZUNANJIH ODVISNOSTI⟩
import io, os, re, sys, collections

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEKSIKON_POT = os.path.join(KOREN, "stroj-orodja", ".geniza", "leksikon-gajice.txt")
BESEDA_RX = re.compile(r"[a-zčšžđć]+", re.IGNORECASE)

def leksikon_novo(tarča=None):
    besede = set()
    for ime in sorted(os.listdir(KOREN)):
        p = os.path.join(KOREN, ime, "KNOWLEDGE.md")
        if os.path.isfile(p) and os.path.abspath(p) != (os.path.abspath(tarča) if tarča else ""):
            try:
                t = io.open(p, encoding="utf-8").read().lower()
            except Exception:
                continue
            besede.update(w.lower() for w in BESEDA_RX.findall(t))
    os.makedirs(os.path.dirname(LEKSIKON_POT), exist_ok=True)
    with io.open(LEKSIKON_POT, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(besede)))
    return besede

def leksikon_beri():
    if os.path.isfile(LEKSIKON_POT):
        with io.open(LEKSIKON_POT, encoding="utf-8") as f:
            return set(w.strip() for w in f if w.strip())
    return leksikon_novo()

def razdalja(a, b, meja=2):
    if abs(len(a) - len(b)) > meja:
        return meja + 1
    if len(a) < len(b):
        a, b = b, a
    prej = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        zdaj = [i]
        for j, cb in enumerate(b, 1):
            zdaj.append(min(prej[j] + 1, zdaj[j - 1] + 1, prej[j - 1] + (ca != cb)))
        if min(zdaj) > meja:
            return meja + 1
        prej = zdaj
    return prej[-1]

def meri(besedilo, leksikon):
    vse = [w.lower() for w in BESEDA_RX.findall(besedilo)]
    vsota = len(vse)
    unikatne = collections.Counter(w for w in vse if len(w) >= 3)
    deficit = {w: n for w, n in unikatne.items() if w not in leksikon}
    return vsota, unikatne, deficit

def main():
    args = sys.argv[1:]
    if not args:
        print("raba: senzor-deficita.py <datoteka> [--semeni]"); return 2
    pot = args[0]
    leksikon = leksikon_novo(pot) if "--semeni" in args else leksikon_beri()
    t = io.open(pot, encoding="utf-8").read()
    vsota, unikatne, deficit = meri(t, leksikon)
    p = [
        "SENZOR-DEFICITA v1.2 @rez σ 6729 ⊙ ukaz ⟡ »slovnica dobesedna + slovnica njegove pošte = več kot obvezna«",
        "leksikon gajice : %d besed" % len(leksikon),
        "besedilo : %s" % pot,
        "žetoni : %d | unikatne ( dolžina >= 3 ) : %d" % (vsota, len(unikatne)),
        "DEFICIT : %d" % len(deficit),
    ]
    tipke, nove = [], []
    for w in sorted(deficit, key=lambda x: (-deficit[x], x)):
        blizu = []
        for b in leksikon:
            if abs(len(b) - len(w)) <= 2 and b[0] == w[0] and razdalja(w, b) <= 2:
                blizu.append(b)
                if len(blizu) >= 5:
                    break
        vrst = "  %4d x  %s  =>  " % (deficit[w], w)
        if blizu:
            tipke.append(w)
            vrst += "TIPKA? ( dobesedno blizu : %s ) — beseda ⟡ nedotakljiva, poročana, ne popravana" % ", ".join(sorted(blizu)[:3])
        else:
            nove.append(w)
            vrst += "NOVA BESEDA? — registracija kovanca ⭢ priča pri viru"
        p.append(vrst)
    p.append("razcep : tipka-kandidatov %d | novobesednih-kandidatov %d" % (len(tipke), len(nove)))
    p.append("MERJENO, ⟨NE⟩ UGIBANO ⊙ 2690 · vsak deficit zahteva svojo optimalno rehabilitacijo ⊙ ⟡ 23. 11. 2026")
    print("\n".join(p))
    return 0

if __name__ == "__main__":
    sys.exit(main())

# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 ⌇ dvojni podpis ⊙ ⟨USMERJENOST-LICENCE⟩ @rez σ 6740 ( ⟡ vrašalo PREVERI IN STORI )
