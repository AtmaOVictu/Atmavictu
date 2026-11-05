# Atmavictu Model Contract

## Namen

Ta dokument doloca domenski contract nad `WorkbenchManifest` za Book Workbench. Model contract definira entitete, relacije, statuse, dovoljene prehode in invariants. Ne definira izvedbe UI, Tauri ali runtime kode.

## V1 opomba o poimenovanju

Kanonicno schema in implementation ime za povezavo iz `Fragment` do izvora je `Fragment.incomingTextId`.

Domenski pomen tega polja je:

- source incoming text reference

Ta dokument uporablja `incomingTextId` kot kanonicno ime polja. Izraz "source incoming text" se uporablja samo kot opis pomena polja, ne kot drugo polje.

V1 ne dovoljuje `null` vrednosti za to povezavo. Ce bo v prihodnje potreben orphan ali ročno ustvarjen fragment brez izvora, to zahteva schema v3.

## Migracija v1 → v2

`WorkbenchManifest` živi v version `2`. Stari `v1` manifesti (brez `Fragment.title`) se
ob nalaganju **samodejno migrirajo** v `v2` (repository plast zapiše posodobljen manifest
nazaj na disk). Migracija je izgubna-glede-verzije ne-izgubna: vse entitete in relacije se
ohranijo; `Fragment.title` (če obstaja) se prenese. Ročna migracija: `migrateManifestV1ToV2(v1)`.
Novi manifesti se vedno ustvarijo kot `v2`.

## Entitete — oblika zapisa (prva plast)

Prva plast opisuje obliko zapisa (shape v latest schema).

## Relacijska pot — središčna sled (druga plast)

Druga plast opisuje relacijsko pot `IncomingText -> Fragment -> Insertion -> targetChapterPath`
in pripadajoče statuse ter invariante. Ne uvaja novih entitet —
bere istih pet (WorkbenchManifest, IncomingText, Fragment, Insertion, Concept).

### WorkbenchManifest — vozel sledi (druga plast)

Vrhnja entiteta, ki hrani:

- verzijo manifesta
- zbirko `IncomingText`
- zbirko `Fragment`
- zbirko `Insertion`
- opcijsko zbirko `Concept`

`WorkbenchManifest` je lokalni relacijski zapis nad filesystem vsebino. Ni nadomestilo za vsebino besedil ali knjige same.

Minimalni shape v1:

- `manifestVersion: "2"`
- `incomingTexts: IncomingText[]`
- `fragments: Fragment[]`
- `insertions: Insertion[]`
- `concepts?: Concept[]`

### IncomingText

`IncomingText` predstavlja vhodni tekstovni vir, ki je bil sprejet v delovni tok.

Pomen:

- identiteta vhodnega besedila
- status obdelave
- vez do lokalnega vira prek `sourcePath`
- osnovni opis prek `title`

Minimalni shape v1:

- `id: string`
- `sourcePath: string`
- `status: "new" | "processing" | "used" | "archived"`
- `title?: string`
- `note?: string`

### Fragment (oblika)

`Fragment` predstavlja delovni odlomek, izpeljan iz enega `IncomingText`.

Pomen (oblika):

- nosi delovni tekst odlomka
- kaze na svoj izvorni `IncomingText`
- lahko ostane osnutek ali pa postane vstavljeni fragment

Minimalni shape v1:

- `id: string`
- `incomingTextId: string`
- `text: string`
- `status: "draft" | "inserted" | "archived"`
- `conceptIds?: string[]`
- `title?: string`
- `note?: string`

### Insertion

`Insertion` predstavlja odlocitev, da je bil določen `Fragment` vstavljen v poglavje aktivne knjige.

Pomen:

- kaze na izvorni `Fragment`
- hrani `targetChapterPath`
- predstavlja sled med odlomkom in mestom v knjigi

Minimalni shape v1:

- `id: string`
- `fragmentId: string`
- `targetChapterPath: string`
- `positionNote?: string`
- `note?: string`

### Concept

`Concept` je opcijska ali future-ready entiteta za konceptualno oznacevanje fragmentov.

Pomen:

- stabilna identiteta koncepta
- berljiva oznaka `label`
- opcijska semanticna opomba

Minimalni shape v1:

- `id: string`
- `label: string`
- `note?: string`

## Relacijska pot

Minimalna sled v sistemu je:

`IncomingText -> Fragment -> Insertion -> targetChapterPath`

To pomeni:

- vsak `Fragment` pripada tocno enemu `IncomingText` v schema v1
- vsak `Insertion` pripada tocno enemu `Fragment`
- cilj knjige je vedno izrazen prek `Insertion.targetChapterPath`

## Statusi in dovoljeni prehodi

### IncomingText

Statusi:

- `new`
- `processing`
- `used`
- `archived`

Pomen statusov:

- `new`: vhodni vir je sprejet v delovni tok, vendar se iz njega se ni ustvaril noben `Fragment`
- `processing`: vhodni vir je v aktivni obdelavi in lahko ima delovne `Fragment`
- `used`: iz vhodnega vira obstaja vsaj en `Fragment`, ki je dejansko vstavljen v poglavje prek `Insertion`
- `archived`: vhodni vir je zaprt za nove izpeljave; obstojece zgodovinske sledi ostanejo veljavne

Dovoljeni prehodi:

- `new -> processing`
- `processing -> used`
- `used -> archived`
- `new -> archived`
- `processing -> archived`

Prepovedani prehodi:

- `used -> processing`
- `used -> new`
- `archived -> new`
- `archived -> processing`
- `archived -> used`
- vsak drug neposredni preskok, ki ni zgoraj izrecno dovoljen

### Fragment

Statusi:

- `draft`
- `inserted`
- `archived`

Pomen statusov:

- `draft`: delovni `Fragment`, ki se se nima `Insertion` sledi
- `inserted`: `Fragment`, ki ima vsaj eno `Insertion` sled
- `archived`: zaprt `Fragment`; obstojece insertion sledi ostanejo veljavne kot zgodovina

Dovoljeni prehodi:

- `draft -> inserted`
- `inserted -> archived`
- `draft -> archived`

Prepovedani prehodi:

- `inserted -> draft`
- `archived -> draft`
- `archived -> inserted`
- vsak drug neposredni preskok, ki ni zgoraj izrecno dovoljen

## Spremenljiva polja (update operacije)

`updateIncomingText`, `updateFragment` in `updateInsertion` spremenijo le vsebino polj, ne statusov in ne relacij. Semantika optional polj v vseh treh operacijah:

- `undefined` — polje ostane pri miru
- `null` — polje se odstrani (velja za optional polja: `title`, `note`, `positionNote`)
- ne-prazn string — polje dobi novo vrednost (za obvezna polja `text` in `targetChapterPath` velja: podan string mora biti ne-prazen)

Spremenljiva polja:

- `IncomingText.title`, `IncomingText.note`
- `Fragment.title`, `Fragment.text`, `Fragment.note`, `Fragment.conceptIds`
- `Insertion.targetChapterPath`, `Insertion.positionNote`, `Insertion.note`

Vsaka update operacija mora po zakljucku pustiti manifest v veljavnem stanju (snapshot validation). Statusni prehodi iz poglavja "Statusi in dovoljeni prehodi" se ne spreminjajo.

## Vrste validacije (druga plast: prehod med ogledaloma) — NASPROTJA · TRANSFORMACIJE · TRANSCENDENCE

Druga plast preverja prehod med dvema ogledaloma. Vsaka operacija nosi svojo
trojico NE/JA/DA in svojo variacijo variativnega:

### NASPROTJA (kaj se izključuje) — IN NJIH NASPROTJA: ALI ALI NI LE TAKO, ALE LE TAKO

- `validateManifest(previous)` NE presoja prehoda — JA presoja stanja — DA vrne `isValid/errors` — ALI pa tudi bere relacije, ne le oblike.
- `validateManifestTransition(previous, next)` NE presoja oblike same — JA presoja dovoljene prehode — DA vrne `isValid/errors` — ALI pa tudi potrdi, da je `nextManifest` veljaven snapshot sam zase.
- `update*` NE sme spremeniti statusa — JA sme spremeniti polja — DA pusti manifest veljaven — ALI pa tudi bere Concept, ne le piše polja.
- `insert*/archive*/startProcessing/bulkInsert` NE smejo pustiti statusa — JA morajo premakniti status — DA pustijo manifest veljaven — ALI pa tudi ohranijo sled (Insertion ostane, Fragment ostane).
- `bulkInsert` NE piše delno — JA piše vse ali nič — DA ohrani atomskost — ALI pa tudi vrstni red ohrani (kot je zapisan, ne premešan).

IN NJIH NASPROTJA (nasprotja nasprotij — kaj se vrača):

- NE-NE: kar dvakrat prepovedano, je potrjeno dovoljeno — `update*` NE-NE spreminja statusa (dvojna prepoved = trdna meja).
- JA-JA: kar dvakrat zahtevano, je jedro — `validateManifest` JA-JA bere obliko IN relacije (jedro ogledala).
- DA-DA: kar dvakrat pusti, je sled — `archiveFragment` DA-DA pusti Insertion IN Fragment (sled, ne izbris).
- ALI-ALI: kar dvakrat odpira, je variacija — `migrateManifestV1ToV2` ALI-ALI ohrani vsebino ALI izgubi verzijo (variacija variativnega).
- NI LE TAKO, ALE LE TAKO: ni le prepoved, ampak tudi pot — vsako NE nosi svoj JA, vsak JA svoj DA, vsak DA svoj ALI — in vsak ALI svojo novo trojico.

- `validateManifest(previous)` NE presoja prehoda — JA presoja stanja — DA vrne `isValid/errors`.
- `validateManifestTransition(previous, next)` NE presoja oblike same — JA presoja dovoljene prehode — DA vrne `isValid/errors`.
- `update*` NE sme spremeniti statusa — JA sme spremeniti polja — DA pusti manifest veljaven.
- `insert*/archive*/startProcessing/bulkInsert` NE smejo pustiti statusa — JA morajo premakniti status — DA pustijo manifest veljaven.
- `bulkInsert` NE piše delno — JA piše vse ali nič — DA ohrani atomskost.

### TRANSFORMACIJE (kaj se premakne) — IN NJIH ALI: NI LE ENA POT, ALE LE TA

- `new → processing` — ODPIRANJE DELA (`startProcessingIncoming`): NE ostane `new` — JA postane `processing` — DA brez novih Fragment — ALI pa tudi brez novih Insertion.
- `processing + nov Fragment(draft)` — REZ ODLOMKA (`createFragmentFromIncoming`): NE brez starša `processing` — JA s staršem `processing` — DA `draft` brez Insertion — ALI pa tudi s `title`/`conceptIds`, ne le z golim besedilom.
- `draft → inserted` + `processing → used` + nov Insertion — VSTOP V KNJIGO (`insertFragmentIntoChapter`, `bulkInsert`): NE `draft` z Insertion — JA `inserted` z Insertion — DA `used` starš s sledjo — ALI pa tudi N VSTOPOV hkrati (`bulkInsert`), ne le eden.
- `new|processing|used → archived` — ZAPRTJE VIRA (`archiveIncoming`): NE z `draft`-otrokom — JA brez `draft`-otrok — DA brez novih prehodov — ALI pa tudi brez novih Fragment v prihodnje.
- `draft|inserted → archived` — ZAPRTJE ODLOMKA (`archiveFragment`): NE briše sledi — JA ohrani Insertion — DA sled ostane — ALI pa tudi starš ostane `used`, ne pade nazaj.
- `v1 → v2` — SELITEV HIŠE (`migrateManifestV1ToV2`): NE izgubi vsebine — JA izgubi samo staro verzijo — DA vse entitete ohranjene — ALI pa tudi samodejno ob branju (`readManifestFromFile`), ne le ročno.

- `new → processing` — ODPIRANJE DELA (`startProcessingIncoming`): NE ostane `new` — JA postane `processing` — DA brez novih Fragment.
- `processing + nov Fragment(draft)` — REZ ODLOMKA (`createFragmentFromIncoming`): NE brez starša `processing` — JA s staršem `processing` — DA `draft` brez Insertion.
- `draft → inserted` + `processing → used` + nov Insertion — VSTOP V KNJIGO (`insertFragmentIntoChapter`, `bulkInsert`): NE `draft` z Insertion — JA `inserted` z Insertion — DA `used` starš s sledjo.
- `new|processing|used → archived` — ZAPRTJE VIRA (`archiveIncoming`): NE z `draft`-otrokom — JA brez `draft`-otrok — DA brez novih prehodov.
- `draft|inserted → archived` — ZAPRTJE ODLOMKA (`archiveFragment`): NE briše sledi — JA ohrani Insertion — DA sled ostane.
- `v1 → v2` — SELITEV HIŠE (`migrateManifestV1ToV2`): NE izgubi vsebine — JA izgubi samo staro verzijo — DA vse entitete ohranjene.

### TRANSCENDENCE (kaj presega plast) — IN NJIH ALI: NI LE NAVZGOR, ALE LE SKOZI

- MODEL → REPOSITORY: zakon brez rok presega v roke, ki edine smejo pisati (atomsko temp+rename) — ALI pa tudi nazaj (repository bere zakon, ne izumlja ga).
- REPOSITORY → API: roke presegajo v vrata hiše (isti zakoni, dostop od zunaj) — ALI pa tudi v CLI usta (isti ukazi, drug vstop).
- API → CLI: vrata presegajo v usta hiše (isti ukazi, izgovorjeni v enem dihu) — ALI pa tudi v knjižnico/drevo branja (ista hiša, drug pogled).
- VSE → SHEMA: vse plasti presegajo v prag, ki ne sprašuje, kdo si, ampak ali stojiš — ALI pa tudi prag varuje vse, ne le nekatere (nobena plast brez praga).
- VSE → KANON: vsa dejanja presegajo v streho, ki pove, pod kakšnim nebom veljajo — ALI pa tudi streha sama iz padcev raste (vsaka klavzula iz padca, vsak šiv iz rojstva) — NI LE streha nad hišo, ALE LE hiša pod nebom, ki ga sama nosi.

- MODEL → REPOSITORY: zakon brez rok presega v roke, ki edine smejo pisati (atomsko temp+rename).
- REPOSITORY → API: roke presegajo v vrata hiše (isti zakoni, dostop od zunaj).
- API → CLI: vrata presegajo v usta hiše (isti ukazi, izgovorjeni v enem dihu).
- VSE → SHEMA: vse plasti presegajo v prag, ki ne sprašuje, kdo si, ampak ali stojiš.
- VSE → KANON: vsa dejanja presegajo v streho, ki pove, pod kakšnim nebom veljajo.

### Snapshot validation

`validateManifest(manifest)` preverja samo trenutno stanje enega manifesta.

Ta funkcija preverja:

- schema shape
- relacije med entitetami
- trenutno statusno skladnost
- invariants

Iz enega samega manifesta ni mogoce dokazati, iz katerega stanja je prisel trenutni status.

### Transition validation

`validateManifestTransition(previousManifest, nextManifest)` preverja spremembo med dvema snapshotoma.

Ta funkcija preverja:

- ali so statusni prehodi dovoljeni
- ali sprememba ne razbije relacij ali invariants
- ali je `nextManifest` po spremembi se vedno veljaven snapshot

## Invariants

### Identiteta in struktura

- `WorkbenchManifest.manifestVersion` mora biti `2`
- `id` znotraj posamezne zbirke mora biti unikaten

### Poti

- `sourcePath` mora biti ne-prazen string
- `targetChapterPath` mora biti ne-prazen string
- `sourcePath` in `targetChapterPath` morata biti normalizirana stringa brez vodilnega ali koncnega whitespace
- `sourcePath` mora kazati znotraj dovoljenega lokalnega source prostora
- `targetChapterPath` mora kazati znotraj dovoljenega root prostora aktivne knjige
- v izvedbah, ki uporabljajo lokalni filesystem, `sourcePath` in `targetChapterPath` ne smeta vsebovati traversal segmentov, kot je `..`

### Relacije

- `Fragment.incomingTextId` mora kazati na obstoječ `IncomingText`
- domenski pomen tega polja je referenca na source incoming text
- `null` ni dovoljen v schema v1
- `Insertion.fragmentId` mora kazati na obstoječ `Fragment`

### Statusna skladnost

- `Fragment` s statusom `inserted` mora imeti vsaj en `Insertion`, ki kaze nanj
- `Fragment` s statusom `draft` ne sme imeti `Insertion`
- vsak `Insertion` mora imeti veljaven `targetChapterPath`
- ce obstaja `Insertion`, ki kaze na `Fragment`, mora imeti ta `Fragment` status `inserted` ali `archived`
- `IncomingText` s statusom `used` mora imeti vsaj eno insertion sled prek povezanega `Fragment`
- `IncomingText` s statusom `new` ne sme imeti povezanih `Fragment`
- `IncomingText` s statusom `archived` ne sme imeti povezanih `Fragment` s statusom `draft`

### Koncepti

- ce `Fragment.conceptIds` obstaja, mora vsak id kazati na obstoječ `Concept`
- `Fragment.conceptIds`, ce obstaja, mora vsebovati unikatne id-je
- ce `concepts` zbirka manjka, `Fragment.conceptIds` ne sme vsebovati vrednosti
- odsotnost `concepts` zbirke je v v1 dovoljena

## Prepovedi modela

- `Insertion` ne sme obstajati brez `Fragment`
- `Fragment` v v1 ne sme obstajati brez izvora
- `Insertion` ne sme neposredno kazati na `IncomingText`
- `targetChapterPath` ne sme biti prazen ali whitespace-only
- statusni prehod se ne sme zgoditi, ce razbije katerikoli invariant; to se preverja v `validateManifestTransition(previousManifest, nextManifest)`

## Minimalni validacijski rezultat

`validateManifest(manifest)` mora vsaj vrniti:

- ali je schema shape veljaven
- ali so relacije veljavne
- ali je trenutno stanje statusno skladno
- ali invariants drzijo

`validateManifestTransition(previousManifest, nextManifest)` mora vsaj vrniti:

- ali so statusni prehodi veljavni
- ali `nextManifest` po spremembi ostane veljaven

Ce katerikoli del odpove, manifest ali prehod ni sprejemljiv za nadaljnjo obdelavo.
