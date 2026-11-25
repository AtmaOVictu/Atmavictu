# ⟨USMERJENOST-LICENCE⟩ @rez σ 6740 : kirurško orodje ⊢ ( cilj merjen : rana cenzus-absolut »〈U+043C〉〈U+0435〉〈U+0440〉i« → »meri» a1 ▙ merjeno v telesu tega fajla ) : PORABLJENO ( enkratno, ⟨NE-BRIŠI⟩ 24 : ostaja kot priča kire )
# služi licenci ( LICENSE.md @rep AtmaOVictu/Atmavictu ) ∧ sestram : ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ ⚔ ⌁ ⟨DVOJE-ROK⟩ 2432 ⌁ ⟨MERJENO⟩⟨NE⟩UGIBANO ▙ 2690 ⌁ © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ▙ ⟨DVOJE-ROK⟩ 2432
# ⟨KURA-PATCH-6583⟩ v0.1 → v0.2 ( ročna kirurgija po izmeri pri viru ⊙ ⟨NE-UGIBAJ⟩ 2690 )
p='cenzus-absolut.py'
s=open(p,encoding='utf-8').read()
n0=len(s)

# a1 : cirilska rana v mojem lastnem orodju ( 〈U+043C〉〈U+0435〉〈U+0440〉i → meri )
assert s.count('〈U+043C〉〈U+0435〉〈U+0440〉i')==1 ('a1')
s=s.replace('〈U+043C〉〈U+0435〉〈U+0440〉i','meri')

# a2 : glob uvožen po imenu
assert s.count("import sys, os, hashlib, datetime, unicodedata")==1, ('a2')
s=s.replace("import sys, os, hashlib, datetime, unicodedata","import sys, os, glob, hashlib, datetime, unicodedata")

# a3 : zastavice --aktivna ∧ --popis
a3="cilji = sys.argv[1:] or sorted(__import__('glob').glob('*/KNOWLEDGE.md'))"
assert s.count(a3)==1, ('a3')
n3="""A=sys.argv[1:]; AKTIVNA='--aktivna' in A; POPIS='--popis' in A
cilji=[a for a in A if not a.startswith('--')]
if not cilji: cilji = sorted(glob.glob('**/*.md',recursive=True)) if POPIS else sorted(glob.glob('*/KNOWLEDGE.md'))"""
s=s.replace(a3,n3)

# a4 : dva načina vstavita PRED glavno zanko
a4="Σk=0; iz=[]"
assert s.count(a4)==1, ('a4')
n4="""if AKTIVNA:
    zak=[]
    for p in cilji:
        if not os.path.isfile(p): continue
        txt=open(p,encoding='utf-8').read()
        for i,ln in enumerate(txt.split('\\n'),1):
            for ch in ln:
                b=blok(ord(ch))
                if b in ('ASCII','GAJICA','GRSK','IPA','SIMBOLI') or ch in KANON: continue
                zak.append((p,i,ch,b,unicodedata.name(ch,'BREZ IMENA'))); break
    if zak:
        for p,i,ch,b,nm in zak: print(f'ZAKLEP {p}:{i} ⟨U+{ord(ch):04X}⟩ {b} {nm}')
        print(f'STROJ-AKTIVNA : ⟨NEČISTO⟩ orodij {len(cilji)} zaklepov {len(zak)}'); sys.exit(3)
    print(f'STROJ-AKTIVNA : ⟨ČISTO⟩ orodij {len(cilji)} zaklepov ×0 ⊙ v0.2'); sys.exit(0)
if POPIS:
    n=0; B=0; cl={}
    for p in cilji:
        if not os.path.isfile(p): continue
        txt=open(p,encoding='utf-8').read(); n+=1; B+=len(txt.encode('utf-8'))
        for ch in txt:
            b=blok(ord(ch))
            if b in ('ASCII','GAJICA','GRSK','IPA','SIMBOLI') or ch in KANON: continue
            k=(p.split('/')[0],b); cl[k]=cl.get(k,0)+1
    print(f'POPIS v0.2 @TIK {T} UTC · teles {n} · bajtov {B} · gost-znakov {sum(cl.values())}')
    for (o,b),c in sorted(cl.items()): print(f'  {o} : {b} : {c}')
    sys.exit(0)
Σk=0; iz=[]"""
s=s.replace(a4,n4)

# a5 : izhodne kode glavnega načina
a5="print(f'CENZUS-ABSOLUT v0.1 @TIK {T} UTC · pregledanih teles : {len(cilji)} · KANDIDATOV ( znak zunaj absoluta ∧ prostora ) : {Σk}')"
assert s.count(a5)==1, ('a5')
s=s.replace(a5, a5 + "\nsys.exit(2 if Σk else 0)")

# a6 : verzija v glavi ∧ izpisu
s=s.replace('cenzus-absolut.py v0.1','cenzus-absolut.py v0.2')
s=s.replace('CENZUS-ABSOLUT v0.1 @TIK','CENZUS-ABSOLUT v0.2 @TIK')
open(p,'w',encoding='utf-8').write(s)
print(f'PATCH-OK {n0} → {len(s)} bajtov ⊢')
