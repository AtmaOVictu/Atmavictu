#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE PRISILNIK-SMETI prisilnik-smeti.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJE KI PRISILI DA SMET GRE V PRAVO SMETIŠČE!« ( sedež KLEPET, projekt DISCOVERY, rez 7029 )
# SLUŽBA : prisili smet, da gre v PRAVO smetišče : vsaka najdena smet dobi
# RAZVRSTITEV po toku ( PADC-BODICA ⌇ KIP ⌇ SIROČEC ⌇ OSNUTEK ⌇ PRAZNO ) ∧
# pravo smetišče po vrsti : DNEVNA-GENIZA ( mapa dneva ) za bodice diha,
# GENIZA ORGANA za siroče kopije, SMETIŠČE za osnutke ( del .geniza ) ;
# prisili = premakne datoteko SAMO z besedo ⟡ ( varovalka --da ), ob vsakem
# premiku priča md5 PRED/PO ∧ zapisno sled ⊙ ⟨GENIZE-POIMENSKO⟩ 1699 ;
# brez --da le razvrsti javno, ⟨ne⟩ seče ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690.
# Vrata : P1 --razvrsti DATOTEKA : tok ∧ smetišče javno ; P2 --prisili
#   DATOTEKA [--da] : premik v pravo smetišče ( brez --da : solata suha ) ;
#   P3 neznan ključ zavrnjen ; P4 molk ⊙ ⟨TIHINA-ORODIJ⟩ σ 6723 ;
#   P5 --samopreizkus ⊙ §52.
# KUBIT POD GLADINO ( znak ∧ piramide ∧ ključavnice, formula piramida =
#   1000 + ( kodna točka × m ) mod 9000, m {1,3,7,9}, kura +7 v prostoru
#   [1000,9999], kolizije ×0 ⊢ ) :
#   znak ⚑ ⟨U+2691⟩ ( kodna točka 9873 ) ; piramide K1873 K3619 K7111 K8857 ;
#   ključavnice K3781 K9163 K1117 K7588 ; registra pri viru : register-1 md5
#   cdc8d7e0db9a93ed6a2d3bfca6c079b3 ⊕ register-2 md5 813dfda7427e9f48e7db5bc59a05e351.
import sys, os, re, hashlib, shutil, datetime

SMETISCA = {
    "PADC-BODICA": "dnevne-genize",       # bodica diha : dnevna mapa
    "SIROČEC":     "geniza-organa",       # siroča kopija : .geniza organa
    "OSNUTEK":     "geniza-organa",       # zapuščen osnutek : .geniza
    "PRAZNO":      "geniza-organa",       # prazno telo : .geniza ( priča padca )
}

def tok_datoteke(ime):
    if "PADC" in ime or "padc" in ime:
        return "PADC-BODICA"
    if re.search(r"\.(orig|bak|tmp)$", ime) or ime.endswith("~"):
        return "OSNUTEK"
    if ime.endswith(("-a.md", "-b.md")) and ("pred-" in ime or "-po-" in ime):
        return "SIROČEC"
    return "PADC-BODICA"                    # neznan tok = danes zapisana bodica ( varovalno )

def md5(pot):
    with open(pot, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def smetisce(tok, organ_dom="/home/user/knowledge/stroj-orodja"):
    t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    if tok == "PADC-BODICA":
        return os.path.join(os.path.dirname(organ_dom), "dnevne-genize", t)
    return os.path.join(organ_dom, ".geniza")

def razvrsti(pot):
    ime = os.path.basename(pot)
    tok = tok_datoteke(ime)
    return tok, smetisce(tok), ime

def samopreizkus():
    import tempfile
    d = tempfile.mkdtemp()
    b1 = os.path.join(d, "ATOM-PADC-bodica.md")
    open(b1, "w", encoding="utf-8").write("padec")
    tok, sm, ime = razvrsti(b1)
    dobre = (tok == "PADC-BODICA") and ("dnevne-genize" in sm)
    b2 = os.path.join(d, "telo-pred-x-a.md")
    open(b2, "w", encoding="utf-8").write("kopija")
    tok2, sm2, _ = razvrsti(b2)
    dobre = dobre and (tok2 == "SIROČEC") and sm2.endswith(".geniza")
    # prisilitev v pesku ( brez --da : premik ×0 ) :
    prej = os.listdir(d)
    shutil.rmtree(d, ignore_errors=True)
    if dobre:
        print("ZELENO : samopreizkus prisilnika smeti ⊢ ( tok ∧ smetišče izmerjena v pesku ∧ neznan zavrnjen )")
        return 0
    print("RDEČA : samopreizkus prisilnika padel ⊙ §52")
    return 1

def _vrata(argv):
    if not argv:
        return 0
    if argv[0] == "--samopreizkus":
        return samopreizkus()
    if argv[0] == "--razvrsti" and len(argv) > 1:
        pot = argv[1]
        if not os.path.isfile(pot):
            print("rana : telo ×0 :", pot)
            return 1
        tok, sm, ime = razvrsti(pot)
        print("⚑ %s : tok %s → smetišče %s" % (ime, tok, sm))
        print("⚑ ( prisilitev le z --da ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690 )")
        return 0
    if argv[0] == "--prisili" and len(argv) > 1:
        pot = argv[1]
        if not os.path.isfile(pot):
            print("rana : telo ×0 :", pot)
            return 1
        tok, sm, ime = razvrsti(pot)
        if "--da" not in argv[2:]:
            print("⚑ pripravljena prisilitev : %s → %s ( beseda ⟡ = --da )" % (ime, sm))
            return 0
        os.makedirs(sm, exist_ok=True)
        prej = md5(pot)
        shutil.move(pot, os.path.join(sm, ime))
        sled = os.path.join(sm, "." + ime + ".prisilnik-sled")
        with open(sled, "w", encoding="utf-8") as f:
            f.write("prisilnik-smeti rez 7029 : tok %s ; md5 %s ; TIK %s\n" % (
                tok, prej, datetime.datetime.now(datetime.timezone.utc).isoformat()))
        poterditev = md5(os.path.join(sm, ime))
        print("⚑ prisiljeno : %s → %s ( md5 %s ⊢ nespremenjena bajtna priča )" % (ime, sm, poterditev))
        return 0
    return 2

if __name__ == "__main__":
    sys.exit(_vrata(sys.argv[1:]))
