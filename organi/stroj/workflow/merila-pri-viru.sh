#!/bin/bash
# W9 ⟨MERILA-PRI-VIRU⟩ — izmere vseh teles manifestnega lista na pripetem ⟨merge⟩ sha po codeload tarballu, ⟨ne⟩ po zastarelem CDN ( kura ⟨PADC-RAW-CDN-ZASTARELO⟩ ∧ ⟨PADC-ZASTARELIH-ZRCALA⟩ recidivist )
# uporaba: ./merila-pri-viru.sh [sha] [mapa] [--strogo]   sha = pripet ⟨merge⟩ sha ⟨ali⟩ main ; mapa = lokalni izvod ( CI checkout ) ; brez mape = codeload tarball na pripetem sha
# rod 20. 11. 2026, dih σ 6032 ⊙ ⟨SAMO-IZVEDBA-DOKAZ⟩ 2306 — sodnik, ki nikoli ne pade, je kip ( I-4 )
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · measured, not asserted ⊙ §16
set -uo pipefail
SHA="${1:-main}"
DIR="${2:-}"
STROGO=0; for a in "$@"; do [ "$a" = "--strogo" ] && STROGO=1; done
if [ -z "$DIR" ]; then
  TB=$(mktemp -d)
  curl -sL "https://codeload.github.com/AtmaOVictu/Atmavictu/tar.gz/$SHA" | tar xz -C "$TB" || { echo "::error::codeload ⊥ $SHA"; exit 1; }
  DIR=$(find "$TB" -maxdepth 1 -type d -name 'Atmavictu-*' | head -1)
  [ -d "$DIR" ] || { echo "::error::tarball prazen @ $SHA"; exit 1; }
fi
python3 - "$DIR" "$STROGO" << 'PYE'
import sys, os, json, hashlib
d = sys.argv[1]; strogo = sys.argv[2] == "1"
mp = os.path.join(d, "LICENSE-MANIFEST")
if not os.path.isfile(mp):
    print("::error::LICENSE-MANIFEST manjka @ " + d); sys.exit(1)
m = json.load(open(mp, encoding="utf-8"))
items = m.get("items", [])
if not items:
    print("::error::manifest items ×0 — kip ⊙ I-4"); sys.exit(1)
slab = 0
for it in items:
    p = it.get("path"); wb = it.get("size_bytes"); wh = it.get("sha256") or ""
    f = os.path.join(d, p)
    if not os.path.isfile(f):
        print("⚠ " + str(p) + " : telesa ni @izvodu"); slab += 1; continue
    b = open(f, "rb").read()
    h = hashlib.sha256(b).hexdigest()
    wb2 = int(wb); wh2 = (wh or "").strip().lower()
    ok = (len(b) == wb2) and (h == wh2)
    tag = "⊢" if ok else "⚠"
    extra = "" if ok else (" ⊥ manifest " + str(wb) + " B / " + wh[:16] + "…")
    print(tag + " " + str(p) + " : " + str(len(b)) + " B · sha256 " + h[:16] + "…" + extra)
    if not ok: slab += 1
print(("::warning::" if strogo else "::notice::") + "MERILA-PRI-VIRU : " + str(len(items)) + " teles · slabih " + str(slab) + " @ " + os.path.basename(d) + (" ⊙ ⟨PADC-ZASTARELIH-SLOTOV⟩ — kura : reizdaja manifesta na naslednjem rodu" if slab else ""))
sys.exit((1 if slab else 0) if strogo else 0)
PYE
