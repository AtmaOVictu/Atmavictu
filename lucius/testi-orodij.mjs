// TESTI-ORODIJ — preverba preverjalcev ( popis lukenj 2026-10-21, luknja 9 ):
// orodje, ki preverja druge, more biti samo preverjeno.
// Zagon: node lucius/testi-orodij.mjs   ( standalone; npm test pokriva samo src/ )
import { test } from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const TU = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const vozli = (skripta, args) => execFileSync('node', [path.join(TU, skripta), ...args], { encoding: 'utf8' });
const zacasi = (vsebina) => {
  const d = fs.mkdtempSync(path.join(os.tmpdir(), 'lucius-test-'));
  const p = path.join(d, 'znak.txt');
  fs.writeFileSync(p, vsebina, 'utf8');
  return p;
};

test('cistina: cirilsko ime datoteke ni vec mogoce — ulovi cirilico v vsebini', () => {
  const p = zacasi('preizkusna vrstica\nzapis z е cirilsko\n');
  let izhod = '';
  let padla = false;
  try { vozli('čistina.mjs', [p]); } catch (e) { padla = true; izhod = e.stdout + e.stderr; }
  assert.ok(padla, 'cistina more pasti na cirilici ( exit 1 )');
  assert.match(izhod, /cirilica/);
});

test('cistina: cista datoteka gre skozi z ⊢', () => {
  const p = zacasi('preizkusna vrstica brez ran\n');
  const izhod = vozli('čistina.mjs', [p]);
  assert.match(izhod, /cirilice 0/);
});

test('druga-rota: slovar mode najde geslo ime ( Lukov slovar, Worth )', { skip: !fs.existsSync('D:/Worth/slovenian_dictionary') }, () => {
  const izhod = vozli('druga-rote.mjs', ['--slovar', 'ime']);
  assert.match(izhod, /pomen/);
});

test('druga-rota: leksikon obstaja in ni prazen ( znane + prepovedane )', () => {
  const znane = fs.readFileSync(path.join(TU, 'znane-besede.txt'), 'utf8')
    .split('\n').filter((v) => v.trim() && !v.startsWith('#'));
  const prepovedane = fs.readFileSync(path.join(TU, 'prepovedane-besede.txt'), 'utf8')
    .split('\n').filter((v) => v.trim() && !v.startsWith('#'));
  assert.ok(znane.length >= 20, `znane-besede preštete ( ${znane.length} ) — more biti vsaj 20`);
  assert.ok(prepovedane.includes('poščeno'), 'padec vnos 4 mora ostati prepovedan ×');
});

test('varuj-most: ciljna mapa obstaja po zagonu ( kopija zapečena )', { skip: !fs.existsSync('D:/OntoProjekt') }, () => {
  vozli('varuj-most.mjs', []);
  assert.ok(fs.readdirSync('D:/OntoProjekt/varnostne-kopije-mosta').length >= 2, 'dnevnik + vsaj ena kopija ⊢');
});
