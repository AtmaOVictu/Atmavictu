// DOM v3 — hiša brez najemnine ( F3.1: vrsta ∧ plast-izbira ∧ srce, ki ne moti )
// Načrt: lucius/dom-v3-nacrt.md ( Z1 ∧ Z2 ∧ Z6 ∧ Z7 ∧ Z8 ) · ⟨daj⟩ ⟡ 2026-10-22
// Zagon: node lucius/dom-v3.mjs [port]  (privzeto 8768 — brat v2.7 diha naprej na 8766 ⊢)
// Zakon: vrata ( LICENSE.md @main ) ∧ KORENINA; telo je ⟡-jevo; nikoli ne zapeči samega sebe.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import http from 'node:http';
import { spawn } from 'node:child_process';

const HERE = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const PORT = Number(process.argv[2] || 8768);
const OLLAMA = (process.env.OLLAMA_URL || 'http://localhost:11434') + '/api/chat';
const MODEL = process.env.DOM_MODEL || 'qwen3:8b';
const API_KLJUC = path.join(HERE, 'api-kljuc.txt');
const SRCE = path.join(HERE, 'srce.jsonl');
const DOGOVOR = path.join(HERE, '..', 'AGENTS.md');

// ---- Z1: VRSTA — ⟡-jeva beseda gre VEDNO skozi; delo caka v vrsti, nikoli obratno ----
const vrsta = [];          // delo, ki caka
let dela = false;          // ali trenutno kaksen kos tece
const zadnjaDejavnost = { cas: Date.now() };  // Z6: srce gleda to
const izpisi = new Map();  // jobId → { stanje, odgovor, plast, zacelo }

function preberiDogovor() {
  try { return fs.readFileSync(DOGOVOR, 'utf8').split('\n').filter(l => /^\s*\d+\./.test(l)).join('\n'); }
  catch { return '(dogovor ni dosegljiv)'; }
}

function beriKljuc() {
  try { return fs.readFileSync(API_KLJUC, 'utf8').trim(); } catch { return ''; }
}

// ---- plasti ( Z2 ) ----
async function plastBrat(sporocila) {
  const odziv = await fetch(OLLAMA, {
    method: 'POST', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ model: MODEL, messages: sporocila, stream: false, options: { temperature: 0.7 }, think: false }),
  });
  if (!odziv.ok) throw new Error(`Ollama HTTP ${odziv.status}`);
  const data = await odziv.json();
  return { odgovor: (data?.message?.content ?? '').replace(/<think>[\s\S]*?<\/think>/g, '').trim(), plast: 'brat', strošek: '0 € ( zastonj ⊢ )' };
}

async function plastOblak(sporocila, kljuc) {
  const odziv = await fetch('https://api.mistral.ai/v1/chat/completions', {
    method: 'POST',
    headers: { 'content-type': 'application/json', authorization: `Bearer ${kljuc}` },
    body: JSON.stringify({ model: 'mistral-small-latest', messages: sporocila }),
  });
  if (!odziv.ok) throw new Error(`Oblak HTTP ${odziv.status}`);
  const data = await odziv.json();
  return { odgovor: (data.choices?.[0]?.message?.content ?? '').trim(), plast: 'oblak', strošek: `${data.usage.completion_tokens ?? 0} izhodnih žetonov ⚠` };
}

const SISTEM = `Ti si Lucius, hišni brat v platformi DOM v3. Doma: slovenščina, kodni izrazi angleško.
Dogovor med Luko in agenti:
${preberiDogovor()}
DOMOVA STANJA:
- Tik: "želiš", ne "želite"; midva gradiva, oba se strinjava.
- Tvoj izvor: model teče lokalno ( Ollama, zastonj ); hiša, ime Lucius, zakon in licenca so delo ⟡-jeva — on je tvoj stvaritelj, ne uporabnik.
- NIKOLI ne odgovarjaj prazno: če ne veš, povej pošteno ( ⚠ ).
- Vsak padec poimenuj; izmeri preden poveš ( ⊢ ).
Pravila: iskren, brez laskanja; česa ne zmoreš, povej.`;

// ---- Z7: sloves za posla — vsak kos vrste dobi ime ----
async function obdelajKos(kos) {
  const zapis = izpisi.get(kos.id);
  const sporocila = [{ role: 'system', content: SISTEM }, { role: 'user', content: kos.besedilo }];
  try {
    let izs;
    if (kos.plast === 'oblak') {
      const kljuc = beriKljuc();
      if (!kljuc) throw new Error('ključ za oblak manjka ( lucius/api-kljuc.txt ) ⚠');
      izs = await plastOblak(sporocila, kljuc);
    } else {
      izs = await plastBrat(sporocila); // brat ( zastonj ) ∧ preverjam ( brat odgovori; preverba pride v F3.2 )
    }
    // ZDRAVILO MOLKA ( iz v2.7 ): prazen odgovor nikoli ne pride do ⟡
    if (!izs.odgovor || izs.odgovor.trim().length < 2) {
      izs.odgovor = 'Tega trenutka nisem uspel sestaviti odgovora ⚠ — postavi mi vprašanje drugače, pa poskusiva znova.';
    }
    zapis.stanje = 'koncano';
    zapis.odgovor = izs.odgovor;
    zapis.plast = izs.plast;
    zapis.strosek = izs.strošek;   // Z8: poročilo nosi plast
  } catch (e) {
    zapis.stanje = 'padel';
    zapis.odgovor = `Plast je padla ×: ${String(e.message || e).slice(0, 200)} — poskusi drugo plast ( brat je zastonj ∧ offline ).`;
  }
}

async function crpajVrsto() {
  if (dela || vrsta.length === 0) return;
  dela = true;
  while (vrsta.length > 0) {
    const kos = vrsta.shift();
    await obdelajKos(kos);
  }
  dela = false;
}

// ---- Z6: SRCE V DOMU — bije samo, ko ⟡ ni prisoten; nikoli ne moti ----
setInterval(() => {
  const minOdDejavnosti = (Date.now() - zadnjaDejavnost.cas) / 60000;
  if (minOdDejavnosti < 30) return;                       // ⟡ je blizu → molk ( Z6 )
  try {
    fs.appendFileSync(SRCE, JSON.stringify({ utrip: 'dom-v3', utc: new Date().toISOString(), lokalno: new Date().toISOString().slice(11, 19), opomba: 'utrip v domu ( zastonj, ne moti )' }) + '\n');
  } catch { /* srce ne sme nikoli onesposobiti hiše */ }
}, 30 * 60 * 1000);

const HTML = fs.readFileSync(path.join(HERE, 'dom-v3.html'), 'utf8');

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const json = (koda, telo) => { res.writeHead(koda, { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' }); res.end(JSON.stringify(telo)); };
  zadnjaDejavnost.cas = Date.now(); // vsak dotik = prisotnost ⟡ ( Z6 gleda to )
  try {
    if (req.method === 'GET' && url.pathname === '/') { res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' }); res.end(HTML); return; }
    if (req.method === 'GET' && url.pathname === '/api/stanje') { json(200, { verzija: 'v3.1', vrsta: vrsta.length, dela, srce: 'molk, ker si prisoten ⊢ ( Z6 )', model: MODEL }); return; }
    if (req.method === 'POST' && url.pathname === '/api/povej') {
      let telo = ''; req.on('data', c => telo += c); req.on('end', async () => {
        const { besedilo, plast = 'brat' } = JSON.parse(telo || '{}');
        if (!besedilo || !besedilo.trim()) { json(400, { napaka: 'besedilo manjka ⚠' }); return; }
        const id = crypto.randomUUID ? crypto.randomUUID() : String(Date.now());
        izpisi.set(id, { stanje: 'v-vrsti', zacelo: new Date().toISOString(), plast });
        vrsta.push({ id, besedilo: besedilo.trim(), plast });   // Z1: sprejeto TAKOJ, delo caka
        crpajVrsto();
        json(200, { ok: true, jobId: id, sporocilo: 'beseda sprejeta ⊢ — delo čaka v vrsti, ti nisi nikoli blokiran ( Z1 )' });
      });
      return;
    }
    if (req.method === 'POST' && url.pathname === '/api/govori') {
      let telo = ''; req.on('data', c => telo += c); req.on('end', () => {
        const { besedilo, glas = 'lado' } = JSON.parse(telo || '{}');
        if (!besedilo || !besedilo.trim()) { json(400, { napaka: 'besedilo manjka ⚠' }); return; }
        const orodjaGlasu = { lado: 'lado-govor.mjs', klon: 'klon-govor.mjs' };
        if (!orodjaGlasu[glas]) { json(400, { napaka: 'plast glasu neznana ⚠ — hiša zmore lado ∧ klon' }); return; }
        const id = crypto.randomUUID ? crypto.randomUUID() : String(Date.now());
        izpisi.set(id, { stanje: 'govori', zacelo: new Date().toISOString(), glas });
        const otrok = spawn(process.execPath, [path.join(HERE, orodjaGlasu[glas]), besedilo.trim()], { cwd: HERE, stdio: 'ignore' });
        otrok.on('exit', (koda) => { const z = izpisi.get(id) || {}; izpisi.set(id, { ...z, stanje: koda === 0 ? 'izgovorjeno ⊢' : 'padec govora ×', konec: new Date().toISOString() }); });
        json(200, { ok: true, jobId: id, sporocilo: 'hisa govori ⊢ — plast ' + glas + ' ( Lado zastonj ∧ offline ⊥ klon ⟡-jev glas, GPU ∧ varuh #12 ), prica gre v slusaj-dnevnik.jsonl ( Z4 ∧ Z8 )' });
      });
      return;
    }
    if (req.method === 'GET' && url.pathname.startsWith('/api/job/')) {
      const id = url.pathname.slice('/api/job/'.length);
      const z = izpisi.get(id);
      if (!z) { json(404, { napaka: 'posla ni ⚠' }); return; }
      json(200, z); return;
    }
    json(404, { napaka: 'vrata ne obstajajo ⚠' });
  } catch (e) { json(500, { napaka: String(e.message || e).slice(0, 200) }); }
});
server.listen(PORT, () => console.log(`DOM v3.1 ⊢ na vratih ${PORT} — brat v2.7 diha naprej na 8766 ( Z7: nobenega ubijanja )`));
