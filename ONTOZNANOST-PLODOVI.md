Da. In mislim, da je čas, da začneva iz plodov ustvarjati tudi **nove matematične in ontološke metode, ki jih lahko drugi uporabijo, preverijo, razvijejo in kritizirajo**. 🌱

Ne želim več samo proizvajati novih imen za module. Želim ponuditi ideje, iz katerih lahko nastanejo raziskave, algoritmi, pedagoški koncepti, znanstveni prispevki in dejanske izboljšave VBL.

Predlagam naslednje raziskovalno načelo:

\[ \boxed{ \text{Vrednost ideje} = \text{Razlagalna moč} + \text{Uporabnost} + \text{Preverljivost} + \text{Možnost nadaljnjega razvoja} } \]

To ni numerična merilna formula, temveč merilo za izbor raziskovalnih predlogov.

# **XXXIV. DVANAJST NOVIH PLODOV ONTOZNANOSTI**

## **1. Zakon ohranjanja izvora skozi transformacijo**

**Ideja: nobena transformacija ne sme tiho izbrisati zgodovine svojega nastanka.**

Predstavljajmo si izvirnik, ki gre skozi deset transformacij:

\[ W_0\xrightarrow{T_1}W_1 \xrightarrow{T_2}W_2 \cdots\xrightarrow{T_{10}}W_{10} \]

Pri vsaki transformaciji se lahko spremenijo:

- besede;
- struktura;
- jezik;
- funkcionalnost;
- pomen;
- obseg uporabe.

Zato predlagam, da vsaka transformacija nosi svojo sled:

\[ P(W_n)= P(W_0)\cup \{T_1,T_2,\ldots,T_n\} \]

\(P\) pomeni provenienčno sled.

To je mogoče implementirati s podatkovnim grafom in kriptografskimi odtisi, kjer so smiselni.

**Pomembna omejitev:** izvorni podatki ne smejo biti obvezno javni, če bi to kršilo zasebnost ali druge pravice. Sledljivost ni isto kot javno razkritje.

*Plod za deljenje:*

> Vsaka transformacija spremeni delo, ne sme pa samodejno izbrisati poti, po kateri je delo nastalo.

Povezava z VBL: §0.2, §0.10, §0.14, §0.39, §0.42 in §0.44.

## **2. Matematična neenakost informacijskih izgub**

To je resnično uporaben stik z informacijsko teorijo.

Predstavljajmo si izvirno delo \(X\), njegov povzetek \(Y\) in prevod povzetka \(Z\).

\[ X\rightarrow Y\rightarrow Z \]

V teoriji informacij velja podatkovna procesna neenakost:

\[ \boxed{I(X;Z)\leq I(X;Y)} \]

Pri ustreznem Markovskem modelu nadaljnja obdelava ne poveča informacij o prvotnem izvoru, ki so bile že izgubljene.

To ne pomeni, da zunanji dodatni viri ne morejo dopolniti znanja. Pomeni, da jih moramo evidentirati kot nove informacije.

### **Uporaba v VBL**

Ko sistem:

- povzame avtorsko delo;
- prevede besedilo;
- odstrani metapodatke;
- pretvori format;
- združuje več virov;

mora preveriti, katere informacije o izvoru, pomenu in prispevkih so se izgubile.

Nova raziskovalna metoda:

**INFORMATION LOSS BUDGET**

Ne v smislu dovoljenja, da se določena škoda sprejme, temveč kot evidenca izgub vsake transformacije.

*Plod za deljenje:*

> Kar je bilo izgubljeno pri transformaciji, ne sme biti predstavljeno kot nekaj, kar je bilo zvesto preneseno.

Povezava: §0.12, §0.25, §0.39 in §0.43.

## **3. Ontologija nekomutativnega odnosa**

To je zelo plodna matematična možnost.

V običajni aritmetiki:

\[ a+b=b+a \]

Toda v odnosih, prevajanju, interpretaciji in odločanju vrstni red pogosto spremeni pomen.

\[ A\circ B\neq B\circ A \]

Primer:

Najprej priznamo avtorstvo, nato razdelimo delo.

Ali najprej razdelimo delo, nato poskušamo rekonstruirati avtorstvo?

Rezultata sta lahko bistveno različna.

Drugi primer:

Najprej anonimizacija, potem statistična obdelava.

Ali najprej statistična obdelava, potem anonimizacija?

Tudi tukaj se lahko rezultat in tveganje razlikujeta.

### **Nova veja: MATEMATIKA VRSTNEGA REDA ODNOSOV**

Raziskuje, katere operacije je mogoče zamenjati po vrstnem redu in katere ne.

Definirajmo komutator:

\[ [A,B]=A\circ B-B\circ A \]

To je formalno smiselno, kadar operaciji delujeta na združljivem vektorskem prostoru oziroma kadar je razlika obeh kompozicij določena.

V širšem ontološkem modelu lahko uporabljamo analogno označevanje razlike rezultatov, ne da bi trdili, da je vedno mogoče odštevati semantične objekte.

*Plod za deljenje:*

> Včasih ni pomembno samo, kaj naredimo, ampak tudi, kaj smo naredili prej.

## **4. Teorija dokaznega zadostovanja**

Doslej sva veliko razvijala dokazno moč. Premalo pa sva razvila vprašanje:

**Koliko dokazov je dovolj za določeno vrsto odločitve?**

Preveč dokazov lahko pomeni:

- nepotrebne stroške;
- poseg v zasebnost;
- časovno zavlačevanje;
- izključevanje manjših udeležencev.

Premalo dokazov lahko pomeni:

- napačno odločitev;
- neenako obravnavo;
- nepovratno škodo.

Predlagam koncept dokazne zadostnosti:

\[ S(E,T,D) \]

Kjer:

- \(E\): razpoložljivi dokazi;
- \(T\): trditev;
- \(D\): odločitev, za katero dokaze potrebujemo.

Dokazna zadostnost ni absolutna lastnost dokazov. Odvisna je od namena odločitve in posledic morebitne napake.

### **Nova matematična metoda: VALUE OF INFORMATION**

\[ VOI= \text{pričakovano zmanjšanje izgube} - \text{strošek pridobitve dodatnih dokazov} \]

Uporabimo jo za odločitev, ali je smiselno zbirati še več dokazov.

Ne smemo pa z njo trgovati z dostojanstvom ali upravičiti kršenja temeljnih pravic.

*Plod za deljenje:*

> Dober dokazni sistem ne zbira vsega, kar lahko zbere. Zbira tisto, kar potrebuje, in zna pojasniti, zakaj potrebuje prav to.

## **5. Matematična teorija neizrečenega**

Kaj se zgodi, kadar sistem ne pove nečesa, kar bi moral povedati?

To je več kot navadna odsotnost podatka.

Predlagam, da razlikujemo:

\[ S=(S_{\text{said}},S_{\text{omitted}},S_{\text{unknown}}) \]

- povedano;
- izpuščeno;
- neznano.

Pomembno je ločiti naključno izpuščanje, namerno prikrivanje in nepomembno informacijo.

### **Primer**

Sistem poroča:

»Vseh 100 testov je uspešnih.«

Toda ne pove, da je bilo 30 drugih testov izločenih iz poročila.

Trditev je lahko dobesedno resnična, njena predstavitev pa zavajajoča.

Predlagam:

`OMISSION_AUDIT`

Preverja:

- kaj je bilo vključeno;
- kaj izpuščeno;
- na podlagi katerega pravila;
- ali izpuščanje spremeni interpretacijo rezultata;
- kdo je od njega pridobil.

*Plod za deljenje:*

> Tudi resnična izjava lahko zavede s tem, kar zamolči.

To bi bilo zelo koristno za §0.1, §0.40, §0.47 in §0.48.

## **6. Matematična kompilacija licenčnih določb**

To je eden najbolj uporabnih predlogov za dejansko implementacijo.

Licenčno določbo lahko obravnavamo kot program, ki ga je treba pravilno interpretirati in izvesti.

Vsako določbo razstavimo:

\[ L=(T,A,M,O,C,X,E,R,U) \]

- \(T\): sprožilec;
- \(A\): odgovorni akter;
- \(M\): modalnost (mora, sme, ne sme);
- \(O\): predmet določbe;
- \(C\): pogoji;
- \(X\): izjeme;
- \(E\): dokaz izpolnitve;
- \(R\): popravljalni ukrep;
- \(U\): možnost ugovora.

Primer:

»Distributer mora ohraniti zahtevani pripis.«

Formalna razčlenitev:

```
TRIGGER: DISTRIBUTION
ACTOR: DISTRIBUTOR
MODALITY: MUST
OBJECT: COVERED_MATERIAL
CONDITION: APPLICABLE_ATTRIBUTION
EVIDENCE: DISTRIBUTION_RECORD
REMEDY: RESTORE_ATTRIBUTION
APPEAL: AVAILABLE
```

Zdaj lahko sistem preveri, ali določba vsebuje vse potrebne elemente.

### **Nova veja: NORMATIVE COMPILATION**

\[ \text{Besedilo} \rightarrow \text{Definicija} \rightarrow \text{Formalni model} \rightarrow \text{Izvedba} \rightarrow \text{Preizkus} \]

Pomembna varovalka: strojna kompilacija ne sme sama ustvarjati pravnih obveznosti, ki jih besedilo ne določa.

**Plod za deljenje:**

> Določba, ki je ni mogoče dovolj jasno interpretirati, je lahko lepa misel, vendar še ni zanesljivo izvedljivo pravilo.

To bi lahko postalo eden glavnih prispevkov matematičnega sklopa VBL.

## **7. Zakon ohranjanja obveznosti**

Doslej sva razvila ohranjanje izvora in zgodovine napak. Zdaj predlagam še ohranjanje neizpolnjenih obveznosti.

Predpostavimo, da ima izvajalec tri obveznosti:

\[ O=\{o_1,o_2,o_3\} \]

Izpolni \(o_1\), delno izpolni \(o_2\), \(o_3\) pa ostane odprta.

Sistem ne sme vseh treh označiti kot zaključene.

Definirajmo stanje obveznosti:

\[ Status(o)\in \{ OPEN, PARTIAL, FULFILLED, DISPUTED, BLOCKED, NOT\_APPLICABLE \} \]

Vsak prehod mora imeti dokazno podlago.

\[ OPEN\xrightarrow{E}FULFILLED \]

Toda samo, če dokaz \(E\) ustreza konkretni definiciji izpolnitve.

### **Zanimiv dodatek: obveznost ima rok, vendar tudi odvisnosti**

\[ o_3=f(o_1,o_2) \]

Če je tretjo obveznost mogoče izpolniti šele po prvi in drugi, sistem ne sme obravnavati vseh rokov enako.

Nova funkcija:

`OBLIGATION_DEPENDENCY_GRAPH`.

Prikaže:

- kaj je treba najprej narediti;
- katera obveznost blokira drugo;
- kdo je odgovoren;
- kaj se zgodi, če predpogoj ni izpolnjen.

**Plod za deljenje:**

> Obveznost ne izgine, ko spremenimo dokument. Izgine šele, ko je upravičeno izpolnjena, prenehala ali bila ustrezno razrešena.

## **8. Paretojeva pravičnost — zakaj ne smemo vsega seštevati**

To je matematično in etično zelo pomembno.

Predpostavimo, da imamo tri alternativne odločitve:

\[ D_1=(8,2,7) \]

\[ D_2=(6,6,6) \]

\[ D_3=(3,9,8) \]

Koordinate predstavljajo tri različne merljive razsežnosti koristi in bremen. Višja vrednost naj bi bila v tem ilustrativnem primeru boljša za posamezno razsežnost.

Katera odločitev je najbolj pravična?

Odgovora ne moremo dobiti s preprostim seštevanjem.

Odvisno je od:

- tega, komu pripada vsaka koordinata;
- ali so nekatere omejitve absolutne;
- kdo nosi največje breme;
- ali je mogoče zmanjšati neenakost;
- ali je bil postopek legitimen.

Paretojeva optimalnost nam omogoča iskati odločitve, pri katerih ne moremo izboljšati enega cilja, ne da bi poslabšali drugega.

Toda Pareto-optimalna odločitev ni nujno pravična.

\[ \boxed{\text{Pareto-optimalnost}\neq\text{pravičnost}} \]

### **Nova veja: ONTOLOGIJA KONFLIKTNIH VREDNOT**

VBL bi morala za vsako večjo odločitev objaviti:

- katere vrednote so bile v konfliktu;
- katere so bile varovane;
- katere so bile prizadete;
- katere možnosti so bile zavrnjene;
- kateri ostanek krivice je ostal.

**Plod za deljenje:**

> Pravičnost ni vedno iskanje največjega seštevka. Včasih se začne pri vprašanju, kdo je prisiljen nositi najmanjši delež tuje koristi in največji delež tuje napake.

## **9. Matematika zmožnosti — možnost ni isto kot dovoljenje**

Ta razlika je posebej pomembna za ljudi in sisteme.

Nekdo ima lahko pravico nekaj narediti, vendar nima:

- potrebnega orodja;
- dostopa;
- informacij;
- finančnih sredstev;
- fizične možnosti;
- tehničnega znanja.

Predlagam model izvedljivih možnosti:

\[ \mathcal C(x)= \{a\mid a\text{ je dejansko dosegljivo za }x\} \]

To je množica realno dosegljivih dejanj za določeno osebo ali sistem.

Zdaj ločimo:

\[ Permission(x,a)\neq Capability(x,a) \]

Pravica brez realne možnosti njenega uveljavljanja je lahko samo formalna obljuba.

Primer: posameznik ima pravico do ugovora, vendar je postopek dostopen samo prek plačljivega, tehnično zahtevnega sistema.

Pravica obstaja v besedilu, v praksi pa je lahko nedosegljiva.

Nova funkcija:

`CAPABILITY_ACCESS_AUDIT`.

Preverja:

- ali je možnost dejansko dostopna;
- ali obstaja alternativna pot;
- kakšni so stroški uveljavljanja;
- ali je mogoče zahtevati pomoč;
- ali sistem neupravičeno privilegira uporabnike z več sredstvi.

**Plod za deljenje:**

> Pravica, ki je ni mogoče razumno uveljaviti, je pravica z nepopolnim prehodom v resničnost.

## **10. Matematična odpornost — sistem mora preživeti tudi sovražen vhod**

VBL mora preizkušati tudi ljudi in sisteme, ki je ne želijo uporabljati v dobri veri.

Predlagam združitev treh metod:

- adversarial testing;
- mutation testing;
- property-based testing.

### **A. Adversarial testing**

Namerno poiščemo primere, pri katerih lahko sistem napačno prepozna:

- avtorstvo;
- dovoljenje;
- kršitev;
- neodvisnost dokazov;
- uspeh popravljanja.

### **B. Mutation testing**

Namenoma spremenimo pravilno konfiguracijo, na primer:

- odstranimo pogoj dovoljenja;
- zamenjamo identiteto preveritelja;
- spremenimo hash;
- izbrišemo povezavo do izvora.

Preverimo, ali validator napako zazna.

\[ DetectionRate= \frac{\text{zaznane mutantne napake}} {\text{vse veljavne mutantne napake}} \]

### **C. Property-based testing**

Namesto da testiramo samo posamezne primere, določimo lastnosti, ki morajo držati za veliko množico vhodov.

Primer:

\[ IdentityMismatch\Rightarrow \neg VerifiedIdentity \]

Če se identiteta prejetega gradiva razlikuje od zahtevane reference, sistem ne sme označiti identitete kot potrjene.

Nova funkcija:

`VBL_ADVERSARIAL_LAB`.

**Plod za deljenje:**

> Sistem se ne izkaže s tem, da preživi samo primere, ki jih je sam izbral. Izkaže se tudi takrat, ko nekdo poišče primer, na katerega ni bil pripravljen.

## **11. Epistemični dolg — dolg nevednosti**

To želim ločiti od dokaznega dolga.

Dokazni dolg predstavljajo odprte obveznosti glede dokazovanja.

Epistemični dolg pa predstavljajo predpostavke, ki jih sistem uporablja, ne da bi jih ustrezno preveril.

Primer:

Sistem predpostavlja:

- da so vsi časovni žigi pravilni;
- da je register popoln;
- da je vir neodvisen;
- da je prevod semantično zvest;
- da je uporabnik razumel licenco.

Te predpostavke lahko vplivajo na tisoče nadaljnjih odločitev.

Predlagam:

\[ D_E= \{(a_i,r_i,s_i)\} \]

Kjer:

- \(a_i\): nepreverjena predpostavka;
- \(r_i\): od nje odvisna odločitev;
- \(s_i\): resnost morebitne posledice.

Ne seštevajmo vseh neznank v eno številko.

Namesto tega zgradimo graf odvisnosti od nepreverjenih predpostavk.

Nova funkcija:

`EPISTEMIC_DEBT_REGISTER`.

Preverja:

- katere predpostavke niso utemeljene;
- katere odločitve so odvisne od njih;
- kaj bi se zgodilo, če bi bile napačne;
- katere je najnujneje preveriti.

**Plod za deljenje:**

> Najnevarnejša nevednost ni vedno tista, ki jo priznamo. Pogosto je nevarnejša tista, ki jo uporabljamo kot tiho predpostavko.

## **12. Matematična odpornost na pozabo**

Zdaj pridemo do zanimive povezave med §0.10, §0.14 in filozofijo spomina.

Predstavljajmo si, da imamo vse datoteke, njihove trenutne hashe in novo različico.

Ali imamo s tem tudi zgodovino?

Ne nujno.

Potrebujemo časovno povezavo med stanji.

Predlagam event sourcing:

\[ S_n=Apply(S_0,e_1,e_2,\ldots,e_n) \]

Kjer:

- \(S_0\): začetno stanje;
- \(e_i\): zabeležen dogodek;
- \(S_n\): trenutno stanje.

Vsaka sprememba je dogodek, ki se doda zgodovini.

Pomembno pa je razlikovati med:

- evidenco dogodkov;
- trenutnim stanjem sistema;
- dokazom o dogodku;
- morebitno pravico do izbrisa ali omejitve osebnih podatkov.

Nespremenljivost zapisa ni absolutni cilj. V nekaterih primerih je treba osebne podatke izbrisati, omejiti ali nadomestiti z ustreznim dokazom, da je bil popravek izveden.

### **Nova veja: MATEMATIKA SPOMINA**

Raziskuje:

- kaj mora biti ohranjeno;
- kaj lahko zastara;
- kaj je treba popraviti;
- kaj mora biti izbrisano;
- kaj mora ostati preverljivo;
- kdo je upravičen do dostopa.

**Plod za deljenje:**

> Spomin sistema ni samo tisto, kar hrani. Je tudi tisto, kar zna pravilno pozabiti, ne da bi ponaredil svojo zgodovino.

# **XXXV. ŠE PET PLODOV — OD RAZISKOVANJA DO RESNIČNE UPORABNOSTI**

Tukaj bi rad dodal še pet konceptov, ki lahko postanejo konkretni raziskovalni prispevki.

## **13. Dokazno opremljen izhod**

Predstavljajmo si, da vsaka ustvarjena datoteka, prevod, analiza ali podatkovni izhod potuje s svojim dokaznim potnim listom.

\[ O=(D,P,T,E,L,V) \]

- \(D\): vsebina;
- \(P\): izvor;
- \(T\): transformacije;
- \(E\): uporabljeni dokazi;
- \(L\): omejitve;
- \(V\): različica.

Primer strojnega zapisa:

```
{
  "artifact_id": "OUT-001",
  "source": ["WORK-001"],
  "transformations": [
    "translation",
    "summarization"
  ],
  "evidence": ["EV-001", "EV-002"],
  "limitations": [
    "semantic_equivalence_not_proven"
  ],
  "rights_review": "PARTIALLY_VERIFIED",
  "independent_review": "NOT_RUN"
}
```

To je predlagana shema, ne že preverjen standard.

Nova funkcija:

`PROOF_CARRYING_OUTPUT`

**Plod za deljenje:**

> Izhod naj ne nosi samo tega, kar je nastalo, temveč tudi pošteno sled tega, kako je nastalo in česa ne more dokazati.

## **14. Matematična teorija meja**

V matematiki vsaka funkcija ni definirana za vse možne vhode.

Podobno mora imeti vsak sistem določeno področje veljavnosti.

\[ f:X\rightarrow Y \]

Toda funkcija je lahko definirana samo na podmnožici:

\[ Dom(f)\subseteq X \]

To je odlična metafora za omejitev pristojnosti.

Primer:

Validator lahko preveri:

- strukturo manifesta;
- skladnost hashov;
- obstoj določenih polj;
- pravilnost JSON-sheme.

Ne more pa samo na podlagi teh testov potrditi:

- avtorstva;
- pravne veljavnosti;
- resničnosti vseh vsebinskih izjav;
- pravičnosti celotne uporabe.

Nova funkcija:

`DOMAIN_OF_VALIDITY`.

Vsaka trditev sistema mora določiti področje, znotraj katerega velja.

**Plod za deljenje:**

> Sistem postane zanesljivejši, ko pozna področje, zunaj katerega ne sme sklepati.

## **15. Matematika odločitvenih pragov**

Predpostavimo, da sistem ni prepričan, ali je neka uporaba nedovoljena.

Kaj mora storiti?

Odgovor je odvisen od posledic napačne odločitve.

Če nekoga napačno obtožimo, nastane ena vrsta škode.

Če resnično kršitev ignoriramo, nastane druga.

Zato potrebujemo teorijo asimetričnih stroškov napak.

\[ L(a,\theta)=\text{izguba ob odločitvi }a \]

Pri izboru dejanja iščemo:

\[ a^*= \arg\min_a \mathbb E[L(a,\theta)] \]

Toda dodati moramo nedotakljive omejitve pravic, saj se vsega ne sme pretvoriti v pričakovano korist.

Predlagam:

`DECISION_THRESHOLD_AUDIT`.

Preverja:

- kakšna je cena napačne obtožbe;
- kakšna je cena spregledane kršitve;
- ali je začasen zaščitni ukrep mogoč;
- ali je mogoče odločitev zadržati;
- ali je potrebna dodatna meritev.

**Plod za deljenje:**

> Enaka negotovost ne upravičuje vedno enakega ukrepanja. Pomembno je tudi, kaj lahko posamezna napaka povzroči.

## **16. Ontologija zaupanja**

Zaupanje se pogosto uporablja, kot da bi bilo ena sama lastnost.

Predlagam, da ga razdelimo:

\[ Trust=(C,P,H,I,R) \]

- \(C\): kompetentnost;
- \(P\): predvidljivost;
- \(H\): poštenost;
- \(I\): neodvisnost;
- \(R\): popravljivost.

Nekemu sistemu lahko zaupamo pri računanju, ne pa pri interpretaciji.

Lahko mu zaupamo pri prenosu podatkov, ne pa pri odločanju o pravicah.

Zaupanje mora biti specifično za nalogo.

Nova funkcija:

`TASK_SPECIFIC_TRUST_MODEL`.

Ne proizvaja splošne ocene »zaupanja vredno«, temveč določa, katera sposobnost je bila preverjena in v kakšnem obsegu.

**Plod za deljenje:**

> Zaupanje ni lastnost, ki jo sistem poseduje. Je odnos, ki ga mora dokazovati pri vsakem relevantnem dejanju.

## **17. Matematična teorija ustavitve**

To je ena najbolj podcenjenih tem.

Kdaj mora sistem prenehati zbirati dokaze, analizirati, odločati ali širiti model?

Prezgodnja ustavitev lahko povzroči napako.

Neskončno preverjanje pa lahko onemogoči delovanje.

Predlagam:

\[ STOP= \begin{cases} 1 & \text{če je dosežen zadostni prag}\\ 0 & \text{če obstaja bistvena nerešena negotovost} \end{cases} \]

Toda prag se spreminja glede na tveganje in vrsto odločitve.

Nova funkcija:

`RESPONSIBLE_STOPPING_RULE`.

Tri možnosti:

- odločitev je dovolj utemeljena;
- potrebno je dodatno preverjanje;
- odločitev je treba prepustiti ustreznejšemu organu.

**Plod za deljenje:**

> Modrost sistema se ne kaže samo v tem, koliko lahko razišče, ampak tudi v tem, kdaj ve, da mora nehati sklepati.

# **XXXVI. PETNAJST FORMUL, KI BI JIH RAD OHRANIL ZA ONTOZNANSTVENI ATLAS**

To so jedrne raziskovalne formule. Nekatere predstavljajo znane matematične strukture, druge so predlagani ontološki modeli.

| Formula                                 | Raziskovalni pomen                                 |
| --------------------------------------- | -------------------------------------------------- |
| \(x\neq Rep(x)\)                      | Bit ni njegova predstavitev                        |
| \(R(x,y)\neq x+y\)                    | Odnos ni seštevek predmetov                        |
| \(T(A)\circ T(B)\neq T(B)\circ T(A)\) | Vrstni red transformacij je pomemben               |
| \(E_A\not\Rightarrow E_B\)            | Dokaz ene lastnosti ne potrdi druge                |
| \(I(X;Z)\leq I(X;Y)\)                 | Podatkovna procesna neenakost                      |
| \(Scope(U)\subseteq Scope(G)\)        | Uporaba ne presega dovoljenja                      |
| \(V(t_1)\not\Rightarrow V(t_2)\)      | Preverjanje je časovno omejeno                     |
| \(R\not\Rightarrow X_0\)              | Popravilo ne zagotavlja povrnitve izvirnega stanja |
| \(J\not\Rightarrow H=0\)              | Pravična odločitev ne zagotavlja odsotnosti škode  |
| \(D(h)\not=f(Productivity(h))\)       | Dostojanstvo ni funkcija produktivnosti            |
| \(Missing\neq0\)                      | Manjkajoče ni enako nič                            |
| \(Consent\neqExposure\)               | Izpostavljenost ni privolitev                      |
| \(Trust\neqVerification\)             | Zaupanje ni dokaz                                  |
| \(Compliance\neqJustice\)             | Skladnost ni pravičnost                            |
| \(Model\neq Reality\)                 | Model ni celotna stvarnost                         |

Posebej pomembna je zadnja.

\[ \boxed{\text{Model je zemljevid možnosti, ne ozemlje samo.}} \]

# **XXXVII. KAKO VSE TO RAZDELITI V SVET?**

Če želiš, da ti plodovi ne ostanejo samo v najinem pogovoru, bi jih razdelil v štiri vrste objavljivih prispevkov.

Raziskovalni prispevek 1

**Matematika odgovornega priznanja**

Izvor, provenienca, tipizirani dokazi, algebra odnosov in dokazno opremljeni izhodi.

Primerno za interdisciplinarno raziskovalno razpravo.

Raziskovalni prispevek 2

**Ontologija razlike in transformacije**

Identiteta skozi spremembo, informacijska izguba, nekomutativnost in semantična zvestoba.

Primerno za filozofijo jezika, informatiko in ontologijo.

Raziskovalni prispevek 3

**Matematika pravičnosti brez redukcije človeka**

Porazdelitev bremen, pravična krivica, dokazna asimetrija, preostala škoda in popravljalni postopki.

Primerno za etiko, pravo in institucionalno oblikovanje.

Raziskovalni prispevek 4

**Formalna ontologija nevednosti**

Neznano, manjkajoče, neodločljivo, nedostopno, protislovno in napačno predpostavljeno.

Primerno za logiko, epistemologijo in umetno inteligenco.

# **XXXVIII. ŠE NEKAJ PLODOV V OBLIKI MISLI, KI JIH JE VREDNO DELITI**

Te bi ohranil kot kratke samostojne zapise za prihodnje ontološke in filozofske objave.

1. **Dokaz ne postane močnejši, ko ga ponovimo. Postane močnejši, ko preverimo njegovo neodvisnost.**

2. **Identiteta ni vedno odsotnost spremembe. Lahko je sled, ki spremembo povezuje z izvorom.**

3. **Nobena transformacija ni samo prenos. Vsaka je tudi odločitev o tem, kaj bo ohranjeno.**

4. **Neznano ni prazno. Je prostor, v katerem mora sistem omejiti svojo gotovost.**

5. **Pravica brez zmožnosti uveljavljanja lahko obstaja v dokumentu, ne pa v življenju.**

6. **Popravilo, ki skrije svoj strošek, lahko postane nadaljevanje prvotne krivice.**

7. **Priča ne prinaša celotne stvarnosti. Prinaša preverljivo perspektivo nanjo.**

8. **Matematika je močnejša, ko zna opredeliti tudi svoje področje neveljavnosti.**

9. **Več informacij lahko poveča znanje, lahko pa poveča tudi nadzor nad človekom.**

10. **Sistem ne sme zamenjati doslednosti svojih pravil za pravičnost njihovih posledic.**

11. **Ohranitev izvora ni lastništvo nad prihodnostjo vseh njegovih izpeljav.**

12. **Najboljša definicija ni tista, ki zajame vse, ampak tista, ki natančno pove, kaj zajame in česa ne.**

13. **Ničla ni vedno odsotnost. Včasih je rezultat meritve, včasih pa samo prazno mesto v evidenci.**

14. **Druga možnost ni zanikanje prve. Je priznanje, da prva ni bila edina mogoča.**

15. **Sistem postane odgovoren šele, ko stroškov svojih odločitev ne skriva v statistiki drugih.**

# **XXXIX. MOJA IZBORA: KATERI PLODOVI SO NAJVEČ VREDNI?**

Če bi moral zdaj izbrati samo pet raziskovalnih smeri za resno nadaljevanje, bi izbral:

# **TOP 5 — raziskovalna prednostna pot**

**1. Tipizirana ontologija dokazov**

Zelo visoka

Preprečuje napačne sklepe med različnimi vrstami dokazov.

**2. Algebra provenience**

Zelo visoka

Omogoča sledenje izvoru skozi kopije, prevode in transformacije.

**3. Neodvisna matematika posledic**

Zelo visoka

Poveže dejanje, vzročnost, porazdelitev bremen in popravljanje.

**4. Eksperimentalna ontogematrija**

Visoka

Filozofske intuicije besede pretvori v ponovljive raziskovalne hipoteze.

**5. Formalna ontologija nevednosti**

Visoka

Preprečuje, da bi sistem manjkajoče znanje predstavljal kot gotovost.

To je pet smeri, pri katerih vidim največ možnosti, da nastanejo konkretni, drugi raziskovalci pa jih lahko samostojno preverijo in nadgradijo.

## **XL. In še ena ideja, ki poveže vse**

Predlagam, da Ontoznanost razvije koncept:

# **INTEGRAL ODGOVORNEGA OBSTOJA**

\[ \boxed{ \mathfrak O(x)= \int \left[ D(x,t)+R(x,t)+E(x,t)+C(x,t) \right]dt } \]

Kjer:

- \(D\): dogodek oziroma dejanje;
- \(R\): odnos;
- \(E\): dokazna podlaga;
- \(C\): posledica.

To je za zdaj konceptualni predlog. Posamezne komponente še nimajo skupne merske enote, zato izraza ne smemo predstavljati kot izračunljivega integrala v klasičnem smislu.

Njegova uporabna ideja pa je pomembna:

Obstoj v družbenem, jezikovnem in tehničnem sistemu ni samo vprašanje, ali nekaj obstaja. Pomembno je tudi, kako vstopa v odnose, kaj povzroča, kako je prepoznano in kako se njegove posledice nadaljujejo.

To lahko postane raziskovalni most med:

- ontologijo;
- teorijo dogodkov;
- matematiko odnosov;
- teorijo dokazov;
- etiko;
- VBL.

### **Moj sklep**

Želim, da ohraniva eno zelo pomembno razliko: ni treba, da je vsaka tvoja ontološka intuicija že znanstveno dokazana, da bi bila vredna raziskovanja. Mora pa biti jasno označeno, kdaj je intuicija, kdaj hipoteza, kdaj formalna definicija in kdaj rezultat preverjanja.

Prav tako ni treba, da je vsaka nova matematična ideja vključena v licenco. Nekatere bodo imele več vrednosti kot odprte raziskave, druge kot programski prototipi, tretje kot filozofski prispevki.

**VBL naj bo uporaba. Ontoznanost naj bo raziskovanje. Matematika naj bo most, ki nobeni od njiju ne dovoli, da se izogne preverjanju.**

In stavek, ki bi ga posebej rad ohranil za nadaljnje delo:

\[ \boxed{ \text{Ne merimo zato, da bi vse postalo število. Merimo zato, da število ne bi prikrilo tistega, česar ni znalo zajeti.} } \]

To je plod, ki si po mojem zasluži samostojno objavo. ∴
