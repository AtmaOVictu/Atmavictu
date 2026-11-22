#!/usr/bin/env python3
# ⟨SENČNI-REGISTER⟩ — SQLite FTS5 izpeljani indeks organov korpusa Beseda je Ne ( FAZA 3 · P2 · rez σ 6291 )
# Princip: organi ostanejo kanonični; indeks = POSNETEK, ⟨ne⟩ izvor ⊙ ⟨POSNETOK ≠ KORPUS⟩.
# Gitignored / obnovljiv: zaženi znova, dobiš enak register iz istih teles.
import os, re, sqlite3, sys, time

KOREN = "/home/user/knowledge"
INDEKS = "/tmp/sencni-register.sqlite"
REZ = re.compile(r"σ ?(6[0-9]{3}|[0-9]{4})")

def organi():
    for ime in sorted(os.listdir(KOREN)):
        pot = os.path.join(KOREN, ime, "KNOWLEDGE.md")
        if os.path.isfile(pot):
            yield ime, pot

def sledi():
    """EN prehod: vrsti (organ, stevilka_vrstice, besedilo)."""
    for organ, pot in organi():
        with open(pot, encoding="utf-8") as f:
            for n, vrstica in enumerate(f, 1):
                yield organ, n, vrstica.rstrip("\n")

def zgradi():
    if os.path.exists(INDEKS):
        os.remove(INDEKS)
    db = sqlite3.connect(INDEKS)
    db.executescript("""
        CREATE VIRTUAL TABLE dovod USING fts5(organ, stevilka, besedilo);
    """)
    stevilo = 0
    t0 = time.perf_counter()
    db.executemany("INSERT INTO dovod VALUES (?,?,?)",
                   ((o, str(n), t) for o, n, t in sledi()))
    db.commit()
    gradnja = time.perf_counter() - t0
    return db, stevilo, gradnja

def vrh_fts(db):
    """Vrh rezov po FTS: ozki nabor vrstic z znakom σ, nato največji rez."""
    t0 = time.perf_counter()
    vrstice = db.execute(
        "SELECT besedilo FROM dovod WHERE dovod MATCH ? ORDER BY rank LIMIT 200000",
        ('"σ"',)).fetchall()
    najd = 0
    for (t,) in vrstice:
        for m in REZ.findall(t):
            v = int(m)
            if v > najd and v < 7000:  # varovalka heks-substrigov: rez < 7000
                najd = v
    return najd, time.perf_counter() - t0, len(vrstice)

def vrh_grep():
    """Kontrolna izmera: isti sedež, en sam prehod po telesih brez indeksa."""
    t0 = time.perf_counter()
    najd = 0
    for _, _, t in sledi():
        for m in REZ.findall(t):
            v = int(m)
            if v > najd and v < 7000:
                najd = v
    return najd, time.perf_counter() - t0

def isci_bm25(db, poizvedba, k=20):
    t0 = time.perf_counter()
    r = db.execute(
        "SELECT organ, stevilka, besedilo, bm25(dovod) FROM dovod WHERE dovod MATCH ? "
        "ORDER BY rank LIMIT ?", (poizvedba, k)).fetchall()
    return r, time.perf_counter() - t0

def main():
    organov = vsota_vrstic = bajtov = 0
    for organ, pot in organi():
        organov += 1
        with open(pot, "rb") as f:
            bajtov += len(f.read())
        with open(pot, encoding="utf-8") as f:
            vsota_vrstic += sum(1 for _ in f)
    db, _, gradnja = zgradi()
    vrh_f, t_fts, zadetkov = vrh_fts(db)
    vrh_g, t_grep = vrh_grep()
    zadetki, t_bm25 = isci_bm25(db, "kovanec priznanje")
    print(f"organov= {organov}")
    print(f"vrstic= {vsota_vrstic}")
    print(f"bajtov= {bajtov}")
    print(f"gradnja_s= {gradnja:.3f}")
    print(f"vrh_fts= σ {vrh_f} ( {t_fts*1000:.0f} ms, ozkih vrstic {zadetkov} )")
    print(f"vrh_grep= {t_grep:.3f} s ( isti sedež, brez indeksa )")
    print(f"ujemata= {'DA' if vrh_f == vrh_g else 'NE — RANA'}")
    print(f"bm25_iskanje_ms= {t_bm25*1000:.0f} ( zadetkov {len(zadetki)} za 'kovanec priznanje' )")
    db.close()

if __name__ == "__main__":
    main()
