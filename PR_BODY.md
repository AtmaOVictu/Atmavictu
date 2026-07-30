Title: feat: ingest Delo proposals; tests, README, CI

Summary:
- Adds `ingest_delo_proposals.py` — idempotent ingestion of Delo proposal JSONs into the review queue or appends decision blocks to `reviews/luka_decisions.md`.
- Adds unit tests for idempotence: `Projects/WorkShade/scripts/tests/test_ingest_delo_proposals.py`.
- Adds `Projects/WorkShade/scripts/README_ingest_delo_proposals.md` with usage instructions.
- Adds CI workflow `.github/workflows/ci.yml` (Python matrix) and `requirements-dev.txt` / `pyproject.toml` for dev deps.
- Integrates proposals into `generate_review_queue.py`.

Details / Rationale:
- Bridge between the Delo canvas `api_delo_propose` persistence and Luka's human review ingestion pipeline.
- Keeps proposals immutable; ingestion only surfaces proposals for human review, no automatic canon mutation.

Files changed (high level):
- `Projects/WorkShade/scripts/ingest_delo_proposals.py`
- `Projects/WorkShade/scripts/tests/test_ingest_delo_proposals.py`
- `Projects/WorkShade/scripts/README_ingest_delo_proposals.md`
- `.github/workflows/ci.yml`
- `requirements-dev.txt`, `pyproject.toml`
- `Projects/WorkShade/scripts/generate_review_queue.py` (call to `scan_delo_proposals()`)

How to test locally:
1. Run `python Projects/WorkShade/scripts/ingest_delo_proposals.py --dry-run` to preview.
2. Run `python Projects/WorkShade/scripts/ingest_delo_proposals.py --to=markdown` to append blocks.
3. Run `pytest -q Projects/WorkShade/scripts/tests/test_ingest_delo_proposals.py`.

Notes:
- The ingestion is idempotent; existing proposals are skipped for the queue target, and duplicate markdown headers are avoided for markdown target.
- CI runs tests using Python matrix and installs `requirements-dev.txt`.

Checklist for PR reviewers:

- [ ] Confirm `ingest_delo_proposals.py` logic matches the project's idempotency and safety constraints.
- [ ] Verify `Projects/WorkShade/scripts/tests/test_ingest_delo_proposals.py` covers idempotence cases adequately.
- [ ] Confirm CI workflow (`.github/workflows/ci.yml`) and `requirements-dev.txt` are acceptable for the repo.
- [ ] Verify `.gitignore` changes preserve the allowlist policy and do not expose large folders.
- [ ] Run the ingestion end-to-end in a staging environment and confirm a proposal appears in `reviews/luka_decisions.md` and/or `logs/review_queue.json` as appropriate.

Meta: If you'd like different reviewers or labels, tell me and I'll apply them to the PR.
