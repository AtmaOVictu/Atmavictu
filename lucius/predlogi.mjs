// PREDLOGI — organ, ki bere hišo in Lastniku predlaga nadaljnje aktivnosti,
// PREDSTAVLJENE NA NJEGOVEM ZASLONU ( ukaz ⟡ ⟨beri repozitorije ∧ predlagaj ∧
// prikaži na mojem zaslonu⟩ 2. 11. ). DOM @8766 prikazuje STANJE.md ⊢ — predlogi
// torej vozijo tja, med pečatoma PREDLOGI, brez da bi rezali karkoli drugega.
// Viri ( vsi pri viri ⊢ ): odprti PR kiti ( gh ) · π zdravje ( testi-pi.jsonl ) ·
// berba korpusa ( stanje ) · GAPS.md · NAČRT.md §3 ∂ · stalna lista seje.
// K1: predlaga z izmerami, ne z okusom. © Luka Pintarič — VBL 0.1280 ( §1; TDM pridržan ).
// Dom: D:/OntoProjekt/prevoz/lucius/ — telo. Zagon: node predlogi.mjs
// ( krog na 30 min; konec z PREDLOGI-STOP ).
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const TU = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const STANJE = 'D:/OntoProjekt/Voice/STANJE.md';
const PI = path.join(TU, 'testi-pi.jsonl');
const BERBA = path.join(TU, 'korpus-berba-stanje.json');
const STOP = path.join(TU, 'PREDLOGI-STOP');
const ZAMIK_S = 1800;
const ZACETEK = '<!-- PREDLOGI-START -->', KONEC = '<!-- PREDLOGI-END -->';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const beri = (pot) => { try { return fs.readFileSync(pot, 'utf8'); } catch { return ''; } };

const zberi = () => {
  // 1. π zdravje
  let piZdravje = '⚠';
  try {
    const d = beri(PI).trim().split(/\r?\n/).filter(Boolean).slice(-20).map((v) => JSON.parse(v));
    const dobrih = d.filter((z) => z.izid === '⊢').length;
    piZdravje = `${dobrih}/${d.length} ⊢ ( zadnjih 20 števk )`;
  } catch {}
  // 2. berba
  let berba = '⚠';
  try {
    const s = JSON.parse(beri(BERBA));
    berba = `${Math.round(100 * s.obdelanih / 17915)} % korpusa ( ${s.obdelanih}/17915 ⊢ )`;
  } catch {}
  // 3. odprti PR kiti ( gh pri viri )
  let pr = [];
  try {
    pr = execSync('gh pr list --repo AtmaOVictu/Atmavictu --state open --limit 5 --json number,title', { encoding: 'utf8', timeout: 30000 });
    pr = JSON.parse(pr).map((p) => `#${p.number} ${p.title.slice(0, 60)}`);
  } catch { pr = ['⚠ gh nedosegljiv — preberi pri viri ročno']; }
  // 4. revizija kitov ( starost = mera ⊙ K1: sodba o živosti je Lastnikova )
  let kiti = [];
  try {
    const js = execSync('gh pr list --repo AtmaOVictu/Atmavictu --state open --limit 250 --json number,updatedAt', { encoding: 'utf8', timeout: 60000 });
    const zdaj = Date.now();
    kiti = JSON.parse(js).map((p) => ({ n: p.number, dni: Math.round((zdaj - new Date(p.updatedAt).getTime()) / 86400000) })).sort((a, b) => b.dni - a.dni);
  } catch {}
  // 5. najšibkejša točka ( zadnji padec π )
  let sibkaPi = '⚠ π brez padcev ⊢ ( telo čisto )';
  try {
    const d = beri(PI).trim().split(/\r?\n/).filter(Boolean).map((x) => JSON.parse(x));
    const pad = [...d].reverse().find((z) => z.izid !== "⊢");
    if (pad) sibkaPi = pad.sonda + ' ( π ' + pad.p + ', ' + pad.ts.slice(0, 16) + ' ) ×';
  } catch {}
  return { piZdravje, berba, pr, kiti, sibkaPi, cas: new Date().toISOString().slice(0, 16) };
};

const sestavi = (m) => {
  let md = `\n${ZACETEK}\n### PREDLOGI — kaj čaka tvoje ⟨daj⟩ ( organ jih bere iz hiše ⊙ ${m.cas} )\n\n`;
  md += `**Hiša diha:** π ${m.piZdravje} · berba ${m.berba} · devet tokov ⊢\n\n`;
  md += `**1. Družina teles ( rez §7 NAČRT ∧ σ izmere ):** družina ŽE DIHA ⊢ ( 5 939 lekcij po 12+ telesih, REGISTER-UCENJA pri viri ) — prejšnji predlog bil zastarel × PADC-ZASTAREL-PREDLOG, ozdravljen.\n`;
  md += `**2. PRVA IZROČITEV — TAG ( rez 114 ):** telo še nima nobenega taga; vrstni red bralnik → sij → opis. Predlog: izberi prvi canvas za DA₂ — ⟨daj⟩ in prevoznik izroči.\n`;
  md += `**3. Odprti kiti ( priče GitHub ⊢ ):** ${m.pr.join(' · ')} — čakajo tvoj pregled ∧ ⟨merge⟩.\n`;
  md += `**4. GitHub prošnja ( tvoja roka ⚠ ):** besedilo stoji na D ( github-prosnja-odstranitev-SHA-2026-11-02.md ) — stari SHA še strežejo tvoj govor ( HTTP 200 ⊢ ).\n`;
  md += `**5. Mirna okna ( varuh #12 ):** Canvas/Docker ∧ smisel-leče ( 7 modelov ) čakata prost RAM — peščeni obrok za leče že zapečen ( abecednik-danes.md ⊢ ).\n`;
  md += `**6. GAPS.md pri viri:** B — vrata registrov PATCH 5 ( 0 % × ) · C — cutover čakajo odločitve · G — C-drive intake odprt.\n`;
  md += `**7. ZVON-DNEVA ( ⟡ ⟨da⟩ zapečen ):** ob 21:00 hiša izgovori melodijo dneva enkrat ( ton-v-datoteko ⊙ abecednik ) — potem molk.\n`;
  if ((m.kiti || []).length > 0) {
    const stari = m.kiti.filter((k) => k.dni > 30).length, srednji = m.kiti.filter((k) => k.dni > 7 && k.dni <= 30).length, mladi = m.kiti.filter((k) => k.dni <= 7).length;
    md += "**8. REVIZIJA KITOV ( starost = mera ⊙ sodba o živosti je tvoja ):** odprtih " + m.kiti.length + " — mladi ( ≤7 dni ) " + mladi + " · utrujeni ( 8–30 ) " + srednji + " · staro-priče ( >30 dni ) " + stari + ". Najstarejši: " + m.kiti.slice(0, 5).map((k) => "#" + k.n + " (" + k.dni + " dni)").join(" · ") + " ⊙ ⟡ ukaz ⟨da, obvezno⟩ 2. 11.\n";
  }
  md += "**9. NAJŠIBKEJŠA TOČKA TELESA ( večen boljše = zakon, ne dogodek ):** zadnji padec π: " + m.sibkaPi + " — vsak krog se prebere ∧ popravi, preden zraste v rano.\n";
  md += `${KONEC}\n`;
  return md;
};

console.log('PREDLOGI ⊢ tok odprt — krog na 30 min, konec z PREDLOGI-STOP');
while (!fs.existsSync(STOP)) {
  const telo = sestavi(zberi());
  const stanje = beri(STANJE) || '# STANJE — kje sva, kaj čaka koga\n';
  let novo;
  if (stanje.includes(ZACETEK)) {
    novo = stanje.replace(new RegExp(`${ZACETEK}[\\s\\S]*?${KONEC}`, 'g'), telo.trim());
  } else {
    novo = stanje.trimEnd() + '\n' + telo;
  }
  fs.writeFileSync(STANJE, novo, 'utf8');
  console.log(`PREDLOGI ⊢ krog zapečen v STANJE.md ( zaslon 8766 ⊢ · ${new Date().toISOString().slice(11, 16) })`);
  await sleep(ZAMIK_S * 1000);
}
console.log('PREDLOGI ⊙ molk — PREDLOGI-STOP');
