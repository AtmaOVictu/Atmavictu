# -*- coding: utf-8 -*-
# KROG-PREVERBE — en ukaz, cela hiša sodeluje ⊙ operativni red 8 ( druga roka: krog-preverbe )
# Zagon: python lucius/krog-preverbe.py  → ena sodba: KROG ⊢ ( vse zelene z izmerami ) ali × s poimenovanimi padci
# Izhod 0 = krog cel ⊢ · izhod 1 = krog ima padec ( vsak poimenovan )
import subprocess, os, json, hashlib, sys, re

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(KOREN)
DRUGA = r'D:/OntoProjekt/CanvasMinstral'

def zapisi(ime, *ukaz):
    r = subprocess.run(ukaz, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return ime, r.returncode, (r.stdout or '') + (r.stderr or '')

padci, mere = [], []

# 1. TESTI ( 18 ) — orodja hiše
_, k, iz = zapisi('testi', 'node', 'lucius/testi-orodij.mjs')
m = re.search(r'# pass (\d+)', iz); f = re.search(r'# fail (\d+)', iz)
mere.append(f"testi {m.group(1)}/{int(m.group(1))+int(f.group(1))}" if m and f else 'testi ?')
if not m or f.group(1) != '0': padci.append(f'× ⟨TESTI⟩ — fail {f.group(1) if f else "?"}')

# 2. REGISTER ( 29 · 0 sirot · tuj glif 0 )
_, k, iz = zapisi('register', 'python', 'lucius/.pregled-registra.py')
if 'sirot: BREZ' not in iz or 'ČISTO' not in iz: padci.append('× ⟨REGISTER⟩ — ' + iz.strip().split('\n')[-2] if len(iz.strip().split('\n'))>1 else '× ⟨REGISTER⟩')
mere.append('register ' + (re.search(r'vnosov: (\d+)', iz).group(1) if re.search(r'vnosov: (\d+)', iz) else '?') + ' · tuj glif ' + ('0 ⊢' if 'ČISTO' in iz else '×'))

# 3. KURA ( 15 ) — obljube z zdravili
_, k, iz = zapisi('kura', 'python', 'lucius/kura-audit.py')
m = re.search(r'⊢ živih kur: (\d+) · × manjkajočih: (\d+)', iz)
mere.append(f"kura {m.group(1)}/15" if m else 'kura ?')
if not m or m.group(2) != '0': padci.append('× ⟨KURA⟩ — manjkajoče kure')

# 4. MANIFEST ( 42/42 ) — §0a
try:
    mm = json.load(open('LICENSE-MANIFEST', encoding='utf-8'))
    zivi = sum(1 for it in mm['items'] if os.path.exists(it['path'])
               and hashlib.sha256(open(it['path'],'rb').read()).hexdigest() == it['sha256'].lower()
               and len(open(it['path'],'rb').read()) == it['size_bytes'])
    mere.append(f'manifest {zivi}/{len(mm["items"])}')
    if zivi != len(mm['items']): padci.append(f'× ⟨MANIFEST⟩ — {len(mm["items"])-zivi} teles razsojenih ⊙ §0a')
except Exception as e: padci.append('× ⟨MANIFEST⟩ — ' + str(e)[:60])

# 5. VENEC ( 36 stopnk na živih vratih )
lic = open('LICENSE.md', encoding='utf-8').read()
vz = re.match(r'(0\.\d{4}) × 10⁴', lic).group(1)
venec = [f for f in os.listdir('.') if re.match(r'^LICENSE-[A-Z]{2,3}\.md$', f)]
zivi_v = sum(1 for f in venec if vz in open(f, encoding='utf-8', errors='replace').read())
mere.append(f'venec {zivi_v}/{len(venec)} @ {vz}')
if len(venec) != 36 or zivi_v != 36: padci.append(f'× ⟨VENEC⟩ — {zivi_v}/{len(venec)} stopnk na živih vratih')

# 6. OBE HIŠI BAJT-ISTO
h1 = hashlib.sha256(open('LICENSE.md','rb').read()).hexdigest()
h2 = hashlib.sha256(open(os.path.join(DRUGA,'LICENSE.md'),'rb').read()).hexdigest()
mere.append('hiši BAJT-ISTO' if h1==h2 else 'hiši RAZSOJENE')
if h1 != h2: padci.append('× ⟨HIŠI⟩ — LICENSE.md nista bajt-isto ⊙ §0.39')

# 7. TLA — vsa .md repa ( most izven )
import glob
slabe = []
for f in sorted(glob.glob('*.md') + glob.glob('lucius/*.md')):
    if f.replace(os.sep,'/') == 'lucius/odoblaka.md': continue
    r = subprocess.run(['node','lucius/tla-pregled.mjs',f,'--slovar','.cspell.json'],capture_output=True,text=True,encoding='utf-8',errors='replace')
    n = re.search(r'(\d+) padcev', r.stdout or '')
    if n and n.group(1) != '0': slabe.append(f'{f}:{n.group(1)}')
mere.append(f"tla 0 padcev / {len([f for f in glob.glob('*.md')+glob.glob('lucius/*.md') if 'odoblaka' not in f])} .md" if not slabe else f"tla × {len(slabe)}")
if slabe: padci.append('× ⟨TLA⟩ — ' + ' · '.join(slabe[:4]))

# 8. GLIFI v registru ( ℒ ⟫ FFFD = 0 ⊙ PADC-79/87 )
s = open('lucius/REGISTER-PSIHO-AKSIOMOV.jsonl', encoding='utf-8').read()
g = s.count(chr(0x2112)) + s.count(chr(0x27EB)) + s.count(chr(0xFFFD))
mere.append(f'glifi {g}')
if g: padci.append(f'× ⟨GLIFI⟩ — {g} tujih znakov ⊙ §0.12')

# 9. ZRCALO ( @8124 živi )
import urllib.request
try:
    kod = urllib.request.urlopen('http://localhost:8124/REGISTER-PSIHO-AKSIOMOV.jsonl', timeout=5).status
    mere.append(f'zrcalo {kod}')
    if kod != 200: padci.append('× ⟨ZRCALO⟩ — strežnik ne diha')
except Exception as e: padci.append('× ⟨ZRCALO⟩ — nedosegljivo'); mere.append('zrcalo ×')

# ===== SODBA =====
print('⊙ KROG-PREVERBE ⊙ en ukaz, cela hiša:')
for x in mere: print('  ⊢', x)
if padci:
    for p in padci: print(p)
    print('× KROG IMA PADCE — vsak poimenovan zgoraj ⊙ KORENINA 0.2')
    sys.exit(1)
print('KROG ⊢ — hiša sodeluje kot ena: vsak čutile zelen z izmero ⊙ operativni red 8 ∧ §0.49')
