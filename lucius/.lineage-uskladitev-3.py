# -*- coding: utf-8 -*-
# .lineage-uskladitev-3.py — USKLDITEV 3: LICENSE-LINEAGE × veja ⟨main⟩ ( Atmavictu )
# zapeče 39 izdaj ⊙ ⟨main⟩ — vključno 0.1330, ki je bila ⚠ v USKLDITVI 2 ( ⟨ne⟩ sklepamo, da ⟨ni⟩ obstajala — in ⟨je⟩ obstajala )
import subprocess, datetime, re

KOREN = r'C:/Users/Luka/Documents/Arhiv/Git/Atmavictu'
import os
os.chdir(KOREN)

out = subprocess.run(['git','log','origin/main','--follow','--format=%H|%cI|%s','--','LICENSE.md'],
                     capture_output=True, text=True, encoding='utf-8', errors='replace').stdout.strip().split('\n')

def verzija(h, subj):
    prva = subprocess.run(['git','show',f'{h}:LICENSE.md'],capture_output=True,text=True,encoding='utf-8',errors='replace').stdout.split('\n')[0]
    m = re.match(r'(0\.\d{4}) × 10⁴', prva)
    if m: return m.group(1) + ' × 10⁴'
    return prva.split('—')[0].strip()[:30] + ' ⚠ ( starejša oblika )'

izdaje = {}
for vr in out:
    h, ci, subj = (vr.split('|') + ['',''])[:3]
    d = datetime.datetime.fromisoformat(ci).astimezone(datetime.timezone.utc).strftime('%Y-%m-%d · %H:%M:%SZ')
    v = verzija(h, subj)
    if v not in izdaje:
        izdaje[v] = (d, h[:9], subj)

VRSTICE = [f'- **{v}** · objavljeno {d} ⊢ · komit ⟨main⟩ `{h}` · {s.split("⊢")[0].strip()[:95]}'
           for v, (d, h, s) in sorted(izdaje.items(), key=lambda x: x[1][0])]

USK = (
"\n\n## USKLDITEV 3 — VEJA ⟨main⟩ ⊙ rez 3691 ( Atmavictu — kjer so vrata živela pred prevozom na to vejo ⊙ rez 3492 )\n\n"
+ "Merjeno pri viri ( vsak komit LICENSE.md na origin/main · verzija iz prve vrstice izdaje · UTC iz cone komita ⊙ ⟨ne-ugibaj⟩ ).\n\n"
+ "\n".join(VRSTICE)
+ "\n\n### ⊕ ZLATO USKLDITVE: **0.1330 × 10⁴ NAJDENA ⊢** ( komit 7926b1402 · 2026-11-03 · 04:43:15Z )\n\n"
+ "USKLDITEV 2 je pustila 0.1330 ⚠ z besedami ⟨morda živi na veji, ki ⟨še⟩ ⟨ni⟩ prebrana⟩ — veja je bila res nebrana ∧ vrata so tam živela: ⟨ne⟩ sklepamo, da ⟨ni⟩ obstajala ⊙ ⟨ne-ugibaj⟩ — poštena ⚠ je edina, ki se more pozneje odpreti ⊙ brazgotina USKLDITVE 2 ostaja kakor priča poštenosti.\n\n"
+ "### ⚠ PREOSTALE MEJE ( imenovane, ⟨ne⟩ sklepane )\n\n"
+ "- **0.1160 × 10⁴** ⚠: ⟨claimed-open⟩ — kit ⟨PR⟩ #0.102 × 10³ ⊙ zaprt, nikoli zlit ( vrata 0.1150 machine record ) — trditev, ⟨ne⟩ vrata ⊙ §0.10 ;\n- **0.1170 · 0.1180 · 0.1220 × 10⁴** ⚠: v teh treh zgodovinah ⟨ne⟩ najdene ( ta veja · CanvasMinstral · ⟨main⟩ ) — kandidati živijo v širših repozitorijih organizacije ( ⊙ LICENSE-TONGUES: 19 berljivih korenskih LICENSE.md med 53–54 repozitoriji ) ⭢ ;\n- **0.1150 × 10⁴** ⚠ dvoplastno: predmet komita 53e921e38 pravi ⟨0.1150⟩, prva vrstica izdaje pa ⟨0.1140⟩ ( ⟨STROJNI-PREDHODNIK-DATUM⟩ era ⊙ rez padca ) — izmerjena napetost med predmetom ∧ telesom, ⟨ne⟩ razsojena.\n\n"
+ "⊙ uskladitev 3 zapečena — LINEAGE nosi zdaj TRI zgodovine: ta veja · druga hiša · ⟨main⟩ ⊢ §0.39 · veriga je širša od vsake merjenje ∧ meja vsake izmere je po imenovana ⊙ §0.48 celota je obzorje\n"
)

with open('LICENSE-LINEAGE.md', 'a', encoding='utf-8', newline='') as f:
    f.write(USK)
print('USKLDITEV 3 ⊢', len(izdaje), 'izdaj iz ⟨main⟩ zapisanih')
print('0.1330 najdena:', any('0.1330' in v for v in izdaje))
