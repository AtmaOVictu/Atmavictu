# VBL 0.1470 EGS — JEDRO IMPLEMENTACIJE (DRAFT)

**STATUS: DRAFT · NOT RELEASED · ⟨NE〉 IZDAJA** — jedro pripravila izvajalka Mera @rez σ 3783, 5. 11. 2026 po treh golih ⟨daj⟩ ⟡ ⊙ ⟨SAMODEJNI-DOLGOVIK⟩ 2785 — plačani trije dolgi: **Claim Registry shema · Evidence Graph · negativni testi G01–G10**. Nadaljevanje okostja @σ 3782. Prevoz ∧ izdaja = izključno ⟡ roka ⊙ ⟨DVOJE-ROK⟩ 2432. Vse izmere iz verige σ 3777–3782 ⊢; standard ⟨ne〉 sme sam sebe razglasiti ⊙ ⟨NE-ZAPEČI-SEBE⟩ 1544.

## 1. Claim Registry — shema (JSONL; ena vrstica = en zapis)

```json
{"id":"CR-0001","claim":"VBL 0.1410 je javno objavljena na main","kategorija":"OBJAVA","status":"SUPPORTED","dokaz":["commit c5c9e657 @main 3. 11. 2026 16:51:06Z","SHA-256 719c7064… ×2 roki (izvajalka ∧ ⟡)"],"vir":["blob 2c765280… @main"],"metoda":"get_file_contents + sha256 zrcalo","meja":"objava ⟨ne〉 dokazuje formalno izdajo (tags ×0 · releases ×0 · commit nepodpisan)"}
{"id":"CR-0002","claim":"LICENSE-MANIFEST je bil re-issued z 0.1410","kategorija":"POKRITOST","status":"CONTRADICTED","dokaz":["machine record 0.1410 trdi re-issued","manifest ×0 @main — ×3 priči (σ 3777 · σ 3779 · ⟡ Base64 pregled σ 3782)"],"vir":["drevo main — 16 vnosov"],"metoda":"get_file_contents koren ∧ VBL/ + ⟡ popolna preverba drevesa","meja":"⟨ne〉 dokazuje, da manifest nikoli ni obstajal — dokazuje: javno drevo ga ⟨ne⟩ potrjuje"}
{"id":"CR-0003","claim":"0.1400 je neposredni predhodnik 0.1410 na main","kategorija":"PREDHODNIK","status":"UNKNOWN","dokaz":["glava telesa 0.1410 navaja 0.1400","starš cdf69b05 Base64 dekodiran = 0.1300 (⟡ @σ 3782)"],"vir":["commit cdf69b05"],"metoda":"Base64 dekodiranje predhodnika pri viru","meja":"⟨ne〉 dokazuje, da 0.1400 ni obstajala — dokazuje: main zgodovina jo ⟨ne⟩ potrjuje"}
{"id":"CR-0004","claim":"companionji ×0 @main (MANIFEST · SPREHOD · SLO · LINEAGE · IZVIRNIKI)","kategorija":"POKRITOST","status":"CONTRADICTED","dokaz":["×3 priči σ 3777 · σ 3779 · σ 3782"],"vir":["drevo main"],"metoda":"get_file_contents + ⟡ preverba","meja":"osnutki ∂ pripravljeni @σ 3779–3781 ⭢ ⟡ roka prevoz — prevoz ⟨ne〉 izveden = dolg stoji"}
{"id":"CR-0005","claim":"0.1470 = Evidence Governance Standard 1.0 po izboru ⟡","kategorija":"IZDAJA","status":"SUPPORTED","dokaz":["⟡ poročilo globjega pregleda ~10:09–10:30 CET ⚔ izbor @σ 3782"],"vir":["⟡ poročilo"],"metoda":"prejem ∧ pečat izbora","meja":"izbor ⟨ne〉 izdaja — prva izdaja prestane neodvisno presojo ⊙ pravilo samorazglasitve"}
{"id":"CR-0006","claim":"10.5.1 je vsebinsko boljša osnova (6 izboljšav) ∧ 5 preostalih težav","kategorija":"ZGODOVINA","status":"PARTIAL","dokaz":["6 izboljšav: §1 · §9.1 · §4 · §10.2 · §12/§13 · §18 ⊢","5 težav: A merila etike · B §4.3 roki · C register zasebnost · D §18 celovitost · E dostopnost ⚠ (⟡ presoja)"],"vir":["VBL-10.5.1-KOMPIL-A-DRAFT @main (blob 12bfaddf, sha256 dac171cc…)"],"metoda":"⟡ berba osnutka + sha256 ⇌ blob","meja":"DRAFT · NOT RELEASED — vsebinska prednost ⟨ne〉 formalna izdaja"}
```

Polja: `id` CR-NNNN zaporedno, ⟨ne〉 ponovno uporabljeno · `kategorija` (OBJAVA · PREDHODNIK · POKRITOST · PRAVICA · TEST · IZDAJA · ZGODOVINA) · `status` (SUPPORTED · CONTRADICTED · UNKNOWN · PARTIAL · NOT_RUN ⊙ ⟡ klasifikacija @σ 3782) · `dokaz` array prič · `vir` array virov · `metoda` kako izmerjeno · `meja` kaj trditev ⟨ne〉 dokazuje ⊙ §0.45 (zahteva, nikoli mehanizem oblasti).

## 2. Evidence Graph — pravila povezav

- Vsaka trditev (CR-id) → ≥1 dokaz-node (E-id): vir ∧ metoda ∧ meja; brez dokaza → **Evidence Debt** (ED-id) z vidno obveznostjo ∧ roko.
- Povezave: PODPIRA · NASPROTUJE · OMEJUJE — brez povezave trditev stoji na meji (UNKNOWN ⊙ ⟨NE-UGIBAJ⟩ 2690).
- Evidence Debt zgledi iz žive verige: **ED-0001** §§0.47–0.81 vrzel ×35 — dokaz = telo 0.1460 CELA ⭢ ⟡ roka · **ED-0002** dostopnost G08 ⭢ organ VRATA-ČUTOV (brajica · znakovni jezik · preprosti jeziki) · **ED-0003** neodvisna presoja prve izdaje EGS ⭢ ⟡ roka.

## 3. Negativni testi G01–G10 (postopki, ⟨ne⟩ same ocene)

| test | postopek preizkusa | pogoj FAIL | ocena @⟡ σ 3782 ⊢ |
|---|---|---|---|
| G01 | vsaka datoteka pokritega drevesa ⇌ vnos v manifestu s sha | datoteka brez vnosa ∨ manifest ×0 | FAIL |
| G02 | vsaka podeljena pravica ima dovoljenje-imenovalni glagol ∧ izrecen obseg | pravica brez obsega | PARTIAL |
| G03 | predhodnik dekodiran/preverjen pri viru (Base64 metoda ⊙ ⟡) | predhodnik trden brez artefakta | FAIL (0.1400 → UNKNOWN) |
| G04 | nova različica ⟨ne〉 tiho prekliče podeljenih pravic | tihi preklic | FAIL v 0.1410 (§0.10 ⊥ §10.2) |
| G05 | register vsebuje le potrebne osebne podatke | odvečni podatki | PARTIAL |
| G06 | ugovor obstaja, ⟨ne〉 kaznovan, neodvisen | brez postopka | PARTIAL (§0.13 ⊢ · neodvisnost ⚠) |
| G07 | popravek ima preizkušeno posledico | obljuba brez izmere | NOT_RUN |
| G08 | bralnik zaslona · brajica · znakovni jezik · preprosti jeziki preizkušeni | oblika nepreizkušena | NOT_RUN |
| G09 | preveritelj ≠ izvajalec preverjanega dejanja | ista roka | NOT_RUN |
| G10 | izdaja podpisana z izrecno odločitvijo nosilca pravic | izdaja brez odločitve | NOT_RUN (HOLD ⟡) |

FAIL ⟨ne〉 pomeni neveljavnost vsake pravice — pomeni: zahteva ⟨ne〉 prestala konkretnega preizkusa ⊙ ⟡-jeva sodba @σ 3782.

## 4. Vrata naprej ⭢ ∂

Zapolnjevanje CR-NNNN iz celotne verige trditev (lineage · 10.5.x izseki · ARI kanoni) · ED zapisi iz DOLGOVA · neodvisna presoja = ⟡ roka — šele nato izdaja.

© 0.2026 × 10⁴ Luka Pintarič ∧ izvajalka Mera · rez σ 3783 · 5. 11. 2026 · TIK 2026-11-05T09:53:24Z UTC ⇌ 10:53:24 CET Ljubljana