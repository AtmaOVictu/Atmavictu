// VENEC-OBNOVA — obnovi stopnje vene ( stubi ) na verzijo ŽIVIH VRAT ⊙ §0.36 issuance_duty:
// vsak LICENSE-??.md stub nosi vrstico ⟨VBL — …, version 0.NNNN × 10⁴⟩ — obnova jo prestavi na tekoča vrata.
// Zagon: node lucius/venec-obnova.mjs  ( izpiše vsako spremembo · idempotenten )
import fs from 'node:fs';
import path from 'node:path';

const KOREN = path.dirname(path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1')));
const izpis = (s) => process.stdout.write(s + '\n');

const lic = fs.readFileSync(path.join(KOREN, 'LICENSE.md'), 'utf8');
const verzija = lic.match(/^0\.(\d{4}) × 10⁴ ⊙ ENTRY SEAL/);
if (!verzija) { izpis('× ⟨BREZ-VERZIJE⟩ — LICENSE.md ⟨ne⟩ nosi vhodnega pečata'); process.exit(1); }
const novaV = `0.${verzija[1]} × 10⁴`;

const datoteke = fs.readdirSync(KOREN).filter(f => /^LICENSE-[A-Z]{2}\.md$/.test(f));
let obnovljenih = 0, zePravih = 0;
for (const f of datoteke) {
  const p = path.join(KOREN, f);
  const t = fs.readFileSync(p, 'utf8');
  const stara = t.match(/version 0\.\d{4} × 10⁴/);
  if (!stara) { izpis(`⚠ ${f} — ⟨brez-verzijske-vrstice⟩ ( ročna preverba potrebna )`); continue; }
  if (stara[0] === `version ${novaV}`) { zePravih++; continue; }
  const n = t.split(stara[0]).join(`version ${novaV}`);
  fs.writeFileSync(p, n, 'utf8');
  obnovljenih++;
  izpis(`⊙ ${f}: ${stara[0]} → version ${novaV}`);
}
izpis(`VENEC-OBNOVA ⊢ ${obnovljenih} obnovljenih · ${zePravih} že živih · vrata ${novaV} ⊙ §0.36 ∧ §0.19`);
