# Smisel — Current State & Next Task List

_Compiled: 2026-07-30 from `GAPS.md` (via list-gaps MCP), `CURRENT.md`, `CLAUDE.md`, live stack probes, git status, and the gate-routing audit. Re-derive from source files for anything time-sensitive._

---

## 1. What We Have — Live State Right Now

### Stack Health
| Component | Status |
|---|---|
| 14 Docker containers | All **Up**, all **healthy** |
| Open WebUI (`:3000`) | 200 |
| Canvas `/delo` (`:8765`) | 200 |
| LangFuse (`:3001`) | 200 |
| n8n (`:5678`) | 200 |
| Qdrant (`:6333`) | 200 |
| Pipeline logs | 0 errors in last 30 lines across all 3 containers |
| Windows tasks | Morning Witness (Ready/Disabled), Nightly Loop (Ready), Watchdog (Ready) |

### Git State
| Repo | Branch | Status |
|---|---|---|
| `D:\AI` root | `feature/ingest-delo-proposals` | **Active rebase** — 4 commits being replayed. `memory-bank/gate-routing-audit-2026-07-30.md` untracked |
| `Ops\space-control` | `master` | `scripts/register_backup_task.ps1` untracked |
| `Compose\SET Up` | `master` | `canvas/delo.html` staged, `pipelines/smart_router_filter.py` modified, `pipelines/prag_pipe.py` untracked |

### Gate Integrity
- All gate scripts confirmed on disk (`gate_closure.py`, `gate_kinds.py`, `promote_edge_candidate.py`, `promote_fragment.py`, `revoke_edge.py`)
- `canvas_server.py` write paths audited clean — no direct canon writes
- Known ungated paths from history all closed (PATCH 5b, CUT 1R-4R)
- Full pipeline line-by-line coverage not yet verified independently

### Graph State
- 164 nodes, 297 edges
- MCP tool reports "no known junk nodes found" — but GAPS.md/CURRENT.md list 5 junk nodes (`TestNode`, `OtherNode`, `Mocassin`, `Luka`, `Lukov`). The graph-node-lookup tool may not recognize them as junk under its classification logic.

### Completed Recently
- **Smisel Delo V1 — CLOSED 2026-07-30.** All 5 acceptance criteria proven live end-to-end. One real proposal (`proposal-9b5a4a65697e0f1951f39189e3bb169e`) exists, awaiting human action.
- Word Work lexeme write path: fixed (read-only mount bug → proxy pattern)
- Nightly Loop / Watchdog: re-enabled (2026-07-29)
- Graph-authority gating: deployed (CUT 1R-4R)
- Gate-routing audit: canvas_server.py confirmed clean (2026-07-30)

---

## 2. Open & Active Items (The Task List)

### HIGH — Blocking or Active

- [ ] **Delo V1 proposal follow-up.** The now-real proposal `proposal-9b5a4a65697e0f1951f39189e3bb169e` (Morning Witness re-enable decision) is awaiting human cut — Luka to review/reject/action. Delo V1 product is closed, this is a process item.
- [ ] **Active rebase on `D:\AI` root.** `feature/ingest-delo-proposals` has a mid-flight rebase replaying 4 commits. Do NOT touch `D:\AI` root git state until this completes or is explicitly aborted. The untracked `memory-bank/` files need to survive the rebase.
- [ ] **Word Work `/api/word-sheet/.../decide` sibling bug.** The lexeme write path was fixed (2026-07-29) via proxy pattern. The `/decide` endpoint likely has the same read-only mount bug — not yet investigated or fixed.
- [ ] **Smisel-canvas unexpected container recreation.** `RestartCount` resets — recurring, boot-correlated, root cause still unidentified. Ongoing operational risk.
- [ ] **`Compose\SET Up` uncommitted changes.** `delo.html` staged, `smart_router_filter.py` modified, `prag_pipe.py` untracked. The `delo.html` change is the propose-panel fix from Delo V1 closure — should be committed with a proper message.
- [ ] **`Ops\space-control` untracked `register_backup_task.ps1`.** Commit or explain why it's there.

### MEDIUM — PATCH 5 Register Separation (Partial)

- [ ] **5a Session Witness** — Minimal proof surface shipped (shared `run_id`, immutable JSONL receipt, read-only `/api/session-witness`). Not full.
- [ ] **5c Decision Surface** — Frame-rejection semantics done (Luka can reject option space). Broader Decision Surface and Session-End Accounting not built.
- [ ] **5d Session-End Accounting** — Not started.
- [ ] **Conversation Lineage V1** — Read-only pipeline shipped (normalize + projection + Canvas `/api/conversation-lineage`). Selection/promotion step not done — Luka needs to pick useful candidates; semantic tension proposals deferred until reviewed examples prove the boundary is useful.

### MEDIUM — Cutover & Cleanup

- [ ] **15 ACL-protected temp dirs** under `Corpus\Library\artifacts\tmp\` — empty, owner is `ATMAVICTU\Luka`, unresolved foreign SIDs persist. Needs admin-context delete. This is the only blocker to closing the `Library.pre_move_20260706` retirement.
- [ ] **5 junk graph nodes** (`TestNode`, `OtherNode`, `Mocassin`, `Luka`, `Lukov`) — removal decision locked, execution on HOLD pending a reference scan (dry-run + backup + mutation receipt required first). CURRENT.md BLOCKERS section applies.
- [ ] **Chronicle merge worktree** — Complete, tested feature (daily narrative generator + Canvas ORACLE panel), 11 commits, ~9600 lines, 4 test files. 9/11 merge conflicts resolved. Not committed. Can resume or discard — decision needed.

### MEDIUM — C-Drive Corpus Intake

- [ ] **Physical inventory done** (~49GB catalogued, 152,914 rows). Only 994 files (2.558 GB) hash-staged to D. One slice (23 conversation JSONs, 0.804 GB) deleted from C.
- [ ] **16.649 GB `COPY` bucket** — not yet staged to D at all.
- [ ] **Scope/ownership ambiguous** — possibly another agent's work (Claude Code?). GAPS.md §G explicitly calls for confirmation of who owns this and what the next approval step is.
- [ ] **The full C-drive intake design** (registry entries, separate Qdrant collections, retrieval contract) exists as conversation history text — not yet written to a `docs/superpowers/specs/` file. Parked behind nightly-loop reconciliation and remaining ungated writers.

### LOW — Documentation & Audit

- [ ] **`JEWIK_APD_WORKSPACE`** (`Projects\Obsidian\JEWIK_APD_WORKSPACE`) — real artifact from 2026-05-04 (earlier Claude instance, separate "JEWIK/APD/Ontoscience" project). 22 files, 8 fixed folders, its own README + manifest. Not referenced in root CLI docs. Needs documentation or acknowledgment.
- [ ] **`Delci\Work_Lineage_R0_Handoff.zip`** — Reviewed and decided (2026-07-19). GAPS.md should mark this closed instead of OPEN.
- [ ] **External Canvas API consumer** — found undocumented during audit. Needs identification and documentation.
- [ ] **Unexplained concurrent session** (2026-07-08, `.git_disabled` incident) — the actor that renamed `.git` mid-session appears to also be the one who fixed the `smisel_morning_report.py` bug. Worth confirming what it is so future sessions don't guess.
- [ ] **38 unpositioned ontology concepts** — deliberately left open (no definition text, low-confidence LLM guesses). Plus 5 non-concept terms in `graph.json` that overlap with the junk-node list above.

---

## 3. What There Is No Evidence Of

- No separate "next task list" file existed before this one. `GAPS.md` is the append-only record; `CURRENT.md` is Delo V1 scoped; `progress.md` is a snapshot summary. This file is the first structured task list that consolidates across all sources.
- No MCP server beyond `smisel-triage` exists. The `smisel-library`, `smisel-gaps`, and `smisel-delo` servers proposed this session don't exist yet — they'd provide structured read/write to library definitions, GAPS.md, and the Delo pipeline respectively.
- Full pipeline line-by-line gate routing audit: not done. The gate-routing audit only covers `canvas_server.py` and the documented closures. 58+ pipeline `.py` files remain unaudited for ungated canon writes.

---

## 4. Next Immediate Actions (Triage Priority)

1. **Resolve the rebase** — the `D:\AI` root git repo is in the middle of a rebase. Nothing else touching root files should proceed until this is resolved.
2. **Commit the SET Up working tree** — `delo.html` (propose panel), `smart_router_filter.py` (modifications), `prag_pipe.py` (new). These are Delo V1 closure artifacts.
3. **Commit or explain `register_backup_task.ps1`** in Ops.
4. **Investigate the `/api/word-sheet/.../decide` bug** — same read-only mount pattern as the already-fixed lexeme path.
5. **Investigate canvas container recreation** — root cause still unknown after multiple occurrences.
6. **Luka reviews the Delo V1 proposal** — `proposal-9b5a4a65697e0f1951f39189e3bb169e` awaits human cut.