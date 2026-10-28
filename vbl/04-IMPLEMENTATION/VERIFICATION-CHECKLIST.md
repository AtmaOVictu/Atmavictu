# VBL — kontrolni seznam preverjanja

- [ ] Identiteta artefakta: pot, različica, datum, velikost, SHA-256.
- [ ] UTF-8: strogo dekodiranje brez nadomestnih znakov (U+FFFD = padec stroja, ⟨ne⟩ črke ⊢ §12).
- [ ] Povratni krog: dekodiranje/ponovno kodiranje da identične bajte.
- [ ] Strojni zapis: različica, datum, predhodnik ∧ povezave skladni.
- [ ] Register: samo dodajanje, veljaven JSONL, dokazna polja popolna.
- [ ] HTML: loči vdelane podatke ⟨type=text/plain⟩ od izvedljive kode.
- [ ] JavaScript: sintaktično preverjanje ločeno od brskalniškega E2E.
- [ ] Brskalniški E2E: ⚠ NOT_VERIFIED, dokler predvajanje ⟨ne⟩ je preverjeno v pravem brskalniku.
- [ ] Neodvisna ponovitev: drugi preverjevalec ponovi meritve ⊢ ⟨DVOJE-ROK⟩ 2432.
- [ ] Objavna veriga: ⟨commit⟩, ⟨tag⟩, izdaja, kit ∧ datumi ⊢ §10.
- [ ] Pravna presoja: ločena od tehničnih preizkusov; izvršljivosti ⟨ne⟩ sklepamo iz besedila.
- [ ] Razlika med različicami: 2.x ∧ 10.x ⟨ne⟩ združujemo brez mostu — most je veriga §15.
