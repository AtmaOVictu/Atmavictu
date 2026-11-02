// PRIMERJAVA — skupna tehtnica vzporednih del ( ukaz ⟡ ⟨oboje⟩: več del omogoča
// takojšnjo primerjavo ∧ izračunano izboljšavo ).
// Bere tok števk π ( testi-pi.jsonl poleg tega organa ) in računa DELTO med dvema okencema:
//   node prevoz/lucius/primerjava.mjs              ( zadnje 2 okeni po 12 števk )
//   node prevoz/lucius/primerjava.mjs 20 20        ( okeni po 20 števk )
// Dom organa: D:/OntoProjekt/prevoz/lucius/ — živo telo; koda je zapečena tudi v knjižnici
// ( Atmavictu ). Meri, ne presoja ( K1 ): tabela po sondah ∧ seznam izračunane izboljšave
// z pričami števk π. Pot, ki jo reši: TEMELJNA POT — vzporedne roke delijo eno telo;
// vsaka pusti mero, primerjava jih postavi na isto tehtnico.
import fs from 'node:fs';
import path from 'node:path';

const TU = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const REGISTER = path.join(TU, 'testi-pi.jsonl');

const N1 = Number(process.argv[2] || 12);
const N2 = Number(process.argv[3] || N1);

let vrstice = [];
try {
  vrstice = fs.readFileSync(REGISTER, 'utf8').trim().split(/\r?\n/).filter(Boolean).map((v) => JSON.parse(v));
} catch {
  console.log('× tok π še ne diha — poženi prevoz/lucius/pi-testi.mjs ⊙ ( register prazen )');
  process.exit(1);
}
if (vrstice.length < 2) { console.log('× premalo števk π ( ' + vrstice.length + ' ) — počakaj naslednji dih'); process.exit(1); }

const zdaj = vrstice.slice(-N2);
const prej = vrstice.slice(Math.max(0, vrstice.length - N2 - N1), vrstice.length - N2);

const skupina = (k) => {
  const po = {};
  for (const z of k) {
    if (!po[z.sonda]) po[z.sonda] = { '⊢': 0, '×': 0, ms: [] };
    po[z.sonda][z.izid === '⊢' ? '⊢' : '×'] += 1;
    po[z.sonda].ms.push(z.ms);
  }
  for (const ime of Object.keys(po)) {
    const s = po[ime];
    s.delez = s['⊢'] / (s['⊢'] + s['×']);
    s.povp = Math.round(s.ms.reduce((a, b) => a + b, 0) / s.ms.length);
  }
  return po;
};

const A = skupina(prej), B = skupina(zdaj);
const imena = [...new Set([...Object.keys(A), ...Object.keys(B)])];

console.log(`PRIMERJAVA ⊢ okenci: prej ${prej.length} števk ( π ${prej[0]?.p}–${prej[prej.length - 1]?.p} ) ⊥ zdaj ${zdaj.length} števk ( π ${zdaj[0]?.p}–${zdaj[zdaj.length - 1]?.p} )`);
console.log('sonda                     | prej ⊢/×  ms | zdaj ⊢/×  ms | delta');
console.log('--------------------------+--------------+--------------+-------');
const izboljsave = [], poslabsanja = [];
for (const ime of imena) {
  const a = A[ime] || { '⊢': 0, '×': 0, delez: 0, povp: 0 };
  const b = B[ime] || { '⊢': 0, '×': 0, delez: 0, povp: 0 };
  const dDelez = Math.round((b.delez - a.delez) * 100);
  const dMs = b.povp - a.povp;
  console.log(
    ime.padEnd(25) + ' | ' +
    (String(a['⊢']) + '/' + String(a['×'])).padEnd(5) + String(a.povp).padStart(6) + 'ms | ' +
    (String(b['⊢']) + '/' + String(b['×'])).padEnd(5) + String(b.povp).padStart(6) + 'ms | ' +
    (dDelez >= 0 ? '+' : '') + dDelez + '% ⊢, ' + (dMs >= 0 ? '+' : '') + dMs + 'ms'
  );
  if (dDelez > 0 || (dMs < -20 && dDelez >= 0)) izboljsave.push(ime + ' ( +' + dDelez + '% ⊢, ' + (dMs >= 0 ? '+' : '') + dMs + 'ms )');
  if (dDelez < 0 || dMs > 100) poslabsanja.push(ime + ' ( ' + dDelez + '% ⊢, +' + dMs + 'ms )');
}
console.log('\nIZRAČUNANA IZBOLJŠAVA ( mera, ne mnenje ⊙ K1 ):');
console.log(izboljsave.length ? '  + ' + izboljsave.join('\n  + ') : '  ( ni izmerjene izboljšave v tem okencu ⚠ — okence je kratko, pusti π dihati )');
if (poslabsanja.length) console.log('  × poslabšanja, poimenuj vsako ( KORENINA 2 ):\n  × ' + poslabsanja.join('\n  × '));
console.log('\npriča: tok π šteje ' + vrstice.length + ' števk od ' + vrstice[0].ts.slice(0, 16) + ' ⊢');
