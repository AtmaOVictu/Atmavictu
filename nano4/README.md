# nano4 — paket VBL 0.1470 (DRAFT_NOT_RELEASED)

Ovojnica osnutka za naslednji izpust VBL. Ni distribucijski paket ∧ ni
izpust: je pripravljalna miza, ki čaka. Žive vrata licence so medtem
pri 0.1520 ∧ ta razlika je pošteno izmerjena stanje, ⟨ne⟩ napaka.

## Kaj je tukaj

**Orodja**
- `validate_package.py` — lokalna preverjevalna vrata: obvezna telesa,
  invariante mašinskega zapisa, resnica verzij, registri, kandidatska
  vrata, žigi popravkov. `--json` = strukturirano, deterministično
  poročilo (vhodi + sha256, izmerjeni rezultati); izhod 1 samo ob FAIL.
- `renumeriraj.py` — pomožno preštevilčenje.
- `tests/` — regresija (spodaj).

**Zapisi**
- `LICENSE-MACHINE-RECORD-0.1470.json` — mašinski zapis paketa:
  version `0.1470 × 10⁴`, `release_status: DRAFT_NOT_RELEASED`,
  `canonical_status: UNVERIFIED`, `predecessor.identity_conflict: true`,
  `mail_delivery.delivered: false`. Padec je del zapisa.
- `PACKAGE-MANIFEST.json` — re-issued register VSEH realnih teles
  paketa z izmerjenimi sha256 (sebe ne seže — §0a).
- `VERSION.txt` — kazalec resnice verzij: `living_door = ../LICENSE-MANIFEST`,
  era paketa, status. Številka živih vrat NIKOLI zapečena tukaj.
- `candidate/` — edini dom izpustnih vhodov (glej `candidate/README.md`).
- `TEST-RESULTS*.txt` ×4 — priče ⟨POSNETEK ≠ KORPUS⟩: nedotaknjene.

**Snovi**
- `00-AUDIT.md` … `04-LEGAL-RESEARCH-NOTES.md`, `RELEASE-GATE.md`,
  `01-architecture-and-license-selection.md`, `02-proposed-clause-text.md`,
  `CROSS-REFERENCE-AUDIT.md`, `HISTORICAL-SOURCE-VERIFICATION.md`,
  `VBL-0.1470-*.md`, `simbolna-licenca-*.md`, `spdx-zahtevek-*.md`,
  `LICENSE.map-repaired.candidate.md`, `final-qa-*.md`,
  `github-main-provenance-*.md`, `validation-2026-11-05.md`,
  `requirements-test.txt`.

## Štirje nosilci verzij

0.1450 telo → 0.1460 pečat → 0.1470 paket (ta mapa) → 0.1520 živa vrata
(`../LICENSE-MANIFEST` na korenu repa). Ena hierarhija, štiri resnice;
`VERSION.txt` kaže na živa vrata, preverjevalnik jih izmeri ob teku.

## Kaj ta vrata NIKOLI ne morejo potrditi

Preverjevalnik meri strukturo ∧ hashe ⟨ne⟩ ljudi. Pošten seznam
`not_certified` je v vsakem poročilu: pravna veljavnost · izdaja ∧
dostava · kanonski status · neodvisen pregled · istost recenzenta.
Človeško odobritev mora izreči človek zunaj tega orodja ∧ poročilo
pošteno loči, kaj je izmerjeno od, česar ni.

## Testi

    python3 -m unittest discover -s nano4/tests -v

Regresija: format izpusta ∧ zgodovina verzij, ujemajoča ∧ nasprotujoča
metapodatka, zastareli hashi, nevarne poti, nepopolni dokazi pregleda,
pokvarjeni registri, kandidatska vrata (sirote, praznina, malformacija).

## Release proces

1. sestavi kandidatko v `candidate/` z lastnim registrom;
2. `validate_package.py --json` — FAIL zapre, PASS odkrije naprej;
3. človeški pregled ∧ odobritev ZUNANJ orodja (priča, ⟨ne⟩ izhod);
4. prevoz skozi verigo (PR + CI) ∧ ⟨merge⟩ ⟡ roka;
5. po izpustu: mašinski zapis dobi nov status ∧ poročilo se prilepi
   kot priča.

## Brazgotina ⟨PADC-MANIFEST-FANTOMI⟩

Stari manifest je pričeval za devet teles, ki nikoli niso pristala v
verigi (schemas/*, source/*, tests/*). Preverjevalnik nad živo verigo
je padel FAIL — ∧ to je DOKAZ, da so vrata fail-closed: fantom ne
preživi preverjanja. Fantomske poti ostajajo zapisane v
`phantom_entries_of_the_fall`, da padec ostane priča, ⟨ne⟩ spomin.
