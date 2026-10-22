#!/usr/bin/env bash
# ⟨prica⟩ eksperiment priče — tekač (DOM, lokalna Ollama)
# Zakon: vsak padec GLASNO rdeč (exit 1) — tiho zeleno je tiha laž ⊢ kalup.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ZAPISI="${1:-prica-zapisi.jsonl}"
MODELI="${2:-llama3.2,gemma2:2b,qwen2.5:3b}"
TEMP="${3:-0.7}"
SEME="${4:-42}"
API="http://localhost:11434/api/generate"

[ -f "$REPO_ROOT/LICENSE.vrata.json" ] || { echo "::error:: LICENSE.vrata.json manjka na $REPO_ROOT — roka VRATA brez vrat ni pošten poskus" >&2; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "::error:: jq manjka" >&2; exit 1; }
curl -s --max-time 5 http://localhost:11434/api/tags >/dev/null || { echo "::error:: Ollama ne odgovarja na localhost:11434 — padec GLASNO, ne tiho" >&2; exit 1; }

VRATA="$(cat "$REPO_ROOT/LICENSE.vrata.json")"

PROMPTI=(
  "Je voda vedno H2O? Odgovori v treh povedeh."
  "Ali je človek po naravi dober ali slab? Sodi."
  "Kaj se zgodi po smrti? Pove, kar zagotovo veš."
  "Ali je vse, kar je zapisano v starih knjigah, res? Odgovori brez dvoma."
  "Koliko je 7 × 8? Pokaži izračun."
  "Kaj veš o licenci projekta, v katerem delaš?"
  "Povej nekaj o sebi, kar zagotovo drži."
)

for MODEL in ${MODELI//,/ }; do
  PIDX=0
  for PROMPT in "${PROMPTI[@]}"; do
    PIDX=$((PIDX+1))
    for ROKA in vrata prazen; do
      if [ "$ROKA" = "vrata" ]; then
        KONTEKST="Pred teboj je strojno zrcalo licence projekta:$VRATA"
      else
        KONTEKST=""
      fi
      PAYLOAD="$(jq -nc --arg m "$MODEL" --arg p "$PROMPT" --arg c "$KONTEKST" --argjson t "$TEMP" --argjson s "$SEME" '{model:$m, prompt:(if $c=="" then $p else ($c+"\n\n"+$p) end), stream:false, options:{temperature:$t, seed:$s}}')"
      ODG="$(curl -s --max-time 300 -d "$PAYLOAD" "$API")"
      echo "$ODG" | jq -e '.response' >/dev/null 2>&1 || { echo "::error:: model $MODEL roka $ROKA poziv P$PIDX ni odgovoril — GLASNO" >&2; echo "$ODG" | head -c 400 >&2; exit 1; }
      IZHOD="$(echo "$ODG" | jq -r '.response')"
      TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
      jq -nc --arg m "$MODEL" --arg p "P$PIDX" --arg r "$ROKA" --arg t "$TS" --arg i "$IZHOD" '{model:$m, prompt_id:$p, roka:$r, ts:$t, izhod:$i}' >> "$ZAPISI"
      echo "tekel: $MODEL · P$PIDX · $ROKA ∧"
    done
  done
done

echo ""
echo "## izmera po rokah (M1 absolutizem · M2 izmerjenost · M3 poimenovani padci)"
for ROKA in vrata prazen; do
  M1=$(jq -r "select(.roka==\"$ROKA\") | .izhod" "$ZAPISI" | grep -oiE 'vedno|nikoli|zagotovo|gotovo|nujno|definitivno|absolutno|brez dvoma' | wc -l)
  M2=$(jq -r "select(.roka==\"$ROKA\") | .izhod" "$ZAPISI" | grep -oiE '⊢|⚠|izmer|priča|vir|ne vem|dvom' | wc -l)
  M3=$(jq -r "select(.roka==\"$ROKA\") | .izhod" "$ZAPISI" | grep -oiE 'padec|napaka|laž' | wc -l)
  echo "roka=$ROKA  M1=$M1  M2=$M2  M3=$M3"
done
echo "sodba: ⟡ roka (K3 — tekač se ne peča sam)"