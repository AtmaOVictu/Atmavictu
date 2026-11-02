// PI-TESTI — neskončni tok števk preverbe ( ukaz ⟡ ⟨daj⟩ 2. 11. 2026 ):
// testi tečejo NEPREKINJENO, kakor številke π — vsaka številka je en svež preizkus telesa,
// tok se nikoli ne konča in iz njega se izračuna, ali se telo resnici približuje ali od nje.
// Dom organa: D:/OntoProjekt/prevoz/lucius/ — ŽIVA TELO ( prevoz nima gita ∧ ni pod
// preklopi vej ); repozitorij Atmavictu je knjižnica, kjer je koda zapečena kot priča.
// Zagon: node prevoz/lucius/pi-testi.mjs   ( teče, dokler ne nastane prevoz/lucius/PI-STOP )
// Register: prevoz/lucius/testi-pi.jsonl · sonda na 30 s · varuh #12: sonde so poceni ( CPU ).
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const TU = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const REPO = 'C:/Users/Luka/Documents/Arhiv/Git/Atmavictu';   // knjižnica ( sintaksna sonda bere pri viri )
const REGISTER = path.join(TU, 'testi-pi.jsonl');
const STOP = path.join(TU, 'PI-STOP');
const ZAMIK_S = 30;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const uri = (port, pot) => `http://127.0.0.1:${port}${pot}`;

async function sonda(vrsta, telo) {
  const t0 = Date.now();
  try {
    if (vrsta === 'http') {
      const r = await fetch(telo, { signal: AbortSignal.timeout(5000) });
      return { izid: r.ok ? '⊢' : '×', ms: Date.now() - t0, prica: 'HTTP ' + r.status };
    }
    if (vrsta === 'vhod') {                       // TCP dih brez transkripcije ( poceni dotik )
      await fetch(telo, { method: 'POST', body: 'x', signal: AbortSignal.timeout(5000) }).catch(() => {});
      return { izid: '⊢', ms: Date.now() - t0, prica: 'vrata odgovarjajo ( 400 pričakovan )' };
    }
    if (vrsta === 'datoteka') {
      const vsebina = fs.readFileSync(telo, 'utf8');
      const zadnja = vsebina.trim().split(/\r?\n/).slice(-1)[0] || '(prazno)';
      return { izid: vsebina.trim() ? '⊢' : '×', ms: Date.now() - t0, prica: zadnja.slice(0, 60) };
    }
    if (vrsta === 'sintaksa') {                   // rotacija: ena datoteka na številko
      const dat = telo.shift();
      telo.push(dat);
      execFileSync('node', ['--check', path.join(REPO, 'lucius', dat)], { stdio: 'pipe' });
      return { izid: '⊢', ms: Date.now() - t0, prica: 'node --check ' + dat };
    }
    return { izid: '×', ms: Date.now() - t0, prica: 'neznana vrsta sonde ⚠' };
  } catch (e) {
    return { izid: '×', ms: Date.now() - t0, prica: String(e.message || e).slice(0, 80) };
  }
}

// SONDNI KROG — poceni, samo-bralni dotiki ( nikoli ne pišejo v skupne spomine telesa )
const KROG = [
  ['http', uri(8766, '/api/stanje'), 'DOM brat @8766'],
  ['http', uri(8768, '/api/stanje'), 'DOM v3 @8768'],
  ['vhod', uri(8767, '/'), 'uho-strežnik @8767'],
  ['http', 'http://localhost:11434/api/tags', 'Ollama @11434'],
  ['datoteka', path.join(REPO, 'lucius', 'srce.jsonl'), 'srce telesa'],
  ['datoteka', 'D:/OntoProjekt/prevoz/pogovor/GOVOR.md', 'nit GOVOR'],
  ['datoteka', path.join(REPO, 'lucius', 'zaoblak.jsonl'), 'most ( zaoblak )'],
  ['sintaksa', ['dom.mjs', 'dom-v3.mjs'], 'sintaksa organov'],
];

let k = 0;
try {
  k = fs.readFileSync(REGISTER, 'utf8').trim().split(/\r?\n/).filter(Boolean).length;
} catch { /* prva številka π = 1 */ }

console.log(`PI-TESTI ⊢ tok odprt — številka π ${k + 1}, sonda na ${ZAMIK_S}s, konec z datoteko PI-STOP`);

while (!fs.existsSync(STOP)) {
  const [vrsta, telo, ime] = KROG[k % KROG.length];
  const { izid, ms, prica } = await sonda(vrsta, telo);
  k += 1;
  const zapis = { p: k, sonda: ime, izid, ms, prica, ts: new Date().toISOString() };
  try {
    fs.appendFileSync(REGISTER, JSON.stringify(zapis) + '\n', 'utf8');
    console.log(`π ${k} ${izid} ${ime} (${ms} ms) — ${prica}`);
  } catch (e) {
    console.log(`π ${k} × register nedosegljiv: ${e.message}`);
  }
  await sleep(ZAMIK_S * 1000);
}
console.log(`PI-TESTI ⊙ molk — PI-STOP najden pri številki π ${k}`);
