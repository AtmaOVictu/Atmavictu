import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { runCaptureIncomingTextProof } from "./captureIncomingTextProof.js";
import { validateManifest, type WorkbenchManifest } from "./workbenchManifest.js";
import { getManifestPath, readManifestFromFile } from "./workbenchManifestRepository.js";
import { LEKSIKON_VERSION, buildLeksikon, buildLookupMap, coinKey, type LeksikonMeta } from "./leksikonZakonov.js";
import { readOrgans, readLeksikonJsonl, writeLeksikon } from "./leksikonZakonovRepository.js";
import { detectWreathDrift, readDeedWitnesses, readLivingDoor, verifyWreath } from "./wreath/index.js";

export type AtmaCliCommand =
  | {
      name: "capture";
      projectRoot: string;
      title: string;
      body: string;
    }
  | {
      name: "show";
      projectRoot: string;
    }
  | {
      name: "verify";
      projectRoot: string;
    }
  | {
      name: "leksikon";
      organiKoren: string;
      izhodMapa: string;
    }
  | {
      name: "najdi";
      leksikonPot: string;
      ime: string;
    }
  | {
      name: "wreath";
      subcommand: "verify" | "drift" | "report";
      projectRoot: string;
    };

export function parseAtmaCliArgs(argv: readonly string[]): AtmaCliCommand {
  const [commandName, ...rest] = argv;

  if (commandName === undefined || commandName.trim().length === 0) {
    throw new Error(
      "Usage: node build/src/atmaCli.js <capture|show|verify|leksikon|najdi> <projectRoot> [title] [body]",
    );
  }

  switch (commandName) {
    case "capture":
      return parseCaptureCommand(rest);
    case "show":
      return {
        name: "show",
        projectRoot: requireCliValue("show requires <projectRoot>.", rest[0]),
      };
    case "verify":
      return {
        name: "verify",
        projectRoot: requireCliValue("verify requires <projectRoot>.", rest[0]),
      };
    case "leksikon":
      return {
        name: "leksikon",
        organiKoren: requireCliValue("leksikon requires <organiKoren> <izhodMapa>.", rest[0]),
        izhodMapa: requireCliValue("leksikon requires <organiKoren> <izhodMapa>.", rest[1]),
      };
    case "najdi":
      return {
        name: "najdi",
        leksikonPot: requireCliValue("najdi requires <leksikonPot> <ime>.", rest[0]),
        ime: requireCliValue("najdi requires <leksikonPot> <ime>.", rest[1]),
      };
    case "wreath":
      return parseWreathCommand(rest);
    default:
      throw new Error(
        "Unknown command: " +
          commandName +
          ". Expected one of: capture, show, verify, leksikon, najdi.",
      );
  }
}

export async function runAtmaCliCommand(command: AtmaCliCommand): Promise<string> {
  switch (command.name) {
    case "capture":
      return runCaptureIncomingTextProof({
        projectRoot: command.projectRoot,
        title: command.title,
        body: command.body,
      });
    case "show":
      return runShowCommand(command.projectRoot);
    case "verify":
      return runVerifyCommand(command.projectRoot);
    case "leksikon":
      return runLeksikonCommand(command.organiKoren, command.izhodMapa);
    case "najdi":
      return runNajdiCommand(command.leksikonPot, command.ime);
    case "wreath":
      return runWreathCommand(command.subcommand, command.projectRoot);
  }
}

function parseWreathCommand(argv: readonly string[]): AtmaCliCommand {
  const [subcommand, projectRoot] = argv;
  const sub = requireCliValue("wreath requires <verify|drift|report> <projectRoot>.", subcommand);
  if (sub !== "verify" && sub !== "drift" && sub !== "report") {
    throw new Error(`Unknown wreath subcommand: ${sub}. Expected one of: verify, drift, report.`);
  }
  return {
    name: "wreath",
    subcommand: sub,
    projectRoot: requireCliValue("wreath requires <verify|drift|report> <projectRoot>.", projectRoot),
  };
}

function runWreathCommand(subcommand: "verify" | "drift" | "report", projectRoot: string): string {
  if (subcommand === "verify") {
    const verification = verifyWreath(projectRoot);
    const lines = [
      "WREATH VERIFY:",
      `STATUS: ${verification.status}`,
      `SLOTS: ${verification.total}`,
      `MATCHED: ${verification.matched}`,
      ...verification.results.map((result) => `- ${result.path}: ${result.matched ? "MATCH" : "MISMATCH"} (${result.actualSha256.length > 0 ? result.actualSha256 : "<absent>"})`),
    ];
    if (verification.status === "FAIL") {
      throw new Error(lines.join("\n"));
    }
    return lines.join("\n");
  }

  if (subcommand === "drift") {
    const report = detectWreathDrift(projectRoot);
    const lines = [
      "WREATH DRIFT:",
      `DRIFT: ${report.drift ? "DA" : "NE"}`,
      `DOOR HASH: ${report.doorHash ?? "<absent>"}`,
      ...report.details.map((detail) => `- ${detail}`),
    ];
    if (report.drift) {
      throw new Error(lines.join("\n"));
    }
    return lines.join("\n");
  }

  const verification = verifyWreath(projectRoot);
  return [
    "WREATH REPORT:",
    `STATUS: ${verification.status}`,
    `SLOTS: ${verification.total}`,
    `MATCHED: ${verification.matched}`,
    `DEEDS: ${readDeedWitnesses(projectRoot).length}`,
    `LIVING DOOR: ${readLivingDoor(projectRoot) !== null ? "DA" : "NE"}`,
  ].join("\n");
}

function parseCaptureCommand(argv: readonly string[]): AtmaCliCommand {
  const [projectRoot, title, body] = argv;

  return {
    name: "capture",
    projectRoot: requireCliValue("capture requires <projectRoot> <title> <body>.", projectRoot),
    title: requireCliValue("capture requires <projectRoot> <title> <body>.", title),
    body: requireCliValue("capture requires <projectRoot> <title> <body>.", body),
  };
}

async function runLeksikonCommand(organiKoren: string, izhodMapa: string): Promise<string> {
  const { organi, merice, izpusteni } = await readOrgans(organiKoren);
  const { leksikon, zrcaljeniOklepaji } = buildLeksikon(organi);

  const skupnoBajtov = merice.reduce((vsota, merica) => vsota + merica.bajti, 0);
  const meta: LeksikonMeta = {
    tik: new Date().toISOString().replace(/\.\d{1,6}Z$/, "Z"),
    generator: "src/leksikonZakonov.ts",
    verzija: LEKSIKON_VERSION,
    organi: merice,
    skupnoBajtov,
    zrcaljeniOklepaji,
  };

  const zapis = await writeLeksikon(izhodMapa, leksikon, meta);
  const zakoni = leksikon.filter((vnos) => vnos.vrsta === "zakon").length;
  const pojmi = leksikon.filter((vnos) => vnos.vrsta === "pojem").length;

  return [
    "LEKSIKON-ZAKONOV",
    `ORGANOV: ${organi.length} (SKUPNO ${skupnoBajtov} B)`,
    izpusteni.length > 0 ? `IZPUSTENI (brez KNOWLEDGE.md): ${izpusteni.join(", ")}` : "IZPUSTENI: 0",
    `ZAKONI: ${zakoni} · POJMI: ${pojmi} · SKUPNO: ${leksikon.length}`,
    `ZRCALJENI OKLEPAJI NORMALIZIRANI: ${zrcaljeniOklepaji}`,
    `JSONL: ${zapis.jsonlPot} (${zapis.jsonlBajti} B)`,
    `MARKDOWN: ${zapis.mdPot} (${zapis.mdBajti} B)`,
  ].join("\n");
}

async function runNajdiCommand(leksikonPot: string, ime: string): Promise<string> {
  const { leksikon } = await readLeksikonJsonl(leksikonPot);
  const mapa = buildLookupMap(leksikon);
  const kljuc = coinKey(ime);
  const vnos = mapa.get(kljuc);

  if (vnos === undefined) {
    return [
      "NAJDEN: ⟨ne⟩",
      `KOVANEC: ${ime} ni v leksikonu (izmerjeno pri kazalu, ⟨ne⟩ ugibano ⊙ Z-2)`,
    ].join("\n");
  }

  const vrstice = vnos.obiski.map((obisk) => {
    if (obisk.condensed) {
      return `- ${obisk.organ} → ×${obisk.count} (prva ${obisk.first} · zadnja ${obisk.last})`;
    }
    return `- ${obisk.organ} → vrstice ${obisk.lines.join(", ")}`;
  });

  return [
    `KOVANEC: ${vnos.ime}`,
    `VRSTA: ${vnos.vrsta} · SKUPNO ×${vnos.skupno} · ORGANOV ×${vnos.obiski.length}`,
    ...vrstice,
  ].join("\n");
}

async function runShowCommand(projectRoot: string): Promise<string> {
  const manifest = await readManifestFromFile(getManifestPath(projectRoot));
  const lastIncomingText = manifest.incomingTexts[manifest.incomingTexts.length - 1];

  return [
    "ATMAVICTU WORKBENCH",
    `MANIFEST VERSION: ${manifest.manifestVersion}`,
    `INCOMING TEXTS: ${manifest.incomingTexts.length}`,
    `FRAGMENTS: ${manifest.fragments.length}`,
    `INSERTIONS: ${manifest.insertions.length}`,
    `LAST INCOMING ID: ${lastIncomingText?.id ?? "<none>"}`,
    `LAST SOURCE: ${lastIncomingText?.sourcePath ?? "<none>"}`,
    `LAST STATUS: ${lastIncomingText?.status ?? "<none>"}`,
  ].join("\n");
}

async function runVerifyCommand(projectRoot: string): Promise<string> {
  const manifestPath = getManifestPath(projectRoot);

  let rawManifest: string;
  try {
    rawManifest = await readFile(manifestPath, "utf8");
  } catch (error) {
    return renderVerifyFailure([
      `Manifest file does not exist or cannot be read: ${manifestPath}`,
      formatErrorMessage(error),
    ]);
  }

  let parsedManifest: unknown;
  try {
    parsedManifest = JSON.parse(rawManifest) as unknown;
  } catch (error) {
    return renderVerifyFailure([
      `Manifest file contains invalid JSON: ${manifestPath}`,
      formatErrorMessage(error),
    ]);
  }

  const result = validateManifest(parsedManifest as WorkbenchManifest);
  if (result.isValid) {
    return ["VERIFY: PASS", "ERRORS: 0"].join("\n");
  }

  return renderVerifyFailure(result.errors);
}

function renderVerifyFailure(errors: readonly string[]): string {
  return ["VERIFY: FAIL", "ERRORS:", ...errors.map((error) => `- ${error}`)].join("\n");
}

function requireCliValue(message: string, value: string | undefined): string {
  if (value === undefined || value.trim().length === 0) {
    throw new Error(message);
  }

  return value;
}

function formatErrorMessage(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}

async function main(): Promise<void> {
  const command = parseAtmaCliArgs(process.argv.slice(2));
  const output = await runAtmaCliCommand(command);
  process.stdout.write(`${output}\n`);
}

function isDirectExecution(): boolean {
  const entryPath = process.argv[1];
  if (entryPath === undefined) {
    return false;
  }

  return resolve(entryPath) === fileURLToPath(import.meta.url);
}

if (isDirectExecution()) {
  try {
    await main();
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    process.stderr.write(`${message}\n`);
    process.exitCode = 1;
  }
}
