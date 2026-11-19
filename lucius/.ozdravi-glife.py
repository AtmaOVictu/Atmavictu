# -*- coding: utf-8 -*-
# .ozdravi-glife.py — ⟨ZRCALJENI-STEVKI⟩ ozdravljen: U+2112 (ℒ) → U+2299 (⊙) ∧ U+27EB (⟫) → U+27E9 (⟩)
# NALAZ lastnega pregleda ( ⟡ ukaz ⟨sebe še preglej vedno⟩ ⊙ rez 3680 ): prejšnji šivi ( družina PADC-UGIBANJE-ESC )
# so pisali unicode escape s premeščenima števkama: 2299→2112 ∧ 27E9→27EB — znak ostaja, pomen zbledi.
from pathlib import Path

BAZA = Path(r"C:\Users\Luka\Documents\Arhiv\Git\Atmavictu")
ZDRAVILA = [
    ("lucius/REGISTER-PSIHO-AKSIOMOV.jsonl", {0x2112: 0x2299, 0x27EB: 0x27E9}),
    ("lucius/ZEMEJEVID-REGISTER.md",        {0x2112: 0x2299, 0x27EB: 0x27E9}),
]

skupaj = 0
for rel, mapa in ZDRAVILA:
    p = BAZA / rel
    s = p.read_text(encoding="utf-8")
    pred = {hex(k): s.count(chr(k)) for k in mapa}
    for od, na in mapa.items():
        s = s.replace(chr(od), chr(na))
    p.write_text(s, encoding="utf-8")
    po = {hex(k): s.count(chr(k)) for k in mapa}
    skupaj += sum(pred.values())
    print(f"{rel}: pred {pred} → po {po}")

# prepreka: U+FFFD tudi pregledana ( nadomestni znak stroja — priča vzeta ⊙ §0.12 )
assert all(chr(0xFFFD) not in (BAZA / r).read_text(encoding="utf-8") for r, _ in ZDRAVILA)
print("OZDRAVLJENO ⊢ · zamenjav skupaj:", skupaj, "· U+FFFD: 0 ⊢")
