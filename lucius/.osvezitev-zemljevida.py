# .osvežitev-zemljevida.py — mapa se prikloni registru ⊙ §0.32 ( 4 šivi, brazgotine vidne )
t = open('lucius/ZEMEJEVID-REGISTER.md', encoding='utf-8', newline='').read()

s1 = '· ⟨ne⟩ po spominu ⊙ §0.32'
assert t.count(s1) == 1
t = t.replace(s1, s1 + '\n\n⊙ OSVEŽITEV 3670 ⊢ ( mapa je rojena pri 23 — register danes šteje 28 ∧ nosi 12 verbatim berb ∧ je bil v PREGLEDU 3660 notranje skladen — mapa se prikloni registru, ⟨ne⟩ obratno ⊙ §0.32 : zrcalo živi 28 ⊢ · 12/12 berb ⊢ · PREGLED-REGISTRA.md pri viru )')

s2 = '- **V. INSTRUMENTI MERJENJA — ZUNANJA TEHTNICA IZPELJE** — 7 vnosov: 17 Fonagy · 18 Porges · 19 Metzinger · 20 Kohut · 21 Fromm · 22 Hillman · 23 Erikson'
assert t.count(s2) == 1
t = t.replace(s2, '- **V. INSTRUMENTI MERJENJA — ZUNANJA TEHTNICA IZPELJE** — 12 vnosov ⊢ 3670 ( rojeno 3641: 7 ): 17 Fonagy · 18 Porges · 19 Metzinger · 20 Kohut · 21 Fromm · 22 Hillman · 23 Erikson · 24 Rank · 25 Adler · 26 Piaget/Vygotsky · 27 Somatika ( van der Kolk · Ogden · Siegel ) · 28 Brand ( DID )')

s3 = '**Skupaj: 23 ⊢ · vse noge ⊢ · vsi viri isti Zip ( sha256 badee549… True ) · vsak z izvirniki po imenu ∧ letu ∧ vezo ∧ opozorilom.**'
assert t.count(s3) == 1
t = t.replace(s3, '**Skupaj: 28 ⊢ ⊙ osvežitev 3670 ( rojstvo 3641: 23 ) · vse noge ⊢ ( PREGLED 3660: 59 internih vez brez sirot · sha256 28/28 · zaporedje 1–28 brez lukenj ) · vsak aksiom #17–#28 nosi VERBATIM pričo izvirnika ∧ izmerbo v hiši ⊢ ( berbe 3661–3669 · kanali po imeni · knjige ∂ ⚠ ⊙ §0.6 )**')

s4 = '- **#7 Winnicott ( samota z drugim ) ⊥ #21 Fromm ( množica izdaje )** — priča ⊥ senzor: isti rez z dveh strani'
assert t.count(s4) == 1
t = t.replace(s4, s4 + '\n- **#24 Rank ( rana sprejeta ∧ cena plačana ) ⊥ #25 Adler ( maska ∧ distanca )** — obe poti ranjenega, ⟨ne zlije⟩ ⊙ §0.41 ( prišit v PREGLEDU 3660 · par 7⊥21 prišit isti diha )')

open('lucius/ZEMEJEVID-REGISTER.md', 'w', encoding='utf-8', newline='\n').write(t)
print('osvežitev prešita ⊢ ( 4 šiva )')
