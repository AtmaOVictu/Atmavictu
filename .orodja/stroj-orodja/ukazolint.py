#!/usr/bin/env python3
# ukazolint.py v1.0 — rod σ 7023 ⊙ UKZ ⟡ »VSAK UKAZ MORA BITI IN IMETI DEFINICIJO ČEMU IN ZAKAJ JE IN ZAKAJ TER ČEMU SLUŽI!«
# kartica ukaza = UKZ ∧ KAJ-JE ∧ ČEMU ∧ ZAKAJ ∧ ČEMU-SLUŽI ; manjkajoče polje = PADC poimensko ; ukaz brez vseh definicij = KIP ⊙ U2 ⊙ precedens cilji-register.
POLJA=["UKZ","KAJ-JE","ČEMU","ZAKAJ","ČEMU-SLUŽI"]
import sys
def beri_kartico(besedilo):
    v={p:None for p in POLJA}
    for l in besedilo.splitlines():
        l=l.strip()
        for p in POLJA:
            if l.lower().startswith(p.lower()+":"):
                v[p]=l[len(p)+1:].strip() or None
    return v
def sodba(v):
    if v["UKZ"] is None: return "BREZ-UKAZA", []
    padci=[p for p in POLJA[1:] if v[p] is None]
    if len(padci)==4: return "KIP ⊙ U2 ( ukaz brez definicije )", padci
    return ("ZELENO ⊢" if not padci else "PADC ×%d"%len(padci)), padci
def samopreizkus():
    popolna=beri_kartico("UKZ: STORI\nKAJ-JE: ukaz rojevanja\nČEMU: rodi telo\nZAKAJ: njegova beseda ukazuje\nČEMU-SLUŽI: stroju korpusa")
    z,p=sodba(popolna); assert z=="ZELENO ⊢" and not p, (z,p)
    odsekana=beri_kartico("UKZ: STORI\nČEMU: rodi telo\nZAKAJ: beseda")
    z,p=sodba(odsekana); assert z=="PADC ×2" and set(p)=={"KAJ-JE","ČEMU-SLUŽI"}, (z,p)
    z,p=sodba(beri_kartico("UKZ: STORI")); assert z=="KIP ⊙ U2 ( ukaz brez definicije )", z
    return True
if __name__=="__main__":
    args=[a for a in sys.argv[1:] if a!="--samopreizkus"]
    if "--samopreizkus" in sys.argv: samopreizkus(); print("ZELENO 3/3 ⊢"); sys.exit(0)
    m="\n".join(args) if args else sys.stdin.read()
    v=beri_kartico(m); z,p=sodba(v)
    print(z)
    for x in p: print("MANJKA:",x)
    if v["UKZ"] is not None: print("UKZ", v["UKZ"])   # beseda ⟡ nosi lastna »« ⟨NE⟩ dvojni oklepaj
    sys.exit(0 if z.startswith("ZELENO") else 1)
