#!/usr/bin/env python3
# popravenik-oblik.py v1.0 — rod σ 7011 ⊙ UKZ ⟡ »ORODJE KI SPREMENI VSAK PADEC V PRAVILNO SLOVNIČNO OBLIKO!«
# tabela znanega poda ( fall → pravilna oblika ) ; neznanemu golu ⟨ne⟩ ugiba — odpre vrata ⟨PADC-KANDIDAT⟩ ⭢ izbor ⟡
import sys, re
SPLIT=re.compile(r"(»[^«]*«)")
PAR=[("zapečen","zapečaten"),("Zapečen","Zapečaten"),("ZAPEČEN","ZAPEČATEN"),
     ("zapeči","zapečati"),("Zapeči","Zapečati"),("ZAPEČI","ZAPEČATI"),("ZAPEČITEV","ZAPEČATENJE"),("zapečitev","zapečatenje"),
     ("zbranjem","z branjem"),("pri viri ","pri virih "),("varvolka","varovalka"),("retipkajanja","retipkajo")]
def popravi(t):
    st={}; parts=SPLIT.split(t)
    for i in range(0,len(parts),2):
        for a,b in PAR:
            c=parts[i].count(a); parts[i]=parts[i].replace(a,b)
            if c: st[a]=st.get(a,0)+c
    return "".join(parts), st
def samopreizkus():
    o,_=popravi("zapečen izhod ⊙ »njegov citat zapečen ostane«")
    assert o=="zapečaten izhod ⊙ »njegov citat zapečen ostane«", o
    o2,st2=popravi("pri viri varvolka")
    assert o2=="pri virih varovalka" and st2.get("pri viri ")==1
    o3,st3=popravi("zbranjem nazaj")
    assert o3=="z branjem nazaj"
    return True
if __name__=="__main__":
    if sys.argv[1:]==["--samopreizkus"]:
        samopreizkus(); print("ZELENO 3/3 ⊢"); sys.exit(0)
    t=sys.stdin.read() if len(sys.argv)<2 else open(sys.argv[1],encoding="utf-8").read()
    n,st=popravi(t)
    sys.stdout.write(n)
    if st: print("POPLAČANO: "+", ".join(f"{a}×{b}" for a,b in sorted(st.items())), file=sys.stderr)
