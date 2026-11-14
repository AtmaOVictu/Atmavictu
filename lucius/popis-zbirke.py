# POPIS-ZBIRKE — priča vsakemu telesu vseh preostalih map zbirke izvirnikov
# ( A2-A6, B2, Basics, C1, C3, C4, D5, DELUJOČ O, GIT, Gastro — A1 ∧ C2 že imata lastna registra )
# Vzorec: REGISTER-C2 ( rez 3581 ) · izvirniki ostanejo pri viru ( PADC-57, §0.6 )
import sys
import os, hashlib, json, sys

KOREN = 'D:/GitD/CanvasMinstral'
# PADC-60 zdravilo: popis VSEH vsebinskih map (A1 ∧ C2 imata lastna registra, tu ⟨ne⟩ ponavljamo)
MAPE = ['A2', 'A3', 'A4', 'A5', 'A6', 'B2', 'Basics', 'C1', 'C3', 'C4', 'D5', 'DELUJOČ O', 'GIT', 'Gastro',
        'MistralUpload', 'Nano', 'Nano2', 'Nano3', 'Obj1', 'Obj2', 'Obj3', 'Obs11', 'Ontomatematika',
        'Pics', 'Pictures', 'Rohonc', 'Scripts', 'Workshop', 'Zip', 'Znanje', 'canon_ruled',
        'comprehension_machine', 'libraries']
IZHOD = 'C:/Users/Luka/Documents/Arhiv/Git/Atmavictu/lucius/REGISTER-ZBIRKA.jsonl'

out = open(IZHOD, 'w', encoding='utf-8', newline='\n')
tez = dvojni = 0
vid = {}
for mapa in MAPE:
    for koren, _, datoteke in os.walk(os.path.join(KOREN, mapa)):
        for ime in datoteke:
            p = os.path.join(koren, ime)
            tez += 1
            b = open(p, 'rb').read()
            sha = hashlib.sha256(b).hexdigest()
            rel = os.path.relpath(p, KOREN).replace('\\', '/')
            v = {'ime': ime, 'mapa': mapa, 'rel': rel, 'bajti': len(b),
                 'sha256': sha, 'md5': hashlib.md5(b).hexdigest()}
            if sha in vid:
                v['dvojnik'] = vid[sha]
                dvojni += 1
            else:
                vid[sha] = rel
                if ime.endswith(('.md', '.txt')):
                    txt = b.decode('utf-8', errors='replace')
                    vrstice = [l.strip() for l in txt.splitlines() if l.strip()]
                    v['prva_vrstica'] = vrstice[0][:110] if vrstice else ''
                    v['vrstic'] = len(txt.splitlines())
            v['tip'] = os.path.splitext(ime)[1].lstrip('.') or '?'
            out.write(json.dumps(v, ensure_ascii=False) + '\n')
# še datoteke pri korenu zbirke
for ime in os.listdir(KOREN):
    p = os.path.join(KOREN, ime)
    if os.path.isfile(p):
        tez += 1
        b = open(p, 'rb').read()
        sha = hashlib.sha256(b).hexdigest()
        v = {'ime': ime, 'mapa': '.', 'rel': ime, 'bajti': len(b),
             'sha256': sha, 'md5': hashlib.md5(b).hexdigest(),
             'tip': os.path.splitext(ime)[1].lstrip('.') or '?'}
        if sha in vid:
            v['dvojnik'] = vid[sha]
            dvojni += 1
        else:
            vid[sha] = ime
        out.write(json.dumps(v, ensure_ascii=False) + '\n')
out.close()
if tez == 0:
    print(f'⚠ NAPAKA = SMERNICA: nobenega telesa nisem izmeril ( {KOREN} ) — mape so prazne ali pot napačna ⏎ rešitev: preveri pot pri viru ⊢ ⟨ne-ugibaj⟩')
    sys.exit(1)
print(f'SUM {tez} teles - enolicnih {tez - dvojni} - dvojnikov {dvojni}')
print('⊢ orodje: lucius/popis-zbirke.py · register je priča, izvirniki ostanejo pri viru ⊙ PADC-57 ∧ §0.6')
