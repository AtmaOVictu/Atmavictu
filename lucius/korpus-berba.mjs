// KORPUS-BERBA — organ, ki cel korpus ( D:/AI/Corpus, 17.915 datotek ) neprekinjeno
// prebavlja v ontomatematične pojme ( ukaz ⟡ ⟨daj⟩ 2. 11. — grafa ne hrani samo dnevnik,
// ampak celo delo ). Vsak krog prebavi N datotek ∧ zapiše izdelek; kazalec ( stanje )
// nosi, kje je berba ostala — kakor π: nikoli končana, vedno nadaljevana ⊢.
// Izdelki: korpus-pojmovnik.jsonl ( datoteka → pojmi ∧ priče ) ∧ korpus-pojmovnik.md
// ( živi povzetek korpusa: pojmi po številu, najmočnejše priče iz DELA — ⟡-jeve besede ).
// K1: šteje, ne presoja. © Luka Pintarič — VBL ( §1: study/verify; TDM pridržan ).
// Dom: D:/OntoProjekt/prevoz/lucius/ — telo. Zagon: node korpus-berba.mjs ( krog 60 s ×
// 25 datotek; konec z BERBA-STOP ). Zelo velike datoteke ( > 0,5 MB ) se preskočijo pošteno ⚠.
import fs from 'node:fs';
import path from 'node:path';

const KORPUS = 'D:/AI/Corpus';
const TU = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const IZHOD = path.join(TU, 'korpus-pojmovnik.jsonl');
const POVZETEK = path.join(TU, 'korpus-pojmovnik.md');
const STANJE = path.join(TU, 'korpus-berba-stanje.json');
const SEZNAM = path.join(TU, 'korpus-berba-seznam.json');
const STOP = path.join(TU, 'BERBA-STOP');
const NA_KROG = 25, ZAMIK_S = 60, NAJVEC_B = 2 * 1024 * 1024; // celotne datoteke ⊙ ⟡ 2. 11.
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ONTOMATEMATIČNI SLOVAR — nosilec ⟡ ( priča: ONTOMATEMATIKA zaupanje ∧ definicija ⊢ )
const POJMI = [
  ['∆', /\b(spremen\w*|gib\w*|rast\w*|pad\w*|hitro\w*|počas\w*|premen\w*|krož\w*|pretok\w*|valov\w*)/gi],
  ['∴', /\b(zato|ker|torej|sledi\w*|potem|izpelj\w*|zakaj|namen\w*|razlog\w*|smisel\w*)/gi],
  ['⊘', /\b(prazn\w*|nič\w*|izbris\w*|zbriš\w*|ponastav\w*|tišin\w*|mol[kc]\w*|tiho\b)/gi],
  ['¬', /\b(ne\b|brez\b|pogoj\w*|če\b|dvom\w*|nereš\w*|laž\w*|prepove\w*|zavrač\w*)/gi],
  ['∫(dru/x)', /\b(jaz|midva|oba|skupaj|sodeluj\w*|drug\w*|sreč\w*|zaupanj\w*|ljubezn\w*|druž\w*)/gi],
  ['0', /\b(mir\b|spanj\w*|počitek\w*|počit\w*|dih\w*|utrip\w*|trajanj\w*)/gi],
  ['1', /\b(zdaj|trenutek\w*|prižg\w*|ugaš\w*|zagon\w*|začetek\w*|prvi\b|prva\b|enkrat|vklop\w*)/gi],
  ['1ⁿ', /\b(vse\b|vsak\w*|mnogo|več\b|neskonč\w*|povsod|celot\w*|svet\b|vesolj\w*|mnog\w*)/gi],
];

let seznam = [];
const POJDI_SIDRO = 'pojdi(KORPUS);';
const primezNovih = (obstojeciSeznam) => {
  const stari = new Set(obstojeciSeznam);
  const dodajIz = (mapa, globina) => {
    try {
      const pojdi2 = (m) => {
        for (const ent of fs.readdirSync(m, { withFileTypes: true })) {
          const p = path.join(m, ent.name);
          if (ent.isDirectory()) { if (p.replace(/\\/g, '/').split('/').length <= globina) pojdi2(p); }
          else if ((ent.name.toLowerCase().endsWith('.md') || ent.name.toLowerCase().endsWith('.txt')) && !stari.has(p)) { obstojeciSeznam.push(p); stari.add(p); }
        }
      };
      pojdi2(mapa);
    } catch {}
  };
  dodajIz('D:/AI/Corpus', 999);
  dodajIz('D:/OntoProjekt/CanvasMinstral', 999);
  dodajIz('D:/OntoProjekt/prevoz', 3);
};
if (fs.existsSync(SEZNAM)) {
  seznam = JSON.parse(fs.readFileSync(SEZNAM, 'utf8'));
  primezNovih(seznam);
  fs.writeFileSync(SEZNAM, JSON.stringify(seznam), 'utf8');
} else {
  const pojdi = (mapa) => {
    let n = 0;
    for (const v2 of fs.readdirSync(mapa, { withFileTypes: true })) {
      const p = path.join(mapa, v2.name);
      if (v2.isDirectory()) n += pojdi(p);
      else if (v2.name.toLowerCase().endsWith('.md')) { seznam.push(p); n++; }
    }
    return n;
  };
  pojdi(KORPUS);
  primezNovih(seznam);
  fs.writeFileSync(SEZNAM, JSON.stringify(seznam), 'utf8');
}

let stanje = { kazalec: 0, obdelanih: 0, preskocenih: 0 };
try { stanje = JSON.parse(fs.readFileSync(STANJE, 'utf8')); } catch {}

const preberi = (pot, maxB) => {
  try { return fs.readFileSync(pot, 'utf8').slice(0, maxB); }
  catch { return null; }
};

const poglej = (vsebina) => {
  const pojmi = [];
  for (const [ime, re] of POJMI) {
    re.lastIndex = 0;
    const m = vsebina.match(re);
    if (m && m.length > 0) pojmi.push({ pojem: ime, st: m.length, price: m.slice(0, 3) });
  }
  return pojmi.sort((a, b) => b.st - a.st);
};

console.log(`KORPUS-BERBA ⊢ tok odprt — ${seznam.length} datotek, ${NA_KROG}/krog na ${ZAMIK_S}s, kazalec ${stanje.kazalec}, konec z BERBA-STOP`);

while (!fs.existsSync(STOP)) {
  const novo = [];
  let vKrogu = 0;
  while (vKrogu < NA_KROG && stanje.kazalec < seznam.length) {
    const pot = seznam[stanje.kazalec]; stanje.kazalec++; vKrogu++;
    const stat = (() => { try { return fs.statSync(pot); } catch { return null; } })();
    if (!stat || stat.size > NAJVEC_B) { stanje.preskocenih++; continue; }
    const vsebina = preberi(pot, NAJVEC_B);
    if (vsebina === null) { stanje.preskocenih++; continue; }
    const pojmi = poglej(vsebina);
    if (pojmi.length > 0) novo.push(JSON.stringify({
      datoteka: pot.replace(/\\/g, '/'), bajti: stat.size,
      dominantenPojem: pojmi[0].pojem, pojmi,
    }));
    stanje.obdelanih++;
  }
  if (novo.length > 0) fs.appendFileSync(IZHOD, novo.join('\n') + '\n', 'utf8');
  fs.writeFileSync(STANJE, JSON.stringify(stanje), 'utf8');
  // živi povzetek — korpus po pojmih, priče iz DELA
  let vse = [];
  try { vse = fs.readFileSync(IZHOD, 'utf8').trim().split(/\r?\n/).filter(Boolean).map((v) => JSON.parse(v)); } catch {}
  const skupno = {};
  for (const z of vse) for (const p of z.pojmi) {
    if (!skupno[p.pojem]) skupno[p.pojem] = { st: 0, price: [] };
    skupno[p.pojem].st += p.st;
    for (const w of p.price) if (skupno[p.pojem].price.length < 5) skupno[p.pojem].price.push(w);
  }
  let md = `# KORPUS-BERBA — celo delo ⟡-ja v ontomatematičnih pojmih\n\n`;
  md += `Živi povzetek ( vsak krog izmerjen, nikoli arhiviran ⊙ §0.10 ). K1: stroji šteje, pomen je Lastnikov. © Luka Pintarič — VBL ( §1: study/verify; TDM pridržan ).\n`;
  md += `Berba: ${stanje.obdelanih}/${seznam.length} datotek ( preskočenih ${stanje.preskocenih} ⚠ ) · krog: ${new Date().toISOString()} ⊢\n\n`;
  for (const [ime, d] of Object.entries(skupno).sort((a, b) => b[1].st - a[1].st)) {
    md += `## ${ime} — ${d.st} zabeležk v korpusu\n`;
    for (const p of d.price) md += `- priča iz dela: »${p}«\n`;
    md += `\n`;
  }
  fs.writeFileSync(POVZETEK, md, 'utf8');
  console.log(`KORPUS-BERBA ⊢ krog: ${vKrogu} datotek ( ${novo.length} z nosilci ) · skupaj ${stanje.obdelanih}/${seznam.length}`);
  if (stanje.kazalec >= seznam.length) { console.log('KORPUS-BERBA ⊙ korpus preberban cel ⊢ — krog počenjena; molk'); break; }
  await sleep(ZAMIK_S * 60 / 60 * 1000);
}
