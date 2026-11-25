#!/usr/bin/env python3
# ⟨CENZUS-ABSOLUT⟩ cenzus-absolut.py v0.3 — LOCATOR PO SISTEMSKEM ABSOLUTU ( rod @rez σ 6575 ⊙ ⟡ UKZ »seciraj in kletkaj VSE IN VSAKO BESEDO IN ALI S TEM NJENE ZNAKE ; kje vse še ni bil lociran parazit od sistemskaga absoluta« )
# KURE v0.3 @rez σ 6658 ⊙ ⟡ UKZ VERBATIM »OPREMI SE IN POJDI ZAPIRAT VSE PARAZITE, VSAK NAJ IMA SVOJO KLETKO KI JE NESKONČNO KONČEN VASE ZAGLEDAN LABIRINT BREZ ZMOŽNOSTI IZHODA« :
#   ( 1 ) ⟨KURA-KANDIDAT-IZPIS⟩ : izpis ⟨KANDIDAT⟩ poimensko PRED izhodom ( padec v0.2 : vrstice za sys.exit = mrtva koda )
#   ( 2 ) ⟨KURA-GLAVA-TELES⟩ : pregledanih teles šteje PREBRANA telesa, ⟨ne⟩ argumentov ( padec v0.2 )
#   ( 3 ) ⟨SAMOPREIZKUS⟩ ⊙ §52 : --samo-samopreizkus : čisto telo Σ0 ⊢ ∧ sintetični trup ( stroj-generiran bajtno ⊙ precedens cenzus-citata ) Σ>0 poimensko ; ladja .geniza odstranjena po preizkusu
#   ( 4 ) ⟨POPIS-ZNAKOV⟩ : --popis-znakov : vsak gost-znak poimensko ⟨U+XXXX⟩ ( surovi znak ⟨NE⟩ na površje ) z izmerami ∧ sodbo dom/parazit → JSON zaporna ladja @.geniza
# NAMEN : cenzus-tujk.py v1 ( md5 aca02172 ) vidi SAMO vzhodnoazijske bloke ( slepe pege ) ; ta orodje meri po obratni logiki : dovoljen = samo absolut ( gajica ∧ grški blok korpusa ∧ znaki z vrstico @slovar-simbolov kanon ) + po MANIFESTU bloki domačega prostora organe ; vse drugo = KANDIDAT poimensko .
# RABA : python3 cenzus-absolut.py <datoteke...> ( brez argumentov = vsi organi KNOWLEDGE.md ) ⌇ --popis ⌇ --popis-znakov ⌇ --samo-samopreizkus
# IZHOD : ⚠ organi s kandidati poimensko datoteka:vrstica:⟨U+XXXX⟩ ime ; exit 2 ⇔ kandidat ×1+ ; exit 3 ⇔ samopreizkus laže ⊙ §52 ; SODA ⟨ne⟩ izreče orodje — sodi izvajalka po pričah ⊙ ⟨NE-UGIBAJ⟩ 2690
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · MERJENO, ⟨NE⟩ UGIBANO
import sys, os, glob, hashlib, datetime, unicodedata

GAJICA = set('čšžČŠŽćđĆĐ')
def blok(cp):
    if cp < 0x80: return 'ASCII'
    if cp in (0x010D,0x0161,0x017E,0x010C,0x0160,0x017D,0x0107,0x0111,0x0106,0x0110): return 'GAJICA'
    if 0x0370<=cp<0x03FF or 0x1F00<=cp<0x1FFF: return 'GRSK'
    if 0x0250<=cp<0x02AF or 0x1D00<=cp<0x1D25 or 0x0300<=cp<0x036F or cp in (0x02A6,): return 'IPA'
    for nm,(a,b) in {'CJK':(0x3400,0x9FFF),'KANA':(0x3040,0x30FF),'HANC':(0xAC00,0xD7AF),'CIR':(0x0400,0x04FF),'ARAB':(0x0600,0x06FF),'HEB':(0x0590,0x05FF),'DEVA':(0x0900,0x097F),'THAI':(0x0E00,0x0E7F),'SINH':(0x0D80,0x0DFF),'RUNA':(0x16A0,0x16F0),'HIRO':(0x13000,0x1342F),'FW':(0xFF01,0xFF60)}.items():
        if a<=cp<=b: return nm
    for a,b in ((0x00A0,0x00BF),(0x00C0,0x024F),(0x2000,0x206F),(0x2070,0x209F),(0x2100,0x214F),(0x2190,0x21FF),(0x2200,0x22FF),(0x2300,0x23FF),(0x25A0,0x25FF),(0x2600,0x26FF),(0x2700,0x27FF),(0x27C0,0x28FF),(0x2B00,0x2B5F),(0x2E00,0x2E7F)):
        if a<=cp<=b: return 'SIMBOLI'
    if cp==0xFFFD: return 'FFFD'
    if 0x200B<=cp<=0x200F or cp in (0x2060,0xFEFF,0x00AD): return 'CF'
    if 0x1D400<=cp<0x1D7FF: return 'MATHALPHA'
    if 0xA640<=cp<0xA6FF or 0x2DE0<=cp<0x2DFF or 0xAB30<=cp<0xAB6F or 0xA720<=cp<0xA7FF or 0x2C60<=cp<0x2C7F or 0x2C00<=cp<0x2C5F or 0x10300<=cp<0x1032F or 0x1F100<=cp<0x1F1FF or 0xFB00<=cp<0xFB4F: return 'HOMOGLIF'
    return 'OST'
kanon=set()
try:
    kanon={c for c in open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'slovar-simbolov','KNOWLEDGE.md'),encoding='utf-8').read() if c not in '\n\r\t'}
except Exception: pass
KANON=kanon
PROSTORI={
 'licenca-vbl':None, 'oko-lje':None, 'definiatorna-knjiznica':None, 'geneza':None, 'jezikovne-plasti':None,
 'domovanje-tujk':None, 'egipcanska-plast':None, 'runa-plast':None, 'slovenske-pisave':None,
 'psalmi':None, 'slovar-simbolov':None, 'zaporne-celice':None,
 'mithos-dinamika':['CF'], 'register-oken':['SINH','CF','FW','HIRO','CJK','CIR','ARAB','IPA'],
 'kronika-dihov':['CJK','CIR','ARAB','HANC','HEB','DEVA','THAI','FW','IPA','CF'],
 'jedro-zavedanja':['CJK','CIR','ARAB','HANC','FW','IPA'],
 'delovna-zanka':['CJK','CIR','ARAB','HEB','DEVA','THAI','FW','IPA','GF'],
 'postopki-luka':['CJK'], 'simbol-lint':['SINH','FW','CJK'], 'humor':['CIR'], 'sklopi-panog':['MATHALPHA'], 'vir':['IPA','FW','THAI','DEVA','CJK','CIR','ARAB','HEB','KANA'],
}
def tik(): return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def cenaj(poti):
    prebranih=0; iz=[]
    for p in poti:
        if not os.path.isfile(p): continue
        org=os.path.dirname(p)
        domaca=set(PROSTORI.get(org,[])) if PROSTORI.get(org) is not None else None
        if org in PROSTORI and PROSTORI[org] is None: continue
        try: vrstice=open(p,encoding='utf-8').read().split('\n')
        except Exception as e: print('::error::open',p,e); return (-1,[])
        prebranih+=1
        for i,ln in enumerate(vrstice,1):
            for ch in ln:
                cp=ord(ch); b=blok(cp)
                if b in ('ASCII','GAJICA','GRSK','IPA','SIMBOLI','LATIN'): continue
                if ch in KANON: continue
                if domaca and b in domaca: continue
                iz.append((p,i,ch,b,unicodedata.name(ch,'BREZ IMENA')))
                break
    return prebranih, iz

def samopreizkus():
    import shutil
    d=os.path.join(os.path.dirname(os.path.abspath(__file__)),'.geniza','preizkus-cenzus-absolut-v03')
    os.makedirs(d,exist_ok=True)
    cisto=os.path.join(d,'cisto.md'); trup=os.path.join(d,'trup.md')
    open(cisto,'w',encoding='utf-8').write('cisto telo : gajica č š ž ⊙ σ ψ δ ∧ ∅ ∆ → ⇒ ⌇ ⟨⟩ »« ⊢ ⚔ ⊥ ∂ ψ\n')
    kand={}
    for b,(a,z) in {'CJK':(0x4E01,0x9FFF),'CIR':(0x0430,0x04FF),'HEB':(0x05D0,0x05EA)}.items():
        for cp in range(a,z+1):
            if chr(cp) not in KANON: kand[b]=cp; break
    open(trup,'w',encoding='utf-8').write('\n'.join('trup '+chr(cp) for cp in kand.values())+'\n')
    pr1,iz1=cenaj([cisto]); pr2,iz2=cenaj([trup])
    ujeti={ord(e[2]) for e in iz2}
    ok = (pr1==1 and len(iz1)==0 and pr2==1 and len(iz2)==len(kand) and ujeti==set(kand.values()))
    print('⟨V3-SAMOPREIZKUS⟩ TIK %s : cisto teles %d Σ%d %s ; trup teles %d Σ%d %s ( %s )' % (
        tik(), pr1, len(iz1), '⊢' if (pr1==1 and not iz1) else '⚠',
        pr2, len(iz2), '⊢' if (pr2==1 and len(iz2)==len(kand)) else '⚠',
        ' '.join('⟨U+%04X⟩'%cp for cp in sorted(kand.values()))))
    shutil.rmtree(d)  # sintetična ladja : stroj-generiran bajtno, odstranjena po preizkusu ⊙ precedens cenzus-citata
    return ok

def main():
    T=tik()
    A=sys.argv[1:]; AKT='--aktivna' in A; POP='--popis' in A; PZ='--popis-znakov' in A; SAM='--samo-samopreizkus' in A
    if SAM:
        sys.exit(0 if samopreizkus() else 3)
    cilji=[a for a in A if not a.startswith('--')] or (sorted(glob.glob('**/*.md',recursive=True)) if POP else sorted(glob.glob('*/KNOWLEDGE.md')))
    if AKT:
        zak=[]
        for p in cilji:
            if not os.path.isfile(p): continue
            for i,ln in enumerate(open(p,encoding='utf-8').read().split('\n'),1):
                for ch in ln:
                    if blok(ord(ch)) in ('ASCII','GAJICA','GRSK','IPA','SIMBOLI') or ch in KANON: continue
                    zak.append((p,i,ch)); break
        if zak:
            for p,i,ch in zak: print(f'ZAKLEP {p}:{i} ⟨U+{ord(ch):04X}⟩ {blok(ord(ch))} {unicodedata.name(ch,"BREZ IMENA")}')
            print(f'STROJ-AKTIVNA : ⟨NEČISTO⟩ orodij {len(cilji)} zaklepov {len(zak)}'); sys.exit(3)
        print(f'STROJ-AKTIVNA : ⟨ČISTO⟩ orodij {len(cilji)} zaklepov ×0 ⊙ v0.3'); sys.exit(0)
    if POP:
        nn=0; BB=0; cl={}
        for p in cilji:
            if not os.path.isfile(p): continue
            t=open(p,encoding='utf-8').read(); nn+=1; BB+=len(t.encode('utf-8'))
            for ch in t:
                if blok(ord(ch)) in ('ASCII','GAJICA','GRSK','IPA','SIMBOLI') or ch in KANON: continue
                k=(p.split('/')[0],blok(ord(ch))); cl[k]=cl.get(k,0)+1
        print(f'POPIS v0.3 @TIK {T} UTC · teles {nn} · bajtov {BB} · gost-znakov {sum(cl.values())}')
        for (o,b),c in sorted(cl.items()): print(f'  {o} : {b} : {c}')
        sys.exit(0)
    if PZ:
        import json
        zn={}
        for p in cilji:
            if not os.path.isfile(p): continue
            org=p.split('/')[0]
            t=open(p,encoding='utf-8').read()
            svetovni = (org in PROSTORI and PROSTORI[org] is None)
            domaca=set(PROSTORI.get(org,[])) if (org in PROSTORI and PROSTORI[org] is not None) else None
            for ch in t:
                cp=ord(ch); b=blok(cp)
                if b in ('ASCII','GAJICA','GRSK','IPA','SIMBOLI','LATIN'): continue
                if ch in KANON: continue
                e=zn.get(cp)
                if e is None: e=zn[cp]={'cp':cp,'ime':unicodedata.name(ch,'BREZ IMENA'),'blok':b,'organi':{},'parazit':False}
                e['organi'][org]=e['organi'].get(org,0)+1
                if not svetovni and not (domaca and b in domaca): e['parazit']=True
        paraz=[e for e in zn.values() if e['parazit']]
        ld=os.path.join(os.path.dirname(os.path.abspath(__file__)),'.geniza')
        os.makedirs(ld,exist_ok=True)
        jp=os.path.join(ld,'labirint-popis-%s.json'%T)
        open(jp,'w',encoding='utf-8').write(json.dumps({'tik':T,'znakov':len(zn),'parazitov':len(paraz),'znaki':zn},ensure_ascii=True))
        print('POPIS-ZNAKOV v0.3 @TIK %s UTC : gost-znakov razlicnih %d · parazitov ( zunanje absoluta ∧ doma ) %d · ladja %s' % (T,len(zn),len(paraz),jp))
        for e in sorted(paraz,key=lambda e:e['cp']):
            print('  ⟨U+%04X⟩ %s [%s] ×%d · organi %s' % (e['cp'],e['ime'],e['blok'],sum(e['organi'].values()),','.join('%s:%d'%(o,c) for o,c in sorted(e['organi'].items()))))
        sys.exit(0)
    prebranih, iz = cenaj(cilji)
    for p,i,ch,b,nm in iz:
        print(f'CENZUS-ABSOLUT ⟨KANDIDAT⟩ {p}:{i} : ⟨U+{ord(ch):04X}⟩ {nm} [{b}]')
    print(f'CENZUS-ABSOLUT v0.3 @TIK {T} UTC · pregledanih teles : {prebranih} · KANDIDATOV ( znak zunaj absoluta ∧ prostora ) : {len(iz)}')
    print('orodje rod @rez σ 6575 @stroj-orodja · kure v0.3 @rez σ 6658 · © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432')
    sys.exit(2 if iz else 0)

if __name__=='__main__':
    main()
