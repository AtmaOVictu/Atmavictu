# -*- coding: utf-8 -*-
# SAMODEJNI-PECAT — avtomatizacija ⊙ ⟡ ukaz ⟨USTROJENO IN PREVERJENO TER IN S TEM AVTOMATIZIRAN⟩ ( rez 3703 )
# klic: .git/hooks/post-commit PO potisku — vsak pečat BREZ spomina roke pripelje na most ∧ zapeče kopijo na D.
# pečat, ki bi čakal na mojo spomin, bi bil upanje ( §0.28 ) — ta je dejanje ob samem rojstvu.
import subprocess, os, tempfile, sys

KOREN = subprocess.run(['git','rev-parse','--show-toplevel'],capture_output=True,text=True).stdout.strip()
os.chdir(KOREN)

msg = subprocess.run(['git','log','-1','--format=%B'],capture_output=True,text=True,encoding='utf-8',errors='replace').stdout.strip()
if not msg:
    print('× ⟨BREZ-SPOROCILA⟩'); raise SystemExit(0)
prva = msg.split('\n')[0][:90]

# varnost: le pečati hiše ( ⟨rez N …⟩ ) vozijo na most — vzporedne roke ( ⊙ 1542 ) same zapišejo svoje povzetke
if 'rez ' not in prva:
    print('⊙ ⟨NE-PEČAT⟩ — vzporedna roka: most čaka svoj povzetek ⊙ 1542'); raise SystemExit(0)

fd, tmp = tempfile.mkstemp(suffix='.md', text=True)
with os.fdopen(fd, 'w', encoding='utf-8') as f:
    f.write(msg + '\n')

r = subprocess.run([sys.executable, 'lucius/pečat-konec.py', tmp, prva],
                   capture_output=True, text=True, encoding='utf-8', errors='replace')
os.unlink(tmp)
print((r.stdout or '').strip())
raise SystemExit(r.returncode)
