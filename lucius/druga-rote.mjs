// DRUGA-ROTE — poizkus roke nad lastnim izpisom: čistina + preverba v enem pregonu.
// Zagon: node lucius/druga-rote.mjs <pot-do-datoteke>
// Pomen ( REGISTER-PADCEV vnos 6 ): pravilo #2 velja brez izjeme tudi za
// daljše izpise v pogovoru — vsak izpis, preden zapusti roko, gre skozi to.
// Orodje ne popravlja — samo priča; popravlja roka, ki ga je napisala ⊢.
import fs from 'node:fs';

const pot = process.argv[2];
if (!pot) {
  console.error('Uporaba: node lucius/druga-rote.mjs <pot-do-datoteke>');
  process.exit(1);
}
const besedilo = fs.readFileSync(pot, 'utf8');

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

// 2) PREVERBA — LanguageTool ( sl ); v javni strežnik ne dajamo skrivnosti ⊢
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

let ran = 0;
for (const ujela of data.matches ?? []) {
  const { vrstica, stolpec } = odstotek(ujela.offset);
  const popravek = ujela.replacements?.[0]?.value ?? '(brez predloga)';
  console.log(`preverba × ${pot}:${vrstica}:${stolpec} ${ujela.shortMessage || ujela.message} → ${popravek}`);
  ran += 1;
}

const cisto = cirilice === 0 && ran === 0;
console.log(cisto
  ? `DRUGA-ROTE: cistina 0 + preverba 0 — izpis cist, roka more poslati ⊢`
  : `DRUGA-ROTE: cirilice ${cirilice} + slovnicnih zadetkov ${ran} — preberi vsakega kakor tujec, nekatere so lažni ( imena, domaca besedila ), ostale popravi ×`);
process.exit(cisto ? 0 : 1);
