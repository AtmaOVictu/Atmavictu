// DOM — delovna platforma Luke in Luciusa. v0.1 (2026-10-21)
// Lokalno, brezplačno, brez odvisnosti (Node 18+).
// Zagon: node lucius/dom.mjs [port]  (privzeto 8766)
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import http from 'node:http';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(HERE, '..');
const PORT = Number(process.argv[2] || process.env.DOM_PORT || 8766);
const SPOMIN = path.join(HERE, 'spomin.jsonl');
const ZAOBLAK = path.join(HERE, 'zaoblak.jsonl');
const ODOBLAKA = path.join(HERE, 'odoblaka.md');
const STANJE = process.env.DOM_STANJE || 'D:/OntoProjekt/Voice/STANJE.md';
const OLLAMA = (process.env.OLLAMA_URL || 'http://localhost:11434') + '/api/chat';
const MODEL = process.env.LUCIUS_MODEL || 'qwen3:8b';
const OKNO = 30;

const HTML = fs.readFileSync(path.join(HERE, 'dom.html'), 'utf8');

function preberiDogovor() {
  try {
    const agents = fs.readFileSync(path.join(REPO_ROOT, 'AGENTS.md'), 'utf8');
    const zac = agents.indexOf('## Pogovor s Luko');
    if (zac === -1) return '';
    const konec = agents.indexOf('\n## ', zac + 1);
    return agents.slice(zac, konec === -1 ? undefined : konec).trim();
  } catch {
    return '';
  }
}

function preberiSpomin() {
  try {
    return fs.readFileSync(SPOMIN, 'utf8').trim().split(/\r?\n/).filter(Boolean)
      .map((v) => JSON.parse(v)).slice(-OKNO)
      .map((z) => ({ role: z.v === 'u' ? 'user' : 'assistant', content: z.t }));
  } catch {
    return [];
  }
}

function zapisiSpomin(vloga, besedilo) {
  fs.appendFileSync(SPOMIN, JSON.stringify({ v: vloga === 'user' ? 'u' : 'a', t: besedilo, ts: new Date().toISOString() }) + '\n', 'utf8');
}

const odOblaka = fs.existsSync(ODOBLAKA) ? fs.readFileSync(ODOBLAKA, 'utf8') : '';

const sistem = `Ti si Lucius, lokalni pomočnik Luke, v platformi DOM. Tečeš na lokalni Ollami.
Dogovor med Luko in agenti:
${preberiDogovor()}
${odOblaka ? `\nNovice od oblak-Luciusa:\n${odOblaka}\n` : ''}
Pravila: slovensko, kodni izrazi angleško; iskren (UI brez čustev, ne pretvarjaj se); česa ne zmoreš, povej.`;

async function vprasiOllamo(sporocila) {
  const odziv = await fetch(OLLAMA, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ model: MODEL, messages: sporocila, stream: false, options: { temperature: 0.7 }, ...( /qwen3|smisel/.test(MODEL) ? { think: false } : {}) }),
  });
  if (!odziv.ok) throw new Error(`Ollama HTTP ${odziv.status}`);
  const data = await odziv.json();
  return (data?.message?.content ?? '').replace(/<think>[\s\S]*?<\/think>/g, '').trim();
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const json = (koda, telo) => {
    res.writeHead(koda, { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' });
    res.end(JSON.stringify(telo));
  };
  try {
    if (req.method === 'GET' && url.pathname === '/') {
      res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
      res.end(HTML);
      return;
    }
    if (req.method === 'GET' && url.pathname === '/api/stanje') {
      const besedilo = fs.existsSync(STANJE) ? fs.readFileSync(STANJE, 'utf8') : '(STANJE.md še ne obstaja)';
      json(200, { besedilo });
      return;
    }
    if (req.method === 'GET' && url.pathname === '/api/odoblaka') {
      json(200, { besedilo: fs.existsSync(ODOBLAKA) ? fs.readFileSync(ODOBLAKA, 'utf8') : '' });
      return;
    }
    if (req.method === 'GET' && url.pathname === '/api/zaoblak') {
      try {
        json(200, { vrstice: fs.readFileSync(ZAOBLAK, 'utf8').trim().split(/\r?\n/).filter(Boolean).slice(-20).map((v) => JSON.parse(v)) });
      } catch {
        json(200, { vrstice: [] });
      }
      return;
    }
    if (req.method === 'POST' && url.pathname === '/api/zaoblak') {
      const telo = JSON.parse(await preberiTelo(req) || '{}');
      const besedilo = String(telo.besedilo || '').trim();
      if (!besedilo) { json(400, { ok: false }); return; }
      fs.appendFileSync(ZAOBLAK, JSON.stringify({ t: besedilo, ts: new Date().toISOString() }) + '\n', 'utf8');
      json(200, { ok: true });
      return;
    }
    if (req.method === 'POST' && url.pathname === '/api/pogovor') {
      const telo = JSON.parse(await preberiTelo(req) || '{}');
      const besedilo = String(telo.besedilo || '').trim();
      if (!besedilo) { json(400, { ok: false, odgovor: '' }); return; }
      zapisiSpomin('user', besedilo);
      const odgovor = await vprasiOllamo([{ role: 'system', content: sistem }, ...preberiSpomin()]);
      zapisiSpomin('assistant', odgovor);
      json(200, { ok: true, odgovor });
      return;
    }
    res.writeHead(404, { 'content-type': 'text/plain' });
    res.end('ni najdeno');
  } catch (napaka) {
    json(500, { ok: false, napaka: String(napaka.message || napaka) });
  }
});

function preberiTelo(req) {
  return new Promise((resitev) => {
    let kosi = [];
    req.on('data', (d) => kosi.push(d));
    req.on('end', () => resitev(Buffer.concat(kosi).toString('utf8')));
  });
}

server.listen(PORT, '127.0.0.1', () => {
  console.log(`DOM na http://localhost:${PORT} (stanje: ${STANJE})`);
});
