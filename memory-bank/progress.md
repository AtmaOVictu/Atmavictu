# Progress

Snapshot written 2026-07-30 from live MCP triage + `GAPS.md` + `Projects\WorkShade\CURRENT.md`. **Re-derive from those two files for anything time-sensitive** — this is a summary at a point in time, not a live feed.

## Working / closed

- C→D storage cutover: complete (2026-07-06). Junctions at old C paths are a safety net, not a second home — D is canonical.
- Register-separation gates (PATCH 5b): auto_curator auto-approve, dialectic/variator/synthesis direct writes, and monthly identity-update merges are all now gated behind explicit human approval.
- Graph-authority gating (CUT 1R–4R, 2026-07-27): `/graph-extract` and `/probe` no longer write `graph.json` directly; edge candidates → promotion → revoke, RAG/`/api/node` now default to approved-tier only.
- Nightly Loop / Watchdog: re-enabled 2026-07-29. Watchdog is stack-health-recovery only; nightly content generation has exactly one trigger owner now.
- Morning Witness: re-enabled 2026-07-30 (both blockers resolved: presence policy superseded, headless pythonw.exe confirmed).
- `Smisel Backup` task: created 2026-07-30, daily 01:30. First run not yet confirmed (no `LastRunTime`). Latest hot backup is still 2026-07-07 (23 days stale as of triage).
- Docker ports restricted to `127.0.0.1` (2026-07-29).
- **Atmavictu Faza 5 — Qdrant semantic search + create-time suggestions done (2026-08-07, Cline):** `src/workbenchSemantic.ts` (pure embedding/index/search builders) + `POST /api/semantic/index-fragments` + `POST /api/semantic/search` (Ollama `bge-m3` → Qdrant `workbench_fragments`); graceful 502 when services unreachable. UI "Semanticno iskanje" section. `createFragmentFromIncoming` accepts `{title?,conceptIds?}`; create form has title + concept checkboxes + "Predlagaj". 85/85 tests; web typecheck+build OK.
- **Atmavictu Faza 4 — LLM-assisted suggestions done (2026-08-07, Cline):** `src/workbenchSuggestions.ts` (pure prompt/parser) + `POST /api/suggestions` calling Ollama (`qwen3:8b`, configurable `ollamaUrl`, 15s timeout) to suggest fragment title + concepts; graceful fallback (400/502, never blocks). UI "Predlagaj" button fills title + concept checks. 76/76 tests; web typecheck+build OK.
- **Atmavictu Faza 3 — Concepts + analysis done (2026-08-07, Cline):** `addConcept` (model + `POST /api/concepts`), `updateFragment` accepts `conceptIds` (validate against existing concepts), analysis views `GET /api/concepts` (fragmentCount), `GET /api/analysis/source`, `GET /api/overview`. UI: VhodniTekstPanel "Koncepti" + "Analiza" sections + per-fragment concept checkboxes. 69/69 tests pass; web typecheck+build OK.
- **Atmavictu Faza 2 — read/rename/update done (2026-08-07, Cline):** `updateIncomingText` (rename source title), `updateFragment` (restore excerpt text + `Fragment.title` for real fragment renaming), `updateInsertion` (retarget chapter path) added to model + API (`POST /.../update`) + UI (`VhodniTekstPanel` rename/uredi, `AktivnaKnjigaPanel` now shows Insertions with uredi). **v2 contract + migration (2026-08-07):** `manifestVersion` → `"2"`, new `schema/workbench.manifest.v2.schema.json`, `migrateManifestV1ToV2()` + repository auto-migrate on load (a v1 file upgrades & persists as v2). Contract-first docs updated. 64/64 tests pass; web typecheck+build OK.
- **Canvas File Manager (2026-08-07, Cline):** `localhost:8765/files` — read / rename / update / archive workspace files. Register-aware danger gating on authority paths + JSONL mutation receipts (`logs/file_ops_receipts.jsonl`); archive (soft-delete → `_archive/`) instead of hard delete. Twin-synced across all 3 `canvas_server.py` copies + `canvas_files.html` source. Writes proxy through open-terminal (`/workspace` is `:ro`).
- **Delo V1: CLOSED 2026-07-30.** All five ACCEPTANCE PROOF criteria proven live (`CURRENT.md` lines 75-100, `GAPS.md` §N). One inert proposal exists, `awaiting_human_cut`.
- Word Work / lexeme write path: found completely broken in production (read-only mount bug), fixed via proxy pattern, proven live (2026-07-29). Sibling `/api/word-sheet/.../decide` route likely has the same bug, not yet fixed.
- Smisel Explorer (Coders Lab final project) built and shipped 2026-07-26.
- `Compose\SET Up` and `D:\AI` root both git-tracked; `Ops\space-control` always was. All three repos currently dirty with uncommitted changes (multi-agent drift, expected).
- Cline onboarded as third agent: `.clinerules\` + `memory-bank\` added 2026-07-29, verified working 2026-07-30.

## Open / in progress (from `GAPS.md`, not actively being worked)

- C-drive corpus intake: physical inventory done (~49GB), only a small hash-verified subset staged to D; the larger 16.6GB "COPY" bucket is untouched. Unowned — no owner confirmed since discovery.
- `Library.pre_move_20260706` ACL residue: 15 empty protected temp dirs, delete not yet attempted.
- `chronicle_merge_attempt` worktree: 9/11 files resolved, not committed — safe to resume or discard.
- `Delci\Work_Lineage_R0_Handoff.zip`: reviewed and decided (2026-07-19), but the §H gap was never formally checked off.
- `smisel-canvas` container recreating unexpectedly — recurring, boot-correlated, root cause still unidentified.
- Junk graph nodes: removal decision locked, execution on HOLD pending a reference scan.
- `JEWIK_APD_WORKSPACE`: dormant prior system discovered 2026-07-30, deliberately kept separate.
- Qdrant collection drift: `knowledge` collection missing, `open-webui_files`/`open-webui_knowledge` undocumented. 3 junk collections remain.
- Canvas API: 11 undocumented endpoints returning 200. `/api/fragments` returned connection error (0), unexpected for a documented endpoint.

## Full ledger

`D:\AI\GAPS.md` — the actual append-only record, sections A through L as of this writing. Read it directly for anything not summarized above.
