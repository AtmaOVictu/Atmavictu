// DRUGA-ROTE — poizkus roke nad lastnim izpisom: čistina + preverba + leksikon v enem pregonu.
// Zagon: node lucius/druga-rote.mjs <pot-do-datoteke>
//        node lucius/druga-rote.mjs --slovar <beseda>   ( izpis gesla iz Lukovega slovarja )
// Pomen ( REGISTER-PADCEV vnos 6 ): pravilo #2 velja brez izjeme tudi za
// daljše izpise v pogovoru — vsak izpis, preden zapusti roko, gre skozi to.
// Vnos 7 ( POŠČENO-TRETJIČ ): orodje bere hišni leksikon:
//   - znane-besede.txt      → hišne besede, ki niso rane ( lažni zadetki LanguageTool )
//   - prepovedane-besede.txt → besede zapečene kot padci — ulovljene VEDRA ×
// Lukov slovar ( D:/Worth/slovenian_dictionary, 2775 gesel ): ko preverba označi
// besedo, orodje pokaže NJENO standardno pomenu in Lukovo rabo ⊢ — roka ne sodi
// po tujem slovarju besede, ki ima doma svoj pomen.
// Orodje ne popravlja — samo priča; popravlja roka, ki ga je napisala ⊢.
import fs from 'node:fs';
import path from 'node:path';

const SLOVAR_MAPA = 'D:/Worth/slovenian_dictionary';

// --- Lukov slovar: zgradi kazalo gesel ( ### beseda ) ---
const kazalo = new Map(); // beseda → { datoteka, vrstica }
const datotekeSlovarja = [];
{
  try {
    for (const ime of fs.readdirSync(SLOVAR_MAPA).filter((f) => /^dictionary_batch_\d+\.md$/.test(f)).sort()) {
      const polna = path.join(SLOVAR_MAPA, ime);
      const vrstice = fs.readFileSync(polna, 'utf8').split('\n');
      datotekeSlovarja.push(vrstice);
      vrstice.forEach((v, i) => {
        const cista = v.replace(/\r$/, '');
        if (!cista.startsWith('### ')) return;
        const b = cista.slice(4).trim();
        if (b) kazalo.set(b.toLowerCase(), { datoteka: ime, vrstica: i, vrstice });
      });
    }
  } catch { /* slovar nedosegljiv — orodje dela naprej, označi ⚠ */ }
}
function geslo(beseda) {
  const z = kazalo.get(beseda.trim().toLowerCase());
  if (!z) return null;
  let standard = null;
  let raba = null;
  for (let i = z.vrstica + 1; i < z.vrstice.length; i++) {
    const v = z.vrstice[i];
    if (v.startsWith('### ')) break;
    if (!standard && v.startsWith('**Standard meaning:**')) standard = v.replace('**Standard meaning:**', '').trim();
    if (!raba && v.startsWith('**Your usage:**')) raba = v.replace('**Your usage:**', '').trim();
    if (standard && raba) break;
  }
  return { datoteka: z.datoteka, standard, raba };
}

// --- Način --slovar: izpiši geslo in končaj ---
if (process.argv[2] === '--slovar') {
  const b = process.argv[3];
  if (!b) { console.error('Uporaba: node lucius/druga-rote.mjs --slovar <beseda>'); process.exit(1); }
  if (kazalo.size === 0) { console.error(`⚠ slovar nedosegljiv ( ${SLOVAR_MAPA} )`); process.exit(1); }
  const g = geslo(b);
  if (!g) { console.log(`SLOVAR: gesla '${b}' ni ( kazalo ima ${kazalo.size} gesel ) ⚠`); process.exit(1); }
  console.log(`SLOVAR ⊢ '${b}' ( ${g.datoteka} )`);
  if (g.standard) console.log(`  pomen: ${g.standard}`);
  if (g.raba) console.log(`  tvoja raba: ${g.raba}`);
  process.exit(0);
}

const pot = process.argv[2];
if (!pot) {
  console.error('Uporaba: node lucius/druga-rote.mjs <pot-do-datoteke> | --slovar <beseda>');
  process.exit(1);
}
const besedilo = fs.readFileSync(pot, 'utf8');
const tu = (ime) => {
  try {
    return fs.readFileSync(new URL('./' + ime, import.meta.url), 'utf8');
  } catch { return ''; }
};
const seznam = (ime) => tu(ime).split('\n').map((v) => v.trim()).filter((v) => v && !v.startsWith('#')).map((v) => v.toLowerCase());
const ZNANE = new Set(seznam('znane-besede.txt'));
const PREPOVEDANE = seznam('prepovedane-besede.txt');
if (ZNANE.size === 0 || PREPOVEDANE.length === 0) {
  console.error('× leksikon manjka ( znane-besede.txt / prepovedane-besede.txt ) — brez njega orodje ne pusti roke ⊢');
  process.exit(1);
}

// 1) CISTINA — zrcalni dvojčki ( enaka logika kakor cistina.mjs )
const ZRCALA = /[\u0370-\u03FF\u0400-\u04FF]/g;
let cirilice = 0;
besedilo.split('\n').forEach((vrstica, i) => {
  for (const zadetek of vrstica.matchAll(ZRCALA)) {
    const k = zadetek[0].charCodeAt(0);
    const ime = k < 0x400 ? 'grscina' : 'cirilica';
    console.log(`cistina × ${pot}:${i + 1} '${zadetek[0]}' [${ime}] → …${vrstica.slice(Math.max(0, zadetek.index - 12), zadetek.index + 12).trim()}…`);
    cirilice += 1;
  }
});

// 2) PREPOVEDANE-BESEDE — padci, zapečeni v registru; ulovljene vedra ×
let prepovedane = 0;
const besede = besedilo.toLowerCase().match(/[a-zA-ZčšžćđČŠŽĆĐ]+/g) ?? [];
for (const b of new Set(besede)) {
  if (PREPOVEDANE.includes(b)) {
    console.log(`prepovedano × '${b}' — beseda zapečena kot padec ( REGISTER-PADCEV ); roka jo popravi pred pošiljanjem`);
    prepovedane += 1;
  }
}

// 3) PREVERBA — LanguageTool ( sl ); v javni strežnik ne dajamo skrivnosti ⊢
const odziv = await fetch('https://api.languagetool.org/v2/check', {
  method: 'POST',
  headers: { 'content-type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({ text: besedilo, language: 'sl' }),
});
if (!odziv.ok) {
  console.error(`preverba × HTTP ${odziv.status} — LanguageTool nedosegljiv`);
  process.exit(1);
}
const data = await odziv.json();

const vrstice = besedilo.split('\n');
const odstotek = (zamik) => {
  let stevec = 0;
  for (let i = 0; i < vrstice.length; i++) {
    if (zamik < stevec + vrstice[i].length + 1) return { vrstica: i + 1, stolpec: zamik - stevec + 1 };
    stevec += vrstice[i].length + 1;
  }
  return { vrstica: '?', stolpec: '?' };
};
const vsebujeZnano = (izsek) => {
  const mali = izsek.toLowerCase();
  for (const z of ZNANE) if (mali.includes(z)) return true;
  return false;
};

let ran = 0;
let znanih = 0;
let slovarskih = 0;
for (const ujela of data.matches ?? []) {
  const { vrstica, stolpec } = odstotek(ujela.offset);
  const popravek = ujela.replacements?.[0]?.value ?? '(brez predloga)';
  const izsek = besedilo.slice(ujela.offset, ujela.offset + (ujela.length ?? 0));
  if (vsebujeZnano(izsek)) {
    znanih += 1; // hišna beseda — lažni zadetek ⊢
    continue;
  }
  if ((ujela.shortMessage || ujela.message || '').startsWith('Številka v besedilu')) {
    znanih += 1; // hišni zapis števil ⊢
    continue;
  }
  console.log(`preverba × ${pot}:${vrstica}:${stolpec} ${ujela.shortMessage || ujela.message} '${izsek.trim()}' → ${popravek}`);
  const g = geslo(izsek.trim());
  if (g) {
    slovarskih += 1;
    if (g.standard) console.log(`  slovar ⊢ pomen: ${g.standard.slice(0, 200)}`);
    if (g.raba) console.log(`  slovar ⊢ tvoja raba: ${g.raba.slice(0, 200)}`);
  }
  ran += 1;
}

const cisto = cirilice === 0 && ran === 0 && prepovedane === 0;
console.log(cisto
  ? `DRUGA-ROTE: cistina 0 + prepovedane 0 + preverba 0 ( ${znanih} hišnih besed ⊢, ${slovarskih} gesel iz Lukovega slovarja ⊢ ) — izpis čist, roka more poslati ⊢`
  : `DRUGA-ROTE: cirilice ${cirilice} + prepovedane ${prepovedane} + slovnicnih zadetkov ${ran} ( ${znanih} hišnih besed ⊢, ${slovarskih} gesel iz Lukovega slovarja ⊢ ) — preberi vsakega kakor tujec, nekatere so lažni, ostale popravi ×`);
process.exit(cisto ? 0 : 1);
