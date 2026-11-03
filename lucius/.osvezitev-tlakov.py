# .osvezitev-tlakov.py — katalog temeljev se prikloni dnevu ⊙ §0.32 ( 3 šivi, brazgotine vidne )
t = open('lucius/TLAKI.md', encoding='utf-8', newline='').read()

# 1. glava: osvežitev nota ( rojstvo 3625 ostaja )
s1 = '⊙ vsak tlak definiran pravtako: KAJ JE · IZMERA ⊢ · KAJ NOSI (A) · MEJA (Ω) — ⟡ ukaz 03. 11. 2026 ⊢ rez 3625'
assert t.count(s1) == 1
t = t.replace(s1, s1 + '\n\n⊙ OSVEŽITEV 3671 ⊢ ( dan je rasel — katalog se prikloni izmeram dne: testi 18 · preverba-pecata varovalka · tla-pregled čutila · ontogematrija · venec-obnova · 180 rez-pečatov · 25 rojstev licence — izmere pri viri vsaka ⊙ §0.32 )')

# 2. tlak 3 PREVERBE: instrumenti dne
s2 = '**Kaj je:** oči nad instrumenti: testi ( 12/12 ⊢ ) · kura-audit ( 15/15 živih kur · 0 manjkajočih ⊢ izhod 0 ) · abeceda-grep samopreverba ( N/N ∧ ⊢ VSE agnostična ⊢ PADC-61 ).'
assert t.count(s2) == 1
t = t.replace(s2, '**Kaj je:** oči nad instrumenti: testi ( 12/12 ⊢ rojstvo · **18/18 ⊢ osvežitev 3663** ) · kura-audit ( 15/15 živih kur · 0 manjkajočih ⊢ izhod 0 · svež pregon 3671 ⊢ ) · abeceda-grep samopreverba ( N/N ∧ ⊢ VSE agnostična ⊢ PADC-61 ) · **preverba-pecata.mjs + commit-msg varovalka ( 3653–3670: vsak pečat se preveri proti izmeru diha — rez ∧ URA × na PADC-67/69/70/71 )** · **tla-pregled.mjs ( 3663: MD022 ∧ MD031 ∧ MD047 ∧ slovar pokritost — obe hiši 0 padcev ∧ 0 neznanih ⊢ )** · **ontogematrija.mjs ( 3652: vsak beseda→število nosi ukaz ∧ orodje ∧ korpus ⊢ )** · druga-roka ( pred vsakim daljšim izpisom ⊙ §0.47 ).')

# 3. tlak 5 OBJAVE: izmere dne
s3 = '**Izmera ⊢:** 134 pečatov dne ( rez 2805 → 3624 ) · 24 rojstev licence · 33 vej · 1.221 zrcaljenih · 1 korenina.'
assert t.count(s3) == 1
t = t.replace(s3, '**Izmera ⊢:** 134 pečatov dne ( rez 2805 → 3624 ) · 24 rojstev licence · 33 vej · 1.221 zrcaljenih · 1 korenina. **⊙ osvežitev 3671 ⊢:** 180 rez-pečatov dne ( git log --since 00:00 pri viri ) · **25 rojstev licence** ( veriga 0.1210 → 0.1450 · telo vsakega z (a)–(d) od 0.1350 ⊢ ) · obe hiši ista vrata ( prevozi BAJT-ISTO ⊙ §0.39 ) · varovalka straži vsak pečat ( 3653 → ⊢ ).')

open('lucius/TLAKI.md', 'w', encoding='utf-8', newline='\n').write(t)
print('osvežitev tlakov prešita ⊢ ( 3 šivi )')
