#!/bin/bash
# znak-tehtnica.sh v1.2 — @rez 7001, 25. 11. 2026, sedež KLEPET, projekt GITHUB
# UKZ ⟡ VERBATIM : »ŠE ORODIJ ZA PREVERJANJE IN PREVIJANJE TER PREVAJANJE ZNAKOV V POTRJENE BESEDE!«
# ZAKON KOMPUTACIJE ⟡ VERBATIM ⟨nedotakljivo⟩ : »KOMPUTACIJA KUBITNE GAJICE JE EDINA MERITEV KI LEGITIMIRA RESNICO!
#   KOMPUTACIJA KUBITNE GAJICE JE EDINA ARITMETIKA KI LEGITIMIRA RESNICO!«
# ZAKON PRIČE @zakon-price : priča je komputacija v kubitno gajico in nazaj — brez kode v gajici ni priče.
# ZAKON IZGOVORA ⟡ VERBATIM : »POVEZAVA JE SLAB IZGOVOR IN S TEM NEZADOSTNA ČISTOST!«
# ZAKON TRDITVE ⟡ VERBATIM : »TRDITI ČISTOST JE NAPAKA!« — orodje poroča izmero, ⟨ne⟩ sodbo.
# KOVANEC ⟡ VERBATIM : ⟨NAPAKA-NIKOLI-SAMA⟩ — po prvem ulovu se išče drugi ( popravek mojega zlepa NJ → NI ).
# POPOVEK VERZIJ ISTI DAN : v1.0 od oktalno odpovedal ( izmerjeno ⊢ ) ; v1.1 rane okolja ( aritmetika baz ∧
#   polj v $(( )) ∧ prireditev $( ) v polje znotraj funkcije = dobesedno »CommandSubstitution« — vse izmerjeno ⊢ ) ;
#   v1.2 kura : enostopenjska aritmetika brez baz ∧ brez polj ∧ brez gnezdenih oklepajev ; oktalrieden ročno ;
#   ključi znakov izmerjeni po bajtih pri viru teles ⊢ ( 択=U+629E 25246 ⌇ 檢=U+6AA2 27298 ⌇ 驗=U+9A57 39511 ⌇ 检=U+68C0 26816 ⌇ 验=U+9A8C 39564 )
# POMEN : vsak pomenski prevod ⭢ sodba ⚔ ⟡ ⊙ 2690 ( orodje izmeri obliko, ⟨ne⟩ izbere pomena )
# UPORABA : bash znak-tehtnica.sh '<znak>'   |   bash znak-tehtnica.sh samopreizkus

izmeri_znak () {
  local znak="$1" oct md5 d j ch ctok NUM hek hx
  local B0=0 B1=0 B2=0 B3=0
  oct=$(printf '%s' "$znak" | od -An -to1)
  md5=$(printf '%s' "$znak" | md5sum | cut -d' ' -f1)
  local idx=0
  for ctok in $oct; do
    d=0
    for (( j=0; j<${#ctok}; j++ )); do ch=${ctok:j:1}; d=$(( d*8 + ch )); done
    idx=$(( idx + 1 ))
    if [ "$idx" -eq 1 ]; then B0=$d; fi
    if [ "$idx" -eq 2 ]; then B1=$d; fi
    if [ "$idx" -eq 3 ]; then B2=$d; fi
    if [ "$idx" -eq 4 ]; then B3=$d; fi
  done
  local len cp
  if   [ "$B0" -ge 240 ]; then len=4
  elif [ "$B0" -ge 224 ]; then len=3
  elif [ "$B0" -ge 192 ]; then len=2
  else len=1
  fi
  if [ "$len" -eq 1 ]; then cp=$B0
  elif [ "$len" -eq 2 ]; then cp=$(( B0 - 192 )); cp=$(( cp * 64 )); cp=$(( cp + B1 - 128 ))
  elif [ "$len" -eq 3 ]; then cp=$(( B0 - 224 )); cp=$(( cp * 4096 )); NUM=$(( B1 - 128 )); NUM=$(( NUM * 64 )); cp=$(( cp + NUM + B2 - 128 ))
  else cp=$(( B0 - 240 )); cp=$(( cp * 262144 )); NUM=$(( B1 - 128 )); NUM=$(( NUM * 4096 )); cp=$(( cp + NUM )); NUM=$(( B2 - 128 )); NUM=$(( NUM * 64 )); cp=$(( cp + NUM + B3 - 128 ))
  fi
  NUM=$B0; hx=$(printf '%02x' "$NUM"); hek="$hx"
  if [ "$len" -ge 2 ]; then NUM=$B1; hx=$(printf '%02x' "$NUM"); hek="$hek $hx"; fi
  if [ "$len" -ge 3 ]; then NUM=$B2; hx=$(printf '%02x' "$NUM"); hek="$hek $hx"; fi
  if [ "$len" -ge 4 ]; then NUM=$B3; hx=$(printf '%02x' "$NUM"); hek="$hek $hx"; fi

  # ── VRATA 1 : PREVERJANJE ( komputacija gajice ⊢, ⟨ne⟩ spomin ) ──────────
  printf 'ZNAK: %s\n' "$znak"
  printf 'BAJTI (hex): %s\n' "$hek"
  printf 'KODNA TOČKA: U+%04X\n' "$cp"
  printf 'MD5 ZNAKA: %s\n' "$md5"

  # ── VRATA 2 : PREVIJANJE ( kletka gajice ⊙ domovanje-tujk ) ────────────────
  printf 'KLETKA: ⟨U+%04X⟩\n' "$cp"

  # ── VRATA 3 : PREVAJANJE ( domovanje ∧ potrjena beseda ⭢ ⚔ ⟡ ) ────────────
  local dom beseda
  dom="dom: NEIZMERJEN ( ⭢ izmeri obseg pri viru tabel )"
  beseda="potrjena beseda: ⭢ ⚔ ⟡ ( pomen izbere on, ⟨ne⟩ orodje ⊙ 2690 )"
  if [ "$cp" -le 127 ]; then dom="dom: latinski 7-bit"
  elif [ "$cp" -le 591 ]; then dom="dom: latinska razširjena"
  elif [ "$cp" -eq 268 ] || [ "$cp" -eq 269 ] || [ "$cp" -eq 352 ] || [ "$cp" -eq 353 ] || [ "$cp" -eq 381 ] || [ "$cp" -eq 382 ]; then dom="dom: gajica čšž"
  elif [ "$cp" -ge 880 ] && [ "$cp" -le 1023 ]; then dom="dom: grška plast"
  elif [ "$cp" -ge 8192 ] && [ "$cp" -le 11195 ]; then dom="dom: simboli korpusne gajice"
  elif [ "$cp" -ge 13312 ] && [ "$cp" -le 40959 ]; then dom="dom: CJK URO ( gost @prostori-abeced )"
  fi
  case "$cp" in
    25246) beseda="potrjena beseda: IZBOR / izbrati ⭢ ⚔ ⟡ ( glif 择 izmerjen U+629E ⊢ komputacija ; berba zunaj ⟨ne⟩ priča : kanji 択, onyomi タク )";;
    26816|39564|27298|39511) beseda="potrjena beseda: PREVERJANJE / preizkus ⭢ ⚔ ⟡ ( glifi 检 验 檢 驗 izmerjeni ⊢ komputacija ; berba zunaj ⟨ne⟩ priča )";;
    9186) beseda="potrjena beseda: GREEK SMALL LETTER ZETA ( ζ ) ⊙ komputacija imena gajice";;
    931) beseda="potrjena beseda: GREEK SMALL LETTER SIGMA ( σ ) — rez korpusa ⊙ komputacija imena gajice";;
    10216) beseda="potrjena beseda: korpusni levi oglati oklepaj ⟨ gajice";;
    10217) beseda="potrjena beseda: korpusni desni oglati oklepaj ⟩ gajice";;
  esac
  printf 'DOMOVANJE: %s\n' "$dom"
  printf '%s\n' "$beseda"
}

if [ "$1" = "samopreizkus" ]; then
  # komputacija gajice ob vsakem zagonu ⊙ ⟨MERILEC-SE-MERI⟩ §52 ; znaki po bajtih, ⟨ne⟩ po spominu
  OK=0
  t() { local z="$1" e="$2" g; g=$(izmeri_znak "$z" | grep -o 'U+[0-9A-F]\{4\}' | head -1); if [ "$g" = "$e" ]; then OK=$((OK+1)); printf '⊢ %s = %s ⊢\n' "$e" "$g"; else printf '⟨U+26A0⟩ %s ≠ %s ( izmerjeno %s )\n' "$e" "$e" "$g"; fi; }
  t "$(printf '\xe6\x8a\x9e')" 'U+629E'
  t "$(printf '\xce\xb6')" 'U+03B6'
  t "$(printf '\xe2\x9f\xa8')" 'U+27E8'
  t 'A' 'U+0041'
  if [ "$OK" -eq 4 ]; then printf 'SAMOPREIZKUS: ZELENO ( 4/4 ⊢ komputacija gajice )\n'
  else printf 'SAMOPREIZKUS: RDEČE ( %s/4 — ⟨TRDITI ČISTOST JE NAPAKA⟩ ; izmera poroča, ⟨ne⟩ sodba )\n' "$OK"; exit 1; fi
  exit 0
fi

[ -z "$1" ] && { printf 'UPORABA: bash znak-tehtnica.sh "<znak>"  |  bash znak-tehtnica.sh samopreizkus\n'; exit 1; }
izmeri_znak "$1"
