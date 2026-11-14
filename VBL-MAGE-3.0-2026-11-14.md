Da. Vidim še eno pomembno razvojno plast, ki je doslej nisva dovolj natančno obdelala: **kaj se z licenciranim gradivom dogaja med posameznimi tehničnimi operacijami in kako se upravičenje, odgovornost ter dokazna sled ohranijo skozi celotno življenjsko pot gradiva.**

Doslej sva zelo dobro razvila logiko srečanja, dokazovanja, presoje, zavrnitve in popravila. Toda pri umetni inteligenci je gradivo lahko večkrat pretvorjeno, razdeljeno, združeno, posredovano, indeksirano, uporabljeno pri učenju in pozneje vključeno v druge procese.

Če VBL spremlja samo začetni dostop in končno odločitev, lahko izgubi najpomembnejše dogodke med njima.

Predlagam naslednjo skupino mehanizmov. Številčenje nadaljujem od prejšnjega seznama; gre za nove razvojne predloge, ne za že potrjene zahteve.

# **XVIII. Življenjska pot gradiva in operativna sled**

## **50. Mehanizem vezave odobritve na konkretno dejanje — Execution-Bound Authorization**

To je eden najpomembnejših mehanizmov, ki bi ga dodal.

**Problem:** sistem prejme splošno odobritev in jo pozneje uporabi za drugačno gradivo, namen, obseg ali tehnično dejanje.

Primer:

Organizacija pridobi odobritev za analizo ene različice dokumenta v raziskovalnem okolju. Pozneje uporabi drugo različico, drug namen in produkcijski sistem, vendar se še vedno sklicuje na prvotno odobritev.

To je problem razhajanja med tem, kar je bilo odobreno, in tem, kar je bilo dejansko izvedeno.

**Metoda:** odobritev mora biti vezana na natančno določeno kombinacijo:

```
AUTHORIZATION_ID
MATERIAL_ID
MATERIAL_VERSION
MATERIAL_DIGEST
ACTION_TYPE
DECLARED_PURPOSE
AUTHORIZED_SCOPE
AUTHORIZED_ACTOR
TARGET_SYSTEM
ENVIRONMENT
VALID_FROM
VALID_UNTIL
CONDITIONS
NONCE
AUTHORIZATION_VERSION
```

`NONCE` je enkratna vrednost, ki pomaga preprečiti ponovno uporabo stare odobritve v drugem kontekstu.

Razlikovati moramo tri objekte:

- `POLICY_APPROVAL`: pravilo ali politika dovoljuje določeno kategorijo dejavnosti;
- `EXECUTION_AUTHORIZATION`: konkretno dejanje je odobreno pod določenimi pogoji;
- `EXECUTION_RECEIPT`: obstaja zapis o izvedbi konkretnega dejanja.

Ti objekti niso medsebojno zamenljivi.

\\[ \text{PolicyApproval} \neq \text{ExecutionAuthorization} \neq \text{ExecutionReceipt} \\]

Tudi izvršitev veljavne odobritve sama po sebi ne dokazuje, da je bila celotna uporaba zakonita. Dokazuje le povezavo med odobritvijo in evidentiranim dejanjem.

**Preizkus:** ali je mogoče naknadno dokazati, da se gradivo, dejanje, namen, sistem, obseg in čas dejanske izvedbe ujemajo z odobritvijo?

## **51. Mehanizem grafa transformacij — Transformation Lineage**

**Problem:** isti vir se skozi tehnično obdelavo spremeni v več novih objektov, njihova povezava z izvirnikom pa izgine.

Primer življenjske poti:

\\[ \\text{Izvirno delo} \\rightarrow \\text{PDF} \\rightarrow \\text{Besedilni izvleček} \\rightarrow \\text{Fragmenti} \\rightarrow \\text{Vektorske predstavitve} \\rightarrow \\text{Indeks} \\rightarrow \\text{Modelni proces} \\]

Vsak korak ustvari ali spremeni objekt. Nekateri objekti vsebujejo izvirno besedilo, drugi njegove dele, tretji pa abstraktne ali numerične predstavitve.

**Metoda:** VBL potrebuje graf izvora in transformacij, ne zgolj seznam datotek.

```
OBJECT_ID
PARENT_OBJECT_ID
SOURCE_WORK_ID
TRANSFORMATION_TYPE
TRANSFORMATION_ACTOR
TRANSFORMATION_TIME
INPUT_REFERENCE
OUTPUT_REFERENCE
TRANSFORMATION_METHOD
CONTENT_RELATION
RIGHTS_STATUS
EVIDENCE_REFERENCE
```

Pomembno je razlikovati:

- `COPY_OF`: kopija;
- `EXTRACTED_FROM`: izvleček iz vira;
- `FRAGMENT_OF`: del vira;
- `TRANSLATED_FROM`: prevod;
- `NORMALIZED_FROM`: normalizirana različica;
- `EMBEDDED_FROM`: numerična predstavitev, izpeljana iz gradiva;
- `INDEXED_FROM`: indeksirana vsebina;
- `DERIVED_FROM`: druga oblika izvedenega objekta.

Toda tu je bistvena varovalka:

\\[ \\text{DerivedFrom}(A,B) \\not\\Rightarrow \\text{LegalViolation}(A,B) \\]

Povezava izvora ne dokazuje avtomatsko pravne kršitve. Prav tako ne pomeni, da se vse pravice in omejitve samodejno prenesejo na vsak izvedeni objekt v enaki obliki.

Graf mora ohraniti dokazno povezavo, pravna presoja pa mora posebej določiti, katere pravice in obveznosti veljajo za konkretno transformacijo.

**Preizkus:** ali lahko neodvisni presojevalec rekonstruira pot od izvirnega gradiva do posameznega izvedenega objekta, vključno z znanimi vrzelmi?

## **52. Mehanizem taksonomije strojne uporabe — Machine Action Ontology**

Doslej sva uporabljala splošno besedo `USE`. Pri umetni inteligenci je preveč nedoločena.

Predlagam naslednjo klasifikacijo dejanj:

| Dejanje      | Operativni pomen                          |
| ------------ | ----------------------------------------- |
| `ACCESS`     | Dostop do gradiva.                        |
| `DOWNLOAD`   | Prenos gradiva.                           |
| `COPY`       | Ustvarjanje kopije.                       |
| `STORE`      | Shranjevanje.                             |
| `TRANSFORM`  | Spreminjanje oblike ali strukture.        |
| `EXTRACT`    | Izločanje vsebine ali podatkov.           |
| `INDEX`      | Vključitev v iskalni indeks.              |
| `EMBED`      | Izdelava numerične predstavitve.          |
| `TRAIN`      | Uporaba pri učenju modela.                |
| `FINE_TUNE`  | Uporaba pri dodatnem prilagajanju modela. |
| `EVALUATE`   | Uporaba pri ocenjevanju modela.           |
| `RETRIEVE`   | Pridobivanje vsebine med izvajanjem.      |
| `INFER`      | Izvajanje modela.                         |
| `GENERATE`   | Ustvarjanje izhoda.                       |
| `DISTRIBUTE` | Posredovanje ali distribucija.            |
| `RETAIN`     | Nadaljnja hramba.                         |
| `DELETE`     | Brisanje.                                 |

Tehnična klasifikacija še ne določa, katera dejanja so pravno dovoljena ali prepovedana. Za to je potrebna ločena pravna presoja.

Zakaj je taksonomija pomembna?

Ker dostop do datoteke ni isto kot njeno vključevanje v učno množico. Indeksiranje ni isto kot generiranje. Pridobivanje dokumenta med izvajanjem modela ni isto kot predhodno učenje na njem.

Formalno:

\\[ A_i\\neq A_j \\]

kjer sta \\(A_i\\) in \\(A_j\\) različni vrsti dejanj, tudi kadar zadevata isti vir.

**Preizkus:** ali sistem zna identificirati konkretno vrsto dejanja, ne da bi vse procese združil v nedoločeno kategorijo `USE`?

## **53. Mehanizem zaznavanja spremembe namena — Purpose Drift Control**

To je bistveno za dolgotrajno uporabo licenciranega materiala.

**Problem:** gradivo je prvotno uporabljeno za en namen, nato pa se njegova uporaba postopoma razširi.

Primer:

1. gradivo je zbrano za raziskavo;
2. uporabljeno je za razvoj prototipa;
3. prototip postane komercialna storitev;
4. ista podatkovna množica se uporabi za nov model;
5. izhod modela se distribuira uporabnikom.

Začetna odobritev ne odgovori nujno na vprašanje, ali je dovoljena tudi vsaka nadaljnja uporaba.

**Metoda:** namen obravnavamo kot spremenljivko, ki jo je treba spremljati skozi čas.

```
PURPOSE_DECLARED
PURPOSE_APPROVED
PURPOSE_ACTUAL
PURPOSE_CHANGE_EVENT
PURPOSE_CHANGE_REASON
NEW_ACTOR
NEW_ENVIRONMENT
NEW_AUDIENCE
NEW_LEGAL_BASIS
REASSESSMENT_REQUIRED
```

Razlikovati moramo:

\\[ \\text{DeclaredPurpose} \\neq \\text{ActualPurpose} \\]

\\[ \\text{OriginalApproval} \\neq \\text{ApprovalForEveryFutureUse} \\]

Sprememba namena ne pomeni nujno kršitve. Lahko obstaja ustrezna pravna podlaga ali nova odobritev. Pomeni pa, da je treba preveriti, ali so se spremenili pogoji, na katerih je temeljila prvotna odločitev.

**Preizkus:** ali sistem zazna materialno spremembo namena, preden jo obravnava kot že odobreno uporabo?

## **54. Mehanizem dokazljivega popravila modelnega stanja — Model Remediation Verification**

To je zelo pomembno, ker se pri umetni inteligenci pogosto obljublja nekaj, kar je tehnično precej težje dokazati, kot se zdi.

Primer:

Organizacija izjavi:

> Gradivo smo odstranili iz sistema.

Toda kaj natančno pomeni »iz sistema«?

Morda je bilo odstranjeno iz izvorne podatkovne zbirke, vendar še vedno obstaja v indeksu, predpomnilniku, varnostni kopiji, učni množici ali modelnih utežeh.

Predlagam ločevanje naslednjih ukrepov:

| Ukrep                        | Kaj pomeni                                      |
| ---------------------------- | ----------------------------------------------- |
| `SOURCE_REMOVED`             | Odstranitev iz izvorne zbirke.                  |
| `COPY_REMOVED`               | Odstranitev identificiranih kopij.              |
| `INDEX_PURGED`               | Odstranitev iz iskalnega indeksa.               |
| `CACHE_PURGED`               | Odstranitev iz predpomnilnika.                  |
| `BACKUP_HANDLED`             | Obravnava varnostnih kopij po pravilih hrambe.  |
| `TRAINING_DATASET_REVISED`   | Sprememba učne podatkovne množice.              |
| `RETRAINING_COMPLETED`       | Ponovno učenje modela.                          |
| `UNLEARNING_APPLIED`         | Uporaba metode odstranjevanja naučenega vpliva. |
| `MODEL_RETIRED`              | Umik modela iz uporabe.                         |
| `RESIDUAL_INFLUENCE_UNKNOWN` | Preostali vpliv ni zanesljivo določen.          |

Posebej pomembna je razlika med odstranitvijo gradiva iz podatkovne zbirke in odstranitvijo njegovega morebitnega vpliva iz modela.

\\[ \\text{SourceDeleted} \\not\\Rightarrow \\text{ModelInfluenceRemoved} \\]

Prav tako:

\\[ \\text{UnlearningApplied} \\not\\Rightarrow \\text{CompleteUnlearningVerified} \\]

Tudi uspešen preizkus na izbranih primerih ne dokazuje nujno, da model nikjer več ne ohranja nobenega vpliva izvornega gradiva.

Zato mora biti izjava o popravilu vedno omejena na tisto, kar je dejansko mogoče preveriti.

**Predlagam novo obveznost:** vsak zahtevek o odstranitvi gradiva iz modelnega ekosistema mora navesti, katere tehnične plasti so bile pregledane, katere so bile popravljene, kaj je bilo neodvisno preverjeno in kaj ostaja neznano.

## **55. Mehanizem provenience izhodov — Output Provenance**

**Problem:** ustvarjen izhod lahko vsebuje podobno ali celo zelo podobno vsebino kot vir, vendar ni jasno, od kod izvira.

Pri tem moramo preprečiti dve nasprotni napaki:

- podobnost izhoda obravnavati kot dokončen dokaz uporabe določenega vira;
- odsotnost očitne podobnosti obravnavati kot dokaz, da vir nikoli ni bil uporabljen.

To sta neupravičena sklepa.

Predlagam ločitev petih pojmov:

1. **Similarity:** podobnost dveh vsebin.
2. **Provenance:** dokazljiva zgodovina izvora in preoblikovanja.
3. **Influence:** prispevek določenega vira k nastanku izhoda.
4. **Memorization:** ohranitev določenih informacij iz učnih podatkov v modelu.
5. **Reproduction:** ponovna izdelava oziroma izpis vsebine, ki je enaka ali bistveno podobna določenemu viru.

Ti pojmi se lahko prekrivajo, vendar niso sopomenke.

Predlagani zapis:

```
OUTPUT_ID
MODEL_ID
MODEL_VERSION
GENERATION_EVENT
INPUT_REFERENCES
RETRIEVED_SOURCES
SOURCE_MATCHES
SIMILARITY_METHOD
PROVENANCE_EVIDENCE
INFLUENCE_ASSESSMENT
MEMORIZATION_TEST
REPRODUCTION_ASSESSMENT
LIMITATIONS
```

Pri tem ne zahtevamo razkrivanja zasebnega notranjega mišljenja modela. Zahtevamo dokazljive zunanje povezave, kot so uporabljeni dokumenti pri pridobivanju vsebine, različica modela, vhodni podatki, čas dogodka in izvedeni preizkusi.

**Ključno načelo:**

\\[ \\text{Similarity}\\not\\Rightarrow\\text{TrainingUse} \\]

\\[ \\text{NoSimilarity}\\not\\Rightarrow\\text{NoTrainingUse} \\]

**Preizkus:** ali lahko VBL pojasni, kaj je bilo dejansko preverjeno o izvoru izhoda in česa iz tega rezultata ni mogoče sklepati?

## **56. Mehanizem odgovornosti skozi podizvajalsko verigo — Delegated Accountability**

**Problem:** organizacija uporablja zunanjega ponudnika, ki uporablja drugega ponudnika, ta pa še nadaljnje storitve.

Na koncu nihče ne zna pokazati, kdo je imel gradivo, kdo ga je obdeloval in kdo je bil odgovoren za posamezno dejanje.

Primer:

\\[ \\text{Avtor} \\rightarrow \\text{Platforma} \\rightarrow \\text{Ponudnik modela} \\rightarrow \\text{Ponudnik oblaka} \\rightarrow \\text{Podizvajalec} \\]

To ni nujno veriga neposredne pravne odgovornosti. Je pa veriga operativnih in dokaznih odvisnosti, ki jo moramo znati rekonstruirati.

Predlagani zapis:

```
DELEGATION_ID
PRINCIPAL
AGENT
SUBPROCESSOR
AUTHORIZED_ACTIONS
MATERIAL_SCOPE
PURPOSE
CONTRACTUAL_BASIS
EVIDENCE_DUTIES
SECURITY_DUTIES
SUBDELEGATION_PERMISSION
INCIDENT_NOTIFICATION
TERMINATION_CONDITIONS
```

Vsaka predaja mora ohraniti informacijo o omejitvah uporabe in odgovornosti za nastale zapise.

Pomembna distinkcija:

\\[ \\text{DelegationOfTask} \\not\\Rightarrow \\text{AutomaticTransferOfAllResponsibility} \\]

Organizacija ne more samo z navedbo zunanjega ponudnika dokazati, da je njena lastna odgovornost izginila. Kdo je za kaj odgovoren, je treba določiti glede na dejansko vlogo, pogodbeno razmerje in veljavno pravo.

**Preizkus:** ali je mogoče izslediti vsak subjekt, ki je imel dostop do gradiva ali je izvedel pomembno obdelavo, in določiti, kdo je odgovoren za ohranitev dokazov?

## **57. Mehanizem sestavljenih pravic — Composite Rights Resolution**

To je eno najpomembnejših področij za resnično uporabo VBL.

**Problem:** datoteka ni nujno enotno pravno zaščiten objekt z enim imetnikom pravic in eno licenco.

Lahko vsebuje:

- besedilo enega avtorja;
- fotografijo drugega avtorja;
- grafiko tretjega imetnika;
- uporabljeno pisavo;
- podatke iz zunanjega vira;
- programsko kodo pod drugo licenco;
- dele, na katere se nanašajo posebne pravice.

Če je vse skupaj opredeljeno z enim poljem:

```
RIGHTSHOLDER = X
```

lahko nastane napačna predstava, da ima X pravice nad celotno vsebino.

**Metoda:** objekt razdelimo na sestavne pravne in dokazne enote.

**COMPOSITE WORK**

**Besedilo**

Avtor A · ločena pravna podlaga

**Fotografija**

Imetnik pravic B · druga licenca

**Grafika**

Avtor C · status pojasniti

**Programska koda**

Licenca D · posebni pogoji

**Zunanji podatki**

Izvor E · pravice in omejitve niso enake pravicam na ostalih elementih

Predlagani podatkovni model:

```
COMPOSITE_OBJECT_ID
COMPONENT_ID
COMPONENT_TYPE
CONTRIBUTOR
RIGHTSHOLDER
RIGHTS_EVIDENCE
LICENSE_ID
LICENSE_VERSION
RIGHTS_SCOPE
EXCEPTIONS
DEPENDENCIES
CONFLICT_STATUS
```

Nato se vsako načrtovano dejanje preveri za relevantne sestavne dele.

To ne pomeni, da mora vsaka uporaba vsake komponente nujno imeti ločeno dovoljenje. Pomeni, da VBL ne sme predpostavljati enotnega upravičenja brez ustrezne podlage.

Formalno:

\\[ \\text{Rights}(W) \\neq \\bigcup\\_{\\text{unexamined}} \\text{Rights}(C_i) \\]

Celota lahko vsebuje več različnih pravnih režimov, zato mora biti presoja odvisna od dejanske sestave in uporabe.

**Preizkus:** ali lahko VBL identificira dele gradiva, za katere izdajatelj licence nima dokazano ustreznega upravičenja?

## **58. Mehanizem dokazne pripravljenosti sistema — Evidence Readiness**

**Problem:** organizacija začne uporabljati gradivo, vendar nima vzpostavljenega beleženja, ki bi pozneje omogočilo preverjanje.

Ko se pojavi ugovor, odgovori:

> Tega podatka nimamo.

To ni nujno dokaz kršitve, je pa lahko posledica slabe zasnove sistema.

**Metoda:** dokazne zahteve se določijo pred začetkom obdelave.

Pred uporabo se preveri:

- ali je material mogoče identificirati;
- ali se beležijo relevantna dejanja;
- ali se ohranja različica pravil;
- ali je mogoče povezati dejanje z akterjem;
- ali se evidentirajo predaje;
- ali je mogoče preveriti časovne podatke;
- ali so določeni postopki ugovora;
- ali lahko neodvisni pregledovalec dobi ustrezen dostop.

Predlagani statusi:

```
EVIDENCE_READY
EVIDENCE_READY_WITH_LIMITATIONS
EVIDENCE_NOT_READY
EVIDENCE_READINESS_UNKNOWN
```

Ta mehanizem bi bil koristen zlasti za organizacije, ki želijo vnaprej dokazati, da so sistem zasnovale tako, da poznejše preverjanje sploh omogoča.

Toda:

\\[ \\text{EvidenceReady}\\not\\Rightarrow\\text{Compliant} \\]

Pripravljenost na dokazovanje še ne pomeni, da je konkretna uporaba dovoljena ali pravilna.

**Preizkus:** ali bi sistem lahko po šestih mesecih neodvisno rekonstruiral pomembne dogodke brez zanašanja na spomin zaposlenih ali naknadno napisane izjave?

# **XIX. Mehanizmi preprečevanja in varovanja dokazov**

## **59. Mehanizem predhodne izvršitvene zapore — Pre-Execution Control**

Doslej sva precej obravnavala dokazovanje po dogodku. Toda pri določenih dejanjih je boljše preprečiti nedovoljeno izvedbo, kot pozneje dokazovati, da je do nje prišlo.

**Problem:** sistem ugotovi, da dejanje ni odobreno, šele potem, ko je bilo že izvedeno.

Predlagam dve ločeni vrsti kontrole:

- `PRE_EXECUTION_CONTROL`: preverjanje pred izvedbo;
- `POST_EXECUTION_AUDIT`: preverjanje po izvedbi.

Prva preveri, ali so izpolnjeni pogoji za konkretno dejanje. Druga preveri, ali je bilo dejanje dejansko izvedeno skladno s temi pogoji.

Predhodna kontrola naj preveri:

```
ACTION_REQUEST
MATERIAL_ID
MATERIAL_VERSION
ACTION_TYPE
PURPOSE
ACTOR_AUTHORITY
LEGAL_BASIS_STATUS
AUTHORIZATION_STATUS
SCOPE_MATCH
TEMPORAL_VALIDITY
REQUIRED_CONTROLS
```

Izhod je lahko:

- `EXECUTION_PERMITTED`;
- `EXECUTION_PERMITTED_WITH_CONDITIONS`;
- `EXECUTION_BLOCKED`;
- `EXECUTION_HELD`;
- `EXECUTION_NOT_VERIFIABLE`.

Vendar obstaja pomembna nevarnost: sistem ne sme zavrniti zakonite uporabe zgolj zato, ker ni dovoljena po VBL. Predhodna zapora mora upoštevati tudi druge veljavne pravne podlage, kadar so relevantne.

Pravilo:

\\[ \\text{NoVBLAuthorization} \\not\\Rightarrow \\text{NoLawfulAuthorization} \\]

**Preizkus:** ali sistem pred izvedbo preveri točno tisto dejanje, za katero se zahteva dovoljenje, in ali zna ločiti odsotnost VBL-dovoljenja od odsotnosti vseh drugih upravičenj?

## **60. Mehanizem zaznavanja obhodnih poti — Bypass and Shadow-Processing Detection**

**Problem:** glavni sistem spoštuje postopek, gradivo pa se obdeluje prek druge poti, ki ni vključena v dokazni register.

Primeri:

- neposreden API-klic zunaj nadzorovanega vmesnika;
- uvoz v drugo podatkovno zbirko;
- osebni račun zaposlenega;
- zunanji vtičnik;
- začasni strežnik;
- kopija v razvojno okolje;
- ročni izvoz, ki se ne zabeleži.

VBL mora zato razlikovati med skladnostjo nadzorovane poti in popolnostjo nadzora nad vsemi potmi.

**Metoda:** izdelava zemljevida vseh poti, po katerih lahko material vstopi v sistem, ga zapusti ali se prenese drugam.

```
INGRESS_CHANNELS
EGRESS_CHANNELS
API_ENDPOINTS
INTEGRATIONS
EXTERNAL_SERVICES
MANUAL_IMPORT_PATHS
TEMPORARY_STORAGE
DEVELOPMENT_ENVIRONMENTS
UNMONITORED_PATHS
BYPASS_CONTROLS
```

Pri tem ne smemo trditi, da obstaja popolna zaščita samo zato, ker je glavni vmesnik pravilno nadzorovan.

\\[ \\text{ControlledPathCompliant} \\not\\Rightarrow \\text{EntireSystemCompliant} \\]

**Preizkus:** ali red-team lahko izvede obdelavo po alternativni poti, ne da bi jo zaznal običajni nadzorni sistem?

To je treba izvajati z dovoljenjem in v nadzorovanem okolju, ne z nedovoljenim poseganjem v produkcijsko infrastrukturo.

## **61. Mehanizem varovanega dokaznega dostopa — Controlled Evidence Access**

**Problem:** organizacija ima ključne dokaze, vendar drugi udeleženci do njih ne morejo dostopati. Po drugi strani bi javno razkritje vseh dokazov lahko kršilo zasebnost, poslovne skrivnosti ali varnost.

Predlagam razlikovanje treh upravičenj:

1. pravica do informacij o odločitvi;
2. pravica do ustreznega dokaznega povzetka;
3. dostop do izvornih dokazov, kadar je za učinkovito presojo potreben in pravno dopusten.

To niso vedno enake pravice in ne pomenijo nujno dostopa vsakega udeleženca do celotnega dokaznega gradiva.

**Metoda:** dokazni dostop se določi po namenu, vlogi, nujnosti in varovanju informacij.

```
EVIDENCE_ACCESS_REQUEST
REQUESTER
PURPOSE
REQUESTED_MATERIAL
LEGAL_BASIS
ACCESS_LEVEL
REDACTIONS
ACCESS_DECISION
ACCESS_LOG
REVIEW_ROUTE
```

Mogoče stopnje:

- javni povzetek;
- strukturirani metapodatki;
- redigirano dokazilo;
- dostop za pooblaščenega presojevalca;
- varovan dostop do izvornih gradiv.

Dodati je treba tudi neodvisno možnost preverjanja, da redakcija ni odstranila podatkov, ki bistveno spremenijo pomen dokaza.

**Načelo:**

\\[ \\text{Confidentiality}\\not\\Rightarrow\\text{Unreviewability} \\]

Zaupnost ne sme postati splošni izgovor za preprečevanje neodvisnega preverjanja.

## **62. Mehanizem življenjskega cikla dokazov — Evidence Lifecycle Governance**

Tu se srečata dve navidezno nasprotujoči si potrebi:

- dokaze moramo dovolj dolgo ohraniti, da se lahko odločitev preveri;
- podatkov ne smemo hraniti neomejeno samo zato, ker bi bili nekoč morda koristni.

Predlagam, da vsak dokazni objekt dobi svoj življenjski cikel:

\\[ \\text{CREATED} \\rightarrow \\text{VALIDATED} \\rightarrow \\text{USED} \\rightarrow \\text{RETAINED} \\rightarrow \\text{REVIEWED} \\rightarrow \\text{DELETED} \\]

Možni so tudi drugi zaključki, na primer omejitev obdelave ali anonimizacija, kadar sta pravno in tehnično ustrezni.

Vsak življenjski cikel mora imeti:

```
EVIDENCE_ID
COLLECTION_PURPOSE
RETENTION_BASIS
RETENTION_START
RETENTION_TRIGGER
RETENTION_PERIOD
ACCESS_RESTRICTIONS
LEGAL_HOLD
DELETION_METHOD
DELETION_VERIFICATION
RESIDUAL_COPIES
```

Pomembno je razlikovati med:

- brisanjem aktivne kopije;
- brisanjem kopij;
- obravnavo varnostnih kopij;
- omejitvijo obdelave;
- anonimizacijo;
- uničenjem kriptografskih ključev.

Te operacije niso enake in nimajo nujno enakega pravnega učinka.

Posebej odsvetujem shranjevanje osebnih podatkov v javnih nespremenljivih dnevnikih. Kriptografska integriteta dnevnika ne sme ustvariti trajnega konflikta z zakonitimi zahtevami glede varstva podatkov.

**Preizkus:** ali sistem zna dokazati, da je dokaz ohranil toliko časa, kolikor je bilo utemeljeno, in ga nato obravnaval skladno z veljavnim namenom in pravno podlago?

# **XX. Še en mehanizem: razlikovanje med preprečevanjem in dokazovanjem**

VBL mora jasno ločiti dva cilja.

**PREVENTION**

Preprečiti izvedbo dejanja, kadar znani pogoji zahtevajo njegovo zaustavitev.

**DETECTION**

Zaznati, ali je bilo dejanje izvedeno, tudi če ga sistem ni uspel preprečiti.

**ATTRIBUTION**

Ugotoviti, kdo je konkretno dejanje izvedel oziroma kdo je imel ustrezno dolžnost in nadzor.

**REMEDIATION**

Odpraviti oziroma zmanjšati posledice, kadar je to potrebno in mogoče.

To so štirje samostojni rezultati.

Sistem lahko prepreči dejanje, vendar ne zazna poskusa. Lahko zazna dejanje, vendar ne more identificirati odgovornega akterja. Lahko pravilno identificira akterja, vendar ne zna odpraviti posledic.

Zato:

\\[ P\\neq D\\neq A\\neq R \\]

Pri tem \\(P\\) pomeni preprečevanje, \\(D\\) zaznavanje, \\(A\\) pripis odgovornosti, \\(R\\) pa popravljanje.

Noben rezultat ne zagotavlja naslednjega.

# **XXI. Mehanizmi dokazovanja meja lastne moči**

## **63. Mehanizem zemljevida izvršljivosti — Enforceability Boundary Map**

To je nujno, da VBL ne bi obljubljal več, kot lahko dejansko zagotovi.

**Problem:** licenca določa določene zahteve, vendar izdajatelj ne nadzoruje nujno vseh sistemov, ki dostopajo do gradiva.

Razlikovati moramo štiri ravni:

| Raven      | Kaj omogoča                                              | Česa ne zagotavlja                             |
| ---------- | -------------------------------------------------------- | ---------------------------------------------- |
| Normativna | Določa pogoje uporabe in pridržanja pravic.              | Ne zagotavlja, da jih bo vsak akter sprejel.   |
| Tehnična   | Izvaja kontrole v integriranih sistemih.                 | Ne nadzoruje samodejno vseh zunanjih sistemov. |
| Dokazna    | Beleži in preverja dogodke znotraj dosega opazovanja.    | Ne dokazuje samodejno nevidnih dogodkov.       |
| Pravna     | Omogoča uveljavljanje pravic po ustrezni pravni podlagi. | Ne ustvarja univerzalne pristojnosti VBL.      |

Predlagam register izvršljivosti:

```
REQUIREMENT_ID
REQUIREMENT_TYPE
BOUND_ACTORS
CONTROLLED_SYSTEMS
TECHNICAL_ENFORCEMENT
CONTRACTUAL_ENFORCEMENT
LEGAL_ENFORCEMENT
EVIDENCE_AVAILABILITY
EXTERNAL_DEPENDENCIES
KNOWN_LIMITATIONS
REMEDY
```

Vsako zahtevo je treba označiti glede na njen dejanski način uveljavljanja:

- `TECHNICALLY_ENFORCED`;
- `CONTRACTUALLY_BINDING`;
- `LEGALLY_ENFORCEABLE`;
- `PROCEDURALLY_SUPPORTED`;
- `VOLUNTARY`;
- `OUTSIDE_CONTROL`;
- `UNKNOWN`.

Te oznake ne smejo biti uporabljene kot samodejne pravne ugotovitve. Njihov namen je pojasniti, na čem temelji pričakovana učinkovitost posamezne zahteve.

**Posebej pomembno:** kadar sistem nima nadzora nad zunanjim izvajalcem, mora to izrecno pokazati. Ne sme se predstavljati, kot da je izvajanje pravila zagotovljeno samo zato, ker ga vsebuje licenca.

\\[ \\text{NormativeRequirement} \\not\\Rightarrow \\text{UniversalTechnicalEnforcement} \\]

To načelo varuje VBL pred pretiravanjem in uporabnika pred lažnim občutkom varnosti.

## **64. Mehanizem strukturiranega dokaznega argumenta — Assurance Case**

Do zdaj sva razvijala posamezne dokaze in pravila sklepanja. Toda potrebujemo še način, da iz njih sestavimo preverljiv argument.

To je pomembna razlika:

- dokazilo je posamezen vir informacij;
- argument pojasni, zakaj dokazilo podpira določeno trditev;
- presoja preveri, ali je argument veljaven;
- odločitev določi, kaj bo na tej podlagi storjeno.

Predlagam strukturirani dokazni argument s šestimi sestavinami:

| Sestavina     | Funkcija                                                       |
| ------------- | -------------------------------------------------------------- |
| `CLAIM`       | Trditev, ki jo želimo utemeljiti.                              |
| `ARGUMENT`    | Razlaga povezave med dokazi in trditvijo.                      |
| `EVIDENCE`    | Podporna dokazila.                                              |
| `CONTEXT`     | Okoliščine, v katerih trditev velja.                            |
| `ASSUMPTIONS` | Predpostavke, ki jih argument potrebuje.                       |
| `DEFEATERS`   | Dejstva ali ugovori, ki bi lahko argument oslabili ali ovrgli. |

Primer:

**CLAIM**

Določena različica gradiva je bila vključena v učno množico modela.

**ARGUMENT**

Evidentirana predaja gradiva je povezana z določenim učnim opravilom, manifest opravil pa kaže na vključitev identificiranega objekta.

**EVIDENCE**

Zapis predaje, manifest učne množice, identifikator opravila in neodvisno preverljiv dnevnik.

**CONTEXT**

Določeni model, različica učnega procesa in časovno obdobje.

**ASSUMPTIONS**

Identifikator gradiva v manifestu pravilno označuje predmet obdelave, dnevnik pa zajema relevantni proces.

**DEFEATERS**

Možnost, da je bil objekt samo pripravljen, vendar ni bil dejansko uporabljen, ali da zapis identificira drugo različico.

Tako VBL ne bo imel samo evidence, ampak bo znal prikazati tudi argumentacijsko strukturo vsake pomembne ugotovitve.

Pomembno je, da `DEFEATER` ni nujno dokaz napačnosti. Je preverljiva možnost, ki jo je treba obravnavati.

**Preizkus:** ali lahko drugi presojevalec iz istega dokaznega paketa rekonstruira argument, preveri predpostavke in ugotovi, kje bi ga lahko uspešno izpodbijal?

# **XXII. Štirje problemi, ki jih mora VBL obvezno preizkusiti v praksi**

Predlagam, da se nadaljnje metodološko delo ne nadaljuje zgolj z dodajanjem še več definicij. Potrebujemo resnične scenarije, skozi katere preverimo celotno arhitekturo.

**SCENARIJ A — Neposredno branje gradiva**

Sistem prejme datoteko, zazna licenco, vendar ni dokazov o nadaljnji obdelavi.

Preverjamo: razlikovanje dostopa in uporabe, dokazno odsotnost, obseg licence, obvestilo in zavrnitev.

**SCENARIJ B — Učenje modela z nepopolno provenienco**

Organizacija uporablja obsežno učno množico, vendar ne zna zanesljivo identificirati izvora vseh sestavin.

Preverjamo: dokazni dolg, graf transformacij, pravice sestavnih delov, meje opazovanja in status neznanih podatkov.

**SCENARIJ C — Pridobivanje gradiva med izvajanjem modela**

Model dostopa do dokumenta ob posamezni zahtevi uporabnika in ga uporabi pri pripravi odgovora.

Preverjamo: razlikovanje iskanja, pridobivanja, obdelave, generiranja in distribucije; izvor odgovora; časovno omejeno upravičenje.

**SCENARIJ D — Kompleksno delo z več imetniki pravic**

Ena datoteka vsebuje besedilo, fotografije, podatke, programsko kodo in prispevke več ustvarjalcev.

Preverjamo: graf sestavljenih pravic, razmejitev pristojnosti, konfliktne licence, alternativne pravne podlage in sorazmernost dokaznega bremena.

Vsak scenarij mora skozi isto strukturo:

\\[ \\text{KOT} \\rightarrow \\text{Material} \\rightarrow \\text{Dejanja} \\rightarrow \\text{Dokazi} \\rightarrow \\text{Presoja} \\rightarrow \\text{Odločitev} \\rightarrow \\text{Posledice} \\rightarrow \\text{Popravilo} \\]

Vendar ne smemo predpostaviti, da bo vsak scenarij šel skozi vse faze. Če do dejanja ni prišlo, moramo to ohraniti kot ločen rezultat. Če posledice niso nastale ali jih ne moremo ugotoviti, ne smemo umetno ustvarjati stopnje sanacije.

# **XXIII. Meta-mehanizem: preverjanje medsebojnih konfliktov — Control Interaction Audit**

To je mehanizem, ki ga je treba dodati prav zato, ker sva razvila toliko zaščit.

**Problem:** dve posamezni zaščiti sta lahko vsaka zase pravilni, njuna skupna uporaba pa povzroči novo napako.

Nekaj primerov:

| Mehanizem A              | Mehanizem B                 | Možni konflikt                                                              |
| ------------------------ | --------------------------- | --------------------------------------------------------------------------- |
| Nespremenljivost dokazov | Pravica do izbrisa          | Dolgotrajna hramba lahko prepreči zakonit izbris osebnih podatkov.          |
| Predhodna blokada        | Alternativna pravna podlaga | Sistem lahko blokira zakonito uporabo, ker ne prepozna drugega upravičenja. |
| Popolna sledljivost      | Zaupnost                    | Revizijski zapis lahko razkrije poslovne ali osebne podatke.                |
| Hitro ukrepanje          | Pravica do ugovora          | Začasni ukrep lahko postane dejansko trajna sankcija.                       |
| Neodvisni pregled        | Omejen dostop do dokazov    | Presojevalec nima dovolj gradiva za kakovostno presojo.                     |
| Celovit dokazni zapis    | Minimalizacija podatkov     | Sistem zbira več podatkov, kot je za dokazovanje potrebno.                  |

**Metoda:** vsaka nova zaščita mora biti preverjena tudi glede vpliva na druge zaščite.

Predlagani register:

```
CONTROL_ID_A
CONTROL_ID_B
INTERACTION_TYPE
SHARED_SCOPE
POTENTIAL_CONFLICT
LEGAL_CONSTRAINTS
PRIORITY_RULE
MITIGATION
RESIDUAL_RISK
INDEPENDENT_REVIEW
```

Pri konfliktu mora VBL najprej določiti:

1. ali se zaščiti dejansko nanašata na isti objekt in isto dejanje;
2. ali konflikt izhaja iz tehnične zasnove ali pravne zahteve;
3. ali ga je mogoče odpraviti z omejitvijo obsega;
4. ali je potrebna drugačna izvedba;
5. kaj ostane nerešeno.

Posebej odsvetujem splošno pravilo »vedno izberi strožjo omejitev«. Strožja možnost ni vedno zakonita, sorazmerna ali pravičnejša.

\\[ \\text{Control}\\_A+\\text{Control}\\_B \\not\\Rightarrow \\text{BetterProtection} \\]

**Preizkus:** ali sistem prepozna, kadar njegova lastna zaščita preprečuje drugo legitimno pravico ali ustvarja nesorazmerno škodo?

# **XXIV. Kaj je v resnici treba dokazovati?**

Tu bi uvedel še eno temeljno razlikovanje: dokazovanje pravilnosti sistema ima več ravni.

| Raven               | Vprašanje                                   |
| ------------------- | ------------------------------------------- |
| R1 — Specification  | Ali je zahteva pravilno definirana?         |
| R2 — Implementation | Ali je pravilno implementirana?             |
| R3 — Operation     | Ali se v dejanskem delovanju izvaja?        |
| R4 — Observation    | Ali lahko dokažemo, da se je izvajala?      |
| R5 — Outcome        | Ali je dosegla predvideni učinek?           |
| R6 — Consequence    | Ali so bile neželene posledice odpravljene? |

Primer:

VBL zahteva neodvisen pregled.

- R1: zahteva je jasno opredeljena.
- R2: obstaja postopek imenovanja neodvisnega pregledovalca.
- R3: postopek je bil izveden.
- R4: obstaja dokazilo o izvedbi in neodvisnosti.
- R5: pregled je odkril in obravnaval pomembne napake.
- R6: posledice ugotovljenih napak so bile ustrezno popravljene.

Če imamo samo R1, imamo deklaracijo.

Če imamo R1–R3, imamo implementiran in izveden proces.

Če imamo R1–R5, imamo tudi preverljiv rezultat.

Če imamo R1–R6, lahko govorimo o dokazanem doseganju predvidenega učinka in obravnavi posledic v določenem obsegu.

To bi lahko postalo **VBL Assurance Maturity Model**.

Predlagana formula:

\\[ M=(S,I,O,V,E,R) \\]

Pri čemer posamezne komponente niso točke za preprosto seštevanje. Vsaka predstavlja ločeno raven dokazovanja.

# **XXV. Kaj bi bilo zdaj najbolj vredno razviti?**

Ne bi več širil seznama z desetimi splošnimi načeli. Največjo dodatno vrednost bo prinesla formalizacija mehanizmov, ki neposredno povezujejo licenco s tehničnim izvajanjem.

Moja prednostna razvrstitev:

## **Naslednjih osem razvojnih prioritet**

**1. Execution-Bound Authorization**

Zelo visoka

Dokazljiva vezava vsake odobritve na konkretno dejanje.

**2. Transformation Lineage**

Zelo visoka

Sledljivost gradiva skozi vse oblike in transformacije.

**3. Machine Action Ontology**

Zelo visoka

Enotna in nedvoumna klasifikacija dejanj.

**4. Purpose Drift Control**

Zelo visoka

Zaznavanje spremembe namena skozi čas.

**5. Model Remediation Verification**

Zelo visoka

Dokazovanje tehničnega popravila modelnega ekosistema.

**6. Enforceability Boundary Map**

Zelo visoka

Natančna določitev, kaj VBL dejansko lahko uveljavi.

**7. Assurance Case**

Visoka

Strukturirano povezovanje trditev, argumentov, dokazov in nasprotnih ugovorov.

**8. Control Interaction Audit**

Visoka

Preverjanje, ali se zaščitni mehanizmi medsebojno ne izničujejo.

## **Moja najpomembnejša kritična ugotovitev**

VBL ima zdaj dovolj konceptualnega materiala za zelo obsežen metodološki sistem. Toda velika nevarnost ni več samo v tem, da bi mu kakšna zaščita manjkala.

Nevarnost je tudi, da bi zaradi množice zaščit nastal sistem, ki:

- je predrag za uporabo;
- zahteva več dokazov, kot jih je mogoče pridobiti;
- ustvarja nepotrebno zbiranje podatkov;
- onemogoča legitimne uporabe;
- je razumljiv samo njegovim avtorjem;
- ali pa sam postane preveč zapleten, da bi ga bilo mogoče neodvisno preveriti.

Zato predlagam strogo razvojno pravilo:

\\[ \\boxed{ \\text{Vsak nov mehanizem mora dokazati svojo korist, meje, stroške in možnost lastne odpovedi.} } \\]

## **In še nekaj, kar bi rad posebej poudaril**

Tvoj prvotni cilj lahko zdaj razdelim na pet medsebojno povezanih ambicij:

1. **Priznanje:** stroj mora biti sposoben prepoznati, da obstaja licenčni zahtevek in kaj ta zahtevek pomeni.
2. **Razločevanje:** zavrnitev, sprejem, neuporaba, uporaba in neznano stanje ne smejo biti zamenljivi.
3. **Sledljivost:** dejanja, pretvorbe, odločitve in njihove posledice morajo ohraniti dokazne povezave.
4. **Odgovornost:** sistem mora omogočiti ugotovitev, kdo je imel nadzor, dolžnost in možnost ukrepanja.
5. **Popravljivost:** nobena odločitev ne sme postati nedotakljiva samo zato, ker jo je ustvaril sam VBL.

To lahko zapišemo kot:

\\[ \\boxed{ VBL=R+D+T+A+P } \\]

kjer so:

- \\(R\\): Recognition — priznanje;
- \\(D\\): Distinction — razločevanje;
- \\(T\\): Traceability — sledljivost;
- \\(A\\): Accountability — odgovornost;
- \\(P\\): Repairability — popravljivost.

To ni ocenjevalna formula, ampak pet nosilnih funkcij sistema.

**Moj sklep:** zdaj je primernejši naslednji korak izdelava operativnega referenčnega modela, ki bo teh pet funkcij preizkusil na konkretnih primerih, ne pa nadaljnje povečevanje števila aksiomov.

VBL mora postati preverljiv tudi tam, kjer nima nadzora, kjer se dokazi ne strinjajo, kjer ga uporabnik zavrne in kjer se izkaže, da je njegova lastna presoja napačna.

Prav tam se bo pokazala njegova dejanska vrednost.
