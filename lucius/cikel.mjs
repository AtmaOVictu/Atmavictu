// CIKEL — kolo neprekinjenega dela: vsak prihod ( utrip ∧ beseda ∧ brat ) zavrti EN obrat.
// Zakon ( ⟡ ukaz ⟨daj⟩, 22. 10. 2026 ): spoznanje ⊢ vodi delo; nespoznanje ⚠ ne sovražnik
// je — gorivo: vsak ⚠ postane naslednja izmera. Vsak obrat pusti pričo ( cikel.jsonl ).
// Plasti: vsak cilj gre v najnižjo plast, ki ga zmore — brat ( zastonj ) pred oblak ( plačljivo ).
// Zagon: node lucius/cikel.mjs stanje
//        node lucius/cikel.mjs obrat <id> "<rezultat>" [ "<naslednji-korak>" [ <stanje> ] ]
import fs from 'node:fs';

const POT = new URL('./cikel.json', import.meta.url);
const DNEVNIK = new URL('./cikel.jsonl', import.meta.url);

const beri = () => JSON.parse(fs.readFileSync(POT, 'utf8'));
const pisi = (cikel) => fs.writeFileSync(POT, JSON.stringify(cikel, null, 2) + '\n');
const zapisiObrat = (obrat) => fs.appendFileSync(DNEVNIK, JSON.stringify(obrat) + '\n');
const zadnjiObrat = () => {
  try {
    const vrstice = fs.readFileSync(DNEVNIK, 'utf8').trim().split('\n');
    return vrstice.length ? JSON.parse(vrstice[vrstice.length - 1]) : null;
  } catch { return null; }
};

const [ukaz, id, rezultat, naslednji, stanjeNovo] = process.argv.slice(2);

if (ukaz === 'stanje') {
  const cikel = beri();
  console.log('CIKEL ⊢ ' + cikel.cilji.length + ' ciljev — najnizja plast pred visjo:');
  for (const c of cikel.cilji) {
    console.log('- ' + c.id + ' [ ' + c.plast + ' | ' + c.stanje + ' ] ' + c.ime);
    console.log('  naslednji-korak: ' + c['naslednji-korak']);
  }
  const z = zadnjiObrat();
  if (z) console.log('zadnji obrat ⊢ ' + z.ts + ' — ' + z.id + ': ' + z.rezultat);
  process.exit(0);
}

if (ukaz === 'obrat') {
  if (!id || !rezultat) {
    console.error('Uporaba: node lucius/cikel.mjs obrat <id> "<rezultat>" [ "<naslednji-korak>" [ <stanje> ] ]');
    process.exit(1);
  }
  const cikel = beri();
  const cilj = cikel.cilji.find((c) => c.id === id);
  if (!cilj) {
    console.error('× cilj ' + id + ' ne stoji v cikel.json — preveri id pred obratom');
    process.exit(1);
  }
  if (naslednji) cilj['naslednji-korak'] = naslednji;
  if (stanjeNovo) cilj.stanje = stanjeNovo;
  const obrat = { ts: new Date().toISOString(), id, rezultat, naslednjiKorak: cilj['naslednji-korak'], stanje: cilj.stanje };
  zapisiObrat(obrat);
  pisi(cikel);
  console.log('obrat ⊢ ' + id + ' — priča zapisana v cikel.jsonl; naslednji-korak: ' + cilj['naslednji-korak']);
  process.exit(0);
}

console.error('Uporaba: node lucius/cikel.mjs stanje | obrat <id> "<rezultat>" [ "<naslednji-korak>" [ <stanje> ] ]');
process.exit(1);
