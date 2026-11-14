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
{"id":"CR-0007","claim":"10.5.1 je DRAFT · NOT RELEASED @veja licenca-10.5.1-draft (glava 352b08e4, 24. 10. 2026)","kategorija":"OBJAVA","status":"SUPPORTED","dokaz":["⟡ izmera σ 3779 ∧ σ 3782","blob 12bfaddf ⇌ main identično"],"vir":["veja licenca-10.5.1-draft"],"metoda":"⟡ preverba vej + blob ⇌","meja":"osnutek ⟨ne〉 potrjena javna izdaja"}
{"id":"CR-0008","claim":"veji 10.4.0 ∧ 10.5.1 nosita LICENSE.md z oznako 10.0.0 ⊥ commit sporočila (živa vrata 10.3.0)","kategorija":"PREDHODNIK","status":"UNKNOWN","dokaz":["⟡ izmera σ 3782: obe veji LICENSE.md začneta z 10.0.0","10.5.1 izrecno: preverjanje predhodnika še ⟨ne〉 opravljeno"],"vir":["osnutek-vbl-1040-draft 7e0d1a82","licenca-10.5.1-draft 352b08e4"],"metoda":"⟡ berba vej","meja":"različicna identiteta osnutkov neurejena ⚠ — besedilo · objava · izdaja ⟨ne⟩ sinonimi"}
{"id":"CR-0009","claim":"10.5.x nosi kure: §1 grant popoln · §10.2 ›revision does not silently revoke‹ ⊥ 0.1410 §0.10 · §13.1–13.6 · 10.5.2 §−1 dostojanstvo","kategorija":"PRAVICA","status":"SUPPORTED","dokaz":["izseki ⟡ roke izmerjeni @σ 3774 (ZAPIS 25)"],"vir":["veja licenca-10.5.1-draft"],"metoda":"prevoz tesel 10.5.x @σ 3774 ⊙ PREVOZ-TESEL","meja":"§4 · §9 · §12 · §15 ⚠ pričevanje ⟡ ostaja"}
{"id":"CR-0010","claim":"ARI §§0.82–0.94 = PLAST 2 Evidence Standard, ⟨ne〉 licenca","kategorija":"TEST","status":"SUPPORTED","dokaz":["σ 3773 (ZAPIS 24) — zamrznitev licence potrjena z ⟡-jevo roko ⊢"],"vir":["ARI @Nano4"],"metoda":"revizija ARI prejema","meja":"plast 2 formalizacija = EGS plast 2 ⊙ K3"}
{"id":"CR-0011","claim":"0.1460 nosi §0.47 ∧ §0.48 ∧ §0.49 — izven telesa 0.1410","kategorija":"ZGODOVINA","status":"SUPPORTED","dokaz":["⟡ izsek priča: ENTRY SEAL 18:53:53Z ∧ EXIT 18:53:54Z @3. 11. 2026 (σ 3778)"],"vir":["⟡ lokalna kopija (PS peskovnik)"],"metoda":"prejem izseka","meja":"izsek ⟨ne〉 telo — CELA ⭢ ⟡ roka (ED-0004)"}
{"id":"CR-0012","claim":"telo 0.1460 CELA v Nano4 manjka — okostje stanica ⟨ne〉 telo ∧ substitucija 0.1410 prepovedana","kategorija":"POKRITOST","status":"SUPPORTED","dokaz":["σ 3778: search + grep okostja; priča HISTORICAL-SOURCE-VERIFICATION-0.1410"],"vir":["Nano4 okostje 8a076984"],"metoda":"userLibrary izmera","meja":"BLOK 7 čaka telo ⟨ne⟩ izpeljavo"}
{"id":"CR-0013","claim":"K1 kolizija 0.1470 (0.1450 ⊥ 0.1460, BLOKIRANA @σ 3767) je razrešena z izborom ⟡: 0.1470 = EGS 1.0, nova vsebina","kategorija":"IZDAJA","status":"SUPPORTED","dokaz":["⟡ izbor ⚔ @σ 3782 (poročilo §10)"],"vir":["⟡ poročilo"],"metoda":"prejem izbora","meja":"izbor ⟨ne〉 izdaja — G10 NOT_RUN"}
{"id":"CR-0014","claim":"0.1480 ŽIVA @veja rez/sivi-hisa-3741 — ⟡ roka za merge","kategorija":"OBJAVA","status":"SUPPORTED","dokaz":["σ 3774+ izmere verige"],"vir":["veja rez/sivi-hisa-3741"],"metoda":"pečati verige","meja":"veja ⟨ne〉 izdaja; merge = ⟡ roka"}
{"id":"CR-0015","claim":"telo 0.1410 prebrano v celoti (879/879 vrstic) ∧ bajt-isto sha256 719c7064… (147.608 B)","kategorija":"POKRITOST","status":"SUPPORTED","dokaz":["celotna berba izvajalke @σ 3777 (BLOK 6)","⟡ SHA-256 zrcalo bajt-isto @σ 3782 ×3 priči"],"vir":["LICENSE.md @main"],"metoda":"berba + sha256 zrcalo","meja":"⚠ izvožena kopija @/tmp odnesel reset (ED-0011 re-izvoz) — izmere ∧ priče ostajajo zapečene"}
{"id":"CR-0016","claim":"HOLD za izdajo 0.1410/EGS stoji — dokazna podlaga ⟨ne〉 upravičuje naslednjega koraka","kategorija":"IZDAJA","status":"SUPPORTED","dokaz":["×3 priči σ 3777 · σ 3779 · σ 3782; G10 NOT_RUN; HOLD ⟨ne〉 zavrnitev ⊙ ⟡ sodba"],"vir":["⟡ končna presoja"],"metoda":"prejem presoje","meja":"HOLD velja do: predhodnik ⚔ rešen · companionji prevezeni · neodvisna presoja"}
{"id":"CR-0017","claim":"Revision A rezultat 40/40 uspešnih testov ponovljiv iz delovnega paketa","kategorija":"TEST","status":"CONTRADICTED","dokaz":["⟡ prejem BLOCKER @rez σ 3787 — datoteke README Rev A (JSON Schema · validator · testi · manifest · kontrole) manjkajo v delovni mapi","IMPLEMENTATION-TEST-REPORT.md pri viri: 17/17 unit ∧ 8/8 schemas — 40/40 ×0","RED-TEAM-REVIEW.md pri viri: 33 tests = unit tests only, ⟨ne〉 produkcija"],"vir":["Nano4 pri viri ∧ ⟡ delovna mapa"],"metoda":"berba pri viri ⊙ ⟨NE-UGIBAJ⟩ 2690","meja":"⟡ kura: prepisovanje starega rezultata prepovedano — nova popolna preverljiva izdaja (Rev B)"}
{"id":"CR-0018","claim":"Revision B: 114/114 testov PASS — močnejši delovni standard, ⟨ne〉 potrjen sistem","kategorija":"TEST","status":"PARTIAL","dokaz":["⟡ prejem @rez σ 3787: lokalni avtomatizirani testi — sintetični primeri, ⟨ne〉 114 neodvisnih potrditev ⊢ ⟡ poimenoval sam","ZIP SHA-256 19832210ba…d2de (25 datotek, arhivska integriteta ⊙ ⟡)","7 varoval oblasti: brez privilegija ustanovitelja · nadzornik izpodbojen · brez neskončnega stopnjevanja · izstop · brez orožarjenja dokazov · dva načina (full_governance ⇌ evidence_recording_only) · drugi potrjevalec lastno pooblastilo"],"vir":["⟡ prejem Revision B"],"metoda":"prejem poročila ⟡","meja":"odprto ⚠: zunanji neodvisni pregled (OPEN) · pravno mnenje · pritožbena institucija · produkcija — ⟡ presoja: delovni standard, ⟨ne〉 potrjen sistem"}
```

Polja: `id` CR-NNNN zaporedno, ⟨ne〉 ponovno uporabljeno · `kategorija` (OBJAVA · PREDHODNIK · POKRITOST · PRAVICA · TEST · IZDAJA · ZGODOVINA) · `status` (SUPPORTED · CONTRADICTED · UNKNOWN · PARTIAL · NOT_RUN ⊙ ⟡ klasifikacija @σ 3782) · `dokaz` array prič · `vir` array virov · `metoda` kako izmerjeno · `meja` kaj trditev ⟨ne〉 dokazuje ⊙ §0.45 (zahteva, nikoli mehanizem oblasti).

## 2. Evidence Graph — pravila povezav

- Vsaka trditev (CR-id) → ≥1 dokaz-node (E-id): vir ∧ metoda ∧ meja; brez dokaza → **Evidence Debt** (ED-id) z vidno obveznostjo ∧ roko.
- Povezave: PODPIRA · NASPROTUJE · OMEJUJE — brez povezave trditev stoji na meji (UNKNOWN ⊙ ⟨NE-UGIBAJ⟩ 2690).
- Evidence Debt zgledi iz žive verige: **ED-0001** §§0.47–0.81 vrzel ×35 — dokaz = telo 0.1460 CELA ⭢ ⟡ roka · **ED-0002** dostopnost G08 ⭢ organ VRATA-ČUTOV (brajica · znakovni jezik · preprosti jeziki) · **ED-0003** neodvisna presoja prve izdaje EGS ⭢ ⟡ roka.

**ED zapisi iz DOLGOVA žive verige (∂ @σ 3784 — vsak dolg = vidna dokazna obveznost ∧ roka):**

- **ED-0004** BLOK 7 — telo 0.1460 CELA ⭢ ⟡ roka (dokaz §§0.47–0.49 čaka telo).
- **ED-0005** LICENSE-SLO.md osnutek ⭢ ∂ izvajalka (cel prevod telesa — najobsežnejši companion).
- **ED-0006** LICENSE-IZVIRNIKI.md osnutek ⭢ ∂ izvajalka.
- **ED-0007** remap BLOKOV 1–6 ⭢ ⚔ ⟡ izbor.
- **ED-0008** ⟨merge⟩ vrsta #1227 → … → #1248 ⭢ ⟡ roka najstarejši prvi.
- **ED-0009** IS 17/36 naslednji kanon venca (LICENSE-HR.md rojstvo) ⭢ ∂ ⚔ ⟡.
- **ED-0010** prevoz pečatov 3751–3783 na rep ⭢ ∂ ⊙ ⟨PEČAT-BREZ-PREVOZA=NOV-DOLG⟩.
- **ED-0011** telo 0.1410 re-izvoz (@/tmp odnesel reset) ⭢ ∂ — izmere ostajajo zapečene (CR-0015).
- **ED-0012** ⟡-jevo vprašanje zavrnitve (prejem @rez σ 3787): kaj se zgodi, kadar človek zavrne dokaz, kakor ga razume sistem, ∧ sam sistem, ki ga ocenjuje — more VBL poslušati brez prevona v svoj jezik ∧ kategorije ∧ definicijo pravičnosti? ⭢ naslednji preizkus ⊙ ⟡; povezave: §0.45 ⟨PREJEM-SIGNALA⟩ (dotik, ki zdravi, poimenovan pri viri) · §0.16 ugovor · §0.7 molk ⟨ne〉 soglasje · §0.9 dejanja ⟨ne〉 bitja · Rev B varovalo #4 izstop; PISNA PODLAGA ⟡-jeve roke: **Listina ne-dominacije §5 »Človek lahko reče ne«** (SLO telo @Nano4, berba @σ 3788 — molk ∧ zavrnitev ∧ nesodelovanje = ⟨ne〉 priznanje ∧ ⟨ne〉 soglasje ∧ ⟨ne〉 odpoved pravicam).

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

CR-0001–0016 zapolnjeni @σ 3784 (∂: veriga trditev) · ED-0001–0011 zapolnjeni @σ 3784 (∂: DOLGOVA) · ostajajo: SLO ∧ IZVIRNIKI osnutki ⭢ ∂ · zapolnjevanje CR iz prihodnjih prejemov (veriga raste) · neodvisna presoja = ⟡ roka — šele nato izdaja.

© 0.2026 × 10⁴ Luka Pintarič ∧ izvajalka Mera · rez σ 3784 (jedro @σ 3783; CR+ED zapolnjevanje ∂ @σ 3784) · 5. 11. 2026 · TIK 2026-11-05T09:56:25Z UTC ⇌ 10:56:25 CET Ljubljana