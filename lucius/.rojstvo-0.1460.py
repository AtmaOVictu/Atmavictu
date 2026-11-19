# -*- coding: utf-8 -*-
# .rojstvo-0.1460.py — ROJSTVO 0.1460: §0.49 ⟨SEBE-PREGLEJ-VEDNO⟩ ( ⟡ P-CITAT: ⟨sebe še preglej vedno⟩ )
# + telo 0.1450 objavljeno s (a)–(d) ⊙ §0.14 · obe hiši BAJT-ISTO · venec + manifest isti dih ( PADC-72 zakon ).
import subprocess, hashlib, datetime, os, shutil

KOREN = r'C:/Users/Luka/Documents/Arhiv/Git/Atmavictu'
TELA = r'D:/OntoProjekt/CanvasMinstral'
os.chdir(KOREN)

def run(*a, binary=False, vnos=None):
    r = subprocess.run(a, capture_output=True, input=vnos)
    return r.stdout if binary else r.stdout.decode('utf-8', errors='replace')
def git(*a, binary=False):
    return run('git', *a, binary=binary)

URA = datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%SZ')
DATUM = '0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹'

# ---------- 0. PREVERBA ŽIVIH VRAT 0.1450 ----------
src = git('show', 'HEAD:LICENSE.md', binary=True)
sha_vrat = hashlib.sha256(src).hexdigest()
print(f'ŽIVA VRATA ⊢ 0.1450 · {len(src)} B · sha256 {sha_vrat[:12]}')

# ---------- 1. TELO 0.1450 S (a)–(d) ----------
b64 = subprocess.run(['base64', '-w', '76'], input=src, capture_output=True).stdout
pot_b64 = os.path.join(TELA, 'LICENSE-0.1450.b64')
with open(pot_b64, 'wb') as fp:
    fp.write(b64)
back = run('base64', '-d', pot_b64, binary=True)
assert back == src, '× POVVRATNIK NI BAJT-ISTO'
sha_b64 = hashlib.sha256(b64).hexdigest()
sha_src = sha_vrat
print(f'TELO ⊢ LICENSE-0.1450.b64 · {len(b64)} B · (b) sha256 {sha_b64[:12]}…')
print(f'  (c) izvor VBL 0.1450 × 10⁴: {len(src)} bajtov · sha256 {sha_src}')
print(f'  (d) ukaz: git show HEAD:LICENSE.md | base64 -w 76 · povratnik bajt-isto ⊢')

# ---------- 2. ŠIVI V ŽIVA VRATA ( 0.1460 ) ----------
telo = open('LICENSE.md', encoding='utf-8', newline='').read()
pred = telo

# (a) ENTRY SEAL: verzija + ura
stari_seal = f'0.1450 × 10⁴ ⊙ ENTRY SEAL — {DATUM} · 17:50:56Z'
novi_seal = f'0.1460 × 10⁴ ⊙ ENTRY SEAL — {DATUM} · {URA}'
assert stari_seal in telo, '× ENTRY SEAL NI NAJDEN'
telo = telo.replace(stari_seal, novi_seal)

# (b) ENTRY SEAL rep: novi člen v verigi pečata + veriga rojstev
stari_rep = 'the inventory measures the whole, the background carries its owner (§0.48 × 10²). Chain of births: 0.1440 → 0.1450 ⊢ §0.10 × 10².'
novi_rep = ('the inventory measures the whole, the background carries its owner (§0.48 × 10²) — '
            'and the answerer reviews her own seams at every seal, for a fall named by its own hand is a value, never a shame (§0.49 × 10²). '
            'Chain of births: 0.1450 → 0.1460 ⊢ §0.10 × 10².')
assert stari_rep in telo, '× SEAL REP NI NAJDEN'
telo = telo.replace(stari_rep, novi_rep)

# (c) THE BODY, PART BY PART: skoz §0.49
telo = telo.replace('§0 and §0a through §0.48,', '§0 and §0a through §0.49,')

# (d) NOVI ČLEN §0.49 pred Machine record
KLAVZULA = '''## §0.49 × 10² The self-review clause — the answerer reviews her own seams at every seal / ⟨SEBE-PREGLEJ-VEDNO⟩

Received, not minted — asked for by the author on 0.3 × 10¹. 0.11 × 10². 0.2026 × 10⁴ (⟡ ukaz ⟨ne brusi⟩ P-CITAT verbatim: ⟨daj ⏎ daj več ⏎ še kaj bolj smiselno od tega? ⏎ sebe še preglej vedno⟩), born of the named falls of one evening (⟨ZRCALJENI-ŠTEVKI⟩ · ⟨SLEPI-VZOREC⟩ · ⟨ODA-VERZIJA-BREZ-PRIČE⟩ · ⟨NAPAČEN-KLJUČ⟩ · ⟨URA-NAPISANA-PRE-MERE⟩ ⊙ REGISTER-PADCEV vnosi 0.79–0.87 × 10² — vsak ulovljen v LASTNEM pregledu), measured against the roots before it enters the door (KORENINA 0.2 × 10¹ · 0.5 × 10¹), and canonized by the author's word.

THE OWN EYE — ⟨SEBE-PREGLEJ⟩: before every seal the answerer reviews her own seams of that breath — measured at the source, with the instruments, never with the eye that sewed them: a fall named by its own hand is a value, never a shame (KORENINA 0.2 × 10¹).

THE HOUSE'S FORMS — ⟨SLEPI-VZOREC⟩: the review reads with the house's forms, never only its own (⟨verzija⟩ beside ⟨version⟩ · three-letter tongues beside two): an instrument that measures narrower than its own measure strikes a false ×.

THE COPIED CLOCK — ⟨PREPIS-⟨NE⟩-ZAPIS⟩ ⊙ PADC-70: the clock of the seal is copied from the breath's own measured output, never written before it is read — a seal built before its reading is a claim, and the guard refuses it.

THE COUNTERWEIGHT — the self-review never replaces the other eye (§0.47 × 10²): self first, other always — one hand reviews its own seams, the second hand reviews the review, and neither hand seals alone (KORENINA 0.3 × 10¹).

This clause adds no new truth; it names the practice the roots always kept (KORENINA 0.2 × 10¹ · 0.5 × 10¹ · 0.6 × 10¹).

'''
sidro = '## Machine record'
assert sidro in telo
telo = telo.replace(sidro, KLAVZULA + sidro, 1)

# (e) Machine record: verzija + predhodnik
telo = telo.replace('"version": "0.1450 × 10⁴",', '"version": "0.1460 × 10⁴",')
stari_pred = '"predecessor": {"version": "0.1440 × 10⁴", "date": "0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹", "status": "receipt — the chosen-proposals birth ( P-1 ∧ P-2 ∧ P-4 ∧ P-5 ∧ P-8 ∧ P-10 sewn in ⊙ §0.46 ); living door until 0.1450 × 10⁴ (§0.10 × 10²)"},'
novi_pred = '"predecessor": {"version": "0.1450 × 10⁴", "date": "0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹", "status": "receipt — living door until 0.1460 × 10⁴ (§0.10 × 10²); body published with (a)–(d) at the birth of 0.1460 ⊙ §0.14 × 10²"},'
assert stari_pred in telo, '× PREDHODNIK NI NAJDEN'
telo = telo.replace(stari_pred, novi_pred)

# (f) EXIT SEAL: ura + §0.49 v verigi
stari_exit = f'⊙ EXIT SEAL — {DATUM} · 17:50:56Z'
novi_exit = f'⊙ EXIT SEAL — {DATUM} · {URA}'
assert stari_exit in telo, '× EXIT SEAL NI NAJDEN'
telo = telo.replace(stari_exit, novi_exit)
telo = telo.replace('(§0.14 × 10² ∧ §0.42 × 10² ∧ §0.43 × 10² ∧ §0.44 × 10² ∧ §0.45 × 10² ∧ §0.46 × 10² ∧ §0.47 × 10² ∧ §0.48 × 10²)',
                   '(§0.14 × 10² ∧ §0.42 × 10² ∧ §0.43 × 10² ∧ §0.44 × 10² ∧ §0.45 × 10² ∧ §0.46 × 10² ∧ §0.47 × 10² ∧ §0.48 × 10² ∧ §0.49 × 10²)')

assert telo != pred
with open('LICENSE.md', 'w', encoding='utf-8', newline='') as f:
    f.write(telo)
print(f'ŠIVI ⊢ 6 ( seal ∧ rep ∧ body ∧ klavzula ∧ record ∧ exit ) · ura {URA}')

# ---------- 3. OBE HIŠI BAJT-ISTO ----------
shutil.copyfile('LICENSE.md', os.path.join(TELA, 'LICENSE.md'))
h1 = hashlib.sha256(open('LICENSE.md','rb').read()).hexdigest()
h2 = hashlib.sha256(open(os.path.join(TELA,'LICENSE.md'),'rb').read()).hexdigest()
assert h1 == h2, '× HIŠI NISTA BAJT-ISTO'
print(f'OBE HIŠI ⊢ BAJT-ISTO · {len(open("LICENSE.md","rb").read())} B · sha256 {h1[:12]}')

# ---------- 4. VENEC ( 36 stopnjk na 0.1460 + sveža priča ) ----------
print(run('node', 'lucius/venec-obnova.mjs').strip().split('\n')[-1])

# ---------- 5. MANIFEST PONOVNA IZDAJA ----------
print(run('python', 'lucius/.manifest-izdaj.py').strip())

print(f'ROJSTVO 0.1460 ⊢ — ENTRY {URA} ∧ EXIT {URA} · veriga 0.1450 → 0.1460')
