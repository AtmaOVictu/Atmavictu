// PREVERI-RENDER — strojna izmera brskalniškega rendera localhost vrat (Playwright iz web/, vrata nedotaknjena).
// Zagon: node lucius/preveri-render-8080.mjs  (playwright.resolve iz web/node_modules)
import { createRequire } from 'module';
const require = createRequire('C:/Users/Luka/Documents/Arhiv/Git/Atmavictu/web/package.json');
const { chromium } = require('playwright');

const VRTA = process.argv[2] ?? 'http://localhost:8080/';
const br = await chromium.launch({ channel: 'msedge' });  // sistemski Edge — ⟨ne⟩ prenos ms-playwright binark ⊙
const page = await br.newPage();
await page.goto(VRTA, { waitUntil: 'networkidle', timeout: 30000 });
const naslov = await page.title();
const telo = (await page.innerText('body')).trim();
const slika = 'C:/Users/Luka/AppData/Local/Temp/render-vrat.png';
await page.screenshot({ path: slika, fullPage: true });
console.log(`NASLOV: ${naslov}`);
console.log(`BESEDILO: ${telo.length} zn`);
console.log(`PRVIH 240: ${telo.slice(0, 240).replace(/\n+/g, ' ⏎ ')}`);
console.log(`SLIKA: ${slika}`);
await br.close();
