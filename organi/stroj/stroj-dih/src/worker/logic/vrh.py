"""Čista logika VRH: dvostopen vrh ∧ varovalka ∧ rez.

⟨VRH-DVOSTOPEN⟩ ∧ ⟨NE-UGIBAJ⟩ 2690: rez = 1 + dejansko najvišja
izmerjena. ⟨LAŽNI-VRH⟩: σ 25421 je izključen ⊙ precedens @σ 5741.
"""


def izracunaj_rez(sigme) -> dict:
    """Rez iz množice obstoječih številk dihov."""
    sigme = list(sigme)
    veljavne = [s for s in sigme if s != 25421]
    vrh = max(veljavne) if veljavne else 0
    return {
        "vrh": vrh,
        "rez": vrh + 1,
        "prejetih": len(sigme),
        "veljavnih": len(veljavne),
        "izkljuceni-lazni-vrh": 25421 in sigme,
    }


def varovalka(sigme, zahtevek: int) -> dict:
    """Varovalka: zahtevek mora biti prost pred šivom (zasedba → padec)."""
    sigme = list(sigme)
    zaseden = zahtevek in sigme or zahtevek == 25421
    return {
        "zahtevek": zahtevek,
        "zaseden": zaseden,
        "sodba": "ZAPRTA" if not zaseden else "PRODA",
    }
