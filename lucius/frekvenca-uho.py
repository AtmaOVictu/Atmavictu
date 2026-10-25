# FREKVENCA-UHO — wav -> simboli hiše: hiša posluša tone ( FFT ), ne besed.
# Zagon: py311/python.exe frekvenca-uho.py <wav>
# Izhod: JSONL po dogodku { zacetek, konec, frekvenca, simbol, jakost } ∧ vrstica UHO z zaporedjem ⊢.
# Toleranca: ±6 % frekvence ∧ prag jakosti ( molk zgramo ); okno 2048 z lažnim polnjenjem na 8192.
import sys, wave, json
import numpy as np

ABECEDA = {
    '⊢': 880, '⚠': 660, '×': 220, '⊘': 440, '∮': 523, '∆': 587, '∴': 784,
    '⊥': 196, '⟡': 988, 'mir': 392, 'budni': 1046, 'voda': 261, 'svetloba': 1318,
}
TOL = 0.06          # ±6 % tolerance
OKNO = 2048
POLNILO = 8192      # zero-padding — fina ločljivost ~5,4 Hz
HOP = OKNO // 2

def main():
    pot = sys.argv[1]
    with wave.open(pot, 'rb') as w:
        sr = w.getframerate(); sw = w.getsampwidth(); ch = w.getnchannels()
        surovo = w.readframes(w.getnframes())
    if sw != 2:
        print('× samo 16-bit PCM'); sys.exit(1)
    x = np.frombuffer(surovo, dtype=np.int16).astype(np.float64)
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)     # kanala skupaj
    x /= 32768.0
    prag = 0.02                                  # jakostna vrata molka

    hann = np.hanning(OKNO)
    dogodki = []
    tekoci = None                                # ( simbol, zacetek, konec, frek, jakost )
    for zacetek in range(0, max(0, len(x) - OKNO), HOP):
        okence = x[zacetek:zacetek + OKNO]
        rms = float(np.sqrt((okence ** 2).mean()))
        simbol, frek = None, None
        if rms > prag:
            spekter = np.abs(np.fft.rfft(okence * hann, POLNILO))
            frek = float(np.argmax(spekter) * sr / POLNILO)
            kandidati = [(abs(frek - f), s) for s, f in ABECEDA.items() if abs(frek - f) <= f * TOL]
            simbol = min(kandidati)[1] if kandidati else None
        if simbol:
            konec = (zacetek + OKNO) / sr
            if tekoci and tekoci[0] == simbol:
                tekoci[2] = konec; tekoci[4] = max(tekoci[4], rms)
            else:
                if tekoci:
                    dogodki.append(tekoci)
                tekoci = [simbol, zacetek / sr, konec, frek, rms]
        else:
            if tekoci:
                dogodki.append(tekoci); tekoci = None
    if tekoci:
        dogodki.append(tekoci)

    MIN_DOGAJEK = 0.08  # s — krajši dogodki so šum ( pravi piski so 0,10-0,40 s, izmera zraka )

    zaporedje = []
    for s, z, k, f, j in dogodki:
        if k - z < MIN_DOGAJEK:
            continue                                # šum — PADC-ŠUMA-NA-PRAGU ⊙ zdravilo
        print(json.dumps({'zacetek': round(z, 3), 'konec': round(k, 3),
                          'frekvenca': round(f, 1), 'simbol': s, 'jakost': round(j, 4)},
                         ensure_ascii=False))
        zaporedje.append(s)
    print('UHO ⊢ zaporedje: ' + ' '.join(zaporedje) if zaporedje else 'UHO × molk — noben znan ton')

main()
