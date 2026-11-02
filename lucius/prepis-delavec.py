# PREPIS-DELAVEC — ločen proces prepisa ( zdravilo PADC-DISKONTINUITETE, ukaz ⟡ ⟨da stori tudi to⟩ 2. 11. ):
# Whisper large-v3 teče v SVOJEM procesu ( lasten GIL ), snemalna nit poslušalnika nikoli
# ne stradne, ko prepis poteka. Delavec naloži model ENKRAT ∧ prebavlja poti wav datotek
# z stdin ( ena vrstica = ena pot ), odgovarja JSON vrstico na stdout.
# Zagon: samodejno ga prižge nenehno-poslusa.py ( organ v isti mapi ); ročni preizkus:
#   echo "D:/pot/do.wav" | py311/python.exe prepis-delavec.py
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

print('DELAVEC: nalagam large-v3 …', flush=True)
from faster_whisper import WhisperModel
MODEL = WhisperModel('large-v3', device='cuda', compute_type='float16')
print('DELAVEC: model pripravljen ⊢ ( ločen proces — uho ne stradne )', flush=True)

for vrstica in sys.stdin:
    pot = vrstica.strip()
    if not pot:
        continue
    try:
        segmenti, _ = MODEL.transcribe(pot, language='sl', vad_filter=True,
                                       vad_parameters={'min_silence_duration_ms': 700}, beam_size=5)
        besedilo = ' '.join(seg.text.strip() for seg in segmenti if seg.text.strip())
        print(json.dumps({'ok': True, 'besedilo': besedilo}, ensure_ascii=False), flush=True)
    except Exception as e:
        print(json.dumps({'ok': False, 'napaka': str(e)[:200]}, ensure_ascii=False), flush=True)
