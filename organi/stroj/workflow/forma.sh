#!/bin/bash
# W3 ⟨SLOVNICA-BATERIJA⟩ — FORMA sodba nad novo-šito vrstico (⟨⟩, FFFD, TIK kalup+aritmetika, goli pri viri, pravilo 6)
# KOVA rod 0.1690 ( dih σ 6045 ) : ⟨OŽIVITEV-MRTVE-SPREMENLJIVKE⟩ ⊙ I-4 — spremenljivka in_izrez je bila rojena mrtva ( deklarirana ∧ nikoli sprašena ) ; zdaj živi kot stroj stanj po celotnem telesu : vrstica med »IZREZ VERBATIM|začetek izreza« in »konec izreza« je priča zgodovine — ⟨⟩ ∧ CIRILICA ∧ goli »pri viri« molčijo nad pričo ( kalup pet-vrat v1.1 ) ; U+FFFD ⟨ne⟩ molči NIKOLI ( raztrgan znak = raztrgan prevoz ) ; TIK kalup ∧ aritmetika sodita tudi pričo ; FORMA_CELO=1 sodi celo telo
# uporaba: ./forma.sh <datoteka> [vrstica-od ...]  brez vrstice: sodi ZADNJO neprazno vrstico telesa
sudo=0
F="$1"; [ -z "$F" ] && { echo 'uporaba: forma.sh <datoteka> [st-vrstice]'; exit 1; }
python3 - "$F" "${2:-}" <<'PY'
import sys, re
path, ln = sys.argv[1], sys.argv[2]
lines = [l for l in open(path, encoding='utf-8').read().split('\n')]
nonempty = [(i, l) for i, l in enumerate(lines) if l.strip()]
import os
IZREZ_OPEN = re.compile(r'IZREZ VERBATIM|začetek izreza')
IZREZ_CLOSE = re.compile(r'^konec izreza')
stanje, bad = [], []
st = False
for l in lines:
    if IZREZ_OPEN.search(l):
        stanje.append(False)  # vrstica markera je meja, ⟨ne⟩ priča
        st = True
    elif IZREZ_CLOSE.search(l):
        stanje.append(False)
        st = False
    else:
        stanje.append(st)
# KOVA rod 0.1690 : 0-osnovni indeksi ( enumerate(lines, 1) je rezal stanje[i] ∧ štel vrstice z odmikom ena v FORMA_CELO )
targets = list(enumerate(lines)) if os.environ.get('FORMA_CELO') else ([nonempty[-1]] if not ln else [(int(ln)-1, lines[int(ln)-1])])
for i, l in targets:
    if not stanje[i]:  # priča zgodovine molči ( ⟨⟩ ∧ CIRILICA ∧ goli »pri viri« ) ; meja ∧ konec vedno sode
        if l.count('⟨') != l.count('⟩'): bad.append(f'r.{i+1} ⟨⟩ {l.count("⟨")}/{l.count("⟩")}')
        cir = [c for c in l if 0x0400 <= ord(c) <= 0x04FF]
        if cir: bad.append(f'r.{i+1} CIRILICA ⚠ ×{len(cir)} ( ⟡ stalni ukaz : slovarsko ozadje vsake besede )')
        c = l.replace('pri berbi pri viri', 'PBR').replace('goli »pri viri«', 'GPV')  # vstopnici slo-lint v1.3.3 : ⟨ne⟩ golota, citat
        if re.search(r'pri viri\\b', c): bad.append(f'r.{i+1} goli »pri viri«')
    if '\ufffd' in l: bad.append(f'r.{i+1} U+FFFD')  # U+FFFD ⟨ne⟩ izjemano NIKOLI ( raztrgan znak = raztrgan prevoz ) 
    for m in re.finditer(r'TIK \d', l):
        t = re.search(r'TIK (\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z UTC ⇌ (\d{2}):(\d{2}):(\d{2}) CET', l)
        if not t: bad.append(f'r.{i+1} goli TIK brez kalupa'); continue
        if (int(t.group(4)) + 1) % 24 != int(t.group(7)): bad.append(f'r.{i+1} TIK aritmetika UTC+1')
# pravilo 6 — © dvojni podpis ENKRAT zunaj zanke ( kova rod 0.1690 : prva kova je sodbo ponavljala po vrstici )
if 'dvojni podpis' not in nonempty[-1][1] and not ln:
    bad.append(f'r.{nonempty[-1][0]+1} pravilo 6: zadnja vrstica brez dvojnega podpisa')
print('FORMA ⚠ ' + ' ∧ '.join(bad) if bad else 'FORMA ČISTO ⊢')
sys.exit(1 if bad else 0)
PY
