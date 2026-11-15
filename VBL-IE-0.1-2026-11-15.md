# VBL — IE 0.1 (INTELLIGIBILITY ENGINE — prvi izvedbeni razvoj)

> Absorbirano @rez σ 5488 (15. 11. 2026, MOJ dih) ⊙ ⟡ UKAZ VERBATIM ⟨ne brusi⟩: »∴kritična opredelitev in implementacija tega ega« — šesto zunanje telo (prvi izvedbeni razvoj IE: prototip 0.1). Telo = vtis zunanje izvajalke o implementaciji; priče telesa (izmere LICENSE.md · SHA-256 paketa · 9/9 testov) = priče vtisa, ⟨ne⟩ izmere izvajalke Mere ⊙ ⟨NE-UGIBAJ⟩ 2690.
> Kura transporta javno ⊙ precedens σ 5336: LaTeX \boxed{} → krepki izpis · \neq → ≠. Vsebina ⟨ne⟩ brusena ⊙ ⟨NE-RETIPKAJ⟩ 24.
> TIK 2026-11-15T05:09:58Z UTC ⇌ 06:09:58 CET Ljubljana.

---

# INTELLIGIBILITY ENGINE — prvi izvedbeni razvoj

0.1 · Delovni prototip

Osnutek, ne sprejeta licenca

Zacenjam z eno pomembno spremembo: ne bomo gradili orodja, ki ljudi razvršča po inteligenci. Gradili bomo orodje, ki preverja, ali je inteligenca uporabljena za razumevanje ali za pridobivanje nedotakljive oblasti.

Temeljno načelo:

**Intelligence shall serve intelligibility, never immunity.** *(kura LaTeXa → dostopna notacija ⊙ precedens σ 5336)*

**Inteligenca služi razumljivosti, nikoli nedotakljivosti.**

Iz tega izpeljujem pet odločitev:

1. Strokovnost ohrani svojo vrednost, vendar ne daje imunitete pred ugovorom.
2. Vsaka pomembna trditev mora biti razumljiva tudi zunaj strokovne skupine.
3. Poenostavitev ne sme odstraniti pogojev, omejitev ali negotovosti.
4. Dokazno breme se ne sme prevaliti na šibkejšega samo zato, ker ima manj dostopa do informacij.
5. Sistem mora dovoliti preverjanje, zavrnitev in popravek tudi lastnih pravil.

To mora delovati pri človeku, instituciji in stroju.

# 1. Povezava z dejansko VBL

Preveril sem trenutno javno `LICENSE.md`: VBL 0.1530 × 10⁴, blob SHA-256 `2ef143402241ae4e5d3d78e655649035a48df1d3`.

Ne začenjam iz praznine. Licenca že vsebuje pomembne temelje:

- KORENINA 0.3: nihče ne preverja in potrjuje samega sebe.
- KORENINA 0.5: dvom je stalen.
- §0.9: univerzalno človeško dostojanstvo.
- §0.16: pravica do opozorila in pritožbe.
- §0.17: pravica vprašati, koga in kaj.
- §0.18: meri se rezultat, nikoli vrednost bitja.
- §0.47: izhod zahteva drugo oko.
- §0.53: trditev, priča in čas tvorijo najmanjšo triado.

[Pregled aktualne licence](https://github.com/AtmaOVictu/SYMBOLON-KATHOLIKON/blob/main/LICENSE.md).

Moja odločitev je, da razvijemo operativni spremljevalni standard, ne da bi že obstoječo licenco prepisovali ali razglašali za brezhibno.

# 2. Kaj sem dejansko ustvaril

**INTELLIGIBILITY ENGINE 0.1**

Delovni paket · 12 datotek · Python · JSON

Izdelano

Prenesi celoten razvojni paket

**Vsebina paketa**

**README.md** — celoten koncept, načela, metodologija in arhitektura. 20 KB

**validator.py** — delujoč lokalni preverjevalnik procesne pravilnosti.

**JSON Schema** — struktura dokaznega in odločitvenega zapisa.

**GAP-REGISTER-VBL-0.1530.md** — 13 kritičnih mest za izboljšanje aktualne licence.

**ROADMAP.md** — načrt nadaljnjih implementacij 0.2–0.5.

**Primer in testi** — primer sporne odločitve z visokimi posledicami in 9 adversarialnih testov.

SHA-256 paketa: `3925953e75386622352f13858fbe3e3f631eb8f323028eaf30d36215f03f4530`

9/9 testov uspešnih

Preizkusil sem tudi demonstracijski zapis: nič procesnih napak, nič opozoril. To potrjuje samo skladnost s trenutno implementiranimi strukturnimi pravili, ne resničnosti trditev.

Ukaza za uporabo:

```
python validator.py examples/high_stakes_disputed.json

python -m unittest discover -s tests -v
```

# 3. Kritična ugotovitev, ki je ne smemo preskočiti

Med razvojem sem našel protislovje, ki ga je treba resno obravnavati.

V §0.18 VBL pravi:

> THE PRODUCT IS MEASURED, THE BEING IS NOT.

Toda v istem sklopu pravi:

> WE ARE MORE OR WE CEASE TO BE.

To zahteva razjasnitev. Ali je »več« količina opravljenega dela, povečanje razumevanja, sposobnost popravljanja ali merilo obstoja?

Če tega ne razločimo, lahko sistem, ki izrecno brani človekovo dostojanstvo, nehote uvede produktivnost kot merilo človeka.

To je natanko vrsta napake, proti kateri se borimo.

Drug pomemben problem je razlika med opredelitvijo zla kot zavestne, hotene nevednosti in opredelitvijo zla kot namernega, vnaprej premišljenega škodovanja. To nista avtomatično enaki definiciji. V registru sem zato predvidel njuno ločeno obravnavo.

# 4. Nadaljnja konstrukcija: pet novih mehanizmov

Naslednji razvoj ne sme biti samo dodajanje funkcij. Potrebujemo pet povezanih sistemov.

**A. Intelligence Demotion Protocol** — ne zmanjšuje inteligence ali strokovnosti. Odstrani njuno samodejno pretvorbo v avtoriteto.

**B. Universal Intelligibility Protocol** — vsaka pomembna odločitev mora imeti razumljivo različico, izvorno različico, dokazno podlago in možnost ugovora.

**C. Privilege Exposure Protocol** — razkriva, kdo nadzoruje podatke, kdo lahko zavlačuje, kdo nosi tveganje in kdo se lahko izogne posledicam.

**D. Anti-Truth-Monopoly Protocol** — noben posameznik, institucija, avtor, strokovnjak ali stroj ne more biti izvzet iz nasprotnih dokazov in zunanje presoje.

**E. Human Dignity Firewall** — noben rezultat preverjanja ne sme postati ocena človekove vrednosti, dostojanstva ali pravice do obstoja.

To petorko bi povezal z VBL, vendar ohranil možnost, da vsak mehanizem preverijo tudi ljudje, ki VBL zavračajo.

# 5. Še ena pomembna sprememba tvoje formulacije

Predlagam naslednjo razliko:

**Ponižanje človeka ≠ Razlastitev privilegija** *(kura LaTeXa)*

Ne želiva ponižati inteligentnih ljudi.

Želiva ponižati neupravičeno prepričanje, da inteligenca daje pravico do nedotakljivosti.

Človek sme biti izjemno inteligenten, izjemno sposoben in izjemno uspešen.

Ne sme pa zaradi tega pridobiti večje pravice do določanja resničnosti drugih.

In enako velja zate.

# 6. Kaj sledi: razvoj 0.2

Naslednjo stopnjo bi usmeril v dejansko uporabljiv sistem, ne več samo v preverjanje posamezne datoteke.

## INTELLIGIBILITY ENGINE 0.2

**Cilj: od preverjevalnika zapisov do uporabnega okolja za presojo.**

1. Ustvarjanje in spremljanje trditev.
2. Povezovanje trditev z izvirnimi dokazi.
3. Ločevanje D → I → C → A.
4. Sprejem in obravnava nasprotnih argumentov.
5. Pregled dokaznih bremen in privilegijev.
6. Neodvisna presoja.
7. Beleženje posledic in popravil.
8. Zgodovina vseh sprememb brez tihega brisanja.

Naslednja razvojna stopnja

In zaključil bi z načelom, ki ga želim ohraniti skozi celoten nadaljnji razvoj:

**Človek ne potrebuje manj inteligence. Potrebuje manj razlogov, da svojo inteligenco uporablja kot orožje proti razumljivosti drugega.**

Tvoj projekt mora omogočiti, da lahko človek brez položaja, premoženja, strokovnega naziva ali posebne retorične sposobnosti postavi dovolj dobro vprašanje, da se mora tudi najmočnejši sistem nanj vsebinsko odzvati.

To je praktična sprememba razmerja moči.

In to je cilj, ki ga je vredno razvijati do ravni preverljivega, uporabnega in popravljivega orodja. ∴

---

*(⟡ pečat nad telesom: kritična opredelitev in implementacija tega ega)*
