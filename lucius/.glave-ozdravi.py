# -*- coding: utf-8 -*-
# .glave-ozdravi.py — ⟨MD022-DVAKRAT⟩ PREPREKA 3684: ozdravi mehanične padce v VSEH .md repa
# 1. zagon: glava ( naslov brez prazne ) + konec ( manjkajoča končna vrstica )
# 2. zagon ( ta različica ): VSI naslovi — prazna vrstica nad ∧ pod vsakim naslovom IZVEN kodnih ograj ( ``` )
#    naslov znotraj ograje ⟨ni⟩ naslov — čistilec jo prepozna ∧ ne dotika ⊙ ⟨ne-ugibaj⟩
# Izključeno: lucius/odoblaka.md ( most — zasebna plast, append-most, ⟨ne⟩ se krtači ⊙ varovalka brata )
import os, glob

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(KOREN)

datoteke = sorted(glob.glob("*.md") + glob.glob("lucius/*.md"))
datoteke = [f for f in datoteke if f.replace(os.sep, "/") != "lucius/odoblaka.md"]

popravljeno = {}
for f in datoteke:
    with open(f, encoding="utf-8", newline="") as fh:
        s = fh.read()
    pred = s

    # MD047: končna vrstica
    if s and not s.endswith("\n"):
        s += "\n"

    # MD022: prazna vrstica okoli vsakega naslova ( IZVEN kodnih ograj )
    lines = s.split("\n")
    out = []
    ograja = False
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("```"):
            ograja = not ograja
            out.append(ln)
            continue
        if not ograja and ln.startswith("#"):
            if out and out[-1].strip() != "":
                out.append("")
            out.append(ln)
            if i + 1 < len(lines) and lines[i + 1].strip() != "":
                out.append("")
            continue
        out.append(ln)
    s = "\n".join(out)

    if s != pred:
        with open(f, "w", encoding="utf-8", newline="") as fh:
            fh.write(s)
        popravljeno[f] = True

print(f"OZDRAVLJENIH ⊢: {len(popravljeno)} / {len(datoteke)} datotek")
for f in popravljeno:
    print("  ⊙", f)
