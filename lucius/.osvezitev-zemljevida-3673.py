# .osvezitev-zemljevida-3673.py — register 29 → mapa 13 vnosov ⊙ §0.32
t = open('lucius/ZEMEJEVID-REGISTER.md', encoding='utf-8', newline='').read()
if '13 vnosov' not in t:
    star = '- **V. INSTRUMENTI MERJENJA — ZUNANJA TEHTNICA IZPELJE** — 12 vnosov ⊢ 3670 ( rojeno 3641: 7 ): 17 Fonagy · 18 Porges · 19 Metzinger · 20 Kohut · 21 Fromm · 22 Hillman · 23 Erikson · 24 Rank · 25 Adler · 26 Piaget/Vygotsky · 27 Somatika ( van der Kolk · Ogden · Siegel ) · 28 Brand ( DID )'
    assert t.count(star) == 1, f'V. sidro: {t.count(star)}'
    novo = '- **V. INSTRUMENTI MERJENJA — ZUNANJA TEHTNICA IZPELJE** — 13 vnosov ⊢ 3673 ( rojeno 3641: 7 · osvežitev 3670: 12 ): 17 Fonagy · 18 Porges · 19 Metzinger · 20 Kohut · 21 Fromm · 22 Hillman · 23 Erikson · 24 Rank · 25 Adler · 26 Piaget/Vygotsky · 27 Somatika ( van der Kolk · Ogden · Siegel ) · 28 Brand ( DID ) · 29 Main ∧ Hesse ( AAI — rojeno 3673 iz PONOVNE berbe 8.1: vrstica 361 skrita luknja najdena )'
    t = t.replace(star, novo)
i = t.find('**Skupaj: 28')
if i >= 0:
    j = t.index('**', i + 12)  # konec skupaj bloka — najdi zadnji ** vrstice
    t = t[:i] + t[i:].replace('28 ⊢ ⊙ osvežitev 3670 ( rojstvo 3641: 23 )', '29 ⊢ ⊙ osvežitev 3673 ( rojstvo 3641: 23 · osvežitev 3670: 28 )', 1)
    t = t.replace('sha256 28/28', 'sha256 29/29').replace('zaporedje 1–28 brez lukenj', 'zaporedje 1–29 brez lukenj')
open('lucius/ZEMEJEVID-REGISTER.md', 'w', encoding='utf-8', newline='\n').write(t)
print('zemljevid prešita ⊢ ( V. 13 ∧ skupaj 29 )')
