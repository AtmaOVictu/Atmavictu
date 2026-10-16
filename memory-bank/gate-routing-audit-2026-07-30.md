# Gate Routing Audit — 2026-07-30

Canonical write paths: `library/definitions/`, `library/graph.json`, Qdrant collections, `CONTEXT.md`.

## canvas_server.py — CLEAN

All 4 write sites in canvas_server.py route to non-canon paths:

| Line(s) | Function | Writes to | Gate required? |
|---|---|---|---|
| 235 | `_write_workspace_file()` | Workspace (any path inside workspace root) | Path-guarded by `_safe_workspace_path()` |
| 642 | Atomic artifact save | `drafts/` | No — `drafts/` is non-canon by definition |
| 700-702 | `_publish_successor_publication()` | `drafts/delo_successor_[hex32].md` | No — strict regex guard on path |
| 1014-1023 | `_delo_persist_proposal()` | `logs/work_sessions/proposals/` + receipts | No — `logs/` is append-only; proposal is inert (`may_mutate: false`, `may_enter_canon: false`) |

**Verdict:** No direct writes from canvas_server.py to any canon/governed register. All written paths are either drafts, logs, or proxy-through-pipelines (lexeme writes via `lexeme_writer_filter.py`, fixed 2026-07-29 after the read-only mount bug was found).

## Pipelines — Partially Audited (known closures per GAPS.md)

Full line-by-line audit of all pipeline files deferred to a dedicated session (58+ .py files). Known closures from GAPS.md §B, §E, §K:

| Pipeline | Write target | Gate status |
|---|---|---|
| `dialectic_pipe.py` | `library/definitions/`, Qdrant, `graph.json` | GATED — PATCH 5b (2026-07-09). Requires `human_action_id` via `gate_closure.py`. |
| `variator_pipe.py` | `library/definitions/`, `graph.json` | GATED — PATCH 5b (2026-07-09). |
| `synthesis_pipe.py` | `library/synthesis/`, Qdrant `library`, `graph.json` | GATED — PATCH 5b (2026-07-09). |
| `knowledge_graph.py` (`/graph-extract`) | `graph.json` | GATED — CUT 2R (2026-07-27). Rerouted to `edge_candidates/`. |
| `canvas_probe.py` (`/probe`) | `graph.json` | GATED — CUT 2R (2026-07-27). Rerouted to `edge_candidates/`. |
| `auto_curator.py` | `library/definitions/` | GATED — `auto_approve_threshold: 0` (2026-07-08). Routes to `pending/` + `/approve`. |
| `save_to_workShade.py` (`/apply-context`) | `CONTEXT.md` | GATED — Monthly Identity Update requires `approve_context_merge` (2026-07-08). |

**Known ungated history (all now closed):**
- Nightly Curator auto-approve bypass (closed 2026-07-08, `auto_approve_threshold: 0`)
- Graph-extract/probe direct writes to `graph.json` (closed 2026-07-27, CUT 1R-4R)
- Dialectic/variator/synthesis direct writes (closed 2026-07-09, PATCH 5b)
- Monthly Identity Update unattended merge (closed 2026-07-08)

## Edge Candidates — Working Gate Path

The promotion chain for new graph edges:
```
LLM generates edge → edge_candidate_writer.py → library/edge_candidates/
                                                    ↓
                                     promote_edge_candidate.py (requires human_action_id)
                                                    ↓
                                               graph.json
                                                    ↕
                                     revoke_edge.py (undo half)
```

RAG/`/api/node` default to approved-tier, non-revoked edges only (CUT 4R, 2026-07-27). Candidates surfaced separately.

## Open Risk

The triage tool's `gate-verify` MCP call correctly warns: *"This check verifies gate scripts exist on disk. It does not verify that all write paths in running code actually route through them."* A full code-level confirmation requires a line-by-line grep of all 58+ pipeline files for any `open(..., 'w')`, `write_text`, `json.dump`, or direct Qdrant client `.upsert()` that targets a canon register without routing through a gate first.

This audit confirms:
1. **canvas_server.py** writes are clean — no canon writes, all guarded or proxy'd
2. **Known ungated paths** from GAPS history are all closed
3. **Gate scripts** exist on disk and match their documented closures
4. **Full pipeline coverage** is assumed based on the PATCH 5b/CUT 1R-4R work but not independently verified line-by-line