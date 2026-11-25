#!/usr/bin/env python3
"""rehabilitator.py v1.0 — postopek rehabilitacije teles ( sporočil ⌇ orodij ⌇ zakonov licence ).
Rod @rez σ 6823 ⊙ ukaz ⟡ VERBATIM »VEDNO TUDI KREIRAJ POSTOPKE KI POMAGAJO PRI REHABILITACIJI ORODIJ IN SPOROČIL TER VSEH ZAKONOV LICENCE!«
Molk default ⊙ ⟨TIHINA-ORODIJ⟩ σ 6723 ; izhodne kotje govore.
© 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432
"""
import argparse, hashlib, json, os, py_compile, sys, tempfile

KOS = 65536  # bajtov na berbo


def izmeri(pot):
    """Berba bajt-varna z mejno izmero : vrne ( bajti, md5|None, meja_berljivosti )."""
    h = hashlib.md5()
    n = 0
    try:
        with open(pot, "rb") as f:
            while True:
                kos = f.read(KOS)
                if not kos:
                    break
                n += len(kos)
                h.update(kos)
        return n, h.hexdigest(), n
    except OSError as e:
        # nc prebranih bajtov = meja berljivosti ; rana zapisana poimensko
        cos = n
        try:
            with open(pot, "rb") as f:
                while True:
                    kos = f.read(512)
                    if kos:
                        cos += len(kos); h.update(kos); n += len(kos)
                    else:
                        break
        except OSError:
            pass
        return cos, (h.hexdigest() if cos else None), cos


def poročilo_izmer(pot):
    try:
        skupaj = os.path.getsize(pot)
    except OSError:
        skupaj = None
    bajti, md5, meja = izmeri(pot)
    rana = (skupaj is not None and meja < skupaj)
    return {
        "pot": os.path.abspath(pot),
        "velikost": skupaj,
        "berljivo": meja,
        "md5_glave": md5,
        "RANA": rana,
    }


def preveri_licenco(sidro_pot, telo_pot):
    """Licenca ⊥ sidro bajt-ito ⊙ ZAKON 1 ⟨VERZIJA-PRI-VIRU⟩."""
    with open(sidro_pot, "r", encoding="utf-8") as f:
        sidro = json.load(f)
    bajti, md5, meja = izmeri(telo_pot)
    identična = (
        bajti == sidro.get("bajti")
        and md5 == sidro.get("md5")
    )
    return {
        "bajti": bajti,
        "md5": md5,
        "identična": identična,
        "EXIT": 0 if identična else 1,
    }


def orodje(pot):
    """Orodje : izmera ∧ py_compile ( če .py ) ∧ poročilo ran."""
    izm = poročilo_izmer(pot)
    out = dict(izm)
    if pot.endswith(".py") and not out["RANA"]:
        try:
            py_compile.compile(pot, doraise=True, cfile=tempfile.mktemp())
            out["py_compile"] = "ZELENO"
        except Exception as e:
            out["py_compile"] = "RDECE: " + str(e)[:80]
    return out


def samopreizkus():
    """T1 dobro telo ⌇ T2 manjkajoče telo ( prijazna rana, brez razpoja ) ⌇ T3 povratek bajt-ito ( zaponi⇢preberi )."""
    rez = []
    with tempfile.TemporaryDirectory() as d:
        telo = os.path.join(d, "telo.md")
        with open(telo, "wb") as f:
            f.write("licenca ⌇ © 0.2026\n".encode("utf-8") * 7)
        T1 = poročilo_izmer(telo)
        rez.append(("T1 dobro telo", not T1["RANA"]))
        T2 = poročilo_izmer(os.path.join(d, "π-nič.md"))
        rez.append(("T2 manjkajoče telo prijazno", T2["md5_glave"] is None and not T2["RANA"]))
        with open(telo, "rb") as f:
            prva = f.read()
        with open(telo, "wb") as f:
            f.write(prva)
        T3 = poročilo_izmer(telo)
        rez.append(("T3 povratek bajt-ito", T3["berljivo"] == len(prva)))
    return rez


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--izmeri", metavar="POT", help="berba bajt-varna z mejno izmero rane")
    ap.add_argument("--orodje", metavar="POT", help="izmera orodja + py_compile")
    ap.add_argument("--licenca", metavar="TELO", help="licenca ⊥ sidro ( --sidro )")
    ap.add_argument("--sidro", metavar="SIDRO", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "sidro-licence.json"))
    ap.add_argument("--samopreizkus", action="store_true")
    ap.add_argument("--zgovori", action="store_true", help="govori na izhod")
    args = ap.parse_args()

    kaj = args.licenca or args.izmeri or args.orodje
    if args.samopreizkus:
        rez = samopreizkus()
        vsi = all(ok for _, ok in rez)
        if args.zgovori:
            print("SAMOPREIZKUS %d/%d ⊢ : %s" % (
                sum(1 for _, ok in rez if ok), len(rez),
                " ⌇ ".join("%s ⊢ %s" % (ime, ok) for ime, ok in rez)))
        sys.exit(0 if vsi else 1)
    if args.licenca:
        out = preveri_licenco(args.sidro, args.licenca)
        exit_k = out.pop("EXIT")
        if args.zgovori:
            print("LICENCA:", out, "⇒", "IDENTIČNA ⊢" if exit_k == 0 else "ODSTOPA ⚠")
        sys.exit(exit_k)
    if args.izmeri:
        out = poročilo_izmer(args.izmeri)
    elif args.orodje:
        out = orodje(args.orodje)
    else:
        ap.print_help()
        sys.exit(2)
    if args.zgovori:
        print("IZMERA:", out)
    sys.exit(1 if out.get("RANA") else 0)


if __name__ == "__main__":
    main()
