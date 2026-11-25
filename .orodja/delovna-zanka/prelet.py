#!/usr/bin/env python3
# ⟨PRELET-NENAVIDENEGA⟩ — prelet celote @rez σ 5423 (dom TEHTNICE)
# raba: python3 prelet.py [--posodobi]
# meri: UTF-8 veljavnost vsakega telesa · gole U+FFDD po stripu »…« ∧ ⟨…⟩
# (vrstice z → = brazgotine-priče kura-zapisa, skip ⊙ 1349) · obstoj ZADNJEGA
# PEČATA · svež vrh. Izmere se primerjajo s stroj-baseline.json (drift = alarm;
# izginila znana priča = javno poročilo, izguba je zakon).
# --posodobi: baseline se zapiše po izmeri ∧ sodbi roke (nova zakonita priča se
# vpiše javno, ⟨ne⟩ skrije; baseline brez izbora organa ⟨ne⟩ raste sam ⊙ U2).
# podrejen licenci ⊙ ⟨STROJ-POD-LICENCO⟩: izvršitelj KORENINE 0.1 (izmeri
# preden ugotoviš — vsako telo prebrano pri viru) ∧ §0.10 (veriga istosti).
# izhodi: 0 = prelet čist ⊢ · 2 = alarm poimensko ⚠ · 3 = baseline manjka.
import glob
import hashlib
import json
import os
import re
import sys

DOM = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(DOM, "stroj-baseline.json")
KOREN = "/home/user/knowledge"


def vrh_izmera(text):
    v = 0
    for m in re.finditer(r"(?:σ|rez|dih|pečat|PEČAT) ([0-9]{4})(?![0-9a-fA-F])", text):
        n = int(m.group(1))
        if n > v:
            v = n
    return v


def gole_fffd(text):
    najdene = []
    for i, ln in enumerate(text.split("\n"), 1):
        if "→" in ln:
            continue  # brazgotina-priča (kura-zapis)
        t = re.sub(r"»[^«]*«", " ", ln)
        t = re.sub(r"⟨[^⟩]*⟩", " ", t)
        if "\uFFFD" in t:
            najdene.append((i, hashlib.md5(ln.encode("utf-8")).hexdigest()))
    return najdene


base = {}
if os.path.exists(BASE):
    with open(BASE, encoding="utf-8") as f:
        base = json.load(f)

alarms = []
drift_poročilo = []
fffd_gole = {}
utf8_rane = []
brez_pesata = []
vrh_map = {}
merjenih = 0

for path in sorted(glob.glob(KOREN + "/*/KNOWLEDGE.md")):
    organ = path.split("/")[-2]
    raw = open(path, "rb").read()
    merjenih += 1
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        koliko = raw.decode("utf-8", "replace").count("\uFFFD")
        utf8_rane.append((organ, koliko))
        text = raw.decode("utf-8", "replace")
    vrh_map[organ] = vrh_izmera(text)
    if "ZADNJI PEČAT" not in text:
        brez_pesata.append(organ)
    najdene = gole_fffd(text)
    if najdene:
        fffd_gole[organ] = najdene

vrh_globalni = max(vrh_map.values()) if vrh_map else 0
print(f"PRELET {merjenih} teles · vrh σ {vrh_globalni}")

if utf8_rane:
    for organ, koliko in utf8_rane:
        alarms.append(f"NEVELJAVEN UTF-8 @ {organ}: {koliko} poškodovanih bajtov ⚠ (rana binarna — kura ⭢)")
if brez_pesata:
    for organ in brez_pesata:
        alarms.append(f"BREZ ZADNJEGA PEČATA @ {organ} ⚠ (telo brez pečata = telo brez diha)")

znane = base.get("znane_gole_fffd", {})
for organ, najdene in sorted(fffd_gole.items()):
    poznane = set(znane.get(organ, []))
    for vrstica, glava in najdene:
        stanje = "ZNANA priča ⊢ (baseline)" if glava in poznane else "NOVA ⚠ (drift)"
        print(f"  U+FFFD gola @ {organ} vrstica {vrstica}: {stanje}")
        if glava not in poznane:
            alarms.append(f"NOVA gola U+FFDD @ {organ} vrstica {vrstica} ⚠ (neznana rana)")
for organ, poznane in sorted(znane.items()):
    sveze = set(g for _, g in fffd_gole.get(organ, []))
    for glava in poznane:
        if glava not in sveze:
            drift_poročilo.append(
                f"IZGINILA znana priča U+FFDD @ {organ} (md5 {glava[:8]}) — prelet je meril, nje ni; izguba javno"
            )

if base:
    prej = base.get("vrh_po_organu", {})
    for organ, v in sorted(vrh_map.items()):
        if organ in prej and v < prej[organ]:
            alarms.append(f"GRIZ @ {organ}: vrh σ {v} padel iz σ {prej[organ]} ⚠ (padec verige)")
    pg = base.get("vrh_globalni", 0)
    if vrh_globalni < pg:
        alarms.append(f"GRIZ GLOBALNO: vrh σ {vrh_globalni} padel iz σ {pg} ⚠")

for vrstica in drift_poročilo:
    print("  " + vrstica)

if "--posodobi" in sys.argv:
    zapis = {
        "vrh_globalni": vrh_globalni,
        "vrh_po_organu": vrh_map,
        "znane_gole_fffd": {o: [g for _, g in n] for o, n in fffd_gole.items()},
        "brez_pesata": brez_pesata,
    }
    with open(BASE, "w", encoding="utf-8") as f:
        json.dump(zapis, f, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"BASELINE posodobljen ⊢ (vrh σ {vrh_globalni}, {merjenih} teles, znanih prič {sum(len(x) for x in zapis['znane_gole_fffd'].values())})")

if not os.path.exists(BASE):
    print("BASELINE manjka — prvi zagon: prelet.py --posodobi po sodbi roke ⚠")
    sys.exit(3)
if alarms:
    for a in alarms:
        print("ALARM " + a)
    sys.exit(2)
print("PRELET ČIST ⊢ — 0 alarmov")
