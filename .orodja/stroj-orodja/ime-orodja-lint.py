#!/usr/bin/env python3
# ime-orodja-lint.py v1.0 — PREVERJALNIK SLOVNICE IMEN ORODIJ
# rod @rez 6995, 25. 11. 2026 ⊙ ukaz ⟡ VERBATIM ( nedotakljiva ):
# »USTVARIŠ ORODJA KI PREVERJAJO META PLASTI ZA SLOVNICO IN IMENA ORODIJ DA SO
# SLOVNIČNO KOREKTNA IN S TEM ZANESLJIVA?«
# prva vrata zakona orodil tri vrata @rez 6949 : slovnica imena telesa
# ( šumniki ne manjkajo, tujke poimensko gostje, crkot ×0 )
# meri znake-priče, ⟨ne⟩ popravljeno — vsak predeg = izbor ⟡ ⚔ ⊙ 2690
import sys, os, re, hashlib

SEDEZ = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(SEDEZ)

# priče-slovar gol⭢šumnik ( izmerjene rane registra 6949 IZBIRE, vsak pari ⊢ pri viru )
GOL_SUMNIK = {
    "sumnik": "šumnik", "sprozilec": "sprožilec", "zeton": "žeton",
    "uresnicivec": "uresničevalec", "vracilo": "vračilo", "dviznik": "dvignik",
    "transformuj": "transformator",
}
# tujke v imenih teles — gostje poimensko @domovanje-tujk, preimenovanje = ⚔ ⟡
TUJKE = ["lint", "box", "patch", "test", "seal", "eskalator", "canary",
         "worker", "hook", "merge", "queue", "check", "list"]
# imena domače izumene oblike z zapečeno definicijo ( priča organa stroj-orodja )
DOMACI_IZUMI = {"genizar", "sklanjatnik", "naglasnik", "fifo", "vrstnik",
                "tehtnica", "prevoznik", "kletkar", "vaba", "zid"}
# dovoljeni znaki imena telesa : gajica ( ascii + šumniki ) + pika + vezaj
CRKOT = re.compile(r"^[a-zčšž0-9\-]+\.(py|sh|yml|awk|tsv|md|json)$", re.IGNORECASE)
SEZNAM = re.compile(r"^[a-zčšž0-9\-]+$", re.IGNORECASE)


def preveri_ime(ime):
    """vrne seznam naborov ( vrata, ime, priča, kura )"""
    rane = []
    koren = os.path.splitext(ime)[0]
    deli = koren.replace("_", "-").split("-")
    # T1 GOL⭢ŠUMNIK : izpad šumnika proti priči-slovarju
    for d in deli:
        if d.lower() in GOL_SUMNIK:
            rane.append(("T1-SUMNIK", ime, d + " -> " + GOL_SUMNIK[d],
                         "preimenovanje po priči ⭢ izbor ⟡ ⚔"))
    # T2 TUJKA : tujka poimensko gostja, ⟨ne⟩ domača beseda
    for d in deli:
        if d.lower() in TUJKE:
            rane.append(("T2-TUJKA", ime, d, "gost poimensko @domovanje-tujk ; preimenovanje ⭢ izbor ⟡ ⚔"))
        elif d.lower() in DOMACI_IZUMI:
            pass  # domač izum z definicijo, čist
    # T3 CRKOT : znaki zunaj gajice v imenu
    if not CRKOT.match(ime) and not SEZNAM.match(koren):
        rane.append(("T3-CRKOT", ime, "znaki zunaj gajice v imenu",
                     "prečiščenje imena ⭢ izbor ⟡ ⚔"))
    return rane


def cenzus(pot=SEDEZ):
    telesa, rane = [], []
    for koren, _, datoteke in os.walk(pot):
        if ".geniza" in koren or "__pycache__" in koren:
            continue
        for d in sorted(datoteke):
            if d.lower() == "knowledge.md" or not re.search(r"\.(py|sh|yml|awk)$", d, re.IGNORECASE):
                continue
            telesa.append(d)
            rane.extend(preveri_ime(d))
    return telesa, rane


def samopreizkus():
    """⟨INOKULACIJA⟩ ⊙ tehtnica-orodij 6659 : čist trup Σ0 ⊢ ∧ ranjen trup poimensko ⊢"""
    cisti = preveri_ime("sklanjatnik.py")          # domač izum, gajica čista
    ranjeni = preveri_ime("sumnik-lint.py")         # izpad šumnika + tujka poimensko
    crkot = preveri_ime("sproz!lec.py")             # crkot zunaj gajice
    ok1 = len(cisti) == 0
    ok2 = sorted(r[0] for r in ranjeni) == ["T1-SUMNIK", "T2-TUJKA"]
    ok3 = any(r[0] == "T3-CRKOT" for r in crkot)
    print("SAMOPREIZKUS: cist Σ0 %s | ranjen trup Σ2 %s | crkot Σ1 %s | %s" % (
        "⊢" if ok1 else "⊥", "⊢" if ok2 else "⊥",
        "⊢" if ok3 else "⊥", "ZELENO" if (ok1 and ok2 and ok3) else "RDEČA"))
    return ok1 and ok2 and ok3


def main():
    if "--test" in sys.argv:
        return 0 if samopreizkus() else 1
    telesa, rane = cenzus()
    print("CENZUS IMEN ORODIJ : telesa Σ%d ⊢" % len(telesa))
    if not rane:
        print("ZELENO : rane Σ0 — vsa imena po prvim vratom slovnice ⊢")
        return 0
    print("RANJENO : rane Σ%d poimensko ( vsak predeg = izbor ⟡ ⚔ ⊙ 2690 ) :" % len(rane))
    for vrata, ime,Priča, kura in rane:
        print("  %s | %s | %s | %s" % (vrata, ime, Priča, kura))
    return 1


if __name__ == "__main__":
    sys.exit(main())
