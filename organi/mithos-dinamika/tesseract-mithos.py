#!/usr/bin/env python3
# TESSERAKT-MITHOS @rez 6278 — replika diferencialnega sistema S(t)=(Z,J,E,N)
# Forme: VERBATIM ⟡ (mithos-dinamika §2) + ZASUTE izbire izvajalke ⭢ sodba ⚔ ⟡
import json, math
from pathlib import Path

# konstante priče σ 5993 ⊢
ac, bc, ge, r0, TR, gphi, T, dphi, kap, lam, Th = 0.9, 0.6, 0.8, 0.5, 40.0, 0.2, 12.0, 0.1, 0.25, 0.35, 0.35
Nstar = kap/lam; Zstar = ac*(Nstar/(Nstar+1))/bc; Ztrig = Th/Nstar
print(f"N* = {Nstar:.4f} analitično; Z* = {Zstar:.4f}; Z_trig = {Ztrig:.4f}")

def run(bj, ndih=600):
    Z,J,E,N = 0.06, 0.4, 0.5, 0.0
    kz, izpust, obrat = 0, 0.0, 0.0
    hist=[]
    for t in range(1, ndih+1):
        Rr = r0*math.cos(2*math.pi*t/TR)
        dJ = ge*math.tanh(abs(Rr)/(J+1.0)) - bj*J*J
        dZ = ac*(N/(N+1.0))*Z - bc*Z*Z
        dN = kap*1.0 - lam*N
        dE = gphi*(J-E) + dphi*max(Z*N-Th, 0.0)
        Z,J,E,N = Z+dZ, J+dJ, E+dE, N+dN
        if Z*N > Th:  # KATARZA: sprostitev napetosti M v priznanje E
            rho = Z*N - Th
            Z -= rho/max(N,1e-9); E += rho; kz += 1; izpust += rho
        obrat += 0.05*E
        hist.append((Z,J,E,N))
    return hist, kz, izpust, obrat

# kalibracija βj na pričo J(600)=3.2489 (bisekcija, izmera ⊢)
lo, hi = 0.0005, 0.05
for _ in range(40):
    mid=(lo+hi)/2; h,_,_,_ = run(mid,600)
    if h[-1][1] > 3.2489: lo=mid
    else: hi=mid
bj=(lo+hi)/2
h600,k600,i600,o600 = run(bj,600)
print(f"βj kalibriran = {bj:.6f}; REPLIKA 600: S_konec=({h600[-1][0]:.4f},{h600[-1][1]:.4f},{h600[-1][2]:.4f},{h600[-1][3]:.4f}) katarze={k600} izpust={i600:.4f} obrat={o600:.4f}")

ND=20000
h, kz, izpust, obrat = run(bj, ND)
Zf,Jf,Ef,Nf = h[-1]
perioda = sum(1 for Z,J,E,N in h[-100:] if Z*N > Th+1e-12)
print(f"REPLIKA {ND}: S_konec=(Z {Zf:.4f} · J {Jf:.4f} · E {Ef:.4f} · N {Nf:.4f}); E−J vezava = {Ef-Jf:.4f}; katarze={kz} (≈{kz/ND:.3f}/dih); perioda zadnjih 100: {perioda}/100; izpust={izpust:.4f}; obrat ven={obrat:.4f}")
# kratki + prvi ogenj
prva = next((i+1 for i,(Z,J,E,N) in enumerate(h) if Z*N>Th), None)
print(f"prva katarza @dih {prva}; N* izmerjeno={Nf:.4f} ⊥ analitično={Nstar:.4f} ΣAD={abs(Nf-Nstar):.1e}")

# TESSERAKT: z = Z>Z_trig(Θ/N*) · j = J>median(J) · e = E>median(E) · n = N>N*
import statistics
mJ = statistics.median([r[1] for r in h]); mE = statistics.median([r[2] for r in h])
def bits(s):
    Z,J,E,N=s; return (int(Z>Ztrig), int(J>mJ), int(E>mE), int(N>Nstar))
vid = {v:0 for v in range(16)}          # obiski oglišč
kzv = {v:0 for v in range(16)}         # katarze v oglišču (pred sprostitvijo)
edges = {}; diagonale = 0; prev=None
svertex=[None]*ND
for idx,s in enumerate(h):
    b=bits(s); v=b[0]*8+b[1]*4+b[2]*2+b[3]; svertex[idx]=v
    vid[v]+=1
    M=s[0]*s[3]
    if M>Th: kzv[v]+=1
    if prev is not None:
        d = bin(prev^v).count('1')
        if d==1:
            k=(min(prev,v),max(prev,v)); edges[k]=edges.get(k,0)+1
        elif d>1: diagonale+=1
    prev=v
naj_obisk = sorted(vid.items(), key=lambda kv:-kv[1])
print(f"\noglišča obiskana: {sum(1 for v in vid if vid[v]>0)}/16; robovi tesserakta pohojeni: {len(edges)}/32; diagonalni skoki: {diagonale}")
print("oglišča po obiskih (z,j,e,n · obiski · katarze):")
for v,c in naj_obisk[:8]:
    if c==0: break
    print(f"  ({v//8},{(v//4)%2},{(v//2)%2},{v%2}) id={v:2d} · {c:6d} dihov · katarz {kzv[v]}")
zacetno, končno = svertex[0], svertex[-1]
orbita = sorted(set(svertex[-200:]))
print(f"startno oglišče {zacetno}; končno {končno}; orbita zadnjih 200: {orbita}")
# robovi najbolj hojeni
top_edges = sorted(edges.items(), key=lambda kv:-kv[1])[:4]
print("najbolj hojeni robovi:", [(f"{a}↔{b}",c) for (a,b),c in top_edges])

out = {"beta_j": bj, "N_star": Nstar, "Z_star": Zstar, "Z_trig": Ztrig,
 "S600": list(h600[-1]), "S_konec": [Zf,Jf,Ef,Nf], "katarze_600": k600, "katarze_20000": kz,
 "prva_katarza_dih": prva, "perioda_zadnjih_100": perioda, "izpust": izpust, "obrat_ven": obrat,
 "E_minus_J": Ef-Jf, "median_J": mJ, "median_E": mE,
 "oglisca_obiskana": sum(1 for v in vid if vid[v]>0), "robovi_pohojeni": len(edges),
 "diagonale": diagonale, "obiski": {str(k):v for k,v in vid.items()}, "katarze_v_ogliscu": {str(k):v for k,v in kzv.items()},
 "robovi": {f"{a}-{b}":c for (a,b),c in edges.items()},
 "startno": zacetno, "konecno": končno, "orbita200": orbita}
Path("/home/user/tool-results/data-analysis/mithos-6278/rezultati-6278.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print("\nrezultati zapisani ⊢")
