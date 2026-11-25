#!/usr/bin/env python3
# spreobracnik-sintakse.py v1.0 — rod σ 7009 ⊙ UKZ ⟡ »ORODJA ZA SPREOBRAČANJE SINTAKSE!«
# korpusna sintaksa → gola besedilna oblika ; neznan znak ⟨ne⟩ molči, ga izpostavi ( trdilnikova norma )
import sys, re
MAPA = {"⊙":" po ukazu ", "⌇":" ; ", "∧":" in ", "⊥":" proti ", "⭢":" kandidat: ", "⚔":" izbor njegov ",
        "∂":" dolg ", "⊢":" priča: ", "σ":" rez ", "§":" člen ", "⇌":" primerja ", "⟨ne⟩":" ne ", "⟨NE⟩":" NE "}
def spremeni(vhod):
    izhod=[]; neznan={}
    for znak in vhod:
        if znak in MAPA: izhod.append(MAPA[znak]); continue
        cp=ord(znak)
        if znak in "⟨⟩«»": izhod.append(znak); continue
        if cp>0x2000 and not (0x2600<=cp<=0x27BF):
            neznan[hex(cp)]=neznan.get(hex(cp),0)+1
            if cp not in (0x1D799,): izhod.append(znak)
        elif cp>0x2500: neznan[hex(cp)]=neznan.get(hex(cp),0)+1; izhod.append(znak)
        else: izhod.append(znak)
    n="".join(izhod).replace("⟨","").replace("⟩","")
    return n, neznan
def samopreizkus():
    v1="⟨ZADNJI PEČAT⟩⊢( ⊙ ⟨NE-UGIBAJ⟩ 2690 )"
    o1,_=spremeni(v1)
    assert "priča:" in o1 and "po ukazu" in o1 and "2690" in o1, o1
    assert "⟨" not in o1 and "⟩" not in o1 and "⊢" not in o1 and "⊙" not in o1, o1
    v2="kura ⌇ ∂ ⭢ ⚔"
    o2,_=spremeni(v2)
    assert all(z not in o2 for z in "⌇∂⭢⚔"), o2
    for bes in ("kura"," ; "," dolg ","kandidat:"," izbor njegov"): assert bes in o2, (bes,o2)
    v3="⟨ne brusi⟩"
    o3,_=spremeni(v3); assert o3=="ne brusi", o3
    return True
if __name__=="__main__":
    if sys.argv[1:]==["--samopreizkus"]:
        samopreizkus(); print("ZELENO 3/3 ⊢"); sys.exit(0)
    t=sys.stdin.read() if len(sys.argv)<2 else open(sys.argv[1],encoding="utf-8").read()
    n,neznani=spremeni(t)
    sys.stdout.write(n)
    if neznani: print("\nNEZNANI ZNAKI ( izpostavljeni, ⟨ne⟩ molčeči ): "+", ".join(f"U+{k[2:].upper()}×{v}" for k,v in sorted(neznani.items())), file=sys.stderr)
