# Implementation test report — VBL 0.1470 candidate

**Run date:** 2026-11-05  
**Environment:** Python standard library plus `jsonschema` 4.26.0 for JSON Schema meta-validation.  
**Scope:** Local package files and synthetic fixtures only. No production deployment, live user data, external identity service, trusted timestamp, or independent reviewer was used.

## Results

| Check | Result | What it establishes |
|---|---|---|
| Unit tests | PASS — 17/17 | The listed validator behaviors passed on synthetic test data. |
| JSON Schema syntax/meta-validation | PASS — 8/8 | All eight schemas are valid Draft 2020-12 schemas according to `jsonschema` 4.26.0. |
| Example ledger | PASS — 2 events | The synthetic JSONL fixture passes the implemented ledger validator. |
| Python compilation | PASS | `validator.py` and the unit-test file compile. |
| CLI smoke test | PASS | The validator help interface runs. |
| Full normative conformance | PARTIAL / NOT VERIFIED | Many requirements require integration, human judgment, external services, user testing, or legal review. |
| Independent review | NOT RUN | The drafter also performed the internal adversarial self-review. |
| Rights-holder release authorization | NOT RUN | No approval for the exact bytes was requested or recorded. |
| Legal review | NOT RUN | No legal conclusion is offered. |
| Accessibility user testing | NOT RUN | Requirements are specified; blind/deaf user testing has not been done. |
| Trusted timestamp/signature/external anchor | NOT RUN | No such infrastructure is configured. |

## Three status dimensions

- `test_result=PASS` — only for the bounded local tests listed above.
- `claim_status=SUPPORTED` — the claim that these 17 unit tests and eight schema checks passed is supported by the captured local output, within this environment and test scope.
- `decision=HOLD` — a passing local suite is not release authorization; independent review, exact-byte rights-holder approval, legal review, accessibility testing, and real-world remedy validation remain outstanding.

## Known limitations of the reference validator

The validator is intentionally a small, dependency-free reference implementation. It does not yet implement full graph storage/query, external anchoring, identity authentication, cryptographic signatures, production access controls, privacy scanning, jurisdiction-specific legal review, accessibility automation, translation quality review, or real-world remedy outcomes. The JSON schemas describe additional record constraints that are not all enforced by the Python reference validator. Do not describe the code as a complete VBL deployment or a certified conformance tool.
