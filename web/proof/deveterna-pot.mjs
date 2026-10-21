// DEVETERNA POT — živi brskalniški proof Faze 2 (Playwright, Edge).
// Zagon (iz korena repa, API naj tece na 4173, UI na 5173):
//   node web/proof/deveterna-pot.mjs <projectRoot>
// Dokazuje acceptance bar: vseh 9 service operacij dosegljivih iz UI,
// VERIFY: PASS drži celo pot, sled inserta preživi oba arhiva.
import { chromium } from "playwright";

const projectRoot = process.argv[2];
if (!projectRoot) {
  console.error("Uporaba: node web/proof/deveterna-pot.mjs <projectRoot>");
  process.exit(1);
}

const UI = process.env.PROOF_UI_URL || "http://localhost:5173";
const KORAK = (n, opis) => console.log(`[${n}/9] ${opis}`);
const PASS = (opis) => console.log(`      ⊢ ${opis}`);

async function verifyPass(page, oznaka) {
  const vrstica = page.locator(".status-bar .status-ok");
  await vrstica.waitFor({ state: "visible", timeout: 15000 });
  const besedilo = await vrstica.textContent();
  if (besedilo !== "VERIFY: PASS") {
    throw new Error(`${oznaka}: statusna vrstica ni VERIFY: PASS, ampak: ${besedilo}`);
  }
  PASS(`${oznaka}: VERIFY: PASS`);
}

const browser = await chromium.launch({ channel: "msedge", headless: true });
const page = await browser.newPage();
page.setDefaultTimeout(20000);

try {
  await page.goto(UI, { waitUntil: "networkidle" });
  await verifyPass(page, "zacetek");

  // 1. capture (Knjiznica -> zajem)
  KORAK(1, "capture");
  await page.locator("section.pane", { has: page.locator("h2", { hasText: "Knjiznica" }) })
    .locator('input[placeholder="Naslov (neobvezno)"]').fill("Brskalniški dokaz");
  await page.locator('textarea[placeholder="Vsebina"]').fill("Telo vhodnega teksta za brskalniški dokaz devetere poti.");
  await page.getByRole("button", { name: "Zajemi" }).click();
  await page.locator(".incoming-list .incoming-row", { hasText: "Brskalniški dokaz" }).waitFor();
  await verifyPass(page, "po capture");

  // 2. start-processing
  KORAK(2, "start-processing");
  // v fixture je natanko en vir; hasText filtri odpadejo, ko naslov postane vrednost inputa
  const vrsticaVira = page.locator(".incoming-list .incoming-row").first();
  await vrsticaVira.getByRole("button", { name: "Zacni obdelavo" }).click();
  await vrsticaVira.locator(".badge", { hasText: "processing" }).waitFor();
  PASS("vir je processing");
  await verifyPass(page, "po start-processing");

  // 3. create-fragment
  KORAK(3, "create-fragment");
  await vrsticaVira.locator('textarea[placeholder="Odlomek..."]').fill("Prvi odstavek dokaznega fragmenta.");
  await vrsticaVira.locator('input[placeholder="Naslov (neobvezno)"]').fill("Dokazni fragment");
  await vrsticaVira.getByRole("button", { name: "Ustvari fragment" }).click();
  await vrsticaVira.locator(".fragment-list li", { hasText: "Dokazni fragment" }).waitFor();
  PASS("fragment je draft");
  await verifyPass(page, "po create-fragment");

  // 4. insert (Aktivna knjiga)
  KORAK(4, "insert");
  const knjiga = page.locator("section.pane", { has: page.locator("h2", { hasText: "Aktivna knjiga" }) });
  const izbira = knjiga.locator("select");
  await izbira.selectOption({ index: 1 }); // prvi draft fragment (edini)
  await knjiga.locator('input[placeholder^="ciljno poglavje"]').fill("poglavje/brskalniski-dokaz.md");
  await knjiga.getByRole("button", { name: "Vstavi" }).click();
  await page.locator(".insertion-row", { hasText: "poglavje/brskalniski-dokaz.md" }).waitFor();
  PASS("insertion viden v Vstavljene sledi");
  await verifyPass(page, "po insert");

  // 5. update-incoming (preimenuj)
  KORAK(5, "update-incoming");
  await vrsticaVira.getByRole("button", { name: "Preimenuj vir" }).click();
  await vrsticaVira.locator('input[aria-label="Nov naslov vira"]').fill("Brskalniški dokaz (preimenovan)");
  await vrsticaVira.getByRole("button", { name: "shrani" }).click();
  await page.locator(".incoming-row", { hasText: "Brskalniški dokaz (preimenovan)" }).waitFor();
  PASS("vir preimenovan");
  await verifyPass(page, "po update-incoming");

  // 6. update-fragment
  KORAK(6, "update-fragment");
  const vrsticaFragmenta = vrsticaVira.locator(".fragment-list li").first();
  await vrsticaFragmenta.getByRole("button", { name: "uredi" }).click();
  await vrsticaFragmenta.locator('textarea[aria-label="Obnovljeno besedilo odlomka"]').fill("Prvi odstavek dokaznega fragmenta. (dopolnjeno)");
  await vrsticaFragmenta.getByRole("button", { name: "Shrani obnovo" }).click();
  await vrsticaFragmenta.locator(".badge", { hasText: "inserted" }).first().waitFor(); // po insertu ni več draft
  PASS("fragment obnovljen");
  await verifyPass(page, "po update-fragment");

  // 7. update-insertion
  KORAK(7, "update-insertion");
  const vrsticaInserta = page.locator(".insertion-row", { hasText: "poglavje/brskalniski-dokaz.md" });
  await vrsticaInserta.getByRole("button", { name: "uredi" }).click();
  await vrsticaInserta.locator('input[aria-label="Pozicijska opomba"]').fill("za uvodom");
  await vrsticaInserta.getByRole("button", { name: "Shrani obnovo" }).click();
  await page.locator(".insertion-row", { hasText: "za uvodom" }).waitFor();
  PASS("insertion ima positionNote");
  await verifyPass(page, "po update-insertion");

  // 8. archive-fragment
  KORAK(8, "archive-fragment");
  await vrsticaFragmenta.getByRole("button", { name: "arhiviraj" }).click();
  await vrsticaFragmenta.locator(".badge", { hasText: "archived" }).waitFor();
  PASS("fragment arhiviran");
  await verifyPass(page, "po archive-fragment");

  // 9. archive-incoming
  KORAK(9, "archive-incoming");
  await vrsticaVira.getByRole("button", { name: "Arhiviraj vir" }).click();
  await vrsticaVira.locator(".badge", { hasText: "archived" }).waitFor();
  PASS("vir arhiviran");
  await verifyPass(page, "po archive-incoming");

  // sled inserta preživi oba arhiva (se vedno viden v UI)
  await page.locator(".insertion-row", { hasText: "poglavje/brskalniski-dokaz.md" }).waitFor();
  PASS("sled inserta preživi oba arhiva (vidna v UI)");

  // neodvisna preverba manifestov (iz brskalnika, čez isti proxy)
  const verify = await page.evaluate(async () => {
    const odziv = await fetch("/api/verify");
    return (await odziv.json()).isValid;
  });
  if (verify !== true) throw new Error("/api/verify ni isValid po deveteri poti");
  PASS("/api/verify isValid=true po deveteri poti");

  console.log("DEVETERNA POT: PASS (9/9, VERIFY: PASS celo pot, sled preživi)");
} finally {
  await browser.close();
}
