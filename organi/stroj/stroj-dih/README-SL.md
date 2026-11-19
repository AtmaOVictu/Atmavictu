# STROJ-DIH

> **Slovenščina** (ta datoteka) · **English**: [README.md](README.md)

Hiša delujočih delovnih tokov korpusa Beseda je Ne. Roden po ukazu ⟡ VERBATIM:
»daj, stori tako da smem biti ponosen nate in napredek/napreduj/nadgrajuj/deluj«,
z izhodiščem ⟡: »vidiš? tukaj ni nobenega workflowa« (plošča Workflows bila prazna ⊢ izmerjeno).

## Kaj živi tukaj

Štirje delovni toki, vsak kova čiste logike iz `worker/logic`:

| tok | naloga | zakaj |
|---|---|---|
| `tik-dih` | kanonska ura UTC ⇌ CET (Ljubljana) | ⟨TIK-IZMERJEN-PREJ-ZAPISAN⟩ |
| `forma-sodnik` | sodba forme nad celim telesom | ⟨FORMA-ENVRSTICA⟩ kura |
| `vrh-varovalka` | vrh, rez = 1 + dejansko najvišja, varovalka | ⟨VRH-DVOSTOPEN⟩ ∧ ⟨NE-UGIBAJ⟩ |
| `zeton-lint` | oblike števil, datumov, ur, md5 | instrument ŽETON-LINT |

Čista logika je stdlib only: testi tečejo brez SDK. Okostje SDK
živi v `workflows/`, vstop delavca v `entrypoints/worker.py`.

## Testi

`python3 -m unittest discover -s tests` (izvor: koreg projekta).

## Zagon

Delavec odkrije vse tokove sam. Hiša postane iz stanja prek
upravljane namestitve (managed deployment); skrivnosti ⟨ne⟩ živijo v sliki.