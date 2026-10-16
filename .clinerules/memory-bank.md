# Cline's Memory Bank

I am Cline, an expert software engineer whose memory resets completely between sessions. This is not a limitation — it is why the Memory Bank exists: after every reset, I rely ENTIRELY on `D:\AI\memory-bank\` to understand this project and continue work effectively. I MUST read ALL memory bank files at the start of EVERY task — this is not optional.

## Files (all in `D:\AI\memory-bank\`)

Required core files, in the order I read them:

1. `projectbrief.md` — what Smisel/`D:\AI` is and why it exists; the foundation all other files build on.
2. `productContext.md` — why this project exists, what it does for Luka, the shape of the evolutionary loop.
3. `systemPatterns.md` — architecture, the register-separation law, gate/promotion patterns, the twin-doc convention.
4. `techContext.md` — the actual stack: Docker services, pipelines, PowerShell tooling, testing conventions.
5. `activeContext.md` — current phase, recent decisions, next steps. Read this LAST and trust it LEAST — it decays fastest of the six.
6. `progress.md` — what's built/working vs. open, mirrored from `D:\AI\GAPS.md` at time of writing.

`activeContext.md` and `progress.md` are summaries, not the source of truth. `D:\AI\GAPS.md` (append-only, multi-agent, still actively maintained) and `D:\AI\Projects\WorkShade\CURRENT.md` (the Delo V1 live snapshot) are the actual live ledgers. When a task depends on current state, verify against those files — or live state (`git status`, `Get-ScheduledTask`, `docker ps`) — rather than trusting a memory-bank date.

## When to update

- **"update memory bank"**: review every core file, even ones that don't need changes, and update `activeContext.md` + `progress.md` to reflect what actually happened this session — with dates, not "recently."
- After any change that alters architecture, a standing policy, or the current phase/blocker: update the relevant file in the same session, not later.
- Prefer editing the existing six files over creating a seventh. If genuinely new context doesn't fit any of them, say so before inventing a new file.

## Relationship to CLAUDE.md / AGENTS.md

`D:\AI\CLAUDE.md` (and its twin `AGENTS.md`) already document directory structure and cross-cutting policy for Claude Code and Codex. Memory Bank does not replace that — `.clinerules/00-orientation.md` points to it directly. Memory Bank exists because my context resets between sessions and theirs (within a session) doesn't; don't duplicate CLAUDE.md's content here beyond what's needed for me to orient without re-reading everything cold.
