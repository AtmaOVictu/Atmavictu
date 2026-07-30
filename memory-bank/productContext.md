# Product Context

## Why Smisel exists

Smisel ("meaning" in Slovenian) is Luka's personal knowledge-and-thinking system: a chat interface (Open WebUI) wired to a growing corpus of definitions, an evolving concept graph, and a formal ontological framework — not a generic chatbot deployment.

The framework is a canonical 8-operator sequence — **O → ⊘ → EN → ⧖ → ∆ → EJ → JAS** (plus NE) — defined in `WorkShade\library\references\00_META_GLOSSARY.md`. These operators are fixed points; the system's job is to develop them (via `/lexikon`, `/seciraj`, `/dialectic`) and grow a concept graph around them, not to have an LLM invent or redefine them.

## The evolutionary loop (what the product actually does)

Conversation → nightly curation of recurring terms → definitions → graph edges → weekly synthesis clusters recent saves → reflection diffs graph snapshots to show what emerged → proposed CONTEXT.md updates close the loop back into the AI's own system prompt/identity.

The system works in two modes: **with Luka** (interactive, during sessions — Delo, Canvas, chat) and **separately from Luka** (continuous candidate generation — nightly curation, synthesis, variator). The boundary is authority, not presence: unattended generation is fine; unattended promotion to canon is not. Every stage of the loop has been found writing directly into approved/canonical state at some point (`GAPS.md` §B, §E, §K). The register-separation law is the mechanism for this boundary, not a guarantee. See `systemPatterns.md`.

## Delo V1 — the current user-facing focus

Luka's own diagnosis (`GAPS.md` §F): the existing surface could show what the system did but not simply *do* something useful for him in one sitting. Delo (`/delo` in Canvas) is the answer: goal in → local-source-grounded draft or decision out, on one page, with proof/uncertainty labeled, ending in an explicit SAVE / DISCARD choice; promotion to canon always requires human action. See `Projects\WorkShade\CURRENT.md` for its live status.

## Who else touches this

- **Claude Code** — root orientation, `Ops\space-control`, cross-cutting audits/gates.
- **Codex** — Smisel Delo V1 / Canvas product work in WorkShade.
- **Cline** (this agent) — no fixed lane yet; oriented here so it doesn't rediscover the register law the hard way.
- Occasional **unidentified concurrent sessions** — documented, not paranoia: `GAPS.md` §E/§J/§L record real instances of files changing mid-session from a source other than the active one.
