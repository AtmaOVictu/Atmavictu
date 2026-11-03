# ABECEDA-GREP — piHON tokovni stroj hišne abecede: grep ∧ FRAGMENTACIJA-VSEH-ŠTEVIL-DO-MERE-MED-0-IN-1 ⊢
# Zagon: python lucius/abeceda-grep.py fragmentiraj <datoteka|->        ( TOK z zgodnjim izhodom — ZAKON ŠESTE SMRTI )
#        python lucius/abeceda-grep.py grep [--stevila|--simboli|--imena|--hex] [-m N] [-n] [VZOREC] <datoteka|->
#        python lucius/abeceda-grep.py abeceda <datoteka|->
#        python lucius/abeceda-grep.py izmeri <datoteke|->          ( vrstice · znaki · bajti · ⟨md5⟩ — pečatni zapis )
#        python lucius/abeceda-grep.py isto <A> <B>                ( bajt-isto ⇌ zrcalo, zgodnji izhod )
#        python lucius/abeceda-grep.py pecat [datoteke|organi]     ( 1 + najvišja izmerjena ⊢ Z-2 — naslednji pečat )
#        python lucius/abeceda-grep.py rez <datoteka> [B/kos]      ( geniza rez po celih vrsticah — frag-NN pot )
#        python lucius/abeceda-grep.py prevoz <lokal> <zrcalo>     ( RED PREVOZA: izmeri -> isto -> pečat ⊢ )
#        python lucius/abeceda-grep.py sha <datoteke|->            ( ⟨sha1⟩ ∧ ⟨blob⟩ ⇌ git hash-object, FIPS 180 )
#        python lucius/abeceda-grep.py rep <datoteke>             ( LOKAL ⇌ ⟨main⟩: blob diska ⇌ blob repa ⊢ )
#        python lucius/abeceda-grep.py vrata [imena]              ( preverjanja na koncih: localhost ŽIVA ∧ / MRTVA × )
#        python lucius/abeceda-grep.py predlog                    ( KOGA ∧ KAJ — predlogi iz izmere ⊙ )
#        python lucius/abeceda-grep.py varuh                      ( VARUH STROJA #12: GPU 85 °C · disk 95 % → USTAVI )
#        python lucius/abeceda-grep.py nasprotje [datoteke]       ( ⟨NASPROTNA-TEHTNICA⟩ §0.18: podpora ⊥ dvom ⊙ )
#        python lucius/abeceda-grep.py rezerviraj [ime]           ( ⟨REZERVACIJA-REZA⟩ ⟨IDEJA-K⟩ — vrsta, ne vzporedje )
#        python lucius/abeceda-grep.py struktura [datoteke]        ( ⟨PRICA-SODELOVANJA⟩ ⟨IDEJA-M⟩ — CI pečatov )
#        python lucius/abeceda-grep.py popis [koren]               ( izmera vsakega telesa + Σ ∧ dvojniki ⚠ )
#        python lucius/abeceda-grep.py speči [N]                  ( organi po zadnjem žigu — najstarejši prvi )
#        python lucius/abeceda-grep.py pulz [N]                    ( berba lastnega pulza ∧ dih manjka ⚠ )
#        python lucius/abeceda-grep.py združi <datoteka|->          ( inverz: 0.1050 × 10⁴ -> 1050, berba mantis )
#        python lucius/abeceda-grep.py test                               ( ⟨druga-roka⟩: stroj preveri sam sebe )
# Zakon ( VBL 0.1050 × 10⁴ §, ⟡ ukaz ⟨daj⟩ ⟨ne brusi⟩ P-CITAT ⟨to uredi tako da fragmentiraš vsa števila do mere med 0 in 1⟩ ):
#   vsaka zapisana števka ⇌ mantisa v [0,1) × poimenovana potenca desetice;
#   ničla invariantna; ⟨sha⟩ hex ∧ ⟨⟩-imena ⟨ne⟩ merjena — ime, ⟨ne⟩ količina ⊙ ⟨ne-ugibaj⟩.
# Hišni red prevoza: PREVOZ -> ISTO ( bajt-isto ⇌ zrcalo ) -> PEČAT — isto je obvezen dih, ne milost ⊢.
# Zakon ( VBL 0.1050 × 10⁴ §, ⟡ ukaz ⟨daj⟩ ⟨ne brusi⟩ P-CITAT ⟨to uredi tako da fragmentiraš vsa števila do mere med 0 in 1⟩ ):
#   vsaka zapisana števka ⇌ mantisa v [0,1) × poimenovana potenca desetice;
#   ničla invariantna; ⟨sha⟩ hex ∧ ⟨⟩-imena ⟨ne⟩ merjena — ime, ⟨ne⟩ količina ⊙ ⟨ne-ugibaj⟩.
# Izmere gredo na stderr — stdout je čisto telo ( tokovi se ceplijo: | head, | wc -l ⊢ ).
import sys
import re
import argparse
import hashlib
import codecs

NADPIS = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
SIMBOLI = "⊢⚠×⊘∮∆∴⊥⟡¬∧⊙σ∂⚔⇌⟨⟩"                      # abeceda hiše ( iz TONI, zvocna-abeceda.mjs )
IMENA = re.compile(r"⟨[^⟩]*⟩")                        # ⟨⟩-imena: ime, ne količina — NE merjena
HEX = re.compile(r"(?<![0-9A-Za-z])[0-9A-Fa-f]{8,}(?![0-9A-Za-z])")   # ⟨sha⟩ hex: NE merjen
STEVILO = re.compile(r"\d{1,3}(?:\.\d{3})+|\d+[,.]\d+|\d+")           # kandidati po veljavnosti ∧
ZE_FRAG = re.compile(r"(?:\s*×\s*10|\s*[⁰¹²³⁴⁵⁶⁷⁸⁹])")                 # že × 10ⁿ ∧ ⟨ne-ugibaj⟩ ×
ECHO = {}                                              # izmere enega diha


def mera(k, n=1):
    ECHO[k] = ECHO.get(k, 0) + n


def _meja(c):
    # meja besede: cifra mora stati sama — ne znotraj imen, poti, verzij ⊙ ⟨ne-ugibaj⟩
    # ( pika kot NASLEDNJI znak je dovoljena — ordinal »14.«; kot PREJŠNJI pa ne — »1« za piko je rep verije )
    return c is None or not re.match(r"[0-9A-Za-z_\-/]", c)


def fragment_število(telo, m):
    """En kandidat -> mantisa v [0,1) × 10ⁿ ALI None ( ne dotakni se: ⟨ne brusi⟩ )."""
    prev = telo[m.start() - 1] if m.start() else None
    if prev == ".":
        mera("verzije"); return None
    if not _meja(prev):
        mera("imena_poti"); return None
    naslednji = telo[m.end()] if m.end() < len(telo) else None
    if not _meja(naslednji):
        mera("imena_poti"); return None
    if naslednji == "." and m.end() + 1 < len(telo) and telo[m.end() + 1].isdigit():
        mera("verzije"); return None                          # 1.0.1, 0.41.1 — verzijska veriga ×
    if ZE_FRAG.match(telo, m.end()):
        mera("ze_fragmentirane"); return None                # × 10ⁿ že piše za hrbtom
    if HEX.fullmatch(m.group(0)):
        mera("hex"); return None
    zapis = m.group(0)
    if not re.search(r"[,.]", zapis) or re.fullmatch(r"\d{1,3}(?:\.\d{3})+", zapis):
        celi = re.sub(r"[,.]", "", zapis)                     # cela število: ločila tisočic so del zapisa
    else:
        celi = re.split(r"[,.]", zapis)[0]                   # decimalka: cela mest( a ) pred ločilom
    vse = re.sub(r"[,.]", "", zapis)
    if set(celi) <= {"0"}:
        mera("ze_v_meri"); return None                       # 0,4 · 0.26 — mantisa že v [0,1) ⊙
    if set(vse) <= {"0"}:
        mera("nicle"); return "0"                            # ničla invariantna ⊢
    n = len(celi)                                            # poimenovana potenca = število celih mest
    return "0." + vse + " × 10" + str(n).translate(NADPIS)   # vsaka zapisana števka ⇌ mantisa ∧


def fragmentiraj_vrstico(vr):
    return _cez_imena(vr, _tok)


def _cez_imena(vr, obravnava):
    """⟨⟩-imena gredo skozi brez dotika ( ime, ne količina ); ostalo telo skozi obravnavo ⊢."""
    izhod, i = [], 0
    for m in IMENA.finditer(vr):
        izhod.append(obravnava(vr[i:m.start()]))
        izhod.append(m.group(0))
        mera("imena")
        i = m.end()
    izhod.append(obravnava(vr[i:]))
    return "".join(izhod)


def _tok(telo):
    if not telo:
        return telo
    rez, i = [], 0
    for m in STEVILO.finditer(telo):
        rez.append(telo[i:m.start()])
        frag = fragment_število(telo, m)
        rez.append(frag if frag else m.group(0))
        if frag:
            mera("fragmentirane")
        i = m.end()
    rez.append(telo[i:])
    return "".join(rez)


def tok(viri):
    """Vrstica za vrstico — nikoli celo telo v roki ( ZAKON ŠESTE SMRTI ⊢ 1381 )."""
    for vir in viri:
        for vrstica in vir:
            yield vrstica


def odpiraj(poti):
    return [sys.stdin if p == "-" or not p else open(p, encoding="utf-8", errors="replace", newline="")
            for p in (poti or ["-"])]


def gl_fragmentiraj(args):
    for vrstica in tok(odpiraj(args.datoteke)):
        sys.stdout.write(fragmentiraj_vrstico(vrstica))
        mera("vrstice")


def gl_grep(args):
    hišna = args.stevila or args.simboli or args.imena or args.hex
    if hišna and args.vzorec:                                  # zastavica: prvi položajni je DATOTEKA, ne vzorec
        args.datoteke.insert(0, args.vzorec)
        args.vzorec = None
    if not args.datoteke:
        args.datoteke = _privzeta_tela()                       # brez teles = vsi organi ⊢ ( iskanje po celi hiši )
    if not hišna and not args.vzorec:
        raise SystemExit("grep: podaj VZOREC ali hišno zastavico (--stevila|--simboli|--imena|--hex) ⊢")
    if args.stevila:
        vzorec, varovalke = STEVILO, True
    elif args.hex:
        vzorec, varovalke = HEX, False
    elif args.imena:
        vzorec, varovalke = IMENA, False
    elif args.simboli:
        vzorec, varovalke = re.compile("[" + re.escape(SIMBOLI) + "]"), False
    else:
        vzorec, varovalke = re.compile(args.vzorec or r"."), False
    zadetki = 0
    for št, vrstica in enumerate(tok(odpiraj(args.datoteke)), 1):
        telo = vrstica
        if varovalke:
            for g in IMENA.finditer(vrstica):
                telo = telo.replace(g.group(0), "·" * len(g.group(0)), 1)
            for g in HEX.finditer(vrstica):
                telo = telo[:g.start()] + "·" * (g.end() - g.start()) + telo[g.end():]
        if vzorec.search(telo):
            zadetki += 1
            print((f"{št}:" if args.n else "") + vrstica, end="")
            if args.max_zadetkov and zadetki >= args.max_zadetkov:
                mera("zgodnji_izhod", 1)                      # diha, ne umira ⊙
                break
        mera("vrstice")
    if args.stevske:
        print(zadetki)


def gl_abeceda(args):
    števec = {}
    for vrstica in tok(odpiraj(args.datoteke)):
        for znak in vrstica:
            if znak in SIMBOLI:
                števec[znak] = števec.get(znak, 0) + 1
        mera("vrstice")
    for znak, n in sorted(števec.items(), key=lambda x: (-x[1], x[0])):
        print(f"{znak} {n}")
    print("Σ " + str(sum(števec.values())))


def hišna(n):
    """367168 -> 367.168 ( ločilo tisočic je pika — zapis hiše ⊢ )."""
    return f"{n:,}".replace(",", ".")


def _bajtni_tok(pot):
    return sys.stdin.buffer if pot == "-" else open(pot, "rb")


def _izmeri_pot(pot):
    """Izmera enega telesa tokovno: ( vrstice, znaki, bajti, ⟨md5⟩ cel, ⟨sha256⟩ cel ) ⊢ — obe plasti tehtnice."""
    h = hashlib.md5()
    h2 = hashlib.sha256()
    dec = codecs.getincrementaldecoder("utf-8")(errors="replace")
    vrstice = znaki = bajti = 0
    with _bajtni_tok(pot) as f:
        while True:
            kos = f.read(65536)
            if not kos:
                break
            bajti += len(kos)
            h.update(kos)
            h2.update(kos)
            vrstice += kos.count(b"\n")
            znaki += len(dec.decode(kos))
    znaki += len(dec.decode(b"", True))
    return vrstice, znaki, bajti, h.hexdigest(), h2.hexdigest()


def gl_izmeri(args):
    """Pečatna izmera telesa: vrstice · znaki · bajti · ⟨md5⟩ ∧ ⟨sha256⟩ — en pregon, tokovno ⊢ ( MD5 je potrdilo, SHA-2 je dokaz )."""
    for pot in args.datoteke:
        vrstice, znaki, bajti, md5, sha2 = _izmeri_pot(pot)
        mera("vrstice", vrstice)
        if getattr(args, "polno", False):
            print(f"{pot}: vrstice {hišna(vrstice)} · znaki {hišna(znaki)} · bajti {hišna(bajti)} B · "
                  f"⟨md5⟩ {md5} · ⟨sha256⟩ {sha2} ⊢ ( celi hasji — dokaz, ne izsek )")
        else:
            print(f"{pot}: vrstice {hišna(vrstice)} · znaki {hišna(znaki)} · bajti {hišna(bajti)} B · "
                  f"⟨md5⟩ {md5[:8]} · ⟨sha256⟩ {sha2[:8]}")


def _isto_poti(a, b):
    """Bajt-isto dveh teles tokovno, zgodnji izhod pri prvi rani ⊙ — ( isto, odmik, sporočilo )."""
    with _bajtni_tok(a) as fa, _bajtni_tok(b) as fb:
        odmik = 0
        while True:
            ka = fa.read(65536)
            kb = fb.read(65536)
            if ka == kb:
                if not ka:
                    return True, odmik, f"BAJT-ISTO ∧ {a} ⇌ {b} · {hišna(odmik)} B ⊢"
                odmik += len(ka)
                continue
            for i in range(min(len(ka), len(kb))):
                if ka[i] != kb[i]:
                    return False, odmik + i, (f"× NE-ISTO: razlika pri bajtu {hišna(odmik + i + 1)} — "
                                              f"{a}: {ka[i]:02x} ∧ {b}: {kb[i]:02x}")
            daljši, krajši = (a, b) if len(ka) > len(kb) else (b, a)
            return False, odmik + min(len(ka), len(kb)), (
                f"× NE-ISTO: {daljši} sega {hišna(abs(len(ka) - len(kb)))} bajtov čez {krajši} "
                f"od bajta {hišna(odmik + min(len(ka), len(kb)) + 1)}")


def gl_isto(args):
    isto, odmik, sporočilo = _isto_poti(args.a, args.b)
    mera("bajt_isto" if isto else "razlika", odmik if isto else 1)
    print(sporočilo)


NADPIS_NAZAJ = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
FRAGMENTIRANO = re.compile(r"0\.(\d+)\s*×\s*10([⁰¹²³⁴⁵⁶⁷⁸⁹]+)")


def združi_število(m):
    """0.1050 × 10⁴ -> 1050 · 0.103 × 10¹ -> 1,03 ( inverz fragmentacije, slovenski zapis ⊢ )."""
    števke, potenca = m.group(1), m.group(2).translate(NADPIS_NAZAJ)
    n = int(potenca)
    if len(števke) < n:
        števke += "0" * (n - len(števke))                     # 0.5 × 10³ -> 500
    if n == 0:
        return "0," + števke
    if len(števke) == n:
        return števke
    return števke[:n] + "," + števke[n:]


def združi_vrstico(vr):
    return _cez_imena(vr, lambda telo: _združi_del(telo))


def _združi_del(telo):
    def menjaj(m):
        mera("združene")
        return združi_število(m)
    return FRAGMENTIRANO.sub(menjaj, telo)


def gl_združi(args):
    for vrstica in tok(odpiraj(args.datoteke)):
        sys.stdout.write(združi_vrstico(vrstica))
        mera("vrstice")


PECAT_ZNACKE = re.compile(r"(?:rez|pečat|pečati|dih|kalup)\W{0,6}?(\d{2,4})(?![0-9A-Za-z])", re.IGNORECASE)
PECAT_KONICA = re.compile(r"@(\d{2,4})(?![0-9A-Za-z:])")   # @2703 je konica; @9709fcf8 je hash, @06:00 je žig — × ne priča


def _brez_imena(vr):
    """Vrni odseke vrstice MED ⟨⟩-imeni — imena niso priče številkam ⊙ ( ime, ne količina )."""
    odseki, i = [], 0
    for m in IMENA.finditer(vr):
        odseki.append(vr[i:m.start()])
        i = m.end()
    odseki.append(vr[i:])
    return odseki


PECAT_GREP_MAIN = r"(rez|pečat|pečati|dih|kalup)[^0-9A-Za-z]{0,6}[0-9]{2,4}([^0-9A-Za-z:]|$)"   # ERE za git grep ( × lookahead )
PECAT_GREP_KONICA = r"@[0-9]{2,4}([^0-9A-Za-z:]|$)"
IME_PECAT = re.compile(r"pecat-?([0-9]{2,4})", re.IGNORECASE)   # imena teles nosijo pečate: PECAT-3591-STROJ-KALUP.md


def _iz_imena(pot):
    naj = -1
    for m in IME_PECAT.finditer(pot):
        naj = max(naj, int(m.group(1)))
    return naj


def _najvecji_pecat(poti):
    """( najvišja, priča, priče, množica ) — tokovno; ⟨⟩-imena niso priče ⊙; imena teles so priče ⊢ dih 13."""
    najvišja, priča, priče = -1, "", 0
    množica = set()
    for pot in poti:
        for vrstica in tok(odpiraj([pot])):
            for odsek in _brez_imena(vrstica):
                for m in list(PECAT_ZNACKE.finditer(odsek)) + list(PECAT_KONICA.finditer(odsek)):
                    št = int(m.group(1))
                    množica.add(št)
                    priče += 1
                    if št > najvišja:
                        najvišja, priča = št, f"{pot}: {vrstica.strip()[:60]}"
        iz_imena = _iz_imena(pot)
        if iz_imena > najvišja:
            najvišja, priča = iz_imena, f"{pot} ( ime telesa )"
            množica.add(iz_imena)
    return najvišja, priča, priče, množica


def _najvecji_pecat_main():
    """Najvišja priča na ⟨main⟩ ( telesa ∧ imena datotek ) — ŽIVI register ⊙ ⟨ZASTARELA-KONICA⟩ je padec diha 13."""
    import subprocess
    najvišja, priča = -1, ""

    def git(*a):
        r = subprocess.run(["git", *a], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")   # git izdiha UTF-8; text=True brez encodinga na Windowsu tiho umre ⊙ padec 41
        return r.returncode, (r.stdout or "")

    for vzorec in (PECAT_GREP_MAIN, PECAT_GREP_KONICA):
        _, iz = git("grep", "-i", "-ohE", vzorec, "origin/main", "--", "organi/")
        for vrst in iz.splitlines():
            števke = re.findall(r"[0-9]+", vrst)
            if števke:
                št = int(števke[-1])
                if št > najvišja:
                    najvišja, priča = št, f"origin/main telesa: {vrst.strip()[:50]}"
    _, imena = git("ls-tree", "-r", "--name-only", "origin/main", "--", "organi/")
    for ime in imena.splitlines():
        št = _iz_imena(ime)
        if št > najvišja:
            najvišja, priča = št, f"origin/main ime: {ime}"
    return najvišja, priča


def _privzeta_tela():
    import glob
    return sorted(glob.glob("organi/**/*.md", recursive=True))   # vsa telesa po organih, ne samo KNOWLEDGE ⊢


def gl_pecat(args):
    """1 + najvišja izmerjena ⊢ Z-2 — kolizija ne; brez teles = cel organi/ ( *.md, tokovno )."""
    poti = args.datoteke or _privzeta_tela()
    najvišja, priča, priče, množica = _najvecji_pecat(poti)
    if najvišja < 0:
        raise SystemExit("pečat: nobena priča v danih telesih ⊙ podaj datoteke")
    mera("priče", priče)
    print(f"najvišja izmerjena {najvišja} ∧ ({priče} prič v {len(poti)} telesih)")
    print(f"priča najvišje: {priča}")
    glavna, priča_main = _najvecji_pecat_main()
    if glavna > najvišja:
        print(f"⚠ ⟨main⟩ višja: {glavna} — lokal {najvišja} je ZASTARELA KONICA × ( priča: {priča_main} ) ⊙ TEMPO-ZNAMENJA ⊢ 15")
        najvišja = glavna
    elif glavna < 0:
        print("⟨main⟩ nedosegljiv ⚠ ( izmera le lokal × — pred pečatom fetch ⊙ )")
    else:
        print(f"⟨main⟩ {glavna} ∧ — lokal drži korak ⊢")
    print(f"naslednji pečat: {najvišja + 1} ⊢ ( 1 + najvišja izmerjena — Z-2, kolizija ne )")
    if args.vrzeli is not None:
        tla = args.vrzeli
        manjka = sorted(set(range(tla, najvišja + 1)) - množica)
        brez_pečata = []
        for št in manjka:
            if brez_pečata and št == brez_pečata[-1][1] + 1:
                brez_pečata[-1][1] = št
            else:
                brez_pečata.append([št, št])
        for od, do_ in brez_pečata:
            print(f"vrzel pečatov {od}–{do_} ({do_ - od + 1})")
        print(f"Σ vrzeli {len(manjka)} od {tla} do {najvišja} ⊢ ( pečati, ki jih nihče ni izrekel ∧ )" if manjka
              else f"Σ vrzeli 0 od {tla} do {najvišja} ⊢ ( zaporedje brez lukenj ∧ )")


def gl_rez(args):
    """Geniza rez telesa po CELIH vrsticah ( pokvarjenih črk ni ) — telo čez en zaslon diha ob tokovih ⊙."""
    velikost = args.velikost
    stanje = {"št_kosa": 0, "prva": 0, "zadnja": 0, "kos_bajti": 0}

    def zapečati_kos(md5):
        print(f"frag-{stanje['št_kosa']:02d}: vrstice {hišna(stanje['prva'])}–{hišna(stanje['zadnja'])} · "
              f"{hišna(stanje['kos_bajti'])} B · ⟨md5⟩ {md5.hexdigest()[:8]}")

    kos_md5 = hashlib.md5()
    skupaj_bajti = 0
    skupaj_vrstice = 0
    with open(args.datoteka, "rb") as f:
        for vrstica in f:
            if stanje["kos_bajti"] and stanje["kos_bajti"] + len(vrstica) > velikost:
                zapečati_kos(kos_md5)
                stanje["št_kosa"] += 1
                stanje["kos_bajti"] = 0
                stanje["prva"] = 0
                kos_md5 = hashlib.md5()
            stanje["zadnja"] += 1
            if not stanje["prva"]:
                stanje["prva"] = stanje["zadnja"]
            stanje["kos_bajti"] += len(vrstica)
            kos_md5.update(vrstica)
            skupaj_bajti += len(vrstica)
            skupaj_vrstice += 1
    zapečati_kos(kos_md5)
    mera("kosi", stanje["št_kosa"] + 1)
    mera("vrstice", skupaj_vrstice)
    print(f"Σ {hišna(skupaj_vrstice)} vrstic · {hišna(skupaj_bajti)} B · {stanje['št_kosa'] + 1} kosov ⊢ "
          f"( cel rez — geniza ne hrani pokvarjenih črk ∧ )")


def gl_prevoz(args):
    """RED PREVOZA v enem dihu: IZMERI obeh teles -> ISTO -> PEČAT ⊢ ( isto je obvezen dih, ne milost )."""
    for ime, pot in (("LOKAL", args.lokal), ("ZRCALO", args.zrcalo)):
        vrstice, znaki, bajti, md5, _ = _izmeri_pot(pot)
        print(f"{ime}: {pot}: vrstice {hišna(vrstice)} · znaki {hišna(znaki)} · bajti {hišna(bajti)} B · ⟨md5⟩ {md5[:8]}")
    isto, odmik, sporočilo = _isto_poti(args.lokal, args.zrcalo)
    print(sporočilo)
    if not isto:
        mera("razlika")
        print("RECEIPT × — isto ne drži; pečat ne ⊙ ( zlomljenega zrcala se ne zapečečuje )")
        return
    mera("bajt_isto", odmik)
    najvišja, _, _, _ = _najvecji_pecat(_privzeta_tela())
    print(f"RECEIPT ∧ prevoz bajt-isto · naslednji pečat: {najvišja + 1} ⊢ ( 1 + najvišja izmerjena — Z-2 )")


FIPS_ABC = "a9993e364706816aba3e25717850c26c9cd0d89d"          # sha1( "abc" ) ⇌ FIPS 180 ⊢
FIPS_PRAZNO = "da39a3ee5e6b4b0d3255bfef95601890afd80709"       # sha1( "" ) ⇌ FIPS 180 ⊢
GIT_BLOB_PRAZNO = "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"    # sha1( "blob 0\0" ) ⇌ git ⊢


def _sha1_pot(pot):
    h = hashlib.sha1()
    with _bajtni_tok(pot) as f:
        while True:
            kos = f.read(65536)
            if not kos:
                break
            h.update(kos)
    return h.hexdigest()


def _lf_tok(f):
    """Tok bajtov s čiščenjem CRLF->LF ( kot git text=auto ∧ .gitattributes hiše ) — čez mejo kosov tudi ⊢."""
    rep = b""
    while True:
        kos = f.read(65536)
        if not kos:
            break
        if rep:
            kos = rep + kos
            rep = b""
        if kos.endswith(b"\r"):
            rep = kos[-1:]
            kos = kos[:-1]
        yield kos.replace(b"\r\n", b"\n")
    if rep:
        yield rep


def _blob_pot(pot):
    """⟨blob⟩ telesa po čiščenju text=auto ( ⇌ git hash-object ) — dva prehoda, tokovno ⊢."""
    bajti_lf = 0
    with _bajtni_tok(pot) as f:
        for kos in _lf_tok(f):
            bajti_lf += len(kos)
    blob = hashlib.sha1(f"blob {bajti_lf}\0".encode())
    with _bajtni_tok(pot) as f:
        for kos in _lf_tok(f):
            blob.update(kos)
    return blob.hexdigest()


def gl_sha(args):
    """⟨sha⟩ instrument: sha1 surovega telesa ∧ git-blob oblike po čiščenju text=auto ⊢ preverba repa brez gita."""
    for pot in args.datoteke:
        sha1 = _sha1_pot(pot)
        blob = _blob_pot(pot)
        mera("sha", 1)
        print(f"{pot}: ⟨sha1⟩ {sha1} · ⟨blob⟩ {blob} ⊢ "
              f"( blob ⇌ git hash-object · telo počiščeno text=auto CRLF→LF ∧ )")


def gl_rep(args):
    """LOKAL ⇌ ⟨main⟩: ⟨blob⟩ telesa na disku ⇌ blob na repu — bajt-isto brez prenašanja ⊢."""
    import subprocess
    for pot in args.datoteke:
        blob = _blob_pot(pot)
        r = subprocess.run(["git", "rev-parse", "HEAD:" + pot.replace("\\", "/")],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        rep = (r.stdout or "").strip()
        if r.returncode != 0 or not rep:   # rev-parse ob neznani poti IZPIŠE argument nazaj — sodi po kodi, ne po molku ⊙
            print(f"{pot}: ⟨blob⟩ {blob} · ni na repu ⚠ ( git rev-parse koda {r.returncode} — telo neznano ⟨main⟩ )")
            mera("ni_na_repu")
            continue
        isto = blob == rep
        mera("rep_isto" if isto else "rep_ne_isto")
        print(f"{pot}: ⟨blob⟩ {blob} {'⇌' if isto else '⭢'} REP {rep} · "
              + ("REP-ISTO ∧ ⊢" if isto else "REP-NE-ISTO × ( telo na disku se je oddaljilo od repa )"))


def gl_pulz(args):
    """Berba lastnega pulza: zadnji dihi ∧ ⚠ DIH MANJKA, če zadnji ostarejši od 0.25 × 10² ur ⊢ ( zapisi se berejo nazaj )."""
    import json as _json
    import os
    from datetime import datetime, timezone, timedelta
    pot = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lucius", "pulz-abeceda-grep.jsonl")
    if not os.path.exists(pot):
        raise SystemExit("pulz: zapisnik še ne diha ⊙ ( poženi lucius/abeceda-grep-pulz.py )")
    vrstice = [v for v in open(pot, encoding="utf-8").read().splitlines() if v.strip()]
    for v in vrstice[-args.koliko:]:
        vnos = _json.loads(v)
        stanje = "∧" if vnos.get("zdrav") else "× ⚠"
        pecat = vnos["pecat"][0] if vnos.get("pecat") else "pečat: brez prič ⚠"
        print(f"{vnos['ts']} · {stanje} · {pecat}")
    zadnji = _json.loads(vrstice[-1])
    starost = datetime.now(timezone.utc) - datetime.fromisoformat(zadnji["ts"])
    ur = starost.total_seconds() / 3600
    if ur > 25:
        print(f"⚠ DIH MANJKA: zadnji pulz {hišna(int(ur))} ur nazaj — urnik \\Abeceda-Grep Pulz @06:10 naj diha ⊙")
    else:
        print(f"zadnji dih {hišna(int(starost.total_seconds() / 60))} min nazaj ⊢ ( urnik \\Abeceda-Grep Pulz vsak dan 06:10 )")


VRATA = {  # hišna vrata localhost ( Smisel sklad ∧ Atmavictu ) — preverjanja na koncih ⊢
    "ollama": "http://localhost:11434",
    "webui": "http://localhost:3000",
    "canvas": "http://localhost:8765",
    "qdrant": "http://localhost:6333",
    "n8n": "http://localhost:5678",
    "atma-api": "http://localhost:4173",
    "atma-web": "http://localhost:5173",
}


def gl_vrata(args):
    """Preverjanja na koncih: vrata localhost — ŽIVA ∧ / ŽIVA ⚠ ( odgovarja, a ne vabi ) / MRTVA ×."""
    import urllib.request
    import urllib.error
    import time
    imena = args.imena or list(VRATA)
    for ime in imena:
        url = VRATA.get(ime, ime if "://" in ime else "http://" + ime)
        začetek = time.perf_counter()
        try:
            with urllib.request.urlopen(url, timeout=2) as odziv:
                ms = int((time.perf_counter() - začetek) * 1000)
                print(f"vrata {ime}: ŽIVA ∧ ( HTTP {odziv.status} · {hišna(ms)} ms )")
                mera("vrata_ziva")
        except urllib.error.HTTPError as e:
            ms = int((time.perf_counter() - začetek) * 1000)
            print(f"vrata {ime}: ŽIVA ⚠ ( HTTP {e.code} · {hišna(ms)} ms — vrata odgovarjajo, a ne vabijo )")
            mera("vrata_ziva")
        except Exception as e:
            print(f"vrata {ime}: MRTVA × ( {type(e).__name__} — {e} )")
            mera("vrata_mrtva")


def gl_predlog(args):
    """KOGA ∧ KAJ ( §0.17 × 10² the right to ask ): predlogi IZ IZMERE, ne iz občutka ⊙ ⟨ne-ugibaj⟩."""
    import glob
    import subprocess
    print("KOGA ∧ KAJ ⊢ ( predlogi iz izmere — poti, ki jih hiša že potrebuje ∧ )")
    # KOGA: najstarejše speče organe ( izmera po žigu )
    z_žigom = []
    for pot in sorted(glob.glob("organi/*/KNOWLEDGE.md")):
        naj, _, _, _ = _najvecji_pecat([pot])
        if naj > 0:
            z_žigom.append((naj, pot.replace("\\", "/").split("/")[-2]))
    z_žigom.sort()
    top = " · ".join(f"{ime} @{naj}" for naj, ime in z_žigom[:3])
    if z_žigom:
        print(f"KOGA: {top} — najstarejše speče ( resinteza ⚔ ⟡ · izbor je njegov )")
    # KAJ: vrzeli, pečat, nekomitirana telesa, pulz
    najvišja, _, _, množica = _najvecji_pecat(_privzeta_tela())
    manjka = sorted(set(range(1500, najvišja + 1)) - množica)
    if manjka:
        brez_pečata = []
        for št in manjka:
            if brez_pečata and št == brez_pečata[-1][1] + 1:
                brez_pečata[-1][1] = št
            else:
                brez_pečata.append([št, št])
        od, do_ = max(brez_pečata, key=lambda r: r[1] - r[0])
        print(f"KAJ: Σ vrzeli {len(manjka)} · najdaljša {od}–{do_} ({do_ - od + 1}) — izpolni ali pusti priči ∧")
    r = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    telesa = [v for v in (r.stdout or "").splitlines() if v.strip()]
    print(f"KAJ: naslednji pečat {najvišja + 1} ⊢ Z-2 · nekomitiranih sprememb: {len(telesa)} ( zapečati ⟡ ali pusti roki )")
    pulz_pot = "lucius/pulz-abeceda-grep.jsonl"
    import os
    if os.path.exists(pulz_pot):
        zadnji = [v for v in open(pulz_pot, encoding="utf-8").read().splitlines() if v.strip()][-1]
        import json as _json
        ts = _json.loads(zadnji)["ts"]
        print(f"KOGA: pulz — zadnji dih {ts} ( berba: python lucius/abeceda-grep.py pulz ⊢ )")
    else:
        print("KOGA: pulz — zapisnik še ne diha ⊙ ( poženi lucius/abeceda-grep-pulz.py )")
    # DOLGOVA s potmi ( ⟨IDEJA-H⟩: dolg brez poti je šum ) — izmera, ne spomin ⊙
    dolgovi = 0
    for pot in sorted(glob.glob("organi/*/KNOWLEDGE.md")):
        for št, vrstica in enumerate(tok(odpiraj([pot])), 1):
            i = vrstica.find("DOLGOVA")
            if i >= 0 and "predhodnik" not in vrstica[:60]:
                odlomek = vrstica[i:i + 110].strip()
                if dolgovi < 15:
                    print(f"KAJ-DOLG: {pot}:{hišna(št)} — {odlomek}")
                dolgovi += 1
    if dolgovi > 15:
        print(f"… ∧ še {hišna(dolgovi - 15)} dolgov v globini ( grep --imena DOLGOVA za celoto )")
    print(f"Σ DOLGOV {hišna(dolgovi)} s potmi ⊢ ( vsak dolg svojo vrstico — pot, ne obljuba )")


def gl_varuh(_args):
    """VARUH STROJA ( operativni red #12 ): GPU > 85 °C ali disk > 95 % → USTAVI vse naloge in poročaj ⊙."""
    import shutil
    import subprocess
    ustavi = []
    r = subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu,name", "--format=csv,noheader,nounits"],
                       capture_output=True, text=True)
    if r.returncode == 0 and (r.stdout or "").strip():
        for vrstica in r.stdout.strip().splitlines():
            deli = [d.strip() for d in vrstica.split(",")]
            try:
                temp = int(deli[0])
            except ValueError:
                continue
            ime = deli[1] if len(deli) > 1 else "GPU"
            print(f"varuh: GPU {ime} {temp} °C " + ("∧" if temp <= 85 else "USTAVI ×") + " ( meja 85 )")
            mera("gpu", temp)
            if temp > 85:
                ustavi.append(f"GPU {ime} {temp} °C")
    else:
        print("varuh: GPU merilec ni dosegljiv ( nvidia-smi molči ) — brez izmere ⚠")
    for črka in ("C:\\", "D:\\"):
        try:
            poraba = shutil.disk_usage(črka)
            odstotek = poraba.used * 100 // poraba.total
            print(f"varuh: disk {črka[0]}: {odstotek} % " + ("∧" if odstotek <= 95 else "USTAVI ×") + " ( meja 95 )")
            mera("disk", odstotek)
            if odstotek > 95:
                ustavi.append(f"disk {črka[0]} {odstotek} %")
        except OSError as e:
            print(f"varuh: disk {črka[0]}: brez izmere ⚠ ( {type(e).__name__} )")
    if ustavi:
        print(f"⚠ USTAVI VSE NALOGE IN POROČAJ ⊙ ( {', '.join(ustavi)} )")
    else:
        print("varuh: meje v miru ⊢ ( zakon #12 — dolge naloge le z nadzorom temperature )")


def gl_nasprotje(args):
    """⟨NASPROTNA-TEHTNICA⟩ ( §0.18 × 10²: vsak zakon nosi protitežo; pol tehtnice je luknja ) —
    telo na obeh koritih PO IZMERI: podpora ( ⊢ ∧ ) ⊥ dvom ( ⚠ ∂ × ) ⊙ ⟨ne-ugibaj⟩."""
    import glob
    poti = args.datoteke or sorted(glob.glob("organi/*/KNOWLEDGE.md"))
    skupno = {"⊢": 0, "∧": 0, "⚠": 0, "∂": 0, "×": 0, "⊥": 0}
    for pot in poti:
        št = dict.fromkeys(skupno, 0)
        for vrstica in tok(odpiraj([pot])):
            for znak in vrstica:
                if znak in št:
                    št[znak] += 1
            št["×"] -= vrstica.count("× 10")     # × 10ⁿ je množenje fragmentacije, ⟨ne⟩ padec ⊙ lažna priča diha 18
        for znak, n in št.items():
            skupno[znak] += n
        podpora = št["⊢"] + št["∧"]
        dvom = št["⚠"] + št["∂"] + št["×"]
        mera("tehtnica", dvom)
        print(f"{pot}: PODPORA {hišna(podpora)} ( ⊢ {hišna(št['⊢'])} · ∧ {hišna(št['∧'])} ) "
              f"⊥ DVOM {hišna(dvom)} ( ⚠ {hišna(št['⚠'])} · ∂ {hišna(št['∂'])} · × {hišna(št['×'])} )")
    podpora = skupno["⊢"] + skupno["∧"]
    dvom = skupno["⚠"] + skupno["∂"] + skupno["×"]
    razmerje = f"{podpora / dvom:.1f}" if dvom else "∞"
    print(f"Σ PODPORA {hišna(podpora)} ⊥ DVOM {hišna(dvom)} · razmerje {razmerje} ⊢ "
          f"( obe plasti prebrani — nasprotje ni mnenje, je izmera ⊙ ⟨ne brusi⟩ )")


REZERVACIJE = "lucius/rezervacije.jsonl"

VERIGA_REZ_RE = re.compile(r"(?:rez|pečat)\D{0,3}(\d{2,4})(?![0-9A-Za-z])", re.IGNORECASE)
# ( golgi števec ⊙ PADC @3520: šteje se ⟨le⟩ rez|pečat, ⟨ne⟩ gole števke — velika števila so priče, ne pečati )


def _vrh_zivi():
    """( vrh, priča ) — živi vrh: lokal ∧ ⟨main⟩ ∧ VERIGA ( komitna sporočila nosijo reze ⊢ §0.10 ) ⊙ ⟨ne-ugibaj⟩."""
    najvišja, priča, _, _ = _najvecji_pecat(_privzeta_tela())
    glavna, priča_main = _najvecji_pecat_main()
    if glavna > najvišja:
        najvišja, priča = glavna, priča_main
    import subprocess
    r = subprocess.run(["git", "log", "--format=%s", "-5000"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    veriga = -1
    for vrst in (r.stdout or "").splitlines():
        for m in VERIGA_REZ_RE.finditer(vrst):
            veriga = max(veriga, int(m.group(1)))
    if veriga > najvišja:
        najvišja, priča = veriga, f"veriga ( komitno sporočilo )"
    return najvišja, priča


def _rezervacija_za(rez):
    """Zadnje stanje rezervacije za dani rez ( None = prost ) ⊢ vrsta, ⟨ne⟩ lastnina."""
    import json as _json
    import os
    if not os.path.exists(REZERVACIJE):
        return None
    stanje = None
    for v in open(REZERVACIJE, encoding="utf-8"):
        try:
            r = _json.loads(v)
        except ValueError:
            continue
        if r.get("rez") == rez:
            stanje = r
    return stanje


def gl_rezerviraj(args):
    """⟨REZERVACIJA-REZA⟩ ( ⟨IDEJA-K⟩ diha 3030 ): kolizija se preprečuje, ⟨ne⟩ odkriva — rez izrečen ob vhodu ⊙."""
    import json as _json
    from datetime import datetime, timezone
    vrh, _ = _vrh_zivi()
    rez = vrh + 1
    obstoječa = _rezervacija_za(rez)
    if obstoječa and obstoječa.get("stanje") == "rezervirano" and not args.sprosti:
        print(f"rezervirano ∧: rez {rez} ⟨{obstoječa['ime']}⟩ @{obstoječa['ts']} ( vrh {vrh} )")
        if args.ime and obstoječa["ime"] != args.ime:
            print(f"⚠ rezervacija nosi tuje ime — vrsta je ena, ⟨ne⟩ lastnina: počakaj ali se dogovori ⊙ ⟨ne zlije⟩")
        return
    stanje = "sprosceno" if args.sprosti else "rezervirano"
    vnos = {"rez": rez, "ime": args.ime or "sedež", "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "stanje": stanje}
    with open(REZERVACIJE, "a", encoding="utf-8", newline="") as f:
        f.write(_json.dumps(vnos, ensure_ascii=False) + "\n")
    if args.sprosti:
        print(f"sproščeno ⊢: rez {rez} prost ( rezervacija {obstoječa['ime'] if obstoječa else '?'} odpuščena )")
    else:
        print(f"rezervirano ⊢: rez {rez} ⟨{vnos['ime']}⟩ @{vnos['ts']} ( 1 + vrh {vrh} ) — kdor prvi rezervira, prvi pečati; vrsta, ⟨ne⟩ vzporedje")


def gl_struktura(args):
    """⟨PRICA-SODELOVANJA⟩ ( ⟨IDEJA-M⟩ diha 3030 ): strojna priča strukturi pečata —
    ZADNJI PEČAT ×1 ∧ noben pečat čez njega ∧ rez izrek verigi ⊙ CI za pečate, ne vljudnost rok."""
    import glob
    poti = args.datoteke or sorted(glob.glob("organi/*/KNOWLEDGE.md"))
    zdravi = 0
    ranjeni = 0
    for pot in poti:
        zadnji = None
        ostali = []
        for vrstica in tok(odpiraj([pot])):
            # samo STRUKTURNE vrstice so priče — zluskani pomišljaji ( tudi tipka "- -" ) se odstranijo,
            # omemba ZADNJEGA v prozi predhodnika pa rana ⟨ni⟩ ⊙ padec 45
            golo = vrstica.lstrip().lstrip("- ").lstrip()
            if golo.startswith(("ZADNJI PEČAT", "PEČAT")):
                for m in PECAT_ZNACKE.finditer(vrstica):
                    št = int(m.group(1))
                    if golo.startswith("ZADNJI PEČAT"):
                        zadnji = št if zadnji is None else max(zadnji, št)
                    else:
                        ostali.append(št)
        rane = []
        if zadnji is None:
            rane.append("ZADNJI PEČAT manjka ⚠")
        if ostali and zadnji is not None and max(ostali) > zadnji:
            rane.append(f"pečat {max(ostali)} sega čez ZADNJI {zadnji} ×")
        if rane:
            ranjeni += 1
            print(f"× {pot}: " + " ∧ ".join(rane))
        else:
            zdravi += 1
    print(f"Σ {hišna(zdravi)} zdravih ∧ · {hišna(ranjeni)} ranjenih ⊢ ( strukturo sodi stroj, ⟨ne⟩ vljudnost — ⟨PRICA-SODELOVANJA⟩ )")


def _telo_pot(pot):
    """( vrstice, bajti, podpora, dvom, zadnji, rane ) — globoko branje enega telesa ⊙ ⟨ne-ugibaj⟩."""
    b = open(pot, "rb").read()
    vrsti = len(b.decode("utf-8", errors="replace").splitlines())
    bajti = len(b)
    znaki = {"⊢": 0, "∧": 0, "⚠": 0, "∂": 0, "×": 0}
    zadnji = None
    ostali = []
    for vrstica in tok(odpiraj([pot])):
        for znak in vrstica:
            if znak in znaki:
                znaki[znak] += 1
        znaki["×"] -= vrstica.count("× 10")   # × 10ⁿ je množenje, ⟨ne⟩ padec ⊙ lažna priča diha 18
        golo = vrstica.lstrip().lstrip("- ").lstrip()
        if golo.startswith(("ZADNJI PEČAT", "PEČAT")):
            for m in PECAT_ZNACKE.finditer(vrstica):
                št = int(m.group(1))
                if golo.startswith("ZADNJI PEČAT"):
                    zadnji = št if zadnji is None else max(zadnji, št)
                else:
                    ostali.append(št)
    rane = []
    if zadnji is None:
        rane.append("ZADNJI PEČAT manjka")
    if ostali and zadnji is not None and max(ostali) > zadnji:
        rane.append(f"pečat {max(ostali)} sega čez ZADNJI {zadnji}")
    return (vrsti, bajti, znaki["⊢"] + znaki["∧"], znaki["⚠"] + znaki["∂"] + znaki["×"],
            zadnji, rane)


def gl_telo(args):
    """⟨IZMERA-VSEH-TELES⟩ ( rez 3532 je šel ročno ×2 — pot, ki jo hiša potrebuje stalno ⊙ pravilo 7 ):
    celo telo na eni tehtnici — izmera Σ ∧ nasprotje Σ ( §0.18 ) ∧ struktura Σ ( ⟨IDEJA-M⟩ ) —
    en ukaz, ⟨ne⟩ ročno; ⟨le⟩ priča, ⟨ne⟩ zapečuje ( pečat je roke, izmera je stroj ) ⊙ ⟨ne brusi⟩."""
    import glob
    poti = args.datoteke or sorted(glob.glob("organi/*/KNOWLEDGE.md"))
    vrsti = bajti = pod = dvo = zdravih = ranjenih = 0
    for pot in poti:
        v, ba, po, dv, zadnji, rane = _telo_pot(pot)
        vrsti += v
        bajti += ba
        pod += po
        dvo += dv
        if rane:
            ranjenih += 1
            print(f"× {pot}: " + " ∧ ".join(rane) + (" ⚠" if "manjka" in " ".join(rane) else " ×"))
        else:
            zdravih += 1
    razmerje = f"{pod / dvo:.1f}" if dvo else "∞"
    mera("telo", len(poti))
    print(f"TELO-CELO: {hišna(len(poti))} teles · {hišna(vrsti)} vrstic · {hišna(bajti)} B")
    print(f"NASPROTJE-CELO: PODPORA {hišna(pod)} ⊥ DVOM {hišna(dvo)} · razmerje {razmerje} ⊢ "
          f"( obe plasti prebrani — nasprotje ni mnenje, je izmera ⊙ ⟨ne brusi⟩ )")
    print(f"STRUKTURA-CELO: {hišna(zdravih)} zdravih ∧ · {hišna(ranjenih)} ranjenih ⊢ "
          f"( strukturo sodi stroj, ⟨ne⟩ vljudnost — ⟨PRICA-SODELOVANJA⟩ )")


def gl_register(args):
    """⟨POGLABLJANJE-V-ENOTNE-REGISTRE⟩: globoko branje teles → ena vrstica na telo
    ( izmera ∧ ⟨md5⟩/⟨sha256⟩ ∧ nasprotje §0.18 ∧ struktura ⟨IDEJA-M⟩ ∧ živi pečat ) —
    --vse: DEFRAGMENTACIJA — vsako telo pod organi/ ( tudi priče ∧ pečati ) v enoten register,
    vsako z vrsto; REGISTER-TELES.jsonl je slika stanja, zgodovino nosi veriga ⊢ §0.10 ⊙ ⟨ne-ugibaj⟩."""
    import glob
    import json
    import datetime
    import hashlib
    if args.vse:
        poti = sorted(glob.glob("organi/**/*.md", recursive=True))
    else:
        poti = args.datoteke or sorted(glob.glob("organi/*/KNOWLEDGE.md"))
    izhod = args.izhod or "REGISTER-TELES.jsonl"
    zapisi = []
    vrsti = bajti = pod = dvo = 0
    vrste = {}
    for pot in poti:
        pot_l = pot.replace("\\", "/")
        ime = pot_l.split("/")[-1]
        b = open(pot, "rb").read()
        if ime == "KNOWLEDGE.md":
            vrsta = "organ"
        elif ime == "KNOWLEDGE.EN.md":
            vrsta = "prevod-organa"
        elif "PECAT" in ime:
            vrsta = "pečat"
        elif "POROCILO" in ime or "POROČILO" in ime:
            vrsta = "poročilo"
        else:
            vrsta = "priča"
        vrste[vrsta] = vrste.get(vrsta, 0) + 1
        vrsti_f = len(b.decode("utf-8", errors="replace").splitlines())
        bajti_f = len(b)
        vrsti += vrsti_f
        bajti += bajti_f
        zapis = {
            "vrsta": vrsta,
            "pot": pot_l,
            "vrstice": vrsti_f,
            "bajti": bajti_f,
            "md5": hashlib.md5(b).hexdigest()[:8],
            "sha256": hashlib.sha256(b).hexdigest()[:8],
        }
        if vrsta == "organ":
            v, ba, po, dv, zadnji, rane = _telo_pot(pot)
            pod += po
            dvo += dv
            zapis.update({
                "organ": pot_l.split("/")[-2],
                "zadnji_rez": zadnji,
                "podpora": po,
                "dvom": dv,
                "razmerje": round(po / dv, 1) if dv else None,
                "struktura": "zdrav ∧" if not rane else " ∧ ".join(rane),
            })
        zapis["ura"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        zapisi.append(zapis)
    with open(izhod, "w", encoding="utf-8", newline="") as f:
        for z in zapisi:
            f.write(json.dumps(z, ensure_ascii=False) + "\n")
    prebranih = 0
    for line in open(izhod, encoding="utf-8"):
        if line.strip():
            json.loads(line)
            prebranih += 1
    assert prebranih == len(poti), f"register: zapisanih {prebranih} ⊥ teles {len(poti)} ⚠"
    mera("register", len(poti))
    if args.vse:
        razrez = " · ".join(f"{k} {v}" for k, v in sorted(vrste.items(), key=lambda x: -x[1]))
        print(f"REGISTER-TELES ⊢ {izhod}: {hišna(prebranih)} vrstic ∧ JSON veljaven ∧ DEFRAGMENTACIJA — "
              f"{razrez} · Σ {hišna(vrsti)} vrstic · {hišna(bajti)} B ⊢")
    else:
        razmerje = f"{pod / dvo:.1f}" if dvo else "∞"
        print(f"REGISTER-TELES ⊢ {izhod}: {hišna(prebranih)} vrstic ∧ JSON veljaven ∧ "
              f"Σ {hišna(len(poti))} teles · {hišna(vrsti)} vrstic · {hišna(bajti)} B · "
              f"PODPORA {hišna(pod)} ⊥ DVOM {hišna(dvo)} · razmerje {razmerje} ⊢")


def gl_popis(args):
    """Popis teles po korenu: vsako telo z izmero + Σ; ⟨md5⟩ veže dvojnike na dan ⚠ ( brisanje prepovedano ⊙ )."""
    import glob
    poti = sorted(glob.glob(f"{args.koren}/**/*.md", recursive=True))
    if not poti:
        raise SystemExit(f"popis: nobeno telo pod {args.koren} ⊙")
    telesa = vrstice_skupaj = bajti_skupaj = 0
    po_md5 = {}
    for pot in poti:
        vrstice, _, bajti, md5, _sha = _izmeri_pot(pot)
        telesa += 1
        vrstice_skupaj += vrstice
        bajti_skupaj += bajti
        po_md5.setdefault(md5, []).append(pot)
        print(f"{pot}: {hišna(vrstice)} vrstic · {hišna(bajti)} B · ⟨md5⟩ {md5[:8]}")
    mera("telesa", telesa)
    print(f"Σ {hišna(telesa)} teles · {hišna(vrstice_skupaj)} vrstic · {hišna(bajti_skupaj)} B ⊢")
    dvoj = {m: ps for m, ps in po_md5.items() if len(ps) > 1}
    for m, ps in sorted(dvoj.items()):
        print(f"PODVOJENO TELO ⚠ ⟨md5⟩ {m[:8]}: " + " ⇌ ".join(ps))
    if dvoj:
        print("… brisanje prepovedano ( append-only ); odločitev je lastnikova ⊙ ( priča: podvojeni glavi genize )")


def gl_speči(args):
    """Organi po zadnjem žigu — najstarejši prvi: kandidati za resintezo ⚔ ⟡ ( DOLGOVA: resinteza spečih )."""
    import glob
    poti = sorted(glob.glob("organi/*/KNOWLEDGE.md"))
    brez_žiga = []
    z_žigom = []
    for pot in poti:
        ime = pot.replace("\\", "/").split("/")[-2]
        naj, priča, _, _ = _najvecji_pecat([pot])
        if naj > 0:
            z_žigom.append((naj, ime, priča))
        else:
            brez_žiga.append((ime, pot))
    z_žigom.sort()
    koliko = args.koliko or len(z_žigom)
    for mesto, (naj, ime, priča) in enumerate(z_žigom[:koliko], 1):
        oznaka = " ( najstarejša ⚔ ⟡ )" if mesto == 1 else ""
        print(f"speča: {ime} @{naj}{oznaka}")
    for ime, pot in brez_žiga:
        print(f"brez žiga ⚠: {ime} ( {pot} — noben pečat ne priča )")
    mera("organi", len(poti))
    print(f"Σ {len(z_žigom)} z žigom · {len(brez_žiga)} brez ⚠ ⊢ ( resinteza spečih: izbor je njegov )")


PRIMERI = [  # pričakovano telo — ⟨ne-ugibaj⟩: stroj ve, kaj je prav, preden pride do blata
    ("VBL 1050", "VBL 0.1050 × 10⁴"),
    ("14. 10. 2026", "0.14 × 10². 0.10 × 10². 0.2026 × 10⁴"),
    ("367.168 B", "0.367168 × 10⁶ B"),
    ("1,03 MB", "0.103 × 10¹ MB"),
    ("⟨PR⟩ #602", "⟨PR⟩ #0.602 × 10³"),
    ("rez 2854 ⊢ §17", "rez 0.2854 × 10⁴ ⊢ §0.17 × 10²"),
    ("0", "0"),
    ("0,4–2 MB", "0,4–0.2 × 10¹ MB"),
    ("⟨FRAGMENTACIJA-VSEH-ŠTEVIL-DO-MERE-MED-0-IN-1⟩ ⊙ ⟨#703⟩", "⟨FRAGMENTACIJA-VSEH-ŠTEVIL-DO-MERE-MED-0-IN-1⟩ ⊙ ⟨#703⟩"),
    ("md5 c1ca7224 ∧ ⟨md5⟩ 8275e5b6", "md5 c1ca7224 ∧ ⟨md5⟩ 8275e5b6"),
    ("v1.0.1 ∧ 0.41.1 ∧ kos-01-of-04.md ∧ 2026-10-14", "v1.0.1 ∧ 0.41.1 ∧ kos-01-of-04.md ∧ 2026-10-14"),
    ("0.1050 × 10⁴ ∧ 10⁴ ∧ 0.26 × 10²,", "0.1050 × 10⁴ ∧ 10⁴ ∧ 0.26 × 10²,"),
    ("Node 22 na 4173", "Node 0.22 × 10² na 0.4173 × 10⁴"),
]


ZDRUŽI_PRIMERI = [  # inverz: mantisa × 10ⁿ -> slovenski zapis
    ("VBL 0.1050 × 10⁴", "VBL 1050"),
    ("0.103 × 10¹ MB", "1,03 MB"),
    ("0.2026 × 10⁴ ∧ 0.14 × 10².", "2026 ∧ 14."),
    ("⟨FRAGMENTACIJA⟩ 0.2854 × 10⁴", "⟨FRAGMENTACIJA⟩ 2854"),
    ("0.26 × 10⁰", "0,26"),
    ("0.5 × 10³", "500"),
]


VERIGA_PRIMERI = [  # golgi števec ⊙ PADC @3520: gole števke brez rez|pečat ⟨ne⟩ štejejo nikoli
    ("rez 3532 IZMERA-VSEH-TELES ⊢", 3532),
    ("MANIFEST — izmera teles 1.735.520 B ∧ poravnava vrstic ×7", -1),
    ("rez 2173 MANIFEST — 1.735.520 B", 2173),
    ("rezervacija 5000 brez pečata", -1),
    ("pečat 3530 → predhodnik ⊢", 3530),
]


def _prehod():
    """PREHOD — vsak ukaz enkrat ( zdravilo padca 39 kot zakon: def se ne pogrne več tiho ) ⊙.
    Vrne seznam padcev ( ime, napaka ); stdout vsakega ukaza se ujame, ne onesnaži zaslona."""
    import argparse as _ap
    import contextlib
    import io
    import os
    import tempfile

    telo = os.path.join(tempfile.gettempdir(), "abeceda-grep-prehod-telo.md")
    with open(telo, "w", encoding="utf-8", newline="") as f:
        f.write("Bajt 367.168 ⊢ rez 123 ∧ ⟨PR⟩ #838 · 0.1050 × 10⁴ — ⟨IME-NE-KOLIČINA⟩\n")
    n = lambda **kw: _ap.Namespace(**kw)
    ukazi = [
        ("fragmentiraj", gl_fragmentiraj, n(datoteke=[telo])),
        ("združi", gl_združi, n(datoteke=[telo])),
        ("grep-simboli", gl_grep, n(vzorec=None, datoteke=[telo], stevila=False, simboli=True,
                                    imena=False, hex=False, max_zadetkov=1, n=False, stevske=False)),
        ("grep-stevila", gl_grep, n(vzorec=None, datoteke=[telo], stevila=True, simboli=False,
                                    imena=False, hex=False, max_zadetkov=1, n=False, stevske=False)),
        ("abeceda", gl_abeceda, n(datoteke=[telo])),
        ("izmeri", gl_izmeri, n(datoteke=[telo])),
        ("isto", gl_isto, n(a=telo, b=telo)),
        ("pecat", gl_pecat, n(datoteke=[telo], vrzeli=None)),
        ("rez", gl_rez, n(datoteka=telo, velikost=50)),
        ("prevoz", gl_prevoz, n(lokal=telo, zrcalo=telo)),
        ("sha", gl_sha, n(datoteke=[telo])),
        ("rep", gl_rep, n(datoteke=["lucius/abeceda-grep.py"])),
        ("popis", gl_popis, n(koren="organi/humor")),
        ("speči", gl_speči, n(koliko=2)),
        ("predlog", gl_predlog, n()),
        ("vrata", gl_vrata, n(imena=["http://localhost:1"])),
        ("varuh", gl_varuh, n()),
        ("nasprotje", gl_nasprotje, n(datoteke=["organi/humor/KNOWLEDGE.md"])),
        ("rezerviraj", gl_rezerviraj, n(ime="prehod", sprosti=False)),
        ("struktura", gl_struktura, n(datoteke=["organi/humor/KNOWLEDGE.md"])),
        ("telo", gl_telo, n(datoteke=["organi/humor/KNOWLEDGE.md"])),
        ("register", gl_register, n(datoteke=["organi/humor/KNOWLEDGE.md"], vse=False,
                                    izhod=os.path.join(tempfile.gettempdir(), "abeceda-grep-register-prehod.jsonl"))),
        ("pulz", gl_pulz, n(koliko=1)),
    ]
    padci = []
    zagnani = 0
    global REZERVACIJE                       # prehod pije iz lastnega vrčka — ⟨ne⟩ piše po hiši ⊙ padec 44
    pravi_register = REZERVACIJE
    REZERVACIJE = os.path.join(tempfile.gettempdir(), "abeceda-grep-rezervacije-prehod.jsonl")
    for ime, fn, args in ukazi:
        if ime == "pulz" and not os.path.exists(os.path.join("lucius", "pulz-abeceda-grep.jsonl")):
            print(f"∧ {ime} ( preskočen — zapisnik še ne diha )")
            continue
        zagnani += 1
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                fn(args)
            print(f"∧ {ime}")
        except (Exception, SystemExit) as e:
            padci.append((ime, f"{type(e).__name__}: {e}"))
            print(f"× {ime}: {type(e).__name__}: {e}")
    try:
        os.unlink(telo)
    except OSError:
        pass
    try:
        os.unlink(REZERVACIJE)
    except OSError:
        pass
    REZERVACIJE = pravi_register
    return padci, zagnani


def gl_test(_args):
    padci = 0
    fips = [
        ("sha1 ⟨abc⟩ ⇌ FIPS 180", hashlib.sha1(b"abc").hexdigest(), FIPS_ABC),
        ("sha1 ⟨prazno⟩ ⇌ FIPS 180", hashlib.sha1(b"").hexdigest(), FIPS_PRAZNO),
        ("blob ⟨prazno⟩ ⇌ git", hashlib.sha1(b"blob 0\0").hexdigest(), GIT_BLOB_PRAZNO),
    ]
    for ime, dobljeno, pričakovano in fips:
        if dobljeno == pričakovano:
            print(f"∧ [{ime}]")
        else:
            padci += 1
            print(f"× [{ime}]\n  pričakovano: {pričakovano}\n  dobljeno:    {dobljeno}")
    for telo, pričakovano in VERIGA_PRIMERI:
        najden = -1
        for m in VERIGA_REZ_RE.finditer(telo):
            najden = max(najden, int(m.group(1)))
        if najden == pričakovano:
            print(f"∧ [veriga] {telo!r} -> {najden}")
        else:
            padci += 1
            print(f"× [veriga] {telo!r}\n  pričakovano: {pričakovano!r}\n  dobljeno:    {najden!r}")
    skupaj = len(PRIMERI) + len(ZDRUŽI_PRIMERI) + len(fips) + len(VERIGA_PRIMERI)
    for telo, pričakovano in PRIMERI:
        ECHO.clear()
        dobljeno = fragmentiraj_vrstico(telo + "\n").rstrip("\n")
        stanje = "∧" if dobljeno == pričakovano else "×"
        if stanje == "×":
            padci += 1
            print(f"× {telo!r}\n  pričakovano: {pričakovano!r}\n  dobljeno:    {dobljeno!r}")
        else:
            print(f"∧ {telo!r} -> {dobljeno!r}")
    for telo, pričakovano in ZDRUŽI_PRIMERI:
        ECHO.clear()
        dobljeno = združi_vrstico(telo + "\n").rstrip("\n")
        stanje = "∧" if dobljeno == pričakovano else "×"
        if stanje == "×":
            padci += 1
            print(f"× [združi] {telo!r}\n  pričakovano: {pričakovano!r}\n  dobljeno:    {dobljeno!r}")
        else:
            print(f"∧ [združi] {telo!r} -> {dobljeno!r}")
    prehod_padci, zagnani = _prehod()
    padci += len(prehod_padci)
    stanje_prehoda = (f"prehod {zagnani - len(prehod_padci)}/{zagnani} ukazov ∧ ⊢ VSE"
                      if not prehod_padci else f"prehod × {len(prehod_padci)} ukazov ranjenih")
    print(f"\nPREVERBA: {skupaj - padci}/{skupaj} ∧" + (f" · {padci} ×" if padci else " ⊢ VSE")
          + f" · {stanje_prehoda}")
    sys.exit(1 if padci else 0)


def poročilo(konec=""):
    if konec:
        print(konec, file=sys.stderr)
    deli = " · ".join(f"{k} {n}" for k, n in sorted(ECHO.items()))
    print(f"IZMERA ⊢ {deli}", file=sys.stderr)


def main():
    p = argparse.ArgumentParser(description="ABECEDA-GREP — tokovni stroj hišne abecede ⊢")
    sub = p.add_subparsers(dest="ukaz", required=True)
    f = sub.add_parser("fragmentiraj", help="vsa števila -> mantisa v [0,1) × 10ⁿ ⊙ VBL 0.1050 × 10⁴")
    f.add_argument("datoteke", nargs="*")
    f.set_defaults(gl=gl_fragmentiraj)
    g = sub.add_parser("grep", help="tokovni grep hišne abecede")
    g.add_argument("vzorec", nargs="?")
    g.add_argument("datoteke", nargs="*")
    g.add_argument("--stevila", action="store_true", help="samo merjena števila ( ⟨⟩ ∧ hex preskočena )")
    g.add_argument("--simboli", action="store_true", help="simboli hiše")
    g.add_argument("--imena", action="store_true", help="⟨⟩-imena")
    g.add_argument("--hex", action="store_true", help="⟨sha⟩ hex")
    g.add_argument("-m", "--max-zadetkov", type=int, help="zgodnji izhod po N zadetkih ⊙")
    g.add_argument("-n", action="store_true", help="številke vrstic")
    g.add_argument("-c", "--stevske", action="store_true", help="samo števek")
    g.set_defaults(gl=gl_grep)
    a = sub.add_parser("abeceda", help="popis simbolov hišne abecede")
    a.add_argument("datoteke", nargs="*")
    a.set_defaults(gl=gl_abeceda)
    i = sub.add_parser("izmeri", help="vrstice · znaki · bajti · ⟨md5⟩ ∧ ⟨sha256⟩ — pečatna izmera")
    i.add_argument("datoteke", nargs="*")
    i.add_argument("--polno", action="store_true", help="celi hasji — dokaz, ne izsek ⊢")
    i.set_defaults(gl=gl_izmeri)
    d = sub.add_parser("isto", help="bajt-isto ⇌ primerjava dveh teles, zgodnji izhod")
    d.add_argument("a")
    d.add_argument("b")
    d.set_defaults(gl=gl_isto)
    c = sub.add_parser("pecat", help="1 + najvišja izmerjena ⊢ Z-2 — naslednji pečat")
    c.add_argument("datoteke", nargs="*")
    c.add_argument("--vrzeli", nargs="?", type=int, const=1000, default=None,
                   help="izpiši manjkajoče pečate (vrzeli); vrednost = spodnja meja ( privzeto 1000 )")
    c.set_defaults(gl=gl_pecat)
    s = sub.add_parser("sha", help="⟨sha⟩ instrument: sha1 ∧ git-blob oblika telesa ⊢")
    s.add_argument("datoteke", nargs="*")
    s.set_defaults(gl=gl_sha)
    rp = sub.add_parser("rep", help="LOKAL ⇌ ⟨main⟩: ⟨blob⟩ diska ⇌ blob repa — bajt-isto ⊢")
    rp.add_argument("datoteke", nargs="*")
    rp.set_defaults(gl=gl_rep)
    vr = sub.add_parser("vrata", help="preverjanja na koncih: hišna vrata localhost ( ŽIVA ∧ / MRTVA × ) ⊙")
    vr.add_argument("imena", nargs="*")
    vr.set_defaults(gl=gl_vrata)
    pr = sub.add_parser("predlog", help="KOGA ∧ KAJ ( §0.17 × 10² ): predlogi iz izmere ⊙ ⟨ne-ugibaj⟩")
    pr.set_defaults(gl=gl_predlog)
    va = sub.add_parser("varuh", help="VARUH STROJA #12: GPU > 85 °C ali disk > 95 % → USTAVI ⊙")
    va.set_defaults(gl=gl_varuh)
    na = sub.add_parser("nasprotje", help="⟨NASPROTNA-TEHTNICA⟩ §0.18: telo na obeh koritih ( podpora ⊥ dvom ) ⊙")
    na.add_argument("datoteke", nargs="*")
    na.set_defaults(gl=gl_nasprotje)
    rz = sub.add_parser("rezerviraj", help="⟨REZERVACIJA-REZA⟩ ⟨IDEJA-K⟩: kolizija se preprečuje, ⟨ne⟩ odkriva ⊙")
    rz.add_argument("ime", nargs="?", default="sedež")
    rz.add_argument("--sprosti", action="store_true", help="rezervacija za trenutni vrh odpuščena ⊢")
    rz.set_defaults(gl=gl_rezerviraj)
    st = sub.add_parser("struktura", help="⟨PRICA-SODELOVANJA⟩ ⟨IDEJA-M⟩: ZADNJI ×1 ∧ noben pečat čez ⊙")
    st.add_argument("datoteke", nargs="*")
    st.set_defaults(gl=gl_struktura)
    tl = sub.add_parser("telo", help="⟨IZMERA-VSEH-TELES⟩: izmera Σ ∧ nasprotje Σ ∧ struktura Σ celih organov ⊙ pravilo 7")
    tl.add_argument("datoteke", nargs="*")
    tl.set_defaults(gl=gl_telo)
    rg = sub.add_parser("register", help="⟨POGLABLJANJE-V-ENOTNE-REGISTRE⟩: globoko branje teles → REGISTER-TELES.jsonl ⊙")
    rg.add_argument("datoteke", nargs="*")
    rg.add_argument("--izhod", nargs="?", default=None, help="pot registra ( privzeto: REGISTER-TELES.jsonl )")
    rg.add_argument("--vse", action="store_true", help="DEFRAGMENTACIJA: vsako telo pod organi/ v enoten register z vrsto ⊙")
    rg.set_defaults(gl=gl_register, vse=False)
    pp = sub.add_parser("popis", help="popis teles po korenu: izmera vsakega + Σ ∧ dvojniki ⚠")
    pp.add_argument("koren", nargs="?", default="organi")
    pp.set_defaults(gl=gl_popis)
    sp = sub.add_parser("speči", help="organi po zadnjem žigu, najstarejši prvi — resinteza ⚔ ⟡")
    sp.add_argument("koliko", nargs="?", type=int)
    sp.set_defaults(gl=gl_speči)
    pu = sub.add_parser("pulz", help="berba lastnega pulza: zadnji dihi ∧ dih manjka ⚠")
    pu.add_argument("koliko", nargs="?", type=int, default=5)
    pu.set_defaults(gl=gl_pulz)
    r = sub.add_parser("rez", help="geniza rez telesa po celih vrsticah ( frag-NN: vrstice · B · ⟨md5⟩ )")
    r.add_argument("datoteka")
    r.add_argument("velikost", nargs="?", type=int, default=100000)
    r.set_defaults(gl=gl_rez)
    v = sub.add_parser("prevoz", help="RED PREVOZA v enem dihu: izmeri obeh -> isto -> pečat ⊢")
    v.add_argument("lokal")
    v.add_argument("zrcalo")
    v.set_defaults(gl=gl_prevoz)
    z = sub.add_parser("združi", help="inverz fragmentacije: 0.1050 × 10⁴ -> 1050")
    z.add_argument("datoteke", nargs="*")
    z.set_defaults(gl=gl_združi)
    t = sub.add_parser("test", help="⟨druga-roka⟩: samopreverba")
    t.set_defaults(gl=gl_test)
    args = p.parse_args()
    sys.stdout.reconfigure(newline="")            # prelomi potujejo nespremenjeni — bajt-isto ⊢
    sys.stdin.reconfigure(newline="")
    try:
        args.gl(args)
        poročilo()
    except BrokenPipeError:
        poročilo("zgodnji izhod ( pipe ) ⊙")


if __name__ == "__main__":
    main()
