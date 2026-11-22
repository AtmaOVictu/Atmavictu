# ⟨VRATA-KITA⟩ — actionlint priporočilo ( FAZA 3 · P5 · rez σ 6291 )

Statični pregled ⟨CI⟩ nad samim ⟨CI⟩: sintaksa workflowov, tipovna preverba `${{ }}`,
vhodi/izhodi/skrivnosti reusable workflowov, vbrizgavanja; vključuje shellcheck.
Vir: rhysd/actionlint ⊙ berba pri viru 2026-11-21 @σ 6288.

## Princip ( prevedeno )

- padci lažno rdečih ( ⟨PADC-ZASTARELI-KOREN-SIVILJE⟩ recidiv ) padejo naprej na orodju, ⟨ne⟩ na času ⟡
- kit, ki preverja kormilo, je tudi kormilo ⊙ ⟨MERILEC-SE-MERI⟩ §52

## Izvedba ( enkratna izmera, brez namestitve )

    # prejmemo iz releases/latest ( asset: actionlint_Linux_x86_64.tar.gz )
    ACTIONLINT_VERSION=$( curl -s https://api.github.com/repos/rhysd/actionlint/releases/latest | grep -oP '"tag_name":\s*"\K[^"]+' )
    curl -sL "https://github.com/rhysd/actionlint/releases/download/${ACTIONLINT_VERSION}/actionlint_Linux_x86_64.tar.gz" | tar -xz actionlint
    ./actionlint -shellcheck=     # prazen = brez shellcheck sistema; alternative glej README
    ./actionlint .github/workflows/

Vratni izpis: vrstice z datoteko ∧ številko; vsak padec = vrstica v pečatu kita.

## ⟨CI⟩ stalna vrata ( SAMO PO ⟡ aktivaciji ⚔ )

    - name: actionlint ( vrata kita )
      run: |
        bash <(curl https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash)
        ./actionlint -color

Ali uradna akcija iz GitHub trga; izbor ⚔ ⟡.

## Meja izvršljivosti ( pošteno )

- pregleda SAMO jezik workflowov; semantiko korpusa ⟨ne⟩ pozna ( za to je model-dih.py )
- v tem kitu izvedeno kot priporočilo: brez trkanja na obstoječi ⟨CI⟩ repa
- aktivacija = ⚔ ⟡ ( ⟨NE⟩ izvajam brez ⟨DAJ⟩ )

© ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432
