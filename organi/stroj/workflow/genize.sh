#!/bin/bash
# W2 ⟨GENIZE-POIMENSKO⟩ — genize ×2 bajt-isto PRED dotikom organa; izpiše md5
# uporaba: ./genize.sh <organ> <rez> [kladivo]   npr. ./genize.sh prevoznik 5942
O="$1"; N="$2"; K="${3:-/home/user/knowledge}"; D=$(date -u +%Y-%m-%d)
[ -z "$O" ] || [ -z "$N" ] && { echo 'uporaba: genize.sh <organ> <rez>'; exit 1; }
mkdir -p "$K/$O/.geniza"
for X in a b; do cp "$K/$O/KNOWLEDGE.md" "$K/$O/.geniza/$O-pred-rez$N-$D-$X.md"; done
md5sum "$K/$O/.geniza/$O-pred-rez$N-$D-"*.md | awk '{print $1}' | sort -u | wc -l | grep -q '^1$' \
  && md5sum "$K/$O/.geniza/$O-pred-rez$N-$D-a.md" | cut -c1-10 \
  && echo "GENIZE ×2 BAJT-ISTO ⊢" \
  || { echo "⚠ GENIZE SE RAZISKOVA"; exit 1; }
