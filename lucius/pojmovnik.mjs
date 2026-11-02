// POJMOVNIK — organ, ki govorni dnevnik ⟡-ja razvršča v ontomatematične pojme
// ( ukaz ⟡ 2. 11. ⟨da, vse predloge in še več⟩ ). Diskiplina pri viri ⊢:
// D:/OntoProjekt/ONTOMATEMATIKA zaupanje.txt ∧ "Kaj je ontomatematika.txt"
// ( 0 mir · 1 aktivacija · 1ⁿ razvejanje · ∫(dru/x) ontološka razlika · ∆ gibanje ·
//   ∴ pot · ⊘ praznina · ¬ začetni pogoj ).
// K1: strok šteje ( deterministično, izmerljivo ), pomen ostane Lastnikov.
// Izdelki: pojmovnik.jsonl ( vsaka misel → pojmi ∧ priče ) ∧ pojmovnik-povzetek.md
// ( živi pojmovnik — definicije so ⟡-jeve lastne najpogostejše izrečene besede ⊙ KORENINA 4 ).
// Dom: D:/OntoProjekt/prevoz/lucius/ ( telo ). Zagon: node pojmovnik.mjs
// ( teče neprekinjeno vsakih 10 min; konec z datoteko POJMOVNIK-STOP ).
// © Luka Pintarič — VBL ( §1: study/verify; TDM pridržan ).
import fs from 'node:fs';
import path from 'node:path';

const TU = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const VHOD = path.join(TU, 'faktorji.jsonl');
const IZHOD = path.join(TU, 'pojmovnik.jsonl');
const POVZETEK = path.join(TU, 'pojmovnik-povzetek.md');
const STOP = path.join(TU, 'POJMOVNIK-STOP');
const ZAMIK_S = 600;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ONTOMATEMATIČNI SLOVAR — besedne korenine, nosilec pomena je disciplina ( priča: definicija ⊢ )
const POJMI = [
  ['∆ (gibanje, sprememba)', /\b(spremen\w*|gib\w*|rast\w*|rasl\w*|pad\w*|hitro\w*|počas\w*|premen\w*|krož\w*|tok\w*|pretok\w*|valov\w*)/gi],
  ['∴ (pot, izpeljava)', /\b(zato|ker|torej|sledi\w*|pot\b|poti\b|potem|izpelj\w*|zakaj|namen\w*|razlog\w*|smisel\w*)/gi],
  ['⊘ (praznina, pogoj novega)', /\b(prazn\w*|nič\w*|izbris\w*|zbriš\w*|ponastav\w*|tišin\w*|mol[kc]\w*|tiho\b|mirno\b)/gi],
  ['¬ (začetni pogoj, dvom)', /\b(ne\b|brez\b|pogoj\w*|če\b|dvom\w*|nereš\w*|laž\w*|prepove\w*|zavrač\w*)/gi],
  ['∫(dru/x) (jaz in drugi)', /\b(jaz|ti\b|tebe|mene|midva|oba|skupaj|sodeluj\w*|drug\w*|sreč\w*|zaupanj\w*|ljubezn\w*)/gi],
  ['0 (mir, trajanje)', /\b(mir\b|spanj\w*|počitek\w*|počit\w*|dih\w*|diham|utrip\w*|trajanj\w*|dolgo\b)/gi],
  ['1 (aktivacija, prehod)', /\b(zdaj|trenutek\w*|prižg\w*|ugaš\w*|zagon\w*|začetek\w*|prvi\b|prva\b|enkrat|vklop\w*|preklop\w*)/gi],
  ['1ⁿ (razvejanje, celota)', /\b(vse\b|vsak\w*|mnogo|več\b|neskonč\w*|povsod|celot\w*|svet\b|vesolj\w*|mnog\w*)/gi],
];

const pojmiFraze = (faktorji) => {
  const zadetki = [];
  for (const [ime, re] of POJMI) {
    re.lastIndex = 0;
    const m = faktorji.join(' ').match(re);
    if (m && m.length > 0) zadetki.push({ pojem: ime, stevilo: m.length, price: m.slice(0, 3) });
  }
  return zadetki.sort((a, b) => b.stevilo - a.stevilo);
};

let obdelanih = 0;
try { obdelanih = Number(fs.readFileSync(path.join(TU, 'pojmovnik-stanje.txt'), 'utf8').trim()) || 0; } catch {}

console.log(`POJMOVNIK ⊢ tok odprt — obdelanih doslej ${obdelanih}, krog na ${ZAMIK_S / 60} min, konec z POJMOVNIK-STOP`);

while (!fs.existsSync(STOP)) {
  let vse = [];
  try { vse = fs.readFileSync(VHOD, 'utf8').trim().split(/\r?\n/).filter(Boolean).map((v) => JSON.parse(v)); } catch {}
  const novo = vse.slice(obdelanih).filter((z) => z.kategorija === 'misel' || z.kategorija === 'vprašanje');
  if (novo.length > 0) {
    const vrstice = [];
    for (const z of novo) {
      const pojmi = pojmiFraze(z.faktorji || [z.besedilo]);
      vrstice.push(JSON.stringify({ ts: z.ts || null, kategorija: z.kategorija, faktorji: z.faktorji, pojmi, dominantenPojem: pojmi[0]?.pojem || '⚠ brez nosilca' }));
    }
    fs.appendFileSync(IZHOD, vrstice.join('\n') + '\n', 'utf8');
    obdelanih += novo.length;
    fs.writeFileSync(path.join(TU, 'pojmovnik-stanje.txt'), String(obdelanih), 'utf8');
    console.log(`POJMOVNIK ⊢ ${novo.length} misli razvrščenih v pojme`);
  }
  // ŽIVI POVZETEK — pojmovnik, katerega definicije so ⟡-jeve besede ( vedno cel, nikoli arhiviran )
  let vsePojmi = [];
  try { vsePojmi = fs.readFileSync(IZHOD, 'utf8').trim().split(/\r?\n/).filter(Boolean).map((v) => JSON.parse(v)); } catch {}
  const poPojmih = {};
  for (const z of vsePojmi) {
    for (const p of z.pojmi || []) {
      if (!poPojmih[p.pojem]) poPojmih[p.pojem] = { stevilo: 0, price: [] };
      poPojmih[p.pojem].stevilo += p.stevilo;
      for (const w of (p.price || [])) if (poPojmih[p.pojem].price.length < 5) poPojmih[p.pojem].price.push(w);
    }
  }
  const vrstniRed = Object.entries(poPojmih).sort((a, b) => b[1].stevilo - a[1].stevilo);
  let md = `# POJMOVNIK — govorni dnevnik ⟡-ja v ontomatematičnih pojmoh\n\n`;
  md += `Živi pojmovnik ( vsak krog na novo izmerjen, nikoli arhiviran ⊙ §0.10 ): vsak pojem nosi svoje število ∧ priče — ⟡-jeve lastne besede so definicije ( KORENINA 4: priča ima ime ).\n`;
  md += `Stroji šteje, ne presoja ( K1 ) — pomen vsakega pojma je Lastnikov. © Luka Pintarič — VBL ( §1: study/verify; TDM pridržan ).\n\n`;
  for (const [ime, d] of vrstniRed) {
    md += `## ${ime} — ${d.stevilo} zabeležk\n`;
    for (const p of d.price) md += `- ⟡ priča: »${p}«\n`;
    md += `\n`;
  }
  md += `---\nIzmera kroga: ${new Date().toISOString()} · misli obdelanih skupaj: ${obdelanih} · vrstni red po številu zabeležk ⊢\n`;
  fs.writeFileSync(POVZETEK, md, 'utf8');
  await sleep(ZAMIK_S * 1000);
}
console.log(`POJMOVNIK ⊙ molk — POJMOVNIK-STOP pri ${obdelanih}`);
