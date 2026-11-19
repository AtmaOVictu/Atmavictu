# -*- coding: utf-8 -*-
# NA-MOST.PY — temeljna pot ( obveza reza 3674: povzetek vsakega diha prileti na most )
# Rabi rešeno pot: luka bere DOM ( 8766 ) → /api/odoblaka → lucius/odoblaka.md ( izven gita ⊙ bratova varovalka ).
# Zagon: python lucius/na-most.py <pot-do-datoteke> [naslov]
# Vsak povzetek: časovni žig ⊢ §0.20 + telo + pečat, da DOM pokaže kaj je novega.
import sys, io
from datetime import datetime, timezone
from pathlib import Path

MOST = Path(r"C:\Users\Luka\Documents\Arhiv\Git\Atmavictu\lucius\odoblaka.md")

def main():
    if len(sys.argv) < 2:
        print("raba: python lucius/na-most.py <pot-do-datoteke> [naslov]")
        sys.exit(1)
    vir = Path(sys.argv[1])
    naslov = sys.argv[2] if len(sys.argv) > 2 else vir.stem
    telo = vir.read_text(encoding="utf-8").strip()
    ura = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M") + " UTC"
    vstop = (
        "\n## " + ura + " — " + naslov + "\n\n"
        + telo + "\n"
        + "\n⊙ na-most.py ⊢ — povzetek odložen na most ( obveza reza 3674 ∧ §0.20 ∧ §0.33 ) · vir priča: "
        + vir.name + "\n"
    )
    with open(MOST, "a", encoding="utf-8") as f:
        f.write(vstop)
    print("NA-MOST ⊢", len(vstop), "znakov · naslov:", naslov, "· ura:", ura)

if __name__ == "__main__":
    main()
