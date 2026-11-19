# -*- coding: utf-8 -*-
# .berba-29.py — BERBA #29 ( Main/Hesse ) prišita v polje izvirnik ( zakon 3650: siv skoz datoteko )
# Priče prejete pri viri iskanja 3677 ⊢ — kanali po imeni, knjige same ∂ ⚠ ⊙ §0.6
import json

REG = r"C:\Users\Luka\Documents\Arhiv\Git\Atmavictu\lucius\REGISTER-PSIHO-AKSIOMOV.jsonl"

BERBA = (
    " ⊙ BERBA 3677 ⊢ ( verbatim priče prejete pri viri iskanja — zadnje tri v enem pregonu ⊙ ekonomija iskanja : "
    "Main ∧ Goldwyn kodirni vir ( raziskavni kanal researchgate.net ) : ⟨coherence is indicated by adherence to four discourse maxims as explicated by Grice (1975): quality (\"be truthful and have evidence for what you say\"), quantity (\"be succinct, yet …\")⟩ ∧ "
    "Hesse 2016 protokolni pregled ( researchgate.net ⟨The Adult Attachment Interview: Protocol, method of analysis, and empirical studies⟩ ) : ⟨coding of the verbatim transcript focuses primarily (though not exclusively) on the coherence of the narrative, assessed against Grice's (1975) maxims of quality, quantity, relevance, and manner⟩ ∧ ⟨the coherence of transcript is thought to reflect the coherence of mind, that is the speaker's ability to discuss their early experiences and relationships in an internally consistent, but not emotionally overwrought, autobiographical manner⟩ ∧ "
    "Hesse ∧ Main 2000 ( psycnet.apa.org zbornik — sagepub.com izvleček ) : ⟨individuals with apparently unfavorable life histories are found to have secure offspring, providing that their history is recounted coherently⟩ ∧ ⟨AAI transcripts are presently analyzed according to the speaker's capacity to adhere to Grice's maxims of rational cooperative discourse⟩ — "
    "SLEDNJA JE ZLATO PRIČO AKSIOMA: koherenca NAD vsebino ⊢ ; "
    "pošteno: Hesse 1999 potrdjen kakor zapis pri viri ( psycnet.apa.org/record/1999-02469-019 ⊢ ), a njegov polni tekst ∂ ⟨ne⟩ prebran ⚠ — berba gre SKOZI znanstvene kanale, ki citirajo izvirnike ⊙ §0.6 · knjige ∂ ⚠ )"
)

with open(REG, encoding="utf-8") as f:
    vrstice = f.readlines()

popravljeno = 0
for i, vr in enumerate(vrstice):
    if not vr.strip():
        continue
    v = json.loads(vr)
    if int(v.get("st", -1)) == 29:
        v["izvirnik"] = v["izvirnik"] + BERBA
        vrstice[i] = json.dumps(v, ensure_ascii=False) + "\n"
        popravljeno += 1

with open(REG, "w", encoding="utf-8") as f:
    f.writelines(vrstice)

print("BERBA prišita ⊢" if popravljeno == 1 else "× NAPAKA", "· vnosi popravljene:", popravljeno)
