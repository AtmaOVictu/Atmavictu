# Active Context

_Last refreshed: 2026-07-30, from a real read of `GAPS.md` + `CURRENT.md` + live MCP triage (not invented). This file decays fastest of the six — re-check the source files before trusting a date on this page._

## Current phase

**Smisel Delo V1 — CLOSED 2026-07-30.** All five ACCEPTANCE PROOF criteria proven live (`CURRENT.md` lines 75-100, `GAPS.md` §N): draft and decision output types, full artifact metadata, continue with `parent_artifact_id`, propose creates non-mutating Work Session candidate, real (not synthetic) goal exercised end-to-end. One inert proposal (`proposal-9b5a4a...`) exists, `awaiting_human_cut`. 

**Current phase is now post-Delo-V1: maintenance + next-priority selection.** No new feature phase has been declared. The open `GAPS.md` items (§C ACL residue, §E chronicle merge, §G C-drive intake, §H Delci handoff, §O JEWIK_APD_WORKSPACE, junk graph nodes) are all HOLD or unowned — none is an active build target.

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
