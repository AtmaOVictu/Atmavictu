#!/usr/bin/env bash
# ⟨GAJICA-LINT⟩ : sodba sporočil komitov vsakega prihodnjega potiska
# ( rojen v dihu σ 6399, 22. 11. 2026 ⊙ ⟡ UKZ »⟨GAJICA-LINT⟩ nad sporočili vsakega prihodnjega potiska, stori« )
# TEHNIKA : stroj meri PISAVO sporočila, ⟨ne⟩ pomen : vsaka kodna točka sporočila komita mora živeti
# v kanonu ( gajica ASCII + č š ž Č Š Ž + števke + gajična ločila + utrjeni rod ) ; gostje zunaj kanona
# ( ⟨U+2014⟩, ⟨U+2013⟩, cirilica, CJK, IPA, emoji, puščice zunaj roda, ⟨U+FFFD⟩, nevidni znaki ) se
# imenujejo poimensko ∧ vrata padejo glasno ( ::error ∧ exit 1 ) ⊙ ⟨GLASNA-RESNICA⟩ ∧ ⟨MERILEC-SE-MERI⟩ §52.
# ⟨IZJEM⟩ : ⟨merge⟩ komiti stroja GitHub molčijo ( roka platforme, ⟨ne⟩ roka korpusa ) ; žetoni
# ⟨U+XXXX⟩ smejo gost poimenovati kjerkoli ( poimenovanje ⟨ne⟩ je gost ) ⊙ ⟨SODBA-IZJEM⟩ priče VERBATIM v »«.
# ⟨MERILEC-SE-MERI⟩ : --sodba-sebe sodi lastna kanarčka ( čist ⟨ne⟩ pada · ranjen MORA pasti ⊙ I-4 ).

set -uo pipefail

GL_MODE="usage"
GL_ARG=""

while [ $# -gt 0 ]; do
  case "$1" in
    --obseg) GL_MODE="obseg"; GL_ARG="${2:-}"; shift 2 ;;
    --besedilo) GL_MODE="besedilo"; GL_ARG="${2:-}"; shift 2 ;;
    --sodba-sebe) GL_MODE="sebe"; shift ;;
    -h|--pomoc)
      echo "uporaba : gajica-lint.sh --obseg PREDNIK..GLAVA | --besedilo DATOTEKA | --sodba-sebe"
      exit 2 ;;
    *)
      echo "⟩gajica-lint⟨ : neznan prag »$1«" >&2
      exit 2 ;;
  esac
done

export GL_MODE GL_ARG

python3 - <<'PY'
import os, re, subprocess, sys

# KANON ⟨EN-RAZLIČICA⟩ : dovoljene kodne točke sporočila potiska.
# gajica = ASCII tiskarski znaki + šumniki ; rod = utrjen znakovni rod korpusa ; + grški par ∅/∆ ( σ ψ ).
DOVOLJENI = set([0x09, 0x0A, 0x0D])
DOVOLJENI |= set(range(0x20, 0x7F))                                   # gajica ASCII ( števke · ločila · črke )
DOVOLJENI |= {0x10D, 0x10C, 0x161, 0x160, 0x17E, 0x17D}               # č Č š Š ž Ž
DOVOLJENI |= {0xA7, 0xA9, 0xAB, 0xB0, 0xB2, 0xB3, 0xB7, 0xBB, 0xD7}   # § © « ° ² ³ · » ×
DOVOLJENI |= {0x2074}                                                 # ⁴
DOVOLJENI |= {0x394, 0x2206, 0x3C3, 0x3C8}                             # Δ σ ψ ( ∆ ⟨U+2206⟩ tipkarski dvojnik ⊙ tipokupec )
DOVOLJENI |= {
    0x27E1,  # ⟡
    0x2299,  # ⊙
    0x2295,  # ⊕
    0x22A2,  # ⊢
    0x22A5,  # ⊥
    0x2307,  # ⌇
    0x2300,  # ⌀
    0x2227,  # ∧
    0x2228,  # ∨
    0x2205,  # ∅
    0x221E,  # ∞
    0x2260,  # ≠
    0x2264,  # ≤
    0x2265,  # ≥
    0x2202,  # ∂
    0x27E8,  # ⟨
    0x27E9,  # ⟩
    0x21D2,  # ⇒
    0x2192,  # →
    0x21CC,  # ⇌
    0x27C2,  # ⟂
    0x2B62,  # ⭢
    0x21AF,  # ↯
    0x26A0,  # ⚠
    0x2694,  # ⚔
    0x27F2,  # ⟲
    0x2026,  # …
    0x2248,  # ≈
}

ZNANI = {
    0xFFFD: 'nadomestni znak',
    0x200B: 'nevidni prostor',
    0x200C: 'nevidni sponec',
    0x200D: 'nevidna spojnica',
    0x200E: 'bidi levo',
    0x200F: 'bidi desno',
    0x202A: 'bidi oklepaj',
    0x202E: 'bidi zamenjava',
    0x2013: 'kratka črtica',
    0x2014: 'dolga črtica',
    0x2019: 'kodlek desni',
    0x201C: 'narekovaj odprti',
    0x201D: 'narekovaj zaprti',
}

# žeton : ⟨U+XXXX⟩ namesto surovega gosta ( X = nadomestek šestnajstiške števke v priči )
ZETON = re.compile('⟨U\\+[0-9A-Fa-fXx]{4,6}⟩')

def ime_cp(cp):
    return '⟨U+{:04X}⟩'.format(cp)

def sodba(besedilo):
    """sodi eno sporočilo : vrne seznam ran ( nizov ) ⊙ stroj meri pisavo, ⟨ne⟩ pomen"""
    rane = []
    telo = ZETON.sub('', besedilo)
    gostje = {}
    for znak in telo:
        cp = ord(znak)
        if cp not in DOVOLJENI:
            gostje[cp] = gostje.get(cp, 0) + 1
    for cp, stev in sorted(gostje.items()):
        ime = ime_cp(cp)
        if cp in ZNANI:
            rane.append('{} ×{} ( {} )'.format(ime, stev, ZNANI[cp]))
        else:
            rane.append('{} ×{}'.format(ime, stev))
    if 'measured' in besedilo.lower():
        rane.append('kolofon »measured« ne sme vstopiti v sporočilo potiska ( © živi v licenci )')
    return rane

def sodi_obseg(obseg):
    """bere komite obsega ⟨ne⟩-merge ∧ sodi vsako sporočilo"""
    try:
        shas = subprocess.run(
            ['git', 'rev-list', '--no-merges', obseg],
            capture_output=True, text=True, check=True).stdout.split()
    except subprocess.CalledProcessError as e:
        print('::error::gajica-lint : obseg »{}« se ne da prebrati ( {} )'.format(obseg, (e.stderr or '').strip()[:200]))
        return 2
    MEJA = 500
    if len(shas) > MEJA:
        print('⟨gajica-lint : obseg nosi {} komitov, sodim prvih {} ⊙ meja glasna⟩'.format(len(shas), MEJA))
        shas = shas[:MEJA]
    skupaj = 0
    padlih = 0
    for sha in shas:
        msg = subprocess.run(
            ['git', 'log', '-1', '--format=%B', sha],
            capture_output=True, text=True, check=True).stdout
        skupaj += 1
        if not msg.strip():
            print('::error::gajica-lint komit {} : sporočilo je prazno'.format(sha[:8]))
            padlih += 1
            continue
        rane = sodba(msg)
        if rane:
            padlih += 1
            print('::error::gajica-lint komit {} : {}'.format(sha[:8], ' ⌇ '.join(rane)))
    print('⟨kanarček : sodena sporočila {} · padla {}⟩'.format(skupaj, padlih))
    if padlih > 0:
        print('::error::gajica-lint : {} sporočil z gosti zunaj kanona · vrata padajo glasno ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354'.format(padlih))
        return 1
    print('⟨vidim : nič⟩ · gajica-lint molči zeleno')
    return 0

def sodi_besedilo(pot):
    try:
        with open(pot, encoding='utf-8') as f:
            msg = f.read()
    except OSError as e:
        print('::error::gajica-lint : berba »{}« padla ( {} )'.format(pot, e))
        return 2
    if not msg.strip():
        print('⟨vidim : prazno besedilo · nič⟩')
        return 0
    rane = sodba(msg)
    if rane:
        print('::error::gajica-lint besedilo {} : {}'.format(pot, ' ⌇ '.join(rane)))
        return 1
    print('⟨vidim : nič⟩ · besedilo čisto gajično')
    return 0

def sodi_sebe():
    """⟨SODBA-SEBE⟩ : čist kanarek ⟨ne⟩ pada ( lažni alarm = kip ) · ranjen MORA pasti ⊙ I-4"""
    cisti = ('pečat σ 6399 ⊙ prevoz teles diha ⟨SAMO-IZVEDBA-DOKAZ⟩ 2306 ⌇ kura ⟨U+2014⟩ ×1 ⊢ '
             '»⟨U+03A3⟩« priča VERBATIM ⊙ ⟨SODBA-IZJEM⟩ · © 0.2026 × 10⁴ ∧ ≤ ≥ ∅ ∆ ⌀ ∞ ⊕ ∨ ↯')
    ranjen = ('kura ' + chr(0x2014) + ' surova črtica ' + chr(0x6C49) + ' ' + chr(0x0430) + ' '
              + chr(0x1F600) + ' ' + chr(0xFFFD) + ': measured, not asserted')
    rane_c = sodba(cisti)
    rane_r = sodba(ranjen)
    pričakovani = {0x2014, 0x6C49, 0x0430, 0x1F600, 0xFFFD}
    ulov = {r.split(' ')[0] for r in rane_r}
    pričakovana_imena = {'⟨U+{:04X}⟩'.format(cp) for cp in pričakovani}
    if rane_c:
        print('::error::⟨SODBA-SEBE⟩ : čist kanarek pada ( lažni alarm ) : ' + ' ⌇ '.join(rane_c))
        return 1
    if not pričakovana_imena.issubset(ulov):
        print('::error::⟨SODBA-SEBE⟩ : ranjen kanarek se izmika ( ulov {} ⊥ pričakovano {} )'.format(
            sorted(ulov), sorted(pričakovana_imena)))
        return 1
    if 'measured' not in ' '.join(rane_r):
        print('::error::⟨SODBA-SEBE⟩ : kolofon »measured« neulovljen')
        return 1
    print('⟨kanarček SODBE-SEBE : čist ×0 ( molči ) · ranjen ×{} ( pada ) ⊙ preizkus pada na telo⟩'.format(len(rane_r)))
    return 0

m = os.environ.get('GL_MODE', 'usage')
if m == 'obseg':
    obseg = os.environ.get('GL_ARG', '')
    if not obseg:
        print('::error::gajica-lint : --obseg brez obsega')
        sys.exit(2)
    sys.exit(sodi_obseg(obseg))
elif m == 'besedilo':
    pot = os.environ.get('GL_ARG', '')
    if not pot:
        print('::error::gajica-lint : --besedilo brez poti')
        sys.exit(2)
    sys.exit(sodi_besedilo(pot))
elif m == 'sebe':
    sys.exit(sodi_sebe())
else:
    print('uporaba : gajica-lint.sh --obseg PREDNIK..GLAVA | --besedilo DATOTEKA | --sodba-sebe')
    sys.exit(2)
PY
