#!/bin/bash
# W1 ⟨VRH-DVOSTOPEN⟩ — izmeri vrh σ po organih, izključi lažne vrhove, predlaga rez, preveri varovalko
# uporaba: ./vrh.sh [kladivo]   kladivo = pot do knowledge (default /home/user/knowledge)
K="${1:-/home/user/knowledge}"
python3 - "$K" <<'PY'
import sys, re, glob, os
K = sys.argv[1]
glitch = int(os.environ.get('VRH_GLITCH', '25421'))  # lažni vrh ⊙ precedens σ 5741
vals = {}
for f in glob.glob(os.path.join(K, '*', 'KNOWLEDGE.md')):
    try: s = open(f, encoding='utf-8').read()
    except Exception: continue
    for m in re.finditer(r'σ (\d{3,5})', s):
        n = int(m.group(1))
        if n != glitch: vals.setdefault(n, []).append(os.path.basename(os.path.dirname(f)))
if not vals: print('vrh ×0'); sys.exit(1)
top = max(vals)
rez = top + 1
organi = sorted(set(vals[top]))[:4]
# varovalka rez
v = vals.get(rez, [])
print(f'VRH {top} @ {", ".join(organi)}')
print(f'REZ = 1 + vrh = {rez}')
print(f'VAROVALKA (σ|rez|dih|pečat|PEČAT) {rez}: ' + ('⚠ NAJDEN @ ' + ', '.join(sorted(set(v))[:3]) if v else '×0 ⊢'))
print(f'TIK { __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") } UTC')
PY
