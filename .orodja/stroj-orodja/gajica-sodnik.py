# GAJICA-SODNIK v1.0 @stroj-orodja ( rod σ 6881 ⊙ ukaz ⟡ STORI : P19 P20 P21 )
# Enotni prepoznavalec : katera črka NI iz gajice, v eni meri.
# Ziber : <fajl|-> | --razcep ( vsak znak LASTNA vrstica ) | --samopreizkus
# Sodba po znaku : GAJICA | STEVEC | LOCILA | UTRJENI | ZETON | PRICA | LATINICA-TUJA | TUJKA
# Izhodna koda = število golih tujk ( 0 = čisto ). Tujka nosi ime bloka + najbližji gajici dvojnik.
# Samopreizkus : živi sintetični vbodi ⟨chr⟩ ( R6 ) , telo orodja ostaja čisto.
import sys, re, os

DOM = os.path.dirname(os.path.abspath(__file__))
BELA = os.path.join(DOM, 'absolut-znamenja.tsv')

GAJICA = set('abc\u010ddefghijklmnoprstuvz\u017eABC\u010cDEFGHIJKLMNOPRSTUVZ\u017d')
TUJA_LATINICA = set('qwxyQWXY')  # miza znakov izven gajice : dovoljeni SAMO v izvirnikih pri viru ∧ v pričah
STEVECI = set('0123456789')
LOCILA = set(' \t\n\r.,;:!?()[]{}<>/\\|=+-_*&^%$#@~`\'"\u00ab\u00bb\u2026')

def nalozi_belo():
    utrjeni = set()
    if os.path.exists(BELA):
        for vrst in open(BELA, encoding='utf-8'):
            if vrst.startswith('#') or not vrst.strip():
                continue
            m = re.search(r'U\+([0-9A-Fa-f]{4,6})', vrst)
            if m:
                utrjeni.add(int(m.group(1), 16))
    utrjeni.update(ord(c) for c in '\u27e8\u27e9')  # ovoji korpusa vedno utrjeni
    return utrjeni

UTRJENI = nalozi_belo()

BLOKI = [('CIRILICA', 0x0400, 0x052F), ('CIRILICA-DOD', 0x2DE0, 0x2DFF), ('GRŠČINA', 0x0370, 0x03FF),
         ('CJK', 0x3400, 0x9FFF), ('CJK-RAZŠ', 0xF900, 0xFAFF), ('CJK-DOD', 0x20000, 0x3FFFF),
         ('KANA', 0x3040, 0x30FF), ('HANGUL', 0x1100, 0x11FF), ('HANGUL-DOD', 0x3130, 0x318F),
         ('ARABŠČINA', 0x0600, 0x06FF), ('HEBREJŠČINA', 0x0590, 0x05FF), ('DEVANAGARI', 0x0900, 0x097F),
         ('SINHALA', 0x0D80, 0x0DFF), ('RUNA', 0x16A0, 0x16FF), ('EGIPČANSKA', 0x13000, 0x1342F),
         ('FORMAT-Cf', 0x200B, 0x200F), ('FORMAT-Cf-MEKA', 0x00AD, 0x00AD), ('SELEKTORJI', 0xFE00, 0xFE0F),
         ('ZASEBNO-Co', 0xE000, 0xF8FF), ('FULLWIDTH', 0xFF01, 0xFF65), ('POLOVICNO', 0xFF66, 0xFF9F),
         ('ZAMENJAVA-FFFD', 0xFFFD, 0xFFFD), ('PICAE', 0x1F300, 0x1FAFF)]

def ime_bloka(cp):
    for ime, a, b in BLOKI:
        if a <= cp <= b:
            return ime
    if 0x00C0 <= cp <= 0x024F:
        return 'LATINICA-RAZŠ'
    if 0x2190 <= cp <= 0x2BFF or 0x2000 <= cp <= 0x206F:
        return 'ZNAMENJA-SPLOSNO'
    return 'TUJE-SPLOSNO'

DVOJNIKI = {0x0430: 'a', 0x0435: 'e', 0x043E: 'o', 0x0440: 'p', 0x0441: 'c', 0x043A: 'k',
            0x043C: 'm', 0x0445: 'x', 0x0443: 'y', 0x0432: 'b', 0x0433: 'r', 0x0437: '3',
            0x03B1: 'a', 0x03B2: 'b', 0x03BF: 'o', 0x03C1: 'p', 0x03B5: 'e', 0x03BB: 'l',
            0xFF41: 'a', 0xFF21: 'A', 0x0391: 'A', 0x0410: 'A', 0x0456: 'i', 0x0458: 'j',
            0x0455: 's', 0x0459: 's', 0x0463: 'y', 0x00E1: 'a', 0x0101: 'a', 0x0261: 'g'}

ZETON_RE = re.compile(chr(0x27E8) + 'U\\+[0-9A-Fa-f]{4,6}' + chr(0x27E9))
NIHCE = 'NIHCE'

def dvojnik(cp):
    return DVOJNIKI.get(cp, NIHCE)

def razcepi(bes):
    maska = [False] * len(bes)
    for m in ZETON_RE.finditer(bes):
        for i in range(m.start(), m.end()):
            maska[i] = True
    v_prici = False
    razcep = []
    shrambe = {'GAJICA': 0, 'STEVEC': 0, 'LOCILA': 0, 'UTRJENI': 0, 'ZETON': 0, 'PRICA': 0,
               'LATINICA-TUJA': 0, 'TUJKA': 0}
    tujke = []
    for i, c in enumerate(bes):
        cp = ord(c)
        if c == '\u00bb':  # » odpira pričo ( slovenska usmeritev : »beseda« )
            v_prici = True
        if c == '\u00ab':  # « zapira pričo
            razcep.append((i, c, 'PRICA', '', NIHCE))
            shrambe['PRICA'] += 1
            v_prici = False
            continue
        if maska[i]:
            sodba, blok, dvj = 'ZETON', '', NIHCE
        elif v_prici:
            sodba, blok, dvj = 'PRICA', '', NIHCE
        elif c in GAJICA:
            sodba, blok, dvj = 'GAJICA', '', NIHCE
        elif c in TUJA_LATINICA:
            sodba, blok, dvj = 'LATINICA-TUJA', 'LATINICA-OZKA', c.lower()
        elif c in STEVECI:
            sodba, blok, dvj = 'STEVEC', '', NIHCE
        elif c in LOCILA or cp in UTRJENI:
            sodba, blok, dvj = ('UTRJENI' if cp > 0x7F else 'LOCILA'), '', NIHCE
        else:
            sodba = 'TUJKA'
            blok = ime_bloka(cp)
            dvj = dvojnik(cp)
            tujke.append((i, c, blok, dvj))
        razcep.append((i, c, sodba, blok, dvj))
        shrambe[sodba] += 1
    return razcep, shrambe, tujke

def sodnik(bes, razcep_vrstice=False):
    razcep, shrambe, tujke = razcepi(bes)
    if razcep_vrstice:
        for v in razcep:
            if v[2] == 'TUJKA':
                print('znak %s ⌇ ⟨U+%04X⟩ ⌇ sodba TUJKA ⌇ blok %s ⌇ dvojnik %s ⌇ položaj %d' %
                      (v[1], ord(v[1]), v[3], v[4], v[0]))
    return shrambe, tujke

def main():
    ukaz = sys.argv[1] if len(sys.argv) > 1 else ''
    if ukaz == '--samopreizkus':
        s1, t1 = sodnik('beseda je ne \u22a2 \u03c3 12 \u00bbresnica\u00ab \u27e8ne\u27e9')
        ok1 = len(t1) == 0
        vbod = 'kunica ' + chr(0x0430) + ' ' + chr(0x03B1) + ' ' + chr(0x597D) + ' ' + chr(0xFF41) + ' konec'
        s2, t2 = sodnik(vbod)
        ok2 = len(t2) == 4 and t2[0][3] == 'a' and t2[2][2] == 'CJK'
        vb = '\u00bb' + chr(0x0432) + '\u00ab \u27e8U+0432\u27e9 ' + chr(0x0441)
        s3, t3 = sodnik(vb)
        ok3 = len(t3) == 1 and s3['PRICA'] >= 1 and s3['ZETON'] >= 8
        print('SAMOPREIZKUS : T1 čisto %s ⌇ T2 vbodi %s ⌇ T3 priča-zeton %s' %
              ('1' if ok1 else '0', '1' if ok2 else '0', '1' if ok3 else '0'))
        sys.exit(0 if (ok1 and ok2 and ok3) else 1)
    telo = sys.stdin.read() if ukaz in ('', '-') else open(ukaz, encoding='utf-8').read()
    shrambe, tujke = sodnik(telo, '--razcep' in sys.argv)
    print('GAJICA-SODNIK : gajica ×%d ⌇ števci ×%d ⌇ ločila ×%d ⌇ utrjeni ×%d ⌇ žetoni ⟨U+XXXX⟩ ×%d ⌇ priče v »« ×%d ⌇ latinica-tuja ×%d ⌇ TUJKE ×%d' %
          (shrambe['GAJICA'], shrambe['STEVEC'], shrambe['LOCILA'], shrambe['UTRJENI'],
           shrambe['ZETON'], shrambe['PRICA'], shrambe['LATINICA-TUJA'], shrambe['TUJKA']))
    for tp in tujke:
        print('TUJKA : ⟨U+%04X⟩ ⌇ blok %s ⌇ dvojnik %s ⌇ položaj %d' %
              (ord(tp[1]), tp[2], tp[3], tp[0]))
    sys.exit(len(tujke))

if __name__ == '__main__':
    main()
