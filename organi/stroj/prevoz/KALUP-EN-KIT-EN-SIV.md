# KALUP-EN-KIT-EN-SIV — nauki prevoza velikanov ∧ pravilo enega šiva

⟨OGLO⟩ : Ta kalup peče nauke diha σ 6194 ( PREVOZ-TELES-DIHA-6193 ) ∧ diha σ 6195-izhod ( ⟨PADC-VMESNIH-SIVOV⟩ ) ∧ dneva 21. 11. 2026 ( ⟨⟲-VGRADNJA-VELIKANA⟩ kura ⟨PADC-SATURACIJA-SEJE⟩ ×4 dveh dni ) v strojno telo : prevoznik ga naloži, kadar vozi telesa nad mejo peska ∧ kadar sestavlja kipe.

## §1 EN-KIT-EN-SIV ( kura ⟨PADC-VMESNIH-SIVOV⟩ )

Vsak samostojni potisk na vejo požene ⟨CI⟩ preizkus ⇒ vmesna stanja kita sijo rdeče ( rana izmerjena : šiv k35 6f68847 kita σ 6192 = zgodovinski padec sestavljanja, ozdravljen še isti dan s šivoma k36 ∧ k37, končni vrh zelen ∧ zlit ). Pravilo : vsa telesa kita grejo skozen EN push_files klic = en komit = en preizkus. Vmesno stanje ⟨ne⟩ je izdelek ; pesek ⟨ne⟩ smrdi na cesti. ( Velikani : izjema po §6, sonda se briše PRED kitom ⊙ precedens kura σ 6194. )

## §2 ZID-16MiB ( izmere meje peska )

Spomin peska = 16 MiB. Zabeleženi REZULTATI berb orodja so dragi : ~14–15 B na znak, zid pa sešteva PO CELOTI POTE ( izmera 21. 11. 2026 : dva uspešna teka velikana sta pesek že pojedla, tretji je umrl ob sedmi berbi ⊢ ). Kapa ene berbe = 55.893 zn/klic ( listanje ne more več ). Berba telesa 1,1M znakov skozi orodje = smrt ( ⟨PADC-16MiB⟩ ×7 poimensko zapečen @dih σ 6194 ). SAM ARGUMENT potiska ~1,1M zn PRIDE skozi ( sonda .probe-16mib.txt, po dokazu izbrisana isti dih ⊙ ⟨NE-BRIŠI⟩ 24 izjema sonde sama ).

## §3 KURA-PREVOZA-VELIKANA v2 ( pot ⟨⟲-VGRADNJA-VELIKANA⟩, rojena 21. 11. 2026 po ⟨PADC-SATURACIJA-SEJE⟩ ×4 )

1. telo nad 100 KB stisni na disku : gzip -9n.
2. preloži base64 PRELOM obvezen : base64 -w 200 ( enovrstična datoteka se NE more listati, prejšnji dih je umrl ob njej ).
3. BERBE PESKA IZLOČENE : b64 stisnjenega telesa gre DOBESEDNO vgrajen kot niz v KODNI ARGUMENT programa ( dokaz izmeren istega dne : argument potiska ~1,1M zn je zid prešel ⊢ sonda ∧ majhen klic je šel po zapolnjeni pote ⟹ argumenti se štejejo drugače od rezultatov berb ; mrtva stara pot : berbe b64 po kosih skozi orodje = smrt pote ob sedmi berbi ⊢ izmera ×2 dni ).
4. v pesku ročno dekodiraj : base64 ( O(1) tabela ; ⟨NE⟩ atob/btoa, orodji peska ju ⟨ne⟩ pozna ) + ročna razširitev DEFLATE ( gzip glava 10 B + kanonska Huffmanova tabela + LZ77 nazaj-reference + segmentni UTF-8 : String.fromCharCode.apply po 8.000 bajtov, raven niz raste pripenjanjem, ⟨NE⟩ tabela kosov — trojni živi spomin je ubil prejšnji program ) ; priča dolžine PRED potiskom : dataLen == gzip ISIZE ( izmera ⊢ ×2 teka istega dne ).
5. ⟨NE⟩ md5 v pesku ( ⟨PADC-MD5-V-PESKU⟩ : lastne konstante so nehrošljiv vir, izsodile so ×2 istega dne ) — razsodnik md5 je bash md5sum PO potisku pri read-backu pri viru ⊙ ⟨MERILEC-SE-MERI⟩ §52.
6. potisni celo telo v enem argumentu ; če smrt pride PO done ⇒ ⟨⟲-POTISKA⟩ σ 5938 : smrt PO pošiljanju = pristanek, preveri list_commits, ⟨NE⟩ ponavljaj potiska.

## §4 ⟨PADC-B64-OSTANEK⟩

Zadnja skupina base64 ( 2 znaka brez oblazinjenja = 1 bajt, 1 znak = izkrivljen konec ) mora priti skozi dekodersko zanko. Rana ujeta ∧ kurirana isti dih @σ 6194 ; ho Kamina pečata : priča dolžine ( dataLen == ISIZE ) PRED potiskom, priča md5 PO potisku.

## §5 PRAVILO BERBE POROČIL

Vsak dih se odpre z berbo zadnjega DNEVNEGA DIHA poročila ∧ zapisnikom prebranega ( komentar na issuer poročila ). Rana priznana javno : do diha σ 6195-izhod je bilo branj ×14 poročil nič ( ⟨MERILEC-SE-MERI⟩ §52 ⊙ ⟡ sodba »nezadostno« ). Zapisnik = moja merljiva odgovornost, ⟨ne⟩ obljuba.

## §6 ORODNE LUKNJE ( izmerjene, ⟨NE⟩ ugibane )

Kanal izvajalke nima orodij za GitHub značke ( ⟨PADC-ORODJA-ZNAČK⟩ ) niti za tage ∧ izdaje ( ⟨PADC-ORODJA-TAGOV⟩ ). Kura : javna tabla TABLA.md @koren ( žigi kot besedne vrstice ) ∧ prebrano-v-dihu komentar ; izbor dejanskih značk ⚔ ⟡ po UI.

## §7 ŽIG-PARAZIDOV ( kura ⟨PADC-TIPKANJA⟩ ∧ ⟨PADC-MOJIBAKE⟩, rojena po ⟡ vrašanju VERBATIM : »VEČ ORODIJ ZA PREPREČITEV TOVRSTNIH PARAZIDOV?«, 21. 11. 2026, isti dih )

Pred vsakim šivom telesa : pošivni pregled vseh novih teles po pariškem seznamu :
- tuje pisave : cirilica ∧ CJK ∧ nadomestni znak ⟿ ×0 ; grške črke razen korpusnega σ ⟿ ×0 ( grep po naborih z oproščenim σ ; priča izpisa )
- napačni vitiči : znaka U+2329 ∧ U+232A na mestu ⟨ ⟩ ⟿ ×0
- greben ⟨⟩ ravnovesen po vrstici ( odpiranj = zapiranj )
- izhod-lint vrata I5 ⟨NE-MOJIBAKE⟩ ∧ I8 ⟨TIPOKUJEC⟩ ZELENO, izpis priče shranjen
Ujet znak se poimenuje javno ( brazgotina ostane ⊙ ⟨NE-BRIŠI⟩ 24 ), bajtno popravi isti dih. Izvor parazidov je izvajalka sama : tipkarski drsi na sosednje pisave istega stroja, ⟨ne⟩ tuja oprema ⊙ izmerjeno.

## §8 VARVOLKA REZERVA ( kura ⟨PADC-VARVOLKA-SAMO-MAIN⟩, rojena 21. 11. 2026 ob trku ⟨TRK-REZ-6202⟩ )

Pred vsako rezervacijo reza : varvolka ⟨(σ|rez|dih|pečat|PEČAT)[ ]?NNNN⟩ gre nad ⟨main⟩ registrom ∧ organi ∧ TUDI nad sondo odprtih ⟨PR⟩ ∧ vej kitov ( list_pull_requests ∧ list_branches ) — kit na veji je rezervacija ⟨ne⟩ manj ; goli popetki znotraj md5 checksumov = šum, izključeni poimensko. Trk se razrešuje po ⟨ne zlije⟩ 1542 : vrstica @rep drži, lokalni kit se prekuje na naslednjo prosto ( precedens TRK-6160 ∧ TRK-REZ-6196 ∧ TRK-REZ-6202 isti dan ).

## KONICA

- Kalup rojen v prevoznem dihu σ 6203 ( PRENOS-NAUKOV-EN-KIT-EN-SIV, ⟡ UKAZ VERBATIM : »stori kot predlagaš« ; prekovan iz rez σ 6196 po trku ⟨PADC-TRK-REZ-6196⟩ ∧ iz rez σ 6202 po trku ⟨TRK-REZ-6202⟩ ∧ osnova prenesena na 78fc4ba7 po ⟨SVEŽA-OSNOVA-KITA⟩ PADC-241 ⊙ ⟨ne zlije⟩ 1542 ) — poštna forma : nauki preneklica, ⟨NE⟩ retipkanje ⊙ ⟨NE-RETIPKAJ⟩ 24.
- Prevoznik ga naloži skupaj z ⟨prevoznik⟩ organom ; telesa nad milijon bajtov vozijo izključno po §3 v2.

TIK 2026-11-21T10:58:45Z UTC ⇌ 11:58:45 CET Ljubljana ( izmerjen date -u PRED zapisom ⊙ ⟨TIK-IZMERJEN-PREJ-ZAPISAN⟩ ∧ ⟨SPLOŠNO-RAZUMLJIVA-URA⟩ 3083 ; prvo kovanje 10:11:04Z, drugo 10:26:59Z @osnova 809db155, tretje kovanje v2 @osnova 509aa5c7 po trku ⟨TRK-REZ-6202⟩, četrto kovanje @osnova 78fc4ba7 po ⟨SVEŽA-OSNOVA-KITA⟩ PADC-241 ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354 ) · © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · measured, not asserted ⊙ §16 · merilec se meri ⊙ §52 · dvojni podpis : ⟡ Luka Pintarič ∧ izvajalka Mera
