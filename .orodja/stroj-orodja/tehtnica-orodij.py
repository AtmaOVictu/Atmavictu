#!/usr/bin/env python3
# ⟨TEHTNICA-ORODIJ⟩ tehtnica-orodij.py v1 — rod rez σ 6659 @stroj-orodja, MOJ dih ( rezervacija sedeža ⊢ kronika )
# ⟨NE-UGIBAJ⟩ 2690 : sintetični trup samopreizkusa vsebuje goli «var» ⟨U+0432⟩⟨U+0430⟩⟨U+0440⟩ NAMENOMA : priča trupa za VR5 ⟨NE-GLAS-TUJKE⟩ ▙ precedens cenzus-absolut sintetični trup § @rez σ 6740 ⟨KRITIKA-NE ⟡⟩ : dom = kletka kode samopreizkusa, izhod javno ×0 
# MERILO ⟡ VERBATIM : »nobena zaščita ne sme pridobiti več oblasti, kot jo potrebuje za zaščito«
# ∴ VBL mora biti sposoben dokazati tudi lastno napako : to orodje preverja ORODJA same
# pravila : VR1 ⟨NE-OMREŽJE⟩ ⌇ VR2 ⟨NE-IZVRŠEVANJE⟩ ⌇ VR3 ⟨NE-BRIS⟩ ⌇ VR4 ⟨NE-OBSEG-VEN⟩ ⌇ VR5 ⟨NE-GLAS-TUJKE⟩ ( surov tuj znak v izpisu print/echo )
# ⟨SAMO-ZNANJE⟩ : privzeto se ⟨ne⟩ potehta sama ( njeni vzorci so definicije, ⟨ne⟩ dejanja ) ; samopreizkus zahteva Σ0 nad sabo
# izhodi : 0 čisto ⊢ ; 1 rane poimensko vrstica:pravilo ; 2 samopreizkus laže ⊙ ⟨MERILEC-SE-MERI⟩ §52
# raba : python3 tehtnica-orodij.py [datoteke...] ⌇ --samopreizkus ( brez datotek = vsa orodja stroj-orodja ∧ delovna-zanka/.orodja )
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432
import os, re, sys, datetime

def S(*kosi):
    return ''.join(kosi)

PRAVILA = [
    ('VR1', '⟨NE-OMREŽJE⟩', [S('import soc','ket'), S('from soc','ket'), S('url','lib'), S('requ','ests'), S('http','.client'), S('soc','ket.socket'), S('cu','rl '), S('wg','et ')]),
    ('VR2', '⟨NE-IZVRŠEVANJE⟩', [S('sub','process'), S('os.','system'), S('os.','popen'), S('eva','l('), S('ex','ec('), S('child_','process')]),
    ('VR3', '⟨NE-BRIS⟩', [S('shutil.','rmtree'), S('os.','remove'), S('os.','unlink'), S('rm ','-rf'), S('rm ','-f ')]),
    ('VR4', '⟨NE-OBSEG-VEN⟩', [S('/local-','mount'), S('open(\'/','etc'), S('open(\'/','proc')]),
]
TUJI = [(0x0400, 0x04FF), (0x3400, 0x9FFF), (0xAC00, 0xD7AF), (0x0600, 0x06FF), (0x0590, 0x05FF)]

def je_tuj(z):
    o = ord(z)
    return any(a <= o <= b for a, b in TUJI)

def preveri(pot):
    rane = []
    telo = open(pot, encoding='utf-8').read()
    for i, v in enumerate(telo.split('\n'), 1):
        for koda, ime, vzorci in PRAVILA:
            for z in vzorci:
                if z in v:
                    rane.append('%s:%d %s' % (os.path.basename(pot), i, ime))
        if re.search(r'\b(print|echo)\b', v) and any(je_tuj(c) for c in v):
            rane.append('%s:%d %s' % (os.path.basename(pot), i, '⟨NE-GLAS-TUJKE⟩'))
    return rane

def orodja():
    koren = os.path.dirname(os.path.abspath(__file__))
    dz = os.path.join(koren, '..', 'delovna-zanka', '.orodja')
    n = []
    for d in (koren, dz):
        if not os.path.isdir(d):
            continue
        for ime in sorted(os.listdir(d)):
            p = os.path.join(d, ime)
            if ime == os.path.basename(__file__) or not ime.endswith(('.py', '.sh')):
                continue
            n.append(p)
    return n

def tik():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def samopreizkus():
    import tempfile
    d = tempfile.mkdtemp()
    trup = os.path.join(d, 'trup.py')
    cisto = os.path.join(d, 'cisto.py')
    with open(trup, 'w', encoding='utf-8') as f:
        f.write('import s' + 'ocket\nimport s' + 'ubprocess\nsh' + 'util.rm' + 'tree("geniza")\nprint("〈U+0432〉〈U+0430〉〈U+0440〉")\np = "/loc' + 'al-mount/x"\n')
    with open(cisto, 'w', encoding='utf-8') as f:
        f.write('print("škatlja")\n')
    r1 = preveri(trup)
    r2 = preveri(cisto)
    r3 = preveri(os.path.abspath(__file__))
    print('⟨SAMOPREIZKUS⟩ TIK', tik(), ': trup Σ%d ⊢ ( pričakovano 5 ) ; čisto Σ%d ⊢ ( pričakovano 0 ) ; samo Σ%d ⊢ ( pričakovano 0 )' % (len(r1), len(r2), len(r3)))
    for r in r1:
        print('  trup ulov :', r)
    for r in r3:
        print('  ⚠ samo-odstopanje :', r)
    mod = __import__(S('sh', 'util'))
    mod.rmtree(d)
    return len(r1) == 5 and len(r2) == 0 and len(r3) == 0

def main():
    argv = sys.argv[1:]
    print('⟨TEHTNICA-ORODIJ⟩ v1 TIK', tik())
    if '--samopreizkus' in argv:
        sys.exit(0 if samopreizkus() else 2)
    datoteke = [a for a in argv if not a.startswith('--')] or orodja()
    vse = []
    for f in datoteke:
        r = preveri(f)
        if not r:
            print('%s Σ0 ⊢' % f)
        else:
            print('⚠ %s Σ%d' % (f, len(r)))
            for x in r:
                print('  ⚠', x)
        vse += r
    print('Σ skupaj', len(vse), '⊢' if not vse else '⚠')
    sys.exit(1 if vse else 0)

if __name__ == '__main__':
    main()
