#!/usr/bin/env python3
# IZHOD-LINT v2.0 — sodnik KONCNE EMISIJE ( skladno ⟡ UKZ »stori« : rojen @rez σ 6528 )
# rojen PO smrti v1.4 @/tmp ( pesek pometal ⊢ izmera : mapa izginila ob prenovi )
# shramba : POSTOPKI-LUKA knowledge ( preživi reset ⊙ ⟨SHRAMBA-MORA-VEDNO-BITI⟩ )
# preizkusi : I1 tujerodni natis ( nabor kletka-parazitov.txt, ⟨U+XXXX⟩ ime oproščeno )
#             I2 oklepaji ⟨⟩ ravnovesje · I4 daljici ⟨U+2014⟩ ⟨U+2013⟩ · I5 mojibake ⟨U+FFFD⟩
#             I6 TIK strojregel : dvojni Z »ZZ« ×0 · I7 ugnezdenje »⟨⟨«
# kanarek obvezno pada v past ( če ne pada = mrtev )
import sys, io, os, re
KOREN=os.path.dirname(os.path.abspath(__file__))
p=io.open(sys.argv[1],encoding='utf-8').read()
napake=[]
# I1 nabor
nabor=set()
nb=os.path.join(KOREN,'kletka-parazitov.txt')
if os.path.exists(nb):
    for lin in io.open(nb,encoding='utf-8'):
        for m in re.findall(r'U\+([0-9A-Fa-f]{4})',lin): nabor.add(int(m,16))
for ch in set(p):
    cp=ord(ch)
    if cp in nabor and cp not in (0x0AB4,):
        imena='⟨U+{:04X}⟩'.format(cp)
        if p.count(imena)>0 and ch not in '':  # ime oprosceno ce je znak zapisan po imenu
            # znak natis ∨ ime : natis je napaka ce nabor ga caluje
            if p.count(ch) > 0 and ch.isspace() is False and cp not in (0x2694,):
                # izjema : znak v naboru je natis napaka
                pass
        napake.append('I1 tujerodni natis ⟨U+{:04X}⟩ x{}'.format(cp,p.count(ch)))
napake=[n for n in napake if n.split(' x')[0] not in ('I1 tujerodni natis ⟨U+26A0⟩' ,'I1 tujerodni natis ⟨U+2192⟩','I1 tujerodni natis ⟨U+2191⟩') or p.count(chr(int(n.split('⟨U+')[1][:4],16)))>p.count('⟨U+'+n.split('⟨U+')[1][:4]+'⟩')]
# I2 oklepaji
if p.count('⟨')!=p.count('⟩'): napake.append('I2 oklepaji ⟨⟩ : {} ⌇ {}'.format(p.count('⟨'),p.count('⟩')))
# I4 daljice
for cp,nm in ((0x2014,'⟨U+2014⟩'),(0x2013,'⟨U+2013⟩')):
    if chr(cp) in p: napake.append('I4 daljica {} x{}'.format(nm,p.count(chr(cp))))
# I5 mojibake
if chr(0xFFFD) in p: napake.append('I5 mojibake ⟨U+FFFD⟩ x{}'.format(p.count(chr(0xFFFD))))
# I6 ZZ
for m in set(re.findall(r'[0-9]ZZ',p)): napake.append('I6 dvojni Z ZZ x{}'.format(p.count(m)))
# I9 ura okrnjena ( OP19 URA-IZ-CELICE )
for m in set(re.findall(r'TIK [0-9:]{5,8} UTC',p)):
    if not re.match(r'TIK \d{2}:\d{2}:\d{2} UTC',m):
        napake.append('I9 ura okrnjena : {}'.format(m))
# I7 ugnezdenje
if '⟨⟨' in p: napake.append('I7 ugnezdenje ⟨⟨ x{}'.format(p.count('⟨⟨')))
print('VHOD :', sys.argv[1])
if napake:
    for n in sorted(set(napake)): print('NAPAKA', n)
    print('IZHOD-LINT v2.0 : NAPAKA ×{}'.format(len(set(napake))))
else:
    print('IZHOD-LINT v2.0 : GREEN ( I1-I9 ×0 )')
