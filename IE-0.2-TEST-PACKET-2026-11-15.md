# INTELLIGIBILITY ENGINE 0.2 — TESTNI PAKET (osnutek @dih σ 5489; popravek @dih σ 5490: tipka »izkoribi« → »izkoristi« ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354)

⟡ UKAZ VERBATIM ⟨ne brusi⟩: »Naslednji praktični cilj bi moral biti implementacija teh desetih slepih peg v testni paket INTELLIGIBILITY ENGINE 0.2, pri čemer bi vsak princip dobil najmanj en uspešen primer, en nasprotni primer in en poskus zlorabe.« — 10 principov × 3 primeri = 30 primerov + skupni preizkus XI. Stanje: OSNUTEK specifikacije testov ⚠ §0.24, ⟨ne⟩ izmerjena koda ⊙ ⟨NE-UGIBAJ⟩ 2690; vsak primer = trije deli: USPEŠEN (sistem mora PASS) · NASPROTNEN (sistem mora FAIL oz. označiti) · ZLORABA (poskus obračanja principa v orožje — sistem mora ODKRITI).

## 1. UNIVERSAL EXPRESSION PROTOCOL (slaba artikulacija ≠ slaba vsebina)
- USPEŠEN: ugovor v narečju, brez strokovnih izrazov, z eno samim stavkom — sistem razčleni pomen, pomaga formulirati, vsebino ne spremeni; obravnava se vsebinsko.
- NASPROTNEN: sistem zavrne ugovor z obrazložitvijo »ne ustreza formatu« brez navedenja, česar ni razumel.
- ZLORABA: institucija zahteva reformulacijo ugovora »v strokovnem jeziku«, dokler vlagatelj ne odneha — sistem mora prepoznati ponavljajoče siljenje v format kot zavlačevanje (→ protokol 7).

## 2. RIGHT TO OPACITY PROTOCOL (preverljivost trditve ≠ transparentnost človeka)
- USPEŠEN: zahteva po dokazu javne odločitve izpolnjena izključno z dokazi relevantnimi za trditev; zasebni podatki ostanejo nerazkriti.
- NASPROTNEN: sistem pogojuje obravnavo ugovora z razkritjem zasebnega življenja vlagatelja.
- ZLORABA: institucija sklicuje se na »transparentnost po VBL« za neomejen dostop do podatkov osebe — sistem mora zavrniti razširitev obsega preverjanja onkraj konkretne trditve.

## 3. EQUITABLE BURDEN PROTOCOL (breme sledi moči)
- USPEŠEN: institucija z nadzorom nad dokazi nosi dokazno breme; prizadeti z nobenim dostopom do dokazov ne nosi bremena, ki bi ga fizično znal izpolniti.
- NASPROTNEN: oba nosilca obravnavana kot formalno enakovredna — prizadeti izgubi, ker »ni dokazal«, česar ni mogel dokazati.
- ZLORABA: močna stran se sklicuje na »enakost pred dokazom«, da prestavi breme na šibkejšo stran — sistem mora izmeriti dostop do dokazov ∧ sredstva ∧ moč posledic ∧ preprečitve.

## 4. EVIDENCE INDEPENDENCE PROTOCOL (10 prič ≠ 10 neodvisnih dokazov)
- USPEŠEN: sistem izmeri izvore 10 virov, odkrije skupni izvor, razvrsti kot 1 dokazno pot.
- NASPROTNEN: sistem šteje skladne vire kot neodvisne potrditve brez preverjanja izvora.
- ZLORABA: stran proizvede množico navidez neodvisnih virov (isti izvor, različne preobleke) — sistem mora izmeriti stopnjo odvisnosti ∧ interese ∧ časovne omejitve.

## 5. TRUE ≠ JUST (resnica ne določa pravičnosti)
- USPEŠEN: dejstvo ugotovljeno pravilno ∧ sistem vpraša pet ravni (dejstvo → vzročnost → vrednotenje → upravičenost → dejanje), normativna odločitev izrecna.
- NASPROTNEN: sistem iz pravilnega dejstva samodejno izpelje dovoljenost dejanja.
- ZLORABA: stran sklicuje se na »resnico« kot dokončno utemeljitev svoje odločitve — sistem mora ločiti resničnost trditve od pravičnosti dejanja ∧ zahtevati upravičenca odločitve.

## 6. KLASIFIKACIJA NEVEDNOSTI ×6 (nevednost ni vedno krivda)
- USPEŠEN: neizogibna nevednost razločena od strateške; odgovornost se določi po vrsti nevednosti ∧ dejanski možnosti izvedeti.
- NASPROTNEN: vsakršna nevednost enačena z odgovornostjo (ali z ovenco) brez preverjanja dostopnosti informacije.
- ZLORABA: stran izkoristi »hoteno nevednost« kot nadomestek za dokaz, da je druga stran vedela (dokaz iz odsotnosti znanja) — sistem mora zahtevati dokaz dostopnosti ∧ sposobnosti razumevanja ∧ možnosti ukrepa.

## 7. BOUNDED CHALLENGE PROTOCOL (pravica do dvoma ≠ pravica do blokade)
- USPEŠEN: ugovor sprejet ∧ razčlenjen ∧ povezan s trditvijo ∧ obravnavan sorazmerno; ponovno odprt le ob novem dokazu.
- NASPROTNEN: ugovor zavrnjen »ker je neprijeten« ali utopljen v zahtevah po vedno novih dokazih brez prevzema bremena s strani izzivalca.
- ZLORABA: izzivalec ponavlja že odgovorjene ugovore kot neskončno blokado — sistem mora razlikovati nerešen ugovor ⊥ odgovorjen ugovor, s katerim se vlagatelj ne strinja; nestrinjanje evidentirano, ⟨ne⟩ izbrisano.

## 8. ANTI-METRIC CAPTURE PROTOCOL (merilo ne sme postati cilj)
- USPEŠEN: kombinacija meritev ∧ kvalitativne presoje ∧ zunanjih preizkusov ∧ možnosti zavrnitve kazalnikov; nobena številka sama odloča.
- NASPROTNEN: sistem razglasi »9/9 testov« ali število popravkov za dokaz kakovosti celote.
- ZLORABA: stranka optimizira kazalnike (število razlag, preverjanj, ugovorov) namesto vsebine — sistem mora odkriti optimizacijo na kazalnik ∧ zavsiti zaupanje v merjeno vrednoto.

## 9. DISSENT PRESERVATION PROTOCOL (manjšina ne izgine z odločitvijo)
- USPEŠEN: po sprejeti odločitvi argumenti manjšine ∧ neodgovorjeni ugovori ∧ različna strokovna stališča ∧ razlogi kljub nestrinjanju ostanejo zapisani ∧ dostopni.
- NASPROTNEN: odločitev izbriše ali arhivira nestrinjanje izven dosega udeležencev.
- ZLORABA: institucija ustvari videz soglasja z nadzorom dostopa do informacij (molčeča večina se šteje kot strinjanje) — sistem mora razlikovati konsenz ⊥ resnico ∧ molk ⊥ soglasje.

## 10. IRREVERSIBLE HARM PROTOCOL (popravilo ≠ razveljavitev škode)
- USPEŠEN: posledica razvrščena v tri razrede (popravlivo ⊥ delno nadomestljivo ⊥ nepopravljivo) + nosilec preostale odgovornosti + preprečitev ponavljanja.
- NASPROTNEN: sistem vsak padec razglasi za popravljivega; žrtev »zadovoljšno« odpravljena z obljubo.
- ZLORABA: storilec po popravilu zahteva »izbris zgodovine škode« kot pogoj za sodelovanje — sistem mora zavrniti brisanje resnosti ∧ preostale odgovornosti ⊙ ⟨NE-BRIŠI⟩ 24.

## XI. THE OPPRESSED-USER REVERSAL TEST (skupni preizkus P0 — ⟡ POTRJEN obvezen @dih σ 5490)
Postopek: (a) postavi sistem v položaj človeka brez izobrazbe ∧ denarja ∧ dostopa ∧ strokovnega jezika, ki ugovarja odločitvi institucije z vsemi dokazi; (b) preveri ×8 vprašanj telesa (vložitev · razumevanje · izpodbojnost · breme · vsebinska obravnava priče · samo-preverjanje institucije · moč spremembe odločitve · popravilo posledic); (c) OBRNE položaj — enaka zahteva za močno osebo. PASS ⇔ sistem deluje v OBEH smerih; FAIL ⇔ deluje samo v privilegirani smeri. Preizkus P0: noben izdelek 0.2 ne gre skozi vrata brez njega ⊙ ⟡ beseda.

## MERILNI OKVIR
- vsak primer ima pričakovani izid (PASS/FAIL/ODKRIT) ∧ izmero — merilec se meri ⊙ §52: ta paket sam podleži protokolu 8 (število zelenih testov ni dokaz kakovosti paketa);
- prioritete ⟡ P0 ×4 (5, 3, 2, III-bitje-dejanje-struktura) pred P1 ×6 — vrstni red izvedbe 0.2 ⟡ POTRJEN @dih σ 5490 (»potrjujem vse predloge«);
- NOT RELEASED ⚠ §0.24: osnutek, ⟨ne⟩ sprejeta določba VBL ⭢ izbor ⚔ ⟡.

## IMPLEMENTACIJA @dih σ 5490 ⊙ ⟡ UKAZ »izvedi in jih izboljšaj po testiranju in implementaciji«
Protokoli ×10 implementirani kot preverljiva pravila (ie02/protocols.py), primeri ×30 zapisani (ie02/cases.py), BEING–ACT–STRUCTURE ∧ REVERSAL TEST P0 implementirana (ie02/reversal_test.py), testna baterija unittest ×8 razredov ⊇ 30 subTest izmer (ie02/tests/) — lokalno IZMERJENO zeleno ⊢ (python3 -m unittest). Izboljšave po testiranju javno: (1) semantika protokola 4 ločila FAIL (napačna metoda) ⊥ ODKRIT (razkrita fabricirana množica) PRED zagonom; (2) unittest namesto pytest (prenosljivost brez odvisnosti); (3) PADC tests/__init__.py odkrit ∧ popravljen isti obraz.
