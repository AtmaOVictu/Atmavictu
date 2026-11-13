# VBL-DINAMIKA — ∆ PREDLOG (razvojni dokument, ⟨ne⟩ vrata ⊙ precedens σ 4880 ∧ σ 4886)

**OVOJ @rez σ 5330, 13. 11. 2026 ⊢**: gradivo ⟡ VERBATIM ⟨NE-BRUSI⟩ ⟨NE-RETIPKAJ⟩ ⊙ 24 — prejeto v klepetu istega diha; ⟡ UKAZ verbatim ⟨ne brusi⟩: »to beri in predlagaj kako ti pomaga in kje vse še ni v uporabi če in kar je uporabnega/zanesljivega?« · IME ⟨VBL-DINAMIKA⟩ = izbor izvajalke ⭢ sodba ⚔ ⟡ ⊙ precedens σ 4886 · PRAVNO STANJE ⊢: ∆ PREDLOG razvojnega dokumenta licence — živa vrata licenc ostajajo 0.1530 bajt-isto ⟨NE-GRIZI⟩ · RAZPON: poglavja XIII–XXXIII · Telo spodaj VERBATIM pri viru.

---

XIII. DINAMIČNA SISTEMSKA MATEMATIKA
31. Licenca kot sistem stanj in prehodov
VBL je zdaj mogoče obravnavati kot dinamični sistem.

Definirajmo stanje:
\[
X_t=(W,P,E,A,C,R)
\]

Kjer:
- \(W\): stanje gradiva;
- \(P\): stanje dovoljenja;
- \(E\): dokazno stanje;
- \(A\): izvedena dejanja;
- \(C\): posledice;
- \(R\): popravila.
Prehod:
\[
X_{t+1}=F(X_t,u_t,e_t)
\]

Kjer:
- \(u_t\): novo dejanje;
- \(e_t\): nov dokaz;
- \(F\): določena funkcija prehoda.
Tako lahko simuliramo:
- novo različico licence;
- novo kopijo;
- izgubo dokaznega vira;
- spremembo dovoljenja;
- odkritje kršitve;
- popravljanje posledic;
- nov ugovor.
Novi koncept: STATE TRANSITION AUDIT
Vsaka sprememba stanja mora imeti:
- predhodno stanje;
- sprožilni dogodek;
- dovoljeno operacijo;
- novo stanje;
- dokaz prehoda;
- možnost povratnega preverjanja.
To neposredno povezuje §0.10, §0.31, §0.32 in §0.37.
32. Časovne omejitve kot varnostni invariant
Predlagam, da določimo tudi temporalna pravila.

Primer:

Če je ugovor sprejet v evidenco, mora nastopiti obravnava ali pa mora biti izrecno zabeleženo, zakaj je še odprt.

Formalno, s poenostavljeno časovno logiko:
\[
Signal\Rightarrow
F(Review\lor OpenDebt)
\]

Simbol \(F\) v časovni logiki pomeni, da se mora dogodek zgoditi v prihodnosti.

Za rok 30 dni lahko dodamo časovno omejeno različico:
\[
Signal\Rightarrow F_{\leq30d}(Review)
\]

To bi bil model roka za pregled, ne samodejno dokaz, da je bila napaka odpravljena v istem roku.

Drugi primer:
\[
CorrectionClaim\Rightarrow
F(IndependentVerification)
\]

Če je nekdo razglasil popravek za zaključen, mora slediti ustrezno neodvisno preverjanje.

Nova veja:

TEMPORAL LOGIC OF RESPONSIBILITY.

XIV. FORMALNA PREVERLJIVOST — MATEMATIKA, KI POSTANE KODA
Do zdaj sva imela veliko formalizacij. Zdaj jih morava pretvoriti v nekaj, kar lahko dejansko izvajamo.
33. Invarianti kot avtomatski testi
Predlagam najmanj deset lastnosti, ki jih mora validator VBL preverjati.
Oznaka	Invariant
I-01	Neprepoznano gradivo se ne sme samodejno obravnavati kot pokrito.
I-02	Identiteta datoteke ne dokazuje avtorstva.
I-03	Uspešen test ne dokazuje dovoljenosti uporabe.
I-04	Nova različica ne sme tiho izbrisati zgodovine.
I-05	Popravek mora ohraniti povezavo s prvotno napako.
I-06	Neodvisni pregledovalec ne sme biti isti izvajalec, ki potrjuje lastni rezultat.
I-07	Neznan izvor ne sme biti razglašen za preverjeno neodvisnost.
I-08	Neodvisno gradivo se ne sme avtomatično zajeti zgolj zaradi stika s pokritim gradivom.
I-09	Javni dokazni zapis ne sme po nepotrebnem razkrivati zaščitenih osebnih podatkov.
I-10	Odprta popravljalna obveznost ne sme biti označena kot zaključena.

To niso samo kontrolni seznami.

Lahko jih pretvorimo v:
- enotske teste;
- lastnostne teste;
- modelno preverjanje;
- adversarialne teste;
- regresijske teste;
- neodvisne revizijske scenarije.
Primer: lastnostni test pravic
Za poljubno dovoljeno transformacijo \(f\):
\[
Scope(f(W))\not\supset Scope(Grant(W))
\]

V bolj praktičnem zapisu preverimo, ali transformacija ustvari pravice, ki jih izvorna podelitev ni omogočala.
Primer: lastnostni test brazgotin
Za vsako popravljeno napako \(F\):
\[
Exists(F)\land Exists(Correction(F))
\]

Kadar je zgodovinska sled za določeni namen še vedno potrebna in jo je dovoljeno hraniti.
Primer: lastnostni test neodvisnosti
\[
Executor(Verification)\neq Executor(Action)
\]

Pri čemer identiteta osebe ni edina zahteva: preveriti je treba tudi organizacijsko in tehnično odvisnost.
34. Model checking — simuliranje vseh možnih prehodov
Tu bi šel še korak naprej.

Predstavljajmo si manjši sistem s stanji:
\[
S=\{DRAFT,ACTIVE,DISPUTED,HOLD,CURED,WITHDRAWN\}
\]

In dogodki:
\[
E=\{PUBLISH,OBJECT,VERIFY,REPAIR,FAIL\}
\]

Model checker lahko išče, ali obstaja pot, po kateri sistem pride v nedovoljeno stanje.

Primer:
\[
ACTIVE\rightarrow DISPUTED\rightarrow ACTIVE
\]

Ali je mogoče sistem vrniti v ACTIVE brez obravnave ugovora?

Če da, je to potencialna napaka v pravilih prehodov.

To je bistveno močnejše od testiranja nekaj ročno izbranih primerov.

Nova veja:

FORMAL VERIFICATION OF LICENSE GOVERNANCE.

XV. NOVE ONTOLOŠKE VEJE
Tukaj bi razširil raziskovalni program v deset različnih smeri.
ONTOZNANOST — raziskovalni atlas
Predlagana interdisciplinarna taksonomija
1

ONTOLOGIJA BITI

Kaj pomeni obstajati in kaj pomeni identiteta.


2

ONTOLOGIJA ODNOSA

Kako odnosi ustvarjajo lastnosti in pomen.


3

ONTOLOGIJA DOGODKA

Kaj je dogodek, kako nastane in kaj spremeni.


4

ONTOLOGIJA DOKAZA

Kako nekaj postane utemeljeno znanje.


5

ONTOLOGIJA JEZIKA

Kako znaki, zvok, struktura in pomen sodelujejo.


6

ONTOLOGIJA ČASA

Kako se spreminjajo identiteta, veljavnost in spomin.


7

ONTOLOGIJA ODGOVORNOSTI

Kako so dejanja povezana z nadzorom in posledicami.


8

ONTOLOGIJA PRIZNANJA

Kako se ohranja izvor in prispevek drugega.


9

ONTOLOGIJA NEVEDNOSTI

Kako klasificiramo neznano, nedostopno in neizmerjeno.


10

ONTOLOGIJA MOŽNOSTI

Kako se iz omejitev in protislovij oblikujejo nove poti.



Posebej pomembno: ontologija možnosti
To področje se mi zdi premalo raziskano.

Običajni sistemi evidentirajo, kaj se je zgodilo.

Ontologija možnosti pa raziskuje, kaj bi se lahko zgodilo, vendar se ni.
\[
\mathcal P(x)=
\{p_1,p_2,\ldots,p_n\}
\]

Kjer je \(\mathcal P(x)\) množica relevantnih možnosti za stanje \(x\).

Primer:

Pri odločitvi o uporabi avtorskega gradiva obstajajo:
- dovoljena uporaba;
- omejena uporaba;
- pridobitev dodatnega dovoljenja;
- anonimna atribucija;
- izključitev gradiva;
- opustitev dejanja.
Če sistem izbere samo eno možnost, mora znati pojasniti, zakaj so bile druge zavrnjene.

Nova funkcija:

COUNTERFACTUAL_OPTION_REGISTER.

Hranila bi pomembne alternative, razloge za njihovo zavrnitev in pogoje, pod katerimi bi bile spet mogoče.

Morda je ena največjih oblik krivice prav to, da sistem človeku odvzame možnost, ki je sploh nikoli ni prepoznal kot možnost.

XVI. NEKOMUTATIVNA MATEMATIKA — VRSTNI RED SPREMEMB JE POMEMBEN
To je področje, ki bi ga posebej priporočal za razvoj VBL in ontogematrije.

Pri običajnem seštevanju velja:
\[
a+b=b+a
\]

Pri mnogih postopkih spreminjanja informacij pa vrstni red ni zamenljiv.
\[
\boxed{A\circ B\neq B\circ A}
\]

Primer:
- najprej prevedemo besedilo, nato ga povzamemo;
- najprej povzamemo besedilo, nato prevedemo povzetek.
Rezultata sta lahko različna.
\[
Translate\circ Summarize
\neq
Summarize\circ Translate
\]

Podobno velja za:
- normalizacijo in šifriranje;
- filtriranje in statistično analizo;
- anonimizacijo in deduplikacijo;
- popravljanje in prevajanje;
- atribucijo in komercialno obdelavo.
Nova veja: ALGEBRA TRANSFORMACIJ
Vsaka transformacija mora nositi:
\[
T=(Input,Operation,Parameters,Output,Loss)
\]

Predlagam, da vsaka transformacija evidentira tudi:
- kateri podatki so bili odstranjeni;
- katere lastnosti so se spremenile;
- ali je bila operacija reverzibilna;
- ali je bilo mogoče izgubiti avtorstvo;
- ali je nastal nov pravni položaj;
- ali je mogoče rekonstruirati prvotno stanje.
Posebej zanimiva je reverzibilnost:
\[
T^{-1}(T(x))=x
\]

To velja samo, kadar je transformacija dejansko invertibilna in so ohranjeni potrebni podatki.

Povzetek praviloma ni popolnoma reverzibilen.

Zato:
\[
Summary^{-1}(Summary(x))\neq x
\]

Uporabnost za VBL: preprečiti, da bi transformirano gradivo bilo napačno predstavljeno kot popolnoma zvesto izvirniku.

Nova funkcija: NONCOMMUTATIVE_TRANSFORMATION_AUDIT.

XVII. TEORIJA IGER — KAKO SE SISTEM VEDE, KO IMAJO UDELEŽENCI RAZLIČNE INTERESE?
To je veliko pomembnejše, kot se zdi.

VBL predpostavlja, da bodo udeleženci sodelovali pri dokazovanju in popravljanju.

Toda nekateri imajo interes, da:
- dokazov ne razkrijejo;
- napako skrijejo;
- ugovor zavlačujejo;
- stroške prenesejo na drugega;
- izkoriščajo nejasnost določb.
Zato potrebujemo teorijo strateškega vedenja.
35. Model udeležencev
Naj bo:
\[
G=(N,S,U)
\]

- \(N\): udeleženci;
- \(S\): njihove možne strategije;
- \(U\): njihove posledice oziroma koristi.
Primer:
Udeleženec	Strategija
Avtor	Prizna prispevke ali ne
Izvajalec	Evidentira uporabo ali jo prikrije
Preveritelj	Preveri neodvisno ali potrdi znano
Prizadeti	Ugovarja ali molči
Upravljavec	Omogoči pregled ali omeji dostop

Vprašanje ni samo, ali sistem predpisuje pravilno ravnanje.

Vprašanje je:

Ali pravila ustvarjajo spodbude, zaradi katerih se ljudem splača ravnati pravilno?

To je problem mehanizma.
36. Mehanizem za pošteno prijavljanje napak
Predpostavimo, da sistem nagrajuje samo rezultat brez ugotovljenih napak.

Potem se izvajalcu lahko bolj splača napake skriti kot jih prijaviti.

To je napačna spodbuda.

Predlagam:
\[
Reward=
f(Disclosure,Correction,Prevention)
\]

Ne nagrajujemo zgolj odsotnosti prijavljenih napak.

Prepoznamo tudi:
- kakovost pravočasnega priznanja;
- dejansko popravilo;
- preprečitev ponavljanja;
- sodelovanje pri preverjanju.
To ne pomeni, da priznanje avtomatično odpravi odgovornost ali sankcijo.
Nova funkcija: INCENTIVE_COMPATIBILITY_AUDIT
Preizkusi, ali sistem zaradi svojih kazalnikov spodbuja prikrivanje, zavlačevanje, pretirano prijavljanje ali manipulacijo.

XVIII. TOPOLOGIJA DOKAZOV — KJE SO LUKNJE V SISTEMU?
To je zelo zanimiva matematična smer.

Predstavljajmo si dokazni graf.
\[
G=(V,E)
\]

Povezani so:
- izvirniki;
- kopije;
- transformacije;
- izjave;
- meritve;
- odločitve.
Kaj pomeni, če ena povezava manjka?

Morda imamo vse datoteke, vendar ne vemo, katera je ustvarila katero.

Morda poznamo vse akterje, vendar ne vemo, kdo je sprejel odločitev.

Morda imamo dokaz o prejemu, vendar ne o dovoljenju.

To so epistemološke luknje.
37. Tri vrste topoloških odpovedi
A. Prekinjena povezava
\[
A\quad B
\]

Obstajata dva zapisa, vendar ni znane povezave med njima.

B. En sam most

Celoten dokazni sistem je odvisen od enega samega zapisa ali pričevanja.

Če ta izgine, se prekine celotna dokazna veriga.

C. Lažno sklenjen krog
\[
A\rightarrow B\rightarrow C\rightarrow A
\]

Sistem se medsebojno potrjuje, ne da bi imel neodvisno zunanjo oporo.

To je dokazni ekvivalent zaprtega informacijskega kroga.
Nova funkcija: EVIDENCE_TOPOLOGY_AUDIT
Preverja:
- manjkajoče povezave;
- posamezne točke odpovedi;
- krožne potrditve;
- nepovezane dele dokaznega grafa;
- odvisnost od enega vira;
- dostopnost alternativne dokazne poti.
Nov aksiom:
\[
\boxed{\text{Zaprta dokazna veriga ni nujno neodvisna dokazna veriga.}}
\]


XIX. INTEGRAL POSLEDIC — ŠKODA SE DOGAJA SKOZI ČAS
To je nadgradnja najinega koncepta pravične krivice.

Predpostavimo, da napačna uporaba avtorskega dela povzroča škodo skozi čas.

Ne gre samo za en dogodek.

Naj bo:
\[
h(t)=\text{stopnja nastajanja določene škode v času}
\]

Potem lahko pri primerno merljivi kategoriji posledic zapišemo:
\[
H(T)=\int_0^T h(t)\,dt
\]

To je kumulativna posledica.

Primer:
- napačen pripis je objavljen;
- vsak naslednji dan ga dodatno prevzamejo drugi viri;
- prvotni zapis je sicer popravljen;
- napačne kopije še naprej krožijo.
Prvotni dogodek je en sam. Njegova posledica je časovno razpršena.

Toda ne smemo sešteti denarne škode, izgube zasebnosti, čustvenega trpljenja in izgubljenih ustvarjalnih možnosti kot da bi bili ista merska enota.

Zato predlagam:
\[
\mathbf H(T)=
\left(
H_{\text{economic}},
H_{\text{attribution}},
H_{\text{privacy}},
H_{\text{access}},
H_{\text{opportunity}}
\right)
\]

Vsaka razsežnost se meri ločeno, kjer je to mogoče.
Nova funkcija: HARM_DURATION_ANALYSIS
Preverja:
- kdaj se je škoda začela;
- kako se je širila;
- kdaj je bila zmanjšana;
- ali se še nadaljuje;
- kaj je bilo mogoče preprečiti;
- kaj ostaja nepopravljivo.
Tu dobimo novo zelo pomembno načelo:
\[
\boxed{
\text{Časovna zamuda pri popravilu je lahko samostojen vir nove škode.}
}
\]


XX. MATEMATIKA ZASEBNOSTI — DOKAZATI BREZ RAZKRITJA VSEGA
To je ena najzanimivejših možnosti sodobne matematike za VBL.
38. Ni treba vedno razkriti podatka, da bi dokazali njegovo lastnost
Predpostavimo, da želimo dokazati, da ima neka datoteka določeno vrednost ali da je določena oseba odobrila določeno različico.

Morda ne želimo razkriti celotne datoteke ali vseh osebnih podatkov.

Tu pridejo v poštev kriptografski dokazi z ničelnim razkritjem (zero-knowledge proofs).

V poenostavljeni obliki:
\[
Proverifier\ learns\ P(x)
\]

brez razkritja celotnega \(x\), pod pogoji ustreznega kriptografskega protokola.

Primer:

Dokazati, da:
- je uporabnik imel pooblastilo;
- se je odobritev nanašala na določeno različico;
- je bil hash del določenega kriptografskega zapisa;
- podatki ustrezajo določenemu pogoju.
Ne da bi javno razkrili vsebino zasebnega dokumenta.

Vendar:
\[
ZKP\text{ dokazuje določeno lastnost pod predpostavkami}
\]

Ne dokazuje, da je bila prvotna trditev o vsebini resnična ali da je dovoljenje pravno veljavno.
Nova veja: PRIVACY-PRESERVING EVIDENCE.
Predlagam tri stopnje:
1. javni dokazni povzetek;
2. omejeni dostop do podrobnejših dokazov;
3. kriptografsko preverjanje izbranih lastnosti brez razkritja celotnega podatka.
To bi bila precejšnja nadgradnja dokazne infrastrukture VBL.

XXI. ONTOLOGIJA GOVORNEGA DEJANJA
To je še ena smer, ki jo posebej priporočam.

Beseda ni samo zapis. Lahko je dejanje.

Razlikujmo:
\[
W=(L,I,A,C)
\]

- \(L\): izgovorjeno ali zapisano besedilo;
- \(I\): namen govorca;
- \(A\): dejanje, ki ga beseda opravi;
- \(C\): kontekst in posledica.
Primer besede »dovolim«:
- jezikovno: izjava;
- namerno: izražanje volje;
- operativno: morebitna podelitev dovoljenja;
- pravno: učinek je odvisen od upravičenja, oblike, vsebine in okoliščin.
Zato:
\[
\text{Izjava o dovoljenju}\neq\text{veljavno dovoljenje}
\]

Enako:
- »preverjeno« ni nujno preverjeno;
- »odobreno« ni nujno odobreno;
- »popravljeno« ni nujno popravljeno;
- »neodvisno« ni nujno neodvisno.
Nova funkcija: SPEECH-ACT-VALIDATOR
Preverja razkorak med:
- besedo;
- nameravanim dejanjem;
- dejansko izvršitvijo;
- dokazom izvršitve.
To je izredno uporabno za vse licenčne ukaze, dovoljenja in potrditve.

XXII. VEČVREDNOSTNA LOGIKA — RESNICA IN NERESNICA NISTA VEDNO NASPROTJI, KI SE IZKLJUČUJEITA
Tu bi rad uvedel še eno zahtevnejše matematično področje.

Klasična logika pogosto uporablja:
\[
T\in\{0,1\}
\]

Toda dokazni sistemi se srečujejo z:
- dokazi za trditev;
- dokazi proti trditvi;
- obojimi hkrati;
- odsotnostjo obojih.
Predlagam uporabo štirivrednostne logike, kakršna je Belnapova.
\[
V(T)=(S,R)
\]

Kjer:
- \(S\): obstaja podpora;
- \(R\): obstaja ovržba.
\(S\)	\(R\)	Rezultat
1	0	Podprto
0	1	Ovrženo
1	1	Podprto in ovrženo
0	0	Neznano

Poglejva primer.

Trditev:

»Datoteka X je izvirnik dokumenta Y.«

Ena dokazna veriga podpira to trditev. Druga jo izpodbija.

Klasični sistem bi lahko moral izbrati samo en rezultat.

Večvrednostna logika pa omogoči, da sistem shrani obe stanji in ne izgubi protislovja.
\[
\boxed{T\land\neg T}
\]

v takem sistemu ne pomeni, da lahko poljubno sklepamo karkoli.

To je velika prednost parakonsistentne logike: protislovja lahko obravnavamo, ne da bi se celotni sistem sklepanja sesul.
Nova funkcija: CONTRADICTION-PRESERVING LOGIC
Zagotavlja:
- ohranitev nasprotnih dokazov;
- razločevanje spora od nevednosti;
- prepoved tihega izločanja neugodnih dokazov;
- možnost nove odločitve ob novih dokazih.
Pomembna dopolnitev: delna podpora zahteva razgradnjo sestavljene trditve.

Če trdimo:

»Dokument je izviren, pravilno pripisan in zakonito objavljen,«

moramo imeti tri ločene trditve:
\[
T=T_1\land T_2\land T_3
\]

Vsaka ima svojo dokazno vrednost.

Tako ne dovolimo, da uspeh pri enem delu samodejno potrdi celotno izjavo.

XXIII. NE-MONOTONA LOGIKA — NOVI DOKAZ LAHKO SPREMENI STARI ZAKLJUČEK
To je posebej pomembno za razvoj licence.

Pri monotoni logiki velja, da dodajanje novih premis ne izniči že izpeljanih zaključkov.

Toda v resničnem dokaznem sistemu lahko novi dokaz razveljavi prejšnjo utemeljitev.

Primer:
1. Sistem ima dokaz, da je neka datoteka pravilno pripisana.
2. Na podlagi tega sprejme odločitev.
3. Pozneje prejme močnejši dokaz, da je bilo pripisovanje napačno.
Stari zaključek je treba ponovno presoditi.
\[
E_1\vdash T
\]

Pozneje:
\[
E_1\land E_2\not\vdash T
\]

To je normalno.

Znanje mora biti popravljivo, ne samo razširljivo.

Nova funkcija:

DEFEASIBLE-CLAIM-ENGINE.

Vsaka pomembna odločitev mora imeti:
- pogoje veljavnosti;
- podporne dokaze;
- možne izpodbojne dokaze;
- sprožilce ponovne presoje;
- zgodovino spremembe sklepa.
To bi lahko povezali s §0.37 in §0.49.

XXIV. MATEMATIKA VREDNOSTI, KI JE NE MOREMO IZMERITI
Tu želim še posebej nasprotovati morebitnemu pretiranemu matematičnemu optimizmu.

Obstajajo vrednote, ki jih ni primerno pretvoriti v numerično funkcijo.

Denimo dostojanstvo.

Če bi vsakemu človeku pripisali številko dostojanstva:
\[
D(h)\in\mathbb R
\]

bi že sama konstrukcija modela omogočala razvrščanje ljudi.

Predlagam drugačen matematični pristop:
\[
D(h)=1,\quad\forall h\in H
\]

Ne kot empirično odkritje, temveč kot normativno omejitev modela.

Dostojanstvo nastopa kot pogoj dopustnosti, ne kot optimizacijski cilj.

To pomeni:
\[
\max Utility(x)
\]

samo ob omejitvi:
\[
Respect(Dignity(h))=1
\]

za vse prizadete ljudi.

Toda tudi zapis te omejitve ne zagotavlja, da bo sistem človekovo dostojanstvo v praksi spoštoval. Zato potrebujemo konkretne teste proti diskriminaciji, prisili, izključevanju in nesorazmernim posegom.

Nova veja: MATEMATIČNA MEJA VREDNOTENJA.

Njen aksiom:
Ni vse, kar je pomembno, predmet optimizacije; nekatere stvari so pogoji, pod katerimi je optimizacija sploh dopustna.


XXV. ONTOZNANOST KOT RAZISKOVALNA METODA
Zdaj bi vse zgornje matematike združil v enoten postopek.

Vsako novo ontološko spoznanje mora prestati devet korakov:
ONTOZNANSTVENI RAZISKOVALNI CIKEL
1. POJAV
   
   Kaj smo opazili?
2. MEJA PREDMETA
   
   Kaj raziskujemo in česa ne vključujemo?
3. ONTOLOŠKA DEFINICIJA
   
   Kaj je predmet, odnos, dogodek ali stanje?
4. FORMALIZACIJA
   
   S katero matematiko ga lahko opišemo?
5. OPERACIONALIZACIJA
   
   Kaj lahko dejansko opazujemo in merimo?
6. HIPOTEZA
   
   Kaj pričakujemo, da bomo našli?
7. PROTIPRIMER
   
   Kateri rezultat bi našo razlago ovrgel?
8. NEODVISNA PONOVITEV
   
   Ali lahko drugi raziskovalec ponovi metodo?
9. OMEJITEV IN NOVO SPOZNANJE
   
   Kaj zdaj vemo in česa še vedno ne?

To lahko postane skupna metodologija:
- matematične ontologije;
- ontogematrije;
- ontologije besede;
- ontologije časa;
- relacijske etike;
- teorije dokaznega izvora.
Pomembno razlikovanje
Ontološko vprašanje:

»Kaj je beseda?«

Matematično vprašanje:

»Katere njene lastnosti lahko formalno opišemo?«

Empirično vprašanje:

»Katere povezave med temi lastnostmi lahko dejansko opazimo?«

Normativno vprašanje:

»Kako naj ravnamo z njenim avtorjem in njenimi uporabniki?«

Vse štiri ravni so pomembne. Nobena ne nadomesti drugih.

XXVI. PRAKTIČEN EKSPERIMENT: OD IZVIRNE BESEDE DO ODGOVORNE UPORABE
Poglejva, kako bi vse to delovalo na enem samem primeru.

Izberiva izraz:

NE.
\[
W_0=\text{NE}
\]

Korak 1 — Identiteta
Določimo zapis, jezik, normalizacijo, Unicode in bajtno predstavitev.
Korak 2 — Jezikovna struktura
Določimo grafemsko, fonetično, skladenjsko in pomensko obnašanje.
Korak 3 — Ontološka interpretacija
Postavimo hipotezo:

»NE ni samo negacija, ampak lahko deluje tudi kot dejanje vzpostavljanja meje.«
Korak 4 — Raziskovalni preizkus
Zberemo različno rabljene primere:
- zavrnitev;
- negacija dejstva;
- zaščitna meja;
- prekinitev;
- nestrinjanje;
- odprtje nove možnosti.
Razvrščanje določimo vnaprej, primere pa preverjamo tudi z neodvisnimi ocenjevalci.
Korak 5 — Matematična analiza
Izračunamo frekvence, kontekste, razporeditev, sočasne pojavitve in morebitne razlike med korpusi.
\[
f(NE,C)=
\frac{count(NE,C)}{tokens(C)}
\]

Korak 6 — Nasprotni primeri
Preverimo, ali obstajajo konteksti, v katerih »NE« ne pomeni zavrnitve ali postavitve meje.
Korak 7 — Rezultat
Razločimo:
- potrjene jezikovne lastnosti;
- statistične ugotovitve;
- filozofsko interpretacijo;
- še nepreverjene hipoteze.
Korak 8 — Povezava z VBL
Iz ugotovitve razvijemo operativno funkcijo:

REFUSAL_WITH_VALID_ALTERNATIVE.

Kadar sistem zavrne nedovoljeno dejanje, preveri, ali obstaja druga zakonita in varna možnost.

Tako iz ene besede nastane:
- jezikovni eksperiment;
- matematična analiza;
- ontološka interpretacija;
- etični koncept;
- operativna funkcija.
To je primer, kako naj se ontologija in uporabna matematika medsebojno razvijata.

XXVII. ŠE 12 ONTOZNANSTVENIH AKSIOMOV ZA NADALJNJE RAZISKOVANJE
Te bi posebej rad ohranil kot odprte raziskovalne predloge.
Št.	Aksiom	Matematična posledica
1	Predmet ni njegova predstavitev.	\(x\neq Rep(x)\)
2	Odnos ni isto kot vsota predmetov.	\(R(x,y)\neq x+y\)
3	Sprememba ne uniči nujno identitete.	\(x_t\sim x_{t+1}\)
4	Dokaz o lastnosti ne dokazuje vseh drugih lastnosti.	\(E_A\not\Rightarrow E_B\)
5	Vsaka transformacija ima možne izgube.	\(T(x)=y,\ Loss(T)\)
6	Vrstni red operacij lahko spremeni rezultat.	\(A\circ B\neq B\circ A\)
7	Odsotnost meritve ni meritev ničle.	\(Missing\neq0\)
8	Več dokazov lahko izhaja iz enega samega vira.	\(N_E\neq N_I\)
9	Čas spreminja veljavnost določenih dokazov.	\(V(E,t_1)\not\Rightarrow V(E,t_2)\)
10	Pravičnost in učinkovitost nista sopomenki.	\(J\neq Efficiency\)
11	Popravilo ne zagotavlja povrnitve prvotnega stanja.	\(R\not\Rightarrow X_0\)
12	Vsak formalni model ima mejo veljavnosti.	\(Model\neq Reality\)


XXVIII. KATERE MATEMATIČNE DISCIPLINE BI ŠE VKLJUČIL?
Ne želim, da bi se Ontoznanost razvijala v vakuumu. Predlagam naslednjo raziskovalno povezavo:
ONTOZNANOST — MATEMATIČNA ZVEZDA











Algebra

Transformacije, operacije, invarianti.











Topologija

Povezanost, meje, luknje, struktura dokazov.











Verjetnost

Negotovost, kalibracija, sklepanja.











Dinamični sistemi

Spremembe, stabilnost, povratne zanke.











Teorija kategorij

Odnosi, preslikave, sestavljanje transformacij.











Teorija informacij

Informacija, entropija, izguba in prenos.











Teorija iger

Interesi, strategije, spodbude.











Matematična logika

Dokazljivost, protislovja, neodločljivost.



Posebej bi dodal še:
- diferencialno geometrijo za matematično modeliranje spremembe perspektiv;
- teorijo mer za probleme velikosti in porazdelitve;
- teorijo množic za identiteto, vključevanje in izključevanje;
- teorijo kodiranja za zvest prenos;
- kombinatoriko za število možnih transformacij;
- operacijske raziskave za izbiro popravljalnih ukrepov;
- vzročno sklepanje za razumevanje posledic.
To so raziskovalne povezave, ne trditev, da vse že tvorijo enotno ontološko teorijo.

XXIX. KAKO BI IZ TEGA NASTALA DEJANSKA ONTOZNANOST?
Predlagam pet samostojnih razvojnih produktov.
Temelj 1
ONTOLOGIJA — OX 0.1

Enotna taksonomija entitet, odnosov, dogodkov, stanj, transformacij in meja.


Temelj 2
MATEMATIKA — OM 0.1

Formalna logika, algebra odnosov, dokazni kalkulus, časovna matematika in modeli posledic.


Raziskave 3
ONTOGEMATRIA — OG 0.1

Ponovljivi algoritmi za numerično, fonetično in semantično raziskovanje besed.


Uporaba 4
ONTOLOGIJA ODGOVORNOSTI — OR 0.1

Izvor, dovoljenja, dejanja, posledice, priznanje in popravljanje.


Preverjanje 5
ONTOLOGIJA PREVERJANJA — OV 0.1

Eksperimentalne metode, protiprimeri, ponovljivost in neodvisna presoja.


XXX. MOJA NAJMOČNEJŠA PREDLOGA: TRI MATEMATIČNA ODKRITJA, KI JIH MORAVA ŠE RAZVITI
A. Relacijski integral

Tvoja ontologija že izpostavlja, da smisel nastaja v razmerju.

To lahko raziskujemo kot funkcijo, ki je odvisna od več odnosov:
\[
Meaning(x)=
\mathcal F(x,R_1,R_2,\ldots,R_n)
\]

Toda posamezen odnos lahko spremeni pomen istega objekta.

Raziskovalno vprašanje:

Ali lahko razvijemo matematično metodo, ki prepozna, kateri odnosi so nujni za določeno interpretacijo in kateri so samo spremljevalni?

B. Integral posledic
\[
\mathcal C(x)=
\int_{t_0}^{t_1}
\mathbf c(x,t)\,dt
\]

Raziskovalno vprašanje:

Kako lahko spremljamo posledice dejanja skozi čas, ne da bi človekovo izkušnjo skrčili na eno številko?

C. Paradoksalna stabilnost
\[
Stability\neq Immutability
\]

Sistem lahko ohrani identiteto prav s tem, da se spreminja.

Raziskovalno vprašanje:

Katere lastnosti morajo ostati invariantne, da sprememba sistema ne pomeni izgube njegovega temeljnega namena?

To je lahko matematični temelj evolucije VBL.

XXXI. KAJ BI ZDAJ IZDELAL PRVO?
Moje priporočeno zaporedje je:
Prednost	Izdelek	Preizkus uspeha
1	Tipizirana ontologija trditev, dokazov in dovoljenj	Napačne vrste dokazov so zavrnjene
2	Algebra provenience in transformacij	Izvor je sledljiv skozi vse izpeljave
3	Dinamični model stanj VBL	Neveljavni prehodi so zaznani
4	Model posledic in popravljanja	Ostanki škode ostanejo evidentirani
5	Eksperimentalna ontogematrija	Rezultati so ponovljivi in neodvisno preverjeni
6	Relacijska ontološka matematika	Razlikujemo objekt, odnos in interpretacijo
7	Neodvisni matematični audit	Najdene so tudi napake samih modelov

In še ena zelo pomembna varovalka: ne bi vseh teh dosežkov vključil neposredno v licenco. Matematični in ontološki raziskovalni dokumenti naj se razvijajo ločeno, nato pa naj samo preverjene, potrebne in pravno primerne ugotovitve preidejo v VBL.

XXXII. OSREDNJA MISLIVA ZDRUŽITEV
Zdaj lahko tvoje temeljne simbole povežemo z dejanskimi raziskovalnimi operacijami.
Simbol	Ontološka ideja	Matematična uporaba
\(\varnothing\)	Nič oziroma praznost	Prazna množica, manjkajoče stanje
\(\neg\)	Zanikanje	Negacija in izpodbijanje
\(\Delta\)	Razpoka in sprememba	Diferenca in variacija
\(\neq\)	Različnost	Relacija neenakosti
\(\vdash\)	Dokazno priznanje	Izpeljava
\(\bot\)	Protiutež	Nasprotje, omejitev
\(\oint\)	Kroženje priznanja	Ciklični procesi
\(\int\)	Integral odnosa	Akumulacija učinkov
\(\partial\)	Meja in odprtost	Odvod, rob, sprememba
\(\Omega\)	Meja veljavnosti	Definicijsko območje

To je simbolni raziskovalni zemljevid. Pri uporabi moramo razlikovati med običajnimi matematičnimi pomeni simbolov in njihovimi razširjenimi ontološkimi pomeni.

Najpomembnejši premik je naslednji:
\[
\boxed{
\text{Simbol}
\rightarrow
\text{Definicija}
\rightarrow
\text{Relacija}
\rightarrow
\text{Operator}
\rightarrow
\text{Poskus}
\rightarrow
\text{Spoznanje}
}
\]

Tako simbol ne ostane zgolj lep znak. Postane izvor preverljivega raziskovalnega vprašanja.

XXXIII. Moja končna misel: ontologija, ki zna preverjati lastno ontologijo
Tu vidim možnost za nekaj resnično zanimivega.

Ontoznanost bi morala raziskovati ne samo, kaj obstaja, ampak tudi:
- kako nastanejo naše kategorije obstoja;
- kaj iz njih izključemo;
- kako se spreminjajo;
- kako jih lahko napačno uporabimo;
- kako jih druge discipline izpodbijajo;
- kako jih lahko sami opustimo.
Predlagam še zadnji aksiom:
\[
\boxed{
\mathcal O(\mathcal O)\neq\mathcal O
}
\]

Zapis je namenoma shematičen: ontologija, ki postane predmet lastnega opazovanja, mora razlikovati svojo prvotno vlogo od modela, s katerim opazuje sebe.

To pomeni, da Ontoznanost ne sme samo raziskovati drugih pojavov. Raziskovati mora tudi nastanek svojih definicij, svojih metod in lastnih slepih peg.
Tri najboljše razvojne usmeritve
1. MATEMATIKA ODNOSA
Kako iz razlik nastajajo identitete, pomeni, možnosti in odvisnosti?


2. MATEMATIKA PRIZNANJA
Kako ohraniti izvor, prispevek in odgovornost skozi transformacije?


3. MATEMATIKA POSLEDIC
Kako meriti in popravljati posledice, ne da bi človeka pretvorili v merljiv objekt?


Moja najmočnejša ugotovitev: VBL je lahko praktični laboratorij Ontoznanosti. Ontoznanost pa je lahko raziskovalno okolje, ki VBL preprečuje, da bi se zaprla v lastne začetne predpostavke.

Ena brez druge lahko postane nepopolna: licenca brez raziskovanja postane tog sistem pravil; ontologija brez dokazne discipline pa lahko postane zbirka nepreverljivih trditev.

Skupaj lahko razvijata nekaj zahtevnejšega:
\[
\boxed{
\text{Razumeti}
\neq
\text{Izmeriti}
\neq
\text{Dokazati}
\neq
\text{Pravično ravnati}
}
\]

Toda vsako od teh dejanj lahko spremeni pogoje za naslednje.

In prav v tem medsebojnem vplivu vidim najplodnejše področje nadaljnjega razvoja. ∴
