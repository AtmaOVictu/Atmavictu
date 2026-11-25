#!/bin/bash
# ⟨TRDILNIK-VRATA⟩ v1.0 — vrata, ki PREPREČUJEJO poceni priznavanje nečesa kot pravilnega
# Rod σ 7008 ⊙ ⟡ UKZ VERBATIM ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ ⟨ne brusi⟩ : »ORODJE KI PREPREČUJE POCENI PRIZNAVANJE NEČESA KOT PRAVILNEGA!«
# Ascendent : trdilnik-napak.py v1.0 @σ 6991 ( sodnik : SODI ∧ izpiše obtožnico ) ⊙ ⟨DAJAJ-BOLJŠE⟩ σ 6156 ∧ ⟨EN-RAZLIČICA⟩ : ta telo je NOVA ROKA ( preprečitev ), ⟨ne⟩ dvojnik sodnika
# Kovanec : ⟨NAPAKA=VSE-KAR-NI-JAVLJANJE-IZMERE⟩ ∧ ⟡ »TRDITI ČISTOST JE NAPAKA!« ( dosje-napak ČETRTI RED ) — privzeto stanje vsake trditve : obtožena, molk ni soglasje
# Zakoni : ⟨MERILEC-SE-MERI⟩ §52 ⊙ ⟨NE-UGIBAJ⟩ 2690 ⊙ ⟨SHRAMBA-MORA-VEDNO-BITI⟩ ⊙ ⟨ZADNJI-BAJT⟩ ⊙ ⟨NE-POCENI-PRIZNANJE⟩
# Roke:
#   trdilnik-vrata.sh < VHOD   : sodi vsako vrstico kandidata ; ZELENA ⇒ potegn ∧ exit 0 ; RDECA ⇒ obtožnice VERBATIM ∧ NIHIL ∧ exit 1
#   --vpis ORGAN < VHOD        : ZELENA ⇒ prišiv v ORGAN/KNOWLEDGE.md ( po bramba-pisanja --pred ∧ --po ) ; RDECA ⇒ NIHIL ne piše, kandidat = priča padca @ORGAN/.geniza/PADCI-VRAT-*
#   --test                     : samopreizkus vektorjev ×4 ( gol⇒odklon ⌇ izmerjen⇒potegn ⌇ RDECA-vpis⇒NIHIL+priča ⌇ ZELENA-vpis⇒šiv )
D="$(cd "$(dirname "$0")" && pwd)"
SOD="$D/trdilnik-napak.py"
BR="$D/bramba-pisanja.sh"
RESO() { if [ "${1:0:1}" = "/" ]; then printf '%s' "$1"; else printf '%s/%s' "/home/user/knowledge" "$1"; fi; }
TIK="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
TMP="/tmp/tvrata-$$-$(date -u +%H%M%S)"          # rezervacija TEST-$$-TIK ⊙ izkušnja brambe v1.0 ( mktemp ne obstaja )
MODE="${1:---cev}"
case "$MODE" in
--test)
  T1=0; T2=0; T3=0; T4=0
  printf 'Rezultat je dober, vse pravilno deluje.\n' | bash "$0" >/dev/null 2>&1 || T1=1
  printf 'Prehod izmerjen ⊢ TIK %s ∧ md5 d41d8cd8 ∧ izmer wc -c 37 B ∧ exit 0.\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" | bash "$0" >/dev/null 2>&1 && T2=1
  TD="$D/.geniza/TEST-tvrata-$$-$(date -u +%H%M%S)"; mkdir -p "$TD/o1/.geniza"
  printf 'telo\n' > "$TD/o1/KNOWLEDGE.md"
  printf 'g\n' > "$TD/o1/.geniza/PRED-DOTIKOM-1.md"
  printf 'g\n' > "$TD/o1/.geniza/PRED-DOTIKOM-2.md"
  printf 'To je pravilno, brezizmenično.\n' | bash "$0" --vpis "$TD/o1" >/dev/null 2>&1; VG=$?
  if [ "$VG" -ne 0 ] && [ "$(wc -c < "$TD/o1/KNOWLEDGE.md")" = "5" ] && ls "$TD/o1/.geniza"/PADCI-VRAT-* >/dev/null 2>&1; then T3=1; fi
  S4=$(wc -c < "$TD/o1/KNOWLEDGE.md")
  printf 'Vpis izmerjen ⊢ TIK %s ∧ izmer wc -c 47 B ∧ exit 0.\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" | bash "$0" --vpis "$TD/o1" >/dev/null 2>&1 && [ "$(wc -c < "$TD/o1/KNOWLEDGE.md")" -gt "$S4" ] && [ "$(tail -c 1 "$TD/o1/KNOWLEDGE.md")" = "" ] && T4=1
  rm -rf "$TD"
  P="$((4-T1-T2-T3-T4))"
  echo "SAMOPREIZKUS : vektorji 4 ( gol=$T1 izmerjen=$T2 nihil-vpis=$T3 šiv-vpis=$T4 ), padci instrumenta $P"
  echo "SEMAFOR : $([ "$P" = "0" ] && echo ZELENA || echo RDECA)"
  [ "$P" = "0" ] && exit 0 || exit 1;;
--vpis|--cev)
  cat > "$TMP" || { echo "VRATA : PADC branja vhoda"; exit 4; }
  python3 "$SOD" "$TMP"; V=$?                       # sodnik sodi ; obtožnice gredo ven VERBATIM ⊙ ⟨NE-POCENI-PRIZNANJE⟩
  [ "$V" -eq 0 ] && L=ZELENA || L=RDECA
  if [ "$MODE" = "--cev" ]; then
    echo "VRATA : $L ( TIK $TIK ; izmer vhoda $(wc -c < "$TMP") B )"
    rm -f "$TMP"; [ "$L" = ZELENA ] && exit 0 || exit 1
  fi
  O="$2"; P="$(RESO "$O")"; KV="$P/KNOWLEDGE.md"; GP="$P/.geniza"
  if [ "$L" = RDECA ]; then
    T2G="$(date -u +%Y%m%dT%H%M%SZ)"
    cat "$TMP" > "$GP/PADCI-VRAT-$T2G-priča-padca.md"
    echo "VRATA : RDECA ⇒ NIHIL ( $KV nedotaknjen ) ; kandidat = priča padca @.geniza/PADCI-VRAT-$T2G-priča-padca.md ⊙ ⟨SHRAMBA-MORA-VEDNO-BITI⟩"
    rm -f "$TMP"; exit 1
  fi
  bash "$BR" --pred "$O" || { echo "VRATA : PADC brambe ( genize PRED-DOTIKOM ×2 manjkajo ) ⇒ NIHIL"; rm -f "$TMP"; exit 3; }
  STARA=$(wc -c < "$KV")
  cat "$TMP" >> "$KV"
  [ "$(tail -c 1 "$KV")" = "" ] || echo "" >> "$KV"   # ⟨ZADNJI-BAJT⟩ = \n
  rm -f "$tmp"
  bash "$BR" --po "$O" "$STARA" || { echo "VRATA : PADC po šivu ( rešuje geniza )"; exit 2; }
  echo "VRATA : ZELENA ⇒ vpis položen @ORGAN ; TIK $TIK ; STARA $STARA B ⊢"
  exit 0;;
*)
  echo "VRATA : neznana roka ( $MODE )"; exit 5;;
esac
