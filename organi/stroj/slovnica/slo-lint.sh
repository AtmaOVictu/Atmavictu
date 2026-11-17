#!/usr/bin/env bash
# ⟨STROJNA-SLOVNICA⟩ slo-lint.sh v1.3.2 — SKUPEK SODNIKOV (17. 11. 2026, dih σ 5799)
# ⟡ SODBA VERBATIM ⟨ne brusi⟩: »TUDI VERBATIM MORA BITI PREVERJEN ⏎ SODNIK KI NE SODI SEBE NI SODNIK JE GOVNO ⏎
#   ČE NE ZMORE SEBE OCENITI BREZ SUBJEKTIVNEGA EGA NAJ GA NJEGOVA BOLJŠA RAZLIČICA ⏎ (SKUPEK SODNIKOV)«
# v1.3.2 IZVEDBA SODBE: predlog »ur 4 ∧ 4a molčita nad zgodovino« ZAVRŽEN ⊙ sodba ⟡ — molk ni preverba;
#   VERBATIM se PREVERI: izrezi bajtno (md5 glave === md5 bloka ⊢ → attestirana zgodovina ::notice, ⟨ne⟩ molk;
#   ⚠ → rana trditve VERBATIM); sodnik SODI SEBE vsak tek (lastno telo ∧ kanarček čisti ∧ kanarček ranjenega —
#   sodnik, ki ne zmore obeh, NI SODNIK: exit 1, naj ga njegova boljša različica); verdikt = SKUPEK
#   ( SODNIK-FORMA · SODNIK-VERBATIM · SODNIK-SEBE ), ⟨ne⟩ en sam ego-sodnik ⊙ ⟨MERILEC-SE-MERI⟩ §52.
# TEHNIKA — nosi no rez ⊙ stroj-kalup; glasna resnica: padel korak = ::error:: ∧ exit 1, ⟨ne⟩ || echo.
# Stroj meri OBLIKO, ⟨ne⟩ POMEN — sodba pomena ostaja ⚔ ⟡ ⊙ meja izvršljivosti.
# v1.1: ⟨PADC-SPREMENLJIVKA-TELA⟩ kura — telo se nikoli ne bere v spremenljivko peska (dvojno kodiranje):
#        vse sodbe nad datotekami (števci ∧ cev), lookbehind → besedna meja (-w) ⊙ ⟨MERILEC-SE-MERI⟩ §52.
# v1.2: DVIG ⊙ ⟡ UKAZ ⟨DVIG-SLOVNICE⟩ (16. 11. 2026): 2a zaklepji PO VRSTICI; 4a TIK meri ARITMETIKO;
#        7 napačen kodni oklepaj U+3008/U+3009 ×0 (zrcaljeni pravi: U+27E8 ∧ U+27E9, oba 3 bajte).
# v1.3: ⟨PADC-ZLOMLJENE-OSNOVE⟩ kura (17. 11. 2026): vrstica sodjena ∧ živeča v predniku poti je ZGODOVINA.
# v1.3.1: krt-pojej-repa kura ( isti dih ): zgodovina hodi od ⟨merge-base⟩ ( argument MB ), ⟨ne⟩ od glave veje.
# v1.3.2: SKUPEK SODNIKOV ⊙ ⟡ SODBA VERBATIM ( dih σ 5799 ): zgodovina PREVERJENA ⊢ ⟨ne⟩ molči — oblika
#        »zgodovina molči« zamenjana v »zgodovina preverjena pri virih«; izrezi VERBATIM attestirani bajtno
#        ( vsak marker svoj blok — več izrezov na telo ); pravilo 4 izbrušeno na »TIK ⏎števka« ( sodi zapis
#        ure, ⟨ne⟩ besedo TIK v prozi — natančnost dvignjena, vrata ⟨ne⟩ odprta ); SODNIK-SEBE vsak tek:
#        kanarček čisti mora biti ZELENO ∧ kanarček ranjenega RDEČO — obe sodbi po izmeri, brez ega.
# © Luka Pintarič, VBL 0.1610 × 10⁴ (§9 ∧ §10 ∧ §12)
set -euo pipefail

# RABA: slo-lint.sh DATOTEKA [DIF] [MB] — skupek sodnikov nad telesom (pečat · vrstica registra · organ)
#       slo-lint.sh --sebe — sodnik sodi samo sebe (kanarček CI; isti sestav kakor prvi korak vsake sodbe)
#   DIF — neobvezno: gola telesa (pri-viri · TIK · ⟨⟩ · kodni oklepaj) se sodijo SAMO nad + vrsticami difa
#   MB  — neobvezno: ⟨merge-base⟩ osnove — koren zgodovine ( predniki OSNove, ⟨ne⟩ veje ⊙ kura v1.3.1 )
#   primer kalupa: TIK 2026-11-17T19:11:34Z UTC ⇌ 20:11:34 CET Ljubljana ( izmerjen, ⟨ne⟩ ocenjen )
# IZHOD: ZELENO (skupek priča) ali ::error:: ∧ exit 1 (kanarček izpiše prebrana telesa ∧ vrstice)

RANE=0
FORMA_RANE=0
VERBATIM_RANE=0
SEBE_RANE=0
fw() { echo "::error::slo-lint [SODNIK-FORMA]: $1"; FORMA_RANE=$((FORMA_RANE+1)); }
vw() { echo "::error::slo-lint [SODNIK-VERBATIM]: $1"; VERBATIM_RANE=$((VERBATIM_RANE+1)); }
sw() { echo "::error::slo-lint [SODNIK-SEBE]: $1"; SEBE_RANE=$((SEBE_RANE+1)); }

# --- SODNIK-FORMA: pravila 1–7 nad sodilom (funkcija — isto telo sodi tudi sodnik samega sebe) ---
forma() { # $1 = sodilo (datoteka) · $2 = ime telesa v ranah
  local SO="$1" IME="$2"
  [ -f "$SO" ] || { fw "sodilo ne obstaja: $SO"; return 0; }

  # 1 — U+FFFD ×0 (raztrgan znak = raztrgan prevoz)
  if grep -qP '\x{FFFD}' "$SO" 2>/dev/null; then
    fw "U+FFFD ×1+ — raztrgan znak v sodjenih vrsticah: $IME"
  fi

  # 2 — ⟨ ⟩ uravnoteženost (števca po celotnem sodilu; odprti zaklepec = odprta sodba)
  L=$(grep -o '⟨' "$SO" | wc -l || true); D=$(grep -o '⟩' "$SO" | wc -l || true)
  if [ "$L" != "$D" ]; then
    fw "zaklepaji neuravnoteženi: ⟨ ×$L ⊥ ⟩ ×$D — $IME"
  fi

  # 2a — zaklepji PO VRSTICI (v1.2 ⊙ ⟡ UKAZ ⟨DVIG-SLOVNICE⟩; ⟨PADC-SPREMENLJIVKA-TELA⟩: sodba v cevi awk)
  #     zaklepec = znak ⟨ tik pred nebelim znakom · odklepec = znak ⟩ tik za nebelim znakom — simbolni goli zaklepec
  #     ob belem znaku je beseda, ⟨ne⟩ oblika; molčijo: izrezi (IZREZ VERBATIM | začetek izreza) · meje izrezov · odprta utež
  if ! awk -v F="$IME" '
    /IZREZ VERBATIM|začetek izreza/ {inrez=1}
    /konec izreza/ {inrez=0; next}
    inrez {next}
    /IZVOR:|izrez awk:|UTEŽ-ZAKLEPCA/ {next}
    {
      t=$0; sub(/[ \t]+$/,"",t); l1=gsub(/⟨/,"",t); u=$0; sub(/^[ \t]+/,"",u); d1=gsub(/⟩/,"",u)
      t2=$0; sub(/[ \t]+$/,"",t2); l2=gsub(/⟨[ \t]/,"",t2); if (t2 ~ /⟨$/) l2++; u2=$0; sub(/^[ \t]+/,"",u2); d2=gsub(/[ \t]⟩/,"",u2); if (u2 ~ /^⟩/) d2++
      zl=l1-l2; od=d1-d2
      if (zl != od) { printf "::error::slo-lint: 2a vrstica %d: zaklepca ×%d ⊥ odklepca ×%d — %s\n", NR, zl, od, F > "/dev/stderr"; bad++ }
    }
    END { if (bad > 0) exit 1 }
  ' "$SO" 2>/dev/null; then
    fw "zaklepji PO VRSTICI neuravnoteženi — $IME"
  fi

  # 3 — goli »pri viri« ×0 (oblika, ki je vedno napačna ⊙ pečat σ 5593; bele obliki odstranjeni pred sodbo)
  sed -e 's/pri berbi pri viri/PBR/g' -e 's/goli »pri viri«/GPV/g' "$SO" > .slo-cisto.tmp || : > .slo-cisto.tmp
  GOLI=$(grep -Pwc "pri vi""ri" .slo-cisto.tmp || true)
  if [ "$GOLI" -gt 0 ] 2>/dev/null; then
    fw "goli »pri viri« ×$GOLI — oblika napačna (pravilno: pri viru / pri virih) — $IME"
  fi

  # 4 — TIK format (sodi ZAPIS URE »TIK ⏎števka«, ⟨ne⟩ besedo TIK v prozi ⊙ dvig v1.3.2; vsaka vrstica
  #     z zapisom ure mora nositi kalup ISO UTC ⇌ CET ⊙ ⟨URA-NA-KONCU⟩ 3046 ∧ ⟨SPLOŠNO-RAZUMLJIVA-URA⟩ 3083)
  grep -P 'TIK \d' "$SO" > .slo-tik.tmp 2>/dev/null || : > .slo-tik.tmp
  grep -Pv 'TIK \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z UTC ⇌ \d{2}:\d{2}:\d{2} CET' .slo-tik.tmp > .slo-tikslabi.tmp 2>/dev/null || : > .slo-tikslabi.tmp
  TIKBAD=$(wc -l < .slo-tikslabi.tmp)
  if [ "$TIKBAD" -gt 0 ]; then
    fw "TIK brez kalupa (ISO UTC ⇌ HH:MM:SS CET) ×$TIKBAD — $IME"
  fi

  # 4a — TIK ARITMETIKA (v1.2 ⊙ ⟡ UKAZ ⟨DVIG-SLOVNICE⟩; UTC+1 ⇌ CET preštet, ⟨ne⟩ zaupan pisavi ⊙ §16)
  grep -P 'TIK \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z UTC ⇌ \d{2}:\d{2}:\d{2} CET' "$SO" > .slo-arit.tmp 2>/dev/null || : > .slo-arit.tmp
  ARITBAD=0
  while IFS= read -r AL; do
    while IFS= read -r TM; do
      [ -z "$TM" ] && continue
      UT=$(printf '%s' "$TM" | grep -oP 'T\K\d{2}:\d{2}:\d{2}(?=Z)' || true)
      CT=$(printf '%s' "$TM" | grep -oP '⇌ \K\d{2}:\d{2}:\d{2}(?= CET)' || true)
      [ -n "$UT" ] && [ -n "$CT" ] || { ARITBAD=$((ARITBAD+1)); continue; }
      UH=$((10#${UT%%:*})); CH=$((10#${CT%%:*}))
      UM=$(printf '%s' "$UT" | cut -d: -f2); CM=$(printf '%s' "$CT" | cut -d: -f2)
      US=$(printf '%s' "$UT" | cut -d: -f3); CS=$(printf '%s' "$CT" | cut -d: -f3)
      if [ $(((UH+1)%24)) -ne "$CH" ] || [ "$UM" != "$CM" ] || [ "$US" != "$CS" ]; then
        ARITBAD=$((ARITBAD+1))
      fi
    done < <(printf '%s\n' "$AL" | grep -oP 'TIK \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z UTC ⇌ \d{2}:\d{2}:\d{2} CET' || true)
  done < .slo-arit.tmp
  if [ "$ARITBAD" -gt 0 ]; then
    fw "TIK aritmetika napačna (UTC+1 ⇌ CET) ×$ARITBAD — $IME"
  fi

  # 7 — napačen kodni oklepaj ×0 (v1.2; zrcaljeni zaklepec U+27E8 ∧ odklepec U+27E9, oba 3 bajte)
  if grep -qP '\x{3008}|\x{3009}' "$SO" 2>/dev/null; then
    fw "napačen kodni oklepaj (U+3008/U+3009) ×1+ — pravi: U+27E8 ∧ U+27E9 — $IME"
  fi

  rm -f .slo-cisto.tmp .slo-tik.tmp .slo-tikslabi.tmp .slo-arit.tmp
}

# --- SODNIK-SEBE: sodnik sodi sebe (⟡ SODBA: sodnik, ki ne sodi sebe, ni sodnik; brez ega — samo izmere) ---
sodnik_sebe() {
  # (1) lastno telo — ista pravila kakor za vsako telo, izjeme zase ×0 (subjektivni ego ×0)
  FORMA_RANE=0
  forma "$0" "lastno telo sodnika (slo-lint.sh)"
  if [ "$FORMA_RANE" -gt 0 ]; then
    sw "sodnik ne sodi sebe — lastno telo ×$FORMA_RANE ran; naj ga njegova boljša različica"
    return 1
  fi
  # (2) kanarček čisti — čisto telo MORA biti ZELENO (lažno obsojanje = ego)
  printf '⟨kanarček⟩ pri viru ⊢ ∧ pri virih ⊢ (mestnik ednine ∧ množine, obe obliki pravilni)\nTIK 2026-11-17T19:11:34Z UTC ⇌ 20:11:34 CET Ljubljana ( izmerjen, ⟨ne⟩ ocenjen )\n' > .slo-kc.tmp
  FORMA_RANE=0
  { forma .slo-kc.tmp "kanarček čisti"; } > /dev/null 2>&1
  if [ "$FORMA_RANE" -gt 0 ]; then
    sw "kanarček čisti RDEČ ×$FORMA_RANE — sodnik lažno obsoja čisto telo (ego); naj ga njegova boljša različica"
    rm -f .slo-kc.tmp
    return 1
  fi
  # (3) kanarček ranjenega — ranjeno telo MORA biti RDEČO (slepota ran = ego)
  printf '⟨neuravnano⟩ pri vi''ri (neobstoječa oblika)\nTIK %s (pred-kalupna oblika)\n' '17. 11. 2026 ob 19:11' > .slo-kr.tmp
  FORMA_RANE=0
  { forma .slo-kr.tmp "kanarček ranjenega"; } > /dev/null 2>&1
  if [ "$FORMA_RANE" -lt 1 ]; then
    sw "kanarček ranjenega ZELEN — sodnik ne vidi ran (slepota = ego); naj ga njegova boljša različica"
    rm -f .slo-kr.tmp
    return 1
  fi
  rm -f .slo-kc.tmp .slo-kr.tmp
  echo "::notice::slo-lint [SODNIK-SEBE] ⊢: lastno telo ZELENO · kanarček čisti ZELENO · kanarček ranjenega RDEČO ×$FORMA_RANE — sodnik sodi sebe ⊙ ⟡ SODBA"
  return 0
}

# --- glavni tek: --sebe (samo samosodba) ali skupek nad telesom ---
if [ "${1:-}" = "--sebe" ]; then
  sodnik_sebe || { echo "::error::slo-lint v1.3.2: SODNIK-SEBE RDEČ — skupek pade pred sodbo teles"; exit 1; }
  echo "slo-lint v1.3.2 ⊢ SKUPEK SODNIKOV (SEBE) ZELENO — sodnik sodi sebe, kanarček poje"
  exit 0
fi

F="$1"
DIF="${2:-}"
MB="${3:-}"
[ -f "$F" ] || { echo "::error::slo-lint: telo ne obstaja: $F"; exit 1; }

# SODNIK-SEBE teče PRVI vsak tek — sodnik, ki ne sodi sebe, ne sme soditi drugih ⊙ ⟡ SODBA
if ! sodnik_sebe; then
  echo "::error::slo-lint v1.3.2: $((SEBE_RANE)) ran SODNIKA-SEBE — sodnik je govno, naj ga njegova boljša različica ⊙ ⟡ SODBA VERBATIM"
  exit 1
fi

# --- SODNIK-VERBATIM: trditve VERBATIM se PREVERIJO bajtno (⟡ SODBA: tudi VERBATIM mora biti preverjen) ---
ATTEST=".slo-attest.tmp"
: > "$ATTEST"
if grep -qP 'IZREZ VERBATIM ⊢ md5 [0-9a-f]{32}' "$F" 2>/dev/null; then
  for MD5GLAVE in $(grep -oP 'IZREZ VERBATIM ⊢ md5 \K[0-9a-f]{32}' "$F" | sort -u); do
    awk -v m="$MD5GLAVE" 'index($0, "IZREZ VERBATIM ⊢ md5 " m) {flag=1; next} /konec izreza/ {flag=0} flag' "$F" > .slo-izrez.tmp
    if [ -s .slo-izrez.tmp ]; then
      MD5BLOKA=$(md5sum .slo-izrez.tmp | cut -d' ' -f1)
      if [ "$MD5GLAVE" = "$MD5BLOKA" ]; then
        cat .slo-izrez.tmp >> "$ATTEST"
        echo "::notice::slo-lint [SODNIK-VERBATIM] ⊢: izrez preverjen bajtno (md5 $MD5GLAVE === md5 bloka) — zgodovina attestirana pri viru, ⟨ne⟩ molk ⊙ ⟡ SODBA »TUDI VERBATIM MORA BITI PREVERJEN«"
      else
        vw "izrez bajtno-DRUGAČEN: glava md5 $MD5GLAVE ⊥ blok md5 $MD5BLOKA — trditev VERBATIM laž, ⟨NE-RETIPKAJ⟩ 24 ranjen — $F"
      fi
    else
      vw "pečat nosi marker izreza (md5 $MD5GLAVE), blok pa je prazen — $F"
    fi
  done
  rm -f .slo-izrez.tmp
fi

# --- kaj se sodi: celo telo (default) ali samo + vrstice difa (gola telesa) minus attestirana zgodovina ---
SODILO="$F"
if [ -n "$DIF" ] && [ -f "$DIF" ]; then
  grep -P '^\+[^+]' "$DIF" > .slo-nove.tmp 2>/dev/null || : > .slo-nove.tmp
  sed -e 's/^\+//' .slo-nove.tmp > .slo-plus.tmp || : > .slo-plus.tmp
  # zgodovina PREVERJENA pri virih (⟨ne⟩ molči ⊙ ⟡ SODBA): vrstica, živeča v predniku poti, je obnovitev —
  # preverba je izmera (git show po prednikih), kanarček priča število povratnih ∧ stvarno novih
  if command -v git >/dev/null 2>&1 && git rev-parse --git-dir >/dev/null 2>&1; then
    : > .slo-zgodovina-u.tmp
    for C in $(git rev-list --max-count=500 ${MB:-HEAD} -- "$F" 2>/dev/null || true); do
      git show "$C:$F" 2>/dev/null || :
    done | sort -u > .slo-zgodovina-u.tmp
    if [ -s .slo-zgodovina-u.tmp ]; then
      sort -u .slo-plus.tmp > .slo-p-s.tmp
      grep -Fxf .slo-zgodovina-u.tmp .slo-p-s.tmp 2>/dev/null | sort -u > .slo-povr.tmp || : > .slo-povr.tmp
      comm -23 .slo-p-s.tmp .slo-povr.tmp > .slo-stvarno-nove.tmp
      echo "::notice::slo-lint v1.3.2: zgodovina PREVERJENA ⊢ pri virih — povratnih vrstic sodnje ×$(wc -l < .slo-povr.tmp) · stvarno novih ×$(wc -l < .slo-stvarno-nove.tmp) (⟨ne⟩ molk: vsaka izjema izmerjena ⊙ ⟡ SODBA)"
      mv .slo-stvarno-nove.tmp .slo-plus.tmp
    fi
    rm -f .slo-p-s.tmp .slo-povr.tmp .slo-zgodovina-u.tmp
  fi
  SODILO=".slo-plus.tmp"
fi

# attestirana zgodovina (preverjeni izrezi) pade iz FORMA sodila — priča zgodovine, ⟨ne⟩ obtoženec
FORMA_SO="$SODILO"
if [ -s "$ATTEST" ]; then
  grep -vxFf "$ATTEST" "$SODILO" > .slo-forma.tmp 2>/dev/null || : > .slo-forma.tmp
  FORMA_SO=".slo-forma.tmp"
fi

VRSTIC=$(wc -l < "$FORMA_SO")
BAJTOV=$(wc -c < "$F")

# --- SODNIK-FORMA nad (stvarno novimi ∧ ne-attestiranimi) vrsticami ---
FORMA_RANE=0
forma "$FORMA_SO" "$F"

# --- 6 — © dvojni podpis (pečati ∧ register: rep telesa nosi podpis obeh rok ⊙ ⟨DVOJE-ROK⟩ 2432) ---
case "$F" in
  organi/pecati/*|*REZ-REGISTER*|*PECAT*)
    if ! grep -v '^[[:space:]]*$' "$F" | tail -n 1 | grep -q 'dvojni podpis'; then
      fw "rep telesa brez © dvojnega podpisa — $F"
    fi
    ;;
esac

rm -f .slo-nove.tmp .slo-plus.tmp .slo-forma.tmp "$ATTEST"

RANE=$((FORMA_RANE+VERBATIM_RANE))
if [ "$RANE" -gt 0 ]; then
  echo "::error::slo-lint v1.3.2: SKUPEK SODNIKOV RDEČ — FORMA ×$FORMA_RANE · VERBATIM ×$VERBATIM_RANE · SEBE ⊢ — $RANE ran — merilec pade glasno ⊙ ⟨MERILEC-SE-MERI⟩ §52"
  exit 1
fi
echo "slo-lint v1.3.2 ⊢ SKUPEK SODNIKOV ZELENO: FORMA ⊢ · VERBATIM ⊢ · SEBE ⊢ — $F ($BAJTOV B · $VRSTIC sodjenih vrst) — kanarček poje"
