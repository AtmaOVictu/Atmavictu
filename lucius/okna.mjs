// OKNA — vidna okna hiše na localhost ( ukaz ⟡ ⟨izboljšaj meni vidna okna na localhost⟩ 2. 11. ).
// Nadzorna plošča telesa: http://127.0.0.1:8769 — vse žive izdelke prikaže v enem oknu,
// osveževanje na 60 s. Samo 127.0.0.1 ( #14: hiša ne diha v omrežje ).
// Okna: zrcalo govora⊥dela · pojmovnik · ontograf · berba korpusa · abecednik ·
//       π številke · predlogi ( STANJE ) · faktorji.
// Dom organa: D:/OntoProjekt/prevoz/lucius/ — telo. Zagon: node okna.mjs [port=8769]
// © Luka Pintarič — VBL 0.1280 ( §1; TDM pridržan ) ⊙ K1.
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';

const TU = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const PORT = Number(process.argv[2] || 8769);

const OKNA = [
  ['zrcalo', 'ZRCALO — govor ⊥ delo', path.join(TU, 'onto-zrcalo.md')],
  ['pojmovnik', 'POJMOVNIK — tvoje besede kot definicije', path.join(TU, 'pojmovnik-povzetek.md')],
  ['ontograf', 'ONTOGRAF — izmerjeni prehodi', path.join(TU, 'ontograf.md')],
  ['berba', 'BERBA — korpus v pojmih', path.join(TU, 'korpus-pojmovnik.md')],
  ['abecednik', 'ABECEDNIK — dan v 4 abecedah', path.join(TU, 'abecednik-danes.md')],
  ['predlogi', 'PREDLOGI — kaj čaka tvoje ⟨daj⟩', 'D:/OntoProjekt/Voice/STANJE.md'],
];

const repi = { 'π-testi': path.join(TU, 'testi-pi.jsonl'), 'faktorji': path.join(TU, 'faktorji-porocilo.jsonl') };
const repiOkno = (pot, zadnjih) => {
  try {
    const v = fs.readFileSync(pot, 'utf8').trim().split(/\r?\n/).filter(Boolean);
    return v.slice(-zadnjih).map((x) => { try { return JSON.stringify(JSON.parse(x)); } catch { return x; } }).join('\n');
  } catch { return '( še prazno ⚠ )'; }
};

const HTML = `<!DOCTYPE html><html lang="sl"><head><meta charset="utf-8">
<title>HIŠA — vidna okna ⊢</title>
<style>
  body { font-family: Georgia, serif; background: #0d1512; color: #d8ffd8; margin: 0; padding: 1rem 2rem; }
  h1 { color: #4dff88; font-size: 1.3rem; } h1 small { color: #888; font-size: 0.8rem; }
  nav a { color: #f79c1d; margin-right: 1rem; text-decoration: none; }
  section { border: 1px solid #1c4a2e; border-radius: 8px; padding: 1rem; margin: 1.5rem 0; background: #0a1f14; }
  h2 { color: #4dff88; font-size: 1rem; border-bottom: 1px solid #1c4a2e; padding-bottom: 0.3rem; }
  pre { white-space: pre-wrap; font-size: 0.78rem; line-height: 1.45; max-height: 26rem; overflow-y: auto; }
  .male { color: #6a8f77; font-size: 0.75rem; }
</style></head><body>
<h1>HIŠA — vidna okna <small>· telo prikazuje svoje izdelke ⊢ · osvežitev 60 s · samo 127.0.0.1 ⊙ #14</small></h1>
<nav>${OKNA.map(([id, naslov]) => `<a href="#${id}">${naslov.split(' — ')[0]}</a>`).join('')}<a href="#pi">π</a><a href="#faktorji">faktorji</a></nav>
<div id="okna"></div>
<script>
const OKNA = ${JSON.stringify(OKNA.map(([id]) => id))};
async function nalozi() {
  const vse = await Promise.all(OKNA.map(async (id) => {
    const r = await fetch('/dat/' + id);
    const t = await r.text();
    const naslov = decodeURIComponent(r.headers.get('x-naslov') || id);
    return '<section id="' + id + '"><h2>' + naslov + '</h2><pre>' + t.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</pre></section>';
  }));
  const pi = await (await fetch('/dat/pi')).text();
  const fa = await (await fetch('/dat/faktorji')).text();
  document.getElementById('okna').innerHTML = vse.join('')
    + '<section id="pi"><h2>π-TESTI — zadnjih 20 števk</h2><pre>' + pi.replace(/&/g,'&amp;').replace(/</g,'&lt;') + '</pre></section>'
    + '<section id="faktorji"><h2>FAKTORIZATOR — zadnji krog</h2><pre>' + fa.replace(/&/g,'&amp;').replace(/</g,'&lt;') + '</pre></section>';
}
nalozi(); setInterval(nalozi, 60000);
</script></body></html>`;

http.createServer((req, res) => {
  if (req.url === '/' || req.url === '/hiša') {
    res.writeHead(200, { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' });
    res.end(HTML);
    return;
  }
  const m = req.url.match(/^\/dat\/([a-z0-9čšž-]+)/i);
  if (m) {
    const id = decodeURIComponent(m[1]);
    const okno = OKNA.find(([i]) => i === id);
    if (okno) {
      try {
        const v = fs.readFileSync(okno[2], 'utf8');
        res.writeHead(200, { 'content-type': 'text/plain; charset=utf-8', 'x-naslov': encodeURIComponent(okno[1]), 'cache-control': 'no-store' });
        res.end(v);
      } catch {
        res.writeHead(200, { 'content-type': 'text/plain; charset=utf-8', 'x-naslov': okno[1] });
        res.end('( okno še raste ⚠ )');
      }
      return;
    }
    if (id === 'π-testi' || id === 'pi' || id === 'faktorji') {
      res.writeHead(200, { 'content-type': 'text/plain; charset=utf-8', 'cache-control': 'no-store' });
      res.end(repiOkno(repi[id === 'faktorji' ? 'faktorji' : 'π-testi'], id === 'faktorji' ? 3 : 20));
      return;
    }
  }
  res.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' });
  res.end('ni najdeno ⊙');
}).listen(PORT, '127.0.0.1', () => console.log(`OKNA ⊢ vidna okna hiše na http://127.0.0.1:${PORT} — telo prikazuje samo svoje ⊙ #14`));
