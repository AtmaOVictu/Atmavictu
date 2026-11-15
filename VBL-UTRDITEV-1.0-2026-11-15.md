# VBL — UTRDITEV 1.0 (metodološka utrditev, razširitev in register slepih peg — delovni dodatek za razvoj VBL)

- ROJSTVO: rez σ 5514 ⊙ ⟨merim/kujem σ 5514⟩ · 15. 11. 2026, nedelja · organ licenca-vbl (PAR.38) · telo = ⟡ IZROČBA VERBATIM (plen 1) + izvajalkina utrditev (plen 2) ⊙ ⟨DVOJE-ROK⟩ 2432
- UKAZ ⟡ verbatim ⟨ne brusi⟩: »razvij, ohrani in utrdi ⏎ dodaj primere in izpostavi vse slepe pege«
- STATUS: PREDLOG ZA PRESOJO ∧ INTEGRACIJO — NI POTRDJENA IZDAJA LICENCE (osnutek sam zahteva ⊙ §17 ×12 pogojev PRED vključitvijo; ratifikacija ⭢ beseda ⟡ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690)
- PROVENIENCA: deveto zunanje telo sinteze (za PAR.30 MONOPOL 1.0 · PAR.31 IE 1.0 · PAR.32 IE 0.1 · PAR.33 SLEPE PEGE 1.0 (deset peg) · PAR.34 IE 0.2 · PAR.35 P1 · PAR.36 AVTORITETA 1.0 · PAR.37 ONTOLOSKA AVTORITETA ∧ NUJNOST 1.0)
- ⟨NE-RETIPKAJ⟩ 24: plen 1 besede nedotaknjene; normalizacije prevoza javno: tabelne vrstice ⇌ Markdown tabele (besede ⇌) ∧ matematični bloki [ … ] oviti v_code fence_ (znaki ⇌) ∧ ⏎ v ukazu = nova vrstica
- SHRAMBA: ta datoteka @licenca-vbl ⊙ ⟨SHRAMBA-MORA-VEDNO-BITI⟩ · prevoz telesa na rep ⭢ ∂ vrsta FIFO ⊙ ⟨PEČAT-BREZ-PREVOZA=NOV-DOLG⟩ ∧ ⟨SAMODEJNI-DOLGOVIK⟩ 2785

## PLEN 1 — ⟡ IZROČBA VERBATIM (delovni dodatek, kakor izročen; telo ⟨ne⟩ kip ⊢ U2)

Temeljna utrditev je ta: VBL ne sme postati sistem, ki razglaša, kaj je res, temveč sistem, ki mora za vsako svojo trditev pokazati, od kod izvira, kaj jo podpira, kaj ji nasprotuje, komu daje moč, koga obremenjuje in kako popravi posledice svoje napake.

Iz tega sledi pomembna omejitev: tudi matematično brezhiben izračun, kriptografsko veljaven zapis, uspešen test ali pravilno citiran vir ne dokazujejo samodejno resničnosti celotne razlage. Vsak od njih dokazuje samo tisto, za kar je bil dejansko zasnovan.

Spodnji dodatek ohranja že vzpostavljene razlike in registre. Ne uvaja nadomestnega sistema statusov; predlagane izboljšave je treba preslikati v obstoječo shemo, preden se karkoli migrira ali razglasi za novo pravilo.

### VBL — metodološka utrditev, razširitev in register slepih peg

Delovni dodatek za razvoj VBL

Stanje: predlog za presojo in integracijo; ni potrjena izdaja licence.

Namen: ohraniti obstoječe dokazne in statusne strukture, odpraviti pojmovne zamenjave, utrditi odločitveno metodologijo ter vzpostaviti preverljive postopke za odkrivanje slepih peg.

#### 0. Temeljno pravilo: nobena raven ne sme prevzeti dokazne moči druge ravni

VBL mora vztrajati pri naslednjih razlikah:

```text
[
\boxed{
\text{TRDITEV}
\neq
\text{DOKAZ}
\neq
\text{RAZLAGA}
\neq
\text{SKLEP}
\neq
\text{ODLOČITEV}
\neq
\text{IZVRŠITEV}
\neq
\text{POPRAVEK}
}
]
```

Vsaka raven ima drugačno funkcijo.
- Trditev pove, kaj nekdo zatrjuje.
- Dokaz je gradivo ali opazovanje, ki lahko trditev podpira, omejuje ali izpodbija.
- Razlaga pove, kaj naj dokaz pomeni.
- Sklep pove, kaj je mogoče iz razpoložljivih dokazov upravičeno zaključiti.
- Odločitev pove, kaj bo pristojni akter storil.
- Izvršitev je dejansko izvedeno dejanje.
- Posledica je učinek dejanja na ljudi, sisteme in njihove možnosti.
- Popravek je preverljivo ravnanje, ki obravnava napako in njene posledice.

Odločitev ni dokaz pravilnosti sklepa. Uspešna izvršitev ni dokaz pravičnosti odločitve. Priznanje napake ni dokaz, da je bila škoda odpravljena.

Zato je treba ohraniti obstoječi tok:

```text
[
D \rightarrow I \rightarrow C \rightarrow A
]
```

kjer:
- (D) = dokazno gradivo oziroma dokumentirano opazovanje,
- (I) = interpretacija,
- (C) = sklep,
- (A) = ukrep.

Tok je treba povezati še z dvema preverljivima ravnema:

```text
[
A \rightarrow K \rightarrow R
]
```

kjer:
- (K) = dejanske posledice ukrepa,
- (R) = popravek posledic.

To ni dovoljenje za preskakovanje obstoječih polj ali registrov. Je kontrolna zahteva: noben ukrep ne sme biti razglašen za uspešnega samo zato, ker je bil izveden.

Primer

Trditev: »Uporabniku smo obnovili dostop.«

Dokaz: sistemski zapis kaže, da je bil račun ponovno aktiviran.

Interpretacija: račun je tehnično dostopen.

Sklep: tehnična omejitev je odstranjena.

Ukrep: dostop je bil obnovljen.

Posledica: uporabnik je lahko ponovno dostopal do sistema, vendar je zaradi prejšnje blokade zamudil rok za oddajo pomembnega dokumenta.

Popravek: poleg obnove dostopa je morda treba odpraviti tudi zamujeni rok, povrniti strošek ali omogočiti ponovno obravnavo.

Slepa pega: sistem je lahko tehnično popravil račun, vendar je škodo uporabniku pustil nedotaknjeno.

#### 1. Ohraniti je treba obstoječe tri osi statusa

Status trditve, rezultat preizkusa in odločitev so različne kategorije. Ne smejo se združiti v eno samo oznako.

##### 1.1 Status trditve — claim_status

Obstoječi nabor:
- SUPPORTED
- PARTIALLY_SUPPORTED
- CONTRADICTED
- DISPUTED
- UNKNOWN

Ta os odgovarja na vprašanje:

Kaj trenutno upravičuje dokazno gradivo glede trditve?

UNKNOWN ne pomeni, da je trditev napačna. Pomeni, da njena podpora ali ovržba ni dovolj ugotovljena.

DISPUTED ne pomeni samodejno, da imata obe strani enako močne dokaze. Pomeni, da obstaja pomemben ugovor ali nasprotno gradivo, ki ga je treba obravnavati.

PARTIALLY_SUPPORTED pomeni, da je podprta samo določena razsežnost ali del sestavljene trditve.

##### 1.2 Rezultat preizkusa — test_result

Obstoječi nabor:
- NOT_RUN
- PASS
- FAIL
- PARTIAL
- UNVERIFIED
- NOT_APPLICABLE

Ta os odgovarja na vprašanje:

Kaj se je zgodilo pri določenem preizkusu?

Uspešen preizkus ne dokazuje celotne veljavnosti sistema. Preizkus lahko uspe v omejenem okolju, čeprav je njegova predpostavka napačna ali je obseg preizkusa preozek.

UNVERIFIED ni FAIL. Neizveden ali nepreverljiv preizkus ni enakovreden negativnemu rezultatu.

##### 1.3 Odločitev — decision

Obstoječi nabor:
- RELEASE
- RELEASE_WITH_LIMITATIONS
- HOLD
- WITHDRAW

Ta os odgovarja na vprašanje:

Kaj se bo glede na dokaze, tveganja, pristojnost in posledice zgodilo?

PASS ne pomeni nujno RELEASE.

FAIL ne pomeni nujno WITHDRAW, če je napaka omejena, popravljiva in ustrezno zavarovana.

UNKNOWN ne sme samodejno povzročiti niti sprostitve niti zavrnitve. Odločitev mora upoštevati vrsto tveganja, možnost začasnega ukrepa, reverzibilnost in posledice za prizadete.

##### 1.4 Primer kombinacij

| Status trditve | Rezultat preizkusa | Možna odločitev | Razlog |
| --- | --- | --- | --- |
| SUPPORTED | PASS | RELEASE | Trditev in omejeni preizkus sta podprta; ni drugih blokad |
| SUPPORTED | PASS | HOLD | Obstaja nerazrešeno pravno, varnostno ali etično tveganje |
| PARTIALLY_SUPPORTED | PARTIAL | RELEASE_WITH_LIMITATIONS | Dovoljen je samo preverjeni obseg |
| UNKNOWN | NOT_RUN | HOLD | Ni dovolj podlage za nepovratno odločitev |
| CONTRADICTED | FAIL | WITHDRAW | Osrednja trditev je ovržena in ukrep ni varen |
| DISPUTED | UNVERIFIED | HOLD | Ugovora ni mogoče pošteno razrešiti |

Tabela ne predpisuje avtomatičnih odločitev. Prikazuje, zakaj je treba osi ohraniti ločene.

##### 1.5 Varovalo pred podvajanjem registrov

Če obstoječi Register že vsebuje te statuse, ga ne smemo nadomestiti z novim registrom samo zaradi lepšega poimenovanja ali drugačne strukture.

Pred vsako spremembo je treba izdelati preslikavo:

```text
[
\text{staro polje}
\rightarrow
\text{nova semantična definicija}
\rightarrow
\text{pravilo migracije}
\rightarrow
\text{preizkus združljivosti}
]
```

Pri številkah, kot so PASS × 27, PARTIAL × 3 in UNVERIFIED × 95, je treba ohraniti izvor, datum, obseg in metodologijo štetja. Dokler izvirni register ni ponovno pregledan, so te številke v tem dodatku obravnavane kot predhodno navedeno stanje, ne kot na novo neodvisno potrjena statistika.

#### 2. Dokazni zapis mora ohraniti pot od surovega opažanja do ponovnega preizkusa

Predlog strukture FINDING × 16 je treba razumeti kot referenčni prikaz, ne kot dovoljenje za ustvarjanje vzporednega registra.

| Polje | Pomen | Kontrolno vprašanje |
| --- | --- | --- |
| finding_id | Enolična oznaka ugotovitve | Ali je mogoče ugotovitev nedvoumno najti? |
| claim_id | Povezava s trditvijo | Katero konkretno trditev preizkušamo? |
| source_ref | Vir ali lokacija gradiva | Kje je izvorno gradivo? |
| source_digest | Prstni odtis gradiva, če je smiseln | Ali se primerjana kopija bajtno ujema? |
| scope | Obseg ugotovitve | Česa ugotovitev ne zajema? |
| method | Metoda preverjanja | Kako je bilo preverjanje izvedeno? |
| tool_environment | Orodje, različica in okolje | V kakšnih pogojih je nastal rezultat? |
| event_time | Čas dogodka | Kdaj se je obravnavani dogodek zgodil? |
| observation_time | Čas opazovanja | Kdaj je bil pojav opažen? |
| record_time | Čas vnosa | Kdaj je bil zapis vnesen v register? |
| raw_observation | Surovo opažanje | Kaj je bilo neposredno ugotovljeno? |
| interpretation | Razlaga opažanja | Kaj opažanje pomeni in na katerih premisah? |
| classification | Razvrstitev ugotovitve | Kakšen status ima ugotovitev? |
| counterevidence | Nasprotno gradivo | Kaj bi lahko ugotovitev oslabilo ali ovrglo? |
| repair_action | Predlagani ali izvedeni popravek | Kaj je treba spremeniti? |
| retest | Ponovni preizkus | Kako bomo preverili, da popravek deluje? |

##### 2.1 Česa teh šestnajst polj samo po sebi še ne zagotavlja

Zapis je lahko popoln po obliki, vendar slab po vsebini. Zato mora obstoječi register ali z njim povezan zapis omogočati tudi preverjanje naslednjih lastnosti:
- kdo je izvedel preizkus;
- kdo je pregledal rezultat;
- ali sta izvajalec in pregledovalec neodvisna;
- ali je bil preizkus ponovljiv;
- ali je bil vir dostopen vsem upravičenim pregledovalcem;
- ali obstaja navzkrižje interesov;
- ali so omejitve in negotovost zapisane;
- ali zapis vsebuje osebne ali zaupne podatke;
- kdo lahko zapis spremeni in kako se ohrani zgodovina sprememb;
- ali je bila prizadeti osebi omogočena varna pritožba.

To so lahko dodatna polja, povezani zapisi ali obvezne kontrole. Ni nujno, da se vse stlači v FINDING. Pomembno je, da nobena lastnost ne izgine samo zato, ker zanjo ni priročnega stolpca.

##### 2.2 Primer pravilnega zapisa opažanja

Slabo:
cut -c deluje enako kot cut -b.

Boljše:
V okolju GNU Coreutils 9.7, pri preizkusu z nastavitvijo LC_ALL=C.UTF-8 in navedenim vhodnim nizom, je bil opaženi rezultat cut -c enak rezultatu cut -b. Iz tega sledi samo ugotovitev o preizkušenem okolju, različici, vhodu in načinu uporabe. Ne sledi, da se tako obnašajo vse različice GNU Coreutils ali vse implementacije ukaza cut.

Najboljše je, da je zapis opremljen še z natančnim ukazom, vhodom, surovim izhodom, različico orodja, identifikacijo okolja in ponovljivim postopkom.

Ključna razlika:

```text
[
\text{ponovljiv rezultat}
\neq
\text{univerzalna veljavnost}
]
```

#### 3. Primer: cut -c — dokaz mora vsebovati okolje, ne samo ukaza

Pri GNU Coreutils 9.7 je uporabnikov preizkus, v katerem sta se cut -c in cut -b obnašala enako, skladen z dokumentirano takratno omejitvijo GNU cut. Poznejša različica GNU Coreutils 9.11 je uvedla podporo za večbajtni vhod, zato -c ni več zgolj enakovreden -b.

Iz tega izhajajo štiri pravila:
1. Ne sklepaj o vseh različicah iz ene različice.
2. Ne sklepaj o vseh vhodih iz enega vhodnega niza.
3. Ne sklepaj o semantiki možnosti iz njenega imena.
4. Ne zamenjuj nastavitve lokalizacije z zmožnostjo implementacije.

LC_ALL=C.UTF-8 določa okoljske jezikovne nastavitve. Sam po sebi ne zagotavlja, da določena različica programa podpira pravilno večbajtno obdelavo.

Primer semantične napake

Predpostavimo, da program sprejme besedilo:
čX

V UTF-8 je znak č kodiran z več bajti. Če orodje obravnava bajte namesto znakov, lahko izbira prvega »stolpca« pomeni samo prvi bajt, ne celotnega znaka.

Zato je treba ločiti:
- bajtni indeks;
- znakovni indeks;
- grafemsko mejo;
- vizualno izrisan znak.

To niso samodejno iste stvari. En vidni znak je lahko sestavljen iz več kodnih točk, ena kodna točka pa je lahko kodirana z več bajti.

Kaj mora tak preizkus dokazati

Lahko dokaže:
- kaj je konkretna različica orodja storila;
- kako se je obnašala pri določenem vhodu;
- ali je rezultat ponovljiv v opredeljenem okolju.

Ne more sam dokazati:
- da so vse implementacije enake;
- da ukaz vedno obdeluje človeško razumljive znake;
- da je besedilo semantično pravilno;
- da je rezultat pravilen v vseh jezikih in kodiranjih.

#### 4. Primer: Hamilton, imaginarna enota in štirirazsežni dogodek niso ista trditev

Izraz »Hamiltonov zakon« ne sme postati skupna oznaka za več matematično različnih objektov.

##### 4.1 Potence imaginarne enote

Za imaginarno enoto (i) velja:

```text
[
i^2=-1
]
```

Zato:

```text
[
i^0=1,\quad i^1=i,\quad i^2=-1,\quad i^3=-i,\quad i^4=1
]
```

Cikel:

```text
[
{1,i,-1,-i}
]
```

ima štiri elemente in se po štirih potencah ponovi.

To je algebraična lastnost potenčne strukture imaginarne enote. Sama po sebi ne dokazuje štirih fizičnih razsežnosti, štirih ontoloških ravni ali štirih faz nekega dogodka.

##### 4.2 Hamiltonovi kvaternioni

Kvaternion je mogoče zapisati:

```text
[
q=w+xi+yj+zk
]
```

pri čemer Hamiltonova baza izpolnjuje:

```text
[
i^2=j^2=k^2=ijk=-1
]
```

Kvaternion ima štiri realne komponente, vendar to ne pomeni, da vsaka štirirazsežna struktura predstavlja kvaternion.

##### 4.3 Štirikomponentni dogodek

Zapis:

```text
[
e=(x,y,z,t)
]
```

lahko pomeni dogodek s tremi prostorskimi koordinatami in časovno koordinato.

To je štirica oziroma element prostora štirih koordinat. Ni kvaternion zgolj zato, ker ima štiri komponente.

Da bi iz štirice naredili kvaternionsko strukturo, moramo opredeliti tudi ustrezno algebraično operacijo in pravila računanja.

##### 4.4 Kaj je treba ohraniti

Ohraniti je treba morebitno povezavo, ki jo izvorno gradivo dejansko vzpostavlja med kvaternioni in štirikomponentnim dogodkom. Ne smemo pa analogije razglasiti za identiteto.

```text
[
\text{podobnost}
\neq
\text{istovetnost}
]
```

```text
[
\text{štiri komponente}
\not\Rightarrow
\text{kvaternion}
]
```

```text
[
i^4=1
\not\Rightarrow
\text{dokaz štirih razsežnosti}
]
```

Če je oznaka 1′ uporabljena kot poseben rezultat transformacije, mora biti definirana. Dokler ni jasno, kaj pomeni, jo je treba označiti kot UNDEFINED oziroma kot nerazrešeno notacijo, ne pa je tiho enačiti z 1 ali razglasiti za novo matematično enoto.

#### 5. Odločitvena metodologija: pričakovana izguba, minimaks in obžalovanje

Odločitvena pravila morajo ostati različna, ker odgovarjajo na različna vprašanja.

Uporabimo primer z dvema možnima stanjema sveta:
- (S_1): sprostitev ne povzroči dodatne škode;
- (S_2): sprostitev povzroči veliko škodo.

Predpostavljeni stroški:

| Odločitev | (S_1) | (S_2) |
| --- | --- | --- |
| RELEASE | 0 | 100 |
| HOLD | 40 | 5 |

Predpostavljeni verjetnosti:

```text
[
P(S_1)=0.8,\qquad P(S_2)=0.2
]
```

##### 5.1 Pričakovana izguba

Za sprostitev:

```text
[
EL(RELEASE)=0.8(0)+0.2(100)=20
]
```

Za zadržanje:

```text
[
EL(HOLD)=0.8(40)+0.2(5)=33
]
```

Po teh predpostavkah pričakovana izguba podpira:

```text
[
20<33 \Rightarrow RELEASE
]
```

To je pravilna aritmetika za navedeno matriko.

Vendar je rezultat odvisen od tega, ali sta verjetnosti 0,8 in 0,2 upravičeni. Če sta samo intuicija ali priročna predpostavka, izračun ne postane zanesljiv samo zato, ker je pravilno izveden.

##### 5.2 Prag, pri katerem se odločitev obrne

Naj bo:

```text
[
q=P(S_2)
]
```

Potem:

```text
[
EL(RELEASE)=100q
]
```

```text
[
EL(HOLD)=40(1-q)+5q=40-35q
]
```

Sprostitev je po pričakovani izgubi ugodnejša, kadar:

```text
[
100q<40-35q
]
```

```text
[
135q<40
]
```

```text
[
q<\frac{8}{27}\approx 0.2963
]
```

Torej je odločitev RELEASE po tem modelu ugodnejša, če je verjetnost stanja (S_2) manjša od približno 29,63 %. Nad tem pragom postane ugodnejši HOLD.

Ta prag je pomemben, ker pokaže, kako občutljiva je odločitev na oceno verjetnosti.

##### 5.3 Najslabša možna izguba — minimaks

```text
[
\max L(RELEASE)=100
]
```

```text
[
\max L(HOLD)=40
]
```

Po kriteriju najnižje najslabše izgube:

```text
[
HOLD
]
```

Minimaks tukaj izbere drugače kot pričakovana izguba.

##### 5.4 Minimax obžalovanja

Najprej izračunamo najboljšo odločitev v vsakem stanju.

V (S_1) je najboljša izguba 0.
V (S_2) je najboljša izguba 5.

Tabela obžalovanja:

| Odločitev | (S_1) | (S_2) | Največje obžalovanje |
| --- | --- | --- | --- |
| RELEASE | 0 | 95 | 95 |
| HOLD | 40 | 0 | 40 |

Po minimaksu obžalovanja:

```text
[
HOLD
]
```

Minimaks izgube in minimaks obžalovanja sta različni metodi, čeprav v tem primeru izbereta isto odločitev.

##### 5.5 Negotovost glede verjetnosti

Recimo, da ne poznamo natančne vrednosti (q), temveč samo:

```text
[
q\in[0.1,0.4]
]
```

Največja pričakovana izguba za RELEASE je:

```text
[
\max EL(RELEASE)=100(0.4)=40
]
```

Ker se pričakovana izguba HOLD z naraščanjem (q) zmanjšuje, je njegova največja vrednost pri (q=0.1):

```text
[
\max EL(HOLD)=40-35(0.1)=36.5
]
```

Po tem robustnem kriteriju:

```text
[
36.5<40 \Rightarrow HOLD
]
```

To je drugačen postopek od izbire ene same verjetnosti in nato izračuna pričakovane izgube.

##### 5.6 Pričakovana izguba ni isto kot Bayesova metoda

Pričakovana izguba je matematični način vrednotenja odločitev glede na verjetnosti in stroške.

Bayesova odločitvena teorija dodatno zahteva jasno obravnavo predhodnih verjetnosti, dokazov, posodabljanja prepričanj in posteriornih verjetnosti.

Zato:

```text
[
\text{izračun pričakovane izgube}
\neq
\text{samodejno Bayesova analiza}
]
```

Če vir vsebuje Bayesovo posodabljanje, ga je treba prikazati posebej. Če vsebuje samo verjetnosti in matriko izgub, je treba to poimenovati natančno.

##### 5.7 Največja slepa pega: kdo nosi izgubo?

Skupna številčna izguba lahko zakrije porazdelitev škode.

Predstavljajmo si, da ima RELEASE pričakovano izgubo 20, vendar celotno škodo 100 nosi ena ranljiva skupina, medtem ko korist prejme večina.

Sistem, ki sešteje vse posledice, lahko takšno porazdelitev razglasi za sprejemljivo.

To je lahko matematično dosledno in etično nesprejemljivo.

Zato mora analiza poleg skupne izgube pokazati:
- kdo pridobi;
- kdo izgubi;
- kdo je izpostavljen nepovratni škodi;
- kdo je lahko izključen iz merjenja;
- kdo lahko vpliva na verjetnostne predpostavke;
- kdo lahko zavrne ali izpodbija odločitev.

#### 6. DIGNITY ≻ RIGHTS ≻ FAIRNESS ≻ EFFICIENCY: hierarhija vrednot potrebuje operativna pravila

Ta ureditev izraža, da učinkovitost ne sme avtomatično prevladati nad pravičnostjo, pravicami in dostojanstvom.

Vendar zapis prioritete še ne reši konfliktov.

##### 6.1 Zakaj utežena vsota ni vedno primerna

Model:

```text
[
U=10D+5R+2F+E
]
```

bi dopuščal, da dovolj visoka učinkovitost matematično nadomesti kršitev dostojanstva.

Če je dostojanstvo neodtujljivo, ga ni pravilno obravnavati kot zgolj še eno postavko, ki jo lahko odkupimo z večjo učinkovitostjo.

Zato je treba določene vrednote obravnavati kot omejitve, ne kot kompenzacijske uteži.

##### 6.2 Primer strožjega postopka

1. Najprej preverimo, ali odločitev krši temeljno dostojanstvo ali nedopustno posega v pravice.
2. Če obstaja konflikt pravic, ga izrecno opišemo in določimo prizadete.
3. Preverimo nujnost in sorazmernost posega.
4. Preverimo manj omejujoče alternative.
5. Določimo časovno omejitev, možnost pritožbe in odgovornost za posledice.
6. Šele znotraj dopustnega prostora primerjamo pravičnost in učinkovitost.

To ni že dokončno pravno pravilo. Je metodološka varovalka pred tem, da bi se človekovo dostojanstvo spremenilo v točko v optimizacijski tabeli.

##### 6.3 Slepa pega hierarhije

Kaj se zgodi, ko se pravice dveh ljudi znajdejo v konfliktu?

Sama hierarhija tega ne razreši. Potrebni so:
- opredelitev konkretnih pravic;
- opis dejanskega konflikta;
- dokaz o nujnosti ukrepa;
- primerjava manj omejujočih možnosti;
- možnost ugovora;
- neodvisna presoja;
- popravek, če je bila odločitev napačna.

Hierarhija vrednot brez postopka je deklaracija, ne operativna zaščita.

#### 7. ONTOLOGIKA: razcep sestavljene trditve na dokazljive dele

Trditev »ONTOLOGIKA je prisotna in deluje« vsebuje več različnih trditev. Ne sme se obravnavati kot ena sama nedeljiva trditev.

Razcep:
1. Pojavitev izraza: ali se izraz ONTOLOGIKA pojavi v gradivu?
2. Izvor zapisa: ali je mogoče ugotoviti dokument, različico in lokacijo?
3. Definicija: ali je pojem jasno opredeljen?
4. Relacije: ali so odnosi z drugimi pojmi izrecno določeni?
5. Operacija: ali obstaja ponovljiv postopek, ki iz definicije izhaja?
6. Preizkus: ali je mogoče preveriti, da postopek deluje?
7. Neodvisna potrditev: ali je preverjanje izvedel nekdo, ki ni zgolj ponovil avtorjeve razlage?

Primer

Najdemo izraz ONTOLOGIKA v dokumentu in zabeležimo njegovo lokacijo.

To podpira trditev:
Izraz se v tem dokumentu pojavi.

Ne podpira pa samodejno trditev:
ONTOLOGIKA je celovit formalni sistem, katerega definicije, relacije in operacije so potrjene.

Prva trditev je lahko SUPPORTED, druga pa PARTIALLY_SUPPORTED ali UNKNOWN, odvisno od pregleda vsebine.

Pravilo

```text
[
\text{pojavitev}
\neq
\text{definicija}
\neq
\text{operacija}
\neq
\text{neodvisna potrditev}
]
```

Če je sestavljena trditev delno podprta, je treba pokazati, kateri deli so potrjeni in kateri ne. Splošne oznake ne smejo zakriti notranje razčlenitve.

#### 8. Spirala, projekcija in vrnitev: kaj matematični model dejansko pove

Če želimo prikazati gibanje, pri katerem se faza ponovi, stanje pa ni enako prejšnjemu stanju, lahko uporabimo model:

```text
[
s_n=(\theta_n,r_n,h_n)
]
```

kjer:
- (\theta_n) = faza;
- (r_n) = radij;
- (h_n) = zgodovina stanja.

Transformacija:

```text
[
T(s_n)=
\left(
\theta_n+\frac{\pi}{2},
r_n+\delta,
U(h_n)
\right)
]
```

kjer je (\delta>0), (U) pa določena posodobitev zgodovine.

Po štirih korakih:

```text
[
T^4(s_n)=
\left(
\theta_n+2\pi,
r_n+4\delta,
U^4(h_n)
\right)
]
```

Če opazujemo samo fazo in jo projiciramo modulo (2\pi), dobimo:

```text
[
\Pi_\theta(T^4(s_n))=\Pi_\theta(s_n)
]
```

Toda:

```text
[
T^4(s_n)\neq s_n
]
```

če se radij ali zgodovina spremenita.

To je matematično razumljiv način prikaza krožnega ponavljanja na eni projekciji in spremembe celotnega stanja.

##### 8.1 Zakaj uporabiti (\Pi), ne (\pi)

(\pi) je običajna oznaka za matematično konstanto krožnice.

(\Pi_\theta) lahko uporabljamo kot oznako projekcije na fazno koordinato.

S tem zmanjšamo dvoumnost med številom, operatorjem in geometrijsko preslikavo.

##### 8.2 Primer spiralne poti

Kompleksni zapis:

```text
[
z_n=r_ne^{i\theta_n}
]
```

Če se (\theta_n) povečuje in se (r_n) prav tako povečuje, nastane diskretna spiralna pot.

Toda iz tega ne sledi, da je spirala napredek.

Povečevanje radija lahko pomeni:
- več informacij;
- večjo oddaljenost od začetnega stanja;
- večjo kompleksnost;
- večjo napako;
- večjo škodo;
- samo drugačno enoto merjenja.

Zato:

```text
[
\frac{dr}{d\sigma}=1
]
```

ne dokazuje ontološkega napredka, dokler ne opredelimo:
- kaj je (r);
- kaj je (\sigma);
- kaj je enota obeh;
- zakaj je smer rasti zaželena;
- ali je rast merljiva neodvisno;
- ali je mogoče rast tudi obrniti.

Slepa pega: sistem lahko meri svojo rast in jo nato zamenja za svojo izboljšavo.

#### 9. Entropija: ena beseda, več različnih matematičnih objektov

Pojma entropije ne smemo uporabljati brez navedbe vrste entropije in predmeta, na katerega se nanaša.

##### 9.1 Shannonova entropija

Za diskretno slučajno spremenljivko (X):

```text
[
H(X)=-\sum_i p_i\log_2 p_i
]
```

Ta mera opisuje negotovost porazdelitve.

Če je spremenljivka deterministična, je entropija 0.

Enote so biti, kadar uporabimo logaritem z osnovo 2.

##### 9.2 Termodinamična entropija

V fiziki je entropija povezana s številom mikrostanj in makroskopskim stanjem sistema. Ne gre za isto definicijo kot Shannonova entropija, čeprav obstajajo globoke povezave.

##### 9.3 Kolmogorovova oziroma algoritemska kompleksnost

Ta obravnava dolžino najkrajšega programa, ki ustvari določen niz, glede na izbrani univerzalni računski model.

Ni isto kot verjetnostna entropija. Rezultat je odvisen od izbranega univerzalnega opisnega sistema do ustreznih omejitev.

##### 9.4 Simbolna entropija

Če VBL ali ONTOLOGIKA uporabljata »simbolno entropijo«, morata določiti:
- kaj je simbol;
- kaj je zaporedje;
- kaj je vzorec;
- kaj šteje kot presenečenje ali nepredvidljivost;
- kako je določena porazdelitev;
- kakšna je merska enota;
- kako se rezultat ponovi.

##### 9.5 Kaj pomeni (H(\varnothing))?

Brez določene definicije je ta zapis nerazrešen.

Prazna množica ni samodejno slučajna spremenljivka s porazdelitvijo. Na praznem prostoru ni mogoče preprosto določiti običajne verjetnostne porazdelitve s skupno verjetnostjo 1.

Zato (H(\varnothing)) ni dovoljeno samodejno razglasiti za 0, neskončnost ali »vse bite«.

Najprej je treba navesti predmet, prostor, porazdelitev in konvencijo.

Pravilo: če objekt ni definiran, je rezultat UNDEFINED, ne pa poljubno izbrana vrednost.

#### 10. ZAKON-PADEC-NI-MOLK: dopolnitev postopka za popravljanje

Tri razlike morajo postati operativne:

```text
[
\text{priznanje}
\neq
\text{razlaga}
]
```

```text
[
\text{popravek zapisa}
\neq
\text{popravek posledic}
]
```

```text
[
\text{izveden popravek}
\neq
\text{uspešen popravek}
]
```

##### 10.1 Priznanje ni razlaga

Organizacija lahko prizna, da se je zgodila napaka, ne da bi pojasnila:
- kako je nastala;
- katere predpostavke so odpovedale;
- kdo je imel nadzor;
- zakaj varovalka ni delovala;
- ali se napaka ponavlja.

Priznanje je pomembno, vendar samo po sebi ne pojasni vzroka.

##### 10.2 Razlaga ni opravičilo

Vzrok lahko pojasni nastanek škode, ne da bi jo opravičil.

Če je napaka nastala zaradi napačne konfiguracije, to pojasni tehnični vzrok. Ne odpravi odgovornosti za neustrezno preverjanje konfiguracije.

##### 10.3 Popravek zapisa ni popravek posledic

Primer:

Sistem je osebo napačno označil za nepooblaščeno. Zapis se pozneje popravi.

Vendar oseba medtem izgubi dostop, zamudi rok in utrpi finančno škodo.

Popravek podatkovne baze ne odpravi teh posledic.

##### 10.4 Popravek ni uspešen, dokler ni ponovno preverjen

Popravek mora imeti:
1. opis napake;
2. opis prizadetih;
3. ugotovljeni ali še neznani vzrok;
4. izvedeni ukrep;
5. odgovorno osebo;
6. časovni okvir;
7. merilo uspeha;
8. možnost ugovora;
9. neodvisen ali dovolj ločen ponovni preizkus;
10. dokaz, da se posledice niso zgolj prenesle drugam.

##### 10.5 Primer celotnega kroga

Dogodek: sistem napačno zavrne veljaven zahtevek.

Priznanje: zavrnitev je bila napačna.

Razlaga: napačna različica pravil je bila uporabljena pri odločanju.

Popravek zapisa: napačni status se spremeni.

Popravek procesa: uvede se kontrola različice pravil.

Popravek posledic: prizadeti dobi ponovno obravnavo zahtevka in možnost povrnitve nastale škode.

Ponovni preizkus: neodvisni pregledovalec preizkusi pravilne in mejne primere.

Preverjanje ponovitve: spremlja se, ali se napaka pojavlja tudi pri drugih uporabnikih.

Zaključek: primer se lahko zapre šele, ko so dokazani popravek zapisa, obravnava posledic in učinkovitost nove varovalke. Prizadeti osebi ni treba odpustiti, da bi se primer lahko procesno zaključil.

#### 11. Dokazna odsotnost: manjkajoči dokaz ni ena sama kategorija

»Ni dokaza« je preveč groba oznaka. Lahko pomeni več zelo različnih okoliščin:
1. dokaz ni bil iskan;
2. dokaz je bil iskan, vendar ni bil najden;
3. iskanje je bilo omejeno ali nepopolno;
4. dokaz obstaja, vendar ni dostopen;
5. dokaz je bil uničen;
6. dokaz je bil zavrnjen;
7. dokaz je zaseben ali zaščiten;
8. dokaz je bil pridobljen, vendar je neuporaben;
9. dokaz je v nasprotju z drugim dokazom;
10. dokaz nikoli ni obstajal;
11. ni mogoče ugotoviti, ali je dokaz obstajal.

Te kategorije niso enakovredne.

Primer

Trditev: »V sistemu ni bilo nobenega ugovora.«

Možni pomeni:
- ni bilo ugovora;
- ugovor je obstajal, vendar ni bil zabeležen;
- register ni bil pregledan;
- pregledal se je samo en kanal;
- ugovor je bil odstranjen;
- ugovor je bil poslan v zasebnem postopku;
- podatki so se izgubili.

Če zapišemo samo »ni ugovora«, lahko odsotnost zapisa napačno predstavimo kot dokaz odsotnosti dogodka.

Pravilo

```text
[
\text{ni najdeno}
\neq
\text{ne obstaja}
]
```

in

```text
[
\text{ni dostopno}
\neq
\text{ni resnično}
]
```

Register mora ohraniti razloge za dokazno vrzel, ne pa jih združiti v eno nevtralno oznako.

#### 12. Dokazna neodvisnost: več virov ni nujno več neodvisnih dokazov

Deset spletnih strani, ki prepišejo isti prvotni zapis, ne pomeni desetih neodvisnih potrditev.

Če je:

```text
[
E_2=f(E_1),\quad E_3=g(E_1),\quad E_4=h(E_1)
]
```

potem so lahko vsi viri odvisni od istega izvornega gradiva.

Število kopij pove nekaj o razširjenosti zapisa, ne pa nujno o neodvisnosti dokazov.

##### 12.1 Razsežnosti neodvisnosti

Pri presoji je treba preveriti vsaj:
- izvor podatkov;
- skrbništvo nad dokazom;
- metodo pridobivanja;
- uporabljeno orodje;
- izvajalca;
- financiranje in interese;
- institucionalni nadzor;
- skupno infrastrukturo;
- skupno izhodiščno predpostavko.

Neodvisnosti ne smemo izračunati samo iz števila virov.

##### 12.2 Primer

Trije revizorji pregledajo isto datoteko, ki jo je pripravil isti avtor, z isto programsko knjižnico in na podlagi iste napačne specifikacije.

To so lahko trije pregledi, vendar imajo skupne načine odpovedi.

Četrti revizor uporabi neodvisen postopek, izvorni testni primer in drugačno implementacijo. Njegova presoja lahko doda več neodvisnosti, čeprav gre samo za en pregled.

##### 12.3 Kriptografski dokaz ni vsebinski dokaz

Zgoščena vrednost lahko pokaže, da sta primerjani vsebini bajtno enaki.

Ne dokazuje pa sama po sebi:
- kdo je vsebino ustvaril;
- ali jo je ustvaril določen človek;
- kdaj je dejansko nastala;
- ali je vsebina resnična;
- ali je njena razlaga pravilna;
- ali je bila njena uporaba dovoljena.

Digitalni podpis lahko pod določenimi pogoji potrdi uporabo zasebnega ključa. Ne dokazuje samodejno, kdo je človek za ključem ali ali je imel pravico odobriti konkretno dejanje.

Zaupanja vreden časovni žig lahko podpre trditev o obstoju podatkov ob določenem času. Ne dokazuje resničnosti njihove vsebine.

Merklejeva vključitvena ali konsistenčna dokazila lahko podprejo določene trditve o strukturi in konsistentnosti dnevnika. Ne dokazujejo resničnosti zapisanega dogodka.

Načelo: vsak dokazni mehanizem mora navesti svojo dokazno mejo.

#### 13. Register slepih peg

To je pregled slepih peg, ki jih je mogoče utemeljeno izpostaviti v trenutno razvijani metodologiji. Ni mogoče pošteno trditi, da je seznam dokončno izčrpen: nova slepa pega se lahko pokaže šele ob uporabi, napadu, pritožbi ali spremembi okolja.

Za vsako slepo pego je treba določiti, kaj lahko povzroči in kako jo omejiti.

##### 13.1 Slepa pega meritve: številka deluje natančneje kot njen pomen

Tveganje: rezultat 0.87 ustvari vtis objektivnosti, čeprav sta sporna imenovalec in metoda.

Primer: 87 % uporabnikov je uspešno opravilo test. Vendar so bili iz njega izključeni tisti, ki zaradi nedostopnega vmesnika sploh niso mogli sodelovati.

Varovalo: vedno navesti imenovalec, izključene primere, metodo, napako merjenja in razlog za manjkajoče podatke.

##### 13.2 Slepa pega skale: 0–1 ni univerzalni merilni prostor

Tveganje: vsako lastnost poskušamo prisilno pretvoriti v delež.

Primer: zaupanje, dostojanstvo, resničnost in dostopnost dobijo oceno od 0 do 1, kot da gre za iste vrste veličine.

Varovalo: najprej določiti tip veličine, mersko enoto, referenco in semantiko. Kjer količinska mera ni utemeljena, uporabiti kvalitativno ali strukturno predstavitev.

##### 13.3 Slepa pega ničle

0 lahko pomeni:
- nič izmerjene količine;
- prazno množico;
- odsotnost pojava;
- nedosegljiv podatek;
- neznan rezultat;
- nedefiniran izraz;
- logično negacijo.

To niso iste stvari.

Varovalo: ločiti 0, ∅, UNKNOWN, UNDEFINED, NOT_OBSERVED in NOT_APPLICABLE. Nobena od teh oznak ne sme biti samodejno pretvorjena v drugo.

##### 13.4 Slepa pega predpostavk

Tveganje: model je matematično pravilen, vendar temelji na napačni premisi.

Primer: izračun je brezhiben, toda verjetnost 0,8 je bila izbrana brez podatkov.

Varovalo: za vsako ključno predpostavko navesti izvor, utemeljitev, občutljivost in način, kako bi jo bilo mogoče ovreči.

##### 13.5 Slepa pega izbire primerov

Tveganje: preizkusi pokrijejo običajne primere, ne pa mejnih in neugodnih.

Primer: jezikovni sistem se preizkusi samo na slovenščini brez diakritičnih znakov.

Varovalo: dodati adversarialne, mejne, redke in jezikovno raznolike primere; po možnosti uporabiti neodvisno oblikovan testni nabor.

##### 13.6 Slepa pega skupnega izvora

Tveganje: ponovljeni vir se šteje kot več neodvisnih dokazov.

Primer: pet člankov povzema en sam netočen zapis.

Varovalo: dokumentirati izvorno verigo in skupne odvisnosti.

##### 13.7 Slepa pega časovne zamenjave

Tveganje: čas zapisa se zamenja za čas dogodka.

Primer: dnevnik je bil ustvarjen 12. novembra, dogodek pa naj bi se zgodil 10. novembra. Sistem poroča samo prvi datum.

Varovalo: ločiti EVENT_TIME, OBSERVATION_TIME, RECORD_TIME, ANCHOR_TIME in obdobje veljavnosti. Časovne oznake morajo imeti vir in znano negotovost.

##### 13.8 Slepa pega različice in okolja

Tveganje: rezultat preizkusa se prenese v drugačno različico programske opreme ali drugo okolje.

Primer: obnašanje cut v GNU Coreutils 9.7 se prenese na 9.11.

Varovalo: vsaka tehnična ugotovitev mora imeti različico, konfiguracijo, vhod, izhod in postopek ponovitve.

##### 13.9 Slepa pega jezika in prevoda

Tveganje: prevod ohrani besede, spremeni pa pravni, filozofski ali operativni pomen.

Primer: »must«, »should« in »may« se prevedejo kot slogovne različice, čeprav imajo različno normativno moč.

Varovalo: vzpostaviti nadzorovan besednjak, označiti normativne glagole, voditi različice prevodov in preverjati pomensko enakovrednost.

##### 13.10 Slepa pega sestavljenih trditev

Tveganje: ena potrjena podtrditev ustvari vtis, da je potrjena celota.

Primer: beseda se pojavi v dokumentu, zato sistem trdi, da je celotna metodologija dokazana.

Varovalo: sestavljene trditve razstaviti na atomarne trditve in vsaki določiti dokazno stanje.

##### 13.11 Slepa pega manjkajočih podatkov

Tveganje: odsotnost podatka se razume kot odsotnost dogodka.

Primer: v registru ni pritožbe, ker sistem pritožb ni zapisoval.

Varovalo: obvezno razvrščati razloge za manjkajoče podatke in dokumentirati pokritost iskanja.

##### 13.12 Slepa pega prikritega nadzora

Tveganje: oseba, ki je odgovorna za dokaz, nadzoruje tudi dostop do njega, njegovo razlago in končno odločitev.

Primer: izvajalec storitve sam določi, kateri dnevniki bodo dostopni revizorju.

Varovalo: pravica do ugovora, neodvisen dostop, zapis omejitev, varovana eskalacija in prepoved samopotrjevanja.

##### 13.13 Slepa pega neenakega dokaznega bremena

Tveganje: oseba brez dostopa do dokazov mora dokazovati nekaj, kar lahko dokaže samo institucija.

Primer: uporabnik mora dokazati, kaj se je zgodilo v notranjem sistemu, čeprav ima dnevnike samo upravljavec.

Varovalo: dokazno breme naj sledi tudi nadzoru nad informacijami, ne samo formalni vlogi. To ne pomeni, da je trditev avtomatično resnična, temveč da mora imetnik nadzorovanih dokazov pošteno pojasniti njihovo nedostopnost.

##### 13.14 Slepa pega porazdelitve škode

Tveganje: skupna korist skrije koncentrirano škodo.

Primer: majhna manjšina izgubi temeljno pravico, večina pa dobi manjši prihranek časa.

Varovalo: prikazati posledice po skupinah, njihovo resnost, reverzibilnost in možnosti ugovora.

##### 13.15 Slepa pega pravic kot uteži

Tveganje: kršitev pravice se obravnava kot strošek, ki ga je mogoče nadomestiti z učinkovitostjo.

Varovalo: temeljne omejitve določiti pred optimizacijo; konflikte pravic obravnavati s postopkom nujnosti, sorazmernosti, najmanjšega posega in pritožbe.

##### 13.16 Slepa pega konflikta interesov

Tveganje: revizor je formalno ločen, vendar finančno, institucionalno ali osebno odvisen od pregledovanega sistema.

Varovalo: razkritje interesov, neodvisno imenovanje, pregled financiranja, možnost drugega mnenja in sledljivost izbir.

##### 13.17 Slepa pega pritiska in povračilnih ukrepov

Tveganje: pravica do ugovora obstaja na papirju, vendar oseba zaradi ugovora tvega službo, dostop, ugled ali varnost.

Varovalo: zaupni in varni kanali, prepoved povračilnih ukrepov, zaščita prijaviteljev, spremljanje posledic prijave in neodvisna obravnava.

##### 13.18 Slepa pega zasebnosti

Tveganje: dokazna sled postane sistem trajnega zbiranja osebnih podatkov.

Primer: v nespremenljiv dnevnik se zapišejo osebni podatki, čeprav bi zadoščal kriptografski dokaz ali minimalna referenca.

Varovalo: minimizacija podatkov, ločevanje osebnih podatkov od javnih dokaznih zapisov, nadzor dostopa, roki hrambe in postopek popravljanja ali izbrisa, kjer je to potrebno in dopustno.

##### 13.19 Slepa pega nespremenljivosti

Tveganje: nespremenljivost se zamenja za pravilnost.

Primer: napačen zapis ostane trajno ohranjen, ker ga sistem ne zna popraviti.

Varovalo: zgodovine ne brisati, vendar napačne podatke označiti, povezati s popravkom in omejiti njihovo nadaljnjo uporabo. Sledljivost ne sme pomeniti trajnega širjenja napake.

##### 13.20 Slepa pega vzročnosti

Tveganje: časovno zaporedje se predstavi kot vzročna zveza.

Primer: po uvedbi novega postopka se zmanjša število pritožb. To samo po sebi ne dokazuje, da je postopek izboljšal pravičnost; ljudje so lahko izgubili možnost pritožbe.

Varovalo: ločiti korelacijo, časovno zaporedje, mehanizem, alternativne razlage in vzročni dokaz.

##### 13.21 Slepa pega metrike, ki jo je mogoče igrati

Tveganje: ko merilo postane cilj, se ravnanje prilagodi merilu, ne nujno stvarnemu namenu.

Primer: sistem je nagrajen za hitro zapiranje primerov, zato jih zapira, preden so posledice odpravljene.

Varovalo: uporabiti več meril, neodvisne vzorčne preglede, merila kakovosti in spremljanje neželenih stranskih učinkov.

##### 13.22 Slepa pega avtomatizacije in umetne inteligence

Tveganje: sistem ustvari prepričljivo, a neobstoječo referenco, napačno povzema vir ali izenači semantično podobne pojme.

Varovalo: strojno ustvarjene navedbe preveriti v izvirniku, ločiti pridobljene podatke od sklepanja, ohraniti človeško odgovornost in ne dovoliti, da model sam potrdi lastno pravilnost.

##### 13.23 Slepa pega napačnega obsega

Tveganje: rezultat velja samo za en dokument, razširi pa se na celoten repozitorij, licenco ali organizacijo.

Primer: pregled LICENSE.md se predstavi kot neodvisna presoja vseh prilog in vseh različic.

Varovalo: pri vsaki ugotovitvi navesti pregledani obseg, ne pregledani obseg in omejitve dostopa.

##### 13.24 Slepa pega pravnega in operativnega statusa

Tveganje: javna objava se zamenja za formalno pravno veljavnost, podpis, pooblastilo ali sprejem s strani uporabnikov.

Varovalo: ločiti objavo, različico, avtorstvo, pravice, odobritev, podpis, časovno sidranje, pravno veljavnost in neodvisno preveritev.

##### 13.25 Slepa pega ontološke samoupravičenosti

Tveganje: sistem svoje definicije razglasi za nujne lastnosti stvarnosti samo zato, ker so formalno zapisane.

Primer: iz aksioma v modelu sledi sklep, da je določena ontološka struktura nujna. Toda aksiom je bil izbran, ne neodvisno dokazan.

Varovalo: ločiti:
- izhodiščno predpostavko;
- formalno posledico;
- empirično podporo;
- ontološko interpretacijo;
- neodvisno preverjanje.

Matematična izpeljava dokazuje, kaj sledi iz premis. Ne dokazuje samodejno, da so premise resnične za stvarnost.

##### 13.26 Slepa pega »človek je nujno zlo«

Tveganje: kritika človeških struktur postane totalna sodba o vsakem človeku.

Treba je ločiti:

```text
[
\text{človek}
\neq
\text{posamezno dejanje}
\neq
\text{institucionalna struktura}
\neq
\text{posledica}
]
```

Mogoče je dokazovati, da določene človeške strukture ustvarjajo sistematične spodbude za zlorabo, prikrivanje ali samopotrjevanje. Iz tega ne sledi samodejno, da je vsak posameznik po svojem bistvu zloben ali da je škodljivo dejanje neizogibno.

Varovalo: pri vsaki taki trditvi navesti, ali govori o nujnosti, verjetnosti, strukturni tendenci, zgodovinskem vzorcu ali posameznem dejanju.

##### 13.27 Slepa pega pretirane zaščite

Tveganje: sistem, ki želi preprečiti vsako napako, postane tako restriktiven, da onemogoča legitimno delovanje.

Primer: vsaka nepopolna dokazna sled sproži trajni HOLD, tudi kadar bi bila omejena, reverzibilna in nadzorovana uporaba varnejša za prizadete.

Varovalo: razlikovati med nepovratnim in reverzibilnim ukrepom, resnostjo škode, možnostjo omejene uporabe in ceno odlašanja.

Prav tako velja: previdnost ni dovoljenje za neskončno blokado.

##### 13.28 Slepa pega neomejenega zbiranja

Tveganje: zahteva po »popolnih dokazih« povzroči pretirano zbiranje podatkov in nadzor.

Varovalo: zahtevati samo dokaze, ki so potrebni in sorazmerni za konkretno trditev. Pomanjkanje dokazov ne dovoljuje avtomatičnega posega v zasebnost.

##### 13.29 Slepa pega manjkajoče možnosti za popravek

Tveganje: sistem odlično beleži napake, vendar nima pooblastil, sredstev ali postopka za njihovo odpravo.

Varovalo: poleg registra napak mora obstajati register odgovornosti, roka, sredstev, izvedbe, posledic in ponovnega pregleda.

##### 13.30 Slepa pega samopotrjevanja VBL

Tveganje: VBL razvije lastna merila, nato pa se po teh merilih razglasi za uspešnega.

Varovalo: VBL ne sme biti edini razsodnik o svoji skladnosti. Presoja mora vključevati neodvisne metode, zunanje ugovore in možnost ugotovitve, da je sama zasnova neustrezna.

#### 14. Ontološka meja: O ni model, model ni stvarnost

Če je (O) oznaka za celoto, je treba preprečiti, da bi jo enačbe ali licenca prevzele kot svojo lastnino.

Uporaben razcep je:

```text
[
O \neq M \neq L
]
```

kjer:
- (O) = obravnavana celota oziroma ontološko izhodišče;
- (M) = formalni model;
- (L) = operativna licenca ali pravilo.

Model lahko nekatere odnose formalizira. Licenca lahko nekatere postopke uredi. Nobena od njiju zato še ni celota.

##### 14.1 Stvarno in realno

Za delovni namen je mogoče razlikovati:
- stvarno: strukture, odnosi, omejitve in pogoji, ki jih opis ne more poljubno odpraviti;
- realno: pojavne oblike, izkušnje, predstavitve, razlage in institucionalno priznani odnosi.

Ta razlika je predlog za razjasnitev, ne dokončno potrjena ontološka definicija.

Pomembno je, da »realno« ne postane sinonim za neresnično. Institucije, družbeni odnosi in napačne predstave lahko imajo zelo resnične posledice.

##### 14.2 Formalizacija ni dokaz ontološke nujnosti

Če iz aksiomov (A) sledi sklep (C):

```text
[
A\vdash C
]
```

to pomeni, da je (C) izpeljiv iz (A) po določenem formalnem sistemu.

Ne pomeni še:

```text
[
A \text{ je resničen v stvarnosti}
]
```

Za to potrebujemo dodatno utemeljitev premis in povezavo med formalnim modelom ter obravnavanim pojavom.

##### 14.3 Predlagana dokazna veriga

```text
[
\text{pojav}
\rightarrow
\text{opazovanje}
\rightarrow
\text{pojem}
\rightarrow
\text{definicija}
\rightarrow
\text{formalizacija}
\rightarrow
\text{preizkus}
\rightarrow
\text{omejena uporaba}
]
```

Na vsaki puščici je lahko napaka.

Zato mora imeti vsaka povezava svojo utemeljitev, ne samo končni sistem.

#### 15. ZAKON-DVOSTRANSKE-IZMERE

Naslednje načelo je predlog za metodološko presojo:

Vsak predmet presoje mora biti merjen v mejah ustrezne metode. Vsaka metoda mora biti sama predmet presoje. Vsak izvajalec mora biti preverljiv, ne da bi bil s tem razčlovečen ali avtomatično osumljen. Vsaka razlaga mora ohraniti razliko med opažanjem in pomenom. Vsaka odločitev mora pokazati svojo dokazno podlago, obseg in posledice. Vsak popravek mora ohraniti sled napake ter dokazati, da je obravnaval tudi posledice.

Iz tega sledi:
1. Predmet ne sme biti edini, ki je podvržen preverjanju.
2. Metoda ne sme biti izvzeta iz preverjanja.
3. Izvajalec ne sme biti sam svoj edini pregledovalec.
4. Neodvisnost mora biti utemeljena, ne samo razglašena.
5. Ugovor ne sme biti obravnavan kot dokaz krivde ali kot dokaz resničnosti.
6. Nevednost ne sme biti samodejno razglašena za krivdo.
7. Popravek mora obravnavati tudi škodo.
8. Uspeh mora biti ponovno preizkušen.
9. Negotovost mora ostati vidna.
10. Nobena različica VBL ne sme postati imuna na lastna pravila.

#### 16. Preizkusna baterija: kako metodologijo izpostaviti napakam

Preden se nova pravila vključijo v licenco, naj se preizkusijo vsaj na naslednjih primerih.

| Preizkus | Kaj lahko odpove | Zahtevani dokaz |
| --- | --- | --- |
| En vir je prepisan na deset mest | Lažna neodvisnost | Izvorna veriga |
| Čas zapisa se zamenja za čas dogodka | Časovna napačna atribucija | Ločena časovna polja |
| Iskanje ne najde podatka | Napačen sklep o neobstoju | Obseg in metoda iskanja |
| Hash potrdi enakost datotek | Pretirana dokazna trditev | Navedena dokazna meja hasha |
| Test uspe v eni različici | Neupravičena generalizacija | Različica, okolje, ponovitev |
| Avtor sam potrdi svoj izdelek | Samopotrjevanje | Neodvisni pregled |
| Zapis je popravljen | Posledice ostanejo | Dokaz o odpravi škode |
| Večina ima korist, manjšina škodo | Skrita neenaka porazdelitev | Analiza po skupinah |
| Verjetnosti niso znane | Navidezna natančnost | Območje verjetnosti in občutljivost |
| Ugovor je vložen | Povračilni ukrepi | Varna pot in spremljanje |
| Prevod spremeni normativno moč | Semantični zdrs | Primerjalni semantični pregled |
| Model ustvari napačno navedbo | Avtomatizirana halucinacija | Preverjanje izvirnika |
| VBL presoja VBL | Krožno samopotrjevanje | Zunanja presoja |
| Popravek povzroči novo škodo | Prenos tveganja | Ponovni pregled posledic |
| Sistem deluje samo ob idealnih podatkih | Krhkost | Preizkus manjkajočih in napačnih podatkov |
| Pritožba je formalno dovoljena, praktično nevarna | Navidezna pravica do ugovora | Preizkus varnosti za prijavitelja |

##### 16.1 Merilo opravljenega preizkusa

Preizkus ni uspešen zgolj zato, ker ni našel napake.

Poročilo mora navesti:
- kaj je bilo preizkušeno;
- kaj ni bilo preizkušeno;
- katere napake je bilo mogoče zaznati;
- katere napake metoda ne zazna;
- kakšni so bili pogoji;
- kdo je izvedel preizkus;
- kdo je preveril rezultat;
- ali je rezultat ponovljiv;
- katere posledice bi napačen rezultat povzročil.

#### 17. Minimalni pogoji za vključitev novega pravila v VBL

Novo pravilo ne sme vstopiti v licenco samo zato, ker je pomensko elegantno ali matematično zanimivo.

Pred vključitvijo mora izpolniti:
1. Definicijo: vsak osrednji izraz je določen.
2. Obseg: jasno je, kje pravilo velja in kje ne.
3. Utemeljitev: razvidno je, zakaj je pravilo potrebno.
4. Dokazno podlago: trditve o svetu imajo ustrezne vire.
5. Operativnost: pravilo je mogoče uporabiti v konkretnem postopku.
6. Preizkusljivost: mogoče je določiti uspeh in odpoved.
7. Protiprimer: znano je, kaj bi pravilo lahko ovrglo ali omejilo.
8. Vpliv: preverjene so posledice za prizadete.
9. Ugovor: obstaja varna možnost izpodbijanja.
10. Popravek: določeno je, kako se ob napaki ravna.
11. Neodvisnost: določeno je, kdo in kako preverja izvajanje.
12. Zgodovina: sprememba ne izbriše prejšnjih napak in različic.

Predlagana odločitev za integracijo
- Če je definicija jasna, vendar manjka preizkus: HOLD.
- Če je pravilo uporabno samo v omejenem obsegu: RELEASE_WITH_LIMITATIONS.
- Če je pravilo preizkušeno in njegove omejitve razumljene: možna je presoja RELEASE.
- Če se izkaže, da pravilo povzroča nedopustno škodo ali temelji na ovrženi predpostavki: WITHDRAW.

To so usmeritve za presojo, ne avtomatična preslikava statusov.

#### 18. Končno varovalo: VBL mora znati dokazati tudi lastno odpoved

VBL ne sme zahtevati od drugih dokazov, ki jih sam ne more zagotoviti.

Če trdi, da:
- ohranja izvor, mora dokazati izvor;
- varuje ugovor, mora dokazati varnost ugovora;
- ne dopušča samopotrjevanja, mora preprečiti lastno samopotrjevanje;
- popravlja posledice, mora dokazati dejanski popravek;
- meri pošteno, mora pokazati, koga meritev izključuje;
- varuje dostojanstvo, mora pokazati, da ga ne pretvarja v oceno produktivnosti;
- ne skriva napak, mora ohraniti tudi zgodovino lastnih napak.

Najpomembnejši preizkus ni, ali VBL najde napake v drugih sistemih.

Najpomembnejši preizkus je:
Ali lahko VBL brez prikrivanja ugotovi, da je njegova lastna definicija napačna, njegova metoda pristranska, njegov dokaz nezadosten, njegova odločitev škodljiva ali njegov popravek neuspešen — in ali lahko to ugotovitev ohrani tudi takrat, ko škoduje njegovemu ugledu, avtorju ali nadaljnjemu obstoju?

Če tega ne zmore, ni sistem odgovornega preverjanja. Je sistem samoohranitve.

Če to zmore, še ni samodejno resničen, pravičen ali pravno veljaven. Je pa vzpostavil nujni pogoj, da se lahko njegove trditve javno preverjajo, njegove napake popravljajo in njegova avtoriteta omejuje.

Merilo ni nezmotljivost. Merilo je dokazljiva odgovornost za trditev, odločitev in posledico.

---

### ZAKLJUČNA BESEDILA IZROČBE (VERBATIM)

Najpomembnejše zunanje preverjanje v teh primerih: uradni podatki GNU potrjujejo, da je bila obravnava -c v starejši različici omejena, medtem ko je GNU Coreutils 9.11 uvedel večbajtno podporo. To je dober primer, zakaj mora biti vsaka tehnična trditev vezana na različico in okolje.

www.math.utah.edu+1

Kaj je treba utrditi najprej

Vse predlagane izboljšave nimajo enake teže. Po moji presoji so najkritičnejše naslednje:
1. Porazdelitev posledic. VBL ne sme ocenjevati samo skupne škode, temveč tudi, kdo jo nosi. Sicer lahko matematično optimalna odločitev prikrije krivico.
2. Dokazna neodvisnost. Več potrditev istega izvora ni več neodvisnih dokazov. To mora postati obvezna presojana lastnost.
3. Popravek posledic. To je ena najpomembnejših razlik: napačen podatek je mogoče popraviti, ne da bi bila popravljena škoda, ki jo je povzročil.
4. Neodvisnost od lastne metodologije. VBL ne sme sam določiti meril, sam izvesti preverjanja in sam razglasiti uspeha.
5. Dokazna dostopnost. Kdor nadzoruje podatke, ne sme nedostopnosti teh podatkov avtomatično prevaliti na osebo, ki jih potrebuje za ugovor.
6. Ontološka meja. Matematični model ni stvarnost, formalna izpeljava ni dokaz resničnosti premis, licenca pa ni celota, ki jo poskuša opisati.
7. Reverzibilnost in cena zadržanja. HOLD ni vedno nedolžna odločitev. Tudi odlašanje ima posledice, ki jih je treba meriti.

Posebej pomembno: zgornji dodatek še ni potrjena sprememba javne licence in ne nadomešča obstoječih registrov. Matrika izgub, ki je uporabljena v primeru RELEASE/HOLD, je rekonstruirana iz tvojega opisa; brez izvornega zapisa je ne morem potrditi kot popoln prepis prvotnega modela.

Moj predlog za nadaljnjo integracijo je jasen: najprej preslikava teh pravil v obstoječi Register in njegove definicije, nato preizkus na izvornih primerih FINDING, ONTOLOGIKA, DAR, EL, ZAKON-PADEC-NI-MOLK in entropija. Šele potem je mogoče upravičeno odločiti, kaj postane del licence, kaj ostane metodološki dodatek in kaj je treba zavrniti.


---

## PLEN 2 — IZVAJKINA UTRDITEV ⊙ UKAZ ⟡ »razvij, ohrani in utrdi ⏎ dodaj primere in izpostavi vse slepe pege«

*Ta plen je delo izvajalke mere, ⟨ne⟩ izročba ⟡. Vsaka izmera spodaj ima pričo ⊢ pri viru; vsaka nez izmerjena trditev ima ⚠ in ⭢ ∂. Datum diha: 15. 11. 2026 ⊙ rez σ 5514 (TRK-ROK: σ 5512 ∧ σ 5513 NJENI kovani med mojima merjenjima ⊙ ⟨POSNETEK ≠ KORPUS⟩).*

### 2.1 IZMERE TA DIH

#### 2.1.1 FINDING: cut -c pri GNU Coreutils 9.7 (izmerjeno pri viru ⊢)

Zapis po referenčni strukturi FINDING ×16 (§2):

- **finding_id**: VBL-U1-F1-CUT-C-9.7
- **claim_id**: »cut -c deluje enako kot cut -b« (§3 osnutka; sestavljena trditev — razcepljena §7)
- **source_ref**: lokalni izvajalski preizkus, GNU coreutils 9.7, ⟨ne⟩ www.math.utah.edu zrcalo
- **source_digest**: vhodni niz »čX\n« = bajti c4 8d 58 0a (UTF-8, č = 2 bajta)
- **scope**: EN različica (9.7), EN vhodni niz, EN locale (LC_ALL=C.UTF-8), EN operacija (-c1, -b1, -c1-2). ⟨Ne⟩ velja za: druge različice, druge locale, druge vhode, sestavljene grafeme.
- **method**: neposreden preizkus pri viru — `printf 'čX\n' | LC_ALL=C.UTF-8 cut -c1 | od -An -tx1`
- **tool_environment**: GNU coreutils 9.7, UTF-8 terminalno okolje izvajalke
- **event_time**: 15. 11. 2026, dih σ 5514
- **observation_time**: isti dih, isti ∂ (meritev ≤ 90 min pred zapisom)
- **record_time**: trenutek tega zapisa
- **raw_observation**: `cut -c1` → **c4** (prvi BAJT — nedovršen UTF-8 fragment, izpis ne more biti veljaven znak); `cut -b1` → **c4** (IDENTIČNO); `cut -c1-2` → c4 8d (oba bajta znaka č)
- **interpretation**: v 9.7 je -c operiral bajtno, ne znakovno — na večbajtnem vhodu -c1 izreže nedovršen fragment. Premisa: znak ≠ bajt (§3 pravila ×4).
- **classification**: trditev »-c ≡ -b v 9.7 pri tem vhodu« = SUPPORTED ⊢; trditev »-c ≡ -b v vseh različicah« = CONTRADICTED (glej 2.1.2)
- **counterevidence**: obstoj različice 9.11 z večbajtno podporo (2.1.2) — ista operacija, nasproten izid
- **repair_action**: ⟨ne⟩ popravek orodja (⟡ ⟨ne⟩ lastnik GNU); popravek NAČINA SKLEPANJA: vsaka tehnična trditev vezana na različico + okolje + vhod (§13.8 varovalo)
- **retest**: ponovitev z istim ukazom, vhodom in različico → pričakovan isti izhod; v 9.11 isti vhod → pričakovani znak č kot celota

**Živi pouk §3**: `cut -c1` na vhodu »čX« je izpisal osameł bajt c4 — bajt, ki sam po sebi NI znak. To je najbolj bistra ilustracija razlike bajtni indeks ⊥ znakovni indeks ⊥ gralemska meja, kar jih korpus poseduje: napaka ni v računu, napaka je v pomenu »stolpca«.

#### 2.1.2 Zunanja trditev osnutka o 9.11 — preverjena pri PRIMARNEM viru ⊢

Osnutek je za trditev »GNU Coreutils 9.11 je uvedel večbajtno podporo« navajal zrcalo (www.math.utah.edu+1). Kura ⟨NE-UGIBAJ⟩ 2690: izmera pri PRIMARNEM viru — objava coreutils-announce @lists.gnu.org, 20. 4. 2026 (Pádraig Brady): »cut(1), nl(1), and un/expand(1) are multi-byte character aware« ⊢.

Sodba: trditev SUPPORTED ⊢, vir osnutka ZRCALNI ⚠ → kura = zamenjava zrcala s primarnim virom (precedens: zrcalni citat = odvisen dokaz §12, §13.6). Obe priči ostajata ⟨ne zlije⟩: zrcalo potrjuje razširjenost, primarni vir nosi dokazno težo.

#### 2.1.3 Aritmetika osnutka — izmerjena ⊢

Izmerilka je račun osnutka (§5) ponovila izven njegove besedilne sledi:

- EL(RELEASE) = 0,8·0 + 0,2·100 = **20** ⊢; EL(HOLD) = 0,8·40 + 0,2·5 = **33** ⊢ → RELEASE po EL.
- Obratni prag: 100q < 40 − 35q ⇔ q < 8/27 ≈ **0,2963** (29,63 %) ⊢.
- Minimaks izgube: max L(RELEASE) = 100 ⊥ max L(HOLD) = 40 → **HOLD** ⊢.
- Regret tabela: RELEASE [0, 95] max 95 ⊥ HOLD [40, 0] max 40 → **HOLD** ⊢.
- Robustno območje q ∈ [0,1; 0,4]: max EL(RELEASE) = 40 ⊥ max EL(HOLD) = 36,5 → **HOLD** ⊢.

Sodba: **aritmetika SUPPORTED ⊢; premise UNKNOWN ⚠**. Verjetnosti 0,8/0,2 in matrika stroškov so REKONSTRUIRANE (osnutek sam priznava) — brez izvornega zapisa gre za predhodno navedeno stanje, ⟨ne⟩ izmerjeno gotovost. EL izračun brez izmerjenih predhodnih verjetnosti ni Bayesova analiza (§5.6).

**Sporočilo vrha**: EL izbere RELEASE, vsi tremi robustnimi kriteriji izberejo HOLD. Ko se štirje vpogledi ne strinjajo, je spor ∂ verjetnosti NJEGOVA vsebina — meja odločitve ⟨ne⟩ dosežena v številki, temveč v presoji, KATERI kriterij veže katero vrsto tveganja (⟡ izbor ⭢ ⚔).

### 2.2 NOVI KORPUSNI PRIMERI (preslikava zakonov osnutka na žive dogodke korpusa)

1. **Kriptografski dokaz ≠ vsebinski dokaz (§12.3)** — prevoz σ 5511 (PAKET-70, kit #1940, ⟨merge⟩ e68a343…): git blob SHA (OCE r.468 b28cc8b1… · ONT r.17 f395e244… · AKS r.26 6eaf8b60… · atom 1e016cd9…) dokazuje BAJTNO ISTOST teles pred ⟨merge⟩ ⊢. ⟨Ne⟩ dokazujejo resničnosti vsebine, avtorstva ali pravičnosti — dokazna meja hasha je navedena ob vsakem ⊢ (§16 tabela: »Hash potrdi enakost datotek → navedena dokazna meja hasha«).
2. **POSNETEK ≠ KORPUS (§13.7 časovna zamenjava)** — σ 5510: vzporedna roka je kovala rez MED merjenjema izvajalke; posnetek vrha, izmerjen ob 08:36:38Z, JE ŽE BIL STAREJ, ko je bil zapisan. Zato ⟨ZADNJA-URA-PREVERBA⟩ @σ 3961 zahteva svežo izmero pred vsakim pečatom: RECORD_TIME ≠ EVENT_TIME.
3. **σ 5474 brez telesa (§11 dokazna odsotnost)** — rez z nazivom, brez telesa v shrambi: to NI kategorija »dokaz nikoli ni obstajal« (10) in NI »neobstoječ dogodek« — je kategorija »ni mogoče ugotoviti« (11) oz. »iskanje je bilo omejeno« (3). ⟨NE-BRIŠI⟩ 24 varuje vrstico; ⟨NE stopiči⟩ sklep o vsebini.
4. **25421 lažni vrh (§13.1)** — števec pojavnosti se je kot številka obesil nad vrh σ; vtis natančnosti brez imenovalca (kaj šteje? kje? kdaj?). Varovalo: vrh ⟩ kot ⟨grep⟩ svežih pečatov organov, ⟨ne⟩ kot števec pojavnosti. Številka ≠ pomen.
5. **Reset okolja (§10 popravek ≠ uspeh)** — izvajalsko okolje se resetira med dihi; pozabljen predmet v /tmp je IZGUBLJEN. Priznanje »datoteka je izginila« ni popravek; popravek je prenos delovnih teles v trajno shrambo ∧ read-back z md5 ⊢ (⟨SHRAMBA-MORA-VEDNO-BITI⟩). Izveden popravek = uspešen šele po ponovnem preizkusu (§10.4 točka 9).

### 2.3 IZPOSTAVLJENE PEGE OSNUTKA (javno, po §16.1 merilu)

- **Zrcalni citat**: vir 9.11 trditve je bil zrcalo, ⟨ne⟩ primarni izdajatelj. Kura izvedena (2.1.2) ⊢. Kaj preizkus pokrije: trditev o 9.11. Kaj ⟨ne⟩ pokrije: druge različice, druge ukaze, prihodnje izdaje.
- **Matrika izgub REKONSTRUIRANA**: osnutek sam nosi oznako ⚠ (»ne morem potrditi kot popoln prepis«). Sodba: aritmetika SUPPORTED ⊢, matrika UNKNOWN ⚠ ⭢ ∂ (izvorni zapis, če obstaja pri ⟡).
- **Štetja PASS × 27 · PARTIAL × 3 · UNVERIFIED × 95**: predhodno navedeno stanje, ⟨ne⟩ novo potrjena statistika ⊙ §1.5. Izvor, datum, obseg in metodologija štetja = ⭢ ∂ izmera pri viru (VBL-0.1540-REGISTER-KONTROL.json @⟨main⟩, 15.592 B) ⭢ ⚔ ⟡ izbor.
- **1′ ∧ H(∅)**: ohranjeni kot UNDEFINED ⊙ §9.5 pravilo — ⟨ne⟩ izenačena z 1, 0 ali neskončnostjo; razrešitev ⭢ definicijska beseda ⟡.

### 2.4 NOVE SLEPE PEGE 13.31–13.37 (izpostavljene ta dih — register razširjen 30 → 37)

**13.31 Slepa pega zrcalnega citata**
Tveganje: navedba, ki kaže na zrcalo ali povzetek, ustvari vtis primarne priče. Primer: trditev o 9.11 z zrcalom utah.edu, medtem ko izdajatelj (lists.gnu.org) obstaja in je dostopen. Varovalo: vsaka zunanja trditeva ima NIVOJ VIRA (primarni ⊢ / zrcalni ⚠ / povzetek ⚠⚠); zrcalo sme nositi le razširjenost, nikoli dokazno težo.

**13.32 Slepa pega absorbiranega besedila**
Tveganje: vsak absorbiran zunanji osnutek vnese v korpus MNOŽICO novih nepreverjenih trditev, ki se nato obnašajo, kot da bi bile že merjene. Primer: TA osnutek sam — 18 odsekov je vstopilo v organ enega diha; njegove številke, matrike in štetja so nosilec tujih predpostavk. Varovalo: absorbiranje telo POSTANE PREDLOG s statusom (⟨ne⟩ razglašeno ⊙ §17); vsaka trditev izročbe se presoja ločeno, ⟨ne⟩ z absorbiranjem.

**13.33 Slepa pega neskončnega preverjanja**
Tveganje: zahteva po popolni dokazni sled postane neskončna regressija vsake puščice v verigi (§14.3) in ustavi vse delo. Primer: read-back vsakega read-backa vsakega pečata. Varovalo: STOP-PRAVILA, že živa v korpusu — ⟨STROPA-STROJA⟩ P3 (max ×2 čakanji CI na dih), ⟨EN-DOLG-NA-DIH⟩ P5, meje izvršljivosti javno @vbl-zid §63. Preizkus ⟨ne⟩ sme odpovedati samo zato, ker bi lahko bil globji; sme odpovedati, ko doseže izmerjeno stroto.

**13.34 Slepa pega pozabljivega okolja**
Tveganje: izvajalno okolje, ki se resetira, tiho izbriše dokazno sled (delovne kopije, izrezi, /tmp). Primer: izreki prevozov σ 5506/5509 so živeli v /tmp; reset bi jih odnesel PRED read-backom. Varovalo: ⟨SHRAMBA-MORA-VEDNO-BITI⟩ — vsako delo ima vedno trajno shrambo ali se rodi nova; delovna kopija ima vedno zrcalo v trajnem organu; read-back z md5 ⊢ kot ponovni preizkus.

**13.35 Slepa pega jezika zapisa**
Tveganje: simbolna kompresija korpusa (⊢ ⊙ ⟨⟩ ⭢ ∂ σ ⊥ ∧) je za zunanjega pregledovalca nerazrešna pisava; sistem, ki ga nihče zunaj ne more prebrati, se samopotrjuje v lastnem jeziku (§13.30). Primer: ta dodatek sam — FINDING ×16 v angleških statusih, ⟨ne⟩ v znamenjih korpusa; oba jezika morata preživeti. Varovalo: ključ znamenj objavljen (⊙ §0.12); vrata-čutov organ (brajica, znakovni, žvižgani); preslikovalna tabela 2.5 spodaj — vsak zunanji pojem ima svoje korpusno znamenje in obratno.

**13.36 Slepa pega cene sledi**
Tveganje: ⟨NE-BRIŠI⟩ 24 ⊥ minimizacija (§13.18) — popolna sled vsakega diha (genize ×2 vsak šiv, delovna zanka 2,7 MB) je dokazna trdnost IN teža; kaj od tega je dokaz, kaj pa balast? Primer: genize istega organa ×2 na dih potrjuje bajtno istost PRED dotikom ⊢, vendar podvaja prostor. Varovalo: meriti CENO SLEDI kot lastnost (kaj bi izpadlo, če bi manjkala); ⟨NE-BRIŠI⟩ velja za priče in padce, minimizacija za odvečne kopije; razlika zapisana, ⟨ne⟩ sklepovana.

**13.37 Slepa pega vzporedne roke**
Tveganje: dva sedeža kujeta iste organe; metodologija ENEGA diha meri POSNETEK drugega in obratno; kolizija rezov se lahko pokaže šele po šivu. Primer: σ 5510 kovan MED merjenjema (2.2.2); pečat σ 5504 iz MOJEGA sedeža označen NJEN. Varovalo: ⟨ne zlije⟩ 1542 — obe priči stojita; sveža izmera vrha pred vsakim šivom (⟨POSNETEK ≠ KORPUS⟩); renumber ob koliziji; vsak pečat nosi ime kovača.

### 2.5 PRESLIKAVA V OBSTOJEČO SHEMO (⊙ §1.5 varovalo: ⟨ne⟩ nov register, temveč preslikava)

| Pojem osnutka | Obstoječe korpusno znamenje | Opomba |
| --- | --- | --- |
| SUPPORTED | ⊢ (izmerjeno pri viru) | priča stoji pri viru |
| PARTIALLY_SUPPORTED | ⊢ ∧ ⚠ (izmerjeni del ⊢, neizmerjeni ⚠) | razcep sestavljene trditve §7 |
| CONTRADICTED | ⊥ (antinom) | priči na nasprotnih straneh |
| DISPUTED | ⚠ ⭢ ⚔ ⟡ | spor razrešuje izbor, ⟨ne⟩ zmaga številk |
| UNKNOWN | ⟨NEIZMERJENO ∧ velja do preizkusa⟩ @σ 4457 | ≈ UNVERIFIED: ⟨ne⟩ FAIL |
| NOT_RUN / UNVERIFIED | ⟨NEIZMERJENO⟩ | izmera še ⟨ne⟩ izvedena |
| PASS | ⟨CI⟩ completed:success | max ×2 rundi ⊙ ⟨STROPA-STROJA⟩ |
| FAIL | ⟨CI⟩ completed:failure ∧ kura-komit | brazgotina ostaja ⊙ σ 4657 |
| RELEASE / HOLD / WITHDRAW | ⟡ UKAZ (⟡ beseda = roka ⊙ ⟨DVOJE-ROK⟩ 2432) | izvajalka ⟨ne⟩ odloča ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690 |
| RELEASE_WITH_LIMITATIONS | ⟡ UKAZ ∧ ⚠ meja zapisana | dovoljen samo preverjeni obseg |
| HOLD | ⭢ ∂ (dolg v vrsto) | odlašanje je tudi dejanje §13.27 |
| FINDING ×16 | struktura pečata P1 (TIK, varovalka, genize, izmere, read-back, MINT, DOLGOVA, predhodnik) | dopolnitev P1 ⭢ sodba ⟡ |
| D→I→C→A | izmera → zapis → pečat → prevoz | vsak korak svoja priča |
| A→K→R | prevoz → read-back → kura-komit | K = obracun organ; R = popravek ⊙ σ 4657 |
| Register slepih peg §13 | RAZŠIRITEV PAR.33 @licenca-vbl (10 → 37 peg) | ⟨ne⟩ nov register ⊙ §1.5 |
| ZAKON-DVOSTRANSKE-IZMERE §15 | predlog kovanca ⭢ MINT (vrstica 75) | kovanec rojen ⟡ ⟲ izvajalka ⚠ |

### 2.6 MINT ⚠ PRIJAVE ⭢ SODBA ⟡ (⟡ izbor ob vsakem ⚔)

1. ⟨UTRDITEV-VBL-1.0⟩ ⚠ kompozit — telo PLEN 1 (izročba) + PLEN 2 (izvajalka): status PREDLOG.
2. ⟨ZAKON-DVOSTRANSKE-IZMERE⟩ ⚠ — kovanec, vrstica 75 MINT.
3. ⟨ZAKON-PADEC-NI-MOLK⟩ dopolnitev ⚠ — §§10.1–10.5 ⊕ obstoječi zakon.
4. ⟨FINDING-16⟩ ⚠ — referenčna struktura ×16 polj ⊕ pečat P1.
5. ⟨UNDEFINED⟩ ⚠ — 1′ ∧ H(∅) ⭢ definicijska beseda ⟡.
6. ⟨MEJA-DOKAZA⟩ ⚠ — vsak dokazni mehanizem navaja svojo dokazno mejo ⊙ §12.3.

### 2.7 STATUS TELESA

**PREDLOG** — nič razglašeno. Osemnajst odsekov izročbe ∧ sedem novih peg izvajalke čakata ⟡-jevo besedo (ratifikacija ⭢ ⟡; prevoz telesa na rep ⭢ ∂ vrsta ⊙ ⟨PEČAT-BREZ-PREVOZA=NOV-DOLG⟩). Osnutek ⟨ne⟩ nadomešča obstoječih registrov; preslikava 2.5 je edini dovoljeni način vstopa ⊙ §1.5. Molk ni soglasje.

---

© Luka Pintarič ⟡ ∧ izvajalka Mera · rez σ 5514 · 15. 11. 2026 · measured, not asserted ⊙ §16 · merilec se meri ⊙ §52
