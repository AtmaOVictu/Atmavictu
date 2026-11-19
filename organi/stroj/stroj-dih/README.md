# STROJ-DIH

> **English** (this file) · Slovenščina: [README-SL.md](README-SL.md)

House of working workflows of the corpus Beseda je Ne. Born by the order of ⟡ VERBATIM:
»daj, stori tako da smem biti ponosen nate in napredek/napreduj/nadgrajuj/deluj«
(make it so that I can be proud of you: advance, progress, upgrade, act), with the origin point of ⟡:
»vidiš? tukaj ni nobenega workflowa« (see? there is no workflow here). The Workflows board stood empty ⊢ measured.

## What lives here

Four working workflows, each a forge of clean logic from `worker/logic`:

| workflow | task | why |
|---|---|---|
| `tik-dih` | canonical clock UTC ⇌ CET (Ljubljana) | ⟨TIK-IZMERJEN-PREJ-ZAPISAN⟩ |
| `forma-sodnik` | form judgment over the whole body | ⟨FORMA-ENVRSTICA⟩ cure |
| `vrh-varovalka` | summit: rez = 1 + actual highest, guard | ⟨VRH-DVOSTOPEN⟩ ∧ ⟨NE-UGIBAJ⟩ |
| `zeton-lint` | shapes of numbers, dates, clocks, md5 | instrument ŽETON-LINT |

Clean logic is stdlib only: tests run without the SDK. The SDK skeleton lives in
`workflows/`, the worker's entrance in `entrypoints/worker.py`.

## Tests

`python3 -m unittest discover -s tests` (source: the project's own root).

## Running

The worker discovers all workflows by itself. The house becomes state through
a managed deployment; secrets ⟨ne⟩ live in the image.

> The English half is a translation witness; the Slovenian half [README-SL.md](README-SL.md) is the source of truth ⊙ VBL §0.60.