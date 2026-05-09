# Atmavictu Service Contract

## Namen

Ta dokument doloca minimalne operacije nad `WorkbenchManifest`. Service contract opisuje dovoljene posege v model, ne pa konkretne implementacije v TypeScriptu ali drugi izvedbeni plasti.

## Splosna pravila

- service plast je edina plast, ki sme spreminjati manifest
- UI nikoli ni izvor resnice za statuse ali relacije
- vsaka operacija mora po zakljucku pustiti manifest v veljavnem stanju
- ce operacija ne uspe, se manifest ne sme delno zapisati
- v izvedbi FAZE 2A ni filesystem write plasti; `sourcePath` je zato lahko deterministična logicna pot, dokler ni dodan dejanski IO sloj
- schema v1 nima top-level `title` polja za manifest; `createEmptyManifest(title?)` lahko argument sprejme za forward compatibility, ne materializira pa ga se v schema v1

## createEmptyManifest()

### Namen

Ustvari prazen, veljaven `WorkbenchManifest` v1.

### Input

- brez argumentov

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

## addIncomingText(title, body)

### Namen

Doda nov vhodni tekst v manifest in ga pripravi za nadaljnjo obdelavo.

### Input

- `title: string`
- `body: string`

### Output

- nov `IncomingText`
- posodobljen manifest

### Spremeni entitete

- doda en `IncomingText`

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
- lahko posodobi status `IncomingText`, ce implementacija to zahteva, vendar mora ostati znotraj dovoljenih prehodov

### Dovoljeni statusni prehodi

- `IncomingText` mora biti vsaj v `processing`
- dovoljeno:
  - brez spremembe statusa `IncomingText`
  - ali `processing -> used` sele, ko obstaja insertion sled
- `Fragment` se vedno ustvari kot `draft`

### Failure cases

- `incomingId` ne obstaja
- `IncomingText` je `archived`
- `IncomingText` je `new`, ce service zahteva predhoden `startProcessingIncoming`
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
- `IncomingText: processing -> used`

### Failure cases

- `fragmentId` ne obstaja
- `Fragment` ni v statusu `draft`
- `targetChapterPath` je prazen ali whitespace-only
- `Insertion.fragmentId` ne bi kazal na veljaven `Fragment`
- povezani `IncomingText` je `archived`

### Minimalni proof / acceptance check

- obstaja nov `Insertion` z ne-praznim `targetChapterPath`
- `Fragment.status === "inserted"`
- novi `Insertion.fragmentId === fragmentId`
- povezani `IncomingText` ni vec `new`

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

## validateManifest(manifest)

### Namen

Preveri, ali je `WorkbenchManifest` skladen s schema, relacijami, statusnimi pravili in invariants.

### Input

- `manifest: WorkbenchManifest`

### Output

- validacijski rezultat z vsaj:
  - `isValid: boolean`
  - `errors: array`

### Spremeni entitete

- nobene; operacija je read-only

### Dovoljeni statusni prehodi

- ni statusnih prehodov

### Failure cases

- schema shape ni veljaven
- manjkajoci ali podvojeni `id`
- `Fragment.incomingTextId` ne kaze na obstoječ `IncomingText`
- `Insertion.fragmentId` ne kaze na obstoječ `Fragment`
- `Fragment.status === "inserted"` brez ustreznega `Insertion`
- `IncomingText.status === "used"` brez zadostne sledi

### Minimalni proof / acceptance check

- veljaven manifest vrne `isValid === true`
- neveljaven manifest vrne `isValid === false`
- `errors` jasno locijo schema napake od relacijskih in statusnih napak

## Operativni vrstni red

Minimalni pricakovani tok je:

1. `createEmptyManifest()`
2. `addIncomingText(title, body)`
3. `startProcessingIncoming(incomingId)`
4. `createFragmentFromIncoming(incomingId, body)`
5. `insertFragmentIntoChapter(fragmentId, targetChapterPath)`
6. `validateManifest(manifest)`

Arhiviranje je dopolnilna operacija po zakljucku aktivne uporabe.
