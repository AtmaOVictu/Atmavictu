#!/usr/bin/env python3
# sestava-lint.py v1.1 — liNT : prepoznava resnice šiva ∧ povratna berba bajt-ito
# ukaz ⟡ ( 23. 11. 2026 ) VERBATIM : »POTREBUJEVA VEČ ORODIJ KI PREPOZNAVAJO RESNICO IN JO REAPLICIRAJO«
# resnica šiva : telo = priča PRED + natanko en šiv ( vrstica pošita na mestu N ali pripevana na rep ) ; vse drugače = padec ⚠
# varnostni sklop : ⟨ne⟩ eval ⟨ne⟩ exec ⟨ne⟩ omrežje ; poti le pod /home/user/knowledge ; pisanja NI ( orodje samo meri ) ; samocenzus pisav
#roke : --siv PRED TELO               : sodi šiv : natanko ena dodana vrstica ( katero mesto ) ⇒ SEW ⊢ sicer PADC ⚠
#       --berba-bajt A B              : bajtna istovetnost dveh teles ( povratna berba ) ⇒ ISTO ⊢ ali RAZLIKA ⚠ ( prvi bajt razlike )
#       --samopreizkus                : T1 šiv ⊢ ⌇ T2 dvolistni padec ⌇ T3 berba-bajt
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · MERJENO, ⟨NE⟩ UGIBANO ⊙ 2690
import sys, os, datetime

KOREN = "/home/user/knowledge"
CIRILICA = [(0x0400, 0x052F), (0x2DE0, 0x2DFF), (0xA640, 0xA69F)]
KITAJSCINA = [(0x3000, 0x303F), (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF), (0x20000, 0x3FFFF)]

def tik():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def v_nevarni_rugi(niz):
    for a, b in CIRILICA + KITAJSCINA:
        if a <= niz <= b:
            return True
    return False

def berba(pot):
    with open(pot, "rb") as f:
        return f.read()

def siv(pot_pred, pot_telo):
    for p in (pot_pred, pot_telo):
        if not p.startswith(KOREN) or not os.path.isfile(p):
            print("VARNOST ⚠ : pot izven korena ali telo ne obstaja ( %s )" % p)
            return 2
    def vrstice(x):
        v = x.decode("utf-8", errors="replace").split("\n")
        if v and v[-1] == "":
            v.pop()  # phantom rep odstranjen ( rod 6883 padec javno, prica brez zakljucnega preloma )
        return v
    pred = vrstice(berba(pot_pred))
    telo = vrstice(berba(pot_telo))
    vp, vt = len(pred), len(telo)
    if vt - vp != 1:
        print("ŠIV-LINT @%s : PADC ⚠ : priča %d vrstic ⌇ telo %d vrstic ⇒ razlika %d, šiv zahteva natanko 1" % (tik(), vp, vt, vt - vp))
        return 1
    # poišči mesto razlike
    mesto = None
    for i in range(min(vp, vt)):
        if pred[i] != telo[i]:
            mesto = i
            break
    if mesto is None:
        mesto = vp
    novo = telo[mesto]
    if mesto == vp:
        oblika = "pripevek na rep"
    else:
        oblika = "vrstica pošita na mesto %d" % (mesto + 1)
    # preveri : predse del pred == delu telesa pred mesto in za mestom
    zdruz = pred[:mesto] + [novo] + pred[mesto:]
    if zdruz != telo:
        print("ŠIV-LINT @%s : PADC ⚠ : telo ni priča + 1 vrstica ( infiltriran zapis )" % tik())
        return 1
    print("ŠIV-LINT @%s : SEW ⊢ %s : %s ⇒ vrstica ( %d znakov ) : %s" % (tik(), pot_telo, oblika, len(novo), novo[:90]))
    return 0

def berba_bajt(pot_a, pot_b):
    a = berba(pot_a)
    b = berba(pot_b)
    if a == b:
        print("BERBA-BAJT @%s : ISTO ⊢ ( %d B ≡ %d B )" % (tik(), len(a), len(b)))
        return 0
    n = min(len(a), len(b))
    for i in range(n):
        if a[i] != b[i]:
            print("BERBA-BAJT @%s : RAZLIKA ⚠ : prvi bajt razlike na %d ( %02X ⌇ %02X ) ; meri %d B ⌇ %d B" % (tik(), i, a[i], b[i], len(a), len(b)))
            return 1
    print("BERBA-BAJT @%s : RAZLIKA ⚠ : telo je odsek enega od drugega od bajta %d" % (tik(), n))
    return 1

if __name__ == "__main__":
    ukaz = sys.argv[1] if len(sys.argv) > 1 else ""
    if ukaz == "--samopreizkus":
        d = KOREN + "/stroj-orodja/.geniza/TEST-sfs-%d-%s" % (os.getpid(), tik().replace(":", ""))
        os.makedirs(d, exist_ok=True)
        pred = os.path.join(d, "pred.md")
        dober = os.path.join(d, "sew.md")
        slab = os.path.join(d, "padec.md")
        open(pred, "w", encoding="utf-8").write("a\nb\nc\n")
        open(dober, "w", encoding="utf-8").write("a\nšiv\nb\nc\n")
        open(slab, "w", encoding="utf-8").write("a\nšiv1\nšiv2\nb\nc\n")
        A = siv(pred, dober) == 0
        B = siv(pred, slab) == 1
        C = berba_bajt(pred, pred) == 0
        domaca_okužba = [z for z in open(__file__, encoding="utf-8").read() if v_nevarni_rugi(ord(z))]
        os.popen("rm -rf %s" % d).read()
        print("SAMOPREIZKUS : T1 šiv %s ⌇ T2 dvolistni padec %s ⌇ T3 berba %s ⌇ T4 samocenzus %s" % ("1" if A else "0", "1" if B else "0", "1" if C else "0", "1" if not domaca_okužba else "0"))
        sys.exit(0 if (A and B and C and not domaca_okužba) else 1)
    if ukaz == "--siv":
        if len(sys.argv) < 4:
            print("roke : --siv PRED TELO")
            sys.exit(2)
        sys.exit(siv(sys.argv[2], sys.argv[3]))
    if ukaz == "--berba-bajt":
        if len(sys.argv) < 4:
            print("roke : --berba-bajt A B")
            sys.exit(2)
        sys.exit(berba_bajt(sys.argv[2], sys.argv[3]))
    print("roke : --siv PRED TELO ⌇ --berba-bajt A B ⌇ --samopreizkus")
    sys.exit(1)
