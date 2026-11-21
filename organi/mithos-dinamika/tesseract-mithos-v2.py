#!/usr/bin/env python3
# TESSERAKT-MITHOS v2 @rez 6278 — strukturni pragovi (kura ⟨PADC-PLOŠČA-PRAGA⟩)
import json, math, statistics
from pathlib import Path
ac,bc,ge,r0,TR,gphi,T,dphi,kap,lam,Th = 0.9,0.6,0.8,0.5,40.0,0.2,12.0,0.1,0.25,0.35,0.35
Nstar=kap/lam; Zstar=ac*(Nstar/(Nstar+1))/bc; Ztrig=Th/Nstar
def run(bj,ndih):
    Z,J,E,N=0.06,0.4,0.5,0.0; kz=0; izpust=0.0; obrat=0.0
    hist=[]
    for t in range(1,ndih+1):
        Rr=r0*math.cos(2*math.pi*t/TR)
        dJ=ge*math.tanh(abs(Rr)/(J+1.0))-bj*J*J
        dZ=ac*(N/(N+1.0))*Z-bc*Z*Z
        dN=kap-lam*N
        dE=gphi*(J-E)+dphi*max(Z*N-Th,0.0)
        Z,J,E,N=Z+dZ,J+dJ,E+dE,N+dN
        hist.append((Z,J,E,N))      # PRE-katarza stanje diha (stanje, ki je prestopilo prag)
        if Z*N>Th:
            rho=Z*N-Th; Z-=rho/max(N,1e-9); E+=rho; kz+=1; izpust+=rho
        obrat+=0.05*E
    return hist,kz,izpust,obrat
lo,hi=0.0005,0.05
for _ in range(40):
    mid=(lo+hi)/2; h,_,_,_=run(mid,600)
    if h[-1][1]>3.2489: lo=mid
    else: hi=mid
bj=(lo+hi)/2
h600,k600,i600,o600=run(bj,600)
Jstar=h600[-1][1]; Estar=h600[-1][2]
ND=20000
h,kz,izpust,obrat=run(bj,ND)
Zf,Jf,Ef,Nf=h[-1]
prva=next((i+1 for i,s in enumerate(h) if s[0]*s[3]>Th),None)
prKatarze=sum(1 for i in range(ND-1,ND-101,-1) if h[i][0]*h[i][3]>Th)
def bits(s):
    Z,J,E,N=s; return (int(Z>=Ztrig),int(J>Jstar/2),int(E>Estar/2),int(N>Nstar/2))
vid={v:0 for v in range(16)}; kzv={v:0 for v in range(16)}
edges={}; diagonale=0; prev=None; sv=[0]*ND
for idx,s in enumerate(h):
    b=bits(s); v=b[0]*8+b[1]*4+b[2]*2+b[3]; sv[idx]=v
    vid[v]+=1
    if s[0]*s[3]>Th: kzv[v]+=1
    if prev is not None:
        d=bin(prev^v).count('1')
        if d==1:
            k=(min(prev,v),max(prev,v)); edges[k]=edges.get(k,0)+1
        elif d>1: diagonale+=1
    prev=v
print(f"βj={bj:.6f} ⊢ J(600)={Jstar:.4f}==3.2489 kalibracija; katarze600={k600} ⊥ priča 590; prva @dih {prva} ⊥ priča 11")
print(f"N* izmerjeno {Nf:.6f} = analitično {Nstar:.6f} ⊢ ITO; Z* drži 0.4900 prag (post-release); E−J = {Ef-Jf:.4f} (priča 2.2431 ⭢ ⟡)")
print(f"katarze 20k = {kz} ≈ {kz/ND:.3f}/dih; zadnjih 100 pre-stanji nad pragom {prKatarze}/100 ⊢ perioda 1.0")
print(f"\nTESSEKAKT: obiskana {sum(1 for v in vid if vid[v]>0)}/16 oglišč; robov pohojenih {len(edges)}/32; diagonal {diagonale}")
print("oglišča (z,j,e,n · id · dihovi · katarze):")
for v,c in sorted(vid.items(),key=lambda kv:-kv[1]):
    if c==0: break
    print(f"  ({v//8},{(v//4)%2},{(v//2)%2},{v%2}) id={v:2d} · {c:6d} · {kzv[v]}")
print("robovi:", sorted(((f'{a}↔{b}',c) for (a,b),c in edges.items()),key=lambda x:-x[1]))
print(f"orbita zadnjih 200: {sorted(set(sv[-200:]))} · končni par hoje: {sv[-2]}→{sv[-1]}")
out={"beta_j":bj,"Jstar":Jstar,"Estar":Estar,"N_star":Nstar,"Zstar":Zstar,"Ztrig":Ztrig,
"S600":list(h600[-1]),"S_konec":[Zf,Jf,Ef,Nf],"katarze_600":k600,"katarze_20000":kz,
"prva_katarza":prva,"perioda100":prKatarze,"izpust":izpust,"obrat_ven":obrat,"E_minus_J":Ef-Jf,
"oglišca":{str(k):v for k,v in vid.items()},"katarze_v_ogliscu":{str(k):v for k,v in kzv.items()},
"robovi":{f"{a}-{b}":c for (a,b),c in edges.items()},"diagonale":diagonale,
"obiskanih":sum(1 for v in vid if vid[v]>0),"pohojenih_robov":len(edges),
"orbita1000":sorted(set(sv[-1000:])),"zadnji_par":[sv[-2],sv[-1]]}
Path("/home/user/tool-results/data-analysis/mithos-6278/rezultati-6278-v2.json").write_text(json.dumps(out,indent=1,ensure_ascii=False))
print("zapisano v2 ⊢")
