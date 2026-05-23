import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { runCaptureIncomingTextProof } from "./captureIncomingTextProof.js";
import { validateManifest, type WorkbenchManifest } from "./workbenchManifest.js";
import { getManifestPath, readManifestFromFile } from "./workbenchManifestRepository.js";

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
    };

export function parseAtmaCliArgs(argv: readonly string[]): AtmaCliCommand {
  const [commandName, ...rest] = argv;

  if (commandName === undefined || commandName.trim().length === 0) {
    throw new Error(
      "Usage: node build/src/atmaCli.js <capture|show|verify> <projectRoot> [title] [body]",
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
    default:
      throw new Error(`Unknown command: ${commandName}. Expected one of: capture, show, verify.`);
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
