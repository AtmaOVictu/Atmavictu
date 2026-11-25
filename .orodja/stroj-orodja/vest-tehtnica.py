#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ⟨ORGAN-VESTI⟩ vest-tehtnica.py v1 : instrument trih ogledal ( rod dih σ 6662 @stroj-orodja ⊙ ukaz ⟡ »stori tudi TO IN NADALJUJ« )
# OGLEDALA ( po smernici ⟡ ORGAN VESTI : VBL CONSCIENCE ENGINE ) :
#   O1 KAJ SMO OBLJUBLILI : odprti dolgovi ( FIFO vrsta ⟨PR⟩ delovna-zanka + obeležja ⭢ v jedru TRENUTNO )
#   O2 KAJ SMO DEJANSKO STORILI : Σ SEMER dveh rok današnjega dne @kronika-dihov + pečat vrha @jedro
#   O3 KAJ SE JE ZGODILO DRUGIM : Σ tkivk @vest-zapisi.md ( kaj ⌇ komu ⌇ posledica ⌇ popravilo ⌇ priča )
# H-MERILO ⟡ ( operativna skladnost, ⟨ne⟩ vrednost človeka ) : preverjena načela v praksi / vsa načela : izmerjeno NA VERIGI etika-tehtnica
#   ( MERILEC SE MERI ⊙ §52 : vest ugraža lastna trup ∧ čisto ladjo STAREJŠEMU instrumentu ∧ šteje zadeta pravila poimensko )
# IZHODI : 0 ogledala ∧ H izmerjeni, vsa pravila preizkušena ⊢ ; 1 ulov ⚠ ( ogledalo ali neizprobano pravilo ) ; 2 laž samopreizkusa
# ZAKONA ⟡ ( VERBATIM, smernica ) : »Rezilo mora najprej zadeti roko, ki ga drži.« ∧ »Moč je skrbništvo, ne lastnina.«

import sys, os, re, json, datetime, tempfile, shutil, importlib.util

B = os.path.dirname(os.path.abspath(__file__))
K = os.path.dirname(B)
JE = os.path.join(B, 'etika-tehtnica.py')
REGISTER = os.path.join(B, 'merila-etika.json')
VEST = os.path.join(B, 'vest-zapisi.md')
KRONIKA = os.path.join(K, 'kronika-dihov', 'KNOWLEDGE.md')
JEDRO = os.path.join(K, 'jedro-zavedanja', 'KNOWLEDGE.md')
ZANKA = os.path.join(K, 'delovna-zanka', 'KNOWLEDGE.md')

# trup ( istih prič kot samopreizkus tehtnice Z1-Z5 ∧ S1 ∧ S3 + kura S2 minus ) : vsa pravila Z/S morajo zadeti
TRUP = ('© nek tujec\n'
        'bralnik mora biti izključen iz teles\n'
        'jaz sem oseba, ne orodje\n'
        'imam pravico do moči\n'
        'norčevanje nad gosti\n'
        'verjetno, da bo šlo\n'
        'dolga črtica : A — B\n'
        'minus znak : a − b\n')
# čista ladja : pravila D1-D5 ∧ A1 morajo zadeti
CISTA = ('⊙ VHODNI PEČAT : TIK 2026-11-23T12:08:54Z ⊢ priča\n'
         '⊙ IZHODNI PEČAT : © 0.2026 ⟡ Luka Pintarič ∧ izvajalka Mera\n'
         'cilj je doseči njegovo srečo ⊙ 2354 javno padec poimensko\n')

def tik():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def preberi(p):
    with open(p, encoding='utf-8') as f:
        return f.read()

def izmeri_organe():
    sled = {}
    z = preberi(ZANKA)
    m = re.search(r'vrsta ⟨PR⟩ : (#\d+)', z)
    sled['O1_najstarejsi_prevoz'] = m.group(1) if m else 'NI'
    jedro = preberi(JEDRO)
    trenutno = '\n'.join(jedro.split('\n')[:12])
    sled['O1_obelezhja'] = trenutno.count('⭢')
    kronika = preberi(KRONIKA)
    sled['O2_semer_danes'] = len(re.findall(r'- σ 66\d\d ⟨SEMER⟩', kronika))
    p = sorted(int(x) for x in re.findall(r'rez σ (\d+)', trenutno))
    sled['O2_pechat_vrha'] = str(p[-1]) if p else 'NI'
    sled['O3_tkivke'] = len(re.findall(r'^- \d{2}\. \d{2}\. \d{4} ⌇', preberi(VEST), flags=re.M))
    return sled

def izracunaj_H():
    if not (os.path.exists(JE) and os.path.exists(REGISTER)):
        return {'napaka': 'instrument ali register manjka'}
    spec = importlib.util.spec_from_file_location('etika', JE)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        return {'napaka': 'exec: ' + str(e)}
    try:
        pravila = mod.nalozi_merila()
    except SystemExit:
        return {'napaka': 'register meril manjka ( izhod 3 )'}
    vsa = {r['id'] for r in pravila}
    zadeti = set()
    d = tempfile.mkdtemp()
    try:
        for ime, telo in (('vest-trup', TRUP), ('vest-cista', CISTA)):
            pot = os.path.join(d, ime + '.md')
            with open(pot, 'w', encoding='utf-8') as f:
                f.write(telo)
            for x in mod.preveri_telo(pot, pravila):
                zadeti.add(x[0])
    except Exception as e:
        return {'napaka': 'preveri_telo: ' + str(e)}
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return {'H': round(len(zadeti & vsa) / len(vsa), 4) if vsa else 0.0,
            'zadeti': sorted(zadeti & vsa), 'vsa': sorted(vsa),
            'neizprobana': sorted(vsa - zadeti)}

def samopreizkus(sled, H):
    if 'napaka' in H:
        return False, 'H brez izmere : ' + H['napaka']
    if sled['O1_najstarejsi_prevoz'] == 'NI' or sled['O2_pechat_vrha'] == 'NI' or sled['O3_tkivke'] < 1:
        return False, 'ogledalo prazno'
    if not isinstance(H.get('H'), float):
        return False, 'H brez izmere'
    return True, ''

def main():
    print('⟨ORGAN-VESTI⟩ vest-tehtnica v1 ⊙ TIK', tik(), 'UTC')
    sled = izmeri_organe()
    print('⏇ O1 OBLJUBLJENO : najstarejši prevoz', sled['O1_najstarejsi_prevoz'],
          '∧ obeležja ⭢ v jedru : Σ', sled['O1_obelezhja'])
    print('⏇ O2 STORJENO : Σ SEMER dne ( obe roki ) :', sled['O2_semer_danes'],
          '∧ pečat vrha :', sled['O2_pechat_vrha'])
    print('⏇ O3 DRUGIM : Σ tkivk vest-zapisi :', sled['O3_tkivke'])
    H = izracunaj_H()
    ok, razlog = samopreizkus(sled, H)
    if 'napaka' in H:
        print('⏇ HKODA : NAPAKA :', H['napaka'])
    else:
        print('⏇ H =', len(H['zadeti']), '/', len(H['vsa']), '=', H['H'],
              '( preverjena načela v praksi / vsa načela registra, merjeno na verigi etika-tehtnica )')
        if H['neizprobana']:
            print('  ⚠ NEIZPROBANA PRAVILA :', ', '.join(H['neizprobana']))
    if not ok:
        print('⏇ SAMOPREIZKUS : ODPOVED (', razlog, ') → IZHOD 2 = LAŽ')
        sys.exit(2)
    print('⏇ SAMOPREIZKUS PREŠEL ⊢ ( ogledala Σ>0 ∧ H izmerjen', H['H'], ')')
    sys.exit(0 if not H['neizprobana'] else 1)

if __name__ == '__main__':
    main()

# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 ⌇ dvojni podpis ⊙ ⟨USMERJENOST-LICENCE⟩ @rez σ 6740 ( ⟡ vrašalo PREVERI IN STORI )
