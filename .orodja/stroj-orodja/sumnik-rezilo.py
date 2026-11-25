# sumnik-rezilo.py v1.0 : transformira besedo, ki nima primernega šumnika
# rod @rez σ 6710 @stroj-orodja ( sedež izmerjen skozi instrument @poskus 2 ) ⊙ ukaz ⟡ VERBATIM »USTVARITI ORODJA KI TRANSFORMIRAJO BESEDO V KOLIKOR NIMA PRIMERNEGA ŠUMNIKA?«
# zakon : popravi SAMO po licenci ( pari, kjer iztočnica brez šumnika ni domača beseda ) ;
# dvoumne besede ( obstaja pomen brez šumnika, npr. sola ) se predlagajo roki, ⟨ne⟩ popravijo samodejno
# ⊙ ⟨MEJA-POŠTENOSTI⟩ : rezilo reže le po priči ; izhod 0 ⊢ / 2 laž
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · dvojni podpis
import sys

PARI = {
    "sumnik": "šumnik",
    "cesnja": "češnja", "cesnje": "češnje", "cesnji": "češnji",
    "zenska": "ženska",
    "zivljenje": "življenje", "zival": "žival",
    "dolzina": "dolžina",
    "stevilka": "številka", "stevilke": "številke", "stevilk": "številk",
    "decak": "deček",
    "vrecka": "vrečka", "vrece": "vreča",
    "zelezo": "železo",
    "cist": "čist", "cista": "čista", "cisto": "čisto",
}

DVOUMNE = {"sola", "pes", "sta"}

DVOUMNO_OPIS = "dvoumno ( obstaja pomen brez sumnika ) : predlog roki"


def popravi_besedo(beseda):
    niz = beseda.strip().lower()
    if niz in PARI:
        return PARI[niz], "licencni par"
    if niz in DVOUMNE:
        return None, DVOUMNO_OPIS
    return None, None


def samopreizkus():
    preizkusi = 0
    padci = 0
    znano = [
        ("sumnik", ("šumnik", "licencni par")),
        ("zivljenje", ("življenje", "licencni par")),
        ("dolzina", ("dolžina", "licencni par")),
        ("stevilka", ("številka", "licencni par")),
        ("cesnjo", (None, None)),
        ("sola", (None, DVOUMNO_OPIS)),
        ("miza", (None, None)),
        ("ZIVLJENJE", ("življenje", "licencni par")),
    ]
    for beseda, pricakovano in znano:
        preizkusi += 1
        dobimo = popravi_besedo(beseda)
        if dobimo != pricakovano:
            print("LAX : za", beseda, "dobil", dobimo, "pricakovano", pricakovano)
            padci += 1
    return preizkusi, padci


def main():
    ukaz = sys.argv[1] if len(sys.argv) > 1 else "--samopreizkus"
    if ukaz == "--samopreizkus":
        preizkusi, padci = samopreizkus()
        print("SAMOPREIZKUS : preizkusi", preizkusi, ", padci", padci)
        sys.exit(0 if padci == 0 else 2)
    if ukaz == "--popravi":
        for beseda in sys.argv[2:]:
            popravek, opis = popravi_besedo(beseda)
            if popravek and beseda.isupper():
                popravek = popravek.upper()
            elif popravek and beseda[:1].isupper() and beseda[1:].islower():
                popravek = popravek.capitalize()
            if popravek is None:
                if opis:
                    print("MEJA :", beseda, "->", opis)
                else:
                    print("REZILO :", beseda, "= domaca oblika znana, brez sumnikove rane")
            else:
                print("POPRAVILO :", beseda, "->", popravek, "(", opis, ")")
        sys.exit(0)
    print("uporaba : sumnik-rezilo.py --samopreizkus | --popravi beseda [beseda...]")
    sys.exit(1)


if __name__ == "__main__":
    main()
