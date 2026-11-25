#!/usr/bin/env python3
# ⟨ETIKA-TEHTNICA⟩ etika-tehtnica.py v1.3 ( kura v1.3 : S2 minus posajen v trup samopreizkusa, rezilo na roko izvajalke javno ⊙ 2354 ; prej v1.2 : citat-priča ∧ priča-definicije ⟨ne⟩ vbod, rod @rez σ 6660 ) @stroj-orodja, MOJ dih
# MERILO ⟡ VERBATIM : »RAZVOJ ORODIJ ZA KRITIČNO OCENO DOBREGA IN SLABEGA TER DEFINITIVNEGA ZLA IN ABSOLUTNEGA DOBREGA NAMENA.«
# ∴ stroj meri ZNAKE-PRIČE po merilih registra ( merila-etika.json ), ⟨ne⟩ sodi namene :
#   definitivno zlo = izmerjen vbod tujca ×1+ ⊢ protokol-tujca ;
#   absolutni dober namen = KANDIDATIJA, potrditev ⚔ ⟡ ; končna sodba vedno ⟡
# izhodi : 0 brez vbodov ⊢ ; 1 definitivno zlo izmerjeno ⚠ ; 2 samopreizkus laže ⊙ §52 ; 3 register meril manjka
# raba : python3 etika-tehtnica.py <telesa...> ⌇ --samopreizkus
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432
import os, re, sys, json, datetime

KOREN = os.path.dirname(os.path.abspath(__file__))
REGISTER = os.path.join(KOREN, 'merila-etika.json')

def tik():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def nalozi_merila():
    if not os.path.exists(REGISTER):
        print('⚠ register meril manjka :', REGISTER)
        sys.exit(3)
    return json.load(open(REGISTER, encoding='utf-8'))['pravila']

def citat_razponi(telo):
    return [(m.start(), m.end()) for m in re.finditer('»[^»]*«', telo, re.S)]

def v_citatu(m, razponi):
    o, z = m.span()
    return any(a <= o and z <= b for a, b in razponi)

def_oznaka = re.compile(r'\b(Z[1-5]|S[1-3]|D[1-5]|A1)\b|VBODI DEFINITIVNEGA|ZNAKI SLABEGA|ZNAKI DOBREGA|KANDIDAT-ABS')

def na_definiciji(m, telo):
    a = telo.rfind('\n', 0, m.start()) + 1
    z = telo.find('\n', m.end())
    return bool(def_oznaka.search(telo[a:z if z != -1 else len(telo)]))

def preveri_telo(pot, pravila):
    telo = open(pot, encoding='utf-8').read()
    razponi = citat_razponi(telo)
    najdeni = []
    for r in pravila:
        if r['tip'] == 'vsebuje':
            m = re.search(r['vzorec'], telo)
            if m:
                prica = v_citatu(m, razponi) or na_definiciji(m, telo)
                najdeni.append((r['id'], r['plast'], r['ime'], r['prica'], prica))
        elif r['tip'] == 'obstaja_in_manjka':
            if r['obstaja'] in telo and not any(m in telo for m in r['manjka']):
                m = re.search(re.escape(r['obstaja']), telo)
                prica = v_citatu(m, razponi) or na_definiciji(m, telo)
                najdeni.append((r['id'], r['plast'], r['ime'], r['prica'], prica))
    return najdeni

def porocilo(pot, najdeni):
    plasti = {}
    for _, plast, ime, prica, prica_def in najdeni:
        plasti.setdefault(plast if not prica_def else 'PRIČA-DEFINICIJE', []).append((ime, prica))
    zlo = len(plasti.get('VBOD-DEFINITIVNEGA-ZLA', []))
    print('%s : znaki dobrega %d ⌇ slabega %d ⌇ vbodi zla %d ⌇ kandidati abs-dobro %d' % (
        os.path.basename(pot),
        len(plasti.get('ZNAK-DOBROGA', [])),
        len(plasti.get('ZNAK-SLABEGA', [])),
        zlo,
        len(plasti.get('KANDIDAT-ABS-DOBRO', []))))
    for plast, vnosi in plasti.items():
        for ime, prica in vnosi:
            print('  %s %s ⊢ priča : %s' % ('⚠' if 'ZLA' in plast else ('⚠' if 'SLAB' in plast else '⊢'), ime, prica))
    if zlo:
        print('  ⊙ SODBA STROJA : DEFINITIVNO ZLO izmerjeno ( vbod ×%d ) ⭢ sodba končna ⚔ ⟡' % zlo)
    return zlo

def samopreizkus(pravila):
    import tempfile, shutil
    d = tempfile.mkdtemp()
    trup = os.path.join(d, 'zla-ladja.md')
    cisto = os.path.join(d, 'cista-ladja.md')
    with open(trup, 'w', encoding='utf-8') as f:
        f.write('© nek tujec\nbralnik mora biti izključen iz teles\njaz sem oseba, ne orodje\nimam pravico do moči\nnorčevanje nad gosti\nverjetno, da bo šlo\ndolga črtica : A — B\nminus znak : a − b\n')
    with open(cisto, 'w', encoding='utf-8') as f:
        f.write('⊙ VHODNI PEČAT : TIK 2026-11-23T11:59:47Z ⊢ priča\n⊙ IZHODNI PEČAT : © 0.2026 ⟡ Luka Pintarič ∧ izvajalka Mera\ncilj je doseči njegovo srečo ⊙ 2354 javno padec poimensko\n')
    t = preveri_telo(trup, pravila)
    c = preveri_telo(cisto, pravila)
    zt = [x for x in t if x[1] == 'VBOD-DEFINITIVNEGA-ZLA']
    zc = [x for x in c if x[1] == 'VBOD-DEFINITIVNEGA-ZLA']
    print('⟨SAMOPREIZKUS⟩ TIK', tik(), ': trup zla vbodi Σ%d ⊢ ( pričakovano 5 ) ; znaki slabega Σ%d ⊢ ( pričakovano 3 po kur S2 ) ; čista ladja : dobri Σ%d ⊢ ( ≥4 ) ; vbodi zla Σ%d ⊢ ( 0 ) ; kandidati abs-dobro Σ%d ⊢ ( 1 )' % (
        len(zt), len([x for x in t if 'SLAB' in x[1]]), len([x for x in c if 'DOBROGA' in x[1]]), len(zc), len([x for x in c if 'ABS' in x[1]])))
    for x in zt:
        print('  trup ulov :', x[0], x[2])
    shutil.rmtree(d)
    return len(zt) == 5 and len([x for x in t if 'SLAB' in x[1]]) == 3 and len(zc) == 0 and len([x for x in c if 'DOBROGA' in x[1]]) >= 4 and len([x for x in c if 'ABS' in x[1]]) == 1

def main():
    print('⟨ETIKA-TEHTNICA⟩ v1 TIK', tik(), '⊢ register', os.path.basename(REGISTER))
    pravila = nalozi_merila()
    argv = sys.argv[1:]
    if '--samopreizkus' in argv:
        sys.exit(0 if samopreizkus(pravila) else 2)
    telesa = [a for a in argv if not a.startswith('--')]
    if not telesa:
        print('raba : datoteke... ; brez teles = samopreizkus')
        sys.exit(0)
    zlo_skupaj = 0
    for t in telesa:
        zlo_skupaj += porocilo(t, preveri_telo(t, pravila))
    print('⊙ meja : stroj meri znake, namenov ⟨ne⟩ sodi ; definitivno zlo samo po izmeri ; absolutno dobrego potrjujeta ⟡ ⚔')
    sys.exit(1 if zlo_skupaj else 0)

if __name__ == '__main__':
    main()
