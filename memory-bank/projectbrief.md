# Project Brief

`D:\AI` is the D-drive storage and operations root for **Smisel**, a local, self-hosted AI stack built around Open WebUI + Ollama + Qdrant, running as 14 Docker containers on Luka's own machine (`ATMAVICTU`). It works in two modes: **with Luka** (interactive, during sessions — Delo, Canvas, chat) and **separately from Luka** (continuous candidate generation — nightly curation, synthesis). The boundary is authority, not presence: unattended generation is fine; unattended promotion to canon requires human action. It is a personal system, not a product-in-development for external users — the "customer" is Luka's own ongoing thinking/writing practice, conducted mostly in Slovenian.

Two code/data folders were migrated here from `C:\Users\Luka\Documents` on 2026-07-06, with NTFS junctions left at the old C paths for backward compatibility — those paths still exist and are still bind-mounted by the Docker stack, but D is canonical.

## Scope of this directory

| Directory | Role |
|---|---|
| `Ops\space-control\` | PowerShell tooling repo — storage inventory, backups, junction-cutover machinery. Own git history, separate from root. |
| `Compose\SET Up\` | The live Smisel stack: compose file, pipelines, functions, n8n workflows, Canvas. |
| `Projects\WorkShade\` | The stack's data workspace — library, definitions, graph, logs, scripts that pipelines mount at `/workspace`. |
| `Corpus\` | Markdown knowledge corpus (Slovenian), 50k+ files. |
| `Backups\smisel_live\` | Timestamped hot/cold backups. |
| `Models\ollama\` | Ollama model storage. |

`D:\AI` root itself became a git repo 2026-07-28, scoped via an allowlist `.gitignore` to root docs only (`CLAUDE.md`, `AGENTS.md`, `.gitignore` — now also `.clinerules/` and `memory-bank/`). It does not track Corpus, Backups, Models, Compose, or Projects.

## Non-goals

Not a commercial product, not multi-tenant, not built for anyone besides Luka to operate. Decisions favor Luka's own working style (Slovenian-language ontology, register discipline, explicit human approval at authority boundaries) over generic best-practice defaults.
