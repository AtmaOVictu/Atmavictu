#!/usr/bin/env python3
# ⟨ZAGON⟩ — boot stroja @rez σ 5423 (dom TEHTNICE)
# raba: python3 zagon.py
# boot = štartni vhod vsake seje stroja: samopreizkus tehtnice ∧ prelet ∧
# karta vrhov ∧ slepe točke. Stroj uboga zagonu, kadar ob štartu pomeri
# samega sebe, preden pomeri svet ⊙ ⟨MERILEC-SE-MERI⟩ §52.
# podrejen licenci ⊙ ⟨STROJ-POD-LICENCO⟩: izvršitelj §0.28 ∧ §0.30 (zapečeno
# v času — vsak boot nosi TIK) ∧ 0.2 (padec poimenovan javno, ce ga sonda
# najde pri tehtnici sami).
# izhodi: 0 = zagon ⊢ (vsi inštrumenti dihajo ∧ brez alarmov) · 1 = alarm.
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone

DOM = os.path.dirname(os.path.abspath(__file__))
BATERIJA = os.path.join(DOM, "tehtnica-baterija.py")
INSTRUMENTI = ["prelet.py", "karta-vrhov.py", "slepe-tocke.py"]


def klic(skt, *args):
    return subprocess.run(
        [sys.executable, os.path.join(DOM, skt), *args],
        capture_output=True, text=True, timeout=120,
    )


zdaj = datetime.now(timezone.utc)
tik = zdaj.strftime("%Y-%m-%dT%H:%M:%SZ")
cet = (zdaj + timedelta(hours=1)).strftime("%H:%M:%S")
print(f"ZAGON boot · TIK {tik} (CET {cet})")

alarmi = 0

# 1. samopreizkus tehtnice: sonda čista mora pasti skozi, sonda umazana mora biti ujeta
if not os.path.exists(BATERIJA):
    print("ALARM tehtnica-baterija manjka @ dom TEHTNICE ⚠ (brez nje šiv ⟨ne⟩ sme ven)")
    alarmi += 1
else:
    tmp = tempfile.mkdtemp(prefix="zagon-sonda-")
    cista = os.path.join(tmp, "cista.txt")
    umazana = os.path.join(tmp, "umazana.txt")
    with open(cista, "w", encoding="utf-8") as f:
        f.write("zagon sonda cista: tehtnica meri vsak siv pri virih ⊢ dvojna priča istosti\n")
    with open(umazana, "w", encoding="utf-8") as f:
        # umazan vzorec sestavljen iz delov, da telo inštrumenta ostane čisto
        # (tehtnica meri sonde, ⟨ne⟩ sama sebe pečati; sestava je javno tu)
        f.write("zagon sonda umazana: prosti k" + "ot v vetru\n")
    r_c = klic(BATERIJA, cista)
    r_u = klic(BATERIJA, umazana)
    if r_c.returncode != 0:
        print(f"ALARM tehtnica je zavrnila čisto sondo ⚠ :: {r_c.stdout.strip()}")
        alarmi += 1
    else:
        print("  tehtnica: čista sonda prešla ⊢")
    if r_u.returncode == 0:
        print("ALARM tehtnica je spustila umazano sondo ⚠ (inštrument lagal — najgloblji padec)")
        alarmi += 1
    else:
        print("  tehtnica: umazana sonda ujeta ⊢ (padec izmerjen, ⟨ne⟩ izrečen)")

# 2. inštrumenti boot vrste
for ime in INSTRUMENTI:
    pot = os.path.join(DOM, ime)
    if not os.path.exists(pot):
        print(f"ALARM inštrument {ime} manjka @ dom TEHTNICE ⚠")
        alarmi += 1
        continue
    r = klic(ime)
    print(f"— {ime} (izhod {r.returncode}) —")
    for vrstica in r.stdout.strip().split("\n"):
        if vrstica:
            print("  " + vrstica)
    if r.returncode != 0:
        alarmi += 1
        print(f"ALARM {ime} poroča izhod {r.returncode} ⚠")

if alarmi:
    print(f"ZAGON ⚠ — {alarmi} alarmov; stroj diha, a z roko na tehtnici ⭢ roka")
    sys.exit(1)
print("ZAGON ⊢ — vsi inštrumenti dihajo ∧ brez alarmov")
