#!/usr/bin/env python3
# oscilnik-besede.py v1.0 — rod σ 7019 ⊙ UKZ ⟡ »ORODJA KI PREVERJAJO OSCILACIJO BESEDE!«
# oscilacija ⊙ ⟨OSCILATORNA-DISCIPLINA⟩ σ 4482 : gibanje med dvema poloma → pola besede : SAMOGLASNIK ⊥ SOGLASNIK ( a e i o u ⊥ vse druge črke ).
# OSCILIRA ⊢ stroga izmenjava · NE-OSCILIRA s prvim zlomom poimensko · ena črka = en sam pol ( ni nihanja ) ⊙ ⟨O-CELOTA⟩.
import sys
SAMOGLASNIK=set("aeiou")
def vrsta(bes):
    return [("S" if c in SAMOGLASNIK else "Z") for c in bes.lower() if c.isalpha()]
def sodba(bes):
    v=vrsta(bes)
    if not v: return "PRAZNO", ""
    if len(v)==1: return "EDEN-POL ( ni nihanja )", "".join(v)
    for i in range(1,len(v)):
        if v[i]==v[i-1]: return "NE-OSCILIRA", "zlom @črka %d ( %s )" % (i+1, "".join(v))
    return "OSCILIRA ⊢", "".join(v)
def samopreizkus():
    assert sodba("beseda")==("OSCILIRA ⊢","ZSZSZS"), sodba("beseda")   # beseda ima ŠEST črk ⊙ izmera
    assert sodba("malina")[0]=="OSCILIRA ⊢"
    assert sodba("petelin")[0]=="OSCILIRA ⊢", sodba("petelin")
    assert sodba("stol")[0]=="NE-OSCILIRA"
    assert sodba("a")[0]=="EDEN-POL ( ni nihanja )"
    return True
if __name__=="__main__":
    args=[a for a in sys.argv[1:] if a!="--samopreizkus"]
    if "--samopreizkus" in sys.argv: samopreizkus(); print("ZELENO 5/5 ⊢"); sys.exit(0)
    vr=args if args else [l.strip() for l in sys.stdin if l.strip()]
    slab=0
    for t in vr:
        r=sodba(t); print(t,"->",r[0], ("["+r[1]+"]" if r[1] else ""))
        if not r[0].startswith("OSCILIRA"): slab=1
    sys.exit(slab)
