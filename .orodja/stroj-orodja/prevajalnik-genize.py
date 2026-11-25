#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE PREVAJALNIK-GENIZE prevajalnik-genize.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJE KI PREVAJA GENIZO V PRAVILNO SLOVNICO!« ( sedež KLEPET, projekt DISCOVERY, rez 7027 )
# ZAKON zapečen isti dih : »GENIZA MORA VEDNO BITI V PRAVILNI SLOVENŠČINI!«
#   ⟡ VERBATIM = ⟨GENIZA-VEDNO-V-PRAVILNI-SLOVENŠČINI⟩ rez 7027 : geniza je
#   bajtna priča telesa ⇒ PRAVILNA SLOVENŠČINA živi najprej na ŽIVEM telesu,
#   geniza se rodi pari PRED/PO bajtno ⊙ ⟨GENIZE-POIMENSKO⟩ 1699.
# SLUŽBA : prevede telo ( ali genizo ) v pravilno slovnico : poišče ne-slovenske
# konstrukcije ( isti register kot kritik-konstrukcij ⊙ rez 7027 ) ∧ izpiše prevod
# s kurami ; piše ŽIVO telo LE z izrečeno besedo ⟡ ( varovalka --da ) ;
# pri vsakem pisanju rodi genize PARI ( pred ∧ po, kopiji a ∧ b ) bajtno ⊙ 1699.
# Vrata : P1 --prevedi DATOTEKA izpiše prevod na zaslon ( ⟨ne⟩ piše ) ;
#   P2 --uporabi DATOTEKA [--da] : brez --da le pove, kaj bi storil (
#   ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690 ) ; z --da piše telo ∧ rodi genize pari
#   bajtno-ito ( pred-{a,b} pred zapisom, po-{a,b} po zapisu, md5 obeh ) ;
#   P3 --popis register prevodov ; P4 neznan ključ zavrnjen ;
#   P5 molk brez ključa ⊙ ⟨TIHINA-ORODIJ⟩ σ 6723 ;
#   P6 --samopreizkus v živo ⊙ §52 ( prevod peska pravilen ∧ azili nedotaknjeni
#   ∧ varovalka živi : --uporabi brez --da ne piše ∧ neznan zavrnjen ) ;
#   P7 out = izhod 0, rana = 1.
# KUBIT POD GLADINO ( rezerviran znak ∧ piramide ∧ ključavnice, formula piramida =
#   1000 + ( kodna točka × m ) mod 9000, m vrstni red {1,3,7,9}, kura +7 ob
#   zasedenosti ∧ kolizije preverjene proti 869 pričam registrov pri viru ⊢ ) :
#   znak ⇌ ⟨U+21CC⟩ ( kodna točka 8652 ) ; piramide K9673 K8956 K7564 K6875 ;
#   ključavnice K3769 K6598 K4657 K5786 ; registra pri viru : register-1 md5
#   cdc8d7e0db9a93ed6a2d3bfca6c079b3 ⊕ register-2 md5 813dfda7427e9f48e7db5bc59a05e351.
import sys, re, os, hashlib, shutil, datetime

PREVODI = [
    # par : ( ujeta , vzorec , kura ) — tujke živijo kot predmet peska v »«
    ("»update«",   r"\bupdate\b",   "posodobitev"),
    ("»file«",     r"\bfile\b",     "datoteka"),
    ("»print«",    r"\bprint\b",    "natis"),
    ("»default«",  r"\bdefault\b",  "privzeto"),
    ("»start«",    r"\bstart\b",    "zagon"),
    ("»end«",      r"\bend\b",      "konec"),
    ("»help«",     r"\bhelp\b",     "pomoč"),
    ("»input«",    r"\binput\b",    "vhod"),
    ("»output«",   r"\boutput\b",   "izhod"),
    ("»error«",    r"\berror\b",    "napaka"),
    ("»tool«",     r"\btool\b",     "orodje"),
    ("»queue«",    r"\bqueue\b",    "vrsta"),
]
CIRILICA = re.compile(r"[\u0400-\u04FF]+")
KURE_CIRILICA = {"wrapped": None}

def azili(besedilo):
    return [(m.start(), m.end()) for m in re.finditer(r"»[^»]*«", besedilo)]

def v_azilu(i, obsegi):
    return any(a <= i < b for a, b in obsegi)

def prevajaj(besedilo):
    """vrne ( prevod , stevilo kur ) ; azili »« nedotaknjeni ⊙ @domovanje-tujk"""
    obsegi = azili(besedilo)
    vis = []   # ( polozaj , kura )
    for _, vzorec, kura in PREVODI:
        for m in re.finditer(vzorec, besedilo):
            if not v_azilu(m.start(), obsegi):
                vis.append((m.start(), m.end(), kura))
    for m in CIRILICA.finditer(besedilo):
        if not v_azilu(m.start(), obsegi):
            vis.append((m.start(), m.end(), "[cirilica→gajica roka ⟡]"))
    vis.sort(reverse=True)
    for a, b, kura in vis:
        besedilo = besedilo[:a] + kura + besedilo[b:]
    return besedilo, len(vis)

def md5(besedilo):
    return hashlib.md5(besedilo.encode("utf-8")).hexdigest()

def pari_genize(pot, staro, novo, ts):
    """rodi genize PARI bajtno-ito v .geniza zraven telesa ⊙ 1699"""
    imenik = os.path.join(os.path.dirname(os.path.abspath(pot)), ".geniza")
    if not os.path.isdir(imenik):
        os.makedirs(imenik)
    ime = os.path.splitext(os.path.basename(pot))[0]
    pari = []
    for crka, vsebina in (("a", staro), ("b", staro)):
        f = os.path.join(imenik, "%s-pred-%s-{c}.md".replace("{c}", crka) % (ime, ts))
        io_write(f, vsebina); pari.append(f)
    for crka, vsebina in (("a", novo), ("b", novo)):
        f = os.path.join(imenik, "%s-po-%s-{c}.md".replace("{c}", crka) % (ime, ts))
        io_write(f, vsebina); pari.append(f)
    return pari

def io_write(pot, vsebina):
    with open(pot, "w", encoding="utf-8") as f:
        f.write(vsebina)

def samopreizkus():
    pesek_pre_1 = ("update telesa", 1, "posodobitev telesa")
    pesek_pre_2 = ("vrsta queue teče", 1, "vrsta vrsta teče")
    pesek_azil = ("posodobi »update« telesa", 0, "posodobi »update« telesa")
    pesek_cir = ("ужival je zunaj", 1, None)
    dobre = True
    for besedilo, st_kur, prica in (pesek_pre_1, pesek_pre_2, pesek_azil):
        novo, kur = prevajaj(besedilo)
        if kur != st_kur or novo != prica:
            dobre = False
    novo_c, kur_c = prevajaj(pesek_cir[0])
    if kur_c != 1:
        dobre = False
    # varovalka : --uporabi brez --da ne piše ( P2 ) ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩
    import tempfile
    d = tempfile.mkdtemp()
    telo = os.path.join(d, "pesek-telo.md")
    io_write(telo, "update peska")
    out = _vrata(["--uporabi", telo])
    varovalka = (out == 0) and (open(telo, encoding="utf-8").read() == "update peska")
    neznan = (_vrata(["--neznankljuc"]) == 2)
    molk = (_vrata([]) == 0)
    if dobre and varovalka and neznan and molk:
        print("ZELENO : samopreizkus prevajalnika genize ⊢ ( prevodi pravili ∧ azili nedotaknjeni ∧ varovalka živi : brez --da pisanje ×0 ∧ neznan zavrnjen ∧ molk živ )")
        shutil.rmtree(d, ignore_errors=True)
        return 0
    print("RDEČA : samopreizkus prevajalnika padel ⊙ §52")
    shutil.rmtree(d, ignore_errors=True)
    return 1

def _vrata(argv):
    if len(argv) == 0:
        return 0                       # molk ⊙ σ 6723
    klj = argv[0]
    if klj == "--samopreizkus":
        return samopreizkus()
    if klj == "--popis":
        for ujeta, vzorec, kura in PREVODI:
            print("- %s ⇌ %s" % (ujeta, kura))
        print("- cirilica ⇌ gajica ( roka ⟡ z izmero )")
        return 0
    if klj == "--prevedi" and len(argv) > 1:
        try:
            with open(argv[1], encoding="utf-8") as f:
                besedilo = f.read()
        except OSError as e:
            print("rana pri berbi :", e)
            return 1
        novo, kur = prevajaj(besedilo)
        sys.stdout.write(novo)
        print("\n⇌ prevodi : %d ( ⟨NE-ODLOČAJ-NAMESTO-⟡⟩ 2690 : pisanje le z --da )" % kur)
        return 0
    if klj == "--uporabi" and len(argv) > 1:
        try:
            with open(argv[1], encoding="utf-8") as f:
                staro = f.read()
        except OSError as e:
            print("rana pri berbi :", e)
            return 1
        novo, kur = prevajaj(staro)
        if kur == 0:
            print("⇌ telo že v pravilni slovenščini ( geniza ⟨ne⟩ potrebuje prevod ⊙ rez 7027 )")
            return 0
        if "--da" not in argv[2:]:
            print("⇌ pripravljenih prevodov : %d ( pisanje ⟨ne⟩ storjeno ; beseda ⟡ = --da )" % kur)
            return 0
        ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        prej = md5(staro); poterjen = md5(novo)
        pari = pari_genize(argv[1], staro, novo, ts)
        io_write(argv[1], novo)       # ŽIVO telo, genize pari rojeni PRED zapisom ⊙ 1699
        print("⇌ preveden : %d kur ; telo md5 %s ⇒ %s ; genize pari ×4 ⊢ ( %s )" % (kur, prej, poterjen, " ∧ ".join(os.path.basename(p) for p in pari[:2])) )
        return 0
    return 2                           # neznan zavrnjen ( P4 )

if __name__ == "__main__":
    sys.exit(_vrata(sys.argv[1:]))
