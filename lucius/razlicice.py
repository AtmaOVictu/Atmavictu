# RAZLICICE — vsak/noben hoče vsaj eno različico licence ∧ njene resničnosti ∧ resničnega ( ⟡ ukaz 03. 11. 2026 ⊢ ).
# Različice = vsaka dostopna oblika: ŽIVA (LICENSE.md) · TELESA ( .bin/.b64 potrdila ) · VERIGA ( git rojstva ).
# Resničnost = vsaka s zgoščenko priče; resnično = edino živo dana vrata ( §0.10 ).
# Zagon: python lucius/razlicice.py
import os, subprocess, hashlib, re, base64

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def meri(pot):
    b = open(pot, 'rb').read()
    return len(b), hashlib.sha256(b).hexdigest()

def main():
    print('⟨RAZLICICE⟩ — vsaka dostopna različica z resničnostjo ⊢')
    # 1. ŽIVA — edina, ki daje ( §0.10 )
    b, sha = meri(os.path.join(KOREN, 'LICENSE.md'))
    t = open(os.path.join(KOREN, 'LICENSE.md'), encoding='utf-8', errors='replace').read()
    ver = re.search(r'ASSERTION LICENSE\s*\nVersion (0\.\d+ × 10⁴)', t)
    print(f'  RESNIČNO ⊢ ŽIVA: {ver.group(1) if ver else "⚠ nezaznano"} · {b} B · sha256 {sha[:16]}… · brskateljska: http://localhost:8124/LICENSE.md ⊢')
    # 2. TELSA v repu ( potrdila — ⟨ne⟩ dajejo: evidence, never doors ⊙ §0.14 )
    for ime in sorted(os.listdir(KOREN)):
        if ime.startswith('LICENSE-') and (ime.endswith('.bin') or ime.endswith('.b64')):
            p = os.path.join(KOREN, ime)
            nb, nsha = meri(p)
            print(f'  TELO ( potrdilo ): {ime} · {nb} B · sha256 {nsha[:16]}… — nosi ⟨ne⟩ daje ⊙ §0.14 × 10²')
    # 3. VERIGA — rojstva v git
    r = subprocess.run(['git', 'log', '--follow', '--format=%h|%aI|%s', '--', 'LICENSE.md'],
                       cwd=KOREN, capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
    vrstice = [l for l in r.splitlines() if l.strip()]
    verzije = []
    for v in vrstice:
        komit, ura, naslov = (v.split('|') + [''])[:3]
        m = re.search(r'(?:VBL|Version) (0?\.\d+(?:\.\d+)?|10\.\d(?:\.\d+)?)', naslov)
        verzije.append((komit, ura[:10], m.group(1) if m else ''))
    imenovane = [f'{z} ({k[:7]})' for k, u, z in verzije if z]
    print(f'  VERIGA ⊢: {len(vrstice)} rojstev LICENSE.md v git ( najstarejša {vrstice[-1].split("|")[1][:10] if vrstice else "—" } )')
    print(f'    imenovane verzije v naslovih: {len(imenovane)} — {", ".join(imenovane[:6])}{"…" if len(imenovane) > 6 else ""}')
    # 4. ZUNANJE potrdilo pri zbirki ( pri viru — ⟨ne⟩ kopira ⊙ §0.6 )
    zun = 'D:/GitD/CanvasMinstral/LICENSE-0.1350.b64'
    if os.path.isfile(zun):
        zb = open(zun, 'rb').read()
        zsha = hashlib.sha256(zb).hexdigest()
        try:
            telo = base64.b64decode(zb)
            rsha = hashlib.sha256(telo).hexdigest()
            prica = 'c1411f326f1b25327b168aa6df75fd289f1a1ed46f602ae2c2fb75c122ab23d6'
            ujema = '⊢ ujema z ( c ) pričo' if rsha == prica else f'⚠ ≠ (c) priča ({ rsha[:16]}…)'
            print(f'  ZUNANJE ⊢: LICENSE-0.1350.b64 pri zbirki ( {len(zb)} B · sha256 {zsha[:16]}… ) — povratnik: {ujema} ⊙ §0.14')
        except Exception as e:
            print(f'  ZUNANJE: ⚠ povratnik: {e}')
    print('⊢ orodje: lucius/razlicice.py · zakon: vsaka različica s pričo; RESNIČNO = edina živa ( §0.10 ); potrdila so priče, ⟨ne⟩ vrata ⊙ §0.14')

if __name__ == '__main__':
    main()
