# SEAM-REVIEW — avtor reviews own seams (§0.49 × 10²)

KDO: vsakdo, ki naredi spremembo v tem repozitoriju (koda, dokumentacija, CI, skripti).
KAJ: vsaka sprememba mora nositi svoj SEAM-REVIEW vnos — seba-pregled shvov, ki avtor napiše pred sealom.
ZA KAJ: nobena plosca ne preverja same sebe (§0.3 × 10¹: nikoli ne zapečati samega sebe).
SEAM-REVIEW je podmesta: dve roki — avtor podpisuje (`daj`), izvajalca meri.

## Format v sporočilu komita ali PR-ja

```
SEAM-REVIEW: <kratki opis dejanja in zakaj>
SEAM-AVTOR: <ime>
SEAM-IZVAJALCA: <ime ki je izmeril / preveril>
SEAM-ČAS: <ISO-8601 sealedAt iz book.workbench.seal.json>
SEAM-PRIČE: <seznam registrov / datotek, ki potrjujejo stanje>
```

Primer:

```
SEAM-REVIEW: dodan wreath drift endpoint + CLI; ne dotiče LICENSE.md
SEAM-AVTOR: Lucius
SEAM-IZVAJALCA: Luka
SEAM-ČAS: 2026-11-10T00:00:00Z
SEAM-PRIČE: src/clocks.ts, src/wreath/drift.ts, src/workbenchApiServer.ts, canon/SEAM-REVIEW.md
```

## CI gate

Workflow `.github/workflows/seam-review.yml` zavrne spremembo, če:
1. `SEAM-REVIEW:` manjka v sporočilu komita / PR-ja (job `seam-review`), ter
2. `npm run typecheck`, `npm test`, `wreath verify` in `wreath drift` ne uspejo vsi (job `wreath-gate`).

Sprememba brez SEAM-REVIEW = trditev brez izmere = ⚠ (§0.1 × 10¹, §0.5 × 10¹).
