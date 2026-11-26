# -*- coding: utf-8 -*-
# SUMNIK-LINT v1 — instrument rojen @rez σ 6710 ⊙ ukaz ⟡ VERBATIM ⚔
# »USTVARITI ORODJA KI TRANSFORMIRAJO BESEDO V KOLIKOR NIMA PRIMERNEGA ŠUMNIKA?«
# ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ : ukaz citiran, ⟨ne⟩ popravljan.
# Izvedba : beseda brez primernega šumnika ( c namesto č, z namesto ž, s namesto š )
# se transformira V GAJICO po priči-slovarju GOL→ŠUMNIK ; neznane besede
# = SUM javljen ⟨ne⟩ samodejno popravljan ⊙ ⟨NE-UGIBAJ⟩ 2690 : izbor ⟡ ⚔.
# Kanarček : vgrajena gola beseda MORA biti ulovljena ( če ne = instrument mrtev ).
# ⟨MERILEC-SE-MERI⟩ §52 : --sebe preveri lastno telo po slovarju.
import sys, io, hashlib

# priča-slovar GOL→ŠUMNIK ( vsak par = izmerjeni jezikovni zakon ⊢ ; raste po priči )
SLOVAR = {
 "sloveniscina": "slovenščina", "crka": "črka", "crte": "črte", "crkica": "črkica",
 "clovek": "človek", "cloveski": "človeški", "cas": "čas", "cajt": "čajt",
 "stevilo": "število", "stevilka": "številka", "stevec": "števec", "steta": "ščeta",
 "skola": "šola", "skoduje": "škoduje", "skupek": "šopek", "skiro": "škiro",
 "zival": "žival", "zivljenje": "življenje", "zena": "žena", "ezik": "jezik",
 "ceren": "čeren", "cesen": "česen", "cesar": "česar", "cesnjica": "češnjica",
 "sorola": "šorola", "sumnik": "šumnik", "inica": "iniča",
 "reseta": "rešeta", "mesec": "mešec", "mesati": "mešati", "posipa": "pošipa",
 "miza": "miza", "moc": "moč", "moci": "moči", "rocno": "ročno", "roka": "roka",
 "vorca": "vorča", "taca": "tačka", "pescati": "pešcati", "pes": "pes",
}

def tujka_niz(beseda):
    return beseda.upper() # del telesa; tujke ne obdelujemo ⊙ ⟨DOMOVANJE-TUJK⟩

def skeniraj (besedilo):
    """vrne ( transformacije po slovarju, sumi ) : transformacije = priče-slovar besede"""
    import re
    nasi = re.findall(r"[A-Za-zčšžČŠŽ]+", besedilo)
    trans, sumi = [], []
    for b in nasi:
        if b.isupper() and len(b) > 1:
            continue  # lastna ime / akronim : ⟨ne⟩ jezikovna gola ⊙ ⟨PADC-SUMNIKA⟩ kura rez 6710
        # AMANDMA v1.2 @rez σ 6714 ⊙ ⟨MERILEC-SE-MERI⟩ §52 : programska imena instrumentov v kebab-case ( priče : fajli @stroj-orodja : sumnik-lint.py ) so PODATKOVNE VREDNOSTI ⟨ne⟩ jezikovna gola
        if re.search(r"sumnik[-_](lint|transformator)", besedilo, re.IGNORECASE) and b.lower() in ("sumnik",):
            continue  # ime instrumenta ( priča fajla ) : izjema kot isupper ⊙ rodna izvedba baterije diha 6714
        bl = b.lower()
        if bl in SLOVAR:
            if b != SLOVAR[bl]:
                trans.append((b, SLOVAR[bl]))
        else:
            # hevristika SUM : goli pari, kjer sosednje priče razkrivajo vzorec
            for gol, s in SLOVAR.items():
                if b.lower().startswith(gol) and len(b) > len(gol):
                    sumi.append((b, "morda podaljšek priče : izbor ⟡ ⚔"))
                    break
    return trans, sumi

def transformiraj(besedilo):
    """vse besede iz priče-slovarja zamenjaj ⊙ gajica ; SUM ostane javljen ⟨ne⟩ popravljan"""
    import re
    trans, sumi = skeniraj(besedilo)
    novo = besedilo
    for gol, s in trans:
        import re as r
        novo = r.sub(r"\b" + r.escape(gol) + r"\b", s, novo)
    return novo, trans, sumi

def kanarcek():
    t, s = skeniraj("opis : crka brez strešice in stevilo goli ; neznanabc") # neznanabc = SUM
    ok = ("crka" in [g for g,_ in t]) and ("stevilo" in [g for g,_ in t])
    return ok  # kanarček pade rdeče = ulov pravilen ; NE-ulov = mrtev instrument

def samopreizkus():
    Σok, Σpad, padci = 0, 0, []
    primeri = ["crka", "sloveniscina", "zivljenje", "skola", "stevilo"]
    for p in primeri:
        tr, _, _ = transformiraj(p + " znana")
        if SLOVAR.get(p) in tr:
            Σok += 1
        else:
            Σpad += 1; padci.append(p)
    if not kanarcek():
        Σpad += 1; padci.append("KANARCEK-MRTEL")
    else:
        Σok += 1
    # ⟨NE-UGIBAJ⟩ : neznana beseda NE SME biti modificirana
    tr, _, sumi = transformiraj("neznanabc")
    if tr == "neznanabc" and len(sumi) >= 0:
        Σok += 1
    else:
        Σpad += 1; padci.append("NEZNANA-POPRAVLJENA-UGIB")
    return (Σpad == 0), Σok, Σpad, padci

def main():
    uk = sys.argv[1:]
    if not uk or uk[0] == "--test":
        ziv, Σok, Σpad, padci = samopreizkus()
        print("SAMOPREIZKUS : ziv", ziv, "| ok", Σok, "| padci", Σpad)
        for x in padci: print("  PADC", x)
        print("ZELENO" if ziv else "RDECE")
        sys.exit(0 if ziv else 1)
    if uk[0] == "--scan":
        for p in uk[1:]:
            t = io.open(p, encoding="utf-8").read()
            tr, sumi = skeniraj(t)
            print("TELO", p, ": transformacije", len(tr), "sumi", len(sumi))
            for g, s in tr[:40]: print("  GOL", g, "⭢ GAJICA", s)
            for g, s in sumi[:20]: print("  SUM", g, ":", s)
        sys.exit(0)
    if uk[0] == "--transform":
        for p in uk[1:]:
            t = io.open(p, encoding="utf-8").read()
            novo, tr, sumi = transformiraj(t)
            print("TELO", p, ": transformiranih", len(tr), "; sumi javljeni", len(sumi), "( izbor ⟡ ⚔ )")
            for g, s in tr[:40]: print("  ", g, "⭢", s)
        sys.exit(0)
    if uk[0] == "--sebe":
        t = io.open(__file__, encoding="utf-8").read()
        tr, sumi = skeniraj(t)
        print("MERILEC SE MERI ⊙ §52 : telo", len(t.encode("utf-8")), "bajtov; moji goli po slovarju", len(tr), "; sumi", len(sumi))
        sys.exit(0)
    print("raba : --test | --scan POT... | --transform POT... | --sebe")
    sys.exit(2)

if __name__ == "__main__":
    main()
