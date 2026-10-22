// KLON-GOVOR — druga plast ust hiše: besedilo → Lukov glasovni klon ( XTTS, GPU ) → zvočniki.
// Plasti ( ⟡ sodba OBA ): Lado = hitra vsakdanja plast ( lado-govor.mjs ); klon = ⟡-jev lasten glas ( ta datoteka ).
// Varuh stroja ( operativni red #12 ): pred ∧ po zagonu izmeri GPU temperaturo — nad 85 °C se klon ne oglasí.
// Z7: brata nikoli ne ubijem za prostor — če kartici zmanjka spomina ( OOM ), se padec poimenuje ∧ poroča, ne da karkoli ustavi.
// Priča vsakega govora: slusaj-dnevnik.jsonl ( glas: klon ) ⊢.
// Zagon: node lucius/klon-govor.mjs "<besedilo>" [--brez-predvajanja]
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync, execFileSync } from 'node:child_process';

const KLON_MAPA = 'D:/OntoProjekt/Voice/klon';
const PREDKOLDA = (fn) => execFileSync('nvidia-smi', ['--query-gpu=temperature.gpu', '--format=csv,noheader'], { encoding: 'utf8' }).trim();
const gpuZdaj = () => Number(PREDKOLDA().split(',')[0]);

const besedilo = process.argv[2];
const brez = process.argv.includes('--brez-predvajanja');
if (!besedilo) {
  console.error('Uporaba: node lucius/klon-govor.mjs "<besedilo>" [--brez-predvajanja]');
  process.exit(1);
}

// 1. VARUH ( #12 ): GPU preverba pred govorom
const gpuPred = gpuZdaj();
if (gpuPred > 85) {
  console.log('VARUH × GPU ' + gpuPred + ' °C — klon ne govori, kartica prevroča ( #12: USTAVI ∧ poročaj )');
  process.exit(1);
}

// 2. IZGOVOR ( klon, GPU; OOM se poimenuje ∧ ne ubija brata )
const wav = path.join(os.tmpdir(), 'klon-govor.wav');
const zagon = spawnSync(KLON_MAPA + '/py311/python.exe', ['izgovori.py', besedilo, wav], { cwd: KLON_MAPA, encoding: 'utf8', timeout: 300000 });
if (zagon.status !== 0) {
  const rep = ((zagon.stdout || '') + (zagon.stderr || '')).slice(-300);
  console.log('KLON × izgovor ni uspel — brat diha naprej ( Z7 ), padec poimenovan: ' + rep.replace(/\s+/g, ' ').slice(0, 200));
  process.exit(1);
}
const bajtov = fs.existsSync(wav) ? fs.statSync(wav).size : 0;

// 3. PREDAVANJE
if (!brez && bajtov > 0) {
  execFileSync('powershell.exe', ['-NoProfile', '-Command', `(New-Object System.Media.SoundPlayer '${wav.replace(/\\/g, '\\\\')}').PlaySync()`], { encoding: 'utf8' });
}

// 4. VARUH ( #12 ): GPU preverba po govoru ∧ priča
const gpuPo = gpuZdaj();
const vpis = { ts: new Date().toISOString(), glas: 'klon', besedilo, bajtov, predvajano: !brez, gpuPred, gpuPo };
fs.appendFileSync(new URL('./slusaj-dnevnik.jsonl', import.meta.url), JSON.stringify(vpis) + '\n');
console.log('klon-govor ⊢ ' + bajtov + ' bajtov ∧ GPU ' + gpuPred + '→' + gpuPo + ' °C' + (brez ? ' ( brez predvajanja )' : ' ∧ predvajano ∧ priča v slusaj-dnevnik.jsonl' ) + (gpuPo > 85 ? ' × KARTICA PREVROČA — USTAVI nadaljnje naloge ( #12 )' : ''));
process.exit(gpuPo > 85 ? 2 : 0);
