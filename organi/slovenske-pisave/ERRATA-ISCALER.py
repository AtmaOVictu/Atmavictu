# ERRATA-ISCALER v2.2 @rez σ 6190 — slovenske-pisave §4.3
# LOČNICA: PRICA ( vrstica z izrecnim dokazom: puščica ∧ PADC ∧ ERRATA ∧ IZVID ) | RANA ( živa napaka, kandidatka kure ).
# Sodba o vsaki vrstici pade roki ( ⟡ VERBATIM ∧ NJENI pečati vidijo izstop ).
# Pravila kure: genize ×2 PRED dotikom; (?<!s) vedno; gola zamenjava prepovedana ⊙ precedens ssprožilec @σ 6188.
SUSPEKTI = {
    "izvrba": "izvršba",
    "varvolka": "varovalka",
    "izvršbena": "izvršena",
    "zleme": "izkrivljene",
    "swalloval": "pogoltnil",
    "pogovoril": "pogoltnil",
    "domociija": "demociija",
    "obnavljen": "obnovljen",
    "frekvca": "frekvenca",
    "vsprošanje": "vprašanje",
    "nedotakneni": "nedotaknjeni",
}
PRICE_MARKERJI = ("→", "PADC", "ERRATA", "errata", "Errata", "IZVID",
                  "varvolka.sh", "ORODJE ⟨VARVOLKA⟩", "IZDELEK-VARVOLKA",
                  "mreze-variant", "| varvolka", "varvolka \u27e8(σ", "varvolka \u27e86")
import glob, os, re
rane_skupaj, price_skupaj = {}, {}
for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "*", "KNOWLEDGE.md"))):
    organ = os.path.basename(os.path.dirname(f))
    t = open(f, encoding="utf-8").read()
    rane, price, mesta = {}, {}, []
    for i, line in enumerate(t.split("\n"), 1):
        je_price = any(m in line for m in PRICE_MARKERJI)
        for b in SUSPEKTI:
            n = line.count(b)
            for _ in range(n):
                if je_price: price[b] = price.get(b, 0) + 1
                else:
                    rane[b] = rane.get(b, 0) + 1
                    mesta.append(f"v{i}:{b}")
        for m in re.finditer(r"(?<![sS])prožilec", line):
            if je_price: price["prožilec_gol"] = price.get("prožilec_gol", 0) + 1
            else:
                rane["prožilec_gol"] = rane.get("prožilec_gol", 0) + 1
                mesta.append(f"v{i}:prožilec_gol")
    if rane: print(f"RANE {organ}: {rane} :: mesta {mesta}")
    if price: print(f"PRIČE {organ}: {price}")
    for k, v in rane.items(): rane_skupaj[k] = rane_skupaj.get(k, 0) + v
    for k, v in price.items(): price_skupaj[k] = price_skupaj.get(k, 0) + v
print("SKUPAJ RANE:", rane_skupaj, ":: skupaj mest:", sum(rane_skupaj.values()))
print("SKUPAJ PRIČE:", price_skupaj, ":: skupaj mest:", sum(price_skupaj.values()))
