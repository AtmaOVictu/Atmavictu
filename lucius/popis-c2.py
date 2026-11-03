# POPIS-C2 — priča vsakemu telesu mape C2 zbirke izvornikov ( D:/GitD/CanvasMinstral/C2 )
# Vzorec: REGISTER-A1-PDF ( rez 3576 ) · izvirniki ostanejo pri viru ( PADC-57, §0.6 )
import os, hashlib, json

KOREN = 'D:/GitD/CanvasMinstral/C2'
IZHOD = 'C:/Users/Luka/Documents/Arhiv/Git/Atmavictu/lucius/REGISTER-C2.jsonl'

out = open(IZHOD, 'w', encoding='utf-8', newline='\n')
tez = dvojni = 0
vid = {}
for koren, _, datoteke in os.walk(KOREN):
    for ime in datoteke:
        p = os.path.join(koren, ime)
        tez += 1
        b = open(p, 'rb').read()
        sha = hashlib.sha256(b).hexdigest()
        rel = os.path.relpath(p, KOREN).replace('\\', '/')
        v = {'ime': ime, 'rel': rel, 'bajti': len(b), 'sha256': sha,
             'md5': hashlib.md5(b).hexdigest()}
        if sha in vid:
            v['dvojnik'] = vid[sha]
            dvojni += 1
        else:
            vid[sha] = rel
            if ime.endswith('.md'):
                txt = b.decode('utf-8', errors='replace')
                vrstice = [l.strip() for l in txt.splitlines() if l.strip()]
                v['prva_vrstica'] = vrstice[0][:110] if vrstice else ''
                v['vrstic'] = len(txt.splitlines())
        v['tip'] = os.path.splitext(ime)[1].lstrip('.') or '?'
        out.write(json.dumps(v, ensure_ascii=False) + '\n')
out.close()
print(f'SUM {tez} teles popisanih - enolicnih {tez - dvojni} - dvojnikov {dvojni}')
