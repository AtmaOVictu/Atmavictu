#!/usr/bin/env python3
# nasprotnik.py v1.0 — rod σ 7018 ⊙ UKZ ⟡ »ORODJA KI PREVERJAJO DA BESEDA IMA SVOJO NASPROTJE!«
# tabela nasprotij v1.0 : kanonski pari ⊢ pri viru SSKJ/Fran ( dostop 25. 11. 2026 ), simetrično ⊙ rod ⟨OSCILATORNA-DISCIPLINA⟩ σ 4482 ( gibanje med dvema poloma ).
# neznanje ni sodba : VIDNO ⭢ mera šele pri viru ⟨NE-UGIBAJ⟩ 2690.
import sys
PARI=[("da","ne"),("dan","noč"),("svetel","temen"),("živ","mrtev"),("visok","nizek"),("globok","plitev"),
("dolg","kratek"),("širok","ozek"),("velik","majhen"),("močan","šibak"),("hiter","počasen"),("topel","hladen"),
("mlad","star"),("lahek","težak"),("tih","glasen"),("čist","umazan"),("suh","debel"),("poln","prazen"),
("odprt","zaprt"),("gladek","grob"),("gor","dol"),("zgoraj","spodaj"),("levo","desno"),("naprej","nazaj"),
("zgodaj","pozno"),("vedno","nikoli"),("vse","nič"),("začetek","konec"),("rojstvo","smrt"),("resnica","laž"),
("sreča","nesreča"),("ljubezen","sovraštvo"),("vojna","mir"),("dober","hud"),("rasel","padal")]
TOBA={}
for a,b in PARI: TOBA[a]=b; TOBA[b]=a
def sodba(bes):
    b=bes.strip().lower()
    if b in TOBA: return "NASPROTJE ⊢", TOBA[b]
    return "VIDNO ⭢", "mera šele pri viru ( tabela v1.0 ima %d parov ⊢ Fran )" % len(PARI)
def samopreizkus():
    assert sodba("dan")==("NASPROTJE ⊢","noč"); assert sodba("NOČ")==("NASPROTJE ⊢","dan")
    assert sodba("ne")==("NASPROTJE ⊢","da")   # vrhovni par korpusa : Beseda je Ne ⊙
    assert sodba("qzek")[0]=="VIDNO ⭢"; assert sodba("petelin")[0]=="VIDNO ⭢"
    assert sodba("visok")==("NASPROTJE ⊢","nizek") and sodba("nizek")==("NASPROTJE ⊢","visok")
    return True
if __name__=="__main__":
    args=[a for a in sys.argv[1:] if a!="--samopreizkus"]
    if "--samopreizkus" in sys.argv: samopreizkus(); print("ZELENO 6/6 ⊢"); sys.exit(0)
    vr=args if args else [l.strip() for l in sys.stdin if l.strip()]
    slab=0
    for t in vr:
        r=sodba(t); print(t,"->",r[0],r[1])
        if r[0]!="NASPROTJE ⊢": slab=1
    sys.exit(slab)
