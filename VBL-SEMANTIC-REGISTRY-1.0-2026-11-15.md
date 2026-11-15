# VBL — SEMANTIC REGISTRY 1.0 — Register semantičnih pogodb pojmov

**Razred**: rojstvo telesa (kandidat) · **Status**: KANDIDAT ⭢ izbor ⟡ (⟨merge⟩ = ratifikacija P38) · **Izvršba**: P38 ⊙ ukaz ⟡ »stori« (15. 11. 2026, nedelja) ⊙ ⟨DVOJE-ROK⟩ 2432
**Dom pri rojstvu**: veja rez/5470-rojstva-artefaktov-presoje ⭢ kit OPEN ⭢ ⟨merge⟩ ⟡ = izbor
**MINT ⚠**: ⟨POGODBA-PRED-POMENOM⟩ ⚠ kompozit — dom ⚔ ⟡ ⊙ ⟨NE-UGIBAJ⟩ 2690
**©**: 0.2026 × 10⁴ Luka Pintarič ∧ izvajalka Mera · »a bare text proves nothing, the chain does« ⊢ §0.10 × 10² · measured, not asserted ⊙ §16

---

## §1 — NAMEN

Semantic Registry 1.0 je prvi od treh artefaktov neodvisne presoje (P38: MAGE 1.0 ⊢ živi pri viru · Semantic Registry 1.0 = TA telo · Adversarial Validation Suite 1.0 = sestrsko telo isti kit). Register daje vsakemu jedrnemu pojmu VBL **semantično pogodbo ×8 polj** ⊙ SIL §11 (pogodba ×8: TERM_ID · DEFINITION · TYPE · SCOPE · PRECONDITIONS · EVIDENCE_REQUIREMENTS · INFERENCE_LIMITS · CHANGE_RULE).

Zakon ⟨POGODBA-PRED-POMENOM⟩: pomen, ki nima pogodbe, je ugibanje; ugibanje je padec ⊙ ⟨NE-UGIBAJ⟩ 2690. Register ⟨ne⟩ spremeni pomenov — le izmeri ∧ zaveže priče ⊙ ⟨NE-RETIPKAJ⟩ 24.

## §2 — STRUKTURA VNOSA (pogodba ×8 ⊙ SIL §11)

| Polje | Nosilec |
|---|---|
| TERM_ID | enolično ime vnosa (SR-xx) |
| DEFINITION | definicija v eni povedi — preverljiva pri viru |
| TYPE | vrsta: dogodek ⊥ dokaz ⊥ presoja ⊥ odločitev ⊥ stanje ⊥ mehanizem |
| SCOPE | kje pojem vlada; zunaj obsega pojem ne velja |
| PRECONDITIONS | kaj mora biti izmerjeno, preden pojem smemo izreči |
| EVIDENCE_REQUIREMENTS | kateri dokazi nosijo vsako uporabo pojma |
| INFERENCE_LIMITS | katerih sklepov ta pojem NE nosi (meja sklepanja) |
| CHANGE_RULE | kako sme se pogodba spremeniti (⟨ne⟩ med uporabo) |

## §3 — REGISTER (SR-01 … SR-12)

**SR-01 VERIFIED_USE** (uporaba, ki jo nosi priča)
- DEFINITION: vsaka uporaba dela, ki ima izmerjeno pričo pri viru istega diha.
- TYPE: stanje uporabe.
- SCOPE: vsako branje, prevod, prevoz ∧ izvajanje telesa VBL.
- PRECONDITIONS: priča obstaja ∧ je berljiva ∧ je izmerjena istega diha.
- EVIDENCE_REQUIREMENTS: naslov priče ∧ datum ∧ izmera (bajti, vrstice, sha).
- INFERENCE_LIMITS: VERIFIED_USE ⟨ne⟩ dokazuje resničnost vsebine — samo izmerjenost uporabe ⊙ SchemaValid ≠ FactuallyTrue ⊙ standard T-09.
- CHANGE_RULE: sprememba samo z novim zapisom, stara ostane ⊙ ⟨NE-BRIŠI⟩ 24.

**SR-02 ABSENCE_CERTIFICATE** (izjava o odsotnosti)
- DEFINITION: izjava »X ne obstaja pri viru«, ki nosi ×14 polj izmere ⊙ standard (K-08 družina).
- TYPE: dokaz o odsotnosti.
- SCOPE: vsak »×0«, »ne najdem«, »odsotno« v poročilih registra.
- PRECONDITIONS: iskanje poimensko ∧ po vseh plasteh ∧ zabeležena metoda ⟨grep⟩.
- EVIDENCE_REQUIREMENTS: poizvedba ∧ njen izid ∧ čas ∧ orodje — ×14 polj polno.
- INFERENCE_LIMITS: odsotnost izmere ⟨ne⟩ je odsotnost pojma; molk ni soglasje ⊙ §0.7 × 10¹.
- CHANGE_RULE: vsak nov »×0« zapolni vsa polja, sicer je ⚠ ⟨ne⟩ ⊢.

**SR-03 HOLD** (odložitev)
- DEFINITION: stanje, v katerem odločitev čaka na izmero ali besedo ⟡; štiri polja: razlog · vir čakanja · rok · priča ⊙ K-08.
- TYPE: odločitev.
- SCOPE: register kontrol, presoje, izbori.
- PRECONDITIONS: razlog poimenovan; HOLD brez razloga je tiho čakanje = padec.
- EVIDENCE_REQUIREMENTS: štiri polja polna ∧ ura presoje izmerjena.
- INFERENCE_LIMITS: HOLD ⟨ne⟩ je zavrnitev; ⟨ne⟩ je potrditev; ⟨ne⟩ se šteje kot rezultat.
- CHANGE_RULE: zaprtje HOLD samo z izmero ali besedo ⟡, zapisano isto.

**SR-04 CLAIM** (trditev)
- DEFINITION: izjava, ki še ni izmerjena; nosi samo sebe.
- TYPE: presoja (neizmerjena).
- SCOPE: vsa poročila, standard, register.
- PRECONDITIONS: poimenovana kot trditev; nikoli prikazana kot izid.
- EVIDENCE_REQUIREMENTS: za prehod v ⊢ potrebuje izmero pri viru.
- INFERENCE_LIMITS: claim se NE sme prikazati kot izmerjen izid ali odločitev ⊙ T-12.
- CHANGE_RULE: claim postane ⊢ samo z izmero; brez nje ostane claim.

**SR-05 TEST_RESULT** (izid preizkusa)
- DEFINITION: izid izvedenega preizkusa, ločen od trditve ∧ od odločitve ⊙ standard §7.
- TYPE: dogodek.
- SCOPE: testovi standarda §12 (T-01 … T-34) ∧ vsak prihodnji.
- PRECONDITIONS: preizkus dejansko izveden; NOT_RUN je pošten izid.
- EVIDENCE_REQUIREMENTS: vhod · metoda · izid · ura · izvajalka.
- INFERENCE_LIMITS: izid testa ⟨ne⟩ je odločitev o dejanju; odločitev se piše ločeno.
- CHANGE_RULE: izid se ⟨ne⟩ spreminja; popravek = nov test, nova vrstica.

**SR-06 DECISION** (odločitev)
- DEFINITION: izbor med potmi, izrečen po izmeri, z avtorjem.
- TYPE: odločitev.
- SCOPE: vsa vrata, kiti, izbori ⚔.
- PRECONDITIONS: izmera obstaja ali pošteno manjka (⚠ poimenovan).
- EVIDENCE_REQUIREMENTS: vir izmere ∧ avtor ∧ ura.
- INFERENCE_LIMITS: odločitev razreda IZBOR ostaja ⟡ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690.
- CHANGE_RULE: sprememba odločitve = nova odločitev z novo pričo.

**SR-07 ACTION_TYPE** (vrsta dejanja)
- DEFINITION: poimenovana vrsta dejanja, ki zahteva izmerjen dogodek spremembe pred izvedbo ⊙ T-10 (namenov 4 · dejanj 8).
- TYPE: mehanizem.
- SCOPE: strojni register kontrol, učenje mašin, vsak zapis »izvedeno«.
- PRECONDITIONS: dogodek spremembe izmerjen; tiho nadaljevanje = ×0.
- EVIDENCE_REQUIREMENTS: namen · dejanje · dogodek · priča.
- INFERENCE_LIMITS: dejanje brez izmerjenega dogodka ni veljavno; ⟨ne⟩ ga popravi poznejša priča.
- CHANGE_RULE: nove vrste dejanj se rodijo poimenovano, ⟨ne⟩ tiho.

**SR-08 REASSESSMENT_REQUIRED** (obvezna ponovna presoja)
- DEFINITION: zastavica, da izmera ali odločitev zahteva ponovno presojo, ker se je vir premaknil ⊙ KOS-4.
- TYPE: stanje.
- SCOPE: vsaka izmera, ki se sklicuje na glavo, datoteko ∨ verigo.
- PRECONDITIONS: vir se je premaknil po izmeri (nova glava ⟨main⟩, nov komit).
- EVIDENCE_REQUIREMENTS: stara izmera ∧ nova izmera ∧ razlog.
- INFERENCE_LIMITS: zastavica ⟨ne⟩ razveljavlja stare izmere — le odpira okno ponovne presoje.
- CHANGE_RULE: zapre se z novo izmero ∧ zapisom istega diha.

**SR-09 RESIDUAL_INFLUENCE_UNKNOWN** (preostali vpliv neznan)
- DEFINITION: poštena izjava, da vpliv dejanja izven izmerjenega obsega ni znan ⊙ standard (K-19 družina).
- TYPE: stanje meje.
- SCOPE: vsak sklep, ki sega čez izmerjeno polje.
- PRECONDITIONS: izmerjen obseg poimenovan.
- EVIDENCE_REQUIREMENTS: kaj je izmerjeno ∧ kje meja stoji.
- INFERENCE_LIMITS: ⟨ne⟩ se sme uporabiti za izogib izmeri, ki je možna ⊙ ⟨NE-UGIBAJ⟩ 2690.
- CHANGE_RULE: nov izid izven obsega rodi novo izmero, ⟨ne⟩ brisanje zastavice.

**SR-10 EVENT ⊥ EVIDENCE ⊥ JUDGMENT ⊥ DECISION** (ločevalna četverica)
- DEFINITION: dogodek ⊥ dokaz ⊥ presoja ⊥ odločitev so štiri razredne entitete, ki se ⟨ne⟩ zlivajo ⊙ standard §8 ∧ T-11 (DOGODEK-atom 45, ZAPIS-atom 6).
- TYPE: mehanizem ločitve.
- SCOPE: celoten register, vsa poročila, vsi kiti.
- PRECONDITIONS: vsak zapis ve, v katerem razredu stoji.
- EVIDENCE_REQUIREMENTS: atom razreda zabeležen pri vsakem zapisu.
- INFERENCE_LIMITS: prenos pomena med razredi = kršitev; šteje se kot padec.
- CHANGE_RULE: četverica je trdna; nove entitete se rodijo poimensko.

**SR-11 INFERENCE_FIREWALL** (meja sklepanja)
- DEFINITION: sklep ne sme prečkati meje, ki jo nosijo dokazi; dolžina sklepa = dolžina verige dokazov ⊙ MAGE 1.0 (prioriteta 3: Inference Firewall).
- TYPE: mehanizem.
- SCOPE: vsak sklep v korpusu, vsak izvod registra.
- PRECONDITIONS: veriga dokazov izmerjena ∧ priče poimenske.
- EVIDENCE_REQUIREMENTS: sklep ⇌ priča 1:1; sklep brez priče je ⚠.
- INFERENCE_LIMITS: požarni zid sam je pogoj, ⟨ne⟩ izid — njegova kršitev se meri ločeno.
- CHANGE_RULE: meja se premakne samo z novo izmero dolžine.

**SR-12 ENFORCEABILITY_BOUNDARY** (meja izvršljivosti)
- DEFINITION: poštena karta, kje licenca izvršljivo ščiti ∧ kje zunanje pravo prevzame ⊙ standard (pravno stanje: ⟨ne⟩ obljublja pravnega nadzora, ki ga licenca sama ne more zagotoviti).
- TYPE: meja.
- SCOPE: TDM ∧ ZASP §57.a ∧ AI Act čl. 53 ∧ patenti ∧ znamke ∧ osebni podatki.
- PRECONDITIONS: vsak zahtevek pravic preverjen proti tej karti.
- EVIDENCE_REQUIREMENTS: vir prava ∧ člen ∧ ura berbe.
- INFERENCE_LIMITS: meja se ⟨ne⟩ razširja z besedami; ⟨ne⟩ izvršljivo = prepovedano trditi izvršljivost ⊙ VBL meje izvršljivosti.
- CHANGE_RULE: premik meje = novo telo plasti, ⟨ne⟩ amandma v tišini.

## §4 — ZEMLJEVID NA VERIGO D→I→C→A→R (Dokaz → razlaga → sklep → dejanje → posledica)

Vsak SR vnos se projicira na verigo ⊙ standard: SR-01/02/04/05 (D · I) → SR-03/06/10/11 (C) → SR-07/12 (A) → SR-08/09 (R). Projekt je karta, ⟨ne⟩ nova oblast: oblast nosi veriga pri viru ⊙ §0.10 × 10².

## §5 — STROJNA BERBA

Register je berljiv strojno: vsak vnos ×8 polj, imena polj nespremenljiva, vrstni red nespremenljiv; JSON zrcalo rodi se z izvedbo, ⟨ne⟩ pred njo ⊙ ⟨MANIFEST-EN-DIH-PO-ROJSTVU⟩. Status telesa: KANDIDAT — register vlada samo po ⟨merge⟩ ⟡ (ratifikacija P38).

## §6 — PRIMANJKLJAJI, KI JIH TA TELO ⟨NE⟩ REŠI

Samoregister ⟨ne⟩ je neodvisna presoja: samo-audit ostaja ⚠ (samopreizkus VBL 1.0: TEST_RESULT = NOT_RUN · DECISION = HOLD). Neodvisnost nosi druga roka nad tem registrom ⊙ standard §13.2 ∧ MAGE (priorita 1: Evidence Independence). To telo je instrument presoje, ⟨ne⟩ presoja sama.

---

*Status: KANDIDAT ⭢ izbor ⟡ — ⟨merge⟩ = ratifikacija P38 · rojeno @rez σ 5470, 15. 11. 2026 ⊙ ukaz ⟡ »stori« · © 0.2026 × 10⁴ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · measured, not asserted ⊙ §16.*
