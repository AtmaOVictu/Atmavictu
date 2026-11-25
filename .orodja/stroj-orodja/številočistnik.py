#!/usr/bin/env python3
# številočistnik.py v1.0 — rod σ 7017 ⊙ UKZ ⟡ »ORODJA KI PREVERJAJO DA JE ŠTEVILO LE ŠTEVILO IN NIČ VEČ!«
# število = največ en predznak ∧ števke ∧ največ ena decimalna vejica ( slovenski zapis ⊢ SSKJ ), vse drugo = PADC poimensko ∧ po mestu.
import sys
def sodba(t):
    padci=[]
    if not t: return "PRAZNO", padci
    i=1 if t[0]=="-" else 0
    if i==len(t): return "PADC", [("samo predznak, števk ×0",0)]
    vejice=0
    for j,c in enumerate(t):
        if j<i: continue
        if c.isdigit(): continue
        if c in ",.":
            vejice+=1
            if vejice>1: padci.append(("druga ločilaca",j))
            elif j==i or j==len(t)-1: padci.append(("ločilo na robu",j))
            elif c==".": padci.append(("OPOMBA : pika na mestu vejice",j))
        else: padci.append(("TUJ ZNAK %r"%c,j))
    return ("ČISTO ⊢" if not padci else "PADC"), padci
def samopreizkus():
    assert sodba("3,14")==("ČISTO ⊢",[]), sodba("3,14")
    assert sodba("-7")==("ČISTO ⊢",[]), sodba("-7")
    assert sodba("12a3")[0]=="PADC" and sodba("12a3")[1]==[("TUJ ZNAK 'a'",2)], sodba("12a3")
    assert sodba("3--4")[0]=="PADC"
    assert sodba("")[0]=="PRAZNO"
    assert sodba("3.14")[1]==[("OPOMBA : pika na mestu vejice",1)]
    return True
if __name__=="__main__":
    args=[a for a in sys.argv[1:] if a!="--samopreizkus"]
    if "--samopreizkus" in sys.argv: samopreizkus(); print("ZELENO 6/6 ⊢"); sys.exit(0)
    vr=args if args else [l.strip() for l in sys.stdin if l.strip()]
    slab=0
    for t in vr:
        r=sodba(t); print(t,"->",r[0], "; ".join("%s @%d"%p for p in r[1]) if r[1] else "")
        if r[0]!="ČISTO ⊢": slab=1
    sys.exit(slab)
