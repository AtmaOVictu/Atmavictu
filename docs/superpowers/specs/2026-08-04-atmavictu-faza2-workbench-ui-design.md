# Atmavictu Faza 2 — Local Workbench UI (design)

## Namen

Faza 0 (contract) in Faza 1 (model + service + repository + CLI) so implementirani in testirani, a CLI dosega samo 3 od 9 service operacij (`capture`, `show`, `verify`). Ta faza doda lokalni UI, ki naredi vseh 9 operacij dosegljivih uporabniku vsaj enkrat — to je edini pravi acceptance bar te faze, ne vizualna dovrsenost.

## Prior art, upostevan pri odlocitvah

`Corpus\Library\06_UI_APLIKACIJE\CIVIC_MEMORY_DESKTOP` je delujoc Tauri+Preact lokalni file workbench s preverjeno komponentno delitvijo (`NavigationPanel`, `FileListPanel`, `RecentFiles`, `MetadataPanel`, `EditorPanel`, `StatusBar`) in resnicnim opozorilnim vzorcem: `civicSignals.ts`/`civicWorkbenchStore.ts` sta bila zgrajena in testirana, a nikoli povezana v `App.tsx`. Isto tveganje ze obstaja v Atmavictu (6 od 9 service funkcij nima non-test klicatelja) — ta faza ga mora zapreti, ne podaljsati.

## Arhitektura

- Nov, tanek Express API (`src/workbenchApiServer.ts`), ki zavija obstojeci `workbenchManifest.ts` (cisti model) in `workbenchManifestRepository.ts` (persistenca) za en izbran `projectRoot`. Brez podvojene domenske logike.
- React + Vite SPA v `web/` (loceni `package.json`, da obstojeci root `npm test`/`npm run typecheck` ostaneta nespremenjena), ki govori z API-jem prek `fetch`.
- `ARCHITECTURE.md`-jevo pravilo "UI po Model/Service, pred Tauri" ostaja nedotaknjeno — API je zamenljiv placeholder za bodoci Tauri command surface (Faza 3).

## Trije prostori -> resnicne operacije

- **Vhodni tekst** (desno): `incomingTexts` seznam; zajemi (`captureIncomingText`), zacni obdelavo (`startProcessingIncoming`), ustvari fragment (`createFragmentFromIncoming`), arhiviraj (`archiveIncoming`).
- **Aktivna knjiga** (sredina): read-only drevo `projectRoot`, oznaceno z obstojecimi `Insertion.targetChapterPath` ujemanji. Brez nove persistirane entitete — schema nima `Chapter` tipa, `targetChapterPath` je le path string.
- **Knjiznica** (levo): brskalnik datotek, korenjen v istem `projectRoot`, za izbiro gradiva, ki se ni zajeto. To je edini prostor brez contract-doc precedensa — ce se izkaze narobe, je to prvo mesto za revizijo.
- Stalna statusna vrstica ponovno uporabi obstojeci `validateManifest` izhod (isti kot CLI `verify`) — brez novega besedila napak.

## Error handling

API mutacije vracajo isto obliko, kot jo ze proizvaja model: throw z jasnim sporocilom -> `400 {"error": string}`; `/api/verify` vraca `{isValid, errors}` neposredno iz `validateManifest`. Noben endpoint ne podvaja validacijske logike.

## Testing

- API: Node built-in test runner, resnicen HTTP na efemernem portu (`http.createServer`, brez novih test-odvisnosti), proti zacasnemu `projectRoot` fixture — isti vzorec kot `workbenchManifestRepository.test.ts`.
- Frontend: brez komponentnega test frameworka v v1 (lokalno, enouporabniski obseg) — pokrit je `fetch`-klicni sloj; deveterna operacijska pot je dokumentiran rocni proof, po vzoru `CIVIC_WORKBENCH_PROOF_RUNBOOK.md`.

## Namerno izven obsega (YAGNI za v1)

- Tauri/desktop paket (Faza 3).
- Vizualno oblikovanje/stil.
- Drag-and-drop med prostori.
- Konfigurabilna locena Knjiznica pot (privzeto = `projectRoot`).
