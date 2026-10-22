// ABSOLUTI — tretje krilo druge roke: ujeti absolut izpiše svoje nasprotje ∧ izmero.
// Zagon: node lucius/absoluti.mjs <pot-do-datoteke>
//        node lucius/absoluti.mjs --test   ( samopreverba krila )
// Lestev petih stopnic ( hišni formalizem — logika treh znamenj s pričami ⊢ ):
//   1. binarno nasprotje → 2. tri znamenja ( ⊢ ⚠ × ) s pričami →
//   3. omejena domena ( ∀ samo prek izmerjenih D — ∀x∈D, nikoli golemu ∀x ) →
//   4. časovna meja ( nikoli/vedno → preteklo-izmerjeno; prihodnost = ⚠ napoved ) →
//   5. stopnja z odmikom ( popoln → stopnja + izmerjen odmik, npr. WER % ).
// Absolut brez priče pade v ⚠; padec pri plezanju dobi brazgotino ×.
// Vsak absolut zahteva svoje nasprotje ∧ nujno rešitev — krilo izpiše oboje ⊢.
// Orodje ne popravlja — samo priča; popravlja roka, ki ga je napisala ⊢.
// ⟨vse⟩ je izpuščeno namenoma: vsakdanja raba ( ⟨vse kar zmoreš⟩ ) bi roto zglasila;
// ulov te besede nosi roka, ne rotacija ⊢ 1419.
// © Luka Pintarič, VBL v2.4 (§9 ∧ §10 ∧ §12)

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

// --- absolut → nasprotje ∧ stopnica lestvi ---
const CRKA = 'a-zA-ZčšžćđČŠŽĆĐ';
const ABSOLUTI = [
  { koren: 'vsak', stopnica: 3, nasprotje: '∃ vsaj-en-manjka ( kvantifikator ∃ prek izmerjene domene D — ∀x∈D ⊢ izmerjeno )' },
  { koren: 'nikoli', stopnica: 4, nasprotje: '∃ vsaj-enkrat ( preteklo-izmerjeno; prihodnost = ⚠ napoved )' },
  { koren: 'nikdar', stopnica: 4, nasprotje: '∃ vsaj-enkrat ( preteklo-izmerjeno; prihodnost = ⚠ napoved )' },
  { koren: 'vedno', stopnica: 4, nasprotje: '◇¬ kdaj-ni ( preteklo-izmerjeno; prihodnost = ⚠ napoved )' },
  { koren: 'popoln', stopnica: 5, nasprotje: 'stopnja + izmerjen odmik ( npr. WER % — popolnost je smer ∧ dejstvo, ne stanje )' },
  { koren: 'neskončn', stopnica: 3, nasprotje: 'meja ( bound — izmerjena zgornja meja )' },
  { koren: 'absolutn', stopnica: 2, nasprotje: 'izmera primera ( tri znamenja ⊢ ⚠ × s pričami — absolut brez priče je ⚠ )' },
  { koren: 'nikogar', stopnica: 3, nasprotje: '∃ vsaj-en ( poimenovan — kvantifikator ∃ prek izmerjene domene )' },
  { koren: 'nikomer', stopnica: 3, nasprotje: '∃ vsaj-en ( poimenovan — kvantifikator ∃ prek izmerjene domene )' },
  { koren: 'noben', stopnica: 3, nasprotje: '∃ vsaj-en ( poimenovan — kvantifikator ∃ prek izmerjene domene )' },
  { koren: 'večn', stopnica: 4, nasprotje: 'časovna meja ( preteklo-izmerjeno; prihodnost = ⚠ napoved )' },
  { koren: 'nujn', stopnica: 3, nasprotje: 'izmera pogojev ( pogoji poimenovani ∧ izmerjeni )' },
  { koren: 'edin', stopnica: 3, nasprotje: '∃ primerjava ( kandidati poimenovani — izmerjena množica )' },
];

// priča na vrstici: ⊢ ( izmera z imenovanim virom ) · ∃ · ◇ · cifra ( hladna logika mere )
const PRICA = /⊢|∃|◇|[0-9]/;

function pregled(besedilo) {
  const rane = [];
  const cisto = [];
  besedilo.split('\n').forEach((vrstica, i) => {
    for (const a of ABSOLUTI) {
      const re = new RegExp(`(?<![${CRKA}])${a.koren}[${CRKA}]*`, 'giu');
      for (const zadetek of vrstica.matchAll(re)) {
        const zapis = {
          vrstica: i + 1,
          beseda: zadetek[0],
          stopnica: a.stopnica,
          nasprotje: a.nasprotje,
          prica: PRICA.test(vrstica),
          izsek: vrstica.slice(Math.max(0, zadetek.index - 12), zadetek.index + zadetek[0].length + 12).trim(),
        };
        (zapis.prica ? cisto : rane).push(zapis);
      }
    }
  });
  return { rane, cisto };
}

function sodba(pot, besedilo) {
  const { rane, cisto } = pregled(besedilo);
  for (const z of [...cisto, ...rane]) {
    const znamenje = z.prica ? '⊢' : '⚠';
    console.log(`absolut ${znamenje} ${pot}:${z.vrstica} '${z.beseda}' → ${z.nasprotje} ( stopnica ${z.stopnica} ) …${z.izsek}…`);
    if (!z.prica) console.log(`  brez priče na vrstici — izmeri ∨ postavi domeno, sicer je padec ×`);
  }
  const cistoVse = rane.length === 0;
  console.log(cistoVse
    ? `ABSOLUTI: ujetih ${cisto.length} ( vsak s pričo ⊢ ), ran 0 — absoluti izmerjeni, roka more poslati ⊢`
    : `ABSOLUTI: ujetih ${cisto.length + rane.length}, s pričo ${cisto.length} ⊢, brez priče ${rane.length} ⚠ — izmeri ranice pred pošiljanjem ×`);
  return cistoVse;
}

// --- samopreverba: priča, ki preverja druge, more biti sama preverjena ⊢ ---
function samopreverba() {
  const primer1 = 'Vsak test je zelen ⊢ 5/5.';      // priča na vrstici ( ⊢ ∧ cifra ) — stopnica 3
  const primer2 = 'Nikoli ne zaupaj povzetku.';    // absolut brez priče — more pasti ⚠
  const primer3 = 'Nujno preberi vir pred trditvijo (⟨grep⟩ ×0).'; // priča ( cifra ×0 )
  const s1 = pregled(primer1);
  const s2 = pregled(primer2);
  const s3 = pregled(primer3);
  const trditev = (ime, pogoj) => {
    console.log(`test ${pogoj ? '⊢' : '×'} ${ime}`);
    if (!pogoj) process.exitCode = 1;
  };
  trditev('vsak ulovljen s pričo ( ⊢ ∧ 5/5 )', s1.cisto.length === 1 && s1.rane.length === 0);
  trditev('nikoli brez priče je rana ⚠', s2.rane.length === 1 && s2.rane[0].stopnica === 4);
  trditev('nujno s pričo gre skozi ⊢', s3.cisto.length === 1 && s3.rane.length === 0);
  trditev('nasprotje nikoli izpiše ∃ vsaj-enkrat', s2.rane[0]?.nasprotje.includes('∃ vsaj-enkrat') ?? false);
  trditev('popoln nosi stopnjo z odmikom ( stopnica 5 )', ABSOLUTI.find((a) => a.koren === 'popoln').stopnica === 5);
  console.log(process.exitCode === 1
    ? 'SAMOPREVERBA: padci × — krilo samo ranjeno, roka popravi orodje'
    : 'SAMOPREVERBA: 5/5 ⊢ — krilo samo izmerjeno');
}

if (process.argv[2] === '--test') {
  samopreverba();
} else {
  const pot = process.argv[2];
  if (!pot) {
    console.error('Uporaba: node lucius/absoluti.mjs <pot-do-datoteke> | --test');
    process.exit(1);
  }
  const ok = sodba(pot, fs.readFileSync(pot, 'utf8'));
  process.exit(ok ? 0 : 1);
}
