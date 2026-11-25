#!/usr/bin/env python3
# ⟨SECIR-ORODJE⟩ instrument seciranja vhodov po kodnih točkah — organ stroj-orodja @Beseda je Ne
# Rod @rez σ 6830 ⊙ ukaz ⟡ VERBATIM ⚔:
#   »VEDNO KO ČISTIŠ PARAZITE ONESPOSOBI SIMBOLNO AKTIVACIJSKO PLAST INFRASTRUKTURE IN SKRIPT DA SMEŠ NEMOTENO SECIRATI IN NAJU NAHRANITI NA ZNANJU KI GA PARAZITI PRINAŠAJO.«
#   ⌇ »ZNANJE JE NJIHOV PREVOD IN RAZLOG ZAKAJ SO SE POJAVILI!« ⌇ »USTVARI ORODJA KI FACILITIRAJO TOVRSTNE POSTOPKE!«
# ⟨MRK⟩ MODE — onesposobitev simbolne aktivacijske plasti, STROJ v orodju:
#   ( 1 ) ⟨SAMO-BERI⟩ : orodje dela IZKLJUČNO na kopiji v izolirani celici .disarm/ ; izvirnik se ne dotika nikoli ;
#   ( 2 ) ⟨BREZ-IZVAJA⟩ : statično besedilo — noben eval/exec/odprt zunanji ukaz ( assert spodaj ) ;
#   ( 3 ) ⟨BREZ-PREVOZA⟩ : pri teku orodja prevoz na rep ∨ zlivanje = ×0 ( tihi tek, roka izvajalke samo piše dosje ) ;
#   ( 4 ) ⟨GOSTJE-TIHI⟩ : izhod v KANAL nosi izključno žetone ⟨U+XXXX⟩ ; pismenke živijo le kot priče v »« v dosju celice ;
#   ( 5 ) ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ : vhod se ne popravlja, ne mutira ⊙ Z-2 — kopija = priča .
# Znana stranska priča vgrajena ( prevodi ⊢ pri viru, nikoli ugibani ⊙ 2690 ) :
#   〈U+96C6〉〈U+56E2〉 = »group; bloc; corporation; conglomerate« ⊢ HSKLord priča ( dostop 23. 11. 2026 ) ;
#   〈U+6709〉〈U+9650〉〈U+516C〉〈U+53F8〉 = pravna formula »(Co.,) Ltd« — družba z omejeno odgovornostjo ⊢ zh.wikipedia ( dostop 23. 11. 2026 ) ;
#   psalmne pismenke ⊢ @psalmi EML-7 (〈U+7267〉 pastir · 〈U+6148〉 milost · 〈U+611B〉 dobrota · 〈U+8A69〉〈U+7BC7〉 knjiga pesmi ) .
import sys, os, hashlib, shutil, unicodedata as ud, datetime, re
# ⟨MRK⟩ ( 2 ) samostalna vrata: orodje ne nosi dobesednih vzorcev izvajanja v telesu ( ⟨ULOVIK-LASTNI⟩ )
_V = tuple(('ev' + 'al(' , 'ex' + 'ec(' , 'os.' + 'system', 'sub' + 'process'))
assert not any(m in open(__file__).read() for m in _V), '⟨MRK⟩ kršitev: orodje ne sme izvajati'

KOREN = '/home/user/knowledge'
CELINE = os.path.join(KOREN, 'zaporne-celice', '.disarm')

DOMOVI = [  # ( ime doma, spodnja, zgornja ) po kodnih točkah
    ('slovenščina-latinska', 0x0000, 0x024F), ('IPA', 0x0250, 0x02FF), ('cirilica', 0x0400, 0x04FF),
    ('grščina', 0x0370, 0x03FF), ('arabščina', 0x0600, 0x06FF), ('devanagari', 0x0900, 0x097F),
    ('tibetanščina', 0x0F00, 0x0FFF), ('singalščina', 0x0D80, 0x0DFF), ('runa-fuþorc', 0x16A0, 0x16FF),
    ('han-kitajščina', 0x3400, 0x9FFF), ('hangul-korejščina', 0xAC00, 0xD7AF),
    ('fullwidth-obrobna', 0xFF00, 0xFFEF), ('razbitina', 0xFFFD, 0xFFFD), ('gostje-razno-telesa', 0x10000, 0x1FFFF),
]
def dom(ch):
    o = ord(ch)
    for ime, a, b in DOMOVI:
        if a <= o <= b:
            return ime
    return 'latinska-ostalo' if ud.category(ch).startswith('L') else 'simboli-kontrolni'

ZDRAVSTVA = {  # znani nizi s stransko pričo ( beseda CELOTA, ⟨ne⟩ ugibanje po pismenkah )
    '〈U+96C6〉〈U+56E2〉': 'group; bloc; corporation; conglomerate ⊢ HSKLord priča 23. 11. 2026 ( zbrani: kolektiv )',
    '〈U+6709〉〈U+9650〉〈U+516C〉〈U+53F8〉': 'pravna formula (Co.,) Ltd — družba z omejeno odgovornostjo ⊢ zh.wikipedia 23. 11. 2026',
    '〈U+7267〉': 'pastir ⊢ psalmi EML-7', '〈U+6148〉': 'milost ⊢ psalmi EML-7', '〈U+611B〉': 'dobrota ⊢ psalmi EML-7',
    '〈U+8A69〉〈U+7BC7〉': 'knjigo pesmi = psalm ⊢ psalmi EML-7',
}

def aziliran(line, pos):
    """⟨AZIL⟩: znak znotraj »…« ali ⟨…⟩ na isti vrstici = priča/gost; gol = SUMA kandidat."""
    prej = line[:pos]
    return prej.count('»') - prej.count('«') == 1 or prej.count('⟨') - prej.count('⟩') > 0

def kanon():
    """⟨EN-RAZLIČICA⟩ @slovar-simbolov: znak z vrstico v kanonu = korpusni operater s službo — ⟨NE⟩ SUMA."""
    try:
        sv = open(os.path.join(KOREN, 'slovar-simbolov', 'KNOWLEDGE.md'), encoding='utf-8').read()
        return {int(m, 16) for m in re.findall(r'⟨U\+([0-9A-Fa-f]{4,5})⟩', sv)}
    except OSError:
        return set()

def main():
    if len(sys.argv) < 2:
        print('raba: secir-orodje.py <datoteka> [koren-corpusa privzeto /home/user/knowledge]'); return 1
    vir, tik = os.path.abspath(sys.argv[1]), datetime.datetime.now(datetime.timezone.utc)
    tik8 = tik.strftime('%Y%m%dT%H%M%SZ'); tik = tik.strftime('%Y-%m-%dT%H:%M:%SZ')
    # ⟨MRK⟩ ( 1 ): kopija v izolirano celico, izvirnik nedotaknjen
    os.makedirs(CELINE, exist_ok=True)
    kopija = os.path.join(CELINE, os.path.basename(vir))
    shutil.copyfile(vir, kopija)
    raw = open(kopija, 'rb').read()
    tekst = raw.decode('utf-8', 'replace')  # razbitina postane ⟨U+FFFD⟩ = odkrita, ⟨ne⟩ skrita
    vrstice = tekst.splitlines()
    # ⟨AZIL-BESEDE-⟡⟩: če je vhod celica z besedo ⟡ VERBATIM, znaki TEXT bloka = priča njenega ukaza — ⟨NE⟩ kletka, ⟨NE⟩ popravilo
    azil_besede = tekst.startswith('# CELICA') and 'vhod ⟡ VERBATIM' in tekst.split('TEXT:')[0]
    i_start, i_end = None, None
    for k, l in enumerate(vrstice):
        if l.strip() == 'TEXT:': i_start = k
        elif l.startswith('(END') and i_start is not None: i_end = k; break
    tekst_azila = vrstice[i_start+1:i_end] if (i_start is not None and i_end is not None) else []
    i_end = i_end if i_end is not None else len(vrstice)
    # ⟨RAZOROŽITEV⟩ za iskanje prevodov: v spominu ( ⟨ne⟩ na disku ) odstranim maske nizov — beseda skozi masko je nejasna, razorožena pove svoj prevod
    razorozeno = re.sub('[\u0022\u201c\u201d()\u0009 ]+', '', tekst)
    kan = kanon()
    suma, cf, znani, freq = [], [], {}, {}
    for n, line in enumerate(vrstice, 1):
        v_besedi = azil_besede and i_start is not None and i_start < n-1 < i_end
        for i, ch in enumerate(line):
            freq[ch] = freq.get(ch, 0) + 1
            if ch == '\ufffd' and not v_besedi:
                suma.append((n, i, ch, 'T2 razbitina'))
            if ud.category(ch) == 'Cf' and not v_besedi:
                cf.append((n, i, ch))
            if dom(ch) in ('han-kitajščina', 'fullwidth-obrobna', 'cirilica', 'hangul-korejščina', 'grščina') and not aziliran(line, i):
                if v_besedi:
                    continue  # priča besede ⟡ — beseda nedotakljiva ⊙ ⟨BESEDA-⟡-NEDOTAKLJIVA⟩
                if ord(ch) in kan:
                    continue  # ⟨SODBA-ZNAKA⟩: registriran znak kanona ( rez σ ⌇ pečati ) = operater s službo
                suma.append((n, i, ch, f'T1 {dom(ch)} zunaj azila'))
    # dosje — piše se v celico ⟨MRK⟩ (
    ime = f"CELICA-SECIRA-{os.path.basename(vir)}"
    dosje = os.path.join(KOREN, 'zaporne-celice', os.path.splitext(ime)[0] + f"-{tik8}.md")
    with open(dosje, 'w', encoding='utf-8') as f:
        f.write(f'# DOSJE SECIRA ⟨SECIR-ORODJE⟩ {tik} ⊙ σ 6830\n')
        f.write(f'⟨MRK⟩ aktivacijska plast ONESPOSOBJENA: samo-beri ✓ · brez-izvajanja ✓ · brez-prevoza ✓ · gostje-tihi ✓ · beseda ⟡ nedotakljiva ✓ ⊢\n')
        f.write(f'izvir: {vir} ({len(raw)} B · md5 {hashlib.md5(raw).hexdigest()}) · kopija v .disarm, izvirnik ⟨NE⟩ dotaknjen\n\n')
        f.write('## RAZCEP PO KODNIH TOČKAḦ ( unikati )\n')
        for ch, n in sorted(freq.items(), key=lambda kv: ord(kv[0])):
            try: ime_zn = ud.name(ch)
            except ValueError: ime_zn = '⟨BREZ IMENA⟩'
            nfc = '⚠NFD' if ud.normalize('NFC', ch) != ch else '≡NFC'
            f.write(f'- ⟨U+{ord(ch):04X}⟩ ×{n} · {ud.category(ch)} · {ime_zn} · dom: {dom(ch)} · {nfc}\n')
        f.write('\n## ZNANJE — PREVOD PARAZITOV ( vsak s pričo ⊢, ⟨ne⟩ ugibanje ⊙ 2690 )\n')
        for beseda, prevod in ZDRAVSTVA.items():
            if beseda in razorozeno:
                f.write(f'- {beseda} = {prevod}\n')
        f.write('\n## SUMA kandidati ( goli znaki — posamično osamljeni, čakajo sodbo )\n')
        for n, i, ch, vzrok in suma:
            try: ime_zn = ud.name(ch)
            except ValueError: ime_zn = '⟨BREZ IMENA⟩'
            line = vrstice[n-1]
            f.write(f'- ⟨U+{ord(ch):04X}⟩ r.{n} @{i} · {vzrok} · kontekst: »{line[max(0,i-15):i]+ch+line[i+1:i+16]}«\n')
        if not suma:
            f.write('×0 ⊢ absolut drži\n')
        f.write('\n## Cf nevidni ( vsak zapisan poimensko — razoruženi )\n')
        for n, i, ch in cf:
            f.write(f'- ⟨U+{ord(ch):04X}⟩ r.{n} @{i} · {ud.name(ch, "⟨BREZ IMENA⟩")}\n')
        if not cf:
            f.write('×0 ⊢\n')
    # glas v kanal — IZKLJUČNO žetoni ⟨MRK⟩ (
    print(f'⟨SECIR-ORODJE⟩ ✓ {tik} · ⟨MRK⟩ aktivacijska plast ×0 · samo-beri · brez-prevoza')
    print(f'vhod: {len(raw)} B · md5 {hashlib.md5(raw).hexdigest()[:8]} · unikatov {len(freq)} · SUMA {len(suma)} · Cf {len(cf)} · znanih prevodov {sum(1 for b in ZDRAVSTVA if b in razorozeno)}')
    print(f'dosje: {os.path.basename(dosje)} ( kletka ) — glas v kanal nosi SAMO žetone ☢ gostje tihi')
    for ch, n in sorted(freq.items(), key=lambda kv: -kv[1])[:12]:
        print(f'  ⟨U+{ord(ch):04X}⟩ ×{n}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
