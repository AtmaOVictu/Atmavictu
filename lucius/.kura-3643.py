# .kura-3643.py — PADC-66 ⟨MANIFEST-DVOJEDNO⟩ zdravilni dih:
# (1) restavracija 5 obrazov vene verbatim iz zgodovine,
# (2) preizdaja celega LICENSE-MANIFEST nad ENIM tokom bajtov (objavljeni LF blob),
# (3) preverba vseh vnosov po izdaji ( druga roka isti pregon ).
import json, hashlib, subprocess, os

KOREN = r'C:/Users/Luka/Documents/Arhiv/Git/Atmavictu'
os.chdir(KOREN)

def run(*a, binary=False):
    r = subprocess.run(a, capture_output=True)
    return r.stdout if binary else r.stdout.decode('utf-8', errors='replace')

def git(*a, binary=False):
    return run('git', *a, binary=binary)

# ---------- (1) restavracija 5 obrazov ----------
OBRAZI = ['LICENSE-LINEAGE.md', 'LICENSE-SPREHOD.md', 'LICENSE-PESEM.md',
          'LICENSE-LICENC.md', 'LICENSE-TONGUES.md']
obrat = {}
for f in OBRAZI:
    h = git('log', '--all', '--format=%H', '-1', '--', f).strip()
    telo = git('show', f'{h}:{f}', binary=True)
    with open(f, 'wb') as fp:
        fp.write(telo)
    git('add', f)
    blob = git('ls-files', '-s', f).split()[1]
    vseb = git('cat-file', '-p', blob, binary=True)
    obrat[f] = {'commit': h, 'blob': blob,
                'sha256': hashlib.sha256(vseb).hexdigest(),
                'size': len(vseb), 'vrstic': vseb.decode('utf-8').count('\n')}
    print(f'RESTAVRIRAN {f} @{h[:8]} · {len(vseb)} B · sha256 {obrat[f]["sha256"][:12]}')

# ---------- (2) preizdaja manifesta nad LF blobi ----------
m = json.load(open('LICENSE-MANIFEST', encoding='utf-8'))
for it in m['items']:
    p = it['path']
    blob = git('ls-files', '-s', p).split()[1]
    vseb = git('cat-file', '-p', blob, binary=True)
    it['sha256'] = hashlib.sha256(vseb).hexdigest()
    it['size_bytes'] = len(vseb)

dodani = []
for f, o in obrat.items():
    m['items'].append({
        'path': f,
        'size_bytes': o['size'],
        'sha256': o['sha256'],
        'note': (f'restored verbatim this breath from its last body in the chain '
                 f'@{o["commit"][:8]} — witness of the 0.1220–0.1250 era, never a door '
                 f'(§0.33 × 10²); no grant rides it (§0.10 × 10²)')
    })
    dodani.append(f)

m['not_physically_restored_yet'] = {
    'files': [],
    'reason': ('all five wreath faces physically restored verbatim this breath '
               '(LINEAGE · SPREHOD · PESEM · LICENC · TONGUES — see items); they ride as '
               'witnesses, never doors (§0.33 × 10²); scar: this field remains named, '
               'the fall ⟨PADC-66⟩ in REGISTER-PADCEV.jsonl keeps its record ⊙ KORENINA 0.2')
}
m['measured_against'] = ('LICENSE.md version 0.1420 × 10⁴ — living door, born readable '
    '(§0.33 × 10²); manifest re-issued in the same breath as the birth (rez σ 3408) ⊙ §0.10 × 10²; '
    're-measured ∧ re-issued over the published byte stream (LF blobs of the chain — .gitattributes '
    'text=auto) this breath: the fall ⟨PADC-MANIFEST-DVOJEDNO⟩ (PADC-66) — the first issuance hashed '
    'the CRLF working tree while the chain publishes LF — named ∧ cured the same breath, scar kept')
m['issuance_duty'] = ('re-measured ∧ re-issued in the same breath as every new version of LICENSE.md '
    '(§0.10 × 10²); scar: the previous manifest was 0.1250 × 10⁴ and stayed stale through the births '
    'of 0.1200 × 10⁴ → 0.1420 × 10⁴ — named ⟨MANIFEST-EN-DIH-PO-ROJSTVU⟩ ∧ cured ⊙ REGISTER-PADCEV; '
    'renewal: the wreath ×36 stubs (AR → ZH) ride as witness-slots awaiting translators, re-measured '
    '∧ re-issued in the same commit wave as LICENSE.md 0.1420 × 10⁴; the law from the fall: the '
    're-issuance rides the same commit wave as the birth, never after it; the law from PADC-66: the '
    'manifest hashes the bytes the chain publishes (LF), never the local checkout — a manifest of '
    'two byte streams identifies nothing (§0a)')

with open('LICENSE-MANIFEST', 'w', encoding='utf-8', newline='\n') as fp:
    json.dump(m, fp, ensure_ascii=False, indent=2)
    fp.write('\n')
git('add', 'LICENSE-MANIFEST')

# ---------- (3) preverba vseh vnosov po izdaji ----------
m2 = json.load(open('LICENSE-MANIFEST', encoding='utf-8'))
ok = 0
for it in m2['items']:
    p = it['path']
    blob = git('ls-files', '-s', p).split()[1]
    vseb = git('cat-file', '-p', blob, binary=True)
    if hashlib.sha256(vseb).hexdigest() == it['sha256'] and len(vseb) == it['size_bytes']:
        ok += 1
    else:
        print('× NE-USTEZA PO IZDAJI:', p)
print(f'PREIZDAJA ⊢ {ok}/{len(m2["items"])} vnosov celih nad LF blobi')
