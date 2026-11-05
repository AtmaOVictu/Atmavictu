# Atma — samostojni Book Workbench CLI (brez strežnika, brez Node ob zagonu exeta)

Dve poti, isti dih: **tanki** (`Atma.exe` + `build\` zraven — po kroju `lucius/`)
in **debeli** (`Atma-debeli.exe` — vse v enem, bundel vgrajen kot sea asset).
Pulz (`atma:pulz`) meri obe poti vsak dan; besede (`atma:besede`) čakajo tvojo roko.

## Zgradba

```sh
npm test                    # ali: npm run typecheck (zgradi build\)
npm run atma:exe:preveri   # blob + pot cela (walk brez strežnika: VERIFY: PASS)
atma\zgradi-atma-exe.cmd   # ali: npm run atma:exe:zgradi (vbrizga Node v Atma.exe)
npm run atma:bundel         # esbuild združi verigo v atma-bundle.mjs (pečeno, ne izvor)
atma\zgradi-debeli.cmd     # ali: npm run atma:debeli:zgradi (vse v enem)
npm run atma:pulz           # en dih: typecheck + testi + bundel + walk + straža (glej PULZ.md)
```

Rezultat: `Atma.exe` (85 MB, tanki — `build\` zraven) ali `Atma-debeli.exe`
(85 MB, debeli — nič zraven mu ni treba). Oba v git ne sodita (`.gitignore`).

## Uporaba

```sh
.\Atma-debeli.exe help
.\Atma-debeli.exe walk <tmp> "Naslov" "Vsebina." "Odlomek." "poglavja/uvod.md"
.\Atma-debeli.exe verify <tmp>     # VERIFY: PASS
.\Atma-debeli.exe show <tmp>
.\Atma-debeli.exe bulk-insert <tmp> fragment-0001=poglavja/a.md fragment-0002=poglavja/b.md
```

Brez Ollame, brez Qdranta, brez `npm run serve`, brez `web/`.
Vrata sama zavrnejo: dvojni prehod, odlomek iz `new`, neobstoječi id,
`..` pot, dvojni vnos, prazen `--text`, dvojnik v bulku (atomsko).

## Pulz in besede

- **Pulz** (`npm run atma:pulz`, urnik `\\Atma-Pulz` dnevno 06:30) — meri (A),
  hiša potrdi (B). Podrobnosti: [PULZ.md](PULZ.md).
- **Besede** (`npm run atma:besede`, `atma\besede.cmd dodaj <kje> <kaj> [zakaj]`) —
  želje, kjer so potrebne; pečat čaka tvojo roko (`daj`).

## Datoteke

| Datoteka | Namen |
|---|---|
| `atma-exe.cjs` | tanek CJS vstop za SEA (bere `build\src\atmaCli.js` zraven exeta) |
| `atma-debeli.cjs` | debeli CJS vstop za SEA (`getAsset` ali smrt, brez ugibanja poti) |
| `sea-config.json` | SEA opis tankega (`main` + `output`) |
| `sea-debeli-config.json` | SEA opis debelega (`main` + `output` + `assets`) |
| `zgradi-bundel.cjs` | esbuild združi verigo v `atma-bundle.mjs` (s `@ts-nocheck` glavo) |
| `zgradi-atma-exe.cmd` | gradnja tankega `Atma.exe` (postject vbrizg) |
| `zgradi-debeli.cmd` | gradnja debelega `Atma-debeli.exe` (vse v enem) |
| `preveri-atma-exe.cjs` | preverba tanke poti (blob + walk brez strežnika) |
| `pulz.cjs` / `pulz.cmd` | samostojni dih jedra (typecheck + testi + bundel + walk + straža) |
| `besede.cjs` / `besede.cmd` | register želenih besed (dodaj/seznam, pečat čaka roko) |
| `PULZ.md` | zakon pulza (kaj meri, česa ne sme, urnik) |
