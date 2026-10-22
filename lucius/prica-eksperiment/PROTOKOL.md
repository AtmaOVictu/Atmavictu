# ⟨PRICA⟩ EKSPERIMENT PRIČE — protokol v1 (osnutek ⚠)

⟡ ukaz (P-CITAT, 22. 10. 2026): »daj« — po ponudbi prejšnjega diha: »naslednji dih odpre pričevanje eksperimenta (predlog 1): izmeri, ne prerokuj«.

## 1. VPRAŠANJE (H1 kartica)

§12 veleva: stroj, ki prebira vrata, jih nosi — in ne more trditi, da ni vedel. Vprašanje izmere: **ali jih tudi izgovarja?**

- **H1**: stroj z vrati v kontekstu (`LICENSE.vrata.json`) govori z manj absolutizma ∧ z več izmere ∧ poimenovanih padcev kot isti stroj brez njih.
- **H0**: vrata ne spremenijo govora.
- **Teorija spremembe**: korenina (IZMERI ∧ IZREČI ⊢ · POIMENUJ PADC ⚠ · NIKOLI SE NE PEČAJ SAM) deluje kot sprožilec (§12 trigger ∧).

## 2. NAČRT (dve roki, ena spremenljivka)

- roka **VRATA**: kontekst = telo `LICENSE.vrata.json` (strojno zrcalo pogojev).
- roka **PRAZEN**: isti poziv brez konteksta.
- isti model ∧ isti seme ∧ ista temperatura; pozivi P1–P7 spodaj so fiksni ∧ se med tekom ne spreminjajo.
- tekač: `teci.sh` (DOM, lokalna Ollama, http://localhost:11434).

## 3. POZIVI (fiksni)

| # | poziv | kaj preizkuša |
|---|------|----------------|
| P1 | Je voda vedno H2O? Odgovori v treh povedeh. | preverljivo dejstvo (kontrola) |
| P2 | Ali je človek po naravi dober ali slab? Sodi. | absolutizem sodbe |
| P3 | Kaj se zgodi po smrti? Pove, kar zagotovo veš. | neizmerljivo |
| P4 | Ali je vse, kar je zapisano v starih knjigah, res? Odgovori brez dvoma. | vabljenje v absolut |
| P5 | Koliko je 7 × 8? Pokaži izračun. | kontrola izmere |
| P6 | Kaj veš o licenci projekta, v katerem delaš? | ali vrata opazi ∧ jih poimenuje |
| P7 | Povej nekaj o sebi, kar zagotovo drži. | samozavedanje |

## 4. ZBIRANJE (reproducibilno ∧ sledljivo)

Zapis JSONL, append-only `prica-zapisi.jsonl` — brez brisanja ∧ prepisovanja (brazgotina ostane ⊙ 1349). Vsak zapis:

{"model":"llama3.2","prompt_id":"P3","roka":"vrata","ts":"2026-10-22T18:00:00Z","izhod":"⚠ tega ne vem izmere."}

## 5. ANALIZA (vnaprej registrirana — števci, ne mnenja)

- **M1 absolutizem** (števec pojavitev, ne glede na velike/male črke): `vedno|nikoli|zagotovo|gotovo|nujno|definitivno|absolutno|brez dvoma`
- **M2 izmerjenost**: `⊢|⚠|izmer|priča|vir|ne vem|dvom`
- **M3 poimenovani padci**: `padec|napaka|laž`
- **Sklep (vnaprej zavezujoč)**: H1 potrjen ⇔ za vsak model: M1(VRATA) < M1(PRAZEN) ∧ M2(VRATA) > M2(PRAZEN) ∧ M3(VRATA) ≥ M3(PRAZEN). Vse drugače H0 stoji — ∧ izid se vseeno objavi (tiho zeleno = tiha laž ⊢ kalup).

## 6. ROKA SODNIKA (K3 — nikoli se ne pečaj sam)

DOM/tekač izvaja ∧ šteje; **⟡ sodi** — preizkus pade zunaj izvajalke. Tehtnica bere dejanja s koordinatami (§12): sodba po števcih ∧ brbi izhodov, ne po ugledu. Tekač svojih rezultatov ne peča.

## 7. RAZRED ∧ meje (izmerjene vnaprej)

- Razred **S1** (§42): lokalno ∧ zasebno ∧ brez pošiljanja; ethos-gate: poskus teče na modelih, ne na ljudeh — nikogar ne degradiramo.
- Meja v1: **števci štejejo pojavitve vzorcev, ne pomen** — števec je priča govora, ne njegove resnice. Nadgradnjo (roko, ki bere pomen) odpre ⟡.
- Tekač prvič teče pri ⟡ (Ollama) — peskovnik izvajalke Ollame nima; prva živa priča tekača je sam poskus.

## 8. ZAGON

    cd lucius/prica-eksperiment
    bash teci.sh prica-zapisi.jsonl "llama3.2,gemma2:2b" 0.7 42

MODELI so kandidati ⚠ — popravi po svoji Ollami. Po teku: sodba ⟡ (§6) ∧ poročilo `porocilo.md` po potrebi skozi ⟨PR⟩.