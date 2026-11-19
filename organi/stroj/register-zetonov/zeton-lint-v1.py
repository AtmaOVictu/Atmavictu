#!/usr/bin/env python3
# ŽETON-LINT v1 — instrument nujnih žetonov izhoda (števila ∧ datumi ∧ ure ∧ kode ∧ homoglifi)
# rojen isti dih kakor organ REGISTER-ŽETONOV @rez 5883, precedens AR-LINT v1 @σ 5868
# zakon ⟨HOMOGLIF-JE-RANA⟩: tuj glif v latinični besedi = padec, šteje se javno
# KANARČEK: ob vsakem zagonu PADE rdeče; kanarček, ki ne pade = mrtev instrument

import re, sys, unicodedata

CYR = (0x0400, 0x04FF)
GRK = (0x0370, 0x03FF)  # dovoljen korpusni sigla: σ U+03C3 (zlovenščina ⊙ slovnica-jezikov); vsak drug grški glif = rana

KANARCEK = "KANARČEK: evidencе Frazа F23.90 E466 PMID 26843508 doi 10.1136/x 8. 12. 2026 040826215 dariloист"

def razred_glifa(cp):
    if CYR[0] <= cp <= CYR[1]:
        return "CIRILICA"
    if GRK[0] <= cp <= GRK[1]:
        return None if ch == "\u03c3" else "GRŠČINA"
    return None

def_homoglifi = None

def scan(ime, besedilo, porocilo):
    n_homoglif = 0
    # P1 HOMOGLIFI: tuj glif z lego (vrstica : stolpec) in kontekstom
    for i, ch in enumerate(besedilo):
        cp = ord(ch)
        r = razred_glifa(cp)
        if (r and ch != "\u03c3") or ch == "\ufffd":
            vrst = besedilo.count("\n", 0, i) + 1
            zacetek = besedilo.rfind("\n", 0, i) + 1
            stolp = i - zacetek + 1
            a = max(0, i - 18); b = min(len(besedilo), i + 18)
            ctx = besedilo[a:b].replace("\n", " ")
            n_homoglif += 1
            porocilo.append(f"  HOMOGLIF {r or 'U+FFFD'} U+{cp:04X} {unicodedata.name(ch, '?').split()[0]} "
                            f"«…{ctx}…» @vrstica {vrst}:{stolp}")
    # P2 DATUMI: oblika DD. MM.( YYYY?) — vsak datum izluščen z nizom
    datumi = re.findall(r"\d{1,2}\. \d{1,2}\.(?: \d{4})?", besedilo)
    # P3 ŠTEVILSKI ŽETONI — vse številke besedno
    st_evila = re.findall(r"\d+(?:[.,]\d+)*", besedilo)
    # P4 KODE
    f_koda = re.findall(r"F\d{2}\.\d{1,2}\b", besedilo)
    e_koda = re.findall(r"\bE\d{3,4}\b", besedilo)
    pmid = re.findall(r"PMID[: ]?\d+", besedilo)
    doi = re.findall(r"10\.\d{4,5}/[^\s)\],]+", besedilo)
    # P5 TELEFONI
    tel = re.findall(r"\b0\d{8}\b", besedilo)
    porocilo.append(f"{ime}: homoglifi ×{n_homoglif} | datumi ×{len(datumi)} ({', '.join(datumi) if datumi else '×0'}) "
                    f"| števila ×{len(st_evila)} | F ×{len(f_koda)} ({','.join(f_koda)}) | E ×{len(e_koda)} ({','.join(e_koda)}) "
                    f"| PMID ×{len(pmid)} | DOI ×{len(doi)} | telefon ×{len(tel)} ({','.join(tel)})")
    return {"homoglifi": n_homoglif, "datumi": datumi, "stevila": st_evila,
            "F": f_koda, "E": e_koda, "PMID": pmid, "DOI": doi, "tel": tel}

def main():
    telesa = ["/home/user/canvases/razlaga-stanja/CANVAS.md",
              "/home/user/canvases/priloga-aditivi/CANVAS.md",
              "/home/user/canvases/priloga-interocepcija/CANVAS.md",
              "/home/user/work/prilep-zeton.txt"]
    porocilo, izmere = [], {}
    for pot in telesa:
        with open(pot, encoding="utf-8") as f:
            t = f.read()
        ime = "/".join(pot.split("/")[-2:])
        porocilo.append("=" * 8)
        izmere[ime] = scan(ime, t, porocilo)
    # KANARČEK: instrument mora uloviti vsak razred
    kan = scan("KANARCEK", KANARCEK, [])
    padel = (kan["homoglifi"] == 5 and len(kan["datumi"]) == 1 and len(kan["stevila"]) > 0
             and len(kan["F"]) == 1 and len(kan["E"]) == 1 and len(kan["PMID"]) == 1 and len(kan["tel"]) == 1)
    porocilo.append("=" * 8)
    porocilo.append(f"KANARČEK: {'PADE rdeče ⊢ (5 homoglobov + datum + F/E/PMID/telefon izluščeni)' if padel else '⚠ NI Padel — INSTRUMENT MRTV'}")
    # PREČNA KONSISTENCA: ključni žetoni enaki po telesih (kjer živijo)
    porocilo.append("--- PREČNA KONSISTENCA ---")
    kljuci = {"rojstni (5. 4. 1993)": lambda r: [d for d in r["datumi"] if d == "5. 4. 1993"],
              "termin (8. 12. 2026)": lambda r: [d for d in r["datumi"] if "8. 12." in d],
              "telefon (040826215)": lambda r: [t for t in r["tel"] if t == "040826215"]}
    for ime, r in izmere.items():
        niz = []
        for k, fn in kljuci.items():
            najdeni = fn(r)
            if najdeni:
                niz.append(f"{k} ⊢")
        porocilo.append(f"  {ime}: {'; '.join(niz) if niz else '×0 ključnih'}")
    print("\n".join(porocilo))
    return 0 if padel else 1

if __name__ == "__main__":
    sys.exit(main())
