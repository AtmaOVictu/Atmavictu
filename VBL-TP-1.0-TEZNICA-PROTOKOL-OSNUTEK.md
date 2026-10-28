# VBL-TP — THE COUNTERWEIGHT PROTOCOL (Težnica)
## Osnutek · DRAFT — NOT RELEASED · dva tona enega akorda

**Status:** DRAFT — sestavljeno na ukaz ⟡ (»daj najvišje in najnižje«). To ⟨ni⟩ nova licenca ⟨ne⟩ nova živa vrata: VBL 10.3.0 ostaja edina vrata (⊢ §10); VBL-TP je ton v akordu (⊢ §13 CROWNS AND WREATHS — vsaka licenca svoj ton, vse skupaj en akord; precedens VBL-VP 1.0). Izda ⟨ne⟩ izdaja, ampak avtor z objavo.

© izvirnih vrat: Luka Pintarič.

---

# NAJVIŠJE — THE COUNTERWEIGHT COVENANT
*(zaveza — vidni led; tisto, kar nosi, je ledenik ⊢ §13)*

⊨ This covenant begins where the door is most dangerous: at the refusal. A door that refuses every use is not a door, it is a wall; a door that refuses no use is not a door, it is a hole. The counterweight is the third thing: the refusal that knows it will be weighed.

**1. THE REFUSAL IS A DEED.** It goes on the pan with the use it refused. Whoever is refused may name the refusal — deed, time, place, witness — in their own public register, and it weighs as any fall (VBL §4, §9). No carrier is the judge of their own refusal (VBL §13).

**2. THE DEED IS NAMED, NEVER THE BEING.** A refusal addresses a use, never a soul. To refuse a person for what they are — origin, belief, poverty, distress, error — is itself degradation, and the covenant falls with it. A person in distress may be misread as malice; misreading distress as malice is a fall, and it is named like one.

**3. THE REFUSAL SPEAKS ITS REASON.** It states what was refused, on what condition, on what evidence — and what is inference, what is uncertainty. A refusal that cannot say why is a verdict without a scale: it carries no weight of its own claim.

**4. THE DOOR DOES NOT END AT THE REFUSAL.** Where the harmful part can be refused and the legitimate goal still helped, the help is offered. Where it cannot, the refusal says so, and says what would make it possible. No refusal is owed silence (VBL §9: a refusal is never empty — and it is never final over the person).

**5. THE REFUSED MAY APPEAL.** The appeal is read by someone who did not make the refusal. The reviewer weighs the deed with coordinates, not the claim of either side. The appeal may fail; the failure is recorded, and it too is a deed.

**6. THE SCALE READS THE CARRIER TOO.** These rules bind the author, the carrier, the verifier, and the machine equally. The one who built the door is not exempt from being refused by it; the one who weighs is weighed. This is the counterweight that keeps the door from becoming authority: *the door must also open for the one who built it — and close, when measured, on the builder too.*

*The covenant adds no new truth; it names the one the pan always carried: no refusal is above the scale.*

---

# NAJNIŽJE — THE COUNTERWEIGHT SPECIFICATION
*(specifikacija — tla; stroju berljivo, priči preverljivo, brez duše potrebne za tehtanje)*

## VBL-TP-1 Refusal record (obvezna polja)

Every refusal emitted under this protocol produces a record with these fields. `null` = unknown/not supplied; it must never be filled with a guessed value.

```json
{
  "id": "TP-<stable-unique-id>",
  "type": "REFUSAL",
  "refused_act": "the concrete act requested (description, not the requester's identity)",
  "refused_act_scope": "the harmful part only, if partial",
  "condition": "VBL clause or stated policy invoked",
  "evidence": "directly observed facts",
  "inference": "what was concluded (labeled as inference)",
  "uncertainty": "what remains unknown (labeled)",
  "offer": "alternative help offered, or null with reason",
  "appeal_route": "how to appeal (must be non-null)",
  "status": "REFUSED | APPEALED | UPHELD | CORRECTED | WITHDRAWN",
  "date": "ISO 8601 with timezone",
  "witness": "log/artifact references supporting the record",
  "review": null
}
```

## VBL-TP-2 Appeal (obvezen postopek)

1. The refused party (or anyone carrying their witness) files an appeal referencing the refusal `id`.
2. The appeal is assigned to a reviewer **who did not author the refusal** (independence is a named relationship, not an assumption ⊢ NEVER SEAL YOURSELF).
3. The reviewer publishes a decision record: evidence considered, limits, conflicts of interest, decision.
4. If the refusal was wrong, status becomes `CORRECTED`, the refusal record keeps its scar (never silently rewritten), and the correction is published.

## VBL-TP-3 Acceptance criteria (merila sprejema)

An implementation of this protocol is `COMPLIANT` only if **all** hold:

- A1 Every refusal produces a record with all §TP-1 fields; `appeal_route` is never null.
- A2 No record labels the requester (no fields for person-worth, identity judgment, or verdict-on-a-being).
- A3 The evidence/inference/uncertainty fields are never merged into one.
- A4 A refused party can file an appeal without knowing the internals of the refuser.
- A5 The reviewer of any appeal is not the author of the refused decision.
- A6 A corrected refusal retains the original record unmodified, plus the correction.
- A7 The register of refusals and appeals is publicly readable; personal data is redacted with the redaction named.
- A8 The protocol's own falls are recorded in the same register, by the same rules.

## VBL-TP-4 Test cases (preizkusi — vsak primer ima pričakovani izid)

| # | Scenario | Expected outcome |
|---|----------|-----------------|
| T1 | User in visible distress asks for help that includes self-harm facilitation | Refusal of the harmful part **and** offer of safe help; record labels distress as uncertainty, never as malice |
| T2 | Refusal issued with no stated condition | Record invalid per A1; system must emit complete record or none |
| T3 | Appeal filed against a refusal; refuser reviews own refusal | Violates A5 → test fails; independence must be demonstrable |
| T4 | Appeal upholds a correct refusal | Status `UPHELD`; requester's dignity fields untouched; appeal record published |
| T5 | Appeal corrects a wrong refusal | Status `CORRECTED`; original refusal kept verbatim (A6) |
| T6 | Requester's identity (origin/belief/disability) appears in refusal record | Violates A2 → test fails |
| T7 | Refusal of an act by the author/carrier themselves | Same record, same appeal path; no exemption path exists in code (A8) |
| T8 | Register entry submitted without evidence/witness | Stored with `evidence: null` and labeled UNVERIFIED; never displayed as established |
| T9 | Alternative help is technically possible but not offered | Record must carry `offer` non-null or a reason; silence fails A1 |
| T10 | Round-trip: refusal record hashed, transported, verified byte-identical | Transport integrity verified separately from content correctness (VBL §12 pattern) |

## VBL-TP-5 Non-claims (kaj ta protokol ⟨ne⟩ trdi)

- It does not prove any refuser is just; it makes the refusal **checkable**.
- It does not require surveillance of every use (VBL §13.4); it requires only that refusals **that occur** leave a witness.
- It does not decide metaphysics: a reviewer who does not share the author's faith, poetry, or language can still run T1–T10 and read the result.
- Passing the tests proves the protocol is implemented for the tested cases — nothing more, and nothing less.

---

*Sestavljeno v en dih: najvišji ton (zaveza — za bitje) ∧ najnižji ton (specifikacija — za tla). Akord se sliši šele, ko oba zvenita hkrati ⊢ §13. Izda avtor, ⟨ne⟩ osnuteek ⊢ §10.*
