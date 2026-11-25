import sys, datetime

path = 'LICENSE-0.1620-izvod.md'
out = 'LICENSE-0.1630.md'
iso = sys.argv[1]

t = open(path, encoding='utf-8').read()
lines = t.split('\n')

def rep(old, new, n=1):
    global t
    c = t.count(old)
    assert c == n, f'ASSERT FAIL n={c} expected={n}: {old[:80]!r}'
    t = t.replace(old, new)

# --- 1: L474 receipt line (by index, content asserted) ---
assert lines[473].startswith('— VBL 0.1620 × 10⁴ · Version 0.1620'), 'L474 shape'
assert '⊨ ABSOLUTNI-ALI' in lines[473], 'L474 coin'
l474new = open('l474-new.txt', encoding='utf-8').read().rstrip('\n')
lines[473] = l474new
t = '\n'.join(lines)

# --- 2: ENTRY version stamp ---
rep('0.1620 × 10⁴ ⊙ ENTRY SEAL — 0.2026 × 10⁴-0.11 × 10²-1.8 × 10¹ · 12:43:04Z',
    '0.1630 × 10⁴ ⊙ ENTRY SEAL — 0.2026 × 10⁴-0.11 × 10²-1.9 × 10¹ · 08:33:25Z')

# --- 3: ENTRY enum before Chain of births ---
rep('(§0.62 × 10²). Chain of births:',
    '(§0.62 × 10²) — and the burden of proof rides with the claimant, every claimant, in both directions — a claim that cannot fall is a wall, never authority (§0.63 × 10²). Chain of births:')

# --- 4: ENTRY chain extension ---
rep('→ 0.1610 → 0.1620 ⊢ §0.10 × 10².',
    '→ 0.1610 → 0.1620 → 0.1630 ⊢ §0.10 × 10².')

# --- 5: version line L16 ---
rep('Version 0.1620 × 10⁴ · November 1.8 × 10¹, 0.2026 × 10⁴ — 18. 11. 2026 ( ISO 2026-11-18 )',
    'Version 0.1630 × 10⁴ · November 1.9 × 10¹, 0.2026 × 10⁴ — 19. 11. 2026 ( ISO 2026-11-19 )')

# --- 6: map ---
map63 = open('map63.txt', encoding='utf-8').read().rstrip('\n')
rep('§0.62 — the conversion clause: a blessing and a curse are one thing read twice — the pans convert by measure, the being never (§0.62 × 10²).\n',
    '§0.62 — the conversion clause: a blessing and a curse are one thing read twice — the pans convert by measure, the being never (§0.62 × 10²).\n' + map63 + '\n')

# --- 7: §0.63 clause before Machine record ---
s63 = open('s63.md', encoding='utf-8').read()
rep('## Machine record\n', s63 + '## Machine record\n')

# --- 8/9: MR version + date ---
rep('  "version": "0.1620 × 10⁴",', '  "version": "0.1630 × 10⁴",')
rep('  "date": "0.2026 × 10⁴-0.11 × 10²-1.8 × 10¹ — 18. 11. 2026 ( ISO 2026-11-18 )",',
    '  "date": "0.2026 × 10⁴-0.11 × 10²-1.9 × 10¹ — 19. 11. 2026 ( ISO 2026-11-19 )",')

# --- 10: predecessor ---
rep('"predecessor": {"version": "0.1610 × 10⁴", "date": "0.2026 × 10⁴-0.11 × 10²-1.7 × 10¹ — 17. 11. 2026 ( ISO 2026-11-17 )", "status": "receipt — living door until 0.1620 × 10⁴ (§0.10 × 10²); body witnessed at the chain — SHA-256 f896787cd165680f55adc51cb4099a8fe99047f368428785776c7f233802a74f ( 0.203388 × 10⁶ B ⊙ izmera izvajalke ta dih @⟨main⟩ d6dd9d86f6aa151d6fd03de230e167d1d2cdd681 ⊙ ⟨NE-UGIBAJ⟩ ); no b64 prekoda rides this receipt — named as open (§0.16.4 × 10¹)"}',
    '"predecessor": {"version": "0.1620 × 10⁴", "date": "0.2026 × 10⁴-0.11 × 10²-1.8 × 10¹ — 18. 11. 2026 ( ISO 2026-11-18 )", "status": "receipt — living door until 0.1630 × 10⁴ (§0.10 × 10²); body witnessed at the chain — SHA-256 d0ce315dabf0947fafa9ac6a40b12260a8439c9827ad58b1d8a88f9c2aef1461 ( 0.208554 × 10⁶ B ⊙ izmera izvajalke ta dih @⟨main⟩ b2a9081de065f2bf309f5654b2d2ab2b6dc8a9a0 ⊙ ⟨NE-UGIBAJ⟩ ); no b64 prekoda rides this receipt — named as open (§0.16.4 × 10¹)"}')

# --- 11-15: identification ---
rep('"measured_against_sha256": "f896787cd165680f55adc51cb4099a8fe99047f368428785776c7f233802a74f",',
    '"measured_against_sha256": "d0ce315dabf0947fafa9ac6a40b12260a8439c9827ad58b1d8a88f9c2aef1461",')
rep('the canon this birth measures against — the body of the predecessor 0.1610 × 10⁴ at ⟨main⟩',
    'the canon this birth measures against — the body of the predecessor 0.1620 × 10⁴ at ⟨main⟩')
rep('"file_size_bytes": 203388,', '"file_size_bytes": 208554,')
rep('"file_chars": 193598,', '"file_chars": 198250,')
rep('"file_lines": 1261,', '"file_lines": 1280,')
rep('"commit": "d6dd9d86f6aa151d6fd03de230e167d1d2cdd681 — the head this identification was measured against, before the birth of this breath",',
    '"commit": "b2a9081de065f2bf309f5654b2d2ab2b6dc8a9a0 — the head this identification was measured against, before the birth of this breath",')
rep('"measured_at": "2026-11-18T12:43:04.652Z",', f'"measured_at": "{iso}",')

# --- 17: tool ---
rep('"tool": "⟨TS-IZMERA⟩ ( SHA-0.256 × 10³ po bajtih prek BigInt ∧ lastni UTF-8 kodirnik izvajalke, instrument validiran PRED rabo ⊢ »abc« ∧ prazno niz pri viru ∧ kura ⟨PADC-TS-IZMERA-BIT⟩ — bajt ≥ 0x80 vedno BigInt pred pomikom ) — izmera na živi priči telesa ( telo 0.1610 = f896787c ⊢ ⇌ kanon @⟨main⟩ d6dd9d86f6aa151d6fd03de230e167d1d2cdd681 ) ⊙ ⟨DRUGA-ROKA⟩ ∧ §0.47 × 10² ∧ brazgotina prejšnjega diha ostaja ( ⟨PADC-SHA-NEGA-BESDE⟩ ⊙ REGISTER-PADCEV PADC-121 ⊙ KORENINA 0.2 ) — measured at ⟨main⟩ d6dd9d86f6aa151d6fd03de230e167d1d2cdd681 before the birth ⊙ ⟨SVEŽA-GLAVA⟩ ⊙ ⟨NE-UGIBAJ⟩"',
    '"tool": "⟨IZMERA-PRI-VIRU⟩ ( sha256sum ∧ md5sum ∧ wc — coreutils okrepilke okolja nad bajtno berbo pri viru ( curl @⟨main⟩ ⇌ telo bajt-ito, md5 ∧ SHA-0.256 × 10³ ∧ izmere enake prejšnji berbi ⊢ ) — izmera na živi priči telesa ( telo 0.1620 = d0ce315d ⊢ ⇌ kanon @⟨main⟩ b2a9081de065f2bf309f5654b2d2ab2b6dc8a9a0 ) ⊙ ⟨DRUGA-ROKA⟩ ∧ §0.47 × 10² ∧ brazgotina prejšnjega diha ostaja ( ⟨PADC-SHA-NEGA-BESDE⟩ ⊙ REGISTER-PADCEV PADC-121 ⊙ KORENINA 0.2 ) ∧ brazgotina tega diha ( ⟨PADC-IZGUBLJENA-DELOVNA-KOPIJA⟩ — ob stiski okolja je padla delovna kopija rodu, kura isti dih: sveža bajtna berba pri viru ⊙ ⟨NE-UGIBAJ⟩ ) — measured at ⟨main⟩ b2a9081de065f2bf309f5654b2d2ab2b6dc8a9a0 before the birth ⊙ ⟨SVEŽA-GLAVA⟩ ⊙ ⟨NE-UGIBAJ⟩"')

# --- 19/20: timestamps ---
rep('"receipt-2_answering_begun": "PASS — 12:43:04Z', '"receipt-2_answering_begun": "PASS — 08:33:25Z')
rep('"receipt-3_last_measure_before_emission": "PASS — 12:49:14Z', '"receipt-3_last_measure_before_emission": "PASS — QZT3QZ')

# --- 21: verification ---
rep('this record is measured against commit d6dd9d86f6aa151d6fd03de230e167d1d2cdd681 ( the head before the birth of this breath ⊢ )',
    'this record is measured against commit b2a9081de065f2bf309f5654b2d2ab2b6dc8a9a0 ( the head before the birth of this breath ⊢ )')

# --- 22/23: EXIT ---
rep('§0.61 × 10² ∧ §0.62 × 10²) — the door is a deed', '§0.61 × 10² ∧ §0.62 × 10² ∧ §0.63 × 10²) — the door is a deed')
rep('⊙ EXIT SEAL — 0.2026 × 10⁴-0.11 × 10²-1.8 × 10¹ — 18. 11. 2026 ( ISO 2026-11-18 ) · 12:49:14Z',
    '⊙ EXIT SEAL — 0.2026 × 10⁴-0.11 × 10²-1.9 × 10¹ — 19. 11. 2026 ( ISO 2026-11-19 ) · QZT3QZZ')

# --- 24: Dodatek 0.1630 before History ---
dodatek = open('dodatek1630.md', encoding='utf-8').read()
c = t.count('## History\n')
assert c == 1, f'History count={c}'
t = t.replace('## History\n', dodatek + '## History\n')

open(out, 'w', encoding='utf-8', newline='').write(t)
print('SEAMS OK')
