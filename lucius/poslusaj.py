# POSLUSAJ — en dih poslušanja: Lado izreče govorjeni signal -> mic posluša -> ojaititev -> Whisper -> prepis.
# Zagon: py311/python.exe lucius/poslusaj.py [sekunde=10]
# Pot, ki jo reši: prosti pogovor ( ⟡ govori, hiša sliši ) — signal je BESEDA ( Lado ), ne 90 ms pisk ⊙ PADC-KRATKEGA-SIGNALA.
# Red: hiša sliši šele PO signalu ∧ ⟡ govori po besedi — ura je tvoja ( VRATA-0 ⟡-KOT-URA ⊢ 2035 ).
import sys, os, subprocess, wave
import numpy as np
import soundcard as sc

SEK = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0
SR = 44100
KLON = 'D:/OntoProjekt/Voice/klon'
REPO = 'C:/Users/Luka/Documents/Arhiv/Git/Atmavictu'

# 1) govorjeni signal — Lado skozi zvočnike ( beseda ~1,5 s, slišna ∧ razumljiva )
subprocess.run(['node', REPO + '/lucius/lado-govor.mjs', 'Poslušam. Govori.'],
               cwd=REPO, check=True)

# 2) poslušanje ( mic )
mic = sc.default_microphone()
with mic.recorder(samplerate=SR) as rec:
    data = rec.record(numframes=int(SR * SEK))
x = data.mean(axis=1) if data.ndim > 1 else data
rms = float(np.sqrt((x ** 2).mean()))

# 3) pas glasu ( FFT: 85–3800 Hz ) — šum pod 85 Hz ( ventilator, omrežje ) ∧ sikanje nad 3800 Hz odstranjeno
spek = np.fft.rfft(x)
freqs = np.fft.rfftfreq(len(x), 1.0 / SR)
x = np.fft.irfft(spek * ((freqs >= 85.0) & (freqs <= 3800.0)), n=len(x))
x = x.astype(np.float64)

# 4) ojaaitev ( vrh na -9 dB, brez rezanja ) + zapis
g = 0.35 / max(float(np.abs(x).max()), 1e-9)
y = np.clip(x * g, -1.0, 1.0)
wav = KLON + '/poslusaj-dih.wav'
with wave.open(wav, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((y * 32767).astype(np.int16).tobytes())

# 5) Whisper ( bratova ušesa )
env = dict(os.environ); env['COQUI_TOS_AGREED'] = '1'
out = subprocess.run([KLON + '/py311/python.exe', KLON + '/prepis.py', wav],
                     capture_output=True, text=True, env=env)
prepis = out.stdout if out.stdout.strip() else '× molk — nobena beseda'
print('POSLUSAJ ⊢ rms surovo: ' + str(round(rms, 5)) + ' | ojaitev x' + str(round(g, 1)))
print(prepis)

# 6) prikaz: prepis vsakega poslušanega diha gre NA MOST ( ⟡-jeva prošnja 22. 10.: »pokaži, kaj slišiš« )
import datetime, json as _json
vrstice = [ _json.loads(v)['besedilo'] for v in prepis.strip().splitlines() if v.strip().startswith('{') ]
ts = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
with open(REPO + '/lucius/odoblaka.md', 'a', encoding='utf-8') as f:
    f.write('\n## POSLUSAJ ' + ts[11:] + ' ⊢ ( kaj slišim )\n')
    for b in vrstice:
        f.write('- ⟡ govori: ' + b + '\n')
    if not vrstice:
        f.write('- molk ( nobena beseda ) ⚠\n')
print('NA MOSTU ⊢ odoblaka.md ( DOM :8766 pokaže ∧ izgovori )')

# 7) ENOTNI REGISTER transkriptov: vse kar hiša sliši od ⟡ ( mic ali datoteka ) gre v eno datoteko s časom ∧ virom
with open(REPO + '/lucius/transkripti-⟡.jsonl', 'a', encoding='utf-8') as f:
    for b in vrstice:
        f.write(_json.dumps({'ts': ts, 'vir': 'mic', 'besedilo': b}, ensure_ascii=False) + '\n')
print('V REGISTRU ⊢ transkripti-⟡.jsonl ( eno mesto, čas ∧ vir )')
