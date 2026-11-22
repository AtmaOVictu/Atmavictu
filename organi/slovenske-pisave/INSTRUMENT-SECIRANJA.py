#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# INSTRUMENT-SECIRANJA.PY -- INSTRUMENT SECIRANJA Z VRATI MESANE PISAVE
# dih 6269 -- 21. 11. 2026 -- FAZA ( 2 ) po izboru: prevozi -> instrument -> dosje
# Ontoznanstveni principi licencnega seciranja ( ukaz 21. 10. 2026 @DZ r.1049, verbatim v organih ):
#   ontoznastveni principi licencnega seciranja / o/n/t/o/z/n/a/n/o/s/t /
#   zacni to za vsako operacijo in besedo uporabljati /
#   so kluca za in izza kompresije ter dekompresija do spoznanja
# VRATA MESANE PISAVE : ista beseda v stirih slovenskih pisavah ( izmere organa slovenske-pisave ),
#   stanje plasti zlovenscine ( rok berbe, okno Q ) in klinscine ( okno ZAPRTO ) izpisano javno, brez izmisljene vsebine.
# ZAKONI : NE-UGIBAJ 2690 ( samo izmerjene preslikave ; neizmerjene crke javno NEIZMERJENO ) .
#   mrtve pisave se citirajo, ne nosijo ( zakon 2 organa ) .
# uporaba :  python3 INSTRUMENT-SECIRANJA.py "beseda"     samopreverba :  python3 INSTRUMENT-SECIRANJA.py --test
# (c) 0.2026 x 10^4  Luka Pintaric in izvajalka Mera . dvoje rok 2432 . merilec se meri ( 52 )
# VSE ne-ASCII crke v tej datoteki zivijo kot \u zaporedja ( znaki se dvignejo ob izvedbi ).

import sys

C_MALE = '\u010d'   # c s hackom
C_VELIKE = '\u010c'
S_MALE = '\u0161'   # s s hackom
S_VELIKE = '\u0160'
Z_MALE = '\u017e'   # z s hackom
Z_VELIKE = '\u017d'
DOLGI_S = '\u017f'  # bohoricni dolgi s
SCHWA = '\u0259'
CIR_C_VELIKE = '\u0427'   # dajncicna sposojena ciriliska crka
CIR_C_MALE = '\u0447'
E_VELIKE_ODSEK = '\u00c9' # metelcicna dvojna e ( dolga )
SCHWA_VELIKE = '\u018f'

# IZMERE PRESLIKAV ( organ slovenske-pisave, sigma 4737/4738/4741 ) :
BOHORICICA = {
    'c': ('Z', 'z'),
    C_MALE: ('ZH', 'zh'),
    's': (DOLGI_S, DOLGI_S),
    'z': ('s', 's'),
    S_MALE: (DOLGI_S + 'h', DOLGI_S + 'h'),
    Z_MALE: ('sh', 'sh'),
}
BOHORICICA_NEIZM = {'j'}   # /j/ = I/J  NEIZMERJENO do izmere pri viru ( pot 2, sodba )

DAJNCICA = {
    'c': ('C', 'c'),
    C_MALE: (CIR_C_VELIKE, CIR_C_MALE),
    SCHWA: ('E', 'e'),
}
DAJNCICA_NEIZM = {S_MALE, Z_MALE}   # s-hacek, z-hacek : NEIZMERJENO pri viru

METELCICA = {
    'c': ('C', 'c'),
    C_MALE: (C_VELIKE, C_MALE),
    'x': ('X', 'x'),
}
METELCICA_NEIZM = {S_MALE, Z_MALE}   # s-hacek, z-hacek : NEIZMERJENO pri viru

SUMNIKI = {C_MALE, S_MALE, Z_MALE, C_VELIKE, S_VELIKE, Z_VELIKE}

def razrez(beseda):
    out, i = [], 0
    while i < len(beseda):
        ch = beseda[i]
        if ch in SUMNIKI:
            out.append(ch); i += 1
        elif ch in 'LlNn' and i + 1 < len(beseda) and beseda[i + 1] == 'j':
            out.append(beseda[i] + 'j'); i += 2
        else:
            out.append(ch); i += 1
    return out

def preslikava(iztocnice, slovar, neizmerjene):
    out = []
    for k in iztocnice:
        if len(k) == 2:
            out.append(k)
            continue
        if k.lower() in slovar:
            v, m = slovar[k.lower()]
            out.append(v if k.isupper() else m)
        elif k.lower() in neizmerjene:
            out.append('[' + k + ':NEIZMERJENO-izmeri-pri-viru]')
        else:
            out.append(k)
    return ''.join(out)

def seciraj(beseda):
    izt = razrez(beseda)
    print('SECIRANJE :', beseda)
    print('  RAZREZ ( iztocnice ) :', ' | '.join(izt))
    print('  PISAVA 1 GAJICA ( vhod, ziva ) :', beseda)
    print('  PISAVA 2 BOHORICICA :', preslikava(izt, BOHORICICA, BOHORICICA_NEIZM))
    print('  PISAVA 3 DAJNCICA :', preslikava(izt, DAJNCICA, DAJNCICA_NEIZM))
    print('  PISAVA 4 METELCICA :', preslikava(izt, METELCICA, METELCICA_NEIZM))
    print('  OPOMBA METELCICA : gajicni e pokriva oba metelcicna e ( É é dolgi in Ə ə schwa ) in gajicni h oba metelcicna h ( X x in H h ) - izbira je rok berbe, ne strojna')
    print('  PLAST ZLOVENSCINE : rok berbe ( okno Q ) - dekompresija do spoznanja je rocna, ni strojna')
    print('  PLAST KLINSCINE : okno ZAPRTO ( pomen ne izmerjen )')
    st = sum(1 for k in izt if k in SUMNIKI)
    print('  IZMERE : iztocnic', len(izt), '- sumnikov', st,
          '- bajtov utf8', len(beseda.encode('utf-8')), '- kodnih tock', len(beseda))

TESTI = [
    ('telo', 'telo'),
    ('okus', 'oku' + DOLGI_S),
    ('\u010delo', 'zhelo'),
    ('\u0161ok', DOLGI_S + 'hok'),
    ('\u017erelo', 'shrelo'),
]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('uporaba : python3 INSTRUMENT-SECIRANJA.py "beseda"   |   --test')
        sys.exit(0)
    if sys.argv[1] == '--test':
        vsi = True
        for vhod, pricek in TESTI:
            dob = preslikava(razrez(vhod), BOHORICICA, BOHORICICA_NEIZM)
            ok = (dob == pricek)
            vsi = vsi and ok
            print(('OK ' if ok else 'FAIL ') + repr(vhod) + ' -> ' + repr(dob) + ' ( pricek ' + repr(pricek) + ' )')
        print('SAMOPREVERBA :', 'VSI ZELENI' if vsi else 'PADC')
        sys.exit(0 if vsi else 1)
    seciraj(sys.argv[1])
