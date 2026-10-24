// LADO-GOVOR — usta hiše: besedilo → Lado ( OneCore sl-SI, zastonj ∧ offline ) → zvočniki.
// Zakon ( Z4 ∧ ⟡ sodba OBA ): Lado je hitra plast ust; klon ( ⟡-jev glas ) je druga plast —
// nobenega ubijanja, oba glasova živita ( Z7 ). Diakritične črke čistijo krog ⊢ ( 13.0 % WER ).
// Zagon: node lucius/lado-govor.mjs "<besedilo>" [--brez-predvajanja]
// Priča vsakega govora: slusaj-dnevnik.jsonl ( glas, besedilo, bajti, čas ) ⊢.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const besedilo = process.argv[2];
const brez = process.argv.includes('--brez-predvajanja');
if (!besedilo) {
  console.error('Uporaba: node lucius/lado-govor.mjs "<besedilo>" [--brez-predvajanja]');
  process.exit(1);
}

const wav = path.join(os.tmpdir(), 'lado-govor.wav');
const ps1 = path.join(os.tmpdir(), 'lado-govor.ps1');
const skripta = `
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation\`1' })[0]
function Await($WinRtTask, $ResultType) {
  $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
  $netTask = $asTask.Invoke($null, @($WinRtTask))
  $netTask.Wait(-1) | Out-Null
  $netTask.Result
}
$null = [Windows.Media.SpeechSynthesis.SpeechSynthesizer,Windows.Media.SpeechSynthesis,ContentType=WindowsRuntime]
$synth = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
$stream = Await ($synth.SynthesizeTextToStreamAsync([System.IO.File]::ReadAllText('${path.join(os.tmpdir(), 'lado-besedilo.txt').replace(/\\/g, '\\\\')}'))) ([Windows.Media.SpeechSynthesis.SpeechSynthesisStream])
$netStream = [System.IO.WindowsRuntimeStreamExtensions]::AsStream($stream)
$ms = New-Object System.IO.MemoryStream
$netStream.CopyTo($ms)
[System.IO.File]::WriteAllBytes('${wav.replace(/\\/g, '\\\\')}', $ms.ToArray())
Write-Output ('bajtov: ' + $ms.Length)
`;
fs.writeFileSync(path.join(os.tmpdir(), 'lado-besedilo.txt'), besedilo, 'utf8');
fs.writeFileSync(ps1, skripta, 'utf8');

const izhod = execFileSync('powershell.exe', ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ps1], { encoding: 'utf8' });
const bajtov = Number((izhod.match(/bajtov: (\d+)/) ?? [0, 0])[1]);

if (!brez && bajtov > 0) {
  execFileSync('powershell.exe', ['-NoProfile', '-Command', `(New-Object System.Media.SoundPlayer '${wav.replace(/\\/g, '\\\\')}').PlaySync()`], { encoding: 'utf8' });
}

const vpis = { ts: new Date().toISOString(), glas: 'lado', besedilo, bajtov, predvajano: !brez };
fs.appendFileSync(new URL('./slusaj-dnevnik.jsonl', import.meta.url), JSON.stringify(vpis) + '\n');
console.log('lado-govor ⊢ ' + bajtov + ' bajtov' + (brez ? ' ( brez predvajanja )' : ' ∧ predvajano ∧ priča v slusaj-dnevnik.jsonl' ));
