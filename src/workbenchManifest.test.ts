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

test("validateManifest rejects unexpected top-level properties", () => {
  const manifest = {
    manifestVersion: "1",
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
    manifestVersion: "1",
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
    manifestVersion: "1",
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
    manifestVersion: "1",
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
    manifestVersion: "1",
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
    manifestVersion: "1",
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
    manifestVersion: "1",
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
    manifestVersion: "1",
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
      manifestVersion: "1",
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
      manifestVersion: "1",
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
      manifestVersion: "1",
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
      manifestVersion: "1",
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
      manifestVersion: "1",
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
      manifestVersion: "1",
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
      manifestVersion: "1",
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
    manifestVersion: "1",
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
