# Active Context

_Last refreshed: 2026-07-30, from a real read of `GAPS.md` + `CURRENT.md` + live MCP triage (not invented). This file decays fastest of the six — re-check the source files before trusting a date on this page._

## Current phase

**Smisel Delo V1 — CLOSED 2026-07-30.** All five ACCEPTANCE PROOF criteria proven live (`CURRENT.md` lines 75-100, `GAPS.md` §N): draft and decision output types, full artifact metadata, continue with `parent_artifact_id`, propose creates non-mutating Work Session candidate, real (not synthetic) goal exercised end-to-end. One inert proposal (`proposal-9b5a4a...`) exists, `awaiting_human_cut`. 

**Current phase is now post-Delo-V1: maintenance + next-priority selection.** No new feature phase has been declared. The open `GAPS.md` items (§C ACL residue, §E chronicle merge, §G C-drive intake, §H Delci handoff, §O JEWIK_APD_WORKSPACE, junk graph nodes) are all HOLD or unowned — none is an active build target.

**New capability added 2026-08-07 (Cline): Canvas File Manager (/files).** A read + rename + restore + archive surface for workspace files at `localhost:8765/files` (button "▤ DATOTEKE" in `/map` nav). Backend: `/api/files`, `/api/files/read`, `/api/files/write`, `/api/files/rename`, `/api/files/archive` in `canvas_server.py`. Register-aware: authority paths (graph.json, definitions/, CONTEXT.md, synthesis/, edge_candidates/, references/) are `danger` → require `confirm:true`, every mutation is logged to `logs/file_ops_receipts.jsonl`. No hard delete — archive moves to `_archive/<timestamp>/`. Writes go through the open-terminal proxy (canvas /workspace is `:ro`), proven live. Frontend source `WorkShade/scripts/canvas_files.html` → deployed `files.html`; backend twin-synced across `canvas_server.py` + `server.py` + `WorkShade/scripts/canvas_server.py`. Known limit: `/functions` (Compose pipeline/function python) are NOT reachable from canvas because only WorkShade is mounted — that's a Phase-3 candidate (extra mount or proxy). Note 2026-08-07: `WorkShade/scripts/*.py` (258 functions) ARE reachable/editable via `/files` — verified reading one live. UI polish added same session: quick-jump buttons (Drafts/Library/Definitions/Scripts/Inbox/Logs/Archive), filename filter, per-type color dots, and a fixed critical bug (onclick handlers now expose globals `window.go/save/createNew/rename/reload/archive/applyFilter` — previously the buttons silently did nothing because all functions were IIFE-local). **Compose/SET Up/functions now READ-ONLY viewable** (2026-08-07): canvas gets a second bind mount `D:/AI/Compose/SET Up/functions:/owu-functions:ro` (+ env `FUNCTIONS_PATH=/owu-functions` in `DockerCompose.yml`); `/files` lists/browses `functions/` (5 OWU functions) but write/rename/archive are refused (runtime-register guard, tested live). Initial `/app/functions:ro` mount failed (can't nest a mountpoint inside an already-`:ro`-mounted `/app`) — `/owu-functions` root avoids that.

**Atmavictu Faza 2 — read/rename/update (2026-08-07, Cline).** Three new pure model operations added to `src/workbenchManifest.ts`: `updateIncomingText` (rename source), `updateFragment` (restore excerpt text), `updateInsertion` (retarget chapter path). Contract-first: docs `SERVICE_CONTRACT.md` and `MODEL_CONTRACT.md` updated. API: `POST /api/incoming/:id/update`, `POST /api/fragments/:id/update`, `POST /api/insertions/:id/update` in `workbenchApiServer.ts`. UI (web/): `VhodniTekstPanel` gets "Preimenuj vir" (inline title edit) and "uredi" (inline textarea + "Shrani obnovo") per Fragment; `AktivnaKnjigaPanel` gets a visible Insertions list with "uredi" (targetChapterPath + positionNote). Optional field semantics: `undefined`=leave, `null`=remove, string=set. **Fragment.title added (2026-08-07)** as a real fragment-renaming field. **v2 contract + migration (2026-08-07):** `manifestVersion` bumped to `"2"`; new `schema/workbench.manifest.v2.schema.json` (Fragment gains `title`); `migrateManifestV1ToV2()` in the model and auto-migration in the repository (`readManifestFromFile` upgrades+persists a v1 file); v1 schema reverted to original (no title). Kept as a clean v1→v2 evolution so existing on-disk manifests upgrade losslessly. All 64 tests pass, web typecheck+build OK. **Faza 3 — Concepts + analysis (2026-08-07):** `addConcept` (model + `POST /api/concepts`), `updateFragment` now accepts `conceptIds` (tag fragments with concepts, validated against existing concepts), and three analytical/read-only views: `GET /api/concepts` (with `fragmentCount`), `GET /api/analysis/source` (per-source draft/inserted/archived counts), `GET /api/overview` (book aggregate + per-chapter insertion counts). UI: `VhodniTekstPanel` gains a "Koncepti" section (create + list) and "Analiza" section, plus per-fragment concept checkboxes in the edit view. This is the "interconnected computations" step — fragments group by concepts, sources show usage. All 69 tests pass, web typecheck+build OK.

## Cline's first triage session (2026-07-30)

Cline ran a full 9-tool MCP triage and read all orientation files. Key live findings:

- **Stack: GREEN.** All 14 Docker containers Up, all 4 scheduled tasks Ready, all 5 HTTP endpoints 200, zero pipeline errors.
- **Backups: AMBER.** Latest hot backup is 2026-07-07 (23 days stale). `Smisel Backup` task was created today, daily 01:30 — no `LastRunTime` yet, but likely hasn't had its first scheduled window.
- **Qdrant: AMBER.** `knowledge` collection (documented) is missing. `open-webui_files` and `open-webui_knowledge` are undocumented. 3 junk collections remain.
- **Git: AMBER.** All 3 repos dirty — expected multi-agent drift pattern, not emergency. Root repo is on `feature/ingest-delo-proposals` branch, not `master`.
- **Gates: GREEN on disk.** All 4 gate mechanisms present. All 4 historically-ungated write paths confirmed closed. Full runtime code-audit (verifying every write path actually routes through gates) has not been done.
- **Canvas: AMBER.** 11 undocumented endpoints returning 200. `/api/fragments` returned 0 (connection error, unexpected for a documented endpoint).
- **Graph: AMBER.** 164 nodes / 297 edges. All nodes report `kind: unknown` (parsing gap or schema gap). 5 junk nodes still present, removal on HOLD.

## Most recent decisions (cumulative through 2026-07-30)

- Presence-based "don't produce while I sleep" policy superseded (2026-07-27) — candidate-level generation may now run continuously; human gating applies only at authority crossings.
- `smisel_continuity_protocol.md` and Decision Surface labels: intentionally separate, cross-referenced not merged.
- Junk graph nodes: removal decision locked, execution still on HOLD pending a reference scan.
- Delo V1: closed. Propose-to-Work-Session proven end-to-end against a real goal (Morning Witness re-enable decision), not synthetic.
- `Smisel Backup` task created 2026-07-30, daily 01:30. `Smisel Morning Witness` re-enabled 2026-07-30 (both blockers resolved: presence policy superseded, headless pythonw.exe confirmed).
- Docker ports restricted to `127.0.0.1` (2026-07-29).
- `JEWIK_APD_WORKSPACE` discovered 2026-07-30 — dormant prior system, deliberately kept separate per existing cross-reference policy. Its Find→Choose→Patch→Prove→Replay cycle adopted into Claude Code collaboration protocol.

## Standing constraint to not forget

The system works in two modes: **with Luka** (interactive, during sessions) and **separately from Luka** (continuous candidate generation). The boundary is authority, not presence: unattended generation is fine; unattended promotion to canon requires a `human_action_id`. The register-separation gates are the mechanism — whether they hold is a live question, not a settled claim.
