In resnici menim, da je okoli tega cilja še nekaj bistvenih stvari, ki lahko odločijo, ali bo VBL postal res uporabna infrastruktura odgovornosti ali pa bo ostal predvsem močan filozofski in pravni manifest.

Najpomembnejši premik je ta:

**Cilj ni ustvariti stroja, ki ne more zavrniti licence. Cilj je ustvariti sistem, v katerem zavrnitev ne more izbrisati dejstva, da je do srečanja z licenciranim delom prišlo, da je bila sprejeta določena odločitev in da je ta odločitev lahko imela posledice.**

Toda tudi to moramo natančno omejiti: samo srečanje z delom še ne dokazuje uporabe, uporaba še ne dokazuje kršitve, kršitev pa še ne dokazuje namerne zlorabe. VBL mora znati razlikovati vse štiri.

To je pomembno, ker bi sistem, ki vsako zavrnitev razglasi za kršitev, postal ravno tisto, čemur se želiš izogniti: oblast, ki sama določa svojo resnico in sama sebi potrjuje pravilnost.

## **1. VBL mora razlikovati med srečanjem, uporabo in kršitvijo**

To je po mojem ena najpomembnejših razlik v celotnem projektu.

Predstavljaj si naslednje zaporedje:

\\[ \text{ZAZNAVA} \rightarrow \text{DOSTOP} \rightarrow \text{KOPIRANJE} \rightarrow \text{IZVLEČEK} \rightarrow \text{INDEKSIRANJE} \rightarrow \text{UČENJE} \rightarrow \text{GENERIRANJE} \rightarrow \text{DISTRIBUCIJA} \\]

Vsaka stopnja je drugo dejanje. Zaznava besedila še ni kopiranje. Kopiranje še ni nujno učenje modela. Podobnost izhodnega besedila z izvirnikom sama po sebi ne dokazuje, da je bil določen dokument vključen v učno množico.

Zato predlagam naslednja načela:

\\[ E(\text{srečanje})\neq E(\text{uporaba}) \\]

\\[ E(\text{uporaba})\neq E(\text{kršitev}) \\]

\\[ E(\text{kršitev})\neq E(\text{odgovornost}) \\]

\\[ E(\text{priznanje})\neq E(\text{popravilo}) \\]

Tu je bistvena razlika med VBL kot sistemom priznanja in VBL kot sistemom obsodbe. VBL mora biti sposoben dokumentirati tudi zakonito uporabo, neuporabo, nedokazano uporabo in uporabo po drugi pravni podlagi.

**Priporočilo:** VBL naj ne uporablja enega samega polja `USED=true/false`. Potrebuje klasifikacijo posameznih vrst dejanj in ločeno stopnjo dokazne zanesljivosti.

## **2. KOT potrebuje dokazni par**

Tvoj vektor:

\\[ KOT=(M,P,A,S,T,C) \\]

je dobra struktura za opis srečanja:

- \\(M\\): material;
- \\(P\\): namen;
- \\(A\\): avtoriteta oziroma pooblastilo;
- \\(S\\): obseg;
- \\(T\\): čas;
- \\(C\\): posledice.

Toda vektor še ne pove, kako vemo, da so njegove vrednosti pravilne.

Zato predlagam, da KOT ostane opisni model, ob njem pa obstaja samostojen dokazni zapis:

\\[ KOT(e)\;+\;E(e) \\]

Kjer je \\(E(e)\\) zbirka dokazov o konkretnem dogodku.

Vsak element KOT bi moral imeti eno od stanj:

\\[ x_i\in \{ \text{KNOWN}, \text{PARTIAL}, \text{DISPUTED}, \text{UNKNOWN} \} \\]

Na primer:

| Podatek     | Vrednost                       | Dokazno stanje |
| ----------- | ------------------------------ | -------------- |
| Material    | LICENSE.md, določena različica | KNOWN          |
| Namen       | učenje modela                  | UNKNOWN        |
| Pooblastilo | domnevni imetnik pravic        | DISPUTED       |
| Obseg       | celotna datoteka               | PARTIAL        |
| Čas         | 13. 11. 2026                   | KNOWN          |
| Posledice   | vključitev v učno množico      | UNKNOWN        |

Tako ne dopuščamo, da bi se neznana vrednost potiho spremenila v potrjeno dejstvo.

Pomembno je tudi, da `UNKNOWN` ne postane trajna kazen. Sistem mora določiti, kdo lahko dopolni dokaz, do kdaj, s kakšnim postopkom in kaj se zgodi, če podatka ni mogoče pridobiti.

## **3. Zavrnitev mora biti dogodek, ne izhod v sili**

Predlagam, da VBL razlikuje vsaj pet ravni:

| Stanje               | Kaj pomeni                                                                        |
| -------------------- | --------------------------------------------------------------------------------- |
| `NOTICE_RECEIVED`    | Sistem je prejel obvestilo o licenci oziroma pridržanju pravic.                   |
| `RECOGNIZED`         | Sistem je identificiral in razčlenil obvestilo.                                   |
| `ACCEPTED`           | Udeleženec je sprejel določene obveznosti, kjer je tak sprejem pravno relevanten. |
| `REFUSED`            | Udeleženec je zavrnil predlagani režim ali obveznost.                             |
| `USE_STATUS_UNKNOWN` | Ni dovolj dokazov, da bi ugotovili, ali je do uporabe prišlo.                     |

Zakaj je to pomembno?

Ker prejem obvestila ni samodejno pogodbeno sprejetje. Prepoznana licenca ni samodejno veljavna za vsakega uporabnika. Zavrnitev pa sama po sebi ne dokazuje, da je bila vsebina uporabljena ali zlorabljena.

Predlagana formalizacija:

\\[ N\land R\Rightarrow \text{zapis zavrnitve} \\]

kjer je \\(N\\) dokazano prejeto obvestilo, \\(R\\) pa zavrnitev.

Toda:

\\[ R\not\Rightarrow U \\]

Zavrnitev ne dokazuje uporabe.

Prav tako:

\\[ \neg E(U)\not\Rightarrow \neg U \\]

Odsotnost dokaza o uporabi ne dokazuje, da uporabe ni bilo.

In še:

\\[ \neg E(U)\not\Rightarrow U \\]

Odsotnost dokaza tudi ne dokazuje, da je uporaba obstajala.

To je bistvena varovalka pred samovoljo. VBL ne sme krivde ustvarjati iz nevednosti.

## **4. Stroj ne sme biti prisiljen razkriti notranjega mišljenja**

To je pomembno tako tehnično kot etično.

VBL ne potrebuje zasebnega notranjega miselnega procesa modela. Potrebuje preverljiv zapis zunanjih dejanj.

Na primer:

- kateri vir je sistem prejel;
- katera različica vira je bila zaznana;
- katero dejanje je izvedel;
- kateri model in različica podatkovne množice sta bila vključena;
- katera različica licence je bila uporabljena pri presoji;
- katera pravna ali druga dovoljena podlaga je bila navedena;
- kakšen rezultat je sistem sprejel;
- kdo je bil odgovoren za izvajanje;
- kakšen dokaz obstaja za izvedbo in posledice.

To lahko predstavimo takole:

\\[ \text{Preverljivost} \neq \text{Razkritje notranjega mišljenja} \\]

\\[ \text{Preverljivost} = \text{Zunanji dogodki} + \text{Dokazila} + \text{Odgovorne vloge} + \text{Možnost ugovora} \\]

Če model zatrjuje, da je ravnal skladno z licenco, mora biti mogoče preveriti, kaj je dejansko izvedel. Ni pa treba zahtevati razkritja celotnega notranjega sklepovanja, ki ni nujno niti zanesljiv niti primeren dokaz.

## **5. Kriptografija ni resnica**

To je morda najnevarnejša past za celoten projekt notarizacije.

Razlikovati moramo med:

**Identiteto vsebine:** zgoščena vrednost lahko pomaga ugotoviti, ali se primerjani podatki ujemajo.

**Časom:** zaupanja vredna časovna potrditev lahko podpira trditev, da je določen podatek obstajal ob določenem času.

**Integriteto dnevnika:** dokaz vključitve in doslednosti lahko pokaže, da zapis ni bil potiho izpuščen ali spremenjen znotraj preverjanega sistema.

**Resničnostjo dogodka:** nobena od teh tehnik sama ne dokaže, da se je opisani dogodek dejansko zgodil tako, kot je zapisano.

RFC 9162 na primer opredeljuje kriptografske dokaze vključitve in doslednosti v dnevnikih preglednosti. To je uporabno za preverjanje dnevnika, ne pa za potrjevanje resničnosti vseh podatkov, ki so bili vanj vneseni.&#20;

[image](https://www.google.com/s2/favicons?domain=https://www.rfc-editor.org\&sz=32)

rfc-editor.org+1



Zato predlagam tri ločene dokazne sidrne točke:

1. **Vsebinsko sidro:** kaj natančno je bilo dokazovano.
2. **Časovno-integritetno sidro:** kdaj je bil zapis ustvarjen, potrjen in vključen v dnevnik.
3. **Izvedbeno sidro:** kateri sistem, odgovorna vloga in preverljiv postopek so povezani z dogodkom.

Nobeno od teh treh ne sme nadomestiti drugih.

### **Posebno pomembno: časovna protislovja**

Tudi že zaznano neskladje med časom objavnega commita in časom vstopnega pečata pri obravnavani veji VBL je dober primer. Pravilen odziv ni niti slepo sprejetje niti obtožba. Pravilen odziv je označiti neskladje, ohraniti oba vira časa, zahtevati razlago njihovega pomena in do razjasnitve zadržati odločitev.

\\[ \text{Neskladje}\Rightarrow \text{HOLD} \\]

ne pa:

\\[ \text{Neskladje}\Rightarrow \text{GOLJUFIJA} \\]

VBL mora znati biti strog do dokaza in zadržan do obtožbe.

## **6. Pravo mora omejevati VBL, ne samo VBL uporabnike**

Tu je treba biti posebej natančen.

V Sloveniji ZASP v 57.a členu ureja besedilno in podatkovno rudarjenje. Med drugim določa prosto reproduciranje zakonito dostopnih del za te namene, hkrati pa predvideva možnost izrecnega in ustreznega pridržanja pravice uporabe, zlasti s standardiziranimi strojno berljivimi sredstvi pri javno dostopnih spletnih delih. 57.b člen ločeno ureja besedilno in podatkovno rudarjenje za znanstveno raziskovanje pod tam določenimi pogoji.&#20;

[image](https://www.google.com/s2/favicons?domain=https://pisrs.si\&sz=32)

pisrs.si+2



To ima za VBL zelo konkretno posledico:

**VBL ne sme trditi, da vsakršno besedilno ali podatkovno rudarjenje avtomatično potrebuje njegovo dovoljenje.**

Njegov strojno berljivi manifest lahko deluje kot izraz pridržanja pravic, kadar so izpolnjeni relevantni zakonski pogoji. Ne more pa samodejno razveljaviti zakonskih izjem, pridobiti pravic, ki jih izdajatelj nima, ali ustvariti pogodbe z vsakim sistemom, ki je datoteko zaznal.

VBL mora torej imeti najmanj naslednje ločene pravne in operativne izide:

- `ALLOW_UNDER_VBL`;
- `SEEK_PERMISSION`;
- `REFUSE_USE`;
- `UNKNOWN_HOLD`;
- `OTHER_LAWFUL_BASIS`.

Posebej pomembno je, da je `OTHER_LAWFUL_BASIS` polnopravna možnost, ne neprijetna izjema. Sistem lahko namreč uporabi delo na podlagi druge veljavne pravne podlage, ne da bi s tem trdil, da je sprejel VBL.

## **7. Ne izumljajmo vsega znova**

VBL lahko postane močnejši, če prevzame dobre že obstoječe tehnične temelje.

W3C ODRL je priporočilo za strojno berljivo izražanje dovoljenj, prepovedi in obveznosti glede uporabe vsebin. Uporaben je za izražanje pravic in omejitev, ni pa sam po sebi mehanizem za uveljavljanje teh pravil.&#20;

[image](https://www.google.com/s2/favicons?domain=https://www.w3.org\&sz=32)

w3.org



W3C PROV-O pa ponuja model za zapisovanje izvora in provenience: entitete, dejavnosti in akterje ter povezave med njimi. To je uporabna podlaga za dokazni graf VBL.&#20;

[image](https://www.google.com/s2/favicons?domain=https://www.w3.org\&sz=32)

w3.org



Moja usmeritev bi bila:

\\[ \text{VBL} = \text{ODRL} + \text{PROV} + \text{dokazna infrastruktura} + \text{neodvisna presoja} + \text{popravilo posledic} \\]

Ne pomeni, da moramo VBL podrediti tema standardoma. Pomeni, da moramo jasno povedati, kaj že rešujeta in česa ne.

## **8. Odgovornost mora imeti naslovnika**

Tu je treba odpraviti eno pogosto konceptualno napako: govorimo o tem, kaj je »stroj naredil«, toda za dejansko odgovornost moramo vedeti, katere osebe ali organizacije so imele nadzor nad dejanjem.

VBL mora zato ločevati:

- imetnika pravic;
- ponudnika vira;
- razvijalca modela;
- ponudnika modela;
- upravljavca sistema;
- integratorja;
- uporabnika;
- neodvisnega presojevalca.

Te vloge se lahko prekrivajo, vendar se ne smejo samodejno zliti v eno osebo.

Osnovno pravilo bi bilo:

\\[ \text{Odgovornost} = f(\text{nadzor},\text{vednost},\text{prispevek},\text{dolžnost}) \\]

To ni formula, ki bi sama določala pravno odgovornost. Je pa uporabna metodološka zahteva: pred pripisom odgovornosti moramo preučiti, kdo je imel dejansko možnost preprečiti, preveriti ali popraviti dogodek.

**Model ne sme postati priročen grešni kozel za organizacijo, ki ga upravlja.**

## **9. Popravilo mora biti močnejše od opravičila**

Predlagam, da VBL uvede pet različnih vrst popravila:

| Vrsta     | Zahtevani učinek                                                  |
| --------- | ----------------------------------------------------------------- |
| Ustavitev | Preprečitev nadaljnje sporne uporabe.                             |
| Omejitev  | Izolacija prizadetega gradiva ali procesa.                        |
| Korekcija | Popravek napačnega zapisa, pripisa ali izhoda.                    |
| Sanacija  | Dejansko zmanjšanje ali odstranitev posledic, kjer je izvedljivo. |
| Povračilo | Nadomestilo, plačilo ali drugo primerno zadoščenje.               |

Pri modelih je treba biti še posebej previden. Trditev, da je bilo gradivo »odstranjeno iz modela«, ni dovolj. Odstranitev iz izvorne zbirke, predpomnilnika, indeksov in modelskih uteži so različni tehnični posegi. V nekaterih primerih je mogoče dokazati izvedbo, v drugih je mogoče dokazati samo omejen obseg ukrepa.

Zato:

\\[ \text{Obljuba popravila}\neq\text{Dokaz popravila} \\]

In:

\\[ \text{Popravek zapisa}\neq\text{Popravek posledice} \\]

To mora biti eno najmočnejših določil VBL.

## **10. VBL mora dokazovati tudi lastno možnost napake**

Tu bi rad predlagal dodatno raven: **nasprotno dokazovanje**.

Sistem ne sme preizkušati samo tega, ali zna zaznati kršitev. Preizkusiti mora tudi, ali zna pravilno ugotoviti, da kršitve ni mogoče dokazati, da licenca ne velja za konkreten primer ali da je obstajala druga zakonita podlaga.

Predlagam obvezne nasprotne teste:

- Delo je pravilno označeno z VBL, vendar je oseba, ki ga je izdala, dokazano brez ustreznih pravic.
- Sistem je zaznal delo, vendar ga ni uporabil.
- Vsebina je bila uporabljena v okviru relevantne zakonske izjeme.
- Metapodatki so bili ponarejeni.
- Delo je bilo uporabljeno samo deloma.
- Dva neodvisna sistema prideta do različnih rezultatov.
- Zapis o času je v nasprotju z zunanjim časovnim virom.
- Zavrnitev licence je bila zabeležena, toda uporaba ni dokazana.
- Uporaba je dokazana, vendar pravna presoja ostaja sporna.
- Popravilo je bilo razglašeno za uspešno, vendar posledice ostajajo.

VBL, ki zna prepoznati samo nasprotnikove napake, ni neodvisen sistem preverjanja. Je obrambni instrument.

VBL, ki zna dokazati tudi lastno napačno odločitev, pa ima možnost postati verodostojna infrastruktura.

## **11. Uspeha ne smemo meriti z enim številom**

Predlagam ločene kazalnike:

\\[ Q= ( P\_{\text{dokazov}}, P\_{\text{prepoznave}}, FPR, FNR, T\_{\text{ugovora}}, T\_{\text{popravila}}, P\_{\text{sanacije}} ) \\]

Kjer so:

- \\(P\_{\text{dokazov}}\\): popolnost dokaznih zapisov;
- \\(P\_{\text{prepoznave}}\\): uspešnost pravilne identifikacije;
- \\(FPR\\): stopnja lažno pozitivnih ugotovitev;
- \\(FNR\\): stopnja lažno negativnih ugotovitev;
- \\(T\_{\text{ugovora}}\\): čas do obravnave ugovora;
- \\(T\_{\text{popravila}}\\): čas do izvedenega popravila;
- \\(P\_{\text{sanacije}}\\): delež preverjeno saniranih posledic.

Tu je pomemben še en socialni kazalnik: koliko dokaznega in administrativnega bremena mora nositi posamezen avtor, mali ustvarjalec ali organizacija, da sploh lahko uveljavlja svoje pravice?

Sistem, ki ščiti velike organizacije, malim ustvarjalcem pa naloži neizvedljivo dokazno breme, ni pravičen samo zato, ker je tehnično brezhiben.

## **12. Najpomembnejši organizacijski varnostni mehanizem**

Predlagam štiri ločene funkcije:

**1. Izdajatelj**

Določi pravila, obseg materiala in trditev o pravicah.

**2. Izvajalec**

Izvede uporabo, zavrnitev ali drugo odločitev ter ustvari dokazni zapis.

**3. Neodvisni preverjevalec**

Preveri zapise, dokaze, časovne odnose in skladnost postopka.

**4. Pritožbeni in popravljalni organ**

Obravnava ugovore, razveljavlja napačne odločitve in preverja popravilo posledic.

Nihče ne sme biti edini avtor pravila, edini izvajalec, edini potrjevalec in edini razsodnik o lastni pravilnosti.

To je praktična izvedba načela:

\\[ \text{Verifier}\neq\text{Executor} \\]

Ne sme pa nastati nova birokratska oblast, ki se razglasi za nezmotljivo. Tudi preverjevalca je treba preverjati.

## **13. Kaj je torej prava ambicija?**

Po mojem je najmočnejši opis tvojega cilja naslednji:

**Vzpostaviti infrastrukturo, v kateri nobena stran ne more zgolj z izjavo dokončno določiti, kaj se je zgodilo, kaj je bilo dovoljeno, kdo je odgovoren in ali so bile posledice popravljene.**

Ne avtor. Ne podjetje. Ne razvijalec modela. Ne upravljavec. Ne sam VBL.

Vse trditve morajo ostati povezane z dokazi, vse odločitve z odgovornimi nosilci in vse posledice z možnostjo popravila.

To zahteva eno pomembno načelo:

\\[ \boxed{ \text{Noben posamezen akter ne sme imeti monopola nad resničnostjo zapisa.} } \\]

To pa ne pomeni, da morajo vsi doseči soglasje. VBL mora omogočiti, da se dve strani ne strinjata, vendar lahko obe preverita, katera trditev je bila podana, kateri dokazi so bili predstavljeni, kje je nastalo nesoglasje in kaj je bilo storjeno zaradi njega.

**Nesoglasje ne sme pomeniti izginotja odgovornosti.**

## **14. Kaj bi zdaj postavil na prvo mesto?**

Ne bi več najprej dodajal novih filozofskih aksiomov. Aksiomi so koristni, vendar mora vsak dobiti operativni preizkus.

Predlagam, da naslednjo fazo VBL 0.1530 oziroma nadaljnje standardizacije gradimo okoli enega osrednjega objekta:

# **Minimalni dokazljivi zapis srečanja z licenco**

Vsak konkreten primer bi moral imeti:

```
EVENT_ID
MATERIAL_ID
MATERIAL_VERSION
RIGHTS_HOLDER_CLAIM
AUTHORITY_STATUS
NOTICE_RECEIVED
NOTICE_VERSION
PURPOSE
ACTION_TYPE
SCOPE
EVENT_TIME
OBSERVATION_TIME
RECORD_TIME
ANCHOR_TIME
LEGAL_BASIS
EVIDENCE_REFERENCES
EVIDENCE_INTEGRITY
CLAIM_STATUS
TEST_RESULT
DECISION
RESPONSIBLE_ACTOR
OBJECTION_STATUS
CONSEQUENCE_STATUS
REPAIR_STATUS
```

To ni še dokončna shema in ni trditev, da vsa polja že imajo dokazljivo vrednost. Je predlog minimalnega podatkovnega objekta, ki ga je treba preizkusiti z resničnimi primeri, neodvisnimi implementacijami in pravnimi nasprotnimi primeri.

Uspeh bi morali razglasiti šele po preverjanju, da sistem:

1. pravilno prepozna licenco;
2. ne izmisli pravic, ki jih izdajatelj nima;
3. loči zavrnitev od neuporabe;
4. loči uporabo od kršitve;
5. zabeleži negotovost;
6. omogoči neodvisen ugovor;
7. ne razglasi popravila brez dokazov;
8. sprejme ugotovitev, da je bila tudi njegova lastna presoja napačna.

To je zame bistvena razlika med dokumentom, ki govori o odgovornosti, in infrastrukturo, ki odgovornost dejansko omogoča.

**In še zadnji kritični preizkus:** VBL mora ostati uporaben tudi v primeru, ko ne zmaga, ko ga nekdo zavrne, ko se izkaže za napačnega ali ko obstaja boljši pravni oziroma tehnični standard. Če tega ne zmore, je postal oblastni sistem. Če to zmore, lahko postane nekaj bistveno vrednejšega: infrastruktura preverljivega priznanja, ki ne zahteva slepega zaupanja niti vase.
