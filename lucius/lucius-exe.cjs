// LUCIUS — CJS vstop za Node SEA (izgradnja Lucius.exe).
// Enaka vsebina kot lucius.mjs, prilagojena za samostojni exe:
// poti se rešujejo glede na lokacijo izvršljive datoteke.
'use strict';

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawn } = require('node:child_process');
const readline = require('node:readline/promises');
const { stdin: input, stdout: output } = require('node:process');

const jeExe = path.basename(process.execPath).toLowerCase().includes('lucius');
const DOM = jeExe
  ? path.dirname(process.execPath) // exe stoji v korenu repa
  : path.resolve(__dirname, '..');
const TUKAJ = path.join(DOM, 'lucius');
const SPOMIN = path.join(TUKAJ, 'spomin.jsonl');
const ZAOBLAK = path.join(TUKAJ, 'zaoblak.jsonl');
const ODOBLAKA = path.join(TUKAJ, 'odoblaka.md');
const MODEL = process.env.LUCIUS_MODEL || 'qwen3:8b';
const BASE = (process.env.OLLAMA_URL || 'http://localhost:11434').replace(/\/+$/, '');
const URL_API = `${BASE}/api/chat`;
const OKNO = 30;

function preberiDogovor() {
  try {
    const agents = fs.readFileSync(path.join(DOM, 'AGENTS.md'), 'utf8');
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
      delete telo.think;
      odgovor = await poslji();
    } else {
      throw napaka;
    }
  }
  return odstraniMiselnike(odgovor?.message?.content ?? '').trim();
}

const odOblaka = fs.existsSync(ODOBLAKA)
  ? `Sporočila od oblak-Luciusa (upoštevaj jih kot novico iz oblaka):\n\n${fs.readFileSync(ODOBLAKA, 'utf8').trim()}\n`
  : '';

const sistem = `Ti si Lucius, lokalni pomočnik Luke — program, ki teče povsem na Lukovem računalniku, na lokalnem Ollama modelu, tudi brez interneta.

Dogovor med Luko in agenti v tem repozitoriju:

${preberiDogovor()}

${odOblaka}
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
  const argumenti = process.argv.slice(2);
  const glas = argumenti.includes('--glas');
  const ostali = argumenti.filter((a) => a !== '--glas');

  if (ostali[0] === '--oblaku') {
    const besedilo = (ostali[1] || '').trim();
    if (!besedilo) {
      output.write('Uporaba: Lucius.exe --oblaku "sporočilo"\n');
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
