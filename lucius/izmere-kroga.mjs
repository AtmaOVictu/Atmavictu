// IZMERE-KROGA — izmeri vsak skok pogovornega kroga in zapiе osnovo za
// primerjavo verzij (A → B → C …). Zagon: node lucius/izmere-kroga.mjs
// Izhod: lucius/izmere-kroga.jsonl (priča ⊢) + izpis na zaslon.
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DNEVNIK = path.join(HERE, 'izmere-kroga.jsonl');
const VZOREC = 'D:/OntoProjekt/Voice/klon/dataset/wavs/seg-0005.wav';

async function izmeri(ime, fn) {
  const t0 = Date.now();
  const izid = await fn();
  return { ime, ms: Date.now() - t0, izid };
}

const rezultati = [];

// 1. prepis (Whisper small, CPU)
if (fs.existsSync(VZOREC)) {
  const wav = fs.readFileSync(VZOREC);
  const r = await izmeri('prepis (slusaj)', async () => {
    const odg = await fetch('http://localhost:8766/api/slusaj', { method: 'POST', body: wav });
    const j = await odg.json();
    return j.ok ? (j.besedilo || '').slice(0, 40) : 'NAPAKA: ' + (j.napaka || '').slice(0, 60);
  });
  rezultati.push(r);
}

// 2. pogovor (Ollama + morebitna preverba v oblaku)
const r2 = await izmeri('pogovor (razmislek + preverba)', async () => {
  const odg = await fetch('http://localhost:8766/api/pogovor', {
    method: 'POST', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ besedilo: 'Reci v enem kratkem stavku: izmera poteka.' }),
  });
  const j = await odg.json();
  return j.ok ? (j.odgovor || '').slice(0, 40) : 'NAPAKA: ' + (j.napaka || '').slice(0, 60);
});
rezultati.push(r2);

const zapis = { ts: new Date().toISOString(), verzija: process.env.IZMERA_VERZIJA || 'A (osnova)', rezultati };
fs.appendFileSync(DNEVNIK, JSON.stringify(zapis) + '\n', 'utf8');
for (const r of rezultati) console.log(`${r.ime}: ${(r.ms / 1000).toFixed(1)} s ⊢ ${r.izid}`);
console.log('zapisano v izmere-kroga.jsonl ⊢');
