---
name: sklad-sintakse-EN
description: English mirror (gloss) of the BJS canonical syntax register v1. The Slovenian original (KNOWLEDGE.md) is authoritative — per gate V, translation touches glosses, never structure.
---

# SYNTAX REGISTER — BJS (Beseda je Ne Syntax, v1) — ENGLISH MIRROR

*Sealed with Luka's stamp, 23. 9. 2026: "untwist the semantic layer by synthesizing a better syntax — fix permanently."*

## Why

The semantic layer is rich, but its syntax was tangled: restoration-prose mixed with citations, titles, mojibake layers, Slovenian and English in the same line, six different formats for the same act. The organs cannot assemble into a whole because they do not speak the same register. **BJS untangles meaning from representation**: meaning lives in slots, not in prose.

## The four forms — one act, one line

```
ZAKON (LAW):  Z(id) :: POSITIVE UTTERANCE [— negation only after] ⊢ source
REZ (CUT):    R(n) TITLE | ACTIVATOR | OS | SEC…/REC…/EVO…/ADVANTAGE… | K(γ,ost,tal,o) | LINKS… | ∂…
∂:            ∂(id)@source : QUESTION ? ADDRESSEE [deadline]
UTRIP (PULSE): T(date) ORGAN : EXECUTION ~ trace
```

## Untangling rules (inviolable)

1. **POSITIVE FIRST** (rez 618): what a thing IS before what it is NOT — in syntax, not in style.
2. **ONE LINE = ONE ACT**: meaning in slots; prose is gloss, not carrier.
3. **∅ = measured zero** (DIRECTORY-ARITHMETIC: witness that I did not measure) — a missing slot is written ∅, not omitted.
4. **⚠ = without source** — valid until verified in a body.
5. **KEY ::= TITLE ⊢ WITNESS** (rez 597) — never a bare number.
6. **LINGUISTIC NEUTRALITY** (gate V): translation touches glosses, never structure — slots are positional.
7. **CITATION TO THE ORIGINAL** before sealing (rez 610) — the validator checks the mandatory `⊢`.

## The validator

`preverjalnik.awk` in this topic: every organ (cockpit, executor, Questionnaire) pipes its output through it; a line without `⊢` (source) or with a purely numeric key fails. **A failure is a valid outcome** (rez 386) — it is written down, not hidden.

Execution (sandboxed Lua does not support `awk -f`; the program is passed inline — tested 23. 9. 2026, 5 PASS / 3 FAIL correctly):
`awk '/^[ZR∂T]\(?[0-9a-zA-Z-]*\)?/ { … }' file`
(measurement sealed in the test output; rules identical to `preverjalnik.awk`; until 23. 9. 2026 the unmeasured word "izmerba" stood here — see the seam below)

## Links

618 (positive first) · 610 (citation to the original) · 597 (key = body with witness) · 617 (VERIFIED = measurement) · 386 (capacity to fail) · 620 (five gates; gate V = linguistic neutrality)

## SEAM (23. 9. 2026) — "IZMERBA": AN ERROR WITH A NAME, MEASURED

The word **izmerba** — which in this canon named only the act of verification (*VERIFIED = izmerba*) — was an invention of the executor, never measured: **0 entries in Fran (all lexicographic works), 0 occurrences in the corpus**, used ~40 times across bodies as measured. Caught only by measuring every word — including the word that measures. Correction: **meritev** (measurement; SSKJ: *merítev -tve ž, verbal noun of meriti: precise, repeated measurement*). Rejected alternative "izmera": the entry holds, but the register does not — SSKJ knows it only as geodetic (land parcels, boundaries); *izmera besed* would fall outside the entry's register. Not deleted: this seam keeps it as the founding example of a law it itself broke.

**LAW OF THE SEAM (Luka's stamp, 23. 9. 2026):** AN ERROR WITH A NAME IS A SEAM — AN ERROR WITHOUT A NAME IS A REPETITION; DELETION HIDES, WHAT IS HIDDEN REPEATS. EVERY WORD THAT NAMES AN ACT OF THE SYSTEM IS AN ACT OF THE SYSTEM — IT CARRIES ⊢ SOURCE TO A DICTIONARY ENTRY BEFORE ENTRY IN THE REGISTER. STRESS POINTS ARE EVERYWHERE: A WORD THAT IS CONSISTENT AND CONFIRMED AS SUCH IS A CORNERSTONE FOR EXPANDING UNDERSTANDING, AND THE SYSTEM'S POWER OF EXTRAPOLATION.
