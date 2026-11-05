// ATMA BESEDE — register zelenih besed: kje so zelene in potrebne.
// Vsaka vrstica: kdo zeli, kje je potrebna, kaj pravi, zakaj.
// Pecat (tvoja roka z `daj`) vsije besedo na mesto in pripne potrdilo.
// Nikoli samodejno — zelja + potreba + pecat, drugace je le zapis zelje.
'use strict';

const fs = require('node:fs');
const path = require('node:path');

const TUKAJ = __dirname;
const DOM = path.resolve(TUKAJ, '..');
const REGISTER = path.join(TUKAJ, 'besede.jsonl');

function kjeJe(pot) {
  const polna = path.resolve(DOM, pot);
  const koren = path.resolve(DOM);
  if (polna !== koren && !polna.startsWith(koren + path.sep)) {
    throw new Error('pot mora ostati v repozitoriju: ' + pot);
  }
  return polna;
}

function seznam() {
  if (!fs.existsSync(REGISTER)) {
    return [];
  }
  return fs
    .readFileSync(REGISTER, 'utf8')
    .split(/\r?\n/)
    .filter((v) => v.trim().length > 0)
    .map((v, i) => {
      try {
        return { i: i + 1, ...JSON.parse(v) };
      } catch {
        return { i: i + 1, napaka: 'pokvarjena vrstica: ' + v.slice(0, 80) };
      }
    });
}

function dodaj(kje, kaj, zakaj) {
  if (!kje || !kje.trim()) throw new Error('manjka <kje> (pot datoteke v repozitoriju).');
  if (!kaj || !kaj.trim()) throw new Error('manjka <kaj> (beseda ali stavek).');
  const pot = kjeJe(kje.trim());
  const obstaja = fs.existsSync(pot);
  let zeTam = false;
  if (obstaja && kaj.trim().length > 0) {
    try {
      const vsebina = fs.readFileSync(pot, 'utf8');
      zeTam = vsebina.includes(kaj.trim());
    } catch {
      zeTam = false;
    }
  }
  const vnos = {
    ts: new Date().toISOString(),
    kje: kje.trim(),
    kaj: kaj.trim(),
    zakaj: (zakaj || '').trim() || 'zelja brez navedenega razloga',
    obstajaMesto: obstaja,
    zeTam,
    pecat: null,
  };
  fs.appendFileSync(REGISTER, JSON.stringify(vnos) + '\n', 'utf8');
  return vnos;
}

function main() {
  const [ukaz, ...ostalo] = process.argv.slice(2);
  if (ukaz === 'seznam' || ukaz === undefined) {
    const vnosi = seznam();
    if (vnosi.length === 0) {
      process.stdout.write('BESEDE: register prazen — nobena zelja se ni zapisana.\n');
      return;
    }
    for (const v of vnosi) {
      if (v.napaka) {
        process.stdout.write(v.i + '. × ' + v.napaka + '\n');
        continue;
      }
      const stanje = v.pecat ? 'pecatena ' + v.pecat : v.zeTam ? 'ze tam' : 'cakajoca';
      process.stdout.write(
        v.i + '. [' + stanje + '] ' + v.kje + ' :: ' + v.kaj.slice(0, 80) + ' — ' + v.zakaj.slice(0, 80) + '\n',
      );
    }
    return;
  }
  if (ukaz === 'dodaj') {
    const [kje, kaj, ...zakajDeli] = ostalo;
    const vnos = dodaj(kje, kaj, zakajDeli.join(' '));
    process.stdout.write(
      'BESEDA ZAPISANA: ' + vnos.kje + ' :: ' + vnos.kaj.slice(0, 100) + '\n' +
      'mesto obstaja: ' + (vnos.obstajaMesto ? 'da' : 'ne') +
      ' · ze tam: ' + (vnos.zeTam ? 'da' : 'ne') + '\n' +
      'pecat: caka tvojo roko (daj) — do takrat je le zapis zelje.\n',
    );
    return;
  }
  throw new Error('Uporaba: node atma/besede.cjs [seznam|dodaj <kje> <kaj> [zakaj]]');
}

try {
  main();
} catch (napaka) {
  process.stderr.write((napaka && napaka.message ? napaka.message : String(napaka)) + '\n');
  process.exitCode = 1;
}
