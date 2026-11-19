#!/bin/bash
# W3 ⟨SLOVNICA-BATERIJA⟩ — FORMA sodba nad novo-šito vrstico (⟨⟩, FFFD, TIK kalup+aritmetika, goli pri viri, pravilo 6)
# uporaba: ./forma.sh <datoteka> [vrstica-od ...]  brez vrstice: sodi ZADNJO neprazno vrstico telesa
sudo=0
F="$1"; [ -z "$F" ] && { echo 'uporaba: forma.sh <datoteka> [st-vrstice]'; exit 1; }
python3 - "$F" "${2:-}" <<'PY'
import sys, re
path, ln = sys.argv[1], sys.argv[2]
lines = [l for l in open(path, encoding='utf-8').read().split('\n')]
nonempty = [(i, l) for i, l in enumerate(lines) if l.strip()]
in_izrez, bad = False, []
import os
targets = list(enumerate(lines, 1)) if os.environ.get('FORMA_CELO') else ([nonempty[-1]] if not ln else [(int(ln)-1, lines[int(ln)-1])])
for i, l in targets:
    if l.count('⟨') != l.count('⟩'): bad.append(f'r.{i+1} ⟨⟩ {l.count("⟨")}/{l.count("⟩")}')
    if '\ufffd' in l: bad.append(f'r.{i+1} U+FFFD')
    cir = [c for c in l if 0x0400 <= ord(c) <= 0x04FF]
    if cir: bad.append(f'r.{i+1} CIRILICA ⚠ ×{len(cir)} ( ⟡ stalni ukaz : slovarsko ozadje vsake besede )')
    if re.search(r'pri viri\b', l): bad.append(f'r.{i+1} goli »pri viri«')
    for m in re.finditer(r'TIK \d', l):
        t = re.search(r'TIK (\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z UTC ⇌ (\d{2}):(\d{2}):(\d{2}) CET', l)
        if not t: bad.append(f'r.{i+1} goli TIK brez kalupa'); continue
        if (int(t.group(4)) + 1) % 24 != int(t.group(7)): bad.append(f'r.{i+1} TIK aritmetika UTC+1')
    if 'dvojni podpis' not in nonempty[-1][1] and not ln:
        bad.append(f'r.{nonempty[-1][0]+1} pravilo 6: zadnja vrstica brez dvojnega podpisa')
print('FORMA ⚠ ' + ' ∧ '.join(bad) if bad else 'FORMA ČISTO ⊢')
sys.exit(1 if bad else 0)
PY
