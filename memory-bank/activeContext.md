# Active Context

_Last refreshed: 2026-07-29, from a real read of `GAPS.md` + `CURRENT.md` (not invented). This file decays fastest of the six — re-check the source files before trusting a date on this page._

## Current phase

**Smisel Delo V1 — live decision/propose verification** (`Projects\WorkShade\CURRENT.md`). Owner: Codex (implementation) / Claude Code (review + docs on PATCH READY or HOLD). The metadata/lifecycle work is done and proven live; the one remaining acceptance criterion — actually exercising "propose to Work Session" for a saved artifact — hasn't been located/run yet. Next concrete step: find that action in the live `/delo` or Canvas DECIDE UI and run it against a real (not synthetic) goal.

## Most recent decisions (2026-07-29 session)

- Presence-based "don't produce while I sleep" policy superseded (2026-07-27, ratified) — candidate-level generation may now run continuously; human gating applies only at authority crossings (candidate→approved, approved→canon). This is why Nightly Loop/Watchdog could be safely re-enabled 2026-07-29.
- `smisel_continuity_protocol.md`'s raw→interpreted→grounded→canonical ladder and the Decision Surface's raw/candidate/approved/canon/indexed/runtime labels: confirmed intentionally separate, cross-referenced rather than merged.
- Junk graph nodes: removal decision locked, execution still on HOLD pending a reference scan (dry-run + backup + mutation receipt required first).

## What just got built into this project (Cline onboarding, this session)

`.clinerules\` (behavior rules + this Memory Bank) and `memory-bank\` (this folder) were added 2026-07-29 so Cline starts oriented instead of cold, mirroring the CLAUDE.md/AGENTS.md twin pattern for a third agent. Added to the root `.gitignore` allowlist and noted in `CLAUDE.md`/`AGENTS.md` — check those two files' current text for the authoritative wording, this note may already be stale.

## Standing constraint to not forget

The system works in two modes: **with Luka** (interactive, during sessions) and **separately from Luka** (continuous candidate generation). The boundary is authority, not presence: unattended generation is fine; unattended promotion to canon requires a `human_action_id`. The register-separation gates are the mechanism — whether they hold is a live question, not a settled claim.
