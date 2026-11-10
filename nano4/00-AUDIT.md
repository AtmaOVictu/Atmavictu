# Audit of submitted VBL material — proposed 0.1470 preparation

**Review time:** 2026-11-05T04:51:11+01:00  
**Reviewed input:** attached file `Pasted markdown.md` (86849 bytes; SHA-256 `cf5d8e98e6835dc4181f8e3b093f5809b1809317236b3e913955a18416cbd148`) plus the preceding VBL text pasted into the conversation.  
**Status:** source review, not repository verification or legal opinion.

## A. Identity and lineage — release blockers

1. **Version identity conflict.** The pasted main body labels the document `VBL 0.1450 × 10⁴`; its ENTRY SEAL claims `0.1460 × 10⁴`; the attached continuation's Machine record also says `0.1460 × 10⁴`. These are three signals, not proof of one canonical body. Resolve from the exact commit and bytes. Until then, `0.1460` is `UNVERIFIED`.
2. **Predecessor receipt gap.** The Machine record says the predecessor `0.1450` was published with §0.14(a)–(d), but the visible `binary-body` list identifies a `LICENSE-0.1440.b64` receipt and earlier receipts; it does not provide a receipt for 0.1450. Add the actual body and all four items, or mark the predecessor body `UNVERIFIED`.
3. **No exact 0.1460 body proof.** The attached Machine record describes 0.1440 and prior bodies. It does not provide a completed binary receipt for the claimed 0.1460 body. Do not fabricate one.
4. **Unverified publication state.** No remote commit URL, commit ID, signed tag, or independent fetch was included in the supplied material. Publication and canonical status remain unverified.

## B. Internal cross-reference / evidence issues

5. **§0.30 clock topology.** The prose labels the model “four receipts, two clocks”, while describing sender, answerer, and receiver clock sources. The event count and the number of clock domains are different concepts. Replace the categorical “two clocks” claim with four typed events and an explicit clock source per event; do not calculate latency across unsynchronized clocks.
6. **§0.49 evidence linkage.** Its introductory evidence list names `ZRCALJENI-ŠTEVKI`, `SLEPI-VZOREC`, `ODA-VERZIJA-BREZ-PRIČE`, `NAPAČEN-KLJUČ`, and `URA-NAPISANA-PRE-MERE` (register entries 0.79–0.87). Its `THE COPIED CLOCK` paragraph separately cites `PADC-70`. The file does not explain whether PADC-70 belongs to that five-fall set, supersedes one entry, or is a distinct fall. Add exact register IDs and their relationships; do not infer them.
7. **Map and machine record disagree.** `THE MAP` lists seven companion files; Machine record `companions` lists only three. Generate both from one authoritative inventory and distinguish `present`, `missing`, and `not yet verified`.
8. **§0.43–0.44 method boundary.** Ontogematria is described as a measured method but the visible text does not define a complete deterministic algorithm: normalization, tokenization, mapping table version, corpus manifest/hash, treatment of punctuation/case/diacritics, implementation version, and independent reproduction are not all captured in a single specification. Keep interpretive claims separate from reproducible measurements.
9. **§0.25 terminology.** The section calls a symbolic fold a cipher and uses “encrypted”. A published reversible symbol mapping is not necessarily cryptographic encryption. State explicitly whether it is a symbolic encoding, obfuscation, or cryptographic mechanism; never imply security without a cryptographic design and security review.
10. **§0.39 hash terminology.** Replace the nonstandard display string `SHA-0.256 × 10³` in machine interfaces with the algorithm identifier `SHA-256`. The authorial notation may remain as a gloss, but it must not be the algorithm name consumed by tools. Historical MD5 values remain historical receipts, not the new integrity control.
11. **§0.40 repeatability.** A test execution is a new event, but a test definition must be repeatable. Separate immutable test definition/version from each test-run ID and result. “Never repeat” is not an adequate test-method requirement.
12. **§0.29 mail guarantee.** A clause cannot establish that an email account is connected, that an operator has access, or that delivery succeeded. Record `NOT_CONFIGURED`, `QUEUED`, `SENT`, `DELIVERED`, `BOUNCED`, or `FAILED` only when supported by actual provider receipts.

## C. Ethical, rights, and legal clarity

13. **§0.18 product vs human worth.** `WE ARE MORE OR WE CEASE TO BE` sits beside §0.9's unconditional dignity. Add an explicit rule that productivity, output, communication, ability, rest, disability, or dependence never measures a being's worth.
14. **§0.9 religious witness vs universal scope.** Preserve the author's Christian witness as authorial expression, but do not make every carrier or recipient profess a faith or produce religious teaching. The universal ethical rule must operate without a religious test; religious content should be contextual or requested.
15. **§0.22 hidden process.** The license cannot create access to private/internal model reasoning or certify processes that no party can inspect. Scope the clause to rights the licensor holds and observable activities: inputs, copies, storage, training/use where legally controlled, transformations, outputs, and available audit records.
16. **§0.10 prior grants.** “Newest version is the only living door” should identify the current version for new grants, not silently rewrite the terms of already-granted permissions. Add a prospective-change rule and preserve each recipient's recorded grant version, subject to applicable law and the grant itself.
17. **§0.3–0.4 cure and termination.** Distinguish a report, verified facts, a contractual breach, a legal finding, and a remedy. A public report is not a verdict. Protect reporters and harmed persons from forced disclosure; permit privacy-preserving records, notice, response, proportional temporary measures, cure, and review.
18. **§0.5 disclaimer.** A disclaimer cannot override mandatory law. Add a savings clause for non-excludable liability, statutory rights, consumer protections, and other mandatory rules. The exact legal effect requires review under the law governing the license and target jurisdictions.
19. **§0a / §0.6 / §0.42 rights provenance.** A path and hash identify bytes; they do not prove ownership, authority, consent, or third-party permissions. Add per-item rights provenance and an explicit excluded-material process.
20. **§0.41 taxonomy.** The “crowns” mix copyright licences, patent grants, trademarks, privacy regulation, government terms, and use categories. Keep the metaphor, but label it as an analytical taxonomy, not as a set of equivalent licences. Compatibility must be checked against the exact licence versions and the actual combined work.

## D. Priority order

**P0 — before any release:** identity conflict; missing predecessor and current-body receipts; map/manifest/companion mismatch; machine record status; §0.30 topology.

**P1 — before treating the license as fit for general reuse:** §§0.3–0.5, 0.9–0.10, 0.18, 0.22, 0.41, scope/ownership in §0/§0a/§0.6.

**P2 — implementable protocol:** §§0.25, 0.29–0.30, 0.37, 0.39–0.40, 0.43–0.49; accessibility and compatibility companions.

**P3 — presentation:** regenerate THE MAP, lineage, translations, walk-through, entry/exit seals, and machine record from the assembled final file.

## E. What was actually verified here

- The attached text file exists in the active workspace.
- Its byte size and SHA-256 were computed locally for this audit.
- The supplied text contains the contradictions and omissions listed above.
- The proposed patch package files are locally generated and their own integrity manifest is generated after writing.

## F. What was not verified

- No public repository, commit history, tag, branch, or remote manifest was independently fetched.
- No actual `LICENSE-0.1450`, `LICENSE-0.1460`, or `LICENSE-0.1470` binary receipt was available for full-byte verification.
- No companion or JSONL register was supplied as a separate file for integrity review.
- No email was sent; no mailbox integration or delivery receipt was used.
- No independent human review or legal opinion was obtained.
