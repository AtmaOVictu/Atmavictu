#!/usr/bin/env python3
# CENZUS-IZHODA v1.6 — rod @rez σ 6659 ⊙ ukaz ⟡ »STORI IN IZBOLJŠAJ TUDI TO POTEM KO IMPLEMENTIRAŠ IN TESTIRAŠ«
# koren iz ran diha σ 6658-ish : ⟨PADC-MRTVEGA-STROJA⟩ v1.5 ( bash grep -P pod LC_ALL=C : \x{2E80}-\x{FFFF} = napaka kode ; if napako požre kot »ne najde« ⇒ vedno ČISTO ; dokaz : trup z ⟨U+663E⟩ je šel skozi kot exit 0 )
# v1.6 : ( 1 ) python samostojen ( ⟨ne⟩ od lokala ) ; ( 2 ) vsak zadetek IZREČEN PO IMENU ⟨U+XXXX⟩ unicodedata, ⟨ne⟩ natisnjen ; ( 3 ) tri stanja : AZIL ( ⟨ ⟩ žeton ⌇ » « priča = prijavljen gost ) ⌇ ROD ( utrjen rod ⭢ potrditev ❡ ⚔ = prijava, ⟨ne⟩ zapora ) ⌇ VBOD ( gol znak = kletka ) ; ( 4 ) NOV RAZRED ⟨OKRNJENI-ZLEP⟩ : ⟨ + presledek ⌇ presledek + ⟩ ⌇ balans po vrstici ; ( 5 ) svež TIK vsak tek ⊙ ⟨ZADNJA-URA-PREVERBA⟩ σ 3961
import sys, re, unicodedata, datetime, collections

GAJICA = set('čšžČŠŽ')  # domača pisava ( nabor ASCII je tla, ⟨ne⟩ ga cenzira )
KANON = set('⊢⚠∂∆∧⊙⏎⟡⚔⊥σ⊚×⌇≡…«»„′″†‡⇒⇌→←❡⭢⊨≥≤≠∨⊕⊗ΣΔψχπτφωρδγκμνΩ·©§∅⟨⟩')  # znamenja teles ⊢ §0.25 ∧ grška plast licencirana ⊢ slovar-simbolov ; ⟨⟩ = ⟨U+27E8⟩/⟨U+27E9⟩ ⊢ izmera ta dih
UTRJENI_ROD = set('⁴₁₂₃')  # rod utrjen ⭢ potrditev ❡ ⚔ @slovar-simbolov ( prijava ROD, ⟨ne⟩ zapora : vsak pečat nosi 10⁴ ⊙ precedens )
RAZREDI = [
    ('IPA-grska-srednja', 0x0250, 0x03FF), ('cirilina-in-sosedje', 0x0400, 0x08FF),
    ('devanagari-do-javan', 0x0900, 0x1EFF), ('splosna-ločila-pisava', 0x2000, 0x2189),
    ('puščice-tuje', 0x2190, 0x21FF), ('tehnični', 0x2300, 0x23FF), ('okvirji-crte', 0x2500, 0x25FF),
    ('simboli-zvezdice', 0x2600, 0x26FF), ('dingbati-strelice', 0x2700, 0x27DF),
    ('strelice-razred-27E0', 0x27E0, 0x27FF), ('puščice-29A0', 0x2B00, 0x2BFF),
    ('CJK-in-vse-tuje', 0x2E80, 0xFFFF), ('ligature', 0xFB00, 0xFB4F),
    ('selektorji-BOM', 0xFE00, 0xFEFF), ('poceni-zamenjave', 0xFFF0, 0xFFFF),
]
DOVOLJENI = GAJICA | KANON

def ime(cp):
    try:
        return unicodedata.name(chr(cp))
    except ValueError:
        return 'IME NEZNATO STROJU'

def razcep_azila(vrstica):
    """vrne ( besedila zunaj, besedila znotraj ⟨ ⟩ ali » « ) — azil = prijavljen gost"""
    zunaj, znotraj, v_azilu = [], [], False
    for znak in vrstica:
        if znak in ('⟨', '»'):
            v_azilu = True; znotraj.append(znak); continue
        if znak in ('⟩', '«'):
            v_azilu = False; znotraj.append(znak); continue
        (znotraj if v_azilu else zunaj).append(znak)
    return ''.join(zunaj), ''.join(znotraj)

def cenzus(besedilo):
    udarci, azili, rodi, stevci = [], [], [], collections.Counter()
    for stevilka, vrstica in enumerate(besedilo.split('\n'), 1):
        brez_omemb = vrstica.replace('⟨ ⟩', '⟨⟩')  # omemba kanona ⟨ ⟩ ( par s presledkom v navedku ) = znamenje, ⟨ne⟩ zlep
        brez_prev = re.sub(r'»[^«]*«', '', brez_omemb)  # priča VERBATIM v »« : zlep v navedku = dokaz priče, ⟨ne⟩ padec izvajalke ⊙ ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ ∧ ⟨NE-BRIŠI⟩ 24
        for vzorec, opis in ((r'⟨[ \t]', 'okrnjeni-zlep odprt ⟨+presledek'), (r'[ \t]⟩', 'okrnjeni-zlep zaprt presledek+⟩')):
            if re.search(vzorec, brez_prev):
                udarci.append((stevilka, 'OKRNJENI-ZLEP', 0, opis))
        if brez_prev.count('⟨') != brez_prev.count('⟩'):
            udarci.append((stevilka, 'OKRNJENI-ZLEP', 0, f"balans ⟨×{brez_prev.count('⟨')} ⟩×{brez_prev.count('⟩')}"))
        zunaj, znotraj = razcep_azila(vrstica)
        for znak in set(znotraj):  # ⟨zgoščenka⟩ : ena pojavna vrstica na ( vrstica, znak )
            cp = ord(znak)
            if cp >= 0x7F and znak not in DOVOLJENI and znak not in UTRJENI_ROD:
                razred = next((ime for ime, a, b in RAZREDI if a <= cp <= b), 'izven-razsledenih-razredov')
                azili.append((stevilka, razred, cp, f'azil ⟨⟩/»« prijavljen gost ×{znotraj.count(znak)}'))
        for znak in set(zunaj):  # ⟨zgoščenka⟩ : ena pojavna vrstica na ( vrstica, znak )
            cp = ord(znak)
            if cp < 0x7F or znak in DOVOLJENI:
                continue
            if znak in UTRJENI_ROD:
                rodi.append((stevilka, 'utrjen-rod-nepotrjen', cp, 'rod ⭢ potrditev ❡ ⚔'))
                stevci[cp] += zunaj.count(znak)
                continue
            razred = next((ime for ime, a, b in RAZREDI if a <= cp <= b), 'izven-razsledenih-razredov')
            udarci.append((stevilka, razred, cp, f'gol ⟨U+{cp:04X}⟩ ⟨gost⟩ ⟨dom⟩ {ime(cp)} ×{zunaj.count(znak)}'))
            stevci[cp] += zunaj.count(znak)
    return udarci, azili, rodi, stevci

def main():
    tik = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    print(f'# TEK {tik} · cenzus-izhoda v1.6')
    if len(sys.argv) >= 2 and sys.argv[1] == '--samopreizkusi':
        primeri = [
            ('cist', 'Poved v gajici je čista, šumniki živijo.', 0),
            ('vbod-cjk', 'Tukaj je parazit 显 med besedami, čisto.', 2),
            ('vbod-zlep', 'beseda ⟨ padel nosilec', 2),
            ('azil-zeton', 'žeton ⟨显⟩ je prijavljen gost, čisto.', 0),
            ('azil-priča', 'priča »显« v navedku, čisto.', 0),
            ('rod-prijava', 'mera 10⁴ v pečatu je rod, čisto.', 0),
            ('omemba-pare', 'raba ⟨ ⟩ je omemba kanona, čisto.', 0),
            ('priča-zlep', 'priča »beseda ⟨ padla v prenosu« je VERBATIM, čisto.', 0),
        ]
        vsi = True
        for ime_b, bes, pricakovan in primeri:
            udarci, _, _, _ = cenzus(bes)
            koda = 2 if udarci else 0
            složilo = (koda == pricakovan)
            print(f'  samopreizkus {ime_b}: exit {koda} {"⊢" if složilo else "⊥"}')
            vsi = vsi and složilo
        print(f'  baterija: {"PISALA ⊢ ( vse pasti padle ) " if vsi else "PADC STROJA ⊥"}')
        sys.exit(0 if vsi else 2)
    if len(sys.argv) < 2:
        print('raba: cenzus-izhoda.py FAJL | --samopreizkusi'); sys.exit(3)
    try:
        besedilo = open(sys.argv[1], encoding='utf-8').read()
    except OSError:
        print('IO: fajl manjka'); sys.exit(3)
    udarci, azili, rodi, stevci = cenzus(besedilo)
    for st, razred, cp, opis in udarci:
        kazalec = f'⟨U+{cp:04X}⟩ ' if cp else ''
        print(f'VBOD vrstica {st} · {razred} · {kazalec}{opis}')
    for st, razred, cp, opa in azili:
        print(f'AZIL vrstica {st} · {razred} · ⟨U+{cp:04X}⟩ · {opa}')
    for st, razred, cp, opa in rodi:
        print(f'ROD vrstica {st} · {razred} · ⟨U+{cp:04X}⟩ · {opa}')
    print(f'SKUPAJ: udarci ×{len(udarci)} ⌇ azili ×{len(azili)} ⌇ rodi ×{len(rodi)}')
    sys.exit(2 if udarci else 0)

if __name__ == '__main__':
    main()
