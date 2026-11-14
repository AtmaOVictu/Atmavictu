# Adversarial self-review — VBL 0.1470 candidate

**Reviewer role:** drafting assistant / internal critic.  
**Independence:** NOT INDEPENDENT. The same assistant prepared the standard and performed this review.  
**Decision:** HOLD. This review is not release authorization.

## Findings retained as blockers

1. No exact predecessor artifact is asserted. The identifier `0.1470` is proposed, not proof of lineage.
2. No rights-holder approval for the exact bytes is present.
3. No jurisdiction-specific legal review has been performed.
4. No external independent reviewer has reviewed the standard or implementation.
5. No trusted timestamp, signing key, external ledger anchor, or independently controlled replica is configured.
6. No deployment has been exercised with real users, affected parties, or sensitive data.
7. Accessibility requirements are specified, but no screen-reader, keyboard, caption, transcript, sign-language, or plain-language usability audit has been performed.
8. The reference validator implements only a subset of the standard; it does not yet validate every graph edge, legal authority, privacy property, accessible user journey, or real-world outcome.

## Deliberate adversarial tests

The unit tests include negative cases for:

- tampered event payload;
- reordered events;
- duplicate event identifier;
- supported claim without evidence;
- dangling evidence reference;
- invented status value;
- executor verifying their own remedy;
- release without rights-holder approval;
- release with unresolved blocker debt despite `PASS`;
- limitations release without public limitations;
- accepted risk without an authority, rationale, and review date; and
- the limitation that a complete ledger rewrite can be re-hashed and pass internal-chain validation.

## Important limitation

The last test is intentional. A hash chain is tamper-evident only relative to a previously trusted head or independently retained anchor. It is not an identity proof and does not stop an actor with control over the entire ledger from rewriting and re-hashing it.

## Required next independent review

A person who did not draft this document or write/run its validator should review the full standard, schemas, validator, test results, and the limitations above. They must be able to recommend `HOLD`, `PARTIAL`, or `WITHDRAW` without the author's approval. Their identity, competence, scope, conflicts, evidence, and dissent must be recorded. Until that happens, this remains a candidate, not a release.
