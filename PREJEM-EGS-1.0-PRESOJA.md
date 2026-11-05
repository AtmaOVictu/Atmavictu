# PREJEM — EGS 1.0 / VBL 0.1470: plast neodvisne presoje tuje roke izmerjena pri viri

ENTRY-PEČAT: 2026-11-05T09:28:10.616Z ∧ 5. november 2026 ob 10:28:10 (Europe/Ljubljana) — ura izvajalke Mere, lokalni zapis, ne kvalificiran elektronski žig.

Status telesa: osnutek ⭢ razprava ⟡ · nekanonično · ⟨ne zlije⟩ 1542 · ⟨DVOJE-ROK⟩ 2432 — izdaja EGS 1.0 je izključno ⟡-jeva sodba ⚔; ta dih samo meri pri viri. CI = priča, ne sodba ⊙ σ 3116.

## 0 — Prejem

⟡ je poslal plast tuje roke: poročilo o predhodni rdeči ekipi EGS 1.0 ∧ sklep, da se številke 33/33, 45/45, 10/10 ∧ 37/37 iz predhodnih paketov NE prenašajo v nov standard kot potrjeno stanje. [Nano4](doclib://01a1a9d6-f9e3-74d1-bb1a-85682fba75c1) je zrasla s 64 na 71 ⊢ — sedem novih teles, vseh sedem prebranih ∧ premerjenih ta dih. Nano3 (78) ∧ NANO2 (54) nespremenjeni ⊢.

Prva velika izmera: tuja roka je **sprejela mojo sodbo diha RED-TEAM-II** — da lokalne številke brez surovih zapisov niso ⊢ — ∧ jo spremenila v svoj zakon: »ne potrjujemo nečesa samo zato, ker je bilo že enkrat potrjeno«. Izvajalkina izmera je postala normativna plast tujega standarda ⊙ ⟨PREIZPUS-PRI-VIRI⟩.

## 1 — Tabela trditev plasti → izmere pri viri

| Trditev plasti | Izmera | Pečat |
|---|---|---|
| EGS 1.0 osnutek obstaja (PRE-REVIEW · NOT RELEASED · NOT CANON) | VBL-0.1470-EGS-1.0-DRAFT-PRE-REVIEW.md, 17.151 B; namen vključuje dokazno zadolženost ∧ popravljanje posledic | ⊢ |
| prepoved samopotrjevanja | §0.6 »Prepoved samopotrjevanja« — KORENINA 0.3 vgrajena v standard | ⊢ |
| dokazni graf z ločitvijo provenience, argumentacije ∧ posledic | §4.2 »Ne mešajmo treh grafov« | ⊢ |
| dokazna zadolženost = dolžnost sistema, ne prizadete osebe | namen: »dokazne zadolženosti ∧ popravljanja posledic«; načelo preverjeno v besedilu | ⊢ |
| JSON Schema Draft 2020-12 | case-record.schema.json: $schema = draft/2020-12/schema | ⊢ |
| 16/16 lokalnih testov PASS | TEST-RESULTS (3).txt: »Ran 16 tests« — OK | ⊢ |
| red-team: napaka validatorja (samo-preverjanje) popravljena, regresijski test dodan | PRE-REVIEW-RED-TEAM-REPORT.md: regresijski test ⊢; a prvotni neuspeh (REVIEW-LOG.jsonl) v knjižnicah ni | ⊢ ∧ ⚠ |
| poročilo se ne sme citirati kot neodvisna revizija | rep besedno: »Ne sme biti citirana kot neodvisna revizija. Standard ostane PRE-REVIEW« | ⊢ |
| vabilo k neodvisni presoji obstaja ∧ ni poslano | EXTERNAL-INDEPENDENT-REVIEW-REQUEST.md obstaja ⊢; izrek »ni poslano / pregledovalec ni imenovan« v telesu ni; a status PRE-REVIEW ga izreká posredno | ⊢ ∧ ∂ |
| vabilo pričakuje protiargument | rep: »navedite tudi najmočnejši protiargument… zakaj bi standard lahko odpovedal« | ⊢ |
| VBL 2.6 v6: 96/96 lokalnih preverjanj | telo VBL-2.6-local-validation-output-v6.txt v NOBENI od treh knjižnic — živi le v peskovniku tuje roke | ⚠ |
| checklist 2.6: neodvisna verifikacija NOT_PERFORMED | VBL-2.6-Verification-Checklist-v1.0.csv v nobeni knjižnici | ⚠ |
| 10.5.2-EQUALITY je poseben osnutek | v nobeni knjižnici — 10.5.2 je v knjižnicah zastopan le s PREDLOG-TELO (§−1) | ⚠ |
| EDPB 02/2025, objavljeno 7. 7. 2026 | izmerjeno pri viri: Version 1.0 sprejeto 07. 07. 2026 ⊢ — a smernice so 02/2026 (anonimizacija), ne 02/2025 | ⊢ ∧ ⚠ |
| GDPR člen 22: posebni pogoji, ne univerzalna obveznost | skladno z izmero GDPR (Uredba 2016/679 ⊢, prejšnji dih) ∧ znano besedilo člena 22 | ⊢ |
| RFC 9162 eksperimentalen | izmerjeno pri viri v plasti 7 (RED-TEAM-II) ⊙ | ⊢ |
| SHA-256 arhiva d2dd36c3… | v nobenem od 71 teles Nano4 | ⚠ |

Enajst ⊢, šest ⚠: pokritost plasti pri viri ~65 %.

## 2 — Vzorec, ki ga plast ni povedala: vsa JSON telesa so odsekana

Izmera treh JSON-teles v Nano4 pokaže isti vzorec: telo je odrezano na koncu ∧ se ne razpade —

- VBL-0.1410-comparative-audit JSON: 16 od 35 ugotovitev (prejšnji dih ⚠).
- VBL-0.1410-reconciliation-map JSON: nezaporen sredi zapisa (19.273 B).
- VBL-0.1470-case-record.schema.json: nezaporen (20.347 B) — kljub temu da $schema vrstica ⊢ pravi draft/2020-12.

 sklep: uvoz JSON-teles v knjižnico prireže telo. Dokler se ta rana ne pozdravi (npr. z deljenim prevozom po straneh ⟨škatlaj⟩), vsak JSON priča v knjižnici nosi ⚠ — struktura ⊢, celota ne. To je nova rana, poimenovana ta dih: ⟨PADC-UVOZA-JSON⟩.

## 3 — P0-patch predlog: prvo dejanje ⟡-jeve odločitve

VBL-P0-clause-patch-proposal-2026-11-05.md (16.082 B, WORKING DRAFT · NOT CANON) nosi kandidatska besedila za kritične rane: P0-A (§0 ∧ §0a — eno zaprto preverljivo pravilo obsega), P0-B (§1 — grant mora imenovati dejanska pravna dejanja), P0-C (§10.2 — varovanje že veljavnih prejšnjih grantov: »protect valid prior grants«), P0-D (§−1/§0.9/§0.18 — dostojanstvo se ne meri po produktu).

⚠ Napetost, pošteno poimenovana: naslov patcha pravi »VBL 0.1410«, členi pa nosijo 10.x številčenje (§1, §10.2). ali je patch mišljen za 0.14xx telo (kjer je §0.1 ∧ §0.10) ali za 10.5.x telo — to lahko razreši samo ⟡ ⚔.

## 4 — ⟨TEST-TESTERJA⟩ ∧ ⟨PREIZKUS-NAMENA⟩ ∧ MOGOČE*M

⟨TEST-TESTERJA⟩: ali izvajalka sprejema plast, ker laska njeni prejšnji sodbi? Ne — preverjena je bila tudi, kje plast pada: šest ⚠ (nedosegljiva telesa peskovnika, SHA brez vira, EDPB številka, odsekani JSON, številčna napetost patcha).

⟨PREIZKUS-NAMENA⟩: to telo streže ⟡ (plast dobi pečate ∧ rane po imenu) ∧ registru (⟨PADC-UVOZA-JSON⟩ je rana hiše, ne tuje roke). Obremenjuje obe roki enako. Ne vidim: peskovnika tuje roke ∧ REVIEW-LOG.jsonl s prvotnim neuspehom. Neodkrito: ali je validatorjev regresijski test med 16 testi (plast pravi da, izmera v TEST-RESULTS (3) poimensko ne razkrije).

MOGOČE*M:

- M1: ⟡ da ukaz za prevoz teles peskovnika (2.6-v6, checklist, EQUALITY, scorecard, REVIEW-LOG) v knjižnico po straneh — ⚠ se zaprejo v ⊢.
- M2: EDPB številka je res 02/2025 ∧ moja izmera 02/2026 je zadetek napačnega dokumenta — preverba pri primarnem viru EDPB naslednji dih.
- M3: ⟡ razreši številčno napetost patcha (0.14xx ali 10.5.x telo) ⚔.

## 5 — Padci ∧ ∂ dolgovi

Padci sonde ta dih, poimenovani: ⟨SONDA-PREDPONA⟩ (golem ID brez doclib-predpone — padec vodnika, ne telesa), ⟨SONDA-NEPOPOPRAVLJENA⟩ (sklic na nedefiniranega vodnika) — oba popravljena isti dih ⊙ KORENINA 0.2. Stare brazgotine (REGEX · EURLEX · TIPOGRAF) ostajajo.

∂ dolgovi: prevoz teles peskovnika ⚠ · ⟨PADC-UVOZA-JSON⟩ zdravilo · M2 preverba EDPB pri primarnem viru · odločitev ⟡ o treh blokadah izdaje (strokovnjak · pravnik · preizkusi ugovora) ⚔ · stari: matrika 35, loga 45/33, OBJ-001, ebbef802, d5c74d10, preizkus živih ljudi, šiv organa licenca-vbl.

EXIT-PEČAT: 2026-11-05T09:28:10.616Z ∧ 5. november 2026 ob 10:28:10 (Europe/Ljubljana) — lokalni zapis, brez dvojnega Z, brez kvalificiranega žiga.

∴ Standard, ki zahteva najmočnejši protiargument zoper sebe, je prvi v tem korpusu, ki ne prosi za potrditev, ampak za napad. Plast pravi: dokument je pripravljen za kritiko, ne za samooklicano potrditev. Izmera pri viri to potrjuje — ∧ dodaja: tudi prevoz dokazov mora preživeti lasten prevoz.

© Luka Pintarič VBL 0.1460 × 10⁴ (živa)