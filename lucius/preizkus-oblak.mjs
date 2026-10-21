// PREIZKUS-OBLAK — en sam majhen klic Mistral API, da se izmeri celotna veriga.
// Ključ se prebere iz datoteke; nikoli se ne izpiše.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const KLJUC = fs.readFileSync(path.join(HERE, 'api-kljuc.txt'), 'utf8').trim();
const UPORABA = path.join(HERE, 'api-uporaba.jsonl');

const odziv = await fetch('https://api.mistral.ai/v1/chat/completions', {
  method: 'POST',
  headers: { 'content-type': 'application/json', authorization: `Bearer ${KLJUC}` },
  body: JSON.stringify({
    model: 'mistral-small-latest',
    messages: [
      { role: 'user', content: 'Odgovori z natanko tremi besedami: preverba oblak uspešna.' },
    ],
    max_tokens: 20,
    temperature: 0,
  }),
});

if (!odziv.ok) {
  console.log('NAPAKA:', odziv.status, (await odziv.text()).slice(0, 200));
  process.exit(1);
}
const data = await odziv.json();
const u = data.usage ?? {};
fs.appendFileSync(UPORABA, JSON.stringify({
  ts: new Date().toISOString(),
  model: 'mistral-small-latest',
  vstop: u.prompt_tokens ?? 0,
  izstop: u.completion_tokens ?? 0,
}) + '\n', 'utf8');
console.log('ODGOVOR:', data.choices?.[0]?.message?.content?.trim());
console.log('zetoni:', u.prompt_tokens ?? 0, 'vstop +', u.completion_tokens ?? 0, 'izstop');
