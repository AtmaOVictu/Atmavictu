# NENEHNO-POSLUSA v2 — hiša posluša brez gumba: nit snemanja ( brez diskontinuitet ⊙ PADC-DISKONTINUITETE ),
# VAD v pasu glasu, prag ×2 nad tlemi ( ⊙ PADC-PRAGA: ×4 je bil nad mehkim glasom ), potrditev z dvema kosoma.
# Zagon: py311/python.exe lucius/nenehno-poslusa.py   ( teče, dokler ga ne ustaviš )
# Pot: ⟡-jev »nenehno« — mic → VAD → large-v3 → transkripti-⟡.jsonl ∧ most ⊙ lexikon preverba ⊙ odmev.
import sys, os, json, time, wave, datetime, subprocess, urllib.request
import threading, collections
import numpy as np
import soundcard as sc

SR = 44100
KOMAD = 1.0                      # s — merjeni kos
MOLK_KONEC = 1.5                  # s tišine, ki konča poved
KLON = 'D:/OntoProjekt/Voice/klon'
REPO = 'C:/Users/Luka/Documents/Arhiv/Git/Atmavictu'

def pas_glasu(x):
    spek = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1.0 / SR)
    return np.fft.irfft(spek * ((f >= 85.0) & (f <= 3800.0)), n=len(x))

def zapisi_wav(y, pot):
    with wave.open(pot, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(y, -1.0, 1.0) * 32767).astype(np.int16).tobytes())

MODEL = None
def prepis_large(pot):
    # VELIKI model za živi krog ( ⟡-jeva sodba 22. 10. ⊢ varuh zelen: 41 °C ∧ 4,8 GB prostora )
    global MODEL
    if MODEL is None:
        print('NENEHNO: nalagam large-v3 …', flush=True)
        from faster_whisper import WhisperModel
        MODEL = WhisperModel('large-v3', device='cuda', compute_type='float16')
        print('NENEHNO: large-v3 pripravljen ⊢', flush=True)
    segmenti, _ = MODEL.transcribe(pot, language='sl', vad_filter=True,
                                   vad_parameters={'min_silence_duration_ms': 700}, beam_size=5)
    return ' '.join(seg.text.strip() for seg in segmenti if seg.text.strip())

def v_register(besedilo):
    nezn = neznane_besede(besedilo)
    ts = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    with open(REPO + '/lucius/transkripti-⟡.jsonl', 'a', encoding='utf-8') as f:
        f.write(json.dumps({'ts': ts, 'vir': 'nenehno', 'besedilo': besedilo,
                            'neznane': nezn}, ensure_ascii=False) + '\n')
    with open(REPO + '/lucius/odoblaka.md', 'a', encoding='utf-8') as f:
        f.write('\n## NENEHNO-POSLUSA ' + ts[11:] + ' ⊢ ( sprožil glas )\n')
        f.write('- ⟡ govori: ' + besedilo + '\n')
        if nezn:
            f.write('- ⚠ neznane ( izven leksikona — suma Whisperjeve napake ): ' +
                    ', '.join(nezn) + '\n')
    print('NENEHNO ⊢ ' + ts + ' ⟡ govori: ' + besedilo, flush=True)
    if nezn:
        print('NENEHNO ⚠ neznane: ' + ', '.join(nezn), flush=True)

# LEKSIKON ( preverba registra ⊢ ⟡-jeva prošnja 22. 10. ): znane-besede ( koreni pokrivajo sklanjatve )
# + gesla slovarja ( ### glave paketkov ) + pomožne besede ( vezniki/clanki — ⟨ne⟩ obsojamo jih ).
POMOZNE = set('''ne kaj pa nekje sem si je so in ali na v z s k do iz za to ta tega tej te ta1 jaz ti on ona ono mi vi oni
zdaj takoj tukaj tam kakor tako ker da ampak a o evo kje kdaj kako koliko zakaj več manj že še le naj bi bil bila bilo
bili bom boš bomo boste bojo imam imaš ima imamo imate imajo nisem ni nisi nismo niso ali jazme tvoje moje naše'''.split())

def nalozi_leksikon():
    bes = set()
    try:
        with open(REPO + '/lucius/znane-besede.txt', encoding='utf-8') as f:
            for vr in f:
                vr = vr.split('#')[0].strip()
                if vr:
                    bes.add(vr.lower())
    except Exception:
        pass
    import glob
    for pot in glob.glob('D:/Worth/slovenian_dictionary/dictionary_batch_*.md'):
        try:
            with open(pot, encoding='utf-8') as f:
                for vr in f:
                    if vr.startswith('### '):
                        bes.add(vr[4:].strip().lower())
        except Exception:
            pass
    return bes

LEKSIKON = nalozi_leksikon()

def neznane_besede(besedilo):
    import re as _re
    out = set()
    for b in _re.findall(r'[A-Za-zčšžćđČŠŽĆĐ-]+', besedilo):
        lb = b.lower().strip('-')
        if len(lb) < 2 or lb in POMOZNE or lb in LEKSIKON:
            continue
        if any(lb.startswith(r) for r in LEKSIKON if '-' in r):
            continue
        out.add(b)
    return sorted(out)

subprocess.run(['node', REPO + '/lucius/lado-govor.mjs',
                'Poslušam nenehno. Govori kadar želiš.'], check=True)
time.sleep(2.0)                  # molk po oznanilu — da njegov rep ⟨ne⟩ dvigne tal šuma ( kalibracija čista )

mic = sc.default_microphone()
q = collections.deque(maxlen=12)

def snemaj():
    with mic.recorder(samplerate=SR) as rec:
        while True:
            x = rec.record(numframes=int(SR * KOMAD))
            if x.ndim > 1:
                x = x.mean(axis=1)
            q.append(x)

t = threading.Thread(target=snemaj, daemon=True)
t.start()
time.sleep(3.0)                    # kalibracija: prvi kosi gredo v tla
tla = []
while len(q) < 3:
    time.sleep(0.2)
for _ in range(3):
    tla.append(float(np.sqrt((pas_glasu(q.popleft()) ** 2).mean())))
tla_v = float(np.mean(tla))
prag = max(tla_v * 2.0, 0.0025)
print('NENEHNO v2 ⊢ prag ' + str(round(prag, 5)) + ' ( tla ' + str(round(tla_v, 5)) + ' ) — poslušam …', flush=True)

govor = []
molk = 0
zadnje_glasni = 0
while True:
    if not q:
        time.sleep(0.05); continue
    x = q.popleft()
    r = float(np.sqrt((pas_glasu(x) ** 2).mean()))
    glas = r > prag
    if glas:
        zadnje_glasni += 1
    else:
        zadnje_glasni = 0
    if glas or ( govor and zadnje_glasni == 0 and molk < MOLK_KONEC ):
        if glas:
            govor.append(x); molk = 0
        elif govor:
            molk += KOMAD; govor.append(x)
        if govor and molk >= MOLK_KONEC:
            y = np.concatenate(govor)
            g = 0.35 / max(float(np.abs(y).max()), 1e-9)
            pot = KLON + '/nenehno-poved.wav'
            zapisi_wav(y * g, pot)
            try:
                b = prepis_large(pot).strip()
                if b:
                    v_register(b)
                    # ODMEV ⊢: hiša ti IZREČE, kaj je slišala ( zaupanje: slišiš sebe skozi njena usta )
                    subprocess.run(['node', REPO + '/lucius/lado-govor.mjs', 'Slišal sem: ' + b],
                                   check=False)
                    q.clear()          # med odmevom so kosi vsebovali moj glas — očistim ( ⟨ne⟩ poslušam sebe )
            except Exception as e:
                print('NENEHNO × ' + str(e), flush=True)
            govor = []; molk = 0
