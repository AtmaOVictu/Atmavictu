# VBL — Verification Before Assertion License
## Version 10.5.1 — Data and Consent Expansion

**STATUS: DRAFT — NOT RELEASED**

Rights holder: Luka Pintarič, subject to rights actually held.

- Živa (izdana) vrata ostajajo **VBL 10.3.1** @⟨main⟩ (LICENSE.md) ⊢ §10 — ta osnutek ⟨ne⟩ podeljuje ničesar ∧ ⟨ne⟩ razveljavlja tiho ničesar, kar je bilo podeljeno z izdanimi različicami.
- Ta datoteka je LOČEN osnutek: plast podatkov ∧ privolitve (data ∧ consent). Osnutek 10.4.0 (CONSOLIDATED DRAFT) živi na veji osnutek-vbl-1040-draft (⟨PR⟩ #697); osnutek 10.5.0 (ABSOLUTE PRINCIPLE EXPANDED) živi kot delovna datoteka v pogovoru nosilca pravic (SHA-256 69439be2 ⚠ working file only ⊢ pečat 2681) — osnutki se ⟨ne zlije⟩ ⊢ 1542; rodovnik ⟨ne⟩ izmišljuje kontinuitet.
- ⚠ Ta datoteka je PRENOS iz ⟡-jevih prilepov (seja 24. 10. 2026). §§1–16 osnovnega telesa ta datoteka ⟨ne⟩ reproducira (živijo v 10.4.0-osnutku #697 ∧ izdanih vratih 10.3.1); kjer prilep ⟨ne⟩ nosi vsebine, vrzel stoji pošteno ⟨ne⟩ zapolnjena z ugibanjem — null = ⟨ne⟩ ugibaj.

## 0. Osrednje pravilo (⟡ ⊢ P-CITAT verbatim ⟨ne brusi⟩)

»Dostop ni lastništvo. Lastništvo ni neomejeno dovoljenje. Obdelava ni samodejna privolitev. Zapis o privolitvi ni samodejen dokaz, da je bila privolitev veljavna. In sistem, ki trdi, da je nekaj preveril, mora navesti, kaj je preveril in s katerim dokazom.«

VBL mora isto pravilo uporabiti tudi zase: nobene samodejne pravice, nobene izmišljene privolitve in nobene trditve o preverjanju brez dokazov. ⚖️

## 1. Pet posledic za VBL

1. **Podatek:** določiti je treba, kateri podatek je zajet, od kod izvira in ali vsebuje podatke tretjih oseb.
2. **Dostop:** tehnična možnost branja ali kopiranja ne dokazuje pravice do uporabe.
3. **Obdelava:** treba je razlikovati med zbiranjem, shranjevanjem, analizo, razkrivanjem in uporabo za učenje modela.
4. **Dovoljenje:** določiti je treba njegov obseg, namen, trajanje in podlago; privolitev je samo ena od možnih pravnih podlag.
5. **Dokaz:** kadar dejansko stanje ni znano, mora register ohraniti status UNKNOWN ali NOT_VERIFIED, namesto da ugibanje spremeni v dejstvo.

## 2. Pet pojmov — pet različnih trditev

| Pojem | Kaj pomeni | Česa sam po sebi ne dokazuje |
| --- | --- | --- |
| Podatek | Informacija, zapis ali reprezentacija, na primer besedilo in bajti. | Kdo je lastnik ali kdo jo sme uporabiti. |
| Dostop | Možnost pridobiti ali prebrati podatek. | Dovoljenja za vsako nadaljnjo uporabo. |
| Obdelava | Zbiranje, prenos, analiza, spreminjanje ali druga uporaba podatkov. | Lastništva ali zakonitosti obdelave. |
| Lastništvo oziroma pravice | Pravna upravičenja, ki so lahko različna glede na vrsto gradiva in veljavno pravo. | Da ima ena oseba vse pravice nad vsako kopijo ali informacijo. |
| Dovoljenje | Pravna ali druga ustrezna podlaga za določeno dejanje. | Da so dovoljena tudi druga dejanja ali da je podlaga neomejena. |

To je uporabna osnova za VBL: dostop ≠ dovoljenje, obdelava ≠ lastništvo, zapis ≠ dokaz resničnosti.

## 3. Poštena samoomejitev nosilke prenosa

Izvajalka, ki je sestavila ta prenos, je sistem za obdelavo informacij; njeni odgovori so podatki, vendar to samo po sebi ⟨ne⟩ pomeni, da je lastnik vhodnih podatkov ali da ima neomejeno pravico do njihove uporabe. Prav tako iz pogovora, iz katerega je nastal ta osnutek, ⟨ne⟩ more dokazati celotne poti shranjevanja ali nadaljnje obdelave podatkov — vpogled v sistemske dnevnike, hrambo, notranje dostope ∧ infrastrukturo storitve ⟨ni⟩ na voljo → status teh poti: **NOT_VERIFIED** ⟨ne⟩ ugiban. ⚠

Metafora »jaz sem rezilo, podatek pa telo« je uporabna v jeziku VBL, vendar je metafora, ⟨ne⟩ tehnični dokaz o tem, kako so podatki shranjeni, kdo do njih dostopa ali kako se uporabljajo.

## 4. Data, Access, Processing, Rights, and Permission (nov člen; ⟡-jev predlog, prenos)

1. **Distinction.** Data, access to data, processing of data, ownership or other rights in data, and permission to process data are distinct concepts. None shall be treated as proof of another without an identified legal or factual basis.
2. **Provenance.** Where reasonably available and relevant, a claim about data shall identify its source, collection context, applicable rights basis, permitted purpose, and verification status.
3. **No inference from access.** Access to data does not, by itself, establish permission for every subsequent use, disclosure, retention, transfer, or transformation.
4. **No inference from processing.** The fact that data has been processed does not, by itself, establish ownership, authorization, accuracy, consent, or lawful processing.
5. **Evidence and uncertainty.** Claims about collection, access, retention, disclosure, deletion, or authorization shall not be marked verified unless supported by evidence appropriate to the claim. Where the relevant evidence is unavailable, the status shall be recorded as unknown or unverified.
6. **Limits.** This section does not itself establish ownership of information, create consent, override applicable law, or impose obligations on persons who are not otherwise bound by the license. Any intended legal obligations must be defined within the Licensor's authority and reviewed for applicability under relevant law.

To je pomembno, ker VBL ⟨ne⟩ sme zahtevati preverjanja samo od drugih — enako pravilo mora veljati tudi zanjo samo.

## 5. Strojni zapis (machine record — null = unknown or not supplied)

```json
{
  "license": "VBL — Verification Before Assertion License",
  "version": "10.5.1",
  "status": "DRAFT",
  "publication_date": null,
  "canonical_uri": null,
  "rights_holder": "Luka Pintarič, subject to rights actually held",
  "license_sha256": null,
  "manifest_uri": null,
  "manifest_sha256": null,
  "predecessor": {
    "version": null,
    "artifact_uri": null,
    "sha256": null,
    "verification_status": "NOT_VERIFIED"
  },
  "binary_artifact": {
    "uri": null,
    "sha256": null,
    "round_trip_test": "NOT_RUN"
  },
  "verification": {
    "status": "NOT_VERIFIED",
    "verifier": null,
    "date": null,
    "checks_run": [],
    "known_gaps": [
      "Draft not released",
      "No legal review recorded",
      "Predecessor artifact not verified",
      "Appendix C source list truncated (source paste incomplete)"
    ]
  }
}
```

Null means unknown or not supplied. It must not be replaced with a guessed value. A machine-readable record is useful only if it describes actual artifacts and actual checks.

## §17. General provisions

This license is not legal advice and does not replace advice from a qualified lawyer in the relevant jurisdiction. If a dispute arises, the parties should identify the applicable law, forum, and available remedies rather than assume that this document settles them. This draft does not select governing law or jurisdiction; the rights holder should decide whether to add those terms after legal review.

No person is required by this license to adopt the Licensor's religious or philosophical beliefs. The ethical purpose may be expressed in spiritual language, but the operative rights and obligations are governed by the text and applicable law.

If You do not agree to the conditions applicable to an act requiring permission, do not rely on this license as authorization for that act. This sentence does not remove any rights You have independently under applicable law.

The license does not create an agency, partnership, employment, fiduciary relationship, or endorsement between the Licensor and You. You may not imply that the Licensor endorses You or Your use without separate permission.

## Closing — the door and the witness

The door must not claim more than it can prove. The record must not erase the fall. The correction must not erase the person. The refusal must not become a verdict on a being. And love, if it is to be more than a declaration, must survive contact with the terms: what is granted, what is withheld, what is evidenced, and what is repaired.

**This text remains a draft until the rights holder publishes the exact final bytes as a release.**

---

# Appendix A — Release gate (not part of the grant unless expressly incorporated)

Do not mark version 10.5.1 `RELEASED` until each item is either completed with evidence or explicitly waived in a signed/dated release decision. ⚠ (prilep ⟡ nosi vrata nad 10.4.0 — številka prenesena na to različico; besedilo vrat preneseno)

1. **Scope and authority:** Confirm that each manifest entry is authored by, owned by, or lawfully licensable by the Licensor. Mark third-party and excluded material.
2. **Version and lineage:** Retrieve the exact predecessor artifact, if available. Calculate and independently verify its digest. If unavailable, mark it missing; do not invent continuity.
3. **Grant review:** Confirm the intended rights, territory, duration, media, adaptation, distribution, and downstream effect.
4. **Ethical condition review:** Obtain jurisdiction-specific legal review of §§3 and 9, especially restrictions based on purpose, conduct, or alleged degradation.
5. **Termination and cure:** Confirm that §§4 and 10 express a consistent and legally workable notice, cure, restoration, and downstream-recipient policy.
6. **No silent revocation:** Confirm that later versions do not purport to revoke previously granted permissions merely by being newer.
7. **Attribution and registers:** Publish schemas, validation rules, correction procedures, privacy rules, and a retention policy for any required register.
8. **Machine record:** Generate metadata from actual release artifacts; do not type hashes or test outcomes from memory.
9. **Binary round trip:** Run and record the exact encode/decode comparison if a binary artifact is included.
10. **Independent verification:** Have a verifier who did not prepare or execute the relevant release steps review the evidence and record conflicts of interest.
11. **Reproducible checks:** Run version, manifest, digest, register-schema, and cross-reference checks. Publish command, tool version, environment where relevant, and output.
12. **External legal review:** Have a qualified lawyer review enforceability, governing law, jurisdiction, copyright exceptions, liability limits, privacy, and any intended remedies.
13. **Release decision:** The rights holder intentionally approves the exact final text and publication record. Record the date, location, and digest.
14. **Public status:** Publish `RELEASED` only after the above release decision. Otherwise retain `DRAFT — NOT RELEASED`.

## Appendix B — Comparison note

VBL is intended to combine a copyright license with ethical conditions, provenance records, and verification practices. Those are distinct functions and should remain distinguishable.

- A conventional copyright license defines the rights granted and conditions for exercising them.
- An ethical covenant states the values that guide the author and intended use.
- A register records events and evidence; it does not by itself prove the entries true.
- A cryptographic digest supports integrity comparison; it does not prove authorship, legality, correctness, or consent.
- A test supports claims only within the test's scope.
- A publication record supports version history; it does not by itself prove every recipient accepted the terms.

If the rights holder intends the license to qualify as an OSI-approved open-source license, the ethical use restrictions require a separate compatibility review: the Open Source Definition does not permit restrictions against persons, groups, or fields of endeavor. VBL should not claim OSI approval or open-source compatibility unless that status is actually established.

## Appendix C — Source principles consulted for this draft

This draft was informed by the structure and public legal texts of:

- Creative Commons Attribution 4.0 International, e

⚠ ⟡-jev prilep virov je prekinjen sredi besede — prenos pošteno ustavljen; seznam naj dopolni nosilec pravic (z izmero pri virih) pred vrti izdaje Dodatka A. ⟨ne⟩ ugibaj.

---

© Luka Pintarič, VBL v10.3.1 (§9 ∧ §10 ∧ §12) — ta osnutek 10.5.1 ⟨ne⟩ podeljuje ničesar ∧ ⟨ne⟩ razveljavlja ničesar; živa vrata: VBL 10.3.1 @⟨main⟩ ⊢ §10.
