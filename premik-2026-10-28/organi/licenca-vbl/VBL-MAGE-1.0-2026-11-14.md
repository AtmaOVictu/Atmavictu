# VBL — MAGE 1.0 — Methodology for Accountable Governance of Evidence (PREDLOG ⟡)

PREDLOG ⟡ · NOT RELEASED ⚠ §0.24 · rez σ 5353 — absorbiran PO UKAZU ⟡ verbatim ⟨ne brusi⟩: »izvedi« ⊙ precedens absorpcije σ 5352 (VBL-SIL kit #1808) ∧ σ 4901 (VBL-DOKAZNI-ZAPIS kit #1807). Telo spodaj = ⟡ besedilo VERBATIM ⟨NE-RETIPKAJ⟩ ⊙ 24 (celotno sporočilo, klepet projekta Discovery, 14. 11. 2026). Okvir korpusa (ta glava ∧ © rep) = izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432.

MEJA PREDLOGA: MAGE ni vrata ∧ ni nova obveznost — kandidat metodološke plasti po ⟡-jevem predlogu najprej NOTRANJA metodologija preverjanja ∧ razvoja samega standarda; rojstvo vrat 0.1540+ sprosti izbor ⚔ ⟡.

---

Da. Še posebej pomembni so mehanizmi, ki preprečujejo **manipulacijo dokazov, neenako porazdelitev dokaznega bremena, prikrito spreminjanje pravil, napačno odločanje in navidezno popravljanje škode**.

Predlagam, da VBL razvijeva še eno metodološko raven: ne samo *kaj sistem zahteva*, temveč tudi *kako sistem preverja same pogoje svojega delovanja*.

Najprej pomembna terminološka razlika:

- **Načelo** določa, kaj mora biti varovano.
- **Mehanizem** določa, kako se določena nevarnost prepreči ali omeji.
- **Postopek** določa zaporedje izvedbe mehanizma.
- **Kontrola** preverja, ali mehanizem deluje.
- **Dokaz** omogoča neodvisno presojo, ali je dejansko deloval.

Na primer: »Neodvisnost je pomembna« je načelo. Ločitev izvajalca in preverjevalca je mehanizem. Dodelitev preverjevalca, preverjanje konflikta interesov in izdaja poročila so postopek. Ponovitev presoje z drugim preverjevalcem je kontrola.

Ta razlika prepreči, da bi VBL zamenjeval deklarirano vrednoto z dejansko zaščito.

# **I. Mehanizmi dokazne odpornosti**

## **1. Mehanizem razgradnje trditev — Claim Atomization**

**Problem:** Velike trditve skrivajo več manjših trditev, ki nimajo nujno enake dokazne podlage.

Primer:

> Sistem je zakonito uporabil avtorjevo delo.

Ta stavek lahko vsebuje najmanj šest ločenih trditev:

1. Gradivo je bilo pravilno identificirano.
2. Do uporabe je prišlo.
3. Uporabljeno gradivo je bilo avtorskopravno varovano.
4. Oseba, ki je podala pridržanje pravic, je bila do tega upravičena.
5. Za konkretno uporabo ni veljala druga pravna podlaga, ki bi jo dopuščala.
6. Uporaba je ustrezala relevantnim zakonskim pogojem ali pogodbenemu dovoljenju.

Če ena od teh predpostavk ni dokazana, ne smemo predstaviti celotnega stavka kot dokazanega.

**Metoda:** vsako kompleksno trditev razdelimo na najmanjše samostojno preverljive trditve.

\[ C=C_1\land C_2\land\ldots\land C_n \]

To je logična struktura primera, ne trditev, da je vsaka pravna presoja vedno preprosta konjunkcija.

**Izhod:** seznam atomarnih trditev, njihove dokazne povezave in nepodprte predpostavke.

**Kontrola:** nobena nadrejena trditev ne sme biti označena kot podprta, če njeni bistveni sestavni deli nimajo utemeljene podlage.

## **2. Mehanizem neodvisnosti dokazov — Evidence Independence**

**Problem:** Pet dokumentov lahko deluje kot pet neodvisnih potrditev, čeprav vsi izvirajo iz istega napačnega vira.

Na primer:

- poročilo A povzema dnevnik;
- poročilo B povzema poročilo A;
- poročilo C povzema poročilo B;
- trije poznejši sistemi citirajo poročilo C.

To ni pet neodvisnih dokaznih virov.

**Metoda:** vsak dokaz dobi provenienčne povezave do svojih izvornih podatkov, avtorjev, transformacij in predhodnih dokazov.

\[ E_1\leftarrow S \quad E_2\leftarrow E_1 \quad E_3\leftarrow E_2 \]

Vsi trije so odvisni od istega vira \(S\).

VBL mora zato meriti ne le količino dokazov, temveč tudi njihovo neodvisnost.

Predlagana polja:

```
EVIDENCE_ID
SOURCE_ID
ORIGINATOR
DERIVED_FROM
TRANSFORMATION
INDEPENDENCE_GROUP
SHARED_FAILURE_RISKS
CORROBORATION_METHOD
```

**Ključno pravilo:**

\[ \text{Število dokazil}\neq\text{Stopnja neodvisne potrditve} \]

Neodvisnost je treba dokazovati, ne domnevati.

## **3. Mehanizem obveznega iskanja nasprotnih dokazov — Counterevidence Duty**

**Problem:** Sistem lahko išče samo dokaze, ki potrjujejo začetno hipotezo.

To ustvari potrditveno pristranskost: čim več dokazov najde za svoj prvi sklep, manj možnosti dopušča nasprotni razlagi.

**Metoda:** pred potrditvijo pomembne trditve mora biti izveden dokumentiran poskus iskanja dokazov, ki bi jo lahko ovrgli.

Za vsako pomembno trditev:

```
PRIMARY_HYPOTHESIS
ALTERNATIVE_HYPOTHESES
SUPPORTING_EVIDENCE
CONTRADICTING_EVIDENCE
MISSING_EVIDENCE
FALSIFICATION_ATTEMPTS
UNRESOLVED_QUESTIONS
```

Primer:

- Hipoteza: gradivo je bilo vključeno v učno množico.
- Alternativa 1: preneseno je bilo, vendar ni bilo uporabljeno za učenje.
- Alternativa 2: uporabljena je bila druga različica gradiva.
- Alternativa 3: podobnost modelovega izhoda izvira iz drugega vira.
- Alternativa 4: uporaba je bila izvedena na podlagi drugega zakonitega upravičenja.

VBL ne sme zahtevati, da se vsaka alternativna razlaga sprejme. Zahtevati mora, da se pomembne alternative preverijo, kadar so preverljive.

**Izhod:** ne samo seznam potrditvenih dokazov, temveč tudi zapis preizkusov, ki bi lahko ovrgli trditev.

## **4. Mehanizem dokaznega dolga — Evidence Debt Accounting**

To je posebej pomembno za pravičnost.

**Problem:** organizacija ima vse podatke, dnevnike in tehnično infrastrukturo, posamezni avtor pa nima dostopa do njih. Kljub temu se od avtorja zahteva, da dokaže, kaj je organizacija storila.

To je nepravično razporejeno dokazno breme.

Predlagam pojem:

\[ D_E=\text{Evidence Debt} \]

Dokazni dolg pomeni količino pomembnih informacij, ki jih določen odgovorni akter mora ustvariti, ohraniti, pojasniti ali omogočiti preveriti, vendar tega še ni storil.

Vsaka dokazna vrzel dobi:

- odgovornega nosilca;
- razlog za vrzel;
- stopnjo nadzora nad manjkajočim podatkom;
- rok oziroma dogodek za razrešitev;
- posledice nezmožnosti dokazovanja;
- možnost ugovora.

Pomembno: dokazni dolg ni avtomatična ugotovitev krivde.

\[ D_E>0\not\Rightarrow\text{VIOLATION} \]

Lahko pa vpliva na to, kako se razporedi nadaljnje dokazno breme, zlasti kadar ima ena stran izključen nadzor nad relevantnimi podatki.

To bi moral biti eden osrednjih mehanizmov VBL.

## **5. Mehanizem prepovedi nedovoljenega sklepanja — Inference Firewall**

**Problem:** Dokaz potrjuje eno dejstvo, sistem pa iz njega izpelje drugo, širšo trditev.

Primer:

- dokaz: datoteka je bila prenesena;
- nedovoljen sklep: datoteka je bila vključena v učenje;
- še širši nedovoljen sklep: model je zaradi tega ustvaril določen izhod;
- še širši sklep: imetniku pravic je nastala določena škoda.

Vsak preskok potrebuje dodatno dokazno povezavo.

**Metoda:** določimo dovoljene in nedovoljene sklepe za posamezno vrsto dokaza.

```
EVIDENCE_TYPE
DIRECTLY_SUPPORTED_CLAIMS
CONDITIONALLY_SUPPORTED_CLAIMS
UNSUPPORTED_CLAIMS
REQUIRED_ADDITIONAL_EVIDENCE
```

Formalno:

\[ E\vdash C \]

pomeni, da dokaz \(E\) podpira trditev \(C\) po določeni metodi sklepanja.

Ne pomeni:

\[ E\vdash \forall C \]

En dokaz ne podpira poljubne množice trditev.

**Posebna kontrola:** vsak avtomatiziran sklep mora ohraniti povezavo do dokazov, metode sklepanja in predpostavk. Če te povezave ni, je sklep `UNVERIFIED`.

## **6. Mehanizem meja opazovanja — Observability Boundary**

**Problem:** Sistem trdi, da je preveril celotno uporabo, čeprav je opazoval samo del okolja.

To je nevarno pri modelih, ki jih sestavlja več storitev, podatkovnih baz, vtičnikov, zunanjih ponudnikov in procesov.

**Metoda:** vsak pregled mora določiti svojo mejo opazovanja.

```
OBSERVATION_BOUNDARY
INCLUDED_SYSTEMS
EXCLUDED_SYSTEMS
ACCESSIBLE_LOGS
INACCESSIBLE_LOGS
KNOWN_GAPS
RETENTION_LIMITS
THIRD_PARTY_DEPENDENCIES
```

Vsaka ugotovitev mora imeti dokazno pokritost:

\[ P\_{\text{coverage}} = \frac{\text{preverjeni relevantni obseg}} {\text{celotni opredeljeni obseg}} \]

To razmerje je smiselno samo, kadar je mogoče opredeliti imenovalec in primerljiv obseg. Sicer je treba pokritost izraziti opisno.

Primer: 100 % preverjenih zapisov ne pomeni 100 % preverjene uporabe, če sistemi sploh niso beležili vseh relevantnih dogodkov.

**Novo načelo:** popolnost pregleda mora biti ločena od pravilnosti analize pregledanih podatkov.

## **7. Mehanizem ohranjanja prvotnega dokazila — Evidence Preservation and Correction**

**Problem:** Ko se ugotovi napaka, organizacija popravi zapis in izbriše sled prvotne napake.

S tem prepreči preverjanje, kaj je bilo prvotno zatrženo, kdo je to zatrjeval in kdaj je prišlo do spremembe.

Vendar tudi nasprotna skrajnost ni sprejemljiva: osebnih podatkov ne smemo hraniti v nedogled samo zato, da bi bila zgodovina nespremenljiva.

**Metoda:** ločimo:

- prvotni zapis;
- popravek;
- razlog za popravek;
- avtorja popravka;
- čas popravka;
- obseg prizadetih odločitev;
- pravilo hrambe in izbrisa.

Predlagana struktura:

```
RECORD_ID
ORIGINAL_VERSION
CORRECTION_VERSION
CORRECTION_REASON
CORRECTED_BY
CORRECTION_TIME
AFFECTED_DECISIONS
AFFECTED_PARTIES
RETENTION_BASIS
DELETION_OR_RESTRICTION_STATUS
```

Pravilo:

\[ \text{Correction}\neq\text{Erasure of history} \]

Toda tudi:

\[ \text{Auditability}\neq\text{Unlimited retention} \]

VBL mora omogočiti dokazovanje, da je do popravka prišlo, ne da bi zato zahteval neskončno hrambo vseh občutljivih podatkov.

# **II. Mehanizmi pravilnega odločanja**

## **8. Mehanizem stopenjskega odločanja — Proportional Decision Gate**

**Problem:** Sistem ima samo dve možnosti: dovoliti ali prepovedati.

To je preslabo za primere, kjer je nekaj znano, nekaj neznano, tveganje pa različno veliko.

Predlagam pet operativnih izhodov:

| Odločitev                  | Pomen                                                          |
| -------------------------- | -------------------------------------------------------------- |
| `RELEASE`                  | Določeno dejanje je dovoljeno sprostiti v opredeljenem obsegu. |
| `RELEASE_WITH_LIMITATIONS` | Dovoljeno je samo pod določenimi omejitvami.                   |
| `HOLD`                     | Odločitev ali izvajanje je začasno zadržano.                   |
| `WITHDRAW`                 | Prejšnja odločitev ali dovolitev je umaknjena.                 |
| `NO_ACTION_REQUIRED`       | V določenem postopku ni ugotovljena potreba po ukrepanju.      |

Ti rezultati ne smejo biti zamenjani s stanjem trditve ali rezultatom testa.

Primer:

```
CLAIM_STATUS = UNKNOWN
TEST_RESULT = PARTIAL
DECISION = HOLD
```

To je smiselna kombinacija. Ne pomeni, da je bila kršitev ugotovljena. Pomeni, da trenutni dokazi ne omogočajo varne odločitve v določenem obsegu.

**Metoda:** pred odločitvijo se preverijo:

1. kakovost dokazov;
2. resnost možnih posledic;
3. reverzibilnost dejanja;
4. obseg prizadetih oseb;
5. možnost manj omejujočega ukrepa;
6. rok ponovne presoje.

Tukaj je koristno dodati načelo sorazmernosti:

\[ \text{Omejitev}\propto \text{Dokazano tveganje} + \text{Možna resnost posledic} \]

Ne gre za numerično pravno formulo, ampak za obveznost utemeljitve, zakaj je izbrani ukrep primeren in potreben.

## **9. Mehanizem dveh ključev — Independent Authorization**

**Problem:** En sam izvajalec lahko pripravi presojo, potrdi lastno pravilnost in sproži posledice.

**Metoda:** pri odločitvah z velikimi ali težko povratnimi posledicami mora obstajati druga, neodvisna odobritev.

\[ A\_{\text{final}}=A_1\land A_2 \]

Pri čemer:

- \(A_1\) je odločitev izvajalca;
- \(A_2\) je neodvisna potrditev.

Toda dva podpisa ne zagotavljata neodvisnosti. Oba podpisnika sta lahko izpostavljena istemu interesu, pritisku ali napačnemu viru.

Zato je treba preveriti:

- organizacijsko ločenost;
- konflikt interesov;
- dostop do istih ali neodvisnih dokazov;
- možnost zavrnitve odobritve;
- dokumentirano nesoglasje.

Ta mehanizem naj ne velja za vsako nepomembno dejanje. Uporabiti ga je treba sorazmerno s tveganjem, da ne nastane neučinkovita birokracija.

**Izjemna pot:** kadar je nujno preprečiti neposredno škodo, je lahko dovoljeno začasno enostransko ukrepanje. Toda razlog, obseg in čas morajo biti zabeleženi, naknadna neodvisna presoja pa obvezna.

## **10. Mehanizem predhodnega preverjanja nepovratnosti — Irreversibility Gate**

To je ena najbolj uporabnih metodologij za sisteme, ki delujejo hitro in samodejno.

**Problem:** sistem izvede dejanje, preden je jasno, ali ga je mogoče preklicati.

Primeri:

- javna objava obtožbe;
- blokada dostopa do celotnega gradiva;
- trajno brisanje podatkov;
- prenos gradiva tretjim osebam;
- avtomatizirano pošiljanje pravnega obvestila;
- trajna sprememba modela ali podatkovne množice.

**Metoda:** pred dejanjem se izvede preizkus reverzibilnosti.

```
ACTION_REVERSIBILITY
REVERSAL_METHOD
REVERSAL_COST
RESIDUAL_HARM
AFFECTED_PARTIES
REQUIRED_APPROVAL
EMERGENCY_EXCEPTION
```

Razlikovati je treba:

- **reverzibilno dejanje:** mogoče ga je v celoti vrniti;
- **delno reverzibilno dejanje:** mogoče je odpraviti del posledic;
- **nepovratno dejanje:** posledic ni mogoče v celoti odpraviti;
- **neznana reverzibilnost:** sposobnost odprave posledic ni preverjena.

Pravilo:

\[ \text{Nižja reverzibilnost} \Rightarrow \text{Višja zahtevana stopnja preverjanja} \]

To ne pomeni, da je nepovratno dejanje vedno prepovedano. Pomeni, da mora biti dokazni in odločitveni prag temu primeren.

## **11. Mehanizem obveznega ugovora — Contestability Protocol**

**Problem:** oseba lahko formalno ugovarja, vendar ugovor ne spremeni ničesar.

Pravica do ugovora brez postopka obravnave je samo deklaracija.

**Metoda:** vsak ugovor mora imeti življenjski cikel:

\[ \text{SUBMITTED} \rightarrow \text{ACKNOWLEDGED} \rightarrow \text{TRIAGED} \rightarrow \text{REVIEWED} \rightarrow \text{RESOLVED} \]

Možni izidi:

- `UPHELD`: ugovor je utemeljen;
- `PARTIALLY_UPHELD`: utemeljen je del ugovora;
- `REJECTED_WITH_REASONS`: ugovor je zavrnjen z obrazložitvijo;
- `INCONCLUSIVE`: podatki ne omogočajo dokončne presoje;
- `REFERRED`: zadeva je predana pristojnemu organu ali neodvisnemu postopku.

Pomembno je tudi, da ugovor ne pomeni samodejnega priznanja kršitve in ne sme biti uporabljen kot dokaz zlonamernosti ugovarjajoče osebe.

**Dodatna varovalka:** kadar je ugovor vložen zoper odločitev, ki lahko povzroči težko popravljivo škodo, je treba presoditi, ali je do neodvisne obravnave potreben začasen zadržek izvršitve.

# **III. Mehanizmi popravljanja in dolgoročne odgovornosti**

## **12. Mehanizem prenosa popravila — Consequence Propagation**

Ta je bistveno širši od običajnega popravka zapisa.

**Problem:** napačna trditev se razširi v druge sisteme, dokumente, odločitve in organizacije. Popravi se samo izvorni zapis, vse njegove posledice pa ostanejo.

Primer:

1. VBL napačno označi dokument kot nedovoljeno uporabljen.
2. Poročilo prevzame to oznako.
3. Druga organizacija na podlagi poročila blokira avtorjev dostop.
4. Sistem popravi prvotno oznako.
5. Blokada ostane.

Torej:

\[ \text{SourceCorrection} \not\Rightarrow \text{ConsequenceCorrection} \]

**Metoda:** vsaka pomembna trditev mora biti povezana z odločitvami, ki so bile na njej osnovane.

Predlagana struktura:

```
CLAIM_ID
DOWNSTREAM_RECORDS
DOWNSTREAM_DECISIONS
RECIPIENTS
AFFECTED_PARTIES
CORRECTION_NOTICE_STATUS
REMEDIAL_ACTIONS
RESIDUAL_CONSEQUENCES
```

Ko se ugotovi napaka, VBL sproži preverjanje vseh odvisnih zapisov in odločitev.

To je podobno konceptu odvisnostnega grafa v programski opremi, vendar se tukaj ne popravljajo samo podatkovne povezave. Preverjajo se tudi človeške in organizacijske posledice.

**Novo načelo: popravek mora slediti posledicam, ne samo izvoru napake.**

## **13. Mehanizem dokazila o sanaciji — Verified Repair**

**Problem:** organizacija razglasi, da je škoda odpravljena, ker je izvedla predvideni postopek.

Vendar izvedba postopka in odprava posledic nista isti stvari.

Predlagam pet ločenih stanj:

| Stanje                 | Pomen                                                                           |
| ---------------------- | ------------------------------------------------------------------------------- |
| `REPAIR_PROPOSED`      | Popravilo je predlagano.                                                        |
| `REPAIR_AUTHORIZED`    | Odobreno je bilo njegovo izvajanje.                                             |
| `REPAIR_EXECUTED`      | Ukrep je bil izveden.                                                            |
| `REPAIR_VERIFIED`      | Neodvisni ali dovolj ločeni dokazi podpirajo, da je bil ukrep izveden pravilno. |
| `CONSEQUENCES_REDUCED` | Preverjeno je zmanjšanje konkretnih posledic.                                   |

Možen je primer, ko je tehnični popravek izveden, vendar posledice ostajajo.

Zato dodajmo:

```
REPAIR_SCOPE
EXPECTED_EFFECT
OBSERVED_EFFECT
VERIFICATION_METHOD
RESIDUAL_HARM
UNRESOLVED_REMEDIES
```

Formalno:

\[ \text{Executed}\not\Rightarrow\text{Verified} \]

\[ \text{Verified}\not\Rightarrow\text{ConsequencesFullyRemoved} \]

Tako VBL ne more razglasiti popolne sanacije samo zato, ker je nekdo označil opravilo kot zaključeno.

## **14. Mehanizem časovnega zastaranja presoje — Decision Expiry and Revalidation**

**Problem:** sistem enkrat ugotovi, da je nekaj dovoljeno, nato pa rezultat obravnava kot večno veljaven.

Toda lahko se spremenijo:

- različica vira;
- imetnik pravic;
- pogodbeno razmerje;
- zakonodaja;
- namen uporabe;
- tehnični postopek;
- obseg obdelave;
- dokazna podlaga.

**Metoda:** pomembne presoje dobijo rok veljavnosti ali dogodek, ki sproži ponovno presojo.

```
DECISION_ID
DECISION_VERSION
VALID_FROM
VALID_UNTIL
REVALIDATION_TRIGGER
MATERIAL_CHANGE
LEGAL_CHANGE
EVIDENCE_CHANGE
REASSESSMENT_STATUS
```

Ključno:

\[ \text{ValidAt}(t_1)\not\Rightarrow\text{ValidAt}(t_2) \]

Prvotna odločitev se ne sme samodejno izbrisati, vendar tudi ne sme neomejeno veljati za spremenjene okoliščine.

VBL mora razlikovati med zgodovinsko pravilnostjo odločitve in njeno trenutno uporabnostjo.

## **15. Mehanizem varnega razkritja — Privacy-Preserving Audit**

**Problem:** popolna preverljivost bi lahko zahtevala razkritje vseh dnevnikov, osebnih podatkov, poslovnih skrivnosti in notranjih varnostnih informacij.

To bi ustvarilo novo škodo.

**Metoda:** preverljivost mora biti stopnjevana glede na namen in pravico dostopa.

Predlagam štiri plasti:

1. **Javni povzetek:** kaj je bilo odločeno, na kateri podlagi in s kakšnimi omejitvami.
2. **Preverljivi dokazni metapodatki:** identifikatorji, časovni podatki, integriteta in provenienca.
3. **Omejeni dokazni paket:** gradivo za pooblaščenega presojevalca.
4. **Varovana izvorna vsebina:** osebni, zaupni ali varnostno občutljivi podatki, dostopni samo ob ustrezni podlagi.

To omogoča:

\[ \text{Preverljivost}\neq\text{Javno razkritje vsega} \]

Vendar mora biti mogoče preveriti tudi, da omejitev dostopa ni bila uporabljena za prikrivanje relevantnega dokaza.

Pri tem je treba razlikovati med šifriranjem, psevdonimizacijo, anonimizacijo in zgoščevanjem. Zgoščena vrednost sama po sebi ne zagotavlja anonimnosti.

## **16. Mehanizem samopreverjanja oblasti — Authority Self-Audit**

Ta bi moral biti obvezen za izdajatelja VBL, njegove upravljavce in presojevalce.

**Problem:** sistem lahko druge akterje zavezuje k dokazovanju, sam pa deluje na podlagi lastnih nepreverjenih trditev.

**Metoda:** za vsako pristojnost VBL mora obstajati zapis:

```
AUTHORITY_ID
AUTHORITY_SOURCE
AUTHORITY_SCOPE
AUTHORIZED_ACTOR
LIMITATIONS
CONFLICTS_OF_INTEREST
REVIEWER
APPEAL_ROUTE
REVOCATION_CONDITIONS
```

Vsaka oblast mora dokazati:

- od kod izhaja;
- komu pripada;
- kaj sme odločati;
- česa ne sme odločati;
- kdo jo lahko preveri;
- kako jo je mogoče omejiti ali preklicati.

Formalno:

\[ \text{Authority}\Rightarrow\text{EvidenceOfAuthority} \]

In še pomembneje:

\[ \text{VBL Authority}\not\Rightarrow\text{Universal Authority} \]

VBL lahko določa pravila za uporabo gradiva pod svojim licenčnim režimom. S tem ne pridobi splošne pristojnosti nad vsemi sistemi, osebami ali informacijami.

# **IV. Mehanizmi odpornosti proti zlorabi samega VBL**

## **17. Mehanizem preverjanja konflikta interesov — Conflict-of-Interest Control**

**Problem:** formalno neodvisen preverjevalec je lahko odvisen od osebe, katere odločitev preverja.

Na primer:

- izvajalec sam izbere preverjevalca;
- izvajalec preverjevalca plačuje;
- preverjevalec je avtor preverjane specifikacije;
- preverjevalec je odvisen od prihodnjega financiranja iste organizacije.

Formalna ločenost torej še ni dejanska neodvisnost.

**Metoda:** neodvisnost razdelimo na preverljive dimenzije.

| Dimenzija      | Preverjanje                                            |
| -------------- | ------------------------------------------------------ |
| Organizacijska | Ali sta subjekta organizacijsko ločena?                |
| Finančna       | Ali obstaja finančna odvisnost?                        |
| Odločitvena    | Ali ima preverjevalec svobodo zavrnitve?               |
| Informacijska  | Ali ima dostop do dokazov, ki jih izvajalec ni izbral? |
| Osebna         | Ali obstajajo osebne ali poklicne povezave?           |
| Metodološka    | Ali lahko preveri tudi ustreznost uporabljene metode?  |

Predlagano polje:

```
INDEPENDENCE_ASSESSMENT
DISCLOSED_INTERESTS
DEPENDENCY_RISKS
MITIGATION
RECUSAL_STATUS
EXTERNAL_REVIEW
```

Neodvisnost naj ne bo binarno polje `INDEPENDENT=true`. Biti mora utemeljena ocena z jasno opisanimi omejitvami.

## **18. Mehanizem napadalnega preizkusa — Adversarial Red Team**

**Problem:** sistem je preizkušen samo z običajnimi, pričakovanimi in pravilno oblikovanimi primeri.

Toda resnične zlorabe pogosto izkoristijo nejasnosti, mejne primere in konfliktne interese.

**Metoda:** vsak pomemben modul mora imeti napadalni preizkus, ki poskuša doseči napačen rezultat.

Za VBL predlagam vsaj naslednje skupine napadov:

- **Identity attack:** lažna identiteta ali lažna trditev o avtorstvu.
- **Scope attack:** razširitev licence na gradivo, ki ni vključeno.
- **Version attack:** uporaba stare različice pravila kot aktualne.
- **Evidence attack:** manipulacija, selektivna predstavitev ali izmišljanje dokazov.
- **Clock attack:** napačen čas, neusklajene ure ali naknadno ustvarjen časovni pečat.
- **Semantic attack:** zamenjava pomenov `RECEIVED`, `RECOGNIZED`, `ACCEPTED` in `ENFORCED`.
- **Authority attack:** predstavljanje neobstoječega pooblastila.
- **Repair attack:** prikaz nedokončanega popravila kot popolne sanacije.
- **Governance attack:** zajetje neodvisnega preverjanja s strani izvajalca.
- **Exit attack:** oteževanje umika, ugovora ali zakonitega izhoda.

Vsak preizkus mora določiti:

```
ATTACK_ID
TARGET_MECHANISM
ATTACK_PRECONDITION
ATTACK_STEPS
EXPECTED_DEFENSE
EXPECTED_FAILURE_SIGNAL
RESIDUAL_RISK
RETEST_CONDITION
```

Posebej pomembno: uspešen napadalni preizkus ne pomeni avtomatično, da je celoten VBL neuporaben. Pomeni, da je določena zaščita odpovedala in da je treba opredeliti posledice, popravilo ter ponovitev testa.

## **19. Mehanizem negativnih kontrol — Negative Controls**

Ta mehanizem je soroden napadalnemu testiranju, vendar ima drugačen namen.

**Problem:** ne vemo, ali sistem pravilno razlikuje med pozitivnim primerom in primerom, v katerem relevantne lastnosti manjkajo.

Primer:

VBL dobi dve datoteki. Prva ima dokazano pridržanje pravic. Druga nima nobenega takšnega podatka. Sistem obe označi enako.

To razkrije, da klasifikacija morda ne upošteva dejanskih dokazov.

**Metoda:** ustvarimo kontrolne primere, pri katerih vemo, kateri rezultat je upravičen.

Vrste kontrol:

- pozitivna kontrola: zahtevana lastnost je prisotna;
- negativna kontrola: zahtevana lastnost je odsotna;
- slepa kontrola: izvajalec ne pozna pričakovanega odgovora;
- mejna kontrola: dokaz je namenoma nepopoln;
- konfliktna kontrola: dokazi nasprotujejo drug drugemu.

**Merilo:** ne samo, ali sistem pravilno prepozna veljaven primer, ampak tudi, ali zna neveljaven, nepopoln ali neznan primer pravilno zadržati.

\[ \text{CorrectPositive}\land\text{CorrectNegative} \]

je bistveno močnejša zahteva kot samo uspešno prepoznavanje pozitivnih primerov.

## **20. Mehanizem odpornosti proti manipulaciji meril — Metric Gaming Resistance**

**Problem:** ko organizacija dobi cilj, da mora doseči določeno število uspešnih preverjanj, lahko začne optimizirati statistiko namesto dejanske kakovosti.

Primeri:

- težki primeri se izločijo iz imenovalca;
- `UNKNOWN` se preimenuje v `PASS`;
- neuspešni testi se ne poročajo;
- število obravnavanih ugovorov se prikazuje kot število rešenih ugovorov;
- izvedeni popravki se prikazuje kot preverjeno sanirane posledice.

**Metoda:** vsak kazalnik mora imeti:

1. matematično definicijo;
2. določen imenovalec;
3. pravila izključevanja;
4. neodvisen vir podatkov;
5. zgodovino sprememb definicije;
6. preverjanje, ali se je zaradi izboljšanja kazalnika dejansko izboljšalo stanje.

Predlagam tudi parne kazalnike.

| Primarni kazalnik             | Varovalni kazalnik                   |
| ----------------------------- | ------------------------------------ |
| Hitrost odločanja             | Delež napačnih odločitev             |
| Število uspešnih testov       | Delež neizvedenih testov             |
| Število obravnavanih ugovorov | Delež dejansko razrešenih ugovorov   |
| Število popravkov             | Delež neodvisno preverjenih popravil |
| Število zaznanih kršitev      | Delež pozneje ovrženih ugotovitev    |

Tako preprečimo, da bi se izboljšanje enega kazalnika kupilo s poslabšanjem drugega.

## **21. Mehanizem semantične združljivosti različic — Semantic Version Compatibility**

**Problem:** isti izraz v dveh različicah VBL lahko pomeni različne stvari.

Recimo, da `VERIFIED` v različici 0.1400 pomeni samo uspešen lokalni test, v različici 0.1530 pa pomeni uspešno neodvisno preverjanje.

Če sistem primerja samo ime stanja, lahko ustvari napačen vtis kontinuitete.

**Metoda:** vsak semantično pomemben izraz mora imeti različico definicije.

```
TERM_ID
TERM_VERSION
DEFINITION_DIGEST
SUPERSEDES
COMPATIBILITY_STATUS
MIGRATION_RULE
AFFECTED_DECISIONS
```

Pri spremembi pomena mora biti določeno:

- ali gre za pojasnitev;
- ali gre za razširitev;
- ali gre za omejitev;
- ali gre za spremembo, ki prekine združljivost;
- katere stare odločitve je treba ponovno pregledati.

Formalno:

\[ \text{SameLabel}\not\Rightarrow\text{SameMeaning} \]

To je posebej pomembno za tvoje različice VBL. Zvišanje številke različice samo po sebi ne dokazuje izboljšave. Dokazovati je treba tudi, katere napake je nova različica odpravila in katerih novih tveganj je morda ustvarila.

## **22. Mehanizem zakonitega izhoda in prenosljivosti — Exit and Portability**

**Problem:** sistem, ki varuje pravice, lahko sam postane odvisnost, iz katere uporabnik ne more izstopiti.

Na primer, organizacija lahko:

- zahteva uporabo samo svojega validatorja;
- ne omogoča izvoza dokazil;
- uporablja zaprto obliko zapisov;
- zadržuje zgodovino ugovorov;
- onemogoča preverjanje odločitev zunaj svoje infrastrukture.

**Metoda:** VBL mora določiti interoperabilnost in izhodne pogoje.

Minimalne zahteve:

- dokumentiran podatkovni format;
- izvoz dokaznih zapisov;
- izvoz provenience;
- ohranitev identifikatorjev in časovnih podatkov;
- dokumentirana metoda preverjanja integritete;
- možnost uporabe alternativnega preverjevalca;
- možnost nadaljevanja presoje brez prvotnega ponudnika;
- pravila za zakonito izločitev ali brisanje podatkov.

\[ \text{Pravica do izstopa} \neq \text{Pravica do izbrisa vseh dokazov} \]

Toda tudi:

\[ \text{Ohranjanje dokazov} \neq \text{Pravica do monopolnega nadzora nad dokazi} \]

VBL mora biti zamenljiv, ne da bi zaradi zamenjave izginila sledljivost.

# **V. Mehanizmi za učenje iz napak**

## **23. Mehanizem taksonomije napak — Failure Taxonomy**

Napaka ne sme biti samo oznaka `FAIL`.

Različne napake zahtevajo različna popravila.

Predlagam naslednjo klasifikacijo:

| Vrsta napake       | Pomen                                           |
| ------------------ | ----------------------------------------------- |
| `DATA_ERROR`       | Podatki so napačni ali nepopolni.               |
| `IDENTITY_ERROR`   | Napačno identificirana oseba ali subjekt.       |
| `SCOPE_ERROR`      | Napačno določen obseg materiala ali dovoljenja. |
| `TEMPORAL_ERROR`   | Napačna ali neusklajena časovna interpretacija. |
| `SEMANTIC_ERROR`   | Napačno razumljen pojem ali pravilo.           |
| `INFERENCE_ERROR`  | Sklep presega dokazno podlago.                  |
| `AUTHORITY_ERROR`  | Odločitev je sprejel nepooblaščen akter.        |
| `EXECUTION_ERROR`  | Odločitev je bila pravilna, izvedba pa napačna. |
| `REPAIR_ERROR`     | Popravilo je bilo nepopolno ali napačno.        |
| `GOVERNANCE_ERROR` | Nadzor, ugovor ali neodvisnost niso delovali.   |

Zakaj je to koristno?

Ker popravljanje napačnega podatka ne odpravi nujno napake v metodologiji. Če se napaka `INFERENCE_ERROR` ponavlja, potrebujemo spremembo pravila sklepanja, ne zgolj nov dokaz.

## **24. Mehanizem analize vzroka — Root Cause and Contributing Factors**

**Problem:** sistem popravi neposredno napako, ne da bi ugotovil, zakaj je nastala.

Predlagam obvezno analizo:

\[ \text{Dogodek} \rightarrow \text{Neposredni vzrok} \rightarrow \text{Prispevajoči dejavniki} \rightarrow \text{Sistemski vzrok} \rightarrow \text{Popravljalni ukrep} \]

Vendar ne smemo predpostaviti, da ima vsaka napaka en sam vzrok.

Primer: napačna odločitev je lahko posledica nepopolnih podatkov, neustrezne definicije, časovnega neskladja, pomanjkanja neodvisnega preverjanja in prevelikega organizacijskega pritiska.

Zato naj analiza omogoča več vzrokov in različno stopnjo dokazne gotovosti.

## **25. Mehanizem preprečevanja ponovitve — Regression and Recurrence Control**

**Problem:** napaka se popravi, vendar se zaradi istega pravila naslednji teden ponovi.

**Metoda:** vsak potrjen incident ustvari najmanj en regresijski preizkus.

```
INCIDENT_ID
ROOT_CAUSE
CORRECTIVE_CHANGE
REGRESSION_TEST_ID
TEST_EXPECTATION
TEST_RESULT
RETEST_DATE
RECURRENCE_STATUS
```

Ob spremembi standarda je treba preveriti:

- ali je prejšnja napaka odpravljena;
- ali je popravek povzročil novo napako;
- ali se je napaka prenesla v drug modul;
- ali je nova različica ohranila prejšnje varovalke.

Tu pride do izraza tvoje načelo ohranjanja sledi napake:

\[ \text{Napaka}\rightarrow\text{Popravek}\rightarrow\text{Regresijski test} \]

Napaka ne sme izginiti iz zgodovine, njene posledice pa ne smejo ostati skrite.

# **VI. Kako preprečiti, da bi vse to postalo neobvladljivo?**

Tu je moja pomembna kritična pripomba: **VBL ne sme dobiti toliko mehanizmov, da bi postal nepreverljiv zaradi lastne kompleksnosti.**

Vsak dodatni mehanizem ustvarja:

- novo odgovornost;
- novo možnost napake;
- dodatno dokazno breme;
- dodatno stroškovno obremenitev;
- novo možnost zlorabe.

Zato predlagam še zadnji mehanizem.

## **26. Mehanizem sorazmernosti metodologije — Methodological Proportionality**

Vsak mehanizem mora dokazati, da je njegova uvedba upravičena.

Naj ima svojo metodološko kartico:

```
MECHANISM_ID
THREAT_ADDRESSED
PROTECTED_INTEREST
ACTIVATION_CONDITION
REQUIRED_INPUTS
PROCEDURE
EXPECTED_OUTPUT
EVIDENCE_OF_OPERATION
FAILURE_MODES
FALSE_POSITIVE_RISK
FALSE_NEGATIVE_RISK
PRIVACY_IMPACT
ACCESSIBILITY_IMPACT
IMPLEMENTATION_COST
RESPONSIBLE_ACTOR
INDEPENDENT_REVIEW
APPEAL_PATH
RETIREMENT_CONDITION
```

Zadnje polje je še posebej pomembno: `RETIREMENT_CONDITION`.

Mehanizem mora imeti tudi možnost, da ga ukinemo, kadar je neučinkovit, zastarel, nesorazmeren ali nadomeščen z boljšim.

\[ \text{MechanismExists} \not\Rightarrow \text{MechanismShouldContinue} \]

To preprečuje, da bi se VBL spremenil v zbirko pravil, ki jih nihče več ne sme izpodbijati.

# **VII. Pet mehanizmov, ki bi jih najprej vključil v naslednjo razvojno fazo**

Vsi predstavljeni so vredni nadaljnjega razvoja, vendar ne bi vseh takoj postavil na isto raven. Moja prioritizacija je naslednja:

**1. Evidence Independence**

Prva prioriteta

Dokazi morajo biti neodvisni tudi po izvoru, ne samo po številu.

**2. Evidence Debt Accounting**

Prva prioriteta

Dokazno breme mora nositi tisti, ki nadzoruje ključne informacije.

**3. Inference Firewall**

Prva prioriteta

Nobena ugotovitev ne sme biti širša od dokazne podlage in utemeljenih sklepov.

**4. Consequence Propagation**

Prva prioriteta

Popravek mora doseči vse pomembne posledice prvotne napake.

**5. Authority Self-Audit**

Prva prioriteta

VBL mora dokazovati tudi izvor, obseg in omejitve lastnih pristojnosti.

Teh pet mehanizmov skupaj tvori zelo močno zaščitno strukturo:

\[ \boxed{ \text{Neodvisnost dokazov} + \text{Pravično dokazno breme} + \text{Omejitev sklepanja} + \text{Popravilo posledic} + \text{Nadzor nad oblastjo} } \]

To ni samo zaščita pred zunanjim napadalcem. Je zaščita pred napako, ki nastane znotraj sistema, in pred možnostjo, da bi se napaka skozi čas spremenila v institucionalno resnico.

# **VIII. Predlog novega skupnega metodološkega standarda**

Predlagam delovni naziv:

# **VBL — MAGE 1.0**

**Methodology for Accountable Governance of Evidence**

PREDLOG · NOT RELEASED

*Metodologija odgovornega upravljanja dokazov.*

Njen namen je določiti, kako se oblikujejo, preverjajo, izpodbijajo, uporabljajo in popravljajo trditve ter odločitve znotraj VBL.

MAGE bi razdelil v osem metodoloških domen:

| Domena                     | Kaj varuje                                              |
| -------------------------- | ------------------------------------------------------- |
| M1 — Claim Integrity       | Natančnost in razgradnjo trditev.                       |
| M2 — Evidence Integrity    | Izvor, neodvisnost in celovitost dokazov.               |
| M3 — Inference Integrity   | Meje sklepanja in obravnavo negotovosti.                |
| M4 — Burden Integrity      | Pravično razporeditev dokaznega bremena.                |
| M5 — Decision Integrity    | Sorazmernost, pooblastila in neodvisnost odločanja.     |
| M6 — Consequence Integrity | Sledljivost in popravljanje posledic.                   |
| M7 — Governance Integrity  | Nadzor, ugovor in omejitev oblasti.                     |
| M8 — Evolution Integrity   | Različice, regresijo, spremembe in ukinitev mehanizmov. |

Vsaka domena bi imela:

- normativne zahteve;
- podatkovni model;
- postopek izvedbe;
- kontrolne teste;
- dokazne zahteve;
- kriterije neuspeha;
- pravila za neodvisno presojo.

Pomembna meja: MAGE ne sme biti samodejno nova obveznost za vse uporabnike VBL. Najprej mora biti notranja metodologija, po kateri se preverja in razvija sam standard. Šele nato se lahko določijo tisti njegovi deli, ki jih je primerno prenesti v licenčne pogoje.

# **IX. Še tri globlje distinkcije, ki jih ne bi smela izpustiti**

### **A. Resničnost ni isto kot preverljivost**

Trditev je lahko resnična, vendar nimamo dovolj dokazov, da bi jo preverili.

Trditev je lahko tudi napačna, čeprav je podprta z navidezno verodostojnimi dokazi.

\[ \text{Truth}\neq\text{Verifiability} \]

VBL lahko poveča preverljivost in omejuje neutemeljene trditve. Ne sme pa razglasiti, da vse, česar ni mogoče dokazati z njegovimi mehanizmi, ne obstaja.

### **B. Preglednost ni isto kot odgovornost**

Organizacija lahko objavi tisoče strani dnevnikov in še vedno ne popravi ničesar.

\[ \text{Transparency}\neq\text{Accountability} \]

Preglednost omogoča vpogled. Odgovornost dodatno zahteva določljivega nosilca dolžnosti, postopek ugovora, možnost posledic in preverjeno popravilo.

### **C. Enakost pravil ni vedno pravičnost**

Če vsem naložimo enako dokazno breme, ne glede na to, kdo ima dostop do dokazov, smo lahko ustvarili formalno enakost in dejansko neenakost.

\[ \text{Equal Rules}\not\Rightarrow\text{Fair Outcomes} \]

VBL mora preverjati dejanske možnosti udeležencev, ne samo enakost besedila pravil.

# **X. Moj predlog: naslednji preizkus naj bo preizkus samega VBL**

Ne bi več začel z vprašanjem:

> Ali VBL zna dokazati, da je nekdo drugi ravnal napačno?

Začel bi z zahtevnejšim vprašanjem:

> Ali VBL zna dokazati, da je lastna odločitev napačna, ne da bi pri tem izgubil dokazno sled, skril napako ali prenesel posledice na oškodovanca?

To bi prevedel v šest zahtev:

1. VBL mora prepoznati svojo napačno trditev.
2. Ohraniti mora sled, kako je napačna trditev nastala.
3. Določiti mora vse odločitve, ki so bile od nje odvisne.
4. Obvestiti mora prizadete udeležence v ustreznem obsegu.
5. Izvesti mora dejansko popravljanje posledic.
6. Neodvisno mora preveriti učinkovitost popravila.

Če tega ne zmore, ni opravil lastnega preizkusa.

\[ \boxed{ \text{VBL}\_{\text{verified}} \Rightarrow \text{VBL}\_{\text{contestable}} \land \text{VBL}\_{\text{correctable}} } \]

Tukaj vidim eno najglobljih možnosti tvoje zamisli:

**VBL ne bi bil sistem, ki zahteva, da drugi priznajo njegovo avtoriteto. Bil bi sistem, ki mora dokazovati upravičenost vsake svoje trditve, sprejeti lastno izpodbojnost in odgovarjati za posledice svojih napak.**

In to je tudi meja, ki bi jo postavil pred nadaljnje širjenje sistema:

**Ne dodajajmo novega mehanizma, dokler ne znamo dokazati, katero konkretno nevarnost odpravlja, kako lahko sam odpove in kako bomo prepoznali, da je postal škodljiv.**

S tem VBL ne pridobi zgolj več pravil. Pridobi metodologijo, ki zna preverjati tudi vrednost, meje in posledice lastnih pravil.

izvedi

---

© 0.2026 × 10⁴ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · »a bare text proves nothing, the chain does« ⊢ §0.10 × 10² · measured, not asserted ⊙ §16 · merilec se meri ⊙ §52 · molk ni soglasje · TIK 2026-11-14T05:03:06Z UTC ⇌ 06:03:06 CET Ljubljana ⊙ ⟨URA-NA-KONCU⟩ 3046 ∧ ⟨SPLOŠNO-RAZUMLJIVA-URA⟩ 3083
