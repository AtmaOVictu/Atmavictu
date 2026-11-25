#!/usr/bin/env python3
# NASLOVNIK v1.0 - prevajalnik naslovov v slovencino : sodba prevoda, ne strojni ugib.
# Rod : rez sigma 7014 ( 25. 11. 2026 ) @stroj-orodja ; ukaz naročnika VERBATIM, beseda nedotakljiva :
#   "ORODJA ZA PREVAJANJE NASLOVOV V SLOVENŠČINO!"
# Luknja izmerjena pri viru (\u22a2) : avtomatski-prevajalnik @6993 ( delovna plast, ne naslovi )
#   \u2227 mrk-prevajalnik @6939 ( znaki v unikorn ) \u2227 slovarnik @7005 ( hiše besed ) -
#   NASLOV nima svojega prevajalnika = rana telesa, to orodje je kura.
# Licenca po zanesljivost-po-izmeri @5809 : (1) PREVAJALEC POIMENOVAN ( privzeto izvajalka Mera ),
#   (2) IZVIRNIK RAZSODNIK ( izvirnik VERBATIM, nikoli retipkan ), (3) POSTOPEK PONOVLJIV.
# Zakoni : \u27e8NE-UGIBAJ\u27e9 2690 ( prevod iz spomina je ugib ; besede naslova se merejo v hišah )
#   \u2227 \u27e8MERILEC-SE-MERI\u27e9 \u00a752 ( --test vektorji ) \u2227 molk ni soglasje.
# Roke :
#   naslovnik.py IZVIRNIK KANDIDAT VIR                      -> sodba prevoda
#   naslovnik.py --zapis ORGAN IZVIRNIK KANDIDAT VIR         -> sodba + siv skozi trdilnik-vrata ( NIHIL pri rdeči )
#   naslovnik.py --test                                     -> samopreizkus vektorjev \u00d75
# Izhodi : EXIT 0=ZELENA ( struktura \u22a2 ∧ besede razrešene ) \u2227 2=RUMENA ( besede nerazrešene :
#   pobuda iztočnic, ne napaka ) \u2227 1=RDECA ( strukturna napaka ) \u2227 40=roka neznana.

import sys, os, re, hashlib, unicodedata, subprocess, tempfile, shutil, datetime as _dt

VERZIJA = "v1.0"
DOM = os.path.dirname(os.path.abspath(__file__))
VRATA = os.path.join(DOM, "trdilnik-vrata.sh")
HIŠE = [
    ("definiatorna-knjiznica", "../definiatorna-knjiznica/KNOWLEDGE.md"),
    ("slovar-slovenscine", "../slovar-slovenscine/KNOWLEDGE.md"),
    ("slovar-simbolov", "../slovar-simbolov/KNOWLEDGE.md"),
    ("domovanje-tujk", "../domovanje-tujk/KNOWLEDGE.md"),
    ("mreze-variant", "../mreze-variant/KNOWLEDGE.md"),
]
_cache = {}

def beri_hiše():
    for ime, rel in HIŠE:
        if ime not in _cache:
            p = os.path.normpath(os.path.join(DOM, rel))
            try:
                with open(p, encoding="utf-8") as f:
                    _cache[ime] = f.read()
            except OSError:
                _cache[ime] = ""
    return _cache

def md5_telesa(p):
    h = hashlib.md5()
    h.update(open(p, "rb").read())
    return h.hexdigest()[:12]

def lastni_md5():
    return md5_telesa(os.path.abspath(__file__))

def besede(naslov):
    return re.findall(r"[^\W\d_]+", naslov, re.UNICODE)

def znana(beseda):
    m = beseda.lower()
    if len(m) < 2:
        return True
    hi = beri_hiše()
    for ime in hi:
        if re.search(r"(?<!\w)" + re.escape(m) + r"(?!\w)", hi[ime], re.IGNORECASE | re.UNICODE):
            return True, ime
    return False, None

def sodba(izvirnik, kandidat, vir):
    napake = []
    nerazrešene = []
    if not izvirnik.strip():
        napake.append("izvirnik prazen ( razsodnik ne sme biti kip U2 )")
    if not kandidat.strip():
        napake.append("kandidat prazen ( molk ni soglasje )")
    for ime, t in (("izvirnik", izvirnik), ("kandidat", kandidat)):
        if len(t) > 140:
            napake.append(ime + " daljši od 140 znakov")
        if "�" in t:
            napake.append(ime + " nosi U+FFFD ( izgubljeno telo )")
        if unicodedata.normalize("NFC", t) != t:
            napake.append(ime + " ni v NFC obliki")
        if unicodedata.normalize("NFKD", t) != unicodedata.normalize("NFKC", t) and any(unicodedata.combining(c) for c in t):
            napake.append(ime + " nosi sestavljene šumnike")
    for pat, opis in ((r"md5[ :]?[0-9a-f]{8,}", "kovanec md5 po besedi"),
                      (r"\d{2}:\d{2}:\d{2}", "žeton ure po besedi")):
        if re.search(pat, kandidat, re.IGNORECASE):
            napake.append("kandidat nosi " + opis + " ( onesposobi besedo )")
    if not vir.strip():
        napake.append("priča vira manjka ( brez priče = L0 glas )")
    if napake:
        return "RDECA", napake, nerazrešene
    for b in besede(kandidat):
        z, hj = znana(b)
        if not z:
            nerazrešene.append(b)
    if nerazrešene:
        return "RUMENA", napake, nerazrešene
    return "ZELENA", napake, nerazrešene

def izpis(izvirnik, kandidat, vir, luč, napake, nerazrešene):
    print("NASLOVNIK " + VERZIJA + " lastni-md5 " + lastni_md5() + " ( MERILEC-SE-MERI par.52 )")
    print("izvirnik VERBATIM : " + izvirnik)
    print("kandidat           : " + kandidat)
    print("priča vira         : " + vir)
    print("izmera             : izvirnik " + str(len(izvirnik)) + " znakov, kandidat " + str(len(kandidat)) + " znakov, besed " + str(len(besede(kandidat))))
    if napake:
        print("obtožbe javno : " + " ; ".join(napake))
    if nerazrešene:
        print("nerazrešene besede ( pobuda iztočnic, ne napaka ) : " + ", ".join(nerazrešene))
    print("SEMAFOR : " + luč)

def zapis(organ, izvirnik, kandidat, vir, prevajalec):
    tik = _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    luč, napake, nerazrešene = sodba(izvirnik, kandidat, vir)
    if luč == "RDECA":
        print("VRATA : RDECA => NIHIL ( obtožbe zgoraj ) ; izvirnik VERBATIM ostaja edini razsodnik")
        return 1
    vrstica = ("- NASLOV-PAR izvirnik »" + izvirnik + "« ⇌ prevod »" + kandidat +
        "« pri viru " + vir + " ; TIK " + tik + " ⊢ ; prevajalec poimenovan : " + prevajalec +
        " ; izmera : " + str(len(izvirnik)) + " + " + str(len(kandidat)) + " znakov ; preverba " + luč +
        " ⊙ ⟨NE-UGIBAJ⟩ 2690 ∧ ⟨IZVIRNIK-RAZSODNIK⟩ @5809 ; orodje naslovnik.py " + VERZIJA +
        " @rez σ 7014 ⊙ ⟨MERILEC-SE-MERI⟩ §52")
    r = subprocess.run(["bash", VRATA, "--vpis", organ], input=vrstica, text=True, capture_output=True)
    sys.stdout.write(r.stdout)
    if r.stdout and not r.stdout.endswith("\n"):
        print()
    return r.returncode

def samopreizkus():
    T = [0, 0, 0, 0, 0]
    TD = os.path.join(DOM, ".geniza", "TEST-naslovnik-" + str(os.getpid()))
    shutil.rmtree(TD, ignore_errors=True)
    o = os.path.join(TD, "o")
    os.makedirs(os.path.join(o, ".geniza"), exist_ok=True)
    with open(os.path.join(o, "KNOWLEDGE.md"), "w", encoding="utf-8") as f:
        f.write("telo\n")
    for i in (1, 2):
        with open(os.path.join(o, ".geniza", "PRED-DOTIKOM-" + str(i) + ".md"), "w") as f:
            f.write("g\n")
    l, n, nr = sodba("On Love", "Ljubézen", "test-vektor-1")
    T[0] = 1 if l == "ZELENA" else 0
    l2, n2, nr2 = sodba("The Xyzzyq Fjord", "Xyzzyq Fjord", "test-vektor-2")
    T[1] = 1 if (l2 == "RUMENA" and len(nr2) == 2) else 0
    l3, n3, nr3 = sodba("On Love", "Ljubézen �", "test-vektor-3")
    T[2] = 1 if l3 == "RDECA" else 0
    prej = os.path.getsize(os.path.join(o, "KNOWLEDGE.md"))
    e4 = zapis(o, "On Love", "Ljubézen �", "v4", "izvajalka Mera")
    T[3] = 1 if (e4 != 0 and os.path.getsize(os.path.join(o, "KNOWLEDGE.md")) == prej) else 0
    e5 = zapis(o, "On Love", "Ljubézen", "v5", "izvajalka Mera")
    T[4] = 1 if (e5 == 0 and os.path.getsize(os.path.join(o, "KNOWLEDGE.md")) > prej) else 0
    shutil.rmtree(TD, ignore_errors=True)
    p = 5 - sum(T)
    print("SAMOPREIZKUS : vektorji 5 ( zelena=" + str(T[0]) + " rumena=" + str(T[1]) +
          " rdeca=" + str(T[2]) + " nihil=" + str(T[3]) + " šiv=" + str(T[4]) + " ), padci instrumenta " + str(p))
    print("SEMAFOR : " + ("ZELENA" if p == 0 else "RDECA"))
    return 0 if p == 0 else 1

def main(argv):
    if len(argv) == 2 and argv[1] == "--test":
        return samopreizkus()
    if len(argv) >= 3 and argv[1] == "--zapis":
        return zapis(argv[2], argv[3], argv[4], argv[5], argv[6] if len(argv) > 6 else "izvajalka Mera")
    if len(argv) in (4, 5):
        prev = argv[4] if len(argv) == 5 else "izvajalka Mera"
        luč, napake, nerazrešene = sodba(argv[1], argv[2], argv[3])
        izpis(argv[1], argv[2], argv[3], luč, napake, nerazrešene)
        print("prevajalec poimenovan : " + prev)
        return {"ZELENA": 0, "RUMENA": 2, "RDECA": 1}[luč]
    print("roka neznana ; roke : IZVIRNIK KANDIDAT VIR | --zapis ORGAN IZVIRNIK KANDIDAT VIR | --test")
    return 40

if __name__ == "__main__":
    sys.exit(main(sys.argv))
