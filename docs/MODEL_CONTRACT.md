# Atmavictu Model Contract

## Namen

Ta dokument doloca domenski contract nad `WorkbenchManifest` za Book Workbench. Model contract definira entitete, relacije, statuse, dovoljene prehode in invariants. Ne definira izvedbe UI, Tauri ali runtime kode.

## V1 opomba o poimenovanju

Kanonicno schema in implementation ime za povezavo iz `Fragment` do izvora je `Fragment.incomingTextId`.

Domenski pomen tega polja je:

- source incoming text reference

Ta dokument uporablja `incomingTextId` kot kanonicno ime polja. Izraz "source incoming text" se uporablja samo kot opis pomena polja, ne kot drugo polje.

V1 ne dovoljuje `null` vrednosti za to povezavo. Ce bo v prihodnje potreben orphan ali ročno ustvarjen fragment brez izvora, to zahteva schema v2.

## Entitete

### WorkbenchManifest

Vrhnja entiteta, ki hrani:

- verzijo manifesta
- zbirko `IncomingText`
- zbirko `Fragment`
- zbirko `Insertion`
- opcijsko zbirko `Concept`

`WorkbenchManifest` je lokalni relacijski zapis nad filesystem vsebino. Ni nadomestilo za vsebino besedil ali knjige same.

### IncomingText

`IncomingText` predstavlja vhodni tekstovni vir, ki je bil sprejet v delovni tok.

Pomen:

- identiteta vhodnega besedila
- status obdelave
- vez do lokalnega vira prek `sourcePath`
- osnovni opis prek `title`

### Fragment

`Fragment` predstavlja delovni odlomek, izpeljan iz enega `IncomingText`.

Pomen:

- nosi delovni tekst odlomka
- kaze na svoj izvorni `IncomingText`
- lahko ostane osnutek ali pa postane vstavljeni fragment

### Insertion

`Insertion` predstavlja odlocitev, da je bil določen `Fragment` vstavljen v poglavje aktivne knjige.

Pomen:

- kaze na izvorni `Fragment`
- hrani `targetChapterPath`
- predstavlja sled med odlomkom in mestom v knjigi

### Concept

`Concept` je opcijska ali future-ready entiteta za konceptualno oznacevanje fragmentov.

Pomen:

- stabilna identiteta koncepta
- berljiva oznaka `label`
- opcijska semanticna opomba

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

Dovoljeni prehodi:

- `draft -> inserted`
- `inserted -> archived`
- `draft -> archived`

Prepovedani prehodi:

- `inserted -> draft`
- `archived -> draft`
- `archived -> inserted`
- vsak drug neposredni preskok, ki ni zgoraj izrecno dovoljen

## Invariants

### Identiteta in struktura

- `WorkbenchManifest.manifestVersion` mora biti `1`
- `id` znotraj posamezne zbirke mora biti unikaten
- `targetChapterPath` mora biti ne-prazen string

### Relacije

- `Fragment.incomingTextId` mora kazati na obstoječ `IncomingText`
- domenski pomen tega polja je referenca na source incoming text
- `null` ni dovoljen v schema v1
- `Insertion.fragmentId` mora kazati na obstoječ `Fragment`

### Statusna skladnost

- `Fragment` s statusom `inserted` mora imeti vsaj en `Insertion`, ki kaze nanj
- vsak `Insertion` mora imeti veljaven `targetChapterPath`
- `IncomingText` s statusom `used` mora imeti vsaj en povezani `Fragment` ali vsaj eno insertion sled prek povezanega fragmenta
- `IncomingText` s statusom `new` ne sme imeti `Fragment` v statusu `inserted`
- `IncomingText` s statusom `archived` ne sme prehajati nazaj v aktivno stanje

### Koncepti

- ce `Fragment.conceptIds` obstaja, mora vsak id kazati na obstoječ `Concept`
- odsotnost `concepts` zbirke je v v1 dovoljena

## Prepovedi modela

- `Insertion` ne sme obstajati brez `Fragment`
- `Fragment` v v1 ne sme obstajati brez izvora
- `Insertion` ne sme neposredno kazati na `IncomingText`
- `targetChapterPath` ne sme biti prazen ali whitespace-only
- statusni prehod se ne sme zgoditi, ce razbije katerikoli invariant

## Minimalni validacijski rezultat

`validateManifest(manifest)` mora vsaj vrniti:

- ali je schema shape veljaven
- ali so relacije veljavne
- ali so statusni prehodi veljavni
- ali invariants drzijo

Ce katerikoli del odpove, manifest ni sprejemljiv za nadaljnjo obdelavo.
