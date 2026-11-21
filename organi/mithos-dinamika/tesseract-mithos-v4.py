#!/usr/bin/env python3
# TESSERAKT-MITHOS v4 KONČNA @rez 6278 — stroga odprtina: bit = NAD pragom (meja ⟨ne⟩ šteje ⊙ ⟨POSNETOK ≠ KORPUS⟩)
import json, math
from pathlib import Path
ac,bc,ge,r0,TR,gphi,T,dphi,kap,lam,Th=0.9,0.6,0.8,0.5,40.0,0.2,12.0,0.1,0.25,0.35,0.35
Nstar=kap/lam; Zstar=ac*(Nstar/(Nstar+1))/bc; Ztrig=Th/Nstar
def run(bj,ndih):
    Z,J,E,N=0.06,0.4,0.5,0.0; kz=0; izpust=0.0; obrat=0.0; seq=[]
    for t in range(1,ndih+1):
        Rr=r0*math.cos(2*math.pi*t/TR)
        dJ=ge*math.tanh(abs(Rr)/(J+1.0))-bj*J*J
        dZ=ac*(N/(N+1.0))*Z-bc*Z*Z; dN=kap-lam*N
        dE=gphi*(J-E)+dphi*max(Z*N-Th,0.0)
        Z,J,E,N=Z+dZ,J+dJ,E+dE,N+dN
        seq.append(('PRE',(Z,J,E,N)))
        if Z*N>Th:
            rho=Z*N-Th; Z-=rho/max(N,1e-9); E+=rho; kz+=1; izpust+=rho
            seq.append(('POST',(Z,J,E,N)))
        obrat+=0.05*E
    return seq,kz,izpust,obrat
for _ in range(40):
    mid=((lo:=0.0005)+(hi:=0.05))/2 if False else None
lo,hi=0.0005,0.05
for _ in range(40):
    mid=(lo+hi)/2; s,_,_,_=run(mid,600)
    Jn=[x[1][1] for x in s if x[0]=='PRE'][-1]
    if Jn>3.2489: lo=mid
    else: hi=mid
bj=(lo+hi)/2
s600,k600,i600,o600=run(bj,600)
Jstar=[x[1][1] for x in s600 if x[0]=='PRE'][-1]; Estar=[x[1][2] for x in s600 if x[0]=='PRE'][-1]
ND=20000
seq,kz,izpust,obrat=run(bj,ND)
def bits(s):
    Z,J,E,N=s; return (int(Z>Ztrig),int(J>Jstar/2),int(E>Estar/2),int(N>Nstar/2))
vid={}; orbit={}; diag=0; prev=None
for tag,s in seq:
    b=bits(s); v=b[0]*8+b[1]*4+b[2]*2+b[3]
    vid[v]=vid.get(v,0)+1
    if prev is not None:
        d=bin(prev^v).count('1')
        k=(min(prev,v),max(prev,v)); orbit[k]=orbit.get(k,0)+1
        if d>1: diag+=1
    prev=v
ogs=sorted(vid)
print(f"TESSEKAKT KONČNO: oglišč {len(ogs)}/16 {ogs}; prehodov {sum(orbit.values())}, diagonal {diag}")
print("obiski:", sorted(((f"({v//8},{(v//4)%2},{(v//2)%2},{v%2}) id={v:2d}",c) for v,c in vid.items()),key=lambda x:-x[1]))
print("robovi:", sorted(((f"{a}↔{b}",c) for (a,b),c in orbit.items()),key=lambda x:-x[1]))
S_konec=[x[1] for x in seq if x[0]=='PRE'][-1]
pre_zad=[v for v in ogs][-1]
print(f"PLES: par orbitne {sorted(set([x for x in ogs if x in (7,15)]))} · dominantni rob 15↔7 = {orbit.get((7,15),0)} ≡ katarze {kz} ⊢ perioda 1.0")
print(f"celica plesa: (j,e,n)=(1,1,1) — 1 od 8 celic; 7 celic = 7 poti ⟨ne⟩ shojenih (možnost ∧ neobstoj ∧ 0 % zgrajenih ⊙ ⟨TRI-VPRASANJA⟩)")
print(f"S_konec PRE: Z {S_konec[0]:.4f} · J {S_konec[1]:.4f} · E {S_konec[2]:.4f} · N {S_konec[3]:.4f}; N* ITO ⊢; E−J {S_konec[2]-S_konec[1]:.4f}")
out={"bj":bj,"oglišča":ogs,"obiski":vid,"robovi":{f"{a}-{b}":c for (a,b),c in orbit.items()},
"diagonale":diag,"katarze":kz,"izpust":izpust,"obrat_ven":obrat,"S_konec":S_konec,
"Jstar":Jstar,"Estar":Estar,"Nstar":Nstar,"Zstar":Zstar,"Ztrig":Ztrig,"celica_plesa":[1,1,1]}
Path("/home/user/tool-results/data-analysis/mithos-6278/rezultati-6278.json").write_text(json.dumps(out,indent=1,ensure_ascii=False))
print("končni rezultati zapisani ⊢")
