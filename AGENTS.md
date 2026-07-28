# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository. It has a twin, `CLAUDE.md`, read by Claude Code — the two are near-identical (only the tool name and self-references differ). Mirror any edit into both, and don't assume single-author continuity: `GAPS.md` documents this project already having real concurrent-agent incidents (section E), so check `git status` in `Ops\space-control` before and after non-trivial changes here.

## What this directory is

`D:\AI` is the D-drive storage and operations root for **Smisel**, a local AI stack (Open WebUI + Ollama + Qdrant + 14 Docker containers). The stack's two code/data folders were migrated here from `C:\Users\Luka\Documents` on 2026-07-06, with NTFS junctions left at the old C paths. `D:\AI` root became a git repo on 2026-07-28, scoped to root docs only via an allowlist `.gitignore` (`*` then explicit `!CLAUDE.md`/`!AGENTS.md`/`!.gitignore`) — it does **not** track Corpus, Backups, Models, Compose, Projects, or any other subdirectory; those remain outside git here. `Ops\space-control` is a separate, independent repo with its own full history. (Inert, empty `.agents\`, `.codex\`, and `src\api\` folders also exist at `D:\AI` root — leftover artifacts with no content. Don't mistake them for tool config.)

| Directory | Contents |
|---|---|
| `Ops\space-control\` | **The only code here.** PowerShell tooling (own git repo) for storage inventory, backups, and the C→D junction cutover. Policies and runbook in `docs\`. |
| `Compose\SET Up\` | The Smisel stack itself (DockerCompose.yml, pipelines, functions, n8n workflows). Junction target of `C:\Users\Luka\Documents\SET Up`. **Has its own detailed `CLAUDE.md` — no `AGENTS.md` twin exists there yet, so read the `CLAUDE.md` before touching the stack regardless of tool.** |
| `Compose\openwebui\` | **Blueprint only — never deployed.** Clean-room OpenWebUI+Ollama compose definition from space-control Shift 3. NOT the live stack (that runs as `smisel-open-webui` on port 3000 with native Windows Ollama on 11434). Do not `docker compose up` it — its containerized Ollama would conflict with native Ollama on port 11434. See its `README.md` for the `down -v` data-destruction warning. |
| `Projects\` | `WorkShade` — the stack's data workspace, junction target of `C:\Users\Luka\Documents\WorkShade`. |
| `Backups\smisel_live\` | Timestamped hot/cold backups with `MANIFEST.json`. Never delete or modify; created by `backup_smisel_live_hot.ps1`. |
| `Corpus\` | Markdown knowledge corpus (Slovenian), organized as `_modules\Jezik`, `_modules\Tematika\T##_*` topic clusters and `tag_*` views. |
| `Models\ollama\` | Ollama model storage. |
| `Demo\` | Scratch/experimental — not part of the live stack (e.g. `method-brain`, a standalone HTML/JS graph demo). |
| `Temp\` | Scratch: `junction_probe` from feasibility tests, plus cutover handle-diagnostic scripts (`find_handle_holders.ps1`, `workshade_handle_guard.ps1`). |
| `Manifests\` | Evidentiary manifests for C-drive corpus intake: physical inventory, provenance, hash-identity, and planned copy/delete operations. Current intake status/open questions: `GAPS.md`. |
| `Imports\` | Bounded staging area for hash-verified copies of intake material, held pending a decision on further processing. Not disposable scratch. |
| `Delci\` | New as of 2026-07-19. Contains `Work_Lineage_R0_Handoff.zip`, a cross-session handoff package. Its embedded README requested a line-by-line review against live WorkShade files; that review was completed the same day (`Projects\WorkShade\docs\audits\work_lineage_r0_review_20260719.md`) and is not treated as a re-open trigger. The one open question the review surfaced — gate-at-creation vs gate-at-seal-only for the draft's §4.2 domain-extension transition — was decided the same day: gate-at-seal-only confirmed, gate-at-creation rejected (`Projects\WorkShade\docs\audits\work_lineage_r0_decision_20260719.md`). See `GAPS.md` §H. |

**Corpus and Backups contain 50k+ files, heavily duplicated across views** — never glob or grep `D:\AI` root-wide; always scope searches to a specific subdirectory.

Open gaps and pending decisions are tracked in `GAPS.md`; treat its contents, not any summary here, as the project-wide tracking source. `Projects\WorkShade\CURRENT.md` is a scoped live snapshot for Smisel Delo V1 only. Verify the relevant record and current live state before acting.

## Junction cutover: COMPLETE (2026-07-06)

Both Documents folders now live on D with junctions left at the old paths. **The C paths are declared aliases, not a second home** — the stack's compose file and container mounts still bind to them (11 bind mounts), which is a known organizing risk (silent aliasing; junction loss would fail every C-consumer and could fork the tree). Policy of record, C-consumer inventory, and the proposed repoint transit: `Ops\space-control\docs\path_aliasing_policy.md`. D paths are canonical for all new code and docs.

- `C:\Users\Luka\Documents\SET Up` → `D:\AI\Compose\SET Up` (junction, verified).
- `C:\Users\Luka\Documents\WorkShade` → `D:\AI\Projects\WorkShade` (junction, verified 2026-07-06 17:40 via `finish_cutover_detached.ps1`; all junction checks in `reports\cutover_verify_post_2026-07-06T17-40-51.json` passed).

Post-cutover rules:

- The rollback folders (`*.pre_cutover_20260706`) were retired on 2026-07-06 with explicit user approval, after verifying the D copies were file-for-file complete (35,460 + 250 files, unmerged `worktree-smisel-chronicle` branch present on D). No rollback path remains on C — recovery now relies on `D:\AI\Backups\smisel_live`.
- The cutover plan lives in one place: `Get-CutoverPlan` in `Ops\space-control\scripts\cutover_common.ps1`. Preflight/execute detect already-completed moves (`Test-MoveAlreadyCutOver`) and skip them, so re-runs are idempotent.
- Gotcha that shaped the tooling: renaming a Documents folder fails with "in use" while any VS Code window holds handles under it — including a Codex session keyed to that folder, and including git-worktree watcher handles on `.git`. That is why `finish_cutover_detached.ps1` runs via Task Scheduler, detached from VS Code.
- The detached-finisher task `Smisel Cutover At Logon` was unregistered on 2026-07-06 after completion. `Smisel Nightly Loop` is a retained stack task, not cutover residue. Its last documented state is disabled under the gate recorded in `GAPS.md` §A; before making any runtime claim, verify the Windows task and all parallel trigger paths. Do not enable, unregister, replace, or otherwise alter it without a fresh explicit decision.

## Working in Ops\space-control

`Ops\space-control\AGENTS.md` (twin: `CLAUDE.md`) has the full picture — script commands, the shared `param()`/function/`$MyInvocation` guard shape every script follows, the `cutover_common.ps1` plan/helpers, the preflight → execute → verify → rollback pipeline and its two live-incident gotchas (`GetNewClosure()`, `-ErrorAction Stop` on `Rename-Item`), and the Pester dot-sourcing test strategy (including that only Pester 3.4.0/legacy `Should Be` syntax is installed here). Read it before editing anything under `scripts\` or `tests\`.

The one-line version: dry-run by default everywhere; mutation requires `-Execute` plus a dated `CUTOVER-APPROVED-<yyyyMMdd>` token; no delete verbs exist in the cutover scripts.

## Working on the Smisel stack

All stack development guidance (pipelines, valves, Qdrant collections, slash commands, the graph.json invariants) is in `Compose\SET Up\CLAUDE.md` — there is no `AGENTS.md` twin in that directory, so read the `CLAUDE.md` there regardless of which tool you are. Two root-level things to know:

- As of 2026-07-07 the stack binds directly to D paths (compose bind mounts, host scripts, task definitions, docs all repointed). The C junctions remain only as a safety net for stragglers — do not create new C-path references.
- `WorkShade\library\references\` holds 30k+ flat files; the same "scope your searches" rule applies there.
