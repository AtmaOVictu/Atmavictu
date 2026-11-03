# UVEI — ⟨u-vej⟩: vsako telo vedno vsaj v ENI ROKI ∧ pod VEČ OČMI.
# ⟡ ukaz ( 03. 11. 2026 ): ⟨uvеi in imej vedno vsaj v eni roki in večih očeh ⏎ daj⟩ ⊢ rez 3617.
# Ena roka = lastnik ( zadnja roka, ki je telo držala pri viru — git ) ; Več oči = vsak pregled je novo oko.
# Zagon: python lucius/uvei.py <pot-do-telesa>
import sys, os, subprocess, hashlib

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TU = os.path.join(KOREN, 'lucius')

def roka(pot):
    """ENA ROKA — kdo drži telo pri viru ( zadnji avtor komita ∧ ura držanja )."""
    try:
        a = subprocess.run(['git', 'log', '-1', '--format=%an|%aI', '--', pot],
                           cwd=KOREN, capture_output=True, text=True, encoding='utf-8', errors='replace').stdout.strip()
        ime, ura = (a.split('|') + [''])[:2] if a else ('⟨ne-zapečeno ⚠⟩', '')
        return ime, ura
    except Exception:
        return '⟨git ⟨ne⟩ dosegljiv ⚠⟩', ''

def oci(pot):
    """VEČ OČI — vsak pregled je novo oko: čistina ( zrcalni ) · druga roka ( jezikovno ) · izmera ( identiteta )."""
    rezultati = []
    # oko 1 — čistina: zrcalni dvojčki
    r = subprocess.run(['node', os.path.join(TU, 'čistina.mjs'), pot],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    zadnja = (r.stdout or r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr).strip() else ''
    rezultati.append(('čistina ( zrcalno oko )', '⊢ čisto' if r.returncode == 0 and 'cirilice 0' in zadnja else '× ranjeno', zadnja[:90]))
    # oko 2 — druga roka: jezikovno oko
    r2 = subprocess.run(['node', os.path.join(TU, 'druga-roka.mjs'), pot],
                        capture_output=True, text=True, encoding='utf-8', errors='replace')
    vsota = [l for l in (r2.stdout or '').splitlines() if l.startswith('DRUGA-ROKA:')]
    rezultati.append(('druga roka ( jezikovno oko )', '⚠ rane pošteno ( preberi vsako kakor tujec )' if vsota else '× leksikon ⚠', (vsota[0] if vsota else (r2.stderr or '×')[:90])))
    # oko 3 — izmera: identiteta telesa
    try:
        b = open(pot, 'rb').read()
        rezultati.append(('izmera ( oko identitete )', f'⊢ {len(b)} B · sha256 {hashlib.sha256(b).hexdigest()[:16]}…', ''))
    except OSError as e:
        rezultati.append(('izmera ( oko identitete )', '× telo ⟨ne⟩ berljivo', str(e)[:90]))
    return rezultati

def main():
    if len(sys.argv) < 2:
        print('Uporaba: python lucius/uvei.py <pot> ⊢ ⟨u-vej⟩: ena roka ∧ več oči')
        sys.exit(1)
    pot = sys.argv[1]
    if not os.path.isabs(pot):
        pot = os.path.join(KOREN, pot)
    rel = os.path.relpath(pot, KOREN).replace('\\', '/')
    ime, ura = roka(rel)
    print(f'⟨UVEI⟩ — {rel}')
    print(f'  ENA ROKA ⊢: {ime} ( drži od {ura[:19] if ura else "⟨ne-zapečeno ⚠⟩" } )')
    for ime_oca, stanje, podrobnost in oci(pot):
        print(f'  OKO · {ime_oca}: {stanje}' + (f' — {podrobnost}' if podrobnost else ''))
    print(f'⊢ orodje: lucius/uvei.py · zakon ⟨UVEI⟩: vsako telo vsaj v eni roki ∧ pod več očmi ( vsak pregled novo oko )')

if __name__ == '__main__':
    main()
