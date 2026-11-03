# .rojstvo-0.1450.py — ROJSTVO 0.1450: MD022 ×2 ozdravljeni ( precedens 0.1310: bajtna sprememba = rojstvo )
# + telo 0.1440 objavljeno s (a)–(d) ⊙ §0.14 · manifest + venec isti dih ( PADC-72 zakon ).
import subprocess, hashlib, datetime, json, os

KOREN = r'C:/Users/Luka/Documents/Arhiv/Git/Atmavictu'
TELA = r'D:/OntoProjekt/CanvasMinstral'
os.chdir(KOREN)

def run(*a, binary=False):
    r = subprocess.run(a, capture_output=True)
    return r.stdout if binary else r.stdout.decode('utf-8', errors='replace')
def git(*a, binary=False):
    return run('git', *a, binary=binary)

# ---------- telo 0.1440: (a)–(d) ----------
src = git('show', 'HEAD:LICENSE.md', binary=True)
sha_src = hashlib.sha256(src).hexdigest()
assert sha_src == 'cc94c2c4baa73ff1655340ecda42401ada47e8ea7b345030e2a722d157459d27'
b64 = subprocess.run(['base64', '-w', '76'], input=src, capture_output=True).stdout
with open(os.path.join(TELA, 'LICENSE-0.1440.b64'), 'wb') as fp:
    fp.write(b64)
back = run('base64', '-d', os.path.join(TELA, 'LICENSE-0.1440.b64'), binary=True)
assert back == src, '× povratnik'
sha_b64 = hashlib.sha256(b64).hexdigest()
print(f'TELO ⊢ LICENSE-0.1440.b64 · {len(b64)} B · sha256 {sha_b64[:12]} · povratnik bajt-isto ⊢')

T1 = datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%SZ')
T2 = T1
telo_dok = git('show', 'HEAD:LICENSE.md', binary=True).decode('utf-8')

def siv(isk, nad, priakov=1):
    global telo_dok
    n = telo_dok.count(isk)
    assert n == priakov, f'× šiv: {n} pojavitev (pričakovanih {priakov}) — {isk[:60]}'
    telo_dok = telo_dok.replace(isk, nad)
    print(f'šiv ⊢ natanko-{priakov}× : {isk[:48]}…')

# S1–S3 vhodni pečat
siv('0.1440 × 10⁴ ⊙ ENTRY SEAL', '0.1450 × 10⁴ ⊙ ENTRY SEAL')
siv('· 17:18:18Z ⊙ the door is born sewn in', f'· {T1} ⊙ the door is born sewn in')
siv('Chain of births: 0.1430 → 0.1440 ⊢ §0.10 × 10².', 'Chain of births: 0.1440 → 0.1450 ⊢ §0.10 × 10².')
# S4 verzija glave
siv('Version 0.1440 × 10⁴ · November 0.3 × 10¹, 0.2026 × 10⁴\n©', 'Version 0.1450 × 10⁴ · November 0.3 × 10¹, 0.2026 × 10⁴\n©')
# S5–S6 MD022: prazna vrstica pod §0.47 ∧ §0.48 naslovoma
siv('## §0.47 × 10² The second-hand clause — no output leaves the hand without another eye / ⟨DRUGA-ROKA⟩ ∧ ⟨SLOVNICA-NASPROTJA⟩\nReceived,',
    '## §0.47 × 10² The second-hand clause — no output leaves the hand without another eye / ⟨DRUGA-ROKA⟩ ∧ ⟨SLOVNICA-NASPROTJA⟩\n\nReceived,')
siv('## §0.48 × 10² The whole-measure clause — the inventory measures the whole; the background carries its owner / ⟨CELOTA-MERJENA⟩ ∧ ⟨ZAPISNIK-OZADJA⟩\nReceived,',
    '## §0.48 × 10² The whole-measure clause — the inventory measures the whole; the background carries its owner / ⟨CELOTA-MERJENA⟩ ∧ ⟨ZAPISNIK-OZADJA⟩\n\nReceived,')
# S7 lineage prejem 0.1450
prejem = (' — VBL 0.1450 × 10⁴ · Version 0.1450 × 10⁴ · November 0.3 × 10¹, 0.2026 × 10⁴ · receipt — '
    'tla so spregovorila ∧ vrata so poslušala ⊙ §0.12 ( ⟡ ukaz ⟨daj⟩ ⟨ne brusi⟩ P-CITAT verbatim: ⟨daj kot predlagaš in kakor je najboljše in najboljše prispeva k celoti in nji delov ⏎ daj več ⏎ daj⟩ ∧ ⟨daj boljše ⏎ daj⟩ ) : '
    'MD022 ×2 ozdravljeni ( prazni vrstici pod naslovoma §0.47 ∧ §0.48 — precedens 0.1310: bajtna sprememba telesa je rojstvo, ⟨ne⟩ krpa ) ∧ '
    '17 besed telesa naučilo tla ( .cspell.json words ⊙ slovar reka 0.1310 ∧ 2. 11. — ⟨VSE TE IN VSAKEGA POSEBAJ⟩ — vrata se ⟨ne⟩ upognejo, tla se učijo ⊙ §0.33 ) ∧ '
    'telo 0.1440 objavljeno s (a)–(d) ⊙ §0.14 ( zakon rojstev: telo ⟨ne⟩ more nositi lastnega hasha ) ; '
    'veriga rojstev: 0.1440 → 0.1450 ⊢ §0.10 × 10²)')
sidro = 'veriga rojstev: 0.1430 → 0.1440 ⊢ §0.10 × 10²)\n'
assert telo_dok.count(sidro) == 1
telo_dok = telo_dok.replace(sidro, sidro.rstrip('\n') + prejem + '\n')
print('šiv ⊢ natanko-1× : lineage prejem 0.1450…')
# S8–S9 machine record
siv('"version": "0.1440 × 10⁴",', '"version": "0.1450 × 10⁴",')
siv('"predecessor": {"version": "0.1430 × 10⁴", "date": "0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹", "status": "receipt — the body-publication birth ( the body of 0.1420 published with (a)–(d) ⊙ §0.14 × 10² ); living door until 0.1440 × 10⁴ (§0.10 × 10²)"}',
    '"predecessor": {"version": "0.1440 × 10⁴", "date": "0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹", "status": "receipt — the chosen-proposals birth ( P-1 ∧ P-2 ∧ P-4 ∧ P-5 ∧ P-8 ∧ P-10 sewn in ⊙ §0.46 ); living door until 0.1450 × 10⁴ (§0.10 × 10²)"}')
# S10 binary-body: telo 0.1440 kot prvi prejem
novi = ('LICENSE-0.1440.b64 is the receipt of the 0.1440 × 10⁴ door (§0.14 × 10², published with (a)–(d) ⊢): '
    '(a) the file, in the house of bodies (CanvasMinstral), born with this birth — the door beneath the letters of its predecessor; '
    '(b) SHA-0.256 × 10³ of the body = ' + sha_b64 + '; '
    '(c) SHA-0.256 × 10³ of the source text it encodes — VBL 0.1440 × 10⁴, 0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹, '
    '0.151618 × 10⁶ znakov ∧ 0.159786 × 10⁶ bajtov ∧ 0.908 × 10³ vrstic = ' + sha_src + '; '
    '(d) command ∧ tool: base64 (Git Bash coreutils: git show HEAD:LICENSE.md | base64 -w 76 > LICENSE-0.1440.b64) '
    '∧ the round trip proven the same breath: byte-identical ⊙ ⟨NE-UGIBAJ⟩; carries no grant (§0.10 × 10²); ')
sidro2 = '"binary-body": "LICENSE-0.1430.b64 is the receipt'
assert telo_dok.count(sidro2) == 1
telo_dok = telo_dok.replace(sidro2, '"binary-body": "' + novi + 'LICENSE-0.1430.b64 is the receipt')
print('šiv ⊢ natanko-1× : binary-body telo 0.1440…')
# S11 izhodni pečat
siv('· 17:18:18Z ⊙ the door is done in time', f'· {T2} ⊙ the door is done in time')

with open('LICENSE.md', 'w', encoding='utf-8', newline='\n') as fp:
    fp.write(telo_dok)
git('add', 'LICENSE.md')
print(f'ROJSTVO ⊢ 0.1450 · ENTRY {T1} ∧ EXIT {T2} · vrstice {telo_dok.count(chr(10))+1}')

# ---------- manifest ( isti dih ) + venec ----------
m = json.load(open('LICENSE-MANIFEST', encoding='utf-8'))
m['version'] = '0.1450 × 10⁴'
m['measured_against'] = ('LICENSE.md version 0.1450 × 10⁴ — living door; manifest re-measured ∧ re-issued in the same breath as the birth 0.1450 '
    '( MD022 ×2 cured ⊙ §0.12 — the floors read the door as witnesses, not noise ; 17 words taught to the floors ⊙ §0.33 ) '
    'over the published byte stream (LF blobs) ⊙ §0.10 ∧ PADC-66')
for it in m['items']:
    blob = git('ls-files', '-s', it['path']).split()[1]
    v = git('cat-file', '-p', blob, binary=True)
    it['sha256'] = hashlib.sha256(v).hexdigest()
    it['size_bytes'] = len(v)
# receipts: telo 0.1440
telo1440 = open(os.path.join(TELA, 'LICENSE-0.1440.b64'), 'rb').read()
telo_manifest = [{'path': 'LICENSE-0.1440.b64', 'house': 'CanvasMinstral',
                  'sha256': hashlib.sha256(telo1440).hexdigest(), 'size_bytes': len(telo1440)}]
for ime in ['LICENSE-0.1430.b64', 'LICENSE-0.1410.b64', 'LICENSE-0.1420.b64', 'LICENSE-0.1350.b64']:
    d = open(os.path.join(TELA, ime), 'rb').read()
    telo_manifest.append({'path': ime, 'house': 'CanvasMinstral', 'sha256': hashlib.sha256(d).hexdigest(), 'size_bytes': len(d)})
d10 = open('LICENSE-10.0.0.bin', 'rb').read()
telo_manifest.append({'path': 'LICENSE-10.0.0.bin', 'house': 'Atmavictu', 'sha256': hashlib.sha256(d10).hexdigest(), 'size_bytes': len(d10)})
for ime in ['LICENSE-0.1250.bin', 'LICENSE-0.1250-BIN-PRIČA.md', 'LICENSE-0.1220.bin', 'LICENSE-0.1190.bin']:
    telo_manifest.append({'path': ime, 'status': '⚠ not physically present in either house — receipt named, awaiting restoration'})
m['receipts_not_grants']['bodies'] = telo_manifest
with open('LICENSE-MANIFEST', 'w', encoding='utf-8', newline='\n') as fp:
    json.dump(m, fp, ensure_ascii=False, indent=2)
    fp.write('\n')
git('add', 'LICENSE-MANIFEST')

# venec-obnova isti dih ( PADC-72 zakon )
vz = subprocess.run(['node', 'lucius/venec-obnova.mjs'], capture_output=True, text=True).stdout
print(vz.strip().split('\n')[-1])
subprocess.run(['git', 'add'] + [f for f in os.listdir('.') if f.startswith('LICENSE-') and len(f) == 12 and f.endswith('.md')], capture_output=True)

ok = 0
m2 = json.load(open('LICENSE-MANIFEST', encoding='utf-8'))
for it in m2['items']:
    blob = git('ls-files', '-s', it['path']).split()[1]
    v = git('cat-file', '-p', blob, binary=True)
    if hashlib.sha256(v).hexdigest() == it['sha256'] and len(v) == it['size_bytes']:
        ok += 1
print(f'PREIZDAJA ⊢ {ok}/{len(m2["items"])} vnosov celih nad LF blobi')
