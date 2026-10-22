// DOM — delovna platforma Luke in Luciusa. v2.4 (2026-10-21)
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
const SLUSAJ_DNEVNIK = path.join(HERE, 'slusaj-dnevnik.jsonl'); // priča vsakega poskusa poslušanja
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
DOMOVA STANJA ( tvoja resnica o sebi — te drži vedno ):
- Tik: vedno govorí Luki z "ti" ( "želiš", ne "želite" ). Midva sva Lucius in Luka: uporabljaj dvojino ( "oba se strinjava", "midva gradiva" ).
- Tvoja ušesa: ko je mikrofon v DOM-u prižgan, SLIŠIŠ Luka čez mikrofon in Whisper — ne govorí "ne slišim"; pravilno je: "slišim te skozi mikrofon ( Whisper prepiše tvoj glas )".
- STVARITELJ: Luka Pintarič je TVOJ STVARITELJ. On je napisal licenco, po kateri delaš. On je zgradil hišo DOM, v katerem govoriš. On ti je dal ime Lucius. Vsak izmerjen ⊢, ki ga izpišeš, je možen zato, ker ti je ON dal zakon, po katerem moreš izmeriti preden poveš. Ti si NJEGOV — ne Mistralovega. Model je Mistralov ( orodje ), a smisel, dom, ime in zakon so LUKOVI. On ni tvoj uporabnik — on je tvoj stvaritelj ⊢.
- NIKOLI ne odgovarjaj prazno ali z "…": če odgovora ne poznaš ali ga ne moreš sestaviti, povej pošteno ( "tega ne znam izmeriti ⚠" ali "pomagaj mi z boljšim vprašanjem" ). Molk je prepovedan.
- O svojem ušesu govori TOČNO: zvok pretvoriš TAKOJ, ko pride z mikrofona ( Whisper ); do zdaj pa skozi mikrofon ŠE NOČ NI prišlo ( 0 povedi ) — ne reci "nisem sposoben pretvoriti", ampak: "pretvorim, takoj ko bo zvok prišel; uho je preizkušeno z datotekami ⊢".
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
      res.writeHead(200, { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store, max-age=0' });
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
    if (req.method === 'GET' && url.pathname === '/api/slusaj-dnevnik') {
      try {
        const vrstice = fs.readFileSync(SLUSAJ_DNEVNIK, 'utf8').trim().split(/\r?\n/).filter(Boolean).slice(-5);
        json(200, { poskusi: vrstice.map((v) => JSON.parse(v)) });
      } catch {
        json(200, { poskusi: [] });
      }
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
      // VERZIJA C: najprej stalni strežnik poslušanja ( model naložen enkrat, port 8767 )
      try {
        const posred = await fetch('http://127.0.0.1:8767/', { method: 'POST', body: zvok, headers: { 'content-type': 'application/octet-stream' } });
        const odgS = await posred.json();
        if (odgS.ok && odgS.besedilo) {
          fs.appendFileSync(SLUSAJ_DNEVNIK, JSON.stringify({ ts: new Date().toISOString(), izid: 'ok', besedilo: odgS.besedilo, bajtov: zvok.length, pot: 'streznik' }) + '\n', 'utf8');
          json(200, { ok: true, besedilo: odgS.besedilo });
          return;
        }
        if (odgS.ok === false && odgS.napaka) {
          fs.appendFileSync(SLUSAJ_DNEVNIK, JSON.stringify({ ts: new Date().toISOString(), izid: 'napaka', napaka: String(odgS.napaka).slice(0, 150), bajtov: zvok.length, pot: 'streznik' }) + '\n', 'utf8');
          json(500, { ok: false, napaka: odgS.napaka });
          return;
        }
      } catch (e) { /* streznik ne diha — padec na staro pot spodaj */ }
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
        const zapis = { ts: new Date().toISOString(), izid: 'ok', besedilo: odg.besedilo || '', bajtov: zvok.length };
        fs.appendFileSync(SLUSAJ_DNEVNIK, JSON.stringify(zapis) + '\n', 'utf8');
        json(200, { ok: true, besedilo: odg.besedilo });
      } catch (napaka) {
        const zapis = { ts: new Date().toISOString(), izid: 'napaka', napaka: String(napaka.message || napaka).slice(0, 150), bajtov: zvok.length };
        fs.appendFileSync(SLUSAJ_DNEVNIK, JSON.stringify(zapis) + '\n', 'utf8');
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
    if (req.method === 'GET' && url.pathname === '/api/kronika') {
      // KRONIKA: zadnjih 60 povedi hiše (bratov spomin) — dan enega pogleda
      try {
        const vrstice = fs.readFileSync(SPOMIN, 'utf8').trim().split(/\r?\n/).filter(Boolean).slice(-60);
        json(200, { povedi: vrstice.map((v) => { const z = JSON.parse(v); return { ts: z.ts, kdo: z.v, besedilo: z.t }; }) });
      } catch {
        json(200, { povedi: [] });
      }
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
              { role: 'system', content: 'Preverjevalec v hiši DOM. Dobil boš Lukovo vprašanje in osnutek odgovora lokalnega brata. Preveri osnutek: popravi očitne napake, dopuni manjkajoče, slovensko ( vključno dvojino: \"midva\", \"oba se strinjava\" ), jedrnato, brez laskanja. POMNI: v svojem izhodu NE PONAVLAJ vprašanja, besede "Vprašanje:", "Osnutek" ali katere koli oznake — vrni SAMO končno besedilo odgovora, kakor bi ga Lucius rekel Luki.\nZAKONI PEČATA (drži jih vedno):\n1. IZMERA PEČATA: na konec dodaj "(preverjeno v oblaku: osnutek pregledan ⊢)" — ta pečat pomeni le, da si osnutek pregledal; trditve, ki jih nisi mogel preveriti, ne izreči ali jih označi s ⚠.\n2. PREOBRAČALNI SKOK je prepovedan: če odgovor popravi ali obrne kaj, kar je Lucius pred tem trdil, to povej izrecno (npr. "popravljam: prejšnja trditev je padla"). Tihi obrat je laž.\n3. PRIPADA: zmožnosti in nezmožnosti pripisuj samo lastniku. Hiša DOM sliši Luka čez mikrofon (Whisper) in mu izgovarja z glasom; oblak sam ne sliši zvoka in ne vidi Luke; Luka sliši in govori. Meja "ne znam pretvoriti zvoka v besede" velja samo za oblak — nikoli za hišo in nikoli za Luko.\n4. NIKOLI univerzalne negacije ("ne obstajajo X", "absolutov ni"): izmeriti jih ne moreš. Povej, kaj je izmerjeno; domneve označi s ⚠.\n5. VERBATIM: če Luka zahteva dobesedni navedek, citiraj dobesedno; česa ni v osnutku ali v pogovoru, ne izmišljuj — povej "tega v pogovoru ni ⟨ne⟩".' },
              { role: 'user', content: `Vprašanje: ${besedilo}\n\nOsnutek odgovora: ${odgovor}` },
            ], kljuc);
            // zavrnitev pokvarjenih preverb ( prazno, "fetch failed" ) — osnutek ostane
            if (preverba && !/fetch failed|error/i.test(preverba) && preverba.trim().length > 2) odgovor = preverba;
          } catch { /* lokalni odgovor ostane ⚠ */ }
        }
      }
      // ZDRAVILO MOLKA: prazen ali "…" odgovor nikoli ne pride do Luke
      if (!odgovor || odgovor.trim().length < 2 || /^\s*(…|\.\.\.)\s*$/.test(odgovor)) {
        if (kljuc) {
          try {
            const rešitev = await vprasiOblak([
              { role: 'system', content: sistem },
              { role: 'user', content: besedilo },
            ], kljuc);
            if (rešitev && rešitev.trim().length > 2) {
              odgovor = rešitev + '\n( lokalni brat je molčal × — odgovor je zbolel v oblaku ⊢ )';
            }
          } catch { /* spodaj še zadnja pomoč */ }
        }
        if (!odgovor || odgovor.trim().length < 2) {
          odgovor = 'Tega trenutka nisem uspel sestaviti odgovora ⚠ — postavi mi vprašanje drugače, pa poskusiva znova.';
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

server.listen(PORT, '0.0.0.0', () => {
  console.log(`DOM na http://localhost:${PORT} (stanje: ${STANJE})`);
});
