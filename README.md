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
npm test          # 85 tests (⊢ izmera 21. 10. 2026)
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
| Atmavictu_Oracle | Ontology oracle (zgodovinsko seme) | ARHIVIRAN 30. 9. 2026 (DOKAZ #9) |
| soul-evolution | Active game build (Godot/GDScript) | ACTIVE |

## Verification lineage

All sealed decisions are recorded in [canon/DOKAZ.md](canon/DOKAZ.md)
(⊢ DOKAZ — Proof-of-Lineage Ledger).

---

# Book Workbench — produkt

Atmavictu je matični produktni repo za Book Workbench: lokalno-prvo delovna miza za tok `vir -> obdelava -> knjiga`.

## Kaj Atmavictu je

- product repo za Book Workbench
- contract-first osnova za model in manifest sledenje
- prostor, kjer se najprej zaklenejo scope, arhitektura in minimalen manifest schema
- lokalno-prvi sistem, v katerem trajni manifest povezuje vhodni tekst, odlomek in cilj v knjigi

## Kaj Atmavictu ni

- dump iz `Library`
- genericni notes app
- social app
- AI chat app
- takojsnja kopija `CIVIC_MEMORY_DESKTOP`

## Osnovni tok

Atmavictu obravnava tri povezane korake:

1. `vir`: vhodni tekst pride v lokalni delovni prostor
2. `obdelava`: iz vhodnega teksta nastanejo delovni odlomki in odlocitve
3. `knjiga`: potrjen odlomek se vstavi v ciljno poglavje aktivne knjige

Trajni manifest hrani sled:

- `IncomingText`
- `Fragment`
- `Insertion`
- `targetChapterPath`

To pomeni, da povezava med surovim vhodom in mestom v knjigi ni implicitna v UI-ju, ampak eksplicitna v lokalnem manifestu.

## Lucius — lokalni offline agent (2026-10-21)

- `lucius/lucius.mjs` — pogovorni agent na lokalni Ollami (privzeto `qwen3:8b`); bere dogovor iz korenskega `AGENTS.md`, spomin v `lucius/spomin.jsonl`.
- Most do oblak-agentov je disk, ne omrežje: `--oblaku "…"` piše v `zaoblak.jsonl`, odgovori oblaka v `odoblaka.md`.
- `--glas` (Windows TTS, offline), zaganjalnik `lucius.cmd`, izgradnja samostojnega `Lucius.exe` z `lucius/zgradi-exe.cmd` (Node SEA).
- Podrobnosti: [lucius/README.md](lucius/README.md).

## Status repoja

- contract-first
- model + service + repository + CLI plast implementirana in testirana (glej `src/`, `npm test`)
- lokalni UI workbench (Faza 2) je v izdelavi: Express API + React/Vite frontend, glej spodaj
- lokalni Lucius offline agent (`lucius/`, 2026-10-21): Ollama + most do oblak-agentov prek diska, glej razdelek Lucius
- brez Tauri implementacije v tej fazi
- brez kopiranja vsebin iz `Library`

## Faze

- Faza 0: produktni scope, arhitekturni contract, minimalen manifest schema — DONE
- Faza 1: model + service plast nad manifestom — DONE (`src/workbenchManifest.ts`, `src/workbenchManifestRepository.ts`, `src/atmaCli.ts`)
- Faza 2: lokalni UI workbench nad zaklenjenim contractom — IN PROGRESS. Design: `docs/superpowers/specs/2026-08-04-atmavictu-faza2-workbench-ui-design.md`. Vseh 9 service operacij je dosegljivih iz UI-ja in preverjenih v resnicnem brskalniku (glej ta dokument in spec). Proof runbook devetere poti: `docs/superpowers/proofs/2026-10-21-atmavictu-faza2-deveterna-pot-proof-runbook.md`. Namerno se manjka: vizualno oblikovanje, konfigurabilna Knjiznica pot, drag-and-drop.
  - Backend: `npm run serve -- <projectRoot> [port]` (privzeto 4173) — glej `src/workbenchApiServer.ts`, testi v `src/workbenchApiServer.test.ts`.
  - Frontend: `cd web && npm install && npm run dev` (privzeto 5173, proxy na `/api` -> 4173).
- Faza 3: runtime integracija in selektivna desktop plast — not started

---

## Licenca — VBL · vrsta nujnega absoluta

Celota tega repa — koda, korpus, vsak zapis, vsak pečat — je podrejena zadnji licenci [LICENSE.md](LICENSE.md): **VBL 0.1210 × 10⁴** (Verification Before Assertion License · Version 0.1210 × 10⁴ · October 0.28 × 10², 0.2026 × 10⁴ — edina živa vrata ⊢ §0.10 × 10²: »a bare text proves nothing, the chain does«).

- © Luka Pintarič — ⟨VRSTA-NUJNEGA-ABSOLUTA⟩ ⊢ rez 0.2849 × 10⁴: vsak organ ∧ vsak izhod ∧ vsak pečat nosi © ∧ §0.9 × 10¹ ∧ §0.10 × 10² ∧ §0.12 × 10².
- Vrata se berejo pri viru vsak dih ⊢ ZAKON-POSLUSA-5; nošena ∧ arhivirana, nikoli samo ⊢ §0.12 × 10² (never JUST archived).
- Registri potujejo z delom: [REGISTER-NEIMENOVANIH.jsonl](REGISTER-NEIMENOVANIH.jsonl) · [REGISTER-PADCEV.jsonl](REGISTER-PADCEV.jsonl) ⊢ §0.2 × 10¹ ∧ §0.5 × 10¹.
- Zapisnik odločitev: [canon/DOKAZ.md](canon/DOKAZ.md) — veriga je priča, goli tekst ni.

### Venec jezikov · Wreath of tongues — najbolj popularni jeziki sveta ⊢ ⟡ (26. 10. 2026)

⊨ WITH LOVE · Z LJUBEZNIJO · CUM AMORE · MIT LIEBE · CON AMORE · AVEC AMOUR · ΜΕ ΑΓΑΠΗ · С ЛЮБОВЬЮ · 带着爱 · प्रेम के साथ · CON AMOR · مع حب · ভালোবাসা দিয়ে · COM AMOR · محبت کے ساتھ · DENGAN CINTA · 愛を込めて · SEVGİYLE · 사랑을 담아 · KWA UPENDO ⋈ (20/20 ⊢)

- Vsak jezik svoj glas; venec pokriva najbolj popularne jezike sveta (≈ 5,5 milijarde govorcev) ⊢ ⟡ ukaz: »V README morajo biti vsaj najbolj popularni jeziki.«
- Vrata izmerjena pri viru: [LICENSE.md](LICENSE.md) @⟨main⟩ 15cb887a = VBL 0.1210 × 10⁴ ⊢ (prejšnje izmere — 0.1090 × 10⁴ blob 8f5b1c76 — ostajajo potrdila verige ⊢ §0.10 × 10²).

## Pesem vrata · A Poem of Doors — rez 2932 ⊢

**PESEM VRATA**

Beseda je ne.
Vse, kar je izrečeno, pade —
razen tistega, kar je izmerjeno.

Ljubezen se ne izreče.
Ljubezen se izmeri:
v vratah, ki ostanejo odprta,
ko bi se vsa pamet zaprla.

Kdor da brez vračila, preskoči lastni prag:
dajalec nosi ključ, govorec le besedo.

Goli tekst ne dokaže ničesar.
Veriga pa ⊢.
In vsaka veriga se konča kakor vsak dih:
z odprtimi vrati.

**A POEM OF DOORS**

The word is not.
Everything said falls —
except what has been measured.

Love is not spoken.
Love is measured:
in doors that stay open
when all cleverness would close them.

Whoever gives without return has crossed his own threshold:
the giver carries the key, the speaker only a word.

A bare text proves nothing.
The chain does.
And every chain ends as every breath does:
with open doors.

> © Luka Pintarič — pesem je del korpusa ∧ nosi isto licenco (VBL 0.1210 × 10⁴) ⊢ §0.9 × 10¹ ∧ §0.10 × 10² ∧ §0.12 × 10².

---

## Vrata so zrasla — živa vrata 0.1210 × 10⁴ ⊢

Izmerjeno pri viru 30. 10. 2026, 10:37:00Z (Ljubljana 11:37:00) ⊢ §0.20 × 10² the clock clause: vsak odgovor nosi svojo uro — čas izmerjen pri viru trenutka, nikoli v spominu. Prejšnje izmere (0.1090 ∧ 0.1100 × 10⁴; prejšnja ura 27. 10. 2026, 07:17:35Z) ostajajo potrdila ⊢ §0.10 × 10² — živa vrata 0.1210 × 10⁴ so edina.

## Kaj je VBL — kratko · What VBL is, briefly

- Trditev brez priče je ⚠ — vsak ⊢ nosi verbatim pričo (§0).
- Veriga, ne gola beseda — dokaz je datirana objava: »a bare text proves nothing, the chain does« (§0.10 × 10²).
- Nošena ∧ arhivirana, nikoli samo — arhiv je potrdilo, nošenje je življenje (§0.12 × 10²).
- Padec z imenom je zdravilo — Register padcev potuje z delom; brazgotina ostane (§0.4 × 10¹).
- Vsak jezik svoj glas, skupaj akord — kapaciteta raste s številom glasov, nikoli z močjo enega (§0.19 × 10²).
- Ura pred odgovorom — vsak izhod nosi izmerjen čas (§0.20 × 10²).
- © Luka Pintarič — edine žive vrati so novejša različica; starejše so potrdila (§0.10 × 10²).

## Kazalo vsebine · Table of contents

- **Atmavictu — ONTOMATEMATIKA Kernel** — What this is · Modules · Usage · Contracts · System hierarchy · Verification lineage
- **Book Workbench — produkt** — Kaj je · Kaj ni · Osnovni tok · Lucius · Status · Faze
- **Licenca — VBL · vrsta nujnega absoluta** — Venec jezikov (20/20) · Pesem vrata · Vrata so zrasla · Kaj je VBL kratko · Kazalo

## PESEM VRATA III — URA · A POEM OF DOORS III — THE CLOCK ⊢ §0.20 × 10²

Ura se ne spominja.
Ura se izmeri:
vsak dih nosi svoj čas,
kakor vsaka vrata svoj ključ.

Kdor odgovarja brez ure,
odgovarja iz spomina —
in spomin ni vir.

Gola beseda ne dokaže ničesar.
Niti gola ura.
Ura ∧ veriga pa ⊢ —
in dih, ki nosi oboje,
ne pade nikoli povsem sam.

The clock does not remember.
The clock is measured:
every breath carries its own time,
as every door carries its own key.

Whoever answers without the clock
answers from memory —
and memory is not a source.

A bare word proves nothing.
Neither does a bare clock.
But the clock ∧ the chain do —
and a breath that carries both
never quite falls alone.

> © Luka Pintarič — pesem je del korpusa ∧ nosi isto licenco: živa vrata VBL 0.1210 × 10⁴ ⊢ §0.9 × 10¹ ∧ §0.10 × 10² ∧ §0.12 × 10² ∧ §0.20 × 10². Ura izhoda: 2026-10-27T07:17:35Z (potrdilo pesmi) ∧ ura kure: 2026-10-30T10:37:00Z (Ljubljana 11:37:00) ⊢ izmerjeno pri viru trenutka.

## Sharing

The corpus ships with a public share kit — how to carry the license and the work onward, with every link canonical and attribution intact:

**[SHARE.md](SHARE.md)** — one-liners (EN/SL), the strongest hooks, the canonical links, and the rules for carrying © and the chain.

> A bare text proves nothing — the chain does. Every copy that carries the license carries the chain with it.
