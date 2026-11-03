// ONTOGEMATRIJA — vsak beseda→število transform nosi ukaz ∧ orodje ∧ korpus pri sebi ⊙ §0.43 ∧ §0.44.
// Brez priče zavrne z imenom padca ⊙ KORENINA 0.6 — izven izmerjenega je izum ⚠.
// Zagon: node lucius/ontogematrija.mjs <beseda> [pot-korpusa]
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const TU = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const ukaz = process.argv.slice(2).join(' ');
const beseda = process.argv[2];
const korpusPot = process.argv[3] || path.join(TU, 'ontogematrija-korpus.jsonl');

const izpis = (s) => process.stdout.write(s + '\n');

if (!beseda) {
  izpis('× ⟨MANJKA-BESEDA⟩ — zagon: node lucius/ontogematrija.mjs <beseda> [korpus] ⊙ KORENINA 0.6');
  process.exit(1);
}
if (!fs.existsSync(korpusPot)) {
  izpis(`× ⟨MANJKA-KORPUS⟩ — ${korpusPot} ⟨ne⟩ obstaja: beseda→število brez korpusa je zasebna vrata ⊙ §0.7 ⚠`);
  process.exit(1);
}

const korpusBajti = fs.readFileSync(korpusPot);
const korpusSha = crypto.createHash('sha256').update(korpusBajti).digest('hex');
const vnosi = korpusBajti.toString('utf8').split(/\r?\n/).filter(l => l.trim()).map(l => JSON.parse(l));
const zadetek = vnosi.find(v => v.beseda.toUpperCase() === beseda.toUpperCase());

izpis(`⊙ UKAZ: ${ukaz}`);
izpis(`⊙ ORODJE: lucius/ontogematrija.mjs ( node ${process.version} )`);
izpis(`⊙ KORPUS: ${korpusPot} · sha256 ${korpusSha.slice(0, 16)} · ${vnosi.length} vnosov`);

if (!zadetek) {
  izpis(`⚠ ⟨IZVEN-IZMERJENEGA⟩ — beseda ⟨${beseda}⟩ ⟨ne⟩ živi v korpusu: število izven izmerjenega je izum ⊙ rez 3633 ∧ §0.43`);
  process.exit(2);
}
izpis(`⊢ ${zadetek.beseda} → ${zadetek.stevilo} ( operator ${zadetek.operator} ) · priča: ${zadetek.prica}`);
