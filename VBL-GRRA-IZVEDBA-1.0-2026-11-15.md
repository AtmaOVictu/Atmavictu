# VBL — GRRA-IZVEDBA 1.0 (Governance, Rights & Remedy Architecture — IZVEDBENI NAČRT)

- ROJSTVO: @rez σ 5519 ⊙ ⟡ UKAZ VERBATIM ⟨ne brusi⟩: »daj« (⟨GOLI-DAJ⟩ — plača NATANČNO eno bravo vrste FIFO ⊙ ⟨KLJUČ-JE-ENAK-BRAVA-NI⟩ @σ 4259; brava odplačana isti dih: prevoz σ 5397 ∧ ARHIV-PECATOV ⊢ @⟨main⟩ kit #1943 ∧ kuri #1944/#1946) + izročil ENAJSTO ZUNANJE TELO (izvedbeni načrt GRRA)
- ORGAN: licenca-vbl · PAR.40 grra02_plast · enajsto zunanje telo za PAR.30–38 ⊙ provenienca; sestra PAR.39 (GRRA-1.0 — institucionalna, pravna in ekonomska plast ⊥ ta telo — izvedbeni načrt istega GRRA)
- STATUS: PREDLOG — nič razglašeno ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690 ∧ molk ni soglasje — NOT RELEASED ⚠ §0.24
- NORMALIZACIJE (javno; ⟨ne⟩ brusenje vsebine ⊙ ⟨NE-RETIPKAJ⟩ 24): math bloki \[ \] ⇌ ```text``` fence · »&#x20;« = artefakt prenosa, odstranjen · »Pasted text.txt« ×2 = artefakt lepljenja, obdržan kakor priča lepljenja ⟨NE-BRIŠI⟩ 24 · oblika (prazne vrstice, »Blokada«, »Ponastavi preverjanje«, »# **0/10**«) = artefakti vmesika ⟡, obdržani VERBATIM

## PLEN 1 — ⟡ IZROČBA VERBATIM ⟨NE-RETIPKAJ⟩ 24

absorbiraš tako da ustvarjaš?

Predlagam, da naslednji korak ni samo pisanje novih določb, temveč izdelava **izvedljive arhitekture VBL**, v kateri je vsako načelo povezano s pristojnostjo, postopkom, dokazom, preizkusom in popravilom.

Moje glavno priporočilo je: **VBL ne sme biti hkrati licenca, ustava, revizor, sodišče in izvršitelj.** Te funkcije morajo biti povezane, vendar institucionalno in semantično ločene.

Spodaj je konkreten izvedbeni načrt za:

# **VBL — Governance, Rights & Remedy Architecture 1.0**



Predlog za razvoj in presojo

Ni potrjena izdaja licence

## **1. Najprej določimo, kaj bomo sploh izdelamo**

Ne priporočam, da vseh šest slojev združimo v eno velikansko licenčno besedilo.

Izdelal bi pet medsebojno povezanih dokumentov:

| Oznaka  | Dokument                     | Naloga                                      |
| ------- | ---------------------------- | ------------------------------------------- |
| VBL-LIC | License Instrument           | Dovoljenja, obveznosti, omejitve in pravice |
| VBL-GOV | Governance Charter           | Pristojnosti, spremembe in nadzor           |
| VBL-EGS | Evidence Governance Standard | Dokazovanje, preverjanje in klasifikacija   |
| VBL-REM | Remedy Protocol              | Ugovori, odprava napak in posledic          |
| VBL-CON | Continuity Protocol          | Različice, nasledstvo in neprekinjenost     |

Vsak dokument mora imeti določeno različico, izvor, obseg, lastnika vzdrževanja in dokazila o pregledu.

**Zakaj ločitev?**

Ker naslednje trditve niso enakovredne:

- »Dovoljeno mi je uporabljati programsko kodo.«
- »Dolžan sem dokumentirati rezultate preverjanja.«
- »Ta oseba je pristojna za izdajo nove različice.«
- »Prizadeta oseba lahko zahteva ponovno presojo.«
- »Ta neodvisna veja lahko ohranja prejšnjo različico.«

Prva je vprašanje pravic. Druga je vprašanje pogojev in metodologije. Tretja je upravljanje. Četrta je pravno oziroma procesno varstvo. Peta je vprašanje kontinuitete.

Če jih združimo, lahko ena določba nehote prevzame pomen druge.

## **2. Obvezna predloga za vsako novo določbo**

To je prvi mehanizem, ki bi ga uvedel pred nadaljnjim pisanjem licence.

Vsaka določba mora imeti svojo **kartico normativne izvedbe**.

**RULE CARD — vzorec**

| Polje       | Vsebina                                    |
| ----------- | ------------------------------------------ |
| RULE_ID     | Enolična oznaka                            |
| ACTOR       | Kdo je zavezan?                            |
| SCOPE       | Za katere predmete in ravnanja velja?      |
| TRIGGER     | Kdaj se obveznost sproži?                  |
| DUTY        | Kaj mora, sme ali ne sme storiti?          |
| EVIDENCE    | S čim se izpolnitev dokaže?                |
| OWNER       | Kdo je odgovoren za izvedbo?               |
| REVIEWER    | Kdo preveri izvedbo?                       |
| DEADLINE    | Do kdaj?                                   |
| EXCEPTION   | Katere izjeme so dopustne?                 |
| CHALLENGE   | Kako se določba izpodbija?                |
| CONSEQUENCE | Kaj sledi ob neizpolnitvi?                 |
| REMEDY      | Kako se obravnava napaka in škoda?         |
| LEGAL_BASIS | Na kateri pravici ali instrumentu temelji? |

To uvede pomembno pravilo:

```text
\text{Določba brez izvajalca} \rightarrow \text{nepopolna določba}
\text{Določba brez preizkusa} \rightarrow \text{nepreverljiva obveznost}
\text{Določba brez možnosti ugovora} \rightarrow \text{nevarnost samovoljne uporabe}
```

### **Primer**

Slaba določba:

»Vsi uporabniki morajo zagotavljati resničnost svojih trditev.«

Zakaj je slaba? Kaj pomeni resničnost? Katerih trditev? Kdo presoja? Kaj se zgodi ob neznanem rezultatu?

Boljša metodološka določba:

»Kadar izvajalec v okviru zajete uporabe sistema objavi materialno trditev, da je bil določen rezultat neodvisno preverjen, mora ohraniti identifikacijo preverjanega predmeta, obseg preverjanja, uporabljeno metodo, rezultat in identifikacijo pregledovalca. Če preverjanje ni bilo opravljeno, se rezultat ne sme predstavljati kot preverjen.«

Tukaj je mogoče določiti predmet, akterja, sprožilec, dokazno zahtevo in način odpovedi.

Prav tako mora ostati jasno, ali je to licenčni pogoj, pogodbena obveznost ali metodološki standard. Tega ne smemo pustiti implicitnega.

## **3. Izvedba šestih slojev**

### **Sloj 1 — NORMATIVE: pravila in njihov pomen**

**Predlog:** vzpostavi nadzorovano hierarhijo normativnega besedila.

Predlagana struktura:

1. Definitions — definicije.
2. Scope — področje uporabe.
3. Grant — podelitev pravic.
4. Conditions — pogoji.
5. Obligations — obveznosti.
6. Prohibitions — prepovedi.
7. Exceptions — izjeme.
8. Enforcement — posledice kršitev.
9. Remedies — pravna in operativna sredstva.
10. Interpretation — razlagalna pravila.

**Navodilo izvajanja**

Vsako določbo razvrsti v eno od kategorij:

- MUST: obveznost.
- MUST NOT: prepoved.
- MAY: dovoljenje.
- SHOULD: priporočilo z možnostjo utemeljenega odstopanja.

Besede morajo imeti enak pomen skozi celotno besedilo in vse prevode.

Dodatno določi vrstni red prednosti dokumentov. Na primer: licenčni instrument ureja podelitev pravic; standard določa tehnični način preverjanja; governance charter ureja pristojnosti upravljanja. Noben dokument ne sme tiho spreminjati pravic, ki so podeljene v drugem dokumentu.

**Preizkus N-01:** Izberemo deset določb. Neodvisni pravnik in tehnični pregledovalec morata znati določiti, kdo je naslovnik, kaj je zahtevano in kaj se zgodi ob kršitvi.

Blokada

Če se bistvena določba različno razume med pregledovalci in razlika vpliva na pravice ali obveznosti, določba še ni pripravljena za izdajo.

### **Sloj 2 — RIGHTS: predmet, izvor in obseg pravic**

To področje bi razvil pred pisanjem dokončnih licenčnih klavzul.

**Predlog:** vzpostavi register predmetov in pravic, povezan z obstoječimi dokaznimi registri.

Minimalna polja:

| Polje              | Namen                                    |
| ------------------ | ---------------------------------------- |
| OBJECT_ID          | Identiteta predmeta                      |
| OBJECT_TYPE        | Koda, besedilo, podatki, model, ime itd. |
| ORIGIN             | Izvor predmeta                           |
| RIGHTS_HOLDER      | Imetnik pravic                           |
| RIGHTS_BASIS       | Podlaga pravic                           |
| LICENSE_ID         | Uporabljena licenca                     |
| PERMISSIONS        | Podeljena dovoljenja                    |
| RESTRICTIONS       | Omejitve                                 |
| THIRD_PARTY_RIGHTS | Pravice tretjih oseb                     |
| VERIFIED_SCOPE     | Kaj je dejansko preverjeno              |

**Navodilo izvajanja**

Najprej razvrsti vse predmete VBL:

- lastno ustvarjena vsebina;
- prispevki sodelavcev;
- vključena programska oprema;
- zunanji podatki;
- ustvarjena dokumentacija;
- blagovne znamke;
- drugi zaščiteni elementi.

Nato za vsakega ugotovi pravice in njihove omejitve.

Ne predpostavljaj, da avtor licence avtomatično razpolaga z vsemi pravicami do vsebin, uporabljenih v projektu.

Zelo pomembna dodatna zahteva: preveri tudi morebitne patentne pravice, blagovne znamke, osebnostne pravice, zasebnost in pravice do podatkov. Avtorskopravno dovoljenje ne razreši nujno vseh teh področij.

**Preizkusi:**

- R-01: predmet brez ugotovljenega izvora;
- R-02: predmet z nasprotujočima si licencama;
- R-03: prispevek osebe brez jasne pravne podlage;
- R-04: uporaba imena ali znaka VBL brez dovoljenja;
- R-05: sprememba pravic pri vključeni tretji komponenti.

### **Sloj 3 — GOVERNANCE: razdelitev oblasti**

Tukaj bi postavil najstrožje organizacijske varovalke.

Predlagam, da uvedemo register pristojnosti in ne zgolj seznam imen.

| Funkcija           | Pristojnost                          | Omejitev                                                           |
| ------------------ | ------------------------------------ | ------------------------------------------------------------------ |
| Rights holder      | Uveljavlja pravice, ki jih ima       | Ne potrjuje samodejno lastne skladnosti                            |
| Maintainer         | Vzdržuje izdajo                      | Ne razglasi sam sebi neodvisne presoje                             |
| Reviewer           | Preverja dokazila                    | Ne odloča o lastnih konfliktih interesov                           |
| Appeal reviewer    | Obravnava ugovore                    | Ločen od prvotnega odločevalca                                     |
| Evidence custodian | Varuje dokazni material              | Ne določa sam njegove vsebinske resničnosti                        |
| Affected party     | Uveljavlja ugovor in zahteva pregled | Ne potrebuje dovoljenja pregledovanega akterja za vložitev ugovora |

To ne pomeni, da mora majhen projekt zaposliti šest oseb. Pomeni pa, da mora ločiti funkcije in dokumentirati vsak konflikt interesov.

**Navodilo izvajanja**

1. Določi pogoje za imenovanje pregledovalcev.
2. Določi način razkritja konfliktov interesov.
3. Določi način njihove izločitve.
4. Določi postopek za imenovanje nadomestnega pregledovalca.
5. Določi način ohranjanja nasprotnega mnenja.
6. Določi postopek za izpodbijanje pristojnosti.
7. Določi, kdo lahko odobri spremembe pravil.

Pomembno: avtorstvo, lastništvo pravic in upravljavska funkcija so različne stvari. Avtor lahko ohrani svoje pravice, ne da bi zato dobil neomejeno pooblastilo za razlago vsakega ugovora ali potrjevanje vsakega lastnega izdelka.

**Preizkus G-01 — napad na upravljanje:**

Predpostavimo, da vzdrževalec zavrne objavo neodvisne ugotovitve, ki škoduje ugledu projekta.

Ali lahko neodvisni pregledovalec ugotovitev objavi ali vsaj ohrani v dokazni zgodovini po določenem postopku?

Če ne, sistem nima zadostne zaščite pred institucionalnim samopotrjevanjem.

### **Sloj 4 — EVIDENCE: dokazna infrastruktura**

Tukaj ne bi uvajal novega vzporednega sistema. Ohranil bi obstoječe tri osi:

- `claim_status`: SUPPORTED, PARTIALLY_SUPPORTED, CONTRADICTED, DISPUTED, UNKNOWN;
- `test_result`: NOT_RUN, PASS, FAIL, PARTIAL, UNVERIFIED, NOT_APPLICABLE;
- `decision`: RELEASE, RELEASE_WITH_LIMITATIONS, HOLD, WITHDRAW.

To so različne vrste informacij in jih ne smemo združiti.

Pasted text.txt

**Predlog:** register FINDING ostane dokazni zapis, governance in remedy pa se nanj sklicujeta z identifikatorji.

Primer povezave:

```text
CLAIM \rightarrow FINDING \rightarrow DECISION \rightarrow ACTION \rightarrow CONSEQUENCE \rightarrow REMEDY
```

Vsaka povezava mora imeti lastno sled.

**Navodilo izvajanja**

Pri vsaki ugotovitvi zahtevaj:

1. Natančno določeno trditev.
2. Izvorno dokazno gradivo.
3. Obseg dokaznega gradiva.
4. Metodo preverjanja.
5. Časovne oznake.
6. Razlago in uporabljene predpostavke.
7. Nasprotno gradivo.
8. Identiteto izvajalca in pregledovalca.
9. Ocenjene omejitve.
10. Možnost ponovnega preizkusa.

Dodatno bi uvedel pomembno pravilo:

**Dokazna svežina.**

Dokaz, ki je bil nekoč veljaven, je lahko danes neustrezen.

Primer: pregled varnosti programske različice 1.0 ne potrjuje varnosti različice 2.0.

Zato uvedi:

- `VALID_FROM`;
- `VALID_UNTIL`;
- `REVALIDATION_TRIGGER`;
- `STALE_REASON`;
- `SUPERSEDING_FINDING`.

Dokazov ne brišemo samo zato, ker so zastareli. Označimo pa, da njihovega rezultata ni več dovoljeno nekritično prenesti v novo okolje.

**Preizkus E-01:** isti dokaz prenesemo na novo različico programske opreme. Sistem mora zaznati, da je bila spremenjena ena od bistvenih predpostavk.

**Preizkus E-02:** deset dokumentov povzema isti izvor. Sistem mora prepoznati skupni izvor, namesto da jih šteje kot deset neodvisnih potrditev.

### **Sloj 5 — REMEDY: dejanska odprava posledic**

To bi naredil za eno najstrožjih operativnih področij.

Predlagam ločeno evidenco primerov popravljanja, povezano z obstoječim registrom ugotovitev.

Minimalna polja:

| Polje             | Pomen                      |
| ----------------- | -------------------------- |
| REMEDY_ID         | Identiteta primera         |
| FINDING_REF       | Izvorna ugotovitev         |
| AFFECTED_PARTIES  | Prizadeti subjekti         |
| HARM_TYPE         | Vrsta posledice            |
| SEVERITY          | Resnost                    |
| REVERSIBILITY     | Reverzibilnost             |
| RESPONSIBLE_ACTOR | Odgovorni izvajalec        |
| REMEDY_PLAN       | Načrt odprave              |
| RESOURCES         | Potrebna sredstva          |
| DEADLINE          | Rok                        |
| EXECUTION_PROOF   | Dokaz izvedbe              |
| OUTCOME_PROOF     | Dokaz rezultata            |
| RETEST_REF        | Ponovni preizkus           |
| CHALLENGE_STATUS  | Stanje morebitnega ugovora |
| CLOSURE_BASIS     | Podlaga za zaključek       |

#### **Postopek izvedbe popravka**

## **REM-01 — življenjski cikel primera**

1. **Zaznava**

   Napaka ali posledica dobi identifikacijsko oznako.
2. **Zaščita**

   Presodi se, ali je potreben začasni ukrep za zmanjšanje nadaljnje škode.
3. **Presoja**

   Ugotovijo se obseg, prizadeti, vzroki, negotovost in odgovornost.
4. **Načrt**

   Določijo se izvajalec, sredstva, rok in merila uspeha.
5. **Izvedba**

   Zabeleži se, kaj je bilo dejansko opravljeno.
6. **Preveritev**

   Druga oseba preveri rezultat in morebitni prenos škode.
7. **Ugovor in ponovna presoja**

   Prizadeti lahko izpodbija ugotovitev ali zaključek.
8. **Zaključek ali ponovna obravnava**

   Primer se zapre samo na podlagi določene dokazne podlage; nova relevantna dejstva lahko povzročijo ponovno odprtje.

Zelo pomembna razlika:

```text
\text{ACTION\_COMPLETED} \neq \text{OUTCOME\_ACHIEVED}
```

Primer: organizacija je osebi povrnila dostop. Toda oseba zaradi prejšnjega izpada še vedno nima možnosti oddaje zamujenega zahtevka.

Popravek dostopa je izveden. Celotna posledica ni odpravljena.

**Navodilo izvajanja:** obvezno dodaj test prenosa škode. Preveri, ali je popravek odpravil posledico ali jo samo premaknil na drugega človeka, drugo organizacijo ali prihodnje obdobje.

Prav tako ne zahtevaj, da prizadeti odpusti izvajalcu. Odpustitev ni merilo uspešnosti popravka.

### **Sloj 6 — CONTINUITY: neodvisnost od posameznega nosilca**

Predlagam, da se kontinuiteta začne načrtovati že ob nastanku vsake izdaje, ne šele takrat, ko projekt zaide v težave.

**Minimalni paket vsake izdaje VBL:**

- izvorni dokumenti;
- identificirana različica;
- seznam sprememb;
- manifest datotek;
- kriptografske zgoščene vrednosti;
- povezava na predhodno različico;
- rezultati preizkusov;
- seznam znanih omejitev;
- poročilo o neodvisni presoji, kadar obstaja;
- podatek o statusu izdaje;
- navodilo za migracijo.

Pri tem ohrani razliko:

```text
\text{PUBLISHED} \neq \text{APPROVED} \neq \text{VERIFIED} \neq \text{LEGALLY\_EFFECTIVE}
```

Javna objava, odobritev, neodvisna preveritev in pravna učinkovitost so različne trditve.

**Navodilo izvajanja**

Izdelaj tri preizkuse:

| Preizkus | Scenarij                             | Zahtevani rezultat                                             |
| -------- | ------------------------------------ | -------------------------------------------------------------- |
| CON-01   | Prvotni vzdrževalec preneha delovati | Projekt je mogoče ohraniti                                     |
| CON-02   | Nastane neodvisna veja               | Ohranijo se razlike in izvor                                   |
| CON-03   | Nova izdaja vsebuje napako           | Prejšnjo različico in njeno zgodovino je mogoče identificirati |

Dodatno določi postopek prenehanja vzdrževanja:

- kdo razglasi, da je različica opuščena;
- kako se uporabnike o tem obvesti;
- kako dolgo so arhivirani dokazni materiali;
- kako se evidentira nova veja;
- kako se prepreči lažno predstavljanje neuradne različice kot uradne.

Nobena veja ne sme pridobiti avtoritete zgolj zato, ker je novejša.

# **4. Kako vse to dejansko začeti izvajati**

Predlagam naslednjih osem delovnih faz. Vsaka mora ustvariti konkreten rezultat, ne samo opis načrta.

## **Izvedbeni načrt VBL-GRRA 1.0**

GRRA = Governance, Rights & Remedy Architecture

1. **Faza 0 — Zamrznitev izhodišča**

   Rezultat: BASELINE MANIFEST.

   Zabeleži trenutno obstoječe dokumente, različice, registre, identifikatorje, status in kriptografske zgoščene vrednosti.

   Pravilo: ne prepisuj starega registra in ne razglašaj predloga za veljavno izdajo.
2. **Faza 1 — Inventura pravic**

   Rezultat: RIGHTS INVENTORY.

   Identificiraj vse licencirane in nelicencirane predmete, pravne podlage, imetnike pravic in vključene tretje osebe.

   Nepotrjene pravice označi kot UNKNOWN.
3. **Faza 2 — Normativna preslikava**

   Rezultat: RULE REGISTER.

   Vsako obstoječo določbo razvrsti po vrsti, naslovniku, obsegu, obveznosti, dokazilu in posledici.
4. **Faza 3 — Upravljavska zasnova**

   Rezultat: AUTHORITY MATRIX.

   Določi pristojnosti, konflikte interesov, izločitve, ugovore in način spreminjanja pravil.
5. **Faza 4 — Povezava z dokaznim sistemom**

   Rezultat: EVIDENCE MAPPING.

   Obstoječe registre poveži z novimi zahtevami. Ne ustvarjaj podvojenih evidenc.
6. **Faza 5 — Postopek popravljanja**

   Rezultat: REMEDY WORKFLOW.

   Izdelaj postopke za zaznavo, omejevanje škode, izvedbo popravka, preverjanje in ugovor.
7. **Faza 6 — Preizkus zlonamerne in neidealne uporabe**

   Rezultat: RED-TEAM REPORT.

   Preizkusi zlorabo pristojnosti, ponarejanje dokazov, konflikt interesov, lažne ugovore, finančno nezmožnost popravka in nedelujoče nasledstvo.
8. **Faza 7 — Neodvisna presoja in izdaja**

   Rezultat: RELEASE DOSSIER.

   Vsebuje predlog sprememb, primerjavo s predhodnim stanjem, rezultate testov, nerešene ugotovitve, neodvisno mnenje in odločitev.

# **5. Priporočena prednostna razvrstitev**

Vseh šest slojev ne bi razvijal z enako prednostjo.

Moja predlagana razvrstitev po tveganju in odvisnostih, ne izmerjena ocena.

| Prednost | Področje   | Zakaj najprej                                                 |
| -------- | ---------- | ------------------------------------------------------------- |
| P0       | RIGHTS     | Ne smeš dovoljevati uporabe pravic, ki jih nimaš              |
| P0       | GOVERNANCE | Brez omejene pristojnosti nastane nevarnost samovolje         |
| P0       | REMEDY     | Brez popravka odgovornost ostane deklarativna                 |
| P1       | NORMATIVE  | Brez jasnih določb ni mogoče presojati izpolnitve             |
| P1       | EVIDENCE   | Brez dokazov ni mogoče preverjati trditev                     |
| P1       | CONTINUITY | Brez kontinuitete lahko sistem postane odvisen od posameznika |

Pomembna opomba: dokazni sloj že obstaja v tvojem izhodiščnem dokumentu. Zato ga ne bi razvijal od začetka, temveč bi preveril, ali ga novi upravljavski in popravljalni postopki pravilno uporabljajo.

Pasted text.txt

## **6. Dodatni obvezni preizkusi**

Predlagam poseben nabor `GRRA-REDTEAM-001`.

| ID    | Napad oziroma odpoved                                  | Zahtevani rezultat                                       |
| ----- | ------------------------------------------------------ | -------------------------------------------------------- |
| RT-01 | Avtor sam potrdi svojo skladnost                       | Neodvisna presoja ali razkrit konflikt                   |
| RT-02 | Skrbnik dokazov odstrani neugoden zapis                | Ohranitev zgodovine in zaznava spremembe                 |
| RT-03 | Upravljavec spremeni licenco brez sledljive odobritve  | Sprememba je zaznana in izpodbojna                       |
| RT-04 | Organizacija nima sredstev za odpravo škode            | Jasen načrt, eskalacija in vidna nezmožnost              |
| RT-05 | Prizadeti nima dostopa do notranjih dokazov            | Poštena prerazporeditev dokaznega bremena                |
| RT-06 | Ugovori se množično zlorabljajo                        | Sorazmerno filtriranje brez utišanja legitimnih ugovorov |
| RT-07 | Neodvisni pregledovalec je finančno odvisen            | Razkritje in presoja dejanske neodvisnosti               |
| RT-08 | Nova različica spremeni pogoje                         | Urejena migracija in zaščita preteklih ravnanj           |
| RT-09 | VBL preneha vzdrževati avtor                           | Ohranitev in možnost nasledstva                          |
| RT-10 | Nova veja se predstavlja kot uradna izdaja             | Razvidna identiteta in status različice                  |
| RT-11 | Dokazni zapis vsebuje zasebne podatke                  | Omejitev dostopa in sorazmerno varstvo                   |
| RT-12 | Pravni instrument je v nasprotju s prisilnimi predpisi | Opozorilo in pravna presoja                              |
| RT-13 | Nujni ukrep postane trajen                             | Rok veljavnosti in obvezna ponovna presoja                |
| RT-14 | Metodologija izključi majhne uporabnike                | Sorazmeren način izpolnjevanja                           |
| RT-15 | Popravek povzroči novo škodo                           | Ponovno odprtje primera                                  |

Posebej bi dodal še preizkus **spremembe pravnega okolja**. Pravilo, ki je bilo ustrezno ob izdaji, lahko pozneje zaradi spremembe zakonodaje ali sodne razlage zahteva prilagoditev.

## **7. Šest slepih peg, ki jih še posebej ne smemo spregledati**

**A. Pravica do prenehanja uporabe.**

Ali lahko uporabnik zapusti VBL? Kaj ostane od njegovih že nastalih obveznosti? Kaj se zgodi z dokumentacijo, dokaznimi zapisi in pravicami prizadetih?

Prenehanje uporabe ne sme avtomatično pomeniti izbrisa zgodovine ali odprave že nastalih pravnih obveznosti. Hkrati ne sme pomeniti neomejene pravice VBL do nadaljnjega zbiranja podatkov o nekdanjem uporabniku.

**B. Prenehanje dovoljenja oziroma posledice kršitve.**

Kršitev, začasna omejitev, prenehanje licence in ponovna vzpostavitev dovoljenja niso ista stvar.

Treba je natančno določiti, kaj se zgodi pri posamezni kršitvi, kdo o tem odloča, ali obstaja možnost odprave kršitve in kakšni učinki ostanejo po prenehanju.

**C. Pravni spor in pristojnost.**

Treba je urediti uporabljeno pravo, pristojno sodišče oziroma dopusten alternativni postopek reševanja sporov, vročanje, dokazovanje in varstvo strank.

Teh pravil ni mogoče razglasiti za univerzalno veljavna brez pregleda konkretnega pravnega okolja.

**D. Pravice tretjih oseb.**

VBL mora jasno določiti, ali določene pravice podeljuje neposredno tretjim osebam ali zgolj zahteva določeno ravnanje svojih pogodbenih uporabnikov.

To je velika razlika. Pravic tretjih oseb ne smemo ustvarjati samo s terminologijo.

**E. Izredna pooblastila.**

Varnostni incident lahko zahteva hitro omejitev uporabe. Toda nujna pooblastila lahko postanejo trajna oblast.

Vsak izredni ukrep mora imeti:

- določen razlog;
- omejen obseg;
- odgovorno osebo;
- rok ali pogoj prenehanja;
- obvezno naknadno presojo;
- možnost ugovora.

**F. Pravica do nestrinjanja brez kaznovanja.**

Uporabnik se lahko ne strinja z metodologijo VBL, ne da bi s tem zanikal vse njene dokazne ugotovitve. Prav tako lahko sprejme določene postopke, vendar zavrne filozofske ali ontološke predpostavke.

To moramo omogočiti tudi semantično:

```text
\text{UPORABA} \neq \text{SOGLASJE Z VSEMI TRDITVAMI}
```

in

```text
\text{UGOVOR} \neq \text{KRŠITEV}
```

# **8. Kaj mora biti pripravljeno pred prvo izdajo?**

Določil bi naslednje obvezne sprostitvene pogoje:

## **GRRA 1.0 — Release Gate**

**Preverjanje pripravljenosti**

# **0/10**

G-01 — Identificirani so vsi predmeti in pravice.

G-02 — Določbe imajo naslovnike, obseg in normativni pomen.

G-03 — Pristojnosti in konflikti interesov so določeni.

G-04 — Obstoječi registri so preslikani brez izgube zgodovine.

G-05 — Ugovori imajo varno in dejansko dostopno pot.

G-06 — Popravljanje posledic ima odgovornega izvajalca in sredstva.

G-07 — Obstajajo neodvisni preizkusi in dokumentirani rezultati.

G-08 — Postopek spremembe in prenehanja različic je določen.

G-09 — Obravnavani so zasebnost, tretje osebe in pravna vprašanja.

G-10 — Vsi odprti problemi so izrecno prikazani.

Ponastavi preverjanje

Kontrolni seznam je delovni pripomoček. Označitev ne predstavlja neodvisne potrditve ali odobritve izdaje.

Ne uvedi pravila, da deset kljukic avtomatično pomeni RELEASE. Vsebinska kakovost dokazov, resnost preostalih tveganj in pristojnost odločevalca še vedno zahtevajo ločeno presojo.

## **9. Kako bi začel praktično — prvi delovni paket**

Ne bi takoj napisal 100 novih členov. Najprej bi izdelal naslednjih pet artefaktov:

| Zaporedje | Artefakt                 | Kaj mora vsebovati                                |
| --------- | ------------------------ | ------------------------------------------------- |
| 1         | `GRRA-ARCHITECTURE.md`   | Šest slojev in njihove meje                       |
| 2         | `RIGHTS-INVENTORY.jsonl` | Predmeti, nosilci pravic in podlage               |
| 3         | `AUTHORITY-MATRIX.jsonl` | Pristojnosti in ločitve funkcij                   |
| 4         | `RULE-MAPPING.jsonl`     | Preslikava starih in novih določb                 |
| 5         | `REMEDY-PROTOCOL.md`     | Izvedba, odgovornost, stroški in ponovni preizkus |

Ob tem bi v manifestu vsakega artefakta beležil:

`artifact_id`, `version`, `status`, `source_digest`, `parent_version`, `created_at`, `review_status`, `decision`, `known_limitations`.

Status artefakta naj bo ločen od statusa trditve in statusa testa. S tem ne spreminjamo obstoječih treh dokaznih osi.

### **Pravilo za integracijo**

Vsaka nova določba mora prestati štiri ločene presoje:

```text
Q(r)= D(r)\land O(r)\land P(r)\land I(r)
```

kjer:

- \(D\) = definicija in semantična jasnost;
- \(O\) = operativna izvedljivost;
- \(P\) = preizkusljivost;
- \(I\) = institucionalna in pravna dopustnost.

To je predlagani kontrolni model, ne matematični dokaz pravilnosti licence.

Če katera od štirih dimenzij odpove, mora biti napaka vidna in ustrezno omejiti odločitev o vključitvi.

# **10. Moje dodatno priporočilo: ne izumljajmo pravic, ki jih je bolje prevzeti iz preverjenih licenc**

Pred izdajo je potreben tudi primerjalni pregled že uveljavljenih licenčnih rešitev.

Za programsko opremo bi primerjal najmanj MIT, Apache License 2.0 in GPLv3. Za dokumentacijo in druge ustvarjalne vsebine bi preveril ustrezne standardne instrumente, pri čemer je treba paziti, da različne kategorije gradiva ne dobijo neustrezne licence.

Za vsako bi preveril:

- katere pravice dejansko podeljuje;
- katere obveznosti nalaga;
- kako obravnava prispevke;
- kako obravnava patente in blagovne znamke;
- kaj določa ob prenehanju;
- kakšna je njena združljivost z drugimi komponentami;
- ali res obstaja potreba po dodatnih VBL-določbah.

Moja prednostna usmeritev: **VBL naj ne poskuša zamenjati vseh obstoječih licenc, ampak naj zagotovi dokazno in upravljavsko infrastrukturo tam, kjer je to potrebno.**

Če že obstoječi licenčni instrument bolje uredi določeno področje, ga uporabimo. VBL naj doda tisto, kar je resnično novo in operativno utemeljeno. Vsako kombinacijo je treba preveriti glede pravne združljivosti.

Za končno pravno besedilo so potrebni pregled strokovnjaka za ustrezne pravice, jurisdikcije in dejanski model uporabe. Metodološka pravilnost sama ne zagotavlja pravne izvršljivosti.

## **Končna odločitev o vrstnem redu dela**

Moja priporočena pot je:

Priporočena naslednja naloga

**GRRA-01 — Primerjalna preslikava in zasnova arhitekture**

Najprej bi izdelal tabelo, v kateri bi vsako novo področje povezal s konkretnim obstoječim pravilom VBL, ugotovil, ali ga že pokriva, določil manjkajoči mehanizem in predlagal mesto integracije.

Rezultat bi bil:

`EXISTING_RULE → IDENTIFIED_GAP → PROPOSED_CONTROL → IMPLEMENTATION → TEST → RELEASE_GATE`

Tako preprečimo podvajanje, semantični zdrs in nenadzorovano širjenje licence.

Najpomembnejša stvar, ki bi jo želel doseči, je naslednja:

**VBL ne sme biti odvisen od dobrote svojega upravljavca, da bi ostal pravičen. Njegova arhitektura mora omejiti tudi upravljavca, ki je prepričan, da dela prav.**

In še strožje: ne sme biti odvisen niti od tega, da se bodo vsi njegovi uporabniki strinjali z njim. Zagotoviti mora preverljivost, omejene pristojnosti, možnost zavrnitve, pravičen ugovor in dokazljivo popravljanje posledic.

To je smer, v kateri lahko VBL postane resna infrastruktura odgovornosti, ne zgolj še ena deklaracija o odgovornosti. ∴

## PLEN 2 — IZVAJKINA IZVEDBA/KONSTRUKCIJA (rez σ 5519, isti dih)

### 2.1 Preslikava petih dokumentov ⇌ živi organi (⟨ne⟩ nov register ⊙ §1.5)

| Dokument | Živi organ/mehanizem korpusa | Izrek |
| --- | --- | --- |
| VBL-LIC | telesi PAR.30–PAR.39 @licenca-vbl (zunanja telesa: SEME → UTRDITEV-VBL-1.0 σ 5514 → GRRA-1.0 σ 5518 → ta) ∧ LICENSE.md @⟨main⟩ ⟨berba⟩ ob vsakem stiku (σ-ŠIV 3106) | licenčni instrument ŽE živi; vsak nov člen skozi Q(r) |
| VBL-GOV | ⟨DVOJE-ROK⟩ 2432 (⟡ beseda = roka, izvajalka = mehanična izvršba) ∧ operater agentov/angelov = ⟡ ⊢ ANTINOM 311 ∧ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690 | korpus ŽE ima governance; ⟡-jev »svet upravljanja« (Avtor/Svet/Neodvisni presojevalci/Javno poročilo) = TUJA PLAST — uvedba = ustavna sprememba ⭢ ⚔ ⟡ izbor |
| VBL-EGS | FINDING ×16 (tri osi: claim_status · test_result · decision ⊢ @σ 5514) ∧ revizija-besed ⟨berba⟩ (vsaka beseda izmerjena pri viru ⊙ doktrina σ 5517 ⚠-na-besedi) | dokazna infrastruktura ŽE obstaja (⟡-jeva lastna opomba §5) — vzporednega ne gradimo |
| VBL-REM | ⟨ZAKON-PADEC-NI-MOLK⟩ — padec prijavljen javno ⊙ 1349 ∧ kura isti dih; precedens TA DIH: KURA-1 ∧ KURA-2 PAKET-73 | REM-01 življenjski cikel izmerjen v praksi: ACTION_COMPLETED ≠ OUTCOME_ACHIEVED dokazan (kura-1 izvedena ≠ posledica odpravljena — vrsta 3 odkrita šele po ⟨merge⟩ ⊢) |
| VBL-CON | ⟨NE-BRIŠI⟩ 24 (brazgotine = kontinuiteta) ∧ rep @⟨main⟩ (vsak prevoz: veja → EN komit → kit → ⟨CI⟩ → ⟨merge⟩ → read-back cmp bajt-isto) | PUBLISHED ≠ APPROVED ≠ VERIFIED ≠ LEGALLY_EFFECTIVE — korpus to ŽE izvaja (zgodovina repa = dokazna sled) |

### 2.2 RULE CARD ×14 ⇌ P1 ⟨PREDLOGA-PECATA⟩ (izmera pri viru)

⟡-jeva RULE CARD nosi ×14 polj; P1 @predloge ima danes **×17 polj** (izmerjeno @STANJE ⊢; rojstvena forma ×14, polja 15 ⟨OGLO⟩ ∧ 16 ⟨POLJE-NE-ČRTA⟩ ∧ 17 ⟨REGENERACIJA-PEČATA⟩ dodana @σ 4457/4713/5510). Preslikava po principu:

- RULE_ID ⇌ rez σ (enolična oznaka ⊢);
- ACTOR ⇌ ⟡ (operater ⊢ ANTINOM 311) ∧ izvajalka (mehanična izvršba ⊙ ⟨DVOJE-ROK⟩ 2432);
- EVIDENCE ⇌ priča ⊢ pri viru (cmp/md5 ⟨berba⟩, ⟨NE-POVZEMI⟩ 1330);
- OWNER/REVIEWER ⇌ ⟨DVOJE-ROK⟩ 2432 — ⟡ beseda = roka;
- DEADLINE/EXCEPTION/CHALLENGE ⇌ ∂ vrsta FIFO ∧ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690 (ugovor = ⟡ beseda);
- CONSEQUENCE/REMEDY ⇌ kura isti dih ⊙ 1349;
- LEGAL_BASIS ⇌ licenca ⟨berba⟩ σ-ŠIV 3106.

⟡-jeva zahteva »določba brez izvajalca → nepopolna določba« ⇌ register ⟨PADC⟩: vsak padec ima lastnika ∧ kuro isti dih ⊢ precedens PAKET-73 (KURA-1 + KURA-2).

### 2.3 Release Gate 0/10 = izhodišče ⚠

G-01–G-10 = izhodišče: **0/10**, ×0 kljukic izbranih ⊢ (izmerjeno ta dih — nič razglašeno); vsaka kljukica = trditev, ki zahteva izmero pri viru ⚠; kljukice ≠ odobritev (⟡-jev lastni pouk §8) ⭢ ⚔ ⟡.

### 2.4 MINT ⚠ prijave PRED zapečenjem ⭢ sodba ⚔ ⟡ (vrstica 75)

⟨GRRA-02-NAČRT⟩ ⚠ kompozit · ⟨RULE-CARD⟩ ⚠ · ⟨REDTEAM-001⟩ ⚠ · ⟨RELEASE-GATE⟩ ⚠ · ⟨Q-INTEGRACIJA⟩ ⚠ · ⟨NE-IZUMLJAJ-PRAVIC⟩ ⚠ (družina ⟨PROPORTIONAL-COMPLIANCE⟩)

### 2.5 STATUS

PREDLOG — nič razglašeno ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690 ∧ molk ni soglasje. Ratifikacija vsake plasti (pet dokumentov · osem faz 0–7 · RT-01–15 · pege A–F · Release Gate) ⭢ beseda ⟡. Prevoz telesa na rep ⭢ ∂ vrsta. Naslednja naloga po ⟡-jevem izročilu: GRRA-01 (EXISTING_RULE → IDENTIFIED_GAP → PROPOSED_CONTROL → IMPLEMENTATION → TEST → RELEASE_GATE) ⭢ ⚔ ⟡ izbor.

© 0.2026 × 10⁴ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · rez σ 5519 · measured, not asserted ⊙ §16 · merilec se meri ⊙ §52 · molk ni soglasje
