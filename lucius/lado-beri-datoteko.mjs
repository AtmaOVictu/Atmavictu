// LADO-BERI-DATOTEKO — hiša prebere kateri koli dokument naglas ( Lado, OneCore sl-SI, zastonj ∧ offline ).
// Pot, ki jo rešuje: dokument → glas ( ⟡ bere z ušesi, hiša nosi usta ) — razširitev lado-govor.mjs,
// kjer je besedilo vhodni argument; tu gre celo datoteko skozi isto sintezo ∧ isti dnevnik ⊢ Z4.
// Zagon: node lucius/lado-beri-datoteko.mjs "<pot-do-datoteke>" [--brez-predvajanja]
// Priča vsake berbe: slusaj-dnevnik.jsonl ⊢.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const vhod = process.argv[2];
const brez = process.argv.includes('--brez-predvajanja');
if (!vhod || !fs.existsSync(vhod)) {
  console.error('Uporaba: node lucius/lado-beri-datoteko.mjs "<pot-do-datoteke>" [--brez-predvajanja]');
  process.exit(1);
}
const besedilo = fs.readFileSync(vhod, 'utf8');

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

const vpis = { ts: new Date().toISOString(), glas: 'lado-berba', besedilo: '[datoteka] ' + vhod + ' (' + bajtov + ' B zvoka)', bajtov, predvajano: !brez };
fs.appendFileSync(new URL('./slusaj-dnevnik.jsonl', import.meta.url), JSON.stringify(vpis) + '\n');
console.log('lado-beri-datoteko ⊢ ' + bajtov + ' bajtov zvoka' + (brez ? ' ( brez predvajanja )' : ' ∧ predvajano ∧ priča v slusaj-dnevnik.jsonl' ));
