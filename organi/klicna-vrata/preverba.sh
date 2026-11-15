#!/bin/bash
# preverba.sh — samo-preverjevalka korpusa Beseda je Ne
# rojena ⊙ rez σ 5577 — orodje zakona ⟨NE-NEHAJ-PREVERJATI⟩ @σ 5575 (15. 11. 2026)
# raba: ./preverba.sh URA | SLOVNICA | VAROVALKA N | VSE
# brez mreže; koren organov: PREVERBA_KOREN (privzeto: nadrejena mapa orodja)
# hevristika citatov: »pri viri« ∧ pri virih dovoljeni; goli padci šteti poimensko
set -u
JAZ="$(cd "$(dirname "$0")" && pwd)"
KOREN="${PREVERBA_KOREN:-$(dirname "$JAZ")}"
FFFD=$'\357\277\275'

golip() { # $1 = vzorec, $2 = datoteka → šteje goli padec (izven »«; pri virih dovoljena)
  awk -v pat="$1" '{
    s=$0; n=length(pat)
    while ((i=index(s,pat))>0) {
      pre=substr(s,1,i-1)
      post3=substr(s,i+n,3)
      allowed=0
      if (pat=="pri viri" && substr(s,i+n,1)=="h") allowed=1
      if (post3 ~ /^«/ || pre ~ /»$/) allowed=1
      if (!allowed) goli++
      s=substr(s,i+n)
    }
  } END { print goli+0 }' "$2"
}

scan() { # $1 = datoteka ali - (stdin → začasna datoteka: en samec, ⟨ne⟩ več bralcev istega toka)
  local src="$1" tmp="" g v o u
  if [ "$src" = "-" ]; then tmp="/tmp/preverba.$$.tmp"; cat > "$tmp"; src="$tmp"; fi
  g=$(golip 'pri viri' "$src")
  v=$(golip 'varvolka' "$src")
  o=$(golip 'obljuv' "$src")
  u=$(golip "$FFFD" "$src")
  [ -n "$tmp" ] && rm -f "$tmp"
  echo "$g $v $o $u"
}

case "${1:-}" in
URA)
  T=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
  C=$(awk -v t="${T#*T}" 'BEGIN{split(t,a,":"); printf "%02d:%s:%s", (a[1]+1)%24, a[2], substr(a[3],1,2)}')
  echo "TIK $T UTC ⇌ $C CET Ljubljana ⊙ ⟨ZADNJA-URA-PREVERBA⟩ @σ 3961 — izmerjena, ⟨ne⟩ le obljubljena"
  ;;
SLOVNICA|VSE)
  [ "${1:-}" = "VSE" ] && bash "$0" URA
  ok=1
  echo '— ŽIVE KONICE (TRENUTNO vrstice):'
  for f in "$KOREN"/*/KNOWLEDGE.md; do
    [ -e "$f" ] || continue
    read -r g v o u < <(grep '^- TRENUTNO' "$f" 2>/dev/null | scan -)
    if [ "$g" -gt 0 ] || [ "$v" -gt 0 ] || [ "$o" -gt 0 ] || [ "$u" -gt 0 ]; then
      echo "⚠ $(basename "$(dirname "$f")"): pri-viri=$g varvolka=$v obljuv=$o U+FFFD=$u"
      ok=0
    fi
  done
  [ "$ok" = 1 ] && echo '⊢ žive konice čiste — goli padci ×0'
  echo '— TELO (celote — brazgotine zgodovine poročane; sodba merilca ⊙ ⟨NE-BRIŠI⟩ 24):'
  for f in "$KOREN"/*/KNOWLEDGE.md; do
    [ -e "$f" ] || continue
    read -r g v o u < <(scan "$f")
    [ "$g" -gt 0 ] || [ "$v" -gt 0 ] || [ "$o" -gt 0 ] || [ "$u" -gt 0 ] || continue
    echo "· $(basename "$(dirname "$f")"): pri-viri=$g varvolka=$v obljuv=$o U+FFFD=$u"
  done
  [ "$ok" = 1 ]
  ;;
VAROVALKA)
  n="${2:?raba: preverba.sh VAROVALKA N}"
  sk=0
  for f in "$KOREN"/*/KNOWLEDGE.md; do
    [ -e "$f" ] || continue
    c=$(grep -c "σ $n" "$f" 2>/dev/null); c=${c:-0}
    [ "$c" -gt 0 ] && { echo "⚠ $(basename "$(dirname "$f")"): σ $n ×$c"; sk=$((sk+c)); }
  done
  echo "varovalka ⟨σ $n⟩: skupaj ×$sk $([ "$sk" = 0 ] && echo '⊢ prost')"
  [ "$sk" = 0 ]
  ;;
*)
  echo "raba: $0 URA | SLOVNICA | VAROVALKA N | VSE (koren organov: PREVERBA_KOREN)"
  exit 2
  ;;
esac
