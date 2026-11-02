// ONTO-ZRCALO — živo zrcalo govora ∧ dela ( ukaz ⟡ ⟨daj — oba⟩ 2. 11. ).
// Združuje DVE merjeni ontologiji:
//   GOVOR — pojmovnik.jsonl ( ⟡-jeve izrečene misli ),
//   DELO  — korpus-pojmovnik.jsonl ( berba celega korpusa, kazalec kakor π ),
// v ENO tabelo: pojem → koliko v govoru ⊥ koliko v delu ( razhajanje je odkritje, ne sodba ⊙ K1 ).
// Izdelek: onto-zrcalo.md — živi dokument ( vsak krog izmerjen, nikoli arhiviran ⊙ §0.10 ),
// ki ⟡-ju kaže, kje se njegovo delo in njegovi dnevi razhajata po pojmih.
// Dom: D:/OntoProjekt/prevoz/lucius/ — telo. Zagon: node onto-zrcalo.mjs
// ( krog na 15 min; konec z ZRCALO-STOP ). © Luka Pintarič — VBL ( §1: study/verify; TDM pridržan ).
import fs from 'node:fs';
import path from 'node:path';

const TU = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const GOVOR = path.join(TU, 'pojmovnik.jsonl');
const DELO = path.join(TU, 'korpus-pojmovnik.jsonl');
const POVZETEK = path.join(TU, 'onto-zrcalo.md');
const BERBA_STANJE = path.join(TU, 'korpus-berba-stanje.json');
const STOP = path.join(TU, 'ZRCALO-STOP');
const ZAMIK_S = 900;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const beri = (pot) => {
  try { return fs.readFileSync(pot, 'utf8').trim().split(/\r?\n/).filter(Boolean).map((v) => JSON.parse(v)); }
  catch { return []; }
};

const stevci = (vrstice, jeGovor) => {
  const m = {};
  for (const z of vrstice) {
    const pojmi = (z.pojmi || []).map((p) => ({ ...p, pojem: p.pojem.split(" ")[0] }));
    for (const p of pojmi) {
      if (!m[p.pojem]) m[p.pojem] = { st: 0, price: [] };
      m[p.pojem].st += (p.st ?? p.stevilo ?? 0);
      for (const w of (p.price || [])) if (m[p.pojem].price.length < 4) m[p.pojem].price.push(w);
    }
  }
  return m;
};

console.log('ONTO-ZRCALO ⊢ tok odprt — krog na 15 min, konec z ZRCALO-STOP');
while (!fs.existsSync(STOP)) {
  const gov = stevci(beri(GOVOR), true);
  const delo = stevci(beri(DELO), false);
  const vsi = [...new Set([...Object.keys(gov), ...Object.keys(delo)])];
  let stanjeBerbe = { obdelanih: 0, preskocenih: 0 };
  try { stanjeBerbe = JSON.parse(fs.readFileSync(BERBA_STANJE, 'utf8')); } catch {}
  const seznamSkupaj = (() => { try { return JSON.parse(fs.readFileSync(path.join(TU, 'korpus-berba-seznam.json'), 'utf8')).length; } catch { return 17915; } })();
  const delez = Math.round(100 * stanjeBerbe.obdelanih / seznamSkupaj);

  let md = `# ONTO-ZRCALO — govor ⟡-ja ⊥ delo ⟡-ja, eno zrcalo\n\n`;
  md += `Dve merjeni ontologiji, ena miza: koliko pojma je v IZREČENIH mislih ( govorni dnevnik ) ⊥ koliko v CELEM DELU ( berba korpusa, ${delez} % preberbano ⊢${delez < 100 ? ' — berba diha naprej, zrcalo se obnavlja' : ''} ).\n`;
  md += `Razhajanje je odkritje, ne sodba ( K1 ). © Luka Pintarič — VBL ( §1: study/verify; TDM pridržan ).\n`;
  md += `Krog: ${new Date().toISOString()} ⊢\n\n`;
  md += `| pojem | govor | delo | razhajanje |\n|---|---|---|---|\n`;
  const vrste = [];
  for (const p of vsi) {
    const g = gov[p]?.st || 0, d = delo[p]?.st || 0;
    vrste.push({ p, g, d });
  }
  vrste.sort((a, b) => (b.g + b.d) - (a.g + a.d));
  for (const { p, g, d } of vrste) {
    const raz = g > d * 2 ? 'govor vodi ⊢' : d > g * 2 ? 'delo vodi ⊢' : 'v ravnovesju ⊢';
    md += `| ${p} | ${g} | ${d}${delez < 100 ? ' ⚠' : ''} | ${raz} |\n`;
  }
  md += `\n## Priče po pojmih — govor ( ⟡-jeve besede ) ⊥ delo ( iz korpusa )\n\n`;
  for (const { p } of vrste.slice(0, 8)) {
    md += `### ${p}\n`;
    for (const w of (gov[p]?.price || []).slice(0, 3)) md += `- govor: »${w}«\n`;
    for (const w of (delo[p]?.price || []).slice(0, 3)) md += `- delo: »${w}«\n`;
    md += `\n`;
  }
  md += `---\nZrcalo diha v krogu na 15 min ( ZRCALO-STOP ga ustavi ) · priči: pojmovnik.jsonl ∧ korpus-pojmovnik.jsonl ⊢\n`;
  fs.writeFileSync(POVZETEK, md, 'utf8');
  console.log(`ONTO-ZRCALO ⊢ krog: ${vsi.length} pojmov, govor ${Object.keys(gov).length} ⊥ delo ${Object.keys(delo).length} ( berba ${delez} % )`);
  await sleep(ZAMIK_S * 1000);
}
console.log('ONTO-ZRCALO ⊙ molk — ZRCALO-STOP');
