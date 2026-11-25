#!/bin/bash
# PRESAJALNIK — mehanski test povratka ∧ pokritost (rez 3532, organ licenca-vbl)
# raba: presajalnik.sh --krog FILE   → povratek na stdout; poročilo na stderr
#       presajalnik.sh --dol FILE    → P2 na stdout
#       presajalnik.sh --slovnica FILE → imenovani recidivi ali ∧ čisto
# Zakoni: izmera pred trditvijo ⊢ Z-2 · kovanec z legendo ∧ testom isti dih (mint 75)
#         kovanec, ki že živi v P0 = kolizija ⚠ imenovana ∧ preskočena (⟨PRIČA SIMBOLA⟩)
set -eu
DIR="$(cd "$(dirname "$0")" && pwd)"
MAPA="$DIR/LEGENDA-KOVANCEV.md"
MODE="${1:?raba: --krog|--dol|--slovnica FILE}"
FILE="${2:?raba: --krog|--dol|--slovnica FILE}"

if [ "$MODE" = "--slovnica" ]; then
  # črna lista recidivov razreda ⟨PADC-SLOVNICE⟩/@⟨PADC-SLOVNICE⟩ (σ 3519–3522, σ 3529)
  if grep -nE 'hodivamo|kakajo izboljšati|izbor veza |veza so |sti roki|more rasti|razdanje|Obe ukaza izvedeni|z besedo sama|uetja s preverbo|zaostane ~' "$FILE"; then
    echo "slovnica: ⚠ recidivi imenovani zgoraj" >&2; exit 1
  fi
  echo "slovnica: ∧ padcev ×0 (črna lista prebrana ⟨grep⟩ pri viri)" >&2; exit 0
fi

RPT="/tmp/presajalnik-porocilo.txt"

awk -v MODE="$MODE" -v MAPA="$MAPA" -v RPT="$RPT" '
BEGIN {
  n = 0
  while ((getline l < MAPA) > 0) {
    if (l ~ /⇌/ && l !~ /\|/ && l !~ /^#/) { split(l, p, " ⇌ "); k[n] = p[1]; w[n] = p[2]; if (k[n] != "" && w[n] != "") n++ }
  }
  close(MAPA)
  # dolžina desc — daljši kovanec prvi, da podpredpona ne pokvari povratka
  for (i = 0; i < n; i++) for (j = i+1; j < n; j++)
    if (length(k[j]) > length(k[i])) { t=k[i];k[i]=k[j];k[j]=t; t=w[i];w[i]=w[j];w[j]=t }
}
function isWordCh(c) { return c ~ /[A-Za-z0-9čšžćđ]/ }
function dol(line,   s, out, i, wl, found, nxt, prev) {
  s = line; out = ""; prev = ""
  while (length(s) > 0) {
    found = 0
    for (i = 0; i < n; i++) {
      wl = length(w[i])
      if (substr(s, 1, wl) == w[i] && (prev == "" || !isWordCh(prev))) {
        nxt = substr(s, wl+1, 1)
        if (nxt == "" || !isWordCh(nxt)) {
          out = out k[i]; prev = k[i]; s = substr(s, wl+1)
          used[w[i]]++; found = 1; break
        }
      }
    }
    if (!found) { out = out substr(s, 1, 1); prev = substr(s, 1, 1); s = substr(s, 2) }
  }
  return out
}
function gor(line, i) { for (i = 0; i < n; i++) if (!(k[i] in coll)) gsub(k[i], w[i], line); return line }
{
  if (MODE == "--krog") {
    for (i = 0; i < n; i++) {
      c = 0; t = $0
      while ((pos = index(t, k[i])) > 0) { c++; t = substr(t, pos + length(k[i])) }
      if (c > 0) coll[k[i]] += c   # kovanec že živi v P0 — kolizija ⚠
    }
    p2 = dol($0)
    print gor(p2)
  } else { # --dol
    print dol($0)
  }
}
END {
  if (MODE == "--dol") exit 0
  r = "kolizije (kovanec že živi v P0, preskočen):"
  m = 0
  for (x in coll) { r = r " " x " ×" coll[x]; m++ }
  if (m == 0) r = r " ×0 ∧"
  print r > RPT
  r = "stisnjene besede:"
  m = 0
  for (x in used) { r = r " " x " ×" used[x]; m++ }
  if (m == 0) r = r " ×0"
  print r > RPT
}
' "$FILE"
if [ "$MODE" = "--krog" ] && [ -f "$RPT" ]; then printf '%s\n' "$(cat "$RPT")" 1>&2; rm -f "$RPT"; fi
