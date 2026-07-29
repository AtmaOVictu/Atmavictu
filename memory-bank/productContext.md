# Product Context

## Why Smisel exists

Smisel ("meaning" in Slovenian) is Luka's personal knowledge-and-thinking system: a chat interface (Open WebUI) wired to a growing corpus of definitions, an evolving concept graph, and a formal ontological framework — not a generic chatbot deployment.

The framework is a canonical 8-operator sequence — **O → ⊘ → EN → ⧖ → ∆ → EJ → JAS** (plus NE) — defined in `WorkShade\library\references\00_META_GLOSSARY.md`. These operators are fixed points; the system's job is to develop them (via `/lexikon`, `/seciraj`, `/dialectic`) and grow a concept graph around them, not to have an LLM invent or redefine them.

## The evolutionary loop (what the product actually does)

Conversation → nightly curation of recurring terms → definitions → graph edges → weekly synthesis clusters recent saves → reflection diffs graph snapshots to show what emerged → proposed CONTEXT.md updates close the loop back into the AI's own system prompt/identity.

Every stage of that loop was, at one point or another, found writing directly into approved/canonical state with no human review (`GAPS.md` §B, §E, §K) — the recurring product lesson here is that **generation is cheap and continuous; promotion to canon is the part that must stay gated.** See `systemPatterns.md` for the register law this became.

## Delo V1 — the current user-facing focus

Luka's own diagnosis (`GAPS.md` §F): the existing surface could show what the system did but not simply *do* something useful for him in one sitting. Delo (`/delo` in Canvas) is the answer: goal in → local-source-grounded draft or decision out, on one page, with proof/uncertainty labeled, ending in an explicit SAVE / DISCARD choice — never automatic promotion. See `Projects\WorkShade\CURRENT.md` for its live status.

## Who else touches this

- **Claude Code** — root orientation, `Ops\space-control`, cross-cutting audits/gates.
- **Codex** — Smisel Delo V1 / Canvas product work in WorkShade.
- **Cline** (this agent) — no fixed lane yet; oriented here so it doesn't rediscover the register law the hard way.
- Occasional **unidentified concurrent sessions** — documented, not paranoia: `GAPS.md` §E/§J/§L record real instances of files changing mid-session from a source other than the active one.
