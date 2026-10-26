#!/usr/bin/env node
// LINIJA-MOST — most mer iz oblaka v okno LUCIUS (linija zaupanja), rez 2807.
// Pot, ki jo rešuje: ⟡ ukaz 24. 10. 2026 ⊢ pečat 2633:
//   »poročilo se vrne k meni na lokalni računalnik v kontrolni center linija zaupanja lucius«
//   — ⟨daj⟩ ⊢ VEČNI-DAJ (16) ∧ AD-PERPETUUM ⊢ 2201 ∧ ukaz-dovol ⊢ 1429.1 ∧ 1237 ∧ 1448.
// Potek: P2 ⟨MOST-V-OKNO⟩ — skript potegne poročila ∧ most s repa na lokalni disk hiše;
//   telo okna živi lokalno pri ⟡ (skrito okno ⊙ 1349) ∧ ⟨ne⟩ na repu ⚠.
// Pravilo 14 (AGENTS.md): most ∧ spomin ∧ dnevnik IZVEN gita — runtime datoteke
//   (linija.jsonl · linija-dostavljeno.json · linija-most-dnevnik.jsonl) so v .gitignore.
// ⟨NE-BRIŠI⟩ ⊢ 24: stanje dostav se samo vejalo dodaja, nikoli brisalo; brez dvojnikov.
// Skrivnosti: skript jih ⟨ne⟩ pozna — javni rep, brez žetona. K1: prevoznik meri, ne prešoja.
// Zagon: node lucius/linija-most.mjs  (Node 18+, brez odvisnosti;
//   obrat v cikel.jsonl zapiše lokalni pogon — oblak ⟨ne⟩ piše v cikel ⚠.)

import { appendFile, mkdir, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const REPO = 'AtmaOVictu/Atmavictu';
const SEZNAM_URL = 'https://api.github.com/repos/' + REPO + '/contents/lucius/porocila';
const MOST_URL = 'https://raw.githubusercontent.com/' + REPO + '/main/lucius/MOST-MERE-LUCIJU.md';
const LOKAL = join(process.cwd(), 'lucius');
const DOSTAVLJENO = join(LOKAL, 'linija-dostavljeno.json');        // ⟨NE-BRIŠI⟩ — brez dvojnikov
const TOK = join(LOKAL, 'linija.jsonl');                            // JSONL tok za kontrolni center
const ODOBLAKA = join(LOKAL, 'odoblaka.md');                       // novice, ki jih DOM že bere ⊢
const DNEVNIK = join(LOKAL, 'linija-most-dnevnik.jsonl');          // priča pogona

async function pojdi(url, vrsta) {
  const odgovor = await fetch(url, { headers: { 'User-Agent': 'linija-most-v1' } });
  if (odgovor.status === 403) { throw new Error('GitHub prag 60 klicov/h ⚠'); }
  if (!odgovor.ok) { throw new Error('⟨ne⟩ — vrata ' + String(odgovor.status) + ' ⚠'); }
  return vrsta === 'json' ? await odgovor.json() : await odgovor.text();
}

async function beriStanje() {
  try { return JSON.parse(await readFile(DOSTAVLJENO, 'utf8')); }
  catch (e) { return []; } // prvi pogon — seznam dostav prazen
}

async function main() {
  await mkdir(LOKAL, { recursive: true });
  const stanje = await beriStanje();
  const videti = new Set(stanje.map(function (v) { return v.ime; }));

  // 1. seznam poročil pri viru
  const seznam = await pojdi(SEZNAM_URL, 'json');
  const dostave = [];
  for (const v of seznam) {
    if (!v || typeof v.name !== 'string' || !v.download_url) { continue; }
    if (videti.has(v.name)) { continue; } // brez dvojnikov
    const telo = await pojdi(v.download_url, 'text');
    dostave.push({ vrsta: 'porocilo', ime: v.name, bajti: telo.length, telo: telo });
    stanje.push({ ime: v.name, bajti: telo.length, ts: new Date().toISOString() });
    videti.add(v.name);
  }

  // 2. most — dostavljen vsakic, ko se bajti spremenijo
  const mostTelo = await pojdi(MOST_URL, 'text');
  const zadnjiMost = stanje.filter(function (v) { return v.ime === 'MOST-MERE-LUCIJU.md'; }).pop();
  if (!zadnjiMost || zadnjiMost.bajti !== mostTelo.length) {
    dostave.push({ vrsta: 'most', ime: 'MOST-MERE-LUCIJU.md', bajti: mostTelo.length, telo: mostTelo });
    stanje.push({ ime: 'MOST-MERE-LUCIJU.md', bajti: mostTelo.length, ts: new Date().toISOString() });
  }

  // 3. dostave V OBEH kanalih hiše: odoblaka.md (DOM bere ⊢) ∧ linija.jsonl (kontrolni center)
  for (const d of dostave) {
    const vrstica = { ts: new Date().toISOString(), vrsta: d.vrsta, ime: d.ime, bajti: d.bajti, telo: d.telo };
    await appendFile(TOK, JSON.stringify(vrstica) + '\n', 'utf8');
    await appendFile(ODOBLAKA, '\n## ' + d.ime + ' (' + String(d.bajti) + ' B) — linija-most\n\n' + d.telo + '\n', 'utf8');
  }

  // 4. stanje dostavljenega — ⟨NE-BRIŠI⟩ ⊢ 24
  await writeFile(DOSTAVLJENO, JSON.stringify(stanje, null, 2) + '\n', 'utf8');

  // 5. priča pogona
  const stevilo = Array.isArray(seznam) ? seznam.length : 0;
  await appendFile(DNEVNIK, JSON.stringify({ ts: new Date().toISOString(), pogon: 'linija-most-v1', porocilaPriViru: stevilo, dostavljeno: dostave.length, mostBajti: mostTelo.length }) + '\n', 'utf8');
  console.log('linija-most ⊢ dostavljeno ' + String(dostave.length) + ' / poročil pri viru: ' + String(stevilo) + ' / most: ' + String(mostTelo.length) + ' B');
}

main().catch(function (napaka) {
  const brezMreze = napaka && (napaka.message === 'fetch failed' || napaka.cause);
  console.error(brezMreze ? '⟨ne⟩ — brez mreže ⚠' : (napaka && napaka.message ? napaka.message : '⟨ne⟩ — padec ⚠'));
  process.exit(1);
});
