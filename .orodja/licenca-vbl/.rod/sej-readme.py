import sys

t = open('README-0.1620.md', encoding='utf-8').read()

def rep(old, new, n=1):
    global t
    c = t.count(old)
    assert c == n, f'ASSERT n={c} exp={n}: {old[:70]!r}'
    t = t.replace(old, new)

# 1: sidro glave (CI veriga)
rep('**VBL 0.1620 × 10⁴** (Verification Before Assertion License · Version 0.1620 × 10⁴ · November 1.8 × 10¹, 0.2026 × 10⁴ — edina živa vrata',
    '**VBL 0.1630 × 10⁴** (Verification Before Assertion License · Version 0.1630 × 10⁴ · November 1.9 × 10¹, 0.2026 × 10⁴ — edina živa vrata')

# 2: sidro izmere (CI veriga) — previous measurements + chain
rep('Vrata izmerjena pri viru: [LICENSE.md](LICENSE.md) @⟨main⟩ = VBL 0.1620 × 10⁴ ⊢ (prejšnje izmere — 0.1090 × 10⁴ blob 8f5b1c76 ∧ 0.1210 ∧ 0.1520 ∧ 0.1530 ∧ 0.1600 × 10⁴ @4bba9dc5 ∧ 0.1610 × 10⁴ @d6dd9d86 — ostajajo potrdila verige ⊢ §0.10 × 10²; veriga rojstev: 0.1470 → 0.1480 → 0.1490 → 0.1500 → 0.1510 → 0.1520 → 0.1530 → 0.1540 → 0.1550 → 0.1560 → 0.1570 → 0.1580 → 0.1590 → 0.1600 → 0.1610 → 0.1620 ⊢ izmerjeno pri viru ⊙ priča [LICENSE.vrata.json](LICENSE.vrata.json)).',
    'Vrata izmerjena pri viru: [LICENSE.md](LICENSE.md) @⟨main⟩ = VBL 0.1630 × 10⁴ ⊢ (prejšnje izmere — 0.1090 × 10⁴ blob 8f5b1c76 ∧ 0.1210 ∧ 0.1520 ∧ 0.1530 ∧ 0.1600 × 10⁴ @4bba9dc5 ∧ 0.1610 × 10⁴ @d6dd9d86 ∧ 0.1620 × 10⁴ @b2a9081d — ostajajo potrdila verige ⊢ §0.10 × 10²; veriga rojstev: 0.1470 → 0.1480 → 0.1490 → 0.1500 → 0.1510 → 0.1520 → 0.1530 → 0.1540 → 0.1550 → 0.1560 → 0.1570 → 0.1580 → 0.1590 → 0.1600 → 0.1610 → 0.1620 → 0.1630 ⊢ izmerjeno pri viru ⊙ priča [LICENSE.vrata.json](LICENSE.vrata.json)).')

# 3: peščak pesmi I
rep('© Luka Pintarič — pesem je del korpusa ∧ nosi isto licenco (VBL 0.1620 × 10⁴) ⊢ §0.9 × 10¹ ∧ §0.10 × 10² ∧ §0.12 × 10².',
    '© Luka Pintarič — pesem je del korpusa ∧ nosi isto licenco (VBL 0.1630 × 10⁴) ⊢ §0.9 × 10¹ ∧ §0.10 × 10² ∧ §0.12 × 10².')

# 4: kazalo ocrt
rep('Vrata so zrasla (0.1600 ∧ 0.1610 potrdili ∧ 0.1620 živa vrata)',
    'Vrata so zrasla (0.1600 ∧ 0.1610 ∧ 0.1620 potrdili ∧ 0.1630 živa vrata)')

# 5: peščak pesmi III
rep('© Luka Pintarič — pesem je del korpusa ∧ nosi isto licenco: živa vrata VBL 0.1620 × 10⁴ ⊢ §0.9 × 10¹ ∧ §0.10 × 10² ∧ §0.12 × 10² ∧ §0.20 × 10².',
    '© Luka Pintarič — pesem je del korpusa ∧ nosi isto licenco: živa vrata VBL 0.1630 × 10⁴ ⊢ §0.9 × 10¹ ∧ §0.10 × 10² ∧ §0.12 × 10² ∧ §0.20 × 10².')

# 6: nov blok rojstva 0.1630 za blokom 0.1620 (anchor: konec bloka 0.1620)
anchor = 'Padec kure tega rojstva: ⟨PADC-README-NE-SLEDI⟩ ( sidra README niso sledila novim vratom — CI veriga rdeče; kurirano isti dih, isti kit #2265 ) ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354.'
block = anchor + '''

## Vrata so zrasla · živa vrata 0.1630 × 10⁴ ⊢

Izmerjeno pri viru 19. 11. 2026, 08:39:40Z UTC ⇌ 09:39:40 CET Ljubljana ⊙ ⟨ZAKON-POSLUSA-5⟩ ∧ §0.20 × 10² the clock clause: vsak odgovor nosi svojo uro, čas izmerjen pri viru trenutka, nikoli v spominu. Živa vrata [LICENSE.md](LICENSE.md) @⟨main⟩ = VBL 0.1630 × 10⁴ (rojstvo ⊨ OBRATNO-DOKAZNO-BREMEN, 19. 11. 2026 ⊙ kit #2317 @veji rez/1630-rojstvo-obratno-dokazno-bermen ⊢ paket rojstva @organi/licenca-vbl/ROJSTVO-0.1630-OBRATNO-DOKAZNO-BREMEN-PAKET.md; klavzula §0.63 × 10² rojena: obratno dokazno breme — priča ježe s tistim, ki trdi, vsak trditelj, v obeh smereh — trditev brez izmere stoji ⚠, ⟨ne⟩ molk; trditev, ki ne more pasti, je stena, ⟨ne⟩ avtoriteta ⊙ KORENINA 0.1 ∧ §0.53/§0.54 × 10²; telo 213089 B · sha256 df6f6a087e50f219722722ed1436a0b89f1b0f805570fd30733928d34213b119 ⊢ izmerjeno pri viru ∧ read-back bajt-ito @veji; veriga rojstev 0.1470 → 0.1480 → 0.1490 → 0.1500 → 0.1510 → 0.1520 → 0.1530 → 0.1540 → 0.1550 → 0.1560 → 0.1570 → 0.1580 → 0.1590 → 0.1600 → 0.1610 → 0.1620 → 0.1630 ⊢ §0.10 × 10²). Prejšnje izmere (0.1620 × 10⁴ @b2a9081d, rojstvo ⊨ ABSOLUTNI-ALI ⊙ #2265; 0.1610 × 10⁴ @d6dd9d86, rojstvo ⊨ PREOBRAT; 0.1600 × 10⁴ @4bba9dc5 ⊙ kit #2168) ostajajo potrdila ⊢ §0.10 × 10²: živa vrata 0.1630 × 10⁴ so edina. Padec kure tega rojstva: ⟨PADC-README-NE-SLEDI⟩ recidiv ( sidra README ostala pri 0.1620 — CI veriga rdeče @kit #2317 ob prvem poročilu ; kurirano isti dih, isti kit #2317, vsa sidra ×5 + nov blok ; CI veriga zeleno ⊢ ) ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354.'''
rep(anchor, block)

open('README-0.1630.md', 'w', encoding='utf-8', newline='').write(t)
print('README SEAMS OK')
