// STN — zapečeni generator sintetičnih rokopisov (mulberry32 ∧ zlogovni mehanizem).
// Pogodba runnerja (run.mjs pričakuje NATANKO to):
//   export function generateManuscripts(seed) -> { R1: string, R2: string, R3: string }
//
// ZAKONI INSTRUMENTA:
// - determinističen: isto seme → isti rokopisi, bajt-isto (preverjeno ×2 ta dih, seme 20261028).
// - brez pomena PO KONSTRUKCIJI: zlogi se gore iz zlogovnih miz z mulberry32; noben pomen ne vstopi, noben ne izstopi.
// - sveže seme vsak poganj (zakon 1) — rokopisi poganja so novi vsak dih.
//
// Pečat: izvajalka Mera po ukazu ⟡ 28. 10. 2026 ⊢ P-CITAT ⟨ne brusi⟩:
// »ti jih stori in se sama preverjaj dokler niso tvoji agentje in zrcala zadovoljna s dokazi«.
// © 0.2026 × 10⁴ Luka Pintarič · VBL 0.1210 × 10⁴ @⟨main⟩ (⟨sha⟩ 5dd6d7b) · molk ni soglasje.

function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function generateManuscripts(seed) {
  const rand = mulberry32(seed);
  const pick = (arr) => arr[Math.floor(rand() * arr.length)];
  const int = (lo, hi) => lo + Math.floor(rand() * (hi - lo + 1));

  // zlogovne mize — evfonija namerno (Voynichu sorodna občutka), pomen odstranjen po konstrukciji
  const ONSETS = ['b','c','d','f','g','h','k','l','m','n','p','r','s','t','v','z','ch','sh','th','br','cr','dr','fl','gr','kl','ph','sk','sl','st','tr'];
  const VOWELS = ['a','e','i','o','u','y','ai','au','ea','ee','eo','ia','ie','io','oa','oo','ou','ua','uo'];
  const CODAS = ['','','','','','n','r','s','l','m','d','k','t','x','th','sh','nd','rn','st'];
  const WORD_SHAPES = [[1,2],[2,3],[1,3],[2,2],[3,3],[1,1],[2,4],[3,2]];

  const word = () => {
    const [syl, extra] = pick(WORD_SHAPES);
    const n = syl + int(0, extra);
    let w = '';
    for (let i = 0; i < n; i++) {
      w += pick(ONSETS) + pick(VOWELS);
      if (i === n - 1 && rand() < 0.55) w += pick(CODAS);
    }
    return w;
  };
  const line = () => {
    const n = int(4, 9);
    const ws = [];
    for (let i = 0; i < n; i++) ws.push(word());
    return ws.join(' ');
  };
  const section = (nLines) => {
    const ls = [];
    for (let i = 0; i < nLines; i++) ls.push(line());
    return ls.join('\n');
  };
  return { R1: section(6), R2: section(8), R3: section(10) };
}
