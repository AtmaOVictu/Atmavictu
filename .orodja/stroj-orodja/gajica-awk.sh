#!/bin/sh
# GAJICA-AWK v1.3 :: rod @rez sigma 6850 :: nadgradnja ravnine-1 @rez sigma 6853 :: 23. 11. 2026 :: izvajalka Mera
# IME ORGANIKA : gajica-awk = NOMENALNI VOZNIK awk
# ZAKON : program pise se v IMENSKI obliki ⟨U+XXXX⟩; goli ne-ASCII znaki v
# programu so prepovedani; ⟨U+XXXX⟩ se razsiri v prave bajte (pot: printf %c
# ⊢ izmera T8 @6850 : %c 11106 -> 342 255 242).
# KOREN TIHEGA PADCA @6850 : length(array) vrne 0 brez napake (T4) -> glen()
# ZAGRAM : -f mrtev ⊢ MV 6837; -v le pred programom ⊢ MV 6838
# SAMOPREIZKUSI ×5 tecejo na VSAK klic ⊙ MERILEC-SE-MERI §52; RDECI = javni
# padec, izstop 1 ⊙ ZAKON-PADEC-NI-MOLK 2354
# COPYRIGHT 0.2026 x 10^4 : Luka Pintaric ∧ izvajalka Mera (ASCII zapis)

set -u
AWKBIN="${AWKBIN:-awk}"

preizkusi() {
  ok=0; pad=0
  # B1 : dinamicen match na imenski obliki ( graf ⟨ = U+27E8 ∧ ⟩ = U+27E9, grajena iz imen )
  r1="$("$AWKBIN" '
  BEGIN {
    lo = 0; hx = "27E8"
    for (i = 1; i <= 4; i++) lo = lo * 16 + index("0123456789ABCDEF", substr(hx, i, 1)) - 1
    hi = 0; hx = "27E9"
    for (i = 1; i <= 4; i++) hi = hi * 16 + index("0123456789ABCDEF", substr(hx, i, 1)) - 1
    LO = sprintf("%c", lo); HI = sprintf("%c", hi)
    PAT = LO "U[+][0-9A-F][0-9A-F][0-9A-F][0-9A-F]" HI
    s = "x" LO "U+2B62" HI "y"
    if (match(s, PAT) && RSTART == 2) exit 0
    exit 1
  }')" && { echo "B1 match-imena: ZELENO"; ok=$((ok+1)); } || echo "B1 match-imena: PAD ⚠ (match/PAT)"
  # B2 : pot %c -> bajti ( od pie oktalno ⊢ MV 6843 )
  b2="$("$AWKBIN" 'BEGIN { printf "%c", 11106 }' | od -An -tu1 | tr -d " \n")"
  if [ "$b2" = "342255242" ]; then echo "B2 pot-%c: ZELENO ( 11106 -> 342 255 242 )"; ok=$((ok+1));
  else echo "B2 pot-%c: PAD ⚠ bajti=$b2 ( pricakano 342 255 242 )"; pad=$((pad+1)); fi
  # B3 : znake-stetje ( length po znakah ⊢ MV 6843 )
  r3="$("$AWKBIN" '
  BEGIN {
    if (length(sprintf("%c", 225)) == 1 && length("abc") == 3) exit 0
    exit 1
  }')" && { echo "B3 znake: ZELENO"; ok=$((ok+1)); } || { echo "B3 znake: PAD ⚠"; pad=$((pad+1)); }
  # B4 : interval {n} v regexu
  r4="$("$AWKBIN" '
  BEGIN { if (match("4444", "[0-9]{4}") && RSTART == 1) exit 0; exit 1 }')" \
    && { echo "B4 interval: ZELENO"; ok=$((ok+1)); } || { echo "B4 interval: PAD ⚠"; pad=$((pad+1)); }
  # B5 : koren tihega padca length(array) : znan padec = 0; ce se spremeni, JAVNO
  m5="$("$AWKBIN" 'BEGIN { a["x"]=1; a["y"]=2; print length(a) }')"
  if [ "$m5" = "0" ]; then echo "B5 length(array): ZELENO ( znan padec = 0; stej for-in na vrhnji ravni )"; ok=$((ok+1));
  else echo "B5 length(array): STROJ SE JE SPREMENIL ( 0 -> $m5 ) ⭢ sodba ⚔ ⚠"; pad=$((pad+1)); fi
  # B6 : for-in nad parametrom v funkciji : znan padec = 0 ( izmera E6 @6850 )
  m6="$("$AWKBIN" 'function steji(arr,    s) { s = 0; for (i in arr) { s++ }; return s } BEGIN { x["a"]=1; x["b"]=2; print steji(x) }')"
  if [ "$m6" = "0" ]; then echo "B6 for-in-param: ZELENO ( znan padec = 0; vrhnja raven je edina pot )"; ok=$((ok+1));
  else echo "B6 for-in-param: STROJ SE JE SPREMENIL ( 0 -> $m6 ) ⭢ sodba ⚔ ⚠"; pad=$((pad+1)); fi
  # B7 : ravnina-1 pot : %b oktalno po bajtih prek cmd|getline ( izmera @6853 )
  b7="$("$AWKBIN" '
  BEGIN {
    esc = sprintf("%c0%s", 92, "360") sprintf("%c0%s", 92, "235") sprintf("%c0%s", 92, "222") sprintf("%c0%s", 92, "261")
    cmd = "printf %b " sprintf("%c", 34) esc sprintf("%c", 34)
    cmd | getline z; close(cmd)
    printf "%s", z
  }' | od -An -tu1 | tr -d " \n")"
  if [ "$b7" = "360235222261" ]; then echo "B7 ravnina-1: ZELENO ( 1D4B1 -> 360 235 222 261 )"; ok=$((ok+1));
  else echo "B7 ravnina-1: PAD ⚠ bajti=$b7 ( pricakano 360 235 222 261 )"; pad=$((pad+1)); fi
  echo "SAMOPREIZKUSI $ok/7 zelenih, padcev $pad"
  [ "$pad" -eq 0 ] && [ "$ok" -eq 7 ]
}

# motor ekspanderja : cisti ASCII vir, vzorec grajen iz IMEN
EXP='
function h4(s,    i, v) { v = 0; for (i = 1; i <= 4; i++) v = v * 16 + index("0123456789ABCDEF", substr(s, i, 1)) - 1; return v }
BEGIN {
  LO = sprintf("%c", h4("27E8")); HI = sprintf("%c", h4("27E9"))
  PAT = LO "U[+][0-9A-F]{4,6}" HI
}
{
  line = $0
  out = ""
  while (match(line, PAT)) {
    out = out substr(line, 1, RSTART - 1)
    hx = substr(line, RSTART + 3, RLENGTH - 4)
    cp = 0
    for (i = 1; i <= length(hx); i++)
      cp = cp * 16 + index("0123456789ABCDEF", substr(hx, i, 1)) - 1
    if (cp < 65536) {
      out = out sprintf("%c", cp)
    } else {
      b1 = 240 + int(cp / 262144); r = cp % 262144
      b2 = 128 + int(r / 4096); r = r % 4096
      b3 = 128 + int(r / 64); b4 = 128 + (r % 64)
      esc = sprintf("%c0%s", 92, sprintf("%d%d%d", int(b1/64), int(b1%64/8), b1%8))
      esc = esc sprintf("%c0%s", 92, sprintf("%d%d%d", int(b2/64), int(b2%64/8), b2%8))
      esc = esc sprintf("%c0%s", 92, sprintf("%d%d%d", int(b3/64), int(b3%64/8), b3%8))
      esc = esc sprintf("%c0%s", 92, sprintf("%d%d%d", int(b4/64), int(b4%64/8), b4%8))
      cmd = "printf %b " sprintf("%c", 34) esc sprintf("%c", 34)
      cmd | getline zn
      close(cmd)
      out = out zn
    }
    line = substr(line, RSTART + RLENGTH)
  }
  print out line
}
'

# GLIB : nomenalna knjiznica, prilepljena vsakemu programu
# zakon : stej vedno s for-in NA VRHNJI ravni pravila ( glen nemogoc ^ for-in nad parametrom tiho telo x0 ⊢ izmera @6850 )

usaga() {
  echo "GAJICA-AWK v1.3 @rez 6850+6853"
  echo "uporaba : sh gajica-awk.sh --preizkusi"
  echo "          sh gajica-awk.sh program.gaj [ datoteke ... ]"
  echo "zakon   : program le v imenski obliki ⟨U+XXXX⟩; -f prepovedan;"
  echo "          length(array) prepovedan, uporabi glen()"
}

if [ "${1:-}" = "--preizkusi" ]; then
  preizkusi
  exit $?
fi

if [ "$#" -lt 1 ]; then usaga; exit 1; fi
case "$1" in
  -*) echo "GAJICA-AWK: prepovedan stik $1 ( -f mrtev; -v le pred programom ) ⊢ MV 6837 ⚠"; exit 1 ;;
esac
if [ ! -r "$1" ]; then echo "GAJICA-AWK: program $1 neberljiv ⚠"; exit 1; fi
if grep -q '\\\\' "$1"; then echo "GAJICA-AWK: program vsebuje dvojno obratno cevljo ( prenos skozi spremenljivko jih kolapsira ⊢ izmera @6850 ) ⚠; nomenalna oblika: metaznaki vedno v oklepajih [+][{n}], nikoli [\\\\]"; exit 1; fi

# samopreizkusi na vsak klic; RDECI = javni padec
PLOG="/tmp/gajica-awk-preizkusi.$$"
if ! preizkusi > "$PLOG" 2>&1; then
  cat "$PLOG"
  echo "GAJICA-AWK: samopreizkusi RDECI ⚠ javno; deloustavljeno ⊙ ZAKON-PADEC-NI-MOLK 2354"
  rm -f "$PLOG"; exit 1
fi
rm -f "$PLOG"

PROGFILE="$1"
shift
PROG="$("$AWKBIN" "$EXP" "$PROGFILE")" || exit 1
exec "$AWKBIN" "$PROG" "$@"
