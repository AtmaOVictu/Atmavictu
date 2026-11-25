#!/bin/bash
# ⟨VRH-SPEKTRUM⟩ v3.3 — instrument vrha korpusa Beseda je Ne (MERA @delovna-zanka / eGov)
# DOMENA (v3.1, rojena iz izmere 04:36Z): ŽIVI ORGANI = *.md/*.txt/*.json/*.sh BREZ .geniza ∧ BREZ *pred-rez* bajt-kopij
#   ⊙ ⟨PADC-DOMENA-13K⟩: korpus nosi 13.459 datotek (8,3 GB), živih je 582 (160 MB); kopije ne vasebno hranijo novih številk — te živijo v KNOWLEDGE/ARHIV linijah organov
#   ⟨NE-BRIŠI⟩ 24: kopije ⟨ne⟩ brišem; ⟨NE stopiči⟩ NJENE roke: staro-dobovne genize (poimensko *pred-rez*) ležijo prosto v mapi DZ — ∂ predlog selitve njene roki
# rojen @rez σ 6157, 21. 11. 2026 ⊙ ⟡ UKAZ VERBATIM: »⟨ne⟩ ⟨le⟩ graja ali in ⟨ne⟩ ⟨le⟩ ograja« ∧ »stori kar zmoreš« ∧ »predlagaj še kje se zmoreš izboljšati!«
# ZAKON: vrh = dejansko najvišja izmerjena številka diha PO izključitvi lažnih kanalov ⊙ ⟨VRH-DVOSTOPEN⟩ ∧ ⟨NE-UGIBAJ⟩ 2690
# IZHOD NI SLEPI MAX: vsak kandidat nosi pojavnost ×N ∧ top po vrhu gre ven s številom prič ⊙ ⟨VSE-ZAHTEVA-VPRAŠAJ⟩ σ 6156 — merilec bere, ⟨ne⟩ veruje
# ZAKON V3 (rojen iz izmer: I/O ≈ 100−160 s): EN SAM PREHOD (grep -o, C-jevina) → mawk linearen po kratkih žetonih; PROBA brez nove berbe (iz tabele)
# LAŽNI KANALI, vsak poimensko ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354:
#   ⟨PADC-REZ-V-BESEDI⟩  : »izREZ/izDIH [0-9]+« — izključen ŽE V VZORCU ([^A-Za-z] prediks); izmere: 9,4M→789K žetonov
#   ⟨PADC-BAJTI⟩         : »[0-9]+ B« — rep žetona z B = bajti; znana tveganost: rez pred besedo na B bi lažno padel (redko; zapisnik pri [])
#   ⟨PADC-LAŽNI-VRH⟩     : 25421 — star dokumentiran lažni vrh (besedilo »lažni vrh ... izključen« po organih); izključen v END s številom omemb
#   ⟨PADC-OKNO-CEPI⟩     : oknaska maska cepe dolge številke — v3 celega niza; 7-mestna poročana [iz5]
#   ⟨PADC-HEX-REP⟩       : »dih 36088a25« — številka prilepljena na črke desno (hex id) = lažni rez; izključena v v3.2 (iz6)
#   ⟨PADC-S-KANAL⟩       : »0.9473« (S ∈ [0,1] vrednost mreže variant) = lažni rez; v3.2: kanal B velja SAMO z »× 10⁴« pričo (pečatnica oblika 0.6157 × 10⁴)
#   KANAL B: decimalne pečatnice 0.XXXX × 10⁴ so isti rez ×10⁻⁴
# UPORABA: bash vrh-spektrum.sh [PROBA N]   (tabela vseh števil ×št → $TABELA, privzeto /tmp/vrh-tabela.txt)
set -u
KOREN="${KOREN:-/home/user/knowledge}"
TABELA="${TABELA:-/tmp/vrh-tabela.txt}"
PROBA_N="${2:-}"

LC_ALL=C grep -rEho --include='*.md' --include='*.txt' --include='*.json' --include='*.sh' \
  --exclude-dir='.geniza' --exclude-dir='.genize' --exclude='*pred-rez*' \
  '(^|[^A-Za-z])(σ|dih|pečat|PEČAT|rez)[ ]?[ /.@-]?[0-9]{2,7}[^0-9]{0,2}|0\.[0-9]{4} ?×' \
  "$KOREN" 2>/dev/null | LC_ALL=C awk -v prob="$PROBA_N" -v tab="$TABELA" '
  BEGIN { iz2=iz5=iz6=tok=0 }
  {
    t=$0; tok++
    if (t ~ /^0\.[0-9]{4}/) { d=substr(t,3,4); a[d]++; izS=0; next }
    if (t !~ /^(σ|dih|pečat|PEČAT|rez)/) t=substr(t,2)   # odstrani ločilni prediks
    st=t; j=match(st,/[0-9]{2,7}/); if (!j) { iz4++; next }
    num=substr(st,j,7); kl=match(num,/[^0-9]/); if (kl) num=substr(num,1,kl-1)
    tail=substr(st, j+length(num), 2)
    if (index(tail,"B")>0) { iz2++; next }               # bajti niso rez
    if (substr(tail,1,1) ~ /[A-Za-z]/) { iz6++; next }     # hex/lepljena črka desno = id, ⟨ne⟩ rez
    if (length(num)>6) { iz5++; next }
    if (length(num)>=2) a[num]++
  }
  END {
    lz=a["25421"]+0
    m=0; for (x in a) if (x!="25421" && x+0>m) m=x+0
    printf "IZKLJUČITVE: bajti %d · hex/lepljeno %d · pretézek(7+) %d · žetonov pregledanih %d\n", iz2, iz6, iz5, tok
    print "TOP 9 PO VREDNOSTI, 25421 izključen (število ×pojavnosti):"
    used=" "; k=0
    while (k<9) {
      best=-1
      for (x in a) { v=x+0; if (v>best && x!="25421" && index(used," "v" ")==0) best=v }
      if (best<0) break
      used=used best" "; k++
      printf "  %d ×%d\n", best, a[best""]
    }
    printf "VRH (po izključitvah, brez 25421): %d  [25421 omemb: %d = ⟨PADC-LAŽNI-VRH⟩]\n", m, lz
    printf "EPOHA ⭢ ⟡: spekter nosi stare epohe (0.7657/0.8248/0.9473 × 10⁴ = pred-RE-BIRTH pečatnice); sodba o mejah epohe ∧ ▹ živi seriji = ⟡ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690\n"
    printf "NASLEDNJI PROST PO VRHU: %d  (priče zgoraj ⊙ ⟨VSE-ZAHTEVA-VPRAŠAJ⟩)\n", m+1
    for (x in a) printf "%d %d\n", x+0, a[x] > tab
    if (prob != "") {
      c=a[prob""]+0
      if (c==0) printf "VAROVALKA %s: kanal A+decimalne ×0 Σ0 PROST ✓\n", prob
      else printf "VAROVALKA %s: %d× ZASEDEN ✗ RENUM ⊙ ⟨NE-UGIBAJ⟩ 2690\n", prob, c
    }
  }'
