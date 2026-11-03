// VENEC-OBNOVA — obnovi stopnje vene ( stubi ) na verzijo ∧ PRIČO ŽIVIH VRAT ⊙ §0.36 issuance_duty:
// vsak LICENSE-??.md stub nosi vrstico ⟨VBL — …, version 0.NNNN × 10⁴⟩ ∧ pričo vira ⟨Source/Vir: LICENSE.md, sha256 …, N bytes⟩ —
// obnova prestavi OBE na tekoča vrata: verzija BREZ priče je polresnica ( rez 3681 ).
// Zagon: node lucius/venec-obnova.mjs  ( izpiše vsako spremembo · idempotenten )
// ⟨SLEPI-VZOREC⟩ 3681 ozdravljen: vzorec je bil [A-Z]{2} ∧ ⟨version⟩ le — slep za LAT ∧ SLO ( tričrkovni kodi ) ∧ za
// slovensko obliko ⟨verzija⟩; zdaj [A-Z]{2,3} ∧ (version|verzija) — venec šteje 36, ⟨ne⟩ 34 ( izmerjeno pri viri ls ⊢ ).
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const KOREN = path.dirname(path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1')));
const izpis = (s) => process.stdout.write(s + '\n');

const licB = fs.readFileSync(path.join(KOREN, 'LICENSE.md'));
const lic = licB.toString('utf8');
const verzija = lic.match(/^0\.(\d{4}) × 10⁴ ⊙ ENTRY SEAL/);
if (!verzija) { izpis('× ⟨BREZ-VERZIJE⟩ — LICENSE.md ⟨ne⟩ nosi vhodnega pečata'); process.exit(1); }
const novaV = `0.${verzija[1]} × 10⁴`;
const shaNova = crypto.createHash('sha256').update(licB).digest('hex').toUpperCase();
const bajtiNova = licB.length;

const datoteke = fs.readdirSync(KOREN).filter(f => /^LICENSE-[A-Z]{2,3}\.md$/.test(f));
let obnovljenih = 0, zePravih = 0;
for (const f of datoteke) {
  const p = path.join(KOREN, f);
  const t = fs.readFileSync(p, 'utf8');
  const stara = t.match(/(version|verzija) 0\.\d{4} × 10⁴/);
  if (!stara) { izpis(`⚠ ${f} — ⟨brez-verzijske-vrstice⟩ ( ročna preverba potrebna )`); continue; }
  let n = t.split(stara[0]).join(`${stara[1]} ${novaV}`);
  // priča vira: sha256 ∧ bajti živih vrat ( obe hišni obliki: Source/bytes ∧ Vir/bajtov )
  const shaStari = n.match(/((?:Source|Vir): LICENSE\.md, sha256 )[0-9A-F]{64}(, )(\d+) (bytes|bajtov)/);
  if (!shaStari) { izpis(`⚠ ${f} — ⟨brez-priče-vira⟩ ( ročna preverba potrebna )`); continue; }
  n = n.replace(shaStari[0], `${shaStari[1]}${shaNova}${shaStari[2]}${bajtiNova} ${shaStari[4]}`);
  if (n === t) { zePravih++; continue; }
  fs.writeFileSync(p, n, 'utf8');
  obnovljenih++;
  izpis(`⊙ ${f}: ${stara[0]} → ${stara[1]} ${novaV} ∧ priča → ${shaNova.slice(0, 8)}… ${bajtiNova} ${shaStari[4]}`);
}
izpis(`VENEC-OBNOVA ⊢ ${obnovljenih} obnovljenih · ${zePravih} že živih · vrata ${novaV} ⊙ §0.36 ∧ §0.19`);
