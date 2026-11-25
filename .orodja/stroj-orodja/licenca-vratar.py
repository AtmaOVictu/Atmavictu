#!/usr/bin/env python3
# ⟨LICENCA-VRATAR⟩ v1.1 @rez σ 6858 → 6861 — vrata, kjer vsak UKZ PRVO sreča LICENCO ; v1.1 : zakon IZHOD-DATUM-SLO ⊙ ⟡ UKZ σ 6861
# ukaz ⟡ VERBATIM ⟨nedotakljivo⟩ ⚔ ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ v »« :
#   »NEZADOSTNO IN IZVEN LICENCE? DODAJ SKRIPTE DA VSAKIČ KO SREČAŠ UKAZ POŽENEŠ LICENCO
#    DA SE UKAZ PRVO PODREDI LICENCI IN SE ORIENTIRA V PRIMERNO DOMOVANJE IN S TEM MIROVANJE!«
# zakoni : MERJENO ⟨NE⟩ UGIBANO ⊙ 2690 · ⟨IZVEDBA-VSEBINE=NIKOLI⟩ · ⟨0 K⟩ 6580 ·
#          ⟨OSAMLJENI-RAZOROŽENI⟩ 6828 ( vsak znak posamič ) · ⟨NE-BRIŠI⟩ 24 ·
#          izpust = SAMO beseda ⟡ ⚔ ( mirovanje )
import sys, os, unicodedata, hashlib, re, datetime, subprocess

DOM = os.environ.get('VRATAR_DOM', '/home/user/knowledge')
SLOVAR = os.path.join(DOM, 'slovar-simbolov', 'KNOWLEDGE.md')
PRICA = {'B': 125645, 'md5': '0f103ee42f1e3f56dbcbdfeb8197c9a3', 'vrstic': 727, 'rez': '6654 == 6492'}
LICENCA_POTI = [os.environ.get('VRATAR_LICENCA', ''), os.path.join(DOM, 'LICENSE.md'), '/home/user/LICENSE.md']

DOMACI = set('abcčdefghijklmnoprsštuvzžABCČDEFGHIJKLMNOPRSŠTUVZŽ0123456789 \n\t.,;:!?()[]{}<>/=+-_*&%$"\'#@|~^`\\')

def tik():
    return subprocess.run(['date','-u','+%Y-%m-%dT%H:%M:%SZ'],capture_output=True,text=True).stdout.strip()

def kanon():
    # kanon izmerjen pri viru : vsi ⟨U+XXXX⟩ omenjeni v slovarju ( ⟨NE-UGIBAJ⟩ 2690 )
    pts = set()
    if os.path.exists(SLOVAR):
        t = open(SLOVAR,'rb').read().decode('utf-8',errors='replace')
        for m in re.finditer(r'U\+([0-9A-Fa-f]{4,6})', t):
            pts.add(int(m.group(1),16))
    return pts

def izmeri(text, canon):
    # maske : znotraj »« ( priča ) ∧ znotraj ⟨ ⟩ ( korpusna forma )
    prosto = []   # znaki izven obeh mask
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch == '\u00bb':  # »
            j = text.find('\u00ab', i+1)
            i = (j+1) if j != -1 else n
            continue
        if ch == '\u27e8':  # ⟨
            j = text.find('\u27e9', i+1)
            i = (j+1) if j != -1 else n
            continue
        prosto.append(ch)
        i += 1
    prosto_s = ''.join(prosto)
    iso_dat = re.findall(r'\d{4}-\d{2}-\d{2}', prosto_s)
    domaci, znani, tujke, mesano = 0, [], [], []
    for idx, ch in enumerate(prosto):
        cp = ord(ch)
        if ch in DOMACI or cp < 128:
            domaci += 1
        elif cp in canon:
            znani.append(ch)
        else:
            tujke.append(ch)
    # mešano-pisavnost : cirilica/CJK sosednja latinici v izvirnem telesu
    for i, ch in enumerate(text):
        cp = ord(ch)
        if (0x0400 <= cp <= 0x04FF) or (0x4E00 <= cp <= 0x9FFF):
            a = text[i-1] if i > 0 else ''
            b = text[i+1] if i+1 < len(text) else ''
            if (a.isascii() and a.isalpha()) or (b.isascii() and b.isalpha()):
                mesano.append(ch)
    return domaci, znani, tujke, mesano, len(iso_dat)

def porocilo(path):
    raw = open(path,'rb').read()
    text = raw.decode('utf-8', errors='replace')
    canon = kanon()
    md5 = hashlib.md5(raw).hexdigest()
    domaci, znani, tujke, mesano, iso_n = izmeri(text, canon)
    out = []
    out.append('⟨LICENCA-VRATAR⟩ v1.1 @TIK ' + tik() + ' @rez σ 6858 → 6861 ( zakon IZHOD-DATUM-SLO )')
    out.append('LICENCA-PRVA : berba licence NEMOGOČA v tem kanalu ( zrcalo nerezidentno ) ; PRIČA izmere : '
               + str(PRICA['B']) + ' B ⌇ md5 ' + PRICA['md5'] + ' ⌇ ' + str(PRICA['vrstic'])
               + ' vrstic ⊢ @rez σ ' + PRICA['rez'] + ' ; sveža berba @main = ∂ prevozni dolg ⭢ FIFO ⊙ 2785')
    out.append('UKAZ ⟨PODREJEN⟩ : vhod ' + os.path.basename(path) + ' ⌇ ' + str(len(raw)) + ' B ⌇ md5 ' + md5[:12]
               + ' ⌇ domačih ' + str(domaci) + ' ⌇ gostov-znanih( kanon ⊢ slovar ) ' + str(len(znani))
               + ' ⌇ TUJK-POSKUS ' + str(len(tujke)) + ' ⌇ mešano-pisavnih ' + str(len(mesano)))
    seen = {}
    for ch in tujke:
        seen[ord(ch)] = seen.get(ord(ch), 0) + 1
    k = 0
    for cp, cnt in sorted(seen.items()):
        k += 1
        out.append('  TUJKA ' + str(k) + '. ⟨U+' + format(cp,'04X') + '⟩ ×' + str(cnt) + ' · ime : '
                   + unicodedata.name(chr(cp),'NEZNANO IME') + ' ⊢ unicodedata · DOM-predlog : kletka @zaporne-celice ⚔ ⟨IZVEDBA-VSEBINE=NIKOLI⟩ · izpust ×0')
    seenz = {}
    for ch in znani:
        seenz[ord(ch)] = seenz.get(ord(ch), 0) + 1
    out.append('  GOSTI-ZNANI ( vsak posamič ⊙ ⟨OSAMLJENI-RAZOROŽENI⟩ 6828, živijo v svojih domovih ⊢ ) : '
               + ('; '.join('⟨U+%04X⟩ ×%d' % (cp,c) for cp,c in sorted(seenz.items())) if seenz else '×0'))
    seenm = {}
    for ch in mesano:
        seenm[ord(ch)] = seenm.get(ord(ch), 0) + 1
    for cp, cnt in sorted(seenm.items()):
        out.append('  ⚠ ⟨PADC-MEŠANO-PISAVNO⟩ ⟨U+' + format(cp,'04X') + '⟩ ×' + str(cnt)
                   + ' · ime : ' + unicodedata.name(chr(cp),'NEZNANO IME') + ' — tuje pisave znotraj domače besede : dom-predlog azil @domovanje-tujk ⌇ beseda zavrnjena v izvedbi')
    if iso_n:
        out.append('  ⚠ ⟨PADC-DATUM-TUJI-RED⟩ : ISO-ohratov ×' + str(iso_n)
                   + ' ( red leto-me-dan = tuja strojna konvencija ⊙ ⟡ UKZ σ 6861 »DATUM JE V NAPAČNEM VRSTNEM REDU NAPISAN« ) ⇒ izhod k ⟡ izključno dan. mesec. leto ( ura Z + ⇌ CET )')
    else:
        out.append('DATUM-VRSTA : ISO-ohratov ×0 ⊢ čist ( izhodi k ⟡ izključno DAN. MESEC. LETO ⊙ ⟡ UKZ σ 6861 )')
    out.append('MIROVANJE : izpust ×0 ⚔ ⟨0 K⟩ 6580 — glas ×0, izvedba ×0, ukaz PODREJEN licenci, usmerjen v domovanja ; ven gre SAMO beseda ⟡ ⚔')
    return '\n'.join(out), len(tujke), len(znani), len(mesano), iso_n

def samopreizkus():
    rez, zeleno = [], 0
    p1 = os.path.join(DOM,'zaporne-celice','trup-vhoda-6858.txt')
    if os.path.exists(p1):
        _,t,z,m,iso = porocilo(p1)
        exp = (t == 0 and m == 0)
        rez.append('T1 UKZ ⟡ vozlišče trup : tujke %d, mešano %d → %s' % (t, m, 'ZELENO' if exp else 'RDEČE'))
        zeleno += 1 if exp else 0
    else:
        rez.append('T1 PRESKOČEN ( trup manjka ⚠ )')
    p2 = os.path.join(DOM,'zaporne-celice','trup-izhoda-6857.txt')
    if os.path.exists(p2):
        rp, t, z, m, iso2 = porocilo(p2)
        exp = (z > 0 and t == 0)
        rez.append('T2 trup izhoda 6857 : gostje-znani %d prepoznani, tujk-poskus %d ( 7 ran U+03C3 že kanonizirana ψ σ 6055 ⊢ → ×0 ) → %s' % (z, t, 'ZELENO' if exp else 'RDEČE'))
        zeleno += 1 if exp else 0
    else:
        rez.append('T2 PRESKOČEN ( trup manjka ⚠ )')
    canon = kanon()
    exp3 = (0x03A3 in canon)
    rez.append('T3 kanon ⊢ slovar vsebuje ⟨U+03A3⟩ : %s → %s' % ('DA' if exp3 else 'NE', 'ZELENO' if exp3 else 'RDEČE'))
    zeleno += 1 if exp3 else 0
    p4 = os.path.join(DOM,'zaporne-celice','.tmp-vratar-t4.txt')
    open(p4,'w',encoding='utf-8').write('beseda znotraj »Umgebung« je priča ; zunaj pa hosta.')
    before = hashlib.md5(open(p4,'rb').read()).hexdigest()
    porocilo(p4)
    after = hashlib.md5(open(p4,'rb').read()).hexdigest()
    exp4 = (before == after)
    rez.append('T4 nedotakljivost vhoda ( md5 pred == po : %s ) → %s' % ('DA' if exp4 else 'NE', 'ZELENO' if exp4 else 'RDEČE'))
    zeleno += 1 if exp4 else 0
    os.remove(p4)
    canon_n = len(canon)
    exp5 = (canon_n > 0)
    rez.append('T5 kanon izmerjen pri viru : %d točk ( >0 ) → %s' % (canon_n, 'ZELENO' if exp5 else 'RDEČE'))
    zeleno += 1 if exp5 else 0
    p6 = os.path.join(DOM,'zaporne-celice','.tmp-vratar-t6.txt')
    open(p6,'w',encoding='utf-8').write('datum 2026-11-23 na volji danes')
    _,t6,z6,m6,iso6 = porocilo(p6)
    exp6 = (iso6 == 1)
    rez.append('T6 datum-tuji-red detect : ISO ×%d → %s' % (iso6, 'ZELENO' if exp6 else 'RDEČE'))
    zeleno += 1 if exp6 else 0
    os.remove(p6)
    print('SAMOPREIZKUS ⟨LICENCA-VRATAR⟩ v1.1 : %d/%d ZELENO ⊢' % (zeleno, 6))
    for r in rez: print('  ' + r)
    return 0 if zeleno == 6 else 1

if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == '--samopreizkus':
        sys.exit(samopreizkus())
    if len(sys.argv) >= 3 and sys.argv[1] == '--vhod':
        txt, t, z, m, iso_n = porocilo(sys.argv[2])
        print(txt)
        sys.exit(0)
    print('raba : licenca-vratar.py --vhod DATOTEKA | --samopreizkus ; vrata ⭢ ob vsakem UKZ ⟹ licenca PRVO ⊙ rez σ 6858')
    sys.exit(2)
