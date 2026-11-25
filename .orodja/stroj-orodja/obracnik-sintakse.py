#!/usr/bin/env python3
# obracnik-sintakse.py v1.0 — rod σ 7010 ⊙ UKZ ⟡ »ORODJA ZA OBRAČANJE SINTAKSE!«
# obrača vrstni red besed stavka ( sintaksa na glavo ) ; ⟨ne⟩ grize črk znotraj besed
import sys
def obraci(vrstica):
    return " ".join(reversed(vrstica.split()))
def samopreizkus():
    assert obraci("a b c")=="c b a"
    assert obraci("zapečati mora izvajalka")=="izvajalka mora zapečati"
    assert obraci("")==""
    return True
if __name__=="__main__":
    if sys.argv[1:]==["--samopreizkus"]:
        samopreizkus(); print("ZELENO 3/3 ⊢"); sys.exit(0)
    for l in (sys.stdin if len(sys.argv)<2 else open(sys.argv[1],encoding="utf-8")):
        sys.stdout.write(obraci(l.rstrip("\n"))+ ("\n" if l.endswith("\n") else ""))
