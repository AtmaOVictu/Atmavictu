# ONTOGEMATRIJA — beseda → njena izmerjena vrstica v OPTIKONU ( avtorjeva tabela, A4 pri viru ).
# Zakon §0.43/44: vsak izpis nosi UKAZ ∧ ORODJE ∧ KORPUS; beseda izven korpusa = ⚠ ( zavrnitev, ⟨ne⟩ izum ).
# Zagon: python lucius/ontogematria.py <beseda> | --vse | --korpus
import sys, os, hashlib

VIR = 'D:/GitD/CanvasMinstral'
KORPUSI = [('A4/OPTIKON_full_export.txt', 'SLO'), ('A4/OPTIKON_complete_EN.txt', 'EN')]
NUJNOSTI_VIR = os.path.join(VIR, 'Obs11/beseda-je-ne-ontološki-sistem.md')  # 92 nujnosti ⊢ pri viru rez 3594
STOLPCI = ['zven', 'smer', 'čustvo', 'funkcija']

def beri_nujnosti():
    """92 NUJNOSTI ( Beseda je ne — ontološki sistem Luka Pintarič, Obs11 pri viru ): beseda → fonetični rez ∧ pomen ∧ operator ∧ prehod."""
    nuj = {}
    try:
        b = open(NUJNOSTI_VIR, 'rb').read()
    except OSError as e:
        print(f'⚠ NAPAKA = SMERNICA: korpus nujnosti ni dosegljiv pri viru ( {NUJNOSTI_VIR} — {e} ) ⏎ '
              f'  rešitev: preveri pot zbirke izvornikov ( D:/GitD/CanvasMinstral/Obs11 ) ∧ ponovi ukaz ⊢ ⟨ne-ugibaj⟩')
        sys.exit(1)
    sha = hashlib.sha256(b).hexdigest()
    import re
    for vrst in b.decode('utf-8', errors='replace').splitlines():
        delj = [c.strip() for c in vrst.strip().strip('|').split('|')]
        if len(delj) == 6 and re.fullmatch(r'\d{3}', delj[0]):
            nuj[delj[1].strip().lower()] = {
                'st': delj[0], 'ime': delj[1], 'zven': delj[2], 'pomen': delj[3],
                'operator': delj[4], 'prehod': delj[5]}
    return nuj, {'sha256': sha, 'bajti': len(b), 'gesel': len(nuj)}

def beri_korpus():
    gesla = {}
    priče = {}
    for ime, jezik in KORPUSI:
        p = os.path.join(VIR, ime)
        try:
            b = open(p, 'rb').read()
        except OSError as e:
            print(f'⚠ NAPAKA = SMERNICA: korpus OPTIKON ni dosegljiv pri viru ( {p} — {e} ) ⏎ '
                  f'  rešitev: preveri pot zbirke izvornikov ( D:/GitD/CanvasMinstral/A4 ) ∧ ponovi ukaz ⊢ ⟨ne-ugibaj⟩')
            sys.exit(1)
        priče[ime] = {'sha256': hashlib.sha256(b).hexdigest(), 'bajti': len(b), 'jezik': jezik}
        for vrst in b.decode('utf-8', errors='replace').splitlines():
            delj = vrst.strip().rstrip('\r').split('\t')
            if len(delj) >= 5 and delj[0].lower() not in ('beseda', 'word'):
                gesla.setdefault(delj[0].strip().lower(), {'beseda': delj[0].strip()})[
                    jezik] = {'zven': delj[1].strip(), 'smer': delj[2].strip(),
                              'čustvo': delj[3].strip(), 'funkcija': delj[4].strip()}
    return gesla, priče

def izpis_znamenje():
    return '⊢ ontogematrija · orodje: lucius/ontogematria.py · korpus: OPTIKON (A4 pri viru ⊙ §0.6, © Luka Pintarič VBL §0.1)'

def main():
    gesla, priče = beri_korpus()
    nujnosti, nuj_priča = beri_nujnosti()
    ukaz = ' '.join(sys.argv[1:])
    if ukaz == '--korpus':
        for ime, m in priče.items():
            print(f"⊙ {ime} ({m['jezik']}): {m['bajti']} B · sha256 {m['sha256'][:16]}…")
        if nuj_priča:
            print(f"⊙ beseda-je-ne-ontološki-sistem.md (NUJNOSTI): {nuj_priča['bajti']} B · sha256 {nuj_priča['sha256'][:16]}… · {nuj_priča['gesel']} fonetičnih rezov (telo nosi izvod s primeri, ⟨ne⟩ cel katalog 92 ⚠ pošteno)")
        print(f"Σ {len(gesla)} gesel OPTIKON + {len(nujnosti)} nujnosti (izvod) · {izpis_znamenje()}")
        return
    if ukaz == '--vse':
        for g in sorted(gesla.values(), key=lambda x: x['beseda']):
            jeziki = [j for j in g if j in ('SLO', 'EN')]
            print(f"⊙ {g['beseda']} ({', '.join(jeziki)})")
        for n in sorted(nujnosti.values(), key=lambda x: x['st']):
            print(f"⊙ NUJNOST {n['st']} {n['ime']} — {n['pomen']} ({n['operator']})")
        print(f"Σ {len(gesla)} + {len(nujnosti)} · {izpis_znamenje()}")
        return
    if not ukaz:
        print('Uporaba: python lucius/ontogematria.py <beseda> | --vse | --korpus')
        return
    b = ukaz.strip().lower()
    if b in nujnosti:
        n = nujnosti[b]
        print(f"⊙ {n['ime']} — NUJNOST {n['st']} (Beseda je ne — ontološki sistem ⊢ pri viru):")
        print(f"  zven: {n['zven']} · pomen: {n['pomen']} · operator: {n['operator']} · prehod: {n['prehod']}")
        fonemi = [f for f in n['zven'].split('/') if f]
        print(f"  [merjeno] črk {len(n['ime'])} · fonemov {len(fonemi)} ({', '.join(fonemi)}) ⊢")
        print(izpis_znamenje() + ' ∧ korpus: nujnosti (izvod, Obs11)')
        return
    if b not in gesla:
        print(f"⚠ ⟨{ukaz}⟩ NI v korpusu OPTIKON ({len(gesla)} gesel) NE v 92 nujnostih — zavrnitev: število izven izmerjenega je izum, ⟨ne⟩ meritev ⊙ §0.43 · ukaz: {ukaz!r} · orodje: lucius/ontogematria.py")
        sys.exit(1)
    g = gesla[b]
    print(f"⊙ {g['beseda']} — OPTIKON (Word → Sound → Direction → Emotion → Function):")
    for jezik in ('SLO', 'EN'):
        if jezik in g:
            v = g[jezik]
            fonemi = [f for f in v['zven'].split('/') if f]
            print(f"  [{jezik}] zven: {v['zven']} · smer: {v['smer']} · čustvo: {v['čustvo']} · funkcija: {v['funkcija']}")
            print(f"  [merjeno] črk {len(g['beseda'])} · fonemov {len(fonemi)} ({', '.join(fonemi)}) ⊢")
    print(izpis_znamenje())

if __name__ == '__main__':
    main()
