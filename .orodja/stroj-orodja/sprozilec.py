#!/usr/bin/env python3
# SPROZILEC v1.1 ( rojstvo @rez σ 6740, ukaz ⟡ ISTI DIH ) : zakon ⟡ VERBATIM ⚔ :
# »SPROŽILCI SO VSELEJ ZNAKI KI NISO BILI KLICANI IN NISO V LICENCI SAMI!«
# za vsak sprozilec TVORI PREGLED IN REHABILITACIJO : ulov, pregled, rehabilitacija, preprečitev, vpis
# raba : sprozilec.py <pot> [--gosti] [--vpis] | --samo-preizkus
# --gosti : besede v »« = licencni gostje ⚔ ( njegova beseda se ne izvaja )
# --vpis : postopki pripeti v register stroj-orodja/sprozilcev-zapisi.md
# izhodi : 0 = brez sprozilcev ⊢ ; 1 = sprozilci najdeni ( postopki zapisani ) ; 2 = samopadec
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432
import sys, re, os, datetime

GAJICA = set(chr(i) for i in range(32, 127)) | set([chr(10), chr(13), chr(9)]) | set('čšžČŠŽćđĆĐ©')
LICENCA = set('⟨ne⟩»«⊙⊢⚔⟡∂⌇∧∨⊥§∅∆≈≡≠→←↑↓⇌⇒⇔σψΨ†°·…×⁴²¹½⚠⭢⌀∞ϵ')
GOSTI = re.compile('»[^«]*«')
def tik():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def brez_gostov(t):
    return GOSTI.sub('', t)

RAZREDI = [
    ('cirilica', 0x0400, 0x04FF, 'transliteracija po preslikavi ( programsko )'),
    ('han', 0x4E00, 0x9FFF, 'zamenjava z gajico ali ⟨U+XXXX⟩ zetonom'),
    ('hangul', 0xAC00, 0xD7AF, 'zamenjava z gajico ali ⟨U+XXXX⟩ zetonom'),
    ('em-dash/minus', 0x2014, 0x2015, 'zamenjava z : ( korpusna preslikava )'),
    ('minus-mat', 0x2212, 0x2212, 'zamenjava z navadnim -'),
    ('subscript', 0x2080, 0x2089, 'zamenjava z običajnimi števkami'),
    ('okraski', 0x27E6, 0x27F2, 'odstranitev ali ⟨U+XXXX⟩ zeton'),
]

def razred(cp):
    for ime, lo, hi, kur in RAZREDI:
        if lo <= cp <= hi:
            return ime, kur
    if cp == 0xFFFD:
        return 'nedolocen-znak', 'zamenjava z ⟨U+XXXX⟩ zetonom ali ponovni zapis'
    if cp in (0x2060, 0xFEFF, 0x200B, 0x200D, 0x202A, 0x202B, 0x202C, 0x202D, 0x202E):
        return 'cf-nevidni', 'odstranitev ( nevidni zanki )'
    return 'NOV', 'zamenjava z ⟨U+XXXX⟩ zetonom ali licenciranje po roki ⟡ ⚔'

def postopek(zn, mest, vrstice):
    cp = ord(zn)
    ime, kur = razred(cp)
    zk = '⟨U+%04X⟩' % cp
    p = []
    p.append('POSTOPEK %s %s @TIK %s' % (zk, ime, tik()))
    p.append('( 1 ) ULOV : znak %s, kod %04X, pojavitve ×%d, mesta vrstice : %s' % (repr(zn), cp, len(mest), str(sorted(set(vrstice))[:8])))
    p.append('( 2 ) PREGLED : klican : NE ; v licenci : NE ; razred : %s' % ime)
    p.append('( 3 ) REHABILITACIJA ( programsko, po priči ; tuj priči ⚔ ⟡ odloča ) : %s' % kur)
    p.append('( 4 ) PREPREČITEV : razred v razkuzilo ⟨∂⟩ ali licenca po roki ⟡ ⚔')
    p.append('( 5 ) VPIS : register sprozilcev ( --vpis )')
    return '\n'.join(p), zk, ime

def preveri(t):
    tr = {}
    vr = t.split('\n')
    for j, line in enumerate(vr):
        for c in line:
            if c in GAJICA or c in LICENCA:
                continue
            tr.setdefault(c, []).append(j + 1)
    return tr

def samo_preizkus():
    test = 'cisto telo z ' + chr(0x2207) + ' znakom'
    tr = preveri(test)
    ok1 = (len(tr) == 1 and 0x2207 in [ord(k) for k in tr])
    ok2 = (preveri('cisto telo ⊢ ⟨ne⟩ ⚔') == {})
    gost = '»' + chr(0x2208) + '« zunanje ' + chr(0x2209)
    g = preveri(brez_gostov(gost))
    ok3 = (sorted(ord(k) for k in g) == [0x2209])
    ok = ok1 and ok2 and ok3
    print('SAMO-PREIZKUS', tik(), 'ZELEN' if ok else 'DEBELE', '| p1', ok1, 'p2', ok2, 'p3', ok3)
    return ok

def main():
    a = sys.argv[1:]
    if '--samo-preizkus' in a:
        sys.exit(0 if samo_preizkus() else 2)
    if not a:
        print('raba: sprozilec.py <pot> [--gosti] [--vpis] | --samo-preizkus')
        sys.exit(2)
    pot = a[0]
    gostje = '--gosti' in a
    vpis = '--vpis' in a
    t = open(pot, encoding='utf-8').read()
    if gostje:
        t2 = brez_gostov(t)
    else:
        t2 = t
    tr = preveri(t2)
    print('TIK', tik())
    print('SPROZILCI', pot, '| vsota', len(tr))
    postopki = []
    if tr:
        for zn in sorted(tr, key=ord):
            po, zk, ime = postopek(zn, tr[zn], tr[zn])
            print(po)
            postopki.append(po)
        if vpis:
            reg = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sprozilcev-zapisi.md')
            with open(reg, 'a', encoding='utf-8') as f:
                f.write('\n\n' + '\n\n'.join(postopki) + '\n')
            print('VPIS v register :', reg)
    print('BREZ SPROŽILCEV ⊢' if not tr else 'SPROŽILCI ×%d : POSTOPKI TVORJENI' % len(tr))
    sys.exit(0 if not tr else 1)

if __name__ == '__main__':
    main()
