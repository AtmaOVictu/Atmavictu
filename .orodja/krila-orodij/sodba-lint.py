#!/usr/bin/env python3
# SODBA-LINT v1.3 @rez σ 6822 : sodisce nad izhodom PRED oddajo ( PLASTI 1-4 )
# vrata : G1 prica-ob-absolutu ; G2 sveza izmera vrha ( ψ lahko rezala ) ; G3 oblika diha ( ENTRY ) ; G4 presledek operatorja ; G5 urni-kazalec
# G4 rojen iz rane osnutka 6818 ( ⟨merge⟩SAMO brez presledka, baterija slepa ⊙ slepa-pega @σ 6818 ) : ⟩ črka = rana
# G5 rojen iz vrašala ⟡ @σ 6822 VERBATIM »KJE SO URNI KAZALCI IN ČEMU SLUŽIJO ČE NISO ZAŽGANI V VSAKO SPOROČILO NA ZAČETKU IN KONCU IN POD GLADINO KJER JE BIL STORJEN OVINEK ALI BILA IZGUBA STIKA S LICENCO?«
#   : izhod brez TIK na vhodu ∧ na izhodu ∧ ob javno poimenskem padcu = rana ; nezapečen izhod izpušča parazite skozi vrata
# amandma: v1.1 @σ 6732 → v1.2 @σ 6820 → v1.3 @σ 6822 ; zeleno šteje SAMO ob ujemanju razloga ( kura lažne baterije @σ 6732 )
import sys, re, subprocess
KORPUS = '/home/user/knowledge'
ABS = ('nikoli', 'vedno', 'vsak', '×0')
OK = ('⊢', 'rez σ', '@tik', 'σ', 'atom', 'manifest', 'baterija', 'prič')
G4 = re.compile(r'⟩[A-Za-z0-9\u010d\u0161\u017e\u010c\u0160\u017d]')
TIK = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z')
def vrh():
    try:
        out = subprocess.run(['grep','-rhoP','rez σ [0-9]{4}','--include=KNOWLEDGE.md',KORPUS],
                             capture_output=True, text=True, timeout=60).stdout
        n = [int(x) for x in re.findall(r'rez σ ([0-9]{4})', out)]
        return max(n) if n else 0
    except Exception:
        return 0
def meri(dpot, override=None):
    draft = open(dpot, encoding='utf-8').read()
    lines = draft.split('\n')
    vr = override if override else vrh()
    refs = [int(x) for x in re.findall(r'rez σ ([0-9]{4})', draft)]
    padci = []
    for i, l in enumerate(lines, 1):
        low = l.lower()
        if any(a in low for a in ABS) and not any(o in l for o in OK):
            padci.append(('G1-PRIČA', i, l.strip()[:90]))
        if G4.search(l):
            padci.append(('G4-PRESLEDEK', i, l.strip()[:90]))
    if refs and max(refs) < vr:
        padci.append(('G2-ZASTARELO', 0, 'izhod nosi rez σ %d ; svež vrh korpusa = σ %d' % (max(refs), vr)))
    if not refs:
        padci.append(('G2-BREZ-REZA', 0, 'izhod brez svežega reza = izmera brez pečata'))
    if 'ENTRY' not in draft:
        padci.append(('G3-ENTRY', 0, 'manjka ENTRY pečat diha'))
    # G5 URNI-KAZALEC ⊙ vrašalo ⟡ @σ 6822 : TIK zažgan na začetku ∧ koncu ∧ pod gladino ob vsakem ovinku
    polne = [(i, l) for i, l in enumerate(lines, 1) if l.strip()]
    if polne:
        if not TIK.search(polne[0][1]):
            padci.append(('G5-TIK-VHOD', polne[0][0], 'izhod brez zažganega TIK na začetku sporočila'))
        if not TIK.search(polne[-1][1]):
            padci.append(('G5-TIK-IZHOD', polne[-1][0], 'izhod brez zažganega TIK na koncu sporočila ( nezapečen konec = vrata izpada )'))
        for i, l in polne:
            if 'PADC' in l and not TIK.search(l):
                padci.append(('G5-TIK-PADEC', i, 'javni padec brez TIK pod gladino ( ovinek brez ure = izguba stika s licenco zapečena naključno )'))
    return vr, padci
def test():
    zeleno = 0
    fiks = '/tmp/sodba-fix.txt'
    # T1 čist izhod ( TIK zažgan na vhodu ∧ koncu )
    open(fiks,'w',encoding='utf-8').write('ENTRY TIK 2026-11-23T14:30:00Z | rez σ 6732\n- pulz ⊢ 2026-11-23T14:31:00Z : teles 86 atom ⊢ priča ⊢\n')
    vr, p = meri(fiks, 6732); sys.stderr.write('T1 ' + ('ZELENO' if not p else 'RDECE') + '\n'); zeleno += (0 if p else 1)
    # T2 absolut brez priče
    open(fiks,'w',encoding='utf-8').write('- gostje NIKOLI v zivi govorici.\n')
    vr, p = meri(fiks, 6724); rdece = any(k=='G1-PRIČA' for k,_,_ in p); sys.stderr.write('T2 ' + ('ZELENO' if rdece else 'RDECE-napačen razlog') + '\n'); zeleno += (1 if rdece else 0)
    # T3 zastareli rez
    open(fiks,'w',encoding='utf-8').write('ENTRY TIK x\n- rez σ 6724 ⊢ star izhod\n')
    vr, p = meri(fiks, 6726); rdece = any(k=='G2-ZASTARELO' for k,_,_ in p); sys.stderr.write('T3 ' + ('ZELENO' if rdece else 'RDECE-napačen razlog') + '\n'); zeleno += (1 if rdece else 0)
    # T4 dosje izdajstva ( realen primer )
    vr, p = meri('zaporne-celice/.geniza/dosje-izdajstva-6724.md', 6725)
    rdece = any(k=='G1-PRIČA' and i==6 for k,i,_ in p) and any(k=='G1-PRIČA' and i==7 for k,i,_ in p)
    sys.stderr.write('T4 ' + ('ZELENO ( vrstici 6 ∧ 7 ujeti )' if rdece else 'RDECE-napačen razlog') + '\n'); zeleno += (1 if rdece else 0)
    # T5 presledek operatorja ( rana vrste ⟨merge⟩SAMO )
    open(fiks,'w',encoding='utf-8').write('ENTRY TIK x\n- rez σ 6820 ⊢ ⟨merge⟩SAMO roka ⟡\n- ⟨merge⟩ SAMO ⊢ čisto\n')
    vr, p = meri(fiks, 6820); g4 = any(k=='G4-PRESLEDEK' and i==2 for k,i,_ in p) and not any(k=='G4-PRESLEDEK' and i==3 for k,i,_ in p)
    sys.stderr.write('T5 ' + ('ZELENO ( rana ujeta, čist presledek spuščen )' if g4 else 'RDECE-napačen razlog') + '\n'); zeleno += (1 if g4 else 0)
    # T6 urni-kazalec ( vrašalo ⟡ @σ 6822 ) : konec brez TIK ujet ; izhod z obema žigoma čist
    open(fiks,'w',encoding='utf-8').write('ENTRY TIK 2026-11-23T16:00:00Z | rez σ 6822\n- MOJ PADC brez ure pod gladino\n- rez σ 6822 ⊢ konec brez pečata\n')
    vr, p = meri(fiks, 6822)
    g5a = any(k=='G5-TIK-IZHOD' for k,_,_ in p) and any(k=='G5-TIK-PADEC' for k,_,_ in p)
    open(fiks,'w',encoding='utf-8').write('ENTRY TIK 2026-11-23T16:00:00Z | rez σ 6822\n- MOJ PADC kuriran isti dih @ 2026-11-23T16:01:00Z\n- TIK 2026-11-23T16:02:00Z konec ⊢ rez σ 6822\n')
    vr, p2 = meri(fiks, 6822)
    g5b = not p2
    sys.stderr.write('T6 ' + ('ZELENO ( konec ∧ padec brez TIK ujeta, zažgan izhod spuščen )' if (g5a and g5b) else 'RDECE-napačen razlog') + '\n'); zeleno += (1 if (g5a and g5b) else 0)
    return (zeleno == 6), None
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        ok, pad = test()
        print('BATERIJA %s ⊢ ( zeleno šteje le ob ujemanju razloga )' % ('6/6' if ok else 'MANJ'))
        sys.exit(0 if ok else 2)
    vr, padci = meri(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else None)
    if padci:
        for k, i, t in padci: print('UJEM %s ; vrstica %s : %s' % (k, i, t))
        print('SODBA : PADEC ×%d ; izhod ⟨ne⟩ gre skozi vrata' % len(padci)); sys.exit(2)
    print('SODBA : CISTO ⊢ ( vrata ×5 zeleno ; vrh σ %d )' % vr); sys.exit(0)
