# Tech Context

## Stack (Docker, `Compose\SET Up\DockerCompose.yml`)

14 containers, all bound to `127.0.0.1` only (tightened 2026-07-29). Core: Open WebUI (`:3000`, chat UI) → Ollama (host, `:11434`, not containerized) → Qdrant (`:6333`, vector DB, collections below) → Tika (`:9998`, doc extraction). Supporting: n8n (`:5678`, scheduled workflows), LangFuse (`:3001`, tracing), SearXNG (`:8888`, search), Crawl4AI (`:11235`, JS-capable crawl), Faster-Whisper (`:8001`, STT), LibreTranslate (`:5000`, EN↔SL), Open Terminal (`:8000`, sandboxed shell), Canvas (`:8765`, the knowledge-graph UI, `canvas/server.py`), ComfyUI (host, `:8188`, image/video gen).

Pipelines reach Ollama via `host.docker.internal:11434`; containers reach each other by service name.

## Qdrant collections

`library` (curated defs, high-priority RAG) · `open-webui_knowledge` (uploads/crawls/whisper, Open WebUI-managed) · `workShade` (raw saves, recall-only) · `memories` (mem0-managed user facts) · `web_cache` (SearXNG cache) · `chat_logs` (indexed conversation turns). Pipeline-generated (undocumented until 2026-07-30 triage): `definitions_live_approved` (approved defs for RAG) · `definitions_workbench_all` (full definition working set). Embedding: `bge-m3`, 1024 dims, multilingual — never swap without re-indexing everything.

## Known junk collections

`Midjourney Styles` · `Prefix Cache` · `Qdrant Web Documentation` — Open WebUI plugin/community artifacts, not Smisel-managed. Safe to drop. `mem0migrations` — mem0 migration residue, investigate before dropping.

## Pipelines (`Compose\SET Up\pipelines\*.py`)

One `.py` file per filter/pipe. **Hot-reload does not work on Windows** (watchfiles gets no NTFS-bridge events through Docker Desktop) — any edit needs `docker compose -f DockerCompose.yml restart pipelines`. Pipes must NOT set `self.type = "pipe"` in `__init__` (falls out of `/v1/models` registration silently) — only `filter`/`manifold` register explicitly. `Valves` must subclass `BaseModel`, never plain `object`.

Pipelines mount `Projects\WorkShade` at `/workspace` — that's why some write routes (e.g. `lexeme_store.py`, found broken 2026-07-29) fail when called in-process from `canvas_server.py`, whose own `/workspace` mount is `:ro`; the working pattern is proxy-through-pipelines (`zivi_dokaz_filter.py`, `lexeme_writer_filter.py`).

## `Ops\space-control` (PowerShell tooling, separate git repo)

Every script: `param()` block with a `..\reports`-relative default output dir, named testable functions, and a top-level `if ($MyInvocation.InvocationName -ne '.')` guard so Pester can dot-source it without triggering a real run. **Only Pester 3.4.0 is installed** — legacy `Should Be` syntax, not Pester 5's `Should -Be`; don't "modernize" test files. `cutover_common.ps1` is the shared plan/helpers module (`Get-CutoverPlan` is the single source of truth for cutover paths/tokens) — two live-incident gotchas to preserve: never wrap mutating steps in `GetNewClosure()` (breaks dot-sourced function resolution), and `-ErrorAction Stop` is load-bearing on every mutating step (esp. `Rename-Item`, which is non-terminating by default).

## Testing conventions elsewhere

WorkShade/Compose Python: pytest-style, targeted suites per feature (e.g. `test_canvas_delo.py`, `test_graph_edge_authority_reconciliation.py`); tests are treated as load-bearing documentation of what a patch actually proved, referenced by name from `GAPS.md` entries.

## Where secrets live

`Compose\SET Up\.env` — DockerCompose reads `${VAR}`; n8n workflows use `$env`. As of 2026-07-26 all 10 previously-hardcoded secrets (a shared bearer token duplicated across scripts/pipelines/n8n JSONs/CLAUDE.md prose) were externalized to `.env`. Never hardcode a new one back in.
