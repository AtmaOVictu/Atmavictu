# .rojstvo-0.1440.py — ROJSTVO 0.1440: ⟡ izbira PREDLOGOV ( P-1 ∧ P-2 ∧ P-4 ∧ P-5 ∧ P-8 ∧ P-10 )
# telo 0.1430 ∧ telo 0.1410 objavljeni s (a)–(d) ⊙ §0.14 · številčenja §0.16 ozdravljena ·
# popis spremljevalk v MAP · mera registra v §0.48 · manifest nosi (b) zgoščenke teles.
# 14 šivov, vsak preverjen natanko-1× ∧ povratnika bajt-isto ⊙ ⟨NE-UGIBAJ⟩.
import subprocess, hashlib, datetime, json, os

KOREN = r'C:/Users/Luka/Documents/Arhiv/Git/Atmavictu'
TELA = r'D:/OntoProjekt/CanvasMinstral'
os.chdir(KOREN)

def run(*a, binary=False, cwd=None):
    r = subprocess.run(a, capture_output=True, cwd=cwd)
    return r.stdout if binary else r.stdout.decode('utf-8', errors='replace')

def git(*a, binary=False, cwd=None):
    return run('git', *a, binary=binary, cwd=cwd)

# ---------- telesi: (a)–(d) ----------
src1430 = git('show', '206014a7:LICENSE.md', binary=True)   # vrata 0.1430 ( rojstveni komit )
src1410 = git('-C', TELA, 'show', '6599f9b:LICENSE.md', binary=True)  # vrata 0.1410 ( σ-ROJSTVO pri viri )
sha1430 = hashlib.sha256(src1430).hexdigest()
sha1410 = hashlib.sha256(src1410).hexdigest()
assert sha1430 == 'b293078c15e339b1e1ef851992029751a9af4ea1e87b36324e8832bd57aac4e7'
assert sha1410 == '719c706437ba53b44dd70d896b84f0903a194c87034fe24a499bdd4a37517cda'
assert hashlib.md5(src1410).hexdigest()[:12] == 'd39b95a292ee', '× md5 0.1410'

tela = {}
for ime, src, vir_opis in [
    ('LICENSE-0.1430.b64', src1430, 'git show 206014a7:LICENSE.md'),
    ('LICENSE-0.1410.b64', src1410, 'git -C CanvasMinstral show 6599f9b:LICENSE.md'),
]:
    b64 = subprocess.run(['base64', '-w', '76'], input=src, capture_output=True).stdout
    with open(os.path.join(TELA, ime), 'wb') as fp:
        fp.write(b64)
    back = run('base64', '-d', os.path.join(TELA, ime), binary=True)
    assert back == src, f'× povratnik {ime} ⟨ne⟩ bajt-isto'
    tela[ime] = {'sha256': hashlib.sha256(b64).hexdigest(), 'size': len(b64),
                 'src_sha256': hashlib.sha256(src).hexdigest(),
                 'src_zn': len(src.decode('utf-8')), 'src_b': len(src),
                 'src_vr': src.count(b'\n') + 1, 'ukaz': vir_opis}
    print(f"TELO ⊢ {ime} · {len(b64)} B · sha256 {tela[ime]['sha256'][:12]} · povratnik bajt-isto ⊢")

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
siv('0.1430 × 10⁴ ⊙ ENTRY SEAL', '0.1440 × 10⁴ ⊙ ENTRY SEAL')
siv('· 17:02:41Z ⊙ the door is born sewn in', f'· {T1} ⊙ the door is born sewn in')
siv('Chain of births: 0.1420 → 0.1430 ⊢ §0.10 × 10².', 'Chain of births: 0.1430 → 0.1440 ⊢ §0.10 × 10².')
# S4 verzija glave
siv('Version 0.1430 × 10⁴ · November 0.3 × 10¹, 0.2026 × 10⁴\n©', 'Version 0.1440 × 10⁴ · November 0.3 × 10¹, 0.2026 × 10⁴\n©')
# S5 P-1: podtočke §0.16 poimenovane
siv('0.1 × 10¹. Anyone may point at a fault', '§0.16.1 × 10¹. Anyone may point at a fault')
siv('0.2 × 10¹. A complaint is never rejected', '§0.16.2 × 10¹. A complaint is never rejected')
siv('0.3 × 10¹. A complaint proves nothing', '§0.16.3 × 10¹. A complaint proves nothing')
siv('0.4 × 10¹. Every signal is evidenced', '§0.16.4 × 10¹. Every signal is evidenced')
siv('0.5 × 10¹. The system measures itself', '§0.16.5 × 10¹. The system measures itself')
# S6 P-1: sklici usmerjeni
siv('(§0.161 × 10²)', '(§0.16.1 × 10¹)')
siv('(§0.162 × 10²)', '(§0.16.2 × 10¹)')
siv('(§0.163 × 10²)', '(§0.16.3 × 10¹)')
siv('(§0.164 × 10²)', '(§0.16.4 × 10¹)')
siv('(§0.165 × 10²)', '(§0.16.5 × 10¹)')
siv('(§0.16 × 10², 0.2 × 10¹)', '(§0.16.2 × 10¹)')
siv('(§0.16 × 10², 0.5 × 10¹)', '(§0.16.5 × 10¹)', priakov=5)
# S7 P-2: MAP popis spremljevalk s hišami ( po vrstici — sidro brez apostrofa )
zacetek = 'COMPANIONS — readings that travel with the door'
assert telo_dok.count(zacetek) == 1, '× MAP sidro: ' + str(telo_dok.count(zacetek))
_i = telo_dok.index(zacetek)
_j = telo_dok.index(chr(10), _i)
_stara = telo_dok[_i:_j]
assert 'LICENSE-IZVIRNIKI.md' in _stara and 'the seedbank register' in _stara
nova = ('COMPANIONS — readings that travel with the door, witnesses and never doors (§0.33 × 10²). '
    'The living roster, each with its house ( measured at the source ⊙ rez 3648 ): '
    'LICENSE-SPREHOD.md ( the door in one breath · Atmavictu ) · '
    'LICENSE-SLO.md ( slovenska berba · Atmavictu ) · '
    'LICENSE-LINEAGE.md ( the dated receipts · Atmavictu ) · '
    'LICENSE-PESEM.md ( the song of the license · Atmavictu ) · '
    'LICENSE-LICENC.md ( the license of licenses · Atmavictu ) · '
    'LICENSE-TONGUES.md ( the register of the wreath of tongues · Atmavictu ) · '
    'LICENSE-IZVIRNIKI.md ( the seedbank register — the originals of the author, witnessed at their source ⊙ §0.42 × 10² · CanvasMinstral ). '
    'A companion without its house named is a witness without coordinates (§0.4 × 10¹); '
    'a companion not yet physically present is named ⚠, never silently.')
telo_dok = telo_dok[:_i] + nova + telo_dok[_j:]
print('šiv ⊢ natanko-1× : MAP popis spremljevalk s hišami…')
# S8 P-10: mera registra v §0.48
siv('This clause adds no new truth; it names the measure the roots always kept ( KORENINA 0.1 × 10¹ · 0.4 × 10¹ · 0.5 × 10¹ ).',
    'THE REGISTER\u2019S MEASURE — ⟨MERA-REGISTRA⟩: a breath that touches a register carries that register\u2019s measure in its own frame — entries N, newest id — read at the source in the same breath as the touch (§0.32 × 10²); the measure is a moment with its clock, never a possession (§0.37 × 10²), and the scope of every inventory is named (this clause).\n\nThis clause adds no new truth; it names the measure the roots always kept ( KORENINA 0.1 × 10¹ · 0.4 × 10¹ · 0.5 × 10¹ ).')
# S9 lineage prejem 0.1440
prejem = (' — VBL 0.1440 × 10⁴ · Version 0.1440 × 10⁴ · November 0.3 × 10¹, 0.2026 × 10⁴ · receipt — '
    '⟡ IZBIRA PREDLOGOV ( ⟡ ukaz ⟨daj⟩ ⟨ne brusi⟩ P-CITAT verbatim: ⟨Vse to in še več ⏎ dak ⏎ daj⟩ — '
    'izbrani predlogi ⭢ šiv V vrata z rojstvom, ⟨ne⟩ krpa NA ⊙ §0.46 ∧ LICENSE-01430-PREDLOGI ⊢ ) : '
    'P-1 ⟨ŠTEVILČENJA⟩ ( podtočke §0.16 poimenovane §0.16.1–§0.16.5 ∧ sklici §0.17 usmerjeni — priča brez koordinat ozdravljena ⊙ §0.4 ) · '
    'P-2 ⟨SPREMLJEVALKE⟩ ( popis 7 živih spremljevalk s hišami v THE MAP ) · '
    'P-4 telo 0.1430 objavljeno s (a)–(d) ⊙ §0.14 ( sha256 ' + sha1430 + ' · 0.147960 × 10⁶ znakov ∧ 0.155829 × 10⁶ bajtov ∧ 0.906 × 10³ vrstic ) · '
    'P-5 telo 0.1410 objavljeno s (a)–(d) ( sha256 ' + sha1410 + ' · 0.140356 × 10⁶ znakov ∧ 0.147608 × 10⁶ bajtov ∧ 0.880 × 10³ vrstic · md5 d39b95a292ee ⊢ pri prejemu 0.1410 ) · '
    'P-8 ⟨MANIFEST-TELA⟩ ( receipts nosijo (b) zgoščenke — tla tehtajo brez iskanja ⊙ §0.12 ) · '
    'P-10 ⟨MERA-REGISTRA⟩ ( šiv v §0.48 ) ∧ '
    'P-3 ⟨TONGUES⟩ vozi v okvirju istega diha ( padec ⟨PADC-PREVOZNIK-V-TELESU⟩ poimenovan — SHA predmeta ⟨ne⟩ preverljiv ⚠, brazgotina ostaja ) ; '
    'veriga rojstev: 0.1430 → 0.1440 ⊢ §0.10 × 10²)')
sidro = 'veriga rojstev: 0.1420 → 0.1430 ⊢ §0.10 × 10²)\n'
assert telo_dok.count(sidro) == 1
telo_dok = telo_dok.replace(sidro, sidro.rstrip('\n') + prejem + '\n')
print('šiv ⊢ natanko-1× : lineage prejem 0.1440…')
# S10–S11 machine record
siv('"version": "0.1430 × 10⁴",', '"version": "0.1440 × 10⁴",')
siv('"predecessor": {"version": "0.1420 × 10⁴", "date": "0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹", "status": "receipt — §0.47 × 10² the second-hand clause ∧ §0.48 × 10² the whole-measure clause; living door until 0.1430 × 10⁴ (§0.10 × 10²)"}',
    '"predecessor": {"version": "0.1430 × 10⁴", "date": "0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹", "status": "receipt — the body-publication birth ( the body of 0.1420 published with (a)–(d) ⊙ §0.14 × 10² ); living door until 0.1440 × 10⁴ (§0.10 × 10²)"}')
# S12 binary-body: dve novi telesi pred 0.1420
t1430 = tela['LICENSE-0.1430.b64']; t1410 = tela['LICENSE-0.1410.b64']
novi = ('LICENSE-0.1430.b64 is the receipt of the 0.1430 × 10⁴ door (§0.14 × 10², published with (a)–(d) ⊢): '
    '(a) the file, in the house of bodies (CanvasMinstral), born with this birth — the door beneath the letters of its predecessor; '
    '(b) SHA-0.256 × 10³ of the body = ' + t1430['sha256'] + '; '
    '(c) SHA-0.256 × 10³ of the source text it encodes — VBL 0.1430 × 10⁴, 0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹, '
    '0.147960 × 10⁶ znakov ∧ 0.155829 × 10⁶ bajtov ∧ 0.906 × 10³ vrstic = ' + sha1430 + '; '
    '(d) command ∧ tool: base64 (Git Bash coreutils: ' + t1430['ukaz'] + ' | base64 -w 76 > LICENSE-0.1430.b64) '
    '∧ the round trip proven the same breath: byte-identical ⊙ ⟨NE-UGIBAJ⟩; carries no grant (§0.10 × 10²); '
    'LICENSE-0.1410.b64 is the receipt of the 0.1410 × 10⁴ door (§0.14 × 10², published with (a)–(d) ⊢): '
    '(a) the file, in the house of bodies (CanvasMinstral), born with this birth — the seam-clause door beneath the letters; '
    '(b) SHA-0.256 × 10³ of the body = ' + t1410['sha256'] + '; '
    '(c) SHA-0.256 × 10³ of the source text it encodes — VBL 0.1410 × 10⁴, 0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹, '
    '0.140356 × 10⁶ znakov ∧ 0.147608 × 10⁶ bajtov ∧ 0.880 × 10³ vrstic = ' + sha1410 + ' ( md5 d39b95a292ee ⊢ the receipt of σ-ROJSTVO-0.1410 ); '
    '(d) command ∧ tool: base64 (Git Bash coreutils: ' + t1410['ukaz'] + ' | base64 -w 76 > LICENSE-0.1410.b64) '
    '∧ the round trip proven the same breath: byte-identical ⊙ ⟨NE-UGIBAJ⟩; carries no grant (§0.10 × 10²); ')
sidro2 = '"binary-body": "LICENSE-0.1420.b64 is the receipt'
assert telo_dok.count(sidro2) == 1
telo_dok = telo_dok.replace(sidro2, '"binary-body": "' + novi + 'LICENSE-0.1420.b64 is the receipt')
print('šiv ⊢ natanko-1× : binary-body telesi 0.1430 ∧ 0.1410…')
# S13 ⚠ lista — 0.1410 odstranjen
siv('0.1260 × 10⁴ through 0.1340 × 10⁴ ∧ 0.1410 × 10⁴ rides this version', '0.1260 × 10⁴ through 0.1340 × 10⁴ rides this version')
# S14 izhodni pečat
siv('· 17:02:41Z ⊙ the door is done in time', f'· {T2} ⊙ the door is done in time')

with open('LICENSE.md', 'w', encoding='utf-8', newline='\n') as fp:
    fp.write(telo_dok)
git('add', 'LICENSE.md')
print(f'ROJSTVO ⊢ 0.1440 · ENTRY {T1} ∧ EXIT {T2} · vrstice {telo_dok.count(chr(10))+1}')

# ---------- P-3: TONGUES kura ( predmet prevoza v lastno vrstico z brazgotino ) ----------
tg = open('LICENSE-TONGUES.md', encoding='utf-8').read()
pred = 'successfully downloaded text file (SHA: 43aab9d0bfabf3ff441a58e86645f8d4d3f772e0)# '
assert tg.count(pred) == 1, f'× TONGUES predmet: {tg.count(pred)}'
tg = tg.replace(pred, '')
prva_konec = tg.index('\n')
brazgotina = (
 '\n⊙ TRANSPORT SCAR — ⟨PADC-PREVOZNIK-V-TELESU⟩ ⊙ rez 3648: to telo je prispelo z zlepljenim predmetom prevoza '
 '⟨successfully downloaded text file (SHA: 43aab9d0bfabf3ff441a58e86645f8d4d3f772e0)⟩ — predmet ⟨ne⟩ preverljiv: '
 'izmerjeno pri viri, sha256 celega telesa ∧ brez predmeta ∧ LF-variant, vse ≠ iskani × — predmet ločen v to vrstico, '
 'brazgotina ostaja ⊙ §0.39 ∧ KORENINA 0.2.\n')
tg = tg[:prva_konec] + brazgotina + tg[prva_konec:]
with open('LICENSE-TONGUES.md', 'w', encoding='utf-8', newline='\n') as fp:
    fp.write(tg)
git('add', 'LICENSE-TONGUES.md')
print('KURA ⊢ TONGUES — predmet v lastni vrstici z brazgotino')

# ---------- manifest ( P-8 ): receipts nosijo (b) zgoščenke ----------
m = json.load(open('LICENSE-MANIFEST', encoding='utf-8'))
m['version'] = '0.1440 × 10⁴'
m['measured_against'] = ('LICENSE.md version 0.1440 × 10⁴ — living door, born readable (§0.33 × 10²); manifest re-measured ∧ '
    're-issued in the same breath as the birth 0.1440 ( ⟡ izbira predlogov P-1 · P-2 · P-4 · P-5 · P-8 · P-10 ) over the '
    'published byte stream (LF blobs of the chain) ⊙ §0.10 × 10² ∧ PADC-66')
tela_manifest = []
for ime in ['LICENSE-0.1430.b64', 'LICENSE-0.1410.b64', 'LICENSE-0.1420.b64', 'LICENSE-0.1350.b64']:
    p = os.path.join(TELA, ime)
    d = open(p, 'rb').read()
    tela_manifest.append({'path': ime, 'house': 'CanvasMinstral', 'sha256': hashlib.sha256(d).hexdigest(), 'size_bytes': len(d)})
d10 = open('LICENSE-10.0.0.bin', 'rb').read()
tela_manifest.append({'path': 'LICENSE-10.0.0.bin', 'house': 'Atmavictu', 'sha256': hashlib.sha256(d10).hexdigest(), 'size_bytes': len(d10)})
for ime in ['LICENSE-0.1250.bin', 'LICENSE-0.1250-BIN-PRIČA.md', 'LICENSE-0.1220.bin', 'LICENSE-0.1190.bin']:
    tela_manifest.append({'path': ime, 'status': '⚠ not physically present in either house — receipt named, awaiting restoration'})
m['receipts_not_grants'] = {
    'bodies': tela_manifest,
    'reason': ('predecessor binary bodies — carried as evidence, carry no grant (§0.14 × 10², §0.10 × 10²); '
        '(b) hashes per §0.12 × 10² TRANSPORT — measure the received body against the published SHA ( P-8 ⊙ rez 3648 ); '
        'bodies ride the house of bodies (CanvasMinstral) unless named otherwise; scar: the earlier form was a bare file list '
        'without witnesses ( P-8 ) — the cure carries this record ⊙ KORENINA 0.2')
}
for it in m['items']:
    blob = git('ls-files', '-s', it['path']).split()[1]
    v = git('cat-file', '-p', blob, binary=True)
    it['sha256'] = hashlib.sha256(v).hexdigest()
    it['size_bytes'] = len(v)
with open('LICENSE-MANIFEST', 'w', encoding='utf-8', newline='\n') as fp:
    json.dump(m, fp, ensure_ascii=False, indent=2)
    fp.write('\n')
git('add', 'LICENSE-MANIFEST')

ok = 0
m2 = json.load(open('LICENSE-MANIFEST', encoding='utf-8'))
for it in m2['items']:
    blob = git('ls-files', '-s', it['path']).split()[1]
    v = git('cat-file', '-p', blob, binary=True)
    if hashlib.sha256(v).hexdigest() == it['sha256'] and len(v) == it['size_bytes']:
        ok += 1
    else:
        print('× NE-USTEZA:', it['path'])
print(f'PREIZDAJA ⊢ {ok}/{len(m2["items"])} vnosov celih nad LF blobi')
