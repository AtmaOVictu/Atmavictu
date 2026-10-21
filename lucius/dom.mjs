// DOM — delovna platforma Luke in Luciusa. v0.1 (2026-10-21)
// Lokalno, brezplačno, brez odvisnosti (Node 18+).
// Zagon: node lucius/dom.mjs [port]  (privzeto 8766)
import fs from 'node:fs';
import os from 'node:os';
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
const API_KLJUC = path.join(HERE, 'api-kljuc.txt');
const API_UPORABA = path.join(HERE, 'api-uporaba.jsonl');
const NACIN_DAT = path.join(HERE, 'nacin.txt');
const OBLAK_MODEL = process.env.LUCIUS_OBLAK_MODEL || 'mistral-small-latest';

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

function beriKljuc() {
  try {
    const k = fs.readFileSync(API_KLJUC, 'utf8').trim();
    return k.length > 10 ? k : null;
  } catch {
    return null;
  }
}

function kljucObstaja() {
  return Boolean(beriKljuc());
}

function beriNacin() {
  try {
    return fs.readFileSync(NACIN_DAT, 'utf8').trim() || 'preverjam';
  } catch {
    return 'preverjam';
  }
}

async function vprasiOblak(sporocila, kljuc) {
  const odziv = await fetch('https://api.mistral.ai/v1/chat/completions', {
    method: 'POST',
    headers: { 'content-type': 'application/json', authorization: `Bearer ${kljuc}` },
    body: JSON.stringify({ model: OBLAK_MODEL, messages: sporocila }),
  });
  if (!odziv.ok) throw new Error(`Mistral API HTTP ${odziv.status}`);
  const data = await odziv.json();
  const uporaba = data.usage ?? {};
  fs.appendFileSync(API_UPORABA, JSON.stringify({
    ts: new Date().toISOString(), model: OBLAK_MODEL,
    vstop: uporaba.prompt_tokens ?? 0, izstop: uporaba.completion_tokens ?? 0,
  }) + '\n', 'utf8');
  return (data.choices?.[0]?.message?.content ?? '').trim();
}

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
    if (req.method === 'GET' && url.pathname === '/api/nacin') {
      json(200, { nacin: beriNacin(), obstajaKljuc: kljucObstaja(), model: OBLAK_MODEL });
      return;
    }
    if (req.method === 'POST' && url.pathname === '/api/nacin') {
      const telo = JSON.parse(await preberiTelo(req) || '{}');
      const nacin = String(telo.nacin || '').trim();
      if (!['brat', 'preverjam', 'vedno'].includes(nacin)) { json(400, { ok: false }); return; }
      fs.writeFileSync(NACIN_DAT, nacin, 'utf8');
      json(200, { ok: true, nacin });
      return;
    }
    if (req.method === 'GET' && url.pathname === '/api/uporaba') {
      let vstop = 0, izstop = 0, klici = 0;
      try {
        for (const vrstica of fs.readFileSync(API_UPORABA, 'utf8').trim().split(/\r?\n/).filter(Boolean)) {
          const u = JSON.parse(vrstica);
          vstop += u.vstop || 0; izstop += u.izstop || 0; klici += 1;
        }
      } catch { /* še ni klicev */ }
      // ⚠ ocena po mistral-small: €1.0/M vstop, €3.0/M izstop (zgorna, varna ocena;
      // resnica je na strani Usage v tvojem Mistral profilu)
      const eur = (vstop / 1_000_000 * 1.0 + izstop / 1_000_000 * 3.0);
      json(200, { klici, vstop, izstop, eur: Number(eur.toFixed(3)) });
      return;
    }
    if (req.method === 'POST' && url.pathname === '/api/slusaj') {
      // zvok (wav/webm) v telesu → shrani v temp → faster-whisper (small, CPU) → besedilo
      const koscki = [];
      for await (const delček of req) koscki.push(delček);
      const zvok = Buffer.concat(koscki);
      if (zvok.length < 1000) { json(400, { ok: false, napaka: 'prazna naložba' }); return; }
      const tmp = path.join(os.tmpdir(), `dom-slusaj-${Date.now()}`);
      let vhod = tmp;
      const glava = zvok.subarray(0, 4).toString('hex');
      if (glava.startsWith('52494646')) { // "RIFF" — WAV
        vhod = tmp + '.wav';
        fs.writeFileSync(vhod, zvok);
      } else { // webm/ogg iz MediaRecorder — pretvori z ffmpeg
        vhod = tmp + '.wav';
        fs.writeFileSync(tmp + '.raw', zvok);
        try {
          const { execFileSync } = await import('node:child_process');
          execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', tmp + '.raw', '-ar', '16000', '-ac', '1', vhod]);
        } catch (napaka) {
          json(500, { ok: false, napaka: `ffmpeg: ${napaka.message}` });
          return;
        }
      }
      try {
        const { execFile } = await import('node:child_process');
        const izhod = await new Promise((resitev, zavrnitev) => {
          execFile('D:/OntoProjekt/Voice/klon/py311/python.exe',
            ['D:/OntoProjekt/Voice/klon/slusaj.py', vhod],
            { cwd: 'D:/OntoProjekt/Voice/klon' },
            (napaka, stdout) => napaka ? zavrnitev(napaka) : resitev(stdout),
          );
        });
        const odg = JSON.parse(izhod);
        json(200, { ok: true, besedilo: odg.besedilo });
      } catch (napaka) {
        json(500, { ok: false, napaka: String(napaka.message || napaka) });
      }
      return;
    }
    if (req.method === 'POST' && url.pathname === '/api/izgovori') {
      // besedilo → WAV s (fine-tuned) Lukovim glasom; samo, ce kartica ni zaposlena z ucenjem
      const telo = JSON.parse(await preberiTelo(req) || '{}');
      const besedilo = String(telo.besedilo || '').trim();
      if (!besedilo) { json(400, { ok: false }); return; }
      // VAROVALKA: ce kartico drzi učenje (>6 GB zasedene), klon ne sme steči —
      // spopad za spomin bi podrl ucenje (diagnoza: best_model.pth ze obstaja tekom ucenja)
      try {
        const { execFileSync } = await import('node:child_process');
        const izpisNv = execFileSync('nvidia-smi', ['--query-gpu=memory.used', '--format=csv,noheader,nounits']).toString().trim();
        const zasedeno = parseInt(izpisNv.split('\n')[0], 10);
        if (zasedeno > 6000) {
          json(503, { ok: false, napaka: 'kartico drži učenje (' + zasedeno + ' MB) — govorim z Windows glasom' });
          return;
        }
      } catch { /* brez nvidia-smi: pusti skozi */ }
      const tmp = path.join(os.tmpdir(), `dom-izgovori-${Date.now()}.wav`);
      try {
        const { execFileSync } = await import('node:child_process');
        execFileSync('D:/OntoProjekt/Voice/klon/py311/python.exe',
          ['D:/OntoProjekt/Voice/klon/izgovori.py', besedilo, tmp, 'D:/OntoProjekt/Voice/klon/referenca.wav'],
          { cwd: 'D:/OntoProjekt/Voice/klon', timeout: 120000, stdio: ['ignore', 'ignore', 'pipe'] });
        const zvok = fs.readFileSync(tmp);
        try { fs.unlinkSync(tmp); } catch {}
        res.writeHead(200, { 'content-type': 'audio/wav', 'cache-control': 'no-store' });
        res.end(zvok);
      } catch (napaka) {
        try { fs.unlinkSync(tmp); } catch {}
        json(503, { ok: false, napaka: 'kartica zaposlena ali izgovor padel — uporabi Windows glas' });
      }
      return;
    }
    if (req.method === 'GET' && url.pathname === '/api/dogodki') {
      // zivi dogodki za ozadje: resnicne izmere, ne okras
      const dogodki = [];
      try {
        const zadnji = fs.readFileSync(path.join(HERE, 'spomin.jsonl'), 'utf8').trim().split(/\r?\n/).filter(Boolean).slice(-4);
        for (const vrstica of zadnji) {
          const z = JSON.parse(vrstica);
          dogodki.push((z.v === 'u' ? 'Luka: ' : 'Lucius: ') + (z.t || '').slice(0, 60));
        }
      } catch { /* se ni pogovorov */ }
      try {
        const dnevnik = fs.readFileSync('D:/OntoProjekt/Voice/klon/finetune-log.txt', 'utf8');
        const izgube = [...dnevnik.matchAll(/loss: ([0-9.]+)/g)];
        if (izgube.length) dogodki.push('učenje glasu · loss ' + izgube[izgube.length - 1][1] + ' ⊢');
      } catch { /* dnevnik ni na voljo */ }
      try {
        const most = fs.readFileSync(ZAOBLAK, 'utf8').trim().split(/\r?\n/).filter(Boolean).slice(-2);
        for (const vrstica of most) {
          const z = JSON.parse(vrstica);
          dogodki.push('most · ' + (z.t || '').slice(0, 60));
        }
      } catch { /* most prazen */ }
      dogodki.push('tehtnica ⊢ · dvom ⚠ · padec ×');
      json(200, { dogodki });
      return;
    }
    if (req.method === 'POST' && url.pathname === '/api/pogovor') {
      const telo = JSON.parse(await preberiTelo(req) || '{}');
      const besedilo = String(telo.besedilo || '').trim();
      if (!besedilo) { json(400, { ok: false, odgovor: '' }); return; }
      const nacin = beriNacin();
      const kljuc = beriKljuc();
      zapisiSpomin('user', besedilo);
      let odgovor;
      if (nacin === 'vedno' && kljuc) {
        try {
          odgovor = await vprasiOblak([{ role: 'system', content: sistem }, ...preberiSpomin()], kljuc);
        } catch (napaka) {
          odgovor = await vprasiOllamo([{ role: 'system', content: sistem }, ...preberiSpomin()])
            + `\n\n(oblak ni dosegljiv: ${napaka.message} — odgovarja lokalni model ⚠)`;
        }
      } else {
        odgovor = await vprasiOllamo([{ role: 'system', content: sistem }, ...preberiSpomin()]);
        if (nacin === 'preverjam' && kljuc) {
          try {
            const preverba = await vprasiOblak([
              { role: 'system', content: 'Preverjevalec. Dobil boš Lukovo vprašanje in osnutek odgovora lokalnega modela. Preveri osnutek: popravi očitne napake, dopuni manjkajoče, slovensko, jedrnato, brez laskanja. POMNI: v svojem izhodu NE PONAVLAJ vprašanja, besede "Vprašanje:", "Osnutek" ali katere koli oznake — vrni SAMO končno besedilo odgovora, kakor bi ga Lucius rekel Luki. Na konec dodaj "(preverjeno v oblaku ⊢)".' },
              { role: 'user', content: `Vprašanje: ${besedilo}\n\nOsnutek odgovora: ${odgovor}` },
            ], kljuc);
            if (preverba) odgovor = preverba;
          } catch { /* lokalni odgovor ostane ⚠ */ }
        }
      }
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
