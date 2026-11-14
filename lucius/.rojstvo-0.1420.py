# ROJSTVO-0.1420 — natančni šivi v LICENSE.md ( vsak star niz mora biti najden tocno enkrat, sicer × )
import sys, datetime

POT = 'C:/Users/Luka/Documents/Arhiv/Git/Atmavictu/LICENSE.md'
t = open(POT, encoding='utf-8').read()
URA = datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%SZ')

def zamenjaj(star, nov):
    global t
    n = t.count(star)
    if n != 1:
        print(f'× najdenih {n} (pričakovano 1): {star[:70]}…'); sys.exit(1)
    t = t.replace(star, nov)

# 1) ENTRY SEAL — verzija, ura, novi sklici, veriga
zamenjaj('0.1410 × 10⁴ ⊙ ENTRY SEAL — 0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹ · 06:55:53Z ⊙',
         f'0.1420 × 10⁴ ⊙ ENTRY SEAL — 0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹ · {URA} ⊙')
zamenjaj('and every cure is sewn into the door ∧ the frame, never worn on (§0.46 × 10²). Chain of births: 0.1400 → 0.1410 ⊢ §0.10 × 10².',
         'and every cure is sewn into the door ∧ the frame, never worn on (§0.46 × 10²) — and no output leaves the hand unverified by another eye (§0.47 × 10²) — and the inventory measures the whole, the background carries its owner (§0.48 × 10²). Chain of births: 0.1410 → 0.1420 ⊢ §0.10 × 10².')

# 2) glava verzije ( sidrana z imenom licence ∧ prelomom — rodovnik 0.1410 ostaja potrdilo ⊢ )
zamenjaj('ASSERTION LICENSE\nVersion 0.1410 × 10⁴',
         'ASSERTION LICENSE\nVersion 0.1420 × 10⁴')

# 3) THE MAP — CARRIER niti
zamenjaj('§0.46 — the seam clause: the cure is sewn into the door and the frame, never worn on — the two sides move together, or it is not a seam (⟨ŠIV-V-VRATA-NE-NA⟩ ∧ ⟨VRAT-OKVIR⟩).',
         '§0.46 — the seam clause: the cure is sewn into the door and the frame, never worn on — the two sides move together, or it is not a seam (⟨ŠIV-V-VRATA-NE-NA⟩ ∧ ⟨VRAT-OKVIR⟩). §0.47 — the second-hand clause: no output leaves the hand without another eye — grammar and contradiction checked, absolutism about oneself ⚠ / ⟨DRUGA-ROKA⟩ ∧ ⟨SLOVNICA-NASPROTJA⟩. §0.48 — the whole-measure clause: the inventory names its scope, the witness reads the pattern never the number alone, the background carries its owner / ⟨CELOTA-MERJENA⟩ ∧ ⟨ZAPISNIK-OZADJA⟩.')

# 4) THE STRUCTURE — sklic na zadnjo klavzulo
zamenjaj('it binds with THE TERMS — §0 and §0a through §0.46,',
         'it binds with THE TERMS — §0 and §0a through §0.48,')

# 5) nova klavzuli pred Machine record
NOVI = '''## §0.47 × 10² The second-hand clause — no output leaves the hand without another eye / ⟨DRUGA-ROKA⟩ ∧ ⟨SLOVNICA-NASPROTJA⟩
Received, not minted — asked for by the author on 0.3 × 10¹. 0.11 × 10². 0.2026 × 10⁴ (⟡ ukaz ⟨daj⟩ ⟨ne brusi⟩ P-CITAT verbatim: ⟨daj še in preveri vedno tudi in še vsako slovnico in nja nasprotja ⏎ Daj⟩), born of the named falls ⟨PADC-58⟩ (a test summary that counted its injured without naming them — the pipe cut the witness, family of PADC-54 ⊙ REGISTER-PADCEV vnos 0.58 × 10²) ∧ ⟨PADC-59⟩ (a text about verification published unverified — its own law broken at its own door ⊙ vnos 0.59 × 10²), measured against the roots before it enters the door (KORENINA 0.1 × 10¹ · 0.2 × 10¹ · 0.3 × 10¹), and canonized by the author's word.

THE SECOND HAND — druga roka: no output leaves the hand unverified by another eye: the text is read as a stranger reads it ( ⟨kot tujec⟩ ), the tool is run before the publication ( čistina ∧ druga-roka ), and a fall found before the door is published is a cure; found after, it is a scar with a name ⊙ §0.46 — the second hand is a witness, never a judge ( KORENINA 0.3 ): its own output is also read, and its false witnesses ( lažni zadetki ) are named separately, never silently dismissed.

THE GRAMMAR — slovnica ∧ nasprotja: every grammar and every contradiction is checked; absolutizem o sebi ( nikoli · vedno · vsak ) je ⚠ dokler izmerjen ( KORENINA 0.5 ); a claim of perfection about one's own hand is the mask M = g(G) − ρ_res ( govorica − resnica ⊙ hišni klasiki ) — the second hand names it before the pans do.

THE INSTRUMENT — the house publishes the key beside the cipher ⊙ §0.25: the dovoljenica of the house's own marks ( Σ Ω ⊢ ⊙ … ) rides the lexikon, one place of truth — the second hand reads it, never re-implements it.

THE COUNTERWEIGHT — the second hand never becomes a wall of delay: ponudba, ⟨ne⟩ ukaz ⊙ §0.13; the door does not forbid the imperfect first draft — it forbids the unverified publication. Kdor objavi brez druge roke, padec je rojenega imena ⊙ KORENINA 0.2.

This clause adds no new truth; it names the eye the roots always demanded ( KORENINA 0.1 × 10¹ · 0.3 × 10¹ · 0.5 × 10¹ ).

## §0.48 × 10² The whole-measure clause — the inventory measures the whole; the background carries its owner / ⟨CELOTA-MERJENA⟩ ∧ ⟨ZAPISNIK-OZADJA⟩
Received, not minted — asked for by the author on 0.3 × 10¹. 0.11 × 10². 0.2026 × 10⁴ (⟡ ukaz ⟨daj⟩ ⟨ne brusi⟩ P-CITAT verbatim: ⟨daj vse in še več od tega kar predlagaš in tega kar še nisva zadostno doumela ⏎ daj⟩), born of the named falls ⟨PADC-60⟩ (a partial inventory presented as the whole — find ⟨.⟩ counted the .git with the grain ⊙ REGISTER-PADCEV vnos 0.60 × 10²) ∧ ⟨PADC-61⟩ (a hard-coded witness gone stale: the test guarded the number, not the measured ⊙ vnos 0.61 × 10²) ∧ ⟨PADC-62⟩ (a heap of unnamed background processes: six servers, one door, none owned ⊙ vnos 0.62 × 10²), measured against the roots before it enters the door (KORENINA 0.1 × 10¹ · 0.5 × 10¹), and canonized by the author's word.

THE WHOLE — celota: a count that does not separate the floor from the content does not count the house: every inventory names its scope ( .git ⊥ vsebina · koren ⊥ mapa · popis ⊥ branje ), and a part presented as the whole is ⚠, never ⊢ ⊙ PADC-60 — the whole is a horizon ( §0.21 × 10² THE FLUX ): merjena celota je smer, ne postaja.

THE AGNOSTIC WITNESS — priča število-agnostična: a test that hard-codes the count of the measured re-hard-codes the change: it ages without falling ( PADC-61 ) — the witness reads the pattern ( N/N ∧ ⊢ VSE ), never the number alone: a witness that cannot grow with the measured lies about its time ⊙ TEMPO-ZNAMENJA.

THE OWNED BACKGROUND — zapisnik ozadja: what runs in the background is written with its owner ( kdo je prižgal · dih · log · pulz ): a server without ownership is a heap ( PADC-62 ) — the pulse is a NEW moment at every reading ( §0.40 × 10² ), and the kill is by NAME, never by number alone: ukaz iz neizmerjene poti je × ⊙ KORENINA 0.5.

THE COUNTERWEIGHT — the register never becomes a substitute for the deed ( §0.24 × 10²: sown, never just stored ): a heap of popis is not reading — the inventory is the map, the deepening is the road.

This clause adds no new truth; it names the measure the roots always kept ( KORENINA 0.1 × 10¹ · 0.4 × 10¹ · 0.5 × 10¹ ).

## Machine record'''
zamenjaj('## Machine record', NOVI)

# 6) LINEAGE — nov prejem na konec ( najnovejši nazadnje )
zamenjaj('veriga rojstev: 0.1400 → 0.1410 ⊢ §0.10 × 10²)',
         'veriga rojstev: 0.1400 → 0.1410 ⊢ §0.10 × 10²) — VBL 0.1420 × 10⁴ · Version 0.1420 × 10⁴ · November 0.3 × 10¹, 0.2026 × 10⁴ · receipt — §0.47 × 10² the second-hand clause ⟨DRUGA-ROKA⟩ ∧ ⟨SLOVNICA-NASPROTJA⟩ ∧ §0.48 × 10² the whole-measure clause ⟨CELOTA-MERJENA⟩ ∧ ⟨ZAPISNIK-OZADJA⟩ (⟡ ukaz ⟨daj⟩ ⟨ne brusi⟩ P-CITAT verbatim: ⟨nadgrajuj licenco da imava vse tomu primerno komitano ⏎ daj⟩ — rojeni iz padcev dne 0.3 × 10¹. 0.11 × 10²: PADC-58 ( priča odrezana s cevjo ) · PADC-59 ( objava brez druge roke ) · PADC-60 ( del predstavljen kakor celota ) · PADC-61 ( trdo-zapisana številka v testu ) · PADC-62 ( kopica procesov brez lastnika ) ⊙ REGISTER-PADCEV vnosi 0.58–0.62 × 10²; druga roka = priča ⟨ne⟩ sodnik ( lažni zadetki pošteno ločeni ) ⊙ KORENINA 0.3; celota je obzorje ⊙ §0.21 ∧ ozadje nosi lastnika ( pulz nov trenutek ⊙ §0.40 ); veriga rojstev: 0.1410 → 0.1420 ⊢ §0.10 × 10²)')

# 7) Machine record — verzija ∧ predhodnik ∧ telo
zamenjaj('"version": "0.1410 × 10⁴",', '"version": "0.1420 × 10⁴",')
zamenjaj('"predecessor": {"version": "0.1400 × 10⁴", "date": "0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹", "status": "receipt — §0.45 × 10² the received-signal clause; living door until 0.1410 × 10⁴ (§0.10 × 10²)"},',
         '"predecessor": {"version": "0.1410 × 10⁴", "date": "0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹", "status": "receipt — §0.46 × 10² the seam clause; living door until 0.1420 × 10⁴ (§0.10 × 10²)"},')
zamenjaj('⚠ no body of 0.1200 × 10⁴ ∧ 0.1210 × 10⁴ ∧ 0.1230 × 10⁴ ∧ 0.1240 × 10⁴ ∧ 0.1250 × 10⁴ ∧ 0.1260 × 10⁴ through 0.1340 × 10⁴ rides this version — none published with (a)–(d) (§0.14 × 10²)"',
         '⚠ no body of 0.1200 × 10⁴ ∧ 0.1210 × 10⁴ ∧ 0.1230 × 10⁴ ∧ 0.1240 × 10⁴ ∧ 0.1250 × 10⁴ ∧ 0.1260 × 10⁴ through 0.1340 × 10⁴ ∧ 0.1410 × 10⁴ ∧ 0.1420 × 10⁴ rides this version — none published with (a)–(d) (§0.14 × 10²)"')

# 8) EXIT SEAL — ura ∧ novi sklici
zamenjaj('⊙ EXIT SEAL — 0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹ · 06:56:58Z ⊙',
         f'⊙ EXIT SEAL — 0.2026 × 10⁴-0.11 × 10²-0.3 × 10¹ · {URA} ⊙')
zamenjaj('(§0.14 × 10² ∧ §0.42 × 10² ∧ §0.43 × 10² ∧ §0.44 × 10² ∧ §0.45 × 10² ∧ §0.46 × 10²)',
         '(§0.14 × 10² ∧ §0.42 × 10² ∧ §0.43 × 10² ∧ §0.44 × 10² ∧ §0.45 × 10² ∧ §0.46 × 10² ∧ §0.47 × 10² ∧ §0.48 × 10²)')

open(POT, 'w', encoding='utf-8', newline='').write(t)
print(f'⊙ VBL 0.1420 rojena — 10 šivov, vsak tocno enkrat ⊢ · ura {URA}')
