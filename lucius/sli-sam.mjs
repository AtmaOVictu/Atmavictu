// SLI-SAM — "slišim sebe": besedilo → glas (TTS, WAV) → Whisper posluša → izpis,
// kaj je glas DEJANSKO povedal. Edina pot, da stroj "sliši" samega sebe.
// Zagon: node lucius/sli-sam.mjs "besedilo, ki ga izgovarjam"
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const BESEDILO = process.argv[2];
if (!BESEDILO) {
  console.error('Uporaba: node lucius/sli-sam.mjs "besedilo"');
  process.exit(1);
}

const WAV = path.join(os.tmpdir(), `sli-sam-${Date.now()}.wav`);
const ps1 = path.join(os.tmpdir(), `sli-sam-${Date.now()}.ps1`);
fs.writeFileSync(ps1, [
  'param($wavPot, $govor)',
  'Add-Type -AssemblyName System.Speech',
  '$s = New-Object System.Speech.Synthesis.SpeechSynthesizer',
  '$s.SetOutputToWaveFile($wavPot)',
  '$s.Speak($govor)',
  '$s.Dispose()',
].join('\r\n'), 'utf8');

execFileSync('powershell.exe', ['-NoProfile', '-ExecutionPolicy', 'Bypass',
  '-File', ps1, '-wavPot', WAV, '-govor', BESEDILO]);
fs.unlinkSync(ps1);

const zvok = fs.readFileSync(WAV);
const odziv = await fetch('http://127.0.0.1:8767/', {
  method: 'POST', body: zvok, headers: { 'content-type': 'application/octet-stream' },
});
const odg = await odziv.json();
fs.unlinkSync(WAV);

console.log('ZAPISOVAL SEM:  ' + BESEDILO);
if (odg.ok) {
  console.log('GLAS JE REKEL:  ' + odg.besedilo);
  const norm = (s) => s.toLowerCase().replace(/[^\p{L}\p{N}\sčšžćđ]/gu, '').split(/\s+/).filter(Boolean);
  const a = norm(BESEDILO), b = norm(odg.besedilo);
  const enake = a.filter((w, i) => b[i] === w).length;
  const odstotek = Math.round(100 * enake / Math.max(1, a.length));
  console.log(`SLI-SAM: ${odstotek}% besed se je vrnilo ${odstotek >= 85 ? '⊢ slišim sebe (skoraj)' : '⚠ glas je izkrivil moje besede'}`);
} else {
  console.log('NAPAKA poslušanja: ' + (odg.napaka || 'neznana'));
  process.exit(1);
}
