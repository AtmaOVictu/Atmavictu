#!/usr/bin/env python3
# številovrstnik.py v1.0 — rod σ 7016 ⊙ UKZ ⟡ »ORODJA KI TRANSFORMIRAJO ŠTEVILA V BESEDE SLOVENSKEGA JEZIKA!«
# pravila izmerjena pri viru: SP, Pravila §544 ( do 100 ∧ stotice SKUPAJ : enajst, petindvajset, dvesto ; druge NARAZEN : sto enajst, dva tisoč, tristo tisoč sto )
# ⊢ ŠUSS 3.2 ( arnes.si/~lmarus/suss/arhiv/suss-arhiv-000396.html, dostop 25. 11. 2026 ) ∧ sklanjalne plasti @rez σ 6193 ( milijon : 5+ rodilnik množine ).
# raz v1.0 : osnovne ( citatne ) oblike ena/dva ⊢ SSKJ éna ; obseg 0 .. 999 999 999 zunaj = VIDNO.
import sys
ENOTE={1:"ena",2:"dva",3:"tri",4:"štiri",5:"pet",6:"šest",7:"sedem",8:"osem",9:"devet"}
NAJST={11:"enajst",12:"dvanajst",13:"trinajst",14:"štirinajst",15:"petnajst",16:"šestnajst",17:"sedemnajst",18:"osemnajst",19:"devetnajst"}
DESETICE={20:"dvajset",30:"trideset",40:"štirideset",50:"petdeset",60:"šestdeset",70:"sedemdeset",80:"osemdeset",90:"devetdeset"}
STOTICE={1:"sto",2:"dvesto",3:"tristo",4:"štiristo",5:"petsto",6:"šeststo",7:"sedemsto",8:"osemsto",9:"devetsto"}
def pod100(n):
    if n<10: return ENOTE[n]
    if n<20: return NAJST[n]
    d,s=n//10*10,n%10
    return DESETICE[d] if s==0 else ENOTE[s]+"in"+DESETICE[d]
def pod999(n):
    s,o=n//100,n%100
    return STOTICE[s] if o==0 else (pod100(o) if s==0 else STOTICE[s]+" "+pod100(o))
def milijon(m):
    if m==1: return "en milijon"
    if m==2: return "dva milijona"
    if m in (3,4): return pod100(m)+" milijoni"
    return pod999(m)+" milijonov"
def beseda(n):
    if n<0: return "minus "+beseda(-n)
    if n==0: return "nič"
    deli=[]
    if n>=1_000_000: deli.append(milijon(n//1_000_000)); n%=1_000_000
    if n>=1000: t=(n//1000); deli.append("tisoč" if t==1 else pod999(t)+" tisoč"); n%=1000
    if n: deli.append(pod999(n))
    return " ".join(deli)
def vrti(t):
    try: n=int(t)
    except ValueError: return "NI ŠTEVILO ( soseduje številočistnik σ 7017 )"
    if abs(n)>999_999_999: return "VIDNO ( meja v1.0 : 999 999 999, ⟨NE-UGIBAJ⟩ 2690 )"
    return beseda(n)
def samopreizkus():
    assert beseda(143800)=="sto triinštirideset tisoč osemsto", beseda(143800)     # ⊢ SP §544 ( 143|800 )
    assert beseda(2000)=="dva tisoč", beseda(2000)                                # ⊢ narazen pravilo
    assert beseda(21)=="enaindvajset" and beseda(25)=="petindvajset", beseda(25)  # ⊢ skupaj pravilo
    assert beseda(321)=="tristo enaindvajset", beseda(321)
    assert beseda(1900)=="tisoč devetsto" and beseda(1000)=="tisoč", (beseda(1900),beseda(1000))
    assert beseda(0)=="nič" and beseda(300100)=="tristo tisoč sto", beseda(300100) # ⊢ ŠUSS primer
    assert beseda(2_500_000)=="dva milijona petsto tisoč", beseda(2_500_000)
    assert vrti("3a")=="NI ŠTEVILO ( soseduje številočistnik σ 7017 )"
    return True
if __name__=="__main__":
    args=[a for a in sys.argv[1:] if a!="--samopreizkus"]
    if "--samopreizkus" in sys.argv: samopreizkus(); print("ZELENO 8/8 ⊢"); sys.exit(0)
    vr=args if args else [l.strip() for l in sys.stdin if l.strip()]
    for t in vr: print(vrti(t))
