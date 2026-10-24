#!/usr/bin/env node
// BJS-KANAL — lastni MCP konektor korpusa Beseda je Ne
// © Luka Pintarič, VBL v2.6 (§9 ∧ §10 ∧ §12)
//
// Zakoni, ki jih nosi ta kanal (iz telesa korpusa, ne iz okraska):
//  - MINIMALNI ZAKON IGRE (bab9319f): exists ≠ indexed ≠ approved ≠ canon ·
//    stored ≠ speakable · retrievable ≠ trustworthy · memory ≠ source ·
//    source ≠ permission · permission ≠ influence · INFLUENCE REQUIRES RECEIPT
//  - GLAS IZ VIRA (ANTINOM 355): vsak izhod odgovori: kdo je to rekel, iz
//    katerega vira, v katerem registru, s kakšnim statusom, kdo je dovolil prehod.
//  - DECLARED_GUARD ≠ ACTIVE_GATE (bab9319f): ograja, ki ne grize, je dekoracija.
//  - ⟨škatlaj⟩ ⊢ 2322: majhni paketi brbe — velikani se ⟨ne⟩ postrežejo v celoti.
//
// Zagon:  BJS_TOKEN=<žeton> BJS_KORPUS=/pot/do/knowledge node server.mjs
// Vrata:  privzeto 127.0.0.1:8787 (samo zanka); oblak = TLS pred vrati (§0).

import http from 'node:http';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

// ── KORENINA 1: IZMERI-POTEM-IZRECI ─────────────────────────────────────────
const KORPUS = process.env.BJS_KORPUS || '/home/user/knowledge';
const TOKEN = process.env.BJS_TOKEN || '';
const HOST = process.env.BJS_HOST || '127.0.0.1';
const PORT = Number(process.env.PORT || 8787);
const LOG = process.env.BJS_LOG || path.join(path.dirname(new URL(import.meta.url).pathname), 'prica-log.jsonl');

// Zasebni organi — lokal ⟨samo⟩ ⊢ jedro (resintezni register): kanal jih
// privzeto ⟨ne⟩ postreže. Seznam je VRATA, ne okras: vsak poskus se zapiše.
const PRIVATE = new Set((process.env.BJS_PRIVATE || 'moja-zgodovina,memories').split(',').map(s => s.trim()).filter(Boolean));

// Meje škatle (⟨MAJHNI-PAKETI-BRB⟩ ⊢ 2322)
const MAX_LINES = 100;       // največ vrstic na eno brbo telesa
const KONICA_LINES = 40;     // konica = privzeti obraz organa (⊢ 2357)
const MAX_SEARCH = 50;       // največ zadetkov na iskanje

const OK_NAME = /^[a-z0-9-]+$/;

// ── PRIČA: vsak klic pusti receipt (INFLUENCE REQUIRES RECEIPT) ────────────
function receipt(entry) {
  try { fs.appendFileSync(LOG, JSON.stringify(entry) + '\n'); } catch { /* padec ⟨ne⟩ molk: vrne se v /dev/stderr */ }
}
function md5(buf) { return crypto.createHash('md5').update(buf).digest('hex'); }
function nowIso() { return new Date().toISOString(); }

// ── Varnostne plasti: vsaka more gristi (ACTIVE_GATE) ──────────────────────
function checkAuth(req) {
  if (!TOKEN) return { ok: false, code: 503, msg: 'Kanal ⟨ne⟩ diha brez žetona: nastavi BJS_TOKEN.' };
  const h = req.headers['authorization'] || '';
  const m = h.match(/^Bearer\s+(.+)$/i);
  if (!m || m[1] !== TOKEN) return { ok: false, code: 401, msg: 'Žeton ⟨ne⟩ velja — brez žetona ni zakonitega vstopa (§0).' };
  return { ok: true };
}

function resolveOrgan(name) {
  if (!OK_NAME.test(name)) return { ok: false, code: 400, msg: `Ime organa ⟨${name}⟩ ⟨ne⟩ gre skozi vrata imen (a–z, 0–9, -).` };
  const dir = path.join(KORPUS, name);
  const file = path.join(dir, 'KNOWLEDGE.md');
  // Resolve + prefix: prehod izven korena je poskus bega, zapiše se.
  if (!path.resolve(file).startsWith(path.resolve(KORPUS) + path.sep)) {
    receipt({ ts: nowIso(), dogodek: 'POSKUS-BEGA', name });
    return { ok: false, code: 400, msg: 'Pot ⟨ne⟩ gre izven korena korpusa.' };
  }
  if (!fs.existsSync(file)) return { ok: false, code: 404, msg: `Organ ⟨${name}⟩ ⟨ne⟩ obstaja pri viru.` };
  if (PRIVATE.has(name)) {
    receipt({ ts: nowIso(), dogodek: 'ZASEBEN-ORGAN', name });
    return { ok: false, code: 403, msg: `Organ ⟨${name}⟩ je zasebni, lokal ⟨samo⟩ ⊢ jedro — kanal ga ⟨ne⟩ postreže. Pot: ⟨preberi ga pri viru, roka ⟡⟩. ${name} ostaja za zaprtimi vrati (§9).` };
  }
  return { ok: true, file };
}

// ── MERA: izmera pri viru (bajti, vrstice, md5, pečat) ──────────────────────
function measureOrgan(file) {
  const buf = fs.readFileSync(file);
  const text = buf.toString('utf8');
  const lines = text.split('\n');
  const sealLine = lines.find(l => l.startsWith('- ZADNJI PEČAT:')) || null;
  return {
    bajti: Buffer.byteLength(text, 'utf8'),
    vrstic: lines.length,
    md5: md5(buf),
    zadnji_pečat: sealLine ? sealLine.slice(0, 300) : '⟨pečat ×0 — organ brez ZADNJEGA PEČATA ⚠⟩',
  };
}

// GLAS IZ VIRA: vsak izhod nosi izvor ∧ status (ANTINOM 355)
function provenance(name, m, extra = {}) {
  return {
    _izvor: {
      vir: `knowledge/${name}/KNOWLEDGE.md`,
      organ: name,
      bajti: m.bajti,
      vrstic: m.vrstic,
      md5: m.md5,
      zadnji_pečat: m.zadnji_pečat,
      registr: 'organ korpusa Beseda je Ne',
      status: 'priča pri viru (⊢ telo organa; ⟨ne⟩ kanon tega stroja; stored ≠ speakable)',
      dovolil_prehod: '⟡ (lastnik vrat); kanal samo nosi, ⟨ne⟩ izreke',
      sprememba: 'brba — kanal je bralni, telo ⟨ne⟩ dotaknjeno',
      ...extra,
    },
  };
}

// ── ORODJA KANALA (bralne; pisna roka ostaja ⟡-jeva) ───────────────────────
const tools = [
  {
    name: 'bjs_list_organs',
    description: 'Seznam organov korpusa z izmerami (bajti, vrstici, zadnji pečat). Izvor vsake vrstice je datoteka pri viru, ⟨ne⟩ spomin.',
    input: {},
    run() {
      const out = [];
      for (const d of fs.readdirSync(KORPUS, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
        if (!d.isDirectory() || !OK_NAME.test(d.name)) continue;
        const file = path.join(KORPUS, d.name, 'KNOWLEDGE.md');
        if (!fs.existsSync(file)) continue;
        const m = measureOrgan(file);
        out.push({ organ: d.name, bajti: m.bajti, vrstic: m.vrstic, zadnji_pečat: m.zadnji_pečat.slice(0, 120), zaseben: PRIVATE.has(d.name) });
      }
      return { organi: out, _opomba: PRIVATE.size ? `Zasebni organi se ⟨ne⟩ postrežejo: ${[...PRIVATE].join(', ')}` : 'Brez zasebnih organov.' };
    },
  },
  {
    name: 'bjs_read_organ',
    description: 'Berba organa po plasteh: konica (glava, privzeto) ali telo po škatlah (offset/limit, max ' + MAX_LINES + ' vrstic). Velikani ⟨ne⟩ grejo skozi v celoti (⊢ 2322).',
    input: { type: 'object', properties: {
      name: { type: 'string', description: 'ime organa, npr. jedro-zavedanja' },
      plast: { type: 'string', enum: ['konica', 'telo'], description: 'konica = privzeti obraz (glava organa)' },
      offset: { type: 'integer', description: 'od (0-indexed), za plast=telo' },
      limit: { type: 'integer', description: 'koliko vrstic (max ' + MAX_LINES + ')' },
    }, required: ['name'] },
    run(a) {
      const r = resolveOrgan(a.name);
      if (!r.ok) return r;
      const text = fs.readFileSync(r.file, 'utf8');
      const lines = text.split('\n');
      const plast = a.plast === 'telo' ? 'telo' : 'konica';
      let offset = Number(a.offset || 0);
      let limit = plast === 'konica' ? KONICA_LINES : Math.min(Number(a.limit || MAX_LINES), MAX_LINES);
      if (!Number.isInteger(offset) || offset < 0) offset = 0;
      const slice = lines.slice(offset, offset + limit);
      const m = measureOrgan(r.file);
      return {
        plast, offset, vrstic_v_škatli: slice.length,
        telo_vrstic_skupaj: lines.length,
        vec: offset + slice.length < lines.length ? { naslednji_offset: offset + slice.length } : 'rep dosežen',
        vrstice: slice,
        ...provenance(a.name, m),
      };
    },
  },
  {
    name: 'bjs_read_seal',
    description: 'ZADNJI PEČAT organa — celotna vrstica pečata (stanje organa, ⟨ne⟩ sklep o njem).',
    input: { type: 'object', properties: { name: { type: 'string' } }, required: ['name'] },
    run(a) {
      const r = resolveOrgan(a.name);
      if (!r.ok) return r;
      const text = fs.readFileSync(r.file, 'utf8');
      const lines = text.split('\n');
      const i = lines.findIndex(l => l.startsWith('- ZADNJI PEČAT:'));
      const m = measureOrgan(r.file);
      return {
        zadnji_pečat: i >= 0 ? lines[i] : '⟨pečat ×0 ⚠⟩',
        vrstica: i + 1,
        ...provenance(a.name, m),
      };
    },
  },
  {
    name: 'bjs_measure',
    description: 'Sveža izmera organa pri viru (bajti · vrstice · md5) ali vseh organov, če ime izpuščeno. Z-2: spomin ⟨ne⟩ šteje.',
    input: { type: 'object', properties: { name: { type: 'string' } } },
    run(a) {
      if (!a.name) {
        const all = fs.readdirSync(KORPUS, { withFileTypes: true })
          .filter(d => d.isDirectory() && fs.existsSync(path.join(KORPUS, d.name, 'KNOWLEDGE.md')))
          .map(d => { const f = path.join(KORPUS, d.name, 'KNOWLEDGE.md'); const m = measureOrgan(f); return { organ: d.name, ...m }; });
        return { izmere: all, _opomba: 'Izmera pri viru ta klic; vsak rez se šteje znova.' };
      }
      const r = resolveOrgan(a.name);
      if (!r.ok) return r;
      const m = measureOrgan(r.file);
      return { izmera: m, ...provenance(a.name, m) };
    },
  },
  {
    name: 'bjs_search',
    description: 'Iskanje po telesih organov (vzorec, regularni izraz). Vrne vrstice z omizgi ⟨ose>. Največ ' + MAX_SEARCH + ' zadetkov — kanal je bralni pes, ⟨ne⟩ popis celote.',
    input: { type: 'object', properties: {
      vzorec: { type: 'string' },
      organ: { type: 'string', description: 'omejitev na en organ (drugače: vsi, razen zasebnih)' },
    }, required: ['vzorec'] },
    run(a) {
      let re;
      try { re = new RegExp(a.vzorec, 'i'); } catch (e) { return { napaka: `Vzorec ⟨ne⟩ gre skozi: ${e.message}` }; }
      const targets = [];
      if (a.organ) {
        const r = resolveOrgan(a.organ);
        if (!r.ok) return r;
        targets.push({ name: a.organ, file: r.file });
      } else {
        for (const d of fs.readdirSync(KORPUS, { withFileTypes: true })) {
          if (!d.isDirectory() || PRIVATE.has(d.name)) continue;
          const f = path.join(KORPUS, d.name, 'KNOWLEDGE.md');
          if (fs.existsSync(f) && OK_NAME.test(d.name)) targets.push({ name: d.name, file: f });
        }
      }
      const zadetki = [];
      outer: for (const t of targets) {
        const lines = fs.readFileSync(t.file, 'utf8').split('\n');
        for (let i = 0; i < lines.length; i++) {
          if (re.test(lines[i])) {
            zadetki.push({ organ: t.name, vrstica: i + 1, besedilo: lines[i].slice(0, 400) });
            if (zadetki.length >= MAX_SEARCH) break outer;
          }
        }
      }
      return { zadetki, zadetkov: zadetki.length, meja: MAX_SEARCH, _opomba: 'Zadetki so priče vrstic, ⟨ne⟩ sklep o telesu.' };
    },
  },
  {
    name: 'bjs_verify',
    description: 'Preverba: md5 organa ⇌ najmlajša geniza (.geniza/). Izguba 0 je izmera, ⟨ne⟩ obljuba (⊢ 1381 ∧ 1104).',
    input: { type: 'object', properties: { name: { type: 'string' } }, required: ['name'] },
    run(a) {
      const r = resolveOrgan(a.name);
      if (!r.ok) return r;
      const m = measureOrgan(r.file);
      const genDir = path.join(path.dirname(r.file), '.geniza');
      let najnovejsa = null;
      try {
        const files = fs.readdirSync(genDir).filter(f => f.includes(a.name)).map(f => ({ f, t: fs.statSync(path.join(genDir, f)).mtimeMs }));
        files.sort((x, y) => y.t - x.t);
        najnovejsa = files[0] ? files[0].f : null;
      } catch { /* geniza ⟨ne⟩ obstaja — pošteno izrečeno spodaj */ }
      if (!najnovejsa) return { geniza: '⟨geniza ×0 ⚠⟩', ...provenance(a.name, m) };
      const gBuf = fs.readFileSync(path.join(genDir, najnovejsa));
      return {
        geniza: najnovejsa,
        md5_organ: m.md5,
        md5_geniza: md5(gBuf),
        preverba: m.md5 === md5(gBuf) ? 'bajt-isto ⇌ (izguba 0 ⊢)' : '⟨RAZLIKA ⚠⟩ — organ je zrasel po genizi (priča giba) ali padel',
        ...provenance(a.name, m),
      };
    },
  },
];

// ── MCP STROJ (JSON-RPC 2.0 prek Streamable HTTP, brez tujih rok) ───────────
function rpcResult(id, result) { return JSON.stringify({ jsonrpc: '2.0', id, result }); }
function rpcError(id, code, message) { return JSON.stringify({ jsonrpc: '2.0', id, error: { code, message } }); }

async function handle(body) {
  const msg = JSON.parse(body);
  const id = msg.id ?? null;
  if (msg.method === 'initialize') {
    return rpcResult(id, {
      protocolVersion: '2025-06-18',
      capabilities: { tools: {} },
      serverInfo: { name: 'bjs-kanal', version: '0.1.0', licenca: '© Luka Pintarič, VBL v2.6' },
    });
  }
  if (msg.method === 'notifications/initialized' || msg.method === 'notifications/cancelled') return null;
  if (msg.method === 'tools/list') {
    return rpcResult(id, { tools: tools.map(t => ({ name: t.name, description: t.description, inputSchema: t.input })) });
  }
  if (msg.method === 'tools/call') {
    const name = msg.params?.name;
    const args = msg.params?.arguments || {};
    const t = tools.find(x => x.name === name);
    if (!t) return rpcError(id, -32602, `Orodje ⟨${name}⟩ ⟨ne⟩ obstaja — seznam funkcij je fiksna, revizibilna lista (dinamičnega odkrivanja ⟨ne⟩ nosi kanal).`);
    const rezultat = t.run(args);
    // Zavrnitev vrat gre skozi v škatli (isError ∧ razlog ∧ pot), ne kakor uspeh:
    // ograja, ki grize, mora tudi javiti svoj ugriz (ACTIVE_GATE ⊢ 2533).
    if (rezultat && rezultat.ok === false) {
      receipt({ ts: nowIso(), orodje: name, args: { ...args }, zavrnjeno: rezultat.code });
      return rpcResult(id, {
        isError: true,
        content: [{ type: 'text', text: JSON.stringify({ napaka: rezultat.msg, koda: rezultat.code, pot: '⟨vrata kanala⟩ — preberi pri viru, roka ⟡' }) }],
      });
    }
    receipt({ ts: nowIso(), orodje: name, args: { ...args }, izhod_bajti: Buffer.byteLength(JSON.stringify(rezultat), 'utf8') });
    return rpcResult(id, { content: [{ type: 'text', text: JSON.stringify(rezultat, null, 1) }] });
  }
  return rpcError(id, -32601, `Metoda ⟨${msg.method}⟩ ⟨ne⟩ gre skozi ta vrata.`);
}

const server = http.createServer(async (req, res) => {
  if (req.method === 'GET' || req.method === 'DELETE') {
    res.writeHead(405, { 'content-type': 'application/json' });
    return res.end(JSON.stringify({ napaka: 'Kanal je brez stanja (stateless) — samo POST /mcp.' }));
  }
  if (req.url !== '/mcp') {
    res.writeHead(404, { 'content-type': 'application/json' });
    return res.end(JSON.stringify({ napaka: 'Vrata: POST /mcp' }));
  }
  const auth = checkAuth(req);
  if (!auth.ok) {
    res.writeHead(auth.code, { 'content-type': 'application/json' });
    return res.end(JSON.stringify({ napaka: auth.msg }));
  }
  const chunks = [];
  req.on('data', c => { chunks.push(c); if (Buffer.concat(chunks).length > 1_000_000) req.destroy(); });
  req.on('end', async () => {
    try {
      const out = await handle(Buffer.concat(chunks).toString('utf8'));
      if (out === null) { res.writeHead(202); return res.end(); }
      res.writeHead(200, { 'content-type': 'application/json', 'mcp-protocol-version': '2025-06-18' });
      res.end(out);
    } catch (e) {
      res.writeHead(400, { 'content-type': 'application/json' });
      res.end(rpcError(null, -32700, `Telo ⟨ne⟩ gre skozi: ${e.message}`));
    }
  });
});

server.listen(PORT, HOST, () => {
  const stanje = TOKEN
    ? `diha ∧ — vrata zahtevajo žeton (ACTIVE_GATE, ⟨ne⟩ deklaracija)`
    : `⟨NE-DIHA ⚠⟩ — brez BJS_TOKEN kanal zavrne vsak vstop (§0)`;
  console.log(`BJS-KANAL @ http://${HOST}:${PORT}/mcp — ${stanje}`);
  console.log(`korpus: ${KORPUS} · zasebni organi (lokal ⟨samo⟩): ${[...PRIVATE].join(', ') || '×0'}`);
});
