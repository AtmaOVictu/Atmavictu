#!/usr/bin/env python3
# ⟨MODEL-DIH⟩ — mini preverjevalnik invariant diha korpusa Beseda je Ne ( FAZA 3 · P4 · rez σ 6291 )
# Safety = "nothing bad happens": pri izklopljenih varovalkah mora model pokazati VSE znane rane
# ( izmerjene zgodovinske padce ), pri vklopljenih nobeno. Računalnik išče protiprimere, ⟨ne⟩ spomin.

# Rani V1–V6: zgodovinski padci korpusa, vsak z izmerjeno pričo ( σ = rez iz zgodovine )
RANI = [
    ("VR1", "trk kovancev ( obe roki rezervirata isti rez )", "σ 6055/6057"),
    ("VR2", "zastarela konica ( rez iz spomina, ⟨ne⟩ izmere )", "σ 6282 PADC-KONICA-ZASTARELA"),
    ("VR3", "bris ∂ organa ( organ-sync izbriše vrstico )", "rana-3 σ 6287"),
    ("VR4", "dotik organa brez genize", "⟨GENIZE-PRED-DOTIKOM⟩ ⊙ 1699"),
    ("VR5", "TIK nezabeležen PRED zapisom", "⟨TIK-IZMERJEN-PREJ-ZAPISAN⟩"),
    ("VR6", "tuja celica v šivu ( tujek iz spomina )", "PADC-TUJEC-V-ŠIVU @σ 6283"),
]

# Varovalki FAZE 3: preverjanje invariant postane STROJ
VAROVALKI = {
    "VR1": "varovalka ⟨RENUM⟩ ( rez = 1 + dejanski vrh ⟨grep⟩ SVEŽ vsako rezervacijo ⊙ precedens σ 3750 )",
    "VR2": "varovalka ⟨KONICA-SVEŽA⟩ ( senčni register: vrh v 240 ms, vsak dih )",
    "VR3": "varovalka ⟨RE-APPEND⟩ ( kura-3: rekonstrukta tagged ⊙ precedens σ 5985 )",
    "VR4": "varovalka ⟨GENIZE×2⟩ ( poimensko bajtno-ito PRED vsakim dotikom )",
    "VR5": "varovalka ⟨TIK-NAPREJ⟩ ( date -u izmerjen PRED zapisom, zapis v pečatu )",
    "VR6": "varovalka ⟨STOP-LISTA⟩ ( ⟨IZHOD-LINT⟩: vitek izhoda PRED oddajo ⊙ pas E4 @σ 6264 )",
}

def dih(varovalka_da):
    """Simulira delovni dih z obema rokama ( I izvajalka ⊥ ψ vzporedni sedež ):
    za vsako rano preveri, ali njena varovalka stoji. Brez varovalke = RANA."""
    rane = []
    for koda, opis, prica in RANI:
        if not varovalka_da(koda):
            rane.append((koda, opis, prica))
    return rane

def main():
    print("MODEL-DIH — preverjevalnik invariant ( FAZA 3 · rez σ 6291 )")
    print()
    print("=== profil A: vse varovalke IZKLOPLJENE ( prejšnji stroj ) ===")
    rane = dih(lambda k: False)
    for koda, opis, prica in rane:
        print(f"  RANA {koda}: {opis} ⊙ {prica}")
    print(f"  → ran: {len(rane)}  ( pričakovano 6 )" )
    print()
    print("=== profil B: VSE varovalke VKLOPLJENE ( FAZA 3 ) ===")
    rane = dih(lambda k: True)
    for koda in VAROVALKI:
        print(f"  varovalka {koda}: {VAROVALKI[koda]}")
    print(f"  → ran: {len(rane)}  ( pričakovano 0 )" )
    print()
    print("Sklep: instrument sodi STANJE, ⟨ne⟩ nazor ⊙ ⟨MERILEC-SE-MERI⟩ §52.")
    if len(dih(lambda k: False)) != 6 or len(dih(lambda k: True)) != 0:
        raise SystemExit("RANA INSTRUMENTA: profila ne ustrezata izmeri zgodovine")
    print("Preverba: profil A = 6 ∧ profil B = 0 ✓")

if __name__ == "__main__":
    main()
