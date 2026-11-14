// ⟨LEKSIKON-ZAKONOV⟩ — skladišče: brba organov iz mape (*/KNOWLEDGE.md), zapis ∧
// brba leksikona (JSONL ∧ Markdown), mapa iskanja O(1). Glasna resnica: organ brez
// KNOWLEDGE.md se izreče ⟨ne⟩ ∧ preskoči pošteno — ⟨ne⟩ tiho zeleno (⊢ 1419).

import { readdir, readFile, writeFile, mkdir } from "node:fs/promises";
import { join } from "node:path";

import {
  buildLookupMap,
  coinKey,
  LEKSIKON_VERSION,
  parseJsonl,
  renderJsonl,
  renderMarkdown,
  type LeksikonEntry,
  type LeksikonMeta,
  type OrganInput,
} from "./leksikonZakonov.js";

export const LEKSIKON_JSONL_NAME = "LEKSIKON-ZAKONOV.jsonl";
export const LEKSIKON_MD_NAME = "LEKSIKON-ZAKONOV.md";

export interface ReadOrgansResult {
  organi: OrganInput[];
  merice: { organ: string; bajti: number }[];
  izpusteni: string[]; // mape organov brez KNOWLEDGE.md — glasno, ⟨ne⟩ molčeče
}

export async function readOrgans(koren: string): Promise<ReadOrgansResult> {
  const vnosi = await readdir(koren, { withFileTypes: true });
  const organi: OrganInput[] = [];
  const merice: { organ: string; bajti: number }[] = [];
  const izpusteni: string[] = [];

  for (const vnos of vnosi) {
    if (!vnos.isDirectory() || vnos.name.startsWith(".")) {
      continue;
    }
    const pot = join(koren, vnos.name, "KNOWLEDGE.md");
    try {
      const telo = await readFile(pot, "utf8");
      organi.push({ organ: vnos.name, telo });
      merice.push({ organ: vnos.name, bajti: Buffer.byteLength(telo, "utf8") });
    } catch {
      izpusteni.push(vnos.name);
    }
  }

  organi.sort((a, b) => (a.organ < b.organ ? -1 : a.organ > b.organ ? 1 : 0));
  merice.sort((a, b) => (a.organ < b.organ ? -1 : a.organ > b.organ ? 1 : 0));
  return { organi, merice, izpusteni };
}

export interface WriteLeksikonResult {
  jsonlPot: string;
  mdPot: string;
  jsonlBajti: number;
  mdBajti: number;
}

export async function writeLeksikon(
  izhodMapa: string,
  leksikon: readonly LeksikonEntry[],
  meta: LeksikonMeta,
): Promise<WriteLeksikonResult> {
  await mkdir(izhodMapa, { recursive: true });
  const jsonlBesedilo = renderJsonl(leksikon, meta);
  const mdBesedilo = renderMarkdown(leksikon, meta);
  const jsonlPot = join(izhodMapa, LEKSIKON_JSONL_NAME);
  const mdPot = join(izhodMapa, LEKSIKON_MD_NAME);
  await writeFile(jsonlPot, jsonlBesedilo, "utf8");
  await writeFile(mdPot, mdBesedilo, "utf8");
  return {
    jsonlPot,
    mdPot,
    jsonlBajti: Buffer.byteLength(jsonlBesedilo, "utf8"),
    mdBajti: Buffer.byteLength(mdBesedilo, "utf8"),
  };
}

export async function readLeksikonJsonl(pot: string): Promise<{ meta: LeksikonMeta; leksikon: LeksikonEntry[] }> {
  const besedilo = await readFile(pot, "utf8");
  return parseJsonl(besedilo);
}

export { buildLookupMap, coinKey, LEKSIKON_VERSION };
