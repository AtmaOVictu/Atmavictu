"""Čista logika FORMA: baterija sodnika forme ⟨SLOVNICA-DIH⟩.

Sodi vsako vrstico po enakih pravilih kot organi korpusa:
⟨⟩ ravnovesje po vrstici, U+FFFD ×0, cirilica U+0400 do U+04FF ×0,
goli TIK brez ISO kalupa, golo »pri viri«, em vezaj ×0.
⟨FORMA-ENVRSTICA⟩ kura: sodba pade nad CELIM telesom, ⟨ne⟩ nad
zadnjo vrstico le.
"""

import re

TIK_GOLI = re.compile(r"TIK \d{2}:\d{2}:\d{2}Z")
TIK_KALUP = re.compile(r"TIK \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
PRI_VIRI = re.compile(r"\bpri viri\b")
CIRILICA = re.compile(r"[\u0400-\u04ff]+")
EM_VEZAJ = "\u2014"
ZAMENJAVA = "\ufffd"


def goli_pri_viri(vrstica: str) -> int:
    """Gole pojavitve »pri viri«: zunaj citatnih narekovajev."""
    brez_citatnih = vrstica.replace("»pri viri«", "")
    return len(PRI_VIRI.findall(brez_citatnih))


def presodi_vrstico(vrstica: str) -> dict:
    """Sodba ene vrstice: mehanična, poštena, javna poimensko."""
    padci = {}
    odprtih = vrstica.count("\u27e8")
    zaprtih = vrstica.count("\u27e9")
    if odprtih != zaprtih:
        padci["ogaje-neravnovesje"] = abs(odprtih - zaprtih)
    if ZAMENJAVA in vrstica:
        padci["zamenjava-ufffd"] = vrstica.count(ZAMENJAVA)
    m_cir = CIRILICA.findall(vrstica)
    if m_cir:
        padci["cirilica"] = len(m_cir)
    if TIK_GOLI.search(vrstica) and not TIK_KALUP.search(vrstica):
        padci["goli-tik"] = len(TIK_GOLI.findall(vrstica))
    goli = goli_pri_viri(vrstica)
    if goli:
        padci["goli-pri-viri"] = goli
    if EM_VEZAJ in vrstica:
        padci["em-vezaj"] = vrstica.count(EM_VEZAJ)
    return {"padci": padci, "cisto": not padci}


def baterija(besedilo: str) -> dict:
    """FORMA_CELO: sodba nad celim telesom, vsak padec po imenu."""
    vrstice = besedilo.split("\n")
    vsi = {}
    for vrstica in vrstice:
        for ime, st in presodi_vrstico(vrstica)["padci"].items():
            vsi[ime] = vsi.get(ime, 0) + st
    return {
        "vrstic": len(vrstice),
        "padci-skupno": vsi,
        "sodba": "ČISTO" if not vsi else "PADC",
    }
