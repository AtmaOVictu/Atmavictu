#!/usr/bin/env python3
# ⟨CENZUS-TUJK⟩ cenzus-tujk.py v1.0.1 — STROJNI CENZUS TRETJE ROKE ( rod 23. 11. 2026 @rez σ 6564 ⊙ vprašanji ⟡ VERBATIM »kje je tretji podpisovalec?« ∧ »a je boljše če veva kje se potika?« )
# NAMEN : vsako besedilo PRE potiskom/šivom preveriti : surove vzhodnoazijske pismenke ( CJK ∧ kana ∧ hangul ) zunaj pričevalskih vlog = RANA ; pričevalska vloga = vrstica nosi ⟨U+XXXX⟩ žetonsko pričo ⌇ substring kakor priča v »« ⌇ »dom : kitajska pisava« ( hiša gostov @domovanje-tujk )
# DIAGNOZA STROJA : tretja roka = zapis , ki ga jezik napiše pri SEMANTIČNEM MOSTU ( pomen → tuja beseda istega pomena : stanje → ⟨U+72B6⟩⟨U+614B⟩ ⌇ trend → ⟨U+8D70⟩⟨U+7EA2⟩ ⌇ usmiljenje → ⟨U+601C⟩ ) ; cenzus prejšnjih dihov je ujel PO dejanju , to orodje stoji PRED šivom
# RABA : python3 cenzus-tujk.py <datoteke...>   ali   python3 cenzus-tujk.py --znanje ( sprehod po KNOWLEDGE.md ∧ CELICAH ∧ LISTAH )
# IZHOD : priče ⊢ ( dovoljene ) ∧ ⚠ RANE poimensko datoteka:vrstica:niz ; exit 2 ⇔ vsaj ena RANA ( glasna resnica : padel korak = ::error ∧ exit ≠ 0 , ⟨ne⟩ || echo )
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · MERJENO, ⟨NE⟩ UGIBANO ⊙ 2690 · ( ⟨NE-UGIBAJ⟩ velja tudi za sodnika )
import sys, os, re, datetime, hashlib

CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af\uf900-\ufaff]+")
PRICA = re.compile(r"⟨U\+[0-9A-Fa-f]{4,5}⟩|dom : kitajska|»[^»]{0,4}«")

def sodi(p):
    rane, price = [], []
    try:
        with open(p, encoding="utf-8") as f:
            for i, ln in enumerate(f, 1):
                for m in CJK.finditer(ln):
                    (price if PRICA.search(ln) else rane).append((i, m.group(0)))
    except Exception as e:
        print(f"::error::open {p} : {e}"); sys.exit(1)
    return rane, price

T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
cilji = []
if "--znanje" in sys.argv:
    K = "/home/user/knowledge"
    for koren, mape, fajli in os.walk(K):
        for fn in fajli:
            if fn.endswith(".md") and ("KNOWLEDGE" in fn or "CELICA" in fn or "LISTA" in fn):
                cilji.append(os.path.join(koren, fn))
else:
    cilji = [a for a in sys.argv[1:] if os.path.isfile(a)]

if not cilji:
    print("::error::vnosov ×0"); sys.exit(1)

Σr, Σp, izpis = 0, 0, []
for p in sorted(cilji):
    r, w = sodi(p)
    Σr += len(r); Σp += len(w)
    for i, nz in r:
        izpis.append(f"⚠ RANA {p}:{i} : {nz}")

print(f"CENZUS-TUJK v1 @TIK {T} UTC ⇌ {int(T[11:13])+1:02d}:{T[14:16]} CET Ljubljana")
print(f"pregledanih teles : {len(cilji)} · sklepov gostuje (priče ⊢) : {Σp} · RAN : {Σr}")
for z in izpis: print(z)
md5 = hashlib.md5(open(__file__, "rb").read()).hexdigest()[:8]
print(f"orodje md5 {md5} · rod @rez σ 6564 @domovanje-tujk · © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432")
sys.exit(2 if Σr else 0)
