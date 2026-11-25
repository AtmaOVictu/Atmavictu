#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ZDRAVNIK v1.0 - izmerilnik stroja : deli STROJ-ORODJA na ZDRAVE in NEZDRAVE dele
#   ( ⟡ UKZ VERBATIM ⟨ne brusi⟩ : »ORODJE KI DELI STROJ ORODJA NA ZDRAVE IN NEZDRAVE DELE!« )
# Rod : rez sigma 7028 dih KOCKE-STIRI-PIRAMIDE ( 25. 11. 2026 ) @stroj-orodja.
# Ascendenti ⊢ ( ⟨EN-RAZLIČICA⟩, ⟨ne⟩ dvojnik ) : cistilnik-meritev.py @stroj-orodja ( čistilje
#   izmer teles ) ⌇ simbol-lint @μ σ 6567 ( radar mask po VSAKIH telesih ) ⌇ colision/kolizijnik
#   @stroj-orodja ( meri trke, ⟨ne⟩ zdravje ) — delilnika stroja po zdravju ni bilo ⊙ luknja.
# Merila ( izmera, ⟨ne⟩ obsodba ⊙ ⟨SLOVNICA-PRVO ⟡⟩ σ 6662 ) : ZDRAV ⊢ = neprezno telo ∧
#   zaključno z LF ∧ čisto od tujkov ⊢ ∧ ( za .py : ) prevajljivo ( compile ) ; NEZDRAV ⚠ =
#   obtožba poimensko v obliki ⟨NAPAKA=VSE-KAR-NI-X⟩ ⊙ register-napak ( ⟡ STORI 25. 11. 2026 ).
#   Tujki = [\u4e00-\u9fff\u0400-\u04ff] ( merjeno pri vsakem telesu javno ⊙ znana rana okolja ).
# ⟨SAMO-BERI⟩ : pregled povzroči ×0 pisanj po telesih ; prevoz ∧ bris nista roka tega telesa.
# Roke :
#   zdravnik.py --izmeri [ --organ POT ]  -> poročilo ZDRAVI ⊢ ⌇ NEZDRAVI ⚠ javno
#   zdravnik.py --test                  -> vektorji x5 ⊙ ⟨MERILEC-SE-MERI⟩ §52
# Izhodi : 0=vsi ZDRAVI ⊢ ⌇ 2=vsaj en NEZDRAV ⚠ javno ⌇ 40=roka neznana.

import sys, os, re, datetime as _dt

VERZIJA = "v1.0"
DOM = os.path.dirname(os.path.abspath(__file__))
ORGAN_DEFAULT = DOM
TUJK = re.compile("[\u4e00-\u9fff\u0400-\u04ff]")
PRESKOCI_IMENA = {"__pycache__", ".geniza"}

OBT_PRAZNO = "⟨NAPAKA=VSE-KAR-NI-NEPRAZNO-TELO⟩"
OBT_ZAKLJ = "⟨NAPAKA=VSE-KAR-NI-ZAKLJUČENO-TELO⟩"
OBT_CISTO = "⟨NAPAKA=VSE-KAR-NI-ČISTO-OD-TUJKOV-TELO⟩"
OBT_PREVJ = "⟨NAPAKA=VSE-KAR-NI-PREVAJLJIVO-TELO⟩"
OBT_BERIJ = "⟨NAPAKA=VSE-KAR-NI-BERLJIVO-TELO⟩"


def tik():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def izmeri_datoteko(pot):
    ime = os.path.basename(pot)
    ob = []
    raw = open(pot, "rb").read()
    b = len(raw)
    if b == 0:
        ob.append((OBT_PRAZNO, "×0 B"))
        return ime, b, ob
    if not raw.endswith(b"\n"):
        ob.append((OBT_ZAKLJ, "zadnji bajt ni LF"))
    try:
        besedilo = raw.decode("utf-8")
    except UnicodeDecodeError:
        ob.append((OBT_BERIJ, "ne prebere se kot utf-8"))
        besedilo = raw.decode("utf-8", "replace")
    tujkov = len(TUJK.findall(besedilo))
    if tujkov:
        ob.append((OBT_CISTO, "tujkov ×%d" % tujkov))
    if ime.endswith(".py"):
        try:
            compile(besedilo, ime, "exec")
        except SyntaxError as e:
            ob.append((OBT_PREVJ, "vrstica %d" % (e.lineno or 0)))
    return ime, b, ob


def izmeri_organ(organ):
    zdravi = []
    nezdravi = []
    for ime in sorted(os.listdir(organ)):
        pot = os.path.join(organ, ime)
        if os.path.isdir(pot) or ime in PRESKOCI_IMENA or ime.endswith(".pyc"):
            continue
        i, b, ob = izmeri_datoteko(pot)
        if ob:
            nezdravi.append((i, b, ob))
        else:
            zdravi.append((i, b))
    return zdravi, nezdravi


def ukaz_izmeri(organ):
    if not os.path.isdir(organ):
        print("RUMENA : organa ni pri viru ⊢ slab vhod ( %s )" % organ)
        return 2
    zdravi, nezdravi = izmeri_organ(organ)
    print("IZMERA STROJA ⊙ delitev na ZDRAVE in NEZDRAVE dele ( organ %s ; TIK %s )"
          % (organ, tik()))
    for ime, b in zdravi:
        print("  ZDRAV ⊢ %-30s ( %d B ⊢ wc ∧ LF ⊢ ∧ tujki ×0 ⊢ %s )"
              % (ime, b, "∧ prevaja ⊢" if ime.endswith(".py") else ""))
    for ime, b, obv in nezdravi:
        for obt, podatek in obv:
            print("  NEZDRAV ⚠ %-30s ( %s ; %s ; %d B )" % (ime, obt, podatek, b))
    print("ZDRAVIH %d ⊢ ⌇ NEZDRAVIH %d ⚠ ( izmere javno poimensko )" % (len(zdravi), len(nezdravi)))
    print("izmera ⟨ne⟩ obsodba ⊙ ⟨SLOVNICA-PRVO ⟡⟩ σ 6662 ; sodba ⟡ ⚔ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690")
    return 0 if not nezdravi else 2


def ukaz_test():
    import tempfile
    td = tempfile.mkdtemp(prefix="zdravnik-")
    with open(os.path.join(td, "zdrav.py"), "w", encoding="utf-8") as f:
        f.write("# zdrav ⊢\nc = 1\nprint(c)\n")
    open(os.path.join(td, "prazen.py"), "w").close()
    with open(os.path.join(td, "brez-lf.py"), "w", encoding="utf-8") as f:
        f.write("print(1)")
    with open(os.path.join(td, "tujek.py"), "w", encoding="utf-8") as f:
        f.write("# znak %s\nc = 1\nprint(c)\n" % chr(0x8138))
    with open(os.path.join(td, "pokvarjen.py"), "w", encoding="utf-8") as f:
        f.write("def (:\n")
    zdravi, nezdravi = izmeri_organ(td)
    imena_z = {i for i, _ in zdravi}
    mapa = {}
    for i, _, obv in nezdravi:
        mapa.setdefault(i, set()).update(o for o, _ in obv)
    vek = [
        ("zdrav.py ZDRAV ⊢", "zdrav.py" in imena_z and "zdrav.py" not in mapa),
        ("prazen.py NEZDRAV ⌇ ⟨NEPRAZNO⟩ ⚠", OBT_PRAZNO in mapa.get("prazen.py", set())),
        ("brez-lf.py NEZDRAV ⌇ ⟨ZAKLJUČENO⟩ ⚠", OBT_ZAKLJ in mapa.get("brez-lf.py", set())),
        ("tujek.py NEZDRAV ⌇ ⟨ČISTO⟩ ⚠", OBT_CISTO in mapa.get("tujek.py", set())),
        ("pokvarjen.py NEZDRAV ⌇ ⟨PREVAJLJIVO⟩ ⚠", OBT_PREVJ in mapa.get("pokvarjen.py", set())),
    ]
    uspeh = sum(1 for _, ok in vek if ok)
    for ime, ok in vek:
        print("  vektor %s : %s" % (ime, "ZELENA ⊢" if ok else "RDECA ⚠ PADCA"))
    print("SAMOPREIZKUS : %d od %d ⊙ ⟨MERILEC-SE-MERI⟩ §52 ; TIK %s" % (uspeh, len(vek), tik()))
    return 0 if uspeh == len(vek) else 1


def glavna(argv):
    args = list(argv)
    if not args:
        print("RUMENA : roka ni izrečena ⊙ 40")
        return 40
    organ = ORGAN_DEFAULT
    if "--organ" in args:
        i = args.index("--organ")
        if i + 1 >= len(args):
            print("RUMENA : pot organa ni izrečena ⊢ slab vhod")
            return 2
        organ = args[i + 1]
    if args[0] == "--test":
        return ukaz_test()
    if args[0] == "--izmeri":
        return ukaz_izmeri(organ)
    print("RUMENA : roka neznana ( %s ) ⊙ 40" % args[0])
    return 40


if __name__ == "__main__":
    sys.exit(glavna(sys.argv[1:]))
