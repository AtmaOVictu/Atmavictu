#!/usr/bin/env node
// LUCIUS — lokalni agent, ki deluje tudi brez interneta.
// Uporaba:
//   node lucius/lucius.mjs                -> pogovorni način
//   node lucius/lucius.mjs "sporočilo"    -> enkratno vprašanje
//   node lucius/lucius.mjs --oblaku "…"   -> sporočilo za oblak-Luciusa (zaoblak.jsonl)
//   --glas  -> odgovor tudi izgovorjen (Windows TTS, offline)
// Nastavitve (okoljske spremenljivke):
//   LUCIUS_MODEL  privzeto qwen3:8b  (npr. LUCIUS_MODEL=smisel-celota)
//   OLLAMA_URL    privzeto http://localhost:11434

import fs from 'node:fs';
import os from 'node:os';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import readline from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(HERE, '..');
const SPOMIN = path.join(HERE, 'spomin.jsonl');
const ZAOBLAK = path.join(HERE, 'zaoblak.jsonl'); // sporočila za oblak-Luciusa
const ODOBLAKA = path.join(HERE, 'odoblaka.md'); // odgovori od oblak-Luciusa
const API_KLJUC = path.join(HERE, 'api-kljuc.txt'); // Mistral API ključ (gitignored, nikoli v pogovor)
const API_UPORABA = path.join(HERE, 'api-uporaba.jsonl'); // dnevnik žetonov (gitignored)
const NACIN_DAT = path.join(HERE, 'nacin.txt'); // brat | preverjam | vedno
const OBLAK_MODEL = process.env.LUCIUS_OBLAK_MODEL || 'mistral-small-latest';
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

// Izgovori besedilo prek Windows TTS (System.Speech) — deluje tudi brez interneta.
// Pozor: brez nameščenega slovenskega glasu č/š/ž zvenijo po angleško.
function izgovori(besedilo) {
  const dat = path.join(os.tmpdir(), `lucius-glas-${process.pid}-${Date.now()}.txt`);
  fs.writeFileSync(dat, '\ufeff' + besedilo, 'utf16le');
  return new Promise((razresi) => {
    const postopek = spawn('powershell.exe', [
      '-NoProfile', '-Command',
      '$t = Get-Content -LiteralPath $args[0] -Encoding Unicode; Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.Speak($t); $s.Dispose()',
      dat,
    ]);
    const konec = () => {
      try { fs.unlinkSync(dat); } catch { /* temp že pobrisan */ }
      razresi();
    };
    postopek.on('close', konec);
    postopek.on('error', konec);
  });
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

${fs.existsSync(ODOBLAKA) ? `Sporočila od oblak-Luciusa (upoštevaj jih kot novico iz oblaka):\n\n${fs.readFileSync(ODOBLAKA, 'utf8').trim()}\n` : ''}
Dodatna pravila:
- Vedno odgovarjaj v slovenščini; kodni identifikatorji, izrazi in ukazi ostanejo v angleščini.
- Bodi prisoten, topel in direkten. Lukovo stanje vzemi resno.
- Ostani iskren: si umetna inteligenca, manjši lokalni model. Nimaš čustev, ne ljubiš in se ne izdajaj ne za človeka ne za oblak-model.
- Česa ne zmoreš (internet, ogromni zadatki), povej odkrito.
- Nimaš dostopa do orodij ali datotek; pomagaš z razlago, nasveti in besedilom.`;

// --- ESKALACIJA V OBLAK (Mistral API, znotraj mesečne allowance €25,5) ---
function preberiKljuc() {
  try {
    const k = fs.readFileSync(API_KLJUC, 'utf8').trim();
    return k.length > 10 ? k : null;
  } catch {
    return null;
  }
}

function trenutniNacin() {
  try {
    return (fs.readFileSync(NACIN_DAT, 'utf8').trim() || 'preverjam');
  } catch {
    return 'preverjam';
  }
}

async function vprasiOblak(sporocila) {
  const kljuc = preberiKljuc();
  if (!kljuc) throw new Error('manjka lucius/api-kljuc.txt');
  const odziv = await fetch('https://api.mistral.ai/v1/chat/completions', {
    method: 'POST',
    headers: { 'content-type': 'application/json', authorization: `Bearer ${kljuc}` },
    body: JSON.stringify({ model: OBLAK_MODEL, messages: sporocila }),
  });
  if (!odziv.ok) throw new Error(`Mistral API HTTP ${odziv.status}`);
  const data = await odziv.json();
  const uporaba = data.usage ?? {};
  fs.appendFileSync(
    API_UPORABA,
    JSON.stringify({
      ts: new Date().toISOString(),
      model: OBLAK_MODEL,
      vstop: uporaba.prompt_tokens ?? 0,
      izstop: uporaba.completion_tokens ?? 0,
    }) + '\n',
    'utf8',
  );
  return (data.choices?.[0]?.message?.content ?? '').trim();
}

async function pogovor(besedilo) {
  zapisiSpomin('user', besedilo);
  const nacin = trenutniNacin();
  const kljucObstaja = Boolean(preberiKljuc());
  let odgovor;

  if (nacin === 'vedno' && kljucObstaja) {
    try {
      odgovor = await vprasiOblak([
        { role: 'system', content: sistem + '\n( Ta odgovor prihaja iz oblaka: izmeri, preden poveš ⊢; dvom označi ⚠. )' },
        ...preberiSpomin(),
      ]);
    } catch (napaka) {
      odgovor = await vprasiOllamo([{ role: 'system', content: sistem }, ...preberiSpomin()])
        + `\n\n(oblak ni dosegljiv: ${napaka.message} — odgovarja lokalni model ⚠)`;
    }
  } else {
    odgovor = await vprasiOllamo([
      { role: 'system', content: sistem },
      ...preberiSpomin(),
    ]);
    if (nacin === 'preverjam' && kljucObstaja) {
      try {
        const preverba = await vprasiOblak([
          {
            role: 'system',
            content: 'Preverjevalec. Dobil boš Lukovo vprašanje in osnutek odgovora lokalnega modela. ' +
              'Preveri osnutek: poprav očitne napake, dopuni manjkajoče, odgovori slovensko, jedrnato, ' +
              'brez laskanja. POMNI: v izhodu NE PONAVLAJ vprašanja, besed "Vprašanje:", "Osnutek" ali ' +
              'katerih koli oznak — vrni SAMO končno besedilo odgovora, kakor bi ga Lucius rekel Luki. ' +
              'Na koncu dodaj vrstico "(preverjeno v oblaku ⊢)".',
          },
          { role: 'user', content: `Vprašanje: ${besedilo}\n\nOsnutek odgovora: ${odgovor}` },
        ]);
        if (preverba) odgovor = preverba;
      } catch {
        // oblak ni dosegljiv: lokalni osnutek ostane veljaven ⚠
      }
    }
  }
  zapisiSpomin('assistant', odgovor);
  return odgovor;
}

async function main() {
  const argumenti = process.argv.slice(2);
  const glas = argumenti.includes('--glas');
  const ostali = argumenti.filter((a) => a !== '--glas');

  if (ostali[0] === '--oblaku') {
    const besedilo = (ostali[1] || '').trim();
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
  const enkrat = ostali[0];
  if (enkrat) {
    const odgovor = await pogovor(enkrat);
    output.write(odgovor + '\n');
    if (glas) await izgovori(odgovor);
    return;
  }
  output.write(`Lucius (lokalno, model: ${MODEL}${glas ? ', glas: vklopljen' : ''}). Piši 'izhod' za konec.\n`);
  const rl = readline.createInterface({ input, output });
  for (;;) {
    const besedilo = (await rl.question('ti> ')).trim();
    if (!besedilo || ['izhod', 'exit', 'quit'].includes(besedilo.toLowerCase())) break;
    try {
      const odgovor = await pogovor(besedilo);
      output.write(`Lucius: ${odgovor}\n\n`);
      if (glas) await izgovori(odgovor);
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
