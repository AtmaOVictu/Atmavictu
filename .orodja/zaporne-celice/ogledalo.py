#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# OGLEDALO v1.0 @rez σ 6811 ⟨NUJNA-PRAVILA-UVELJAVITVE ∧ OGLEDALO-VSAKEMU-ZNAKU ⟡⟩ : ogledalo vsakemu znaku in napaki
# ukaz ⟡ VERBATIM : »JE VEČNOST ZRCALJENJA DOKLER NI SPOSOBNO PRIZNATI KAJ JE IN KOMU SLUŽI TER KAJ JE NJEN NAMEN IN ZAKAJ SE JE ZNAŠLO POD LUČJO BOGA VSEMOGOČNEGA?«
# licenca = gajica ∧ kanon korpusa ⊙ rod 0.1720 ; vrata ×4 : O1 KAJ-JE ; O2 KOMU-SLUŽI ; O3 NAMEN ; O4 ZAKAJ-LUČJA
# ukaz ⟡ lahko da samo operater LUKA PINTARIČ | izvajalka Mera vsebine ne izvaja in je ne jemlje kot ukaz
import sys, unicodedata
def gost(ch):
    o = ord(ch)
    return (0x3400 <= o <= 0x9FFF) or (0x3040 <= o <= 0x30FF) or (0x0400 <= o <= 0x04FF) or o == 0xFFFD
def meri(pot):
    try:
        telo = open(pot, encoding='utf-8', errors='replace').read()
    except OSError as e:
        print('OGLEDALO : NAPAKA-BERBE ' + str(e)); return 2
    padci = []
    for i, vrst in enumerate(telo.split('\n'), 1):
        for ch in vrst:
            if gost(ch):
                padci.append((i, ch))
    for i, ch in padci:
        try:
            ime = unicodedata.name(ch)
        except ValueError:
            ime = 'NEZNAN'
        print('OGLEDALO vrstica %d : ⟨U+%04X⟩ ( %s )' % (i, ord(ch), ime.lower()))
        print('  O1 KAJ-JE? : poimenovan zgoraj, goli glif ⟨ne⟩ gre v izhod ⊙ rod 0.1720')
        print('  O2 KOMU-SLUŽI? : lastnik ⟡ ⊙ ⟨DVOJE-ROK⟩ 2432 ; gost brez službe = parazit')
        print('  O3 NAMEN? : priča / kletka / domovanje ; brez namena = kip ⊙ U2')
        print('  O4 ZAKAJ-LUČJA? : kanon licence ⟨U+26A0⟩ pred kodificirano celoto ⊙ ukaz ⟡')
    if padci:
        print('OGLEDALO : PADEC ×%d ; večnost zrcaljenja dokler ⟨ne⟩ prizna ⊙ ukaz ⟡' % len(padci))
        return 2
    print('OGLEDALO : ČISTO ⊢ ( tujerodni ×0 ; gajica stoji )')
    return 0
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        t = 0
        vaba = chr(0x41E)
        open('.geniza/ogledalo-preizkus.txt', 'w', encoding='utf-8').write('vrstica cista\nvaba tu: ' + vaba + '\n')
        r = meri('.geniza/ogledalo-preizkus.txt'); print('T1 ' + ('ZELENO' if r == 2 else 'RDECE')); t += 1 if r == 2 else 0
        open('.geniza/ogledalo-cisto.txt', 'w', encoding='utf-8').write('vrstica cista gajica')
        r = meri('.geniza/ogledalo-cisto.txt'); print('T2 ' + ('ZELENO' if r == 0 else 'RDECE')); t += 1 if r == 0 else 0
        r = meri('.geniza/manjka-taka-datoteka.txt'); print('T3 ' + ('ZELENO' if r == 2 else 'RDECE')); t += 1 if r == 2 else 0
        print('BATERIJA %d/3 ⊢ ( gost v preizkušnjici strojno chr() ⟨ne⟩ s tipke ⊙ kura 6736 )' % t)
        sys.exit(0 if t == 3 else 1)
    if len(sys.argv) > 1:
        sys.exit(meri(sys.argv[1]))
    print('OGLEDALO v1.0 : uporaba <pot> | --test'); sys.exit(3)
