import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { runCaptureIncomingTextProof } from "./captureIncomingTextProof.js";
import {
  addConcept,
  archiveFragment,
  archiveIncoming,
  bulkInsert,
  createFragmentFromIncoming,
  insertFragmentIntoChapter,
  startProcessingIncoming,
  updateFragment,
  updateIncomingText,
  updateInsertion,
  validateManifest,
  type Fragment,
  type IncomingText,
  type Insertion,
  type WorkbenchManifest,
} from "./workbenchManifest.js";
import {
  getManifestPath,
  mutateManifestFile,
  readManifestFromFile,
} from "./workbenchManifestRepository.js";

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
      name: "start-processing";
      projectRoot: string;
      incomingId: string;
    }
  | {
      name: "create-fragment";
      projectRoot: string;
      incomingId: string;
      body: string;
      title?: string;
    }
  | {
      name: "insert";
      projectRoot: string;
      fragmentId: string;
      targetChapterPath: string;
    }
  | {
      name: "update-incoming";
      projectRoot: string;
      incomingId: string;
      title?: string | null;
      note?: string | null;
    }
  | {
      name: "update-fragment";
      projectRoot: string;
      fragmentId: string;
      text?: string;
      title?: string | null;
      note?: string | null;
    }
  | {
      name: "update-insertion";
      projectRoot: string;
      insertionId: string;
      targetChapterPath?: string;
      positionNote?: string | null;
      note?: string | null;
    }
  | {
      name: "archive-fragment";
      projectRoot: string;
      fragmentId: string;
    }
  | {
      name: "archive-incoming";
      projectRoot: string;
      incomingId: string;
    }
  | {
      name: "add-concept";
      projectRoot: string;
      label: string;
      note?: string;
    }
  | {
      name: "help";
    }
  | {
      name: "bulk-insert";
      projectRoot: string;
      pairs: Array<{ fragmentId: string; targetChapterPath: string }>;
    }
  | {
      name: "walk";
      projectRoot: string;
      title: string;
      body: string;
      fragmentBody: string;
      targetChapterPath: string;
    };

export function parseAtmaCliArgs(argv: readonly string[]): AtmaCliCommand {
  const [commandName, ...rest] = argv;

  if (commandName === undefined || commandName.trim().length === 0) {
    throw new Error(
      "Usage: node build/src/atmaCli.js <capture|show|verify|start-processing|create-fragment|insert|update-incoming|update-fragment|update-insertion|archive-fragment|archive-incoming|add-concept|bulk-insert|walk> <projectRoot> [...]",
    );
  }

  switch (commandName) {
    case "capture":
      return parseCaptureCommand(rest);
    case "help":
      return { name: "help" };
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
    case "bulk-insert": {
      const bulkRoot = requireCliValue(
        "bulk-insert requires <projectRoot> <fragmentId=targetChapterPath> [...].",
        rest[0],
      );
      const pairs = rest.slice(1).map((pair) => {
        const cut = pair.indexOf("=");
        if (cut <= 0 || cut >= pair.length - 1) {
          throw new Error(
            "bulk-insert pairs must look like <fragmentId=targetChapterPath>: " + pair,
          );
        }
        return {
          fragmentId: pair.slice(0, cut),
          targetChapterPath: pair.slice(cut + 1),
        };
      });
      if (pairs.length === 0) {
        throw new Error("bulk-insert requires at least one <fragmentId=targetChapterPath> pair.");
      }
      return { name: "bulk-insert", projectRoot: bulkRoot, pairs };
    }
    case "start-processing":
      return {
        name: "start-processing",
        projectRoot: requireCliValue("start-processing requires <projectRoot> <incomingId>.", rest[0]),
        incomingId: requireCliValue("start-processing requires <projectRoot> <incomingId>.", rest[1]),
      };
    case "create-fragment": {
      const fragmentProjectRoot = requireCliValue(
        "create-fragment requires <projectRoot> <incomingId> <body> [title].",
        rest[0],
      );
      const fragmentIncomingId = requireCliValue(
        "create-fragment requires <projectRoot> <incomingId> <body> [title].",
        rest[1],
      );
      const fragmentBody = requireCliValue(
        "create-fragment requires <projectRoot> <incomingId> <body> [title].",
        rest[2],
      );
      const fragmentTitle = rest[3]?.trim() ? rest[3] : undefined;
      return {
        name: "create-fragment",
        projectRoot: fragmentProjectRoot,
        incomingId: fragmentIncomingId,
        body: fragmentBody,
        ...(fragmentTitle !== undefined ? { title: fragmentTitle } : {}),
      };
    }
    case "insert":
      return {
        name: "insert",
        projectRoot: requireCliValue("insert requires <projectRoot> <fragmentId> <targetChapterPath>.", rest[0]),
        fragmentId: requireCliValue("insert requires <projectRoot> <fragmentId> <targetChapterPath>.", rest[1]),
        targetChapterPath: requireCliValue(
          "insert requires <projectRoot> <fragmentId> <targetChapterPath>.",
          rest[2],
        ),
      };
    case "update-incoming":
      return parseUpdateIncomingCommand(rest);
    case "update-fragment":
      return parseUpdateFragmentCommand(rest);
    case "update-insertion":
      return parseUpdateInsertionCommand(rest);
    case "archive-fragment":
      return {
        name: "archive-fragment",
        projectRoot: requireCliValue("archive-fragment requires <projectRoot> <fragmentId>.", rest[0]),
        fragmentId: requireCliValue("archive-fragment requires <projectRoot> <fragmentId>.", rest[1]),
      };
    case "archive-incoming":
      return {
        name: "archive-incoming",
        projectRoot: requireCliValue("archive-incoming requires <projectRoot> <incomingId>.", rest[0]),
        incomingId: requireCliValue("archive-incoming requires <projectRoot> <incomingId>.", rest[1]),
      };
    case "add-concept": {
      const conceptProjectRoot = requireCliValue(
        "add-concept requires <projectRoot> <label> [--note <note>].",
        rest[0],
      );
      const conceptLabel = requireCliValue(
        "add-concept requires <projectRoot> <label> [--note <note>].",
        rest[1],
      );
      const conceptNote = readFlagValue(rest.slice(2), "--note");
      return {
        name: "add-concept",
        projectRoot: conceptProjectRoot,
        label: conceptLabel,
        ...(conceptNote !== undefined ? { note: conceptNote } : {}),
      };
    }
    case "walk": {
      const walkProjectRoot = requireCliValue(
        "walk requires <projectRoot> <title> <body> <fragmentBody> <targetChapterPath>.",
        rest[0],
      );
      const walkTitle = requireCliValue(
        "walk requires <projectRoot> <title> <body> <fragmentBody> <targetChapterPath>.",
        rest[1],
      );
      const walkBody = requireCliValue(
        "walk requires <projectRoot> <title> <body> <fragmentBody> <targetChapterPath>.",
        rest[2],
      );
      const walkFragmentBody = requireCliValue(
        "walk requires <projectRoot> <title> <body> <fragmentBody> <targetChapterPath>.",
        rest[3],
      );
      const walkTarget = requireCliValue(
        "walk requires <projectRoot> <title> <body> <fragmentBody> <targetChapterPath>.",
        rest[4],
      );
      return {
        name: "walk",
        projectRoot: walkProjectRoot,
        title: walkTitle,
        body: walkBody,
        fragmentBody: walkFragmentBody,
        targetChapterPath: walkTarget,
      };
    }
    default:
      throw new Error(
        "Unknown command: " +
          commandName +
          ". Expected one of: capture, help, show, verify, start-processing, create-fragment, insert, bulk-insert, update-incoming, update-fragment, update-insertion, archive-fragment, archive-incoming, add-concept, walk.",
      );
  }
}

export async function runAtmaCliCommand(command: AtmaCliCommand): Promise<string> {
  switch (command.name) {
    case "help":
      return renderHelp();
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
    case "start-processing": {
      const result = await mutateManifestFile(command.projectRoot, (manifest) =>
        startProcessingIncoming(manifest, command.incomingId),
      );
      return renderEntityLine("STARTED", result.value.id, result.value.status);
    }
    case "create-fragment": {
      const created = await mutateManifestFile(command.projectRoot, (manifest) =>
        createFragmentFromIncoming(manifest, command.incomingId, command.body, {
          ...(command.title !== undefined ? { title: command.title } : {}),
        }),
      );
      return renderEntityLine("FRAGMENT", created.value.id, created.value.status);
    }
    case "insert": {
      const inserted = await mutateManifestFile(command.projectRoot, (manifest) =>
        insertFragmentIntoChapter(manifest, command.fragmentId, command.targetChapterPath),
      );
      return renderInsertionLine(inserted.value);
    }
    case "bulk-insert": {
      const inserted = await mutateManifestFile(command.projectRoot, (manifest) =>
        bulkInsert(manifest, command.pairs),
      );
      return inserted.value.map((one) => renderInsertionLine(one)).join("\n");
    }
    case "update-incoming": {
      const updated = await mutateManifestFile(command.projectRoot, (manifest) =>
        updateIncomingText(manifest, command.incomingId, {
          ...(command.title !== undefined ? { title: command.title } : {}),
          ...(command.note !== undefined ? { note: command.note } : {}),
        }),
      );
      return renderIncomingLine(updated.value);
    }
    case "update-fragment": {
      const updated = await mutateManifestFile(command.projectRoot, (manifest) =>
        updateFragment(manifest, command.fragmentId, {
          ...(command.text !== undefined ? { text: command.text } : {}),
          ...(command.title !== undefined ? { title: command.title } : {}),
          ...(command.note !== undefined ? { note: command.note } : {}),
        }),
      );
      return renderFragmentLine(updated.value);
    }
    case "update-insertion": {
      const updated = await mutateManifestFile(command.projectRoot, (manifest) =>
        updateInsertion(manifest, command.insertionId, {
          ...(command.targetChapterPath !== undefined
            ? { targetChapterPath: command.targetChapterPath }
            : {}),
          ...(command.positionNote !== undefined ? { positionNote: command.positionNote } : {}),
          ...(command.note !== undefined ? { note: command.note } : {}),
        }),
      );
      return renderInsertionLine(updated.value);
    }
    case "archive-fragment": {
      const archived = await mutateManifestFile(command.projectRoot, (manifest) =>
        archiveFragment(manifest, command.fragmentId),
      );
      return renderEntityLine("ARCHIVED", archived.value.id, archived.value.status);
    }
    case "archive-incoming": {
      const archived = await mutateManifestFile(command.projectRoot, (manifest) =>
        archiveIncoming(manifest, command.incomingId),
      );
      return renderEntityLine("ARCHIVED", archived.value.id, archived.value.status);
    }
    case "add-concept": {
      const added = await mutateManifestFile(command.projectRoot, (manifest) =>
        addConcept(manifest, {
          label: command.label,
          ...(command.note !== undefined ? { note: command.note } : {}),
        }),
      );
      return ["CONCEPT: " + added.value.id, "LABEL: " + added.value.label].join("\n");
    }
    case "walk":
      return runWalkCommand(command);
  }
}

function parseUpdateIncomingCommand(argv: readonly string[]): AtmaCliCommand {
  const projectRoot = requireCliValue(
    "update-incoming requires <projectRoot> <incomingId> [--title <title>|--clear-title] [--note <note>|--clear-note].",
    argv[0],
  );
  const incomingId = requireCliValue(
    "update-incoming requires <projectRoot> <incomingId> [--title <title>|--clear-title] [--note <note>|--clear-note].",
    argv[1],
  );
  const flags = argv.slice(2);
  const title = readNullableFlag(flags, "--title", "--clear-title");
  const note = readNullableFlag(flags, "--note", "--clear-note");
  assertNoUnknownFlags(flags, ["--title", "--clear-title", "--note", "--clear-note"]);

  if (title === undefined && note === undefined) {
    throw new Error("update-incoming requires at least one of --title or --note.");
  }

  return {
    name: "update-incoming",
    projectRoot,
    incomingId,
    ...(title !== undefined ? { title } : {}),
    ...(note !== undefined ? { note } : {}),
  };
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

function parseUpdateFragmentCommand(argv: readonly string[]): AtmaCliCommand {
  const projectRoot = requireCliValue("update-fragment requires ids and flags.", argv[0]);
  const fragmentId = requireCliValue("update-fragment requires ids and flags.", argv[1]);
  const flags = argv.slice(2);
  const text = readFlagValue(flags, "--text");
  const title = readNullableFlag(flags, "--title", "--clear-title");
  const note = readNullableFlag(flags, "--note", "--clear-note");
  assertNoUnknownFlags(flags, ["--text", "--title", "--clear-title", "--note", "--clear-note"]);
  if (text === undefined && title === undefined && note === undefined) {
    throw new Error("update-fragment requires at least one of --text, --title or --note.");
  }
  return {
    name: "update-fragment",
    projectRoot,
    fragmentId,
    ...(text !== undefined ? { text } : {}),
    ...(title !== undefined ? { title } : {}),
    ...(note !== undefined ? { note } : {}),
  };
}

function parseUpdateInsertionCommand(argv: readonly string[]): AtmaCliCommand {
  const projectRoot = requireCliValue("update-insertion requires ids and flags.", argv[0]);
  const insertionId = requireCliValue("update-insertion requires ids and flags.", argv[1]);
  const flags = argv.slice(2);
  const targetChapterPath = readFlagValue(flags, "--target");
  const positionNote = readNullableFlag(flags, "--position-note", "--clear-position-note");
  const note = readNullableFlag(flags, "--note", "--clear-note");
  assertNoUnknownFlags(flags, ["--target", "--position-note", "--clear-position-note", "--note", "--clear-note"]);
  if (targetChapterPath === undefined && positionNote === undefined && note === undefined) {
    throw new Error("update-insertion requires at least one of --target, --position-note or --note.");
  }
  return {
    name: "update-insertion",
    projectRoot,
    insertionId,
    ...(targetChapterPath !== undefined ? { targetChapterPath } : {}),
    ...(positionNote !== undefined ? { positionNote } : {}),
    ...(note !== undefined ? { note } : {}),
  };
}

function readFlagValue(flags: readonly string[], name: string): string | undefined {
  for (let index = 0; index < flags.length; index += 1) {
    if (flags[index] === name) {
      const value = flags[index + 1];
      if (value === undefined || value.trim().length === 0) {
        throw new Error(name + " requires a non-empty value.");
      }
      return value;
    }
  }
  return undefined;
}

function readNullableFlag(flags: readonly string[], name: string, clearName: string): string | null | undefined {
  const value = readFlagValue(flags, name);
  const cleared = flags.includes(clearName);
  if (value !== undefined && cleared) {
    throw new Error(name + " and " + clearName + " cannot be used together.");
  }
  if (value !== undefined) {
    return value;
  }
  if (cleared) {
    return null;
  }
  return undefined;
}

function assertNoUnknownFlags(flags: readonly string[], known: readonly string[]): void {
  for (let index = 0; index < flags.length; index += 1) {
    const flag = flags[index];
    if (flag === undefined || !flag.startsWith("--")) {
      continue;
    }
    if (!known.includes(flag)) {
      throw new Error("Unknown flag: " + flag + ". Expected one of: " + known.join(", ") + ".");
    }
    if (readFlagValue(flags.slice(index), flag) !== undefined) {
      index += 1;
    }
  }
}

function renderEntityLine(kind: string, id: string, status: string): string {
  return kind + ": " + id + "\nSTATUS: " + status;
}

function renderIncomingLine(value: IncomingText): string {
  return "INCOMING: " + value.id + "\nSTATUS: " + value.status + "\nSOURCE: " + value.sourcePath + "\nTITLE: " + (value.title ?? "<none>") + "\nNOTE: " + (value.note ?? "<none>");
}

function renderFragmentLine(value: Fragment): string {
  return "FRAGMENT: " + value.id + "\nSTATUS: " + value.status + "\nFROM: " + value.incomingTextId + "\nTITLE: " + (value.title ?? "<none>") + "\nTEXT: " + value.text;
}

function renderInsertionLine(value: Insertion): string {
  return "INSERTION: " + value.id + "\nFRAGMENT: " + value.fragmentId + "\nTARGET: " + value.targetChapterPath + "\nPOSITION: " + (value.positionNote ?? "<none>");
}

async function runWalkCommand(command: { projectRoot: string; title: string; body: string; fragmentBody: string; targetChapterPath: string }): Promise<string> {
  const lines: string[] = [];
  const consequence = await runCaptureIncomingTextProof({ projectRoot: command.projectRoot, title: command.title, body: command.body });
  lines.push(consequence);
  const manifest = await readManifestFromFile(getManifestPath(command.projectRoot));
  const incoming = manifest.incomingTexts[manifest.incomingTexts.length - 1];
  if (incoming === undefined) {
    throw new Error("walk failed: no incoming text after capture.");
  }
  const started = await mutateManifestFile(command.projectRoot, (current) => startProcessingIncoming(current, incoming.id));
  lines.push(renderEntityLine("STARTED", started.value.id, started.value.status));
  const created = await mutateManifestFile(command.projectRoot, (current) => createFragmentFromIncoming(current, incoming.id, command.fragmentBody));
  lines.push(renderEntityLine("FRAGMENT", created.value.id, created.value.status));
  const inserted = await mutateManifestFile(command.projectRoot, (current) => insertFragmentIntoChapter(current, created.value.id, command.targetChapterPath));
  lines.push(renderInsertionLine(inserted.value));
  const verify = await runVerifyCommand(command.projectRoot);
  lines.push(verify);
  return lines.join("\n");
}
function renderHelp(): string {
  return [
    "ATMA — Book Workbench CLI (samostojno, brez streznika).",
    "",
    "capture <root> <title> <body>                        zajemi vhod",
    "start-processing <root> <incomingId>                  zacni obdelavo",
    "create-fragment <root> <incomingId> <body> [title]    ustvari odlomek",
    "insert <root> <fragmentId> <target>                   vstavi odlomek v poglavje",
    "bulk-insert <root> <fid=target> [...]                 atomsko vstavi vec odlomkov",
    "update-incoming <root> <id> [--title t|--clear-title] [--note n|--clear-note]",
    "update-fragment <root> <id> [--text t] [--title t|--clear-title] [--note n|--clear-note]",
    "update-insertion <root> <id> [--target p] [--position-note n|--clear-position-note] [--note n|--clear-note]",
    "archive-fragment <root> <fragmentId>                  arhiviraj odlomek",
    "archive-incoming <root> <incomingId>                  arhiviraj vhod",
    "add-concept <root> <label> [--note n]                 dodaj pojem",
    "walk <root> <title> <body> <fragBody> <target>        cela pot v enem dihu",
    "show <root>                                          povzetek manifesta",
    "verify <root>                                        VERIFY: PASS / FAIL",
    "help                                                 ta pomoc",
    "",
    "Primer: atma walk <tmp> \"Naslov\" \"Vsebina.\" \"Odlomek.\" \"poglavja/uvod.md\"",
  ].join("\n");
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
  // V bundlu (ATMA_BUNDLE=1 prek esbuild --define) import.meta.url kaze na
  // zdruseni bundel, ne na izvorni atmaCli.ts — primerjava z process.argv[1]
  // je zato lazno resnicna ob vsakem uvozu. Meja: v bundlu se main zbudi le,
  // ce je vstopna tocka res bundel sam (neposredni `node atma-bundle.mjs ...`).
  if (typeof process !== "undefined" && (process.env as Record<string, string>)["ATMA_BUNDLE"] === "1") {
    const entryPath = process.argv[1];
    if (entryPath === undefined) {
      return false;
    }
    const bundelIme = "atma-bundle.mjs";
    return entryPath.endsWith(bundelIme) || entryPath.endsWith(bundelIme.replace(/\//g, "\\"));
  }

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
