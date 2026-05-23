import { mkdir, readFile, rename, rm, writeFile } from "node:fs/promises";
import { basename, dirname, isAbsolute, join, relative, resolve } from "node:path";
import { randomUUID } from "node:crypto";

import {
  addIncomingText,
  createEmptyManifest,
  validateManifest,
  type AddIncomingTextInput,
  type IncomingText,
  type ManifestUpdate,
  type WorkbenchManifest,
} from "./workbenchManifest.js";

export const MANIFEST_FILE_NAME = "book.workbench.json";

export type ManifestRepositoryErrorCode =
  | "MISSING_FILE"
  | "INVALID_JSON"
  | "INVALID_MANIFEST"
  | "WRITE_FAILURE";

export interface CaptureIncomingTextConsequence {
  title: "POSLEDICA";
  lastAction: "ZAJEMI VNOS";
  createdPath: string;
  manifestTrail: {
    incomingTextId: string;
    sourcePath: string;
  };
  currentState: "CAPTURED";
  nextAction: "RAZREZI";
  proofBoundary: "Fragment se ni ustvarjen.";
}

export class ManifestRepositoryError extends Error {
  readonly code: ManifestRepositoryErrorCode;

  constructor(code: ManifestRepositoryErrorCode, message: string, options?: { cause?: unknown }) {
    super(message);
    this.name = "ManifestRepositoryError";
    this.code = code;

    if (options?.cause !== undefined) {
      Object.defineProperty(this, "cause", {
        configurable: true,
        enumerable: false,
        value: options.cause,
        writable: true,
      });
    }
  }
}

export function getManifestPath(projectRoot: string): string {
  return join(requireNonEmptyPath("projectRoot", projectRoot), MANIFEST_FILE_NAME);
}

export async function captureIncomingText(
  projectRoot: string,
  input: AddIncomingTextInput,
): Promise<ManifestUpdate<IncomingText>> {
  const normalizedProjectRoot = requireNonEmptyPath("projectRoot", projectRoot);
  const manifestPath = getManifestPath(normalizedProjectRoot);
  const manifest = await loadManifestForUpdate(normalizedProjectRoot);
  const result = addIncomingText(manifest, input);
  const bodyFilePath = resolveProjectFilePath(normalizedProjectRoot, result.value.sourcePath, "sourcePath");

  await writeTextFileAtomically(bodyFilePath, input.body, "incoming body file");

  try {
    await writeManifestToFile(manifestPath, result.manifest);
  } catch (error) {
    await rm(bodyFilePath, { force: true }).catch(() => undefined);
    throw error;
  }

  return result;
}

export function createCaptureIncomingTextConsequence(
  result: ManifestUpdate<IncomingText>,
): CaptureIncomingTextConsequence {
  return {
    title: "POSLEDICA",
    lastAction: "ZAJEMI VNOS",
    createdPath: result.value.sourcePath,
    manifestTrail: {
      incomingTextId: result.value.id,
      sourcePath: result.value.sourcePath,
    },
    currentState: "CAPTURED",
    nextAction: "RAZREZI",
    proofBoundary: "Fragment se ni ustvarjen.",
  };
}

export function renderCaptureIncomingTextConsequence(
  consequence: CaptureIncomingTextConsequence,
): string {
  return [
    consequence.title,
    `ZADNJE DEJANJE: ${consequence.lastAction}`,
    `USTVARJENO: ${consequence.createdPath}`,
    `MANIFEST SLED: ${consequence.manifestTrail.sourcePath}`,
    `TRENUTNO STANJE: ${consequence.currentState}`,
    `NASLEDNJI KORAK: ${consequence.nextAction}`,
    `DOKAZNA MEJA: ${consequence.proofBoundary}`,
  ].join("\n");
}

export async function readManifestFromFile(filePath: string): Promise<WorkbenchManifest> {
  const normalizedFilePath = requireNonEmptyPath("filePath", filePath);

  let rawContent: string;
  try {
    rawContent = await readFile(normalizedFilePath, "utf8");
  } catch (error) {
    if (isNodeError(error) && error.code === "ENOENT") {
      throw new ManifestRepositoryError(
        "MISSING_FILE",
        `Manifest file does not exist: ${normalizedFilePath}`,
        { cause: error },
      );
    }

    throw new ManifestRepositoryError(
      "INVALID_JSON",
      `Failed to read manifest file: ${normalizedFilePath}`,
      { cause: error },
    );
  }

  let parsedManifest: unknown;
  try {
    parsedManifest = JSON.parse(rawContent) as unknown;
  } catch (error) {
    throw new ManifestRepositoryError(
      "INVALID_JSON",
      `Manifest file contains invalid JSON: ${normalizedFilePath}`,
      { cause: error },
    );
  }

  return parseAndValidateManifest(parsedManifest, normalizedFilePath);
}

export async function writeManifestToFile(
  filePath: string,
  manifest: WorkbenchManifest,
): Promise<void> {
  const normalizedFilePath = requireNonEmptyPath("filePath", filePath);
  assertManifestIsValid(manifest, normalizedFilePath);
  const manifestJson = `${JSON.stringify(manifest, null, 2)}\n`;

  await writeTextFileAtomically(normalizedFilePath, manifestJson, "manifest file");
}

export async function ensureManifestFile(
  projectRoot: string,
  title?: string,
): Promise<WorkbenchManifest> {
  const manifestPath = getManifestPath(projectRoot);

  try {
    return await readManifestFromFile(manifestPath);
  } catch (error) {
    if (!(error instanceof ManifestRepositoryError) || error.code !== "MISSING_FILE") {
      throw error;
    }
  }

  const manifest = createEmptyManifest(title);
  await writeManifestToFile(manifestPath, manifest);
  return manifest;
}

function parseAndValidateManifest(parsedManifest: unknown, filePath: string): WorkbenchManifest {
  if (!isPlainObject(parsedManifest)) {
    throw new ManifestRepositoryError(
      "INVALID_MANIFEST",
      `Manifest JSON must parse to an object: ${filePath}`,
    );
  }

  const manifest = parsedManifest as unknown as WorkbenchManifest;
  assertManifestIsValid(manifest, filePath);
  return manifest;
}

function assertManifestIsValid(manifest: WorkbenchManifest, filePath: string): void {
  const validationResult = validateManifest(manifest);
  if (!validationResult.isValid) {
    throw new ManifestRepositoryError(
      "INVALID_MANIFEST",
      `Manifest validation failed for ${filePath}: ${validationResult.errors.join(" | ")}`,
    );
  }
}

async function loadManifestForUpdate(projectRoot: string): Promise<WorkbenchManifest> {
  const manifestPath = getManifestPath(projectRoot);

  try {
    return await readManifestFromFile(manifestPath);
  } catch (error) {
    if (!(error instanceof ManifestRepositoryError) || error.code !== "MISSING_FILE") {
      throw error;
    }
  }

  return createEmptyManifest();
}

function resolveProjectFilePath(projectRoot: string, relativeFilePath: string, name: string): string {
  const normalizedProjectRoot = resolve(requireNonEmptyPath("projectRoot", projectRoot));
  const normalizedRelativeFilePath = requireNonEmptyPath(name, relativeFilePath);

  if (isAbsolute(normalizedRelativeFilePath)) {
    throw new ManifestRepositoryError(
      "WRITE_FAILURE",
      `${name} must be a relative path inside projectRoot: ${normalizedRelativeFilePath}`,
    );
  }

  const resolvedFilePath = resolve(normalizedProjectRoot, normalizedRelativeFilePath);
  const relativeToRoot = relative(normalizedProjectRoot, resolvedFilePath);

  if (relativeToRoot.startsWith("..") || isAbsolute(relativeToRoot)) {
    throw new ManifestRepositoryError(
      "WRITE_FAILURE",
      `${name} must stay within projectRoot: ${normalizedRelativeFilePath}`,
    );
  }

  return resolvedFilePath;
}

async function writeTextFileAtomically(
  filePath: string,
  content: string,
  fileLabel: string,
): Promise<void> {
  const normalizedFilePath = requireNonEmptyPath("filePath", filePath);
  const parentDirectory = dirname(normalizedFilePath);
  const tempFilePath = join(parentDirectory, `${basename(normalizedFilePath)}.${randomUUID()}.tmp`);

  try {
    await mkdir(parentDirectory, { recursive: true });
    await writeFile(tempFilePath, content, "utf8");
    await rename(tempFilePath, normalizedFilePath);
  } catch (error) {
    await rm(tempFilePath, { force: true }).catch(() => undefined);
    throw new ManifestRepositoryError(
      "WRITE_FAILURE",
      `Failed to write ${fileLabel}: ${normalizedFilePath}`,
      { cause: error },
    );
  }
}

function requireNonEmptyPath(name: string, value: string): string {
  const normalizedValue = value.trim();
  if (normalizedValue.length === 0) {
    throw new Error(`${name} must be a non-empty string.`);
  }

  return normalizedValue;
}

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isNodeError(error: unknown): error is NodeJS.ErrnoException {
  return error instanceof Error;
}
