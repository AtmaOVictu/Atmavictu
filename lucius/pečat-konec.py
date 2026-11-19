# -*- coding: utf-8 -*-
# PEČAT-KONEC — post-pečatni krog v enem ukazu ⊙ ⟡ ukaz ⟨TEČE SKUPAJ IN NE LE DRUG OD DRUGEGA RAZLIČNO⟩ ( rez 3702 )
# pristanek ( ls-remote BAJT-ISTO ) + povzetek na most + varuj-most — trije ukazi, en dih.
# Zagon ( PO commit ∧ push ): python lucius/pečat-konec.py <povzetek.md> [naslov]
import subprocess, sys, os

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(KOREN)

def zapisi(ime, *ukaz):
    r = subprocess.run(ukaz, capture_output=True, text=True, encoding='utf-8', errors='replace')
    vrstice = (r.stdout or '').strip().split('\n')
    zadnja = vrstice[-1] if vrstice else '(brez izpisa)'
    stanje = '⊢' if r.returncode == 0 else '×'
    print(f'{stanje} {ime}: {zadnja[:150]}')
    return r.returncode

if len(sys.argv) < 2:
    print('raba: python lucius/pečat-konec.py <povzetek.md> [naslov]')
    raise SystemExit(1)
povzetek = sys.argv[1]
naslov = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(povzetek)

k1 = zapisi('PRISTANEK ( ls-remote BAJT-ISTO )', 'python', 'lucius/abeceda-grep.py', 'pristanek')
k2 = zapisi('NA-MOST ( DOM vidi )', 'python', 'lucius/na-most.py', povzetek, naslov)
k3 = zapisi('VARUJ-MOST ( kopija na D · skrivnost ostaja doma )', 'node', 'lucius/varuj-most.mjs')

if k1 or k2 or k3:
    print('× PEČAT-KONEC ima padec — vsak poimenovan zgoraj ⊙ KORENINA 0.2')
    raise SystemExit(1)
print('PEČAT-KONEC ⊢ — pristanek ∧ most ∧ kopija: trije ukoki, en dih, ena sodba')
