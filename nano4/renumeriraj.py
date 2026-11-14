import re
p = 'D:/OntoProjekt/CanvasMinstral/Nano4/simbolna-licenca-okvir-⟡-vbl-⟡-prevod-kanona-v-simbolno-plast-⟡-sistemski-⟡-osnutek.md'
t = open(p, encoding='utf-8').read()
# 1. glavi: 17A -> 20, 20 -> 17 (zacasni oznaki, da se ne pokrijejo)
t = t.replace('## 17A. BOLJŠI TOKI', '## 99X. BOLJŠI TOKI')
t = t.replace('## 20. PRESEJALNIK', '## 17. PRESEJALNIK')
t = t.replace('## 99X. BOLJŠI TOKI', '## 20. BOLJŠI TOKI')
# 2. seznam v §16: vrstici - §17: in - §20: zamenjata mesti vsebini
t = t.replace('- §17: trije tokovi A/B/C', '- §99X: trije tokovi A/B/C')
t = t.replace('- §20: presejalnik', '- §17: presejalnik')
t = t.replace('- §99X: trije tokovi A/B/C', '- §20: trije tokovi A/B/C')
open(p, 'w', encoding='utf-8').write(t)
print('glavi + seznam zamenjani')
