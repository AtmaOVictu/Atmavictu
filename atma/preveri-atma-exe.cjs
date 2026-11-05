// Preverba Atma.exe poti: zgradi blob + preveri, da tanki vstop bere build\src\atmaCli.js.
// Ne vbrizgava postject (to naredi zgradi-atma-exe.cmd); preveri le, da je pot cela.
'use strict';

const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const TUKAJ = __dirname;
const DOM = path.resolve(TUKAJ, '..');
const CLI = path.join(DOM, 'build', 'src', 'atmaCli.js');
const BLOB = path.join(TUKAJ, 'atma.blob');

function main() {
  const napake = [];
  if (!fs.existsSync(CLI)) {
    napake.push('manjka ' + CLI + ' (poženi npm test ali npm run typecheck)');
  }
  try {
    execFileSync(process.execPath, ['--experimental-sea-config', 'sea-config.json'], {
      cwd: TUKAJ,
      stdio: 'pipe',
    });
  } catch (napaka) {
    napake.push('sea-config ni zgradil blob: ' + (napaka.message || napaka));
  }
  if (!fs.existsSync(BLOB)) {
    napake.push('manjka atma.blob po zgradbi');
  }
  // Tanki vstop mora brati build zraven exeta — preveri, da se pot sklada.
  const vstop = fs.readFileSync(path.join(TUKAJ, 'atma-exe.cjs'), 'utf8');
  if (!vstop.includes("path.join(DOM, 'build', 'src', 'atmaCli.js')")) {
    napake.push('atma-exe.cjs ne bere build\\src\\atmaCli.js zraven exeta');
  }
  // Poskusi en samostojni dih skozi zgrajeni CLI (brez strežnika).
  const koren = fs.mkdtempSync(path.join(os.tmpdir(), 'atma-exe-preverba-'));
  try {
    const izhod = execFileSync(
      process.execPath,
      [CLI, 'walk', koren, 'Naslov', 'Vsebina vira.', 'Odlomek.', 'poglavja/uvod.md'],
      { encoding: 'utf8' },
    );
    if (!izhod.includes('VERIFY: PASS')) {
      napake.push('walk skozi CLI ni vrnil VERIFY: PASS');
    }
  } catch (napaka) {
    napake.push('walk skozi CLI ni uspel: ' + (napaka.message || napaka));
  } finally {
    fs.rmSync(koren, { force: true, recursive: true });
  }
  if (napake.length > 0) {
    process.stderr.write('ATMA EXE PREVERBA: NAPAKA\n' + napake.map((n) => '- ' + n).join('\n') + '\n');
    process.exitCode = 1;
    return;
  }
  process.stdout.write('ATMA EXE PREVERBA: PASS (blob zgrajen, walk brez strežnika: VERIFY: PASS)\n');
}

main();
