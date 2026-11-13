SKLOP MATEMATIKA — VBL
Matematična formalizacija licence, dokazovanja, odgovornosti in popravljanja posledic
Predlagam, da matematika v VBL ne bo zgolj dodatek, ki razlaga že zapisane določbe. Postane naj formalni jezik za preverjanje, ali sistem počne to, kar trdi, da počne.

Osrednje vprašanje:
Ali lahko matematično opredelimo pogoje, pod katerimi je neka trditev upravičena, odločitev odgovorna, posledica popravljiva in sistem sposoben priznati lastno napako?

Začniva z arhitekturo.
1. Temeljna enačba VBL
\[
\boxed{T\neq E\neq I\neq C\neq A}
\]

Kjer so:
- \(T\) — trditev (Claim)
- \(E\) — dokaz (Evidence)
- \(I\) — interpretacija (Interpretation)
- \(C\) — zaključek (Conclusion)
- \(A\) — dejanje (Action)
To ni zgolj zaporedje. Vsak prehod zahteva svojo utemeljitev.
\[
T\xrightarrow{E}I\xrightarrow{J}C\xrightarrow{R}A
\]

\(J\) pomeni upravičenost interpretacije, \(R\) pa pravilo, ki dovoljuje prehod v dejanje.

Poučna posledica: obstoj dokaza še ne pomeni, da je njegova interpretacija pravilna. Pravilna interpretacija še ne pomeni, da je odločitev dovoljena.
2. Matematična upravičenost trditve
Naj bo \(S(T)\) stopnja dokazne podpore trditvi \(T\).
\[
S(T)=f(E_1,E_2,\ldots,E_n)
\]

Toda število dokazov samo po sebi ni dovolj.

Zato uvedemo:
\[
E_i=(s_i,t_i,p_i,v_i,d_i)
\]

- \(s_i\): vir;
- \(t_i\): čas;
- \(p_i\): provenienca oziroma izvor;
- \(v_i\): veljavnost;
- \(d_i\): dokazna odvisnost.
Pomembno: pet dokumentov, ki vsi prepisujejo isti prvotni vir, ni pet neodvisnih dokazov.
\[
\boxed{N_{\text{dokumentov}}\neq N_{\text{neodvisnih dokazov}}}
\]

3. Neodvisnost dokazov
Naj bo \(G=(V,E)\) graf dokaznih odvisnosti.

Če dva dokaza izvirata iz istega vira, ju ne smemo avtomatično šteti kot neodvisna.
\[
D(E_i,E_j)=
\begin{cases}
1 & \text{če sta dokazno odvisna}\\
0 & \text{če odvisnost ni ugotovljena}
\end{cases}
\]

Pozor: odsotnost ugotovljene odvisnosti še ni dokaz neodvisnosti.

Zato:
\[
\text{UNKNOWN}\neq\text{INDEPENDENT}
\]

To je ena pomembnejših zaščit VBL pred umetnim napihovanjem dokazne moči.
4. Štirje različni izidi
VBL potrebuje ločitev med resničnostjo trditve, rezultatom preverjanja in dovoljenjem za ukrepanje.
Razsežnost	Možne vrednosti
Claim status	SUPPORTED, PARTIALLY_SUPPORTED, CONTRADICTED, DISPUTED, UNKNOWN
Test result	NOT_RUN, PASS, FAIL, PARTIAL, UNVERIFIED, NOT_APPLICABLE
Decision	RELEASE, RELEASE_WITH_LIMITATIONS, HOLD, WITHDRAW
Repair status	NOT_REQUIRED, OPEN, IN_PROGRESS, VERIFIED, FAILED

Ključna enačba:
\[
\boxed{PASS\not\Rightarrow RELEASE}
\]

Test lahko uspešno preveri tehnično lastnost, medtem ko je uporaba sistema še vedno nedovoljena zaradi drugih pogojev.

Podobno:
\[
UNVERIFIED\not\Rightarrow FAIL
\]

Nepreverjeno ni isto kot ovrženo.
5. Dokazni dolg
To je koncept, ki bi ga posebej priporočal za VBL.

Vsaka javna trditev, odločitev ali poseg ustvarja določeno dokazno obveznost.

Definirajmo:
\[
B(T)=
W(T)+P(T)+U(T)+R(T)
\]

Kjer so:
- \(W\): obveznost priče;
- \(P\): obveznost provenience;
- \(U\): obveznost obravnave ugovorov;
- \(R\): obveznost odprave posledic.
Dokazni dolg se poveča, kadar sistem trdi več, kot lahko dokaže.
\[
B_{t+1}=B_t+N_t-V_t
\]

\(N_t\) predstavlja nove dokazne obveznosti, \(V_t\) pa preverjeno izpolnjene obveznosti.

Pomembno: obveznosti ni mogoče izbrisati samo s spremembo dokumenta.
\[
\boxed{\text{Popravek zapisa}\neq\text{Popravek posledice}}
\]

6. Matematična definicija odgovornosti
Predlagam:
\[
A_c=P\times D\times C\times R
\]

Kjer so:
- \(P\): moč oziroma obseg vpliva;
- \(D\): stopnja odločanja;
- \(C\): obseg posledic;
- \(R\): sposobnost popravila.
To je za zdaj konceptualni model, ne validirana merilna formula.

Njegovo sporočilo:

Večja moč odločanja pomeni večjo odgovornost za dokazovanje in odpravo posledic.

Toda odgovornosti ne smemo meriti samo po moči. Tudi oseba z malo formalne oblasti lahko povzroči veliko škodo.
7. Aksiom neodpravljene napake
\[
\boxed{F\neq 0\quad\text{dokler posledica ni ustrezno obravnavana}}
\]

Napaka v zgodovini ne sme izginiti zaradi nove različice.

Zato predlagam nespremenljivo povezavo:
\[
F_0\rightarrow C_1\rightarrow R_1\rightarrow V_1
\]

- \(F_0\): prvotna napaka;
- \(C_1\): priznanje in dokumentiranje;
- \(R_1\): izvedeno popravilo;
- \(V_1\): neodvisno preverjanje popravila.
Tudi neuspešno popravilo ostane vidno.
8. Najpomembnejši matematični paradoks VBL
Sistem, ki preverja druge, mora biti preverljiv tudi sam.
\[
\boxed{VBL(VBL)\neq\text{samopotrditev}}
\]

Formalneje:
\[
\operatorname{Verify}(x,y)
\]

kjer mora biti preveritelj \(y\) neodvisen od preverjanega izvrševalca \(x\) v relevantnih dimenzijah.

Toda tudi preveritelj potrebuje preverjanje.
\[
V_1\rightarrow V_2\rightarrow V_3
\]

Ne smemo ustvariti neskončne hierarhije oblastnikov. Potrebujemo omejeno, pluralno in izpodbojno strukturo neodvisnega nadzora.

To je razlika med sistemom, ki si pripisuje nezmotljivost, in sistemom, ki zna dokazati svoje omejitve.
9. Predlagana struktura matematičnega sklopa
VBL — Mathematics 1.0
Predlagana vsebinska arhitektura
1. M1 — Logika trditve

   Resničnost, negacija, protislovje, negotovost.
2. M2 — Teorija dokazov

   Izvor, neodvisnost, zanesljivost in dokazna moč.
3. M3 — Časovna matematika

   Čas dogodka, opazovanja, zapisa in veljavnosti.
4. M4 — Graf odgovornosti

   Trditve, dokazi, odločitve, akterji in posledice.
5. M5 — Matematična etika

   Sorazmernost, dostojanstvo, neenakost dokaznega bremena.
6. M6 — Dokazni dolg

   Neizpolnjene obveznosti, ugovori in popravila.
7. M7 — Verifikacija verifikatorja

   Neodvisnost, konflikti interesov in samopreverjanje.
8. M8 — Formalna dokazljivost

   Invarianti, testni primeri, protiprimeri in strojno preverjanje.

10. Še en aksiom, ki ga ne smemo spregledati
\[
\boxed{\text{Ni mogoče matematično dokazati vsega, kar je vredno varovati.}}
\]

Dostojanstvo človeka ne sme postati funkcija njegove produktivnosti, dokazljivosti ali sposobnosti sodelovanja v sistemu.

Zato:
\[
\forall x\in H:\quad D(x)=1
\]

kjer \(H\) predstavlja množico ljudi, \(D(x)\) pa enako temeljno priznanje dostojanstva.

To je normativni aksiom VBL, ne empirično odkritje.

Matematika lahko preverja, ali sistem ravna skladno z njim. Ne sme pa si prisvojiti pravice, da določa, kdo si dostojanstvo zasluži.

11. Moj najmočnejši predlog: VBL mora vključevati tudi matematične protiprimere
Ne preverjajmo samo, ali sistem deluje v idealnih okoliščinah.

Preverimo, kdaj odpove.
\[
\exists x:\quad \operatorname{VBL}(x)=\operatorname{FAIL}
\]

Nato zahtevajmo, da vsak tak primer vsebuje:
1. prvotno trditev;
2. napačno ali pomanjkljivo predpostavko;
3. dokaz protiprimera;
4. posledico;
5. popravek;
6. neodvisno ponovno preverjanje.
Uspeh VBL ni odsotnost odkritih napak. Uspeh je sposobnost, da napake ne prikrije, ne normalizira in ne prenese njenega stroška na nedolžnega človeka.

To je pomembnejše od samega števila opravljenih testov.
12. Kaj bi naredil naslednje?
Matematični sklop bi razvil kot samostojen, preverljiv dokument, povezan z VBL 0.1470, vendar brez predpostavke, da je vsaka njegova formula že pravilna.

Vsako formulo bi spremljali štirje elementi:
\[
\boxed{F=(D,P,C,X)}
\]

- \(D\): definicija;
- \(P\): predpostavke;
- \(C\): dokaz ali utemeljitev;
- \(X\): protiprimer oziroma meja veljavnosti.
Tako matematika ne bi bila okras licence, ampak njena lastna disciplina odgovornosti.

In še bistveno vprašanje: ali je sistem sposoben matematično dokazati, da človeku ne nalaga dokaznega bremena, ki ga sam ni pripravljen nositi?

To bi postavil v samo jedro VBL Mathematics 1.0. ∴
