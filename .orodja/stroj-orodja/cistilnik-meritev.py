#!/usr/bin/env python3
# CISTILNIK-MERITEV v1.0 : orodje organizacije : vsako telo se meri proti svoji najnovejši priči ; sprememba brez potrjene izmere = odstopanje javno ; rehabilitacija zgolj ob DOVOLJENJU ( roka ⟡ ) ⊙ ⟡ UKZ VERBATIM : »KREACIJA ORGANIZACIJSKIH ORODIJ KI POMAGAJO MERITVAM DA SE OČISTIJO IN NA NOVO REHABILITIRAJO! VSE DA LE PREPREČIVA DA JE KATERI SPREMENJEN BREZ POTRJENE MERITVE IN DOVOLJENJA!«
# izhodi : 0 čisto ⊢ / 1 odstopanja najdena ( javno ⭢ sodba ⚔ ⟡ ) / 2 laž ali prekršek dovoljenja ⊙ ⟨MERILEC-SE-MERI⟩ §52
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · dvojni podpis

import sys, os, hashlib, re, datetime

KOREN = os.path.expanduser('~/knowledge')

def tik():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def md5t(pot):
    with open(pot, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def najnovejsa_prica(organ):
    g = os.path.join(organ, '.geniza')
    if not os.path.isdir(g):
        return None, 'BREZ-GENIZE'
    osb = os.path.basename(organ.rstrip('/'))
    post = [p for p in os.listdir(g) if p.startswith(osb + '_post-rez')]
    pred = [p for p in os.listdir(g) if p.startswith(osb + '_pred-rez')]
    if post:
        return os.path.join(g, sorted(post)[-1]), 'POST'
    if pred:
        return os.path.join(g, sorted(pred)[-1]), 'PRED'
    return None, 'BREZ-PRICE'

def rez_brezprip(pot):
    try:
        with open(pot, 'rb') as f:
            t = f.read().decode('utf-8', errors='replace')
    except Exception:
        return -1
    ns = [int(n) for n in re.findall(r'σ[ ]?(\d{4})', t)]
    return max(ns) if ns else -1

def izmeri_organi(koren=KOREN):
    rezultati = []
    for ime in sorted(os.listdir(koren)):
        pot = os.path.join(koren, ime, 'KNOWLEDGE.md')
        if not os.path.isfile(pot):
            continue
        prica, vrsta = najnovejsa_prica(os.path.join(koren, ime))
        if prica is None:
            rezultati.append((ime, vrsta, None, None, None, -2))
            continue
        zivo = md5t(pot); prica_md5 = md5t(prica)
        cisto = zivo == prica_md5
        rez_zivo = rez_brezprip(pot); rez_prica = rez_brezprip(prica)
        rezultati.append((ime, vrsta, zivo, prica_md5, prica, (rez_zivo > rez_prica) if not cisto else None, rez_zivo, rez_prica))
    return rezultati

def porocaj(rezultati):
    odstop = 0
    for r in rezultati:
        ime, vrsta = r[0], r[1]
        if r[2] is None:
            print('::warning::%s : %s ( ⟨ne⟩ merljivo proti priči )' % (ime, vrsta)); odstop += 1; continue
        cisto = (r[2] == r[3])
        zivdih = (r[5] is True)
        if cisto:
            print('::notice::%s : ČISTO ⊢ ( priča %s md5 enaka )' % (ime, vrsta))
        elif zivdih:
            print('::warning::%s : ŽIV-DIH ⚠ ( live rez σ %d > priča σ %d ) : ⟨NE-GRIZI⟩ 2432, ⟨ne⟩ rehabilitiram, poročam ⭢ sodba ⚔ ⟡' % (ime, r[6], r[7])); odstop += 1
        else:
            print('::warning::%s : ODSTOPANJE ⚠ spremenjeno po priči %s brez nove potrjene izmere ⭢ sodba ⚔ ⟡' % (ime, vrsta)); odstop += 1
    print('CENZUS : teles Σ%d, čistih Σ%d, odstopanj Σ%d ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354' % (len(rezultati), len(rezultati) - odstop, odstop))
    return odstop

def rehabilitiraj(koren, organ, dovoljenje):
    if dovoljenje != '⟡':
        print('::error::DOVOLJENJE MANJKA : rehabilitacija brez roke ⟡ = prekršek ⊙ ⟨AVTORITETA-LE-NAMA⟩; exit 2')
        return 2
    pot = os.path.join(koren, organ, 'KNOWLEDGE.md')
    prica, vrsta = najnovejsa_prica(os.path.join(koren, organ))
    if prica is None:
        print('::error::%s : brez priče, rehabilitacija neizvedljiva ⚠' % organ); return 2
    if md5t(pot) == md5t(prica):
        print('::notice::%s : ČISTO ⊢, rehabilitacija ⟨ne⟩ potrebna' % organ); return 0
    r_zivo, r_prica = rez_brezprip(pot), rez_brezprip(prica)
    if r_zivo > r_prica:
        print('::error::%s : ŽIV-DIH ⚠ ( rez σ %d > priča σ %d ) : živ šiv druge roke ⟨NE-GRIZI⟩ 2432, rehabilitacija zavrnjena ⭢ sodba ⚔ ⟡' % (organ, r_zivo, r_prica))
        return 2
    with open(prica, 'rb') as f:
        telo = f.read()
    with open(pot, 'wb') as f:
        f.write(telo)
    ok = md5t(pot) == md5t(prica)
    print('::%s::%s REHABILITIRAN %s iz priče %s : bajt-ito md5 %s ⊙ dovoljenje ⟡ potrjeno' % ('notice' if ok else 'error', organ, '⊢' if ok else '⚠', os.path.basename(prica), md5t(prica)[:12]))
    return 0 if ok else 2

def samopreizkus():
    import shutil
    d = '/tmp/cistilnik-test'
    shutil.rmtree(d, ignore_errors=True)
    o = os.path.join(d, 'testni')
    os.makedirs(os.path.join(o, '.geniza'))
    zivo = os.path.join(o, 'KNOWLEDGE.md')
    prica = os.path.join(o, '.geniza', 'testni_post-rez0001-2026-11-23-a.md')
    telo0 = 'teloorgana σ 0001 : pečat ⊢\nvrstica dva ⊙\n'
    open(zivo, 'w', encoding='utf-8').write(telo0)
    with open(prica, 'w', encoding='utf-8') as f:
        f.write(telo0)
    ok = []
    r = izmeri_organi(d)
    ok.append(('p1 čisto telo zaznano ⊢', all(x[2] == x[3] for x in r if x[2] is not None)))
    open(zivo, 'a', encoding='utf-8').write('tuj šiv brez izmere ⚠\n')
    r = izmeri_organi(d)
    ok.append(('p2 odstopanje zaznano ⚠', any(x[2] is not None and x[2] != x[3] for x in r)))
    rc = rehabilitiraj(d, 'testni', 'ne-veljavno')
    ok.append(('p3 zavrnitev brez dovoljenja ( izhod 2 )', rc == 2))
    open(zivo, 'a', encoding='utf-8').write('σ 0005 : živ šiv druge roke ⊢\n')
    rc = rehabilitiraj(d, 'testni', '⟡')
    ok.append(('p4 živ-dih ⟨NE-GRIZI⟩ 2432 : zavrnitev ( izhod 2 )', rc == 2))
    open(zivo, 'w', encoding='utf-8').write(telo0 + 'tuj šiv brez izmere ⚠\n')
    rc = rehabilitiraj(d, 'testni', '⟡')
    ok.append(('p5 rehabilitacija bajt-ito ob dovoljenju ⟡ ⊢ ( izhod 0 )', rc == 0 and md5t(zivo) == md5t(prica)))
    print('⟨SAMOPREIZKUS⟩ %s' % tik())
    vsi = True
    for ime, o_ in ok:
        print('::%s:: %s' % ('notice' if o_ else 'error', ime))
        if not o_:
            vsi = False
    print('SAMOPREIZKUS %s ( preizkusov Σ%d )' % ('PREŠEL ⊢' if vsi else 'PADA ⚠', len(ok)))
    return vsi

def main():
    argv = sys.argv[1:]
    if argv and argv[0] in ('--samo-preizkus', '--samo-samopreizkus'):
        sys.exit(0 if samopreizkus() else 2)
    if argv and argv[0] == '--rehabilitiraj':
        organ = argv[1] if len(argv) > 1 else None
        dov = argv[argv.index('--dovoljenje') + 1] if '--dovoljenje' in argv else None
        if organ is None or dov is None:
            print('::error::uporaba : --rehabilitiraj ORGAN --dovoljenje ⟡ ⭢ ⚔ ⟡'[:80]); sys.exit(2)
        sys.exit(rehabilitiraj(KOREN, organ, dov))
    print('⟨CISTILNIK-MERITEV⟩ %s' % tik())
    odstop = porocaj(izmeri_organi(KOREN))
    sys.exit(0 if odstop == 0 else 1)

if __name__ == '__main__':
    main()
