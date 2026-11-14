# VBL 0.1530 — evidenčni pregled in neodvisni auditni načrt

**Datum pregleda:** 13. november 2026  
**Repozitorij:** `AtmaOVictu/SYMBOLON-KATHOLIKON`  
**Predmet:** `LICENSE.md`  
**Status ugotovitve:** javna objava na stranski veji je potrjena; objava na `main` ni potrjena.

## 1. Stanje virov

| Element | Ugotovitev | Status |
|---|---|---|
| Privzeta veja | `main` | potrjeno |
| `main` head | `202a1bb7dcaf39f2fb3dcde56467444595a1796f` | potrjeno |
| `main` LICENSE blob | `316c38cb62459c653f9d3088322c5d8ecb599b25` | potrjeno |
| `main` label | VBL 0.1490 × 10⁴ | potrjeno |
| Razvojna veja | `rez/4893-vrata-01530-sync` | potrjeno |
| Veja head / commit | `704a29ea7226b74915d67e785d89b48a6f944da0` | potrjeno |
| Veja LICENSE blob | `2ef143402241ae4e5d3d78e655649035a48df1d3` | potrjeno |
| Veja label | VBL 0.1530 × 10⁴ | potrjeno |
| Razlika do `main` | 1 komit naprej, 0 zaostankov; samo `LICENSE.md` v primerjavi | potrjeno |
| GitHub release | seznam izdaj vrnil prazen seznam | potrjeno za pregledani endpoint |
| GitHub tags | pregled ni bil uspešno zaključen | nepreverjeno |
| Podpis komita 0.1530 | `verified: false`, razlog `unsigned` | potrjeno |
| Neodvisna pravna presoja | ni bila opravljena | NOT_RUN |
| Neodvisni tehnični audit | ni bil opravljen | NOT_RUN |
| Notariziran časovni žig | ni bil potrjen | UNVERIFIED |

## 2. Vsebinski diff 0.1490 → 0.1530

GitHub compare poroča o eni spremenjeni datoteki `LICENSE.md`, 95 dodanih in 27 odstranjenih vrsticah.

Vidne spremembe v diffu vključujejo:

1. različico in začetni pečat preusmeri iz 0.1490 na 0.1530;
2. doda §0.52 o pravu, ki naj se uporabi, in §0.53 o triadi trditev–priča–čas;
3. razširi definiciji `pravoslovje` in `zlovje`;
4. §0.29 spremeni iz trditve, da pošiljanje poteka samodejno, v obveznost pošiljanja, ki ni izpolnjena zgolj z besedilno izjavo;
5. razčleni del prej združenega zemljevida določb §0.46–§0.53.

## 3. Kritično odprto neskladje časovnih pečatov

Besedilo `LICENSE.md` na veji 0.1530 navaja `ENTRY SEAL` ob `2026-11-13 23:26:00Z` in `EXIT SEAL` ob `2026-11-13 23:27:00Z`. GitHubov komit, ki objavi ta blob, pa je označen z `2026-11-13T21:05:24Z`. Vsi trije časi so označeni kot UTC. Vstopni pečat je torej 2 uri, 20 minut in 36 sekund PO času komita; izstopni pečat je 2 uri, 21 minut in 36 sekund PO času komita. Ob času tega pregleda je bil tudi vstopni pečat še v prihodnosti glede na razpoložljivo lokalno uro.

To je časovno neskladje, ki ga ni dovoljeno popraviti z ugibanjem. Možne razlage (napačno zapisan čas, napačen vir ure, predvideni namesto dejanskega pečata ali druga semantika) niso dokazane. Potrebni so izvirni zapisi obeh ur, dokaz o izvoru ure in pojasnilo, kaj ENTRY/EXIT SEAL pomenita v primerjavi s časom komita.

- `claim_status`: `SUPPORTED` — GitHub navaja komitni čas 21:05:24Z; besedilo licence navaja 23:26:00Z in 23:27:00Z.
- `claim_status`: `UNKNOWN` — kateri od časov predstavlja dejanski čas nastanka, pečatenja ali objave v smislu klavzul 0.20, 0.28 in 0.30.
- `test_result`: `FAIL` za preprost kronološki test `ENTRY_SEAL ≤ publication_commit ≤ EXIT_SEAL`; dejanske semantike pečatov še niso pojasnjene.
- `decision`: `HOLD` za časovno potrjeno izdajo, dokler vir in pomen časov nista pojasnjena.

## 4. Pomembna omejitev stanja

VBL 0.1530 je najnovejša najdena različica `LICENSE.md` v pregledanem repozitoriju, vendar ni na privzeti veji `main`. Zato je ne smemo opisati kot trenutno glavno izdajo ali kot podpisano izdajo. Njen komit je nepodpisan. Različica 0.1490 ostaja v `main`.

## 5. Predlagana klasifikacija VBL stanja

- `claim_status`: `SUPPORTED` za trditev, da je besedilo 0.1530 javno dostopno na imenovani veji.
- `claim_status`: `CONTRADICTED` za trditev, da je 0.1530 že na `main`.
- `claim_status`: `UNKNOWN` za trditev, da je 0.1530 pravno izvršljiva v vseh predvidenih primerih.
- `test_result`: `PARTIAL` — pregled veje, datoteke in primerjave je opravljen; oznake, vsi spremljevalni artefakti in neodvisni pregledi niso dokončani.
- `decision`: `HOLD` za razglasitev 0.1530 kot glavne ali pravno potrjene izdaje.

## 6. Tveganja, ki zahtevajo pregled

### 5.1 Doseg licence

Vsaka določba, ki poskuša zajeti neodvisno delo, ideje, dejstva, metode, zasebne podatke ali neodvisno notranje delovanje modela, potrebuje posebej omejen pravni temelj. Zgolj deklaracija v licenci ne ustvari pravic, ki jih imetnik nima.

### 5.2 Skriti procesi modelov

Zahteva po merljivosti procesa ne sme trditi, da je zasebno notranje sklepanje pregledano, kadar je nedostopno. Zunanja sled uporabe je lahko preverljiva; notranji proces je lahko `UNVERIFIED`.

### 5.3 Zasebnost in nespremenljivi registri

Ne objavljati osebnih podatkov ali identifikatorjev v javnem nespremenljivem registru samo zato, da bi dosegli trajnost dokaza. Potrebni so minimizacija, rok hrambe in način popravka/anonimizacije.

### 5.4 Pravno področje

§0.52 navaja pravo kraja, kjer avtor podpiše. To je preširoko, če ni jasno določen podpisnik, trenutek, kolizijska pravila, področje uporabe in obvezne določbe. Klavzula o pravu ne more izključiti kogentnih predpisov ali pravic tretjih oseb.

## 7. Zunanji pravni referenčni viri (orientacijski, ne pravno mnenje)

- Evropska komisija, AI Act Service Desk — časovnica uporabe AI Act, pregledano 13. 11. 2026: https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline
- Evropska komisija, Navigating the AI Act FAQ: https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act
- GOV.SI, avtorske in sorodne pravice ter povezava do neuradnega prečiščenega besedila ZASP: https://www.gov.si/en/topics/copyright-and-related-rights/
- Direktiva (EU) 2019/790, člena 3 in 4 — raziskovalni TDM in splošna TDM izjema s pridržkom pravic: https://eur-lex.europa.eu/legal-content/SL-EN/TXT/?uri=CELEX%3A32019L0790
- EDPB Guidelines 02/2025 on processing of personal data through blockchain technologies: https://www.edpb.europa.eu/documents/guideline/guidelines-022025-on-processing-of-personal-data-through-blockchain_en

## 8. Dodatna pravna ugotovitev: TDM pridržek

Člen 4(3) Direktive (EU) 2019/790 veže splošno izjemo za besedilno in podatkovno rudarjenje na to, da imetnik pravic uporabe ni izrecno pridržal na ustrezen način; za javno dostopno spletno vsebino je izrecno naveden primer strojno berljivih sredstev. Člen 4(4) ohranja uporabo člena 3, ki ureja raziskovalni TDM. VBL zato potrebuje strojno berljiv, verzioniran in preverljiv zapis pridržka, vendar ne sme obljubljati, da tak zapis izključi vse izjeme ali vse vrste TDM.

## 9. Naslednji neodvisni pregledi

1. `LEGAL`: obseg avtorskih pravic, pogodbeno sprejetje, TDM rezervacije in izjeme, izbira prava, izvršljivost, sorazmernost pravnih sredstev.
2. `TECHNICAL`: manifest, strojno berljiva identifikacija, hash, podpis, časovna oznaka, različice, ponovljivost in interoperabilnost.
3. `PRIVACY`: podatkovna minimizacija, osebni podatki, hramba, ugovor, izbris in popravek.
4. `ETHICAL`: vpliv na avtorje, uporabnike, prizadete osebe in neenakost dokaznega bremena.
5. `ADVERSARIAL`: napačna klasifikacija, lažna zavrnitev, skrita uporaba, zavajajoč zapis in zloraba registra.

**Zaključek:** najnovejši najdeni kandidat je VBL 0.1530 na stranski veji. Njegovega statusa ne smemo napihniti. Priporočena odločitev za uradno razglasitev: `HOLD` do združitve ali drugega dokazljivega akta objave in neodvisnih pregledov.
