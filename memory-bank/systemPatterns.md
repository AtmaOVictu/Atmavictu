# System Patterns

## The register-separation law (constitutional, locked 2026-07-07)

Named registers, not flat terms: raw archive ≠ operative corpus ≠ candidate queue ≠ approved corpus ≠ canon ≠ indexed/retrievable memory ≠ runtime function. Existence ≠ authority; generation ≠ decision; retrieval ≠ truth; indexing ≠ canon.

**Placement, not prohibition**: the same shortcuts (silent promotion, hidden authority, collapsing registers) that are corruption at an authority crossing (candidate→approved, approved→canon) are perfectly fine inside a low-authority, reversible, or symbolic layer. The question before acting is always "what layer is this write in," not "is this kind of shortcut allowed in general."

Every object carries two identities: **what it is** (status + provenance) and **where it may act** (use-rights) — kept in one policy table keyed by status, not scattered per-object.

## The gate pattern this produced

Every writer that touches approved/canon state now goes through an explicit gate rather than writing directly:

- `gate_closure.py` — generic request/list/apply/reject engine; dialectic/variator/synthesis pipes generate but require a verified `human_action_id` to actually write `library/definitions/`, `library/synthesis/`, Qdrant, or `graph.json`.
- `edge_candidate_writer.py` / `promote_edge_candidate.py` / `revoke_edge.py` — graph edges land in `library/edge_candidates/` first; promotion is a separate, auditable step with an `authority_ref`; revoke is the undo half (added 2026-07-27, CUT 3R — the pattern didn't have an undo before that).
- `auto_curator.py`'s old `auto_approve_threshold` (silent commit at ≥8 mentions) — closed 2026-07-08, default now 0; everything routes through `pending/` + `/approve`.
- `apply_context_merge.py` — `CONTEXT_INBOX.md` → `CONTEXT.md` (the AI's own system prompt) requires a verified `approve_context_merge` action; used to merge unattended.

**Lesson visible across every one of these** (`GAPS.md` §B/§E/§K): the bug is never "the LLM said something wrong" — it's an unattended writer with a direct path to canon. When adding anything new that writes `library/definitions/`, `graph.json`, or `CONTEXT.md`, assume it needs a gate unless it's explicitly a candidate/draft path.

## Mutation posture, generally

Dry-run by default, explicit opt-in for real writes, e.g.:
- `Ops\space-control` cutover scripts: `-Execute` + a dated `CUTOVER-APPROVED-<yyyyMMdd>` token, exact match required. No delete verb exists in that repo's scripts at all.
- Delo saves are always `canonical_status: non_canon` drafts; "propose to Work Session" is a separate, still-unverified-live step (see `Projects\WorkShade\CURRENT.md`).

## Twin-doc convention

`CLAUDE.md` (Claude Code) and `AGENTS.md` (Codex) are near-identical twins wherever they coexist (root; not yet in `Compose\SET Up\` or `Ops\space-control`, which only have one). Edit both together. This repo now also carries `.clinerules\` for Cline — treat it as a third sibling in spirit (same orientation, adapted register), not a fork with its own separate truth.

## Atomic writes / graph-specific invariants

`graph.json` must never be written with plain `open(..., "w")` — use the atomic-write helpers (`_save_graph()`, `_graph_atomic_write()`), which also snapshot history. Never edit `graph.json` from PowerShell — `ConvertFrom-Json` silently returns `$null` on the case-duplicate keys the file already has; use Python. Full node/edge invariants: `Compose\SET Up\CLAUDE.md` → "Canonical Framework (Onto-System)".

## Concurrency is real, not hypothetical

Documented incidents, not a theoretical warning: `.git` renamed and restored mid-session by another process (§E), a definition's `status` reverted minutes after being demoted by this session (§E), an orphan n8n trigger running the same nightly pipeline in parallel with the "disabled" host task for weeks undetected (§A, `INC_2026_07_09_ORPHAN_TRIGGER_NIGHTLY_CANON_LOOP`), 137+ uncommitted WorkShade paths accumulated across sessions (§F). Check `git status` before and after non-trivial work; don't assume a dirty tree is yours.
