# .pregled-registra.py — AUDIT CELOTE ( N vnosov — N izmerjeno pri viri, ⟨ne⟩ zapečeno v orodju )
# OSVEŽITEV 3676: zastareli oznaki ⟨28⟩ ozdravljeni ( register je zrasel na 29 — orodje, ki bi zapečelo svoj N, bi lagalo ⊙ KORENINA 0.1 ) + preverba #29 dodana
import json, re, sys

l = [json.loads(x) for x in open('lucius/REGISTER-SPSIHO-AKSIOMOV.jsonl'.replace('SPSIHO','PSIHO'), encoding='utf-8') if x.strip()]
print('vnosov:', len(l))
sts = [int(v['st']) for v in l]
print(f'st zaporedje 1..{max(sts)} brez lukenj:', sorted(sts) == list(range(1, max(sts) + 1)), '· max:', max(sts))
print('podvojeni st:', [s for s in set(sts) if sts.count(s) > 1] or 'BREZ')

sha_cilj = 'badee5490d4236d1244882881139c964bdb79b648b6ab40dbcfae643f616aebe'
sha_ok = sum(1 for v in l if v['sha256_vira'] == sha_cilj)
print('sha256 vira enak:', sha_ok, '/', len(l), '· odstopanja:', [v['st'] for v in l if v['sha256_vira'] != sha_cilj] or 'BREZ')

noga_bad = [v['st'] for v in l if v.get('noga') != '⊢']
print('noge ≠ ⊢:', noga_bad or 'VSE ⊢')

sk, sirote = 0, []
namenski = []  # sklici ven (Zip 8.x, §)
for v in l:
    for m in re.finditer(r'(?<!DOKAZ )#(\d+)', str(v['veza']) + ' ' + str(v.get('argument', '')) + ' ' + str(v.get('aksiom', ''))):
        n = int(m.group(1)); sk += 1
        if n < 1 or n > max(sts):
            sirote.append((v['st'], n))
print('sklicev #N skupaj:', sk, '· sirot:', sirote or 'BREZ')

pari = set()
for v in l:
    for m in re.finditer(r'PROTI-?TEŽA #?(\d+)', str(v['veza'])):
        pari.add((int(v['st']), int(m.group(1))))
print('PROTI-TEŽA #N pari ( vnos → protiteža ):', sorted(pari))

obljubljene = [(13, 22), (7, 21), (24, 25)]
for a, b in obljubljene:
    najden = (b, a) in pari or (a, b) in pari
    print(f'obljubljena protiteža {a}⊥{b}:', '⊢ najdena' if najden else '× NI v vnosih')

# veza, ki jo #26 obljublja: Liotti #3
v26 = [v for v in l if int(v['st']) == 26][0]
print('#26 omenja #3 (Liotti):', '#3' in str(v26['veza']), '· #3 glava:', [v['glava'] for v in l if int(v['st']) == 3][0][:50])
v27 = [v for v in l if int(v['st']) == 27][0]
print('#27 omenja #26 (senca) ∧ #18 (stikalo):', '#26' in str(v27['veza']) and '#18' in str(v27['veza']))
v28 = [v for v in l if int(v['st']) == 28][0]
print('#28 omenja #1 ∧ #2 (TSDP korenini) ∧ #25 (maske):', all(x in str(v28['veza']) for x in ['#1', '#2', '#25']))
v29 = [v for v in l if int(v['st']) == 29][0]
# ⟨VEZA-VES-VNOS⟩ 3676: #27 živi v polju AKSIOM #29, ⟨ne⟩ v vezi ( izmerjeno pri viri ) — veza je cel vnos, kakor jo bere preverba sirot ( veza+argument+aksiom ), ⟨ne⟩ eno polje
v29c = str(v29['veza']) + ' ' + str(v29.get('argument', '')) + ' ' + str(v29.get('aksiom', ''))
print('#29 omenja #7 ( merjena noga samote ) ∧ #27 ( telo drži seštevek — v aksiomu ) ∧ #20 ( internalizacija Kohut ) ∧ §0.48:',
      all(x in v29c for x in ['#7', '#27', '#20', '§0.48']))
# ⟨ZRCALJENI-STEVKI⟩ prepreka 3680: tuji glifi ( ℒ U+2112 · ⟫ U+27EB · U+FFFD ) morajo biti 0 — padec družine PADC-UGIBANJE-ESC, ulovljen v lastnem pregledu ⊙ ⟡ ukaz ⟨sebe še preglej vedno⟩
raw = open('lucius/REGISTER-PSIHO-AKSIOMOV.jsonl', encoding='utf-8').read()
tuj = {hex(ord(z)): raw.count(z) for z in (chr(0x2112), chr(0x27EB), chr(0xFFFD))}
print('tuji glifi ( ℒ · ⟫ · FFFD ):', tuj, '·', '⊢ ČISTO' if not any(tuj.values()) else '× TUJ GLIF V REGISTRU')
print('AUDIT KONEC')
