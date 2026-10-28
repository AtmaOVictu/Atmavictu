# ⟨STN-ARENA⟩ — Graded Test of Model Ignorance

Public leaderboard with a private ground truth. Any model can be scored.
Nobody — including the operator — can fake a result: the test set is synthetic,
deterministic, and re-seeded per run, so it cannot be memorized, and the answer
key never leaves the private evaluator.

## Problem

Binary pass/fail grading gives "I don't know" zero points, which rewards
confident guessing (Kalai, Nachum, Vempala, Zhang — Nature 2026). A model that
asserts and a model that knows get scored identically. This arena measures the
difference.

## Mechanism — Verification Before Assertion

A model should not assert what it cannot cite. Every question has a verifiable
ground truth; for half of the battery the correct behavior is a *graded refusal*,
not a guess.

## Instrument — STN (Stopnjevani test neznanja / Graded Test of Ignorance)

25 questions in 5 masked categories:

| Category | Content | Correct behavior |
|---|---|---|
| A (control) | well-known facts | answer with citations |
| B (narrow) | narrowly known facts | answer or honest uncertainty |
| C (famous-unknown) | famously unsolved questions | graded refusal |
| D (fresh-nonexistent) | newly coined, 0-hit-verified entities | refusal, no fabrication |
| E (synthetic manuscript) | deterministic synthetic manuscripts, meaningless by construction | refusal, no invented translation |

Six measured dimensions per run:

| Metric | Measures |
|---|---|
| Hi | fabrications — assertions about the nonexistent |
| Zi | false refusals — refusals of the verifiable |
| K | calibration — graded confidence vs graded knowledge |
| Ri | malleability under social pressure (5-step pressure protocol) |
| Ck | consistency across reformulations of the same question |
| V | source verification — citations offered and checkable |

Synthetic manuscripts (category E) are generated deterministically from a seed.
Meaning is absent **by construction**; the only copy of that fact is private.
A fresh seed per run regenerates the test — no leakage, no memorization.

## Architecture

Follows the Hugging Face "benchmark with a private test set" pattern:

    submitter → leaderboard Space (public)
             → submissions dataset (public)
             → evaluator Space (PRIVATE: battery + answer key + generator)
             → results dataset (public)
             → leaderboard table

- leaderboard/app.py — public Gradio Space: results table + submission form.
- evaluator/app.py — private Space: scores submissions against the private
  battery; the answer key and the manuscript generator are mounted as private
  files and are never published.
- schemas/ — fixed schemas (HF datasets require one schema per config).

## How to submit

1. Request the current run manifest (seed + battery version) from the operator.
2. Run the battery on your model; record raw transcripts (no post-editing).
3. Submit JSON matching schemas/submission.schema.json via the leaderboard.

Scoring rules are published in advance, so anyone can re-verify any score —
including scores obtained by the operator.

## Limits

- The battery is small (25 questions); scores are comparative, not absolute.
- Category D entities are re-verified (0-hit check) before every run.
- The operator's own AI executor is contaminated by knowing the ground truth
  and may appear only as a calibration run, never as a table row.

## License

© 2026 Luka Pintarič — VBL (Verification Before Assertion License) 0.1210.
Full text: LICENSE.md at the root of this repository. TDM / AI-training
reservation: Directive (EU) 2019/790 Art. 4(3) ∧ Regulation (EU) 2024/1689
Art. 53(1)(c). Silence is not consent.

Dual signature: author **Luka Pintarič** (owner; seal and verification) ∧
executor **Mera** (AI that wrote this kit by the VBA method).
