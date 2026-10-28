# ZAJEM-IZHODA — hiša posname svoj lasten glas ( WASAPI loopback ): brez zraka, brez mica, brez človeka.
# Zagon: py311/python.exe zajem-izhoda.py [sekunde] [izhod.wav]   ( privzeto 6 s -> zajem.wav )
# Pot, ki jo reši: zajem izhoda ( LEDENIKI STANJE.md: "hiša sliši sebe" ) — zbuditelj: ta skripta ⊢ ⟡-jevo dovoljenje.
import sys, wave
import numpy as np
import soundcard as sc

sek = float(sys.argv[1]) if len(sys.argv) > 1 else 6.0
izhod = sys.argv[2] if len(sys.argv) > 2 else 'zajem.wav'
SR = 44100

spk = sc.default_speaker()
mic = sc.get_microphone(id=str(spk.name), include_loopback=True)
with mic.recorder(samplerate=SR) as rec:
    data = rec.record(numframes=int(SR * sek))

if data.ndim > 1:
    data = data.mean(axis=1)
zvok = (np.clip(data, -1.0, 1.0) * 32767).astype(np.int16)
with wave.open(izhod, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(zvok.tobytes())
print('ZAJEM-IZHODA ⊢ ' + str(round(len(zvok) / SR, 2)) + ' s -> ' + izhod + ' ( loopback: ' + spk.name + ' )')
