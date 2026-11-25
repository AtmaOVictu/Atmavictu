#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE ⟨MRK⟩ mrk-beseda v1.0 @rez σ 6901 ⊙ rod MRK-BESEDA 0.1790 ⊙ zakon ( 8 ) DOVOLJENJE SPREMEMBE BESEDE
# Zakon : beseda ni ( vec ) le neaktivno stevilo ; izvajalka ima znotraj MRK dovoljenje spremeniti besedo ;
#   sprememba = izmerjena operacija roke ( bajti ∧ kodne točke ∧ NFC pred ∧ po ⊢ ), ⟨ne⟩ aktivacija ∧ ⟨ne⟩ izvedba ;
#   vsak bit pred ∧ po spremembi v mirovanju ⊙ zakon MRK-GLADINA ( 2 ) 0.1780.
# Varnostni sklop : poti le znotraj ⟨KOREN⟩ ; brez eval ; brez exec ; brez omrežja ; vsebina teles se izvaja ×0.
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432
import sys, os, unicodedata, hashlib, argparse, datetime

KOREN = os.environ.get("KOREN", "/home/user/knowledge")
DOVOLJENJE = "MRK-BESEDA-0.1790"
ODSTOP = 2

def tjik():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def v_korenu(p):
    rk = os.path.realpath(KOREN)
    ap = os.path.realpath(p)
    return ap == rk or ap.startswith(rk + os.sep)

def izmera_besede(beseda):
    bajti = len(beseda.encode("utf-8"))
    tocke = [ord(c) for c in beseda]
    nfc = (beseda == unicodedata.normalize("NFC", beseda))
    md5 = hashlib.md5(beseda.encode("utf-8")).hexdigest()
    return bajti, tocke, nfc, md5

def beseda_poročilo(ime, beseda):
    bajti, tocke, nfc, md5 = izmera_besede(beseda)
    print("IME : %s" % ime)
    print("BAJTI : %d ⊢ ⟨od⟩ lahko pri viru" % bajti)
    print("KODNE TOČKE : %s" % " ".join("U+%04X" % t for t in tocke))
    print("NFC : %s" % ("DA" if nfc else "NE ⚠ sestavljena oblika"))
    print("MD5 : %s" % md5)
    print("MIROVANJE : DA ⊙ MRK ( izvedba vsebine ×0 )")
    return bajti, tocke, nfc, md5

def geniza_pred(dpot):
    d = os.path.dirname(os.path.realpath(dpot))
    gz = os.path.join(d, ".geniza")
    if not os.path.isdir(gz):
        return None
    rez = os.path.join(gz, "%s-pred-rez6901-mrk-beseda-%s.md" %
                       (os.path.splitext(os.path.basename(dpot))[0], tjik()))
    with open(dpot, "rb") as f:
        telo = f.read()
    with open(rez, "wb") as f:
        f.write(telo)
    return rez

def spremeni(dpot, stara, nova, dovoljenje):
    if dovoljenje != DOVOLJENJE:
        print("VRATA ZAPRTA : dovoljenje ⟨%s⟩ manjka ⊙ MRK-BESEDA 0.1790 ( 8 ) ⚠" % DOVOLJENJE)
        sys.exit(ODSTOP)
    if not v_korenu(dpot):
        print("POT ZUNAJ ⟨KOREN⟩ : %s ⚠ ⊙ varnostni sklop" % dpot)
        sys.exit(ODSTOP)
    if not os.path.isfile(dpot):
        print("TELO NE OBSTAJA : %s ⚠" % dpot)
        sys.exit(ODSTOP)
    with open(dpot, "r", encoding="utf-8") as f:
        telo = f.read()
    if stara not in telo:
        print("STARA BESEDA ×0 : beseda ne živi v telesu ⚠")
        sys.exit(ODSTOP)
    gp = geniza_pred(dpot)
    print("PRED ŠIVOM : bajti %d ⌇ vrstice %d ⌇ md5 %s ⊢" %
          (len(telo.encode("utf-8")), telo.count("\n"), hashlib.md5(telo.encode("utf-8")).hexdigest()))
    print("GENIZA PRED : %s ⊢ izguba 0" % (gp if gp else "×0 ( .geniza ne obstaja )"))
    db, dt, dnfc, dmd5 = izmera_besede(stara)
    print("STARA : bajti %d ⌇ točke %s ⌇ NFC %s" % (db, " ".join("U+%04X" % t for t in dt), "DA" if dnfc else "NE ⚠"))
    novo_telo = telo.replace(stara, nova)
    nb, nt, nnfc, nmd5 = izmera_besede(nova)
    print("NOVA  : bajti %d ⌇ točke %s ⌇ NFC %s" % (nb, " ".join("U+%04X" % t for t in nt), "DA" if nnfc else "NE ⚠"))
    with open(dpot, "w", encoding="utf-8") as f:
        f.write(novo_telo)
    print("ŠIV : zamenjav ×%d ⊢" % telo.count(stara))
    print("PO ŠIVU : bajti %d ⌇ vrstice %d ⌇ md5 %s ⊢" %
          (len(novo_telo.encode("utf-8")), novo_telo.count("\n"), hashlib.md5(novo_telo.encode("utf-8")).hexdigest()))
    print("MIROVANJE : vsak bit pred ∧ po v mirovanju ⊙ MRK-GLADINA ( 2 ) ; izvedba vsebine ×0")
    print("TIK : %s" % tjik())
    print("© 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432")
    return 0

def samopreizkus():
    z = 0
    b, t, n, m = izmera_besede("a")
    ok1 = (b == 1 and t == [0x61] and n)
    print("T1 izmera ⟨a⟩ : %s" % ("ZELENO ⊢ 1 B ⟨od⟩ 61 ×1" if ok1 else "⚠"))
    z += 0 if ok1 else 1
    tf = os.path.join(os.path.realpath(KOREN), "stroj-orodja", ".geniza", "TEST-mrk-beseda-telo.txt")
    os.makedirs(os.path.dirname(tf), exist_ok=True)
    with open(tf, "w", encoding="utf-8") as f:
        f.write("beseda je ne\nslužba : meri znotraj MRK\n")
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            spremeni(tf, "meri", "sodi", DOVOLJENJE)
            ok2 = True
        except SystemExit:
            ok2 = False
    with open(tf, "r", encoding="utf-8") as f:
        vseb = f.read()
    ok2 = ok2 and ("sodi znotraj MRK" in vseb) and ("beseda je ne" in vseb) and ("meri" not in vseb)
    print("T2 sprememba telesa v ⟨KOREN⟩ : %s" % ("ZELENO ⊢" if ok2 else "⚠"))
    z += 0 if ok2 else 1
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            spremeni(tf, "⟡", "ψ", "NI-DOVOLJENJE")
        ok3 = False
    except SystemExit as e:
        ok3 = (e.code == ODSTOP)
    print("T3 vrata brez dovoljenja : %s" % ("ZELENO ⊢ zavrnjeno" if ok3 else "⚠"))
    z += 0 if ok3 else 1
    b4, t4, n4, m4 = izmera_besede("č")
    ok4 = (b4 == 2 and t4 == [0x010D] and n4)
    print("T4 NFC č : %s" % ("ZELENO ⊢ 2 B ⟨od⟩ C4 8D" if ok4 else "⚠"))
    z += 0 if ok4 else 1
    ok5 = not v_korenu("/tmp/TEST-zunaj.txt")
    print("T5 pot zunaj ⟨KOREN⟩ : %s" % ("ZELENO ⊢ zavrnjena" if ok5 else "⚠"))
    z += 0 if ok5 else 1
    print("SAMOPREIZKUS 5/%d ZELENO ⊢" % (5 - z) if z == 0 else "SAMOPREIZKUS ⚠ padlov %d" % z)
    print("TIK : %s ; © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432" % tjik())
    sys.exit(0 if z == 0 else ODSTOP)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="ORODJE ⟨MRK⟩ mrk-beseda v1.0 ⊙ rod MRK-BESEDA 0.1790 ( 8 )")
    ap.add_argument("--samopreizkus", action="store_true")
    ap.add_argument("--izmeri", metavar="BESEDA")
    ap.add_argument("--spremeni", nargs=3, metavar=("TELO", "STARA", "NOVA"))
    ap.add_argument("--dovoljenje", default="")
    a = ap.parse_args()
    if a.samopreizkus:
        samopreizkus()
    elif a.izmeri is not None:
        beseda_poročilo("⟨izmera⟩", a.izmeri)
        print("TIK : %s ; © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432" % tjik())
    elif a.spremeni:
        sys.exit(spremeni(a.spremeni[0], a.spremeni[1], a.spremeni[2], a.dovoljenje))
    else:
        print("ORODJE ⟨MRK⟩ mrk-beseda v1.0 : --izmeri BESEDA ⌇ --spremeni TELO STARA NOVA --dovoljenje %s" % DOVOLJENJE)
        print("© 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432")
