# Atmavictu Faza 2 — deveterna operacijska pot: proof runbook

> Ročni dokaz acceptance barja Faze 2, po vzoru `CIVIC_WORKBENCH_PROOF_RUNBOOK.md`.
> Bar: vseh 9 service operacij dosegljivih iz UI vsaj enkrat; `VERIFY: PASS` drži celo pot;
> sled inserta preživi oba arhiva. Vizualna dovršenost NI bar.

## Zagon (dve lupini)

```sh
# lupina 1 — API (privzeto pristanisce 4173)
npm run serve -- <projectRoot> [port] [extraLibraryRoot]

# lupina 2 — UI (privzeto 5173, proxy /api -> 4173)
cd web && npm install && npm run dev
```

## Devet korakov (ročno, v brskalniku)

| # | Operacija | Kje v UI |
|---|---|---|
| 1 | capture | Knjiznica (levo): izberi vir → Vhodni tekst (desno): zajem |
| 2 | start-processing | Vhodni tekst: zacni obdelavo |
| 3 | create-fragment | Vhodni tekst: ustvari fragment |
| 4 | insert | Fragment → Aktivna knjiga: `targetChapterPath` → vstavi |
| 5 | update-incoming | Vhodni tekst: popravi naslov/opombo |
| 6 | update-fragment | Fragment: popravi besedilo/opombo |
| 7 | update-insertion | Insertion: popravi `positionNote` |
| 8 | archive-fragment | Fragment: arhiviraj |
| 9 | archive-incoming | Vhodni tekst: arhiviraj |

## Preverbe (držijo ob vsakem teku)

1. Statusna vrstica pokaže `VERIFY: PASS` po vsakem koraku (isti izhod kot CLI `verify`).
2. Po 8. in 9. koraku sled inserta OSTANE vidna: `targetChapterPath ← fragment` se ne izgubi z arhiviranjem.
3. `book.workbench.json` v `projectRoot` je po koncu veljaven manifest (`npm run atma -- verify <projectRoot>`).

## Priče doslej

- **2026-08-04** — živi brskalniški dokaz (Playwright), devetera pot prehojena, `VERIFY: PASS` celo pot (zapisano v specu Faze 2 in README).
- **2026-10-21 (dop.)** — živi API dokaz (⊢ izpis v seji agenta Mistral Vibe, isti endpointi, ki jih kliče UI): capture → start-processing → create-fragment → insert → update×3 → archive-fragment → archive-incoming; `isValid: true` sredi poti in po obeh arhivih; sled `poglavje/dokaz.md ← Fragment dokaza` preživi oba arhiva. 85/85 testov, `web` typecheck + vite build zeleni; istega dne komit `4857890` (CI `web` posel + REGISTER-PADCEV vnos 3).
- **2026-10-21 (ponovljivi brskalniški dokaz)** — `web/proof/deveterna-pot.mjs` (Playwright, Edge headless): 9/9 operacij v resničnem brskalniku, `VERIFY: PASS` po vsakem koraku, sled `poglavje/brskalniski-dokaz.md` preživi oba arhiva, neodvisni `/api/verify` = true. Ponovljiv ukaz: API na 4173 + vite na 5173 + `node web/proof/deveterna-pot.mjs <projectRoot>` ( začasni projectRoot; trije popravki teka zabeleženi v seji: selectOption index, `.first()` namesto hasText med urejanjem, badge `inserted` namesto `draft` po insertu ).

## Pravilo teka

Vsak nov teki runbooka se zapiše sem z datumom in pričo (⊢ izpis ali ⚠ opis); teki brez zapisa niso dokaz.
