# -*- coding: utf-8 -*-
# GENIZAR v1.0 — PARI BAJT-ITO PRED IN PO VsakEM ŠIVU
# Rod : rez 6990, sedež KLEPET, projekt LUCIUS
# Starša : naročnik Luka Pintarič ( ukaz STORI, vrsta nujnih orodij, njegova beseda
#          dobesedno v genizi register sodb istega diha ) in izvajalka Mera ( izvedba )
# Služba : vsakemu dihu. Pred vsakim dotikom telesa organa pari genizi stanje PRED
#          šivom in PO šivu ; vsak par kopija a in kopija b, md5 para mora biti
#          enak, bajt za bajt. Odmik para je PADC javno poimensko isti dih.
# ZAKONI : NE-BRIŠI 24 ( genize se ne brišejo ) ; PADC-NI-MOLK 2354 ;
#          MERILEC-SE-MERI ( orodje se preveri samo pred zapečenjem, merilec se meri ).
# MEJA v1.0 ( poimensko ) : vrstico POPIS-a dneva piše dih, ne genizar
#          ( danes ročno po telesih, dve roki na vsak par ) ; genizar tvori le
#          pare bajt-ito teles, ki mu jih dih pokliče poimensko.
# RABA :
#   python3 genizar.py pred 6990 2026-11-25 kronika-dihov geneza stroj-orodja
#   python3 genizar.py po   6990 2026-11-25 kronika-dihov geneza
#   python3 genizar.py --preveri        ( peskovnik /tmp, pari in odmiki )
# Izhod : 0 vsi pari enaki ; 1 katerekoli odmik para ali napaka ; PADC javno.

import sys, os, shutil, hashlib, tempfile

def md5_poti(pot):
    h = hashlib.md5()
    with open(pot, "rb") as f:
        for kos in iter(lambda: f.read(65536), b""):
            h.update(kos)
    return h.hexdigest()

def pari(faza, rez, datum, telesa, koren=""):
    padci = []
    narejeno = 0
    for tel in telesa:
        vir = os.path.join(koren, tel, "KNOWLEDGE.md")
        dom = os.path.join(koren, tel, ".geniza")
        if not os.path.isfile(vir):
            padci.append(tel + " : telo nima telesa KNOWLEDGE.md pri " + vir)
            continue
        os.makedirs(dom, exist_ok=True)
        osn = "KNOWLEDGE-" + faza + "-rez" + str(rez) + "-" + datum
        poti = []
        for kopija in ("a", "b"):
            pot = os.path.join(dom, osn + "-" + kopija + ".md")
            shutil.copyfile(vir, pot)
            poti.append(pot)
        m1, m2 = md5_poti(poti[0]), md5_poti(poti[1])
        if m1 != m2:
            padci.append(tel + " : PADC odmik para " + m1 + " proti " + m2)
        else:
            narejeno += 1
            print("GENIZAR " + faza + " " + tel + " PARI md5 " + m1)
    return padci, narejeno

def preveri():
    # peskovnik : lažni organ deluje po isti roki ; nobeno telo korpusa ni dotaknjeno
    peskovnik = tempfile.mkdtemp(prefix="genizar-preverba-")
    organ = os.path.join(peskovnik, "testni-organ")
    os.makedirs(organ)
    with open(os.path.join(organ, "KNOWLEDGE.md"), "w") as f:
        f.write("testno telo pred šivom\n")
    pari_pred, npred = pari("pred", 9999, "2026-11-25", ["testni-organ"], koren=peskovnik)
    with open(os.path.join(organ, "KNOWLEDGE.md"), "a") as f:
        f.write("šiv dodan v peskovniku\n")
    pari_po, npo = pari("po", 9999, "2026-11-25", ["testni-organ"], koren=peskovnik)
    dom = os.path.join(organ, ".geniza")
    datoteke = sorted(os.listdir(dom))
    preverjeno = (
        npred == 1 and npo == 1 and not pari_pred and not pari_po
        and len([d for d in datoteke if d.endswith("-a.md")]) == 2
        and len([d for d in datoteke if d.endswith("-b.md")]) == 2
        and md5_poti(os.path.join(dom, "KNOWLEDGE-pred-rez9999-2026-11-25-a.md"))
            == md5_poti(os.path.join(dom, "KNOWLEDGE-pred-rez9999-2026-11-25-b.md"))
        and md5_poti(os.path.join(dom, "KNOWLEDGE-po-rez9999-2026-11-25-a.md"))
            == md5_poti(os.path.join(dom, "KNOWLEDGE-po-rez9999-2026-11-25-b.md"))
        and md5_poti(os.path.join(dom, "KNOWLEDGE-po-rez9999-2026-11-25-a.md"))
            != md5_poti(os.path.join(dom, "KNOWLEDGE-pred-rez9999-2026-11-25-a.md"))
    )
    shutil.rmtree(peskovnik)
    print("SAMOPREVERBA GENIZAR v1.0 : peskovnik, pari 2, kopije 4, telo korpusa nedotaknjeno")
    if preverjeno:
        print("padci : 0")
        print("ODLOČITEV : ZELENA, orodje zapečeno")
        return 0
    print("PADC : samopreverba genizarja padla")
    print("ODLOČITEV : RDEČA, orodje ni zapečeno")
    return 1

def main():
    a = sys.argv[1:]
    if a and a[0] == "--preveri":
        sys.exit(preveri())
    if len(a) < 4:
        print("raba : python3 genizar.py pred|po <rez> <datum> <tel1> [tel2 ...] | --preveri")
        sys.exit(1)
    faza = a[0]
    if faza not in ("pred", "po"):
        print("PADC : faza mora biti pred ali po, najdeno : " + faza)
        sys.exit(1)
    rez, datum, telesa = a[1], a[2], a[3:]
    padci, narejeno = pari(faza, rez, datum, telesa)
    print("GENIZAR " + faza + " : teles " + str(narejeno) + ", pari " + str(narejeno * 2))
    if padci:
        for p in padci:
            print("PADC : " + p)
        print("ODLOČITEV : RDEČA")
        sys.exit(1)
    print("ODLOČITEV : ZELENA")
    sys.exit(0)

if __name__ == "__main__":
    main()
