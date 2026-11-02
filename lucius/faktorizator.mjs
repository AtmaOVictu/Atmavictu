// FAKTORIZATOR — trajajoči organ z izdelki ( ukaz ⟡ 2. 11.: ideja je imeti trajajoče
// procese s smiselnimi produkti / faktorizacijo / kategorizacijo ).
// Bere register govora ( transkripti-⟡.jsonl v telesu ) in vsak nov stavek:
//   1. FAKTORIZIRA — razcepi na povedi/konice ( izdelki: faktorji ),
//   2. KATEGORIZIRA — pravilno, deterministično, izmerljivo ( ne mnenje ⊙ K1 ):
//      ukaz-⟡ ( daj/⟡/naredi ) · vprašanje ( ? ) · vlak-malo ( mrmranje: hvala, aja … )
//      · tehnična-meritev ( kode/številke ) · misel ( ostalo ),
//   3. ZAPIŠE izdelek v faktorji.jsonl + merjenje vsakega poteka v faktorji-porocilo.jsonl.
// Dom organa: D:/OntoProjekt/prevoz/lucius/ — telo. Zagon: node prevoz/lucius/faktorizator.mjs
// ( teče neprekinjeno; konec z datoteko FAKTOR-STOP ). © Luka Pintarič — VBL ( §1: verify ).
import fs from 'node:fs';
import path from 'node:path';

const TU = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const VHOD = path.join(TU, 'transkripti-⟡.jsonl');
const IZHOD = path.join(TU, 'faktorji.jsonl');
const POROCILO = path.join(TU, 'faktorji-porocilo.jsonl');
const STOP = path.join(TU, 'FAKTOR-STOP');
const ZAMIK_S = 60;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const faktoriziraj = (besedilo) => besedilo
  .split(/(?<=[.!?…])\s+|\s*;\s*/u)
  .map((f) => f.trim())
  .filter((f) => f.length > 0);

const kategoriziraj = (besedilo) => {
  const b = besedilo.trim();
  if (/⟡|\bdaj\b|\bdaj\s*$/i.test(b)) return 'ukaz-⟡';
  if (b.includes('?')) return 'vprašanje';
  if (b.length < 15 && /^(hvala|aja|mhm|hm|dobro|ne|da|o|ok|ej|pa)\b/i.test(b)) return 'vlak-malo';
  if (/\b[0-9a-f]{4,}\b|\b0x[0-9a-f]+\b|\d+\s*(gb|mb|°c|b|kb)\b/i.test(b)) return 'tehnična-meritev';
  return 'misel';
};

let obdelanih = 0;
try { obdelanih = Number(fs.readFileSync(path.join(TU, 'faktor-stanje.txt'), 'utf8').trim()) || 0; } catch {}

const preberiVhod = () => {
  try {
    return fs.readFileSync(VHOD, 'utf8').trim().split(/\r?\n/).filter(Boolean).map((v) => JSON.parse(v));
  } catch { return []; }
};

console.log(`FAKTORIZATOR ⊢ tok odprt — obdelanih doslej: ${obdelanih}, novih vsakih ${ZAMIK_S}s, konec z FAKTOR-STOP`);

while (!fs.existsSync(STOP)) {
  const vse = preberiVhod();
  const novo = vse.slice(obdelanih);
  if (novo.length > 0) {
    const poKategorijah = {};
    let faktorjev = 0;
    const vrstice = [];
    for (const z of novo) {
      const k = kategoriziraj(z.besedilo || '');
      const f = faktoriziraj(z.besedilo || '');
      faktorjev += f.length;
      poKategorijah[k] = (poKategorijah[k] || 0) + 1;
      vrstice.push(JSON.stringify({
        ts: z.ts || null, ura: z.ura || null, vir: z.vir || 'nenehno',
        kategorija: k, faktorji: f, bajtov: (z.besedilo || '').length,
        neznane: z.neznane || [],
      }));
    }
    fs.appendFileSync(IZHOD, vrstice.join('\n') + '\n', 'utf8');
    obdelanih += novo.length;
    fs.writeFileSync(path.join(TU, 'faktor-stanje.txt'), String(obdelanih), 'utf8');
    const porocilo = { cas: new Date().toISOString(), novo: novo.length, obdelanihSkupaj: obdelanih, faktorjev, poKategorijah };
    fs.appendFileSync(POROCILO, JSON.stringify(porocilo) + '\n', 'utf8');
    console.log(`FAKTORIZATOR ⊢ ${novo.length} novih → ${faktorjev} faktorjev · ${JSON.stringify(poKategorijah)}`);
  }
  await sleep(ZAMIK_S * 1000);
}
console.log(`FAKTORIZATOR ⊙ molk — FAKTOR-STOP pri ${obdelanih}`);
