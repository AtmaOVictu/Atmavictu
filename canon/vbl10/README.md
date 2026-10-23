# VBL 10.0.0 draft prototype

This folder contains an experimental validator for the non-active draft in
`../VBL-10.0.0-DRAFT.md`. It validates incident, verification, correction, and
release records against `schemas/records.schema.json` and applies additional
cross-record checks in `validate.py`.

It is not a production ledger, legal decision engine, immutable storage system,
signature verifier, permission registry, or proof of VBL conformance. The current
validator checks local record files and SHA-256 artifact identity only. It does
not prove who authored an artifact, whether evidence is truthful or complete,
whether actors are genuinely independent, or whether any legal or ethical
conclusion is correct.

## Requirements

Python 3.10+ and the `jsonschema` package are required. In this repository,
`jsonschema` is listed in the development requirements.

## Use

Validate one JSON record:

```powershell
python canon/vbl10/validate.py path\to\record.json
```

Validate a JSON Lines register:

```powershell
python canon/vbl10/validate.py path\to\register.jsonl
```

Paths referenced by a release record are resolved relative to the release
manifest and must remain inside that directory. A missing register is reported
as missing, not treated as an empty register.

Run the focused tests from the repository root:

```powershell
python -m unittest discover -s canon/vbl10/tests -v
```

The prototype intentionally does not emit a release-level `VERIFIED` result
unless artifact digest, register files, test results, and independent review
meet the implemented checks. A successful record validation is only a statement
that the available structural and implemented semantic checks passed.
