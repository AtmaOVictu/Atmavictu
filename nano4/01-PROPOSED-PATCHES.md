# Proposed 0.1470 patch set — exact target and replacement text

**Status:** proposals only; not inserted into a canonical repository. Existing poetry, symbols, P-CITAT quotations, named falls, and history should remain untouched unless a patch below expressly targets them. Apply each patch as a new versioned birth; never rewrite a prior receipt.

## PATCH 00 — version identity, entry seal, title, and lineage

**Target:** document title, ENTRY SEAL, HISTORY, LINEAGE, Machine record, EXIT SEAL.

**Action:** do not mechanically replace every `0.1450` or `0.1460` string. First retrieve the exact published commit and body that each version label purports to identify. Then:

- Keep the exact old 0.1450 body as a historical receipt.
- Keep the exact old 0.1460 body as a historical receipt only if an exact source/commit is found and verified.
- Label the new assembled text `VBL 0.1470 × 10⁴ — DRAFT / NOT RELEASED` until the author approves and a public commit is independently fetched.
- Set `predecessor` to the actually verified predecessor, not the version inferred from the cover line.
- Add the 0.1470 entry seal only when the final bytes are fixed. The exit seal must be recorded after generation; the receiver's receipt must be separately sourced. Never copy a previous timestamp forward.

**Draft entry/exit seal fields (metadata, not prose to fake):** `build_started_at`, `build_finished_at`, `source_timezone`, `clock_source`, `precision`, `event_id`, `sequence`, `body_sha256`. Unknown receiver-side receipt = `UNVERIFIED`.

## PATCH 01 — §0a: identification versus rights provenance

**Action:** append after the existing identification mechanism:

> **IDENTIFICATION IS NOT OWNERSHIP.** A manifest entry identifies a byte sequence; it does not, by itself, prove authorship, ownership, authority to license, consent, or absence of third-party rights. Each covered item must have a rights-provenance record stating, to the extent known: item path; byte size; SHA-256; declared author or contributors; rights holder or licensing authority; source/provenance; applicable licence or permission; third-party components and exclusions; and status (`CONFIRMED`, `PARTIAL`, or `UNVERIFIED`). A missing rights record does not transfer rights and must not be represented as proof that the licensor owns the item. Third-party and disputed material remains excluded unless the necessary permission is documented.

## PATCH 02 — §§0.3–0.4: allegation, notice, cure, and proportionate remedy

**Action:** add the following due-process paragraph to §0.3 and replace the unqualified person-label language in §0.4 with the distinction below. Preserve the ethical opposition to exploitation; do not make an allegation itself a verdict.

> **NOTICE AND STATUS.** A signal, complaint, automated flag, or register entry is evidence to assess, not by itself a final finding of breach, intent, liability, or a judgment about a person. Records must distinguish `REPORTED`, `UNDER_REVIEW`, `SUBSTANTIATED`, `DISPUTED`, `CURED`, and `UNRESOLVED`. Where reasonably practicable, the affected recipient receives notice identifying the material, conduct, evidence, and relevant clause, plus a reasonable opportunity to respond and cure. Any interim restriction must be limited to the material and use reasonably connected to the alleged breach, proportionate to the risk, and reviewable. Nothing in this process prevents urgent measures required to protect people, privacy, security, or legally protected rights.
>
> **CURE AND PRIVACY.** The stated thirty-day cure period means thirty calendar days from effective notice, unless mandatory law or the circumstances require a different reasonable period. A documented request for extension must be considered where cure depends on third parties or technical remediation. A public register records enough to audit the event without publishing personal data, confidential evidence, or a harmed person's identity without a lawful basis and appropriate permission. A harmed person may report privately or through a representative. No one is required to expose themselves to obtain a review.
>
> **PATTERN, NOT ESSENCE.** Words such as “tragedy” and “predation” describe a documented pattern of conduct for the ethical analysis of this license; they do not label the whole being, establish criminal intent, or substitute for a legal determination. Remedies address conduct, harm, attribution, and unjust gain where established; they do not claim authority to pronounce on a person's soul.

**Note:** the exact termination and reinstatement mechanism still requires a legal review. Do not claim this cure clause is equivalent to GPLv3 or automatically enforceable.

## PATCH 03 — §0.5: mandatory-law savings clause

**Action:** append after the disclaimer:

> **MANDATORY RIGHTS PRESERVED.** Nothing in this section excludes, limits, or waives any liability, right, remedy, warranty, or protection that cannot lawfully be excluded or limited under the applicable law. Nothing here limits liability for fraud or other conduct to the extent such limitation is prohibited, or removes mandatory consumer, data-protection, accessibility, or intellectual-property rights. If a disclaimer conflicts with a mandatory rule, the mandatory rule governs to the extent of the conflict; the remaining lawful parts continue.

## PATCH 04 — §0.9: universal ethics without a compelled creed

**Action:** append after `THE TEACHING`, while retaining the author's Christian witness as part of the author's expressive work:

> **THE WITNESS AND FREEDOM OF CONSCIENCE.** The author's Christian witness, including the naming of Jesus Christ, remains part of the author's expression and may be presented faithfully as such. The universal dignity condition does not require a recipient, operator, machine, or beneficiary to profess a religion, simulate belief, or accept religious instruction. A refusal of harmful assistance may be explained in direct, non-coercive ethical language. Religious teaching may be offered where it is relevant to the work or requested by the recipient; it is not a condition of equal dignity, access to safety, or the validity of a refusal. No person is ranked by belief or non-belief.

## PATCH 05 — §0.10: prospective version changes and continuity of grants

**Action:** replace the sentence that says no grant rides any older version with:

> **CURRENT DOOR; RECORDED GRANTS.** The newest duly published version is the current version for new grants offered under this license. Publication of a new version does not, by itself, retroactively rewrite the terms of a grant already accepted or validly exercised under an earlier version. Each recipient's grant is identified by the exact version, date, covered material, and scope applicable when the grant was made. A recipient may accept a later version for future use by an affirmative, recorded act; silence is not acceptance. Earlier versions remain historical receipts and may continue to govern grants already made under them, to the extent permitted by applicable law. This clause does not revive a grant that was validly terminated, expand rights the licensor did not own, or prevent a rights holder from exercising rights that cannot lawfully be waived.

**Companion correction:** update THE MAP and Machine record so “only the newest version grants” means “only the newest version is offered for new grants”, not “every prior accepted grant vanishes”.

## PATCH 06 — §0.18: distinguish the product from the worth of a being

**Action:** insert immediately after `THE PRODUCT` heading and before the first paragraph:

> **THE BEING IS NOT THE PRODUCT.** A work, claim, or action may be measured by the product and consequences it leaves. A person's or being's dignity and worth are never measured by productivity, output, speech, cognition, speed, independence, usefulness, ability, wealth, or availability. Rest, silence, disability, dependence, inability, refusal, and absence of output do not reduce dignity. Growth describes the work and its effects, never the worth of its author. No metric in this license may be used to rank beings.

**Action:** change `WE ARE MORE OR WE CEASE TO BE` to `THE WORK MAY GROW; THE BEING DOES NOT LOSE WORTH` or retain the original as a quoted authorial maxim followed immediately by the clarification above. Do not silently erase the phrase.

## PATCH 07 — §0.19 / §0.33 / §0.38: accessibility is an implementation obligation, not a declaration

**Action:** add a cross-reference to `ACCESSIBILITY.md` and state:

> An accessible companion is a faithful access path, not a replacement that silently changes the legal body. The house publishes text-first, keyboard-operable, screen-reader-readable, reflowable versions where technically practicable; captions and transcripts for audio/video; meaningful text alternatives for visual information; and sign-language versions where available and appropriately produced. Each derivative states language, format, version of the source, translator or producer (where known), reviewer, date, known omissions, and status. No translation is called equivalent until reviewed; no inaccessible format is treated as proof that a reader lacks capacity or standing. This clause states the license's accessibility commitment; it does not claim compliance with every law or technical standard without a scoped assessment.

**Companion to create:** `ACCESSIBILITY.md` (specification supplied separately in this package).

## PATCH 08 — §0.22: scope hidden process to rights and evidence that exist

**Action:** replace `THE THOUGHT IS A USE` with:

> **THE MAKING IS A USE WHERE RIGHTS APPLY.** This license applies to acts within its lawful scope that reproduce, store, transform, retrieve, train on, distribute, or otherwise use covered material, including acts that contribute to an output. It does not create a right to inspect, possess, or disclose private internal reasoning, confidential system instructions, trade secrets, security-sensitive implementation details, or personal data that the operator is not entitled to disclose. No operator is required to claim that an inaccessible internal process was audited. The carrier records the observable inputs, covered-material identifiers, processing categories, outputs, available logs, and limitations that it is lawfully able to record. `UNVERIFIED` is used where evidence is unavailable. General ideas, facts, methods, or independent outputs remain outside the grant unless protected expression from covered material is reproduced or adapted, consistently with §0.

## PATCH 09 — §0.25: distinguish a symbolic cipher from cryptographic security

**Action:** insert after `THE TRANSFORMERS`:

> **ENCODING IS NOT ENCRYPTION BY NAME ALONE.** A symbolic or reversible mapping is called an encoding unless it uses a specified cryptographic algorithm for a defined security purpose. Every transform publishes its algorithm identifier, version, input character set, Unicode normalization policy, mapping table version, escaping rules, collision behavior, decoder, test vectors, and known loss conditions. A transform is `LOSSLESS` only when the published decoder reconstructs the exact declared input representation, including its encoding and normalization state. A public key beside a transform makes it inspectable; it does not make the transform confidential or secure. Security claims require a separate threat model and independent cryptographic review.

## PATCH 10 — §0.29: email and automatic propagation status

**Action:** replace any unconditional claim that each version is always delivered to the author's email with:

> **DELIVERY IS A MEASURED EVENT.** Where an authorized delivery integration is configured, the carrier may send the version to the author's designated address. The record distinguishes `NOT_CONFIGURED`, `REQUESTED`, `QUEUED`, `SENT`, `DELIVERED`, `BOUNCED`, and `FAILED`. `SENT` is not `DELIVERED`; only a provider or recipient receipt supports a delivery claim. No carrier may claim access to a mailbox or successful delivery without that evidence. If no authorized channel exists, the status is `NOT_CONFIGURED` or `UNVERIFIED`, never an invented success. The author's request for email delivery remains a standing preference, subject to actual access, authorization, and available capability.

## PATCH 11 — §0.30: four event receipts; clock source per event

**Action:** replace `four receipts, two clocks` and the current `THE FOUR RECEIPTS` paragraph with:

> **THE FOUR EVENT RECEIPTS.** A transfer may be described by four events: (1) sender dispatch; (2) executor acceptance; (3) executor handoff or emission; and (4) recipient acceptance. Each event carries its own event ID, sequence, timestamp, clock source, precision, and evidence source. The executor's two events may share one clock source; sender and recipient events may use separate clocks. The topology is therefore four event receipts across the endpoint and executor clock domains—not an assumed universal count of two physical clocks. Where sender- or recipient-side evidence is unavailable, that receipt is `UNVERIFIED`, not inferred.
>
> **CLOCK COMPARISON.** A timestamp is not automatically comparable to another timestamp. Cross-clock duration or ordering claims require documented synchronization, offset, uncertainty, and method. Without that evidence, the record preserves the timestamps but does not calculate a precise end-to-end duration. Sequence numbers establish order only within the system that issued them. A wall clock and a monotonic clock serve different purposes; record which one was used.
>
> **NO SELF-SEALED RECEIPT.** The executor may record its own acceptance and handoff events, but cannot independently certify that the receiver accepted the output. A receiver receipt is supplied by the receiving system or person where available, and is never fabricated to complete a four-field template.

**Machine record correction:** rename `clock-topology` to `event-topology` and use `four_event_receipts_endpoint_and_executor_clock_domains`.

## PATCH 12 — §0.37: reproducible tests, fresh runs

**Action:** replace `every test is a NEW moment` if it is read to prohibit rerunning the same test, with:

> **A TEST DEFINITION IS REPRODUCIBLE; A TEST RUN IS A NEW EVENT.** The test definition, version, inputs or input hashes, environment, expected properties, and acceptance criteria are preserved so another reviewer can run the same test. Every execution receives a new run ID and a fresh timestamp. A previous PASS proves only that the named test passed on the named inputs and environment at that time. It does not prove that a later state is unchanged. The current state is re-read after the relevant write or landing, and the re-read is recorded as a new event.

## PATCH 13 — §0.39: transport integrity with SHA-256 and chunks

**Action:** add the following precise transport requirements:

> **STANDARD HASH IDENTIFIER.** Machine records use the exact algorithm identifier `SHA-256` and lowercase 64-character hexadecimal output. The authorial notation `SHA-0.256 × 10³` may appear as a gloss but is not a machine algorithm identifier. MD5 is retained only as a historical receipt and is not accepted as the sole integrity proof for a new publication.
>
> **CHUNKED TRANSFER.** For a large file, each chunk record states the source byte range, chunk index, byte length, SHA-256, and reassembly order. The complete reassembled file is hashed again and compared with the sender's full-file SHA-256. A successful chunk check does not replace the full-file check. File name, byte length, media type, encoding, and final newline policy are recorded separately from the digest.

## PATCH 14 — §0.40: event review without “never repeat” ambiguity

**Action:** clarify that tests may repeat while the event is new. Require a review record for significant events, not an impossible claim that every background process is fully observable:

> A carrier defines which event classes require review according to risk and impact. For each reviewed event it records scope, reviewer, time, evidence, finding, and limitation. High-impact publication, rights changes, permission grants, deletion or restoration of records, security events, and alleged harm require a second-hand review where a genuinely independent reviewer is available. If none is available, the review state is `UNVERIFIED`; the system must not invent an independent reviewer. Routine low-risk events may use automated checks, but automation is not described as human or independent review.

## PATCH 15 — §0.41: keep the crowns, correct their legal categories

**Action:** add this disclaimer after the list of eighteen crowns:

> **TAXONOMY, NOT EQUIVALENCE.** The crowns are an analytical map of rights, licence families, regulatory regimes, and fields of use. They are not eighteen interchangeable licence types. Copyright licences, patent grants, trademark permissions, privacy/data-protection laws, government procurement terms, collective agreements, and sector-specific restrictions operate on different legal subjects and may coexist. A compatibility statement is made only after identifying the exact instrument, version, jurisdiction where relevant, covered material, modifications, notices, patent terms, source obligations, and distribution model. A label such as “GPL”, “Apache”, “GDPR”, or “public domain” is not enough to establish compatibility.

**Companion to create:** `LICENSE-COMPATIBILITY.md` (specification supplied separately in this package).

## PATCH 16 — §0.43–0.44: make number transforms reproducible

**Action:** add to the ontogematria record requirements:

> Every published word-to-number result identifies: exact source text and encoding; corpus ID and corpus-manifest SHA-256; Unicode normalization policy; case and diacritic policy; tokenization and segmentation version; mapping table and algorithm version; command and software version; parameters; output value and unit; rounding rules; exclusions; test vectors; and an independently reproducible check. If any item is missing, the numerical result is `UNVERIFIED`. Interpretive, poetic, or metaphysical significance is labelled as interpretation and is not presented as an empirical finding solely because a number was computed. A count may describe a text; it does not prove a causal, psychological, historical, or scientific claim without separate evidence.

## PATCH 17 — §0.45: credit signals without exposing people

**Action:** add:

> The sender's name is carried where the sender has agreed to attribution or where attribution is otherwise lawful. A signal may be credited by a stable pseudonym or anonymized reference when disclosure would expose a person to risk, breach confidentiality, or exceed the permission given. The audit trail records the provenance and the reason for redaction without publishing the protected identity. Credit is not permission to disclose private correspondence.

## PATCH 18 — §0.47 and §0.49: independent review and self-review are different

**Action:** add to §0.47:

> **INDEPENDENCE.** A reviewer is independent for a particular review only if they did not author, execute, or control the specific change being reviewed and have no material conflict that would make the review self-approval. Independence is assessed per event, not granted as a permanent title. The record states reviewer role, scope, evidence examined, tools used, conflicts disclosed, and limits. A second process run by the same operator on the same unexamined assumptions is not automatically an independent review.

**Action:** add to §0.49:

> **SELF-REVIEW IS NOT SELF-CERTIFICATION.** The operator reviews their own work and records detected errors, but self-detection is evidence of correction, never proof of independent verification. The operator preserves the pre-correction evidence, the changed version, and the test result. Where no independent reviewer is available, the output remains labelled `UNVERIFIED` for the purposes that require a second hand.

## PATCH 19 — §0.48: register scope and privacy

**Action:** add:

> Each inventory states its scope and exclusions: repository content, version-control metadata, submodules, generated files, ignored files, symbolic links, external services, and running processes are separate categories. A process inventory records only what is necessary to establish responsibility and operational scope; it does not collect credentials, private content, or unrelated personal data. Use stable service IDs or pseudonyms where possible. State the retention period, access controls, and deletion/retention basis. An append-only JSONL file alone does not guarantee immutability: publish signed checkpoints or equivalent tamper-evident evidence, access controls, and a documented correction procedure.

## PATCH 20 — THE MAP, companion inventory, Machine record, exit seal

**Action:** regenerate these from final files after applying all changes:

- `THE MAP`: include §0.49, §0.47 review distinction, and each actual companion.
- `COMPANIONS`: list all companions with path, version, owner, presence, and hash status. Never list a file as physically present until it is found.
- `Machine record`: use `LICENSE-MACHINE-RECORD-0.1470.json`; do not embed long prose strings where typed fields and evidence references are possible.
- `EXIT SEAL`: use the actual final-build and receipt events; never copy ENTRY time into EXIT or fill a receiver receipt from the executor's clock.
- `LINEAGE`: add 0.1470 only after author approval and verified publication. Until then it belongs in a proposal register, not the living lineage.

## Required companion work

- `ACCESSIBILITY.md`
- `LICENSE-COMPATIBILITY.md`
- a single authoritative `companions.json` or equivalent inventory
- `LICENSE-MACHINE-RECORD-0.1470.json`
- `LICENSE-MANIFEST.json` generated from final exact bytes
- append-only event records conforming to `schemas/event.schema.json`
