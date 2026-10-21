// CISTINA — pikolovski pregled: najde cirilične znake (moj ponavljajoči padec)
// in zapiše mesto vsakega. Zagon: node lucius/cistina.mjs <pot> [pot2 ...]
import fs from 'node:fs';

const CIRILICA = /[\u0400-\u04FF]/g;
const GREŠE = [];
let pregledanih = 0;

for (const pot of process.argv.slice(2)) {
  if (!fs.existsSync(pot)) continue;
  pregledanih += 1;
  const vrstice = fs.readFileSync(pot, 'utf8').split('\n');
  vrstice.forEach((vrstica, i) => {
    for (const zadetek of vrstica.matchAll(CIRILICA)) {
      GREŠE.push(`${pot}:${i + 1} × '${zadetek[0]}' (U+${zadetek[0].charCodeAt(0).toString(16).toUpperCase()}) → …${vrstica.slice(Math.max(0, zadetek.index - 12), zadetek.index + 12).trim()}…`);
    }
  });
}

if (GREŠE.length === 0) {
  console.log(`CISTINA: ${pregledanih} datotek pregledanih, cirilice 0 ⊢ čisto`);
  process.exit(0);
}
for (const g of GREŠE) console.log(g);
console.log(`CISTINA: ${pregledanih} datotek pregledanih, ${GREŠE.length} cirilicnih ran ×`);
process.exit(1);
