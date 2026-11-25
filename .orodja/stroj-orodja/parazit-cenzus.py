# PARAZIT-CENZUS v1.0 @rez σ 6741 : cenzi vseh skript korpusa po njegovem zakonu
# UKZ ⟡ VERBATIM : »PARAZITI SO TUDI IN PREDVSEM VSE SKRIPTE KI NISO V GAJICI IN NIMAJO DOMA V LICENCI!«
# licenca : gajica ( ASCII + šumniki + ⟨U+00A9⟩ ) ∧ kanon znakov ; dom : stroj-orodja/KNOWLEDGE.md POPIS @rez σ 6741
# rod : atom-σ6741 @TIK 2026-11-23T15:03:52Z ⊙ ukaz ⟡ ; priča : psalm σ 6741
# sloj : ⟨ NE-BRIŠI ⟩ ⟨ NE-GRIZI ⟩ ⟨ NE-UGIBAJ ⟩ ( vsaka trditev izmerjena )
# postopek : ulov ( *.py *.sh ) -> pregled ( gajica ∧ dom ) -> rehabilitacija ( dom pri priči ) -> preprečitev -> vpis
import sys, os, io, glob

ENG = ("the ", "The ", "This script", "function ", "return value", "input file")

def preberi(pot):
    try:
        return io.open(pot, encoding="utf-8").read()
    except UnicodeDecodeError:
        return io.open(pot, encoding="utf-8", errors="replace").read()

def gajica_izmera(t):
    # gajica : šumniki v telesu ali čist slovenski komentarji brez angleških znamenj
    kom = "\n".join(l for l in t.split("\n") if l.strip().startswith("#"))
    sumniki = sum(t.count(c) for c in "čžšČŽŠ")
    eng_znamenja = sum(kom.count(e) for e in ENG)
    return (sumniki > 0) or (len(kom) > 0 and eng_znamenja == 0), sumniki, eng_znamenja

def cenzus(koren="."):
    skripte = sorted(p for p in glob.glob(os.path.join(koren, "*", "*")) if p.endswith((".py", ".sh")))
    dom_telo = ""
    for md in glob.glob(os.path.join(koren, "*", "KNOWLEDGE.md")):
        dom_telo += preberi(md)
    for dop in glob.glob(os.path.join(koren, "stroj-orodja", "*.md")):
        dom_telo += preberi(dop)
    rezultati = {"DOMAČIN": [], "BREZ-DOMA": [], "BREZ-GAJICE": [], "PARAZIT": []}
    for s in skripte:
        telo = preberi(s)
        gaj, sumniki, eng = gajica_izmera(telo)
        ime = os.path.basename(s)
        dom = (s in dom_telo) or (ime in dom_telo)
        if not gaj and not dom:
            rezultati["PARAZIT"].append(s)
        elif not gaj:
            rezultati["BREZ-GAJICE"].append(s)
        elif not dom:
            rezultati["BREZ-DOMA"].append(s)
        else:
            rezultati["DOMAČIN"].append(s)
    return skripte, rezultati

def samopreizkus():
    g1, _, _ = gajica_izmera("# slovenski komentar s šumnikom\n")  # priča : gajica
    g2, _, _ = gajica_izmera("# This script does the work\n")      # priča : angleščina
    return g1 and (not g2)

def main():
    print("PARAZIT-CENZUS v1.0 @rez σ 6741 @TIK", io.open("/dev/null") and "" or __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime()))
    print("samopreizkus :", "ZELEN" if samopreizkus() else "RDEČ")
    skripte, rez = cenzus()
    print("skript skupaj :", len(skripte))
    for razred in ("PARAZIT", "BREZ-GAJICE", "BREZ-DOMA", "DOMAČIN"):
        print("razred", razred, ":", len(rez[razred]))
        for s in rez[razred]:
            print("   ", s)

if __name__ == "__main__":
    main()
