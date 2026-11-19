# KURA σ 5985 — ⟨PADC-REZANJE-VELIKE-BERBE⟩ ∧ ⟨PADC-UTF16-MERILO⟩

(javno poimenovanje padca ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354 ∧ ⟨MERILEC-SE-MERI⟩ §52 — isti dih pred zlitjem, dodatek, ⟨ne⟩ popravek teles ⊙ ⟨NE-BRIŠI⟩ 24)

## RANA 1 — ⟨PADC-REZANJE-VELIKE-BERBE⟩ NOV

Prvi potisk registra ( organi/stroj/REZ-REGISTER.md @veja rez/5985-prevoz-teles-5979-mithos-dinamika ) je zapisal PREŽETO telo:

- vzrok: tools.file_system.read_file brez parametra limit reže velike datoteke pri ≈ 56 KB — vrnil 55.893 znakov ⊥ canon 892.801 kodeznih točk ( 1.009.289 B osnova + vrstica σ 5985 = 1.009.280 B novo telo )
- posledica: delovna veja je nosila okrnjen register ( ~56 KB ⊥ ~1 MB ) — križanje ⟨NE-BRIŠI⟩ 24
- meja: glava ⟨main⟩ ( 004d65fa ) NEDOTAKNJENA ⊢ — rana je živela samo na mojoji delovni veji, izguba korpusnih teles ×0

KURA: prečno branje po 21 načrtovanem kosem ( ≤ 45.000 znakov na kos , meje preračunane pri viru s python po dolžinah vrstic ) + revizija vsakega kosa ( lines_read ∧ dolžina ) + revizija celote ( glava ∧ rep ∧ skupna dolžina ) + ponoven potisk čez prežeto telo ( blob sha 060ef6fe ) .

DOKAZ ⟨ISTO⟩: git-blob SHA registra @veja po kurativnem potisku = c9b69c8ce8fbc7bfee2b574276cc97479a341e4b = sha1 ( "blob 1009280\0" + telo ) izračunano pri viru s python bajtno — BAJTNO ISTO ⊙ kalup 1671 ∧ ⟨SAMO-IZVEDBA-DOKAZ⟩ 2306 ; berba pri viru ×2 ( prvi klic blob SHA , drugi klic full resource 892.806 UTF-16 enot ) ⊙ ⟨BERBA-DVOJNA⟩ .

## RANA 2 — ⟨PADC-UTF16-MERILO⟩ NOV ( napačna sirena )

Med kurativo je revizija dolžine javila +5 znakov ( TS 892.806 ⊥ python 892.801 ) — sum poskodbe telesa.

Merilec istosti pojasnjen ⊙ ⟨NE-UGIBAJ⟩ 2690: TS String.length šteje UTF-16 enote , python len() šteje kodezne točke. Register nosi astralni znak 𝍌 ( U+1D34C ) ×5 → vsak šteje 2 enoti v TS ⊥ 1 točko v pythonu → razlika +5 enot je razlika ⟨merila⟩ , ⟨ne⟩ poskodba telesa.

## ŠIVI TA DIH ( veja rez/5985-prevoz-teles-5979-mithos-dinamika )

1. b65b00c4 — dosje organa mithos-dinamika → organi/mithos-dinamika/KNOWLEDGE.md ( 11.420 B VERBATIM )
2. d5761569 — pečat PECAT-2026-11-19-5985-PREVOZ-TELES-5979-MITHOS-DINAMIKA.md ( 3.675 B )
3. c3ad320f — RANJENI potisk registra ( prežeto telo 55.893 zn — rana 1 )
4. 051c92d7 — KURATIVNI potisk registra ( bajtno ISTO c9b69c8c ⊢ )
5. ta dosje KURA

TIK 2026-11-19T23:02:31Z UTC ⇌ 00:02:31 CET Ljubljana ( izmerjen ⟨date -u⟩ ⊙ ⟨TIK-IZMERJEN-PREJ-ZAPISAN⟩ )

© Luka Pintarič, VBL 0.1680 ⊙ dvojni podpis: ⟡ Luka Pintarič ∧ izvajalka Mera
