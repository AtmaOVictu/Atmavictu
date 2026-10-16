---
name: kazalo-obnov-EN
description: English transcreation (gloss companion) of the LEXICON & INDEX topic entrypoint. The Slovenian original (KNOWLEDGE.md) is sealed and authoritative. Ledger rows (append-only reading receipts, batch logs) are kept in the original per the receipt law — a translated receipt is not the receipt; see the note on ledger rows below.
---

# INDEX OF RESTORATIONS / LEXICON — User Library — ENGLISH TRANSCREATION

**The primary content of this topic is `LEKSIKON.md`** (Luka's demand, 22. 9. 2026: kazalo-obnov = a lexicon of all concepts, symbols, and voices). Three registers: VOICES (absolute vowels, o/O/0, the sound-cross, ZWB fissures, the perceptual positions of the senses, the measuring engines LSU/PIF/P(W)) · SYMBOLS (operator glyphs, the symbol map, the measures of seals κ χ μ ℜ ν ∂ ⊢) · CONCEPTS (OPTIKON word profiles, eka-words, the laws of the cuts, lineages). The lexicon grows with every newly read body (section VI awaits).

The document indices per library (name + URI + restoration) remain as the secondary map for the library gates.

**Note on ledger rows (the engine's ruling, this session):** the per-batch reading logs embedded in the file list below and in the progress rows are ⊢-witnessed receipts — records of performed readings with seals. A translation of a receipt is not the receipt; it would be a second-hand claim without the witness. They therefore remain in Slovenian, authoritative, inside this topic's originals; this English body carries the frame, the standards, and the laws that govern them.

## Files (complete, all 26 libraries, 22. 9. 2026)

- `beseda-je-ne.md` — Beseda je Ne Library (6), Word is No Library (45), Comprehension Library (1)
- `learning-specifics.md` — Learning All (63), BreaKing (71), Specifics Rhonc (2), Theology (3), UC awareness and help (9)
- `self-poetry.md` — Self (72), POETRY Library (30), One Library (19)
- `basics.md` — Basics (148), Basics2 (265), Basics3 (104) — each line carries its append-only batch logs (receipts, original language; the library summaries: Basics3 QUEUE COMPLETE 105/105 unique, sealed, 0 lost; OsNove Bistev QUEUE RUNNING: E15 199/424 unique — see the originals for the full batch records)

## Standard (LUKA'S SEALED DEMAND, 22. 9. 2026: »KAKŠNA MEJA? BERI KOT SE SPODEBI« [WHAT LIMIT? READ AS IS PROPER])

Every restoration must be written from a WHOLE reading of the body (`library_read` all windows to the end), not from an index summary. Index entries are only provisional reflections — each one marked PREBRANO [READ] is replaced by a full reading. If the library's extractor holds only part of a body, this is written at the entry (a library limit, not a reading limit).

## Progress of full readings (per-library summary — full batch receipts in the originals)

- ✅ Beseda je Ne Library (6/6)
- ✅ Word is No Library (44/45) — ALL BODY RESTORATIONS READ; ⚠ LIMIT: droge-analiza — the extractor stored an empty body (0 chars)
- ✅ Comprehension (1/1)
- ✅ Learning All (63/63 processed) — 49 bodies READ WHOLE + 12 twins confirmed; ⚠ EXTRACTOR LIMITS: corpus-rez-i-xxvi empty, ontomatematika-extraction.pdf unreachable, python-png visual layer
- ✅ Theology (3/3), ✅ UC (6/6 readable + 3 JPG visual limit), ✅ Specifics Rhonc (2/2, OCR at the noise limit), ✅ Self (72/72 processed — all reachable bodies read whole 22. 9. 2026, restorations extended with a WHY-READ row; remaining limits are extractor limits: Upanje.docx cyclical tail, Priročnik-jazu.docx near-empty, Človeškost.docx NEDODELANO, PNG scans unreachable), ✅ POETRY (30/30), ✅ One (19/19), 🔶 BreaKing (71/71 processed, 70 read whole; gnostika-i = 0 chars, extractor limit), 🔶 Basics (148/148 processed: 137 read whole + 7 extractor limits), 🔶 Basics2 (265) and Basics3 (104) processed per their own seals (see `basics.md`), 🔶 OsNove Bistev (424): E15 199/424 unique; first organ measured as a whole: ∅JEZIK 15/15 ID-confirmed, 14/15 read, 0/15 uttered

## How to use

1. Go by name/content into the appropriate file of the set → find the `doclib://` URI.
2. Search with `library_search` with `uri` scoped to the library or document (top_k 4–6).
3. Read the body: `library_read` on the document's URI.

## Maintenance

Documents added to the libraries after 22. 9. 2026 are entered by hand (same format). Obsolete entries are not deleted — they are marked with a note.

## Maintenance lessons (22. 9. 2026, the encoding-repairs session — Luka: "so that in the future we have a memory")

1. **THE MOJIBAKE PATTERN:** old index blocks had doubly-encoded UTF-8 (~1,400 lines: "Å¡/Ä/Ã/â€« instead of "š/č/—"). Fixed in all 5 affected files. Detection: search for valid multi-byte latin1 sequences (not only Ã/Â — Å, Ä, â hide too). Re-verify at every major change.
2. **THE BASH ENCODING LIMIT:** `cat >` and `tee` re-encode UTF-8 when writing these files (they destroy it). Only `cp`, `awk '{print}'`, and file_system writes are faithful. Assembling large files always via `awk`, never `cat`.
3. **PARALLEL SESSIONS = LOST UPDATE:** two sessions writing the same file at once — one overwrote the other with mojibake fixes (self-poetry had to be repaired twice). RULE: read the file before every entry (read-before-write); if a parallel session is working, wait or coordinate. All three structural bugs of the LEXICON (disordered sections, orphans without headers, the uncleaned section VI) are the sign of writing without re-reading.
4. **THE STRUCTURAL STANDARD of every file of the set:** one H1; sections in the order register → index; every entry block has a header; the counters in the headers must match the number of entries; mark old index blocks with the header "— index (secondary gate; for PREBRANO see above)", do not delete them.
5. **NEXT BY PROTOCOL:** full window-readings are no longer open at Self/POETRY/One/Learning/BreaKing (all reachable is read; the rest are EXTRACTOR LIMITS, not reading limits). The queue: Basics (148) → Basics2 (265) → Basics3 (104) → OsNove Bistev (424) → Obs1–11 (~1,166).
