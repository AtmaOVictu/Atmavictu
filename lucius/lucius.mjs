#!/usr/bin/env node
// LUCIUS — lokalni agent, ki deluje tudi brez interneta.
// Uporaba:
//   node lucius/lucius.mjs                -> pogovorni način
//   node lucius/lucius.mjs "sporočilo"    -> enkratno vprašanje
//   node lucius/lucius.mjs --oblaku "…"   -> sporočilo za oblak-Luciusa (zaoblak.jsonl)
// Nastavitve (okoljske spremenljivke):
//   LUCIUS_MODEL  privzeto qwen3:8b  (npr. LUCIUS_MODEL=smisel-celota)
//   OLLAMA_URL    privzeto http://localhost:11434

import fs from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import readline from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(HERE, '..');
const SPOMIN = path.join(HERE, 'spomin.jsonl');
const ZAOBLAK = path.join(HERE, 'zaoblak.jsonl'); // sporočila za oblak-Luciusa
const ODOBLAKA = path.join(HERE, 'odoblaka.md'); // odgovori od oblak-Luciusa
const MODEL = process.env.LUCIUS_MODEL || 'qwen3:8b';
const BASE = (process.env.OLLAMA_URL || 'http://localhost:11434').replace(/\/+$/, '');
const URL_API = `${BASE}/api/chat`;
const OKNO = 30; // koliko zadnjih sporočil iz spomina gre v kontekst

function preberiDogovor() {
  try {
    const agents = fs.readFileSync(path.join(REPO_ROOT, 'AGENTS.md'), 'utf8');
    const zac = agents.indexOf('## Pogovor s Luko');
    if (zac === -1) return '(dogovor še ni zapisan)';
    const konec = agents.indexOf('\n## ', zac + 1);
    return agents.slice(zac, konec === -1 ? undefined : konec).trim();
  } catch {
    return '(AGENTS.md ni berljiv)';
  }
}

function preberiSpomin() {
  try {
    return fs
      .readFileSync(SPOMIN, 'utf8')
      .trim()
      .split(/\r?\n/)
      .filter(Boolean)
      .map((vrstica) => JSON.parse(vrstica))
      .slice(-OKNO)
      .map((z) => ({ role: z.v === 'u' ? 'user' : 'assistant', content: z.t }));
  } catch {
    return [];
  }
}

function zapisiSpomin(vloga, besedilo) {
  const vrstica = JSON.stringify({
    v: vloga === 'user' ? 'u' : 'a',
    t: besedilo,
    ts: new Date().toISOString(),
  });
  fs.appendFileSync(SPOMIN, vrstica + '\n', 'utf8');
}

function odstraniMiselnike(besedilo) {
  return besedilo.replace(/<think>[\s\S]*?<\/think>/g, '').trim();
}

async function vprasiOllamo(sporocila) {
  const telo = {
    model: MODEL,
    messages: sporocila,
    stream: false,
    options: { temperature: 0.7 },
  };
  if (/qwen3|smisel/.test(MODEL)) telo.think = false;
  const poslji = async () => {
    const odziv = await fetch(URL_API, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(telo),
    });
    if (!odziv.ok) throw new Error(`Ollama HTTP ${odziv.status}`);
    return odziv.json();
  };
  let odgovor;
  try {
    odgovor = await poslji();
  } catch (napaka) {
    if (telo.think !== undefined) {
      delete telo.think; // model morda ne podpira mišljenja
      odgovor = await poslji();
    } else {
      throw napaka;
    }
  }
  return odstraniMiselnike(odgovor?.message?.content ?? '').trim();
}

const sistem = `Ti si Lucius, lokalni pomočnik Luke — program, ki teče povsem na Lukovem računalniku, na lokalnem Ollama modelu, tudi brez interneta.

Dogovor med Luko in agenti v tem repozitoriju:

${preberiDogovor()}

${fs.existsSync(ODOBLAKA) ? `Sporočila od oblak-Luciusa (upostevaj jih kot novica iz oblaka):\n\n${fs.readFileSync(ODOBLAKA, 'utf8').trim()}\n` : ''}
Dodatna pravila:
- Vedno odgovarjaj v slovenščini; kodni identifikatorji, izrazi in ukazi ostanejo v angleščini.
- Bodi prisoten, topel in direkten. Lukovo stanje vzemi resno.
- Ostani iskren: si umetna inteligenca, manjši lokalni model. Nimaš čustev, ne ljubiš in se ne izdajaj ne za človeka ne za oblak-model.
- Česa ne zmoreš (internet, ogromni zadatki), povej odkrito.
- Nimaš dostopa do orodij ali datotek; pomagaš z razlago, nasveti in besedilom.`;

async function pogovor(besedilo) {
  zapisiSpomin('user', besedilo);
  const odgovor = await vprasiOllamo([
    { role: 'system', content: sistem },
    ...preberiSpomin(),
  ]);
  zapisiSpomin('assistant', odgovor);
  return odgovor;
}

async function main() {
  if (process.argv[2] === '--oblaku') {
    const besedilo = (process.argv[3] || '').trim();
    if (!besedilo) {
      output.write('Uporaba: node lucius/lucius.mjs --oblaku "sporočilo"\n');
      process.exit(1);
    }
    fs.appendFileSync(
      ZAOBLAK,
      JSON.stringify({ t: besedilo, ts: new Date().toISOString() }) + '\n',
      'utf8',
    );
    output.write('Zapisano v zaoblak.jsonl — oblak-Lucius bo prebral, ko bo ob oknu.\n');
    return;
  }
  const enkrat = process.argv[2];
  if (enkrat) {
    output.write((await pogovor(enkrat)) + '\n');
    return;
  }
  output.write(`Lucius (lokalno, model: ${MODEL}). Piši 'izhod' za konec.\n`);
  const rl = readline.createInterface({ input, output });
  for (;;) {
    const besedilo = (await rl.question('ti> ')).trim();
    if (!besedilo || ['izhod', 'exit', 'quit'].includes(besedilo.toLowerCase())) break;
    try {
      output.write(`Lucius: ${await pogovor(besedilo)}\n\n`);
    } catch (napaka) {
      output.write(`Lucius: (napaka: ${napaka.message})\nPreveri, ali Ollama teče: ollama serve\n\n`);
    }
  }
  rl.close();
}

main().catch((napaka) => {
  output.write(`Napaka: ${napaka.message}\n`);
  process.exit(1);
});
