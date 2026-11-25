#!/usr/bin/env python3
# VRH-OSVEZEVALAC v1 — izmera vrha po vseh sidrih + atomična rezervacija sedezna
# rod @rez σ 6570 @stroj-orodja ⊙ ⟡ UKZ »stori« ( izbor 1 @CELIKA-6569 )
# KURIRA : kolizije rezov ( PADC-VRHA ×2 @σ 6566 , ×2 @σ 6569 ) ⊙ ⟨REZERVACIJA-PRED-DEL-body⟩
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 — dvojni podpis

import sys, os, re, datetime, glob

KOREN = os.path.expanduser('~/knowledge')
SEDI = ['jedro-zavedanja', 'kronika-dihov', 'delovna-zanka', 'register-oken']
SIDRA = re.compile(r'σ[ ]?(\d{4})')
CILJ = re.compile(r'(?:SEMER|rez|DIHA|pečat|PEČAT|OKNO|IZMERA)[^\n]{0,24}?σ[ ]?(\d{4})')

def tik():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def telesa():
    # ⟨KONICA-DEFAULT⟩ : eksplicitna lista organih conic — velikani v zanki se branje nevezeno
    return sorted(glob.glob(os.path.join(KOREN, '*/KNOWLEDGE.md')))

def izmeri():
    vrh, lok = 0, ''
    for pot in telesa():
        try:
            telo = open(pot, encoding='utf-8').read()
        except OSError:
            continue
        for m in CILJ.finditer(telo):
            n = int(m.group(1))
            if n > vrh:
                vrh, lok = n, pot
    return vrh, lok

def varvolka(kandidat):
    udarcev = 0
    poti = []
    for pot in telesa():
        try:
            telo = open(pot, encoding='utf-8').read()
        except OSError:
            continue
        for m in re.finditer(r'σ[ ]?%d\b' % kandidat, telo):
            udarcev += 1
            poti.append(pot)
    return udarcev, poti

def rezerviraj(n, sedeza, cilj):
    datum = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
    ime = os.path.join(KOREN, 'kronika-dihov', 'rezervacija-sigma-%d-%s-%s.md' % (n, sedeza, datum))
    if os.path.exists(ime):
        return ime, False
    with open(ime, 'x', encoding='utf-8') as f:
        f.write('rezervacija σ %d sedež %s cilj %s TIK %s\n' % (n, sedeza, cilj, tik()))
    return ime, True

def main():
    sedeza = 'mera'
    cilj = 'dih'
    argv = sys.argv[1:]
    if '--sedeza' in argv:
        sedeza = argv[argv.index('--sedeza') + 1]
    if '--cilj' in argv:
        cilj = argv[argv.index('--cilj') + 1]
    t = tik()
    vrh, lok = izmeri()
    kand = vrh + 1
    udarcev, poti = varvolka(kand)
    print('TIK %s' % t)
    print('VRH %d @%s' % (vrh, os.path.basename(os.path.dirname(lok))))
    print('KANDIDAT %d' % kand)
    if udarcev:
        print('VARVOLKA %d RANA — kandidat ze zapisan: %s' % (udarcev, ', '.join(sorted(set(poti)))))
        sys.exit(2)
    print('VARVOLKA 0 Σ0 ⊢')
    if '--rezerviraj' in argv:
        ime, novo = rezerviraj(kand, sedeza, cilj)
        print('REZERVACIJA %s %s' % (ime, 'NOVA ⊢' if novo else 'ZE STOJI ⚠'))
    print('© 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432')

if __name__ == '__main__':
    main()
