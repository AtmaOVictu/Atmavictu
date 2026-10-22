// PISK — zvočni odziv hiše: ⊢ = visok ton, × = nizek ton, ⚠ = srednji.
// Zagon: node lucius/pisk.mjs [ok|padec|dvom]
// Uporaba: po vsakem preizkusu ali padcu — hiša spregovori z zvokom.
import { execFileSync } from 'node:child_process';

const VRSTA = process.argv[2] || 'ok';

// frekvence po tvojem JEWIK sistemu ( iz Obsidiana ):
// regeneracija 13.1 Hz ni slišna — uporabimo višje harmonike za pisk
const TONI = {
  ok:     { f: 880,  tr: 0.09 },  // ⊢ visok, kratek — uspeh
  dvom:   { f: 660,  tr: 0.14 },  // ⚠ srednji, daljši — dvom
  padec:  { f: 220,  tr: 0.25 },  // × nizek, dolg — padec
};

const ton = TONI[VRSTA];
if (!ton) {
  console.error('Uporaba: node lucius/pisk.mjs [ok|padec|dvom]');
  process.exit(1);
}

// PowerShell: [console]::beep( frekvenca, trajanje_ms )
const ms = Math.round(ton.tr * 1000);
execFileSync('powershell.exe', ['-NoProfile', '-Command',
  `[console]::beep(${ton.f}, ${ms})`]);
console.log(`PISK ${VRSTA}: ${ton.f} Hz ⊢`);
