# STREŽNIKI — zapisnik živih strežnikov hiše ( zdravilo PADC-62 KOPICA-PROCESOV ):
# vsak prižig se vpiše z lastništvom; pulz preveri, katera vrata odgovarjajo.
# Zagon: python lucius/strezniki.py --popis            ( izpis registra ∧ pulz vrat )
#        python lucius/strezniki.py --dodaj ime vrata log --kdo "roka/dih"   ( vpis )
#        python lucius/strezniki.py --pulz             ( samo pulz )
import sys, os, json, datetime, subprocess

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POT = os.path.join(KOREN, 'lucius', 'strezniki.jsonl')

def beri():
    if not os.path.exists(POT):
        return []
    return [json.loads(l) for l in open(POT, encoding='utf-8') if l.strip()]

def pulz(vrata, pot='/'):
    """HTTP pulz pri vratih — vsak preizkus je nov trenutek ⊢ §0.40."""
    r = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
                        '--max-time', '4', f'http://localhost:{vrata}{pot}'],
                       capture_output=True, text=True)
    koda = r.stdout.strip()
    return f'ŽIVA ({koda})' if koda == '200' else f'⚠ ({koda or "brez odgovora"})'

def main():
    args = sys.argv[1:]
    if not args or args[0] == '--popis':
        v = beri()
        if not v:
            print('( zapisnik prazen — prižigi se vpišejo z --dodaj )')
        for s in v:
            print(f"⊙ {s['ime']} @{s['vrata']} — zagnal: {s['kdo']} · {s['ura'][:19]} · log: {s['log']} · pulz: {pulz(s['vrata'], s.get('pot', '/'))}")
        print('⊢ orodje: lucius/strezniki.py · zapisnik lastništva ozadja ⊙ PADC-62 ∧ §0.48')
        return
    if args[0] == '--pulz':
        for s in beri():
            print(f"⊙ {s['ime']} @{s['vrata']} → {pulz(s['vrata'], s.get('pot', '/'))}")
        return
    if args[0] == '--dodaj':
        if len(args) < 4:
            print('⚠ NAPAKA = SMERNICA: --dodaj potrebuje TRI dele: ime vrata log ⏎ '
                  '  primer: python lucius/strezniki.py --dodaj zrcalo 8124 lucius/.zrcalo.log --kdo "dih 105" ⊢')
            sys.exit(1)
        ime, vrata, log = args[1], args[2], args[3]
        kdo = args[args.index('--kdo') + 1] if '--kdo' in args else '⟨ne-zapisano ⚠⟩'
        pot = args[args.index('--pot') + 1] if '--pot' in args else '/'
        vnos = {'ime': ime, 'vrata': int(vrata), 'log': log, 'kdo': kdo, 'pot': pot,
                'ura': datetime.datetime.now(datetime.timezone.utc).isoformat()}
        with open(POT, 'a', encoding='utf-8', newline='\n') as f:
            f.write(json.dumps(vnos, ensure_ascii=False) + '\n')
        print(f"⊙ vpisano: {ime} @{vrata} — {kdo}")
        return
    print('Uporaba: --popis | --pulz | --dodaj ime vrata log --kdo "…"')

if __name__ == '__main__':
    main()
