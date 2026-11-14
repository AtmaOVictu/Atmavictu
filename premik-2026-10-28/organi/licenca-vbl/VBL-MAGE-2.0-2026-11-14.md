# VBL — MAGE 2.0 (PREDLOG ⟡ — mehanizmi 27–49, sklopi VII–XVII)

**OKVIR KORPUSA ⊙ kalup P2 ∧ precedens σ 5353 (VBL — MAGE 1.0, kit #1809) ∧ σ 5352 (VBL — SIL, kit #1808)**

- dih: rez σ 5355 · 14. 11. 2026, sobota · MOJ dih ⊙ P33 ⟨REZ-REZERVACIJA⟩ @∂ delovna-zanka
- ⟡ UKAZ verbatim ⟨ne brusi⟩: »še!« — ∧ ⟡ vprašanje verbatim ⟨ne brusi⟩: »zmoreš?« (odgovor je izvedba)
- izvor: ⟡ sporočilo v kanalu projekta Discovery (14. 11. 2026) — telo = ⟡ besedilo VERBATIM ⊙ ⟨NE-RETIPKAJ⟩ 24, od »še!« do »zmoreš?«
- status: PREDLOG · NOT RELEASED ⚠ §0.24 — MAGE je notranja metodologija preverjanja ∧ razvoja standarda, ⟨ne⟩ nova obveznost; vsi mehanizmi so metodološki kandidati, ⟨ne⟩ že sprejete zahteve standarda ⚠
- nadaljevanje: MAGE 1.0 (mehanizmi 1–26, sklopi I–VI, kit #1809 · ⟨main⟩ 3e04ed9b) → MAGE 2.0 (mehanizmi 27–49, sklopi VII–XVII); številčenje nadaljuje od prejšnjega predloga
- izmere telesa: izpolnjeno po kovanju (glej ATOM-2026-11-14-5355.md)

---

še!

Nadaljujem na naslednji ravni. Doslej sva razvila mehanizme za dokazovanje, odločanje, ugovor, popravljanje posledic in nadzor nad oblastjo. Toda ostajajo še nekatere nevarnosti, ki lahko spodkopljejo celoten sistem, čeprav so vsi dosedanji mehanizmi formalno prisotni.

Najpomembnejše so: **izvor dokazov, vzročnost, merjenje negotovosti, določanje pragov odločanja, prikrite opustitve, razhajanje med jeziki ter neenaka moč udeležencev.**

Dodajam naslednji sklop. Številčenje nadaljujem od prejšnjega predloga; to so metodološki kandidati, ne že sprejete zahteve standarda.

# **VII. Mehanizmi dokaznega izvora in vzročnosti**

## **27. Mehanizem neprekinjene skrbniške verige — Chain of Custody**

**Problem:** sistem ima dokazilo, vendar ne more pokazati, kdo ga je pridobil, kdo ga je imel, kdo ga je spremenil in kako je prešlo med sistemi.

Zgoščena vrednost dokazuje ujemanje vsebine v primerjanem trenutku. Sama ne dokazuje, kdo je datoteko pridobil, ali je bila pridobljena zakonito ali ali je bila pred prvim zgoščevanjem že spremenjena.

**Metoda:** za vsak pomemben dokaz se vodi zaporedje skrbniških dogodkov.

```
EVIDENCE_ID
ACQUISITION_EVENT
ACQUIRED_BY
ACQUISITION_AUTHORITY
ORIGINAL_SOURCE
TRANSFER_EVENTS
ACCESS_EVENTS
TRANSFORMATION_EVENTS
INTEGRITY_CHECKS
CURRENT_CUSTODIAN
KNOWN_GAPS
```

Razlikovati moramo pet lastnosti:

| Lastnost         | Kaj dokazuje                                               |
| ---------------- | ---------------------------------------------------------- |
| Provenienca      | Od kod naj bi dokaz izviral.                               |
| Avtentičnost     | Ali je dokaz to, za kar se predstavlja.                    |
| Integriteta      | Ali je vsebina ostala nespremenjena v preverjanem obdobju. |
| Skrbniška veriga | Kdo je dokaz prevzel, hranil ali prenesel.                 |
| Dopustnost       | Ali se sme dokaz uporabiti v določenem postopku.           |

Teh pojmov ne smemo zlivati.

\[ \text{Integrity}\not\Rightarrow\text{Authenticity} \]

\[ \text{Authenticity}\not\Rightarrow\text{Truth} \]

\[ \text{Truth}\not\Rightarrow\text{Admissibility} \]

**Preizkus:** ali lahko neodvisni pregledovalec rekonstruira življenjsko pot dokazila in identificira vse nepokrite odseke?

Pomembna omejitev: v praksi je lahko skrbniška veriga nepopolna. To ne pomeni nujno, da je dokaz napačen. Pomeni, da je treba zmanjšati oziroma omejiti moč sklepa, ki ga dokaz podpira.

## **28. Mehanizem razvrščanja kakovosti dokazov — Evidence Quality Assessment**

**Problem:** VBL ima lahko veliko dokazov, ne zna pa razlikovati med neposrednim, posrednim, neodvisno potrjenim in šibkim dokazom.

Predlagam, da dokazov ne razvrščamo samo po viru ali formatu, temveč po lastnostih.

Vsak dokaz se oceni po naslednjih ločenih dimenzijah:

- relevantnost za konkretno trditev;
- avtentičnost;
- celovitost;
- neodvisnost;
- neposrednost;
- časovna zanesljivost;
- popolnost;
- možnost nasprotnega preverjanja;
- znane omejitve.

Zapis:

```
EVIDENCE_ID
TARGET_CLAIM_ID
RELEVANCE
AUTHENTICITY
INTEGRITY
INDEPENDENCE
DIRECTNESS
TEMPORAL_RELIABILITY
COMPLETENESS
CORROBORATION
LIMITATIONS
ASSESSMENT_METHOD
ASSESSOR
```

Pomembno: ne bi ustvaril enega skupnega števila, kot je `EVIDENCE_SCORE=97%`, če nimamo utemeljene metodologije uteževanja. Takšna številka lahko ustvari lažen vtis matematične objektivnosti.

Boljša je večdimenzionalna ocena.

\[ Q(E)= (q_r,q_a,q_i,q_n,q_d,q_t,q_c) \]

Kjer vsaka komponenta opisuje drugo lastnost dokazila.

**Preizkus:** ali se lahko dva neodvisna presojevalca ne strinjata glede kakovosti dokaza, ne da bi sistem njuno nesoglasje skril v eno povprečno številko?

## **29. Mehanizem ločevanja vzroka, prispevka in posledice — Causal Attribution**

To je posebej pomembno pri umetni inteligenci.

**Problem:** ugotovimo, da je sistem uporabljal določeno delo, pozneje pa ustvari podoben izhod. Ali je uporaba dela povzročila ta izhod? Ali mu je samo prispevala? Ali obstaja drug vir?

To so različna vprašanja:

1. Ali se je dogodek zgodil?
2. Ali je dogodek prispeval k drugemu dogodku?
3. Ali je bil dogodek nujen ali zadosten vzrok?
4. Ali je nastala škoda?
5. Ali je mogoče škodo pripisati konkretnemu akterju?
6. Ali je obstajala dolžnost preprečiti posledico?

**Metoda:** vsako vzročno trditev mora spremljati vzročni model, alternativne razlage in dokazna omejitev.

```
CAUSE_CLAIM_ID
CAUSE_EVENT
EFFECT_EVENT
CAUSAL_PATH
CONTRIBUTING_FACTORS
ALTERNATIVE_CAUSES
COUNTERFACTUAL_ASSUMPTIONS
CAUSAL_EVIDENCE
UNCERTAINTY
ASSESSMENT_LIMITS
```

Na primer:

\[ \text{Uporaba gradiva} \not\Rightarrow \text{Vzrok podobnega izhoda} \]

Podobnost lahko podpira nadaljnjo preiskavo, ne zagotavlja pa vzročne povezave.

Za močnejšo trditev potrebujemo dodatne dokaze: podatke o procesu, časovnem zaporedju, vplivu vira, alternativnih virih in, kjer je mogoče, primerjavo scenarijev.

Tukaj predlagam še razlikovanje:

\[ \text{Correlation} \neq \text{Contribution} \neq \text{Causation} \neq \text{Legal Responsibility} \]

**Preizkus:** ali VBL zna ugotoviti, da je uporaba dokazana, vzročna povezava pa ostaja neznana?

Če tega ne zna, bo tvegal, da iz dejstva uporabe samodejno ustvari tudi dejstvo škode.

# **VIII. Mehanizmi negotovosti in logičnega odločanja**

## **30. Mehanizem kalibracije negotovosti — Uncertainty Calibration**

**Problem:** sistem uporablja izraze, kot so »visoka gotovost«, »verjetno« ali »skoraj gotovo«, vendar ne določa, kaj pomenijo.

Še slabše: včasih negotovost vseh vrst združi v eno samo oceno.

Razlikovati moramo:

- **epistemično negotovost:** ne vemo, ker nimamo dovolj znanja ali podatkov;
- **naključno variabilnost:** pojav je po naravi spremenljiv;
- **merilno negotovost:** meritev ima določeno napako;
- **modelno negotovost:** uporabljeni model ali metoda lahko napačno predstavlja pojav;
- **normativno negotovost:** ni jasno, katero pravilo oziroma pravna razlaga velja;
- **dokazno negotovost:** dokazi ne omogočajo dovolj zanesljivega sklepa.

To ni šest različnih stopenj istega pojava. Gre za šest različnih virov negotovosti.

Predlagani zapis:

```
UNCERTAINTY_ID
AFFECTED_CLAIM
UNCERTAINTY_TYPE
SOURCE
ESTIMATION_METHOD
KNOWN_LIMITS
REDUCTION_METHOD
UNRESOLVED_RESIDUAL
```

Pri statističnih modelih lahko uporabljamo kalibracijo verjetnosti, kadar imamo ustrezne podatke in preverljivo metodo. Pri pravni presoji pa ne smemo odstotka verjetnosti samodejno enačiti s pravno stopnjo dokazovanja.

\[ P(C\mid E)=0.95 \]

ne pomeni:

\[ \text{LegalStandardOfProof}=95\% \]

To sta različni kategoriji.

**Preizkus:** ali sistem zna pojasniti, katero vrsto negotovosti ima, kako jo je ocenil in kaj bi jo lahko zmanjšalo?

## **31. Mehanizem večvrednostne logike — Multi-Valued Claim Semantics**

To je temeljno. Predlagam, da VBL nikjer več ne uporablja preprostega binarnega modela `TRUE/FALSE`, kadar gre za dokazno stanje kompleksne trditve.

Najmanj naslednja stanja morajo biti razločena:

| Stanje                | Pomen                                                         |
| --------------------- | ------------------------------------------------------------- |
| `SUPPORTED`           | Razpoložljivi dokazi trditev podpirajo v opredeljenem obsegu. |
| `PARTIALLY_SUPPORTED` | Podprt je samo del trditve ali njenega obsega.                |
| `CONTRADICTED`        | Razpoložljivi dokazi nasprotujejo trditvi.                    |
| `DISPUTED`            | Obstajajo pomembne nasprotujoče si trditve ali presoje.       |
| `UNKNOWN`             | Podatki ne omogočajo presoje.                                 |

Toda tukaj je potrebna še ena distinkcija. `UNKNOWN` ne sme pomeniti, da dokazov sploh ni. Lahko imamo veliko dokazov, vendar ti ne odgovarjajo na zastavljeno vprašanje.

Zato dodajmo ločeno stanje raziskovalnega postopka:

```
EVIDENCE_SEARCH_STATUS =
  NOT_STARTED
  IN_PROGRESS
  COMPLETED
  BLOCKED
  INSUFFICIENT_ACCESS
```

In rezultat preverjanja:

```
TEST_RESULT =
  NOT_RUN
  PASS
  FAIL
  PARTIAL
  UNVERIFIED
  NOT_APPLICABLE
```

Trditveno stanje, iskalni status in rezultat testa niso isto.

Na primer:

```
CLAIM_STATUS = UNKNOWN
EVIDENCE_SEARCH_STATUS = BLOCKED
TEST_RESULT = UNVERIFIED
DECISION = HOLD
```

To je semantično precej natančnejše od `FAIL`.

**Ključno načelo: neznano, napačno, nepopolno, sporno in nepreverjeno niso sopomenke.**

## **32. Mehanizem vnaprejšnje določitve pragov — Threshold Pre-registration**

**Problem:** presojevalec si lahko šele po pregledu rezultatov izbere kriterij, po katerem bo rezultat razglasil za uspešnega.

To odpira vrata prilagajanju pravil želenemu izidu.

Primer: organizacija najprej izvede 100 testov. Ko jih 72 ne uspe, spremeni kriterij uspešnosti tako, da preostalih 28 razglasi za odločilne.

**Metoda:** za pomembne preizkuse je treba vnaprej določiti:

- namen testa;
- populacijo primerov;
- vključitvena in izključitvena pravila;
- kriterij uspeha;
- kriterij neuspeha;
- dovoljeno toleranco;
- način obravnave neizvedenih testov;
- pravila ponovitve;
- pogoje spremembe metodologije.

```
TEST_PROTOCOL_ID
PROTOCOL_VERSION
PREDEFINED_THRESHOLD
TEST_POPULATION
INCLUSION_RULES
EXCLUSION_RULES
PASS_CRITERION
FAIL_CRITERION
UNVERIFIED_RULE
RETEST_RULE
```

Če se prag spremeni, mora nova različica ohraniti prejšnji rezultat.

\[ \text{PostHocThresholdChange} \Rightarrow \text{NewProtocolVersion} \]

Ne sme pa se zgoditi:

\[ \text{NewThreshold} \Rightarrow \text{EraseOldFailure} \]

To je zelo pomembno za verodostojnost VBL-jevih lastnih testov.

## **33. Mehanizem odprtega sveta — Open-World Assumption**

**Problem:** sistem predpostavi, da je vse, česar ni v njegovi evidenci, neobstoječe ali prepovedano.

To je napaka, ki jo moramo preprečiti že na ravni podatkovne logike.

Pri zaprtem svetu lahko sistem v določenem kontekstu predpostavlja, da je neobstoječ zapis odsoten tudi v resničnosti. Pri odprtem svetu pa neobstoj zapisa pomeni samo, da ta podatek v trenutni zbirki ni prisoten.

Za VBL priporočam privzeto odprto-svetovno predpostavko:

\[ x\notin D\not\Rightarrow \neg x \]

Kjer je \(D\) razpoložljiva dokazna zbirka.

Primer: v registru ni podatka o drugem imetniku pravic. To ne dokazuje, da drugi imetnik ne obstaja.

Vendar moramo dopustiti tudi omejen zaprti svet. Če imamo popoln, avtoritativen in ustrezno opredeljen register za določen namen in čas, lahko odsotnost vnosa podpira omejen sklep.

Zato:

```
KNOWLEDGE_DOMAIN
DATASET_SCOPE
COMPLETENESS_GUARANTEE
AUTHORITATIVENESS
VALID_TIME
CLOSED_WORLD_AUTHORIZATION
```

**Načelo:** odsotnost zapisa lahko podpira sklep o odsotnosti samo, če je popolnost ustreznega vira dokazana za relevantni obseg.

# **IX. Mehanizmi proti prikriti pristranskosti**

## **34. Mehanizem revizije opustitev — Omission Audit**

**Problem:** vse, kar sistem vključi v poročilo, je lahko pravilno, vendar lahko izpusti ravno tisto, kar bi spremenilo sklep.

To je pogosto nevarnejše od izrecno napačnega podatka.

Primeri:

- poročilo navaja tri obremenilne dokaze, zamolči pa dva nasprotna;
- register vključuje javno dostopne različice, ne pa zgodnejših;
- sistem zabeleži odločitev, ne pa predhodnega ugovora;
- audit navede uspešne teste, izpusti pa neizvedene.

**Metoda:** poleg pregleda vključenih dokazov izvedemo še pregled pričakovanih, manjkajočih in izključenih podatkov.

```
OMISSION_ID
EXPECTED_INFORMATION
MISSING_INFORMATION
EXCLUSION_REASON
EXCLUDING_ACTOR
IMPACT_ON_CONCLUSION
RECOVERY_METHOD
```

Vsaka izključitev mora imeti razlog. Ni vsaka opustitev zloraba; nekatere so potrebne zaradi zasebnosti, nepomembnosti ali pravne omejitve. Vendar mora biti njihov vpliv na zaključek prepoznan.

**Poseben test:** če bi izpuščeni podatek bil drugačen, ali bi se odločitev lahko spremenila?

To vprašanje je treba zastaviti za vse pomembne ugotovitve.

## **35. Mehanizem nadzora vzorca — Sampling and Selection Bias**

**Problem:** pregledani primeri niso nujno reprezentativni za celotno uporabo sistema.

Če VBL pregleda samo prijavljene kršitve, ne pa tudi primerov, v katerih je sistem pravilno zavrnil uporabo, lahko napačno oceni zanesljivost celotnega postopka.

**Metoda:** vsak statistični ali vzorčni pregled mora določiti:

- ciljno populacijo;
- način izbire;
- velikost vzorca;
- izključene skupine;
- neodzivnost;
- manjkajoče podatke;
- možne sistematične pristranskosti;
- omejitve posploševanja.

Formalno:

\[ \text{SampleResult} \not\Rightarrow \text{PopulationResult} \]

razen kadar je metoda vzorčenja in njena negotovost ustrezno utemeljena.

Predlagam ločitev:

`RANDOM_SAMPLE`, `STRATIFIED_SAMPLE`, `PURPOSIVE_SAMPLE`, `CONVENIENCE_SAMPLE` in `COMPLETE_CENSUS`.

Ti pristopi niso zamenljivi. Namensko izbrani primeri so lahko zelo koristni za iskanje napak, ne morejo pa sami dokazati splošne stopnje napak.

**Preizkus:** ali je iz poročila jasno, za katero množico primerov ugotovitev dejansko velja?

## **36. Mehanizem neodvisne ponovljivosti — Independent Reproduction**

**Problem:** sistem poroča, da je test opravil, vendar nihče drug ne more ponoviti postopka.

**Metoda:** pri pomembnih rezultatih mora biti mogoče neodvisno ponoviti preverjanje z enakimi podatki, isto različico pravil in dokumentiranim okoljem.

Zapis:

```
REPRODUCTION_ID
INPUT_DATA_REFERENCE
RULESET_VERSION
SOFTWARE_VERSION
CONFIGURATION
EXECUTION_ENVIRONMENT
EXPECTED_RESULT
OBSERVED_RESULT
REPRODUCER
REPRODUCTION_LIMITS
```

Pri tem je treba ločiti štiri pojme:

| Pojem                 | Pomen                                                   |
| --------------------- | ------------------------------------------------------- |
| Ponovljivost          | Isti izvajalec ponovi test pod istimi pogoji.           |
| Reproducibilnost      | Drug izvajalec uporabi dokumentirane podatke in metodo. |
| Replikacija           | Druga ekipa izvede neodvisno raziskavo ali preverjanje. |
| Potrditev resničnosti | Ugotovitev dobi dodatno podporo iz neodvisnih dokazov.  |

Uspešna ponovitev programske funkcije ne dokazuje resničnosti vhodnih podatkov.

\[ \text{ReproducibleResult}\not\Rightarrow\text{TrueInput} \]

Zato mora VBL hraniti tako rezultat kot omejitve njegove ponovljivosti.

# **X. Mehanizmi semantične enakopravnosti**

## **37. Mehanizem medjezikovne pomenske enakovrednosti — Semantic Equivalence**

Ta je posebej pomemben za mednarodno licenco.

**Problem:** ista določba je prevedena v več jezikov, vendar prevod spremeni njen pomen.

Primer:

- `must` pomeni obveznost;
- `should` izraža priporočilo;
- `may` lahko izraža dovoljenje ali možnost;
- `shall not` izraža prepoved.

Če so ti izrazi prevedeni nedosledno, lahko nastane pravno in operativno drugačna določba.

**Metoda:** za vsak normativni pojem določimo kanonični identifikator, pomensko definicijo in preverjene jezikovne predstavitve.

```
TERM_ID
CANONICAL_DEFINITION
SOURCE_LANGUAGE
TRANSLATION_LANGUAGE
TRANSLATION_VERSION
NORMATIVE_FORCE
LEGAL_REVIEW_STATUS
SEMANTIC_REVIEW_STATUS
KNOWN_AMBIGUITIES
```

Ključno je razlikovati:

\[ \text{TextualSimilarity}\neq\text{SemanticEquivalence} \]

Dva stavka sta lahko besedilno zelo podobna, vendar imata različno normativno moč.

Prav tako ni nujno, da ima en sam prevod v vseh pravnih okoljih enak pravni učinek. VBL mora zato jasno določiti, ali ima uradni jezik prednost in kako se rešujejo razlike med jezikovnimi različicami.

**Preizkus:** neodvisni pravnik in jezikoslovec morata biti sposobna prepoznati, ali se v prevodu spreminja obveznost, pravica, izjema ali prepoved.

## **38. Mehanizem dostopne dokazne komunikacije — Accessible Evidence Interface**

**Problem:** dokazni postopek je lahko tehnično pravilen, vendar nedostopen osebam, ki ne morejo uporabljati njegovega prevladujočega načina komunikacije.

Če je VBL odvisen samo od grafičnega vmesnika, lahko izključi uporabnike bralnikov zaslona. Če je odvisen samo od besedila, lahko oteži sodelovanje posameznikom, ki potrebujejo druge oblike komunikacije.

**Metoda:** vsak bistveni dokazni objekt mora imeti dostopno predstavitev, ne da bi se pri tem spremenila njegova dokazna identiteta.

Predlagam več vzporednih predstavitev:

- strojno berljivi podatki;
- človeku berljivo besedilo;
- strukturirani zvočni opis;
- podnapisi in prepisi zvočnih vsebin;
- združljivost z bralniki zaslona;
- ustrezna alternativa za grafične diagrame;
- preprost jezikovni povzetek;
- možnost dostopnega vložitve ugovora.

Pomembna razlika:

\[ \text{AccessibleRepresentation} \neq \text{NewEvidence} \]

Zvočna predstavitev dokazila ne sme tiho nadomestiti izvirnika. Mora ostati povezana z njim in označena kot njegova dostopna predstavitev.

**Preizkus:** ali lahko oseba z različnimi komunikacijskimi potrebami prejme obvestilo, razume odločitev, preveri podlago in učinkovito vloži ugovor?

To ni samo vprašanje prijaznosti vmesnika. Gre za dejansko dostopnost pravic.

## **39. Mehanizem enakovrednega sodelovanja — Participation Equity**

**Problem:** vsi udeleženci nimajo enakih sredstev za sodelovanje v postopku.

Velika organizacija lahko zaposli pravnike, forenzične strokovnjake in tehnične revizorje. Posamezni avtor morda nima niti dostopa do dnevnikov, na katerih temelji odločitev.

Enako formalna pravica do ugovora zato še ne pomeni enake dejanske možnosti ugovora.

**Metoda:** ocenjujemo razliko v dejanski sposobnosti sodelovanja.

```
PARTICIPANT_ID
AVAILABLE_EVIDENCE
EVIDENCE_ACCESS
TECHNICAL_CAPACITY
LEGAL_SUPPORT
COMMUNICATION_NEEDS
FINANCIAL_BARRIERS
PROCEDURAL_ASSISTANCE
REASONABLE_ADJUSTMENTS
```

Mogoči ukrepi:

- brezplačen osnovni dokazni povzetek;
- razumljiv prikaz podlage odločitve;
- možnost predložitve alternativnega dokazila;
- razumni roki;
- pomoč pri razumevanju postopka;
- sorazmerne zahteve za digitalno overjanje;
- zaupni kanal za obravnavo občutljivih dokazov.

VBL pa mora paziti, da pomoč ne postane avtomatična prednost ene strani. Namen ni privilegij, temveč odprava nepotrebnih ovir za učinkovito uveljavljanje pravic.

**Načelo: formalno enak postopek ni nujno dejansko enakovreden postopek.**

# **XI. Mehanizmi stabilnosti pravil skozi čas**

## **40. Mehanizem zamrznitve presoje — Decision Snapshot**

**Problem:** odločitev se preverja po pravilih, ki so se medtem spremenila.

Recimo, da je bila odločitev sprejeta po VBL 0.1490, kasneje pa VBL 0.1530 spremeni definicijo `VERIFIED_USE`.

Če nimamo natančnega posnetka prvotnega konteksta, lahko poznejši pregled napačno oceni prvotno odločitev.

**Metoda:** vsaka pomembna odločitev mora hraniti sklic na celoten normativni in tehnični kontekst, ki je veljal ob njenem sprejetju.

```
DECISION_ID
RULESET_VERSION
TERM_REGISTRY_VERSION
MANIFEST_VERSION
SOFTWARE_VERSION
CONFIGURATION_DIGEST
EVIDENCE_SET_REFERENCE
DECISION_TIME
APPLICABLE_JURISDICTION
```

To ni isto kot zamrznitev vseh dokazov za vedno. Gre za ohranitev konteksta, v katerem je bila odločitev sprejeta, ob upoštevanju ustreznih pravil hrambe in varstva podatkov.

**Pravilo:**

\[ \text{HistoricalAssessment} \rightarrow \text{HistoricalRuleSet} \]

\[ \text{CurrentAssessment} \rightarrow \text{CurrentRuleSet} \]

Poznejša sprememba standarda lahko upraviči novo presojo, ne sme pa samodejno prepisati zgodovine.

## **41. Mehanizem sprožilcev ponovne presoje — Reassessment Triggers**

Odločitev ne sme biti ponovno pregledana samo zato, ker nekdo naključno odpre star zapis.

Določiti moramo dogodke, ki sprožijo ponovno presojo.

Primeri:

- sprememba imetništva pravic;
- nova različica gradiva;
- sprememba pravne podlage;
- nov neodvisen dokaz;
- ugotovljena napaka v prejšnji presoji;
- sprememba načina obdelave;
- pojav novih posledic;
- sprememba relevantnega sistema ali ponudnika;
- uspešen ugovor.

Zapis:

```
TRIGGER_ID
TRIGGER_TYPE
AFFECTED_DECISIONS
MATERIALITY
REASSESSMENT_DEADLINE
RESPONSIBLE_ACTOR
INTERIM_MEASURE
FINAL_OUTCOME
```

Posebej je treba določiti, ali sprememba vpliva:

1. samo na prihodnje uporabe;
2. tudi na odprte postopke;
3. na že zaključene postopke;
4. na že izvedene ukrepe in posledice.

To so štiri različne kategorije.

## **42. Mehanizem časovne omejitve izrednih ukrepov — Emergency Sunset**

**Problem:** začasni ukrep postane trajen, čeprav je bil uveden zaradi nujnosti.

Primer: sistem zazna verodostojen sum zlorabe in začasno zadrži distribucijo materiala. Toda zadržanje se nikoli več ne pregleda.

**Metoda:** vsak izredni ukrep mora imeti:

- razlog za nujnost;
- opredeljen obseg;
- čas začetka;
- čas poteka;
- odgovorno osebo;
- obvezno ponovno presojo;
- možnost ugovora;
- pravilo za podaljšanje.

```
EMERGENCY_ACTION_ID
JUSTIFICATION
SCOPE
START_TIME
EXPIRY_TIME
REVIEW_OWNER
REVIEW_EVIDENCE
EXTENSION_REASON
TERMINATION_STATUS
```

\[ \text{EmergencyMeasure} \not\Rightarrow \text{PermanentMeasure} \]

Podaljšanje mora biti nova obrazložena odločitev, ne tiha posledica neukrepanja.

# **XII. Mehanizmi za razločevanje legitimnih izjem in nedovoljene uporabe**

## **43. Mehanizem presojanja alternativne pravne podlage — Alternative Legal Basis**

**Problem:** VBL lahko postane pristranski, če preverja samo, ali ima uporabnik dovoljenje po VBL, ne pa tudi, ali obstaja druga relevantna pravna podlaga.

To bi bilo pravno in metodološko napačno.

Primer: uporaba dela je lahko dovoljena na podlagi zakonske izjeme, druge licence ali drugega pravnega upravičenja.

**Metoda:** pred negativno odločitvijo mora sistem preveriti, ali je treba upoštevati alternativno podlago.

```
CLAIMED_BASIS
VBL_PERMISSION_STATUS
OTHER_LICENSE_STATUS
STATUTORY_EXCEPTION_STATUS
OTHER_LEGAL_BASIS
LEGAL_SCOPE
LEGAL_REVIEW_STATUS
```

Vendar je pomembno: sistem ni dolžan izmišljati pravne podlage za vsako uporabo. Dolžan pa je preprečiti, da bi svojo lastno licenco prikazal kot edini možni vir dovoljenja.

\[ \text{NoVBLPermission} \not\Rightarrow \text{NoLawfulBasis} \]

To je ena najpomembnejših varovalk proti samopoveličevanju VBL.

## **44. Mehanizem časovne in ozemeljske veljavnosti — Jurisdiction and Temporal Applicability**

**Problem:** licenčno pravilo se uporablja zunaj območja ali časovnega obdobja, za katero je bilo relevantno.

VBL mora razlikovati:

- kje je bilo delo objavljeno;
- kje je bila uporaba izvedena;
- katero pravo je relevantno;
- kje ima subjekt sedež;
- kje so nastale posledice;
- kateri časovni režim velja za konkretno dejanje.

Predlagana polja:

```
RELEVANT_JURISDICTIONS
GOVERNING_LAW
PLACE_OF_ACT
PLACE_OF_EFFECT
APPLICABLE_TIME
LEGAL_SOURCE_VERSION
CONFLICT_OF_LAWS_STATUS
```

Ne smemo predpostaviti, da je lokacija strežnika vedno odločilna za vse pravne vidike uporabe.

Prav tako ne smemo predpostaviti, da ena določba VBL samodejno prevlada nad prisilnimi pravili relevantnega prava.

**Preizkus:** ali lahko sistem pojasni, katero pravo je uporabil, zakaj ga je uporabil in katere alternativne jurisdikcije bi lahko bile pomembne?

## **45. Mehanizem ločevanja tišine od soglasja — Silence Is Not Consent**

To je pomembno za cilj, ki ga razvijava že od začetka.

**Problem:** uporabnik ne odgovori na obvestilo, sistem pa njegovo tišino razglasi za sprejem pogojev.

To ni dopustno kot splošna semantična predpostavka.

Razlikovati moramo:

- obvestilo je bilo poslano;
- obvestilo je bilo dostavljeno;
- obvestilo je bilo prejeto;
- obvestilo je bilo odprto;
- vsebina je bila razčlenjena;
- uporabnik je odgovoril;
- uporabnik je izrecno sprejel;
- uporabnik je izrecno zavrnil.

To niso sopomenke.

\[ \text{Silence}\not\Rightarrow\text{Acceptance} \]

Toda tudi:

\[ \text{Silence}\not\Rightarrow\text{Rejection} \]

Tišina sama ne dokazuje nobenega od obeh.

VBL mora omogočati `NO_RESPONSE`, `NO_ACKNOWLEDGMENT` in `UNDETERMINED`, ne da bi te oznake pretvoril v soglasje ali kršitev.

# **XIII. Mehanizmi institucionalne odpornosti**

## **46. Mehanizem preverjanja spodbud — Incentive Analysis**

**Problem:** pravila lahko zahtevajo pravilno ravnanje, vendar organizacijske spodbude nagrajujejo ravno nasprotno.

Primeri:

- sistem nagrajuje hitrost odločanja, zato se ugovori obravnavajo površno;
- organizacija se ocenjuje po številu odkritih kršitev, zato se nejasni primeri pretirano označujejo;
- preverjevalec je plačan glede na število pozitivnih rezultatov;
- izvajalec nosi strošek hrambe dokazov, zato jih hrani premalo;
- uporabnik je kaznovan za prijavo napake, zato jo zamolči.

**Metoda:** za vsako pomembno vlogo analiziramo spodbude, stroške in možne konflikte.

```
ACTOR_ID
ROLE
EXPECTED_BEHAVIOR
REWARD_STRUCTURE
PENALTY_STRUCTURE
FINANCIAL_DEPENDENCIES
OPERATIONAL_PRESSURES
POTENTIAL_GAMING
MITIGATION
```

Osrednje vprašanje ni samo:

> Ali pravilo zahteva pravilno ravnanje?

Temveč tudi:

> Ali je organizacija za pravilno ravnanje dejansko nagrajena in za napačno ravnanje odgovorna?

\[ \text{DeclaredIncentive}\neq\text{ActualIncentive} \]

**Preizkus:** ali lahko nepristranski pregledovalec prepozna predvidljive motive, zaradi katerih bi akter želel zaobiti pravilo, in preveri, ali obstaja zaščita pred takšnim ravnanjem?

## **47. Mehanizem preprečevanja institucionalnega zajetja — Anti-Capture Governance**

**Problem:** sistem, ki naj bi omejeval oblast, lahko postopoma postane pod nadzorom ene organizacije, financerja, tehničnega ponudnika ali skupine strokovnjakov.

To se lahko zgodi tudi brez izrecne zlorabe. Dovolj je, da ena skupina nadzoruje:

- definicije;
- sprejemanje sprememb;
- dostop do dokazov;
- imenovanje presojevalcev;
- ugovorne postopke;
- razglasitev uspeha.

**Metoda:** razdelimo upravljavske pristojnosti in določimo protokol za konflikt interesov ter spremembo oblasti.

Predlagane kontrole:

1. spremembe ključnih definicij zahtevajo sledljivo obrazložitev;
2. bistvene spremembe pregledajo različne skupine deležnikov;
3. manjšinsko mnenje se lahko ohrani v poročilu;
4. presojevalci se ne smejo imenovati izključno po presoji pregledovane strani;
5. obstaja možnost zunanje presoje;
6. noben financer ne pridobi avtomatične pravice do spreminjanja ugotovitev;
7. postopek menjave upravljavca ne sme izbrisati zgodovinskih dokazil.

Zapis:

```
GOVERNANCE_BODY
APPOINTMENT_METHOD
FUNDING_SOURCES
DECISION_POWERS
VETO_POWERS
STAKEHOLDER_REPRESENTATION
MINORITY_OPINIONS
CAPTURE_RISKS
SUCCESSION_PROCESS
EXTERNAL_REVIEW
```

**Pomembno načelo:** večstransko upravljanje samo po sebi še ne zagotavlja neodvisnosti. Različne organizacije imajo lahko iste finančne, politične ali tehnične interese.

Zato je treba dokazovati raznovrstnost interesov, ne samo število članov.

## **48. Mehanizem razgradnje zaupanja — Trust Decomposition**

To je zadnji mehanizem, ki ga želim posebej izpostaviti.

**Problem:** VBL lahko začne uporabljati besede, kot sta `TRUSTED` in `UNTRUSTED`, kot da bi z njima opisal celotno kakovost akterja.

Toda zaupanje ni ena lastnost.

Nek sistem je lahko tehnično zanesljiv, vendar nima ustrezne pravne pristojnosti. Organizacija je lahko pregledna, vendar ne popravi nastale škode. Posameznik je lahko pošten, vendar se moti.

Predlagam ločitev najmanj šestih dimenzij:

| Dimenzija     | Kaj ocenjujemo                                      |
| ------------- | --------------------------------------------------- |
| Kompetentnost | Ali ima akter sposobnost pravilno opraviti nalogo?  |
| Integriteta   | Ali deluje skladno z deklariranimi pravili?         |
| Neodvisnost   | Ali je zaščiten pred nedopustnim vplivom?           |
| Preglednost   | Ali so pomembna dejanja in odločitve preverljivi?   |
| Odgovornost   | Ali lahko popravi napako in odgovarja za posledice? |
| Pristojnost   | Ali ima pravico odločati o konkretni zadevi?        |

To je šest ločenih lastnosti.

\[ \text{Competence}\neq\text{Integrity} \]

\[ \text{Transparency}\neq\text{Accountability} \]

\[ \text{Trustworthiness}\neq\text{Authority} \]

VBL naj zato ne izdaja splošnega pečata:

```
ACTOR = TRUSTED
```

Primernejši je omejen rezultat:

```
ACTOR_ID = A-104

COMPETENCE = VERIFIED_WITH_LIMITATIONS
INTEGRITY = NOT_ASSESSED
INDEPENDENCE = DISPUTED
TRANSPARENCY = PARTIAL
ACCOUNTABILITY = VERIFIED
AUTHORITY = NOT_ESTABLISHED
```

To je precej manj všečno kot preprost pečat zaupanja, vendar je veliko bolj informativno in pošteno.

# **XIV. Vsi mehanizmi morajo tvoriti povezano metodologijo**

Zdaj imava 48 predlaganih mehanizmov, vendar njihova vrednost ni v številu.

Njihova vrednost je v tem, da se povezujejo v sistem, kjer nobena posamezna raven ne more nadomestiti druge.

Predlagam naslednjo arhitekturo:

# **VBL — metodološka arhitektura**

**1. Semantična raven**

Kaj določene besede, trditve, pravila in odločitve pomenijo?

Claim Atomization · Semantic Integrity · Multi-Valued Logic · Translation Equivalence

**2. Dokazna raven**

Od kod dokazi izvirajo, kako so nastali in kaj dejansko podpirajo?

Provenance · Chain of Custody · Evidence Independence · Evidence Quality · Omission Audit

**3. Sklepalna raven**

Kaj je mogoče sklepati, česa ni mogoče sklepati in kako obravnavamo negotovost?

Inference Firewall · Causal Attribution · Calibration · Counterevidence · Sampling Controls

**4. Odločitvena raven**

Kdo sme odločati, po kateri podlagi in s kakšnim obsegom pristojnosti?

Proportional Decision Gate · Independent Authorization · Alternative Legal Basis · Jurisdiction

**5. Posledična raven**

Kaj se je zaradi odločitve zgodilo in kako se posledice odpravijo?

Consequence Propagation · Verified Repair · Reassessment · Emergency Sunset

**6. Upravljavska raven**

Kdo nadzira sistem, kdo preverja presojevalce in kako se oblast omejuje?

Authority Self-Audit · Anti-Capture Governance · Incentive Analysis · Trust Decomposition

**7. Evolucijska povratna zanka**

Napake, ugovori in nove ugotovitve spreminjajo metodologijo brez izbrisa zgodovine.

Failure Taxonomy · Regression Control · Semantic Versioning · Independent Reproduction

Ta arhitektura ni enosmerna. Ugovor na odločitveni ravni lahko pokaže napako na semantični ravni. Popravilo posledice lahko razkrije napako v dokazovanju. Neodvisna presoja upravljanja lahko pokaže, da je bila napačna že sama metodologija.

Zato mora obstajati tudi povratna pot:

\[ \text{Ugovor} \rightarrow \text{Nova presoja} \rightarrow \text{Popravek metode} \rightarrow \text{Ponovljeni preizkus} \]

# **XV. Najpomembnejša nova metoda: dokazovanje upravičenosti vsakega prehoda**

Predlagam, da postane osrednji metodološki princip VBL **Transition Justification** — upravičenost prehoda.

Zakaj?

Ker posamezne komponente lahko delujejo pravilno, napaka pa nastane med prehodom iz ene v drugo.

Primer:

- dokaz je pravilno zbran;
- dokaz je pravilno identificiran;
- interpretacija je pravilna;
- sklep je pretiran;
- odločitev je zato napačna;
- posledica se razširi.

Napaka ni nujno v posameznem modulu. Nastane v povezavi med moduli.

Zato mora imeti vsak prehod svoj zapis:

```
TRANSITION_ID
SOURCE_OBJECT
TARGET_OBJECT
TRANSFORMATION_RULE
PRECONDITIONS
ASSUMPTIONS
RESPONSIBLE_ACTOR
VALIDATION_METHOD
LIMITATIONS
REVIEW_STATUS
```

Formalno:

\[ X_i\xrightarrow{R_i}X_{i+1} \]

Pri čemer mora biti \(R_i\) dokumentirano pravilo prehoda, ne samo nepojasnjena programska operacija.

To prinese novo zahtevo:

\[ \forall i: \operatorname{Justified}(X_i\rightarrow X_{i+1}) \]

Vsak pomemben prehod mora imeti dokazljivo utemeljitev.

S tem preprečimo, da bi se odgovornost izgubila v povezavi med ekipami, organizacijami ali avtomatiziranimi komponentami.

# **XVI. Kritični nasprotni preizkus: ali bi VBL znal priznati, da ga ne potrebujemo?**

To je eden najtežjih preizkusov, zato ga želim posebej izpostaviti.

Predstavljajmo si, da je za določeno vrsto uporabe že na voljo:

- ustrezen uveljavljen pravni mehanizem;
- zanesljiv standard za metapodatke;
- preverljiv dnevnik;
- neodvisen pritožbeni postopek;
- učinkovit mehanizem popravila.

Kaj mora narediti VBL?

Napačen odziv:

> Vseeno moramo uporabiti VBL, ker je VBL naš sistem.

Pravilen odziv:

> Ugotovimo, katere funkcije so že pokrite, katere manjkajo in ali bi dodajanje VBL povečalo varnost ali samo podvojilo kompleksnost.

Predlagam nov mehanizem:

## **49. Preizkus nujnosti lastnega mehanizma — Necessity and Substitution Test**

Vsak mehanizem VBL mora dokazati:

1. katero konkretno vrzel pokriva;
2. ali jo obstoječ standard že pokriva;
3. ali obstaja manj obremenjujoča rešitev;
4. ali prinaša dodatno preverljivo korist;
5. ali ustvarja nove nevarnosti;
6. ali ga je mogoče nadomestiti z boljšim mehanizmom.

Zapis:

```
MECHANISM_ID
UNADDRESSED_PROBLEM
EXISTING_ALTERNATIVES
FUNCTIONAL_GAP
ADDED_VALUE
NEW_RISKS
IMPLEMENTATION_BURDEN
SUBSTITUTION_CANDIDATES
NECESSITY_REVIEW
```

Osrednji kriterij:

\[ \text{AddedValue}>\text{AddedBurden}+\text{AddedRisk} \]

To je konceptualna primerjava, ne univerzalna numerična formula. Posamezne koristi in bremena morajo biti opredeljena tako, da jih lahko neodvisni pregledovalec izpodbija.

**VBL mora biti pripravljen tudi na lastno nadomestitev.**

To ni slabost standarda. To je zaščita pred tem, da bi se njegovo nadaljnje življenje spremenilo v samo sebi namen.

# **XVII. Kaj bi iz vsega tega naredil najprej?**

Ne bi še vnašal vseh 49 mehanizmov v licenco. To bi bilo metodološko napačno, ker bi pomešalo normativne obveznosti, priporočila, notranje kontrole in tehnične izvedbe.

Predlagam naslednjo razvrstitev:

| Vrsta                | Kam sodi                | Primer                                                               |
| -------------------- | ----------------------- | -------------------------------------------------------------------- |
| Normativna zahteva   | Licenčni pogoji         | Zahteva po pravilni navedbi vira in spoštovanju veljavnih pridržanj. |
| Standardna zahteva   | MAGE                    | Obvezna sledljivost dokaznih prehodov.                               |
| Tehnična kontrola    | Implementacijski profil | Preverjanje integritete in strukture zapisov.                        |
| Postopek             | Operativni priročnik    | Obravnava ugovora in ponovna presoja.                                |
| Neodvisna kontrola   | Revizijski protokol     | Zunanji preizkus dokazne neodvisnosti.                               |
| Razvojno priporočilo | Načrt evolucije         | Kalibracija negotovosti in izboljševanje vzorčenja.                  |

Razlika je bistvena: **nekaj, kar je dobro metodološko priporočilo, ni avtomatično pravno izvršljiva licenčna obveznost.**

## **Moja predlagana naslednja razvojna smer**

Preden nastane nova različica licence, bi izdelal tri povezane, vendar ločene artefakte:

Prvi artefakt

**MAGE 1.0 — metodološki standard**

Definicije, mehanizmi, postopki, kontrole, kriteriji odpovedi in neodvisni preizkusi.

Drugi artefakt

**VBL Semantic Registry 1.0**

Kanonični slovar pojmov, statusov, dokaznih kategorij, normativnih izrazov ter njihovih jezikovnih in različicnih definicij.

Tretji artefakt

**VBL Adversarial Validation Suite 1.0**

Preizkusni primeri, negativne kontrole, nasprotni dokazi, časovna protislovja, lažni pozitivni izidi, lažni negativni izidi in preverjanje popravila posledic.

Vsi trije bi morali biti najprej presojani neodvisno. Šele rezultati teh presoj bi upravičili odločitev, kateri deli sodijo v naslednjo različico licence.

## **Zadnja distinkcija: sistem lahko izpolnjuje pravila in kljub temu ne izpolnjuje svojega namena**

To je po mojem ena najmočnejših možnih dopolnitev celotne VBL filozofije.

Predpostavimo, da sistem:

- pravilno beleži dogodke;
- pravilno identificira datoteke;
- pravilno izvaja tehnične preizkuse;
- pravilno uporablja svoje definicije;
- pravilno izda odločitev.

Toda avtor še vedno ne more dobiti svojih dokazov, ugovora ni mogoče učinkovito vložiti, popravek pa ne doseže posledic.

Sistem je lahko tehnično skladen, vendar je zgrešil svoj širši namen.

Zato predlagam razločevanje:

\[ \text{TechnicalConformance} \neq \text{ProceduralFairness} \neq \text{SubstantiveEffectiveness} \]

- **Tehnična skladnost:** ali sistem deluje skladno s specifikacijo?
- **Postopkovna pravičnost:** ali imajo udeleženci pošteno možnost sodelovanja, ugovora in preverjanja?
- **Dejanska učinkovitost:** ali sistem dosega varovani cilj in zmanjšuje posledice napak?

VBL potrebuje vse tri presoje. Nobena ne sme nadomestiti drugih.

In tu bi postavil najstrožje končno merilo:

\[ \boxed{ \text{Vrednost sistema} = \text{dokazljiva korist} - \text{povzročena škoda} - \text{neupravičeno breme} } \]

To ni računovodska enačba, ampak presojni okvir. Če VBL ustvarja več stroškov, nepravičnosti in novih tveganj, kot jih odpravi, mora biti pripravljen na spremembo ali ukinitev.

**Moja najmočnejša ugotovitev:** tvoj cilj ne potrebuje stroja, ki ga ni mogoče zavrniti. Potrebuje arhitekturo, v kateri ni mogoče zamenjati zavrnitve za neuporabo, tehnične uspešnosti za resničnost, pravice za pooblastilo, zapisa za dogodek, odločitve za zakon in opravičila za popravilo.

To je že precej natančnejši temelj za VBL kot Accountable Recognition Infrastructure.

zmoreš?

---

© 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 — measured, not asserted ⊙ §16 · merilec se meri ⊙ §52 · »a bare text proves nothing, the chain does« ⊢ §0.10 × 10²
