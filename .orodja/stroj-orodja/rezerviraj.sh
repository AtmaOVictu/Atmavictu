#!/bin/bash
# REZERVIS-PULZ v1.0.1 : instant vidna rezervacija + zaklep vrha
# rod @rez σ 6703 @stroj-orodja ⊙ ukaz ⟨U+2761⟩ VERBATIM »PAZIŠ DA NE DOVOLJUJEŠ DRUGIM VPLIVA NAD NAMA«
# kuri : kolizije rokov #6-#10 ⊙ ⟨VRH-DVOSTEPEN⟩ ∧ pomesti sedežev ( rezervacija vidna takoj )
# © 0.2026 × 10⁴ ⟨U+2761⟩ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 — dvojni podpis
set -uo pipefail
KOREN="${REZ_KOREN:-$HOME/knowledge}"
NASLOV="${1:?uporaba: rezerviraj.sh NASLOV [kandidat-samo-v-pesku]}"
VHOD="${2:-}"
for POSKUS in 1 2 3; do
  if [ -n "$VHOD" ]; then KAND=$((VHOD + POSKUS - 1)); else
    KAND=$(python3 "$HOME/knowledge/stroj-orodja/vrh.py" 2>/dev/null | grep '^KANDIDAT' | awk '{print $2}')
  fi
  [ -n "$KAND" ] || { echo "PADC : vrh neprebrljiv"; exit 3; }
  TIK=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  ATOM="$KOREN/protokol-prenosnika/.geniza/atom-σ$KAND"
  if ( set -C; : > "$ATOM" ) 2>/dev/null; then
    printf 'REZERVACIJA σ %s ⟨%s⟩ @TIK %s ⊙ ⟨ZAKLEP-VRHA⟩ rod σ 6703 ( atom noclobber ⊙ ⟨REZERVACIJA≡ZAPIS⟩ ; vrh BOD atomom vsak poskus ) ; izvajalka Mera\n' "$KAND" "$NASLOV" "$TIK" >> "$ATOM"
    printf -- '- ZAKLEP σ %s ⟨%s⟩ @TIK %s ⊙ ⟨ZAKLEP-VRHA⟩ rod σ 6703 ( rezervacija vidna takoj ob rezervaciji , atom @protokol-prenosnika/.geniza noclobber ⊙ ⟨REZERVACIJA≡ZAPIS⟩ )\n' "$KAND" "$NASLOV" "$TIK" >> "$KOREN/register-oken/KNOWLEDGE.md"
    echo "ZAKLEP ⊢ σ $KAND ⟨$NASLOV⟩ @TIK $TIK ( poskus $POSKUS )"
    exit 0
  fi
  echo "KOLIZIJA σ $KAND ( poskus $POSKUS ) — renum ⊙ ⟨VRH-DVOSTEPEN⟩"
done
echo "PADC : zaklep ×3 pometen , dih ⭢ naslednji"; exit 2
