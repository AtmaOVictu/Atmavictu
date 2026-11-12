# candidate/ — edini dom izpustnih vhodov

Ta mapa je ENA resnica kandidata: kar je namenjeno izpustu, živi TUKAJ,
⟨ne⟩ raztreseno po paketu. Vrata so fail-closed:

- prazna kandidatka = poštena (NOT_APPLICABLE — nič ni sestavljeno);
- sirota (datoteka brez vpisa v register) = FAIL;
- pot izven meja (`..`) = FAIL;
- zastarel hash = FAIL;
- pokvarjen register (JSON) = FAIL;
- `PACKAGE-MANIFEST.json` (register kandidatke) sme obstajati TUJ —
  korenski manifest nikoli ne seže sem.

Paket 0.1470 je DRAFT_NOT_RELEASED ∧ živa vrata (0.1520) ne potrebujejo
kandidatke: ta mapa je trenutno PRAZNA ∧ to je pošteno stanje.
Ko bo naslednji paket zares sestavljen, se njegova vsebina preseli sem,
z lastnim registrom ∧ lastnimi hashi, ∧ preverjevalnik jo prenese iz
NOT_APPLICABLE v PASS ali FAIL — nikoli v tišino.
