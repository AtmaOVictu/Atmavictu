# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository. It has a twin, `CLAUDE.md`, read by Claude Code — the two are near-identical (only the tool name and self-references differ). Mirror any edit into both, and don't assume single-author continuity: `GAPS.md` documents this project already having real concurrent-agent incidents (section E), so check `git status` in `Ops\space-control` before and after non-trivial changes here.

## What this directory is

`D:\AI` is the D-drive storage and operations root for **Smisel**, a local AI stack (Open WebUI + Ollama + Qdrant + 14 Docker containers). The stack's two code/data folders were migrated here from `C:\Users\Luka\Documents` on 2026-07-06, with NTFS junctions left at the old C paths. `D:\AI` root became a git repo on 2026-07-28, originally scoped to root docs only via an allowlist `.gitignore` (`*` then explicit un-ignores) — it still does **not** track Corpus, Backups, Models, Compose, or Projects; those remain outside git here. `Ops\space-control` is a separate, independent repo with its own full history. (Inert, empty `.agents\`, `.codex\`, and `src\api\` folders also exist at `D:\AI` root — leftover artifacts with no content. Don't mistake them for tool config.)

**The allowlist premise is now stale for one thing: real product code.** Since 2026-07-29 (`cdba504` onward) this same repo also carries **Atmavictu**, a TypeScript product tracked directly at root (`src\`, `docs\`, `schema\`, `package.json`, `tsconfig.json` — see "Working on Atmavictu" below). `.gitignore`'s own comment has since been updated to acknowledge this ("un-ignore only the root docs and the Atmavictu product source meant to be tracked here") — don't assume new files under `src\`/`docs\`/`schema\` are auto-tracked by the current ignore rules regardless, check `git status` explicitly, since the allowlist is per-file, not per-directory-intent. Corpus/Backups/Models/Compose/Projects are unaffected by this and remain outside git as before (verified via `git ls-files` — nothing under `Projects\` is tracked, despite one dead allowlist line for a WorkShade changelog file that was never actually added).

As of 2026-07-29, `.clinerules\` and `memory-bank\` are real, active tool config for a third agent, Cline — behavior rules plus a pre-populated project-orientation Memory Bank (see `.clinerules\memory-bank.md` for how Cline maintains it). Not to be confused with the inert folders above. Treat it as a third sibling of this twin-doc pair in spirit: same orientation, adapted for a tool whose memory resets between sessions. If root policy changes here, consider whether `.clinerules\00-orientation.md` or the Memory Bank need a matching update.

| Directory | Contents |
|---|---|
| `src\`, `docs\`, `schema\`, `package.json`, `tsconfig.json` | **Atmavictu / Book Workbench** — TypeScript product code tracked at repo root. Contract-first manifest system for a `vir -> obdelava -> knjiga` (source → processing → book) workflow. See "Working on Atmavictu" below. |
| `Ops\space-control\` | PowerShell tooling (own git repo) for storage inventory, backups, and the C→D junction cutover. Policies and runbook in `docs\`. |
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

## Working on Atmavictu

Atmavictu is a Book Workbench for a `vir -> obdelava -> knjiga` (source → processing → book) editorial workflow: an `IncomingText` gets cut into working `Fragment`s, and a confirmed `Fragment` becomes an `Insertion` at a `targetChapterPath` in the active book. The point of the product is a **persistent local manifest** — `book.workbench.json` in the target project root — that makes the `IncomingText -> Fragment -> Insertion -> targetChapterPath` trail explicit and machine-checkable instead of implicit in some future UI. Full narrative in `README.md`; the binding contracts are `docs\ARCHITECTURE.md` (three-space model: Knjiznica/library, Aktivna knjiga/active book, Vhodni tekst/incoming text — plus the Model → Service → UI → Tauri/backend layering rule, where UI is never the source of truth for relations), `docs\MODEL_CONTRACT.md` (entities, statuses, allowed/forbidden transitions, invariants), and `docs\SERVICE_CONTRACT.md` (the operation-by-operation contract: inputs, entity effects, allowed transitions, failure cases, acceptance checks). Contract-first is the explicit house rule here: lock schema/model/service behavior before UI or runtime.

**Commands** (from `package.json`, Node ESM + TypeScript, strict mode):

- `npm run typecheck` — `tsc --noEmit`
- `npm test` — compiles (`tsc`), then runs `node --test "build/src/*.test.js"` (Node's built-in test runner against compiled output, not Jest/Mocha; there's a `*.test.ts` next to every source file)
- `npm run atma -- <capture|show|verify> <projectRoot> [title] [body]` — the `atmaCli.ts` CLI (needs a build first, or use the built form: `node build/src/atmaCli.js ...`)
- `npm run proof:capture` — runs `captureIncomingTextProof.ts` directly, a thin proof-of-flow wrapper around `capture`

**Source layout** (`src\`):

- `workbenchManifest.ts` — the pure domain model: entity shapes, `validateManifest()` (single-snapshot schema/relation/invariant check) and `validateManifestTransition()` (checks a status transition between two snapshots is allowed and leaves a valid result)
- `workbenchManifestRepository.ts` — the only persistence layer: reads/writes `book.workbench.json` atomically (temp file + rename), guards `sourcePath`/`targetChapterPath` against escaping `projectRoot` (rejects absolute paths and `..` traversal), and is the sole layer allowed to mutate the manifest per the service contract
- `captureIncomingTextProof.ts`, `atmaCli.ts` — thin CLI wrappers over the repository layer; no domain logic of their own
- `schema\workbench.manifest.v1.schema.json` — the JSON Schema `book.workbench.json` must validate against (`manifestVersion` is a literal `"1"`; paths are constrained via a shared `PathString` pattern)
- `workbenchManifestSchema.test.ts` is the one test file with no same-named source sibling — it loads the JSON Schema directly and asserts on its `$defs` (e.g. that `PathString`/`NonBlankString` are actually reused, not duplicated), rather than testing a `.ts` module.
- `workbenchApiServer.ts` (Faza 2, added 2026-08-04) — a thin Express API wrapping the model/repository layer for one `projectRoot`; no domain logic of its own. Run with `npm run serve -- <projectRoot> [port]` (default port 4173). Tests in `workbenchApiServer.test.ts` hit it over real loopback HTTP (ephemeral port, no mocking) against a temp `projectRoot`, exercising all 9 service operations end-to-end.

**Faza 2 UI workbench (in progress, 2026-08-04):** design doc is `docs\superpowers\specs\2026-08-04-atmavictu-faza2-workbench-ui-design.md` — read it before touching `web\` or `workbenchApiServer.ts`. The acceptance bar for this phase is explicit: all 9 service operations reachable from the UI at least once (the CLI only ever reached 3). Verified live in a real browser via Playwright, not just via tests — capture → start-processing → create-fragment → insert → archive-fragment → archive-incoming, with `VERIFY: PASS` holding throughout and the insertion trail surviving both archives.

- `web\` is a **separate** npm project (own `package.json`/`tsconfig.json`, React + Vite + TypeScript strict) so the root `npm test`/`npm run typecheck` stay scoped to the CLI/service layer. Run it with `cd web && npm install && npm run dev` (port 5173, Vite proxies `/api` to the API server on 4173 — both must be running).
- Known, disclosed gaps, not oversights: no visual design pass; Knjiznica pane has no contract-doc precedent for what folder it browses (defaults to `projectRoot` itself — first place to revisit if this turns out wrong); Aktivna knjiga's tree view only annotates *existing files* with insertion counts, so a `targetChapterPath` that was never materialized as a real file (the common case — `insertFragmentIntoChapter` never writes one) simply doesn't appear there; no drag-and-drop.
- `.github\workflows\atmavictu-ci.yml`'s path filter (`src/**`, `schema/**`, `package.json`, `package-lock.json`, `tsconfig.json`) does **not** cover `web\` — a `web\`-only change currently triggers no CI at all. Not fixed yet; flagging so it isn't mistaken for coverage that exists.

**CI and status docs (fixed as of `6e7e232`, 2026-07-30; Faza 2 section above updated 2026-08-04 — don't re-flag as stale without re-checking):**

- `.github\workflows\atmavictu-ci.yml` is the real CI for the root TS project: triggers on push/PR to `src/**`, `schema/**`, `package.json`, `package-lock.json`, `tsconfig.json`, runs `npm ci` then `npm run typecheck` and `npm test` on Node 22 (see the `web\` CI gap noted just above). Don't confuse it with `.github\workflows\ci.yml`, which is Python-flavored and path-filtered to `Projects/WorkShade/**` — that one still builds/tests nothing here.
- `README.md`'s "Status repoja"/"Faze" sections are current, not stale: Faza 0 and Faza 1 (model + service + repository + CLI layer, `src\workbenchManifest.ts`/`workbenchManifestRepository.ts`/`atmaCli.ts`) are marked DONE; Faza 2 (UI workbench) is marked IN PROGRESS (see above); Faza 3 (Tauri/runtime integration) is marked not started, matching `src\`/`web\` (no Tauri code exists yet).
- Root `pyproject.toml`/`requirements-dev.txt` are not Atmavictu's — they're the dev-dependency list (`pytest`, `jsonschema`, `black`, `isort`, `flake8`) for the Python CI (`.github\workflows\ci.yml`) that tests `Projects/WorkShade/**`. Atmavictu has no Python code and doesn't need them; don't add TypeScript equivalents there or assume they gate `npm test`.
