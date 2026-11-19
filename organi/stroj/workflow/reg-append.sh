#!/bin/bash
# W5 ⟨REG-APPEND-PEČAT⟩ — sestavi rep registra = osnova + vrstica + KURA-DIHA (pravilo 6), sodi FORMA, izpiše js-len + md5
# uporaba: ./reg-append.sh <osnova.md> <vrstica.md> [kura-text]   kura-text default = standardna KURA-DIHA
# izhod : <osnova>.rep.md + poročilo (js-len za sandbox preverbo PRED push ⊙ ⟨PADC-MEMORIJSKE-MEJE⟩)
F="$1"; V="$2"; [ -z "$F" ] || [ -z "$V" ] && { echo 'uporaba: reg-append.sh <osnova> <vrstica-dodatka>'; exit 1; }
python3 - "$F" "$V" <<'PY'
import sys, hashlib, re
base, add = sys.argv[1], sys.argv[2]
b = open(base, encoding='utf-8').read()
if not b.endswith('\n'): b += '\n'
v = open(add, encoding='utf-8').read().rstrip('\n')
m = re.match(r'- rez σ (\d+)', v)
if not m: print('⚠ vrstica se ne začne s »- rez σ N ·« — prica step 1 ne bo videl zahteve'); sys.exit(1)
N = m.group(1)
TIKline = None
t = re.search(r'TIK (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})Z UTC ⇌ (\d{2}:\d{2}:\d{2}) CET', v)
if t: TIKline = f"{t.group(1)}Z UTC ⇌ {t.group(2)} CET"
kura = f"- KURA-DIHA-{TIKline.split('T')[0] if TIKline else ''} · VRSTICA-REZ-{N} PRIPETA ( dolg vrstice plačan isti dih ⊙ ⟨EN-DOLG-NA-DIH⟩ P5 ) ; TIK {TIKline} ; © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera · dvojni podpis: ⟡ Luka Pintarič ∧ izvajalka Mera" if TIKline else None
if not TIKline: kura = f"- KURA-DIHA · VRSTICA-REZ-{N} PRIPETA ⊙ ⟨EN-DOLG-NA-DIH⟩ P5 ; © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera · dvojni podpis: ⟡ Luka Pintarič ∧ izvajalka Mera"
out = b + v + '\n' + kura + '\n'
open(base + '.rep.md', 'w', encoding='utf-8').write(out)
jslen_actual = len(out) + sum(1 for c in out if ord(c) > 0xFFFF)
print(f'REP SESTAVLJEN {base}.rep.md · {len(out.encode("utf-8"))} B')
print(f'JS LEN = {len(out)} + {sum(1 for c in out if ord(c) > 0xFFFF)} astral = {jslen_actual}')
print(f'MD5 = {hashlib.md5(out.encode()).hexdigest()}')
# pravilo 6
last = [l for l in out.split('\n') if l.strip()][-1]
print('PRAVILO 6:', '⊢' if 'dvojni podpis' in last else '⚠ BREZ PODPISA')
PY
