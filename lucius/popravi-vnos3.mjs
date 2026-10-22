// popravi-vnos3.mjs — enkraten popravek: neveljaven ubežnik v JSON vrstici 3 REGISTER-PADCEV
import fs from 'node:fs';
const vrstice = fs.readFileSync('REGISTER-PADCEV.jsonl', 'utf8').split('\n').filter((l) => l.trim());
let l3 = vrstice[2];
// rana: D:\AI — en sam backslash je v JSON neveljaven ubežnik; pravilno je D:\\AI
const pred = l3.includes('D:') ? l3.slice(l3.indexOf('D:'), l3.indexOf('D:') + 12) : '(ni)';
l3 = l3.replaceAll('D:\\AI', 'D:\\\\AI');
try {
  JSON.parse(l3);
  console.log('pred popravkom pri D: ' + JSON.stringify(pred));
  vrstice[2] = l3;
  fs.writeFileSync('REGISTER-PADCEV.jsonl', vrstice.join('\n') + '\n');
  const vse = vrstice.map((l) => JSON.parse(l));
  const brez = vse.filter((x) => !x.cure || !String(x.cure).trim()).length;
  console.log('register čitljiv ⊢: ' + vse.length + ' vnosov ∧ brez zdravila: ' + brez);
  console.log('vnos 3: ' + vse[2].padec + ' — ' + vse[2].cure.slice(0, 60));
} catch (e) {
  console.log('SE PADA: ' + e.message.slice(0, 60));
  process.exit(1);
}
