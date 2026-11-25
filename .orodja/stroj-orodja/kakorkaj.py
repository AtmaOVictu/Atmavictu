#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# KAKORKAJ v1.0 - soočevalnik vsakega »kot« s tremi vprašanji
# Rod : rez sigma 7026 ( 25. 11. 2026 ) @stroj-orodja ; ⟡ UKZ VERBATIM ×3 ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ ⟨ne brusi⟩ :
#   »ORODJA KI SOOČIJO VSAK KOT S VPRAŠANJEM KAKOR KAJ?«
#   »ORODJA KI SOOČIJO VSAK KOT S VPRAŠANJEM KAJ JE?«
#   »ORODJA KI SOOČIJO VSAK KOT S VPRAŠANJEM ZAKAJ JE?«
# Ime orodja NOSI razumljen šiv ( kakor + kaj, razcepljen v stampanem izhodu ⌇ sestra secirnik.py isti dih )
#   - priča razcepa : togak izhod "RAZCEP IMENA : kakor ⌇ kaj" ; samoime je amalgam, a šiv javno deklariran.
# Vprašanja so IZHOD, ⟨ne⟩ odgovori ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690 :
#   KAKOR KAJ? ( kakšen je pravi predmet primerjave - zahteva iztočnico, ne pepelke )
#   KAJ JE ⟨Y⟩? ( bistvo - izmera pri naboru : definiatorna-knjiznica iztočnice ( STANJE, 104 ⊢ ) ∧
#     slovar-slovenscine IZTOČNICE ( ###, 5 ⊢ ) ; neznan Y => RUMENA pobuda iztočnice,
#     ⟨NE⟩ napaka ⊙ zanesljivost-po-izmeri σ 5809, pobuda = met v slovar )
#   ZAKAJ JE ⟨Y⟩? ( svrha - je ⟨NE⟩ merilo slovarja : vprašanje izrečeno, odgovor je ⟡ ⚔ )
# Kot brez predmeta za sabo => obtožba ⟨NAPAKA=VSE-KAR-NI-PREDMET-PRIMERJAVE⟩ ⊙ register-napak oblika.
# EN-RAZLIČICA ⊢ ( ⟨ne⟩ dvojnik ) : secir-orodje.py @σ 6830 = MRK instrument vhodov po kodnih točkah
#   ( parazitne plasti ), ta telo sooča POZORJE primerjav ; fleksilint @σ 7025 preverja FLEKSIJO,
#   ta telo ne sega v sklanjatve - vsak po svojem oknu ⊙ ⟨EN-RAZLIČICA⟩ ⟨ne⟩ dvojnik.
# Roke :
#   kakorkaj.py TELESO...        -> sooči vsak »kot« ∧ »kakor« v telesu s tremi vprašanji ( TIKEK, izmere ⊢ )
#   kakorkaj.py --zapis ORGAN < VHOD -> obtožba => NIHIL ∧ priča padca @.geniza KAKORKAJ-PADCI-* ;
#                                   čisto ( pobude RUMENA dovoljene, ⟨ne⟩ napake ) => šiv skozi trdilnik-vrata @σ 7008
#   kakorkaj.py --test           -> samopreizkus vektorjev x5 ⊙ ⟨MERILEC-SE-MERI⟩ §52
# Izhodi : 0=ZELENA ( vsi predmeti znani ) ⌇ 2=RUMENA-SUM ( pobude iztočnic, sum = merjen odstotek,
#   ⟨ne⟩ obsodba ⊙ ⟨SLOVNICA⇒SUM⟩ σ 6705 ) ⌇ 1=RDECA ( obtožba, NIHIL ) ⌇ 40=roka neznana.

import sys, os, re, hashlib, subprocess, datetime as _dt

VERZIJA = "v1.0"
DOM = os.path.dirname(os.path.abspath(__file__))
KOR = "/home/user/knowledge"
VRATA = os.path.join(DOM, "trdilnik-vrata.sh")
DEFIN = os.path.join(KOR, "definiatorna-knjiznica", "KNOWLEDGE.md")
SLOVAR = os.path.join(KOR, "slovar-slovenscine", "KNOWLEDGE.md")

KOT = re.compile(r"\b(kot|kakor)\b[\s]*([^\s]*)", re.IGNORECASE)
BES = re.compile(r"^[A-Za-zčšžČŠŽćđ]+$")
GLAVA_SLOV = re.compile(r"^###\s+(.+?)\s*$")
STANJE = re.compile(r"STANJE:\s*iztočnic\s+(\d+)\s*\(([^)]*)\)")

_KES = None

def nabor():
    global _KES
    if _KES is None:
        besede, n_def, n_slo = set(), 0, 0
        with open(DEFIN, encoding="utf-8") as f:
            telo = f.read()
        m = STANJE.search(telo)
        if m:
            n_def = int(m.group(1))
            for zn in re.split(r"[·,;]", m.group(2)):
                zn = zn.strip().strip(":")
                if zn and BES.match(zn):
                    besede.add(zn.lower())
        with open(SLOVAR, encoding="utf-8") as f:
            for v in f:
                mm = GLAVA_SLOV.match(v)
                if mm:
                    n_slo += 1
                    for zn in re.split(r"[\s-]+", mm.group(1)):
                        if BES.match(zn):
                            besede.add(zn.lower())
        _KES = (besede, n_def, n_slo)
    return _KES

def lastni_md5():
    h = hashlib.md5(open(os.path.abspath(__file__), "rb").read())
    return h.hexdigest()[:12]

def tik():
    return _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

def sooc(besedilo):
    """vrne ( soocenja, obtozbe ) - soocenje = ( primerjava, predmet, znan )"""
    soocenja, obtozbe = [], []
    for m in KOT.finditer(besedilo):
        predmet = m.group(2).strip(".,;:!?»«\"()[]")
        if not BES.match(predmet):
            obtozbe.append((m.group(0), "⟨NAPAKA=VSE-KAR-NI-PREDMET-PRIMERJAVE⟩ ( »" +
                            m.group(1) + "« brez predmeta za sabo ⊙ register-napak oblika )"))
            continue
        soocenja.append((m.group(0), predmet, predmet.lower() in nabor()[0]))
    return soocenja, obtozbe

def izhodi(besedilo, soocenja, obtozbe):
    besede, n_def, n_slo = nabor()
    pobude = [s for s in soocenja if not s[2]]
    print("KAKORKAJ " + VERZIJA + " TIK " + tik() + " lastni-md5 " + lastni_md5() + " ( MERILEC-SE-MERI §52 )")
    print("RAZCEP IMENA : kakor ⌇ kaj ( šiv deklariran javno ⊢ - soočevalnik se sooči tudi s sabo )")
    print("nabor izmerjen pri viru ⊢ : definiatorna-knjiznica iztočnic " + str(n_def) +
          " ∧ slovar-slovenscine iztočnic " + str(n_slo) + " ( wc ∧ grep ⊢ )")
    print("izmera : " + str(len(besedilo)) + " znakov, " + str(besedilo.count("\n")) + " vrstic ; soočenja " +
          str(len(soocenja)) + " ( wc ⊢ )")
    for prim, predmet, znan in soocenja:
        print("soočeno poimensko : »" + prim + "«")
        print("  1. KAKOR KAJ? - kakšen je pravi predmet primerjave ⟨" + predmet + "⟩ ; zahteva iztočnico ( izrek vprašanja ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690 )")
        if znan:
            print("  2. KAJ JE ⟨" + predmet + "⟩? - bistvo živi pri viru ⊢ ( predmet v naboru izmerjen : definiatorna ∧ ali slovar, grep ⊢ )")
        else:
            print("  2. KAJ JE ⟨" + predmet + "⟩? - RUMENA pobuda iztočnice za ⟨" + predmet + "⟩ ( ⟨NE⟩ napaka ⊙ zanesljivost-po-izmeri σ 5809 : pobuda metanja v slovar )")
        print("  3. ZAKAJ JE ⟨" + predmet + "⟩? - svrha ni merilo slovarja : vprašanje izrečeno, odgovor je ⟡ ⚔ ( ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690 )")
    for vzorec, kovanec in obtozbe:
        print("obtožba poimensko : »" + vzorec + "« " + kovanec)
    if obtozbe:
        print("SEMAFOR : RDECA ( obtožbe " + str(len(obtozbe)) + " ⇒ NIHIL )")
        return 1
    if pobude:
        print("SUM pobud iztočnic + " + str(len(pobude)) + " izmera ⊙ ⟨SLOVNICA⇒SUM⟩ σ 6705 ( sum = merjen odstotek, ⟨ne⟩ obsodba )")
        print("SEMAFOR : RUMENA-SUM")
        return 2
    print("SEMAFOR : ZELENA ( vsi predmeti primerjav znani pri viru ⊢ )")
    return 0

def zapis(organ, besedilo):
    soocenja, obtozbe = sooc(besedilo)
    if obtozbe:
        P = organ if organ.startswith("/") else os.path.join(KOR, organ)
        gtik = _dt.datetime.now(_dt.UTC).strftime("%Y%m%dT%H%M%SZ")
        gp = os.path.join(P, ".geniza")
        pri = ""
        if os.path.isdir(gp):
            with open(os.path.join(gp, "KAKORKAJ-PADCI-" + gtik + "-priča-padca.md"), "w", encoding="utf-8") as f:
                f.write(besedilo if besedilo.endswith("\n") else besedilo + "\n")
            pri = " ; priča padca @.geniza/KAKORKAJ-PADCI-" + gtik + "-priča-padca.md"
        print("PREPREČITEV : obtožbe => NIHIL ( " + P + " nedotaknjen )" + pri +
              " ⊙ beseda primerjave brez predmeta je kip")
        return izhodi(besedilo, soocenja, obtozbe)
    r = subprocess.run(["bash", VRATA, "--vpis", organ],
                       input=besedilo if besedilo.endswith("\n") else besedilo + "\n",
                       text=True, capture_output=True)
    sys.stdout.write(r.stdout)
    if r.stdout and not r.stdout.endswith("\n"):
        print()
    return r.returncode

def samopreizkus():
    T = [0, 0, 0, 0, 0]
    s1, o1 = sooc("humor kot vic telesa ⊢")
    T[0] = 1 if (len(s1) == 1 and s1[0][2] and not o1) else 0
    s2, o2 = sooc("mir kakor cvetje je redek")
    T[1] = 1 if (len(s2) == 1 and not s2[0][2] and not o2) else 0
    s3, o3 = sooc("konec je kot.")
    T[2] = 1 if (len(o3) == 1 and "PREDMET-PRIMERJAVE" in o3[0][1] and not s3) else 0
    import shutil
    TD = os.path.join(DOM, ".geniza", "TEST-kakorkaj-" + str(os.getpid()))
    shutil.rmtree(TD, ignore_errors=True)
    o = os.path.join(TD, "o")
    os.makedirs(os.path.join(o, ".geniza"), exist_ok=True)
    with open(os.path.join(o, "KNOWLEDGE.md"), "w", encoding="utf-8") as f:
        f.write("telo\n")
    for i in (1, 2):
        with open(os.path.join(o, ".geniza", "PRED-DOTIKOM-" + str(i) + ".md"), "w") as f:
            f.write("g\n")
    prej = os.path.getsize(os.path.join(o, "KNOWLEDGE.md"))
    e4 = zapis(o, "cvet kot svetloba izrečen ⊢ TIK merjeno wc\n")
    T[3] = 1 if (e4 == 0 and os.path.getsize(os.path.join(o, "KNOWLEDGE.md")) > prej) else 0
    shutil.rmtree(TD, ignore_errors=True)
    besede, n_def, n_slo = nabor()
    T[4] = 1 if (n_def >= 100 and n_slo >= 1 and os.path.isfile(DEFIN) and os.path.isfile(SLOVAR)) else 0
    p = 5 - sum(T)
    print("SAMOPREIZKUS : vektorji 5 ( predmet-znan=" + str(T[0]) + " pobuda=" + str(T[1]) +
          " brez-predmeta=" + str(T[2]) + " zapis-siv=" + str(T[3]) + " nabor=" + str(T[4]) +
          " ), padci instrumenta " + str(p) + " ; nabor " + str(len(besede)) + " besed ( wc ⊢ )")
    print("SEMAFOR : " + ("ZELENA" if p == 0 else "RDECA"))
    return 0 if p == 0 else 1

def main(a):
    if a == ["--test"]:
        return samopreizkus()
    if len(a) >= 2 and a[0] == "--zapis":
        return zapis(a[1], sys.stdin.read())
    if a:
        besedilo = "\n".join(a)
        soocenja, obtozbe = sooc(besedilo)
        return izhodi(besedilo, soocenja, obtozbe)
    print("roke : TELESO... ⌇ --zapis ORGAN < VHOD ⌇ --test ; izhodi : 0 ZELENA ⌇ 2 RUMENA-SUM ( pobude ) ⌇ 1 RDECA ( NIHIL ) ⌇ 40")
    return 40

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
