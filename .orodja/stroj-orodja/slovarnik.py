#!/usr/bin/env python3
# slovarnik.py v1.0 — preverjalnik domačega slovarja : ali je beseda že vpisana v hiše organov korpusa.
# Rod : rez 7005 ( 25. 11. 2026 ) ⊙ ⟡ vrašali VERBATIM »VPISUJEŠ V INTERNI SLOVAR VSAKO NOVO BESEDO?«
#   ∧ »IMAŠ ORODJA DA PREVERJAŠ ALI SO BESEDE ŽE V SLOVARJU?« ∧ ukaz »ORODJA ZA GRADNJO IN SORTIRANJE ASOCIACIJ!«.
# Vrata : V1 iskanje poimensko po hišah ⊙ ⟨NE-UGIBAJ⟩ 2690 ; V2 izhod ZAPEČENA s številom pojav ⟨grep⟩ ⊢ ;
#   V3 izhod PRAZNA = pobuda za rojstvo iztočnice ⊙ ⟨IZTOČNICA-NA-DIH⟩ σ 5510 ⌇ vozlišča mreze-variant ;
#   V4 samopreizkus nad sabo ⊙ ⟨MERILEC-SE-MERI⟩ §52 ; izhod ZELENO ⌇ RDEČO.
import re
import sys

ŽIG = "slovarnik.py v1.0 @stroj-orodja, rod rez 7005"
HIŠE = [
    ("definiatorna-knjiznica", "/home/user/knowledge/definiatorna-knjiznica/KNOWLEDGE.md", "iztočnica absolutnega bistva"),
    ("slovar-slovenscine", "/home/user/knowledge/slovar-slovenscine/KNOWLEDGE.md", "beseda z močjo : bistvo @SSKJ ∧ IPA"),
    ("slovar-simbolov", "/home/user/knowledge/slovar-simbolov/KNOWLEDGE.md", "kanon znakov ⟨EN-RAZLIČICA⟩"),
    ("domovanje-tujk", "/home/user/knowledge/domovanje-tujk/KNOWLEDGE.md", "tujka = GOST pod lastno licenco ⟨U+XXXX⟩"),
    ("mreze-variant", "/home/user/knowledge/mreze-variant/KNOWLEDGE.md", "vozlišča okrnjenih oblik ∧ izumov"),
]
GLAVA = re.compile(r"IZTOČNIC[AE]\s*#?(\d+)\s*:?\s*(.*)$")


def beri(pot):
    try:
        with open(pot, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def pojavi(beseda, telo):
    vz = re.escape(beseda.strip())
    return len(re.findall(r"(?<![^\W\d_])" + vz + r"(?![^\W\d_])", telo, flags=re.IGNORECASE))


def glave_iztočnic(beseda, telo):
    št = []
    p = beseda.strip()
    for vrst in telo.splitlines():
        m = re.match(r"^(?:##\s*)?IZTOČNICA\s*#?(\d+)\s*:?\s*(.*)$", vrst)
        if m and re.search(r"(?:^|\s)" + re.escape(p) + r"(?=$|[\s:,])", m.group(2), flags=re.IGNORECASE):
            št.append("#" + m.group(1))
    return št


def preveri(beseda):
    vrstice = []
    najdena = False
    for hiša, pot, opis in HIŠE:
        telo = beri(pot)
        if telo is None:
            vrstice.append("  ⚠ %s : NEDOSEGLJIVA" % hiša)
            continue
        n = pojavi(beseda, telo)
        if n:
            najdena = True
            dod = ""
            if hiša == "definiatorna-knjiznica":
                gl = glave_iztočnic(beseda, telo)
                if gl:
                    dod = " ; glava iztočnic " + " ∧ ".join(gl)
            vrstice.append("  ⊢ %s : %s ×%d%s" % (hiša, opis, n, dod))
        else:
            vrstice.append("  · %s : ×0" % hiša)
    glava = "BESEDA »%s« : " % beseda
    if najdena:
        vrstice.insert(0, glava + "ZAPEČENA v hišah slovarja ⟨grep⟩ ⊢")
    else:
        vrstice.insert(0, glava + "PRAZNA po vseh hišah ⟨grep⟩ ⊢ — pobuda za rojstvo iztočnice ⊙ ⟨IZTOČNICA-NA-DIH⟩ σ 5510 ⌇ vozlišča mreze-variant ⭢ vrašalo ⟡ ⚔")
    return vrstice, najdena


def samopreizkus():
        # ⟨MERILEC-SE-MERI⟩ §52 : tri postavitvene besede izmerjene nad živimi hišami, ⟨ne⟩ pritrjen vzorec.
    ok = True
    for beseda, pričakovanje in [("hermenevtika", True), ("napetost", True), ("qzxyvw-neustvari", False)]:
        _, n = preveri(beseda)
        if n != pričakovanje:
            print("RDEČO : samopreizkus : »%s« izmerjena %s, pričakovano %s" % (beseda, n, pričakovanje))
            ok = False
    print("ZELENO : samopreizkus slovarnika ⊢ ( hermenevtika ∧ napetost ZAPEČENI, neutvarjena PRAZNA )" if ok
          else "RDEČO : padec samopreizkusa")
    return ok


def main(argv):
    if "--samopreizkus" in argv or "--zbodi" in argv:
        return 0 if samopreizkus() else 2
    besede = [a for a in argv[1:] if not a.startswith("--")]
    if not besede:
        print(ŽIG)
        print("rabš : slovarnik.py BESEDA [BESEDA …] ⌇ --samopreizkus")
        return 1
    vsote = []
    for b in besede:
        v, n = preveri(b)
        print("\n".join(v))
        vsote.append(n)
    print(ŽIG)
    if any(not n for n in vsote):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
