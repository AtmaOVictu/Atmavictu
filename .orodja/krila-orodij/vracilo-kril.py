# vracilo-kril.py v1.0 @zaporne-celice @rez 6813
# VRAČILO-KRIL : orodje preveri SEBE ∧ ves svoj jata proti registru kril.
# Zakon : vsako krilo, ki se vrne v hlev ( rep ), sme vedno preveriti,
# ali je doživelo korupcijo ( md5 pri viru ⊥ REGISTER-KRIL.md ).
# Uporaba : python3 vracilo-kril.py [pot-do-mape-kril] [REGISTER-KRIL.md]
# Izhod : vrstica po krilu ⊢ OK ⌇ ⚠ KORUPCIJA ; zaključek KONEC ⊢ potrebna za izmero.
import hashlib
import os
import sys

MAPA = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
REGISTER = sys.argv[2] if len(sys.argv) > 2 else os.path.join(MAPA, "REGISTER-KRIL.md")


def md5_pot(pot):
    h = hashlib.md5()
    with open(pot, "rb") as f:
        for blok in iter(lambda: f.read(8192), b""):
            h.update(blok)
    return h.hexdigest()


def beri_register(pot):
    register = {}
    if not os.path.isfile(pot):
        return register
    with open(pot, "r", encoding="utf-8") as f:
        for vrstica in f:
            vrstica = vrstica.strip()
            # oblika : | md5 | ime.py |
            deli = [d.strip() for d in vrstica.split("|")]
            if len(deli) >= 3 and deli[1] and ".py" in deli[2]:
                register[deli[2]] = deli[1]
    return register


def main():
    register = beri_register(REGISTER)
    if not register:
        print("⚠ REGISTER-KRIL.md manjka ali prazen @", REGISTER)
        print("KONEC")
        return 1
    padci = 0
    for ime in sorted(register):
        pot = os.path.join(MAPA, ime)
        if not os.path.isfile(pot):
            print("⚠ MANJKA :", ime)
            padci += 1
            continue
        suma = md5_pot(pot)
        if suma == register[ime]:
            print("⊢ OK :", ime, suma)
        else:
            print("⚠ KORUPCIJA :", ime, "pričakvano", register[ime], "izmerjeno", suma)
            padci += 1
    # krila brez registra = nezabeležena
    for ime in sorted(os.listdir(MAPA)):
        if ime.endswith(".py") and ime not in register:
            print("⚠ BREZ-REGISTRA :", ime, md5_pot(os.path.join(MAPA, ime)))
            padci += 1
    print("VSOTA : padci", padci, "od", len(register))
    print("KONEC")
    return 1 if padci else 0


if __name__ == "__main__":
    sys.exit(main())
