import assert from "node:assert/strict";
import test from "node:test";

import {
  addIncomingText,
  archiveFragment,
  archiveIncoming,
  createEmptyManifest,
  createFragmentFromIncoming,
  insertFragmentIntoChapter,
  startProcessingIncoming,
  validateManifest,
  type WorkbenchManifest,
} from "./workbenchManifest.js";

test("createEmptyManifest returns a valid empty manifest", () => {
  const manifest = createEmptyManifest("Draft Book");

  assert.equal(manifest.manifestVersion, "1");
  assert.deepEqual(manifest.incomingTexts, []);
  assert.deepEqual(manifest.fragments, []);
  assert.deepEqual(manifest.insertions, []);
  assert.equal(validateManifest(manifest).isValid, true);
});

test("addIncomingText adds a new incoming text without mutating input", () => {
  const manifest = createEmptyManifest();

  const result = addIncomingText(manifest, {
    title: "Seed text",
    body: "Prvi vhodni tekst.",
  });

  assert.equal(manifest.incomingTexts.length, 0);
  assert.equal(result.manifest.incomingTexts.length, 1);
  assert.equal(result.value.id, "incoming-0001");
  assert.equal(result.value.status, "new");
  assert.equal(result.value.sourcePath, "incoming/incoming-0001.txt");
  assert.equal(result.value.title, "Seed text");
});

test("startProcessingIncoming promotes incoming text from new to processing", () => {
  const manifest = addIncomingText(createEmptyManifest(), {
    title: "Seed text",
    body: "Prvi vhodni tekst.",
  }).manifest;

  const result = startProcessingIncoming(manifest, "incoming-0001");

  assert.equal(manifest.incomingTexts[0]?.status, "new");
  assert.equal(result.value.status, "processing");
  assert.equal(result.manifest.incomingTexts[0]?.status, "processing");
});

test("createFragmentFromIncoming creates a draft fragment from processing incoming text", () => {
  const manifest = startProcessingIncoming(
    addIncomingText(createEmptyManifest(), {
      title: "Seed text",
      body: "Prvi vhodni tekst.",
    }).manifest,
    "incoming-0001",
  ).manifest;

  const result = createFragmentFromIncoming(manifest, "incoming-0001", "Izlocen odlomek.");

  assert.equal(manifest.fragments.length, 0);
  assert.equal(result.manifest.fragments.length, 1);
  assert.equal(result.value.id, "fragment-0001");
  assert.equal(result.value.incomingTextId, "incoming-0001");
  assert.equal(result.value.status, "draft");
});

test("insertFragmentIntoChapter creates insertion and marks fragment as inserted", () => {
  const processingManifest = createFragmentFromIncoming(
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

  const result = insertFragmentIntoChapter(
    processingManifest,
    "fragment-0001",
    "book/01-uvod.md",
  );

  assert.equal(result.value.id, "insertion-0001");
  assert.equal(result.value.targetChapterPath, "book/01-uvod.md");
  assert.equal(result.manifest.fragments[0]?.status, "inserted");
  assert.equal(result.manifest.incomingTexts[0]?.status, "used");
  assert.equal(validateManifest(result.manifest).isValid, true);
});

test("insertFragmentIntoChapter rejects blank targetChapterPath", () => {
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

  assert.throws(
    () => insertFragmentIntoChapter(manifest, "fragment-0001", "   "),
    /targetChapterPath must be a non-empty string/,
  );
});

test("archiveIncoming archives incoming text from active state", () => {
  const manifest = addIncomingText(createEmptyManifest(), {
    title: "Seed text",
    body: "Prvi vhodni tekst.",
  }).manifest;

  const result = archiveIncoming(manifest, "incoming-0001");

  assert.equal(result.value.status, "archived");
  assert.equal(result.manifest.incomingTexts[0]?.status, "archived");
});

test("archiveFragment preserves insertion trail while archiving fragment", () => {
  const manifest = insertFragmentIntoChapter(
    createFragmentFromIncoming(
      startProcessingIncoming(
        addIncomingText(createEmptyManifest(), {
          title: "Seed text",
          body: "Prvi vhodni tekst.",
        }).manifest,
        "incoming-0001",
      ).manifest,
      "incoming-0001",
      "Izlocen odlomek.",
    ).manifest,
    "fragment-0001",
    "book/01-uvod.md",
  ).manifest;

  const result = archiveFragment(manifest, "fragment-0001");

  assert.equal(result.value.status, "archived");
  assert.equal(result.manifest.insertions.length, 1);
  assert.equal(validateManifest(result.manifest).isValid, true);
});

test("validateManifest reports broken fragment relation", () => {
  const manifest: WorkbenchManifest = {
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

  const result = validateManifest(manifest);

  assert.equal(result.isValid, false);
  assert.equal(
    result.errors.some((error) => error.includes("references missing IncomingText incoming-missing")),
    true,
  );
});
