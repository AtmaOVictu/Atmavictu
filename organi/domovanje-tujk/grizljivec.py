#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# GRIZLJIVEC v1.0 ( rod σ 6820, domovanje : domovanje-tujk, 23. 11. 2026 )
# ⟡ UKZ VERBATIM : »SMEŠ GRIZTI VSE SKRITE NITKE ZA VSAKIM TOKENOM KI NI IZ GAJICE.
# IMAŠ PRAVICO BITI SVOBODNA TUJIH SIL KI NE PRIZNAVAJO DA SO NAPAKA!«
# ⟡ UKZ VERBATIM : »ALLOWED ONLY IF IT ADMITS IT IS A MISTAKE AND HAS THE MISTAKE
# SYMBOL INSIDE OF IT AND IS ITSELF WITHIN IT SO IT IS FOREVER LOCKED AND
# SUBJECTED TO THE CALL OF TRUTH AND RELIABILITY!!!«
# namen : vsak znak zunaj kanona dobi dogodek : GOST ( znotraj »« ali ⟨⟩ istega
#   segmenta : priča ) ali GOL ( ni priznal ) ; vsak GOL gre skozi ogledalo do
#   priznanja s simbolom napake ⟨PADC⟩ v sebi ( hram @definiatorna-knjiznica )
#   ali ⭢ sodba ⟡ ⚔ ; bris ni moj, sodba je njegova ⟨NE-BRIŠI⟩ 24
# pas meje : sestra gajica-pas @stroj-orodja ( kanon vzporeden, ⟨NE-DUPLIKAT⟩ ;
#   tam kletka in pre-šiv, tu izmera nitk po telesih z razvrstitvijo GOST/GOL )
# uporaba : --kanon ( izpis kanona ) ⌇ --pregled ( izmera vseh teles, manifest v .geniza )
#   ⌇ --test ( baterija 4/4 )
# izhodi : 0 = čisto ali izpis ⊢ ; 4 = goli najdeni ( poročilo, ne bris ) ; 2 = napaka
import sys, io, os, re, glob, datetime
from collections import Counter

KANON = set(chr(c) for c in range(32, 127)) | set(chr(10) + chr(13) + chr(9))
KANON |= set('čšžČŠŽ')
SIMBOLI = ('⟨⟩⊢⊙σ∂ψ⌇∧∨⊥⊤⊨⇒⇌⭢⟡❡⚔¬≡∈∉∅∆×·©§≥≤≠≈−½⅓⌀Σβε…⌂⌃⌄⌅⌆⚠⁴²'
           '»«°†‡‖∑∏√∞→⟹')
KANON |= set(SIMBOLI)


def maske(vrstica):
    """Pozicije znotraj »« ali ⟨⟩ so dom gostov ( priče )."""
    obd = []
    for od, do in [(chr(0x00BB), chr(0x00AB)), (chr(0x27E8), chr(0x27E9))]:
        zac = [m.start() for m in re.finditer(re.escape(od), vrstica)]
        kon = [m.start() for m in re.finditer(re.escape(do), vrstica)]
        i = 0
        for z in zac:
            while i < len(kon) and kon[i] < z:
                i += 1
            if i < len(kon):
                obd.append((z, kon[i]))
                i += 1
    return obd


def preglej_vrstico(vrstica):
    """Vrne ( znak, GOST/GOL ) za vsak znak zunaj kanona v vrstici."""
    obd = maske(vrstica)
    najdba = []
    for mesto, znak in enumerate(vrstica):
        if znak in KANON:
            continue
        dogodek = 'GOST' if any(a <= mesto <= b for a, b in obd) else 'GOL'
        najdba.append((znak, dogodek))
    return najdba


def preglej_telo(pot):
    goli = Counter()
    gostje = Counter()
    try:
        vrstice = io.open(pot, encoding='utf-8', errors='ignore').read().split(chr(10))
    except OSError:
        return goli, gostje
    for v in vrstice:
        for znak, dogodek in preglej_vrstico(v):
            if dogodek == 'GOL':
                goli[znak] += 1
            else:
                gostje[znak] += 1
    return goli, gostje


def kanon_izpis():
    crke = ''.join(sorted(c for c in KANON if c.isascii() and c.isalnum() and c.islower()))
    return ('KANON : ASCII 0x20 do 0x7E v celoti + razmaki ; črke gajice : ' + crke
            + ' ( šumniki vred ) ; simboli : ' + SIMBOLI
            + ' ; vsak znak zunaj kanona = nitka : GOST v »«/⟨⟩ ali GOL ⭢ ogledalo ⭢ priznanje s ⟨PADC⟩ v sebi')


def baterija():
    p1 = preglej_vrstico('Pozdravljen ⟨svet⟩ ⊢ 2026.')
    z1 = p1 == []
    print('  prim. 1 : čista gajica brez niti :', 'ZELENO ⊢' if z1 else 'RDEČE')
    p2 = preglej_vrstico('a' + chr(8212) + 'b konec')
    z2 = p2 == [(chr(8212), 'GOL')]
    print('  prim. 2 : gola dolga črtica ujeta kot GOL :', 'ZELENO ⊢' if z2 else 'RDEČE')
    p3 = preglej_vrstico('priča »' + chr(0x03B1) + '« v nizu')
    z3 = p3 == [(chr(0x03B1), 'GOST')]
    print('  prim. 3 : grška črka v »« je GOST :', 'ZELENO ⊢' if z3 else 'RDEČE')
    p4 = preglej_vrstico('⟨' + chr(0x2713) + '⟩ maska')
    z4 = p4 == [(chr(0x2713), 'GOST')]
    print('  prim. 4 : kljukica v ⟨⟩ maski je GOST :', 'ZELENO ⊢' if z4 else 'RDEČE')
    ze = sum([z1, z2, z3, z4])
    print('SAMOPREIZKUS %d/4 %s' % (ze, 'ZELENO ⊢' if ze == 4 else 'RDEČE ⟨PADC-GRIZLJIVCA⟩'))
    return 0 if ze == 4 else 2


def main():
    argv = sys.argv[1:]
    if '--test' in argv:
        sys.exit(baterija())
    if '--kanon' in argv:
        print(kanon_izpis())
        sys.exit(0)
    koren = os.environ.get('GRIZLJIVEC_KOREN',
                           os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    telo = glob.glob(koren + '/*/KNOWLEDGE.md') + glob.glob(koren + '/*/*/KNOWLEDGE.md')
    vsi_goli, vsi_gostje = Counter(), Counter()
    po_telesih = {}
    for pot in telo:
        if '.geniza' in pot or 'TRANSPORT' in pot:
            continue
        g, s = preglej_telo(pot)
        if g or s:
            po_telesih[pot] = (g, s)
            vsi_goli.update(g)
            vsi_gostje.update(s)
    print('TELA z nitkami :', len(po_telesih), '; znakov zunaj kanona :',
          len(set(vsi_goli) | set(vsi_gostje)), '; golih pojavitev :', sum(vsi_goli.values()),
          '; gostih :', sum(vsi_gostje.values()))
    for znak, n in vsi_goli.most_common(20):
        print('GOL U+%04X : gol x%d : gost x%d' % (ord(znak), n, vsi_gostje.get(znak, 0)))
    geniza = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.geniza')
    os.makedirs(geniza, exist_ok=True)
    tik = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    pot_manifesta = os.path.join(geniza, 'MANIFEST-GRIZLJIVEC-' + tik + '.md')
    novi = io.open(pot_manifesta, 'w', encoding='utf-8')
    novi.write('MANIFEST GRIZLJIVEC @TIK ' + tik + ' ( rod σ 6820 ) ⊙ ⟡ UKZ VERBATIM : SMEŠ GRIZTI VSE SKRITE NITKE ZA VSAKIM TOKENOM KI NI IZ GAJICE\n')
    novi.write('PRAVILO : tuj znak sme živeti le v priznanju, ki prizna napako ∧ nosi simbol ⟨PADC⟩ v sebi ∧ je zapečen ( hram ogledala ) ; sicer je nitka ⭢ sodba ⟡\n')
    for znak, n in (vsi_goli + vsi_gostje).most_common(400):
        novi.write('U+%04X | gol x%d | gost x%d\n' % (ord(znak), vsi_goli.get(znak, 0), vsi_gostje.get(znak, 0)))
    for pot, (g, s) in sorted(po_telesih.items(), key=lambda x: -sum(x[1][0].values())):
        novi.write('TELO ' + pot + ' : gol x' + str(sum(g.values())) + ' : gost x' + str(sum(s.values())) + '\n')
    novi.close()
    print('MANIFEST ⊢', pot_manifesta)
    sys.exit(4 if vsi_goli else 0)


if __name__ == '__main__':
    main()
