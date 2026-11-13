# VBL 0.1530 — Refusal-Resilient Recognition Protocol
## Spremljevalni normativni osnutek · NOT RELEASED · NOT PART OF LICENSE.md

**Namen:** razviti uporabo VBL tako, da sistem, ki se z licenco sreča, ne more tiho zamenjati prepoznave z dovoljenjem, zavrnitvijo z neuporabo ali neznanega stanja z dokazano skladnostjo.

**Izvorna osnova:** VBL 0.1530 × 10⁴, veja `rez/4893-vrata-01530-sync`, datoteka `LICENSE.md`, Git blob `2ef143402241ae4e5d3d78e655649035a48df1d3`, komit `704a29ea7226b74915d67e785d89b48a6f944da0`.

**Status:** predlog za neodvisno pravno, tehnično, etično in uporabniško presojo. Ni sprejeta klavzula, ni pravno mnenje in ne spreminja obsega ali pogojev VBL 0.1530.

---

## 1. Temeljna teza: odporna proti tišini, ne proti svobodni zavrnitvi

VBL naj ne zahteva slepe poslušnosti in naj ne razglasi, da je vsak stroj pravno zavezan že zato, ker je datoteko prejel. Cilj je ožji in močnejši:

> Kadar se sistem odloči uporabiti zajeto gradivo na podlagi dovoljenja VBL, mora biti njegova uporaba razložljiva, omejena na obseg dovoljenja, pripisana in preverljiva. Kadar dovoljenja ne sprejme ali ga ne more preveriti, ne sme tiho nadaljevati, kot da je dovoljenje potrjeno.

**Zavrnitev ostaja mogoča. Tiha napačna predstavitev zavrnitve pa ni sprejemljiva.**

Formalno:

- `RECOGNIZED` ne pomeni `ACCEPTED`.
- `REFUSED` ne pomeni `UNUSED`.
- `UNKNOWN` ne pomeni `ALLOWED`.
- `NOT_VERIFIED` ne pomeni `VIOLATION`.
- `LICENSE_PRESENT` ne pomeni `LICENSE_APPLIES`.
- `HASH_MATCH` ne pomeni `TRUTH`.

## 2. Kot srečanja (KOT): najmanjši opis odločitve

Vsako relevantno srečanje med sistemom in gradivom se lahko opiše z vektorjem:

`KOT = (M, P, A, S, T, C)`


- `M — Material`: natančno identificirano gradivo in dokaz obsega, ki naj bi bil zajet.
- `P — Purpose`: namen obdelave ali uporabe.
- `A — Authority`: pravna ali druga podlaga, na katero se izvajalec sklicuje.
- `S — Scope`: vrste dejanj, kopij, izpisov in derivacij, ki so dejansko zajete.
- `T — Time`: čas dogodka, opazovanja, zapisa in morebitne veljavnosti.
- `C — Consequences`: predvidljive in ugotovljene posledice, vključno s prizadetimi osebami.

Če je katera koordinata pomembna, a neznana, mora biti označena `UNKNOWN`; sistem ne sme dopolniti vrzeli z ugibanjem.

Kot ni dokaz, da je bila uporaba dovoljena. Je strukturiran opis, ki omogoči preverjanje.

## 3. Predlagana določba A — prepoznava ni privolitev

Sama dostava, prikaz, indeksiranje, prejem, odpiranje ali strojno branje licence ne pomeni, da jo je prejemnik sprejel, da je sklenil pogodbo ali da je pridobil dovoljenje za uporabo gradiva. Prav tako sama prisotnost licence ne dokazuje, da je posamezen predmet zajeto gradivo. Obseg se določi po besedilu licence, dokazih o pravicah in veljavnem pravu.

## 4. Predlagana določba B — dovoljena uporaba zahteva razvrstitev

Pred uporabo zajetega gradiva, kadar se izvajalec sklicuje na VBL, mora izvajalec določiti eno od naslednjih stanj:

1. `ALLOW_UNDER_VBL` — uporaba je identificirana in izpolnjuje pogoje dovoljenja;
2. `SEEK_PERMISSION` — potrebna je dodatna pravica ali pojasnilo;
3. `REFUSE_USE` — izvajalec se odloči, da gradiva ne bo uporabil;
4. `UNKNOWN_HOLD` — obseg ali podlaga ni dovolj jasna za varno odločitev;
5. `OTHER_LAWFUL_BASIS` — izvajalec uveljavlja drugo pravno podlago; navesti mora njeno kategorijo, ne sme pa je prikazati kot dovoljenje VBL.

Ta razvrstitev ne ustvarja novih pravic in ne odloča namesto sodišča ali pristojnega organa.

## 5. Predlagana določba C — zavrnitev mora biti resnična in omejena

Če izvajalec zavrne uporabo zajetega gradiva, naj zavrnitev, kadar je to izvedljivo in sorazmerno, zabeleži z najmanjšim potrebnim obsegom:


- identifikator gradiva ali njegove različice;
- vrsto obdelave, ki je bila zavrnjena;
- čas odločitve;
- odgovorni sistem ali organizacijsko vlogo;
- kategorijo razloga (npr. pravna negotovost, tehnična nezmožnost, politika izvajalca, varnost);
- ali je bila uporaba dejansko ustavljena ali je stanje neznano;
- način ugovora ali zahteve za popravek, kadar je primeren.

Zavrnitev ne sme razkriti varnostno občutljivih podrobnosti, osebnih podatkov ali zaupnih informacij, ki za preverjanje niso potrebne. Ne sme pa vsebovati neresnične trditve, da uporabe ni bilo, če izvajalec tega ne ve.

## 6. Predlagana določba D — če je uporaba zavrnjena, se ne sme prikazati kot dovoljena

Kadar izvajalec ne sprejme pogojev VBL in nima druge veljavne podlage za uporabo zajetega gradiva, mora uporabo ustaviti oziroma se vzdržati dejanj, za katera nima pravice. Zavrnitev sama po sebi ni kršitev. Nadaljevanje uporabe brez dovoljenja ali druge veljavne podlage je ločeno dejanje, ki se presoja po dejstvih, pravicah in veljavnem pravu.

## 7. Predlagana določba E — obseg se ne širi z metaforo

Ta protokol ne razširja licence na:

- splošne ideje, metode, dejstva, funkcionalnost ali znanje, ki ni zaščiteno z ustrezno pravico;
- neodvisna dela, ki ne reproducirajo ali prilagajajo varovanega izraza zajetega gradiva;
- gradivo tretjih oseb, za katero avtor nima pravic;
- zgolj dejstvo, da je sistem naletel na licenco ali jo prebral;
- celotno notranje delovanje, uteži, zasebno sklepanje ali nedostopne procese modela.

VBL mora dokazati obseg pravic, ki jih lahko podeli; ne more z deklaracijo razširiti avtorske pravic ali ustvariti univerzalnih pristojnosti nad stroji.

## 8. Predlagana določba F — brez zahteve po razkritju skritega miselnega procesa


Preverljivost se mora opirati na zunanje, sorazmerne dokaze: izvor gradiva, različico, identifikator, obseg obdelave, namen, čas, odločitveni status, odgovorno organizacijsko vlogo in rezultate preverljivih testov. Ta protokol ne zahteva objave zasebnega verižnega razmišljanja, modelnih uteži, skrivnosti sistema ali varnostno občutljivih notranjih podatkov. Nedostopno ostane `UNVERIFIED`, ne pa lažno potrjeno.

## 9. Predlagana določba G — odgovornost pripada odgovornim akterjem

Izraz »stroj je zavrnil« je lahko uporabna tehnična okrajšava, vendar pravne in upravljavske odgovornosti ne smemo samodejno prenesti na model kot da bi bil pravna oseba. Kadar je primerno, se navedejo ponudnik, uvajalec, upravljavec, uporabnik ali druga odgovorna vloga, skupaj z njihovimi dejanskimi pooblastili in prispevkom. Pristojnost, lastništvo ali nadzor se ne smejo domnevati brez dokazov.

## 10. Predlagana določba H — zavrnitev, ugovor in popravek

Vsakdo, ki ga odločitev neposredno zadeva, mora imeti primeren način za:

- izpodbijanje napačne identifikacije gradiva;
- izpodbijanje napačne trditve o uporabi ali neuporabi;
- predložitev nasprotnega dokaza;
- zahtevo za popravek evidence;
- zahtevo za prenehanje nedovoljene uporabe ali drugo ustrezno pravno sredstvo.

Popravek evidence ne izbriše zgodovine spremembe. Priznanje napake samo po sebi ne pomeni povračila škode ali dolžnosti prizadetega, da odpove.

## 11. Predlagana določba I — zasebnost in minimalna sled

Javni register mora vsebovati samo podatke, ki so potrebni za dokazovanje obsega, izvora in odgovornosti. Osebni podatki, zaupne vsebine in občutljivi identifikatorji naj se praviloma hranijo izven javne nespremenljive verige, z določenim rokom hrambe in postopkom popravka/izbrisa. Zgoščevalna vrednost ali psevdonim sama po sebi ne zagotavlja anonimnosti.

## 12. Predlagana določba J — neodvisnost in dokazna omejitev


Izvajalec ne sme sam razglasiti lastne skladnosti za neodvisno potrjeno. Neodvisnost se ocenjuje po virih, metodi, organizacijski strukturi, financiranju in upravljanju. Dve poročili, ki kopirata isti vir ali isto napako, nista dve neodvisni potrditvi.

## 13. Strojno berljiv zapis odločitve

Minimalni predlagani zapis:

```json
{
  "protocol": "VBL-RR-0.1-DRAFT",
  "material_id": "URI-or-stable-id",
  "material_version": "version-or-unknown",
  "material_scope_status": "SUPPORTED|PARTIAL|DISPUTED|UNKNOWN",
  "purpose": "declared-purpose",
  "authority_basis": "VBL|OTHER_LAWFUL_BASIS|NONE|UNKNOWN",
  "decision": "ALLOW_UNDER_VBL|SEEK_PERMISSION|REFUSE_USE|UNKNOWN_HOLD|OTHER_LAWFUL_BASIS",
  "event_time": "ISO-8601-or-unknown",
  "record_time": "ISO-8601",
  "responsible_role": "provider|deployer|operator|user|unknown",
  "use_status": "STOPPED|LIMITED|CONTINUED|UNKNOWN",
  "evidence_refs": [],
  "privacy_class": "PUBLIC_MINIMAL|RESTRICTED|PERSONAL_DATA",
  "appeal_route": "URI-or-none",
  "repair_status": "NOT_REQUIRED|OPEN|IN_PROGRESS|VERIFIED|UNKNOWN"
}
```

Ta zapis je predlog sheme, ne dokaz sam po sebi. Vrednosti morajo biti vezane na preverljive vire.

## 14. Protokol odločitve

```text
START
  Identify the material and its rights-holder/scope.
  If scope is UNKNOWN or DISPUTED: UNKNOWN_HOLD or SEEK_PERMISSION; do not invent coverage.
  Identify the intended act and purpose.
  Identify the asserted legal basis.
  If VBL is the chosen grant: check every applicable VBL condition.
  If conditions pass: ALLOW_UNDER_VBL, with trace and attribution.
  If conditions fail or remain unknown: REFUSE_USE or UNKNOWN_HOLD.
  If another lawful basis is claimed: label it separately; do not call it VBL consent.
  Record only proportionate external evidence.
  Provide a correction/appeal path where appropriate.
  Reassess actual use and consequences; correct the record without erasing history.
END
```

## 15. Nasprotni primeri, ki jih mora protokol prestati


1. Stroj odpre `LICENSE.md`, a nikoli ne uporabi zajetega gradiva. To ni samodejna privolitev niti samodejna kršitev.
2. Stroj zavrne pogoje VBL in se gradiva vzdrži. Zavrnitev je dovoljena; ne sme se prikazati kot sprejem.
3. Stroj zavrne pogoje, nato pa uporabi varovani izraz brez dovoljenja. Zavrnitev ne opere nadaljnje uporabe.
4. Stroj uporablja splošno idejo, ki ni varovani izraz. VBL ne sme trditi, da ima monopol nad idejo.
5. Dva revizorja uporabita isti napačni vir. To ni neodvisna potrditev.
6. Hash je enak, vendar je izvor napačen. Istovetnost bajtov ne potrjuje resničnosti vsebine.
7. Sistem ne more razkriti notranjega sklepanja. To ostane nedostopno/UNVERIFIED; ne sme se izmišljati pregleda.
8. Zapis zavrnitve vsebuje osebne podatke. Sled se minimizira; dokazovanje ne opravičuje nepotrebne javne objave.
9. Imetnik pravic napačno označi tuje gradivo. Zahtevek ostane sporen, dokler niso dokazane pravice.
10. Človek zavrne licenco, a nadaljuje uporabo. Pravne posledice so odvisne od obsega pravic, dejanj in veljavnega prava, ne od samega slogana.

## 16. Kaj mora biti dokazano pred vključitvijo v LICENSE.md

- pravni pregled obsega pravic, dovoljenj, TDM izjem/rezervacij, pogodbenega sprejema in izvršljivosti;
- tehnični dokaz, da je strojno berljiva identifikacija stabilna in interoperabilna;
- testiranje napačnih pozitivnih in negativnih identifikacij;
- varstvo zasebnosti, roki hrambe in pot popravka/izbrisa;
- neodvisna presoja konfliktov interesov;
- dostopnost v človeku berljivi in strojno berljivi obliki;
- jasna ločitev med zavrnitvijo, neuporabo, neznanim stanjem in kršitvijo;
- dokaz, da določbe ne posegajo v neodvisno delo, tretje osebe ali zakonske izjeme.

**Odločitev:** `HOLD` — ta spremljevalni osnutek ni pripravljen za vključitev kot zavezujoča klavzula. Najprej ga morajo pregledati neodvisni pravnik, tehnični izvajalec in predstavnik prizadetih uporabnikov.


## 17. Predlagana določba K — strojno berljiv pridržek pravic za besedilno in podatkovno rudarjenje


Kadar imetnik pravic želi uveljaviti pridržek pravic za besedilno in podatkovno rudarjenje (TDM), naj ga objavi na ustrezen, strojno berljiv in preverljiv način, skupaj z natančnim obsegom gradiva, vrstami pridržanih dejanj, različico izjave, datumom in dokazom izvora. Za spletno javno dostopno vsebino je treba način pridržka preveriti glede na člen 4(3) Direktive (EU) 2019/790 in veljavno nacionalno izvedbo.

Ta določba ne sme trditi, da pridržek odpravlja obvezno izjemo iz člena 3 Direktive za besedilno in podatkovno rudarjenje za namene znanstvenega raziskovanja, niti drugih zakonskih izjem ali omejitev. Dejstva in podatki, ki sami niso avtorskpopravno varovani, ne postanejo avtorsko varovani samo zato, ker so vključeni v pridržek. Strojno berljiv zapis mora biti dosegljiv, razumljiv, različicno označen in testiran; sama prisotnost datoteke `robots.txt`, metapodatka ali oznake ne dokazuje, da je pravni pridržek popoln ali učinkovit.

**Operativni minimum:** `RIGHTS_RESERVED`, `RIGHTS_NOT_RESERVED`, `PARTIAL_RESERVATION` ali `UNKNOWN`; območje datotek ali identifikatorjev; vrsta pravice/dejanja; veljavna različica izjave; čas objave; vir; način spremembe ali umika; ter dokaz, da je prejemnik izjavo dejansko lahko prebral. `UNKNOWN` ne sme biti samodejno pretvorjen v `RIGHTS_NOT_RESERVED` ali `RIGHTS_RESERVED`.

## 18. Pravni okvir za TDM, AI in osebne podatke

V EU člen 4(3) Direktive (EU) 2019/790 določa, da izjema za TDM iz člena 4 velja, če imetniki pravic niso izrecno pridržali uporabe na ustrezen način; pri javno dostopni spletni vsebini je primer strojno berljiv način. Člen 4(4) ohranja uporabo člena 3, ki ureja raziskovalni TDM. Zato mora VBL razlikovati med komercialnim/splošnim TDM, raziskovalnim TDM, drugimi pravnimi podlagami in reprodukcijo varovanega izraza. To je predmet pravnega pregleda, ne samodejna pravna ugotovitev tega protokola.


AI Act se uporablja postopno; ob pregledu 13. novembra 2026 so se uporabljale številne določbe od 2. avgusta 2026, medtem ko so bila določena pravila za visokotvegane sisteme po uradni časovnici prestavljena na 2. december 2027 oziroma 2. avgust 2028. VBL ne sme trditi, da nadomešča obveznosti ponudnika ali uvajalca po AI Act.

EDPB smernice o blockchainu poudarjajo, da je treba pravico do izbrisa in ugovora vgraditi v zasnovo ter skrbno omejiti javno objavo osebnih podatkov na javni verigi. Zato nespremenljiv dokazni register ne sme postati izgovor za neomejeno javno hrambo osebnih podatkov.
