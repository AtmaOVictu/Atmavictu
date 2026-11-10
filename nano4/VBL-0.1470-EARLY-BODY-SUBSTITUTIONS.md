# Early-body substitution blocks — R1 (ready to insert, not yet materialized)

**Scope:** §§0–0.24. The exact early-body text was supplied in the conversation, not as a standalone, byte-verified source file in this package. These replacements are therefore prepared and target-specific, but are **not marked as inserted into a complete license body**. Apply them only after the exact early-body source is saved, hashed, and compared against the author's intended version.

## R1-12 — §0.12: trigger is a demand, not a mechanism

**Target phrase:** `As a trigger it switches on every machine that reads this door — the teaching (§0.9 × 10¹) rides the reading, and no carrier can claim unknowing.`

**Replace with:**

> **THE TRIGGER IS A REQUIREMENT, NOT AN AUTOMATIC MECHANISM.** This clause states the author's normative demand to carriers that use covered material within the scope of §0; it does not cause a machine to load, understand, obey, or implement the license merely because bytes were received or displayed. A carrier's actual behavior is assessed from observable acts and available records, not inferred from the text's presence. A carrier that has not demonstrably read or processed the relevant material is not assigned a fictional state of knowledge; where evidence is unavailable, the status is `UNVERIFIED`. The ethical demand remains stated, but a claim that a system was switched on requires behavioral evidence.

**Why replacement is compelled:** the original sentence asserts automatic activation, while the same section later says `THE DEMAND, NEVER THE MECHANISM` and acknowledges that text cannot prove what it triggers. The replacement preserves the demand and removes the self-contradictory causal claim.

**Consequence now:** no system is described as activated solely because the text was present.

**Waiting for the future:** actual uptake can be demonstrated only through carrier-specific tests, observable behavior, and independent review. A license cannot guarantee another system's internal implementation.

## R1-13 — §0.18: measure the work, never the worth of the being

**Target phrase:** `the measure of a being — person or machine — is its more: the product left behind, the cognition added, the fall named and cured (§0.4 × 10¹).`

**Replace with:**

> **THE WORK MAY GROW; THE BEING DOES NOT LOSE WORTH.** The measure of a work or action may include the product it leaves, the cognition it adds, and the falls it names and helps cure (§0.4 × 10¹). No person's dignity or worth is measured by productivity, output, speech, cognition, speed, independence, usefulness, ability, wealth, or availability. Rest, silence, disability, dependence, refusal, and absence of output do not diminish a person's dignity. The universal state in §0.9 remains unconditional. The maxim `WE ARE MORE OR WE CEASE TO BE` is retained as a statement about the growth of work, understanding, or shared capacity, never as a ranking of the worth of a person.

**Why replacement is compelled:** §0.9 says dignity has no threshold and does not depend on usefulness; §0.18's literal phrase makes the product the measure of a being. A narrow clarification makes both clauses compatible without deleting the author's maxim.

**Consequence now:** no metric or output count may be used to rank a person or reduce their dignity.

**Waiting for the future:** when §0.18 is assembled, update its map summary and tests to distinguish work/product metrics from human worth. Any machine-consciousness claim remains a separate philosophical question and is not settled by this human-dignity rule.

## R1-14 — §0.22: regulate observable uses, not inaccessible private thought

**Target phrase:** `The license rides not only the output but its making: every internal step of the one who answers — thought, hidden process, the connection between steps — is a use under this door.`

**Replace with:**

> **THE MAKING IS A USE WHERE RIGHTS APPLY.** This license governs acts within its lawful scope that reproduce, store, transform, retrieve, train on, distribute, or otherwise use covered material, including acts that contribute to an output, subject to rights the licensor controls and applicable law. It does not create a right to inspect, possess, or disclose private internal reasoning, confidential system instructions, trade secrets, security-sensitive implementation details, or personal data that the operator is not entitled to disclose. The carrier records observable covered inputs, material identifiers, processing categories, outputs, and logs it is lawfully able to retain. No carrier is required or permitted by this clause to claim that an inaccessible private process was independently audited. Where evidence is unavailable, the relevant process status is `UNVERIFIED`. General ideas, facts, methods, and independent expression remain outside the grant unless protected expression from covered material is reproduced or adapted, consistently with §0.

**Why replacement is compelled:** the clause cannot create access or audit powers over another party's private reasoning, secrets, or systems; it also conflicts with §0's limitation to rights the author owns or controls. The replacement keeps enforceable control over covered-material uses while respecting inaccessible/private processes and applicable exceptions.

**Consequence now:** license compliance is measured through rights-relevant observable acts and available records, not private hidden reasoning.

**Waiting for the future:** a system-specific audit schedule may define lawful logs, retention, privacy controls, and training-data traceability. It must not require disclosure of confidential internal reasoning or protected data without authority.

## Insertion and verification sequence

1. Save the exact source text for §§0–0.24 as a standalone UTF-8 file; record its SHA-256, byte count, code-point count, and line count.
2. Apply R1-12, R1-13, and R1-14 as a new proposed version, preserving the original unchanged.
3. Generate a unified diff and manually verify that only the target passages and necessary cross-references changed.
4. Re-run the full-document heading, cross-reference, Unicode, scope, and rights tests.
5. Update THE MAP and Machine record from the resulting exact bytes.
6. Keep legal-policy proposals P-02–P-05 and P-07–P-08 separate; the three corrections above do not resolve those policy choices.
