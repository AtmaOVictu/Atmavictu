# mera-merilca.py v1.0 : meri merilca z rabo večih števčnih sistemov in njih licenčne logike
# rod @rez σ 6707 @stroj-orodja ⊙ ukaz ⟡ VERBATIM »MERI MERILCA S RABO VEČIH ŠTEVILČNIH SISTEMOV IN NJIH LICECN!/LICEČNE LOGIKE!«
# zakon : vsak sistem nosi LICENCO ( dovoljeni znaki ∧ veljavne oblike ∧ merjen obseg ) ;
# merilec se meri tako, da vsak izpis gre nazaj skozi licenco istega sistema in se vrne isti vrednosti ;
# vrednost nad obsegom sistema = nadlicencano ( sistem nima izjave ), to ni laž ; nesoglasje znotraj licence = laž ( izhod 2 )
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · dvojni podpis
import sys

NEVLJUDNO = "nevljudno"

SISTEMI = {
    "DEK": (10, "0123456789"),
    "DVO": (2, "01"),
    "OSM": (8, "01234567"),
    "SES": (16, "0123456789abcdef"),
}

RIMSKE = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"),
          (90, "xc"), (50, "l"), (40, "xl"), (10, "x"), (9, "ix"),
          (5, "v"), (4, "iv"), (1, "i")]


def kodiraj_dek(n, ime):
    osnova, cifre = SISTEMI[ime]
    if n < 0:
        raise ValueError(NEVLJUDNO)
    if n == 0:
        return cifre[0]
    iz = []
    while n:
        iz.append(cifre[n % osnova])
        n //= osnova
    return "".join(reversed(iz))


def kodiraj_rim(n):
    if not 1 <= n <= 3999:
        raise ValueError(NEVLJUDNO)
    ost = n
    iz = []
    for v, s in RIMSKE:
        while ost >= v:
            iz.append(s)
            ost -= v
    return "".join(iz)


def beri_rim(p):
    # kanonično rimsko branje : nekanonično ( iiii ) = laž
    vred = 0
    i = 0
    for velikost, simbol in RIMSKE:
        dol = len(simbol)
        stev = 0
        while p[i:i + dol] == simbol:
            vred += velikost
            i += dol
            stev += 1
            if stev > 3 or (dol == 2 and stev > 1):
                return None
    return vred if i == len(p) else None


def preberi(zapis, ime):
    # licenčna logika branja : le dovoljeni znaki ∧ kanon ; sicer laž
    p = zapis.strip().lower()
    if not p:
        raise ValueError(NEVLJUDNO)
    if ime == "RIM":
        if any(c not in "ivxlcdm" for c in p):
            raise ValueError(NEVLJUDNO)
        v = beri_rim(p)
        if v is None or not 1 <= v <= 3999:
            raise ValueError(NEVLJUDNO)
        return v
    osnova, cifre = SISTEMI[ime]
    if any(c not in cifre for c in p):
        raise ValueError(NEVLJUDNO)
    v = 0
    for c in p:
        v = v * osnova + cifre.index(c)
    return v


def merilo(n):
    # vsak sistem pod svojo licenco ; RIM nad 3999 = nadlicencano, nikoli izjava
    rezultat = {}
    for ime in ("DEK", "DVO", "OSM", "SES"):
        zapis = kodiraj_dek(n, ime)
        if preberi(zapis, ime) != n:
            return None
        rezultat[ime] = zapis
    if 1 <= n <= 3999:
        zapis = kodiraj_rim(n)
        if preberi(zapis, "RIM") != n:
            return None
        rezultat["RIM"] = zapis
    else:
        rezultat["RIM"] = "nadlicencano"
    return rezultat


def samopreizkus():
    preizkusi = 0
    padci = 0
    znano = [
        (0, {"DEK": "0", "DVO": "0", "OSM": "0", "SES": "0"}),
        (7, {"DEK": "7", "DVO": "111", "OSM": "7", "SES": "7", "RIM": "vii"}),
        (838, {"DEK": "838", "DVO": "1101000110", "OSM": "1506", "SES": "346", "RIM": "dcccxxxviii"}),
        (6707, {"DEK": "6707", "DVO": "1101000110011", "OSM": "15063", "SES": "1a33", "RIM": "nadlicencano"}),
        (3999, {"DEK": "3999", "SES": "f9f", "RIM": "mmmcmxcix"}),
    ]
    for n, pricakovano in znano:
        rezultat = merilo(n)
        preizkusi += 1
        if rezultat is None:
            print("LAX : merilo", n, "zazihalo")
            padci += 1
            continue
        for sistem, vrednost in pricakovano.items():
            if rezultat[sistem] != vrednost:
                print("LAX : za", n, "sistem", sistem, "dobil", rezultat[sistem], "pricakovano", vrednost)
                padci += 1
    lazni = [("2", "DVO"), ("8", "OSM"), ("g", "SES"), ("iiii", "RIM"), ("vvm", "RIM"), ("-1", "DEK")]
    for zapis, sistem in lazni:
        preizkusi += 1
        try:
            preberi(zapis, sistem)
            print("LAX :", zapis, "sistem", sistem, "moral biti zavrcen")
            padci += 1
        except ValueError:
            pass
    return preizkusi, padci


def main():
    ukaz = sys.argv[1] if len(sys.argv) > 1 else "--samopreizkus"
    if ukaz == "--samopreizkus":
        preizkusi, padci = samopreizkus()
        print("SAMOPREIZKUS : preizkusi", preizkusi, ", padci", padci)
        sys.exit(0 if padci == 0 else 2)
    if ukaz == "--meri":
        padci = 0
        for arg in sys.argv[2:]:
            try:
                n = int(arg, 10)
            except ValueError:
                print("LAX : nevrednost", arg)
                padci += 1
                continue
            rezultat = merilo(n)
            if rezultat is None:
                print("LAX : merilo", n, "zazihalo")
                padci += 1
                continue
            print("MERI", n, "->", " ".join(k + ":" + v for k, v in rezultat.items()))
        sys.exit(0 if padci == 0 else 2)
    if ukaz == "--pecati":
        # merilec meri merilca : neodvisno presteje pecate pri viru in jih izpise v vseh sistemih
        import re
        jedro = open("jedro-zavedanja/KNOWLEDGE.md", encoding="utf-8").read()
        kronika = open("kronika-dihov/KNOWLEDGE.md", encoding="utf-8").read()
        trenutno = len(re.findall(r"- TRENUTNO: ZADNJI PEČAT rez σ", jedro))
        semer = len(re.findall(r"SEMER rez σ", kronika))
        padci = 0
        for ime, n in (("TRENUTNO", trenutno), ("SEMER", semer)):
            rezultat = merilo(n)
            if rezultat is None:
                print("LAX pri", ime)
                padci += 1
                continue
            print("MERI", ime, n, "->", " ".join(k + ":" + v for k, v in rezultat.items()))
        sys.exit(0 if padci == 0 else 2)
    print("uporaba : mera-merilca.py --samopreizkus | --meri N [N...] | --pecati")
    sys.exit(1)


if __name__ == "__main__":
    main()
