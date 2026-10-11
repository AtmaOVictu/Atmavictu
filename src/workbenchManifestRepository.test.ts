import assert from "node:assert/strict";
import { mkdtemp, readFile, readdir, rm, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import test from "node:test";

import {
  type AddIncomingTextInput,
  addIncomingText,
  createEmptyManifest,
  createFragmentFromIncoming,
  startProcessingIncoming,
  type WorkbenchManifest,
} from "./workbenchManifest.js";
import {
  captureIncomingText,
  createCaptureIncomingTextConsequence,
  MANIFEST_FILE_NAME,
  ManifestRepositoryError,
  ensureManifestFile,
  getManifestPath,
  readManifestFromFile,
  writeManifestToFile,
} from "./workbenchManifestRepository.js";

test("getManifestPath returns book.workbench.json inside project root", () => {
  const manifestPath = getManifestPath("project/root");

  assert.equal(manifestPath, join("project/root", MANIFEST_FILE_NAME));
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

test("captureIncomingText persists body file and manifest trail", async () => {
  const projectRoot = await createTempDirectory();
  const input: AddIncomingTextInput = {
    title: "Seed text",
    body: "Prvi vhodni tekst.",
  };

  try {
    const result = await captureIncomingText(projectRoot, input);
    const manifestPath = getManifestPath(projectRoot);
    const bodyFilePath = join(projectRoot, result.value.sourcePath);
    const rawManifest = JSON.parse(await readFile(manifestPath, "utf8")) as WorkbenchManifest;
    const restoredManifest = await readManifestFromFile(manifestPath);
    const bodyContent = await readFile(bodyFilePath, "utf8");

    assert.equal(result.value.id, "incoming-0001");
    assert.equal(result.value.sourcePath, "incoming/incoming-0001.txt");
    assert.equal(bodyContent, input.body);
    assert.equal(rawManifest.incomingTexts[0]?.sourcePath, "incoming/incoming-0001.txt");
    assert.equal("body" in (rawManifest.incomingTexts[0] as unknown as Record<string, unknown>), false);
    assert.deepEqual(restoredManifest, result.manifest);
  } finally {
    await cleanupTempDirectory(projectRoot);
  }
});

test("capture consequence summary exposes sourcePath without leaking body", async () => {
  const projectRoot = await createTempDirectory();
  const input: AddIncomingTextInput = {
    title: "Seed text",
    body: "Prvi vhodni tekst.",
  };

  try {
    const result = await captureIncomingText(projectRoot, input);
    const consequence = createCaptureIncomingTextConsequence(result);

    assert.equal(consequence.title, "POSLEDICA");
    assert.equal(consequence.lastAction, "ZAJEMI VNOS");
    assert.equal(consequence.createdPath, "incoming/incoming-0001.txt");
    assert.equal(consequence.manifestTrail.sourcePath, "incoming/incoming-0001.txt");
    assert.equal(consequence.currentState, "CAPTURED");
    assert.equal(consequence.nextAction, "RAZREZI");
    assert.equal(consequence.proofBoundary, "Fragment se ni ustvarjen.");
    assert.equal("body" in consequence.manifestTrail, false);
  } finally {
    await cleanupTempDirectory(projectRoot);
  }
});

test("captureIncomingText rejects blank body and does not create manifest", async () => {
  const projectRoot = await createTempDirectory();

  try {
    await assert.rejects(
      () => captureIncomingText(projectRoot, { title: "Seed text", body: "   " }),
      /body must be a non-empty string/,
    );

    await assert.rejects(
      () => readFile(getManifestPath(projectRoot), "utf8"),
      (error: unknown) => error instanceof Error && "code" in error && error.code === "ENOENT",
    );
  } finally {
    await cleanupTempDirectory(projectRoot);
  }
});

test("captureIncomingText rejects unsafe sourcePath", async () => {
  const projectRoot = await createTempDirectory();

  try {
    await assert.rejects(
      () =>
        captureIncomingText(projectRoot, {
          title: "Seed text",
          body: "Prvi vhodni tekst.",
          sourcePath: "../outside.txt",
        }),
      /sourcePath cannot contain traversal segments/,
    );

    await assert.rejects(
      () => readFile(getManifestPath(projectRoot), "utf8"),
      (error: unknown) => error instanceof Error && "code" in error && error.code === "ENOENT",
    );
  } finally {
    await cleanupTempDirectory(projectRoot);
  }
});

test("captureIncomingText does not report success when body file write fails", async () => {
  const projectRoot = await createTempDirectory();

  try {
    await writeFile(join(projectRoot, "incoming"), "occupied", "utf8");

    await assert.rejects(
      () =>
        captureIncomingText(projectRoot, {
          title: "Seed text",
          body: "Prvi vhodni tekst.",
        }),
      (error: unknown) =>
        error instanceof ManifestRepositoryError &&
        error.code === "WRITE_FAILURE" &&
        error.message.includes("incoming-0001.txt"),
    );

    await assert.rejects(
      () => readFile(getManifestPath(projectRoot), "utf8"),
      (error: unknown) => error instanceof Error && "code" in error && error.code === "ENOENT",
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
