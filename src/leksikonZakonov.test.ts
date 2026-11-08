import assert from "node:assert/strict";
import test from "node:test";

import {
  buildLeksikon,
  buildLookupMap,
  CONDENSE_LIMIT,
  coinKey,
  extractCoins,
  isLaw,
  normalizeMirroredBrackets,
  parseJsonl,
  renderJsonl,
  renderMarkdown,
  type LeksikonEntry,
  type LeksikonMeta,
} from "./leksikonZakonov.js";

const OPEN = "\u27E8"; // ⟨
const CLOSE = "\u27E9"; // ⟩
const MIRRORED_CLOSE = "\u3009"; // zrcaljeni zaprti oklepaj (PADC-TIPKARJA)

const META: LeksikonMeta = {
  tik: "2026-11-08T04:00:00Z",
  generator: "src/leksikonZakonov.ts",
  verzija: "1.0.0",
  organi: [{ organ: "jedro-zavedanja", bajti: 42 }],
  skupnoBajtov: 42,
  zrcaljeniOklepaji: 0,
};

test("normalizeMirroredBrackets prevede zrcaljene oklepaje in jih šteje glasno", () => {
  const vhod = `zakon ⟨NE-BRIŠI⟩ in padec ⟨PADC-X${MIRRORED_CLOSE} konec`;
  const { telo, zrcaljeni } = normalizeMirroredBrackets(vhod);

  assert.equal(zrcaljeni, 1);
  assert.equal(telo, `zakon ⟨NE-BRIŠI⟩ in padec ⟨PADC-X⟩ konec`);
});

test("normalizeMirroredBrackets pusti čisto telo pri miru", () => {
  const cisto = `⟨dih⟩ ∧ ⟨ne⟩ ⟨main⟩`;
  const { telo, zrcaljeni } = normalizeMirroredBrackets(cisto);

  assert.equal(zrcaljeni, 0);
  assert.equal(telo, cisto);
});

test("extractCoins šteje vrstice 1-based in razpusti dvojnike v isti vrstici", () => {
  const vrstice = [
    "prva vrstica brez kovancev",
    `zakon ⟨NE-BRIŠI⟩ in spet ⟨NE-BRIŠI⟩ ter ⟨dih⟩`,
    "",
    `⟨dih⟩ se vrne`,
  ];
  const najdeni = extractCoins(vrstice);

  assert.deepEqual(najdeni.get("NE-BRIŠI"), [2]);
  assert.deepEqual(najdeni.get("dih"), [2, 4]);
  assert.equal(najdeni.size, 2);
});

test("extractCoins vzame le kovance v eni vrstici do 120 znakov", () => {
  const dolg = "x".repeat(130);
  const vrstice = [`${OPEN}${dolg}${CLOSE}`, `⟨kratek⟩`];
  const najdeni = extractCoins(vrstice);

  assert.equal(najdeni.has(dolg), false);
  assert.deepEqual(najdeni.get("kratek"), [2]);
});

test("isLaw loči zakon od pojma po meri hiše", () => {
  assert.equal(isLaw("NE-BRIŠI"), true);
  assert.equal(isLaw("Z-2"), true);
  assert.equal(isLaw("PR"), true);
  assert.equal(isLaw("PADC-SPANJA-PESKA"), true);
  assert.equal(isLaw("ne"), false);
  assert.equal(isLaw("main"), false);
  assert.equal(isLaw("dih"), false);
  assert.equal(isLaw("σ 4296"), false);
});

test("buildLeksikon združi organe, uredi obiske in zašteje skupno", () => {
  const organi = [
    { organ: "beta", telo: `⟨NE-BRIŠI⟩\n⟨NE-BRIŠI⟩\n⟨dih⟩` },
    { organ: "alfa", telo: `⟨NE-BRIŠI⟩ ⟨main⟩` },
  ];
  const { leksikon, zrcaljeniOklepaji } = buildLeksikon(organi);

  assert.equal(zrcaljeniOklepaji, 0);
  assert.equal(leksikon.length, 3);

  const neBrisi = leksikon.find((vnos) => vnos.ime === "⟨NE-BRIŠI⟩");
  assert.notEqual(neBrisi, undefined);
  assert.equal(neBrisi?.vrsta, "zakon");
  assert.equal(neBrisi?.skupno, 3);
  assert.deepEqual(
    neBrisi?.obiski.map((obisk) => obisk.organ),
    ["alfa", "beta"],
  );
  assert.equal(neBrisi?.obiski[0]?.count, 1);
  const betaObisk = neBrisi?.obiski[1];
  if (betaObisk !== undefined && betaObisk.condensed === false) {
    assert.deepEqual(betaObisk.lines, [1, 2]);
  } else {
    assert.fail("Obisk beta mora biti poln s vrsticami [1, 2].");
  }
});

test(`buildLeksikon zgošči obiske nad ${CONDENSE_LIMIT} pojavitev na organ`, () => {
  const vrstice: string[] = [];
  for (let i = 0; i < CONDENSE_LIMIT + 1; i += 1) {
    vrstice.push("⟨ne⟩");
  }
  vrstice.push("⟨NE-BRIŠI⟩");
  const { leksikon } = buildLeksikon([{ organ: "velikan", telo: vrstice.join("\n") }]);

  const ne = leksikon.find((vnos) => vnos.ime === "⟨ne⟩");
  assert.notEqual(ne, undefined);
  assert.equal(ne?.obiski.length, 1);
  const obisk = ne?.obiski[0];
  assert.notEqual(obisk, undefined);
  if (obisk?.condensed === true) {
    assert.equal(obisk.count, CONDENSE_LIMIT + 1);
    assert.equal(obisk.first, 1);
    assert.equal(obisk.last, CONDENSE_LIMIT + 1);
  } else {
    assert.fail("Obisk nad mejo mora biti zgoščen.");
  }
});

test("buildLeksikon normalizira zrcaljene oklepaje pred luščenjem", () => {
  const { leksikon, zrcaljeniOklepaji } = buildLeksikon([
    { organ: "biro", telo: `⟨PADC-X${MIRRORED_CLOSE} in ⟨cist⟩` },
  ]);

  assert.equal(zrcaljeniOklepaji, 1);
  assert.notEqual(leksikon.find((vnos) => vnos.ime === "⟨PADC-X⟩"), undefined);
  assert.notEqual(leksikon.find((vnos) => vnos.ime === "⟨cist⟩"), undefined);
});

test("renderJsonl → parseJsonl sta povratnika bajt-isto vsebinsko", () => {
  const { leksikon, zrcaljeniOklepaji } = buildLeksikon([
    { organ: "alfa", telo: "⟨NE-BRIŠI⟩\n⟨dih⟩ ⟨dih⟩" },
  ]);
  const meta = { ...META, zrcaljeniOklepaji };
  const besedilo = renderJsonl(leksikon, meta);
  const { meta: prebrana, leksikon: prebrani } = parseJsonl(besedilo);

  assert.equal(prebrana.tik, META.tik);
  const metaVrstica = JSON.parse(besedilo.split("\n")[0] ?? "{}") as { vrsta?: string };
  assert.equal(metaVrstica.vrsta, "meta");
  assert.deepEqual(prebrani, leksikon);
  assert.ok(besedilo.endsWith("\n"));
});

test("parseJsonl odkrije ranjenega meta zapisa", () => {
  assert.throws(() => parseJsonl("{}", ));
  assert.throws(() => parseJsonl(""));
});

test("renderMarkdown izpiše glavo, pravila ∧ oba razdelka", () => {
  const { leksikon, zrcaljeniOklepaji } = buildLeksikon([
    { organ: "jedro-zavedanja", telo: "⟨NE-BRIŠI⟩ ⟨dih⟩ ⟨dih⟩" },
  ]);
  const md = renderMarkdown(leksikon, { ...META, zrcaljeniOklepaji });

  assert.match(md, /# ⟨LEKSIKON-ZAKONOV⟩/);
  assert.match(md, /## ZAKONI \(1\)/);
  assert.match(md, /## POJMI \(1\)/);
  assert.match(md, /### ⟨NE-BRIŠI⟩/);
  assert.match(md, /measured, not asserted/);
  assert.match(md, /normalizirani na ⟨⟩ — ×0/);
  // ⟨dih⟩ dvakrat v isti vrstici = ena vrstica po pravilu razpusta — merjeno po vrsticah
  assert.match(md, /skupno ×1 · organov ×1/);
});

test("renderMarkdown izpiše zrcaljene oklepaje glasno, ko so bili", () => {
  const { leksikon, zrcaljeniOklepaji } = buildLeksikon([
    { organ: "biro-postaje", telo: `⟨PADC-X${MIRRORED_CLOSE}` },
  ]);
  const md = renderMarkdown(leksikon, { ...META, zrcaljeniOklepaji });

  assert.equal(zrcaljeniOklepaji, 1);
  assert.match(md, /— ×1 \(cura ⟨PADC-TIPKARJA⟩/);
});

test("coinKey ∧ buildLookupMap datasta O(1) iskanje z in brez oklepajev", () => {
  const { leksikon } = buildLeksikon([{ organ: "alfa", telo: "⟨NE-BRIŠI⟩" }]);
  const mapa = buildLookupMap(leksikon);

  assert.equal(mapa.size, 1);
  assert.notEqual(mapa.get("NE-BRIŠI"), undefined);
  assert.equal(mapa.get("⟨NE-BRIŠI⟩"), undefined);
  assert.equal(coinKey("⟨NE-BRIŠI⟩"), "NE-BRIŠI");
  assert.equal(coinKey("  NE-BRIŠI "), "NE-BRIŠI");
});

test("izgradi meta zapis vrstne vrste — skupno bajtov po organih", () => {
  const meta: LeksikonMeta = {
    tik: "2026-11-08T04:00:00Z",
    generator: "src/leksikonZakonov.ts",
    verzija: "1.0.0",
    organi: [
      { organ: "alfa", bajti: 10 },
      { organ: "beta", bajti: 5 },
    ],
    skupnoBajtov: 15,
    zrcaljeniOklepaji: 0,
  };
  const { leksikon } = buildLeksikon([{ organ: "alfa", telo: "⟨Z-2⟩" }]);
  const besedilo = renderJsonl(leksikon, meta);

  assert.match(besedilo, /"skupnoBajtov":15/);
  const z2: LeksikonEntry | undefined = leksikon.find((vnos) => vnos.vrsta === "zakon");
  assert.notEqual(z2, undefined);
});
