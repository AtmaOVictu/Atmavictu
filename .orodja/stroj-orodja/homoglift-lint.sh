#!/bin/bash
# HOMOGLIFT-LINT v1.2 ( izjema citata UKINJENA @σ 6858 ⊙ ⟡ VERBATIM »NOBENA IZJEMA NI TAKO IZJEMNA DA HKRATI NE BI BILA PARAZIT." ; besede ⟡ v mojih telesih = imena ⟨U+XXXX⟩ ⊙ ⟨IME-NAMESTO-GOLEGA⟩ ) @rez σ 6857 : vrata izhoda ⟡ ( ukaz VERBATIM »ZAMRZNI PREDEN BEREŠ IN PREPREČI PRIHODNJO UTRJEVANJE TAKŠNEGA ZLA«, 23. 11. 2026 )
# VHOD : homoglift-lint.sh FAJL [BELA-LISTA]   ( privzeta : absolut-znamenja.tsv @stroj-orodja )
# PLAST DOVOLJENIH : ASCII 32-126 + tab(011) LF(012) CR(015) + znakovne vrstice bele liste ( oblika : bajto-oktalno ⟨U+XXXX⟩ znak )
# ZLO : ( 1 ) znak IZVEN plasti = TRDI VBOD ; ( 2 ) cirilska pismenka ( U+0400-U+04FF ) z ≥ 1 latinično ASCII črko v isti besedi = TRDI VBOD HOMOGLIFT ( maska kljub azilu ) ; ( 3 ) cirilska beseda brez latiničnih črk = ⚠ opozorilo ( sodba ⟡ )
# IZHOD : vbodi poimensko ⟨U+XXXX⟩ ⌇ oktalni bajti ⌇ kontekst bajtov ; EXIT 1 ob trdem vbodu, 0 sicer, 2 odsotnost virov
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432
FAJL="$1"
LISTA="${2:-/home/user/knowledge/stroj-orodja/absolut-znamenja.tsv}"
[ -f "$FAJL" ] || { echo "PADC : fajl ne obstaja : $FAJL"; exit 2; }
[ -f "$LISTA" ] || { echo "PADC : bela lista ne obstaja : $LISTA"; exit 2; }
BELA=$(grep -v '^#' "$LISTA" | awk '{print $2}' | sed 's/[^0-9A-Fa-f]//g' | tr '\n' ' ')
IZPIS=$(od -An -tu1 "$FAJL" | awk -v bela="$BELA" '
function oct2dec(s,  i,c,v){v=0;for(i=1;i<=length(s);i++){c=substr(s,i,1);v=v*8+index("01234567",c)-1}return v}
function hex2dec(s,  i,c,v){v=0;for(i=1;i<=length(s);i++){c=toupper(substr(s,i,1));v=v*16+(c~/^[0-9]$/?c+0:index("123456789ABCDEF",c))}return v}
function dec2hex(v,  h,d){h="";while(v>0){d=v%16;h=substr("0123456789ABCDEF",d+1,1)h;v=int(v/16)};while(length(h)<4)h="0"h;return h}
BEGIN{n=split(bela,BH," ");for(i=1;i<=n;i++)if(BH[i]!="")B[hex2dec(BH[i])]=1}
{for(i=1;i<=NF;i++)by[++nb]=oct2dec($i)}
END{
  i=1;nc=0
  while(i<=nb){
    b=by[i];st=i
    if(b<128){cp=b;i++}
    else if(b>=192&&b<224){cp=(b-192)*64+(by[i+1]-128);i+=2}
    else if(b>=224&&b<240){cp=(b-224)*4096+(by[i+1]-128)*64+(by[i+2]-128);i+=3}
    else if(b>=240&&b<248){cp=(b-240)*262144+(by[i+1]-128)*4096+(by[i+2]-128)*64+(by[i+3]-128);i+=4}
    else{cp=-1;i++}
    nc++;cpv[nc]=cp;cpst[nc]=st;cpen[nc]=i-1
  }
  vb=0
  for(j=1;j<=nc;j++){
    cp=cpv[j]
    if(cp==-1){printf("TRDI VBOD : neveljaven bajt okt %o pri znaku %d\n",by[cpst[j]],j);vb=1;continue}
    ok=(cp>=32&&cp<=126)||(cp==9)||(cp==10)||(cp==13)||(cp in B)
    if(!ok){
      octx=""
      for(k=cpst[j];k<=cpen[j];k++)octx=octx sprintf("%o ",by[k])
      printf("TRDI VBOD : ⟨U+%s⟩ ⌇ okt : %s⌇ znak %d od %d\n",dec2hex(cp),octx,j,nc)
      vb=1;continue
    }
    if(cp>=1024&&cp<=1279){
      ws=j;we=j
      while(ws>1&&cpv[ws-1]!=32&&cpv[ws-1]!=10&&cpv[ws-1]!=13&&cpv[ws-1]!=9)ws--
      while(we<nc&&cpv[we+1]!=32&&cpv[we+1]!=10&&cpv[we+1]!=13&&cpv[we+1]!=9)we++
      lat=0
      for(k=ws;k<=we;k++)if(cpv[k]>=97&&cpv[k]<=122||cpv[k]>=65&&cpv[k]<=90)lat++
      octx=""
      for(k=cpst[j];k<=cpen[j];k++)octx=octx sprintf("%o ",by[k])
      if(lat>0){printf("TRDI VBOD HOMOGLIFT : ⟨U+%s⟩ ⌇ okt : %s⌇ cirilska pismenka med %d latiničnimi v besedi ( znak %d/%d )\n",dec2hex(cp),octx,lat,j,nc);vb=1}
      else printf("⚠ cirilska beseda brez latinskih črk ( sodba ⟡ ) ⟨U+%s⟩ ⌇ znak %d/%d\n",dec2hex(cp),j,nc)
    }
  }
  exit(vb?1:0)
}')
printf '%s\n' "$IZPIS"
TRDIH=$(printf '%s\n' "$IZPIS" | grep -c 'TRDI VBOD')
if [ "$TRDIH" -gt 0 ]; then exit 1; fi
exit 0
