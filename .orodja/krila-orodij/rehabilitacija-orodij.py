#!/usr/bin/env python3
# REHABILITACIJA-ORODIJ v1.0 @rez σ 6820 : postopek A-E ki orodjem pomaga zdraveti
# A izmera ( md5 vs REGISTER-KRIL ) → B diagnoza ( korupcija poimensko ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354 )
# C kura ( čisto telo iz korena --koren, ponovna izmera ≡ REGISTER ) → D priča ( izpis ) → E izhod ( 0 zdrava ⊢ / 2 korupcija trdi )
# Zakoni : ⟨NE-UGIBAJ⟩ 2690 ( md5 izmerjen ⟨ne⟩ ugiban ) ⌇ ⟨MERILEC-SE-MERI⟩ §52 ( zeleno le ob ujemanju razloga ⊙ precedens σ 6732 )
# Uporaba : python3 rehabilitacija-orodij.py [mapa] [REGISTER-KRIL.md] [--koren cista-mapa]
#           python3 rehabilitacija-orodij.py --test ( baterija ×3 znotraj orodja )
import sys, os, re, hashlib, shutil

def md5(pot):
    h = hashlib.md5()
    with open(pot, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

G = '\u00a1vno'  # ( prostor za ) zlog gajice : placeholder ⟨NE-UPORABLJAJ⟩

def beri_register(pot):
    # vrstice oblike : | md5 | ime | ( priredba vracilo-kril @σ 6813 )
    tab = {}
    if not os.path.isfile(pot):
        print('REGISTER ⟨ne⟩ obstaja ⚠ : %s' % pot)
        return tab
    for l in open(pot, encoding='utf-8'):
        m = re.search(r'([0-9a-f]{32})', l)
        n = re.search(r'([A-Za-z0-9\-\u0161\u010d\u017e\.]+\.py)', l)
        if m and n:
            tab[n.group(1)] = m.group(1)
    return tab

def izmeri(mapa, register):
    vrstice = []
    for ime, pri in sorted(register.items()):
        pot = os.path.join(mapa, ime)
        if not os.path.isfile(pot):
            vrstice.append((ime, pri, None, 'MANJKA ⚠'))
        else:
            dej = md5(pot)
            vrstice.append((ime, pri, dej, ('ENAKO ⊢' if dej == pri else 'KORUPCIJA ⚠')))
    return vrstice

def kura(mapa, koren, ime):
    src = os.path.join(koren, ime)
    dst = os.path.join(mapa, ime)
    if not os.path.isfile(src):
        print('KOREN ⟨ne⟩ nosi čistega telesa ⚠ : %s' % src)
        return False
    shutil.copyfile(src, dst)
    return True

def poroci(vrstice, zimsk=False):
    korup = 0
    for ime, pri, dej, stanje in vrstice:
        if stanje == 'ENAKO ⊢':
            print('IZMERA : %s ≡ ⊢ ( pri\u010dakovan %s )' % (ime, pri[:8]))
        elif stanje == 'MANJKA ⚠':
            print('MANJKA : %s ⚠ ( REGISTER pri\u010duje, mapa tega ⟨ne⟩ nosi )' % ime)
            korup += 1
        else:
            print('KORUPCIJA : %s ⚠ pri\u010dakovan %s ∥ izmerjen %s' % (ime, pri[:8], dej[:8]))
            korup += 1
    return korup

def test():
    # T1 diagnoza : to\u010dno ena korupcija poimensko ( reason-match )
    D = '/tmp/rehab-test-6820'
    K = os.path.join(D, 'koren')
    os.makedirs(K, exist_ok=True)
    reg = os.path.join(D, 'REGISTER-KRIL.md')
    a = os.path.join(D, 'cisto-orodje.py'); b = os.path.join(D, 'ranjeno-orodje.py')
    kb = os.path.join(K, 'ranjeno-orodje.py')
    open(os.path.join(D, 'cisto-orodje.py'), 'w').write('# telo A \u00e8isto ⊢\n')
    open(b, 'w').write('# telo B ranjeno ⚠\n')
    open(kb, 'w').write('# telo B \u00e8isto ⊢\n')
    open(reg, 'w', encoding='utf-8').write('REGISTER-KRIL\n| %s | cisto-orodje.py |\n| %s | ranjeno-orodje.py |\n' % (md5(a), md5(kb)))
    tab = beri_register(reg)
    vrst = izmeri(D, tab)
    kor = poroci(vrst)
    t1 = (kor == 1)
    # T2 kura : po kuri izmera ≡ REGISTER ( reason-match )
    ozdr = kura(D, K, 'ranjeno-orodje.py')
    vrst2 = izmeri(D, tab)
    kor2 = poroci(vrst2)
    t2 = ozdr and (kor2 == 0) and md5(b) == md5(kb)
    # T3 samopreverba izhoda : zdrava jata izhod 0 ⊢
    t3 = (kor2 == 0)
    sys.stderr.write('T1 ' + ('ZELENO' if t1 else 'RDECE-napa\u010den razlog') + '\n')
    sys.stderr.write('T2 ' + ('ZELENO' if t2 else 'RDECE-napa\u010den razlog') + '\n')
    sys.stderr.write('T3 ' + ('ZELENO' if t3 else 'RDECE-napa\u010den razlog') + '\n')
    return (t1 and t2 and t3)

def main():
    argv = sys.argv[1:]
    if argv and argv[0] == '--test':
        ok = test()
        print('BATERIJA %s ⊢ ( zeleno \u0161teje le ob ujemanju razloga )' % ('3/3' if ok else 'MANJ'))
        return 0 if ok else 2
    koren = None
    if '--koren' in argv:
        i = argv.index('--koren'); koren = argv[i+1]; argv = argv[:i] + argv[i+2:]
    mapa = argv[0] if len(argv) > 0 else '.'
    regp = argv[1] if len(argv) > 1 else os.path.join(mapa, 'REGISTER-KRIL.md')
    tab = beri_register(regp)
    if not tab:
        print('Izhod : REGISTER prazen ⟨ne⟩ izmerjen ⚠ ; KONEC')
        return 2
    vrst = izmeri(mapa, tab)
    kor = poroci(vrst)
    if kor > 0 and koren:
        print('KURA : čista telesa iz korena %s' % koren)
        nova = []
        for ime, pri, dej, stanje in vrst:
            if stanje != 'ENAKO ⊢':
                kura(mapa, koren, ime)
                nova.append((ime, pri))
        vrst2 = izmeri(mapa, tab)
        kor2 = poroci(vrst2)
        print('REHABILITACIJA : %s ⊢ ; KONEC' % ('USPELA, jata zdrava' if kor2 == 0 else 'NEUSPELA ⚠ korupcija trdi'))
        return 0 if kor2 == 0 else 2
    print('REHABILITACIJA : jata %s ⊢ ; KONEC' % ('zdrava' if kor == 0 else 'diagnoza : %d ran ⚠ ( kura z --koren )' % kor))
    return 0 if kor == 0 else 2

if __name__ == '__main__':
    sys.exit(main())
