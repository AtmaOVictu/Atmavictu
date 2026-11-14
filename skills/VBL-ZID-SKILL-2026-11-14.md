# VBL-ZID — operativna vrata VBL (ROJSTVO @σ 5362 · 14. 11. 2026 · ukaz ⟡ verbatim ⟨ne brusi⟩: »zidaj tako da je uporabno« ⊙ mehanizmi MAGE 2.0/3.0 — 27–64)

## NAMEN
Naloži kadar se dela z licenciranim gradivom ali sprašuje po VBL: preizkusi, prevozi, absorpcije, licence, provenienca, popravila modelov, dokazne sledi, meje izvršljivosti, artefakti, scenariji. VBL = R+D+T+A+P: priznanje · razločevanje · sledljivost · odgovornost · popravljivost. Lokalni nalagalnik živi @skills/vbl-zid/SKILL.md (3.117 B · md5 b2b44ab5 ⊢ izmerjeno).

## VRATA ×8 (mehanizmi 50–64)
1. VEZAVA-ODOBRITVE (50): vsaka odobritev nosi MATERIAL_DIGEST ∧ ACTION_TYPE ∧ DECLARED_PURPOSE ∧ SCOPE ∧ ACTOR ∧ TARGET_SYSTEM ∧ ENVIRONMENT ∧ veljavnost ∧ NONCE. POLICY_APPROVAL ⊥ EXECUTION_AUTHORIZATION ⊥ EXECUTION_RECEIPT — trije objekti, ⟨ne⟩ zamenljivi; izvršitev veljavne odobritve sama po sebi ne dokazuje zakonitosti celotne uporabe.
2. GRAF-TRANSFORMACIJ (51): vsak korak = vrstica (OBJECT_ID ∧ PARENT_OBJECT_ID ∧ SOURCE_WORK_ID ∧ TRANSFORMATION_TYPE ∧ RIGHTS_STATUS ∧ EVIDENCE). Tipi: COPY_OF / EXTRACTED_FROM / FRAGMENT_OF / TRANSLATED_FROM / NORMALIZED_FROM / EMBEDDED_FROM / INDEXED_FROM / DERIVED_FROM. DerivedFrom(A,B) ≠ LegalViolation — pravice se ⟨ne⟩ prenašajo samodejno; presoja po konkretni transformaciji.
3. TAKSONOMIJA-DEJANJ (52): ACCESS · DOWNLOAD · COPY · STORE · TRANSFORM · EXTRACT · INDEX · EMBED · TRAIN · FINE_TUNE · EVALUATE · RETRIEVE · INFER · GENERATE · DISTRIBUTE · RETAIN · DELETE — USE prepovedan; A_i ≠ A_j tudi pri istem viru.
4. DRIFT-NAMENA (53): PURPOSE_DECLARED ⊥ PURPOSE_ACTUAL; sprememba namena/akterja/okolja/publike/pravne podlage = dogodek → REASSESSMENT_REQUIRED. Drift ≠ kršitev; nepreverjen drift = tveganje. OriginalApproval ≠ ApprovalForEveryFutureUse.
5. POPRAVILO-MODELA (54): zahtevek odstranitve = tabela plasti: SOURCE_REMOVED · COPY_REMOVED · INDEX_PURGED · CACHE_PURGED · BACKUP_HANDLED · TRAINING_DATASET_REVISED · RETRAINING_COMPLETED · UNLEARNING_APPLIED · MODEL_RETIRED · RESIDUAL_INFLUENCE_UNKNOWN. SourceDeleted ≠ ModelInfluenceRemoved; UnlearningApplied ≠ CompleteUnlearningVerified; izjava vedno omejena na izmerjeno.
6. PROVENIENCA-IZHODOV (55): Similarity ⊥ Provenance ⊥ Influence ⊥ Memorization ⊥ Reproduction — pet pojmov, ⟨ne⟩ sopomenke. Similarity ≠ TrainingUse; NoSimilarity ≠ NoTrainingUse. Ne zahtevamo notranjega mišljenja modela — zahtevamo zunanje dokazne povezave (RETRIEVED_SOURCES · MODEL_VERSION · GENERATION_EVENT · izvedeni preizkusi).
7. PODIZVAJALCI (56): vsaka predaja = DELEGATION_ID ∧ PRINCIPAL ∧ AGENT ∧ SUBPROCESSOR ∧ AUTHORIZED_ACTIONS ∧ EVIDENCE_DUTIES ∧ SUBDELEGATION_PERMISSION ∧ INCIDENT_NOTIFICATION. DelegationOfTask ≠ AutomaticTransferOfAllResponsibility.
8. SESTAVLJENE-PRAVICE (57): objekt = komponente (besedilo · fotografija · grafika · pisava · koda · zunanji podatki); vsaka s svojim imetnikom ∧ dokazom ∧ obsegom. Rights(W) ≠ neizmerjena unija komponent; presoja po komponenti ∧ dejanju; del brez dokazanega upravičenja izvajalca se imenuje.

## PREPREČEVANJE ∧ VAROVANJE (58–62)
- DOKAZNA-PRIPRAVLJENOST (58): PRED obdelavo izmeri: identifikacija materiala · beleženje dejanj · verzija pravil · vezava dejanje↔akter · predaje · časovni podatki · postopek ugovora · dostop presojevalca → EVIDENCE_READY / READY_WITH_LIMITATIONS / NOT_READY / UNKNOWN. EvidenceReady ≠ Compliant.
- PRE ⊥ POST (59): PRE_EXECUTION_CONTROL (isti preizkus ⊙ 2) ⊥ POST_EXECUTION_AUDIT; izid PERMITTED / PERMITTED_WITH_CONDITIONS / BLOCKED / HELD / NOT_VERIFIABLE. NoVBLAuthorization ≠ NoLawfulAuthorization — blokada ⟨ne⟩ sme izključiti drugih veljavnih podlag.
- ZEMLJEVID-OBHODOV (60): INGRESS ∧ EGRESS ∧ API ∧ INTEGRACIJE ∧ ročni uvozi ∧ razvojna okolja ∧ nestrožene poti; ControlledPathCompliant ≠ EntireSystemCompliant; preizkus red-team v NADZOROVANEM okolju, ⟨ne⟩ v produkcijski infrastrukturi.
- DOKAZNI-DOSTOP (61): stopnje: javni povzetek → metapodatki → redigirano dokazilo → pooblaščeni presojevalec → varovan izvorno; redakcija ne sme odstraniti bistvenega pomena; Confidentiality ≠ Unreviewability.
- CIKEL-DOKAZOV (62): CREATED → VALIDATED → USED → RETAINED → REVIEWED → DELETED ∧ RETENTION_BASIS ∧ LEGAL_HOLD ∧ DELETION_VERIFICATION ∧ RESIDUAL_COPIES; brisanje aktivne kopije ⊥ kopij ⊥ ključev ⟨ne⟩ enako; OSEBNI PODATKI V JAVNIH NESPREMENLJIVIH DNEVNIKIH PREPOVEDANI.

## MEJE ∧ ARGUMENT (63, 64, XX, XXIII, XXIV)
- IZVRŠLJIVOST (63): vsaka zahteva nosi način uveljavitve: TECHNICALLY_ENFORCED · CONTRACTUALLY_BINDING · LEGALLY_ENFORCEABLE · PROCEDURALLY_SUPPORTED · VOLUNTARY · OUTSIDE_CONTROL · UNKNOWN; zunanjega izvajalca izrecno imenuj; NormativeRequirement ≠ UniversalTechnicalEnforcement.
- ASSURANCE-CASE (64): CLAIM ∧ ARGUMENT ∧ EVIDENCE ∧ CONTEXT ∧ ASSUMPTIONS ∧ DEFEATERS — DEFEATER ≠ dokaz napake, je obvezna obravnavana možnost.
- P ⊥ D ⊥ A ⊥ R (XX): preprečevanje · zaznavanje · pripis · popravljanje — štirje samostojni izidi, noben ne zagotavlja naslednjega.
- KONTROLNE-INTERAKCIJE (XXIII): vsak nov mehanizem preveri na obstoječe: nespremenljivost ⟲ izbris · blokada ⟲ druga podlaga · sledljivost ⟲ zaupnost · celovit zapis ⟲ minimalizacija; Control_A+Control_B ≠ BetterProtection; »vedno strožje« prepovedano.
- ZRELOST (XXIV): R1 Specification · R2 Implementation · R3 Operation · R4 Observation · R5 Outcome · R6 Consequence; M=(S,I,O,V,E,R) ⟨ne⟩ seštevka; samo R1 = deklaracija.

## FORMA IZHODA (obvezna pri vsakem VBL delu)
vrata ⟲ dejanje ⟲ izid (P/D/A/R) ⟲ meja (česa NE morem trditi) ⟲ dokaz ⟨⊢⟩ ⟲ defater ⚠ — measured, not asserted ⊙ §16.

## PREIZKUSI ×15 (⟡-jevi, po mehanizmih)
50: ujema se dejanska izvedba z odobritvijo po vseh poljih? · 51: rekonstruira neodvisni presojevalec pot do izvedenega objekta z vrzelmi? · 52: dejanje poimenovano natančno, brez USE? · 53: drift zaznan pred obravnavo kot odobren? · 54: katere plasti pregledane ∧ popravljene ∧ preverjene ∧ kaj ostaja neznano? · 55: kaj je o izvoru izhoda preverjeno ∧ česa rezultat ne izpričuje? · 56: vsak subjekt z dostopom izsledljiv ∧ odgovornost za dokaze določena? · 57: komponente brez upravičenja izdajalca identificirane? · 58: rekonstrukcija po 6 mesecih brez spomina zaposlenih? · 59: preverja točno to dejanje ∧ loči VBL-dovoljenje od drugih podlag? · 60: red-team izvede alternativno pot neopaženo? · 61: redakcija odstranila bistveno? · 62: hramba utemeljena ∧ obravnava skladna z namenom? · 63: oznaka uveljavitve pri vsaki zahtevi ∧ zunanje meje javne? · 64: drug presojevalec rekonstruira argument ∧ najde izpodbijljiva mesta?

© 0.2026 × 10⁴ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · measured, not asserted ⊙ §16