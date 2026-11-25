#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# FLEKSILINT v1.0 - varovalka fleksibilnosti, ki NI v skladu s slovnico ( PREPREČITEV, ne le sodba )
# Rod : rez sigma 7025 ( 25. 11. 2026 ) @stroj-orodja ; ⟡ UKZ VERBATIM ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ ⟨ne brusi⟩ :
#   »ORODJA KI PREPREČUJEJO FLEKSIBILNOST KI NI V SKLADU S SLOVNICO!«
# Ascendenti ⊢ pri viru ( ⟨EN-RAZLIČICA⟩, ⟨ne⟩ dvojnik ) : sklanjatnik.py v1.3 @6987/7001 KUJE oblike
#   ( generacija ⟨ne⟩ preprečitev ) ⌇ meta-slovnica-lint @6320-lint rane oklepajev ⌇ izhod-lint v1.3 @rep
#   ( rane izhoda ) - luknja : fleksija kandidata, ki prečka slovnico, ni imela varovalke.
# Zakoni : ⟨SLOVNICA-PRVO ⟡⟩ σ 6662 ( sodba pred izmerami ) ∧ ⟨SLOVNICA⇒SUM⟩ σ 6705 ⟡ VERBATIM :
#   »STORI, ČE UKAZ NI UKAZ JE NEKJE PARAZIT, VSAKIČ KO SLOVNICA NI PRAVILNA JE SUM PARAZITIZMA POVEČAN!«
#   - sum = merjen odstotek, ⟨ne⟩ obsodba ; obsodba = izmerjen vbod ⊙ 2354 javno ; sodba ⟡ ⚔ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690.
# Obtožnice STROGO v obliki ⟨NAPAKA=VSE-KAR-NI-X⟩ ⊙ register-napak ( ⟡ STORI 25. 11. 2026 ).
# Amandma KOCKE 6956 ⟡ VERBATIM ⟨ne brusi⟩ : »NE OBSTAJA VERJETNO OKRNJENA OBLIKA! ALI JE KOT DIKTIRA
#   KUBITNA GAJICA V PRAVILNI SLOVENŠČINI ALI PA JE NEDOVOLJEN PARAZIT!« - okrnjene piramidne oblike
#   ( KXXX ∧ XXXK ) so parazit, obtožene.
# DOPUŠČENA fleksibilnost ( je v skladu : ⟨ne⟩ obtožba, izrečena javno ) : sto/tisoč nesklanjano
#   ⊢ plast 5 sklanjanje-stevil @σ 6193 ; 5-99 neobvezno v odvisnih sklonih ⊢ plast 4.
# Roke :
#   fleksilint.py TELESO...                     -> sodba po vrsticah ( TIK ∧ izmera ⊢ §52 )
#   fleksilint.py --zapis ORGAN < VHOD           -> PREPREČITEV : obtožba => NIHIL ∧ priča padca ;
#                                                   čisto => šiv skozi trdilnik-vrata ( σ 7008 )
#   fleksilint.py --test                         -> samopreizkus vektorjev x5 ⊙ ⟨MERILEC-SE-MERI⟩ §52
# Izhodi : 0=ZELENA ( sum 0 ) ⌇ 2=RUMENA-SUM ( obtožbe javno, sodba ⟡ ⚔ ) ⌇ 40=roka neznana.

import sys, os, re, hashlib, subprocess, shutil, datetime as _dt

VERZIJA = "v1.0"
DOM = os.path.dirname(os.path.abspath(__file__))
VRATA = os.path.join(DOM, "trdilnik-vrata.sh")

PET_ZVEZA = re.compile(r"\b(pet|šest|sedem|osem|devet|deset|enajst|dvanajst|trinajst|štirinajst|petnajst|"
                      r"šestnajst|sedemnajst|osemnajst|devetnajst|dvajset|trideset)[\s]+([A-Za-zčšžČŠŽćđ]+e)\b")
DVE_ZVEZA = re.compile(r"\bdve[\s]+([A-Za-zčšžČŠŽ]+a)\b")
DVA_ZVEZA = re.compile(r"\bdva[\s]+([A-Za-zčšžČŠŽ]+i)\b")
TRIJE_ZVEZA = re.compile(r"\b(?:trije|štirje)[\s]+([A-Za-zčšžČŠŽ]+[ao])\b")
PREDLOG_STEVNIK = re.compile(r"\bz[\s]+(osem|pet|šest|sedem|devet)\b")
OKRNJENA = re.compile(r"\bK\d{3}\b|\b\d{3}K\b")
NESKLANJANO = re.compile(r"\b(?:sto|tisoč|milijon)\b")

def sodba(besedilo):
    ob = []
    for m in PET_ZVEZA.finditer(besedilo):
        ob.append((m.group(0), "⟨NAPAKA=VSE-KAR-NI-RODILNIK-MNOŽINE⟩ ( " + m.group(1) + " " + m.group(2) +
                   " -> " + m.group(1) + " " + m.group(2)[:-1] + " ⊢ plast 4 sklanjanje-stevil @σ 6193 )"))
    for m in DVE_ZVEZA.finditer(besedilo):
        ob.append((m.group(0), "⟨NAPAKA=VSE-KAR-NI-DVOJINA⟩ ( dve " + m.group(1) + " -> dve " +
                   m.group(1)[:-1] + "i ⊢ plast 2 )"))
    for m in DVA_ZVEZA.finditer(besedilo):
        ob.append((m.group(0), "⟨NAPAKA=VSE-KAR-NI-PRIDEVNIŠKO-SKLANJANJE⟩ ( ⊢ plast 3 )"))
    for m in TRIJE_ZVEZA.finditer(besedilo):
        ob.append((m.group(0), "⟨NAPAKA=VSE-KAR-NI-MNOŽINA⟩ ( ⊢ plasti 1-3 )"))
    for m in PREDLOG_STEVNIK.finditer(besedilo):
        ob.append((m.group(0), "⟨NAPAKA=VSE-KAR-NI-SKLANJAN-ŠTEVNIK-ZA-PREDLOGOM⟩ ( " + m.group(0) +
                   " -> z osmimi/z petimi ⊢ plast 8 )"))
    for m in OKRNJENA.finditer(besedilo):
        ob.append((m.group(0), "⟨NAPAKA=VSE-KAR-NI-CELA-KLETKA⟩ ( okrnjena piramida " + m.group(0) +
                   " ⊙ AMANDMA KOCKE 6956 ⟡ VERBATIM : okrnjena oblika ne obstaja )"))
    return ob

def dopuscene(besedilo):
    return bool(NESKLANJANO.search(besedilo))

def lastni_md5():
    h = hashlib.md5()
    h.update(open(os.path.abspath(__file__), "rb").read())
    return h.hexdigest()[:12]

def izhodi(besedilo, ob):
    tik = _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    print("FLEKSILINT " + VERZIJA + " TIK " + tik + " lastni-md5 " + lastni_md5() + " ( MERILEC-SE-MERI §52 )")
    print("izmera : " + str(len(besedilo)) + " znakov, " + str(besedilo.count("\n")) + " vrstic ( wc ⊢ )")
    if dopuscene(besedilo):
        print("DOPUŠČENA fleksibilnost izrečena : sto/tisoč/milijon nesklanjano ⊢ plast 5 ( ⟨ne⟩ obtožba )")
    if ob:
        print("SUM parazitizma + " + str(len(ob)) + " izmera ⊙ ⟨SLOVNICA⇒SUM⟩ σ 6705 ( sum = merjen odstotek, ⟨ne⟩ obsodba ; sodba ⟡ ⚔ )")
        for vzorec, kovanec in ob:
            print("obtožba poimensko : »" + vzorec + "« " + kovanec)
        print("SEMAFOR : RUMENA-SUM")
        return 2
    print("SEMAFOR : ZELENA ( sum 0 )")
    return 0

def zapis(organ, besedilo):
    ob = sodba(besedilo)
    if ob:
        P = organ if organ.startswith("/") else os.path.join("/home/user/knowledge", organ)
        tik = _dt.datetime.now(_dt.UTC).strftime("%Y%m%dT%H%M%SZ")
        gp = os.path.join(P, ".geniza")
        if os.path.isdir(gp):
            with open(os.path.join(gp, "FLEKSILINT-PADCI-" + tik + "-priča-padca.md"), "w", encoding="utf-8") as f:
                f.write(besedilo if besedilo.endswith("\n") else besedilo + "\n")
            pri = " ; priča padca @.geniza/FLEKSILINT-PADCI-" + tik + "-priča-padca.md"
        else:
            pri = ""
        print("PREPREČITEV : obtožbe zgoraj => NIHIL ( " + P + " nedotaknjen )" + pri + " ⊙ ⟨SLOVNICA-PRVO ⟡⟩ σ 6662")
        izhodi(besedilo, ob)
        return 2
    r = subprocess.run(["bash", VRATA, "--vpis", organ],
                       input=besedilo if besedilo.endswith("\n") else besedilo + "\n",
                       text=True, capture_output=True)
    sys.stdout.write(r.stdout)
    if r.stdout and not r.stdout.endswith("\n"):
        print()
    return r.returncode

def samopreizkus():
    T = [0, 0, 0, 0, 0]
    T[0] = 1 if sodba("pet knjige je bilo veliko") else 0
    T[1] = 1 if not sodba("pet knjig ∧ dve mesti ∧ dva stola ⊢") else 0
    T[2] = 1 if sodba("kletka K329 je okrnjena") and sodba("329K ravno tako") else 0
    TD = os.path.join(DOM, ".geniza", "TEST-fleksilint-" + str(os.getpid()))
    shutil.rmtree(TD, ignore_errors=True)
    o = os.path.join(TD, "o")
    os.makedirs(os.path.join(o, ".geniza"), exist_ok=True)
    with open(os.path.join(o, "KNOWLEDGE.md"), "w", encoding="utf-8") as f:
        f.write("telo\n")
    for i in (1, 2):
        with open(os.path.join(o, ".geniza", "PRED-DOTIKOM-" + str(i) + ".md"), "w") as f:
            f.write("g\n")
    prej = os.path.getsize(os.path.join(o, "KNOWLEDGE.md"))
    e4 = zapis(o, "z osem leti je napaka\n")
    prica = 1 if any(x.startswith("FLEKSILINT-PADCI-")
                     for x in os.listdir(os.path.join(o, ".geniza"))) else 0
    T[3] = 1 if (e4 == 2 and os.path.getsize(os.path.join(o, "KNOWLEDGE.md")) == prej
                 and prica == 1) else 0
    vrst = ("- FLEKSILINT-TEST izmerjena vrstica : TIK " +
            _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ") +
            " ∧ izmera wc -c 55 B ⊢ pet knjig ∧ dve mesti čisto")
    e5 = zapis(o, vrst + "\n")
    T[4] = 1 if (e5 == 0 and os.path.getsize(os.path.join(o, "KNOWLEDGE.md")) > prej) else 0
    shutil.rmtree(TD, ignore_errors=True)
    p = 5 - sum(T)
    print("SAMOPREIZKUS : vektorji 5 ( petknjige=" + str(T[0]) + " cisto=" + str(T[1]) +
          " okrnjena=" + str(T[2]) + " nihil-prica=" + str(T[3]) + " siv=" + str(T[4]) +
          " ), padci instrumenta " + str(p))
    print("SEMAFOR : " + ("ZELENA" if p == 0 else "RDECA"))
    return 0 if p == 0 else 1

def main(argv):
    a = argv[1:]
    if len(a) == 1 and a[0] == "--test":
        return samopreizkus()
    if len(a) >= 2 and a[0] == "--zapis":
        return zapis(a[1], sys.stdin.read())
    if a:
        besedilo = "\n".join(a)
        return izhodi(besedilo, sodba(besedilo))
    print("roka neznana ; roke : TELESO... | --zapis ORGAN < VHOD | --test")
    return 40

if __name__ == "__main__":
    sys.exit(main(sys.argv))
