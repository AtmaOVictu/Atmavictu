// ATMA PULZ — samostojni dih jedra: izmeri, pripni, predlagaj. Nikoli ne peca sam.
// Po kroju lucius/abeceda-grep-pulz.py, a za Atmo: typecheck + testi + bundel + debeli walk.
// Vsak tek pusti ENO vrstico v atma/utrip.jsonl (append-only, kot srce.jsonl).
// Sopecatenje: pulz meri (A), hisa potrdi (B) — predlogi cakajo v atma/predlogi.jsonl.
'use strict';

const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const TUKAJ = __dirname;
const DOM = path.resolve(TUKAJ, '..');
const UTRIP = path.join(TUKAJ, 'utrip.jsonl');
const PREDLOGI = path.join(TUKAJ, 'predlogi.jsonl');

function izmeri(ukaz, args, cwd) {
  const zacetek = Date.now();
  // Na Windows `npm` ni izvrsina datoteka, ampak .cmd skripta — rabi lupino.
  const naWin = process.platform === 'win32' && (ukaz === 'npm' || ukaz.endsWith('npm.cmd'));
  const praviUkaz = naWin ? 'cmd.exe' : ukaz;
  const praviArgs = naWin ? ['/c', 'npm', ...args] : args;
  try {
    const izhod = execFileSync(praviUkaz, praviArgs, { cwd: cwd || DOM, encoding: 'utf8', stdio: 'pipe' });
    return { ok: true, ms: Date.now() - zacetek, izhod: String(izhod).slice(-500) };
  } catch (napaka) {
    const izhod = (napaka.stdout || '') + (napaka.stderr || '') + (napaka.message || String(napaka));
    return { ok: false, ms: Date.now() - zacetek, izhod: String(izhod).slice(-500) };
  }
}

function main() {
  const zdaj = new Date().toISOString();
  // 1. roka: typecheck
  const typecheck = izmeri(process.execPath, ['node_modules/typescript/bin/tsc', '--noEmit']);
  // 2. roka: testi (tsc + node --test)
  const testi = izmeri('npm', ['test'], DOM);
  // 3. roka: bundel (esbuild zdruzi verigo)
  const bundel = izmeri(process.execPath, ['atma/zgradi-bundel.cjs'], DOM);
  // 4. roka: debeli walk (cel dih skozi bundel, brez streznika)
  let walk = { ok: false, ms: 0, izhod: 'ni merjen' };
  const koren = fs.mkdtempSync(path.join(os.tmpdir(), 'atma-pulz-'));
  try {
    const bundelPot = path.join(TUKAJ, 'atma-bundle.mjs');
    if (fs.existsSync(bundelPot)) {
      walk = izmeri(
        process.execPath,
        [bundelPot, 'walk', koren, 'Pulz', 'Vsebina pulza.', 'Odlomek pulza.', 'poglavja/pulz.md'],
      );
      if (walk.ok && !walk.izhod.includes('VERIFY: PASS')) {
        walk = { ok: false, ms: walk.ms, izhod: walk.izhod.slice(-300) + ' (brez VERIFY: PASS)' };
      }
    } else {
      walk = { ok: false, ms: 0, izhod: 'manjka atma-bundle.mjs (pozheni npm run atma:bundel)' };
    }
  } finally {
    fs.rmSync(koren, { force: true, recursive: true });
  }
  // 5. straza: bliznjica na namizju — ali cilj obstaja in diha
  let bliznjica = { obstaja: false, cilj: '', diha: false };
  try {
    const namizje = path.join(os.homedir(), 'Desktop');
    const lnk = path.join(namizje, 'Atma.lnk');
    bliznjica.obstaja = fs.existsSync(lnk);
    const debeli = path.join(DOM, 'Atma-debeli.exe');
    bliznjica.cilj = fs.existsSync(debeli) ? debeli : '';
    bliznjica.diha = bliznjica.cilj !== '';
  } catch {
    bliznjica = { obstaja: false, cilj: '', diha: false };
  }
  const zdrav = typecheck.ok && testi.ok && bundel.ok && walk.ok;
  const vrstica = {
    ts: zdaj,
    verzija: 'ATMA-PULZ',
    zdrav,
    typecheck: { ok: typecheck.ok, ms: typecheck.ms },
    testi: { ok: testi.ok, ms: testi.ms },
    bundel: { ok: bundel.ok, ms: bundel.ms },
    walk: { ok: walk.ok, ms: walk.ms },
    bliznjica,
  };
  if (!zdrav) {
    const razlogi = [];
    if (!typecheck.ok) razlogi.push('typecheck: ' + typecheck.izhod.slice(-200));
    if (!testi.ok) razlogi.push('testi: ' + testi.izhod.slice(-200));
    if (!bundel.ok) razlogi.push('bundel: ' + bundel.izhod.slice(-200));
    if (!walk.ok) razlogi.push('walk: ' + walk.izhod.slice(-200));
    vrstica.padci = razlogi;
  }
  fs.appendFileSync(UTRIP, JSON.stringify(vrstica) + '\n', 'utf8');
  const stanje = zdrav ? '∧' : '× ⚠';
  process.stdout.write(
    'ATMA PULZ ' + stanje + ' ' + zdaj + ' · typecheck:' + (typecheck.ok ? 'PASS' : 'FAIL') +
    ' testi:' + (testi.ok ? 'PASS' : 'FAIL') + ' bundel:' + (bundel.ok ? 'PASS' : 'FAIL') +
    ' walk:' + (walk.ok ? 'PASS' : 'FAIL') + ' bliznjica:' + (bliznjica.diha ? 'diha' : 'molci') + '\n',
  );
  if (!zdrav) {
    process.exitCode = 1;
  }
}

main();
