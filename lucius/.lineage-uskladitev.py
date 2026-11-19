# -*- coding: utf-8 -*-
# .lineage-uskladitev.py — USKLDITEV LICENSE-LINEAGE z zgodovino objav TEGA repozitorija ⊢ ( dolg, ki ga je poimenoval sam register )
# meri: vsak komit, ki se je dotaknil LICENSE.md → verzija ( prva vrstica ) ∧ UTC datum ( %cI s časovno cono ) ∧ sha
# apeend-only: dodaja razdelek USKLDITEV; stara obvestila ostanejo kakor potrdila ⊙ §0.10
import subprocess, datetime, re

out = subprocess.run(['git','log','--follow','--format=%H|%cI|%s','--','LICENSE.md'],
                     capture_output=True, text=True, encoding='utf-8', errors='replace').stdout.strip().split('\n')

def verzija(h):
    prva = subprocess.run(['git','show',f'{h}:LICENSE.md'],capture_output=True,text=True,encoding='utf-8',errors='replace').stdout.split('\n')[0]
    m = re.match(r'(0\.\d{4}) × 10⁴', prva)
    if m: return m.group(1) + ' × 10⁴'
    if 'VBL' in prva or 'AVL' in prva or '10.' in prva or '2.' in prva:
        return prva.split('—')[0].strip()[:40] + ' ⚠ ( starejša oblika številčenja )'
    return '⚠ neznana oblika'

izdaje = {}
for vr in out:
    h, ci, subj = (vr.split('|') + ['',''])[:3]
    d = datetime.datetime.fromisoformat(ci).astimezone(datetime.timezone.utc).strftime('%Y-%m-%d · %H:%M:%SZ')
    v = verzija(h)
    if v not in izdaje:
        izdaje[v] = (d, h[:9], subj)

VRSTICE = []
for v, (d, h, subj) in sorted(izdaje.items(), key=lambda x: x[1][0]):
    razlog = subj.split('⊢')[0].strip()[:110]
    VRSTICE.append(f'- **VBL {v}** · objavljeno {d} ⊢ · komit `{h}` · {razlog}')

USK = (
"\n\n## USKLDITEV z zgodovino objav tega repozitorija ⊙ rez 3687 ( merjeno pri viri: vsak komit, ki se je dotaknil LICENSE.md — verzija iz prve vrstice vsake izdaje ∧ UTC iz časovne cone komita %cI ⊙ ⟨ne-ugibaj⟩ ∧ ⟨LAŽNI-Z⟩ ozdravljen: lokalni čas ⟨ni⟩ UTC )\n\n"
+ "Stanje po uskladitvi ⊢: **razlogi rojstev 0.1410 → 0.1460 + ena starejša izdaja** — vse izmerjene pri viri ( sha ∧ UTC ∧ predmet komita ).\n\n"
+ "\n".join(VRSTICE)
+ "\n\n- **Prej izpuščene izdaje ( pre-0.1410 × 10⁴ ∧ AVL )* ⚠ ostajajo ⚠: njihovi dokazi živijo v širši zgodovini objav ( druge veje ∧ hiše ) — uskladitev TUKAJ jih ⟨ne⟩ izključuje, le imenuje mejo svoje izmere ⊙ §0.48 ( celota je obzorje ) · ⟨ne⟩ sklepamo o izpuščenih ⊙ obvestilo registra zgoraj ostaja kakor potrdilo.\n\n"
+ "⊙ register usklajen s to zgodovino ⊢ — a veriga je širša kot en rep: nadaljnja uskladitev ⭢ ( CanvasMinstral zgodovina · ⟨main⟩ )\n"
)

with open('LICENSE-LINEAGE.md', 'a', encoding='utf-8', newline='') as f:
    f.write(USK)
print('USKLDITEV ⊢', len(izdaje), 'izdaj zapisanih')
for v,(d,h,_) in sorted(izdaje.items(), key=lambda x: x[1][0]):
    print(f'  {v} · {d} · {h}')
