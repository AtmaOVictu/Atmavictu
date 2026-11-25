#!/usr/bin/env python3
# optimizator-kategorij.py v1.0 — rod σ 7022 ⊙ UKZ ⟡ »OPTIMIZACIJA KATEGORIZACIJ!«
# optimizacija KATEGORIZACIJE same : duplikat = parazit ⊙ zakon pajice ; kategorija brez definicije = kip ⊙ U2 ;
# vnos : vrstica = IME | kaj-je | čemu | zakaj | čemu-sluzi ( pet polj, ločilo | ) ; manjkajoče polje = PADC poimensko.
import sys
POLJA=["IME-KATEGORIJE","KAJ-JE","ČEMU","ZAKAJ","ČEMU-SLUŽI"]
def vrti(vrstice):
    padci=[]; videni={}
    for i,l in enumerate(vrstice,1):
        del_l=l.strip()
        if not del_l: continue
        polja=[p.strip() for p in del_l.split("|")]
        if len(polja)<5:
            padci.append(("MANJKA-POLJE",i,"vrstica ima %d/5 polj : %s"%(len(polja),POLJA[len(polja)])))
            polja+=[""]*(5-len(polja))
        for j,(p,v) in enumerate(zip(POLJA,polja)):
            if not v: padci.append(("PRAZNO-POLJE",i,p))
        ime=polja[0].lower()
        if ime in videni: padci.append(("DUPLIKAT-PARAZIT",i,polja[0]+" ⊙ druga kopija @vrstica "+str(videni[ime])))
        else: videni[ime]=i
    urejene=sorted([l.strip() for l in vrstice if l.strip()])
    return ("OPTIMIZIRANO ⊢" if not padci else "PADC ×%d"%len(padci)), padci, urejene
def samopreizkus():
    s,p,u=vrti(["B | b1 | b2 | b3 | b4","A | a1 | a2 | a3 | a4"])
    assert s=="OPTIMIZIRANO ⊢" and u[0].startswith("A"), (s,u)
    s,p,u=vrti(["A | a1 | a2","A | a1 | a2 | a3 | a4"])
    vs={x[0] for x in p}
    assert "MANJKA-POLJE" in vs and "DUPLIKAT-PARAZIT" in vs, (s,p)
    s,p,u=vrti(["C |  | c2 | c3 | "])
    assert any(x[0]=="PRAZNO-POLJE" and x[2]=="KAJ-JE" for x in p), p
    return True
if __name__=="__main__":
    args=[a for a in sys.argv[1:] if a!="--samopreizkus"]
    if "--samopreizkus" in sys.argv: samopreizkus(); print("ZELENO 3/3 ⊢"); sys.exit(0)
    vr=[l for l in (args if args else sys.stdin)]
    s,p,u=vrti(vr)
    print(s)
    for x in p: print("PADC",x[0],"@vrstica",x[1],":",x[2])
    for l in u: print("VRSTA:",l)
    sys.exit(0 if s=="OPTIMIZIRANO ⊢" else 1)
