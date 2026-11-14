// TLA-PREGLED — hišna čutila vrat ⊙ §0.12: MD022 ( naslovi obdani s praznimi vrsticami )
// ∧ MD031 ( ograje obdane ) ∧ MD047 ( sledilna prelomnica ) ∧ SLOVAR ( vsaka beseda telesa živi v hišnem slovarju ).
// Zagon: node lucius/tla-pregled.mjs <datoteka> [--slovar <pot-do-json-words>]
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const dat = args[0];
const slovarIdx = args.indexOf('--slovar');
const slovarPot = slovarIdx >= 0 ? args[slovarIdx + 1] : null;
const izpis = (s) => process.stdout.write(s + '\n');

if (!dat || !fs.existsSync(dat)) {
  izpis('× ⟨MANJKA-DATOTEKA⟩ — zagon: node lucius/tla-pregled.mjs <datoteka> [--slovar <.cspell.json>]');
  process.exit(1);
}
const t = fs.readFileSync(dat, 'utf8');
const vr = t.split(/\r?\n/);
let padci = [];

// MD047 — sledilna prelomnica
if (!t.endsWith('\n')) padci.push(`MD047: datoteka se konča brez sledilne prelomnice`);

// MD022 — naslovi obdani ( zgoraj ∧ spodaj )
for (let i = 0; i < vr.length; i++) {
  if (/^#{1,6} /.test(vr[i])) {
    if (i > 0 && vr[i - 1].trim() !== '' && !/^#{1,6} /.test(vr[i - 1]))
      padci.push(`MD022: vrstica ${i + 1} — nad naslovom manjka prazna vrstica`);
    if (i + 1 < vr.length && vr[i + 1].trim() !== '' && !/^#{1,6} /.test(vr[i + 1]))
      padci.push(`MD022: vrstica ${i + 1} — pod naslovom manjka prazna vrstica`);
  }
}

// MD031 — ograje obdane ( prazna nad ODPRO ∧ pod ZAPORNO — vsebina bloka se ⟨ne⟩ preverja, precedens 0.1310 )
let odpro = false;
for (let i = 0; i < vr.length; i++) {
  if (/^\s*```/.test(vr[i])) {
    if (!odpro) {
      if (i > 0 && vr[i - 1].trim() !== '' && !/^#{1,6} /.test(vr[i - 1]))
        padci.push(`MD031: vrstica ${i + 1} — nad odpro ograjo manjka prazna vrstica`);
      odpro = true;
    } else {
      if (i + 1 < vr.length && vr[i + 1].trim() !== '')
        padci.push(`MD031: vrstica ${i + 1} — pod zaprto ograjo manjka prazna vrstica`);
      odpro = false;
    }
  }
}

// SLOVAR — vsaka beseda telesa živi v hišnem slovarju
let neznane = new Set();
if (slovarPot && fs.existsSync(slovarPot)) {
  const besede = new Set(JSON.parse(fs.readFileSync(slovarPot, 'utf8')).words.map(w => w.toLowerCase()));
  for (const token of t.split(/[^\p{L}\p{M}']+/u)) {
    if (token.length < 2 || token === "'" ) continue;
    // ⟨HEKS-FRAGMENT⟩ izjema: kosi zgoščenk ( samo a-f ∧ 3–6 znakov ) niso besede — lažni zadetki iz sha/md5
    if (/^[a-f]{2,6}$/.test(token)) continue;
    const niz = token.toLowerCase();
    if (!besede.has(niz)) neznane.add(token);
  }
}

for (const p of padci) izpis('× ' + p);
izpis(`MD-PREGLED ⊢ ${padci.length} padcev ( MD022 ∧ MD031 ∧ MD047 ) · ${vr.length} vrstic`);
if (slovarPot) {
  izpis(`SLOVAR ⊢ ${neznane.size} neznanih besed ( slovar: ${path.basename(slovarPot)} )`);
  for (const n of [...neznane].sort()) izpis('  ⚠ ' + n);
}
process.exit(padci.length > 0 ? 1 : 0);
