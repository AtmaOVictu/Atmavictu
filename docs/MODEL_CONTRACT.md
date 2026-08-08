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

## Entitete
## Entitete

### WorkbenchManifest

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

### Fragment

`Fragment` predstavlja delovni odlomek, izpeljan iz enega `IncomingText`.

Pomen:

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
- `Fragment.title`, `Fragment.text`, `Fragment.note`
- `Insertion.targetChapterPath`, `Insertion.positionNote`, `Insertion.note`

Vsaka update operacija mora po zakljucku pustiti manifest v veljavnem stanju (snapshot validation). Statusni prehodi iz poglavja "Statusi in dovoljeni prehodi" se ne spreminjajo.

## Vrste validacije
## Vrste validacije

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
