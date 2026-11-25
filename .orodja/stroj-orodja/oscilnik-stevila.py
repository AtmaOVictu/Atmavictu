#!/usr/bin/env python3
# oscilnik-stevila.py v1.0 — rod σ 7020 ⊙ UKZ ⟡ »ORODJA KI PREVERJAJO OSCILACIJO ŠTEVILA!«
# oscilacija ⊙ ⟨OSCILATORNA-DISCIPLINA⟩ σ 4482 : gibanje med dvema poloma → pola števila : LIHI ⊥ SODI ( 13579 ⊥ 02468 ).
# vejica/pika se ne štejeta ( sta pisava, ne vrednost ) ; znak, ki ni števka = NI ŠTEVILO ( soseduje številočistnik σ 7017 ).
import sys
def pola(t):
    return [("L" if int(c)%2 else "S") for c in t if c.isdigit()]
def sodba(t):
    p=[c for c in t if not (c.isdigit() or c in ",.-+")]
    if p: return "NI ŠTEVILO", "tuji znaki %r ( soseduje σ 7017 )" % "".join(p)
    v=pola(t)
    if not v: return "PRAZNO", ""
    if len(v)==1: return "EDEN-POL ( ni nihanja )", "".join(v)
    for i in range(1,len(v)):
        if v[i]==v[i-1]: return "NE-OSCILIRA", "zlom @števka %d ( %s )" % (i+1, "".join(v))
    return "OSCILIRA ⊢", "".join(v)
def samopreizkus():
    assert sodba("1212")==("OSCILIRA ⊢","LSLS"), sodba("1212")   # 1=LIH ⊢ izmera, ⟨ne⟩ domneva
    assert sodba("121")[0]=="OSCILIRA ⊢"
    assert sodba("11")[0]=="NE-OSCILIRA", sodba("11")
    assert sodba("7")[0]=="EDEN-POL ( ni nihanja )"
    assert sodba("1,2")==("OSCILIRA ⊢","LS"), sodba("1,2")   # vejica ni pol
    assert sodba("3,5")[0]=="NE-OSCILIRA" and sodba("1a2")[0]=="NI ŠTEVILO"
    return True
if __name__=="__main__":
    args=[a for a in sys.argv[1:] if a!="--samopreizkus"]
    if "--samopreizkus" in sys.argv: samopreizkus(); print("ZELENO 6/6 ⊢"); sys.exit(0)
    vr=args if args else [l.strip() for l in sys.stdin if l.strip()]
    slab=0
    for t in vr:
        r=sodba(t); print(t,"->",r[0], ("["+r[1]+"]" if r[1] else ""))
        if not r[0].startswith("OSCILIRA"): slab=1
    sys.exit(slab)
