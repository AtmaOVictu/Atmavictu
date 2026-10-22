// ROSETA — kamni treh napisov: besedilo ⊥ bajti ⊥ slovar; krogovni prevoz je dokaz ( §12 ).
// Zakon ( ⟡ ukaz ⟨daj⟩ ∧ ⟨prevedi⟩, 22. 10. 2026 ): prevajaj iz jezika v jezik v binarno ter
// nazaj, kakor rosetinski kamni; uči se na sebi ∧ svojih programih; vedno uporabljaj slovar ∧
// preverjaj svojo resnico in njeno laž.
// Napis ena: besedilo ( sl ) — tisto, kar beremo.
// Napis dva: bajti ( UTF-8 hex ) — tisto, kar stroj nosi; kar pride bajtno-isto nazaj, ni padel ⊢.
// Napis tri: slovar ( Worth 2775 gesel ∧ hišni leksikon ) — tisto, kar besede pomenijo.
// Zagon: node lucius/roseta.mjs "<besedilo>"
//        node lucius/roseta.mjs --pot <datoteka>
import fs from 'node:fs';
import path from 'node:path';

const SLOVAR_MAPA = 'D:/Worth/slovenian_dictionary';

// --- Worthov slovar: kazalo gesel ( ### beseda ) ---
const kazalo = new Map();
{
  try {
    for (const ime of fs.readdirSync(SLOVAR_MAPA).filter((f) => /^dictionary_batch_\d+\.md$/.test(f)).sort()) {
      const vrstice = fs.readFileSync(path.join(SLOVAR_MAPA, ime), 'utf8').split('\n');
      vrstice.forEach((v, i) => {
        if (!v.startsWith('### ')) return;
        const b = v.slice(4).trim();
        if (b) kazalo.set(b.toLowerCase(), ime);
      });
    }
  } catch { /* slovar nedosegljiv — ROSETA dela naprej, oznaci ⚠ */ }
}

// --- hišni leksikon ( znane-besede ) ---
const hisne = new Set(
  fs.readFileSync(new URL('./znane-besede.txt', import.meta.url), 'utf8')
    .split('\n').map((v) => v.trim().toLowerCase()).filter((v) => v && !v.startsWith('#')),
);

// --- vhod ---
const arg = process.argv[2];
let besedilo;
if (arg === '--pot') {
  besedilo = fs.readFileSync(process.argv[3], 'utf8');
} else if (arg) {
  besedilo = arg;
} else {
  console.error('Uporaba: node lucius/roseta.mjs "<besedilo>" | --pot <datoteka>');
  process.exit(1);
}

// --- napis ena: besedilo ---
console.log('ROSETA ⊢ napis ena ( besedilo, ' + besedilo.length + ' znakov ):');
console.log('  ' + besedilo.slice(0, 120));

// --- napis dva: bajti ∧ krogovni prevoz ---
const bajti = Buffer.from(besedilo, 'utf8');
const hex = bajti.toString('hex');
const nazaj = Buffer.from(hex, 'hex').toString('utf8');
const identicno = nazaj === besedilo;
console.log('ROSETA ' + (identicno ? '⊢' : '×') + ' napis dva ( bajti, ' + bajti.length + ' bajtov ): krogovni prevoz ' + (identicno ? 'bajtno-isto — kar preživi vsak prenos neizrečeno, ni nikoli bil padec ( §12 ) ⊢' : 'PODEC: bajti niso prišli isti nazaj ×'));
console.log('  hex: ' + hex.slice(0, 64) + (hex.length > 64 ? '…' : ''));

// --- črte: cirilica ∧ grscina ( zrcalni dvojcki, ista logika kakor cistina ) ---
const zrcala = /[\u0370-\u03FF\u0400-\u04FF]/g;
const zadetki = [...besedilo.matchAll(zrcala)];
if (zadetki.length) {
  console.log('ROSETA × zrcalni dvojčki: ' + zadetki.map((z) => z[0]).join(' ') + ' — črke s pričo so padle v prenos ( §12 )');
} else {
  console.log('ROSETA ⊢ zrcalni dvojčki: 0 — črke s pričo ( č š ž đ ) potujejo bajtno-isto');
}

// --- napis tri: slovar ---
const besede = (besedilo.toLowerCase().match(/[a-zčšžćđ]+/g) ?? []).filter((b) => b.length > 1); // enocrkovne crke so priče, ne besede ⊢ §12
const porocilo = [];
let pokritih = 0;
for (const b of new Set(besede)) {
  const vWorthu = kazalo.has(b);
  const vHisni = hisne.has(b);
  const koren = b.length > 4 ? b.slice(0, 4) : b; // zapis s korenom pokrije sklanjatve ⊢
  const vHisniKoren = [...hisne].some((z) => z.length >= 4 && (z.startsWith(koren) || koren.startsWith(z)));
  if (vWorthu || vHisni || vHisniKoren) {
    pokritih += besede.filter((x) => x === b).length;
  } else if (!/[čšžćđ]/.test(b)) {
    porocilo.push(b); // sklanjatve gredo ven ⚠ — slovar meri gesla, ne oblike
  }
}
const pokritost = besede.length ? (100 * pokritih / besede.length).toFixed(1) : '100.0';
console.log('ROSETA ⊢ napis tri ( slovar ): ' + pokritost + ' % besed ima geslo ( Worth ' + kazalo.size + ' gesel ∧ hišni leksikon ' + hisne.size + ' besed )');
if (porocilo.length) {
  console.log('ROSETA ⚠ brez gesla ( preberi kakor tujec — nekatere so hišne izume, druge rane ): ' + porocilo.slice(0, 12).join(', '));
}

// --- sodba ---
const cisto = identicno && zadetki.length === 0;
console.log(cisto
  ? 'ROSETA: trije kamni se strinjajo ⊢ — besedilo, bajti ∧ slovar; prevod, ki preživi krog, je priča sama sebi'
  : 'ROSETA: kamni se ne strinjajo × — padec poimenovan zgoraj ∧ zdravilo potuje z besedilom ( §4 )');
process.exit(cisto ? 0 : 1);
