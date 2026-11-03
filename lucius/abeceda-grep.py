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
    """Izmera enega telesa tokovno: ( vrstice, znaki, bajti, ⟨md5⟩ cel ) ⊢."""
    h = hashlib.md5()
    dec = codecs.getincrementaldecoder("utf-8")(errors="replace")
    vrstice = znaki = bajti = 0
    with _bajtni_tok(pot) as f:
        while True:
            kos = f.read(65536)
            if not kos:
                break
            bajti += len(kos)
            h.update(kos)
            vrstice += kos.count(b"\n")
            znaki += len(dec.decode(kos))
    znaki += len(dec.decode(b"", True))
    return vrstice, znaki, bajti, h.hexdigest()


def gl_izmeri(args):
    """Pečatna izmera telesa: vrstice · znaki · bajti · ⟨md5⟩ — en pregon, tokovno ⊢."""
    for pot in args.datoteke:
        vrstice, znaki, bajti, md5 = _izmeri_pot(pot)
        mera("vrstice", vrstice)
        print(f"{pot}: vrstice {hišna(vrstice)} · znaki {hišna(znaki)} · bajti {hišna(bajti)} B · ⟨md5⟩ {md5[:8]}")


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


def _najvecji_pecat(poti):
    """( najvišja, priča, priče, množica ) — tokovno; ⟨⟩-imena niso priče ⊙."""
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
    return najvišja, priča, priče, množica


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
        vrstice, znaki, bajti, md5 = _izmeri_pot(pot)
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
                           capture_output=True, text=True)
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


def gl_popis(args):
    """Popis teles po korenu: vsako telo z izmero + Σ; ⟨md5⟩ veže dvojnike na dan ⚠ ( brisanje prepovedano ⊙ )."""
    import glob
    poti = sorted(glob.glob(f"{args.koren}/**/*.md", recursive=True))
    if not poti:
        raise SystemExit(f"popis: nobeno telo pod {args.koren} ⊙")
    telesa = vrstice_skupaj = bajti_skupaj = 0
    po_md5 = {}
    for pot in poti:
        vrstice, _, bajti, md5 = _izmeri_pot(pot)
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
    skupaj = len(PRIMERI) + len(ZDRUŽI_PRIMERI) + len(fips)
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
    print(f"\nPREVERBA: {skupaj - padci}/{skupaj} ∧" + (f" · {padci} ×" if padci else " ⊢ VSE"))
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
    i = sub.add_parser("izmeri", help="vrstice · znaki · bajti · ⟨md5⟩ — pečatna izmera")
    i.add_argument("datoteke", nargs="*")
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
