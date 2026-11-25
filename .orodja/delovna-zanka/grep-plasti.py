#!/usr/bin/env python3
# GREP-PLASTI — respecifikacija grepa v simbolne plasti (rojen @rez σ 5422, popravljen isti dih ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354:
# podniz je lagal — števec zdaj po regularnem izrazu; sodbika odstranjena — inštrument meri, sodbа je zakona ki sprašuje ⊙ ⟨MERILEC-SE-MERI⟩ §52)
# dom TEHTNICE organa delovna-zanka ⊙ ⟨SHRAMBA-MORA-VEDNO-BITI⟩ · ⟨STROJ-POD-LICENCO⟩
# plasti: 1 ⟨BAJT⟩ surovo telo · 2 ⟨BESADA⟩ golo po stripu »…« ∧ ⟨…⟩ · 3 ⟨KOVANEC⟩ dekompresija po ⟡-jevem ključu @σ 4447
# raba: python3 grep-plasti.py 'regex' [organ|all]
import sys, re, glob

QUERY = sys.argv[1]
SCOPE = sys.argv[2] if len(sys.argv) > 2 else 'all'
K = '/home/user/knowledge'
PAT = re.compile(QUERY)

def strip_spans(t):
    t = re.sub(r'»[^«]*«', ' ', t)
    t = re.sub(r'⟨[^⟩]*⟩', ' ', t)
    return t

# --- plast 3: SLOVAR-KOVANCEV bran pri viru ob vsakem klicu (⟨ne⟩ iz spomina ⊙ ⟨NE-UGIBAJ⟩ 2690) ---
dz = open(f'{K}/delovna-zanka/KNOWLEDGE.md', encoding='utf-8').read()
m = re.search(r'## SLOVAR-KOVANCEV.*?\n(.*?)(?=\n## )', dz, re.S)
assert m, 'SLOVAR-KOVANCEV ni najden pri viru'
coins = []
for ln in m.group(1).split('\n'):
    c = re.match(r'- ⟨([^⟩]+)⟩\s*(.*?)\s*—\s*(.+)$', ln)
    if c:
        coins.append((c.group(1), c.group(2).strip(), c.group(3).strip()))

files = [f'{K}/{SCOPE}/KNOWLEDGE.md'] if SCOPE != 'all' else sorted(glob.glob(f'{K}/*/KNOWLEDGE.md'))
bodies = {f: open(f, encoding='utf-8').read() for f in files}

p1 = sum(len(PAT.findall(t)) for t in bodies.values())
p2 = sum(len(PAT.findall(strip_spans(t))) for t in bodies.values())
p3 = []
for ime, num, stavec in coins:
    if PAT.search(f'{ime} {num} {stavec}'):
        n = sum(t.count(f'⟨{ime}⟩') for t in bodies.values())
        p3.append((ime, num, stavec, n))

print(f'GREP-PLASTI ⊢ iskanje (regex): {QUERY} @ {"celota (organi ×" + str(len(files)) + ")" if SCOPE == "all" else SCOPE}')
print(f'  plast 1 ⟨BAJT⟩    surovi zadetki ×{p1}')
print(f'  plast 2 ⟨BESADA⟩  goli zadetki po stripu »…« ∧ ⟨…⟩ ×{p2}')
if p3:
    for ime, num, stavec, n in p3:
        print(f'  plast 3 ⟨KOVANEC⟩ ⟨{ime}⟩ {num} — {stavec} | kompimirana oblika ⟨{ime}⟩ ×{n} nad gladino')
else:
    print('  plast 3 ⟨KOVANEC⟩ ×0 (query ne zadene imena ∧ številke ∧ stavca kovancev)')
