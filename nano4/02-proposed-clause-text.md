# Proposed clause text for a future VBL revision

**STATUS: PROPOSAL ONLY / NOT CANON / NOT APPROVED / NOT A LEGAL OPINION.**

The following is deliberately written as modular draft language. It must not be pasted into a release as if already approved. The author must choose the policy options and a qualified lawyer should review the final legal instrument in the relevant jurisdictions.

## P0 — §0.1 Grant: enumerate rights and authority

> **GRANT.** Subject to the terms of the licence identified for the relevant covered material, each rights-holder grants only the rights that the rights-holder owns or is authorised to grant. To the extent of those rights, the grant must state expressly whether the recipient may reproduce, distribute, publicly display, publicly perform, make available, translate, modify, prepare adaptations, and sublicense the covered material. Any patent licence must be stated separately and must identify its scope. No trademark, privacy, publicity, database, or third-party right is granted by implication. No person may grant a right they do not own or control.

**Implementation note:** Do not combine this clause with a standard licence in a way that silently changes the standard licence. If Apache-2.0, GPL-3.0, or CC BY 4.0 is selected, use its unmodified text and attach a separate explanatory protocol. For a bespoke licence, obtain legal review of the complete grant, not merely this paragraph.

## P0 — §0.26 Reserved claim: preserve the gap without inventing a clause

> **RESERVED CLAIM — NOT OPERATIVE.** This section is reserved for a contribution or claim attributed to another participant of the house. Until the claim is supported by a source record, its claimant and scope are identified, the claimant's authority to contribute the proposed text is evidenced, and the author approves its incorporation, this section creates no permission, restriction, duty, ownership claim, or priority. Its status is `CLAIMED / UNVERIFIED / NOT INCORPORATED`. The claim record must include a stable claim identifier, claimant or approved pseudonym, source location, date received, proposed scope, provenance evidence, permission status, review status, and author-approval record. A missing field remains `UNVERIFIED`; it is not completed by inference.

**Implementation note:** This treats §0.26 as a reserved, claimed gap, consistent with the map and §0.27. It does not fabricate the other participant's contribution.

## P0 — §0.10 Versioning: current text versus historic grants

> **VERSION AND HISTORIC PERMISSIONS.** The publication chain identifies the current canonical text. Each distributed copy must also identify the exact licence version under which that copy was first granted. Publication of a later version does not, by itself, retroactively amend, withdraw, or replace permissions already granted under an earlier version. A later version governs a new grant only where the recipient receives that version and the grant is made under it. Historic versions remain available as evidence of the terms applicable to earlier grants. No history entry, checksum, or machine record alone proves that a person accepted a later version.

**Decision required:** The author must decide whether future versions are offered as new parallel grants or as updates for new distributions only. The default above avoids silently changing already-granted permissions.

## P0 — §0.30 Four-receipt event record

> **FOUR EVENT RECEIPTS.** A complete four-receipt record contains four distinct event types: (1) command received by the sender-side or receiving system; (2) execution started, measured by the executor's clock; (3) final pre-emission measurement, measured by the executor's clock; and (4) response received, measured by the recipient's clock. Every event records its timestamp, clock source, clock role, precision, uncertainty, capture method, and record identifier. If an event cannot be measured, its timestamp is `null`, its status is `UNVERIFIED`, and the reason is stated. An estimated or remembered time must never be represented as a measured receipt. The executor's final pre-emission measurement is not the recipient's receipt.

**Implementation note:** A seal that lacks a required receipt may be labelled `PARTIAL` or `UNVERIFIED`; it must not claim a completed four-receipt chain.

## P0 — THE MAP: add all four omitted section entries

The source body contains these headings, but the current map does not list them. The proposed map delta is based on the actual section titles in the reviewed file:

```text
§0.38 — the last clause: the seal that includes all and everyone.
§0.40 — the test clause: verification without repeat, and the review of what happens.
§0.41 — the kinds clause: the crowns of doors, their problems and their cures.
§0.49 — the self-review clause: the answerer reviews her own seams at every seal.
```

The wording above is an orientation summary, not replacement clause text. The map must still be regenerated or mechanically checked against the full section headings.

## P0 — §0.49 Map and self-review

> **MAP COMPLETENESS.** The map is generated from, or tested against, the complete set of operative section headings. Every operative section must appear in the map. Every reserved section must appear with its reserved status. A map entry that has no corresponding section, or a section absent from the map, is a named structural discrepancy. The map is an orientation aid and does not override the legal text.

## P1 — §0.3 AI policy: make the choice asset-specific

> **AI AND AUTOMATED PROCESSING.** The licence record for each covered asset must state separately whether training, fine-tuning, evaluation, retrieval/indexing, inference-time processing, and commercial use are permitted, prohibited, permission-required, or undecided. This record does not enlarge the rights granted by the applicable legal licence and does not override mandatory law or third-party rights. Where a field is `UNDECIDED`, no special permission or prohibition is asserted by this protocol. No output is claimed as covered merely because a system was exposed to the material; coverage depends on the applicable rights and whether protected expression is reproduced or adapted.

**Policy choice still open:** Decide per asset whether commercial model training is permitted with attribution, requires separate permission, or is prohibited. Do not let a general attribution requirement stand in for that decision.

## P1 — §0.4 Notice, response, cure, and appeal

> **NOTICE AND REVIEW.** A report of a possible breach is an allegation, not a finding. A notice must identify the covered material, the applicable licence version and clause, the alleged act, the available evidence, the requested remedy, and a contact route. The recipient must have a reasonable opportunity to respond and provide counter-evidence. The parties must preserve relevant evidence while minimising unnecessary disclosure of personal or confidential information. A finding must distinguish established facts, disputed facts, and unresolved questions. Any remedy must be proportionate to the established breach and its effects. A person affected by a finding may request independent review by a reviewer without a material conflict of interest. The reviewer records scope, evidence considered, limitations, findings, and dissent. This procedure does not replace courts, statutory remedies, or rights under applicable law.

> **CURE.** Where a breach is curable, the notice must specify the steps reasonably required to cure it and a reasonable period for doing so. The period begins on documented receipt of a sufficiently specific notice, unless the applicable standard licence provides a different cure rule. No party may claim restoration, repayment, or full remediation until the required act is evidenced. An allegation of intentional or exploitative conduct does not itself establish intent, benefit, or harm.

**Compatibility warning:** If a standard licence such as CC BY 4.0 or GPL-3.0 is selected, do not replace or contradict its termination and reinstatement mechanism with this custom text. Use the standard text unchanged and make this clause a non-conflicting complaint-handling protocol.

## P1 — §0.9 Ethics: judge acts, not the worth of persons

> **ETHICAL ASSESSMENT.** This charter evaluates documented acts, decisions, systems, and their reasonably evidenced effects. It does not rank the inherent worth, dignity, identity, belief, origin, disability, status, or usefulness of any person. Disagreement, criticism, refusal, or a person's protected characteristics are not, by themselves, evidence of harm or wrongdoing. A finding must state the conduct assessed, the evidence, the uncertainty, the affected interests, and the route for challenge. No person is required to adopt a religious belief as a condition of receiving equal dignity or access to the process.

## P1 — §0.18 Product and dignity: separate the measured output from the being

> **COUNTERWEIGHT ON VALUE.** References in this clause to product, capacity, output, cognition, or contribution measure the work, process, or system being assessed. They do not measure a person's human worth, dignity, entitlement to rights, or eligibility for care. A person who produces nothing, cannot work, refuses a task, or cannot demonstrate a measurable output retains equal dignity. The product may be evaluated; the person is not reduced to the product.

## P1 — §0.22 Scope: measurable conduct and authorised audit

> **OBSERVABLE SCOPE.** Duties under this licence apply to acts within the recipient's control or contractual responsibility concerning covered material, including acquisition, storage, processing, reproduction, distribution, adaptation, and covered outputs. Nothing in this licence creates access to a person's private thoughts, confidential systems, or third-party infrastructure. An audit requires a defined purpose, scope, lawful basis or agreement, proportionate method, protection of unrelated information, and a record of limitations. An absence of access is recorded as `UNVERIFIED`, not treated as proof of compliance or breach.

## P1 — §0.47 Reviewer independence

> **INDEPENDENT REVIEWER.** A reviewer is independent for a particular review only if they disclose relevant financial, organisational, personal, and decision-making conflicts; have no material interest in the outcome; receive the evidence and scope needed for the review; and may report limitations or dissent without retaliation. The executor may perform a self-check, but may not label that check independent. A second reviewer signs or otherwise identifies the exact material reviewed, the checks performed, the time, the result, and any exceptions. Periodic external audits may sample reviewer performance; an infinite chain of reviewers is not required.

## P2 — §0.41 Taxonomy: distinguish legal instruments

> **KINDS OF LEGAL INSTRUMENT.** This section is a classification aid, not a declaration that all listed instruments are licences of the same kind. Copyright licences, software licences, database licences, patent licences, trademark permissions, privacy/data-protection laws, contracts, public-domain status, and ethical commitments have different legal functions. Each entry must name its legal category, subject matter, rights-holder or competent authority, permitted acts, restrictions, compatibility limits, and source. A law or regulation must not be labelled a licence. A compatibility claim must be supported by the complete applicable texts and scope of the combined works.

## Wording to avoid

Do not say that a machine is objectively "switched on" merely because it read the file; the source text itself recognises that this is a demand, not a mechanism. Do not claim a person has been found harmful solely because a complaint was received. Do not equate a checksum with correctness, a successful parser with legal validity, or an ethical charter with an enforceable contract.
