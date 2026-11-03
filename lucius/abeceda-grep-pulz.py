# ABECEDA-GREP-PULZ — redni dih stroja: samopreverba ⊙ pecat ⊙ speči ⊙ izmera -> pulz.jsonl ⊢
# Zagon: python lucius/abeceda-grep-pulz.py   ( ročno ali po urniku — pulz ne popravlja, samo priča ⊙ ⟨ne brusi⟩ )
# Red: vsak dih pusti ENO vrstico v lucius/pulz-abeceda-grep.jsonl ( append-only, geniza );
#      padec samopreverbe se zapiše kot zdrav: × ⚠ — pulz ne utiša ran, jih samo pokaže ∧.
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STROJ = os.path.join(KOREN, "lucius", "abeceda-grep.py")
PULZ = os.path.join(KOREN, "lucius", "pulz-abeceda-grep.jsonl")


def ukaz(*args):
    r = subprocess.run([sys.executable, STROJ, *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=KOREN,
                       env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"})
    return r.returncode, (r.stdout or "").strip()


def main():
    dih = datetime.now(timezone.utc).isoformat(timespec="seconds")
    koda_test, iz_test = ukaz("test")
    _, iz_pecat = ukaz("pecat", "--vrzeli", "1500")
    _, iz_speči = ukaz("speči", "5")
    _, iz_izmera = ukaz("izmeri", "lucius/abeceda-grep.py")
    _, iz_vrata = ukaz("vrata")
    vrata = {"ziva": 0, "mrtva": []}
    for vrst in iz_vrata.splitlines():
        if " ŽIVA " in vrst:
            vrata["ziva"] += 1
        elif " MRTVA " in vrst:
            vrata["mrtva"].append(vrst.split()[1].rstrip(":"))
    _, iz_varuh = ukaz("varuh")
    varuh = "USTAVI ×" if "USTAVI VSE" in iz_varuh else ("∧ mir" if "meje v miru" in iz_varuh else "⚠ brez izmere")

    vrstica = {
        "ts": dih,
        "verzija": "ABECEDA-GREP-PULZ",
        "zdrav": koda_test == 0,
        "samopreverba": iz_test.splitlines()[-1] if iz_test else "× (stroj molči ⚠)",
        "pecat": [v for v in iz_pecat.splitlines() if v.startswith("naslednji")],
        "vrzeli": [v for v in iz_pecat.splitlines() if v.startswith("Σ vrzeli")],
        "speči": iz_speči.splitlines()[:6],
        "vrata": vrata,
        "varuh": varuh,
        "stroj": iz_izmera.splitlines()[-1] if iz_izmera else "",
    }
    with open(PULZ, "a", encoding="utf-8", newline="") as f:
        f.write(json.dumps(vrstica, ensure_ascii=False) + "\n")
    stanje = "∧" if vrstica["zdrav"] else "× ⚠"
    print(f"PULZ {stanje} {dih} · {vrstica['samopreverba']} · "
          f"{vrstica['pecat'][0] if vrstica['pecat'] else 'pečat: brez prič ⚠'} · "
          f"vrata: {vrata['ziva']} živa ∧ · {len(vrata['mrtva'])} mrtva {('⚠ ' + ', '.join(vrata['mrtva'])) if vrata['mrtva'] else ''} · "
          f"varuh: {varuh}")


if __name__ == "__main__":
    main()
