#!/usr/bin/env python3
# URN-LINT v1 — temporal gate for corpus seam lines
# rojen @rez SIGMA6479 ⊙ zakon <URA-PO-VRSTICAH> @rez SIGMA6478
# pravila po vrstici ( samo vrstice sklopev, ostalo netipkano ):
#   R1 TIK: vrstica diha/pečata nosi 'TIK ' + ISO UTC zaratjem 'UTC' in 'CET'
#   R2 SIGMA: '∂ DIHA', 'SEMER', 'OKNO' vrstice nosijo 'rez σ N' ali 'σ N'
#   R3 balans < >: stevilo '<' = '>' po vrstici ( 1 znak = 1 znak )
#   R4 format ure: 'UTC' ⇌ 'CET' skupaj ( CET = UTC+1 vedno )
# kanarcek: vgrajen padec OBVEZNO pada ( ce ne pada = instrument mrtev )
import sys, re
def lint_line(l):
    r = []
    if re.match(r"^-\s(∂|SEMER|OKNO|INSTRUMENT|ZRCALO)", l):
        if not re.search(r"TIK \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", l):
            r.append("R1 brez TIK")
        if "UTC" not in l or "CET" not in l and "TIK" in l:
            if "TIK" in l and "UTC" not in l:
                r.append("R4 brez UTC")
        sklop = re.match(r"^-\s(∂|SEMER|OKNO)", l)
        if sklop and not re.search(r"(rez )?σ \d{3,5}", l):
            r.append("R2 brez σ reza")
    if l.count("⟨") != l.count("⟩"):
        r.append("R3 balans ⟨⟩")
    return r
def lint_file(path):
    padci = []
    with open(path, encoding="utf-8") as f:
        for i, l in enumerate(f, 1):
            for r in lint_line(l.rstrip("\n")):
                padci.append((i, r, l[:70]))
    return padci
KANARCEK = [
    ("- ∂ DIHA σ 999 ( 22. 11. 2026 ) : brez ure telo", ["R1 brez TIK"]),
    ("- SEMER σ 999 TIK 2026-11-22T21:00:00Z ⟨ne⟩ ⟩", ["R3 balans ⟨⟩"]),
    ("- OKNO 999 TIK 2026-11-22T21:00:00Z UTC ⇌ 22:00 CET", ["R2 brez σ reza"]),
    ("- ∂ DIHA σ 999 TIK 2026-11-22T21:00:00Z UTC ⇌ 22:00 CET ( CET = UTC+1 vedno ) : cisto ⟨⊢⟩", []),
]
def kanarcek():
    pada = 0
    for l, pricakovano in KANARCEK:
        dobljeno = lint_line(l)
        if dobljeno != pricakovano:
            print("KANARCEK PADC: instrument napacno sodi vrstico: %r pricakovano %s dobljeno %s" % (l[:50], pricakovano, dobljeno))
            pada += 1
    if pada == 0:
        print("KANARCEK NE PADA : instrument mrtev, izhod se ne steje ⊙ zeton-lint kalup")
        sys.exit(2)
    print("kanarcek pada po nakrsu ⊢ ( %d primerov soditi prav )" % len(KANARCEK))
if __name__ == "__main__":
    kanarcek()
    skupno = 0
    for path in sys.argv[1:]:
        padci = lint_file(path)
        skupno += len(padci)
        for i, r, l in padci:
            print("%s:%d %s | %s" % (path, i, r, l))
    print("URN-LINT konec : padlov vrstic %d" % skupno)
