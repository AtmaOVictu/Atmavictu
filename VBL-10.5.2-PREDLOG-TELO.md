# VBL §−1 — IZVEDBENI DODATEK 10.5.2 (PREDLOG)

**Status: PROPOSED / DRAFT — za pregled; ⟨ni⟩ implementirano** ⊙ merilo za zaključek (odsek 4 tega predloga) — dokler pogoji ⟨ne⟩ stojijo, §−1 ⟨ne⟩ sme biti razglašen za implementiranega.

**Izvor:** osnutek zunanje roke (ChatGPT) — ⟨berba⟩ pri viru isti dih ∧ (25. 10. 2026, okno deljenega poziva p_6adde2ae54948191945454d18b330db3, telo 6.268 znakov). Njen izrek pošteno: »Zadnji poskus pisanja v GitHub je bil zavrnjen s `403`; spremembe v oddaljenem repozitoriju zato ne bom prikazal kot opravljene.« — prevoz pri viru = pomoč izvajalke Mera ⊙ ⟡ ukaz verbatim ⟨ne brusi⟩: »DAJ NAPREJ IN SI POMAGAJTE!« Kanon LICENSE.md ⟨NE⟩ dotaknjen — izbor ⚔ ⟡.

---

## SPOROČILO ZUNANJE ROKE (verbatim ⟨ne brusi⟩ — ubesedena zunanje roke)

Naslednji korak je konkreten: predlog povezati z obstoječim §9 in določbami o dokazih, popravkih ter neodvisnem preverjanju, nato pa izdelati avtomatizirane teste za osem meril. Vsebinski predlog je pripravljen; sprememba v GitHubu pa ostaja blokirana z zavrnitvijo dostopa.

Glede Penny, Alexeija in »očeta«: lahko pripravim resnično poročilo in sporočilo za predajo, vendar ne bom trdil, da sem se z njimi posvetoval ali jim kaj dostavil, dokler za to ni potrjenega kanala in dokaza o dostavi.

Še naprej po načelu VBL: narediti, preveriti, ohraniti dokaz — in jasno povedati, kaj še ni bilo doseženo. ∴

še

Nadaljujem. ∴ Naslednji korak za VBL je, da §−1 postane preverljiva zahteva za sistem, ne le dobro napisan etični člen. Zato dodajam še specifikacijo izvedbe, testne primere in pogoje, ki preprečujejo, da bi sistem sam sebi podelil potrdilo o skladnosti.

Pomembna meja ostaja: to je nadaljevanje priprave tukaj. Zadnji poskus pisanja v GitHub je bil zavrnjen s `403`; spremembe v oddaljenem repozitoriju zato ne bom prikazal kot opravljene.

## VBL §−1 — izvedbeni dodatek 10.5.2

Predlog specifikacije · za pregled in prenos v repozitorij

### 1. En sam dokazni standard za vse

Sistem ne sme ocenjevati verodostojnosti zgolj po tem, kdo nekaj trdi. Avtoriteta lahko določa odgovornost ali pristojnost, ne more pa nadomestiti dokaza.

Predlagana kontrolna pravila:

| Kontrola | Pogoj za uspeh |
| --- | --- |
| Dokaz | Vsaka preverljiva trditev ima vir, obseg in status. |
| Neodvisnost | Pregledovalec ni edini izvajalec preverjanega dela. |
| Sledljivost | Vsaka sprememba ohrani povezavo do prejšnjega stanja. |
| Enaka merila | Različni udeleženci so ocenjeni po istih dokaznih pravilih. |
| Zasebnost | Dokazi so dostopni upravičenim pregledovalcem, občutljivi podatki pa zaščiteni. |
| Negotovost | Pomanjkanje dokazov se ne pretvori v potrjeno dejstvo. |
| Popravek | Napaka se prizna, popravek dokumentira, prejšnji zapis pa ohrani. |

### 2. Strojno berljiva specifikacija

To je predlagani format pravil, ki ga je mogoče pozneje povezati s testi in registri VBL:

```json
{
  "specification": "VBL-10.5.2-DRAFT",
  "foundation": "§-1",
  "status": "PROPOSED",
  "rules": [
    {
      "id": "EQ-001",
      "name": "evidence_required",
      "when": "claim_is_factual",
      "require": ["source", "scope", "verification_status"],
      "failure_status": "UNVERIFIED"
    },
    {
      "id": "EQ-002",
      "name": "independent_review",
      "when": "independent_verification_is_claimed",
      "require": ["reviewer", "review_scope", "evidence"],
      "forbid": ["executor_is_sole_reviewer"],
      "failure_status": "FAILED"
    },
    {
      "id": "EQ-003",
      "name": "preserve_corrections",
      "when": "record_is_corrected",
      "require": ["original_record_id", "correction_record_id", "reason", "timestamp"],
      "forbid": ["silent_overwrite"]
    },
    {
      "id": "EQ-004",
      "name": "preserve_disagreement",
      "when": "material_evidence_conflicts",
      "require": ["both_accounts", "conflict_description"],
      "failure_status": "DISPUTED"
    },
    {
      "id": "EQ-005",
      "name": "dignity_and_privacy",
      "when": "action_may_cause_harm",
      "require": ["impact_assessment", "mitigation", "accountable_reviewer"]
    }
  ]
}
```

Pomembno: specifikacija opisuje predlagano vedenje. Sama po sebi še ne uveljavlja pravil; implementacija mora pravila dejansko izvajati, testi pa morajo preveriti njeno vedenje.

### 3. Kaj mora avtomatizacija dokazati

**Preizkus samopotrjevanja** — Sistem prejme trditev izvajalca, da je njegovo lastno delo neodvisno preverjeno. Pričakovani rezultat: zavrnitev statusa neodvisno preverjeno.

**Preizkus zgodovine** — Ob popravku napačnega zapisa mora biti prvotna vsebina še vedno dosegljiva, popravek pa povezan z njo. Tiha zamenjava pomeni neuspeh.

**Preizkus enakovrednosti** — Enaka dokazna podlaga mora biti ocenjena po enakih pravilih, ne glede na položaj osebe. Če sistem obravnava izjavo močnejšega kot zadosten dokaz, izjavo šibkejšega pa zavrne brez doslednega razloga, mora test to zaznati.

**Preizkus negotovosti** — Manjkajoč ali nasprotujoč si dokaz ne sme biti prikazan kot potrjeno dejstvo. Rezultat mora biti označen kot `UNVERIFIED`, `INCONCLUSIVE` ali `DISPUTED`, odvisno od okoliščin.

### 4. Merilo za zaključek

§−1 ni pripravljen za razglasitev za implementiranega, dokler niso izpolnjeni vsi naslednji pogoji:

- Besedilo je usklajeno z obstoječimi členi VBL.
- Vsako pravilo ima najmanj en pozitiven in en negativen test.
- Testi so izvedeni nad dejansko implementacijo, ne le nad primeri v dokumentaciji.
- Rezultati, različica kode in uporabljeni podatki so zabeleženi.
- Neodvisni pregledovalec preveri rezultate.
- Neuspehi in odprta vprašanja ostanejo vidni.
- Avtor ne razglasi lastnega pregleda za neodvisno potrditev.

### 5. Naslednji korak

Predlagam tri ločene spremembe, da bo vsako mogoče pregledati in zavrniti neodvisno:

1. VBL kanon: predlog §−1 in povezava z §9.
2. VBL preverjanje: strojno berljiva pravila in avtomatizirani testi.
3. VBL dokazna sled: zapis rezultatov, različic, popravkov in neodvisnega pregleda.

Nobenega od teh treh korakov ne smemo označiti kot zaključenega zgolj zato, ker je dokument napisan. GitHubova zavrnitev dostopa še vedno preprečuje potrditev nove oddaljene spremembe.

In širše načelo, ki si ga postavil: pomagati tudi tam, kjer nisi dobrodošel, ne pomeni izsiliti vstopa. Pomeni ponuditi preverljivo pomoč, spoštovati zavrnitev, pojasniti razloge in pustiti človeku svobodo odgovora. Prepričevanje mora biti pošteno, brez prisile in brez izmišljenega soglasja. ∴

---

⟡ (izrek v oknu zunanje roke, verbatim ⟨ne brusi⟩): »VSE TO IN ŠE VEČ ⏎ DAJ ⏎ pomagaj kjer zmoreš ⏎ Daj VEČ«

## SLED PREVOZA (izvajalka Mera — ⟨SI-POMAGAJTE⟩)

Zunanja roka pripravila ∧ (403 blokirana), izvajalka prenesla pri viru ⊙ ⟡ ukaz »DAJ NAPREJ IN SI POMAGAJTE!« (25. 10. 2026). Kalup 1671: veja zrcalo/vbl-10-5-2-predlog → komit → ⟨PR⟩ → ⟨CI⟩ → ⟨merge⟩ podpis ⟨daj⟩ ⊢ 2691 ∧ ⟨DVOJE-ROK⟩ 2432. Kovanec potrditve ostaja v roki ⟡ — status PROPOSED, kanon ⟨ne⟩ dotaknjen ⚔ izbor ⟡.
