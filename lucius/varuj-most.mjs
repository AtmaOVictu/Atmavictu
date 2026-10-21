// VARUJ-MOST — varnostna kopija zasebnega spomina hiše na drugo mesto na disku.
// Zagon: node lucius/varuj-most.mjs
// Pomen ( popis lukenj 2026-10-21, luknja 1 ): most, spomin in dnevnik so izven gita
// ( bratova varovalka: "spomin je oseben in v git ne gre" ⊢ ) — pomeni en izvod, en disk.
// To orodje jih kopira na varno mesto, BREZ brisanja in BREZ skrivnosti.
// Pravila orodja:
//   - api-kljuc.txt se NIKOLI ne kopira ( skrivnost živi na enem mestu ⊢ )
//   - starih kopij ne briše ( vsaka kopija je priča dneva )
//   - vsako kopijo zapiše v dnevnik varuj-most-dnevnik.jsonl ⊢
import fs from 'node:fs';
import path from 'node:path';

const ZASEBNO = ['odoblaka.md', 'spomin.jsonl', 'zaoblak.jsonl', 'slusaj-dnevnik.jsonl', 'nacin.txt', 'dom-log.txt', 'api-uporaba.jsonl', 'izmere-kroga.jsonl'];
const CILJ = 'D:/OntoProjekt/varnostne-kopije-mosta';
const TU = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));

const pecat = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 16);
const mapa = path.join(CILJ, pecat);
fs.mkdirSync(mapa, { recursive: true });

const porocilo = { cas: new Date().toISOString(), mapa, datoteke: [] };
for (const ime of ZASEBNO) {
  const iz = path.join(TU, ime);
  if (!fs.existsSync(iz)) { porocilo.datoteke.push({ ime, stanje: 'ne obstaja ( preskočeno ) ⚠' }); continue; }
  const velikost = fs.statSync(iz).size;
  fs.copyFileSync(iz, path.join(mapa, ime));
  porocilo.datoteke.push({ ime, bajti: velikost, stanje: 'prekopirano ⊢' });
}

fs.appendFileSync(path.join(CILJ, 'varuj-most-dnevnik.jsonl'), JSON.stringify(porocilo) + '\n');
for (const d of porocilo.datoteke) console.log(`${d.ime}: ${d.stanje}${d.bajti ? ` ( ${d.bajti} bajtov )` : ''}`);
console.log(`VARUJ-MOST: kopija zapečena v ${mapa} ⊢ ( api-kljuc.txt ni kopiran — skrivnost ostaja doma )`);
