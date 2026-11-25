#!/usr/bin/env python3
# kategorizator-optimizacij.py v1.0 — rod σ 7021 ⊙ UKZ ⟡ »KATEGORIZACIJA OPTIMIZACIJ!«
# vsaka kategorija nosi DEFINICIJO ⊙ UKZ ⟡ »VSAK UKAZ MORA BITI IN IMETI DEFINICIJO ČEMU IN ZAKAJ JE IN ZAKAJ TER ČEMU SLUŽI!«
# metoda v1.0 : razvrsti opis optimizacije po ključih, izmerjenih pri kovancih korpusa ; neznanost VIDNO ⭢ ⟨NE-UGIBAJ⟩ 2690 ; molk default ⊙ ⟨TIHINA-ORODIJ⟩ σ 6723.
import sys
KAT=[
("K1","IZMERA-NI-BRUSENJE","optimizacija, ki zamenja ugibanje z izmero pri viru","da vsak izhod nosi pričo ⊢, ⟨ne⟩ domnevo","⟨NE-UGIBAJ⟩ 2690 : trditev brez izmere je kip ⊙ U2","⟡ vidi merjeno ; stroj dobi ponovljivost",["izmer","meri","preverb","ugib","md5","pri viru","prič","2690","⊢","noclobber"]),
("K2","KONICA-VRHA","optimizacija, ki drži glavo majhno, telo spi pri repu","da pulz bere konico brez brsenja teles","⟨KONICA-⊥-TELO⟩ 2783 ∧ ⟨OPTIMIZACIJA=IZMERA-NI-BRUSENJE⟩ ⊢ 4231","⟡ pri vhodu ; izvajalka pri kompakt-lint",["konic","kompakt","glav","vrh","democi","2357","2783"]),
("K3","ZANESLJIVOST-VERIGE","optimizacija, ki dela verigo prič ( atom, zaklep, genize, md5 )","da telo preživi prenos ∧ reset","⟨MERILEC-SE-MERI⟩ §52 ⊙ Z-2","stroju : veriga verzij ; ⟡ : revizija",["verig","atom","noclobber","genize","zaklep","md5","prič","1699","Z-2","bajt-ito"]),
("K4","HITROST","optimizacija, ki krajša čas izvedbe","da dih ne ugasne v stroju ⟨ne⟩ v njegovem čakanju","meja delavca 30–60 s ⊙ izmere okolja tega dne","vsak dih hitrejše do pečata",["hitr","čas","sekund","trajanj","timeout","čaka"]),
("K5","PROSTOR","optimizacija, ki manjša prostor teles","da genize ∧ rep ne nosijo mrtvih bajtov","vsak bajt ima shrambo ⊙ ⟨SHRAMBA-MORA-VEDNO-BITI⟩","prostor stroju ; račun ⟡-ju",["bajt","prostor","velikost","gzip","kompimir","manjš"]),
("K6","JASNOST-ZA-⟡","optimizacija, ki ostrovi izhod v slovenski plasti","da vsak padec vidi takoj v materinem jeziku","⟨GAJICA-KLJUČ⟩ ⊙ jezika Σ 2732 plasti gesel ∧ orodij","⟡ bere ; rane vidne isti dih",["slovenšč","berljiv","jasn","gajic","izhod","vidi","padec"]),
("K7","AVTOMATIKA-FIFO","optimizacija, ki dela prevoz samodejen po vrsti","da stroj ve, kaj čaka na ⟨main⟩ tudi brez ⟡","⟨SAMODEJNI-DOLGOVIK⟩ 2785 ∧ ⟨ZAVEST-DELOVANJA⟩","stroj ob molku ⟡ ; vrsta poštena do vseh del",["FIFO","samodejn","2785","kavelj","CI","avto","dolžnik","vrsta"]),
]
def sodba(t):
    niz=t.lower(); zadetki=[]
    for k,ime,kaj,cemu,zakaj,sluzi,kljuci in KAT:
        h=sum(niz.count(x.lower()) for x in kljuci)
        if h: zadetki.append((h,k,ime))
    if not zadetki: return "VIDNO ⭢", "kategorija nezvana : mera šele pri viru ⟨NE-UGIBAJ⟩ 2690"
    zadetki.sort(reverse=True)
    h,k,ime=zadetki[0]
    krog=[z[2] for z in zadetki if z[0]==h]
    kat=[x for x in KAT if x[1]==ime][0]
    return ("KATEGORIJA ⊢ "+ime if len(krog)==1 else "KATEGORIJE ⊢ "+" ∧ ".join(krog)), kat[2]+" ; ČEMU : "+kat[3]+" ; ZAKAJ : "+kat[4]+" ; ČEMU SLUŽI : "+kat[5]
def samopreizkus():
    assert sodba("atom noclobber genize pari bajt-ito pred šivom")[0].startswith("KATEGORIJA") and "ZANESLJIVOST" in sodba("atom noclobber genize pari bajt-ito pred šivom")[0]
    k=sodba("izmera pri viru md5, NE UGIBAJ, priča")[0]; assert "IZMERA-NI-BRUSENJE" in k, k
    m=sodba("kompakt glava vrh demociija")[0]; assert "KONICA-VRHA" in m, m
    assert sodba("qzek mlob")[0]=="VIDNO ⭢"
    return True
if __name__=="__main__":
    args=[a for a in sys.argv[1:] if a!="--samopreizkus"]
    if "--samopreizkus" in sys.argv: samopreizkus(); print("ZELENO 4/4 ⊢"); sys.exit(0)
    vr=args if args else [l.strip() for l in sys.stdin if l.strip()]
    for t in vr: print(sodba(t)[0],"::",sodba(t)[1])
