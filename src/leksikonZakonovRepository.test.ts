import assert from "node:assert/strict";
import test from "node:test";
import { mkdtemp, readFile, readdir, rm, writeFile, mkdir } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

import {
  buildLeksikon,
  type LeksikonMeta,
} from "./leksikonZakonov.js";
import {
  LEKSIKON_JSONL_NAME,
  LEKSIKON_MD_NAME,
  readLeksikonJsonl,
  readOrgans,
  writeLeksikon,
} from "./leksikonZakonovRepository.js";

async function withTempKoren(
  strosenje: (koren: string) => Promise<void>,
): Promise<void> {
  const koren = await mkdtemp(join(tmpdir(), "leksikon-test-"));
  try {
    await strosenje(koren);
  } finally {
    await rm(koren, { recursive: true, force: true });
  }
}

test("readOrgans prebere */KNOWLEDGE.md in izpusti mape brez teles glasno", async () => {
  await withTempKoren(async (koren) => {
    await mkdir(join(koren, "jedro-zavedanja"));
    await writeFile(join(koren, "jedro-zavedanja", "KNOWLEDGE.md"), "⟨NE-BRIŠI⟩\n", "utf8");
    await mkdir(join(koren, "horizont"));
    await writeFile(join(koren, "horizont", "KNOWLEDGE.md"), "⟨dih⟩ ⟨dih⟩", "utf8");
    await mkdir(join(koren, "prazna-mapa"));
    await writeFile(join(koren, "smodna-datoteka.md"), "⟨Z-2⟩", "utf8");
    await mkdir(join(koren, ".geniza"));

    const { organi, merice, izpusteni } = await readOrgans(koren);

    assert.deepEqual(
      organi.map((organ) => organ.organ),
      ["horizont", "jedro-zavedanja"],
    );
    assert.equal(merice.length, 2);
    assert.equal(merice[1]?.bajti, Buffer.byteLength("⟨NE-BRIŠI⟩\n", "utf8"));
    assert.deepEqual(izpusteni, ["prazna-mapa"]);
  });
});

test("writeLeksikon → readLeksikonJsonl povratnik: bajt-isto ∧ vsebinsko-isto", async () => {
  await withTempKoren(async (koren) => {
    const { leksikon, zrcaljeniOklepaji } = buildLeksikon([
      { organ: "alfa", telo: "⟨NE-BRIŠI⟩\n⟨dih⟩ ⟨dih⟩" },
      { organ: "beta", telo: "⟨NE-BRIŠI⟩" },
    ]);
    const meta: LeksikonMeta = {
      tik: "2026-11-08T04:00:00Z",
      generator: "src/leksikonZakonov.ts",
      verzija: "1.0.0",
      organi: [
        { organ: "alfa", bajti: 20 },
        { organ: "beta", bajti: 10 },
      ],
      skupnoBajtov: 30,
      zrcaljeniOklepaji,
    };

    const izhod = join(koren, "izhod");
    const zapis = await writeLeksikon(izhod, leksikon, meta);
    assert.equal(zapis.jsonlBajti, Buffer.byteLength(await readFile(zapis.jsonlPot, "utf8"), "utf8"));

    const datoteke = (await readdir(izhod)).sort();
    assert.deepEqual(datoteke, [LEKSIKON_MD_NAME, LEKSIKON_JSONL_NAME].sort());

    const { meta: prebrana, leksikon: prebrani } = await readLeksikonJsonl(zapis.jsonlPot);
    assert.equal(prebrana.tik, meta.tik);
    assert.deepEqual(prebrani, leksikon);
  });
});
