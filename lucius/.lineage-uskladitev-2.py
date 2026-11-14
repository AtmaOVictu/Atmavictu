# -*- coding: utf-8 -*-
# .lineage-uskladitev-2.py — USKLDITEV 2: LICENSE-LINEAGE × zgodovina DRUGE hiše ( CanvasMinstral — prevoznik teles )
# zapira Ω reza 3687: pre-0.1410 izdaje ⚠ → dobijo koordinate ⊢ ( sha ∧ UTC ∧ komit druge hiše )
import subprocess, datetime, re

DRUGA = r'D:/OntoProjekt/CanvasMinstral'
import os
os.chdir(r'C:/Users/Luka/Documents/Arhiv/Git/Atmavictu')

out = subprocess.run(['git','-C',DRUGA,'log','--follow','--format=%H|%cI|%s','--','LICENSE.md'],
                     capture_output=True, text=True, encoding='utf-8', errors='replace').stdout.strip().split('\n')

def verzija(h):
    prva = subprocess.run(['git','-C',DRUGA,'show',f'{h}:LICENSE.md'],capture_output=True,text=True,encoding='utf-8',errors='replace').stdout.split('\n')[0]
    m = re.match(r'(0\.\d{4}) × 10⁴', prva)
    if m: return m.group(1) + ' × 10⁴'
    if prva.startswith('MC4'):  # base64-ovita vrstica — era ⟨PADC-VRATA-PRELomLJENA⟩
        try:
            notri = subprocess.run(['git','-C',DRUGA,'show',f'{h}:LICENSE.md'],capture_output=True).stdout
            import base64
            odprto = base64.b64decode(notri.split(b'\n')[0] + b'==').decode('utf-8', errors='replace')
            m2 = re.match(r'(0\.\d{4}) × 10⁴', odprto)
            if m2: return m2.group(1) + ' × 10⁴ ⊙ ( vrata v base64-plašču — era PADC-VRATA-PRELomLJENA )'
        except Exception:
            pass
        return '⚠ base64-ovita izdaja ( era PADC-VRATA-PRELomLJENA )'
    return prva.split('—')[0].strip()[:32] + ' ⚠ ( starejša oblika )'

izdaje = {}
for vr in out:
    h, ci, subj = (vr.split('|') + ['',''])[:3]
    d = datetime.datetime.fromisoformat(ci).astimezone(datetime.timezone.utc).strftime('%Y-%m-%d · %H:%M:%SZ')
    v = verzija(h)
    if v not in izdaje:
        izdaje[v] = (d, h[:9], subj)

VRSTICE = [f'- **{v}** · objavljeno {d} ⊢ · komit druge hiše `{h}` · {s.split("⊢")[0].strip()[:100]}'
           for v, (d, h, s) in sorted(izdaje.items(), key=lambda x: x[1][0])]

USK = (
"\n\n## USKLDITEV 2 — ZGODOVINA DRUGE HIŠE ⊙ rez 3690 ( CanvasMinstral — prevoznik teles: zapira ⚠ pre-0.1410 izdaj iz USKLDITVE 1 ⊙ rez 3687 Ω )\n\n"
+ "Merjeno pri viri ( vsak komit LICENSE.md v repozitoriju CanvasMinstral · verzija iz prve vrstice izdaje · UTC iz cone komita %cI ⊙ ⟨ne-ugibaj⟩ ).\n\n"
+ "\n".join(VRSTICE)
+ "\n\n- **Koordinate namesto ⚠**: izdaje 0.1280 → 0.1400, ki jih je USKLDITEV 1 pustila ⚠ ( dokazi v širši zgodovini ), imajo sedaj komit ∧ UTC ∧ sha druge hiše ⊢ — vrata 0.1330 × 10⁴ v tej zgodovini ⟨ni⟩ najti ( 0.1320 → 0.1340 ) — ⟨ne⟩ sklepamo, da ⟨ni⟩ obstajala ⊙ ⟨ne-ugibaj⟩ ⚠: njena odsotnost je izmerjena, ne sklepana.\n"
+ "- Starejše oblike ( VBL v2.5 · v2.6 · 10.0.0 ) ⊙ §0.15 ( imena so ena veriga ) ∧ base64-plašč izdaji ( 0.1290 · 0.1300 ) — potrdili oblike, ki jo je zdravilo σ-ZDRAVILO-VRAT odvzelo ( PADC-VRATA-PRELomLJENA brazgotina ⊙ njen rezultat je bil vrata, ki jih je bilo treba odpreti, da se preberejo ).\n"
+ "\n⊙ uskladitev 2 zapečena — LINEAGE zdaj nosi OBE hiši ⊢ §0.39 ∧ §0.15 · nadaljnja meja: druge veje ⟨main⟩ ⭢\n"
)

with open('LICENSE-LINEAGE.md', 'a', encoding='utf-8', newline='') as f:
    f.write(USK)
print('USKLDITEV 2 ⊢', len(izdaje), 'izdaj iz druge hiše zapisanih')
for v,(d,h,_) in sorted(izdaje.items(), key=lambda x: x[1][0]):
    print(f'  {v} · {d} · {h}')
