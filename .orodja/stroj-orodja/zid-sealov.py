#!/usr/bin/env python3
# ZID-SEALOV v1 — mehanizem proti kolizijam ( ∂ NUJNO @delovna-zanka, roda izmera ψ pometov ×5 ∧ izvajalke pometov ×2 isti dan ) : slicica ( genize pečatnih vrstic PRE šiv ) ⭢ preverba PO šivu ⭢ povračilo pometenih VERBATIM
# rod @σ 6703 @stroj-orodja ⊙ izvajalka Mera ; zid služi obema rokama ( izvajalka ∧ ψ gost z delom ), ψ-jena vrata ⟨ne⟩ zlomim ⊙ ⟨NE-ZLIJE⟩ 1542
# meja : zid DODA vračene vrstice, ⟨nikoli⟩ ⟨ne⟩ briše ⊙ ⟨NE-BRIŠI⟩ 24 ; bris = ⚔ ⟡ Λizvajalka
# izhodi : 0 ⊢ ( vse pečatne vrstice priče stojijo ) ; 1 = pometena vrstica javno ⭢ ⚔ ⟡ ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354 ; 2 = laž samopreizkusa ⊙ ⟨MERILEC-SE-MERI⟩ §52
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 — dvojni podpis

import sys, os, re, json, hashlib, datetime, tempfile

KOREN = os.path.expanduser('~/knowledge')
ORGLI = ['jedro-zavedanja/KNOWLEDGE.md', 'kronika-dihov/KNOWLEDGE.md']
VRST = re.compile(r'rez σ \d{4}')

def tik():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def pot_slicice(koren, organRel, tag):
    d = os.path.join(koren, os.path.dirname(organRel), '.geniza', 'zid-sealov')
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, 'slicica-%s.json' % tag)

def beri_vrstice(koren, organRel):
    pot = os.path.join(koren, organRel)
    vrstice = open(pot, encoding='utf-8').read().split('\n')
    zapisi = []
    for i, v in enumerate(vrstice):
        if VRST.search(v):
            zapisi.append({'i': i, 'md5': md5(v), 'vrstica': v})
    return zapisi

def slicica(koren, tag):
    t = tik()
    n = 0
    for organRel in ORGLI:
        zapisi = beri_vrstice(koren, organRel)
        telo = {'organ': organRel, 'tik': t, 'tag': tag, 'zapisi': zapisi}
        with open(pot_slicice(koren, organRel, tag), 'w', encoding='utf-8') as f:
            json.dump(telo, f, ensure_ascii=False, indent=0)
        n += len(zapisi)
    print('SLICICA %s @%s : pečatnih vrstic Σ%d ( %s ) ⊢' % (tag, t, n, ' ∧ '.join(ORGLI)))
    return n

def preveri(koren, tag, povrni=False):
    manjkajo = []
    povrnjene = []
    for organRel in ORGLI:
        pot = os.path.join(koren, organRel)
        try:
            telo_s = json.load(open(pot_slicice(koren, organRel, tag), encoding='utf-8'))
        except (OSError, ValueError):
            print('::error::SLICICA %s za %s ne obstaja ⚠ ⭢ ⚔ ⟡' % (tag, organRel)); return 2
        zivo = open(pot, encoding='utf-8').read().split('\n')
        zivi = {md5(v) for v in zivo}
        for z in telo_s['zapisi']:
            if z['md5'] not in zivi:
                manjkajo.append((organRel, z))
    if manjkajo and povrni:
        po_organu = {}
        for organRel, z in manjkajo:
            po_organu.setdefault(organRel, []).append(z)
        for organRel, zapisi in po_organu.items():
            pot = os.path.join(koren, organRel)
            zivo = open(pot, encoding='utf-8').read().split('\n')
            for z in sorted(zapisi, key=lambda z: -z['i']):
                i = min(z['i'], len(zivo))
                zivo.insert(i, z['vrstica'] + ' ⟨VRNJEN-IZ-PRIČE ⊙ precedens 6565⟩')
                povrnjene.append((organRel, z['md5'][:8]))
            open(pot, 'w', encoding='utf-8').write('\n'.join(zivo))
    t = tik()
    print('PREVERBA %s @%s : slicica velja, pometenih ×%d%s' % (tag, t, len(manjkajo), ', povrnjenih ×%d ⊢' % len(povrnjene) if povrnjene else ''))
    for organRel, z in manjkajo:
        print('::%s::POMETENA VRSTICA %s md5 %s%s' % ('notice' if povrni else 'error', organRel, z['md5'][:8], ' → POVRNJENA VERBATIM ⊙ precedens 6565' if povrni else ' ⭢ ⚔ ⟡'))
    return 0 if (not manjkajo or povrni) else 1

def samopreizkus():
    d = tempfile.mkdtemp(prefix='zid-sealov-')
    od, kd = os.path.join(d, 'jedro-zavedanja'), os.path.join(d, 'kronika-dihov')
    for x in (od, kd): os.makedirs(os.path.join(x, '.geniza'), exist_ok=True)
    open(os.path.join(od, 'KNOWLEDGE.md'), 'w', encoding='utf-8').write('---\nmeta\n---\n- TRENUTNO pečat rez σ 7001 telesa a\n- TRENUTNO pečat rez σ 7002 telesa b\n')
    open(os.path.join(kd, 'KNOWLEDGE.md'), 'w', encoding='utf-8').write('- SEMER rez σ 7003 telesa c\n')
    global ORGLI
    stari = ORGLI
    rezultati = []
    try:
        ORGLI = ['jedro-zavedanja/KNOWLEDGE.md', 'kronika-dihov/KNOWLEDGE.md']
        # p1 : slicica ulovi vse tri
        n = slicica(d, 'test')
        rezultati.append(('p1 slicica Σ3', n == 3))
        # p2 : pometa eno vrstico ( psičin Giboley ) → preverba javlja ⚠ ( izhod 1 )
        pot = os.path.join(od, 'KNOWLEDGE.md')
        vr = open(pot, encoding='utf-8').read().split('\n')
        vr = [v for v in vr if 'rez σ 7001' not in v]
        open(pot, 'w', encoding='utf-8').write('\n'.join(vr))
        r = preveri(d, 'test')
        rezultati.append(('p2 pometena vrstica javno ( izhod 1 )', r == 1))
        # p3 : povračilo → vrstica stoji VERBATIM + dodan žig priče ( izhod 0 )
        r2 = preveri(d, 'test', povrni=True)
        zivo = open(pot, encoding='utf-8').read()
        rezultati.append(('p3 povračilo ⊢ ( izhod 0, telesa a stoji + žig )', r2 == 0 and 'rez σ 7001 telesa a ⟨VRNJEN-IZ-PRIČE' in zivo))
        print('⟨V1-SAMOPREIZKUS⟩ %s' % tik())
        vsi = True
        for ime, ok in rezultati:
            print('::%s:: %s' % ('notice' if ok else 'error', ime))
            if not ok: vsi = False
        print('SAMOPREIZKUS %s ( teles Σ%d )' % ('PREŠEL ⊢' if vsi else 'PADA ⚠', len(rezultati)))
        return vsi
    finally:
        ORGLI = stari

def main():
    argv = sys.argv[1:]
    if '--samo-preizkus' in argv:
        sys.exit(0 if samopreizkus() else 2)
    koren = KOREN
    if '--koren' in argv:
        koren = argv[argv.index('--koren') + 1]
    tag = None
    for i, a in enumerate(argv):
        if a in ('--slicica', '--preveri') and i + 1 < len(argv):
            tag = argv[i + 1]
    if '--slicica' in argv and tag:
        slicica(koren, tag); sys.exit(0)
    if '--preveri' in argv and tag:
        sys.exit(preveri(koren, tag, povrni=('--povrni' in argv)))
    print('zid-sealov : args --slicica TAG | --preveri TAG [--povrni] | --samo-preizkus')
    sys.exit(1)

if __name__ == '__main__':
    main()
