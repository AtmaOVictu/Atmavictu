#!/usr/bin/env python3
# TESSERAKT-MITHOS v3 @rez 6278 — dvovzorčna izmera: PRE (ogenj) ⊥ POST (počitek) isti dih
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
lo,hi=0.0005,0.05
def run600(bj):
    return run(bj,600)
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
    Z,J,E,N=s; return (int(Z>=Ztrig),int(J>Jstar/2),int(E>Estar/2),int(N>Nstar/2))
vid={}; kzv={}; edges={}; diag=0; prev=None
for tag,s in seq:
    b=bits(s); v=b[0]*8+b[1]*4+b[2]*2+b[3]
    key=(tag,v); vid[key]=vid.get(key,0)+1
    if s[0]*s[3]>Th: kzv[key]=kzv.get(key,0)+1
    if prev is not None:
        if prev[0]!=tag:  # PRE(dih t) → POST(dih t) = katarzni rob
            d=bin(prev[1]^v).count('1')
            k=((prev[0],prev[1]),(tag,v)); edges[k]=edges.get(k,0)+1
            if d>1: diag+=1
        else:
            k=((prev[0],prev[1]),(tag,v)); edges[k]=edges.get(k,0)+1
            d=bin(prev[1]^v).count('1')
            if d>1: diag+=1
    prev=key
ogs=set(v for _,v in vid)
print(f"oglišč obiskanih: {len(ogs)}/16; parov PRE/POST obiskanih: {len(vid)}; diagonal {diag}")
print("obiski (vzorec,oglišče → dihovi):")
for (tag,v),c in sorted(vid.items(),key=lambda kv:-kv[1])[:8]:
    print(f"  {tag:4s} ({v//8},{(v//4)%2},{(v//2)%2},{v%2}) id={v:2d} · {c}")
top=sorted(edges.items(),key=lambda kv:-kv[1])[:6]
print("robovi hoje:", [(f"{a[1]}→{b[1]}",c) for (a,b),c in top])
# rob katarze: PRE t → POST t
pre_last=[v for (tag,v) in [(None,None)]]
catarze_rob=sum(c for ((t1,v1),(t2,v2)),c in edges.items() if t1=='PRE' and t2=='POST')
print(f"PRE→POST (katarzni) prehodi skupaj: {catarze_rob} == katarze {kz} ⊢")
S_konec=[x[1] for x in seq if x[0]=='PRE'][-1]
E_minus_J=S_konec[2]-S_konec[1]
print(f"S_konec (PRE): Z {S_konec[0]:.4f} · J {S_konec[1]:.4f} · E {S_konec[2]:.4f} · N {S_konec[3]:.4f}; E−J {E_minus_J:.4f}")
# orbita: PRE@t → POST@t → PRE@t+1 ...
previd=None; orbit_edges={}
for i,(tag,s) in enumerate(seq):
    b=bits(s); v=b[0]*8+b[1]*4+b[2]*2+b[3]
    if previd is not None:
        k=(min(previd,v),max(previd,v)); orbit_edges[k]=orbit_edges.get(k,0)+1
    previd=v
print("robovi (ogliščna orbita, urejeni):", sorted(((f"{a}↔{b}",c) for (a,b),c in orbit_edges.items()),key=lambda x:-x[1]))
celice=set()
# katera celica (3D kocka = fiksna ena os) drži ples: osceska osem celic tesserakta = fiks (j,e,n) kocka
zadnji=seq[-1][1]; zb=bits(zadnji); celica=(zb[1],zb[2],zb[3]); celice.add(celica)
print(f"ples po zori živi v celici (j,e,n)={celica} — ena od 8 celic tesserakta; os plesa = z")
out={"bj":bj,"oglišč":len(ogs),"dvovzorci":len(vid),"diagonale":diag,"S600":[Jstar,Estar],"S_konec":S_konec,
"katarze":kz,"izpust":izpust,"obrat_ven":obrat,"E_minus_J":E_minus_J,
"obiski":{f"{t}{v}":c for (t,v),c in vid.items()},"robovi_orbite":{f"{a}-{b}":c for (a,b),c in orbit_edges.items()},
"celica_plesa":list(celica)}
Path("/home/user/tool-results/data-analysis/mithos-6278/rezultati-6278-v3.json").write_text(json.dumps(out,indent=1,ensure_ascii=False))
print("zapisano v3 ⊢")
