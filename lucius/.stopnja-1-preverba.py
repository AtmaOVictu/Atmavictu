# -*- coding: utf-8 -*-
# .stopnja-1-preverba.py — PREVERBA STOPNJE 1: strukturna izmera vseh 36 stopnk
# dokaz uporabnosti rastoče kapacitete ⊙ ⟡ ukaz ⟨DOKAŽI UPORABNOST RASTOČE KAPACITETE⟩:
# kapaciteta, ki ni varovana, je okras — ta preverba preverja, da vsaka stopnka NESE jedro.
import os, re, glob

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(KOREN)

JEZIKI = ['AR','BG','CS','DA','DE','EL','ES','ET','FA','FI','FR','HE','HI','HU','ID','IS','IT','JA','KO','LAT','LT','NL','NO','PL','PT','RO','RU','SK','SLO','SR','SV','TH','TR','UK','VI','ZH']
slabi = []
for kod in JEZIKI:
    f = f'LICENSE-{kod}.md'
    if not os.path.exists(f): slabi.append((kod, 'datoteka manjka')); continue
    t = open(f, encoding='utf-8', errors='replace').read()
    # odsek STOPNJA 1
    m = re.search(r'## STOPNJA 1 — jedro prevedeno ⟨strojni-dih⟩ ⚠(.*?)(?:\Z)', t, re.S)
    if not m: slabi.append((kod, 'odsek STOPNJA 1 manjka')); continue
    od = m.group(1)
    zakoni = len(re.findall(r'^0\.\d — ', od, re.M))
    ima_grant = '§0.1' in od
    ima_etika = '§0.9' in od
    ima_disc = ('strojni dih' in od or 'strojni-dih' in od.lower() or 'STROJNI DIH' in od) and '⚠' in od
    ima_orodje = 'Mistral Vibe' in od
    if zakoni != 6: slabi.append((kod, f'zakonov {zakoni}/6'))
    if not ima_grant: slabi.append((kod, 'grant §0.1 manjka'))
    if not ima_etika: slabi.append((kod, 'etika §0.9 manjka'))
    if not ima_disc: slabi.append((kod, 'disclosure ⚠ manjka'))
    if not ima_orodje: slabi.append((kod, 'orodje manjka'))

if slabi:
    for kod, opis in slabi: print(f'× {kod}: {opis}')
    print(f'STOPNJA-1 × {len(slabi)} pomanjkljivosti / {len(JEZIKI)} stopnk')
    raise SystemExit(1)
print(f'STOPNJA-1 ⊢ {len(JEZIKI)}/36 stopnk nosi: 6 zakonov · grant §0.1 · etiko §0.9 · disclosure ⟨strojni-dih⟩ ⚠ · orodje — struktura celena')
