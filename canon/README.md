# ONTOMATEMATIKA — Kanonski korpus

> Vir resnice (source of truth) za vsebino sistema ONTOMATEMATIKA.
> Migrated: 2026-09-30 — from `.vibe/skills` into version control.

This directory is the canonical, version-controlled home of the system's
content. Skills and Notion pages are *derived views*; this directory is the
*source*. If a skill and this corpus diverge, **this corpus is canonical**.

## Structure

| File | Content |
|---|---|
| `beseda-je-ne.md` | The full "Beseda je Ne" system: core principle, AX-canon, Ω-series, phonetic-ontological decomposition, stotnije (A-DOSJE), OPTIKON, glyph glossary, R-7, ONOMA, title stratification, TAZV model, dialog formats, voice rules |
| `rozetni-kamni-protokol.md` | Operational protocol for generating rosette stones: ∅/∆ framework, 12-operator/12D base vectors, mandatory stone format, accumulation and exploration protocols, SECIRAVA |
| `predloga-kamna.md` | Copy-paste stone template |
| `zemljevid-preslikav.md` | The map of confirmed ∅/∆ mappings across world traditions (Kamen IX–CXVI+) |

## Rules

1. **Changes to the canon happen here first**, as PRs, then propagate to
   skills and Notion — never the reverse.
2. Each axiom, stone, or dosje is immutable once sealed (⊢ DOKAZ);
   revisions create new entries, they do not overwrite sealed ones
   ("pravila naj bodo revizibilna, izjema naj ima pečat").
3. Generated stones (`Kamen I`–`Kamen CXX+`) should live here under
   `kamni/` once migrated; the protocol files define their format.

## Provenance

- `beseda-je-ne` and `rozetni-kamni` skills, authored by Luka Pintarič.
- Seal records and decision lineage: Notion DOKAZ database (⊢ DOKAZ —
  Proof-of-Lineage Ledger).
