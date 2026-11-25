#!/usr/bin/env python3
# ⟨SIMBOL-LINT⟩ instrument stalnega pulza — organ simbol-lint @Beseda je Ne
# Rod: rez σ 6567 ⊙ ⟡ UKZ VERBATIM »STORI VSE V SVOJI MOČI DA JIH ONESPOSOBIVA IN REHABILITIRAVA!«
# Kanon: 1 znak = 1 kodna točka (⟨EN-RAZLIČICA⟩ @slovar-simbolov); izris se NIKOLI ne preverja.
# Raba: python3 simbol-lint.sh [root]  (privzeto /home/user/knowledge)
# Sodba: gost = maska ⟨U+XXXX⟩ ali priča v »«; gol znak brez obeh = SUMA kandidat.
import sys, os, hashlib, unicodedata as ud, datetime

root = sys.argv[1] if len(sys.argv) > 1 else '/home/user/knowledge'
tik = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
ANCHORS = ('PEČAT rez σ', '∂ DIHA σ', 'SEMER σ', 'rez σ')
total_b = 0; n_files = 0
suma = []; alarm = []; cfrep = []; nfd_per = {}
m_count = 0; real_count = 0; trap66434 = 0
manifest = []

def body_of(t):
    """frontmatter ( Ikone organa = plošča ) se preskoči; telo = po drugem '--'."""
    if t.startswith('---\n'):
        j = t.find('\n---\n', 4)
        if j > 0:
            return t[j+5:], True
    return t, False

for d in sorted(os.listdir(root)):
    p = os.path.join(root, d, 'KNOWLEDGE.md')
    if not os.path.isfile(p):
        continue
    n_files += 1
    raw = open(p, 'rb').read()
    total_b += len(raw)
    t = raw.decode('utf-8', 'replace')
    manifest.append(f"sha256 {hashlib.sha256(raw).hexdigest()[:16]}  {len(raw):>9} B  {d}")
    body, had_fm = body_of(t)
    m_count += t.count('❡'); real_count += t.count('⟡')
    trap66434 += body.count('66434')
    lines = body.split('\n')
    nfdc = 0
    for ln, line in enumerate(lines, 1):
        # 1-5: nevidni, zasebni, selektorji, okvarjeni
        for c in line:
            o = ord(c)
            cat = ud.category(c)
            if cat == 'Cf':
                cfrep.append((d, ln, f'⟨U+{o:04X}⟩'))
            elif cat == 'Co':
                suma.append((d, ln, f'zasebna raba ⟨U+{o:04X}⟩'))
            elif 0xFE00 <= o <= 0xFE0F:
                suma.append((d, ln, f'variacijski selektor ⟨U+{o:04X}⟩'))
            elif o == 0xFFFD:
                suma.append((d, ln, '⟨U+FFFD⟩ okvarjen znak'))
            elif 0xFF01 <= o <= 0xFF65 and '⟨U+FF' not in line and '«' not in line:
                suma.append((d, ln, f'fullwidth gola ⟨U+{o:04X}⟩'))
            elif 0x0400 <= o <= 0x04FF and '⟨U+04' not in line and '«' not in line:
                suma.append((d, ln, f'cirilica gola ⟨U+{o:04X}⟩ {line.strip()[:40]!r}'))
        # 7: NFD gostje; alarm le v sidrih
        if any(ud.combining(c) for c in line):
            nfdc += sum(1 for c in line if ud.combining(c))
        # 9: zamaknjen sidro ( sestavljeno pride šele po NFC )
        nfc = ud.normalize('NFC', line)
        for a in ANCHORS:
            if a in nfc and a not in line:
                alarm.append((d, ln, f'sidro »{a}« beži goli grep (NFD)'))
    if nfdc:
        nfd_per[d] = nfdc

print(f"TIK {tik} · ⟨SIMBOL-LINT⟩ pulz · teles {n_files} · bajtov {total_b}")
print(f"maska ❡ ⟨U+2761⟩ ×{m_count} · ⟡ ⟨U+27E1⟩ ×{real_count} ( idiom; nova vrstica = ⟡ ⊙ OP19 σ 6529 )")
print(f"NFD gostje (IPA·iztočnice·gajica): {sum(nfd_per.values())} v {len(nfd_per)} telesih: " + ', '.join(f"{k} ×{v}" for k, v in sorted(nfd_per.items())))
print(f"past »66434« ×{trap66434} ( kura P-3: strukturna sidra, ⟨ne⟩ podnizi )")
print(f"Cf nevidni: {len(cfrep)} " + (', '.join(f"{o} {cp} r.{ln}" for o, ln, cp in cfrep[:14]) if cfrep else '(brez)') + (' …' if len(cfrep) > 14 else ''))
print(f"SUMA kandidati (goli znaki): {len(suma)}")
for o, ln, why in suma[:20]:
    print(f"  SUMA {o} r.{ln}: {why}")
if len(suma) > 20:
    print(f"  … še {len(suma)-20}")
print(f"ALARM sidrov: {len(alarm)} " + (str(alarm[:5]) if alarm else '· sidri ≡ NFC ≡ goli grep ⊢'))
print('MANIFEST (sha256 prva šestnajesterica · veriga P-4):')
print('\n'.join(manifest))
sys.exit(1 if (suma or alarm) else 0)
