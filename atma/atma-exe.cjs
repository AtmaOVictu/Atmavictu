// ATMA — CJS vstop za Node SEA (izgradnja Atma.exe).
// Tanka lupina po kroju lucius-exe.cjs: sam Node runtime je v exetu,
// ukazna logika ostane v build\src\atmaCli.js zraven exeta
// (kakor Lucius.exe bere AGENTS.md zraven sebe).
// Zato Atma.exe deluje brez nameščenega Node — build\ pa potuje zraven.
'use strict';

const path = require('node:path');
const { pathToFileURL } = require('node:url');

const jeExe = path.basename(process.execPath).toLowerCase().includes('atma');
const DOM = jeExe
  ? path.dirname(process.execPath) // exe stoji v korenu repa
  : path.resolve(__dirname, '..');

async function main() {
  const cliUrl = pathToFileURL(path.join(DOM, 'build', 'src', 'atmaCli.js')).href;
  const cli = await import(cliUrl);
  const command = cli.parseAtmaCliArgs(process.argv.slice(2));
  const output = await cli.runAtmaCliCommand(command);
  process.stdout.write(output + '\n');
}

main().catch((napaka) => {
  const sporocilo = napaka && napaka.message ? napaka.message : String(napaka);
  process.stderr.write(sporocilo + '\n');
  process.exitCode = 1;
});
