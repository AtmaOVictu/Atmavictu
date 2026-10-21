// PREVERBA — slovnična druga roka: LanguageTool (jezik sl), javni API.
// Zagon: node lucius/preverba.mjs <pot-do-datoteke>
// Besedilo gre na javni strežnik languagetool.org — vanj NE dajajmo skrivnosti ⊢.
import fs from 'node:fs';

const pot = process.argv[2];
if (!pot) {
  console.error('Uporaba: node lucius/preverba.mjs <pot-do-datoteke>');
  process.exit(1);
}
const besedilo = fs.readFileSync(pot, 'utf8');

const odziv = await fetch('https://api.languagetool.org/v2/check', {
  method: 'POST',
  headers: { 'content-type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({ text: besedilo, language: 'sl' }),
});
if (!odziv.ok) {
  console.error('LanguageTool HTTP', odziv.status);
  process.exit(1);
}
const data = await odziv.json();

const vrstice = besedilo.split('\n');
const odstotek = (zamik) => {
  let stevec = 0;
  for (let i = 0; i < vrstice.length; i++) {
    if (zamik < stevec + vrstice[i].length + 1) return { vrstica: i + 1, stolpec: zamik - stevec + 1 };
    stevec += vrstice[i].length + 1;
  }
  return { vrstica: '?', stolpec: '?' };
};

let ran = 0;
for (const ujela of data.matches ?? []) {
  const { vrstica, stolpec } = odstotek(ujela.offset);
  const popravek = ujela.replacements?.[0]?.value ?? '(brez predloga)';
  const izsek = ujela.context?.text?.slice(Math.max(0, ujela.context.offset - 20), ujela.context.offset + ujela.context.length).replace(/\n/g, ' ');
  console.log(`r${vrstica}:${stolpec} × ${ujela.shortMessage || ujela.message}`);
  console.log(`   "…${izsek}…" → ${popravek}`);
  ran += 1;
}
console.log(ran === 0 ? 'PREVERBA: čisto ⊢' : `PREVERBA: ${ran} ran ⚠`);
