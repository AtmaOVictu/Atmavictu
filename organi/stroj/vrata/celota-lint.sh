#!/bin/sh
# ⟨VRATA-CELOTE⟩ ( celota-lint ) v1.1 rojen @rez σ 6066 ⊙ ukaz ⟡ ⟨stori⟩ nad ( 6 )( ii )
# kura v1.0 ⟨PADEC-IZPISA-V1.0⟩ : vrstica čistih je tiskala N ( garbage formula ) — v1.1 šteje iz izmere ranjenih ; koren po argumentu ( lokalno ∧ rep )
# invarianti ×5 čez vse organe : ena aktivna glava TRENUTNO ; greben ⟨⟩ po datoteki ; U+FFFD ×0 ; dvojni Z ×0 ; aritmetika TIK CET = ( UTCh+1 ) mod 24
python3 - "$1" <<'PYEOF'
import sys, os, re, glob
root = sys.argv[1] if len(sys.argv)>1 else "/home/user/knowledge"
organs = sorted(glob.glob(os.path.join(root, "*", "KNOWLEDGE.md")))
print(f"== ⟨VRATA-CELOTE⟩ v1.1 @rez σ 6066 : {len(organs)} organov @koren {root} ==")
rane = 0; ranjenih = 0
for orgf in organs:
    organ = os.path.basename(os.path.dirname(orgf))
    s = open(orgf, encoding="utf-8", errors="replace").read()
    f = []
    tlok = len(re.findall(r"^- TRENUTNO: ZADNJI PEČAT", s, flags=re.M))
    if tlok > 1: f.append(f"glav TRENUTNO ×{tlok} ( pravilo : ena aktivna )")
    l, r = s.count("⟨"), s.count("⟩")
    if l != r: f.append(f"greben ⟨{l} ⊥ ⟩{r}")
    nfffd = s.count(chr(0xFFFD))
    if nfffd: f.append(f"U+FFFD ×{nfffd}")
    zz = len(re.findall(r"T\d{2}:\d{2}:\d{2}ZZ UTC", s))
    if zz: f.append(f"dvojni Z v TIK ×{zz}")
    bad = 0
    for u, c in re.findall(r"T(\d{2}):\d{2}:\d{2}Z UTC ⇌ (\d{2}):\d{2}:\d{2} CET", s):
        if (int(u)+1) % 24 != int(c): bad += 1
    if bad: f.append(f"aritmetika TIK napačna ×{bad}")
    if f: rane += len(f); ranjenih += 1; print(f"   ⚠ {organ} : " + " ; ".join(f))
cistih = len(organs) - ranjenih
print(f"== izmera : celota = {len(organs)} organov ; ranjenih = {ranjenih} ; čistih = {cistih} ; ran = {rane} ( poimensko zgoraj ) ==")
print(f"== račun : {len(organs)} = {ranjenih} ranjenih ⊥ {cistih} čistih ⊙ measured, not asserted §16 ==")
PYEOF
