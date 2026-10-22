// CISTINA — nano-mikroskop hiše: najde zrcalne dvojčke ( cirilico U+0400–U+04FF,
// grscino U+0370–U+03FF — obe sta vizualna dvojčka latinskih crk na nivoju kodne tocke )
// in zapise mesto vsakega. Zagon: node lucius/cistina.mjs <pot> [pot2 ...]
import fs from 'node:fs';

const ZRCALA = /[\u0370-\u03FF\u0400-\u04FF]/g;
const IMENA = { grscina: '\u0370-\u03FF', cirilica: '\u0400-\u04FF' };
function imeZnaka(z) {
  const k = z.charCodeAt(0);
  return k < 0x400 ? 'grscina' : 'cirilica';
}
const GREŠE = [];
let pregledanih = 0;

for (const pot of process.argv.slice(2)) {
  if (!fs.existsSync(pot)) continue;
  pregledanih += 1;
  const vrstice = fs.readFileSync(pot, 'utf8').split('\n');
  vrstice.forEach((vrstica, i) => {
    for (const zadetek of vrstica.matchAll(ZRCALA)) {
      GREŠE.push(`${pot}:${i + 1} × '${zadetek[0]}' [${imeZnaka(zadetek[0])}] (U+${zadetek[0].charCodeAt(0).toString(16).toUpperCase()}) → …${vrstica.slice(Math.max(0, zadetek.index - 12), zadetek.index + 12).trim()}…`);
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
