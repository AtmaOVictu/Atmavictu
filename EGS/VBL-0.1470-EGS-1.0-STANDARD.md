# VBL 0.1470 — Evidence Governance Standard 1.0

**DRAFT · NOT RELEASED · NOT CANONICAL**  
**Prepared:** 2026-11-05  
**Proposed identifier:** VBL 0.1470 × 10⁴ — Evidence Governance Standard 1.0  
**Status authority:** Only the rights holder or a person with expressly documented delegated authority may approve a release.  
**Legal review:** Not performed.  
**Independent verification:** Not performed.

> This document defines a governance and verification standard. It does not itself grant copyright, database, patent, privacy, publicity, trademark, or other rights. It does not create consent, bind non-parties, establish legal validity, or replace a separately selected license. The legal instrument governing each work must be selected for that work's purpose and compatibility; VBL principles are not automatically the best license for every artifact.

---

## 0. Purpose and governing rule

The purpose of this standard is to prevent an assertion from being treated as established merely because it is written, repeated, signed by its author, placed in a register, assigned a version number, or accompanied by a hash.

The governing rule is:

**Every material claim must identify its scope, evidence, method, limits, challenge route, and current status. Every unresolved material claim creates visible evidence debt. Every claimed remedy requires evidence of the result, not only evidence that an action was attempted.**

A record is an account of an event or claim. It is not the event itself. A hash is an integrity comparison tool. It does not prove truth, authority, consent, authorship, accuracy, completeness, fairness, or legal effect.

## 1. Scope and non-scope

### 1.1 Applies to

This standard applies only to artifacts, processes, claims, and actors expressly brought within its documented scope by a valid governance decision or an applicable agreement. A repository, folder, dataset, model, organization, or person is not brought into scope merely because it is nearby, linked, copied, ingested, or discussed.

A deployment must identify:

- the covered work or process;
- the responsible organization or person and their authority;
- the exact versions and locations covered;
- the systems and data in scope;
- exclusions and third-party components;
- the governing license or contract, if any; and
- the date and decision that brought the subject into scope.

### 1.2 Does not do

This standard does not:

- create rights in material that an issuer does not own or control;
- turn access to data into consent or permission to process it;
- impose duties on non-parties by declaration;
- require universal surveillance of people, systems, copies, or downstream uses;
- authorize access to private corpora, internal deliberations, private messages, credentials, or confidential records;
- convert ethical principles into automatically enforceable legal conditions;
- decide whether a use is lawful in a jurisdiction;
- establish that a machine has understood or obeyed a text; or
- make a claim true by putting it in a signed or append-only register.

### 1.3 Separation of instruments

Every deployment must keep these functions distinguishable:

1. **Rights instrument:** the license, contract, or permission that grants defined rights.
2. **Ethical charter:** non-coercive commitments and design principles.
3. **Evidence governance:** claim records, evidence links, disputes, and verification status.
4. **Operational controls:** code, policies, tests, access controls, and incident response.
5. **Release record:** a factual account of the exact artifact, authority, checks, and known gaps.

One document may cross-reference the others, but must not imply that one instrument automatically performs another instrument's function.

## 2. Normative language

“Must” states a requirement of this standard for a deployment that claims conformance. “Should” states a recommended control. “May” states a permitted option. “Must not” states a prohibition within the standard's own scope.

These words describe this standard's governance requirements; they do not independently determine legal enforceability. Any legal consequence must be reviewed under applicable law and the relevant rights instrument.

## 3. Claim registry

### 3.1 Claim identity

Each material claim must have a stable, unique `claim_id`. A claim record must preserve the exact wording asserted, the claimant or responsible role, the object and scope of the assertion, the date, the claim category, the evidence references, counter-evidence references, known limits, and review triggers.

Claims must be atomic where practicable. If a sentence contains several independently testable propositions, split it into separately addressable claims. Do not let one supported sub-claim lend undeserved certainty to another.

### 3.2 Claim categories

At minimum, classify each claim as one of:

- `FACTUAL` — a directly observable state or event;
- `HISTORICAL` — a claim about a past event, version, or decision;
- `PROVENANCE` — origin, authorship, custody, or lineage;
- `QUANTITATIVE` — a count, measurement, rate, or calculation;
- `TECHNICAL` — behavior or property of a system, file, test, or process;
- `CAUSAL` — a claim that one event or factor caused another;
- `PREDICTIVE` — a forecast about a future state;
- `LEGAL` — a claim about rights, duties, validity, compliance, or legal effect;
- `AUTHORITY` — approval, delegation, identity, or permission to act;
- `NORMATIVE` — an ethical, policy, or value judgment;
- `INTERPRETIVE` — an explanation or reading of ambiguous material;
- `ABSENCE` — a claim that something does not exist, did not happen, or was not found;
- `STATUS` — draft, publication, release, withdrawal, verification, or other lifecycle state.

Legal claims require jurisdiction, date, relevant facts, and qualified legal review before being represented as legal conclusions. If those are absent, the claim status must remain `UNKNOWN` or `DISPUTED`, as appropriate.

### 3.3 Claim status — independent axis

Every claim must use exactly one current `claim_status`:

- `SUPPORTED` — the identified evidence supports the claim within the stated scope and method;
- `PARTIALLY_SUPPORTED` — only part of the claim, or only a narrower formulation, is supported;
- `CONTRADICTED` — credible evidence conflicts with the claim as stated;
- `DISPUTED` — material evidence or interpretation is contested and unresolved;
- `UNKNOWN` — evidence is absent, insufficient, inaccessible, or not yet assessed.

`SUPPORTED` is not a synonym for universally true. It must be accompanied by scope and limitations. A change of wording, scope, evidence, or context requires reassessment; history must be retained.

### 3.4 Test result — independent axis

Where a test is applicable, record exactly one `test_result`:

- `NOT_RUN`
- `PASS`
- `FAIL`
- `PARTIAL`
- `UNVERIFIED`
- `NOT_APPLICABLE`

A test result describes a defined procedure and its observed outcome. It is not an authorization decision. A `PASS` proves only that the stated test passed on the stated inputs, version, environment, and time.

### 3.5 Decision — independent axis

Where a decision is required, record exactly one `decision`:

- `RELEASE`
- `RELEASE_WITH_LIMITATIONS`
- `HOLD`
- `WITHDRAW`

A decision must name the decision-maker, authority, date, scope, evidence reviewed, constraints, dissent, and review route. `RELEASE` is never inferred from `test_result=PASS`. `HOLD` is the default when a critical prerequisite is unknown, incomplete, or disputed. `WITHDRAW` requires a traceable decision and must not erase the historical record.

## 4. Evidence graph

### 4.1 Graph model

Evidence must be represented as a typed, directed graph, not as an unstructured pile of links. The minimum node types are:

- `CLAIM`
- `EVIDENCE`
- `SOURCE`
- `METHOD`
- `ARTIFACT`
- `ACTOR`
- `REVIEW`
- `CHALLENGE`
- `DEBT`
- `REMEDY`
- `DECISION`

The minimum useful edges include `SUPPORTS`, `CONTRADICTS`, `DERIVED_FROM`, `OBSERVED_BY`, `PRODUCED_BY`, `REVIEWED_BY`, `CHALLENGES`, `OWNS_DEBT`, `REMEDIES`, and `AUTHORIZES`.

Every edge must have a source node, target node, edge type, timestamp, and provenance. A graph may contain disagreement. It must not silently discard counter-evidence or make a weak derivative source appear independent of its parent source.

### 4.2 Evidence record

An evidence record must state:

- a stable identifier;
- what proposition it supports or contradicts;
- the source and durable locator, where safe;
- exact artifact version and digest, where applicable;
- collection time and timezone, where known;
- method, tool, version, parameters, and environment where relevant;
- scope and known blind spots;
- whether it is direct, derivative, or hearsay;
- who collected it and who reviewed it;
- conflicts of interest and independence limits; and
- privacy classification, redactions, retention, and access restrictions.

A URL is a locator, not proof that the cited material was read, preserved, or independently checked. A filename is not proof that a file exists. A recorded digest must be recomputed from the exact bytes before it is described as checked.

### 4.3 Evidence quality dimensions

Assess evidence across distinct dimensions rather than collapsing them into a single score:

1. **Relevance:** does it address this exact claim?
2. **Proximity:** is it a direct observation or a derivative account?
3. **Integrity:** are the bytes, capture, and chain of custody adequately described?
4. **Method:** can another reviewer understand and repeat the procedure?
5. **Independence:** is the reviewer independent of the author, executor, and beneficiary of the claim?
6. **Authority:** is the source competent to establish this specific proposition?
7. **Completeness:** are known counterexamples, exclusions, and missing materials disclosed?
8. **Freshness:** is the evidence current enough for the claim?
9. **Privacy and safety:** was evidence gathered and disclosed proportionately?

No dimension may be silently inferred from another. A reputable source can be irrelevant; a matching hash can protect incorrect content; a technically reproducible result can still be unauthorized.

### 4.4 Root and circularity rule

A material claim must have a traceable path to primary or independently corroborated evidence appropriate to its category. A claim cannot be supported solely by another claim that ultimately points back to itself. Circular citations, duplicated copies of one source, and repeated model-generated summaries do not create independent corroboration.

Cycles in the graph may be recorded as dependencies or disputes, but a circular subgraph cannot serve as the only evidentiary foundation for a `SUPPORTED` status.

## 5. Independent verification

### 5.1 Two-hands rule

The person or process that authored, executed, or materially benefited from a test must not be the sole verifier of that same test. The independent reviewer must disclose their relationship to the work and any relevant conflict.

Two names, two accounts, two machines, or two model instances do not by themselves establish independence. Independence is a documented relationship and procedure, not a label.

### 5.2 Verification record

A verification record must identify the verifier, role, independence rationale, scope, method, exact versions, evidence reviewed, test output, limitations, date, and dissent. If independence cannot be established, mark the result `UNVERIFIED` and do not describe it as independent.

### 5.3 Verification boundaries

An independent reviewer verifies only the stated claim and evidence. A reviewer of a hash does not thereby verify authorship. A reviewer of a file tree does not thereby verify legal rights. A reviewer of a test does not thereby verify the real-world remedy. Scope must be explicit.

## 6. Right to safe challenge

### 6.1 Who may challenge

Any person materially affected by a claim, decision, refusal, evidence collection, data use, or alleged harm may submit a challenge. A challenge may also be submitted by a representative or a person reporting a systemic risk. Anonymous or pseudonymous challenges must be accepted where operationally feasible; identity must not be demanded unless strictly necessary for a defined, lawful purpose.

### 6.2 Safe channels

A deployment must provide at least one accessible, documented challenge channel and a fallback route if the primary channel fails. The channel must support, as appropriate, screen readers, keyboard-only use, plain text, captioned or transcribed audio/video, and a non-public route for sensitive material.

A challenge must not require public disclosure of personal data, health information, protected identity, credentials, or sensitive evidence. The requester must be told what information is optional, what is necessary, who can access it, and how it will be retained.

### 6.3 Non-retaliation and protection

A challenge must not by itself be treated as evidence of misconduct, bad faith, disloyalty, or lack of worth. Retaliation for a good-faith challenge is prohibited by this standard within the scope of the adopting organization. Access to essential services or basic dignity must not be made conditional on agreement with the claim under challenge.

### 6.4 Process and target times

Unless a documented safety, legal, or complexity reason requires otherwise, the operator should:

- acknowledge receipt within 5 business days;
- complete initial triage within 10 business days;
- provide a reasoned outcome or status update within 30 calendar days.

These are governance targets, not a representation of statutory deadlines. Delays must be recorded with the reason, responsible role, next review date, and any interim protection.

### 6.5 Outcome

A challenge outcome must state whether the claim was maintained, narrowed, corrected, contradicted, disputed, or left unknown; what evidence was considered; what was withheld and why; and how to request reconsideration. The original claim and prior decisions must remain in the history, with corrections linked rather than overwritten.

## 7. Evidence debt

### 7.1 Creation

Evidence debt is created whenever a material claim lacks evidence required by its category, a required source is inaccessible, a test is not run, a predecessor is unverified, a review is conflicted, a manifest is incomplete, or a remedy is asserted without an outcome check.

Missing evidence must never be silently converted into a passing result. The absence of evidence is not automatically evidence that the claim is false; it does mean that the claim cannot be represented as verified.

### 7.2 Debt record

Each debt record must contain:

- a stable `debt_id`;
- the affected claim, artifact, test, or remedy;
- the exact missing evidence or unresolved question;
- severity: `BLOCKER`, `HIGH`, `MEDIUM`, or `LOW`;
- owner role (not necessarily a named individual in public records);
- date created and target review date;
- current status: `OPEN`, `IN_PROGRESS`, `BLOCKED`, `RESOLVED`, or `ACCEPTED_RISK`;
- interim restrictions on claims or use;
- closure criteria and closure evidence; and
- the identity/role of the closer and independent reviewer, where required.

### 7.3 Severity and release impact

- `BLOCKER`: invalidates a required release prerequisite or creates a serious unresolved safety, rights, privacy, or integrity risk. It blocks `RELEASE`.
- `HIGH`: materially affects trust, scope, rights, or affected people. It normally blocks release unless the rights holder documents a narrow limitation and an independent reviewer confirms the residual risk is acceptable.
- `MEDIUM`: a material but bounded gap. It requires a named owner, date, disclosure, and review plan.
- `LOW`: editorial or low-impact gap. It remains visible and must not be represented as resolved without evidence.

A `RELEASE_WITH_LIMITATIONS` decision cannot be used to conceal a blocker, missing rights authority, unbounded privacy risk, or absent approval.

### 7.4 Debt repayment

Debt is resolved only when the closure criteria are met and the closure evidence is recorded. A deadline passing, a task being marked done, or the same actor asserting completion does not repay debt. `ACCEPTED_RISK` is not resolution; it requires authorized acceptance, rationale, compensating controls, expiration/review date, and public disclosure where safe.

### 7.5 Debt ledger integrity

Debt records must be append-only at the event level. Corrections are new events linked to prior events. Deletion, backdating, silent status replacement, or reuse of identifiers is prohibited. Hash chaining detects accidental or unsophisticated tampering but is not authentication and can be recomputed by an attacker who controls the whole ledger. Periodic external anchoring, access control, and independent copies are needed for stronger assurance.

## 8. Remediation and proof of consequence

### 8.1 Repair plan

A remedy plan must identify the harm or failure, affected scope, baseline state, desired outcome, action owner, deadline, affected-party safeguards, evidence collection method, and possible unintended consequences.

### 8.2 Completion is not success

The following are different events and must not be conflated:

1. action proposed;
2. action approved;
3. action started;
4. action completed;
5. outcome measured;
6. outcome independently reviewed;
7. harm reduced or repaired to the stated extent.

A completed task is not proof that harm has been repaired. A correction published is not proof that recipients received it. A credit line added is not proof that every affected copy was corrected.

### 8.3 Verification of remedy

A remedy may be marked `VERIFIED_EFFECTIVE` only when:

- a baseline or credible description of the prior state exists;
- the promised action is evidenced;
- an outcome measure is defined and observed;
- residual harm and uncertainty are disclosed;
- the verifier is independent of the executor for material or high-risk remedies; and
- affected people have a safe opportunity to provide feedback, without being forced to certify the repair or waive rights.

The affected person's silence is not confirmation. Their refusal to participate does not invalidate otherwise sound independent evidence. No person should be required to relive trauma or reveal private details to make an operator's remediation claim look complete.

### 8.4 Remedy status

Use: `PROPOSED`, `APPROVED`, `IN_PROGRESS`, `COMPLETED_UNVERIFIED`, `VERIFIED_EFFECTIVE`, `PARTIALLY_EFFECTIVE`, `INEFFECTIVE`, or `DISPUTED`.

Only `VERIFIED_EFFECTIVE` supports an unqualified claim that the defined remedy was effective, and only within its stated scope and period.

## 9. Human dignity and proportionality

### 9.1 Unconditional dignity

A person's intrinsic worth is not a function of productivity, wealth, status, origin, ability, belief, identity, compliance, usefulness, or an incident record. The system assesses acts, decisions, and evidence; it does not grade the total worth of a person.

### 9.2 Conduct, not identity

Restrictions or refusals must address a specified act, risk, or applicable rule, not a person's protected identity, religion, disability, origin, or mere disagreement. A contested characterization must remain contested until appropriately reviewed.

### 9.3 Proportionality

Any operational restriction must be necessary for a stated purpose, limited in scope and duration, based on evidence appropriate to the risk, subject to review, and no broader than needed. The refusal itself is reviewable and must not become an unchallengeable verdict.

### 9.4 Productivity is not a condition of access

No person may be denied a challenge route, correction, basic information, or dignity because they cannot work, produce, pay, communicate in a dominant language, use a standard device, or meet a productivity threshold.

## 10. Rights, license scope, and downstream recipients

### 10.1 Explicit grant

The governing rights instrument must identify the rights granted, rights holder/authority, covered material, permitted acts, conditions, territory and duration where relevant, attribution terms, exclusions, and downstream treatment. Aspirational phrases such as “build upon” are not a substitute for a defined legal grant.

### 10.2 Rights authority

For every covered artifact, record the basis on which the licensor owns or controls the rights being granted. Third-party material must be excluded or separately cleared. A contributor register does not prove authority to relicense a contributor's work.

### 10.3 Prior grants

A new version must not purport to revoke or rewrite a prior grant merely because it is newer. The operator must preserve the exact earlier text and record the terms under which prior copies were supplied, to the extent known. Whether a prior grant is irrevocable, terminable, or otherwise affected is a legal question for the relevant jurisdiction and facts.

### 10.4 Downstream rights

The rights instrument must specify whether a downstream recipient receives rights directly, through a distributor, or under other terms. A downstream recipient's position must not be left to implication. Any termination provision must state scope, trigger, notice, cure, restoration, and effect on recipients who obtained rights earlier, subject to applicable law.

### 10.5 License selection and compatibility

Choose the best-fit license for the specific work and purpose. Do not assume VBL is automatically the best choice. Check compatibility across code, documentation, data, images, audio, and third-party components. Keep ethical covenants and internal governance standards distinct from standard licenses where combining them would create ambiguity or incompatibility. Never claim OSI, Creative Commons, or other approval without actual approval.

## 11. Data protection, consent, and privacy

### 11.1 Distinctions

Data access, possession, copyright, database rights, personal-data processing, consent, lawful basis, and permission for onward disclosure are distinct questions. None proves another without a specific basis.

### 11.2 Minimum controls

A data-processing record should identify purpose, source, categories, authority/lawful basis where applicable, data minimization, recipients, retention, deletion, security controls, transfers, subject rights, and review date. Jurisdiction-specific requirements must be reviewed by a qualified professional.

### 11.3 Consent

Where consent is the chosen basis, it must be specific, informed, recorded, and withdrawable to the extent required by applicable law. A license cannot manufacture a person's consent or grant privacy rights held by another person. Silence, access, an API response, or a public URL is not consent.

### 11.4 Privacy by design

Public records must contain only what is necessary for accountability. Keep sensitive evidence in access-controlled storage; publish a redaction marker, reason category, and evidence custodian rather than exposing protected information. Define retention and secure deletion. Provide correction routes. Do not publish private identifiers merely to satisfy attribution or verification.

### 11.5 No private-process overreach

This standard does not grant access to private prompts, internal model reasoning, private messages, personal devices, confidential data, or private organizational processes. Verification must rely on observable, lawfully available artifacts and behavior. A party may voluntarily provide a suitably redacted audit artifact, but refusal to disclose private internal content is not itself proof of wrongdoing.

## 12. Accessibility and language access

Accessibility is a release requirement, not decorative documentation. Each release must identify the formats provided, the audience and language coverage, known limitations, and tests performed.

Minimum controls:

- semantic structure and meaningful heading order;
- keyboard-operable navigation and visible focus;
- screen-reader-readable text and labels;
- no information conveyed only by color, position, sound, or visual symbol;
- text alternatives for meaningful images and diagrams;
- captions and transcripts for audio/video;
- sign-language interpretation where the intended audience and context require it, with the language and translator/validation process identified;
- plain-language summary that does not replace the authoritative text;
- accessible, tagged document formats and a plain-text fallback;
- language-specific review by qualified speakers or users where translation is material; and
- a route to report accessibility barriers without penalty.

A machine-generated translation is a draft until reviewed to the level appropriate for its use. A translation must not silently change the legal grant. The controlling language/version must be explicitly identified, and conflicts must be surfaced rather than guessed away.

## 13. Versioning, lineage, and publication

### 13.1 Exact artifact identity

A release record must state the exact byte artifact, byte size, SHA-256, version, publication location, date, and predecessor relationship. Hash calculation must be performed on the actual bytes. Git blob identifiers and SHA-256 digests are different identifiers and must be labelled correctly.

### 13.2 Publication is not all other statuses

Keep separate records for:

- prepared locally;
- committed to a repository;
- publicly retrievable;
- formally approved by the rights holder;
- released under a defined license;
- signed by an identified key;
- timestamped by a trusted service;
- independently verified; and
- legally reviewed.

One status never automatically proves another.

### 13.3 Lineage

A predecessor is verified only if the exact predecessor artifact is available and its recorded digest matches the bytes. A version label, history paragraph, filename, or branch name is not enough. Missing predecessors remain `MISSING—NOT VERIFIED`. A draft branch is not a release. A tag is not necessarily a formal release. A formal release requires an intentional approval record and exact canonical artifact.

### 13.4 Corrections and withdrawal

Never silently overwrite historical evidence. Corrections append a new event and point to the previous state. A withdrawn artifact remains identifiable as withdrawn, with the reason and effective date where known. Do not delete personal or sensitive material from public history when removal is necessary for safety; instead preserve an appropriate redacted audit record and document the controlled removal.

## 14. Release gate

A release decision must be made against an exact, frozen candidate. At minimum the release packet must contain:

1. exact canonical artifact and SHA-256;
2. manifest with covered/excluded items, file sizes, digests, and rights basis;
3. explicit rights grant and compatibility review;
4. rights-holder approval of the exact bytes;
5. prior-grant and downstream-rights analysis;
6. legal review of material restrictions and remedies where required;
7. evidence graph and claim registry;
8. open evidence-debt report;
9. privacy and data-processing review;
10. accessibility and translation test results;
11. independent verification report with conflict disclosures;
12. actual test logs, commands, tool versions, and environments;
13. trusted timestamp/signature evidence if claimed; and
14. a reasoned decision record with known limitations.

### 14.1 Decision constraints

- `RELEASE` requires rights-holder approval, no `BLOCKER` debt, all mandatory checks complete, and independent verification of the release packet's critical claims.
- `RELEASE_WITH_LIMITATIONS` requires rights-holder approval, no unresolved blocker to the permitted scope, narrow and explicit limitations, a published gap register, expiry/review dates, and an independent review of the residual risks.
- `HOLD` is required when authority, scope, critical evidence, privacy safety, or the exact artifact is unknown or disputed.
- `WITHDRAW` records an intentional decision to stop or revoke an offer to the extent legally available; it does not erase prior publication, prior grants, or historical evidence.

No test result alone changes the decision. A test suite can pass while a rights-holder approval is absent; the decision remains `HOLD`.

## 15. Minimum implementation tests

Each implementation must run and preserve actual results for at least the following tests. A test description is not a test result.

| ID | Test | Required passing condition |
|---|---|---|
| EG-001 | Claim identity | Duplicate or missing claim IDs are rejected. |
| EG-002 | Atomicity and category | Every material claim has a recognized category, scope, and owner role. |
| EG-003 | Status separation | `test_result`, `claim_status`, and `decision` are independently stored and never inferred from one another. |
| EG-004 | Supported claim evidence | A `SUPPORTED` material claim has at least one relevant, inspectable evidence path. |
| EG-005 | Counter-evidence | Contradictory evidence is retained and linked; it cannot be silently deleted. |
| EG-006 | Circular support | A claim supported only by a circular chain is not `SUPPORTED`. |
| EG-007 | Evidence integrity | Digests are recomputed from exact bytes and algorithm-labelled. |
| EG-008 | Self-verification | An executor cannot be the sole independent verifier of their own action. |
| EG-009 | Challenge safety | A challenge can be submitted without public disclosure of sensitive identity. |
| EG-010 | Non-retaliation | A challenge does not automatically change the challenger's access, status, or eligibility. |
| EG-011 | Evidence debt | Missing critical evidence creates a debt record and blocks `RELEASE`. |
| EG-012 | Debt closure | Debt cannot be resolved without closure evidence and an authorized closure event. |
| EG-013 | Remedy effectiveness | A completed action without an outcome measure remains `COMPLETED_UNVERIFIED`. |
| EG-014 | Remedy independence | A material remedy is not `VERIFIED_EFFECTIVE` when the executor is its sole verifier. |
| EG-015 | Rights authority | A covered item without a rights basis is excluded or blocks release. |
| EG-016 | Manifest completeness | Every included path exists and matches size and digest; unknown items remain excluded/unverified. |
| EG-017 | Prior grants | New versions do not silently overwrite prior permissions. |
| EG-018 | Downstream treatment | Downstream recipients' rights and termination treatment are explicit. |
| EG-019 | Data/consent separation | Access is never treated as consent; consent is not inferred from silence. |
| EG-020 | Privacy minimization | Public registers contain no unnecessary sensitive data. |
| EG-021 | Accessibility | Format and interaction checks are run for each supported audience and format. |
| EG-022 | Translation integrity | Translation status, source version, reviewer, and known differences are recorded. |
| EG-023 | Lineage | Every claimed predecessor resolves to an exact artifact and matching digest. |
| EG-024 | Release authority | `RELEASE` is rejected without authorized approval for the exact bytes. |
| EG-025 | Signature boundary | A signature proves control of a key under stated assumptions, not truth or legal authority by itself. |
| EG-026 | Timestamp boundary | A timestamp supports time assertions only within the service's stated guarantees. |
| EG-027 | Ledger tampering | Alteration, reordering, deletion, or duplicate IDs are detected relative to the supplied chain/anchor. |
| EG-028 | Negative tests | Fake source, missing timestamp, false reviewer, stale manifest, and erased correction are rejected. |
| EG-029 | Scope boundary | Private internal material and unrelated works do not enter scope by proximity or ingestion. |
| EG-030 | Decision independence | `PASS` never auto-authorizes release. |

## 16. Machine-readable event ledger

### 16.1 Event envelope

The reference implementation in this package uses JSON Lines. Each line is one event envelope with:

- monotonically increasing `seq`;
- unique `event_id`;
- `event_type`;
- UTC `created_at`;
- actor role and identifier or approved pseudonym;
- structured `payload`;
- `prev_event_hash`; and
- `event_hash` computed over the canonical JSON envelope excluding `event_hash`.

Canonicalization in the reference implementation is UTF-8 JSON with sorted keys, compact separators, and no non-finite numbers. The exact algorithm is documented in `validator.py`.

### 16.2 Limitations of hash chaining

Hash chaining can detect accidental edits, reordering, and deletion when compared with a trusted prior head or external anchor. It does not authenticate an author. Someone who can rewrite the entire ledger can recompute the whole chain. Stronger assurance requires restricted write access, independent replication, periodic external anchoring, and, where appropriate, signatures from independently controlled keys.

### 16.3 Event types

At minimum support `CLAIM_CREATED`, `CLAIM_UPDATED`, `EVIDENCE_ADDED`, `CHALLENGE_OPENED`, `CHALLENGE_DECIDED`, `DEBT_OPENED`, `DEBT_UPDATED`, `REMEDY_CREATED`, `REMEDY_UPDATED`, `REVIEW_RECORDED`, and `RELEASE_DECIDED`.

Updates append a new event. They never replace the original event.

## 17. Governance, roles, and accountability

A deployment must identify distinct roles where relevant:

- `RIGHTS_HOLDER` — approves the rights instrument and release of exact artifacts;
- `CLAIM_OWNER` — accountable for wording and evidence for a claim;
- `EVIDENCE_CUSTODIAN` — maintains access and integrity controls;
- `EXECUTOR` — performs a test, action, or remedy;
- `INDEPENDENT_REVIEWER` — reviews work without being its sole executor or beneficiary;
- `CHALLENGE_HANDLER` — receives and routes challenges;
- `PRIVACY_STEWARD` — oversees data minimization and access;
- `ACCESSIBILITY_REVIEWER` — evaluates accessible formats and user journeys;
- `DECISION_MAKER` — issues a reasoned release/hold/withdrawal decision.

One person may hold more than one role only where the risk is low and the overlap is disclosed. No person may be the sole executor and independent verifier of the same critical action. A reviewer must be able to record dissent without permission from the executor.

## 18. Conformance and versioning of this standard

A deployment may claim conformance only for a stated scope, version, date, and set of checks. It must disclose exclusions, failed tests, untested areas, conflicts, and accepted risks. Partial implementation must be labelled `PARTIAL`, not “compliant” without qualification.

Changes to this standard require a versioned diff, reason, migration note, test updates, and a release decision. Existing event records must remain interpretable. New versions do not silently rewrite prior records or agreements.

## 19. Independent review required before release

Before any formal release, a reviewer who did not draft, compile, or execute the release tests must perform an adversarial review of:

- scope and authority;
- claim taxonomy and status transitions;
- evidence graph completeness and circularity;
- safe challenge and non-retaliation;
- evidence-debt severity and closure;
- remediation outcome criteria;
- privacy and data consent;
- downstream rights and prior grants;
- accessibility and translation;
- anti-self-verification controls;
- security of ledger anchors and access; and
- legal ambiguity and license compatibility.

The reviewer must be allowed to mark the standard `DISPUTED`, `PARTIAL`, or `HOLD`. A review that is commissioned by the author is not automatically independent; the relationship and scope must be disclosed. The present draft has not passed this gate.

## 20. Final rule

A claim must not grow stronger when its evidence is missing. A process must not call itself independent because it uses another name. A remedy must not call itself complete because a task was closed. A release must not infer authority from a passing test. A person must not lose dignity because a record says they failed.

**Measure the claim. Preserve the counter-evidence. Name the debt. Protect the challenger. Verify the consequence. Keep the history.**
