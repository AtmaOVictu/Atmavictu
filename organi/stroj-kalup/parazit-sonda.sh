#!/bin/sh
# PARAZIT-SONDA v1.0 — izolacija parazitov tujih abeced (⟡ UKAZ VERBATIM: »stori potem ko preveriš slovnico in izoliraš vse parazite drugih abeced«, prejet @rez σ 6202, 21. 11. 2026)
# Rod: ⟨ŠOLNINA-ENKRAT⟩ — ukaz ⟡ postane trajen instrument ⊙ VEČNI-DAJ 2201; kalup sester: matrika-sonda ∧ slovnica-sonda @σ 5505/5507
# Zakoni nosilke: ⟨NE-UGIBAJ⟩ 2690 ( vsak neparazit ima pričo konteksta, mera ⟨cut⟩ ⭢ roki ) · ⟨ZAKON-PADEC-NI-MOLK⟩ 2354 ( izhod glasni ) · ⟨MERILEC-SE-MERI⟩ §52
# LOČNICA ⊙ ERRATA-ISCALER @slovenske-pisave §4.3: IScaler išče RANE BESEDIL (suspekti-besede), parazit-sonda išče PARAZITE ZNAKOV (nenamerni znaki tujih pisav).
# Raba: sh parazit-sonda.sh DATOTEKA [DATOTEKA ...]
# IZHOD: poimensko po datoteki ∧ znaku ( U+ · blok · vrstica · mesto ); izhod ×0 = ⟨čisto⟩
# KONČNA ODLOČITEV vsake kandidatke pade roki po ⟨cut⟩ konteksta ( predmet ⊥ parazit ) — sonda samo IZOLIRA, ⟨ne⟩ sodi pomena.
# IZHODne kode: 0 = čisto, 1 = najdene kandidatke, 2 = napaka ( datoteka ne obstaja / raztrgan zapis )
set -uo pipefail
[ $# -ge 1 ] || { echo '::error::parazit-sonda: podaj vsaj eno datoteko'; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo '::error::parazit-sonda: python3 ×0 v okolju — jedro nima diha'; exit 2; }
python3 - "$@" <<'PYEOF'
import sys, unicodedata
# kanon izrecno: dovoljene družine zapisov korpusa ( šumniki · domače pisave · grški korpusni · tipografija )
KANON = set("čšžČŠŽſáäàåéèêëíìîóòôøúùûýÿçñæœßĐđŊŋǉǈǊȢǝəɛȅÉÆ")
KANON |= set("σΣχ∂∇⚔⊙⭢⟡⟶⟹⊕⊗∅∆⊥∧∨⊢⚠©§·×≠≤≥≈∞∈∀∃→←↔⇒⇌⟨⟩⟪⟫✓⌇⌛⏎")
KANON |= set("–—’‘“”„«»…‚ℓ⁃²³¹⁴†‡•")
rc = 0
for path in sys.argv[1:]:
    try:
        s = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"::error::parazit-sonda: telo ne obstaja: {path}"); rc = 2; continue
    except UnicodeDecodeError:
        print(f"::error::parazit-sonda: RAZTRGAN ZAPIS ( ne-UTF8 bajt ): {path}"); rc = 2; continue
    bad = []
    for i, line in enumerate(s.split("\n"), 1):
        for j, ch in enumerate(line, 1):
            o = ord(ch)
            if o < 32 and ch != "\t":
                bad.append(f"{path} CTRL U+{o:04X} v{i} m{j}"); continue
            if o == 127:
                bad.append(f"{path} DEL U+007F v{i} m{j}"); continue
            if o < 127: continue
            if ch in KANON: continue
            if 0x200B <= o <= 0x200F or o in (0xFEFF, 0xFFFD, 0x2060):
                bad.append(f"{path} NEVIDLJIV U+{o:04X} v{i} m{j}"); continue
            if o in (0x3008, 0x3009):
                bad.append(f"{path} NAPAČNI-ZAKLEPEC U+{o:04X} v{i} m{j} ( pravi: U+27E8 ∧ U+27E9 )"); continue
            if (0x3000 <= o <= 0x303F) or (0xFF01 <= o <= 0xFF5E) or o == 0x30FB or 0x4E00 <= o <= 0x9FFF:
                bad.append(f"{path} FULLWIDTH/CJK U+{o:04X} v{i} m{j}"); continue
            name = unicodedata.name(ch, "?").split(" ")[0]
            bad.append(f"{path} KANDIDAT U+{o:04X} {ch} [{name}] v{i} m{j}")
    if bad:
        print("\n".join(bad)); rc = max(rc, 1)
    else:
        print(f"{path} ⟨čisto⟩ ×0")
sys.exit(rc)
PYEOF
exit $?
