// Zdruzi CLI verigo v en sam ESM bundel za debelega Atma.exe.
// 2 (esbuild) rodi — 1 (rocni vstop) drzi: esbuild nosi verigo v ESM
// (CJS ne prenese import.meta + top-level await iz CLI vstopov),
// debeli ESM vstop poklice izvozeni funkciji, tanki ostane kot varovalka.
// Brez novih odvisnosti razen ze namescenega esbuild (devDependency).
'use strict';

const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');

const TUKAJ = __dirname;
const DOM = path.resolve(TUKAJ, '..');
const VSTOP = path.join(DOM, 'src', 'atmaCli.ts');
const IZHOD = path.join(TUKAJ, 'atma-bundle.mjs');

function main() {
  // esbuild zdruzi TS verigo v en ESM (ohrani import.meta + top-level await).
  // --define ugasne oba CLI main ob uvozu: bundel je knjiznica, ne ukaz.
  // --banner pripne glavo, ki urejevalniku pove: to je peceno, ne izvor —
  // TS in JS preverba zanj ne veljata (meja, ne popravek).
  execFileSync(
    process.execPath,
    [
      path.join(DOM, 'node_modules', 'esbuild', 'bin', 'esbuild'),
      VSTOP,
      '--bundle',
      '--platform=node',
      '--format=esm',
      '--target=node22',
      '--define:process.env.ATMA_BUNDLE="1"',
      '--banner:js=// @ts-nocheck — ATMA bundel: peceno, ne izvor; ne popravljaj, zgradi znova.',
      '--outfile=' + IZHOD,
    ],
    { stdio: 'inherit' },
  );
  const statistika = fs.statSync(IZHOD);
  process.stdout.write('ATMA BUNDEL: ' + IZHOD + ' (' + statistika.size + ' B)\n');
}

main();
