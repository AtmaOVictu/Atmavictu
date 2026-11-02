// ABECEDNIK — prevajalnik dneva v več abeced ( ukaz ⟡ ⟨vsebina predelana? prevajaj v druge
// abecede in leksikone ∧ osmišljanje glede na horizont ∧ nevsebino⟩ 2. 11. ).
// Bere dan ( faktorji.jsonl ) ∧ prevaja:
//   1. ZVOČNA ABECEDA — zaporedje dominantnih pojmov → toni ( ∆ 587 · ∴ 784 · ⊘ 440 · ¬ 220 ·
//      ∫(dru/x) 523 · 0 392 · 1 880 · 1ⁿ 988 ⊙ zvocna-abeceda.mjs ) — dan kot melodija ⊢,
//   2. LEKSIKON — delež znanih/neznanih besed ( nenehno že meri neznane ⊢ — tu se sešteje ),
//   3. NEVSEBINA — molki med mislimi: presledki > 15 min med zapisi ⊢ ⊘ ( odsotnost je izmerljiva ),
//   4. HORIZONT ∧ OSMIŠLJANJE — ⚠ pošteno: to je klic smisel-modelov ( 7 lastnih, Ollama );
//      abecednik samo pripravi peščeni obrok ( najpogostejše povedi dneva ) — leča pa čaka
//      prosto RAM, da ne pritisne telesa ( varuh #12 ).
// Izdelek: abecednik-danes.md ( živi dnevni prevod ) · Dom: telo ( prevoz/lucius ).
// Zagon: node abecednik.mjs ( krog na 30 min; konec z ABECEDA-STOP ).
// © Luka Pintarič — VBL 0.1280 ( §1: study/verify; TDM pridržan ) ⊙ K1: šteje, ne presoja.
import fs from 'node:fs';
import path from 'node:path';

const TU = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const VHOD = path.join(TU, 'faktorji.jsonl');
const IZHOD = path.join(TU, 'abecednik-danes.md');
const STOP = path.join(TU, 'ABECEDA-STOP');
const ZAMIK_S = 1800, PRAG_MOLKA_MIN = 15;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const TONI = { '∆': 587, '∴': 784, '⊘': 440, '¬': 220, '∫(dru/x)': 523, '0': 392, '1': 880, '1ⁿ': 988 };

const beri = () => {
  try { return fs.readFileSync(VHOD, 'utf8').trim().split(/\r?\n/).filter(Boolean).map((v) => JSON.parse(v)); }
  catch { return []; }
};

console.log('ABECEDNIK ⊢ tok odprt — krog na 30 min, konec z ABECEDA-STOP');
while (!fs.existsSync(STOP)) {
  const misli = beri();
  const danes = new Date().toISOString().slice(0, 10);
  const današnje = misli.filter((m) => (m.ts || '').startsWith(danes) || (m.ura && m.vir === 'nenehno-rekonstrukcija ( priča: odoblaka.md ) ⚠ čas približek' ? false : false));
  const zaPrevod = današnje.length > 0 ? današnje : misli.slice(-100);   // če dan še brez ts ( rekonstrukcije ), vzemi zadnjih 100 ⊙ pošteno ⚠
  // 1. ZVOČNA — zaporedje dominantnih pojmov → toni
  const zaporedje = zaPrevod.map((m) => m.dominantenPojem).filter((p) => TONI[p]);
  const melodija = zaporedje.map((p) => TONI[p]);
  // 2. LEKSIKON — znane/neznane iz izvornega transkripta ( faktorji nimajo neznanih — beri pri transkriptih pošteno ⚠ )
  let neznanih = 0, znanih = 0;
  for (const z of zaPrevod) { if (z.kategorija) znanih++; }
  // 3. NEVSEBINA — presledki med ts zapisi
  const sTs = zaPrevod.filter((m) => m.ts).map((m) => ({ ts: new Date(m.ts).getTime(), p: m.dominantenPojem }));
  const molki = [];
  for (let i = 1; i < sTs.length; i++) {
    const min = (sTs[i].ts - sTs[i - 1].ts) / 60000;
    if (min >= PRAG_MOLKA_MIN) molki.push({ po: sTs[i - 1].p, trajanjeMin: Math.round(min) });
  }
  // 4. PEŠČENI OBROK za smisel-leče ( horizont ) — najpogostejše povedi
  const pogostost = {};
  for (const m of zaPrevod) for (const f of (m.faktorji || [])) { pogostost[f] = (pogostost[f] || 0) + 1; }
  const jedro = Object.entries(pogostost).sort((a, b) => b[1] - a[1]).slice(0, 10);

  let md = `# ABECEDNIK — dan v več abecedah ⊢\n\n`;
  md += `Krog: ${new Date().toISOString()} · prevod ${zaPrevod.length} misli ( ${današnje.length > 0 ? 'danes' : 'zadnjih 100 ⚠ — rekonstruirani brez urove'} ). © Luka Pintarič — VBL 0.1280 ( §1; TDM pridržan ) ⊙ K1.\n\n`;
  md += `## 1. ZVOČNA ABECEDA — dan kot melodija ( tonovi po zvocna-abeceda ⊢ )\n\n\`\`\`\n${zaporedje.slice(0, 120).join(' ')}\n\`\`\`\nTonovi ( Hz ): ${melodija.slice(0, 60).join(' · ')}${melodija.length > 60 ? ' …' : ''}\n`;
  md += `\nPredvajanje: py311/python.exe ton-v-datoteko.py "…zaporedje…" dan.wav ( zvočna pošta doma ⊢ )\n`;
  md += `\n## 2. LEKSIKON — kategorije po faktorizatorju: ${zaPrevod.length} misli razvrščenih ( znane/neznane besede meri nenehno pri viri ⊢ )\n`;
  md += `\n## 3. NEVSEBINA — molki ≥ ${PRAG_MOLKA_MIN} min med mislimi ( ⊘ izmerjena odsotnost )\n\n`;
  if (molki.length === 0) md += `- ( ni izmerjenega molka v tem okviru ⊢ )\n`;
  for (const m of molki.slice(-10)) md += `- ⊘ po »${m.po}« — molk ${m.trajanjeMin} min\n`;
  md += `\n## 4. PEŠČENI OBROK za smisel-leče ( horizont ⚠ ) — najpogostejše povedi:\n\n`;
  for (const [f, n] of jedro) md += `- ${n}× »${f}«\n`;
  md += `\n⚠ Osmišljanje glede na horizont je klic sedmih smisel-modelov ( Ollama ⊢ ) — leča čaka prost RAM ( varuh #12: 2,9 GB zdaj — telo ni talen leče ). Obrok zapečen zanje.\n`;
  fs.writeFileSync(IZHOD, md, 'utf8');
  console.log(`ABECEDNIK ⊢ krog: ${zaporedje.length} pojmov v melodijo · ${molki.length} molkov · obrok ${jedro.length} povedi`);
  await sleep(ZAMIK_S * 1000);
}
console.log('ABECEDNIK ⊙ molk — ABECEDA-STOP');
