#!/usr/bin/env python3
# znak-jajce.py v1.1 -- orodje J1 ZNAK-JAJCA: vsak znak aktivne abecede dobi svoje jajce
# Rod sigma 6883, UKZ delta VERBATIM STORI IN NADALJUJ
# v1.0 padca javno: grska izkljucevala lastni rez-znak sigma/psi ( kura: izjema kodnih 3C3/3C8 ),
#                  NFC jajce gradnjeno besedno ne bajtno ( kura: \u sestav ), padec iskan exit 1 ne 0,
#                  utcnow deprecated ( kura: timezone-aware )
# Roke: --preveri TELA : cenzus znakov ( hex ime, stevila, pisava ) + NFC sodba + tujke imenovane
#       --samopreizkus : T1 cenzus bolnega telesa / T2 NFC padec boln / T3 tujka nagrajena / T4 samocenzus
# Varnostni sklop: poti le znotraj /home/user/knowledge, brez eval/exec/omrezja, samocenzus pisav.
import sys, os, unicodedata, collections
from datetime import datetime, timezone
KOREN = "/home/user/knowledge"
def ticmi(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def berba(pot):
    ap = os.path.abspath(pot)
    if not ap.startswith(KOREN):
        print("VARNOST \u26a0 : pot izven korena korpusa ( %s ) => zavrnjena" % ap)
        sys.exit(2)
    return open(ap, "rb").read()
def tujka(ch):
    o = ord(ch)
    if o in (0x3C3, 0x3C8):  # sigma in psi: rez-znaka korpusa, ⟩ne⟨ tujki
        return False
    return (0x400 <= o <= 0x4FF) or (0x4E00 <= o <= 0x9FFF) or (0x3040 <= o <= 0x30FF) or (0x370 <= o <= 0x3FF) or (0xAC00 <= o <= 0xD7AF)
def preveri(pot):
    b = berba(pot)
    t = b.decode("utf-8", errors="replace")
    nfc = unicodedata.is_normalized("NFC", t)
    zn = collections.Counter(ch for ch in t if not ch.isascii() and not ch.isspace())
    tuj = [ch for ch in zn if tujka(ch)]
    print("ZNAK-JAJCE @%s : %s" % (ticmi(), os.path.abspath(pot)))
    print("  NFC : %s \u23c7 razlicnih znakov : %d" % ("DA \u22a2" if nfc else "NE \u26a0", len(zn)))
    for ch, n in sorted(zn.items(), key=lambda x: -x[1]):
        print("  \u27e8U+%04X\u27e9 x%d %s" % (ord(ch), n, "\u26a0 TUJKA" if tujka(ch) else "\u22a2 gajica"))
    print("SODBA : %s ( tujk %d )" % ("\u010cISTO \u22a2" if (nfc and not tuj) else "PADC \u26a0", len(tuj)))
    return 0 if (nfc and not tuj) else 1
def samocenzus(pot):
    t = berba(pot).decode("utf-8", errors="replace")
    return [ch for ch in set(t) if tujka(ch)]
def samopreizkus():
    d = KOREN + "/stroj-orodja/.geniza/TEST-znak-%d-%s" % (os.getpid(), ticmi().replace(":", ""))
    os.makedirs(d, exist_ok=True)
    t1 = os.path.join(d, "znaki.txt")
    open(t1, "w", encoding="utf-8").write("\u03c3 \u22a2 \u2299 \u22a5 \u2202 pri\u010da po izmeri \u22a2\n")
    A = (samocenzus(__file__) == []) and (os.waitstatus_to_exitcode(os.system("python3 %s --preveri %s >/dev/null 2>&1" % (__file__, t1))) == 0)
    t2 = os.path.join(d, "nfc.txt")
    s = "a" + "\u0301" + " znak sestavljen"
    open(t2, "w", encoding="utf-8").write(s)
    B = (unicodedata.is_normalized("NFC", s) is False) and (os.waitstatus_to_exitcode(os.system("python3 %s --preveri %s >/dev/null 2>&1" % (__file__, t2))) == 1)
    t3 = os.path.join(d, "tujka.txt")
    open(t3, "w", encoding="utf-8").write("pri\u010da z [%s] tujko\n" % chr(0x436))
    izhod3 = os.popen("python3 %s --preveri %s 2>&1" % (__file__, t3)).read()
    C = ("\u27e8U+0436\u27e9" in izhod3) and ("TUJKA" in izhod3) and ("PADC \u26a0" in izhod3)
    D = len(samocenzus(__file__)) == 0
    os.system("rm -rf %s" % d)
    print("SAMOPREIZKUS : T1 cenzus boln %s \u23c7 T2 NFC padec boln %s \u23c7 T3 tujka nagrajena %s \u23c7 T4 samocenzus %s" % ("1" if A else "0", "1" if B else "0", "1" if C else "0", "1" if D else "0"))
    return 0 if (A and B and C and D) else 1
if __name__ == "__main__":
    uk = sys.argv[1] if len(sys.argv) > 1 else ""
    if uk == "--preveri":
        sys.exit(preveri(sys.argv[2] if len(sys.argv) > 2 else ""))
    if uk == "--samopreizkus":
        sys.exit(samopreizkus())
    print("roke : --preveri TELA \u23c7 --samopreizkus")
    sys.exit(1)
