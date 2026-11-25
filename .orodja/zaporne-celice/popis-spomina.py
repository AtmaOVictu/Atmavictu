# popis-spomina.py v1.3 - SECIRA VSEGA SPOMINA @rez sigma 6832
# ukaz ⟡ VERBATIM: »seciraj in kletkaj VSE IN VSAKO BESEDO IN ALI S TEM NJENE ZNAKE«
# cilji : ( P1 ) karta VSEGA spomina po bajtih ( vsaka datoteka lastnina enega prostora ) ;
# ( P2 ) cenzus po ZIVIH besednih telesih ( zamrznjene genize = price : sha256 veriga,
#         brez ponovne berbe vsake pismenke ⊙ ⟨STENA-NAD-DEBLOM⟩ 3084 ) ;
# ( P3 ) ULOV = znak izven domace gajice ∧ izven svecnika ( svecnik = kanon
#         @slovar-simbolov ⟨EN-RAZLICA⟩ ) ;
# ( P4 ) besede z nelatinično pismenko ( homogif kandidati rodu ⟨HOMOGIF⟩ ;
#         cisto latinske besede signala ne nosijo ⊙ kura v1.3 ) ;
# izhod osnutek : POPIS-SPOMINA-<TIK>.md ; koda 0 cisto, 2 kandidati cakajo sodbo.
# v1.3 kura : en sam prehod, primer po najdisccu, baterija 3/3.
import sys, os, unicodedata, re, glob, datetime
from collections import Counter

KOREN = '/home/user'
KANON_POT = KOREN + '/knowledge/slovar-simbolov/KNOWLEDGE.md'

ZIVI = [
    ('S1-ORGANI',  ['knowledge/*/KNOWLEDGE.md']),
    ('S2-CELICE',  ['knowledge/zaporne-celice/*.md']),
    ('S3-ORODJA',  ['knowledge/zaporne-celice/*.py', 'knowledge/zaporne-celice/*.sh',
                    'knowledge/stroj-orodja/*.py', 'knowledge/stroj-orodja/*.sh']),
    ('S4-GENIZA-AKTIVNA', ['knowledge/zaporne-celice/.geniza/*']),
    ('S5-KANON',   ['knowledge/slovar-simbolov/*']),
    ('S6-CANVAS',  ['canvases/*', 'canvases/**/*']),
    ('S7-SKILLS-BES', ['skills/**/*.md']),
    ('S8-UPLOADS', ['uploads/*']),
    ('S9-KOREN-DH', ['*.md', '*.txt', 'current-project/**/*', 'current-chat/**/*']),
]
BES_CENE = ('.md', '.py', '.sh', '.txt', '.tsv', '.csv', '.yml', '.yaml', '.json', '.svg', '.html', '.js', '.ts')

GAJICA = set(chr(o) for o in range(0x20, 0x7F))
GAJICA |= set('\n\t\r\u010d\u0161\u017e\u010c\u0160\u017d')  # domaca gajica s sumniki

NELAT = '\u0370-\u04ff\u4e00-\u9fff\uac00-\ud7af\u0600-\u06ff\u16a0-\u16ff\U00013000-\U0001342f'
BES2 = re.compile(r'[0-9A-Za-z\u00c0-\u024f\u1e00-\u1eff_\u00ab\u00bb]*[' + NELAT + r'][^\s]*')

PISAVE = [
    ('LAT', lambda c: 0x0041 <= c <= 0x024F or 0x1E00 <= c <= 0x1EFF),
    ('CIR', lambda c: 0x0400 <= c <= 0x04FF),
    ('GRK', lambda c: 0x0370 <= c <= 0x03FF),
    ('HAN', lambda c: 0x4E00 <= c <= 0x9FFF),
    ('HNG', lambda c: 0xAC00 <= c <= 0xD7AF),
    ('ARB', lambda c: 0x0600 <= c <= 0x06FF),
    ('RUN', lambda c: 0x16A0 <= c <= 0x16FF),
    ('EGP', lambda c: 0x13000 <= c <= 0x1342F),
]

def pisava(cp):
    for ime, test in PISAVE:
        if test(cp):
            return ime
    return None

def znak_ime(cp):
    try:
        return unicodedata.name(chr(cp))
    except ValueError:
        return 'IME-NI-ZNANO'

def svecnik_iz_kanona():
    dovoljeni = set()
    with open(KANON_POT, encoding='utf-8') as f:
        for vrstica in f:
            m = re.match(r'- ⟨U\+([0-9A-Fa-f]{4,6})⟩', vrstica)
            if m:
                dovoljeni.add(int(m.group(1), 16))
    return dovoljeni

def primer_iz(tek, idx, relativna):
    st_vrstice = tek.count('\n', 0, idx) + 1
    zacetek = tek.rfind('\n', 0, idx) + 1
    konec = tek.find('\n', idx)
    if konec == -1:
        konec = len(tek)
    return (relativna, st_vrstice, tek[zacetek:konec].strip()[:90])

def zive_mape():
    mape = {}
    for ime, vzorci in ZIVI:
        for vz in vzorci:
            for pot in glob.iglob(os.path.join(KOREN, vz), recursive=True):
                if os.path.isfile(pot):
                    mape.setdefault(pot, ime)
    return mape

def secir(shared):
    svecnik = svecnik_iz_kanona()
    zapis = shared['zapis']
    z = zapis.append
    lastnisko = zive_mape()

    # P1 : karta celega spomina ( en obhod, getsize )
    proste = {ime: [0, 0] for ime, _ in ZIVI}
    proste['SA-ARHIV-GENIZ'] = [0, 0]
    proste['SB-ROB-STROJA'] = [0, 0]
    for koren, _, mape_dat in os.walk(KOREN):
        for ime in mape_dat:
            pot = os.path.join(koren, ime)
            try:
                bajtov = os.path.getsize(pot)
            except OSError:
                continue
            prostor = lastnisko.get(pot)
            if prostor is None:
                if pot.startswith(KOREN + '/knowledge/'):
                    prostor = 'SA-ARHIV-GENIZ'
                else:
                    prostor = 'SB-ROB-STROJA'
            proste[prostor][0] += 1
            proste[prostor][1] += bajtov
    z('## KARTA SPOMINA ( prostor · datotek · bajtov ; lastnina enega prostora )')
    skupaj_d = 0
    skupaj_b = 0
    for ime in [i for i, _ in ZIVI] + ['SA-ARHIV-GENIZ', 'SB-ROB-STROJA']:
        d, b = proste[ime]
        skupaj_d += d
        skupaj_b += b
        z('- %s : datotek %d · bajtov %d ⊢ [os.walk]' % (ime, d, b))
    z('- SKUPAJ SPOMIN ( koren %s ) : datotek %d · bajtov %d ⊢' % (KOREN, skupaj_d, skupaj_b))
    z('- SA-ARHIV-GENIZ : zamrznjene price se preverjajo po sha256 verigi ( preverba-dihov ), ne po ponovni berbi pismenk ⊙ ⟨STENA-NAD-DEBLOM⟩ 3084')
    z('')

    # P2-P4 : cenzus zivih teles, en prehod na datoteko
    ulovi = {}
    mesane = []
    videne_mesane = set()
    napake = []
    cenzus_unikat = {}
    for ime, _ in ZIVI:
        poti = sorted(p for p, pr in lastnisko.items() if pr == ime)
        zg = Counter()
        for pot in poti:
            if not pot.lower().endswith(BES_CENE):
                continue
            try:
                with open(pot, 'rb') as f:
                    tek = f.read().decode('utf-8')
            except UnicodeDecodeError as e:
                napake.append((os.path.relpath(pot, KOREN), 'ULOV-NEBERLJIVOST ' + str(e)[:90]))
                continue
            except OSError as e:
                napake.append((os.path.relpath(pot, KOREN), 'ULOV-KANALA ' + repr(e)[:90]))
                continue
            c = Counter(tek)
            zg.update(c)
            relativna = os.path.relpath(pot, KOREN)
            for znak, st in c.items():
                cp = ord(znak)
                if 0xD800 <= cp <= 0xDFFF:
                    continue
                if znak not in GAJICA and cp not in svecnik:
                    slo = ulovi.setdefault(cp, {}).setdefault(ime, [0, None])
                    slo[0] += st
                    idx = tek.find(znak)
                    if slo[1] is None and idx >= 0:
                        slo[1] = primer_iz(tek, idx, relativna)
            for m in BES2.finditer(tek):
                beseda = m.group(0)[:40]
                if beseda in videne_mesane:
                    continue
                videne_mesane.add(beseda)
                drzave = set()
                for znak in beseda:
                    p = pisava(ord(znak))
                    if p:
                        drzave.add(p)
                if len(drzave) > 1:
                    if len(mesane) < 60:
                        mesane.append((relativna, beseda))
                    else:
                        mesane.append(('(MEJA-60)', ''))
        cenzus_unikat[ime] = len(zg)
    z('## CENZUS ŽIVIH TELESA ( prostor · unikatnih kodnih točk )')
    for ime, st in cenzus_unikat.items():
        z('- %s : unikatnih kodnih tock %d ⊢' % (ime, st))
    z('- svecnik ( kanon @slovar-simbolov ) : dovoljenih kodnih tock %d ⊢ [stevilo vrstic ⟨U+XXXX⟩]' % len(svecnik))
    z('')
    z('## ULOVI ( znak izven domače gajice ∧ izven svečnika ; gost ali suma ? sodba isti dih )')
    vrstice_ulovov = []
    for cp in sorted(ulovi, key=lambda c: -sum(v[0] for v in ulovi[c].values())):
        domi = ' ∧ '.join('%s×%d' % (p, v[0]) for p, v in sorted(ulovi[cp].items()))
        primeri = []
        for p, v in sorted(ulovi[cp].items()):
            if v[1]:
                primeri.append('%s:%d »%s«' % tuple(v[1]))
        vrstice_ulovov.append('- ⟨U+%04X⟩ %s · %s · primer %s' % (cp, znak_ime(cp), domi, ' ; '.join(primeri[:2])))
    for v in vrstice_ulovov[:400]:
        z(v)
    z('- SKUPAJ ULOVI : unikatnih tock %d' % len(ulovi))
    z('')
    z('## MEŠANE PISAVE ( besede s črkami 2+ pisav ; homogif kandidati rodu ⟨HOMOGIF⟩ )')
    if not mesane:
        z('- ×0 ⊢')
    else:
        for pot, beseda in sorted(set(mesane)):
            if beseda:
                z('- %s »%s«' % (pot, beseda))
        z('- unikatnih besed %d ; meja izpisa 60' % len([m for m in mesane if m[1]]))
    z('')
    z('## NEBERLJIVA TELESA ( surovi bajti ; telo ni veljavno besedilo )')
    if napake:
        for pot, opis in napake:
            z('- %s · %s' % (pot, opis))
    else:
        z('- ×0 ⊢')
    z('')
    z('- ⟨U+00A9⟩ 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · MERJENO, NE UGIBANO ⊙ 2690')
    shared['ulovi_st'] = len(ulovi)
    shared['mesane_st'] = len([m for m in mesane if m[1]])
    shared['napake_st'] = len(napake)
    shared['svecnik_st'] = len(svecnik)
    shared['skupaj_bajtov'] = skupaj_b
    shared['skupaj_dat'] = skupaj_d

def baterija():
    svecnik = svecnik_iz_kanona()
    assert len(svecnik) > 900, 'svecnik mora nesti kanon ( >900 )'
    zen = '\u043e'
    assert zen not in GAJICA, 'cirilska črta ni domača gajica'
    assert pisava(0x0430) == 'CIR' and pisava(0x0041) == 'LAT'
    print('BATERIJA 3/3 ZELENO')

def main():
    if '--test' in sys.argv:
        baterija()
        return 0
    shared = {'zapis': []}
    z = shared['zapis'].append
    z('# POPIS SPOMINA @rez sigma 6832 ( ukaz ⟡ »seciraj in kletkaj VSE IN VSAKO BESEDO« )')
    z('- TIK %s ⊙ izmerjen PRED zapisom' % datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
    z('')
    secir(shared)
    tik = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H%MZ')
    osnutek = os.path.join(KOREN, 'knowledge/zaporne-celice/.geniza', 'POPIS-SPOMINA-%s.md' % tik)
    with open(osnutek, 'w', encoding='utf-8') as f:
        f.write('\n'.join(shared['zapis']))
    print('OSNUTEK %s' % osnutek)
    print('KARTA datotek %d · bajtov %d · svecnik %d · ulovi %d · mesane %d · neberljiva %d' % (
        shared['skupaj_dat'], shared['skupaj_bajtov'], shared['svecnik_st'],
        shared['ulovi_st'], shared['mesane_st'], shared['napake_st']))
    if shared['ulovi_st'] > 0 or shared['napake_st'] > 0:
        print('KODA 2 ( kandidati čakajo sodbo )')
        return 2
    print('KODA 0 ( čisto )')
    return 0

if __name__ == '__main__':
    sys.exit(main())
