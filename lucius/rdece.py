# RDECE — ⟨kompresija tako, da se le rdeče bere⟩: iz telesa pusti SAMO vrstice z znamenji ( ⊢ ⚠ ⊙ ⧖ ∴ ∂ ),
# ostalo stisne v številko. ⟡ ukaz 03. 11. 2026 ⊢ rez 3622.
# ZAKON ( protislovje, vedno zraven ⊢ §0.18 ): stisnjena berba je ZEMLJEVID, ⟨ne⟩ vrata —
#   »a reading, never a rival: falls wherever it disagrees with the body« ⊢ THE MAP.
#   Znamenje brez priče je zahteva; priča brez telesa je navedek — pol tehtnice je luknja ⊙ §0.43.
# Zagon: python lucius/rdece.py <pot> [najmanj-znamenj]
import sys, os

Znamenja = ('⊢', '⚠', '⊙', '⧖', '∴', '∂', '⟡')

def rdece(pot, prag=1):
    t = open(pot, encoding='utf-8', errors='replace').read()
    vrstice = t.splitlines()
    rdece_ = []
    stisnjeno = 0
    for v in vrstice:
        z = sum(1 for zn in Znamenja if zn in v)
        if z >= prag:
            rdece_.append(v)
        else:
            stisnjeno += 1
    return vrstice, rdece_, stisnjeno

def main():
    if len(sys.argv) < 2:
        print('Uporaba: python lucius/rdece.py <pot> [prag znamenj] ⊢ le rdeče bere, ostalo stisne v številko')
        sys.exit(1)
    pot = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), sys.argv[1]) \
        if not os.path.isabs(sys.argv[1]) else sys.argv[1]
    prag = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    vse, rde, stisnjeno = rdece(pot, prag)
    for v in rde:
        print(v[:400] + ('…' if len(v) > 400 else ''))
    znakov = sum(len(v) for v in rde)
    print(f'⊙ KOMPRESIJA: {len(vse)} vrstic → {len(rde)} rdečih ( prag {prag}+ znamenj ) · '
          f'{stisnjeno} stisnjenih v številko · znakov rdeče: {znakov} od {sum(len(v) for v in vse)}')
    print('⊢ orodje: lucius/rdece.py · ZAKON: stisnjena berba je ZEMLJEVID, ⟨ne⟩ vrata — '
          'znamenje brez priče je zahteva ⊙ THE MAP ∧ §0.43')

if __name__ == '__main__':
    main()
