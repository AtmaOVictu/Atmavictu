// ZVOČNA-ABECEDA — vsak simbol hiše ima svoj ton; hiša "govori" v čistih frekvencah.
// Zagon: node lucius/zvocna-abeceda.mjs [simbol]  ali  brez argumenta = celo abecedo
// Namen: da hiša sama sliši svoje stanje — brez besed, samo tonov ⊢
import { execFileSync } from 'node:child_process';

const ABECEDA = {
  // tehtnica ( licenca )
  '⊢':   { f: 880,  tr: 0.10 },  // dokaz — visok, jasen
  '⚠':   { f: 660,  tr: 0.14 },  // dvom — srednji, daljši
  '×':   { f: 220,  tr: 0.25 },  // padec — nizek, dolg
  // JEWIK operatorji ( tvoji iz Obsidiana )
  '⊘':   { f: 440,  tr: 0.08 },  // rez — srednji, kratek
  '∮':   { f: 523,  tr: 0.12 },  // kroženje — raste
  '∆':   { f: 587,  tr: 0.10 },  // gibanje
  '∴':   { f: 784,  tr: 0.15 },  // resnica
  '⊥':   { f: 196,  tr: 0.20 },  // vertikala — najnižji
  '⟡':   { f: 988,  tr: 0.18 },  // razpoka — najvišji, najdaljši
  // stanja hiše
  'mir':     { f: 392,  tr: 0.30 },  // mirovanje — dolg, mehak
  'budni':   { f: 1046, tr: 0.10 },  // prisotnost — najvišji, kratek
  'voda':    { f: 261,  tr: 0.40 },  // teža — zelo dolg, zelo nizek
  'svetloba':{ f: 1318, tr: 0.20 },  // upanje — najvišji harmonik
};

const simbol = process.argv[2];
const ms = (v) => Math.round(v * 1000);

if (simbol && ABECEDA[simbol]) {
  const t = ABECEDA[simbol];
  execFileSync('powershell.exe', ['-NoProfile', '-Command', `[console]::beep(${t.f}, ${ms(t.tr)})`]);
  console.log(`${simbol}: ${t.f} Hz ⊢`);
} else if (!simbol) {
  // cela abeceda — vrstni red: tehtnica, operatorji, stanja
  const vrstni = ['⊢','⚠','×','⊘','∮','∆','∴','⊥','⟡','mir','budni','voda','svetloba'];
  for (const s of vrstni) {
    const t = ABECEDA[s];
    execFileSync('powershell.exe', ['-NoProfile', '-Command', `[console]::beep(${t.f}, ${ms(t.tr)})`]);
    console.log(`${s}: ${t.f} Hz`);
    // premor med toni ( brez ukaza — PowerShell sam počaka )
  }
  console.log('ZVOČNA ABECEDA ⊢ — vsak simbol je zapel');
} else {
  console.log('Ne poznam tega simbola. Poznam: ' + Object.keys(ABECEDA).join(' '));
}
