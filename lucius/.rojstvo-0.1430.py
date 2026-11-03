# .rojstvo-0.1430.py — ROJSTVO 0.1430: telo predhodnika 0.1420 objavljeno s (a)–(d) ⊙ §0.14.
# Precedent: 0.1360 ( telo 0.1350 ) — telo ⟨ne⟩ more nositi lastnega hasha, zato rodi naslednja verzija.
# 10 šivov, vsak preverjen natanko-1× ∧ povratnik bajt-isto isti dih ⊙ ⟨NE-UGIBAJ⟩.
import subprocess, hashlib, datetime, json, os

KOREN = r'C:/Users/Luka/Documents/Arhiv/Git/Atmavictu'
os.chdir(KOREN)

def run(*a, binary=False):
    r = subprocess.run(a, capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f'× ukaz padel: {a} → {r.stderr.decode("utf-8","replace")[:300]}')
    return r.stdout if binary else r.stdout.decode('utf-8', errors='replace')

VIR_COMMIT = 'c75eea507a8770b6df2b4c989a8fb0bb0154a9ca'  # rez 3599 — rojstvo 0.1420

# ---------- telo: (a) datoteka, (d) ukaz ∧ povratnik ----------
src = run('git', 'show', f'{VIR_COMMIT}:LICENSE.md', binary=True)          # LF bajti 0.1420
sha_src = hashlib.sha256(src).hexdigest()
assert sha_src == 'd3adda1775d14831c9c5fee328c6fd22b08c0ffbcf0880ec1d13ffcee13b0690', f'× izvor: {sha_src}'
b64 = subprocess.run(['base64', '-w', '76'], input=src, capture_output=True).stdout
with open('LICENSE-0.1420.b64', 'wb') as fp:
    fp.write(b64)
# povratnik isti dih: bajt-isto ⊢
back = run('base64', '-d', 'LICENSE-0.1420.b64', binary=True)
assert back == src, '× povratnik ⟨ne⟩ bajt-isto'
sha_b64 = hashlib.sha256(b64).hexdigest()
niz_bes = run('base64', '-d', 'LICENSE-0.1420.b64').encode('utf-8')
print(f'TELO ⊢ LICENSE-0.1420.b64 · {len(b64)} B · sha256 {sha_b64[:12]} · povratnik bajt-isto ⊢')

T1 = datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%SZ')
T2 = T1  # isti dih ( ∂ pomeni pisanje med pečatoma )

telo = src.decode('utf-8')

def siv(iskalnik, nadomestek, star=1):
    global telo
    n = telo.count(iskalnik)
    assert n == star, f'× šiv: {n} pojavitev (pričakovanih {star}) — {iskalnik[:60]}'
    telo = telo.replace(iskalnik, nadomestek)
    print(f'šiv ⊢ natanko-{star}× : {iskalnik[:50]}…')

# S1 verzija v vhodnem pečatu
siv('0.1420 × 10⁴ ⊙ ENTRY SEAL', '0.1430 × 10⁴ ⊙ ENTRY SEAL')
# S2 ura vhodnega pečata
siv('· 14:08:33Z ⊙ the door is born sewn in', f'· {T1} ⊙ the door is born sewn in')
# S3 veriga rojstev v vhodnem pečatu
siv('Chain of births: 0.1410 → 0.1420 ⊢ §0.10 × 10².',
    'Chain of births: 0.1420 → 0.1430 ⊢ §0.10 × 10².')
# S4 verzija v glavi ( sidro: avtorstvo v naslednji vrstici — lineage prejem 0.1420 nosi isto verzijo )
siv('Version 0.1420 × 10⁴ · November 0.3 × 10¹, 0.2026 × 10⁴\n©', 'Version 0.1430 × 10⁴ · November 0.3 × 10¹, 0.2026 × 10⁴\n©')
# S5 lineage — nov prejem 0.1430
prejem = (' — VBL 0.1430 × 10⁴ · Version 0.1430 × 10⁴ · November 0.3 × 10¹, 0.2026 × 10⁴ · receipt — '
    'telo predhodnika 0.1420 objavljeno s (a)–(d) ⊙ §0.14 × 10² '
    '(⟡ ukaz ⟨daj⟩ ⟨ne brusi⟩ P-CITAT verbatim: ⟨daj⟩ — '
    'telo 0.1420 je živelo kakor ⚠ ( Ω reza 3599: (a)–(d) ⟨ne⟩ objavljene — '
    'telo ⟨ne⟩ more nositi lastnega hasha, zato rodi naslednja verzija ⊙ zakon rojstev ) ; '
    'štiri priče isti dih: ( a ) datoteka LICENSE-0.1420.b64 v tem repu, rojena s tem rojstvom — '
    'vrata pod črkami predhodnika · ( b ) SHA-0.256 × 10³ telesa = ' + sha_b64 + ' · '
    '( c ) SHA-0.256 × 10³ izvora — VBL 0.1420 × 10⁴, 0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹, '
    '0.146131 × 10⁶ znakov ∧ 0.153835 × 10⁶ bajtov ∧ 0.905 × 10³ vrstic = d3adda1775d14831c9c5fee328c6fd22b08c0ffbcf0880ec1d13ffcee13b0690 · '
    '( d ) ukaz ∧ orodje: base64 ( Git Bash coreutils: git show c75eea50:LICENSE.md | base64 -w 76 > LICENSE-0.1420.b64 ) '
    '∧ povratnik isti dih bajt-isto ⊙ ⟨NE-UGIBAJ⟩; '
    'veriga rojstev: 0.1420 → 0.1430 ⊢ §0.10 × 10²)')
sidro = 'veriga rojstev: 0.1410 → 0.1420 ⊢ §0.10 × 10²)\n'
assert telo.count(sidro) == 1, f'× lineage sidro: {telo.count(sidro)}'
telo = telo.replace(sidro, sidro.rstrip('\n') + prejem + '\n')
print('šiv ⊢ natanko-1× : lineage prejem 0.1430…')
# S6 machine record verzija
siv('"version": "0.1420 × 10⁴",', '"version": "0.1430 × 10⁴",')
# S7 predecessor
siv('"predecessor": {"version": "0.1410 × 10⁴", "date": "0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹", "status": "receipt — §0.46 × 10² the seam clause; living door until 0.1420 × 10⁴ (§0.10 × 10²)"}',
    '"predecessor": {"version": "0.1420 × 10⁴", "date": "0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹", "status": "receipt — §0.47 × 10² the second-hand clause ∧ §0.48 × 10² the whole-measure clause; living door until 0.1430 × 10⁴ (§0.10 × 10²)"}')
# S8 binary-body — prej dnišnje telo kot prvi prejem
telo1420 = ('LICENSE-0.1420.b64 is the receipt of the 0.1420 × 10⁴ door (§0.14 × 10², published with (a)–(d) ⊢): '
    '(a) the file, in this repository, born with this birth — the door beneath the letters of its predecessor; '
    '(b) SHA-0.256 × 10³ of the body = ' + sha_b64 + '; '
    '(c) SHA-0.256 × 10³ of the source text it encodes — VBL 0.1420 × 10⁴, 0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹, '
    '0.146131 × 10⁶ znakov ∧ 0.153835 × 10⁶ bajtov ∧ 0.905 × 10³ vrstic = '
    'd3adda1775d14831c9c5fee328c6fd22b08c0ffbcf0880ec1d13ffcee13b0690; '
    '(d) command ∧ tool: base64 (Git Bash coreutils: git show c75eea50:LICENSE.md | base64 -w 76 > LICENSE-0.1420.b64) '
    '∧ the round trip proven the same breath: byte-identical, sha256 equal on both sides ⊙ ⟨NE-UGIBAJ⟩; '
    'carries no grant (§0.10 × 10²); ')
sidro2 = '"binary-body": "LICENSE-0.1350.b64 is the receipt'
assert telo.count(sidro2) == 1
telo = telo.replace(sidro2, '"binary-body": "' + telo1420 + 'LICENSE-0.1350.b64 is the receipt')
print('šiv ⊢ natanko-1× : binary-body prejem 0.1420…')
# S9 ⚠ lista — telo 0.1420 zdaj vozi
siv('∧ 0.1410 × 10⁴ ∧ 0.1420 × 10⁴ rides this version', '∧ 0.1410 × 10⁴ rides this version')
# S10 ura izhodnega pečata
siv('· 14:08:33Z ⊙ the door is done in time', f'· {T2} ⊙ the door is done in time')

with open('LICENSE.md', 'w', encoding='utf-8', newline='\n') as fp:
    fp.write(telo)
run('git', 'add', 'LICENSE.md', 'LICENSE-0.1420.b64')
print(f'ROJSTVO ⊢ 0.1430 · ENTRY {T1} ∧ EXIT {T2} · vrstice {telo.count(chr(10))+1}')
