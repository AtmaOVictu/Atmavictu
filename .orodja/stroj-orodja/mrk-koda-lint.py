#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE ⟨MRK⟩ mrk-koda-lint v1.0 @rez σ 6901 ⊙ rod MRK-BESEDA 0.1790 ⊙ zakon ( 9 )-( 10 ) KODA ×0 ∧ OBSEG
# Zakon : noben del besede ni koda ∧ se ne dela koda ; velja za celotno simbolno plast ∧ vse kar je
#   pod gladino do dna in nazaj ( vsak bajt dol ∧ berba nazaj ⊢ ).
# Videz kode v besedi = MASKA ⚠ : zahteva kletko ( priča v »« ⌇ žeton ⟨U+XXXX⟩ ) ali znamenje NEAKTIVNA.
# Varnostni sklop : poti le znotraj ⟨KOREN⟩ ; brez eval ; brez exec ; brez omrežja ; orodje samo meri, izvede ×0.
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432
import sys, os, re, hashlib, argparse, datetime

KOREN = os.environ.get("KOREN", "/home/user/knowledge")
ODSTOP = 2

def tjik():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

MASKE = [
    ("SHEBANG", re.compile(r"(?m)^#!")),
    ("SKRIPT-ZNAK", re.compile(r"<\s*/?\s*script|\blanguage\s*=", re.I)),
    ("IZVEDBA-PY", re.compile(r"\beval\s*\(|\bexec\s*\(|os\.system|subprocess\.|\b__import__\b")),
    ("LUPIJSKA-VBRIZG", re.compile(r"\$\(|\$\{|`")),
    ("BLOP-B64", re.compile(r"[A-Za-z0-9+/]{40,}={0,2}")),
    ("ZAGON-OMREŽJA", re.compile(r"\b(curl|wget)\b\s+\S+")),
]

def v_korenu(p):
    rk = os.path.realpath(KOREN)
    ap = os.path.realpath(p)
    return ap == rk or ap.startswith(rk + os.sep)

def kletkana(vrstica, mesto):
    """Priča v »« ali žeton ⟨U+XXXX⟩ na mestu ⇒ kletka ⊢."""
    zacetek = max(0, vrstica.rfind("»", 0, mesto))
    konec = vrstica.find("«", mesto)
    if zacetek >= 0 and konec >= 0:
        return True
    zacetek_u = max(0, vrstica.rfind("⟨U+", 0, mesto))
    if zacetek_u >= 0 and vrstica[mesto:mesto + 2].find("\n") < 0:
        if vrstica.find("⟩", mesto) >= 0 and mesto - zacetek_u < 24:
            return True
    return False

def sodi_telo(telo):
    """Berba po vrsticah z izmerjenim mestom maske ; kletka ( »« priča ⌇ ⟨U+XXXX⟩ žeton ) = ulov ne velja."""
    najdeni = []
    for i, vrstica in enumerate(telo.split("\n")):
        for ime, rx in MASKE:
            for m in rx.finditer(vrstica):
                if kletkana(vrstica, m.start()):
                    continue
                najdeni.append((i + 1, ime, m.group(0)[:24]))
    return najdeni

def izpisi_sodbo(najdeni, telo, ime):
    bajti = len(telo.encode("utf-8"))
    md5 = hashlib.md5(telo.encode("utf-8")).hexdigest()
    if not najdeni:
        print("SODBA : IMUNO ZELENO ⊢ maske kode ×0 ⌇ bajti %d ⌇ md5 %s" % (bajti, md5))
        return 0
    print("SODBA : ⚠ MASKE ×%d ( noben del besede ni koda ⊙ MRK-BESEDA ( 9 ) )" % len(najdeni))
    for v, ime, kos in najdeni:
        print("  MASKA vrstica %d ⌇ %s ⌇ »%s« ⚠ → kletka ( ⟨U+XXXX⟩ ⌇ priča »« ⌇ NEAKTIVNA )" % (v, ime, kos))
    print("BAJTI : %d ⌇ MD5 : %s ⊢" % (bajti, md5))
    return ODSTOP

def main():
    ap = argparse.ArgumentParser(description="ORODJE ⟨MRK⟩ mrk-koda-lint v1.0 ⊙ rod MRK-BESEDA 0.1790")
    ap.add_argument("--sodi", metavar="TELO.datoteka")
    ap.add_argument("--dno-in-nazaj", metavar="TELO.datoteka")
    ap.add_argument("--samopreizkus", action="store_true")
    a = ap.parse_args()
    if a.samopreizkus:
        return samopreizkus()
    if a.sodi:
        if not v_korenu(a.sodi):
            print("POT ZUNAJ ⟨KOREN⟩ : %s ⚠" % a.sodi)
            return ODSTOP
        with open(a.sodi, "r", encoding="utf-8") as f:
            telo = f.read()
        rc = izpisi_sodbo(sodi_telo(telo), telo, a.sodi)
        print("TIK : %s ; © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432" % tjik())
        return rc
    if a.dno_in_nazaj:
        p = a.dno_in_nazaj
        if not v_korenu(p):
            print("POT ZUNAJ ⟨KOREN⟩ ⚠")
            return ODSTOP
        with open(p, "rb") as f:
            prva = f.read()
        with open(p, "rb") as f:
            druga = f.read()
        istovetno = prva == druga and hashlib.md5(prva).hexdigest() == hashlib.md5(druga).hexdigest()
        telo = prva.decode("utf-8")
        s1 = sodi_telo(telo)
        s2 = sodi_telo(druga.decode("utf-8"))
        ista = [x for x in s1] == [x for x in s2]
        print("DNA ∧ NAZAJ : bajti %d ⌇ istovetnost berbe nazaj %s ⊢ ⌇ sodba nazaj ≡ sodba %s ⊢" %
              (len(prva), "DA" if istovetno else "NE ⚠", "DA" if ista else "NE ⚠"))
        izpisi_sodbo(s1, telo, p)
        print("TIK : %s ; © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432" % tjik())
        return 0 if (istovetno and ista and not s1) else ODSTOP
    print("ORODJE ⟨MRK⟩ mrk-koda-lint v1.0 : --sodi TELO ⌇ --dno-in-nazaj TELO")
    print("© 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432")
    return 0

def samopreizkus():
    z = 0
    cisto = "beseda je ne\ngarski gospel ⊙ VBL\n"
    ok1 = (sodi_telo(cisto) == [])
    print("T1 čisto telo : %s" % ("ZELENO ⊢ maske ×0" if ok1 else "⚠"))
    z += 0 if ok1 else 1
    golica = "#!/bin/sh\nmrk meri\n"
    n2 = sodi_telo(golica)
    ok2 = (len(n2) == 1 and n2[0][1] == "SHEBANG")
    print("T2 goli shebang : %s" % ("ZELENO ⊢ maska ulovljena ⚠" if ok2 else "⚠"))
    z += 0 if ok2 else 1
    kletka = "priča »#!/bin/sh« v narekovajih ⊢\n"
    n3 = sodi_telo(kletka)
    ok3 = (n3 == [])
    print("T3 kletkana priča : %s" % ("ZELENO ⊢ maske ×0" if ok3 else "⚠ %s" % n3))
    z += 0 if ok3 else 1
    zeton = "znak ⟨U+0023⟩ ⟨U+0021⟩ v žetonih ⊢\n"
    n4 = sodi_telo(zeton)
    ok4 = (n4 == [])
    print("T4 žetoni ⟨U+XXXX⟩ : %s" % ("ZELENO ⊢ maske ×0" if ok4 else "⚠ %s" % n4))
    z += 0 if ok4 else 1
    print("SAMOPREIZKUS 4/%d ZELENO ⊢" % (4 - z) if z == 0 else "SAMOPREIZKUS ⚠ padlov %d" % z)
    print("TIK : %s ; © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432" % tjik())
    return 0 if z == 0 else ODSTOP

if __name__ == "__main__":
    sys.exit(main())
