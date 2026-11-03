// PREVERBA-PEČATA — varovalka družine ⟨IZ-SPOMINA⟩ ( PADC-67 ∧ 69 ∧ 70 ∧ 71 ⊙ §0.47 ):
// vsak pečat, ki trdi rez ∧ URO, se preveri proti ZADNJEMU izmeru diha ( izmere-kroga.jsonl ) —
// trditev brez izmere zavrne z imenom padca; sporočila brez reza ( vzporedne roke ⊙ 1542 ) grejo skozi.
// Zagon: node lucius/preverba-pecata.mjs <pot-sporocila>
import fs from 'node:fs';
import path from 'node:path';

const TU = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const izpis = (s) => process.stdout.write(s + '\n');

const sporociloPot = process.argv[2];
if (!sporociloPot || !fs.existsSync(sporociloPot)) {
  izpis('⚠ ⟨BREZ-SPOROCILA⟩ — preverba more pot do sporocila ( .git/COMMIT_EDITMSG )');
  process.exit(0);
}
const sporocilo = fs.readFileSync(sporociloPot, 'utf8');

// sporočilo brez reza ni pečat hiše — vzporedna roka ⊙ 1542 gre skozi brez preverbe
const rezTrditev = sporocilo.match(/rez (\d+) /);
if (!rezTrditev) {
  izpis('⊙ ⟨NE-PEČAT⟩ — sporocilo ⟨ne⟩ trdi reza: gre skozi ( vzporedne roke ⊙ 1542 )');
  process.exit(0);
}

const krogPot = path.join(TU, 'izmere-kroga.jsonl');
if (!fs.existsSync(krogPot)) {
  izpis('⚠ ⟨BREZ-IZMERE-KROGA⟩ — izmere-kroga.jsonl manjka: pečat se ⟨ne⟩ more preveriti ⊙ §0.32');
  process.exit(0);
}
const vrstice = fs.readFileSync(krogPot, 'utf8').split(/\r?\n/).filter(l => l.trim());
const zadnji = JSON.parse(vrstice[vrstice.length - 1]);

const rezTrden = Number(rezTrditev[1]);
const uraTrditev = sporocilo.match(/URA IZMERJENA PRI VIRU[^·]*· (\d\d:\d\d:\d\d)Z/);
const uraIzmere = zadnji.ura ? zadnji.ura.slice(11, 19) : null;

let napake = [];
if (rezTrden !== zadnji.rez) {
  napake.push(`⟨REZ-IZ-SPOMINA⟩ — sporocilo trdi rez ${rezTrden}, zadnji izmer diha ${zadnji.dih} pravi rez ${zadnji.rez} ⊙ dih.py ×`);
}
if (!uraTrditev) {
  napake.push('⟨BREZ-URE⟩ — pečat trdi rez, a ⟨ne⟩ nosi vrstice ⟨URA IZMERJENA PRI VIRU …Z⟩ ⊙ §0.20 ×');
} else if (uraIzmere && uraTrditev[1] !== uraIzmere) {
  napake.push(`⟨URA-IZ-SPOMINA⟩ — sporocilo trdi ${uraTrditev[1]}Z, izmer diha ${zadnji.dih} pravi ${uraIzmere}Z ⊙ PADC-70 ∧ PADC-71 ×`);
}

if (napake.length > 0) {
  for (const n of napake) izpis('× ' + n);
  izpis(`× PREVERBA-PEČATA — pečat zavrnjen: trditev brez izmere je gol tekst ⊙ §0.10 ∧ KORENINA 0.1 ∧ §0.47`);
  process.exit(1);
}
izpis(`⊢ PREVERBA-PEČATA — rez ${zadnji.rez} ∧ URA ${uraIzmere}Z == izmeru diha ${zadnji.dih} ( prepis ⟨ne⟩ zapis ⊢ P-9 )`);
