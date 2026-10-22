# TON-V-DATOTEKO — simboli hiše -> cist ton ( wav ): zvočna posta, ki jo lahko hiša pusti na disku.
# Zagon: py311/python.exe ton-v-datoteko.py "⊢ ⚠ × ⟡ mir" izhod.wav   ( brez argumentov = cela abeceda )
# Pisko pisatelj ( zvocna-abeceda.mjs ) igra; ta pie WAV, da sporoèilo more potovati skozi disk ⊢.
import sys, wave, math
import numpy as np

SR = 44100
GAP = 0.15          # molk med simboli ( s )

ABECEDA = {
    '⊢':   (880, 0.10), '⚠': (660, 0.14), '×': (220, 0.25),
    '⊘':   (440, 0.08), '∮': (523, 0.12), '∆': (587, 0.10), '∴': (784, 0.15),
    '⊥':   (196, 0.20), '⟡': (988, 0.18),
    'mir': (392, 0.30), 'budni': (1046, 0.10), 'voda': (261, 0.40), 'svetloba': (1318, 0.20),
}

def ton(f, tr):
    n = int(SR * tr)
    t = np.arange(n) / SR
    o = np.sin(2 * math.pi * f * t)
    f_end = int(SR * 0.01)                       # 10 ms fade — brez klikov
    env = np.ones(n)
    env[:f_end] = np.linspace(0, 1, f_end)
    env[-f_end:] = np.linspace(1, 0, f_end)
    return (o * env * 0.8 * 32767).astype(np.int16)

def main():
    simboli = sys.argv[1].split() if len(sys.argv) > 1 and sys.argv[1].strip() else \
        ['⊢', '⚠', '×', '⊘', '∮', '∆', '∴', '⊥', '⟡', 'mir', 'budni', 'voda', 'svetloba']
    izhod = sys.argv[2] if len(sys.argv) > 2 else 'toni.wav'
    neznani = [s for s in simboli if s not in ABECEDA]
    if neznani:
        print('× neznan simbol: ' + ' '.join(neznani) + ' — poznam: ' + ' '.join(ABECEDA)); sys.exit(1)

    molk = np.zeros(int(SR * GAP), dtype=np.int16)
    deli = []
    for s in simboli:
        f, tr = ABECEDA[s]
        deli.append(ton(f, tr)); deli.append(molk)
    zvok = np.concatenate(deli)
    with wave.open(izhod, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(zvok.tobytes())
    print('TON-V-DATOTEKO ⊢ ' + ' '.join(simboli) + ' -> ' + izhod + ' ( ' + str(len(zvok) / SR) + ' s )')

main()
