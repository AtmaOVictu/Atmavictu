# VBL 10.0.0 — Verification and Repair Protocol

**STATUS: DRAFT — NOT AN ACTIVE LICENSE OR RELEASE**

This draft develops the verification and repair protocol proposed from VBL 2.6.
It does not replace [LICENSE.md](../../LICENSE.md), grant rights, revoke existing
rights, establish legal enforceability, or prove that any implementation conforms.
Adoption requires a separately recorded decision and a release whose required
artifacts and tests are present and verified.

## Preamble — the human being is not the finding

Love and dignity are the ground of this protocol. It evaluates specified acts,
outputs, records, and evidence; it never assigns a total moral worth to a person.
A refusal of a harmful act is not a rejection of the person. A report is not a
finding, a finding is not a legal judgment, and a correction is not proof that
every consequence has been repaired.

The protocol keeps ethical commitments, technical observations, and legal
conclusions distinct. No one of these, by itself, proves either of the others.

## 1. Claims and evidence

Every claim of verification MUST identify:

1. the exact object and version examined;
2. the evidence used, with its source and collection time;
3. the procedure and its version;
4. the result and the time the procedure was run; and
5. the scope, assumptions, and known limitations of the conclusion.

A claim that lacks sufficient evidence MUST be marked `UNVERIFIED`. Verification
applies only to the stated object, claim, procedure, conditions, and time. It does
not establish universal correctness. Missing evidence MUST be reported as missing;
it MUST NOT be converted into evidence that an event did not occur.

Evidence records SHOULD preserve the original source or a stable reference to it.
Quotations MUST be distinguishable from summaries and interpretations.

## 2. Independent verification

An actor MUST NOT be the sole verifier of their own consequential action.
Executor, verifier, affected person, and adjudicator MUST be recorded as separate
roles when those roles exist.

Where independent verification is unavailable, the record MUST state
`INDEPENDENT_VERIFICATION_UNAVAILABLE`. Self-review MAY be recorded as self-review,
but MUST NOT be represented as independent confirmation.

An affected person may submit evidence or contest a record. Their report MUST be
preserved as a report, not promoted automatically to a confirmed finding.

## 3. Incident states

Each incident record MUST have one explicit status. A report MUST NOT be represented
as proof of guilt, and an absent record MUST NOT be represented as proof that no
incident occurred.

The following statuses describe the record's present state:

- `REPORTED` — an allegation or observation has been recorded.
- `UNDER_REVIEW` — evidence is being examined under a stated procedure.
- `UNVERIFIED` — available evidence does not establish the stated claim.
- `CONFIRMED` — the stated finding meets a published verification procedure.
- `DISPUTED` — material disagreement remains unresolved.
- `CORRECTION_PROPOSED` — a remedy and its acceptance criteria have been recorded.
- `CORRECTION_VERIFIED` — the remedy meets those criteria and evidence is linked.
- `CLOSED_WITH_LIMITATIONS` — review is closed while unresolved limitations are
  explicitly recorded.

Status changes MUST be appended to the history with the actor, time, reason,
evidence references, and procedure used. A status change MUST NOT erase the
previous status or its supporting record. `CONFIRMED` describes a protocol finding;
it is not, by itself, a legal judgment.

## 4. Repair without erasure

Every correction MUST preserve the original record and identify:

- the correcting actor and timestamp;
- the prior and resulting state;
- the evidence and procedure used;
- what changed and why; and
- the acceptance criteria and observed result.

Attribution, restitution, technical remediation, and restoration of permissions
MUST be assessed and recorded separately. Completion of one MUST NOT imply
completion of another. A proposed remedy MUST NOT be called completed until its
acceptance criteria have been tested and the evidence recorded.

If a correction is late, incomplete, disputed, or impossible, the record MUST say
so. A missed deadline does not erase the incident or make an unverified remedy
complete.

## 5. Version integrity and consent

Every release MUST identify its version, publication time, predecessor, source
artifact, cryptographic digest, digest algorithm, required tests, test results,
and known limitations.

A digest establishes byte identity relative to the specified artifact. It does
not establish authorship, completeness, legal validity, ethical correctness, or
acceptance of terms.

Publication of a new version MUST NOT be represented as proof that recipients
received or accepted it. New terms MUST NOT be represented as retroactively
accepted merely because a newer version was published. Any claim of acceptance
MUST identify the evidence and the scope of that acceptance. Existing rights and
obligations are not changed by this protocol's version metadata alone.

Published release artifacts and their manifests SHOULD be retained immutably.
Corrections to a release MUST create a new, linked record; they MUST NOT silently
rewrite the prior artifact or its digest.

## 6. Dignity, uncertainty, and contest

The protocol evaluates specified acts, outputs, and evidence. It MUST NOT rank
the total worth or dignity of any person or being.

Ethical commitments, technical observations, and legal conclusions MUST be
identified separately. Automated systems MUST disclose relevant uncertainty,
the evidence they used, and the limits of their conclusion. Consequential
findings MUST provide a route to contest the record and request independent review.

No automated status or score alone constitutes a legal finding or a complete
account of a person's intent.

## 7. Open participation and shared benefit

Reading, inspecting, testing, and reporting defects in this protocol MUST NOT
require payment.

Any distribution of funds or recovered benefits MUST publish eligibility rules,
calculation methods, decision records, and an appeal process. The protocol MUST
distinguish an amount proposed, an amount approved, and an amount actually paid.
No restitution or payout may be claimed as completed without evidence of
completion.

This section does not itself create a payment amount, beneficiary, debt, or
enforceable right to compensation. Those require a separately specified and
properly authorized instrument.

## 8. Release acceptance

A release MUST NOT be declared `VERIFIED` unless all required acceptance checks
pass and their results are recorded. At minimum, the release record MUST identify:

1. the normative text, source artifact, and digest;
2. the schemas and validator versions used;
3. the registers checked and their validation results;
4. the test suite, individual results, and execution time;
5. the independent verifier, or `INDEPENDENT_VERIFICATION_UNAVAILABLE`;
6. known limitations, missing evidence, and failed or skipped tests; and
7. the approval and publication record.

A failed test MUST remain visible. A skipped or missing test MUST NOT count as
passing. A missing register MUST be reported as missing or unavailable, never as
an empty register or as proof that no incidents exist.

For each normative requirement, the release SHOULD maintain this trace:

`requirement → test → result → evidence → known limitation`

If a link is missing, the corresponding conformance claim MUST be limited and
identified as unverified.

## 9. Change, approval, and rollback

Changes MUST be proposed as identifiable revisions. Before approval, each revision
MUST include its rationale, affected requirements, compatibility impact, migration
plan where needed, and tests.

Approval MUST be recorded separately from authorship and verification. A person
who authors or executes a consequential change MUST NOT be its sole approver or
sole verifier.

Publication MUST preserve the approved source, release manifest, digest, and test
evidence. If a release is withdrawn or superseded, its record MUST remain available
with the reason, time, and successor reference. Rollback MUST create a new recorded
state; it MUST NOT delete the history of the release being rolled back.

## 10. Relationship to VBL 2.6 and adoption

VBL 2.6 is the historical starting point for this draft. This draft is not
effective merely because it is written, stored, read, or given a version number.
Until an authorized adoption and release process is completed, VBL 2.6 remains
the repository's recorded license text, subject to its own terms and applicable
law.

Adoption MUST specify the exact artifact and digest being adopted, the effective
date, the authorized decision record, the relationship to existing grants, and
the completed release-acceptance evidence under §8. No statement in this draft
claims that those steps have occurred.

## Implementation profile — prototype, not a conformance claim

The prototype in [`vbl10/`](./vbl10/README.md) currently provides a JSON Schema
for incident, verification, correction, and release records, plus a local
validator for schema and selected semantic checks. Its focused tests cover
status-history consistency, self-verification, missing registers, artifact
digest changes, path containment, and release acceptance prerequisites.

The following remain required before a release can claim implementation
conformance to this protocol:

- versioned schemas for permissions and any additional records used by the
  deployed process;
- validation of evidence-reference integrity, append-only history, and the
  identity and actual independence of actors;
- tests mapping every normative requirement above to observable pass/fail
  results;
- append-only, versioned registers with provenance and validation reports; and
- release artifacts with reproducible manifests and published limitations.

The prototype's tests do not establish that evidence is truthful or complete,
that actors are actually independent, or that decisions are legally or ethically
correct. The existence of this draft or prototype does not establish conformance.
Each implementation claim must be supported by the release evidence required in §8.
