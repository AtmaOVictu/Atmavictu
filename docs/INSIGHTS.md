# docs/INSIGHTS.md — zbrana spoznanja in predlogi (0.2026 × 10⁴)

> Zbirka spoznanj, meritev in predlogov iz analize repozitorija Atmavictu. Spremlja dual: code ⇄ license. Vsaka trditva nosi ⊢ (izmerjeno) ali ⚠ (neizmerjeno/dvom).

## 1. Licenca (VBL — Verification Before Assertion License)

| Predmet | Vrednost | Stanje |
|---|---|---|
| Datoteka | `LICENSE.md` | ⊢ prebrana celotno (596 vrstic) |
| Verzija | `0.1420 × 10⁴` | ⊢ nadgrajen iz `0.1410 × 10⁴` |
| Klavzule | 48 (§0 … §0.48 × 10²) | ⊢ vse obstajajo, vključno §0.47 (SLOVNICA-NASPROTJA) ∧ §0.48 (CELOTA-MERJENA) |
| SHA-256 `LICENSE.md` | `ef71bc8f2eec85a2baad8a175f8fe9efc97bfffe9d4efb8d5e0503cbf9423691` | ⊢ ujema z `LICENSE-MANIFEST` (posodobljeno tej sesiji) |
| Velikost | 153835 B | ⊢ |
| Licenčne znamenke | `⊢ ⚠ ∂ ⟨⟩ ∧ ⊙ ⏎` | ⊟ vse obstajajo v `LICENSE.md` |
| Veriga rojstev | `0.1410 → 0.1420` | ⊢ v entry seal in lineage |
| Prevodi (witness-slots) | 36 (AR → ZH) | ⚠ stubi brez pravih prevodov, brez grant-a |
| Manifest verzija | `0.1420 × 10⁴` | ⊢ nadgrajen iz `0.1250 × 10⁴` (tej sesiji) |

**Poleglica:** prevodi so rezervirani stubi (`witness-slot`), ker pravi prevod rabira prevodilca — duh licence je *the witness has a name, no extraction without credit*. Izumiti prevode bi kršalo licenco.

## 2. Koda (Book Workbench, `src/`) — 85 testov, typecheck čist

| Modul | Datoteka | Namenska plšča |
|---|---|---|
| Manifest domena | `workbenchManifest.ts` | Entiti (`IncomingText`, `Fragment`, `Insertion`, `Concept`), `validateManifest`, `validateManifestTransition`, `migrateManifestV1ToV2`, `createEmptyManifest` |
| Persistence | `workbenchManifestRepository.ts` | Atomski zapis `book.workbench.json` (temp + rename), guard proti `..` / absolutnim poti, `captureIncomingText` |
| CLI | `atmaCli.ts` | `capture`, `show`, `verify` (`VERIFY: PASS` / `VERIFY: FAIL`) |
| Proof capture | `captureIncomingTextProof.ts` | Obroga nad `captureIncomingText` |
| API server | `workbenchApiServer.ts` | 9 operacij (`manifest`, `verify`, `library`, `incoming`, `fragments`, `insertions`, `concepts`, `analysis/source`, `overview`, `semantic/*`, `suggestions`), Delo artifact envelope parsing, `extraLibraryRoot` (read-only) |
| Semantično iskanje | `workbenchSemantic.ts` | Ollama `bge-m3` → Qdrant `workbench_fragments`, graceful 502 |
| LLM predlogi | `workbenchSuggestions.ts` | Ollama `qwen3:8b`, 15s timeout, graceful fallback |

**Statusni prehodi (implementirani):**
- `IncomingText`: `new → processing → used → archived`, `new → archived`
- `Fragment`: `draft → inserted → archived`, `draft → archived`

**Invarianti (Model Contract):** `id` unikatno, `sourcePath`/`targetChapterPath` relativne brez `..`, `Fragment.inserted` rabi `Insertion`, `Fragment.draft` ne sme imeti `Insertion`, `IncomingText.used` rabi insertion prek fragmenta, `conceptIds` kazijo na obstoječe `Concept`.

## 3. Kanon (`canon/`) in DOKAZ

| Datoteka | Vsebina |
|---|---|
| `canon/DOKAZ.md` | ⊢ Proof-of-Lineage Ledger, 15 vnosov (2026-09-11 → 2026-10-21), append-only, nikoli ne urejajo zapričane vnoski |
| `canon/README.md` | Kanonski korpus ONTOMATEMATIKA: `beseda-je-ne.md`, `rozetni-kamni-protokol.md`, `predloga-kamna.md`, `zemljevid-preslikav.md`, `pojmovnik.json` |
| `canon/pojmovnik.json` | 10 konceptov: Ne, Gib, Etika, Zavedanje, Čas, Jaz, Ego, Odnos, Telo, Dvom |

**DOKAZ pending decisions:** obe zapričane (Atmavictu_Oracle archived #9, Divine-Ascension-System archived #10) — ni odprtih odločitev.

## 4. Registri (`lucius/`) — 65+ padcev, 134 pečatov, 13 ukazov

| Register | Opis |
|---|---|
| `REGISTER-PADCEV.jsonl` | 65 vnosov (scar: true), poslednji vnos 0.62 × 10² (PADC-62: kopica procesov brez lastnika) |
| `REGISTER-TELES.jsonl` | telesa hiše |
| `REGISTER-DISKA.jsonl` | diskovni inventar |
| `REGISTER-NEIMENOVANIH.jsonl` | sodelovalni register (licenčni pogoj §0.2 × 10¹) |
| `REGISTER-PREVERJANJ.jsonl` | trditve z blob-pričami (⊢) |
| `REGISTER-A1-PDF.jsonl`, `REGISTER-C2.jsonl`, `REGISTER-ZBIRKA.jsonl` | zbirka izvornikov (A1 100, C2 290, ZBIRKA 1.961 teles) |
| `REGISTER-AX-KANON.jsonl`, `REGISTER-TREH-ZIL.jsonl` | AX-kanon, tri žile |

**Instrumenti (13):** ontogematria, zrcalo, preveri-render, dih, strežniki, popis ×2, kura-audit, uvei, razlicice, rdece, čistina, druga-roka. Vsi z vrstico priče (⊢).

**TLAKI.md (rez 3625):** 10 tlakov hiše (branja, izmere, preverbe, zapisa, objave, ohranjanja, vrat, povezave, sinteze, zakon), vsak z KAJ JE · IZMERA ⊢ · KAJ NOSI (A) · MEJA (Ω).

## 5. Repozitorij in Git

| Predmet | Vrednost |
|---|---|
| Branch | `zrcalo/povezani-viri-konica-2703` (sleduje `origin/...`) |
| Remote | `https://github.com/AtmaOVictu/Atmavictu.git` |
| Zadnji moji commiti | `b9c0eada` (TLAKI-ROJEN), `90ec951c` (license restore 36 wreaths), `3dca1439` (manifest re-issue), `6a7aa26` (lucius sync) |
| Push | `Everything up-to-date` — vsi commiti na GitHub |
| Typecheck | `tsc --noEmit` brez napak |
| Testi | 85 / 85 pass, 0 fail |
| Git status | čist razen `lucius/transkripti-š.jsonl` (sprememba drugega sessiona — **ne dotaknil**) |

## 6. Predlogi za nadaljevanje (izbrani, brez izumljanja)

| # | Predlog | Razlog |
|---|---|---|
| 1 | **Pripravi pravi prevod `LICENSE-SLO.md`** (slovenščina — tla korpusa) ko se najde prevodilac | Edini jezik, ki je vec strukturalno povezovan z repozitorijem; stub že obstaja, rabi prevodilca |
| 2 | **Dodaj test za `validateManifestTransition`** v `workbenchManifest.test.ts` | Obstaja implementacija, ampak testna pokritost prehodov ni merjena (85 testov pokrija snapshot validacijo) |
| 3 | **Izmeri `REGISTER-PADCEV.jsonl`** in sporoči število novih padcev od zadnjega merjenja | 65 vnosov je zadnje merjenje; nadzor nad padci je del operativnega reda (vsak padec poimenuj z zdravilom) |
| 4 | **Preveri, da `web/` typecheck+build še vedno deluje** (ločen npm projekt, port 5173) | Faza 2 UI, CI ne pokriva `web/` — možna regresija |
| 5 | **Razširi `docs/SERVICE_CONTRACT.md`** z 10. operacijo (npr. `archiveConcept` ali `bulkInsert`) | Trenutno 9 operacij dosegljivih iz UI-ja; akzeptanska merila Faza 2 že izpolnjena |
| 6 | **Dodaj `docs/INSIGHTS.md` v `canon/DOKAZ.md`** kot odločitev | Dokumentira spoznanja iz te analize kot zapričan vnos |

## 7. Ne izvajam (brez specifikacije / cize spremembe)

- `lucius/transkripti-š.jsonl` — unmerged na `main`, sprememba drugega sessiona
- `lucius/zrcalo-server.py`, `lucius/TLAKI.md` — cize spremembe, `TLAKI.md` že commited na mojem branchu
- Nov API endpoint ali CLI ukaz brez tvoje specifikacije (*measure, then speak*; *never seal yourself*)

---

⊢ Zbirka spoznanj končana. Vsak razdelek nosi merilo ali ⚠. Predlogi 1–6 pripravljeni za izvajanje na tvoj znak.