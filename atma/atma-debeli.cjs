// ATMA — debeli CJS vstop za Node SEA (samostojni Atma.exe, vse v njem).
// Zgrajen z esbuild: celotna CLI veriga je zdrusena v en atma-bundle.mjs,
// vgrajen v exe kot sea asset. Brez ugibanja poti: getAsset ali smrt,
// diag na vsakem koraku — da se vidi, kje zares pade.
// Tanka pot (atma-exe.cjs + build\) ostane kot druga roka / varovalka.
'use strict';

const path = require('node:path');
const { pathToFileURL } = require('node:url');

async function main() {
  const sea = require('node:sea');
  if (!sea || typeof sea.getAsset !== 'function' || !sea.isSea()) {
    throw new Error('Atma-debeli tece samo kot Atma-debeli.exe (ni SEA okolja).');
  }
  let surovina;
  try {
    surovina = sea.getAsset('atma-bundle.mjs');
  } catch (napaka) {
    throw new Error(
      'Atma-debeli: vgrajenega bundla ni: ' + (napaka && napaka.message ? napaka.message : String(napaka)),
    );
  }
  const { writeFileSync, unlinkSync } = require('node:fs');
  const { tmpdir } = require('node:os');
  const pot = path.join(tmpdir(), 'atma-bundle-' + process.pid + '.mjs');
  // getAsset vrne ArrayBuffer — writeFileSync hoce string/Buffer/TypedArray/pogled.
  // Pogled brez kopiranja, brez odvisnosti od Buffer modula.
  const bajti = new Uint8Array(surovina);
  writeFileSync(pot, bajti);
  let bundel;
  try {
    bundel = await import(pathToFileURL(pot).href);
  } finally {
    try {
      unlinkSync(pot);
    } catch {
      // temp se pocisti ob izhodu sistema; molcimo, da ne kalimo izhoda
    }
  }
  const output = await bundel.runAtmaCliCommand(bundel.parseAtmaCliArgs(process.argv.slice(2)));
  process.stdout.write(output + '\n');
}

main().catch((napaka) => {
  const sporocilo = napaka && napaka.message ? napaka.message : String(napaka);
  process.stderr.write(sporocilo + '\n');
  process.exitCode = 1;
});

