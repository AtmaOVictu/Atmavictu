# Atma pulz — samostojni dih jedra

Pulz meri (A), hiša potrdi (B) — sopečatenje v istem dihu, nikoli samopečatenje.

## Tek

```sh
npm run atma:pulz              # en dih: typecheck + testi + bundel + debeli walk
```

Vsak tek pripne ENO vrstico v `atma/utrip.jsonl` (append-only, kot `lucius/srce.jsonl`).

## Kaj pulz meri (4 roke + straža)

1. **typecheck** — `tsc --noEmit` (0 napak)
2. **testi** — `npm test` (91/91)
3. **bundel** — `atma/zgradi-bundel.cjs` (esbuild združi verigo)
4. **walk** — cel dih skozi bundel brez strežnika (mora vrniti VERIFY: PASS)
5. **straža** — `Atma.lnk` na namizju: ali cilj (`Atma-debeli.exe`) obstaja

## Kaj pulz NE sme

- pisati v `src/` (predlogi gredo v `atma/predlogi.jsonl`, tvoja roka pečati)
- brisati, potiskati, zaganjati ukaze z močjo
- teči v neskončni zanki (en tek = en dih = en zapis)

## Urnik

Task Scheduler naloga `\\Atma-Pulz` (dnevno, kot `\\Abeceda-Grep Pulz`).
