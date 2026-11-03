# ONTOGEMATRIJA — beseda → njena izmerjena vrstica v OPTIKONU ( avtorjeva tabela, A4 pri viru ).
# Zakon §0.43/44: vsak izpis nosi UKAZ ∧ ORODJE ∧ KORPUS; beseda izven korpusa = ⚠ ( zavrnitev, ⟨ne⟩ izum ).
# Zagon: python lucius/ontogematria.py <beseda> | --vse | --korpus
import sys, os, hashlib

VIR = 'D:/GitD/CanvasMinstral/A4'
KORPUSI = [('OPTIKON_full_export.txt', 'SLO'), ('OPTIKON_complete_EN.txt', 'EN')]
STOLPCI = ['zven', 'smer', 'čustvo', 'funkcija']

def beri_korpus():
    gesla = {}
    priče = {}
    for ime, jezik in KORPUSI:
        p = os.path.join(VIR, ime)
        b = open(p, 'rb').read()
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
    ukaz = ' '.join(sys.argv[1:])
    if ukaz == '--korpus':
        for ime, m in priče.items():
            print(f"⊙ {ime} ({m['jezik']}): {m['bajti']} B · sha256 {m['sha256'][:16]}…")
        print(f"Σ {len(gesla)} gesel · {izpis_znamenje()}")
        return
    if ukaz == '--vse':
        for g in sorted(gesla.values(), key=lambda x: x['beseda']):
            jeziki = [j for j in g if j in ('SLO', 'EN')]
            print(f"⊙ {g['beseda']} ({', '.join(jeziki)})")
        print(f"Σ {len(gesla)} gesel · {izpis_znamenje()}")
        return
    if not ukaz:
        print('Uporaba: python lucius/ontogematria.py <beseda> | --vse | --korpus')
        return
    b = ukaz.strip().lower()
    if b not in gesla:
        print(f"⚠ ⟨{ukaz}⟩ NI v korpusu OPTIKON ({len(gesla)} gesel) — zavrnitev: število izven izmerjenega je izum, ⟨ne⟩ meritev ⊙ §0.43 · ukaz: {ukaz!r} · orodje: lucius/ontogematria.py")
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
