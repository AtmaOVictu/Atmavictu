# VBL 0.1470 — release gate

**Purpose:** prevent a draft, a partial assembly, or a locally passing test suite from being presented as a released or canonical licence.

**Current status:** `BLOCKED`. This is expected. The supplied source snapshot contains the continuation from §0.25 into §0.49 and the historical machine record; the exact complete earlier body (§§0–0.24) is not present as one byte-verifiable source file. The identity of the claimed predecessor is unresolved (0.1450 versus 0.1460).

## Hard release conditions

A release candidate is eligible for human release review only when every applicable condition below has evidence tied to exact bytes and a named event:

1. **Complete body:** one assembled file contains the complete approved clauses, front matter, map, lineage, machine record, and seals. An intentionally reserved clause such as §0.26 is labelled `CLAIMED_OPEN` with provenance; it is not silently filled or treated as a missing accidental heading.
2. **Identity and predecessor:** the predecessor is resolved from an immutable source locator and commit/object ID, exact byte size, and SHA-256. A cover label or copied machine record is insufficient.
3. **Rights provenance:** each covered item has an item-level rights record. A path or hash identifies bytes; it does not prove authorship, ownership, permission, or consent.
4. **Author approval:** an affirmative approval record names the exact candidate version and SHA-256. Silence, inferred intent, or approval of a different draft does not qualify.
5. **Independent review:** reviewer identity and role are recorded; the reviewer did not author, execute, or control the reviewed change and has no undisclosed material conflict. The review states scope, evidence, limitations, and result.
6. **Legal review:** the actual grant, termination, cure, attribution, privacy, third-party, and compatibility terms have been reviewed for the intended jurisdictions and uses. Research notes alone are not a legal opinion.
7. **Companions and registers:** every companion and required register is present at its declared path, has a size and SHA-256, and its status matches reality. `UNVERIFIED` is not release-ready.
8. **Reproducible tests:** tests identify definitions, versions, inputs, environments, and run IDs. A prior `PASS` is not evidence of a later state. A repeatable test definition may be executed more than once.
9. **Publication evidence:** the exact committed body is retrievable from the stated remote repository and its commit/object ID and digest match the candidate. A local file or a prepared patch does not prove publication.
10. **Time and delivery evidence:** entry and build-finish events are measured independently; a receiver-side receipt is supplied by the receiver. `SENT` is not `DELIVERED`. Cross-clock duration claims require documented synchronization and uncertainty.
11. **Manifest and binary receipts:** manifest entries are generated from final committed bytes. Predecessor and current binary receipts meet §0.14(a)–(d); missing receipts remain explicitly `UNVERIFIED`.

## Status rules

- `BLOCKED`: one or more hard conditions are missing, false, stale, or unverified.
- `READY_FOR_AUTHOR_AND_INDEPENDENT_REVIEW`: all mechanical prerequisites are present, but this is not a release and does not imply legal validity.
- `RELEASED`: only a separate, explicitly authorized release process may set this status after the candidate is approved and the published remote bytes are independently fetched and matched.

The local checker in `check_release_gate.py` intentionally cannot set `RELEASED`. It checks a supplied evidence record for completeness and exact-file integrity. It does not prove that a named person is who they claim to be, that an approval is legally valid, or that a reviewer is genuinely independent. Those facts need external evidence and human judgment.

## Current blockers (from supplied materials)

- Exact full §§0–0.24 source file: not supplied as a byte-verifiable artifact.
- Predecessor identity: unresolved between 0.1450 and 0.1460.
- 0.1450 / 0.1460 predecessor binary receipts: not supplied and not independently verified.
- §0.26: explicitly claimed by another open hand; exact source, author, permission, and status remain unresolved.
- Seven named original companion files: not supplied as separate files in this package; presence and hashes unverified.
- `REGISTER-NEIMENOVANIH.jsonl` and `REGISTER-PADCEV.jsonl`: not supplied as separate files.
- Author approval of the exact 0.1470 digest: not supplied.
- Independent reviewer: not appointed or evidenced.
- Jurisdiction-specific legal review: not performed.
- Public commit and remote fetch matching a complete 0.1470 body: not supplied.
- Receiver-side mail delivery receipt: not supplied; no delivery is claimed.

## Re-running

From the package root:

```bash
python check_release_gate.py release-evidence.template.json
python validate_package.py
python -m unittest discover -s tests -v
```

The template is deliberately incomplete and should return `BLOCKED`. Do not edit the template to invent evidence merely to obtain a green status.
