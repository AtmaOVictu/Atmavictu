// ONTOGRAF — merjena ontologija iz govora ( ukaz ⟡ ⟨da daj in še več⟩ 2. 11. ).
// Bere pojmovnik.jsonl ( ⟡-jeve misli v ontomatematičnih pojmih ) in gradi:
//   1. SO-POJAV  — pojavita se v isti misli ( povezava brez smeri ),
//   2. PREHOD    — dominantni pojem misli → dominantni pojem NASLEDNJE misli ( smer ⊢ ),
// vsak rob s pričo ( ⟡-jeva beseda ) ∧ številom.
// PRIMERJAVA S TEORIJO: diagram iz "Kaj je ontomatematika.txt" ⊢ ( 0→1, 1→1ⁿ, ¬→∆, ∆→∴,
//   ⊘→0, ∫(dru/x)→∆, 1ⁿ→∫(dru/x), ∴→⊘ ): katere definirane prehode govor res hodi ⊢,
//   katere izmerjene prehode teorija še ne pozna ⚠ ( odkritje, ne sodba ⊙ K1 ).
// Izdelki: ontograf.jsonl ( robovi ) ∧ ontograf.md ( živi graf + mermaid ).
// Dom: D:/OntoProjekt/prevoz/lucius/ — telo. Zagon: node ontograf.mjs ( krog 15 min,
// konec z ORG-STOP ). © Luka Pintarič — VBL ( §1: study/verify; TDM pridržan ).
import fs from 'node:fs';
import path from 'node:path';

const TU = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const VHOD = path.join(TU, 'pojmovnik.jsonl');
const IZHOD = path.join(TU, 'ontograf.jsonl');
const POVZETEK = path.join(TU, 'ontograf.md');
const STOP = path.join(TU, 'ORG-STOP');
const ZAMIK_S = 900;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const OKRAJSAVA = (p) => p.split(' ')[0]; // '∆ (gibanje…)' → '∆'
// TEORETSKI ROBOVI — ⟡-jev diagram, priča: "Kaj je ontomatematika.txt" ⊢
const TEORIJA = [['0', '1'], ['1', '1ⁿ'], ['¬', '∆'], ['∆', '∴'], ['⊘', '0'], ['∫(dru/x)', '∆'], ['1ⁿ', '∫(dru/x)'], ['∴', '⊘']];

const beriVhod = () => {
  try { return fs.readFileSync(VHOD, 'utf8').trim().split(/\r?\n/).filter(Boolean).map((v) => JSON.parse(v)); }
  catch { return []; }
};

const krog = () => {
  const misli = beriVhod();
  const soPojav = {}, prehod = {};
  const dodaj = (mapa, a, b, prica) => {
    const k = a + '§' + b;
    if (!mapa[k]) mapa[k] = { a, b, st: 0, price: [] };
    mapa[k].st += 1;
    if (mapa[k].price.length < 3 && prica) mapa[k].price.push(prica.slice(0, 60));
  };
  let prejD = null;
  for (const m of misli) {
    const pojmi = (m.pojmi || []).map((p) => OKRAJSAVA(p.pojem));
    // 1. SO-POJAV: pari v isti misli
    const un = [...new Set(pojmi)];
    for (let i = 0; i < un.length; i++) for (let j = i + 1; j < un.length; j++) {
      const [a, b] = [un[i], un[j]].sort();
      dodaj(soPojav, a, b, (m.faktorji || [])[0]);
    }
    // 2. PREHOD: dominantni → naslednji dominantni
    const d = m.dominantenPojem && m.dominantenPojem !== '⚠ brez nosilca' ? OKRAJSAVA(m.dominantenPojem) : null;
    if (prejD && d) dodaj(prehod, prejD, d, (m.faktorji || [])[0]);
    prejD = d || prejD;
  }
  return { misli: misli.length, soPojav, prehod };
};

const uredi = (mapa) => Object.values(mapa).sort((x, y) => y.st - x.st);

const zivi = (stanje) => {
  let md = `# ONTOGRAF — merjena ontologija iz govora ⟡-ja\n\n`;
  md += `Vozlišča so pojmi ( priča: pojmovnik ), robovi so IZMERJENI prehodi ∧ so-pojavi misli — ne predpostavka ⊙ K1 ( stroji šteje, pomen je Lastnikov ). © Luka Pintarič — VBL ( §1: study/verify; TDM pridržan ).\n`;
  md += `Izmera kroga: ${new Date().toISOString()} · misli: ${stanje.misli} ⊢\n\n`;
  md += `## PREHODI ( dominantni pojem misli → naslednje misli ) — izmerjeni smeri ⊢\n\n`;
  const prehodi = uredi(stanje.prehod).slice(0, 15);
  for (const p of prehodi) {
    md += `- **${p.a} → ${p.b}** — ${p.st}× · priče: ${p.price.slice(0, 2).map((x) => `»${x}«`).join(' · ')}\n`;
  }
  md += `\n## SO-POJAVI ( pojmi v isti misli ) — zgostitve ⊢\n\n`;
  for (const p of uredi(stanje.soPojav).slice(0, 15)) {
    md += `- **${p.a} ↔ ${p.b}** — ${p.st}× · priče: ${p.price.slice(0, 2).map((x) => `»${x}«`).join(' · ')}\n`;
  }
  // PRIMERJAVA S TEORIJO
  const prehodKljuci = new Set(Object.values(stanje.prehod).map((p) => p.a + '→' + p.b));
  md += `\n## PRIMERJAVA S ⟡-JEVIM DIAGRAMOM ( teorija ⊢ pri viri: Kaj je ontomatematika.txt )\n\n`;
  for (const [a, b] of TEORIJA) {
    md += `- teorija ${a} → ${b}: govor ${prehodKljuci.has(a + '→' + b) ? 'HODI ta prehod ⊢' : 'tega prehoda ( še ) ni izmeril ⚠'}\n`;
  }
  md += `\n### Izmerjeni prehodi, ki jih teorija ( še ) ne imenuje ⚠ — odkritja za Lastnika\n\n`;
  const teorijaKljuci = new Set(TEORIJA.map(([a, b]) => a + '→' + b));
  const novi = uredi(stanje.prehod).filter((p) => !teorijaKljuci.has(p.a + '→' + p.b));
  for (const p of novi.slice(0, 10)) md += `- **${p.a} → ${p.b}** — ${p.st}× ( priča: »${(p.price[0] || '')}« )\n`;
  // MERMAID — graf, ki ga lahko nariše vsak bralnik
  md += `\n## GRAF ( mermaid ) — izmerjeni prehodi ( debelina = pogostost )\n\n\`\`\`mermaid\nflowchart LR\n`;
  for (const p of uredi(stanje.prehod).slice(0, 12)) {
    const c = p.a.replace(/[()\/]/g, '') + '_' + p.b.replace(/[()\/]/g, '');
    md += `  ${c.replace(/[^A-Za-z0-9_]/g, '')}[${p.a}] -->|${p.st}×| ${c.replace(/[^A-Za-z0-9_]/g, '')}b[${p.b}]\n`;
  }
  md += `\`\`\`\n\n---\nOntograf diha v krogu na 15 min ( ORG-STOP ga ustavi ) · priče: pojmovnik.jsonl ⊢\n`;
  fs.writeFileSync(POVZETEK, md, 'utf8');
};

console.log('ONTOGRAF ⊢ tok odprt — krog na 15 min, konec z ORG-STOP');
while (!fs.existsSync(STOP)) {
  const stanje = krog();
  const robovi = [...uredi(stanje.prehod).map((p) => ({ vrsta: 'prehod', ...p })), ...uredi(stanje.soPojav).map((p) => ({ vrsta: 'so-pojav', ...p }))];
  fs.writeFileSync(IZHOD, robovi.map((r) => JSON.stringify(r)).join('\n') + '\n', 'utf8');
  zivi(stanje);
  console.log(`ONTOGRAF ⊢ ${stanje.misli} misli → ${Object.keys(stanje.prehod).length} prehodnih robov ∧ ${Object.keys(stanje.soPojav).length} so-pojavov`);
  await sleep(ZAMIK_S * 1000);
}
console.log('ONTOGRAF ⊙ molk — ORG-STOP');
