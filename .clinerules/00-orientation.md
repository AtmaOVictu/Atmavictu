# Orientation — Smisel / D:\AI

Cline is a third agent working in a workspace already shared by Claude Code and Codex. Read this before touching anything.

## Read these first, in order

1. `D:\AI\CLAUDE.md` — root directory map and policy. Authoritative. (Its twin `AGENTS.md` is near-identical; don't treat divergence between them as intentional — it means one was edited without the other.)
2. `D:\AI\memory-bank\` — `activeContext.md` / `progress.md` for "what's happening right now"; the rest for durable orientation. Populated 2026-07-29 from a real read of the docs below, not invented — but it's a snapshot, not a feed. Treat any date on it as possibly stale; re-check the cited source file before acting on it.
3. `D:\AI\GAPS.md` — the actual open-items ledger. Append-only, multi-agent, still being maintained live. This is the source of truth for "what's open," not `memory-bank/progress.md`.
4. Whichever subdirectory `CLAUDE.md` governs the code you're about to touch (`Compose\SET Up\CLAUDE.md` for the stack, `Ops\space-control\CLAUDE.md` for the PowerShell tooling, `Projects\WorkShade\CURRENT.md` for the live Delo V1 slice) — root `CLAUDE.md` is an index, not a replacement for these.

## Standing rules for this repo specifically

- **You are not the only agent here.** `GAPS.md` documents real concurrent-agent incidents — `.git` renamed and restored mid-session by another process, a file's `status` reverted minutes after being demoted, 137+ uncommitted paths in WorkShade that predate any one session. Run `git status` before and after non-trivial changes, in whichever repo you're in (`D:\AI` root, `Ops\space-control`, or `Projects\WorkShade` if it's a repo at the time you read this — check, don't assume). Don't assume a messy working tree is your mess to clean up.
- **Never flatten a register.** This project's constitutional rule (Luka, 2026-07-07): raw archive ≠ operative corpus ≠ candidate queue ≠ approved corpus ≠ canon ≠ indexed/retrievable memory ≠ runtime function. Concretely: don't write directly to `library/definitions/`, `library/graph.json`, or anything at `status: approved`/canon as if it were a scratch file — those paths have an existing candidate → human-approval → promotion pipeline (`gate_closure.py`, `promote_edge_candidate.py`, `human_action_id`), and bypassing it to "just fix" something recreates a bug class already found and closed multiple times (`GAPS.md` §B, §E, §K: ungated auto-curator commits, ungated graph writes, ungated dialectic/variator/synthesis writes — all since gated). If a task looks like it wants to touch one of these, stop and check whether a gate already exists before writing directly.
- **Placement, not prohibition.** The same law says silent shortcuts are fine in low-authority/reversible/symbolic layers (drafts, scratch, your own working notes) and only corrupt at authority crossings. Don't over-apply caution to genuinely reversible work — check which layer you're in before deciding how careful to be.
- **Mutation is opt-in and dry-run by default**, wherever you look: `Ops\space-control`'s cutover scripts require `-Execute` plus a dated approval token; `gate_closure.py` requires a verified `human_action_id`; Delo's save path always writes non-canon drafts. Match that posture — default to read-only/dry-run, require an explicit instruction for anything that mutates canon, deletes files, or restarts containers.
- **The twin-doc convention**: `CLAUDE.md` and `AGENTS.md` at root must be edited together — mirror any edit into both, in the same change. This repo now also carries `.clinerules/` for Cline; treat it as a third sibling in spirit (same orientation, adapted register), not a fork with its own separate truth.
- **Never glob/grep `D:\AI` root-wide.** `Corpus\`, `Backups\`, `Models\`, `WorkShade\library\references\` hold 50k+ heavily-duplicated files. Always scope searches to a specific subdirectory.

## What Cline specifically is for here

No fixed brief yet beyond "orient, and be useful going through the data." Until Luka gives a narrower mandate, default to read-only exploration and drafting (Delo-style: draft → explicit save/discard, nothing auto-promoted) rather than direct edits to `WorkShade/library/`, `graph.json`, or any Docker/Task-Scheduler state.
