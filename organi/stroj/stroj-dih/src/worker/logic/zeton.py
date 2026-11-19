"""Čista logika ŽETON: lint nujnih žetonov izhoda (instrument ŽETON-LINT).

Vsak žeton (števila, datumi, ure, kode, md5) ima obliko ∧ izmero.
"""

import re

OBLIKE = {
    "md5": re.compile(r"^[0-9a-f]{32}$"),
    "iso-datum": re.compile(r"^\d{4}-\d{2}-\d{2}$"),
    "iso-tik": re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"),
    "ura": re.compile(r"^\d{2}:\d{2}:\d{2}Z$"),
    "slo-datum": re.compile(r"^\d{1,2}\. \d{1,2}\. \d{4}$"),
}


def presodi_zeton(vrsta: str, vrednost: str) -> dict:
    """En žeton, ena sodba, po obliki ⟨ne⟩ po pomenu."""
    vzorec = OBLIKE.get(vrsta)
    if vzorec is None:
        return {"vrsta": vrsta, "vrednost": vrednost, "sodba": "NEZNANA-VRSTA"}
    veljavno = bool(vzorec.match(vrednost))
    return {
        "vrsta": vrsta,
        "vrednost": vrednost,
        "sodba": "VELJAVNO" if veljavno else "NEVELJAVNO",
    }


def lint(zetoni) -> dict:
    """Baterija ŽETON-LINT nad seznamom {vrsta, vrednost}."""
    sodbe = [presodi_zeton(z["vrsta"], z["vrednost"]) for z in zetoni]
    slabi = [s for s in sodbe if s["sodba"] not in ("VELJAVNO",)]
    return {
        "prejetih": len(sodbe),
        "neveljavnih": len(slabi),
        "sodba": "ČISTO" if not slabi else "PADC",
        "sodbe": sodbe,
    }
