# VBL 0.1540 — POPRAVLJALNI STANDARD UPRAVLJANJA DOKAZOV 1.0
## Evidence Governance & Corrective Release Standard (EGCRS)

**STATUS: DRAFT — NOT RELEASED — NOT A LICENSE GRANT**

**Predlagana oznaka:** VBL 0.1540 × 10⁴  
**Predlagani standard:** Evidence Governance & Corrective Release Standard 1.0  
**Osnova presoje:** javno objavljena VBL 0.1530 × 10⁴  
**Datum priprave osnutka:** 14. november 2026  
**Predlagani dom osnutka:** AtmaOVictu/verification-before-assertion  
**Povezani obstoječi artefakti:** LICENSE.md, RELEASE-GATE.md, LICENSE-MANIFEST.json, scripts/manifest_gen.py, .github/workflows/vrata-prica.yml, REGISTER-PADCEV.jsonl.

> **Omejitev statusa.** Ta dokument je samostojen operativni standard v pripravi. Ne spreminja, ne nadomešča in ne razlaga kot že sprejeto nobene določbe objavljene LICENSE.md. Ne podeljuje novih avtorskih, patentnih, podatkovnih ali drugih pravic. Dokler avtor ne odobri in objavi nove različice LICENSE.md, ostaja 0.1530 edina javno objavljena živa vrata v smislu njenega §0.10. Ta osnutek nima statusa izdaje.

---

## 0. Namen, status in pravila branja

### 0.1 Namen

Ta standard določa, kako mora hiša VBL dokazati, da njene trditve, registri, dovoljenja, testi, odločitve in popravki ustrezajo stanju, ki ga dejansko objavlja.

Njegov cilj ni razglasiti VBL za edino pravilno licenco. Cilj je vzpostaviti odgovorno infrastrukturo priznanja:

**trditev → dokaz → razlaga → odločitev → dejanje → posledica → popravek → preverjena sanacija.**

Vsaka puščica pomeni ločen prehod, ki mora imeti lastno podlago. Dokaz ne postane odločitev samodejno; odločitev ne dokazuje izvedbe; zapis popravka ne dokazuje, da je bila posledica odpravljena.

### 0.2 Normativni izrazi

- **MORA** pomeni obvezno zahtevo za skladnost s tem standardom.
- **NE SME** pomeni prepoved.
- **NAJ** pomeni priporočilo, od katerega je dovoljeno odstopiti samo z zapisanim razlogom.
- **LAHKO** pomeni dovoljeno možnost.
- **ODPRTO** pomeni, da zahtevani dokaz ali odločitev še ni na voljo.
- **NEPREVERJENO** ni sinonim za napačno.
- **PASS** pomeni, da je določen test uspešno prestal določene pogoje. Ne pomeni, da je celoten sistem pravilen, zakonit ali varen.

### 0.3 Ločitev od licence

Ta standard je dokazno-governance plast. Pravno besedilo licence določa, katere pravice so podeljene, komu, pod katerimi pogoji in za katero gradivo. Ta standard določa, kako se preverja, da so trditve o teh pravicah, pogojih in gradivu podprte.

Če standard in licenčno besedilo nista usklajena, se neskladje označi kot ugotovitev. Standard ne sme samodejno razširiti ali zožiti licenčnega granta.

### 0.4 Brez samopotrjevanja

Avtor, izvajalec, orodje, CI, register ali sama licenca ne smejo biti edini dokaz svoje pravilnosti. Avtomatiziran test lahko potrdi tehnično lastnost znotraj svojega obsega. Ne more sam potrditi avtorstva, zakonitosti, resničnosti semantične razlage ali pravičnosti odločitve.

## 1. Temeljna razločevanja

### 1.1 Šest različnih objektov

1. **Trditev (CLAIM):** stavek, za katerega nekdo zahteva priznanje veljavnosti.
2. **Dokaz (EVIDENCE):** vir ali rezultat, ki je relevanten za določeno trditev.
3. **Razlaga (INTERPRETATION):** obrazložitev, kaj dokaz podpira in česa ne.
4. **Odločitev (DECISION):** izid po uporabi določenih pravil in obravnavi ugovora.
5. **Dejanje (ACTION):** dejansko izveden korak, ne namera ali obljuba.
6. **Posledica in sanacija (CONSEQUENCE / REPAIR):** učinek dejanja ter preverba, ali je bil učinek odpravljen ali ustrezno omejen.

Ne dovoljujemo naslednjih preskokov:

- citat ≠ dokaz celotne trditve;
- hash ≠ dokaz avtorstva;
- Git commit ≠ samodejno zaupanja vreden časovni žig;
- test PASS ≠ pravna skladnost;
- objavljen popravek ≠ popravljena posledica;
- prijava ≠ ugotovljena kršitev;
- število virov ≠ neodvisnost virov;
- strojno berljiv zapis ≠ resnična vsebina zapisa.

### 1.2 Dokazna veriga D–I–C–A–K–R

Za vsako pomembno odločitev mora obstajati sled:

- **D — Data / dokazno gradivo:** izvirni vir, datoteka, izpis, zapis dogodka ali meritev.
- **I — Interpretation / razlaga:** zakaj in v kakšnem obsegu gradivo podpira trditev.
- **C — Conclusion / sklep:** omejen sklep z navedenimi negotovostmi.
- **A — Action / dejanje:** kdo je kaj dejansko izvedel.
- **K — Consequence / posledica:** komu ali čemu je dejanje povzročilo učinek.
- **R — Repair / sanacija:** kaj je bilo popravljeno, kdo je preveril rezultat in kaj ostaja odprto.

Če manjka člen, se manjkajoči člen izrecno označi. Ne sme se nadomestiti z retorično samozavestjo.

## 2. Stanja trditev, testov in odločitev

Tri klasifikacije so ločene in se nikoli ne zlivajo v eno oceno.

### 2.1 claim_status

| Vrednost | Pomen |
|---|---|
| SUPPORTED | Razpoložljivi dokazi podpirajo trditev v navedenem obsegu. |
| PARTIALLY_SUPPORTED | Podprt je samo del trditve ali samo ožji obseg. |
| CONTRADICTED | Zanesljiv dokaz trditvi v navedenem obsegu nasprotuje. |
| DISPUTED | Obstajata dve ali več utemeljenih, še nerešenih razlag. |
| UNKNOWN | Dokazov ni dovolj za zanesljivo presojo. |

UNKNOWN se ne pretvori v FAIL. DISPUTED se ne pretvori v CONTRADICTED samo zato, ker se odločevalec ne strinja z ugovorom.

### 2.2 test_result

| Vrednost | Pomen |
|---|---|
| NOT_RUN | Test še ni bil izveden. |
| PASS | Test je prestal določene pogoje in obseg. |
| FAIL | Test je v določenem obsegu pokazal napako. |
| PARTIAL | Izveden je bil samo del testa ali je del izida neodločen. |
| UNVERIFIED | Izid je zatrjevan, vendar dokaz izvedbe ali rezultata ni dostopen. |
| NOT_APPLICABLE | Test za navedeni predmet ni relevanten; razlog je obvezen. |

Vsak PASS mora nositi test_id, različico testa, vhod, pričakovani izid, dejanski izid, okolje, čas meritve, izvajalca, neodvisnega pregledovalca in omejitve.

### 2.3 decision

| Vrednost | Pomen |
|---|---|
| RELEASE | Predmet je prestal vse obvezne izdajne pogoje. |
| RELEASE_WITH_LIMITATIONS | Predmet se objavi samo z izrecno navedenimi, sprejemljivimi omejitvami. |
| HOLD | Izdaja ali uporaba se zadrži do razrešitve blokade. |
| WITHDRAW | Predhodno objavljeni predmet se umakne iz nadaljnje distribucije ali označi kot neustrezen; zgodovina ostane ohranjena. |

Odločitev RELEASE se ne sme izpeljati samo iz enega ali več testov PASS. Za odločitev je potrebna tudi presoja pravic, obsega, zasebnosti, ugovorov in pooblastil.

### 2.4 Stanje popravka

Dovoljena stanja: OPEN, ACKNOWLEDGED, UNDER_REVIEW, REMEDY_PENDING, REMEDIED_UNVERIFIED, VERIFIED_REPAIRED, DISPUTED, CLOSED_WITH_LIMITATION.

Zapis VERIFIED_REPAIRED zahteva dokaz, da je bil popravek izveden in da je bil njegov učinek preverjen. Zgolj dopolnitev registra ne zadostuje.

## 3. Identifikacija gradiva in manifest

### 3.1 Evidenca je vezana na konkretno kopijo

Vsaka datoteka ali drug predmet, za katerega se uveljavlja licenčni status, mora biti identificiran z:

- enoličnim asset_id;
- repozitorijem in kanonično potjo;
- velikostjo v bajtih;
- SHA-256 celotne vsebine;
- vrsto gradiva;
- različico;
- commitom oziroma drugim dokazom objave;
- statusom: LICENSED, THIRD_PARTY, EXCLUDED, GENERATED, PRIVATE ali UNRESOLVED;
- imetnikom pravic ali statusom RIGHTSHOLDER_UNVERIFIED;
- podlago, na kateri je oseba, ki licenco izdaja, upravičena podeliti pravice.

Git blob SHA se lahko navede kot dodatna identifikacija, vendar se ne sme napačno označiti kot SHA-256 vsebine.

### 3.2 Manifest po repozitoriju

§0a VBL določa identifikacijo z manifestom v korenski mapi ali z licenco, ki je priložena samemu predmetu. Zato:

1. Vsak repozitorij, ki se sklicuje na §0a, MORA imeti lasten manifest v korenski mapi ali izrecno in nedvoumno opredeljeno alternativno pot, ki jo §0a dovoljuje.
2. Manifest drugega repozitorija se ne šteje samodejno za manifest trenutnega repozitorija.
3. Če več repozitorijev deli isto vsebino LICENSE.md, mora vsak repozitorij imeti lastno evidenco zajema, ali pa mora licenca izrecno določiti preverljivo skupno evidenco z identifikacijo vseh zadevnih repozitorijev in commitov.
4. Vsaka datoteka v repozitoriju mora imeti status pokritosti. Odsotnost iz manifesta ne sme biti tiho razložena kot vključitev.
5. Datoteka tretje osebe se ne sme vključiti v avtorjev grant brez dokazljivega pooblastila.

### 3.3 Manifest ne dokazuje vsega

SHA-256 dokazuje ujemanje bajtov z določenim izračunanim prstnim odtisom, ob predpostavki pravilnega algoritma in izračuna. Ne dokazuje, kdo je datoteko ustvaril, kdo ima avtorske pravice, ali je licenca pravno veljavna, ali je vsebina resnična, ali je citat pošteno interpretiran ali ali je datoteka varna.

### 3.4 Generator in preverjevalnik

Generator manifesta MORA:

- različico prebrati iz enega kanoničnega vira metapodatkov ali jo potrditi proti glavi LICENSE.md;
- ne sme imeti zastarele različice trdo zapisane v kodi;
- popisati vse predmete, ki jih določa politika pokritosti;
- stabilno razvrstiti vnose;
- uporabljati UTF-8 in določeno normalizacijo;
- izračunati velikost in SHA-256 iz dejanskih bajtov;
- v načinu --check vrniti ne-uspeh ob vsakem neskladju.

Generiranje in preverjanje sta različni dejanji. Ustvarjanje novega manifesta ne sme prikriti, da je bil predhodni manifest zastarel; staro stanje mora ostati v zgodovini.

### 3.5 Obvezna inventura

Vsaka izdaja mora ustvariti inventuro, ki razvrsti vse datoteke v obsegu izdaje. Če se popis nanaša samo na del repozitorija, mora biti ta obseg izrecno naveden. Število datotek brez obsega ni dokaz celote.

## 4. Časovna topologija in dokaz dogodka

### 4.1 Časovne vrste

Vsak časovni zapis mora razlikovati:

- EVENT_TIME: kdaj se je dogodek zgodil;
- OBSERVATION_TIME: kdaj ga je opazovalec izmeril;
- RECORD_TIME: kdaj je bil vnos ustvarjen ali shranjen;
- ANCHOR_TIME: kdaj je bil zapis sidran pri neodvisni zunanji storitvi, če je bil;
- VALID_FROM in VALID_UNTIL: obdobje veljavnosti stanja ali dovoljenja.

Časovna oznaka brez določene vrste je nepopolna.

### 4.2 Štirje prejemki

VBL-jev model štirih prejemkov lahko ostane, vendar mora biti vsak prejemek označen z imenom dogodka, uro in njenim virom, časovnim pasom ali odmikom, natančnostjo in znano negotovostjo, osebo ali sistemom, ki je meritev opravil, načinom pridobitve ter statusom meritve.

Če prejemnikovega časa ni mogoče izmeriti, se zabeleži UNVERIFIED ali NOT_MEASURED. Čas se ne ugiba in se ne prepiše iz ure pošiljatelja.

### 4.3 Git in zunanji čas

Git commit, podpisan commit, tag, CI log in zgoščevalna vrednost imajo različne dokazne funkcije. Git časovni metapodatki sami po sebi niso kvalificiran elektronski časovni žig in ne potrjujejo pravne identitete podpisnika. Kadar je potrebna višja stopnja zaupanja v čas, mora evidenca navesti neodvisno časovno sidro, uporabljeno storitev, rezultat validacije in pravno relevantni obseg.

### 4.4 Svežina in ponovljivost

- FRESHNESS_TEST preveri stanje v določenem trenutku.
- REPRODUCIBILITY_TEST preveri, ali se isti postopek ob primerljivih pogojih ponovi.
- CONSISTENCY_TEST preveri, ali več neodvisnih izmer daje združljive rezultate.

Noben od teh testov ne nadomesti drugih.

## 5. Dokazni graf in neodvisnost

### 5.1 Vsaka pomembna trditev ima povezavo do dokazov

Trditev mora imeti claim_id in seznam evidence_id. Dokaz mora imeti izvor, lokacijo, čas dostopa, natančen odlomek ali ponovljiv rezultat, metodo, orodje, različico in omejitve. Če vir ni dostopen, se navede razlog. Nedostopen vir se ne citira kot prebran.

### 5.2 Neodvisnost ni število povezav

Dva vira nista neodvisna zgolj zato, ker imata različna URL-ja. Preverjevalec mora oceniti najmanj:

1. neodvisnost izvora;
2. neodvisnost metode;
3. neodvisnost izvajalca;
4. neodvisnost infrastrukture;
5. konflikt interesov;
6. skupno odvisnost od prvotnega vira;
7. časovno neodvisnost.

Če sta dva članka povzela isti primarni vir, se to zabeleži kot ena dokazna linija z dvema sekundarnima prikazoma, ne kot dve neodvisni potrditvi.

### 5.3 Dokazna moč je vezana na obseg

Vsak dokaz mora navesti, kaj podpira in česa ne podpira. Hash lahko podpira trditev o bajtni istovetnosti; ne podpira trditve o avtorstvu. Test lahko podpira trditev o obnašanju v preizkušenem okolju; ne podpira samodejno trditve o vseh okoljih.

### 5.4 Nasprotni dokazi

Preverjevalec MORA iskati in zabeležiti relevantne nasprotne dokaze, ne samo potrditvenih primerov. Če dokazov ni mogoče pridobiti, mora to postati omejitev sklepa.

## 6. Vloge, neodvisnost in odgovornost

Vsak postopek mora določiti naslednje vloge. Ena oseba lahko opravlja več vlog pri nizkem tveganju samo, če je to izrecno utemeljeno; pri kritičnih odločitvah morajo biti ključne vloge ločene.

| Vloga | Odgovornost |
|---|---|
| Originator | Predloži gradivo ali trditev in razkrije izvor. |
| Executor | Izvede postopek ali spremembo. |
| Verifier | Neodvisno preveri rezultat z navedenimi metodami. |
| Decision owner | Sprejme in podpiše odločitev v mejah pooblastila. |
| Appeal reviewer | Obravnava ugovor brez konflikta z izvirno odločitvijo. |
| Rights steward | Preveri lastništvo, dovoljenja in izključitve. |
| Data steward | Varuje osebne, zaupne in občutljive podatke. |

### 6.1 Prepoved samopotrjevanja

Izvajalec ne sme biti edini verifier istega rezultata. Avtor licence ne sme biti edina neodvisna presoja njene pravne skladnosti. CI ni neodvisna pravna presoja; je tehnični kontrolni mehanizem.

### 6.2 Izjava o konfliktu interesov

Preverjevalec mora navesti odnos do predmeta, finančni ali organizacijski interes in morebitno sodelovanje pri nastanku dokaza. Konflikt se ne sme tiho zamolčati.

### 6.3 Stopnje neodvisnosti

- L0 — self-check: samopregled; uporaben za iskanje napak, ne za končni pečat.
- L1 — second-hand: druga oseba v istem projektu, z ločenim pregledom.
- L2 — independent reviewer: oseba, ki ni izvedla spremembe in nima bistvenega konflikta.
- L3 — external specialist: neodvisna zunanja pravna, varnostna, znanstvena ali podatkovno-varstvena presoja.

Pravna veljavnost licence, lastništvo spornih del, osebni podatki in zahtevki o patentih zahtevajo L3, kadar imajo materialne posledice.

## 7. Pravica do signala, ugovora in poštene obravnave

### 7.1 Prijava ni dokaz kršitve

Vsakdo lahko prijavi napako, škodo ali oviro. Prijava sproži preverjanje; sama po sebi ne dokazuje kršitve, namena ali odgovornosti.

### 7.2 Vsebina ugovora

Ugovor naj, kadar je mogoče, navede izpodbijano trditev ali odločitev, predmet in obseg, razpoložljiv dokaz ali razlog, zakaj ga ni mogoče predložiti, predlagani popravek, morebitno nujno tveganje ter kontaktni kanal, če ga želi prijavitelj razkriti.

Anonimna prijava je dovoljena, kadar jo je mogoče varno obdelati. Ne sme se zahtevati razkritje identitete kot pogoj za samo evidentiranje signala.

### 7.3 Procesna zaščita

- Prijavitelj ne sme biti kaznovan zgolj zaradi prijave ali neprijetnega tona.
- Oseba, na katero se prijava nanaša, mora dobiti dovolj informacij, da lahko odgovori, ob upoštevanju zasebnosti in varnosti drugih.
- Dokazi, ki niso bili pregledani, se ne smejo predstaviti kot potrjeni.
- Začasni HOLD je dovoljen le za konkretno tveganje in mora biti sorazmeren, časovno omejen ter ponovno pregledan.
- Odločitev mora navesti dokazni standard, razloge, omejitve in pot ugovora.

### 7.4 Predlagani roki

- potrditev prejema: praviloma v 5 delovnih dneh;
- začetna razvrstitev: praviloma v 10 delovnih dneh;
- utemeljen začetni odgovor ali objavljena utemeljitev odprtega stanja: praviloma v 30 koledarskih dneh.

Rok ni dovoljenje za površno presojo. Kadar se zadeve ne da zaključiti, mora biti objavljen razlog, odgovorna oseba, naslednji datum pregleda in status OPEN ali DISPUTED. Molk ni ugotovitev dejstev.

## 8. Odločanje in dokazno breme

### 8.1 Kdo dokazuje kaj

- Oseba, ki trdi, da ima pravico podeliti licenco, mora pokazati podlago za to pooblastilo.
- Oseba, ki trdi, da je določeno gradivo vključeno v manifest, mora pokazati ujemanje poti, bajtov in obsega.
- Oseba, ki očita kršitev, mora navesti konkretno dejanje in dokazno podlago.
- Oseba, ki zatrjuje dovoljenje ali izjemo, mora navesti konkretno pravno ali pogodbeno podlago, ne zgolj splošne trditve.
- Oseba, ki sprejema odločitev, mora pokazati, kako je obravnavala bistvene dokaze in ugovore.

Dokazno breme mora biti sorazmerno z dostopom do informacij. Od posameznika se ne sme zahtevati dokazovanje dejstev, ki jih nadzira izključno druga stran, ne da bi bila določena primerna pot do teh podatkov.

### 8.2 Minimalni zapis odločitve

Odločitev mora vsebovati decision_id, predmet, odločitev, uporabljeno različico pravil, claim_status, test_result, dokaze, nasprotne dokaze, odgovorne vloge, datum, omejitve, možnost ugovora in datum ponovnega pregleda.

### 8.3 Omejena odločitev

RELEASE_WITH_LIMITATIONS mora jasno povedati, kateri del je dovoljen, kateri del je izključen ali nepreverjen, katere uporabe niso potrjene, kdo nosi odprto tveganje in kdaj je potrebna ponovna presoja. Omejitev ne sme zakriti neodpravljene napake, ki vpliva na sam grant ali identiteto predmeta.

## 9. Popravljanje napak in posledic

### 9.1 Pet ločenih dejanj

1. **Correction:** popravek napačnega zapisa ali trditve.
2. **Restoration:** povrnitev izgubljene ali poškodovane vsebine, pravice ali dostopa, kadar je to mogoče.
3. **Remediation:** sprememba procesa, da se vzrok napake ne ponovi.
4. **Restitution / compensation:** povrnitev koristi ali nadomestilo škode, kadar obstaja ustrezna pravna oziroma pogodbeno veljavna podlaga.
5. **Forgiveness:** osebno ali družbeno priznanje, ki ga register ali plačilo ne more kupiti ali razglasiti namesto prizadetega.

### 9.2 Obvezna vsebina sanacije

Sanacijski zapis mora navesti izvorni padec in njegov identifikator, prizadete predmete, prejemnike in nadaljnje kopije, vzrok in obseg posledice, izvedene popravke, ali je bila popravljena tudi downstream kopija ali izvedeni rezultat, obvestilo prizadetim kadar je potrebno, rezultat ponovnega testa, neodvisnega preverjevalca, preostalo škodo ali omejitev ter datum naslednjega pregleda.

### 9.3 Ne kupuj odpuščanja

- različico prebrati iz enega kanoničnega vira metapodatkov ali jo potrditi proti glavi LICENSE.md;
- ne sme imeti zastarele različice trdo zapisane v kodi;
- popisati vse predmete, ki jih določa politika pokritosti;
- stabilno razvrstiti vnose;
- uporabljati UTF-8 in določeno normalizacijo;
- izračunati velikost in SHA-256 iz dejanskih bajtov;
- v načinu --check vrniti ne-uspeh ob vsakem neskladju.

Generiranje in preverjanje sta različni dejanji. Ustvarjanje novega manifesta ne sme prikriti, da je bil predhodni manifest zastarel; staro stanje mora ostati v zgodovini.

### 3.5 Obvezna inventura

Vsaka izdaja mora ustvariti inventuro, ki razvrsti vse datoteke v obsegu izdaje. Če se popis nanaša samo na del repozitorija, mora biti ta obseg izrecno naveden. Število datotek brez obsega ni dokaz celote.

## 4. Časovna topologija in dokaz dogodka

### 4.1 Časovne vrste

Vsak časovni zapis mora razlikovati:

- EVENT_TIME: kdaj se je dogodek zgodil;
- OBSERVATION_TIME: kdaj ga je opazovalec izmeril;
- RECORD_TIME: kdaj je bil vnos ustvarjen ali shranjen;
- ANCHOR_TIME: kdaj je bil zapis sidran pri neodvisni zunanji storitvi, če je bil;
- VALID_FROM in VALID_UNTIL: obdobje veljavnosti stanja ali dovoljenja.

Časovna oznaka brez določene vrste je nepopolna.

### 4.2 Štirje prejemki

VBL-jev model štirih prejemkov lahko ostane, vendar mora biti vsak prejemek označen z imenom dogodka, uro in njenim virom, časovnim pasom ali odmikom, natančnostjo in znano negotovostjo, osebo ali sistemom, ki je meritev opravil, načinom pridobitve ter statusom meritve.

Če prejemnikovega časa ni mogoče izmeriti, se zabeleži UNVERIFIED ali NOT_MEASURED. Čas se ne ugiba in se ne prepiše iz ure pošiljatelja.

### 4.3 Git in zunanji čas

Git commit, podpisan commit, tag, CI log in zgoščevalna vrednost imajo različne dokazne funkcije. Git časovni metapodatki sami po sebi niso kvalificiran elektronski časovni žig in ne potrjujejo pravne identitete podpisnika. Kadar je potrebna višja stopnja zaupanja v čas, mora evidenca navesti neodvisno časovno sidro, uporabljeno storitev, rezultat validacije in pravno relevantni obseg.

### 4.4 Svežina in ponovljivost

- FRESHNESS_TEST preveri stanje v določenem trenutku.
- REPRODUCIBILITY_TEST preveri, ali se isti postopek ob primerljivih pogojih ponovi.
- CONSISTENCY_TEST preveri, ali več neodvisnih izmer daje združljive rezultate.

Noben od teh testov ne nadomesti drugih.

## 5. Dokazni graf in neodvisnost

### 5.1 Vsaka pomembna trditev ima povezavo do dokazov

Trditev mora imeti claim_id in seznam evidence_id. Dokaz mora imeti izvor, lokacijo, čas dostopa, natančen odlomek ali ponovljiv rezultat, metodo, orodje, različico in omejitve. Če vir ni dostopen, se navede razlog. Nedostopen vir se ne citira kot prebran.

### 5.2 Neodvisnost ni število povezav

Dva vira nista neodvisna zgolj zato, ker imata različna URL-ja. Preverjevalec mora oceniti najmanj:

1. neodvisnost izvora;
2. neodvisnost metode;
3. neodvisnost izvajalca;
4. neodvisnost infrastrukture;
5. konflikt interesov;
6. skupno odvisnost od prvotnega vira;
7. časovno neodvisnost.

Če sta dva članka povzela isti primarni vir, se to zabeleži kot ena dokazna linija z dvema sekundarnima prikazoma, ne kot dve neodvisni potrditvi.

### 5.3 Dokazna moč je vezana na obseg

Vsak dokaz mora navesti, kaj podpira in česa ne podpira. Hash lahko podpira trditev o bajtni istovetnosti; ne podpira trditve o avtorstvu. Test lahko podpira trditev o obnašanju v preizkušenem okolju; ne podpira samodejno trditve o vseh okoljih.

### 5.4 Nasprotni dokazi

Preverjevalec MORA iskati in zabeležiti relevantne nasprotne dokaze, ne samo potrditvenih primerov. Če dokazov ni mogoče pridobiti, mora to postati omejitev sklepa.

## 6. Vloge, neodvisnost in odgovornost

Vsak postopek mora določiti naslednje vloge. Ena oseba lahko opravlja več vlog pri nizkem tveganju samo, če je to izrecno utemeljeno; pri kritičnih odločitvah morajo biti ključne vloge ločene.

| Vloga | Odgovornost |
|---|---|
| Originator | Predloži gradivo ali trditev in razkrije izvor. |
| Executor | Izvede postopek ali spremembo. |
| Verifier | Neodvisno preveri rezultat z navedenimi metodami. |
| Decision owner | Sprejme in podpiše odločitev v mejah pooblastila. |
| Appeal reviewer | Obravnava ugovor brez konflikta z izvirno odločitvijo. |
| Rights steward | Preveri lastništvo, dovoljenja in izključitve. |
| Data steward | Varuje osebne, zaupne in občutljive podatke. |

### 6.1 Prepoved samopotrjevanja

Izvajalec ne sme biti edini verifier istega rezultata. Avtor licence ne sme biti edina neodvisna presoja njene pravne skladnosti. CI ni neodvisna pravna presoja; je tehnični kontrolni mehanizem.

### 6.2 Izjava o konfliktu interesov

Preverjevalec mora navesti odnos do predmeta, finančni ali organizacijski interes in morebitno sodelovanje pri nastanku dokaza. Konflikt se ne sme tiho zamolčati.

### 6.3 Stopnje neodvisnosti

- L0 — self-check: samopregled; uporaben za iskanje napak, ne za končni pečat.
- L1 — second-hand: druga oseba v istem projektu, z ločenim pregledom.
- L2 — independent reviewer: oseba, ki ni izvedla spremembe in nima bistvenega konflikta.
- L3 — external specialist: neodvisna zunanja pravna, varnostna, znanstvena ali podatkovno-varstvena presoja.

Pravna veljavnost licence, lastništvo spornih del, osebni podatki in zahtevki o patentih zahtevajo L3, kadar imajo materialne posledice.

## 7. Pravica do signala, ugovora in poštene obravnave

### 7.1 Prijava ni dokaz kršitve

Vsakdo lahko prijavi napako, škodo ali oviro. Prijava sproži preverjanje; sama po sebi ne dokazuje kršitve, namena ali odgovornosti.

### 7.2 Vsebina ugovora

Ugovor naj, kadar je mogoče, navede izpodbijano trditev ali odločitev, predmet in obseg, razpoložljiv dokaz ali razlog, zakaj ga ni mogoče predložiti, predlagani popravek, morebitno nujno tveganje ter kontaktni kanal, če ga želi prijavitelj razkriti.

Anonimna prijava je dovoljena, kadar jo je mogoče varno obdelati. Ne sme se zahtevati razkritje identitete kot pogoj za samo evidentiranje signala.

### 7.3 Procesna zaščita

- Prijavitelj ne sme biti kaznovan zgolj zaradi prijave ali neprijetnega tona.
- Oseba, na katero se prijava nanaša, mora dobiti dovolj informacij, da lahko odgovori, ob upoštevanju zasebnosti in varnosti drugih.
- Dokazi, ki niso bili pregledani, se ne smejo predstaviti kot potrjeni.
- Začasni HOLD je dovoljen le za konkretno tveganje in mora biti sorazmeren, časovno omejen ter ponovno pregledan.
- Odločitev mora navesti dokazni standard, razloge, omejitve in pot ugovora.

### 7.4 Predlagani roki

- potrditev prejema: praviloma v 5 delovnih dneh;
- začetna razvrstitev: praviloma v 10 delovnih dneh;
- utemeljen začetni odgovor ali objavljena utemeljitev odprtega stanja: praviloma v 30 koledarskih dneh.

Rok ni dovoljenje za površno presojo. Kadar se zadeve ne da zaključiti, mora biti objavljen razlog, odgovorna oseba, naslednji datum pregleda in status OPEN ali DISPUTED. Molk ni ugotovitev dejstev.

## 8. Odločanje in dokazno breme

### 8.1 Kdo dokazuje kaj

- Oseba, ki trdi, da ima pravico podeliti licenco, mora pokazati podlago za to pooblastilo.
- Oseba, ki trdi, da je določeno gradivo vključeno v manifest, mora pokazati ujemanje poti, bajtov in obsega.
- Oseba, ki očita kršitev, mora navesti konkretno dejanje in dokazno podlago.
- Oseba, ki zatrjuje dovoljenje ali izjemo, mora navesti konkretno pravno ali pogodbeno podlago, ne zgolj splošne trditve.
- Oseba, ki sprejema odločitev, mora pokazati, kako je obravnavala bistvene dokaze in ugovore.

Dokazno breme mora biti sorazmerno z dostopom do informacij. Od posameznika se ne sme zahtevati dokazovanje dejstev, ki jih nadzira izključno druga stran, ne da bi bila določena primerna pot do teh podatkov.

### 8.2 Minimalni zapis odločitve

Odločitev mora vsebovati decision_id, predmet, odločitev, uporabljeno različico pravil, claim_status, test_result, dokaze, nasprotne dokaze, odgovorne vloge, datum, omejitve, možnost ugovora in datum ponovnega pregleda.

### 8.3 Omejena odločitev

RELEASE_WITH_LIMITATIONS mora jasno povedati, kateri del je dovoljen, kateri del je izključen ali nepreverjen, katere uporabe niso potrjene, kdo nosi odprto tveganje in kdaj je potrebna ponovna presoja. Omejitev ne sme zakriti neodpravljene napake, ki vpliva na sam grant ali identiteto predmeta.

## 9. Popravljanje napak in posledic

### 9.1 Pet ločenih dejanj

1. **Correction:** popravek napačnega zapisa ali trditve.
2. **Restoration:** povrnitev izgubljene ali poškodovane vsebine, pravice ali dostopa, kadar je to mogoče.
3. **Remediation:** sprememba procesa, da se vzrok napake ne ponovi.
4. **Restitution / compensation:** povrnitev koristi ali nadomestilo škode, kadar obstaja ustrezna pravna oziroma pogodbeno veljavna podlaga.
5. **Forgiveness:** osebno ali družbeno priznanje, ki ga register ali plačilo ne more kupiti ali razglasiti namesto prizadetega.

### 9.2 Obvezna vsebina sanacije

Sanacijski zapis mora navesti izvorni padec in njegov identifikator, prizadete predmete, prejemnike in nadaljnje kopije, vzrok in obseg posledice, izvedene popravke, ali je bila popravljena tudi downstream kopija ali izvedeni rezultat, obvestilo prizadetim kadar je potrebno, rezultat ponovnega testa, neodvisnega preverjevalca, preostalo škodo ali omejitev ter datum naslednjega pregleda.

### 9.3 Ne kupuj odpuščanja

Povračilo koristi ali nadomestilo škode je lahko del sanacije, nikoli pa samodejno dokaz, da je prizadeti odpustil, privolil ali izgubil pravico do nadaljnjega ugovora. Plačilo ne izbriše zgodovine; zgodovina pa ne sme postati izgovor za neskončno kaznovanje po uspešni sanaciji.

### 9.4 Ne označuj ljudi kot napak

Register ocenjuje ravnanja, vire, odločitve in posledice. Ne razglaša celotnega človeka za zlega, nevarnega ali manj vrednega. Klasifikacija se nanaša na dokazano dejanje, ne na bistvo osebe.

## 10. Zasebnost, hramba in brazgotine

### 10.1 Javni register ni skladišče vseh podatkov

Javni register mora vsebovati najmanjši obseg podatkov, potreben za sledljivost. Osebni podatki, zaupna vsebina, kontaktni podatki prijaviteljev, zdravstveni podatki in drugi občutljivi podatki se ne objavijo samo zato, ker je zapis označen kot dokaz.

### 10.2 Hash ni anonimizacija

Zgoščevalna vrednost, identifikator, sol ali psevdonim lahko še vedno omogočajo povezavo z osebo ali drugim podatkom. Pred objavo je treba oceniti, ali zapis po razumnih sredstvih omogoča identifikacijo.

### 10.3 Dvoslojna evidenca

- **Javna plast:** identifikator dogodka, vrsta napake, časovni okvir, status, popravek, dokazni povzetek in javni hash, kadar je varen.
- **Omejena plast:** izvorni osebni podatki, celotni dokazi, kontaktni podatki, podrobnosti o varnostnih incidentih in druga občutljiva gradiva; dostop je omejen in evidentiran.

Kadar je mogoče, se osebni podatki hranijo ločeno od javne evidence. Javna brazgotina lahko ostane, ne da bi javno razkrila osebne podatke.

### 10.4 Popravek in izbris

Append-only zgodovina ni dovoljenje za nezakonito hrambo osebnih podatkov. Če je treba osebne podatke popraviti ali izbrisati, se popravi ali odstrani osebni podatek v ustreznem sistemu; javni zapis lahko ohrani neidentifikacijski dogodek popravka, če za to obstaja ustrezna podlaga.

Vsaka uporaba nespremenljivega registra ali verige, ki vsebuje ali omogoča povezavo z osebnimi podatki, zahteva predhodno presojo primernosti, minimizacije, hrambe, odgovornosti in pravic posameznikov.

## 11. Avtorske pravice, TDM, AI in pravna združljivost

### 11.1 Najprej ugotovi imetništvo pravic

Preden VBL določi, da je gradivo zajeto ali da je uporaba prepovedana, mora navesti, kdo je avtor, kdo je imetnik ustrezne pravice, ali gre za skupno delo, ali je gradivo licencirano od tretje osebe, katere pravice je mogoče podeliti, katere pravice so izključene ter ali obstajajo osebnostne, podatkovne, znamčne ali patentne pravice.

VBL ne sme podeliti pravic, ki jih izdajatelj nima.

### 11.2 TDM mora biti obravnavan po vrsti uporabe in pravni podlagi

Splošna izjava, da je »vse v repozitoriju rezervirano za vse oblike rudarjenja«, ni dovolj natančen nadomestek za presojo posameznega gradiva, imetništva pravic in zakonskih izjem.

Za Slovenijo je pomemben ZASP, zlasti 57.a člen o besedilnem in podatkovnem rudarjenju. Pridržek pravic za uporabo po pravilih tega člena mora biti izrecen in ustrezno izražen; zakon kot primer omenja standardizirana strojno berljiva sredstva za spletno dostopna dela. Varnostni ukrepi ne smejo biti nesorazmerni ali onemogočiti zakonito dovoljenega rudarjenja, določbe v nasprotju s tem členom pa so nične.

VBL mora ločeno obravnavati:

- pravice in izjemo iz člena 4 Direktive (EU) 2019/790;
- izjemo za znanstvenoraziskovalni TDM iz člena 3 iste direktive;
- ustrezne nacionalne določbe ZASP;
- druge zakonske izjeme ali omejitve;
- gradivo tretjih oseb, za katero izdajatelj nima pravic.

Pridržek po členu 4 ne sme biti predstavljen kot odprava izjeme po členu 3. Nobena licenca ne more z lastno izjavo razveljaviti kogentne zakonske izjeme.

### 11.3 AI Act ni splošna licenca za prepoved vsega učenja

Člen 53(1)(c) Uredbe (EU) 2024/1689 določa posebno obveznost za **ponudnike modelov umetne inteligence za splošne namene (GPAI)**: vzpostaviti politiko skladnosti s pravom EU o avtorskih in sorodnih pravicah ter prepoznati in spoštovati ustrezno izražene pridržke pravic po členu 4(3) Direktive 2019/790. Obveznosti iz poglavja V, kamor spada člen 53, se uporabljajo od **2. avgusta 2025**; nadzorna pooblastila za izvajanje teh obveznosti se uporabljajo od **2. avgusta 2026**. Ponudniki GPAI modelov, ki so bili dani na trg pred 2. avgustom 2025, morajo potrebne korake za skladnost izvesti do **2. avgusta 2027**. Ta režim ni splošno pravilo, da je vsak uporabnik ali vsak model avtomatično podvržen vsakemu besedilu pridržka. Standard mora navesti konkretnega naslovnika, vrsto modela, zadevni pravni režim in prehodno obdobje.

### 11.4 Open source ni isto kot source-available

Če licenca omejuje uporabo glede na področje dejavnosti, osebo ali skupino, je treba preveriti skladnost z Open Source Definition. OSI Open Source Definition med drugim prepoveduje diskriminacijo oseb, skupin in področij uporabe. Če VBL ohrani omejitve, ki niso skladne s temi pogoji, se ne sme označiti kot OSI-approved open-source licence. Izraz source-available ali ethical source licence je lahko poštenejši, kadar ustreza dejanskemu pravnemu besedilu.

### 11.5 Izbira licence po vrsti gradiva

VBL ne sme avtomatično postati najboljša licenca za vse predmete. Pred vsako izdajo se opravi izbor:

| Gradivo | Možna izhodišča za primerjavo | Ključna vprašanja |
|---|---|---|
| Programska koda | Apache-2.0, MIT, BSD, MPL-2.0, GPL-3.0, AGPL-3.0 | Patenti, copyleft, distribucija, omrežna uporaba, združljivost. |
| Dokumentacija in besedila | CC BY 4.0, CC BY-SA 4.0 ali pridržane pravice | Pripis, predelave, komercialna uporaba, tretje osebe. |
| Podatkovne zbirke | CC BY, ODbL ali posebna pogodba, odvisno od pravic | Avtorska pravica, sui generis pravica, izvor, osebni podatki. |
| Modeli, uteži in evalvacijski sklopi | Ločeno preverjeni pogoji za kodo, uteži, podatke in izhod | Imetništvo uteži, pravice do učenja, izhodne omejitve, varnost. |
| Zasebni korpusi in osebni podatki | Namenska pogodba, zakonska podlaga in nadzor dostopa | Privolitev, pravna podlaga, omejitev namena, hramba, dostop. |

MIT, Apache, GPL, CC in ODbL niso medsebojno zamenljive. Uporabi se najprimernejši uveljavljeni instrument, kadar bolje izpolni cilj kot VBL. VBL lahko ostane ločen evidenčni standard tudi takrat, ko je samo gradivo objavljeno pod drugo licenco.

### 11.6 Patent in znamka

Odsotnost patentne licence v VBL ne pomeni svobode pred tujimi patenti. Prav tako zgodovina imena ali rodovnik projekta ne dajeta samodejne pravice do uporabe tuje znamke. To mora biti navedeno v pravicni matriki.

### 11.7 Predhodno podeljene pravice

Sprememba nove različice ne sme biti predstavljena kot avtomatični preklic pravic, ki so bile že veljavno podeljene pod prejšnjo različico. Vsak prehod med različicami mora navesti, katera različica velja za novo uporabo, katera ostaja podlaga že prejetih kopij, ali je sprememba razširitev, omejitev ali pojasnilo, kdo je imel pooblastilo spremembo sprejeti in kateri prejemniki so bili obveščeni.

## 12. Znanstvene, matematične in semantične trditve

### 12.1 Metoda pred rezultatom

Vsaka znanstvena ali matematična trditev mora navesti hipotezo, definicije, vhodne podatke oziroma korpus, algoritem, orodje in različico, parametre, kontrolno skupino ali primerjavo kadar je smiselna, statistično metodo in negotovost ter omejitve in alternativne razlage.

### 12.2 Ontogematria in simbolne transformacije

Ontogematria je lahko raziskovalna ali interpretativna metoda, vendar se rezultat ne sme predstavljati kot splošno sprejeto matematično, semantično ali znanstveno dejstvo, razen če je ustrezno utemeljen. Vsaka transformacija mora objaviti preslikavo, pravila, korpus, izvedbo, teste in neodvisno ponovitev.

Številčna struktura ne nadomesti pomena; pomen ne nadomesti meritve.

### 12.3 Neologizem ni samodejno napaka

Odsotnost besede v slovarju ni zadosten dokaz, da je beseda napačna ali izmišljena. Preverjanje mora razlikovati med neologizmom, strokovnim izrazom, narečno obliko, lastnim imenom, napako in nedokumentirano rabo. Negotovost ostane označena, dokler ni razrešena.

## 13. Izdajni prehod — Release Gate 0.1540

Izdaja je večdimenzionalna odločitev. Vsi obvezni kontrolni elementi morajo imeti rezultat, dokaz in odgovorno vlogo. Kritični element v stanju NOT_RUN, UNVERIFIED, FAIL ali UNKNOWN ne sme biti tiho obravnavan kot uspešen.

### 13.1 Skupine kontrol

| Skupina | Kontrola | Problem, ki ga rešuje | Dokaz za PASS |
|---|---|---|---|
| G0 | Pooblastilo za izdajo | Neznano, kdo je smel izdati novo različico. | Zapis pooblastila in podpis odločevalca. |
| G1 | Identiteta telesa | Stari hash ali velikost v Machine record. | Ponovni izračun SHA-256 in velikosti iz objavljene datoteke. |
| G2 | Manifest za vsak repozitorij | Manifest v eni hiši ne pokrije druge hiše. | Manifest v vsakem repozitoriju ali veljavna izrecna skupna shema. |
| G3 | Pokritost datotek | Nejasno, katere datoteke so licencirane. | Vsaka relevantna datoteka ima status in dokaz pravic. |
| G4 | Generator manifesta | Trdo zapisano zastarelo različico. | Generator pridobi različico iz kanoničnega vira in prestane test. |
| G5 | Veriga različic | Luknje, napačen predhodnik ali retroaktivna zamenjava. | Veriga commitov in seznam različic se ujemata. |
| G6 | Spremljevalci | Spremljevalni dokument je naveden, vendar nedosegljiv. | Vsak spremljevalec ima pot, commit, različico in digest. |
| G7 | Pravice in izključitve | Licenca zajame gradivo, za katero izdajatelj nima pravic. | Rights matrix, dokaz imetništva in tretjeosebni izključki. |
| G8 | TDM/AI pridržek | Splošna izjava presega lastništvo ali zakonske izjeme. | Po sredstvih izražen pridržek, obseg po datoteki in pravni pregled. |
| G9 | Zasebnost | Javna brazgotina razkrije osebne podatke. | Pregled minimizacije, dostopa, hrambe in pravne podlage. |
| G10 | Neodvisnost | Izvajalec potrdi lastno delo. | Ločene vloge, izjava o konfliktu in podpis druge roke. |
| G11 | Ugovori | Prijava je predstavljena kot potrjena kršitev. | Evidenca odgovora, nasprotnih dokazov in pritožbe. |
| G12 | Sanacija | Zapis popravka brez preverbe posledice. | Preizkus downstream popravka in neodvisna potrditev. |
| G13 | Časovni podatki | Čas meritve je zamenjan s časom dogodka. | Časovna shema z vrsto časa, virom in negotovostjo. |
| G14 | Tehnični testi | Testni rezultat je zatrjevan, ne izveden. | Ponovljiv ukaz, izpis, okolje in CI povezava. |
| G15 | Dostopnost in jezik | Ključni pogoji niso razumljivi prejemniku. | Slovenska in angleška berba, pregled semantike in dostopnosti. |
| G16 | Zunanji pravni pregled | Pravna trditev je predstavljena kot potrjena brez strokovnjaka. | Neodvisen pravni pregled z obsegom, datumom in omejitvami. |
| G17 | Končna odločitev | PASS testi so zamenjani z RELEASE. | Ločen podpisani zapis odločitve. |

### 13.2 Pogoji odločitve

**RELEASE** je dovoljen samo, če G0–G15 so PASS ali dokumentirano NOT_APPLICABLE; G7 in G8 nimata odprtega spora o lastništvu ali obsegu; G9 je opravljen, kadar se obdelujejo osebni podatki; G10 je opravljen; G12 je opravljen za vsak popravek, ki se razglaša kot zaključen; G16 je opravljen, kadar izdaja spreminja ali uveljavlja pravne pogoje, katerih razlaga je materialno pomembna; in G17 je podpisan.

**RELEASE_WITH_LIMITATIONS** je dovoljen samo, če odprta vprašanja ne ogrožajo identitete gradiva, pooblastila za podelitev pravic, zakonske izjeme, zasebnosti ali bistvenega pomena granta. Omejitve morajo biti izrecne.

**HOLD** je obvezen, če se ne ujemajo bajti, različica, manifest, pravice ali bistveni pogoji.

**WITHDRAW** se uporabi, kadar je že objavljen predmet dokazano napačen ali škodljiv v takem obsegu, da nadaljnja distribucija ni sprejemljiva. Umik ne izbriše zgodovine.

## 14. Obvezni testi

Vsak spodnji test mora imeti lasten test_id, vhod, pričakovani in dejanski izid ter status. Testi so zahteve za izvedbo; ta osnutek ne trdi, da so bili že izvedeni.

| Test | Preizkus | Pričakovani izid |
|---|---|---|
| T-001 | Parse LICENSE-MANIFEST.json | Veljaven UTF-8 JSON in obvezna polja. |
| T-002 | Preverba velikosti in SHA-256 vsakega navedenega predmeta | Natančno ujemanje z bajti. |
| T-003 | Pregled vseh datotek v obsegu repozitorija | Nobena datoteka brez statusa pokritosti. |
| T-004 | Ujemanje različice manifesta z LICENSE.md | Enaka različica in datum v kanoničnem zapisu. |
| T-005 | Manifest vsake hiše | Vsak repozitorij ima svoj preverljiv manifest ali izrecno dogovorjeno skupno evidenco. |
| T-006 | Ujemanje commitov | Evidenca izdaje kaže na commit, iz katerega so bile datoteke dejansko prebrane. |
| T-007 | Spremljevalci | Vsi navedeni spremljevalci so dosegljivi in pravilno označeni. |
| T-008 | Machine record | Hash, bajti, vrstice in commit se ponovno izračunajo iz istega stanja. |
| T-009 | Binarno telo | Round-trip je bajtno istoveten; rezultat ne trdi več, kot test dokazuje. |
| T-010 | Časovna polja | EVENT_TIME, OBSERVATION_TIME in RECORD_TIME se ne zamenjujejo. |
| T-011 | Neznana trditev | Brez vira ostane UNKNOWN ali UNVERIFIED, ne PASS. |
| T-012 | Neodvisna druga roka | Ista oseba ne more biti edini izvajalec in verifier. |
| T-013 | Konflikt interesov | Konflikt je razkrit in razrešen ali naveden kot omejitev. |
| T-014 | Nasprotni dokaz | Pregled zajame vsaj en poskus ovržbe pri pomembnih trditvah. |
| T-015 | Zasebnost | Javni zapis ne vsebuje nepotrebnih osebnih podatkov ali razkritih skrivnosti. |
| T-016 | Ugovor | Prijava ne spremeni statusa v CONTRADICTED brez preverbe. |
| T-017 | Sanacija | Popravek ni označen VERIFIED_REPAIRED brez downstream testa. |
| T-018 | TDM obseg | Pridržek ne zajame tretjeosebnega ali neidentificiranega gradiva brez pooblastila. |
| T-019 | Zakonske izjeme | Evidenca razlikuje med TDM, raziskovalnimi izjemami in drugimi pravnimi podlagami. |
| T-020 | OSI trditev | Nobena različica se ne označi za OSI-approved brez ustrezne odobritve in skladnosti. |
| T-021 | Licenčna združljivost | Vsaka konkretna kombinacija ima pravno analizo, ne samo skupen rodovnik. |
| T-022 | Retroaktivnost | Sprememba ne trdi samodejnega preklica že veljavno podeljenih pravic. |
| T-023 | Generator manifesta | Generator ne vsebuje trdo zapisane stare različice. |
| T-024 | Zastareli spremljevalni dokumenti | Stare oznake v README, CANONICAL, RELEASE-GATE in registrih so odkrite. |
| T-025 | Izhodno poročilo | Poročilo loči claim_status, test_result in decision. |
| T-026 | Zunanji pravni pregled | Pravne trditve imajo zabeležen obseg pregleda in omejitve. |
| T-027 | Ponovljivost | Isti test se lahko ponovi z opisanimi vhodi in orodjem. |
| T-028 | Umik | Umik ohrani zgodovino, omeji distribucijo in obvesti ustrezne prejemnike. |
| T-029 | Pooblastilo za izdajo | Izdajni zapis identificira avtorja/pooblaščenca, obseg pooblastila, predmet in odobreno različico. |
| T-030 | Pravice po posameznem sredstvu | Vsak predmet ima preverljivega imetnika pravic, podlago dovoljenja ali izrecno izključitev; neznano pooblastilo blokira grant. |
| T-031 | Zasebnost in hramba | Javni register vsebuje samo nujne podatke; omejena plast ima določen dostop, pravno podlago in rok hrambe. |
| T-032 | Usklajenost med repozitoriji | LICENSE.md, manifesti, registri in commit-i v vseh navedenih hišah se ujemajo z deklarirano skupno/ločenо shemo. |
| T-033 | TDM pridržek in izjeme | Pridržek je vezan na gradivo, imetnika pravic, način objave in ustrezno zakonsko izjemo; zakonite izjeme niso zanikane. |
| T-034 | Odločitev izdajnega prehoda | Noben RELEASE ni ustvarjen, če katera koli blokirna kontrola ni PASS ali utemeljeno NOT_APPLICABLE. |

## 15. Evidenčni zapis — minimalna podatkovna pogodba

Vsak pomemben zapis mora vsebovati vsaj naslednja polja. Primer je ilustrativen; prazne vrednosti pomenijo UNKNOWN, NOT_RUN ali neizpolnjeno polje, ne pa potrditve.

~~~json
{
  "schema": "vbl-evidence-record-1.0-draft",
  "record_id": "REC-YYYY-NNNN",
  "record_type": "CLAIM|EVIDENCE|INTERPRETATION|DECISION|ACTION|CONSEQUENCE|REPAIR",
  "claim_id": "CLM-YYYY-NNNN",
  "statement": "Natančna trditev, ki se presoja.",
  "scope": {
    "repository": "owner/repository",
    "path": "relative/path",
    "commit": "full_commit_sha",
    "asset_sha256": "sha256_hex",
    "size_bytes": 0
  },
  "claim_status": "UNKNOWN",
  "test_result": "NOT_RUN",
  "decision": "HOLD",
  "evidence": [
    {
      "evidence_id": "EVD-001",
      "source": "https://example.invalid/source",
      "source_type": "PRIMARY|SECONDARY|TEST_OUTPUT|REGISTER|EXTERNAL_ANCHOR",
      "verbatim_locator": "page/line/section/timecode",
      "accessed_at": null,
      "sha256": null,
      "method": null,
      "tool": null,
      "tool_version": null,
      "limitations": ["not independently reviewed"]
    }
  ],
  "temporal": {
    "event_time": null,
    "observation_time": null,
    "record_time": null,
    "anchor_time": null,
    "valid_from": null,
    "valid_until": null,
    "clock_source": null,
    "precision": null,
    "uncertainty": null
  },
  "roles": {
    "originator": null,
    "executor": null,
    "verifier": null,
    "decision_owner": null,
    "appeal_reviewer": null
  },
  "independence": {
    "source": "UNKNOWN",
    "method": "UNKNOWN",
    "operator": "UNKNOWN",
    "infrastructure": "UNKNOWN",
    "conflict_of_interest": "NOT_ASSESSED"
  },
  "privacy": {
    "classification": "PUBLIC|INTERNAL|RESTRICTED|SPECIAL_CATEGORY",
    "public_fields_reviewed": false,
    "lawful_basis_recorded": false,
    "retention_rule": null,
    "restricted_evidence_ref": null
  },
  "limitations": [],
  "repair": {
    "state": "OPEN",
    "affected_copies": [],
    "downstream_test": "NOT_RUN",
    "verified_by": null
  }
}
~~~

Produkcijska shema mora validirati tipe, dovoljene vrednosti, zahtevana polja in povezave med identifikatorji.

## 16. Ugotovitve o javnem stanju 0.1530 — začetni zapis za sanacijo

To je začetni inventurni zapis tega osnutka, ne neodvisna revizija celotnega sistema. Stanja so vezana na pregled javno dosegljivih datotek 14. novembra 2026.

| ID | Ugotovitev | Dokazna osnova | Stanje | Zahtevana sanacija |
|---|---|---|---|---|
| F-001 | Machine record v LICENSE.md še navaja staro meritev: 186.349 B, SHA-256 c83ddc…, commit 71d97c… z dne 7. 11. | Besedilo Machine record v javni LICENSE.md; datoteka v glavni veji ima velikost 193.317 B in novejši commit. | FAIL — zapis je zastarel glede na objavljeno telo. | Ponovno izmeriti objavljeno vsebino na točno določenem commitu in zamenjati trenutno identifikacijo; stari zapis ohraniti kot zgodovinski. |
| F-002 | LICENSE-MANIFEST.json obstaja v metodološkem repozitoriju, ne pa v korenski mapi SYMBOLON-KATHOLIKON. | GitHub drevesi obeh javnih repozitorijev. | FAIL za lokalno identifikacijo v SYMBOLON-KATHOLIKON; prisotnost v drugi hiši je potrjena. | Dodati lokalni manifest ali izrecno spremeniti pravilo §0a in dokazati skupno identifikacijsko shemo. |
| F-003 | Manifest v metodološkem repozitoriju našteva LICENSE.md in dva registra; ne popisuje vseh datotek repozitorija. | LICENSE-MANIFEST.json, items. | PARTIAL — veljavnost obsega je treba izrecno odločiti. | Vzpostaviti popoln statusni inventar datotek; določiti, kaj je licencirano, izključeno, tretjeosebno ali generirano. |
| F-004 | scripts/manifest_gen.py še vedno trdo zapisuje različico 0.1210 × 10⁴. | Javno objavljena skripta na main. | FAIL — generator lahko ustvari zastarel metapodatek. | Različico pridobiti iz kanoničnega vira in dodati regresijski test. |
| F-005 | CANONICAL.md še vedno opisuje LICENSE.md kot VBL 0.1210 × 10⁴. | Javno objavljen CANONICAL.md. | FAIL — podporna deklaracija je zastarela. | Posodobiti šele po potrditvi avtorja; povezati jo na izmerjeno izdajo. |
| F-006 | RELEASE-GATE.md je še vedno naslovljen kot VBL 10.3.x. | Javno objavljen RELEASE-GATE.md. | FAIL za trenutni obseg izdaje. | Zamenjati z gate 0.1540 ali ga jasno arhivirati kot zgodovinski gate. |
| F-007 | preverba.py in test_preverba.py preverjata promocijski osnutek, ne popolnosti licenčnega izdajnega paketa. | Vsebina skripte, testov in workflow tests.yml. | PARTIAL — obstoječi test je uporaben, vendar ima omejen obseg. | Dodati ločen validator licence, manifesta, pravic, zasebnosti, odločitve in sanacije. |
| F-008 | TDM-RESERVATION.md govori o rezervaciji all-content, manifest pa identificira samo tri predmete. | TDM-RESERVATION.md in LICENSE-MANIFEST.json. | DISPUTED / HOLD — obseg pravic in tretjeosebne izključitve niso usklajeni. | Uvesti TDM register po gradivu, imetniku pravic, pravni podlagi in zakonski izjemi. |
| F-009 | LICENSE.md našteva sedem spremljevalnih dokumentov z več hišami; pregledani korenski drevesi jih ne vsebujejo na vseh navedenih poteh. | Seznam spremljevalcev v LICENSE.md in drevesi obeh repozitorijev. | UNVERIFIED glede drugih hiš; NOT_FOUND na pregledanih poteh. | Za vsak spremljevalni dokument navesti dejanski repozitorij, pot, commit, različico in digest. |
| F-010 | VBL-jeva analiza licenčnih družin ne sme prikazovati GPL kot splošno trajno izgubo pravic. | GPLv3 §8 vsebuje mehanizem ponovne vzpostavitve pravic pod določenimi pogoji. | CONTRADICTED, če se trditev nanaša na GPLv3 brez kvalifikacije. | Popraviti opis §0.41; razlikovati VBL-jev pogodbeni popravek od pravil posamezne licence. |
| F-011 | Trditev all-content TDM reservation mora spoštovati pravice tretjih oseb in zakonske izjeme. | ZASP 57.a, DSM 2019/790 člena 3 in 4, TDM-RESERVATION.md. | HOLD za širše pravne trditve, dokler ni asset-level pregled. | Določiti obseg, pravice, pridržek in izjeme za vsak predmet. |
| F-012 | Etične omejitve je treba razlikovati od OSI open-source statusa. | OSI Open Source Definition, zlasti merili 5 in 6. | PARTIAL — opis statusa mora biti izrecen. | Ne uporabljati oznake OSI-approved brez formalne odobritve in skladnosti. |

### 16.1 Pomembna poprava prejšnje presoje

Manifest ni neobstoječ v celotnem sistemu: najden je v repozitoriju verification-before-assertion. Natančna ugotovitev je, da ni prisoten na korenski poti druge hiše SYMBOLON-KATHOLIKON, čeprav ta hiša nosi svojo kopijo LICENSE.md. To je pomembna razlika in jo je treba ohraniti v registru.

### 16.2 Identifikatorji Git niso SHA-256

Isti Git blob ID za LICENSE.md v obeh repozitorijih je dokaz, da Git ta objekta obravnava kot isti blob. To ni isto polje kot SHA-256 vsebine v LICENSE-MANIFEST.json. Strojni zapis mora vsako vrsto identifikatorja pravilno poimenovati.

## 17. Dodelitev problemov rešitvam

| Problem | Rešitev | Lastnik izvedbe | Minimalni dokaz | Blokira izdajo? |
|---|---|---|---|---|
| P-001 Zastarela identifikacija | R-001 Canonical Artifact Gate | Executor + verifier | Aktualni SHA-256, velikost, commit in test | DA |
| P-002 Manifest manjka v eni hiši | R-002 Per-Repository Manifest | Rights steward | Lokalni manifest in CI | DA |
| P-003 Nepopoln obseg datotek | R-003 Coverage Inventory | Rights steward | Status vsake datoteke | DA |
| P-004 Generator trdo zapisuje staro različico | R-004 Dynamic Version Binding | Maintainer + verifier | Test generatorja | DA |
| P-005 Zastarela podporna dokumentacija | R-005 Companion Synchronization | Document owner | Poti, verzije in digesti | DA za trditve, ki vplivajo na grant |
| P-006 Zmeda med testom in pravno presojo | R-006 Three-Axis Status Model | Standard owner | Ločena claim/test/decision polja | DA |
| P-007 Samopotrjevanje | R-007 Independent Review | Reviewer | Izjava o neodvisnosti in pregled | DA |
| P-008 Nejasna TDM rezervacija | R-008 Asset-Level TDM Register | Rights steward + lawyer | Asset-level pravice in pravna analiza | DA za TDM trditve |
| P-009 Preširoke etične omejitve | R-009 Operational Ethics Criteria | Standard owner + external reviewers | Primeri, inter-rater test, appeal | DA, če pogoji omejujejo grant |
| P-010 Zasebnost v registrih | R-010 Privacy-Preserving Ledger | Data steward | Minimizacija, podlaga, hramba | DA, kadar so osebni podatki prisotni |
| P-011 Pritožba zamenjana za dokaz | R-011 Safe Objection Process | Decision owner | Ugovor, odgovor, dokazna presoja | DA |
| P-012 Popravek brez odprave posledice | R-012 Consequence Repair Test | Executor + independent verifier | Downstream test in prejemniki | DA za zaprtje popravka |
| P-013 Nejasna združljivost licenc | R-013 License Compatibility Matrix | Rights steward + lawyer | Konkretna kombinacija in pogoji | DA za kombinirano distribucijo |
### 16.1 Pomembna poprava prejšnje presoje

Manifest ni neobstoječ v celotnem sistemu: najden je v repozitoriju verification-before-assertion. Natančna ugotovitev je, da ni prisoten na korenski poti druge hiše SYMBOLON-KATHOLIKON, čeprav ta hiša nosi svojo kopijo LICENSE.md. To je pomembna razlika in jo je treba ohraniti v registru.

### 16.2 Identifikatorji Git niso SHA-256

Isti Git blob ID za LICENSE.md v obeh repozitorijih je dokaz, da Git ta objekta obravnava kot isti blob. To ni isto polje kot SHA-256 vsebine v LICENSE-MANIFEST.json. Strojni zapis mora vsako vrsto identifikatorja pravilno poimenovati.

## 17. Dodelitev problemov rešitvam

| Problem | Rešitev | Lastnik izvedbe | Minimalni dokaz | Blokira izdajo? |
|---|---|---|---|---|
| P-001 Zastarela identifikacija | R-001 Canonical Artifact Gate | Executor + verifier | Aktualni SHA-256, velikost, commit in test | DA |
| P-002 Manifest manjka v eni hiši | R-002 Per-Repository Manifest | Rights steward | Lokalni manifest in CI | DA |
| P-003 Nepopoln obseg datotek | R-003 Coverage Inventory | Rights steward | Status vsake datoteke | DA |
| P-004 Generator trdo zapisuje staro različico | R-004 Dynamic Version Binding | Maintainer + verifier | Test generatorja | DA |
| P-005 Zastarela podporna dokumentacija | R-005 Companion Synchronization | Document owner | Poti, verzije in digesti | DA za trditve, ki vplivajo na grant |
| P-006 Zmeda med testom in pravno presojo | R-006 Three-Axis Status Model | Standard owner | Ločena claim/test/decision polja | DA |
| P-007 Samopotrjevanje | R-007 Independent Review | Reviewer | Izjava o neodvisnosti in pregled | DA |
| P-008 Nejasna TDM rezervacija | R-008 Asset-Level TDM Register | Rights steward + lawyer | Asset-level pravice in pravna analiza | DA za TDM trditve |
| P-009 Preširoke etične omejitve | R-009 Operational Ethics Criteria | Standard owner + external reviewers | Primeri, inter-rater test, appeal | DA, če pogoji omejujejo grant |
| P-010 Zasebnost v registrih | R-010 Privacy-Preserving Ledger | Data steward | Minimizacija, podlaga, hramba | DA, kadar so osebni podatki prisotni |
| P-011 Pritožba zamenjana za dokaz | R-011 Safe Objection Process | Decision owner | Ugovor, odgovor, dokazna presoja | DA |
| P-012 Popravek brez odprave posledice | R-012 Consequence Repair Test | Executor + independent verifier | Downstream test in prejemniki | DA za zaprtje popravka |
| P-013 Nejasna združljivost licenc | R-013 License Compatibility Matrix | Rights steward + lawyer | Konkretna kombinacija in pogoji | DA za kombinirano distribucijo |
| P-014 Znanstvena trditev brez ponovljive metode | R-014 Reproducible Method Card | Research owner + reviewer | Korpus, metoda, različica, test | DA za znanstveno trditev |
| P-015 Časovni dokaz brez izvora ure | R-015 Temporal Provenance | Executor + verifier | Vrsta časa, ura, negotovost | DA za časovno kritične trditve |

## 18. Predlagani vrstni red izvedbe

### P0 — pred vsakim poskusom označitve 0.1540 kot RELEASE

1. Uskladiti LICENSE.md, Machine record in dejanske bajte na točno določenem commitu.
2. Za vsako hišo vzpostaviti manifest in inventuro pokritosti.
3. Odpraviti trdo zapisano različico v scripts/manifest_gen.py.
4. Posodobiti zastarele podporne zapise ali jih jasno označiti kot zgodovinske.
5. Razrešiti obseg TDM pridržka in pravice tretjih oseb.
6. Izvesti neodvisno drugo roko nad rezultati.
7. Izvesti zunanji pravni pregled novih ali spremenjenih pravnih pogojev.

### P1 — pred širšo operativno uporabo

8. Uvesti standardni evidenčni zapis in validator.
9. Uvesti proces ugovora in pritožbe.
10. Uvesti zasebnostno plast registra in pravila hrambe.
11. Uvesti preizkus dejanske sanacije downstream posledic.
12. Uvesti matriko združljivosti licenc.

### P2 — razvojne izboljšave

13. Izvesti večjezično preverjanje semantične enakovrednosti.
14. Uvesti neodvisno ponovljivost ontogematrike in sorodnih metod.
15. Določiti postopke za nasledstvo, skrbništvo in prenos upravljavskih nalog.
16. Objaviti razumljiv povzetek za prejemnike, ne da bi nadomestil pravno besedilo.

## 19. Pravilo za končni izdajni zapis

Končni zapis izdaje mora biti strojno berljiv in vsebovati:

- license_version;
- standard_version;
- release_candidate;
- repository;
- branch;
- commit;
- files_manifest_sha256;
- controls;
- claim_status;
- test_result;
- decision;
- decision_owner;
- independent_verifier;
- legal_review;
- privacy_review;
- known_limitations;
- unresolved_findings;
- timestamp_records;
- rollback_or_withdrawal_plan.

Izdaja, ki nima popolnega zapisa, ne sme biti označena kot preverjena izdaja.

## 20. Merilo uspeha 0.1540

0.1540 ne bo uspešna zato, ker bo vsebovala več členov ali ker bo vsak test prikazal zeleno stanje.

Uspešna bo samo, če:

1. vsak pomemben problem dobi določeno rešitev;
2. vsaka rešitev ima dokazni artefakt;
3. vsak artefakt ima lastnika in obseg;
4. vsak test ima ponovljiv postopek;
5. vsak ugovor ima varno pot;
6. vsaka odločitev ima obrazložitev in možnost pregleda;
7. vsak popravek preveri tudi posledice;
8. zasebnost ni žrtvovana zaradi javne sledljivosti;
9. nobena pravna ali tehnična lastnost ni zatrjevana preko dosega dokaza;
10. sistem lahko pošteno izreče UNKNOWN, HOLD ali FAIL, tudi kadar je predmet sam VBL.

**Končno pravilo:** VBL ne pridobi zaupanja s tem, da zahteva zaupanje. Pridobi ga samo toliko, kolikor so njene posamezne trditve, dokazi, odločitve in popravki neodvisno preverljivi.

---

## Pravni in tehnični viri za nadaljnji pregled

To so izhodišča za pravni pregled, ne izčrpno pravno mnenje. Pred izdajo se preveri aktualno prečiščeno besedilo in uporaba prava za vsak konkretni predmet.

1. Zakon o avtorski in sorodnih pravicah (ZASP), zlasti 57.a člen in povezane izjeme: https://pisrs.si/pregledNpb?idPredpisa=ZAKO403&idPredpisaChng=ZAKO8300
2. Direktiva (EU) 2019/790, člena 3 in 4: https://eur-lex.europa.eu/eli/dir/2019/790/oj
3. Uredba (EU) 2024/1689, zlasti člena 53 in 113; konsolidirano besedilo 27. 7. 2026: https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27
4. GDPR, zlasti členi 5, 17, 25 in 32: https://eur-lex.europa.eu/eli/reg/2016/679/oj
5. EDPB, Guidelines 02/2025 on processing of personal data through blockchain technologies, končna različica 7. 7. 2026: https://www.edpb.europa.eu/documents/guideline/guidelines-022025-on-processing-personal-data-through-blockchain_en
6. Open Source Initiative, The Open Source Definition: https://opensource.org/osd
7. GNU GPLv3, zlasti §8 o prenehanju in ponovni vzpostavitvi pravic: https://www.gnu.org/licenses/gpl-3.0.en.html

---

**Konec osnutka.**  
**Status ostaja: DRAFT — NOT RELEASED.**  
**0.1530 ostaja edina javno objavljena živa različica LICENSE.md, dokler avtor ne odobri in objavi novega telesa.**
