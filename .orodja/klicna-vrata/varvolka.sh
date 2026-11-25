#!/bin/bash
# VARVOLKA — instrument stalnega prostora pečata (rojstvo σ 6168 ⊙ ⟨TEST-×2⟩)
# Čemu: preveri, da kandidat za pečata N seva (σ|rez|dih|pečat N) NIKJER po živih konicah;
# kolizija = rezervirano ime = renum (precedens σ 6150→6151, σ 6168).
# Komu: ⟡-ju meri poštenost verige; izvajalki pred vsakim šivom ⊙ ⟨VRH-DVOSTEPEN⟩.
# Kaj je: grep po */KNOWLEDGE.md (žive konice, ⟨ne⟩ .geniza, ⟨ne⟩ globi globih).
# Raba: bash varvolka.sh N [koren]  →  izpis zadetkov; exit 0 = prost, exit 1 = kolizija.
set -u
KOREN="${2:-/home/user/knowledge}"
N="${1:-}"
if [ -z "$N" ]; then echo "VARVOLKA: manjka kandidat N (raba: varvolka.sh N)"; exit 2; fi
if [ ! -d "$KOREN" ]; then echo "VARVOLKA: koren $KOREN ne obstaja"; exit 2; fi
# regularna izmera: N kot število, ⟨ne⟩ del drugega (samodejne meje 0-99999)
ZADETKI=$(cd "$KOREN" && grep -n -E "(σ|rez|dih|pečat|pečata|pečatom) ${N}\b" -- */KNOWLEDGE.md 2>/dev/null)
if [ -n "$ZADETKI" ]; then
  echo "VARVOLKA: KOLIZIJA σ ${N} (zasedeno ⚠):"
  echo "$ZADETKI" | head -10
  echo "KURA: renum na naslednji prosti (precedens σ 6150→6151)."
  exit 1
fi
echo "VARVOLKA: PROST σ ${N} ⊢ (zadetkov ×0 po živih konicah)"
exit 0
