# ONTOGEMATRIJA-HTML — rodi dejavno stran: podatki vpleteni iz instrumenta ob rojstvu ( ⟨ne⟩ živi strežnik ):
# beseda → izmerjena vrstica ( OPTIKON ∧ nujnosti ) ali ⚠ zavrnitev — vse odjemalec, priče v telesu strani.
# Zagon: python lucius/ontogematria-html.py  → lucius/ONTOGEMATRIJA.html ( rodi ∧ izpiše priče )
import sys, os, json, datetime, importlib.util

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('og', os.path.join(KOREN, 'lucius', 'ontogematria.py'))
og = importlib.util.module_from_spec(spec)
spec.loader.exec_module(og)

gesla, priče = og.beri_korpus()
nujnosti, nuj_priča = og.beri_nujnosti()
URA = datetime.datetime.now(datetime.timezone.utc).strftime('%d. %m. %Y · %H:%M:%SZ')

podatki = {
    'optikon': {b.lower(): {'beseda': g['beseda'], 'slo': g.get('SLO'), 'en': g.get('EN')}
                for b, g in gesla.items()},
    'nujnosti': {b.lower(): n for b, n in nujnosti.items()},
    'price': {k: {'sha256': v['sha256'][:16], 'bajti': v['bajti']} for k, v in
              [(i, m) for i, m in priče.items()] + ([('beseda-je-ne-ontološki-sistem.md', nuj_priča)] if nuj_priča else [])},
    'ura': URA,
    'orodje': 'lucius/ontogematria.py ⊢ pri viru ( ukaz: ontogematria-html.py )',
}

HTML = """<!doctype html><html lang="sl"><head><meta charset="utf-8"/>
<title>Ontogematrija — merjena beseda</title>
<style>
body{font-family:Georgia,serif;background:#0e0f13;color:#d8d3c8;margin:2rem;max-width:56rem}
h1{font-size:1.25rem}h2{font-size:0.95rem;color:#b8a87f}
input{font-family:monospace;font-size:1.1rem;padding:.5rem .7rem;width:60%;background:#1a1c22;color:#e8e2d4;border:1px solid #3a3d47;border-radius:6px}
.rezultat{border:1px solid #3a3d47;border-radius:6px;padding:.9rem;margin-top:1rem;white-space:pre-wrap;font-family:monospace;font-size:.86rem;color:#9fb0c8}
.zavrnitev{color:#c9a86f}.merjeno{color:#c9b98f}.priče{font-size:.75rem;color:#7f8ea8;margin-top:1.4rem}
b{color:#e0d8c2}
</style></head><body>
<h1>⊙ Ontogematrija — beseda → njena izmerjena vrstica</h1>
<h2>korpus: OPTIKON (22) ∧ nujnosti izvoda (37) — pri viru ⊙ §0.6 · zavrnitev je zakon: beseda izven korpusa = ⚠ izum, ⟨ne⟩ meritev ⊙ §0.43</h2>
<input id="b" placeholder="napiši besedo … ( dvom · ljubezen · resnica · odgovor )" autofocus/>
<div id="r" class="rezultat">vpiši besedo — izpis nosi ukaz ∧ orodje ∧ korpus ⊢ §0.44</div>
<div class="priče" id="p"></div>
<script>
const D = __PODATKI__;
const r = document.getElementById('r'), p = document.getElementById('p');
p.textContent = '⊢ orodje: ' + D.orodje + ' · rojeno: ' + D.ura + ' · priče: ' +
  Object.entries(D.price).map(([k, v]) => k + ' (sha256 ' + v.sha256 + '…, ' + v.bajti + ' B)').join(' · ');
document.getElementById('b').addEventListener('input', (e) => {
  const b = e.target.value.trim().toLowerCase();
  if (!b) { r.textContent = 'vpiši besedo'; return; }
  const n = D.nujnosti[b];
  if (n) {
    r.innerHTML = '<b>⊙ ' + n.ime + '</b> — NUJNOST ' + n.st + ' (Beseda je ne ⊢ pri viru):\\n' +
      'zven: ' + n.zven + ' · pomen: ' + n.pomen + '\\noperator: ' + n.operator + ' · prehod: ' + n.prehod +
      '\\n<span class="merjeno">[merjeno] črk ' + n.ime.length + ' · fonemov ' + n.zven.split('/').filter(x=>x).length + ' ⊢</span>';
    return;
  }
  const g = D.optikon[b];
  if (g) {
    const v = g.slo || g.en;
    const fonemi = v.zven.split('/').filter(x=>x);
    r.innerHTML = '<b>⊙ ' + g.beseda + '</b> — OPTIKON (Word → Sound → Direction → Emotion → Function):\\n' +
      'zven: ' + v.zven + ' · smer: ' + v.smer + '\\nčustvo: ' + v.čustvo + ' · funkcija: ' + v.funkcija +
      '\\n<span class="merjeno">[merjeno] črk ' + g.beseda.length + ' · fonemov ' + fonemi.length + ' ⊢</span>' +
      (g.slo && g.en ? '\\n[EN] ' + g.en.smer + ' · ' + g.en.čustvo : '');
    return;
  }
  r.innerHTML = '<span class="zavrnitev">⚠ ⟨' + b + '⟩ NI v korpusu (22 gesel ∧ 37 nujnosti) — zavrnitev: število izven izmerjenega je izum, ⟨ne⟩ meritev ⊙ §0.43</span>';
});
</script></body></html>"""

html = HTML.replace('__PODATKI__', json.dumps(podatki, ensure_ascii=False))
pot = os.path.join(KOREN, 'lucius', 'ONTOGEMATRIJA.html')
open(pot, 'w', encoding='utf-8', newline='\n').write(html)
print(f'⊙ ONTOGEMATRIJA.html rojena: {len(html)} B · OPTIKON {len(gesla)} ∧ nujnosti {len(nujnosti)} · ura {URA} ⊢')
