import assert from "node:assert/strict";
import { mkdtemp, readFile, readdir, rm, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import test from "node:test";

import {
  addIncomingText,
  createEmptyManifest,
  createFragmentFromIncoming,
  startProcessingIncoming,
  type WorkbenchManifest,
} from "./workbenchManifest.js";
import {
  MANIFEST_FILE_NAME,
  ManifestRepositoryError,
  ensureManifestFile,
  getManifestPath,
  readManifestFromFile,
  writeManifestToFile,
} from "./workbenchManifestRepository.js";

test("getManifestPath returns book.workbench.json inside project root", () => {
  const manifestPath = getManifestPath("C:/temp/project");

  assert.equal(manifestPath, "C:\\temp\\project\\book.workbench.json");
});

test("ensureManifestFile creates a new manifest when file is missing", async () => {
  const projectRoot = await createTempDirectory();

  try {
    const manifest = await ensureManifestFile(projectRoot, "Book Draft");
    const manifestPath = getManifestPath(projectRoot);
    const persistedManifest = JSON.parse(await readFile(manifestPath, "utf8")) as WorkbenchManifest;

    assert.equal(manifest.manifestVersion, "1");
    assert.deepEqual(manifest.incomingTexts, []);
    assert.deepEqual(manifest.fragments, []);
    assert.deepEqual(manifest.insertions, []);
    assert.deepEqual(persistedManifest, manifest);
  } finally {
    await cleanupTempDirectory(projectRoot);
  }
});

test("writeManifestToFile and readManifestFromFile support roundtrip", async () => {
  const projectRoot = await createTempDirectory();

  try {
    const manifestPath = getManifestPath(projectRoot);
    const manifest = createFragmentFromIncoming(
      startProcessingIncoming(
        addIncomingText(createEmptyManifest(), {
          title: "Seed text",
          body: "Prvi vhodni tekst.",
        }).manifest,
        "incoming-0001",
      ).manifest,
      "incoming-0001",
      "Izlocen odlomek.",
    ).manifest;

    await writeManifestToFile(manifestPath, manifest);
    const restoredManifest = await readManifestFromFile(manifestPath);

    assert.deepEqual(restoredManifest, manifest);
  } finally {
    await cleanupTempDirectory(projectRoot);
  }
});

test("readManifestFromFile rejects invalid JSON", async () => {
  const projectRoot = await createTempDirectory();

  try {
    const manifestPath = getManifestPath(projectRoot);
    await writeFile(manifestPath, "{ invalid json", "utf8");

    await assert.rejects(
      () => readManifestFromFile(manifestPath),
      (error: unknown) =>
        error instanceof ManifestRepositoryError &&
        error.code === "INVALID_JSON" &&
        error.message.includes("invalid JSON"),
    );
  } finally {
    await cleanupTempDirectory(projectRoot);
  }
});

test("readManifestFromFile rejects manifest with broken relation", async () => {
  const projectRoot = await createTempDirectory();

  try {
    const manifestPath = getManifestPath(projectRoot);
    const brokenManifest: WorkbenchManifest = {
      manifestVersion: "1",
      incomingTexts: [],
      fragments: [
        {
          id: "fragment-0001",
          incomingTextId: "incoming-missing",
          text: "Odlomek",
          status: "draft",
        },
      ],
      insertions: [],
      concepts: [],
    };

    await writeFile(manifestPath, `${JSON.stringify(brokenManifest, null, 2)}\n`, "utf8");

    await assert.rejects(
      () => readManifestFromFile(manifestPath),
      (error: unknown) =>
        error instanceof ManifestRepositoryError &&
        error.code === "INVALID_MANIFEST" &&
        error.message.includes("references missing IncomingText"),
    );
  } finally {
    await cleanupTempDirectory(projectRoot);
  }
});

test("writeManifestToFile rejects invalid manifest before write", async () => {
  const projectRoot = await createTempDirectory();

  try {
    const manifestPath = getManifestPath(projectRoot);
    const invalidManifest = {
      manifestVersion: "1",
      incomingTexts: [],
      fragments: [],
      insertions: [
        {
          id: "insertion-0001",
          fragmentId: "fragment-missing",
          targetChapterPath: "book/01-uvod.md",
        },
      ],
      concepts: [],
    } as WorkbenchManifest;

    await assert.rejects(
      () => writeManifestToFile(manifestPath, invalidManifest),
      (error: unknown) =>
        error instanceof ManifestRepositoryError &&
        error.code === "INVALID_MANIFEST" &&
        error.message.includes("references missing Fragment"),
    );

    await assert.rejects(
      () => readFile(manifestPath, "utf8"),
      (error: unknown) => error instanceof Error && "code" in error && error.code === "ENOENT",
    );
  } finally {
    await cleanupTempDirectory(projectRoot);
  }
});

test("atomic write creates final file with valid JSON and no temp file residue", async () => {
  const projectRoot = await createTempDirectory();

  try {
    const manifestPath = getManifestPath(projectRoot);
    const manifest = addIncomingText(createEmptyManifest(), {
      title: "Seed text",
      body: "Prvi vhodni tekst.",
    }).manifest;

    await writeManifestToFile(manifestPath, manifest);

    const rawManifest = await readFile(manifestPath, "utf8");
    const parsedManifest = JSON.parse(rawManifest) as WorkbenchManifest;
    const directoryEntries = await readdir(projectRoot);

    assert.deepEqual(parsedManifest, manifest);
    assert.equal(directoryEntries.includes(MANIFEST_FILE_NAME), true);
    assert.equal(
      directoryEntries.some(
        (entry) => entry.startsWith(`${MANIFEST_FILE_NAME}.`) && entry.endsWith(".tmp"),
      ),
      false,
    );
  } finally {
    await cleanupTempDirectory(projectRoot);
  }
});

async function createTempDirectory(): Promise<string> {
  return mkdtemp(join(tmpdir(), "atmavictu-manifest-"));
}

async function cleanupTempDirectory(projectRoot: string): Promise<void> {
  await rm(projectRoot, { force: true, recursive: true });
}
