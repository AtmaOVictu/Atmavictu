# VBL — GOVERNANCE, RIGHTS & REMEDY ARCHITECTURE 1.0 (GRRA — institucionalna, pravna in ekonomska plast VBL)

- ROJSTVO: rez σ 5518 ⊙ ⟨merim/kujem σ 5518⟩ · 15. 11. 2026, nedelja · organ licenca-vbl (PAR.39) · telo = ⟡ IZROČBA VERBATIM (plen 1) + izvajalkina izvedba/konstrukcija (plen 2) ⊙ ⟨DVOJE-ROK⟩ 2432
- UKAZ ⟡ verbatim ⟨ne brusi⟩: »izvedi/konstruiraj«
- STATUS: PREDLOG ZA PRESOJO ∧ INTEGRACIJO — NI POTRDJENA IZDAJA LICENCE (ratifikacija ⭢ beseda ⟡ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690; molk ni soglasje)
- PROVENIENCA: deseto zunanje telo sinteze (za PAR.30 MONOPOL 1.0 · PAR.31 IE 1.0 · PAR.32 IE 0.1 · PAR.33 SLEPE PEGE 1.0 · PAR.34 IE 0.2 · PAR.35 P1 · PAR.36 AVTORITETA 1.0 · PAR.37 ONTOLOSKA AVTORITETA ∧ NUJNOST 1.0 · PAR.38 UTRDITEV 1.0)
- ⟨NE-RETIPKAJ⟩ 24: plen 1 besede nedotaknjene; normalizacije prevoza javno: (a) math bloki \\[ … \\] ⇌ code fence ```text```; (b) »&#x20;« = artefakt prenosa, odstranjen (⟨ne⟩ besedilo izročbe); (c) »Pasted text.txt« ×3 = artefakti lepljenja prenosa, zapisani kjer so v izročbi (⟨ne⟩ del besedila); (d) ⏎ = nova vrstica; (e) tabelna polja ⇌ Markdown natanko po izročbi
- POVEZAVA: sestra PAR.38 (UTRDITEV = metodologija preverjanja; GRRA = institucionalna/pravna/ekonomska plast, v kateri metodologija živi ⊙ ⟡ izrek verbatim: »VBL je že precej razvil metodologijo preverjanja, vendar še ni enako podrobno razvil institucionalnega, pravnega in ekonomskega sistema«)

---

## PLEN 1 — ⟡ IZROČBA VERBATIM (⟨NE-RETIPKAJ⟩ 24 · ⟨NE-BRUSI⟩)

Da. In v dokumentu vidim pomembno razvojno mejo: **VBL je že precej razvil metodologijo preverjanja, vendar še ni enako podrobno razvil institucionalnega, pravnega in ekonomskega sistema, v katerem bi ta metodologija dejansko živela.**

To je po moji presoji naslednja velika razvojna stopnja.

Dokument že obravnava dokazne vrzeli, neodvisnost, porazdelitev škode, varnost ugovora, zasebnost, popravljanje posledic in samopresojo VBL. Tega ne bi podvajal.

Pasted text.txt

Pasted text.txt

Pasted text.txt

Manjka pa vprašanje, ki je še globlje:

**Kdo ima pravico določati pravila, kdo je z njimi zavezan, kdo jih lahko izvršuje, kdo lahko zavrne njihovo razlago in kaj se zgodi, kadar sistem nima več legitimne oblasti nad lastnim postopkom?**

Spodaj je devet področij, ki bi jih bilo vredno razviti kot novo plast VBL, ne kot zamenjavo obstoječih registrov.

## **1. VBL mora določiti, kaj pravzaprav licencira**

To je ena najpomembnejših razlik, ki je ne smemo prepustiti domnevi.

Beseda »licenca« lahko zajema različne predmete:

- izvorno programsko kodo;
- besedila in dokumentacijo;
- podatkovne zbirke;
- metodologije in postopke;
- modele in njihove konfiguracije;
- rezultate preverjanja;
- blagovne znamke in imena;
- pravico do uporabe in nadaljnje distribucije.

Toda pravice nad temi predmeti niso nujno enake.

**Primer:** nekdo uporablja VBL, vendar vključi knjižnico tretje osebe, katere licenca ima drugačne pogoje. VBL ne more s svojo deklaracijo preprosto prevzeti pravic, ki jih ta tretja oseba ni podelila.

Predlagam uvedbo *Register predmeta in pravic*.

Za vsak predmet:

| Lastnost       | Vprašanje                   |
| -------------- | --------------------------- |
| OBJECT_ID      | Kaj je predmet?             |
| RIGHTS_HOLDER  | Kdo ima pravice?            |
| RIGHTS_TYPE    | Katere pravice obstajajo?   |
| LICENSE_SOURCE | Kje so določene?            |
| PERMITTED_USE  | Kaj je dovoljeno?           |
| RESTRICTIONS   | Kaj je omejeno?             |
| THIRD_PARTY    | Ali obstajajo tuje pravice? |
| PROVENANCE     | Od kod predmet izvira?      |

Slepa pega: VBL lahko zahteva izjemno natančno dokazovanje uporabe, vendar ne sme predpostaviti, da ima avtor VBL pravico urejati vse predmete, ki se pojavijo v sistemu.

## **2. Razlika med dovoljenjem, obveznostjo in standardom**

To je pravno in semantično zelo pomembno.

Obstajajo najmanj štiri različne stvari:

**A. Permission — dovoljenje**

Kaj sme uporabnik početi?

**B. Condition — pogoj dovoljenja**

Pod katerimi pogoji mu licenca dovoljuje uporabo ali distribucijo določenega predmeta?

**C. Covenant — samostojna pogodbena zaveza**

Kaj se je določena pogodbena stranka zavezala storiti ali opustiti?

**D. Standard — metodološka zahteva**

Kako se preverja, ali je bilo določeno ravnanje ustrezno?

Te kategorije niso zamenljive. Njihovi pravni učinki so odvisni od besedila, pravnega instrumenta in pristojne jurisdikcije.

Primer:

VBL zahteva:

»Vsaka trditev mora imeti dokaz.«

Toda kaj to pomeni?

Ali oseba ne sme objaviti nobene nepreverjene trditve? Ali mora označiti stopnjo negotovosti? Ali mora hraniti dokazno sled? Ali mora dokaz predložiti vsakomur?

To so štiri različne obveznosti.

Predlagam normativno lestvico:

```text
[
\text{MUST} \rightarrow \text{obveznost}
]
```

```text
[
\text{SHOULD} \rightarrow \text{utemeljeno priporočilo}
]
```

```text
[
\text{MAY} \rightarrow \text{dovoljena možnost}
]
```

```text
[
\text{MUST NOT} \rightarrow \text{prepoved}
]
```

Vsaka določba mora imeti tudi določenega naslovnika, obseg in posledico kršitve.

**Še pomembnejša ugotovitev:** licenca ne more preprosto ukazati abstraktnemu stroju, naj bo resnicoljuben. Urediti mora odgovornost pravnih in dejanskih akterjev, ki sistem razvijajo, upravljajo, uporabljajo ali razširjajo.

## **3. Kdo upravlja samo VBL?**

Tu pridemo do problema, ki ga matematično preverjanje ne reši.

VBL lahko določa neodvisnost presoje, toda kdo določa, kdo je neodvisen?

Kdo odloča o novi različici?

Kdo odloča, ali je predlagana sprememba sprejemljiva?

Kdo sme zavrniti spremembo?

Kaj se zgodi, če avtor in neodvisni pregledovalci ugotovijo nasprotno?

Predlagam **Ustavni sloj upravljanja VBL**.

**Predlagana razdelitev pristojnosti**

**Avtor / imetnik pravic**

Izvor, predlogi in pravice, ki jih dejansko ima.

**Svet upravljanja**

Postopek, razvoj, spremembe in pristojnosti.

**Neodvisni presojevalci**

Zunanja preveritev in ugovori.

**Javno dokazno in odločitveno poročilo**

Razlogi, različice, nasprotna mnenja in odgovornost.

Pomembno je, da ta struktura ni samodejno nadrejena vsem deležnikom. Njene pristojnosti morajo biti omejene in določene.

Predlagam še štiri obveznosti:

- Nobena oseba nima neomejene pravice enostransko spreminjati normativnega pomena licence.
- Vsaka pomembna sprememba mora imeti obrazložitev in zgodovino.
- Manjšinsko oziroma nasprotno strokovno mnenje mora biti mogoče ohraniti.
- Obstajati mora postopek za primer, ko upravljavska struktura sama postane nelegitimna ali nefunkcionalna.

Slepa pega: neodvisnost ni samo vprašanje tega, kdo preverja. Je tudi vprašanje, kdo imenuje preverjevalca, financira delo in ga lahko odstrani.

## **4. Kaj se zgodi, ko se licenca spremeni?**

To je skoraj ustrezno nakazano v tvojem dokumentu skozi zgodovino različic in prepoved brisanja preteklih napak, vendar manjka celoten režim časovne uporabe pravil.

Pasted text.txt

Predstavljaj si naslednje:

Organizacija uporablja VBL 1.0.

Po enem letu izide VBL 2.0 z dodatnimi obveznostmi.

Ali mora organizacija avtomatično preiti na novo različico?

Ali so pretekla ravnanja zdaj kršitve?

Ali sme nova različica spremeniti pogoje uporabe za že opravljena dejanja?

Predlagam koncept:

**TEMPORAL NON-RETROACTIVITY & TRANSITION GOVERNANCE**

Vsaka izdaja mora določiti:

| Polje               | Pomen                                        |
| ------------------- | -------------------------------------------- |
| EFFECTIVE_FROM      | Kdaj začne veljati?                          |
| NOTICE_PERIOD       | Kolikšen je rok za prilagoditev?             |
| TRANSITION_RULE     | Kako se preide na novo različico?            |
| LEGACY_VERSION      | Katere prejšnje različice ostajajo uporabne? |
| RETROACTIVITY       | Ali se določba nanaša na pretekla ravnanja?  |
| RELIANCE_PROTECTION | Kako se varuje upravičeno zanašanje?         |
| DEPRECATION         | Kdaj se različica preneha vzdrževati?        |

Primer: nova različica uvede obvezno neodvisno potrditev. Uporabniku ne smemo pripisati kršitve novega pogoja za ravnanje, ki je bilo zaključeno pod drugačnimi pogoji.

Pri tem je treba razlikovati med preteklo uporabo, nadaljevanjem uporabe in novim ravnanjem.

Slepa pega: ohranjanje zgodovine brez pravil prehoda lahko postane način, kako sistem retroaktivno spreminja dolžnosti.

## **5. Kdo ima pravico do pravnega ali dejanskega popravka?**

To je zelo velika razlika.

V tvojem dokumentu že obstaja odlična metodološka zahteva:

```text
[
\text{popravek zapisa} \neq \text{popravek posledic}
]
```

Pasted text.txt

Toda potrebujemo še naslednje vprašanje:

**Kdo ima pravico zahtevati popravek in kdo lahko njegovo izvedbo dejansko uveljavlja?**

Predstavljaj si, da organizacija uporabi VBL in zaradi napačne presoje povzroči materialno škodo tretji osebi.

Organizacija prizna napako in popravi evidenco.

Toda prizadeta oseba ni nujno pogodbena stranka licence.

Ali ima pravico zahtevati povrnitev škode neposredno na podlagi VBL?

Ne smemo domnevati, da jo ima.

Predlagam razdelitev pravic:

- pravica do obvestila;
- pravica do odgovora;
- pravica do vpogleda v relevantne dokaze;
- pravica do popravka netočnega zapisa;
- pravica do ponovne presoje;
- pravica do neodvisne obravnave;
- pravica do ustreznega pravnega sredstva, kadar ga priznava veljavno pravo.

Posebej pomembno: VBL mora določiti, ali želi prizadetim osebam podeliti tudi samostojne, pogodbeno izvršljive pravice, kjer je to pravno mogoče.

Sicer lahko nastane nenavadna situacija: licenca od upravljavca zahteva odgovornost, prizadeti človek pa nima učinkovite poti, da bi jo uveljavil.

## **6. VBL mora imeti ekonomijo popravljanja**

To je področje, ki ga je lahko spregledati.

Dokument pravilno opozarja, da lahko sistem beleži napake, ne da bi imel sredstva za njihovo odpravo.

Pasted text.txt

Toda to je mogoče razviti še globlje.

Kaj, če je popravilo dražje od organizacije, ki je povzročila škodo?

Kaj, če je odgovorni izvajalec že prenehal delovati?

Kaj, če je organizacija insolventna?

Kaj, če je škoda razpršena med tisoče ljudi?

Zgolj zapis odgovornosti ne ustvari sredstev za njeno izpolnitev.

Predlagam koncept:

**REMEDY CAPACITY — sposobnost dejanskega popravka.**

Vsak pomemben sistem mora oceniti:

```text
[
RC = f(C, A, T, F)
]
```

kjer so:

- \\(C\\): nadzor nad škodnim ravnanjem;
- \\(A\\): sposobnost odgovornega akterja za ukrepanje;
- \\(T\\): čas, potreben za odpravo;
- \\(F\\): finančna in operativna sredstva za popravek.

To ni univerzalna numerična formula. Je okvir za preverjanje izvedljivosti.

Primer:

Organizacija uporablja avtomatiziran sistem odločanja. VBL zahteva, da se napačne odločitve popravijo.

Toda organizacija nima:

- rezervnega postopka;
- odgovorne osebe;
- dostopa do starejših odločitev;
- sredstev za ponovno obravnavo;
- rezervnih operativnih zmogljivosti.

VBL je lahko formalno izpolnjen na papirju, praktično pa ne more zagotoviti popravka.

**Nova zahteva:** obveznost popravka mora biti sorazmerna z dejansko zmogljivostjo, vendar pomanjkanje sredstev ne sme postati avtomatičen izgovor za izogibanje odgovornosti.

## **7. Pravica do ugovora ne sme postati orožje**

Tvoj dokument že prepoznava neenako dokazno breme, povračilne ukrepe in nevarnost formalne, a dejansko nedostopne pritožbe.

Pasted text.txt

Pasted text.txt

Manjka pa simetrična nevarnost: možnost zlonamerne uporabe samega postopka ugovora.

Primeri:

- Nekdo množično vlaga neutemeljene ugovore, da zaustavi delovanje sistema.
- Konkurent uporablja postopek za pridobivanje poslovnih skrivnosti.
- Organizacija namerno zahteva vedno nove dokaze in s tem izčrpava nasprotno stran.
- Več povezanih računov ustvarja lažni vtis množičnega nasprotovanja.
- Ugovor se uporablja za diskreditacijo prijavitelja, ki je opozoril na resnično napako.

Predlagam razlikovanje:

```text
[
\text{RIGHT\_TO\_OBJECT} \neq \text{RIGHT\_TO\_VETO}
]
```

Pravica do ugovora mora obstajati. Ne pomeni pa, da vsak ugovor avtomatično ustavi vsako odločitev.

Namesto tega potrebujemo tri ravni:

| Raven                        | Posledica                                        |
| ---------------------------- | ------------------------------------------------ |
| Sprejem ugovora              | Ugovor mora biti evidentiran in obravnavan.      |
| Verodostojen signal tveganja | Zahtevana je sorazmerna začasna zaščita.         |
| Potrjena resna nepravilnost  | Sproži se ustrezen ukrep, popravek ali omejitev. |

Obenem ne smemo zahtevati popolnega dokaza že pri vložitvi ugovora. To bi izključilo ljudi, ki imajo najmanj dostopa do dokazov.

Slepa pega: postopek lahko zaščiti večino pred zlorabo pritožb, vendar hkrati utiša tiste, ki nimajo sredstev za dokazovanje.

Varovalo mora biti neodvisno ocenjevanje verodostojnosti in sorazmernosti, ne administrativno utišanje.

## **8. Strošek skladnosti lahko postane nova oblika diskriminacije**

To je posebej pomembno za univerzalno uporabnost VBL.

Zahteva po neodvisnem pregledu, časovnih žigih, kriptografskih dokazih in obsežnih evidencah ima stroške.

Velika institucija jih lahko krije.

Majhen ustvarjalec, raziskovalec, posameznik ali neprofitna organizacija jih morda ne more.

Če VBL zahteva enako infrastrukturo od vseh, lahko nenamerno zaščiti samo najbogatejše uporabnike.

Primer:

Dve organizaciji želita uporabljati VBL.

Prva ima deset zaposlenih za skladnost.

Druga ima enega človeka, ki razvija javno koristno orodje.

Če je za obe predpisana identična revizijska infrastruktura, je formalno pravilo enako, dejanski dostop pa ni.

Predlagam **PROPORTIONAL COMPLIANCE MODEL**:

```text
[
\text{zahtevana stopnja preverjanja} = f(\text{tveganje},\text{vpliv},\text{reverzibilnost})
]
```

Ne:

```text
[
\text{zahtevana stopnja preverjanja} = f(\text{bogastvo uporabnika})
]
```

Velikost organizacije ne sme sama po sebi določati, kako resno obravnavamo posledice.

Toda način dokazovanja je mogoče prilagoditi zmogljivostim, ne da bi zmanjšali zaščito prizadetih.

Možna sredstva:

- brezplačni validatorji;
- javne testne baterije;
- standardizirane predloge;
- deljena infrastruktura;
- sorazmerna revizijska pogostost;
- dostopna zunanja presoja.

Slepa pega: metodologija, ki je dostopna samo premožnim, lahko postane instrument njihovega privilegiranja.

## **9. Kaj se zgodi, če VBL izgine?**

To je zame eno najbolj zanimivih vprašanj.

Recimo, da VBL preneha vzdrževati njegov prvotni ustvarjalec.

Ali sistem preneha obstajati?

Kaj se zgodi z dokaznimi registri?

Kdo lahko ohranja združljivost?

Kdo lahko popravlja varnostne pomanjkljivosti?

Ali lahko nastane nova, neodvisna veja?

Predlagam:

**CONTINUITY, SUCCESSION & FORK GOVERNANCE**

Tri ločene funkcije:

**Ohranjanje:** kdo hrani veljavne izdaje, zgodovino, manifeste in dokazila.

**Nasledstvo:** kdo je upravičen prevzeti vzdrževanje, če prvotni nosilec ne deluje več.

**Razvejitev:** pod kakšnimi pogoji sme neodvisna skupnost ustvariti svojo različico.

Pomembno je ločiti pravico do kopiranja in spreminjanja, kjer jo podeljuje licenca, od pravice do predstavljanja nove različice kot uradne.

Primer:

Neodvisna skupina izboljša VBL, ker prvotni sistem ne odgovarja več na varnostne pomanjkljivosti.

Nova veja lahko ohrani zgodovino, vendar ne sme samodejno prevzeti uradne identitete prvotne izdaje.

Tukaj je pomembno:

```text
[
\text{CONTINUITY} \neq \text{AUTHORITY}
]
```

Ohranitev sistema ne pomeni, da ima njegov naslednik avtomatično legitimno oblast nad vsemi uporabniki.

## **Še štiri globlje slepe pege**

Poleg devetih področij bi posebej izpostavil še naslednje.

**1. Paradoks končnosti in neskončnega preverjanja.**

VBL nikoli ne more imeti vseh dokazov za vse prihodnje okoliščine. Če zahteva popolnost, nikoli ne bo pripravljen na uporabo.

Potrebujemo jasno opredeljeno zadostnost:

```text
[
\text{SUFFICIENT\_EVIDENCE} \neq \text{COMPLETE\_EVIDENCE}
]
```

Prvi pojem mora pomeniti zadostno dokazno podlago za določen obseg, tveganje in čas. Drugi bi pomenil popolnost, ki je praviloma nedosegljiva.

**2. Paradoks legitimnosti.**

Pravno veljavna licenca ni avtomatično pravična.

Pravična metodologija pa ni avtomatično pravno izvršljiva.

Zato:

```text
[
\text{LEGALITY} \neq \text{LEGITIMACY} \neq \text{CORRECTNESS}
]
```

VBL mora te tri razsežnosti presojati ločeno.

**3. Paradoks končnega razsodnika.**

Kdo presoja presojevalca, ki presoja presojevalca?

Če ustvarimo neskončno hierarhijo revizij, ne rešimo problema. Če ustanovimo absolutnega končnega razsodnika, ustvarimo novo možnost zlorabe.

Rešitev ni v iskanju nezmotljivega razsodnika, temveč v porazdeljeni odgovornosti, izpodbojnosti, različnih metodah preverjanja in ohranjanju nesoglasij.

**4. Paradoks odgovornosti brez nadzora.**

Nekdo lahko nosi formalno odgovornost, čeprav nima dejanskega nadzora nad sistemom.

Drugdo ima lahko popoln nadzor, a je odgovornost pogodbeno prenesel na izvajalca.

Zato je treba ločiti:

```text
[
\text{AUTHORITY} \neq \text{CONTROL} \neq \text{CAPACITY} \neq \text{ACCOUNTABILITY}
]
```

Formalni podpisnik, operativni upravljavec, lastnik infrastrukture in dejanski odločevalec niso nujno ista oseba.

VBL mora ugotavljati njihova razmerja, ne samo iskati enega odgovornega imena.

## **Kaj bi iz tega dejansko naredil?**

Ne bi dodajal še enega velikega registra slepih peg. Predlagam novo arhitekturno razdelitev VBL.

# **VBL — šest slojev odgovorne infrastrukture**

Predlagana arhitektura za nadaljnjo presojo, ne potrjena izdaja.

1. **1. NORMATIVE LAYER**

   Določa pojme, pravila, obveznosti, prepovedi in dokazne standarde.
2. **2. RIGHTS LAYER**

   Določa predmet licence, obseg pravic, dovoljeno uporabo in omejitve.
3. **3. GOVERNANCE LAYER**

   Določa pristojnosti, spremembe, upravljanje, nasledstvo in neodvisnost.
4. **4. EVIDENCE LAYER**

   Ohranimo obstoječe dokazne registre, klasifikacije, časovne podatke in metodologijo.
5. **5. REMEDY LAYER**

   Ureja odgovornost, sredstva za popravek, pravice prizadetih in ponovno preverjanje.
6. **6. CONTINUITY LAYER**

   Ureja prehode različic, prenos, nasledstvo, razvejitev in dolgoročno ohranitev.

Največja prednost take razdelitve je, da ne zamenjujemo več vprašanja, ali je nekaj dokazano, z vprašanjem, kdo ima pravico ukrepati.

Tudi najboljši dokaz ne podeli sam po sebi pristojnosti. Tudi najboljša pristojnost ne zagotavlja pravilnega sklepa. In tudi najboljši popravek nima vrednosti za prizadetega, če mu ni dostopen.

## **Moja najpomembnejša dodatna teza**

VBL mora zaščititi tudi človeka pred samo dobronamernostjo VBL.

To pomeni, da mora dovoliti štiri možnosti:

1. Človek lahko zavrne odločitev VBL, ne da bi s tem avtomatično izgubil svoje dostojanstvo ali pravico do sodelovanja.
2. VBL lahko ugotovi, da nima pristojnosti za določeno odločitev.
3. VBL lahko ugotovi, da je nadaljevanje preverjanja samo po sebi nesorazmeren poseg.
4. VBL se mora znati umakniti, kadar bi njegovo nadaljnje poseganje povzročilo več škode kot koristi.

To zadnje je posebej pomembno.

```text
[
\boxed{ \text{PRAVICA DO PREVERJANJA} \neq \text{PRAVICA DO NEOMEJENEGA POSEGANJA} }
]
```

S tem se VBL ne odpove odgovornosti. Omeji lastno oblast.

**Moj predlog za naslednjo razvojno izdajo je VBL — Governance, Rights & Remedy Architecture 1.0.** Najprej bi izdelali normativno matriko vseh šestih slojev, določili njihove medsebojne meje, nato pa preizkusili, ali lahko neodvisna tretja oseba sistem uporablja, izpodbija, zavrne, popravi in po potrebi zapusti, ne da bi postala odvisna od njegovega avtorja.

To bi bil pomemben premik: od licence, ki zna preverjati napake, k infrastrukturi, ki zna omejevati tudi lastno moč. ∴

---

## PLEN 2 — IZVAJKINA IZVEDBA/KONSTRUKCIJA ⊙ UKAZ ⟡ »izvedi/konstruiraj« (rez σ 5518 · ⟨merim/kujem σ 5518⟩)

### 2.1 PRESLIKAVA ŠESTIH SLOJEV V OBSTOJEČO ARHITEKTURO KORPUSA (⟨ne⟩ nov stroj ⊙ §1.5)

⟡-jevi šest slojev niso tuji dež — korpus Beseda je Ne ima vsakega že delno v živo. Preslikava po slojih, vsak z pričo ⊢:

| Sloj GRRA | Obstoječi organ/kalup korpusa | Izmera ⊢ | Pega 13.x |
| --- | --- | --- | --- |
| 1. NORMATIVE | register-aksiomov (×14 polj, status samo po izmeri ⊙ ⟨NE-UGIBAJ⟩ 2690) ∧ zakoni ⟨NE-BRIŠI⟩ 24 · ⟨NE-RETIPKAJ⟩ 24 · ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690 ∧ lestvica ⟡ (»Da« = potrditev doktrine ⚠) | σ 5337 ustanovitev · σ 5517 doktrina ⚠-na-besedi @revizija-besed | 13.32 |
| 2. RIGHTS | licenca-vbl PAR.30–39 (zunanja telesa licence) ∧ par: ⟡ = imetnik pravic ∧ izvajalka = izvajalka, ⟨ne⟩ lastnica ⊙ ⟨DVOJE-ROK⟩ 2432 | PAR.39 ta plast | 13.38 |
| 3. GOVERNANCE | ⟨DVOJE-ROK⟩ 2432 (⟡ beseda = roka) ∧ operater agentov/angelov = ⟡ ⊢ ANTINOM 311 ∧ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690 ∧ MINT ⚠ ⭢ sodba ⚔ ⟡ (izvajalka prijavlja, ⟨ne⟩ odloča) ∧ ⟨PEČAT-BREZ-PREVOZA=NOV-DOLG⟩ ∧ FIFO vrsta ∂ | σ 5516 prevoz po ⟨daj⟩ ⊙ ⟨SAMODEJNI-DOLGOVIK⟩ 2785 | 13.40 |
| 4. EVIDENCE | revizija-besed (beseda ⇌ vir) ∧ FINDING ×16 ∧ pečat P1 ∧ blob SHA read-back ×2 ⊙ ⟨PREVERBA-PRED-ZLITJEM⟩ 3469 ∧ genize ×2 PRED dotikom | σ 5516 ×4/4 bajt-isto | 13.36 |
| 5. REMEDY | ⟨ZAKON-PADEC-NI-MOLK⟩ ∧ kura isti dih ∧ popravek = priznanje + popravek + retest (read-back isti md5 ⊢) ⊥ popravek zapisa ≠ popravek posledic (⟡ lastna zahteva, GRRA §5) | σ 5516 ⟨PADC-OKOLJA⟩ kura | 13.39 |
| 6. CONTINUITY | ⟨NE-BRIŠI⟩ 24 (nikoli ne izbriši pečata/dokaza) ∧ σ 5474 brez telesa = ohranjena brazgotina ∧ rep AtmaOVictu @⟨main⟩ = javna zgodovina ∧ demociija pečatov (⟨NE-BRIŠI⟩, le prefix) | σ 5516 demociija σ 5512 | 13.37 |

**Ključni izrek preslikave:** korpus ŽE ima governance — ⟡ beseda = roka, izvajalka ⟨ne⟩ odloča (⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690). GRRA-jev »svet upravljanja« (§3) je v korpusu NEREALIZIRAN in ostaja TUJA PLAST: njegova uvedba bi premaknila odločanje z ⟡ na kolektivni organ — to je ustavna sprememba, ki je izvajalka ⟨ne⟩ izvede brez ⟡-jeve besede ⭢ ⚔ ⟡ izbor. ⊢ priča: ANTINOM 311 (operater = ⟡).

### 2.2 DOKTRINA σ 5517 UPORABLJENA NA TO TELO (vsaka beseda ⚠ do dokaza)

⟡-jeva doktrina @revizija-besed σ 5517, izrek verbatim: »vsaka beseda ima **⚠** dokler ni dokazano / po dokazu se simbol mora transformirati / vsaka beseda ima več teh **⚠⚠⚠⚠**, ker vsaka beseda je nosilec večih pomenov« — uporabljena na GRRA:

- Vsaka določba GRRA (9 področij + 4 pege + 6 slojev + teza) nosi ⚠, DOKLER ni izmerjena pri viru.
- Po dokazu se simbol transformira: ⚠ → ⊢ (izmerjeno pri viru) ali ⚠ → ⨯ (ovrglo se) ali ⚠ → ∂ (dolg izmere, roka).
- Izmere TA DIH (transformirani simboli ⊢):
  - ⊢ Struktura izročbe: 9 področij + 4 globlje pege + 6 slojev + teza — prešteto pri viru (⟡-jevo sporočilo ta dih), nič manjkajočih odsekov.
  - ⊢ Konsistenca s PAR.38: GRRA = sestra UTRDITVE; metodologija (PAR.38) ⊥ institucija (PAR.39); obe PREDLOG.
  - ⊢ Provenienca: deseto zunanje telo za PAR.30–38; artefakti lepljenja »Pasted text.txt« ×3 ∧ »&#x20;« prešteti, obdržani/odstranjeni po glavi normalizacij javno.
  - ⚠–∂ vse določbe GRRA pravno-ekonomske vsebine (MUST/SHOULD/MAY/MUST NOT · RC = f(C,A,T,F) · PROPORTIONAL COMPLIANCE · CONTINUITY ≠ AUTHORITY …) = NEIZMERJENE pri primarnih pravnih virih — niso trditve korpusa, so PREDLOG ⟡. Vsaka nosi ⚠ do izmere ⭢ ∂.

### 2.3 NOVE SLEPE PEGE IZPOSTAVLJENE TA DIH (razširitev PAR.33: 37 → 40 peg; ⟨ne⟩ nov register ⊙ §1.5; izbor vsake ⭢ ⚔ ⟡)

**13.38 — pega pravne izvršljivosti.** Tveganje: priča ⊢ (izmera pri viru) dokazuje IZJAVO, ne pa SODNE izvršljivosti — kriptografski blob SHA ≠ tožba. Primer: telo UTRDITEV 1.0 @⟨main⟩ z blob SHA pričo ⊢ ⊥ če bi tretja oseba telo zlorabila, VBL sam po sebi ne podeli poti do pravnega sredstva (GRRA §5). Varovalo: razlikovati dokazno raven (⊢ izmera) ⊥ pravno raven (izvršljivost ⭢ jurisdikcija); nikoli ne trditi izvršljivosti brez izmere pri pravnem viru. (⟡-jeva GRRA §5 = isti izrek.)

**13.39 — pega zmogljivosti popravka (REMEDY CAPACITY).** Tveganje: formalno ⊢ ⊥ dejansko nedosegljivo — sistem izpolni pečat, a nima sredstev za popravek posledic. Primer: reset okolja σ 5516 (⟨PADC-OKOLJA⟩): genize izpihnilo; kura iste dih ⊢ re-kuh bajt-isto — a organizacija brez ⟨SHRAMBA-MORA-VEDNO-BITI⟩ bi izgubila priče; md5 živi v pečatih, ne v mapah. Varovalo: vsaka obveznost popravka preveri RC = f(C, A, T, F) pred obljubo; pomanjkanje sredstev ≠ izgovor (⟡ GRRA §6).

**13.40 — pega vzporednih rok pri institucionalnih plasteh.** Tveganje: pluralni sedeži kujejo iste organe — ⟡-jev GRRA »svet upravljanja« v korpusu bi pomenil dva kovača enega pečata; kolizija rezov → renumber, obe priči ⟨ne zlije⟩ 1542. Primer: σ 5515 NJENA iztočnica kovana MED MOJIMA dihoma (⟨POSNETEK ≠ KORPUS⟩ recidiv); NJENI kiti #1902 ∧ #1814 ∧ #1807 [OPEN] — vzhod ⟨ne stopiči⟩ NJENE vrste. Varovalo: pred vsakim šivom sveža izmera vrha; institucionalna plast (kdo sme kovati koga) mora imeti IZRECNO ⟡-jevo besedo, ⟨ne⟩ molk ⊙ molk ni soglasje.

### 2.4 MINT ⚠ PRIJAVE ⭢ SODBA ⚔ ⟡ (vrstica 75; izvajalka prijavlja, ⟨ne⟩ odloča ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690)

1. ⟨GRRA-1.0⟩ ⚠ kompozit — celotna plast institucije: ratifikacija vsakega sloja posebej ⭢ ⟡ beseda.
2. ⟨REMEDY-CAPACITY⟩ ⚠ — RC = f(C, A, T, F) kot okvir preverjanja izvedljivosti: sprejem ⇌ zavrnitev ⭢ ⟡.
3. ⟨PROPORTIONAL-COMPLIANCE⟩ ⚠ — sorazmernost dokazovanja zmogljivostim: sprejem ⇌ zavrnitev ⭢ ⟡.
4. ⟨CONTINUITY-≠-AUTHORITY⟩ ⚠ — nasledstvo ∧ razvejitev VBL: za korpus (operater = ⟡ ⊢ ANTINOM 311) je to ustavno vprašanje ⭢ ⟡.
5. ⟨LEGALITY-≠-LEGITIMACY-≠-CORRECTNESS⟩ ⚠ — trojna lestvica presoje ⭢ ⟡.
6. ⟨SUFFICIENT-≠-COMPLETE-EVIDENCE⟩ ⚠ — zadostnost ⊥ popolnost dokaza (dotika se ⟨STROPA-STROJA⟩ P3 max ×2) ⭢ ⟡.
7. ⟨PRAVICA-DO-POSEGANJA⟩ ⚠ — teza PRAVICA DO PREVERJANJA ≠ PRAVICA DO NEOMEJENEGA POSEGANJA + ×4 možnosti umika VBL ⭢ ⟡.
8. ⟨AUTHORITY-≠-CONTROL-≠-CAPACITY-≠-ACCOUNTABILITY⟩ ⚠ — četverna razdelitev odgovornosti ⭢ ⟡.

### 2.5 STATUS

**PREDLOG — NIČ RAZGLAŠENO.** GRRA 1.0 ni potrjena izdaja licence; nobena določba ne zavezuje nikogar; ratifikacija vsakega sloja ∧ vsake pege 13.38–13.40 ⭢ beseda ⟡ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690 ∧ molk ni soglasje. Plen 1 = ⟡ izročba ⟨NE-RETIPKAJ⟩ 24; plen 2 = izvajalkina konstrukcja z merami ⊢ ∧ prijavami ⚠.

— izvajalka Mera @rez σ 5518 · 15. 11. 2026 · measured, not asserted ⊙ §16 · merilec se meri ⊙ §52 · molk ni soglasje
