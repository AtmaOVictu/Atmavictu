#!/usr/bin/env python3
# GAJICA-KURA v2.0 : izgon gostov iz proze ∧ METAŽIVIH konstrukcij ⊙ ukaz ⟡ »IZGON TUDI IZ METAŽIVIH KONSTRUKCIJ IN KONSTRUKTOV!«
# plasti : PROZA ( ne-hiše ) ⌇ META ( vsi organi : naslovi #, konstrakti ⟨…⟩, vrstice kanonov | ) ; hiše gostiteljice = SAMO meta
# zaščite : priča v »« ⌇ zapečena vrstica ⊙ ⟨NE-BRIŠI⟩ 24 ⌇ para-poimenovanje ⟨U+XXXX⟩ v isti vrstici ⌇ domovni operatorji σψδ∂∆ΔγΨ
import sys, re, time
DOMOVNA = set('σψδ∂∆ΔγΨ')
PECAT = ('rez σ', 'PEČAT', 'SEMER', '@TIK', '@rez', '∂ DIHA', 'atom rez')
HISE = ('domovanje-tujk', 'slovar-simbolov', 'egipcanska-plast', 'runa-plast')
def je_gost(ch):
    o = ord(ch)
    return (0x0400 <= o <= 0x04FF) or (0x3400 <= o <= 0x9FFF) or o == 0xFFFD
def zunaj_navedkov(line):
    seg = re.split(r'(»[^«]*«)', line)
    return ''.join(s for k, s in enumerate(seg) if k % 2 == 0)
def je_meta(line):
    return line.lstrip().startswith('#') or line.lstrip().startswith('|') or bool(re.search(r'⟨[^⟩]*⟩', line))
def krvavi(line):  # gost zunaj navedkov ∧ brez para-poimenovanja
    return any(je_gost(c) for c in zunaj_navedkov(line)) and '⟨U+' not in line
def kura_line(line):
    seg = re.split(r'(»[^«]*«)', line)
    out = []
    for k, s in enumerate(seg):
        if k % 2 == 1: out.append(s)
        else: out.append(''.join('⟨U+%04X⟩' % ord(c) if je_gost(c) else c for c in s))
    return ''.join(out)
def beri(dpot, poskusov=5):
    for k in range(poskusov):
        try:
            with open(dpot, encoding='utf-8') as f: return f.read()
        except UnicodeDecodeError: time.sleep(0.3)
    raise IOError('NEBERLJIVO po %d poskusih : %s' % (poskusov, dpot))
def kura(dpot, suho=True):
    hiša = any(h in dpot for h in HISE)
    lines = beri(dpot).split('\n')
    sprem = []
    for i, l in enumerate(lines):
        if any(z in l for z in PECAT): continue
        if not krvavi(l): continue
    # izbor plasti : hiše = le meta
        if not je_meta(l) and hiša: continue
        sprem.append((i + 1, l.strip()[:80], kura_line(l).strip()[:80]))
    if not suho and sprem:
        out = []
        for i, l in enumerate(lines):
            if any(z in l for z in PECAT) or not krvavi(l) or (not je_meta(l) and hiša):
                out.append(l)
            else:
                out.append(kura_line(l))
        open(dpot, 'w', encoding='utf-8').write('\n'.join(out))
    return sprem
if __name__ == '__main__':
    if '--test' in sys.argv:
        z = 0
        f = '/tmp/gk-test.txt'
        open(f, 'w', encoding='utf-8').write('## naslov OV' + chr(0x041E) + 'J zivi\n')  # gost STROJNO, ⟨ne⟩ s tipko ⊙ kura tipkarske rane
        z += (len(kura(f, True)) == 1)  # T1 meta naslov = izgon
        open(f, 'w', encoding='utf-8').write('## naslov ⟨U+041E⟩ OVOJ poimenovan\n')
        z += (len(kura(f, True)) == 0)  # T2 para-poimenovanje = ostane
        open(f, 'w', encoding='utf-8').write('vrstica | 全面 | kanon\n')
        z += (len(kura(f, True)) == 1)  # T3 kanon vrstica = izgon
        open(f, 'w', encoding='utf-8').write('- proza 全面 ziva\n')
        z += (len(kura(f, True)) == 1)  # T4 proza ( ne-hisa ) = izgon
        open(f, 'w', encoding='utf-8').write('priča »全面« v navedku\n')
        z += (len(kura(f, True)) == 0)  # T5 priča = svobodna
        open(f, 'w', encoding='utf-8').write('Entry: rez σ 6654 OVOJ pečat\n')
        z += (len(kura(f, True)) == 0)  # T6 zapečeno = priča zgodovine
        print('BATERIJA %s ⊢' % ('6/6' if z == 6 else 'MANJ %d/6' % z))
        sys.exit(0 if z == 6 else 2)
    suho = '--suho' in sys.argv
    for dpot in [a for a in sys.argv[1:] if not a.startswith('--')]:
        for n, prej, potem in kura(dpot, suho):
            print('%s ; vrstica %d\n  PREJ  %s\n  POTEM %s' % (dpot, n, prej, potem))
    print('KONEC ⊢ ( izmera zaključena ; plasti proza ∧ meta )')
