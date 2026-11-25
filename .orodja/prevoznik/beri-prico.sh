#!/usr/bin/env bash
# ⟨BERI-PRIČO⟩ — orodje branja prič iz shrambe @prevoznik (rojstvo @rez σ 5598, 15. 11. 2026)
# Uporaba: beri-prico.sh SHRAMBA URI-ZNAMENJE IZHOD [PRIČA]
# Prebere NATANČNO ENO pričo (resource) iz shrambe velikih odgovorov po URI-znamenju;
# zadetki ≠ 1 → odstop javno ⊙ ⟨NE-UGIBAJ⟩ 2690 (×0 = molk ni priča, ×2 = dvoglasje ni edinost);
# izhod bajt-ito: jq -j → BREZ dodanega \n ⊙ kura za padec dodane končnice;
# če je dana PRIČA (krajevna datoteka), se izmeri md5 obeh ∧ nesoglasje → odstop ⊙ ⟨MERILEC-SE-MERI⟩ §52.
# »a bare text proves nothing, the chain does« ⊢ §0.10
set -euo pipefail

SHR="$1"; ZNAMENJE="$2"; IZHOD="$3"; PRICA="${4:-}"

[ -f "$SHR" ] || { echo "⟨BERI-PRIČO⟩ ⚠ ODKIV: shramba ni najdena: $SHR" >&2; exit 1; }

STEVNIK=$(jq --arg z "$ZNAMENJE" '[.content[] | select(.type=="resource") | select(.resource.uri | contains($z))] | length' "$SHR")

if [ "$STEVNIK" -ne 1 ]; then
  echo "⟨BERI-PRIČO⟩ ⚠ ODKIV: zadetkov po znamenju »$ZNAMENJE« je $STEVNIK, zahtevan je natanko 1 (⟨NE-UGIBAJ⟩ 2690: ×0 ni priča, ×2+ ni edinost) — branje ODBITO" >&2
  exit 1
fi

jq -j --arg z "$ZNAMENJE" '.content[] | select(.type=="resource") | select(.resource.uri | contains($z)) | .resource.text' "$SHR" > "$IZHOD"

ZN=$(wc -c < "$IZHOD")
MD5=$(md5sum "$IZHOD" | cut -d' ' -f1)

URI=$(jq -r --arg z "$ZNAMENJE" '.content[] | select(.type=="resource") | select(.resource.uri | contains($z)) | .resource.uri' "$SHR")

echo "⟨BERI-PRIČO⟩ ⊢ priča prebrana bajt-ito: $ZN B · md5 $MD5 · $URI"

if [ -n "$PRICA" ]; then
  [ -f "$PRICA" ] || { echo "⟨BERI-PRIČO⟩ ⚠ ODKIV: priča ni najdena: $PRICA" >&2; exit 1; }
  MD5P=$(md5sum "$PRICA" | cut -d' ' -f1)
  if [ "$MD5" != "$MD5P" ]; then
    echo "⟨BERI-PRIČO⟩ ⚠ ODKIV: md5 nesoglasje — shramba $MD5 ⊥ priča $MD5P ⊙ ⟨MERILEC-SE-MERI⟩ §52" >&2
    exit 1
  fi
  echo "⟨BERI-PRIČO⟩ ⊢ ZNAK-ISTO: md5 shrambe = md5 priče = $MD5"
fi
