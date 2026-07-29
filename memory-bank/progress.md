# Progress

Snapshot written 2026-07-29 from `GAPS.md` and `Projects\WorkShade\CURRENT.md`. **Re-derive from those two files for anything time-sensitive** — this is a summary at a point in time, not a live feed, and this project's own history (`GAPS.md` §D, on `path_aliasing_policy.md`) is an explicit cautionary tale about a status doc drifting from reality.

## Working / closed

- C→D storage cutover: complete (2026-07-06). Junctions at old C paths are a safety net, not a second home — D is canonical.
- Register-separation gates (PATCH 5b): auto_curator auto-approve, dialectic/variator/synthesis direct writes, and monthly identity-update merges are all now gated behind explicit human approval.
- Graph-authority gating (CUT 1R–4R, 2026-07-27): `/graph-extract` and `/probe` no longer write `graph.json` directly; edge candidates → promotion → revoke, RAG/`/api/node` now default to approved-tier only.
- Nightly Loop / Watchdog: re-enabled 2026-07-29 (the CUT 1R–4R gating is what made this safe — the "produce while I sleep" concern was about ungated writes, not the schedule itself). Watchdog is stack-health-recovery only; nightly content generation has exactly one trigger owner now, after an orphan n8n workflow was found running the same job in parallel for weeks undetected.
- Docker ports restricted to `127.0.0.1` (2026-07-29).
- Word Work / lexeme write path: found completely broken in production (read-only mount bug), fixed via proxy pattern, proven live (2026-07-29). A sibling route (`/api/word-sheet/.../decide`) likely has the same bug, not yet fixed.
- Smisel Explorer (Coders Lab final project, separate repo) built and shipped 2026-07-26; read-only consumer of 4 documented Canvas endpoints.
- `Compose\SET Up` and `D:\AI` root both git-tracked now (2026-07-26 and 2026-07-28 respectively); `Ops\space-control` always was. `Projects\WorkShade` — check current state, historically had long uncommitted stretches.

## Open / in progress

- **Delo V1** (current focus, owner Codex/Claude Code): draft+decision artifact lifecycle proven live 2026-07-29 with full metadata (`artifact_id`, `source_refs`, etc.). **Not yet proven**: the "propose to Work Session" step (candidate + receipt) — no propose action found in the current `/delo` UI; may live in Canvas's DECIDE panel instead. This is the next concrete thing to verify, not to build from scratch.
- Morning Witness task: still deliberately `Disabled` (only Watchdog + Nightly Loop were approved to re-enable 2026-07-29).
- C-drive corpus intake: physical inventory done (~49GB catalogued), only a small hash-verified subset actually staged to D; the larger 16.6GB "COPY" bucket is untouched. One approved slice (23 conversation JSON files) deleted from C 2026-07-29.
- `Library.pre_move_20260706` ACL residue: 15 empty protected temp dirs, delete not yet attempted (needs admin context).
- `chronicle_merge_attempt` worktree: a complete, tested feature (daily narrative generator + Canvas ORACLE panel), 9/11 files resolved, not committed — safe to resume or discard.
- `Delci\Work_Lineage_R0_Handoff.zip`: reviewed and its one open question decided (2026-07-19); no longer a live gap, kept as history.
- `smisel-canvas` container recreating unexpectedly (`RestartCount` resets) — recurring, boot-correlated, root cause still unidentified.
- Junk graph nodes (`TestNode`, `OtherNode`, `Mocassin`, `Luka`, `Lukov`): removal decision locked, execution on HOLD pending a reference scan.

## Full ledger

`D:\AI\GAPS.md` — the actual append-only record, sections A through L as of this writing. Read it directly for anything not summarized above.
