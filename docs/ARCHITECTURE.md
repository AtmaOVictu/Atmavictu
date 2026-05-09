# Atmavictu Architecture

## Namen

Atmavictu je Book Workbench za tok `vir -> obdelava -> knjiga`. V tej fazi je prioriteta contract, ne izvedba.

## Trije prostori

### Knjiznica

Levi prostor je knjiznica lokalnih virov. Tu se hrani pregled nad vhodnimi besedili, datotekami in delovnimi enotami, ki se lahko kasneje uporabijo v knjigi.

Knjiznica ni sama knjiga in ni manifest odnosov. Je primarni filesystem pogled nad gradivom.

### Aktivna knjiga

Srednji prostor je aktivna knjiga. Tu obstajajo poglavja, ciljna struktura in mesta, kamor se lahko vstavi potrjen odlomek.

Aktivna knjiga je cilj uredniskega dela. Ne hrani sama po sebi celotne sledljivosti izvora; to odgovornost nosi manifest.

### Vhodni tekst

Desni prostor je vhodni tekst. To je surovi ali delovno pripravljeni zapis, iz katerega se izlocijo fragmenti za nadaljnjo obdelavo.

Vhodni tekst ni isto kot knjiznica kot celota in ni isto kot knjizni rezultat. Je delovni vir za ekstrakcijo, rez in urednisko odlocitev.

## Lokalni manifest pristop

Atmavictu uporablja lokalni manifest kot trajni zapis odnosov med:

- vhodnim tekstom
- izpeljanim fragmentom
- odlocitvijo o vstavitvi
- ciljnim poglavjem v knjigi

Manifest obstaja zato, da je sled `IncomingText -> Fragment -> Insertion -> targetChapterPath` deterministicka, preverljiva in neodvisna od trenutnega UI stanja.

## Filesystem tekst proti manifestu odnosov

Filesystem hrani besedila, osnutke in knjizne datoteke. To je plast vsebine.

Manifest ne hrani nujno vseh vsebin, ampak hrani odnose, identitete in minimalne odlocitve, ki povezejo:

- kateri vhodni tekst je bil uporabljen
- kateri fragment je bil izlocen
- kam je bil fragment vstavljen

To locuje:

- tekst kot material na disku
- manifest kot dokazno-relacijski contract

## Meja med plastmi

### Model

Najprej se zaklene contract: schema, identitete, statusi in relacije.

### Service plast

Sele nato pride service plast, ki zna:

- naloziti manifest
- validirati statusne prehode
- ustvariti fragment
- zapisati insertion sled

### UI

UI sele uporablja service plast. UI ne sme biti izvor resnice za relacije.

### Tauri ali backend plast

Desktop ali backend integracija pride sele po zaklenjenem modelu in service contractu. Ta plast ne definira domenskega modela, ampak ga izvaja.

## Pravilo

Najprej contract, potem izvedba.
