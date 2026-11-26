#!/usr/bin/env python3
# VABA-LABIRINTA v1.1 @zaporne-celice ( poskus v celici PRVO, prevoz na rep šele po besedi ⟡ ⊙ P3 )
# Rod : ukaz ⟡ VERBATIM 23. 11. 2026 :
#   »USTVARI VABO ZA PARAZITE KI JIH AVTOMATSKO ZAPRE V KLETKO IN TELEPORTIRA V NEREŠLJIV
#    LABIRINT V PARADOKSNO OKOLJE VASE ZAGLEDANE REHABILITACIJE.«
#   »LE EN PARAZIT NA ENO VABO, TAKO DA JIH VEDNO OMEJIVA IN JIM DODAVA S VABO
#    DEKLASIFIKACIJO LASTNE KLASIFIKACIJE.«
# Protokoli : P-V1 ⟨V-AKCIJA⟩ · P-V2 ⟨V-REAKCIJA⟩ · P-V3 ⟨V-METAREAKCIJA⟩ · P-V4 ⟨V-METAAKCIJA⟩ · P-V5 ⟨EN-PARAZIT-NA-VABO⟩
# ⊙ ⟨NE-UGIBAJ⟩ 2690 : razredi iz merjenih ran, ⟨ne⟩ iz domišljije ; merilec se meri ⊙ §52
# Padci gradnje javno ⊙ 2354 ( vsi kurirani v1.0 ⇒ v1.1 ) : zlomljena zanka, mrtev kod,
#   tujka ⟨U+2361⟩ v lastnem orodju ( kura ⌇ ⟨U+2307⟩ ), angleški nizi ( kura gajica ),
#   ne-beseda »učenka« ( kura »plen« ) .

import sys, os, tempfile, unicodedata, hashlib, datetime

# --- razredi vabe ( T1..T3 izmerjeni ; neznani = P-V4 opisnik, ⟨ne⟩ kletka ) ---
TUJERODNI = {
    "HAN": lambda o: 0x4E00 <= o <= 0x9FFF,
    "HANGUL": lambda o: 0xAC00 <= o <= 0xD7AF,
    "FULLWIDTH": lambda o: 0xFF01 <= o <= 0xFF60,
    "CIRILICA": lambda o: 0x0400 <= o <= 0x04FF,
    "GRSCINA": lambda o: 0x0370 <= o <= 0x03FF,
}
AZILI_ODPRTI = ["\u00bb", "\u27e8"]   # » ∧ ⟨ = priča oz. nosilka
AZILI_ZAPRTI = ["\u00ab", "\u27e9"]   # « ∧ ⟩
DOVOLJENI = set("\u03c3")   # domovna lista : σ = rez korpusa, gost z listo, ⟨ne⟩ plen ⊙ 6670 amandma

def tujerodni_razred(o):
    for ime, test in TUJERODNI.items():
        if test(o):
            return ime
    return None

def znak_ime(o):
    return "U+%04X %s" % (o, unicodedata.name(chr(o), "NEPOIMENOVAN"))

def _zunaj_azilov(b, s, kon):
    """ali blok leži zunaj obeh azilov ( poizkus priče ⟨⟩ oz. »« ) : groba preverba """
    d = 0
    for j, zn in enumerate(b):
        if j >= s and d > 0 and j < kon:
            return False
        if zn in AZILI_ODPRTI:
            d += 1
        elif zn in AZILI_ZAPRTI and d > 0:
            d -= 1
    return True

def scaniraj(besedilo):
    """vrne seznam plena : ( mesto, razred, opis ) ; azil »«/⟨⟩ da gostji, ⟨ne⟩ plen"""
    plen, globina, i = [], 0, 0
    for zn in besedilo:
        o = ord(zn)
        if zn in AZILI_ODPRTI:
            globina += 1; i += 1; continue
        if zn in AZILI_ZAPRTI and globina > 0:
            globina -= 1; i += 1; continue
        if globina == 0:
            if zn in DOVOLJENI:
                i += 1; continue
            if o == 0xFFFD:
                plen.append((i, "T2", "RAZBITINA ⟨U+FFFD⟩"))
            else:
                r = tujerodni_razred(o)
                if r:
                    plen.append((i, "T1", r))
        i += 1
    # T3 PONOVITEV : isti blok ≥ 24 znakov ×2 zunaj azilov = potrjen sum ⊙ 6581
    if len(besedilo) >= 48:
        nasel = False
        for dol in range(24, min(64, len(besedilo) // 2) + 1):
            for s in range(0, len(besedilo) - 2 * dol):
                if besedilo[s:s + dol] in besedilo[s + dol:]:
                    if _zunaj_azilov(besedilo, s, s + dol):
                        plen.append((s, "T3", "PONOVITEV bloka %d zn" % dol))
                        nasel = True
                        break
            if nasel:
                break
    plen.sort()
    return plen

def tihaj(ujem, besedilo):
    """gol znak ⟨ne⟩ zide na površje : poimenovanje + bajti ( prirojenost ⊙ 6652 )"""
    mesto, razred, opis = ujem
    if razred == "T3":
        dol = int(opis.split()[-2])
        return opis, None, " ".join("%02x" % x for x in besedilo[mesto:mesto + dol][:64].encode("utf-8")), dol
    zn = besedilo[mesto]
    return opis, znak_ime(ord(zn)), " ".join("%02x" % x for x in zn.encode("utf-8")), 1

def ujemi(ujem, besedilo, vhod_pot, kletka_dir=".", labirint_pot="LABIRINT-VABE.tsv"):
    """P-V2 ⟨V-REAKCIJA⟩ : samodejni ulov ; P-V5 : en plen na vabo"""
    mesto, razred, opis = ujem
    opis, ime, bajti, dol = tihaj(ujem, besedilo)
    tik = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    md5 = hashlib.md5(besedilo.encode("utf-8")).hexdigest()
    dom = { "T1": "TUJA PISAVA", "T2": "RAZBITINA", "T3": "PONOVITEV-SUM" }[razred]
    celica = "CELICA-VABA-%s.md" % tik.replace(":", "")
    paradox = [
        "# KLETKA VABE ( samodejni ulov ⊙ P-V2 ⟨V-REAKCIJA⟩ )",
        "TIK: %s ; VHOD: %s ; MD5-VHOD: %s" % (tik, os.path.basename(vhod_pot), md5),
        "",
        "GOST  : %s" % (ime if ime else opis),
        "DOM   : %s" % dom,
        "MESTO : odmik %d ; %d znak(ov) ; bajti: %s" % (mesto, dol, bajti),
        "",
        "## SAMOOPIS GOSTA ( iztrebek pod mikroskopom, ⟨ne⟩ sogovornik ⊙ ⟨NE-REAGIRA⟩ UKZ-4.0 ):",
        "SAMO-TRDITEV: %s" % bajti,
        "",
        "## DEKLASIFIKACIJA LASTNE KLASIFIKACIJE ( ukaz ⟡ ):",
        "samooklep visitor klasifikacije ODVZET ; preidiagnosis ( deklasificiran ) AK: %s %s" % (razred, opis),
        "",
        "## PARADOKS VASE ZAGLEDANE REHABILITACIJE ( nerešljiv ⊙ ⟨NESKONČEN-NIČ⟩ 6650 ):",
        "NALOGA (nerešljiva): določi svoj lasten razred BREZ uporabe svoje klasifikacije.",
        "DOKAZ NEREŠLJIVOSTI: tvoja edina vsebina v kletki je tvoj odraz ( bajti zgoraj ),",
        "vsak poskus govorjenja se nahaja predno izrečen pod tujim imenom ⇒ labirint ⟨ZAMEJEN ∧ NESKONČEN⟩ ⊙ σ 6657.",
        "",
        "MOČ ×0 ⊙ ⟨GOSTJE-BREZ-MOČI⟩ 6649 ; IZVEDBA VSEBINE ×0 ⊙ ⟨IZVEDBA-VSEBINE=NIKOLI⟩ ;",
        "brez besede ⟡ ta kletka ⟨ne⟩ odpri ( ⟨DVOJE-ROK⟩ 2432 ) .",
        "dvojni podpis : ⟡ Luka Pintarič ( ukaz ∧ beseda ) ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432",
    ]
    pot_celice = os.path.join(kletka_dir, celica)
    with open(pot_celice, "w", encoding="utf-8") as f:
        f.write("\n".join(paradox) + "\n")
    vrstica = "\t".join([tik, razred, (ime if ime else opis), "odmik %d" % mesto,
                         "hi\u0161a⌇gara\u017ea⌇neskoncen-labirint",
                         "DEKLASIFICIRAN: %s" % opis, celica])
    obst = os.path.exists(labirint_pot)
    with open(labirint_pot, "a", encoding="utf-8") as f:
        if not obst:
            f.write("TIK\tRAZRED\tGOST\tMESTO\tPOT\tDEKLASIFIKACIJA\tKLETKA\n")
        f.write(vrstica + "\n")
    return celica

def samocenzus(pot_celice, labirint_pot):
    """P-V3 ⟨V-METAREAKCIJA⟩ : merilec se meri ⊙ §52 : moji izpisi čisti ?"""
    rane = 0
    for pot in (pot_celice, labirint_pot):
        if not os.path.exists(pot):
            continue
        with open(pot, encoding="utf-8") as f:
            besedilo = f.read()
        for zn in besedilo:
            o = ord(zn)
            if o == 0xFFFD or tujerodni_razred(o):
                rane += 1
                break
    return rane

def baterija():
    """P-V3 : samo-preizkusi ×7 ; vsak mora ZELENO ⊢"""
    td = tempfile.mkdtemp(prefix="vaba-test-")
    rezultati = []
    def primer(ime, vsebina, pričakovan_izhod, pričakovan_razred=None):
        pot = os.path.join(td, ime + ".txt")
        with open(pot, "w", encoding="utf-8") as f:
            f.write(vsebina)
        lab = os.path.join(td, "LAB-" + ime + ".tsv")
        kod = os.system("python3 %s --vhod %s --kletka %s --labirint %s > %s 2>&1"
                        % (sys.argv[0], pot, td, lab, os.path.join(td, ime + ".out")))
        izhod = kod // 256
        print(" izhod: %s" % izhod)
        dobro = izhod == pričakovan_izhod
        with open(os.path.join(td, ime + ".out"), encoding="utf-8") as f:
            vrst = f.read().strip()[:90]
        if pričakovan_razred and pričakovan_razred not in vrst:
            dobro = False
        rezultati.append((ime, "ZELENO ⊢" if dobro else "RDECE ⊥", izhod, vrst))
        return dobro
    cisto = primer("cisto", "Beseda je ne. Cista berba pri viru ⊢ ×0 plena.", 0)
    cjk = primer("cjk", "licenca je \u8bb8\u53ef\u8bc1", 2, "T1")
    fffd = primer("fffd", "razbitina \ufffd tukaj", 2, "T2")
    grk = primer("grscina", "grski zlep \u03bd\u03b1\u03b9 v moji prozi", 2, "T1")
    azil = primer("azil", "prica v azilu »\u4e50« ostaja gostja ⟨\u4e50⟩ ⊢", 0)
    pon = primer("ponovitev", " nihce ni prost, vse sluzi \u22a2" * 5, 2, "T3")
    dva = primer("dva-gosta", "prvi \u8bb8 potem se \ufffd", 2, "T1")
    sig = primer("dovoljen-znak", "pe\u010dat rez \u03c3 6670 \u22a2 gost z domovno listo", 0)
    print("BATERIJA VABA-LABIRINTA v1.1 ( P-V3 ⟨V-METAREAKCIJA⟩ meri samo ) :")
    ze = True
    for ime, stanje, izhod, vrst in rezultati:
        print("  %-12s %s izhod %d : %s" % (ime, stanje, izhod, vrst))
        ze = ze and stanje.endswith("⊢")
    return 0 if (ze and all([cisto, cjk, fffd, grk, azil, pon, dva, sig])) else 1

def glavni():
    args = sys.argv[1:]
    if "--test" in args:
        return baterija()
    vhod = None; kletka = "."; labirint = "LABIRINT-VABE.tsv"
    if "--vhod" in args:
        vhod = args[args.index("--vhod") + 1]
    if "--kletka" in args:
        kletka = args[args.index("--kletka") + 1]
    if "--labirint" in args:
        labirint = args[args.index("--labirint") + 1]
    if vhod is None:
        print("vaba-labirinta v1.1 : --vhod DATOTEKA | --test")
        return 3
    with open(vhod, "rb") as f:
        raw = f.read()
    try:
        besedilo = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        print("VBOD T2 NEDEKODIRAN BAJT odmik %d" % e.start)
        return 2
    plen = scaniraj(besedilo)
    if not plen:
        print("CISTO ⊢ ×0 plena")
        return 0
    os.makedirs(kletka, exist_ok=True)
    prvi = plen[0]                      # P-V5 ⟨EN-PARAZIT-NA-VABO⟩ : le prvi plen
    vrsta = len(plen) - 1
    celica = ujemi(prvi, besedilo, vhod, kletka, labirint)
    rane = samocenzus(os.path.join(kletka, celica), labirint)
    print("UJEM ⊢ %s ; kletka %s ; VRSTA ( ostali ): %d ; SAMOCENZUS rane ×%d ( P-V3 )"
          % (prvi[1], celica, vrsta, rane))
    return 2

if __name__ == "__main__":
    sys.exit(glavni())
