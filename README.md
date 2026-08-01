# Atmavictu

Atmavictu je matični produktni repo za Book Workbench: lokalno-prvo delovno mizo za tok `vir -> obdelava -> knjiga`.

## Kaj Atmavictu je

- product repo za Book Workbench
- contract-first osnova za model in manifest sledenja
- prostor, kjer se najprej zaklenejo scope, arhitektura in minimalni podatkovni model
- lokalno-prvi sistem, kjer trajni manifest povezuje vhodni tekst, odlomek in cilj v knjigi

## Kaj Atmavictu ni

- dump iz `Library`
- genericni notes app
- social app
- AI chat app
- takojsnja kopija `CIVIC_MEMORY_DESKTOP`

## Osnovni tok

Atmavictu obravnava tri povezane korake:

1. `vir`: vhodni tekst pride v lokalni delovni prostor
2. `obdelava`: iz vhodnega teksta nastanejo delovni odlomki in odlocitve
3. `knjiga`: potrjen odlomek se vstavi v ciljno poglavje aktivne knjige

Trajni manifest hrani sled:

- `IncomingText`
- `Fragment`
- `Insertion`
- `targetChapterPath`

To pomeni, da povezava med surovim vhodom in mestom v knjigi ni implicitna v UI-ju, ampak eksplicitna v lokalnem manifestu.

## Status repoja

- contract-first
- model + service + repository + CLI plast implementirana in testirana (glej `src/`, `npm test`)
- brez React, Vite, Tauri ali UI implementacije v tej fazi
- brez kopiranja vsebin iz `Library`

## Faze

- Faza 0: produktni scope, arhitekturni contract, minimalni manifest schema — DONE
- Faza 1: model + service plast nad manifestom — DONE (`src/workbenchManifest.ts`, `src/workbenchManifestRepository.ts`, `src/atmaCli.ts`)
- Faza 2: lokalni UI workbench nad zaklenjenim contractom — not started
- Faza 3: runtime integracija in selektivna desktop plast — not started
