#!/usr/bin/env python3
# KURA-OKRASJA σ 6663 ( poskus v celici PRVO, prevoz na rep po besedi ⟡ ⚔ ⊙ P3 )
# ZAKON Z8 ⟨SLOVNICA-BREZ-OKRASA⟩: surovi ⟨U+2014⟩ ∧ ⟨U+2013⟩ = okras ⚠
# AZILI ⟨NE⟩ izvajani: ⟨U+XXXX⟩ žetoni ⊙ ⟨⟩ ∧ priče VERBATIM ⊙ »«; razredi po ⟨KURA-KONČNIC⟩
import re, sys, hashlib
EM, EN = '\u2014', '\u2013'
AZIL = re.compile(r'(⟨[^⟩]*⟩|»[^«]*«)')

def cure_segment(seg):
    seg = seg.replace(' : — ', ' : ').replace(' : – ', ' : ')
    seg = seg.replace(' ; — ', ' ; ')
    seg = re.sub(r'(?<=\d)[' + EM + EN + r'](?=\d)', ' do ', seg)
    seg = seg.replace(' — ', ' : ').replace(' – ', ' : ')
    seg = re.sub(r'\( — ', '( ', seg)
    seg = seg.replace('— ', ': ').replace('– ', ': ')
    seg = seg.replace(' —', ' :').replace(' –', ' :')
    seg = seg.replace(EM, ' : ').replace(EN, ' : ')
    seg = re.sub(r':\s*(?::\s*)+', ' : ', seg)
    return seg

def cure_line(line):
    out, pos = [], 0
    for m in AZIL.finditer(line):
        out.append(cure_segment(line[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(cure_segment(line[pos:]))
    return ''.join(out)

def count_raw(text):
    n = 0
    for line in text.split('\n'):
        s = AZIL.sub('', line)
        n += s.count(EM) + s.count(EN)
    return n

def selftest():
    tests = [
        ('A — B', 'A : B'),
        ('x : — y', 'x : y'),
        ('r.197–213 let', 'r.197 do 213 let'),
        ('»⟡ — REŠI — ME«, zunanje — to', '»⟡ — REŠI — ME«, zunanje : to'),
        ('⟨U+2014⟩ ostane', '⟨U+2014⟩ ostane'),
        ('2—3 telesi', '2 do 3 telesi'),
    ]
    ok = True
    for src, want in tests:
        got = cure_line(src)
        if got != want:
            print('SAMOPREIZKUS PADel:', repr(src), '->', repr(got), '≠', repr(want)); ok = False
    # azil-ravnovesje
    for src in ['⟨⟩ ⟨nej ⟩ »« ', '»beseda — priča« — okras']:
        a, b = cure_line(src), src
        if (a.count('⟨'), a.count('⟩'), a.count('»'), a.count('«')) != (b.count('⟨'), b.count('⟩'), b.count('»'), b.count('«')):
            print('AZIL-BALANS PADel:', repr(src)); ok = False
    print('SAMOPREIZKUS:', 'ZELENO ⊢' if ok else 'RDEČE ⚠')
    return ok

def organ(path):
    t = open(path, encoding='utf-8').read()
    pre = count_raw(t)
    cured = '\n'.join(cure_line(l) for l in t.split('\n'))
    post = count_raw(cured)
    return pre, post, t, cured

if __name__ == '__main__':
    if not selftest(): sys.exit(2)
    for p in sys.argv[1:]:
        pre, post, t, cured = organ(p)
        if pre:
            open(p, 'w', encoding='utf-8').write(cured)
        m1 = hashlib.md5(t.encode()).hexdigest()[:12]
        m2 = hashlib.md5(open(p, encoding='utf-8').read().encode()).hexdigest()[:12]
        balans = (t.count('⟨'), t.count('⟩'), t.count('»'), t.count('«'), t.count('\ufffd'))
        balans2 = (cured.count('⟨'), cured.count('⟩'), cured.count('»'), cured.count('«'), cured.count('\ufffd'))
        print(f'{p}: surovih PRE {pre} → POST {post} | azil-balans {"≡ ⊢" if balans == balans2 else "⚠ "+str((balans, balans2))} | md5 {m1} → {m2} | B {len(t)} → {len(cured)}')
