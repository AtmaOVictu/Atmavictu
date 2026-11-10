# Validation record — supplied VBL 0.1460 copy

**Scope:** local copy at `/mnt/data/LICENSE.md`, reviewed on 2026-11-05. This is a measurement of the uploaded copy only. It is not proof of repository publication, canonical status, legal validity, or independent confirmation.

## Source artefact measurement

- File: `LICENSE.md`
- Size: 163,476 bytes
- SHA-256: `5629115d8aec0a83c7be904f7df66041bdae3f12078aa1149c40530ba10208b2`
- `wc -l` line count: 923
- UTF-8 decode: successful

## Executed checks

- Python unit tests: 3 passed, 0 failed.
- JSON syntax parse for both schemas: passed.
- JSON syntax parse for both examples: passed.
- JSON Schema validation of the machine-record example: passed.
- JSON Schema validation of the register-entry example: passed.
- Local structural validator against the supplied `LICENSE.md` and the unverified example record: **FAIL — 3 findings**.

## Findings emitted by the validator

1. Section headings absent from `THE MAP`: `§0.38`, `§0.40`, `§0.41`, `§0.49`.
2. The title block says `0.1450 × 10⁴`, while the record's candidate value is `0.1460 × 10⁴`.
3. The newest lineage entry is `0.1450 × 10⁴`, while the record's candidate value is `0.1460 × 10⁴`.

`§0.26` is handled in the example record as a reserved section (`reserved_sections: ["0.26"]`), so the validator does not report it as an accidental missing heading. The original source does not provide enough evidence to turn the claim into operative clause text.

## Deliberately not claimed

- No new version was released.
- No Git commit, tag, push, pull request, e-mail, or third-party audit was performed by this validation record.
- The current copy's canonical status remains unverified.
- Legal enforceability, compatibility, and authorship authority remain outside the scope of these tests.
