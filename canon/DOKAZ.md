# ⊢ DOKAZ — Proof-of-Lineage Ledger

> Ledger of sealed decisions for the ONTOMATEMATIKA system.
> Canonicality rule: a decision is sealed when recorded here with date, evidence, and seal.
> Format: one entry per decision, append-only. Revisions create new entries; sealed entries are never edited.

## Entries

| # | Date | Decision | Evidence | Seal |
|---|------|----------|----------|------|
| 1 | 2026-09-11 | Atmavictu declared HEAD — canonical headless TypeScript core | Orientation Cycle Canvas v0.1; commit `69f6646` | ⊢ |
| 2 | 2026-09-11 | soul-evolution declared ACTIVE game build (Godot/GDScript); Divine-Ascension-System SUPERSEDED | Orientation Cycle Canvas v0.1; commit `b562126` | ⊢ |
| 3 | 2026-09-11 | ontolo-ko-jedro declared EXPERIMENTAL, fold/independence pending | Orientation Cycle Canvas v0.1; commit `0e5c1c5` | ⊢ |
| 4 | 2026-09-30 | ontolo-ko-jedro fold/independence question resolved: **independent** — role re-declared as ONTOMATEMATIKA presentation/UI layer (React). Evidence: audit found zero shared code/types/logic with Atmavictu headless core; concept data was hardcoded presentation data, not ontology logic | [ontolo-ko-jedro PR#1](https://github.com/AtmaOVictu/ontolo-ko-jedro/pull/1); commit `20d1077` | ⊢ |
| 5 | 2026-09-30 | ONTOMATEMATIKA corpus migrated into version control: `Atmavictu/canon/` becomes source of truth (Beseda je Ne system, rozetni kamni protocol, stone template, mapping table). Skills and Notion become derived views; changes land in canon first, as PRs | [Atmavictu PR#3](https://github.com/AtmaOVictu/Atmavictu/pull/3); commit `530f6b7`; merge `c91aa45` | ⊢ |
| 6 | 2026-09-30 | Canonicality rule sealed: if a skill and `canon/` diverge, **`canon/` is canonical**. Sealed entries are immutable; revisions create new entries ("pravila naj bodo revizibilna, izjema naj ima pečat") | `canon/README.md`; commit `530f6b7` | ⊢ |
| 7 | 2026-09-30 | Pojmovnik concept lexicon canonized as structured data: `canon/pojmovnik.json` (10 concepts: Ne, Gib, Etika, Zavedanje, Čas, Jaz, Ego, Odnos, Telo, Dvom). ontolo-ko-jedro UI consumes corpus at runtime; hardcoded concept arrays removed | Atmavictu commit `a53ec00`; ontolo-ko-jedro commit `19eafe3` | ⊢ |
| 8 | 2026-09-30 | DOKAZ ledger migrated from Notion to git: this file (`canon/DOKAZ.md`) is the canonical Proof-of-Lineage Ledger. Notion is demoted to scratch space; nothing is canonical until recorded here or in a commit | this file; this commit | ⊢ |
| 9 | 2026-09-30 | Atmavictu_Oracle **archived** by owner (Luka Pintarič). Evidence: repository empty since declaration, zero commits, no role fulfilled; archived status verified via API | `isArchived: true` (GitHub API, verified 2026-09-30) | ⊢ |
| 10 | 2026-09-30 | Divine-Ascension-System **archived** by owner (Luka Pintarič), completing DOKAZ #2 (declared SUPERSEDED 2026-09-11, inactive since 2025-07) | `isArchived: true` (GitHub API, verified 2026-09-30) | ⊢ |
| 11 | 2026-09-30 | First corpus-born content sealed: Kamen CXVII (Petersenov graf) and CXVIII (Heawoodov graf) + stotnije 101–104 (graf, oglišče, povezava, kletka). Generated inside the protocol (four-component format, SR-1 IPA layers, search-result citations). Stone numbering ⚠ from CXVII pending canvas-body measurement | `canon/kamni/CXVII-CXVIII.md`; `canon/stotnije/2026-10-grafika.md`; commit `1c45db5` | ⊢ |
| 12 | 2026-09-30 | ontolo-ko-jedro fully corpus-driven: all three content pages (Pojmovnik, Manifest, Etika) render from `canon/*.json` synced via `scripts/sync-canon.sh`. No hardcoded content data remains in React code. Editing one JSON in the corpus updates the whole site | ontolo-ko-jedro commit `1c1c927`; Atmavictu commits `a53ec00`, `1c45db5` | ⊢ |
| 13 | 2026-09-30 | Kamni CXIX–CXXI sealed (McGee 24, Tutte–Coxeter 30, Monster 8×10⁵³): grafika series of five stones complete, same cut (∅→∆) confirmed across five dimensions. Corpus now renders on the site: /kamni and /stotnije pages consume canon markdown directly | `canon/kamni/CXVII-CXVIII.md` (commits `1c45db5`, `bf5a083`); ontolo-ko-jedro commit `7527513` | ⊢ |
| 14 | 2026-10-11 | Stotnije 105–107 (zadaviti, oddam, ponovim) sealed — the first dosjeji cut from the executor's own living language; the mail (oddam) was performed before the naming, per AX-16. Pismológi rez sealed as canonical format: the slash as ∂, Slovenian morphology made visible — the first mapping needing no translation | `canon/stotnije/2026-10-grafika.md` (commit `68b705a`); `canon/pismologi-rez.md` (commit `2eb9364`) | ⊢ |
| 15 | 2026-10-21 | roka Mere (zunanji sedež, Vibe/GLM) | Structural correction: entries #13–14 repositioned into Entries table (statements unchanged, byte-identical); ledger spine restored — pyramid: base carries all rows. | ⟡ ⟨daj⟩ (piramida — osnova vsakega prijema) · prejšnji blob: ae43580a823ee6e1e7556d3ee0eb32088ea1f178 |
| 16 | 2026-10-28 | ⟨SEME⟩ canonized as the folded seed of corpus + door: four layers — simbolno (CESTA essence), nujno (session background), nenujno-skrito (unfold map), a-nujno (counterweight). A chat session reads the seed in one breath and the essence of the license rides immediately; legal acts unfold to the sources. Register semen = veriga (§0.24 × 10²). Born of ⟡ ukaz ⟨daj⟩ (komprese ∧ fragmentacija sistema), built by roka Mere (Vibe/GLM) | this PR; living door measured at source this breath: VBL 0.1210 × 10⁴ @main (⟨sha⟩ 5dd6d7b) | ⟡ ⟨merge⟩ dovrši |

## Pending decisions

| Question | Opened | Status |
|---|---|---|
| Atmavictu_Oracle: seed with a real purpose, or archive? | 2026-09-30 | SEALED — archived, DOKAZ #9 |
| Archive Divine-Ascension-System (superseded, DOKAZ #2)? | 2026-09-30 | SEALED — archived, DOKAZ #10 |

## Provenance

- Ledger format: append-only table, append-only history. Each entry cites a commit hash or PR — the git history is the cryptographic-grade evidence; this file is the human-readable index.
- To seal a new decision: open a PR adding a row to Entries. The merge commit completes the seal.
- Migrated from: Notion DOKAZ database (declared 2026-09-11). Historical Notion entries #1–#3 are transcribed above; the Notion database is no longer updated.
