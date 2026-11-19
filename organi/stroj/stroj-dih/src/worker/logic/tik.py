"""Čista logika TIK: kanonska ura korpusa (⟨TIK-IZMERJEN-PREJ-ZAPISAN⟩).

Vstop: UTC trenutek. Izhod: niz kalupa
»TIK 2026-11-19T10:18:53Z UTC ⇌ 11:18:53 CET Ljubljana«
po ⟨URA-NA-KONCU⟩ 3046 ∧ ⟨SPLOŠNO-RAZUMLJIVA-URA⟩ 3083.
Zakon organa ⟨ZADNJA-URA-PREVERBA⟩ @σ 3961: CET = UTC+1 vedno.
"""

from datetime import datetime, timedelta, timezone

DNEVI = (
    "ponedeljek", "torek", "sreda", "četrtek", "petek", "sobota", "nedelja",
)

MESECI = (
    "januar", "februar", "marec", "april", "maj", "junij",
    "julij", "avgust", "september", "oktober", "november", "december",
)


def izmeri_tik(dt_utc: datetime) -> dict:
    """Izmeri kanonski TIK iz UTC trenutka (vedno prej, ne ocenjen)."""
    if dt_utc.tzinfo is None:
        dt_utc = dt_utc.replace(tzinfo=timezone.utc)
    dt_utc = dt_utc.astimezone(timezone.utc)

    dt_cet = dt_utc + timedelta(hours=1)

    iso_utc = dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    ura_cet = dt_cet.strftime("%H:%M:%S")
    niz = "TIK {} UTC ⇌ {} CET Ljubljana".format(iso_utc, ura_cet)
    datum_cet = "{}. {}. {}".format(dt_cet.day, dt_cet.month, dt_cet.year)

    return {
        "tik_utc": iso_utc,
        "ura_cet": ura_cet,
        "cet_iz_utc": "UTC+1",
        "datum_cet": datum_cet,
        "dan_cet": DNEVI[dt_cet.weekday()],
        "mesec_cet": MESECI[dt_cet.month - 1],
        "niz": niz,
    }


def tik_iz_niza(iso_utc: str) -> dict:
    """TIK iz množično podanega ISO niza (npr. »2026-11-19T10:18:53Z«)."""
    dt = datetime.strptime(iso_utc.split(".")[0].rstrip("Z"), "%Y-%m-%dT%H:%M:%S")
    dt = dt.replace(tzinfo=timezone.utc)
    return izmeri_tik(dt)
