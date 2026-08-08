# Atmavictu Service Contract

## Namen

Ta dokument doloca minimalne operacije nad `WorkbenchManifest`. Service contract opisuje dovoljene posege v model, ne pa konkretne implementacije v TypeScriptu ali drugi izvedbeni plasti.

## Splosna pravila

- service plast je edina plast, ki sme spreminjati manifest
- UI nikoli ni izvor resnice za statuse ali relacije
- vsaka operacija mora po zakljucku pustiti manifest v veljavnem stanju
- ce operacija ne uspe, se manifest ne sme delno zapisati
- v izvedbi trenutne faze obstaja filesystem write plast za materializacijo `IncomingText.body`; `sourcePath` je deterministična relativna pot do lokalne datoteke z vhodnim telesom
- schema v2 nima top-level `title` polja za manifest; `createEmptyManifest(title?)` lahko argument sprejme za forward compatibility, ne materializira pa ga se v schema v2
- `validateManifest(manifest)` preverja samo trenutno stanje enega manifesta
- `validateManifestTransition(previousManifest, nextManifest)` preverja dovoljene prehode med dvema snapshotoma
- statusnih prehodov ni mogoce dokazati iz enega samega manifesta
- `sourcePath` in `targetChapterPath` morata slediti pravilom iz model contracta

- `WorkbenchManifest` je trenutno v version `2`. Stari `v1` manifesti se ob nalaganju samodejno migrirajo v `v2` (glej `migrateManifestV1ToV2` v model contractu).

## createEmptyManifest()
## createEmptyManifest()

### Namen

Ustvari prazen, veljaven `WorkbenchManifest` v2.

### Input

- `title?: string`

### Output

- nov `WorkbenchManifest`

### Spremeni entitete

- ustvari vrhnji manifest
- inicializira prazne zbirke `incomingTexts`, `fragments`, `insertions`
- `concepts` je lahko prazna zbirka ali izpuscena, ce ostane skladna s schema v1

### Dovoljeni statusni prehodi

- ni statusnih prehodov; gre za inicializacijo

### Failure cases

- `manifestVersion` ni `1`
- rezultat nima obveznih zbirk
- rezultat ni skladen s schema v1

### Minimalni proof / acceptance check

- rezultat validira proti schema v1
- `incomingTexts.length === 0`
- `fragments.length === 0`
- `insertions.length === 0`

## addIncomingText(title?, body)

### Namen

Doda nov vhodni tekst v manifest in ga pripravi za nadaljnjo obdelavo.

### Input

- `title?: string`
- `body: string`

### Output

- nov `IncomingText`
- posodobljen manifest

### Spremeni entitete

- doda en `IncomingText`
- sama operacija ne zapisuje vsebine na filesystem; to naredi repository/persistence plast, ki materializira `body` na `sourcePath`

### Dovoljeni statusni prehodi

- nov zapis se ustvari v statusu `new`

### Failure cases

- `title` je prazen, ce implementacija to prepove
- `body` je prazen ali whitespace-only
- ni mogoce ustvariti stabilnega `sourcePath` ali ekvivalentne lokalne reference
- ustvarjeni zapis krsi schema v1

### Minimalni proof / acceptance check

- v manifestu obstaja nov `IncomingText`
- `status === "new"`
- `sourcePath` je ne-prazen string
- `title` in vhodni vir sta sledljiva
- nov `IncomingText` se ustvari brez povezanih `Fragment`
- ce klic poteka prek repository capture toka, `body` obstaja kot lokalna datoteka na `sourcePath`

## startProcessingIncoming(incomingId)

### Namen

Premakne `IncomingText` iz stanja `new` v aktivno obdelavo.

### Input

- `incomingId: string`

### Output

- posodobljen `IncomingText`
- posodobljen manifest

### Spremeni entitete

- spremeni status enega `IncomingText`

### Dovoljeni statusni prehodi

- `new -> processing`

### Failure cases

- `incomingId` ne obstaja
- `IncomingText` ni v statusu `new`
- ciljni prehod bi krsil invariants

### Minimalni proof / acceptance check

- tocno en `IncomingText` spremeni status v `processing`
- nobena druga entiteta se ne spremeni

## createFragmentFromIncoming(incomingId, body)

### Namen

Iz obstojecega `IncomingText` ustvari delovni `Fragment`.

### Input

- `incomingId: string`
- `body: string`

### Output

- nov `Fragment`
- posodobljen manifest

### Spremeni entitete

- doda en `Fragment`
- ne spremeni `IncomingText.status`; status `used` je rezerviran za vhodni vir z dejansko insertion sledjo

### Dovoljeni statusni prehodi

- `IncomingText` mora biti v `processing` ali `used`
- ta operacija ne izvaja statusnega prehoda na `IncomingText`
- `Fragment` se vedno ustvari kot `draft`

### Failure cases

- `incomingId` ne obstaja
- `IncomingText` je `archived`
- `IncomingText` je `new`; predhodno je potreben `startProcessingIncoming`
- `body` je prazen ali whitespace-only
- ustvarjeni `Fragment` ne kaze na veljaven `IncomingText`

### Minimalni proof / acceptance check

- v manifestu obstaja nov `Fragment`
- `Fragment.incomingTextId === incomingId`
- `Fragment.status === "draft"`
- `Fragment.text` je ne-prazen string

## insertFragmentIntoChapter(fragmentId, targetChapterPath)

### Namen

Zabelezi, da je `Fragment` vstavljen v ciljno poglavje aktivne knjige.

### Input

- `fragmentId: string`
- `targetChapterPath: string`

### Output

- nov `Insertion`
- posodobljen `Fragment`
- po potrebi posodobljen povezani `IncomingText`
- posodobljen manifest

### Spremeni entitete

- doda en `Insertion`
- spremeni `Fragment.status`
- lahko spremeni status povezanega `IncomingText`

### Dovoljeni statusni prehodi

- `Fragment: draft -> inserted`
- `IncomingText: processing -> used`, ce je to prva insertion sled za ta vhodni vir
- `IncomingText` lahko ostane `used`, ce vhodni vir insertion sled ze ima

### Failure cases

- `fragmentId` ne obstaja
- `Fragment` ni v statusu `draft`
- `targetChapterPath` je prazen ali whitespace-only
- `targetChapterPath` krsi path pravila iz model contracta
- `Insertion.fragmentId` ne bi kazal na veljaven `Fragment`
- povezani `IncomingText` je `new`
- povezani `IncomingText` je `archived`

### Minimalni proof / acceptance check

- obstaja nov `Insertion` z ne-praznim `targetChapterPath`
- `Fragment.status === "inserted"`
- novi `Insertion.fragmentId === fragmentId`
- povezani `IncomingText.status === "used"`

## archiveIncoming(incomingId)

### Namen

Arhivira `IncomingText`, ko aktivna obdelava ni vec potrebna.

### Input

- `incomingId: string`

### Output

- posodobljen `IncomingText`
- posodobljen manifest

### Spremeni entitete

- spremeni status enega `IncomingText`

### Dovoljeni statusni prehodi

- `new -> archived`
- `processing -> archived`
- `used -> archived`

### Failure cases

- `incomingId` ne obstaja
- `IncomingText` je ze `archived`
- `IncomingText` ima povezani `Fragment` s statusom `draft`
- arhiviranje bi krsilo sledljivost, ki jo zahteva implementacija

### Minimalni proof / acceptance check

- ciljni `IncomingText.status === "archived"`
- relacije `Fragment` in `Insertion` ostanejo nespremenjene

## archiveFragment(fragmentId)

### Namen

Arhivira `Fragment`, kadar ni vec del aktivnega uredniskega toka.

### Input

- `fragmentId: string`

### Output

- posodobljen `Fragment`
- posodobljen manifest

### Spremeni entitete

- spremeni status enega `Fragment`

### Dovoljeni statusni prehodi

- `draft -> archived`
- `inserted -> archived`

### Failure cases

- `fragmentId` ne obstaja
- `Fragment` je ze `archived`
- prehod iz `archived` v drugo stanje

### Minimalni proof / acceptance check

- ciljni `Fragment.status === "archived"`
- ce obstaja povezan `Insertion`, ta ostane nespremenjen kot dokazna sled

## updateIncomingText(incomingId, { title?, note? })

### Namen

Posodobi meta-podatke vhodnega teksta (obnova odlomka / preimenovanje vira). Operacija ne spreminja statusa in ne premika filesystem `sourcePath`; samo `title` in `note` se lahko spremenita. `undefined` pomeni "pusti pri miru", `null` pomeni "odstrani polje", ne-prazn string pomeni "nastavi novo vrednost".

### Input

- `incomingId: string`
- `title?: string | null`
- `note?: string | null`

### Output

- posodobljen `IncomingText`
- posodobljen manifest

### Spremeni entitete

- spremeni `title` in/ali `note` enega `IncomingText`

### Dovoljeni statusni prehodi

- ni statusnih prehodov; operacija ohrani trenutni status

### Failure cases

- `incomingId` ne obstaja
- podan `title` je prazen ali whitespace-only
- rezultat krsi schema ali invariante

### Minimalni proof / acceptance check

- ciljni `IncomingText` ima posodobljen `title`/`note`
- status ostane nespremenjen
- manifest ostane veljaven snapshot

## updateFragment(fragmentId, { text?, note? })

### Namen

Posodobi delovni odlomek (obnova teksta). Operacija ne spreminja statusa; lahko spremeni `text` (obvezen ne-prazen, ce je podan) in `note`. `undefined` pomeni "pusti pri miru", `null` pomeni "odstrani polje".

### Input

- `fragmentId: string`
- `title?: string | null`
- `text?: string`
- `note?: string | null`

### Output

- posodobljen `Fragment`
- posodobljen manifest

### Spremeni entitete

- spremeni `text` in/ali `note` enega `Fragment`

### Dovoljeni statusni prehodi

- ni statusnih prehodov; operacija ohrani trenutni status

### Failure cases

- `fragmentId` ne obstaja
- podan `text` je prazen ali whitespace-only
- rezultat krsi schema ali invariante

### Minimalni proof / acceptance check

- ciljni `Fragment` ima posodobljen `text`/`note`
- status ostane nespremenjen
- manifest ostane veljaven snapshot

## updateInsertion(insertionId, { targetChapterPath?, positionNote?, note? })

### Namen

Posodobi insertion sled (preimenovanje/obnova ciljnega mesta). Operacija ne spreminja statusa pripadajocega `Fragment`; spremeni lahko `targetChapterPath` (obvezen ne-prazen relativni path, ce je podan), `positionNote` in `note`. `undefined` pomeni "pusti pri miru", `null` pomeni "odstrani polje".

### Input

- `insertionId: string`
- `targetChapterPath?: string`
- `positionNote?: string | null`
- `note?: string | null`

### Output

- posodobljen `Insertion`
- posodobljen manifest

### Spremeni entitete

- spremeni `targetChapterPath`, `positionNote` in/ali `note` enega `Insertion`

### Dovoljeni statusni prehodi

- ni statusnih prehodov; operacija ohrani status odlomka in vira

### Failure cases

- `insertionId` ne obstaja
- podan `targetChapterPath` je prazen ali whitespace-only
- podan `targetChapterPath` je absoluten ali vsebuje traversal segmente (preverjeno prek validacije ne `nextManifest`)
- rezultat krsi schema ali invariante

### Minimalni proof / acceptance check

- ciljni `Insertion` ima posodobljen `targetChapterPath`/`positionNote`/`note`
- pripadajoci `Fragment` in `IncomingText` ohranita status
- manifest ostane veljaven snapshot

## validateManifest(manifest)
## validateManifest(manifest)

### Namen

Preveri, ali je trenutni snapshot `WorkbenchManifest` skladen s schema, relacijami, trenutno statusno skladnostjo in invariants.

### Input

- `manifest: WorkbenchManifest`

### Output

- validacijski rezultat z vsaj:
  - `isValid: boolean`
  - `errors: array`

### Spremeni entitete

- nobene; operacija je read-only

### Dovoljeni statusni prehodi

- ni statusnih prehodov; funkcija preverja samo snapshot

### Failure cases

- schema shape ni veljaven
- manjkajoci ali podvojeni `id`
- `Fragment.incomingTextId` ne kaze na obstoječ `IncomingText`
- `Insertion.fragmentId` ne kaze na obstoječ `Fragment`
- `Fragment.status === "inserted"` brez ustreznega `Insertion`
- `Fragment.status === "draft"` z obstojeco `Insertion` sledjo
- `IncomingText.status === "used"` brez vsaj ene insertion sledi prek povezanega `Fragment`
- `IncomingText.status === "new"` s povezanim `Fragment`
- `IncomingText.status === "archived"` s povezanim `Fragment.status === "draft"`

### Minimalni proof / acceptance check

- veljaven manifest vrne `isValid === true`
- neveljaven manifest vrne `isValid === false`
- `errors` jasno opisujejo schema, relacijske ali invariant napake snapshota

## validateManifestTransition(previousManifest, nextManifest)

### Namen

Preveri, ali je prehod iz `previousManifest` v `nextManifest` skladen z dovoljenimi statusnimi prehodi in ali `nextManifest` po spremembi ostane veljaven snapshot.

### Input

- `previousManifest: WorkbenchManifest`
- `nextManifest: WorkbenchManifest`

### Output

- validacijski rezultat z vsaj:
  - `isValid: boolean`
  - `errors: array`

### Spremeni entitete

- nobene; operacija je read-only

### Dovoljeni statusni prehodi

- preveri samo prehode, ki jih dovoljuje model contract
- ne sme dovoliti prehoda, ki pusti `nextManifest` v neveljavnem stanju

### Failure cases

- `IncomingText` ali `Fragment` izvede prepovedan statusni prehod
- prehod ustvari relacijsko nekonsistenten `nextManifest`
- `nextManifest` po prehodu ne validira kot veljaven snapshot

### Minimalni proof / acceptance check

- dovoljen prehod vrne `isValid === true`
- prepovedan prehod vrne `isValid === false`
- `errors` jasno opisujejo, kateri prehod ni dovoljen

## Operativni vrstni red

Minimalni pricakovani tok je:

1. `createEmptyManifest()`
2. `addIncomingText(title, body)`
3. `startProcessingIncoming(incomingId)`
4. `createFragmentFromIncoming(incomingId, body)`
5. `insertFragmentIntoChapter(fragmentId, targetChapterPath)`
6. `validateManifest(manifest)`
7. `validateManifestTransition(previousManifest, nextManifest)` za operacije, ki spreminjajo statuse

Arhiviranje je dopolnilna operacija po zakljucku aktivne uporabe.
