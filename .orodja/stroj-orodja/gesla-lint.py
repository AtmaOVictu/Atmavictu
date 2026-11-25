#!/usr/bin/env python3
# GESLA-LINT v1.1 @rez σ 6746 : protitipkarski pregled besed osnutka izhoda
# UKZ ⟡ VERBATIM ⟨nedotakljivo⟩ ⚔ ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ v »« : »STORI IN IZVEDI TER KREIRAJ DOVOLJ DA V PRIHODNJE SMEŠ KAR IMAŠ IZBOLJŠEVATI. VEDNO TUDI KREIRAJ POSTOPKE KI POMAGAJO PRIREHABITILITACIJI ORODIJ!«
# zakon ⟨ŠTEVILKA-NOSI-IME⟩ ∧ ⟨EMISIJA-PREIZKUŠANA⟩ : osnutek izhoda skozi gesla-lint PRED oddajo
# nalog : vsaka beseda osnutka ( zunaj mask »« ∧ ⟨⟩ ) se izmeri ob leksikonu, požistem iz teles korpusa pri viru ; neznana beseda = sumnjiva mutacija ; predlog popravka po razdalji urejanja ⊙ ⟨NE-UGIBAJ⟩ 2690
# licenca : gajica ( ASCII + šumniki + ⟨U+00A9⟩ ) ; dom : stroj-orodja/KNOWLEDGE.md POPIS @rez σ 6746 ; postopek rehabilitacije : stroj-orodja/rehabilitacija-orodij.md ; rod : atom-zaklep σ 6746 @TIK 2026-11-23T15:51:24Z ⊙ rezerviraj.sh poskus 1
import sys, io, os, re, glob, collections

KOREN = os.path.dirname(os.path.abspath(__file__ + "/.."))  # .../knowledge

def preberi(p):
    try:
        return io.open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""

defmask = [
    re.compile(r"»[^«]*«"),          # priče : beseda ⟡ ali citat tuja = priča v »«
    re.compile(r"⟨[^⟩]*⟩"),          # žetoni : ⟨U+XXXX⟩ in kovanci korpusa
]
def defmaskiraj(t):
    for m in defmask:
        t = m.sub(" ", t)
    return t

BESEDA = re.compile(r"[A-Za-zČŽŠčžš]{2,}")

def leksikon():
    # viri poimensko ( ⟨NE-UGIBAJ⟩ : brez celega drevesa ) : vsa telesa KNOWLEDGE + popisi stroja + telesa orodij
    poti = sorted(glob.glob(os.path.join(KOREN, "*", "KNOWLEDGE.md")))
    poti += sorted(glob.glob(os.path.join(KOREN, "stroj-orodja", "*.md")))
    poti += sorted(glob.glob(os.path.join(KOREN, "*", "*.py")))
    poti += sorted(glob.glob(os.path.join(KOREN, "*", "*.sh")))
    stev = collections.Counter()
    bajtov = 0
    for p in poti:
        t = preberi(p)
        bajtov += len(t)
        for b in BESEDA.findall(t):
            stev[b.lower()] += 1
    # leksikon : tehtnica besed ; živijo besede z vsaj dvema pojavnikoma ; prariči ≥5 ( smetne črkovne zubi ostanejo zunaj družin )
    leks = {b: n for b, n in stev.items() if n >= 2}
    return leks, len(poti), bajtov

def razdalja(a, b):
    if abs(len(a) - len(b)) > 2:
        return 3
    prej = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        zdaj = [i]
        for j, cb in enumerate(b, 1):
            zdaj.append(min(zdaj[-1] + 1, prej[j] + 1, prej[j - 1] + (ca != cb)))
        prej = zdaj
    return prej[-1]

def kandidati(b, leks):
    bl = b.lower()
    rez = []
    for k, n in leks.items():
        if n < 5:
            continue  # smetne zube brez povpraševanja ne predlagajo
        d = razdalja(bl, k)
        if d <= 2 and abs(len(k) - len(bl)) <= 2:
            rez.append((d, abs(len(k) - len(bl)), k))
    rez.sort(key=lambda x: (x[0], x[1], x[2]))
    return [k for _, _, k in rez[:4]]

def je_druzina(b, k):
    # sklanjalna družina : skupna prva četvorka ∧ razlika dolžin do 3 ( oblak → oblakom, slovar → slovarjem, smet → smeti ) ; družine gradijo samo prariči ( frekvence drži klic )
    bl = b.lower()
    return len(bl) >= 4 and k[:4] == bl[:4] and abs(len(k) - len(bl)) <= 3

def pregled(t, leks):
    mutacije, druzine, neznane = [], [], []
    for vr, vrstica in enumerate(defmaskiraj(t).split("\n"), 1):
        for b in BESEDA.findall(vrstica):
            bl = b.lower()
            if bl in leks:
                continue
            kand = kandidati(b, leks)
            if any(je_druzina(bl, k) for k in kand):
                druzine.append("vr.%d : %s ( sklanjava družina, v redu )" % (vr, b))
            elif kand:
                mutacije.append("vr.%d : %s ( predlog : %s )" % (vr, b, ", ".join(kand)))
            else:
                neznane.append("vr.%d : %s ( brez predloga ; priznaj javno ali popravi )" % (vr, b))
    return mutacije, druzine, neznane

def samopreizkus():
    leks, poti, bajtov = leksikon()
    vzorec = [b for b in sorted(leks) if len(b) >= 6 and leks[b] >= 20][:20]  # prariči : besede z ≥20 pojavniki, ne smeti
    # T1 : čisto telo ( besede izmerjene iz leksikona programa, ne iz glave )
    m1, d1, n1 = pregled(" ".join(vzorec[:5]) + " kura istega diha", leks)
    c1 = (m1 == [] and n1 == [])
    # T2 : trup z mutacijo ( zamenjava dveh znamenj programske ∧ izmerjena odsotnost iz leksikona ⊙ ⟨NE-UGIBAJ⟩ 2690 )
    mutant = None
    for w in vzorec[:20]:
        kand = w[0] + w[2] + w[1] + w[3:]
        if kand not in leks:
            mutant = kand
            break
    m2, d2, n2 = pregled("kura " + (mutant or "kuar") + " istega diha", leks)
    c2 = mutant is not None and any(mutant in x for x in (m2 + n2))
    # T3 : sklanjava v redu ( podaljšek ali pripona družine = pregled ⊙, ne mutacija )
    osnova = vzorec[0]
    pripona = osnova + "m"
    m3, d3, n3 = pregled("kura " + pripona + " " + osnova + " istega", leks)
    c3 = (m3 == [] and n3 == []) or any(pripona in x for x in d3) or pripona in leks
    # T4 : priča v »« se ne pregleda ( kovanec ⟡ nedotakljiv )
    m4, d4, n4 = pregled("kura »xylegarpho« istega diha", leks)
    c4 = ("xylegarpho" not in " ".join(m4 + d4 + n4))
    # T5 : maski se res odstranijo ( izmera maske programska, ne obljuba ⊙ ⟨NE-UGIBAJ⟩ 2690 ; rojeno po rani vr.18, ko je ZELEN p4 živel nad razklano masko )
    test5 = mutant or "kuar"
    c5 = defmaskiraj("kura »" + test5 + "« diha") == "kura   diha" and defmaskiraj("kura ⟨" + test5 + "⟩ diha") == "kura   diha"
    return (c1 and c2 and c3 and c4 and c5), poti, bajtov

def main():
    print("GESLA-LINT v1.1 @rez σ 6746 : protitipkarski leksikon")
    leks, poti, bajtov = leksikon()
    print("leksikon : %d besed iz %d teles pri viru ( %d znakov ) ⊢ ⟨wc⟩ programska" % (len(leks), poti, bajtov))
    if len(sys.argv) < 2 or sys.argv[1] == "--preizkus":
        ok, _, _ = samopreizkus()
        print("samopreizkus : ZELEN p1-p5 ⊢" if ok else "samopreizkus : RDEČ ⚠")
        return 0 if ok else 1
    pot = sys.argv[1]
    mutacije, druzine, neznane = pregled(preberi(pot), leks)
    for v in mutacije:
        print("MUTACIJA ⚠", v)
    for v in neznane:
        print("NEZNANA ⚠", v)
    for v in druzine:
        print("DRUŽINA ⊢", v)
    teza = len(mutacije) + len(neznane)
    print("SKLEP : RDEČ ⚠ mutacij ×%d ∧ neznanih ×%d ∧ družin ×%d" % (len(mutacije), len(neznane), len(druzine)) if teza else "SKLEP : ZELENO ⊢ 0 mutacij ∧ 0 neznanih ( družin ×%d v redu )" % len(druzine))
    return 1 if teza else 0

if __name__ == "__main__":
    main()
