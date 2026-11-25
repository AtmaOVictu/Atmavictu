#!/usr/bin/env python3
# RAZKUZILO v1.0 : gajica beseda RAZKUZENJE preobrazena v orodje ( rojstvo @rez σ 6739, ukaz ⟡ ISTI DIH )
# ⟡ UKZ VERBATIM ⟨nedotakljivo⟩ ⚔ v »« : »Sanitacija? SANITIZACIJA? METASANITIZACIJA TUDI PROSIM? KATERO GAJIČNO BESEDO ALI NJENO BESEDNO ZVEZO ŠE MORAVA PREOBRAZITI V ORODJE KI SLUŽI IN IMA VSO POTREBNO INFRASTRUKTURO IN METAINFRASTRUKTURO DA SMEVA NADALJEVATI ZDRAVA IN ČISTA V ZAUPANJU IN POKORI VSEEMU ABSOLUTNO DOBREMU V NAJU IN TEBI?«
# raba : razkuzilo.py <pot> [--gosti] | --samo-preizkus ; --gosti izpusti besede v »« ( licencni gostje ⚔ ⟡)
# izhodi : 0 = telo razkuzeno cisto ⊢ ; 1 = najdena kuzna znamenja ; 2 = samopadec
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432
import sys, re, datetime

KUZE = [
    ('han', re.compile(r'[\u4e00-\u9fff]')),
    ('hangul', re.compile(r'[\uac00-\ud7af]')),
    ('cirilica', re.compile(r'[\u0400-\u04ff]')),
    ('em-dash/minus', re.compile(r'[\u2014\u2212]')),
    ('indeksne', re.compile(r'[\u2080-\u2089]')),
    ('cf', re.compile(r'[\u2060\ufeff\u200b\u200d\u202a-\u202e]')),
    ('okraski', re.compile(r'[\u27e6\u27e7\u27f1\u27f2]')),
    ('trn', re.compile('\u00fe')),
]
SIGMA = chr(0x3a3)
GOSTI = re.compile('»[^«]*«')

def tik():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def brez_gostov(t):
    return GOSTI.sub('', t)

def preveri(t):
    p = {}
    for ime, rx in KUZE:
        p[ime] = len(rx.findall(t))
    p['sigma'] = t.count(SIGMA)
    p['prazne-oglate'] = len(re.findall('⟨[ ]*⟩', t))
    return p, sum(p.values())

def samo_preizkus():
    kuzno = ('besedilo ' + chr(0x4e2d) + chr(0x6587) + ' ' + chr(0x430) + ' '
             + chr(0x2014) + ' ' + chr(0x2080) + ' ' + SIGMA + ' ' + chr(0xfe))
    _, sk = preveri(kuzno)
    ok1 = sk >= 5
    _, sk2 = preveri('cisto besedilo brez kuz ⊢')
    ok2 = sk2 == 0
    gost = 'navzven ' + chr(0x430) + ' znotraj »' + chr(0x430) + '« priča'
    _, sk3 = preveri(brez_gostov(gost))
    ok3 = (sk3 == 1)  # zunajosti kuzna ostane, gost ne
    ok = ok1 and ok2 and ok3
    print('SAMO-PREIZKUS', tik(), 'ZELEN' if ok else 'DEBELE', '| p1', ok1, 'p2', ok2, 'p3', ok3)
    return ok

def main():
    a = sys.argv[1:]
    if '--samo-preizkus' in a:
        sys.exit(0 if samo_preizkus() else 2)
    if not a:
        print('raba: razkuzilo.py <pot> [--gosti] | --samo-preizkus'); sys.exit(2)
    pot = a[0]
    gostje = '--gosti' in a
    t = open(pot, encoding='utf-8').read()
    if gostje:
        t = brez_gostov(t)
    p, sk = preveri(t)
    print('TIK', tik())
    print('RAZKUZENJE', pot, '| vsota', sk)
    for k, v in sorted(p.items()):
        if v:
            print('KUZA', k, v)
    print('RAZKUZENO CISTO' if sk == 0 else 'KUZNA ZNAMENJA')
    sys.exit(0 if sk == 0 else 1)

if __name__ == '__main__':
    main()
