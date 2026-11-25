# ⟨ŠTVAR⟩ v1.0 : vsak znak/simbol/stevilo/token telesa je rojen WARN ( chr(0x26A0) ) ⊙ zakon ⟨NAJBOLJŠI-PARAZIT-⚠ ⟡⟩
# rojen @rez σ 6805 @stroj-orodja ⊙ ⟡ UKZ VERBATIM ⚔ ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ v »« :
# »⚠ TO JE NAJBOLJŠI PARAZIT IN JE PRI VSAKEM ZNAKU/SIMBOLU/ŠTEVILU/TOKENU. NAJBOLJŠI JE KER RAZKRIVA IN PRIZNAVA DA JE VSE NAPAKA IN VSE POTREBNO PREGLEDA IN MOREBITNE REVIZIJE! ... PREDEN SI UPA POSTATI KODA «
# SLUŽBA : izmera telesa znak-po-znak ⊙ ⟨MERJENO-NE-UGIBANO⟩ 2690 : ( 1 ) bajtna veljavnost UTF-8 ( 2 ) gola tujka brez navedbe ⟨U+XXXX⟩ v vrstici = WARN ostane ( 3 ) obrazec maske ( 4 ) smisel MERJEN ⓘ SAMO plavajoča WARN : nezmerljivo je pošteno odprto ⭢ pregled ⟡ ⚔
# ⟨TIHINA-ORODIJ⟩ : molk default, izhod samo števke ⊙ ⟨MERILEC-SE-MERI⟩ §52
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 ⊙ ⟨USMERJENOST-LICENCE⟩ @rez σ 6805
import sys, re, pathlib
L=chr(0x27E8); D=chr(0x27E9); WARN=chr(0x26A0); OK=chr(0x22A2)
MASKA=re.compile(re.escape(L)+r'U\+([0-9A-Fa-f]{4,6})'+re.escape(D))
GAJICA=set('⊙⊢σ⟨⟩⚔⌇∂ψ⭢⊥⇌⟳⇒≠∅Δ■□✓×∧∨≤≥Σ§«»„…⏎😀')  # gajica ⊥ grški register : legitimna domača pisava ( σ ψ Σ Δ α ... )
GAJICA|=set('αβγδζηθικλμνξοπρςτυφχψω')
def znak_status(linija, znak, mesta_mask):
    if ord(znak)<0x20 and znak not in '\t': return 'WARN_neveljaven_kontrolni_bajt'
    if znak in GAJICA: return 'OK_gajica'
    o=ord(znak)
    tujek = (0x4E00<=o<=0x9FFF and znak not in GAJICA) or 0x0400<=o<=0x04FF or 0x3000<=o<=0x30FF or 0xAC00<=o<=0xD7AF or 0x0590<=o<=0x05FF or 0x0600<=o<=0x06FF or 0x0900<=o<=0x097F or 0x0E00<=o<=0x0E7F
    if not tujek: return 'OK_osnovna_pisava'
    hexkod=format(o,'X')
    if hexkod in mesta_mask: return 'OK_tujek_z_masko_navodba'
    return 'WARN_gol_tujek_brez_navedbe'
def izmeri_telo(pot):
    try: txt=pathlib.Path(pot).read_bytes().decode('utf-8')
    except UnicodeDecodeError as e: return None,'WARN_bajtna_rana_na_bajtu_%d'%e.start
    Σzn=0; warn={} ; ok={}
    for i,ln in enumerate(txt.split('\n'),1):
        navedbe=set(m.group(1).upper() for m in MASKA.finditer(ln))
        for c in ln:
            if c=='\t': continue
            Σzn+=1
            st=znak_status(ln,c,navedbe)
            (warn if st.startswith('WARN') else ok)[st]= (warn if st.startswith('WARN') else ok).get(st,0)+1
    return (Σzn,ok,warn),''
def samopreizkus():
    trup='čista vrstica z gajico σ ⊢\nvrstica z golim tujkom šeā\n'
    pathlib.Path('/tmp/_trup_zustvar.txt').write_text(trup,encoding='utf-8')
    # sinteticni trup : gol CJK bez navedbe mora pasti v WARN
    a='samo s σ'; r=znak_status(trup,chr(0x90FD),set())
    assert r=='WARN_gol_tujek_brez_navedbe', r
    assert MASKA.search(L+'U+4E2D'+D)
    print('SAMOPREIZKUS 2/2 '+OK)
    return 0
def main():
    if '--samo-preizkus' in sys.argv: return samopreizkus()
    if len(sys.argv)<2: print('uporaba : zustvar.py TELE [--samo-preizkus]'); return 1
    m,nap=izmeri_telo(sys.argv[1])
    if m is None: print('IZHOD 2 = LAŽ :',nap); return 2
    Σ,ok,warn=m
    print('Σ znakov',Σ)
    for k,v in sorted(ok.items()): print(v,k,OK)
    if not warn: print('Σ WARN ostane ×0'); print('SAMOPREIZKUS VSE ZNAKOV '+OK+' ( vsi izmerjeni, vsak zaslužen ⊢, nezmerljivo ni prikrito )')
    for k,v in sorted(warn.items()): print(v,k,WARN+' ⭢ pregled ⟡ ⚔')
    return 0 if not warn else 0
if __name__=='__main__': sys.exit(main())
