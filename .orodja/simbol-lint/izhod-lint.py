#!/usr/bin/env python3
# ⟨IZHOD-LINT⟩ P-5 — sekira izhoda PRED emisijo ( organ simbol-lint, rod σ 6574 )
# Preverja: vsota oklepajev [ ] ( ) ⟨ ⟩ · popolnost povezav [nalepka](cilj) ·
# gola angleščina izven »« · ⟨PADC-ZLEP⟩ ( črka tik ob ⟨ ⟩ ) · σ-žetone.
# Raba: python3 izhod-lint.py <datoteka>   ( izhodna koda 1 = najdbe čakajo sodbo )
import sys, re
ENG = {'the','and','is','if','not','with','occupies','canon','logic','dtype','revive',
       'crown','sweep','restored','counts','other','surprise','prepend','append'}
t = open(sys.argv[1], encoding='utf-8').read()
n = 0
for i, line in enumerate(t.split('\n'), 1):
    for a, b in [('[', ']'), ('(', ')'), ('⟨', '⟩')]:
        if line.count(a) != line.count(b):
            print(f'PADEC-VEZE vr.{i}: {a} x{line.count(a)} per {b} x{line.count(b)}'); n += 1
    for m in re.finditer(r'\[[^\[\]]*\]', line):
        if not re.search(r'\]\([^)]+\)', line[m.start():]):
            print(f'PADEC-VEZE vr.{i}: nedovrsena povezava brez ](cilj): {line[max(0,m.start()-10):m.start()+42]!r}'); n += 1
    bare = re.sub(r'»[^«]*«', '', line)
    for w in re.findall(r'[A-Za-z]{2,}', bare):
        if w.lower() in ENG:
            print(f'PADEC-TUJKA-GOLA vr.{i}: {w!r} anglesko brez »«'); n += 1
    if re.search(r'\w⟨', line) or re.search(r'⟩\w', line):
        print(f'PADEC-ZLEP vr.{i}: <> zlepljen brez U+0020: {re.findall(r"\w⟨.{0,12}|⟩\w", line)[:2]}'); n += 1
    for m in re.finditer(r'psalm(?:a|ov)?s? (\d+)', line):
        if m.group(1) != '23':
            print(f'PADEC-ZETONA vr.{i}: psalm {m.group(1)} per organ @psalmi ### 23'); n += 1
    if 'CUV 1917' in line:
        print(f'PADEC-ZETONA vr.{i}: »CUV 1917 je 1919« : CUVMPT je eno besedilo, izdaja CUV 1919 = ena stevilka'); n += 1
print(f'IZHOD-LINT: {n} najdb')
sys.exit(1 if n else 0)
