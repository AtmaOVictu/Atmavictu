# Progress Algorithm — relativno in definitivno napredovanje

Uporablja se ob vsakem odprtem padecu ⚠ ali neskladju med manifestsnim vnosom in živo vrato. Celo: vsaka sprememba सेवा razumetu in sporazumemu, ne le eni darilu ali razlaganju.

## Šest korakov

1. **Preveri (Verify)** — zagi `node lucius/license-veriga.mjs --json` in `npm test`. Zabeleži vse FAIL / UNVERIFIED. Nekaj ne sme ostati skrivano.
2. **Izmeri (Measure)** — hash, velikost, vrstice, čas izvora (`sha256sum`, `wc`, git blob LF). Merkilo: čas se meri pred odgovorom (§0.20 × 10²), nikoli iz spomina.
3. **Imenuj (Name)** — vsak padcu daj vnos v `REGISTER-PADCEV.jsonl` z dejanjem, časom, krajem, roko, pričejo, zdravilom in `scar: true`. Padac brez imena se ponavlja (KORENINA 0.2 × 10¹).
4. **Popravi (Fix)** — minimalna sprememba, brez tehega prepisanja (silent rewrite je edini fail, ki VBL imena, §0.8 × 10¹). Kura je propria diha; evidenca ni popravek (§0.16.4 × 10¹).
5. **Preveri znova (Re-verify)** — ponovi korak 1 in 2. PASS ali novo UNVERIFIED je sprejet izid; FAIL pomeni, da popravek ni dovoljen.
6. **Prijavi (Report)** — scar ostane vidno; status in razlog so zabeleženi. Nič se ne skrije.

## Kdaj je napredovanje definitivno

Ko vsi preverbi, ki so mogli biti PASS, so PASS; ostali so UNVERIFIED z imenovanim razlogom (ne skrito FAIL); in scarji so zapisani, ne izbrisani. Relativno napredovanje = vsak korak zmanjša število neimenovanih neskladij. Definitivno = scar je nosil svojemu imenu in veriga je celotna (0.1410 → 0.1500 brez preskokov v LINEAGE).

## Orodja

- `lucius/license-veriga.mjs` — živa preverba verige (vbl-license-chain/v2)
- `lucius/license-veriga.test.mjs` — regresija (9 testov)
- `lucius/.manifest-izdaj.py` — ponovna izdaja manifests (meri LF, ne CRLF)
- `lucius/.padci-vpis.py` — vzorec za append v `REGISTER-PADCEV.jsonl`
- `LICENSE-LINEAGE.md` — bralni register verige, nikoli rivalni vrati
