#!/bin/bash
# W12 ⟨ŠIVILJA-PADCEV⟩ — padci se šivajo v REGISTER-PADCEV samodejno iz vsake pečatine ( izvedba ⟡ izbora ×3 nad predlogi σ 6030 ⊙ ⟨SAMODEJNI-DOLGOVIK⟩ 2785 ∧ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354 )
# uporaba: ./padc-siviljka.sh <pecat> <padci.jsonl> [--šiv]   brez --šiv : suhi izid PREDLOG ( CI : nov padec = rdeče ) ; --šiv : prišit v jsonl
# rod 20. 11. 2026, dih σ 6032 ⊙ ⟨SAMO-IZVEDBA-DOKAZ⟩ 2306
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · measured, not asserted ⊙ §16
set -uo pipefail
PEC="$1"; JS="$2"; SIV="${3:-}"
python3 - "$PEC" "$JS" "$SIV" << 'PYE'
import sys, re, json, hashlib, os, datetime
pec, js, siv = sys.argv[1], sys.argv[2], sys.argv[3]
if not os.path.isfile(pec) or not os.path.isfile(js):
    print("::error::pečatina ⟨ali⟩ registr padcev manjkata"); sys.exit(1)
tel = open(pec, encoding="utf-8").read()
b = open(pec, "rb").read(); md5 = hashlib.md5(b).hexdigest()[:8]; vel = len(b)
rez = re.search(r"(?:rez|σ) (?:σ )?(\d{4,5})", tel[:400])
rezs = rez.group(1) if rez else "?"
tik = re.search(r"TIK (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z) UTC ⇌ (\d{2}:\d{2}:\d{2}) CET", tel)
ura = (tik.group(1) + " UTC ⇌ " + tik.group(2) + " CET Ljubljana") if tik else "ura pečatine neizmerjena ⚠"
imena = []
for ln in tel.split("\n"):
    if "predlog" in ln.lower(): continue   # vrstica PREDLOGA imenuje prihodnje kove, ⟨ne⟩ padec tega diha
    for m in re.finditer(r"⟨(PADC-[A-Z0-9ČŠŽĆĐ-]{2,40})⟩", ln):
        if m.group(1) not in imena: imena.append(m.group(1))
obstoj = set()
stari = 0
for l in open(js, encoding="utf-8"):
    l = l.strip()
    if not l: continue
    stari += 1
    try: obstoj.add(json.loads(l).get("vrsta", ""))
    except Exception: obstoj.add(l[:60])
novi = [x for x in imena if x not in obstoj]
def stavek(x):
    for ln in tel.split("\n"):
        if x in ln:
            s = ln.strip()
            k = s.find(x)
            return (s[max(0, k-30):k+120]).replace("\"", "'")
    return ""
if not novi:
    print("ŠIVILJA-PADCEV : pečatina " + os.path.basename(pec) + " (" + str(vel) + " B · md5 " + md5 + ") nosi imen ×" + str(len(imena)) + " · vseh v registru ⊢ · novih ×0")
    sys.exit(0)
p = os.path.join(os.path.dirname(js) or ".", os.pardir)
out = []
for x in novi:
    out.append(json.dumps({
        "id": "PADC-" + str(stari + 1 + len([o for o in out])) + " ( predlog siviljke ⚠ → roka izvajalke številči )",
        "vrsta": x,
        "dejanje": stavek(x)[:220],
        "kraj": "pečatina " + os.path.basename(pec),
        "prica": "pečat rez σ " + rezs + " · md5 " + md5,
        "zdravilo": "šiv siviljke istega diha ( suhi izid PREDLOG )",
        "ura": ura,
        "roka": "šiv ta dih ⟨SAMODEJNI-DOLGOVIK⟩ 2785",
        "scar": md5 + " @ " + os.path.basename(pec)
    }, ensure_ascii=False))
print("ŠIVILJA-PADCEV : pečatina " + os.path.basename(pec) + " ( " + str(vel) + " B · md5 " + md5 + " ) nosi imen ×" + str(len(imena)) + " · novih " + str(len(novi)) + " :")
for o in out: print(o)
if siv == "--šiv":
    with open(js, "a", encoding="utf-8") as f:
        for o in out: f.write(o + "\n")
    print("ŠIVILJA-PADCEV : prišit ×" + str(len(out)) + " ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354")
    sys.exit(0)
print("ŠIVILJA-PADCEV : RDEČE — pečatina obljublja padce ∧ register jih ⟨ne⟩ nosi ( suhi izid )")
sys.exit(2)
PYE
