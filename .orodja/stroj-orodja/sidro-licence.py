#!/usr/bin/env python3
# SIDRO-LICENCE v1.1 : zasideklicence : licenca zasidrana bajtno ; vsaka sprememba semantike se izmeri ⌇ povrne
# rod @rez σ 6811 @stroj-orodja ⊙ ukaz ⟨U+2761⟩ VERBATIM: "NALOŽI LICENCO IN JO ZASIDRAJ"
# KURA v1.1 @rez σ 6816 ⊙ ukaz ⟡ "POTRDI IN UTRJUJ PREVERJENE OPERACIJE IN JIH PREVERI TER IZBOLJŠAJ" : ⟨PADC-SIDRA-SAMOPREIZKUSA⟩ ( rod σ 6811 : zaponi(test) je zapekel trup samopreizkusa v PRODUKCIJSKO sidro ) ⇒ samopreizkus izoliran na lastno sidro v .genizi ∧ preizkus T4 ⟨SIDRO-PRODUKCIJE-NEDOTAKNJENO⟩ : izmera produkcije PRED ⊥ PO testu bajt-ito ( plast, ki meri, ali je samo merjenje spremenilo merjenega ⊙ ⟨MERILEC-SE-MERI⟩ §52 )
# ⟨U+2125⟩ : ( 1 ) sidro = izmera bajt-ita pri viru ( bajti ⌇ vrstice ⌇ md5 ⌇ sha256 ⌇ TIK ) zapisana v sidro-licence.json
#           ( 2 ) --preveri : sveža izmera ⊥ sidro ; odmik = RANA poimensko ( semantika se je spremenila brez izmere )
#           ( 3 ) --povrni : povratek bajt-ito iz priče ( telo slovenščine/zlovenščine se vrne )
#           ( 4 ) --samopreizkus : kanarček vsak tek ⊙ ⟨MERILEC-SE-MERI⟩ §52 ; molk default ⊙ ⟨TIHINA-ORODIJ⟩ σ 6723 ; T4 produkcija nedotaknjena ⊙ σ 6816
# © 0.2026 × 10⁴ ⟨U+2761⟩ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 : dvojni podpis
import sys, json, hashlib, os, argparse, glob, datetime

HIŠA = os.path.dirname(os.path.abspath(__file__))
SIDRO = os.path.join(HIŠA, "sidro-licence.json")
GENIZA = os.path.join(HIŠA, ".geniza")

def tik():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def izmeri(pot):
    telo = open(pot, "rb").read()
    return {
        "bajti": len(telo),
        "vrstice": telo.count(b"\n"),
        "md5": hashlib.md5(telo).hexdigest(),
        "sha256": hashlib.sha256(telo).hexdigest(),
    }

def poroci(naslov, vrstice, zgovori=False):
    """molk default : poročilo gre v .genizo ; stdout SAMO na --zgovori ⚔ ⟨U+2761⟩ ⊙ ⟨TIHINA-ORODIJ⟩"""
    telo = naslov + "\n" + "\n".join(vrstice) + "\n"
    pot = os.path.join(GENIZA, "POROCILO-sidro-licence-%s.md" % tik().replace(":", ""))
    with open(pot, "w", encoding="utf-8") as f:
        f.write(telo)
    if zgovori:
        print(telo)
    return pot

def zaponi(telo_pot, prica_pot="", pot_sidra=None):
    m = izmeri(telo_pot)
    m["tik"] = tik()
    m["prica"] = prica_pot
    m["vir"] = "LICENSE.md @rep AtmaOVictu/Atmavictu ⟨main⟩"
    with open(pot_sidra or SIDRO, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=1, sort_keys=True)
    return m

def preveri(telo_pot, pot_sidra=None):
    if not os.path.exists(pot_sidra or SIDRO):
        return 2, "SIDRO ×0 : zaponi licenco prvo", {}
    s = json.load(open(pot_sidra or SIDRO, encoding="utf-8"))
    m = izmeri(telo_pot)
    if m["md5"] == s["md5"] and m["bajti"] == s["bajti"] and m["sha256"] == s["sha256"]:
        return 0, "⊢ IDENTIČNA ⊥ sidro ( bajti %d ⌇ vrstice %d ⌇ md5 %s )" % (m["bajti"], m["vrstice"], m["md5"]), m
    rane = []
    for k in ("bajti", "vrstice", "md5", "sha256"):
        if m[k] != s[k]:
            rane.append("%s : sidro %s ⊥ telo %s" % (k, s[k], m[k]))
    return 1, "⚠ RANA : semantika licence odmaknjena od sidra ; " + " ⌇ ".join(rane), m

def povrni(prica_pot, cilj_pot):
    """povratek bajt-ito : telo slovenščine se vrne iz priče ; priča ostane ⊙ ⟨NE-BRIŠI⟩ 24"""
    telo = open(prica_pot, "rb").read()
    prej = izmeri(cilj_pot) if os.path.exists(cilj_pot) else {"md5": "-"}
    open(cilj_pot, "wb").write(telo)
    po = izmeri(cilj_pot)
    ok = po["md5"] == izmeri(prica_pot)["md5"]
    return ok, "POVRATEK %s ⭢ %s : %s ⭢ %s ( bajti %d )" % (prica_pot, cilj_pot, prej["md5"], po["md5"], po["bajti"])

def samopreizkus():
    """kanarček v1.1 @σ 6816 : dober telo ⊢ ∧ ranjen trup ⚠ ∧ povratek bajt-ito ⊢ ∧ PRODUKCIJSKO sidro nedotaknjeno ⊢ ⊙ ⟨INOKULACIJA⟩ σ 6658"""
    # T4 osnova : produkcija se izmeri PRED testom ( bajt-ito );
    prej_prod = open(SIDRO, "rb").read() if os.path.exists(SIDRO) else b""
    # test živi v CELICI na lastnem sidru ( ⟨NE⟩ na produkciji ⊙ kura σ 6816 )
    sidro_test = os.path.join(GENIZA, "sidro-SAMOPREIZKUS-%s.json" % tik().replace(":", ""))
    test = os.path.join(GENIZA, "sidro-samopreizkus-%s.md" % tik().replace(":", ""))
    trup = os.path.join(GENIZA, "sidro-trup-%s.md" % tik().replace(":", ""))
    telo = "# telo v slovenščini ⟡\nbeseda je ne ⊢ pri viru\n"
    with open(test, "w", encoding="utf-8") as f:
        f.write(telo)
    z = zaponi(test, test, sidro_test)
    k1 = preveri(test, sidro_test)
    with open(trup, "w", encoding="utf-8") as f:
        f.write("# telo v angleščini? semantic drift here\nbeseda je ne ⊢ pri viru\n")
    k2 = preveri(trup, sidro_test)
    k3 = povrni(test, trup)
    po_prod = open(SIDRO, "rb").read() if os.path.exists(SIDRO) else b""
    k4 = (prej_prod == po_prod and (po_prod != b"" or not os.path.exists(SIDRO)))
    for p in (test, trup, sidro_test):
        if os.path.exists(p):
            os.remove(p)
    delo = [k1[0] == 0, k2[0] == 1, k3[0] is True, k4 is True]
    return all(delo), delo, z

def main():
    ap = argparse.ArgumentParser(description="SIDRO-LICENCE v1.1 : licenca zasidrana bajtno ; samopreizkus izoliran ⊙ σ 6816")
    ap.add_argument("--zaponi", metavar="TELO", help="zasidraj telo ( izmera ⭢ sidro-licence.json )")
    ap.add_argument("--prica", default="", help="pot priče ( povratek iz nje )")
    ap.add_argument("--preveri", metavar="TELO", help="sveža izmera ⊥ sidro")
    ap.add_argument("--povrni", nargs=2, metavar=("PRICA", "CILJ"), help="povrnitev bajt-ito iz priče")
    ap.add_argument("--samopreizkus", action="store_true")
    ap.add_argument("--zgovori", action="store_true", help="⟨edina-vrata-glasu⟩ ⚔ ⟨U+2761⟩")
    a = ap.parse_args()
    izhodi = []
    if a.samopreizkus:
        ok, delo, z = samopreizkus()
        stanje = "SAMOPREIZKUS 4/4 ⊢" if ok else "SAMOPREIZKUS PADEL"
        izhodi.append((0 if ok else 2, stanje + " : T1 dober ⊢ %s ⌇ T2 trup ⚠ %s ⌇ T3 povratek ⊢ %s ⌇ T4 produkcija nedotaknjena ⊢ %s" % tuple(delo)))
    if a.zaponi:
        m = zaponi(a.zaponi, a.prica)
        izhodi.append((0, "ZASIDRANO ⊢ : bajti %d ⌇ vrstice %d ⌇ md5 %s ⌇ sha256 %s ⌇ TIK %s" % (m["bajti"], m["vrstice"], m["md5"], m["sha256"], m["tik"])))
    if a.preveri:
        k, sporocilo, m = preveri(a.preveri)
        izhodi.append((k, sporocilo))
    if a.povrni:
        ok, sporocilo = povrni(a.povrni[0], a.povrni[1])
        izhodi.append((0 if ok else 1, sporocilo))
    if not izhodi:
        ap.print_help()
        return 0
    poroci("POROCILO-sidro-licence @TIK %s" % tik(), [s for _, s in izhodi], a.zgovori)
    return max(k for k, _ in izhodi)

if __name__ == "__main__":
    sys.exit(main())
