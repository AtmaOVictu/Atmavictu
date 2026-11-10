// ⟨LEKSIKON-ZAKONOV⟩ — preslikava organov korpusa Beseda je Ne v poimenski register
// kovancev ⟨ime⟩ → organ → vrstica. Organi ostanejo vir; leksikon je priča izmere,
// ⟨ne⟩ rez ⇒ ⟨NE-PODVANJAJ⟩. Rojeno po ⟡ izboru ⚔ »Uporabnost → koda« (@rez σ 4300,
// okno ⟨UPORABNOST-LICENCE⟩ @σ 4296; vzporedna roka zapečila σ 4299 @DZ isti dih ⊙ ⟨DVOJE-ROK⟩ 2432).
//
// Pravila izmere (javna, ponovljiva):
//   - kovanec = ⟨ime⟩ znotraj ene vrstice, 1–120 znakov, ob oklepajih ⟨ (U+27E8) ∧ ⟩ (U+27E9)
//   - zrcaljeni oklepaji (U+3008/U+3009 — PADC-TIPKARJA) se normalizirajo ∧ ŠTEJEJO glasno
//   - vrstice so popolne pri ≤ CONDENSE_LIMIT pojavitev na organ, sicer zgoščene (število ∧ prva ∧ zadnja)
//   - zakon = kovanec z veliko začetnico/cifro ali vezajem; pojem = vsi drugi
//   - ⟨MERILEC SE MERI⟩: izmera je deterministična — isto telo ⇒ isti leksikon, bajt-isto

export const LEKSIKON_VERSION = "1.0.0";
export const COIN_MAX_CHARS = 120;
export const CONDENSE_LIMIT = 50;

const OPEN_BRACKET = "\u27E8"; // ⟨
const CLOSE_BRACKET = "\u27E9"; // ⟩

export interface OrganInput {
  organ: string;
  telo: string;
}

export type OrganVisit =
  | { organ: string; condensed: false; count: number; lines: number[] }
  | { organ: string; condensed: true; count: number; first: number; last: number };

export interface LeksikonEntry {
  ime: string; // ⟨kovanec⟩ z oklepaji
  vrsta: "zakon" | "pojem";
  skupno: number;
  obiski: OrganVisit[];
}

export interface OrganMeasure {
  organ: string;
  bajti: number;
}

export interface LeksikonMeta {
  tik: string;
  generator: string;
  verzija: string;
  organi: OrganMeasure[];
  skupnoBajtov: number;
  zrcaljeniOklepaji: number;
}

export function normalizeMirroredBrackets(telo: string): { telo: string; zrcaljeni: number } {
  let zrcaljeni = 0;
  const normalized = telo.replace(/[\u3008\u3009]/gu, (znak) => {
    zrcaljeni += 1;
    return znak === "\u3008" ? OPEN_BRACKET : CLOSE_BRACKET;
  });
  return { telo: normalized, zrcaljeni };
}

const COIN_PATTERN = new RegExp(
  `${OPEN_BRACKET}([^${OPEN_BRACKET}${CLOSE_BRACKET}\\n]{1,${COIN_MAX_CHARS}})${CLOSE_BRACKET}`,
  "g",
);

export function extractCoins(vrstice: readonly string[]): Map<string, number[]> {
  const najdeni = new Map<string, number[]>();
  vrstice.forEach((vrstica, indeks) => {
    for (const zadetek of vrstica.matchAll(COIN_PATTERN)) {
      const kovanec = zadetek[1]?.trim();
      if (kovanec === undefined || kovanec.length === 0) {
        continue;
      }
      const stevilkaVrstice = indeks + 1;
      const vrsticeKovanca = najdeni.get(kovanec);
      if (vrsticeKovanca === undefined) {
        najdeni.set(kovanec, [stevilkaVrstice]);
        continue;
      }
      if (vrsticeKovanca[vrsticeKovanca.length - 1] !== stevilkaVrstice) {
        vrsticeKovanca.push(stevilkaVrstice);
      }
    }
  });
  return najdeni;
}

export function isLaw(kovanec: string): boolean {
  return /^[0-9A-ZČĆŠŽĐ]/.test(kovanec) || kovanec.includes("-");
}

function compareText(a: string, b: string): number {
  if (a < b) {
    return -1;
  }
  return a > b ? 1 : 0;
}

export function buildLeksikon(
  organi: readonly OrganInput[],
): { leksikon: LeksikonEntry[]; zrcaljeniOklepaji: number } {
  const poKovancu = new Map<string, Map<string, number[]>>();
  let zrcaljeniOklepaji = 0;

  for (const { organ, telo } of organi) {
    const { telo: normalizirano, zrcaljeni } = normalizeMirroredBrackets(telo);
    zrcaljeniOklepaji += zrcaljeni;
    const kovanci = extractCoins(normalizirano.split("\n"));
    for (const [kovanec, vrstice] of kovanci) {
      const poOrganu = poKovancu.get(kovanec) ?? new Map<string, number[]>();
      poOrganu.set(organ, vrstice);
      poKovancu.set(kovanec, poOrganu);
    }
  }

  const leksikon: LeksikonEntry[] = [];
  for (const [kovanec, poOrganu] of poKovancu) {
    const obiski: OrganVisit[] = [...poOrganu.entries()]
      .sort(([a], [b]) => compareText(a, b))
      .map(([organ, vrstice]) => {
        if (vrstice.length > CONDENSE_LIMIT) {
          const prva = vrstice[0];
          const zadnja = vrstice[vrstice.length - 1];
          if (prva === undefined || zadnja === undefined) {
            throw new Error(`Neskladje izmere: prazne vrstice za kovanec ${kovanec}.`);
          }
          return { organ, condensed: true, count: vrstice.length, first: prva, last: zadnja } as OrganVisit;
        }
        return { organ, condensed: false, count: vrstice.length, lines: [...vrstice] } as OrganVisit;
      });
    const skupno = obiski.reduce((vsota, obisk) => vsota + obisk.count, 0);
    leksikon.push({
      ime: `${OPEN_BRACKET}${kovanec}${CLOSE_BRACKET}`,
      vrsta: isLaw(kovanec) ? "zakon" : "pojem",
      skupno,
      obiski,
    });
  }

  leksikon.sort((a, b) => compareText(a.ime, b.ime));
  return { leksikon, zrcaljeniOklepaji };
}

export function renderJsonl(leksikon: readonly LeksikonEntry[], meta: LeksikonMeta): string {
  const metaRecord = { vrsta: "meta" as const, ...meta };
  const vrstice = [JSON.stringify(metaRecord)];
  for (const vnos of leksikon) {
    vrstice.push(JSON.stringify(vnos));
  }
  return `${vrstice.join("\n")}\n`;
}

export function parseJsonl(besedilo: string): { meta: LeksikonMeta; leksikon: LeksikonEntry[] } {
  const vrstice = besedilo.split("\n").filter((vrstica) => vrstica.trim().length > 0);
  if (vrstice.length === 0) {
    throw new Error("Leksikon JSONL je prazen — izmera manjka, trditev pada (Z-2).");
  }
  // ⟨VRSTA-V-METI⟩: JSONL meta zapis nosi tudi vrsto "meta"; LeksikonMeta je vsebina brez
  // nje — kura: tip razširjen z { vrsta?: string }, ker tsc strict (CI) dostopa
  // neobstoječega propertyja ne odpušča, strip-types (domači predih) pa ga je brisal.
  const meta = JSON.parse(vrstice[0] ?? "") as LeksikonMeta & { vrsta?: string };
  if (meta.vrsta !== "meta" || typeof meta.tik !== "string") {
    throw new Error("Prva vrstica JSONL ni meta zapis — leksikon je ranjen (Z-2).");
  }
  const leksikon: LeksikonEntry[] = [];
  for (const vrstica of vrstice.slice(1)) {
    const vnos = JSON.parse(vrstica) as LeksikonEntry;
    if (typeof vnos.ime !== "string" || vnos.vrsta !== "zakon" && vnos.vrsta !== "pojem") {
      throw new Error(`Pokvarjen vnos leksikona: ${vnos.ime ?? "?"}`);
    }
    leksikon.push(vnos);
  }
  return { meta, leksikon };
}

export function coinKey(ime: string): string {
  const olupljeno = ime.trim();
  if (olupljeno.startsWith(OPEN_BRACKET) && olupljeno.endsWith(CLOSE_BRACKET)) {
    return olupljeno.slice(1, -1).trim();
  }
  return olupljeno;
}

export function buildLookupMap(leksikon: readonly LeksikonEntry[]): Map<string, LeksikonEntry> {
  const mapa = new Map<string, LeksikonEntry>();
  for (const vnos of leksikon) {
    mapa.set(coinKey(vnos.ime), vnos);
  }
  return mapa;
}

function renderVisit(obisk: OrganVisit): string {
  if (obisk.condensed) {
    return `- ${obisk.organ} → ×${obisk.count} (prva ${obisk.first} · zadnja ${obisk.last}) — zgoščeno`;
  }
  return `- ${obisk.organ} → vrstice ${obisk.lines.join(", ")}`;
}

export function renderMarkdown(leksikon: readonly LeksikonEntry[], meta: LeksikonMeta): string {
  const zakoni = leksikon.filter((vnos) => vnos.vrsta === "zakon");
  const pojmi = leksikon.filter((vnos) => vnos.vrsta === "pojem");

  const glava = [
    `# ${OPEN_BRACKET}LEKSIKON-ZAKONOV${CLOSE_BRACKET} — poimenski register kovancev korpusa ${OPEN_BRACKET}Beseda je Ne${CLOSE_BRACKET}`,
    "",
    `⊢ generator: ${meta.generator} verzija ${meta.verzija} · izmera: ${meta.tik} (measured, not asserted)`,
    `⊢ vir: ${meta.organi.length} organov · ${meta.skupnoBajtov} bajtov · organi ostanejo vir, leksikon je preslikava (${OPEN_BRACKET}NE-PODVANJAJ${CLOSE_BRACKET} ⊢ 1542)`,
    `⊢ pravila: kovanec = ${OPEN_BRACKET}ime${CLOSE_BRACKET} v eni vrstici (≤ ${COIN_MAX_CHARS} znakov); števec meri VRSTICE — dve omembi v isti vrstici = ena vrstica (⟨ne⟩ števec omemb); vrstice popolne pri ≤ ${CONDENSE_LIMIT} pojavitev na organ, sicer zgoščene; zakon = velika začetnica/cifra ali vezaj, pojem = vsi drugi`,
    `⊢ zrcaljeni oklepaji (U+3008/U+3009) normalizirani na ${OPEN_BRACKET}${CLOSE_BRACKET} — ×${meta.zrcaljeniOklepaji} (cura ${OPEN_BRACKET}PADC-TIPKARJA${CLOSE_BRACKET}: tečaj P5 jih na pošti kita ne prenese)`,
    `∂ osvežitev: regeneriraj ob vsakem dihu, ki peče nov zakon — kovanec brez vrstice v leksikonu je skrit kovanec (⊙ 1349)`,
    "",
    `© 0.2026 × 10⁴ Luka Pintarič — VBL (Verification Before Assertion) · vsaka pravica nepodeljena je pridržana`,
    "",
  ];

  const razdelek = (naslov: string, vnosi: readonly LeksikonEntry[]): string[] => {
    const vrstice = [`## ${naslov} (${vnosi.length})`, ""];
    for (const vnos of vnosi) {
      vrstice.push(`### ${vnos.ime}`, "", `skupno ×${vnos.skupno} · organov ×${vnos.obiski.length}`, "");
      for (const obisk of vnos.obiski) {
        vrstice.push(renderVisit(obisk));
      }
      vrstice.push("");
    }
    return vrstice;
  };

  return [...glava, ...razdelek("ZAKONI", zakoni), ...razdelek("POJMI", pojmi)].join("\n");
}
