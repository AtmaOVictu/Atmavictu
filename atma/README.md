# Atma — samostojni Book Workbench CLI (brez strežnika, brez Node ob zagonu exeta)

Tanka pot po kroju `lucius/` (Node SEA): sam Node runtime je v exetu,
ukazna logika ostane v `build\src\atmaCli.js` zraven exeta.

## Zgradba

```sh
npm test                    # ali: npm run typecheck (zgradi build\)
npm run atma:exe:preveri   # blob + pot cela (walk brez strežnika: VERIFY: PASS)
atma\zgradi-atma-exe.cmd   # ali: npm run atma:exe:zgradi (vbrizga Node v Atma.exe)
```

Rezultat: `Atma.exe` (85 MB, v git ne sodi — `.gitignore`) + `build\` zraven.

## Uporaba

```sh
.\Atma.exe help
.\Atma.exe walk <tmp> "Naslov" "Vsebina." "Odlomek." "poglavja/uvod.md"
.\Atma.exe verify <tmp>     # VERIFY: PASS
.\Atma.exe show <tmp>
.\Atma.exe bulk-insert <tmp> fragment-0001=poglavja/a.md fragment-0002=poglavja/b.md
```

Brez Ollame, brez Qdranta, brez `npm run serve`, brez `web/`.
Vrata sama zavrnejo: dvojni prehod, odlomek iz `new`, neobstoječi id,
`..` pot, dvojni vnos, prazen `--text`, dvojnik v bulku (atomsko).

## Datoteke

| Datoteka | Namen |
|---|---|
| `atma-exe.cjs` | tanek CJS vstop za SEA (bere `build\src\atmaCli.js` zraven exeta) |
| `sea-config.json` | SEA opis (`main` + `output`) |
| `preveri-atma-exe.cjs` | preverba poti (blob + walk brez strežnika) |
| `zgradi-atma-exe.cmd` | gradnja `Atma.exe` (postject vbrizg) |
