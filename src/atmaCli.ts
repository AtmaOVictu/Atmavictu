import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { runCaptureIncomingTextProof } from "./captureIncomingTextProof.js";
import { validateManifest, type WorkbenchManifest } from "./workbenchManifest.js";
import { getManifestPath, readManifestFromFile } from "./workbenchManifestRepository.js";
import {
  verifyWreath,
  loadWreathManifest,
  verifyWreathSlot,
  type WreathSlotResult,
  listTongues,
  tongueFromSlot,
  readDeedWitnesses,
  hasAnyDeed,
  allReviewedNone,
  readLivingDoor,
  detectWreathDrift,
  type ReviewStatus,
} from "./wreath/index.js";

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
      name: "wreath";
      subcommand: "verify" | "report" | "drift";
      projectRoot: string;
    };

export function parseAtmaCliArgs(argv: readonly string[]): AtmaCliCommand {
  const [commandName, ...rest] = argv;

  if (commandName === undefined || commandName.trim().length === 0) {
    throw new Error(
      "Usage: node build/src/atmaCli.js <capture|show|verify|wreath> <projectRoot> [title] [body]",
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
    case "wreath":
      return parseWreathCommand(rest);
    default:
      throw new Error(
        `Unknown command: ${commandName}. Expected one of: capture, show, verify, wreath.`,
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
    case "wreath":
      return runWreathCommand(command);
  }
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

/**
 * Pripravi vrstico poročila za en wreath slot: jezik, kanon, slot, hash,
 * pregled (druga roka) in dejanska priča.
 */
function buildWreathRow(root: string, slot: WreathSlotResult): string[] {
  const tongue = tongueFromSlot(slot.path);
  const hash = slot.matched ? "✓" : "✗";
  const review = allReviewedNone(root, [slot.path])[0] ?? { stage: "none" };
  const stage = review.stage === "none" ? "—" : review.stage;
  const deed = hasAnyDeed(root) ? "⊢" : "—";
  return [
    tongue ? tongue.code : "—",
    tongue ? tongue.language : "—",
    slot.path,
    hash,
    stage,
    deed,
  ];
}

function renderWreathReport(root: string): string {
  const verification = verifyWreath(root);
  const tongues = listTongues();
  const deeds = readDeedWitnesses(root);
  const lines: string[] = [];
  lines.push("WREATH — priče veneca");
  lines.push(`uključenih slotov: ${verification.total} · ujemajočih: ${verification.matched} · stanje: ${verification.status}`);
  lines.push("");
  lines.push(
    ["jezik", "jezik (ime)", "slot", "hash", "pregled", "dejanje"].join(" | "),
  );
  lines.push(["-----", "-----------", "-----", "----", "-------", "------"].join("-|-"));
  for (const result of verification.results) {
    lines.push(buildWreathRow(root, result).join(" | "));
  }
  lines.push("");
  lines.push(`dejanske priče v registru: ${deeds.length}`);
  lines.push(`živa vrata: ${readLivingDoor(root) ? "prisotne" : "odsotne"}`);
  lines.push("");
  lines.push(verification.status === "PASS" ? "WREATH VERIFY: PASS" : "WREATH VERIFY: " + verification.status);
  return lines.join("\n");
}

function parseWreathCommand(argv: readonly string[]): AtmaCliCommand {
  const [subcommand, ...rest] = argv;
  if (subcommand !== "verify" && subcommand !== "report" && subcommand !== "drift") {
    throw new Error(
      `Unknown wreath subcommand: ${subcommand ?? "<none>"}. Expected one of: verify, report, drift.`,
    );
  }
  return {
    name: "wreath",
    subcommand: subcommand as "verify" | "report" | "drift",
    projectRoot: requireCliValue(`wreath ${subcommand} requires <projectRoot>.`, rest[0]),
  };
}

async function runWreathCommand(command: Extract<AtmaCliCommand, { name: "wreath" }>): Promise<string> {
  if (command.subcommand === "verify") {
    const verification = verifyWreath(command.projectRoot);
    let summary = [
      `WREATH VERIFY: ${verification.status}`,
      `slotov: ${verification.total}, ujemajočih: ${verification.matched}`,
    ].join("\n");
    if (verification.status !== "PASS") {
      for (const result of verification.results) {
        if (!result.matched) {
          summary += `\n- ${result.path}: hash ${result.actualSha256 ?? "<missing>"} ≠ manifest ${result.sha256}`;
        }
      }
    }
    return summary;
  }
  if (command.subcommand === "drift") {
    return renderWreathDrift(command.projectRoot);
  }
  return renderWreathReport(command.projectRoot);
}

function renderWreathDrift(root: string): string {
  const report = detectWreathDrift(root);
  const lines: string[] = [];
  lines.push("WREATH — drift interferenca");
  lines.push(report.drift ? "WREATH DRIFT: DETECTED" : "WREATH DRIFT: none");
  lines.push(`živa vrata (LICENSE.md): ${report.doorHash ?? "<absent>"}`);
  lines.push(`manifest slot LICENSE.md: ${report.manifestSlotHash ?? "<absent>"}`);
  for (const detail of report.details) {
    lines.push(`- ${detail}`);
  }
  if (report.details.length === 0) {
    lines.push("door ≡ manifest slot — brez drift-a; companionji so priče, ne vrata");
  }
  return lines.join("\n");
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
