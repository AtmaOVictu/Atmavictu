import assert from "node:assert/strict";
import test from "node:test";

import {
  addConcept,
  addIncomingText,
  archiveFragment,
  archiveIncoming,
  createEmptyManifest,
  createFragmentFromIncoming,
  insertFragmentIntoChapter,
  startProcessingIncoming,
  updateFragment,
  updateIncomingText,
  updateInsertion,
  migrateManifestV1ToV2,
  validateManifest,
  type WorkbenchManifest,
  type WorkbenchManifestV1,
} from "./workbenchManifest.js";

test("createEmptyManifest returns a valid empty manifest", () => {
  const manifest = createEmptyManifest("Draft Book");

  assert.equal(manifest.manifestVersion, "2");
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
    manifestVersion: "2",
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

test("validateManifest rejects unexpected top-level properties", () => {
  const manifest = {
    manifestVersion: "2",
    incomingTexts: [],
    fragments: [],
    insertions: [],
    rogue: true,
  } as unknown as WorkbenchManifest;

  const result = validateManifest(manifest);

  assert.equal(result.isValid, false);
  assert.equal(result.errors.some((error) => error.includes("Unexpected WorkbenchManifest property: rogue")), true);
});

test("validateManifest rejects unexpected properties on incoming texts", () => {
  const manifest = {
    manifestVersion: "2",
    incomingTexts: [
      {
        id: "incoming-0001",
        sourcePath: "incoming/incoming-0001.txt",
        status: "new",
        rogue: true,
      },
    ],
    fragments: [],
    insertions: [],
  } as unknown as WorkbenchManifest;

  const result = validateManifest(manifest);

  assert.equal(result.isValid, false);
  assert.equal(
    result.errors.some((error) => error.includes("IncomingText incoming-0001 has unexpected property rogue")),
    true,
  );
});

test("validateManifest rejects unexpected properties on fragments and insertions", () => {
  const manifest = {
    manifestVersion: "2",
    incomingTexts: [
      {
        id: "incoming-0001",
        sourcePath: "incoming/incoming-0001.txt",
        status: "used",
      },
    ],
    fragments: [
      {
        id: "fragment-0001",
        incomingTextId: "incoming-0001",
        text: "Odlomek",
        status: "inserted",
        rogue: true,
      },
    ],
    insertions: [
      {
        id: "insertion-0001",
        fragmentId: "fragment-0001",
        targetChapterPath: "book/01-uvod.md",
        rogue: true,
      },
    ],
  } as unknown as WorkbenchManifest;

  const result = validateManifest(manifest);

  assert.equal(result.isValid, false);
  assert.equal(
    result.errors.some((error) => error.includes("Fragment fragment-0001 has unexpected property rogue")),
    true,
  );
  assert.equal(
    result.errors.some((error) => error.includes("Insertion insertion-0001 has unexpected property rogue")),
    true,
  );
});

test("validateManifest rejects invalid optional string property types", () => {
  const manifest = {
    manifestVersion: "2",
    incomingTexts: [
      {
        id: "incoming-0001",
        sourcePath: "incoming/incoming-0001.txt",
        status: "used",
        title: 123,
      },
    ],
    fragments: [
      {
        id: "fragment-0001",
        incomingTextId: "incoming-0001",
        text: "Odlomek",
        status: "inserted",
        note: 456,
      },
    ],
    insertions: [
      {
        id: "insertion-0001",
        fragmentId: "fragment-0001",
        targetChapterPath: "book/01-uvod.md",
        positionNote: 789,
      },
    ],
  } as unknown as WorkbenchManifest;

  const result = validateManifest(manifest);

  assert.equal(result.isValid, false);
  assert.equal(
    result.errors.some((error) => error.includes("IncomingText incoming-0001 title must be a string when present")),
    true,
  );
  assert.equal(
    result.errors.some((error) => error.includes("Fragment fragment-0001 note must be a string when present")),
    true,
  );
  assert.equal(
    result.errors.some((error) => error.includes("Insertion insertion-0001 positionNote must be a string when present")),
    true,
  );
});

test("validateManifest rejects new incoming text with related fragments", () => {
  const manifest: WorkbenchManifest = {
    manifestVersion: "2",
    incomingTexts: [
      {
        id: "incoming-0001",
        sourcePath: "incoming/incoming-0001.txt",
        status: "new",
      },
    ],
    fragments: [
      {
        id: "fragment-0001",
        incomingTextId: "incoming-0001",
        text: "Odlomek",
        status: "draft",
      },
    ],
    insertions: [],
  };

  const result = validateManifest(manifest);

  assert.equal(result.isValid, false);
  assert.equal(
    result.errors.some((error) => error.includes("IncomingText incoming-0001 with status new cannot have related fragments")),
    true,
  );
});

test("validateManifest rejects used incoming text without insertion trail", () => {
  const manifest: WorkbenchManifest = {
    manifestVersion: "2",
    incomingTexts: [
      {
        id: "incoming-0001",
        sourcePath: "incoming/incoming-0001.txt",
        status: "used",
      },
    ],
    fragments: [
      {
        id: "fragment-0001",
        incomingTextId: "incoming-0001",
        text: "Odlomek",
        status: "draft",
      },
    ],
    insertions: [],
  };

  const result = validateManifest(manifest);

  assert.equal(result.isValid, false);
  assert.equal(
    result.errors.some((error) => error.includes("IncomingText incoming-0001 with status used must have an insertion trail")),
    true,
  );
});

test("validateManifest rejects archived incoming text with draft fragments", () => {
  const manifest: WorkbenchManifest = {
    manifestVersion: "2",
    incomingTexts: [
      {
        id: "incoming-0001",
        sourcePath: "incoming/incoming-0001.txt",
        status: "archived",
      },
    ],
    fragments: [
      {
        id: "fragment-0001",
        incomingTextId: "incoming-0001",
        text: "Odlomek",
        status: "draft",
      },
    ],
    insertions: [],
  };

  const result = validateManifest(manifest);

  assert.equal(result.isValid, false);
  assert.equal(
    result.errors.some(
      (error) => error.includes("IncomingText incoming-0001 with status archived cannot have draft fragments"),
    ),
    true,
  );
});

test("validateManifest rejects traversal segments in sourcePath and targetChapterPath", () => {
  const manifest: WorkbenchManifest = {
    manifestVersion: "2",
    incomingTexts: [
      {
        id: "incoming-0001",
        sourcePath: "../incoming/incoming-0001.txt",
        status: "used",
      },
    ],
    fragments: [
      {
        id: "fragment-0001",
        incomingTextId: "incoming-0001",
        text: "Odlomek",
        status: "inserted",
      },
    ],
    insertions: [
      {
        id: "insertion-0001",
        fragmentId: "fragment-0001",
        targetChapterPath: "../book/01-uvod.md",
      },
    ],
  };

  const result = validateManifest(manifest);

  assert.equal(result.isValid, false);
  assert.equal(
    result.errors.some((error) => error.includes("IncomingText incoming-0001 sourcePath cannot contain traversal segments")),
    true,
  );
  assert.equal(
    result.errors.some(
      (error) => error.includes("Insertion insertion-0001 targetChapterPath cannot contain traversal segments"),
    ),
    true,
  );
});

test("validateManifest rejects absolute sourcePath variants", () => {
  const manifests: WorkbenchManifest[] = [
    {
      manifestVersion: "2",
      incomingTexts: [
        {
          id: "incoming-0001",
          sourcePath: "/tmp/file.txt",
          status: "new",
        },
      ],
      fragments: [],
      insertions: [],
    },
    {
      manifestVersion: "2",
      incomingTexts: [
        {
          id: "incoming-0001",
          sourcePath: "C:\\Users\\Luka\\secret.txt",
          status: "new",
        },
      ],
      fragments: [],
      insertions: [],
    },
    {
      manifestVersion: "2",
      incomingTexts: [
        {
          id: "incoming-0001",
          sourcePath: "C:/Users/Luka/secret.txt",
          status: "new",
        },
      ],
      fragments: [],
      insertions: [],
    },
    {
      manifestVersion: "2",
      incomingTexts: [
        {
          id: "incoming-0001",
          sourcePath: "\\\\server\\share\\file.txt",
          status: "new",
        },
      ],
      fragments: [],
      insertions: [],
    },
  ];

  for (const manifest of manifests) {
    const result = validateManifest(manifest);

    assert.equal(result.isValid, false);
    assert.equal(
      result.errors.some((error) => error.includes("sourcePath must be a relative path")),
      true,
    );
  }
});

test("validateManifest rejects absolute targetChapterPath variants", () => {
  const manifests: WorkbenchManifest[] = [
    {
      manifestVersion: "2",
      incomingTexts: [
        {
          id: "incoming-0001",
          sourcePath: "incoming/incoming-0001.txt",
          status: "used",
        },
      ],
      fragments: [
        {
          id: "fragment-0001",
          incomingTextId: "incoming-0001",
          text: "Odlomek",
          status: "inserted",
        },
      ],
      insertions: [
        {
          id: "insertion-0001",
          fragmentId: "fragment-0001",
          targetChapterPath: "/tmp/chapter.md",
        },
      ],
    },
    {
      manifestVersion: "2",
      incomingTexts: [
        {
          id: "incoming-0001",
          sourcePath: "incoming/incoming-0001.txt",
          status: "used",
        },
      ],
      fragments: [
        {
          id: "fragment-0001",
          incomingTextId: "incoming-0001",
          text: "Odlomek",
          status: "inserted",
        },
      ],
      insertions: [
        {
          id: "insertion-0001",
          fragmentId: "fragment-0001",
          targetChapterPath: "D:\\data\\chapter.md",
        },
      ],
    },
    {
      manifestVersion: "2",
      incomingTexts: [
        {
          id: "incoming-0001",
          sourcePath: "incoming/incoming-0001.txt",
          status: "used",
        },
      ],
      fragments: [
        {
          id: "fragment-0001",
          incomingTextId: "incoming-0001",
          text: "Odlomek",
          status: "inserted",
        },
      ],
      insertions: [
        {
          id: "insertion-0001",
          fragmentId: "fragment-0001",
          targetChapterPath: "//server/share/chapter.md",
        },
      ],
    },
  ];

  for (const manifest of manifests) {
    const result = validateManifest(manifest);

    assert.equal(result.isValid, false);
    assert.equal(
      result.errors.some((error) => error.includes("targetChapterPath must be a relative path")),
      true,
    );
  }
});

test("validateManifest accepts safe relative sourcePath and targetChapterPath", () => {
  const manifest: WorkbenchManifest = {
    manifestVersion: "2",
    incomingTexts: [
      {
        id: "incoming-0001",
        sourcePath: "incoming/incoming-0001.txt",
        status: "used",
      },
    ],
    fragments: [
      {
        id: "fragment-0001",
        incomingTextId: "incoming-0001",
        text: "Odlomek",
        status: "inserted",
      },
    ],
    insertions: [
      {
        id: "insertion-0001",
        fragmentId: "fragment-0001",
        targetChapterPath: "chapters/chapter-001.md",
      },
    ],
  };

  const result = validateManifest(manifest);

  assert.equal(result.isValid, true);
  assert.deepEqual(result.errors, []);
});

test("validateManifestTransition rejects invalid status transitions", async () => {
  const moduleNamespace = await import("./workbenchManifest.js");
  const validateManifestTransition = Reflect.get(
    moduleNamespace,
    "validateManifestTransition",
  ) as ((previousManifest: WorkbenchManifest, nextManifest: WorkbenchManifest) => { isValid: boolean; errors: string[] }) | undefined;

  assert.equal(typeof validateManifestTransition, "function");

  const previousManifest = addIncomingText(createEmptyManifest(), {
    title: "Seed text",
    body: "Prvi vhodni tekst.",
  }).manifest;

  const nextManifest: WorkbenchManifest = {
    ...previousManifest,
    incomingTexts: previousManifest.incomingTexts.map((incomingText) => ({
      ...incomingText,
      status: "used",
    })),
  };

  const result = validateManifestTransition!(previousManifest, nextManifest);

  assert.equal(result.isValid, false);
  assert.equal(
    result.errors.some((error) => error.includes("Invalid IncomingText transition for incoming-0001: new -> used")),
    true,
  );
});

test("validateManifestTransition accepts allowed status transitions", async () => {
  const moduleNamespace = await import("./workbenchManifest.js");
  const validateManifestTransition = Reflect.get(
    moduleNamespace,
    "validateManifestTransition",
  ) as ((previousManifest: WorkbenchManifest, nextManifest: WorkbenchManifest) => { isValid: boolean; errors: string[] }) | undefined;

  assert.equal(typeof validateManifestTransition, "function");

  const previousManifest = addIncomingText(createEmptyManifest(), {
    title: "Seed text",
    body: "Prvi vhodni tekst.",
  }).manifest;

  const nextManifest = startProcessingIncoming(previousManifest, "incoming-0001").manifest;
  const result = validateManifestTransition!(previousManifest, nextManifest);

  assert.equal(result.isValid, true);
  assert.deepEqual(result.errors, []);
});

test("updateIncomingText renames the source title without changing status", () => {
  const manifest = addIncomingText(createEmptyManifest(), {
    title: "Star naslov",
    body: "Prvi vhodni tekst.",
  }).manifest;

  const result = updateIncomingText(manifest, "incoming-0001", { title: "Nov naslov" });

  assert.equal(result.value.title, "Nov naslov");
  assert.equal(result.value.status, "new");
  assert.equal(result.manifest.incomingTexts[0]?.title, "Nov naslov");
  assert.equal(validateManifest(result.manifest).isValid, true);
  // input manifest is not mutated
  assert.equal(manifest.incomingTexts[0]?.title, "Star naslov");
});

test("updateIncomingText removes note on null", () => {
  const manifest = addIncomingText(createEmptyManifest(), {
    title: "Vir",
    body: "Prvi vhodni tekst.",
    note: "pozni opomba",
  }).manifest;
  assert.equal(manifest.incomingTexts[0]?.note, "pozni opomba");

  const result = updateIncomingText(manifest, "incoming-0001", { note: null });

  assert.equal(result.value.note, undefined);
});

test("updateIncomingText rejects blank title", () => {
  const manifest = addIncomingText(createEmptyManifest(), { body: "Prvi vhodni tekst." }).manifest;

  assert.throws(
    () => updateIncomingText(manifest, "incoming-0001", { title: "   " }),
    /title must be a non-empty string/,
  );
});

test("updateIncomingText throws for a missing incoming text", () => {
  const manifest = addIncomingText(createEmptyManifest(), { body: "Prvi vhodni tekst." }).manifest;

  assert.throws(
    () => updateIncomingText(manifest, "incoming-missing", { title: "Nov naslov" }),
    /IncomingText not found: incoming-missing/,
  );
});

test("updateFragment edits the working excerpt text without a status change", () => {
  const manifest = createFragmentFromIncoming(
    startProcessingIncoming(
      addIncomingText(createEmptyManifest(), { title: "Vir", body: "Prvi vhodni tekst." }).manifest,
      "incoming-0001",
    ).manifest,
    "incoming-0001",
    "Star odlomek.",
  ).manifest;

  const result = updateFragment(manifest, "fragment-0001", { text: "Nov odlomek po obnovi." });

  assert.equal(result.value.text, "Nov odlomek po obnovi.");
  assert.equal(result.value.status, "draft");
  assert.equal(validateManifest(result.manifest).isValid, true);
  assert.equal(manifest.fragments[0]?.text, "Star odlomek.");
});

test("updateFragment rejects blank text", () => {
  const manifest = createFragmentFromIncoming(
    startProcessingIncoming(
      addIncomingText(createEmptyManifest(), { title: "Vir", body: "Prvi vhodni tekst." }).manifest,
      "incoming-0001",
    ).manifest,
    "incoming-0001",
    "Star odlomek.",
  ).manifest;

  assert.throws(
    () => updateFragment(manifest, "fragment-0001", { text: "   " }),
    /text must be a non-empty string/,
  );
});

test("updateInsertion renames the target chapter path without touching fragment status", () => {
  const manifest = insertFragmentIntoChapter(
    createFragmentFromIncoming(
      startProcessingIncoming(
        addIncomingText(createEmptyManifest(), { title: "Vir", body: "Prvi vhodni tekst." }).manifest,
        "incoming-0001",
      ).manifest,
      "incoming-0001",
      "Odlomek.",
    ).manifest,
    "fragment-0001",
    "chapters/01-uvod.md",
  ).manifest;

  const result = updateInsertion(manifest, "insertion-0001", {
    targetChapterPath: "chapters/02-jedro.md",
    positionNote: "za uvodom",
  });

  assert.equal(result.value.targetChapterPath, "chapters/02-jedro.md");
  assert.equal(result.value.positionNote, "za uvodom");
  // fragment and incoming keep their statuses
  assert.equal(result.manifest.fragments[0]?.status, "inserted");
  assert.equal(result.manifest.incomingTexts[0]?.status, "used");
  assert.equal(validateManifest(result.manifest).isValid, true);
});

test("updateInsertion rejects blank targetChapterPath", () => {
  const manifest = insertFragmentIntoChapter(
    createFragmentFromIncoming(
      startProcessingIncoming(
        addIncomingText(createEmptyManifest(), { title: "Vir", body: "Prvi vhodni tekst." }).manifest,
        "incoming-0001",
      ).manifest,
      "incoming-0001",
      "Odlomek.",
    ).manifest,
    "fragment-0001",
    "chapters/01-uvod.md",
  ).manifest;

  assert.throws(
    () => updateInsertion(manifest, "insertion-0001", { targetChapterPath: "  " }),
    /targetChapterPath must be a non-empty string/,
  );
});
test("updateFragment sets a title (rename) without changing status", () => {
  const manifest = createFragmentFromIncoming(
    startProcessingIncoming(
      addIncomingText(createEmptyManifest(), { title: "Vir", body: "Prvi vhodni tekst." }).manifest,
      "incoming-0001",
    ).manifest,
    "incoming-0001",
    "Star odlomek.",
  ).manifest;

  const result = updateFragment(manifest, "fragment-0001", { title: "Moj naslov odlomka" });

  assert.equal(result.value.title, "Moj naslov odlomka");
  assert.equal(result.value.status, "draft");
  assert.equal(result.manifest.fragments[0]?.title, "Moj naslov odlomka");
  assert.equal(validateManifest(result.manifest).isValid, true);
  assert.equal(manifest.fragments[0]?.title, undefined);
});

test("updateFragment removes a title on null", () => {
  const titled = updateFragment(
    createFragmentFromIncoming(
      startProcessingIncoming(
        addIncomingText(createEmptyManifest(), { title: "Vir", body: "Prvi vhodni tekst." }).manifest,
        "incoming-0001",
      ).manifest,
      "incoming-0001",
      "Star odlomek.",
    ).manifest,
    "fragment-0001",
    { title: "Moj naslov" },
  ).manifest;

  const result = updateFragment(titled, "fragment-0001", { title: null });

  assert.equal(result.value.title, undefined);
  assert.equal(validateManifest(result.manifest).isValid, true);
});

test("updateFragment rejects a blank title", () => {
  const manifest = createFragmentFromIncoming(
    startProcessingIncoming(
      addIncomingText(createEmptyManifest(), { title: "Vir", body: "Prvi vhodni tekst." }).manifest,
      "incoming-0001",
    ).manifest,
    "incoming-0001",
    "Star odlomek.",
  ).manifest;

  assert.throws(
    () => updateFragment(manifest, "fragment-0001", { title: "   " }),
    /title must be a non-empty string/,
  );
});
test("migrateManifestV1ToV2 upgrades a v1 manifest to v2 losslessly", () => {
  const manifestV1: WorkbenchManifestV1 = {
    manifestVersion: "1",
    incomingTexts: [
      {
        id: "incoming-0001",
        sourcePath: "incoming/incoming-0001.txt",
        status: "used",
        title: "Vir",
      },
    ],
    fragments: [
      {
        id: "fragment-0001",
        incomingTextId: "incoming-0001",
        text: "Odlomek.",
        status: "inserted",
        conceptIds: ["concept-0001"],
      },
    ],
    insertions: [
      {
        id: "insertion-0001",
        fragmentId: "fragment-0001",
        targetChapterPath: "chapters/01-uvod.md",
      },
    ],
    concepts: [{ id: "concept-0001", label: "Bistvo" }],
  };

  const migrated = migrateManifestV1ToV2(manifestV1);

  assert.equal(migrated.manifestVersion, "2");
  // lossless: same ids, fields, and connected conceptIds survive
  assert.equal(migrated.incomingTexts[0]?.title, "Vir");
  assert.deepEqual(migrated.fragments[0]?.conceptIds, ["concept-0001"]);
  assert.equal(migrated.insertions[0]?.targetChapterPath, "chapters/01-uvod.md");
  assert.equal(migrated.concepts?.[0]?.label, "Bistvo");
  assert.equal(validateManifest(migrated).isValid, true);
  // input is not mutated
  assert.equal(manifestV1.manifestVersion, "1");
});

test("migrateManifestV1ToV2 carries an existing Fragment.title when present", () => {
  const manifestV1: WorkbenchManifestV1 = {
    manifestVersion: "1",
    incomingTexts: [],
    fragments: [
      {
        id: "fragment-0001",
        incomingTextId: "incoming-0001",
        text: "Odlomek.",
        status: "draft",
        title: "Moja opozorilo",
      },
    ],
    insertions: [],
  };
  // a v1 fragment referencing a missing incoming is fine as an input to migration;
  // the migration itself is a shape-preserving copy, not a validator gate.
  const migrated = migrateManifestV1ToV2(manifestV1);

  assert.equal(migrated.manifestVersion, "2");
  assert.equal(migrated.fragments[0]?.title, "Moja opozorilo");
});
test("addConcept creates a new concept with a unique id", () => {
  const manifest = createEmptyManifest();

  const result = addConcept(manifest, { label: "Bistvo" });

  assert.equal(result.value.id, "concept-0001");
  assert.equal(result.value.label, "Bistvo");
  assert.equal(result.manifest.concepts?.length, 1);
  assert.equal(validateManifest(result.manifest).isValid, true);
  assert.equal(manifest.concepts?.length, 0);
});

test("addConcept rejects a blank label", () => {
  const manifest = createEmptyManifest();

  assert.throws(
    () => addConcept(manifest, { label: "   " }),
    /label must be a non-empty string/,
  );
});

test("updateFragment assigns conceptIds to a fragment", () => {
  const base = createFragmentFromIncoming(
    startProcessingIncoming(
      addIncomingText(createEmptyManifest(), { title: "Vir", body: "Prvi vhodni tekst." }).manifest,
      "incoming-0001",
    ).manifest,
    "incoming-0001",
    "Odlomek.",
  ).manifest;
  const withConcept = addConcept(base, { label: "Bistvo" }).manifest;

  const result = updateFragment(withConcept, "fragment-0001", { conceptIds: ["concept-0001"] });

  assert.deepEqual(result.value.conceptIds, ["concept-0001"]);
  assert.equal(validateManifest(result.manifest).isValid, true);
});

test("updateFragment clears conceptIds on null and rejects unknown concepts", () => {
  const base = createFragmentFromIncoming(
    startProcessingIncoming(
      addIncomingText(createEmptyManifest(), { title: "Vir", body: "Prvi vhodni tekst." }).manifest,
      "incoming-0001",
    ).manifest,
    "incoming-0001",
    "Odlomek.",
  ).manifest;
  const withConcept = addConcept(base, { label: "Bistvo" }).manifest;
  const tagged = updateFragment(withConcept, "fragment-0001", { conceptIds: ["concept-0001"] }).manifest;

  // clear works
  const cleared = updateFragment(tagged, "fragment-0001", { conceptIds: null });
  assert.equal(cleared.value.conceptIds, undefined);

  // unknown concept is rejected by validation
  assert.throws(
    () => updateFragment(tagged, "fragment-0001", { conceptIds: ["concept-missing"] }),
    /references missing Concept/,
  );
});
