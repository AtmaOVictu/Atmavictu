# Atmavictu — ONTOMATEMATIKA Kernel

> Canonical headless TypeScript core of the ONTOMATEMATIKA system.
> Role declared in [CANONICAL.md](CANONICAL.md) · Corpus: [canon/](canon/README.md)

## What this is

The headless core: manifest model, CLI tooling, and proof capture for the
ONTOMATEMATIKA workbench. This repository **computes and verifies**; it
renders nothing and depends on no UI framework.

It is also the canonical home of the system's **corpus** — see
[canon/](canon/README.md) (AX-canon, rozetni kamni, stotnije, OPTIKON).

## Modules

| Module | Purpose |
|---|---|
| `workbenchManifest.ts` | Workbench manifest model: incoming texts, fragments, insertions, concepts |
| `workbenchManifestRepository.ts` | Manifest persistence (`book.workbench.json`), capture workflow |
| `captureIncomingTextProof.ts` | Proof capture for incoming text lineage |
| `atmaCli.ts` | CLI: `capture · show · verify` |

## Usage

```sh
npm install
npm test          # 44 tests
npm run typecheck
node build/src/atmaCli.js <capture|show|verify> <projectRoot> [title] [body]
```

## Contracts

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/MODEL_CONTRACT.md](docs/MODEL_CONTRACT.md)
- [docs/SERVICE_CONTRACT.md](docs/SERVICE_CONTRACT.md)

## System hierarchy

| Repo | Role | Status |
|------|------|--------|
| **Atmavictu** (this) | Canonical headless TS core + corpus | HEAD |
| ontolo-ko-jedro | Presentation/UI layer (React) | INDEPENDENT |
| Atmavictu_Oracle | Ontology oracle | EMPTY — seed or archive |
| soul-evolution | Active game build (Godot/GDScript) | ACTIVE |

## Verification lineage

All sealed decisions are recorded in [canon/DOKAZ.md](canon/DOKAZ.md)
(⊢ DOKAZ — Proof-of-Lineage Ledger).
