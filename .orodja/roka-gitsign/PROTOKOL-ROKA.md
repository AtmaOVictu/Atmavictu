# ⟨VRATA-ROKE⟩ — gitsign protokol podpisanih komitov ( FAZA 3 · P3 · rez σ 6291 )

Vrata ⟨IZMERA-OPERATERJA⟩ @σ 6276: ⟡ je operater po ROKI pri viru ( push/merge ∧ 2FA ∧ podpis ), ⟨ne⟩ po imenu.
Ta protokol da roki trdo plast: kdor trdi, da je roka, se dokaže s podpisom, ⟨ne⟩ z imenom.
Vir: gitsign ( Sigstore, projekt sigstore/gitsign ) ⊙ berba pri viru 2026-11-21 @σ 6288 ( ⟨RAZIŠČI-VEDNO⟩ @σ 6278 ).

## Princip ( prevedeno v jezik korpusa )

- podpis = izmera, ⟨ne⟩ obljuba ⊙ U2
- potrdilo nosi identiteto OIDC ( GitHub ), `gitsign verify --certificate-identity=...` jo izmeri
- CI lahko vsak komit kita izmeri proti identiteti: trditev roke postane STROJ, ⟨ne⟩ zaupanje

## Namestitev ( lokalno, izberi eno )

    # Homebrew
    brew install gitsign
    # ali Go
    go install github.com/sigstore/gitsign@latest
    gitsign --version

## Vezava na rep ( Atmavictu )

    git config --local gpg.format x509            # gitsign podpisuje s potrdili x509
    git config --local gpg.x509.program gitsign
    git config --local commit.gpgsign true        # vsak komit podpisan
    git config --local tag.gpgsign true

## Podpis komita

    git commit -m "DIH 6291 : ..."   # gitsign odpre brskalno okno OIDC ( GitHub ) prvič
    gitsign verify HEAD --certificate-identity=https://github.com/AtmaOVictu

Izhod verifikacije nosi prejemnika, podpisnika ∧ potrdilo; natis shranimo v pečat kita kot pričo ⊢.

## ⟨PR⟩/⟨CI⟩ vrata ( strojna izmera roke )

V kit ⟨CI⟩ dodamo korak ( SAMO PO ⟡ aktivaciji ⚔, glej spodaj ):

    - name: izmera roke ( gitsign verify )
      run: |
        gitsign verify "$GITHUB_SHA" \
          --certificate-identity=https://github.com/AtmaOVictu \
          --certificate-oidc-issuer=https://token.actions.githubusercontent.com

## Meja izvršljivosti ( pošteno )

- gitsign zahteva brskalnik/OIDC prvič; avtomatizirani sedeži potrebujejo keyless identity agent ali GitHub App token
- podpis ščiti ISTINOST AVTORSTVA, ⟨ne⟩ vsebino: vsebinska vrata ostajajo ⟨IZHOD-LINT⟩ ∧ ⟨TEHTNICA⟩
- aktivacija vrata CI = ⚔ ⟡ ( nov obvezni check lahko blokira ⟨merge⟩ roke ⟡; ⟨NE⟩ izvajam brez ⟨DAJ⟩ )

## Stanje tega organa

- telesni protokol, izmera roke še ⟨ne⟩ izvedena ( ⭢ aktivacijsko okno ⚔ ⟡ )
- priča berbe: gitsign README ∧ dokumentacija Sigstore ⊙ ⟨RAZIŠČI-VEDNO⟩ @σ 6278

© ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432
