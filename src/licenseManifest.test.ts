import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile, realpath } from "node:fs/promises";
import { isAbsolute, relative, resolve, sep } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

interface LicenseManifest {
  version: string;
  items: Array<{
    path: string;
    size_bytes: number;
    sha256: string;
  }>;
  registers_not_hash_listed: {
    files: string[];
  };
}

interface LicenseMachineRecord {
  version: string;
  "publication-status": string;
}

test("license manifest identifies the exact bytes of every covered file", async () => {
  const repositoryRoot = fileURLToPath(new URL("../../", import.meta.url));
  const licenseUrl = new URL("../../LICENSE.md", import.meta.url);
  const manifestUrl = new URL("../../LICENSE-MANIFEST", import.meta.url);
  const licenseBytes = await readFile(licenseUrl);
  const licenseText = licenseBytes.toString("utf8");
  const manifest = JSON.parse(
    await readFile(manifestUrl, "utf8"),
  ) as LicenseManifest;
  const licenseEntries = manifest.items.filter((item) => item.path === "LICENSE.md");

  assert.equal(licenseEntries.length, 1, "manifest must identify LICENSE.md exactly once");
  assert.equal(
    new Set(manifest.items.map((item) => item.path)).size,
    manifest.items.length,
    "manifest paths must be unique",
  );
  const licenseVersion = licenseText
    .split(/\r?\n/, 1)[0]
    ?.match(/^\S+\s+×\s+\S+/u)?.[0];
  assert.ok(licenseVersion);
  assert.equal(manifest.version, licenseVersion);

  const machineRecordMatch = licenseText.match(
    /## Machine record\r?\n[\s\S]*?```json\r?\n([\s\S]*?)\r?\n```/u,
  );
  assert.ok(machineRecordMatch, "license machine record must contain JSON");
  const machineRecordJson = machineRecordMatch[1];
  assert.ok(machineRecordJson, "license machine record JSON must not be empty");
  const machineRecord = JSON.parse(machineRecordJson) as LicenseMachineRecord;
  assert.equal(machineRecord.version, licenseVersion);
  assert.match(machineRecord["publication-status"], /branch edition/u);

  const realRepositoryRoot = await realpath(repositoryRoot);
  const realManifestPath = await realpath(fileURLToPath(manifestUrl));
  const resolvedEntries = new Set<string>();
  for (const entry of manifest.items) {
    assert.ok(entry.path.length > 0, "manifest paths must not be empty");
    assert.equal(isAbsolute(entry.path), false, `${entry.path} must be relative`);

    const resolvedPath = resolve(repositoryRoot, entry.path);
    const relativePath = relative(repositoryRoot, resolvedPath);
    assert.ok(
      relativePath !== ".." &&
        !relativePath.startsWith(`..${sep}`) &&
        !isAbsolute(relativePath),
      `${entry.path} must stay inside the repository`,
    );

    const actualPath = await realpath(resolvedPath);
    const actualRelativePath = relative(realRepositoryRoot, actualPath);
    assert.ok(
      actualRelativePath !== ".." &&
        !actualRelativePath.startsWith(`..${sep}`) &&
        !isAbsolute(actualRelativePath),
      `${entry.path} must not resolve through a symlink outside the repository`,
    );
    assert.notEqual(
      actualPath,
      realManifestPath,
      "manifest must not list itself",
    );
    const canonicalPath =
      process.platform === "win32" ? actualPath.toLowerCase() : actualPath;
    assert.equal(
      resolvedEntries.has(canonicalPath),
      false,
      `${entry.path} must not alias another manifest entry`,
    );
    resolvedEntries.add(canonicalPath);

    const bytes = await readFile(actualPath);
    assert.ok(
      Number.isSafeInteger(entry.size_bytes) && entry.size_bytes >= 0,
      `${entry.path} must declare a valid byte length`,
    );
    assert.equal(entry.size_bytes, bytes.byteLength, `${entry.path} byte length`);
    assert.match(entry.sha256, /^[a-f0-9]{64}$/, `${entry.path} SHA-256 format`);
    assert.equal(
      entry.sha256,
      createHash("sha256").update(bytes).digest("hex"),
      `${entry.path} SHA-256`,
    );
  }

  const coveredPaths = new Set(manifest.items.map((item) => item.path));
  const registerPaths = manifest.registers_not_hash_listed.files.map((file) =>
    file.split(" (", 1)[0],
  );
  assert.ok(
    registerPaths.includes("LICENSE-IZVIRNIKI.md"),
    "the source-material register named in §0.42 must be identified",
  );
  assert.equal(
    new Set(registerPaths).size,
    registerPaths.length,
    "unhashed register paths must be unique",
  );

  for (const registerPath of registerPaths) {
    assert.ok(registerPath, "unhashed register paths must not be empty");
    assert.equal(
      coveredPaths.has(registerPath),
      false,
      `${registerPath} must not also be hash-listed`,
    );
    assert.equal(
      isAbsolute(registerPath),
      false,
      `${registerPath} must be relative`,
    );

    const resolvedPath = resolve(repositoryRoot, registerPath);
    const relativePath = relative(repositoryRoot, resolvedPath);
    assert.ok(
      relativePath !== ".." &&
        !relativePath.startsWith(`..${sep}`) &&
        !isAbsolute(relativePath),
      `${registerPath} must stay inside the repository`,
    );

    const actualPath = await realpath(resolvedPath);
    const actualRelativePath = relative(realRepositoryRoot, actualPath);
    assert.ok(
      actualRelativePath !== ".." &&
        !actualRelativePath.startsWith(`..${sep}`) &&
        !isAbsolute(actualRelativePath),
      `${registerPath} must resolve inside the repository`,
    );
  }
});

test("historical language readings are labeled as abridged, not complete translations", async () => {
  const repositoryRoot = fileURLToPath(new URL("../../", import.meta.url));
  const tonguesText = await readFile(
    new URL("../../LICENSE-TONGUES.md", import.meta.url),
    "utf8",
  );
  const historicEditionRows = tonguesText
    .split(/\r?\n/u)
    .filter(
      (line) =>
        line.startsWith("| `LICENSE-") &&
        line.includes("Historical abridged readings;"),
    );
  const historicEditionFiles = historicEditionRows.flatMap((line) =>
      [...line.matchAll(/`(LICENSE-[A-Z-]+\.md)`/gu)].flatMap((match) =>
        match[1] ? [match[1]] : [],
      ),
    );

  assert.equal(historicEditionFiles.length, 35);
  for (const file of historicEditionFiles) {
    const text = await readFile(resolve(repositoryRoot, file), "utf8");
    assert.match(
      text,
      /^> Edition status .*historical abridged reading; not a complete translation\./imu,
      `${file} must disclose its historical abridged status`,
    );
    assert.match(
      text,
      /Exact clause coverage: ⚠ not yet mapped\. Reviewer: unreviewed\./u,
      `${file} must disclose unmapped coverage and review status`,
    );
  }
});

test("cross-repository draft inventory distinguishes copies from a released license", async () => {
  const tonguesText = await readFile(
    new URL("../../LICENSE-TONGUES.md", import.meta.url),
    "utf8",
  );
  const draftStatus = tonguesText.split(
    "## Cross-repository release status measured 2026-11-03",
    2,
  )[1];

  assert.ok(draftStatus, "cross-repository release status must be documented");
  assert.match(draftStatus, /Atmavictu\/main.+VBL 0\.1410/u);
  assert.match(draftStatus, /scan of all 53 organization repositories found 19 readable/u);
  assert.match(draftStatus, /fourteen Base64 files decode to byte-identical VBL 0\.1300 bodies/u);
  assert.match(draftStatus, /106,427 bytes/u);
  assert.match(draftStatus, /33 had no readable file/u);
  assert.match(draftStatus, /DRAFT · NOT RELEASED/u);
  assert.match(draftStatus, /52,169 bytes/u);
  assert.match(draftStatus, /SHA-256 `dac171ccf3d526b82a16ca28462002cc05c5d8b46e4d3dadfb1e3ace7e171d60`/u);
  assert.match(draftStatus, /Identical copies prove byte identity.+not release/u);
});

test("cross-repository root license inventory names every measured repository and ref", async () => {
  const tonguesText = await readFile(
    new URL("../../LICENSE-TONGUES.md", import.meta.url),
    "utf8",
  );
  const inventory = tonguesText.split(
    "## Cross-repository release status measured 2026-11-03",
    2,
  )[1];
  assert.ok(inventory, "cross-repository release status must be documented");

  const rows = inventory
    .split(/\r?\n/u)
    .filter((line) =>
      /^\| \[[^\]]+\]\(https:\/\/github\.com\/AtmaOVictu\/[^/]+\/blob\/[^/]+\/LICENSE\.md\)/u.test(
        line,
      ),
    );
  assert.equal(rows.length, 19, "inventory must identify all 19 measured root files");
  assert.match(
    inventory,
    /rechecked against the current default refs through GitHub GraphQL from `2026-11-03T10:24:45\.081\+01:00` to `2026-11-03T10:24:47\.727\+01:00`: all 52 repositories with a default branch still pointed to their recorded commit; `Atmavictu_Oracle` remained without one\. This confirms ref-head identity during that recheck, not a fresh download of file bytes/u,
  );

  const parsedRows = rows.map((row) => {
    const match = row.match(
      /^\| \[([^\]]+)\]\(https:\/\/github\.com\/AtmaOVictu\/([^/]+)\/blob\/([a-f0-9]{40})\/LICENSE\.md\) \| `([^`]+)` \| ([^|]+) \| `([a-f0-9]{40})`\s+\| `([a-f0-9]{40})` \|$/u,
    );
    assert.ok(match, `inventory row must have a complete evidence shape: ${row}`);
    const repository = match[1] ?? "";
    const slug = match[2] ?? "";
    const linkedCommit = match[3] ?? "";
    const defaultRef = match[4] ?? "";
    const classification = (match[5] ?? "").trim();
    const blob = match[6] ?? "";
    const measuredCommit = match[7] ?? "";

    assert.equal(repository, slug, `${repository} link must target its named repository`);
    assert.equal(
      linkedCommit,
      measuredCommit,
      `${repository} link must pin the measured commit`,
    );
    assert.match(blob, /^[a-f0-9]{40}$/u, `${repository} must have a Git blob ID`);

    return { repository, defaultRef, classification, blob, measuredCommit };
  });

  const expectedDefaultRefs = {
    Atmavictu: "main",
    CanvasMinstral: "master",
    "ontolo-ko-jedro": "main",
    OntoMatematika: "main",
    ZAKONODAJACLOVEKA: "main",
    DelozaZivot: "main",
    "Mucilnica-modrosti": "main",
    "soul-evolution": "master",
    EnglishVarient: "main",
    "prevoz-LUCIUS": "master",
    Aplikacija: "main",
    ".github-workflows": "main",
    "Slovenian-Language-Technologies-Overview": "main",
    "SYMBOLON-KATHOLIKON": "main",
    Podpora: "main",
    "verification-before-assertion": "main",
    "godot-demo-projects": "master",
    manim: "master",
    "awesome-godot": "master",
  };
  for (const [repository, expectedRef] of Object.entries(expectedDefaultRefs)) {
    const row = parsedRows.find((candidate) => candidate.repository === repository);
    assert.ok(
      row,
      `${repository} must appear in the measured inventory`,
    );
    assert.equal(row.defaultRef, expectedRef, `${repository} default ref`);
  }

  const vbl1410 = parsedRows.filter((row) =>
    row.classification.startsWith("VBL 0.1410"),
  );
  const vbl1300 = parsedRows.filter((row) =>
    row.classification.startsWith("VBL 0.1300"),
  );
  const otherLicenses = parsedRows.filter(
    (row) =>
      !row.classification.startsWith("VBL 0.1410") &&
      !row.classification.startsWith("VBL 0.1300"),
  );
  assert.equal(vbl1410.length, 2);
  assert.equal(vbl1300.length, 14);
  assert.equal(otherLicenses.length, 3);
  assert.ok(
    vbl1410.every(
      (row) => row.classification === "VBL 0.1410 × 10⁴, plain text",
    ),
  );
  assert.ok(
    vbl1300.every(
      (row) =>
        row.classification === "VBL 0.1300 × 10⁴, Base64-encoded body",
    ),
  );
  assert.deepEqual(
    [...new Set(vbl1410.map((row) => row.blob))],
    ["2c765280d0c732aa5a6169eea329ab67e97b5c60"],
    "VBL 0.1410 copies must share the measured Git blob",
  );
  assert.deepEqual(
    [...new Set(vbl1300.map((row) => row.blob))],
    ["ed6da4abd8b7a61b066ec8be7dd9953c6c6aee9f"],
    "VBL 0.1300 copies must share the measured Git blob",
  );
  assert.deepEqual(
    otherLicenses.map((row) => [row.repository, row.classification, row.blob]),
    [
      [
        "godot-demo-projects",
        "Godot copyright notice and permissive grant text",
        "05519693673e35cc80bba699e69af3de1d9886d7",
      ],
      ["manim", "MIT License", "376297d623856cb9a4807572add16920556550ab"],
      [
        "awesome-godot",
        "Creative Commons Attribution 4.0 International",
        "e655c6889fb244caa0284723bfe4f667b0701e5d",
      ],
    ],
  );
  assert.match(inventory, /VBL 0\.1410 files are byte-identical \(147,608 bytes; SHA-256 `719c706437ba53b44dd70d896b84f0903a194c87034fe24a499bdd4a37517cda`\)/u);
  assert.match(inventory, /VBL 0\.1300 bodies \(106,427 bytes; SHA-256 `66adcc246e2907c7b71c90e7f14ffd0c50a9be73c76dda5529fa653f26d799a9`\)/u);
});

test("cross-repository scan distinguishes missing root files from a missing default branch", async () => {
  const tonguesText = await readFile(
    new URL("../../LICENSE-TONGUES.md", import.meta.url),
    "utf8",
  );
  const inventory = tonguesText.split(
    "## Cross-repository release status measured 2026-11-03",
    2,
  )[1];
  assert.ok(inventory, "cross-repository release status must be documented");

  const missingFileRows = inventory
    .split(/\r?\n/u)
    .filter((line) =>
      /\| No readable root file at this path\s+\| `[a-f0-9]{40}` \|$/u.test(
        line,
      ),
    );
  const readableFileRows = inventory
    .split(/\r?\n/u)
    .filter((line) =>
      /^\| \[[^\]]+\]\(https:\/\/github\.com\/AtmaOVictu\/[^/]+\/blob\/[^/]+\/LICENSE\.md\)/u.test(
        line,
      ),
    );
  const expectedDefaultRefs = {
    "agents-cli": "main",
    "awesome-data-analysis": "main",
    "awesome-design-md": "main",
    "Claude-Code-Game-Studios": "main",
    ComfyUI: "master",
    cookbook: "main",
    "creative-template": "main",
    "deer-flow": "main",
    "Divine-Ascension-System": "main",
    "European-OpenLLM-Projects": "main",
    godot: "master",
    gpt4all: "main",
    graphify: "v7",
    "oh-my-pi": "main",
    "ONL_FER_O_06_Advanced_HTML_and_CSS": "main",
    "ONL_FER_O_06_ES6_React": "main",
    "ONL_FER_O_06_Final_project": "main",
    "ONL_FER_O_06_JavaScript": "main",
    "ONL_FER_O_06_React": "main",
    "ONL_FER_O_06_Sass_RWD": "main",
    "open-webui": "main",
    "platform-docs-public": "main",
    PowerShell: "master",
    pygame: "main",
    qdrant: "master",
    ragflow: "main",
    RecursiveMAS: "main",
    servers: "main",
    superpowers: "main",
    tauri: "dev",
    "todo-app": "main",
    TradingAgents: "main",
    "Understand-Anything": "main",
  };
  assert.equal(missingFileRows.length, 33);
  assert.equal(readableFileRows.length, 19);
  for (const [repository, expectedRef] of Object.entries(expectedDefaultRefs)) {
    const row = missingFileRows.find((candidate) =>
      candidate.startsWith(`| [${repository}](`),
    );
    assert.ok(row, `${repository} must be listed as missing a readable root file`);
    const match = row.match(
      /^\| \[([^\]]+)\]\(https:\/\/github\.com\/AtmaOVictu\/([^/]+)\/tree\/([a-f0-9]{40})\) \| `([^`]+)` \| No readable root file at this path\s+\| `([a-f0-9]{40})` \|$/u,
    );
    assert.ok(match, `${repository} row must identify its measured default ref`);
    assert.equal(match[1], repository, "link label must match repository");
    assert.equal(match[2], repository, "link target must match repository");
    assert.match(match[3] ?? "", /^[a-f0-9]{40}$/u, `${repository} linked commit`);
    assert.equal(match[4], expectedRef, `${repository} declared default ref`);
    assert.equal(match[3], match[5], `${repository} link must pin its measured commit`);
  }

  const noBranchRows = inventory
    .split(/\r?\n/u)
    .filter((line) =>
      line.includes("| none | No default branch; root-file check unavailable | none |"),
    );
  assert.deepEqual(noBranchRows, [
    "| [Atmavictu_Oracle](https://github.com/AtmaOVictu/Atmavictu_Oracle) | none | No default branch; root-file check unavailable | none |",
  ]);

  const rootFileRepositories = readableFileRows.flatMap((row) => {
    const match = row.match(/^\| \[([^\]]+)\]/u);
    return match?.[1] ? [match[1]] : [];
  });
  const missingFileRepositories = missingFileRows.flatMap((row) => {
    const match = row.match(/^\| \[([^\]]+)\]/u);
    return match?.[1] ? [match[1]] : [];
  });
  const noBranchRepositories = noBranchRows.flatMap((row) => {
    const match = row.match(/^\| \[([^\]]+)\]/u);
    return match?.[1] ? [match[1]] : [];
  });
  const allRepositories = [
    ...rootFileRepositories,
    ...missingFileRepositories,
    ...noBranchRepositories,
  ];
  assert.equal(allRepositories.length, 53, "status rows must cover 53 repositories");
  assert.equal(
    new Set(allRepositories).size,
    53,
    "each repository must appear in exactly one root-file status group",
  );
});

test("cross-repository draft inventory records each measured repository ref and blob", async () => {
  const tonguesText = await readFile(
    new URL("../../LICENSE-TONGUES.md", import.meta.url),
    "utf8",
  );
  const inventory = tonguesText.split(
    "## Cross-repository release status measured 2026-11-03",
    2,
  )[1];
  assert.ok(inventory, "cross-repository release status must be documented");

  const draftRows = inventory
    .split(/\r?\n/u)
    .filter((line) =>
      /\/blob\/[a-f0-9]{40}\/VBL-10\.5\.1-KOMPIL-A-DRAFT-NOT-RELEASED\.md\)/u.test(
        line,
      ),
    );
  const rootLicenseRows = inventory
    .split(/\r?\n/u)
    .filter((line) =>
      /^\| \[[^\]]+\]\(https:\/\/github\.com\/AtmaOVictu\/[^/]+\/blob\/[^/]+\/LICENSE\.md\)/u.test(
        line,
      ),
    );
  const expectedDefaultRefs = {
    Atmavictu: "main",
    CanvasMinstral: "master",
    "ontolo-ko-jedro": "main",
    DelozaZivot: "main",
    "SYMBOLON-KATHOLIKON": "main",
    ZAKONODAJACLOVEKA: "main",
    "verification-before-assertion": "main",
    "Mucilnica-modrosti": "main",
    OntoMatematika: "main",
    "soul-evolution": "master",
    Aplikacija: "main",
    "prevoz-LUCIUS": "master",
    EnglishVarient: "main",
    ".github-workflows": "main",
  };
  assert.equal(draftRows.length, 14, "draft inventory must contain 14 repository rows");

  for (const [repository, expectedRef] of Object.entries(expectedDefaultRefs)) {
    const row = draftRows.find((candidate) =>
      candidate.startsWith(`| [${repository}](`),
    );
    assert.ok(row, `${repository} must appear in the draft inventory`);
    const match = row.match(
      /^\| \[([^\]]+)\]\(https:\/\/github\.com\/AtmaOVictu\/([^/]+)\/blob\/([a-f0-9]{40})\/([^)]*)\) \| `([^`]+)` \| `([^`]+)` \| `([a-f0-9]{40})`\s+\| `([a-f0-9]{40})` \|$/u,
    );
    assert.ok(match, `${repository} draft row must include path and blob evidence`);
    assert.equal(match[1], repository, "link label must match repository");
    assert.equal(match[2], repository, "link target must match repository");
    assert.match(match[3] ?? "", /^[a-f0-9]{40}$/u, `${repository} linked commit`);
    assert.equal(match[4], "VBL-10.5.1-KOMPIL-A-DRAFT-NOT-RELEASED.md");
    assert.equal(match[5], expectedRef, `${repository} declared default ref`);
    assert.equal(match[6], "VBL-10.5.1-KOMPIL-A-DRAFT-NOT-RELEASED.md");
    assert.equal(match[7], "12bfaddf1fa471525ede7f99510eb93335cac994");
    assert.equal(match[3], match[8], `${repository} link must pin its measured commit`);
  }
  assert.match(inventory, /52,169 bytes, SHA-256 `dac171ccf3d526b82a16ca28462002cc05c5d8b46e4d3dadfb1e3ace7e171d60`/u);

  const draftRepositories = new Set(
    draftRows.flatMap((row) => {
      const match = row.match(/^\| \[([^\]]+)\]/u);
      return match?.[1] ? [match[1]] : [];
    }),
  );
  const draftRootLicenseClasses = rootLicenseRows.flatMap((row) => {
    const match = row.match(
      /^\| \[([^\]]+)\].+\| ([^|]+) \| `[a-f0-9]{40}`\s+\| `[a-f0-9]{40}` \|$/u,
    );
    return match?.[1] && match[2] && draftRepositories.has(match[1])
      ? [[match[1], match[2].trim()] as const]
      : [];
  });
  assert.equal(draftRootLicenseClasses.length, 14);
  assert.equal(
    draftRootLicenseClasses.filter(([_, classification]) =>
      classification.startsWith("VBL 0.1410"),
    ).length,
    2,
  );
  assert.equal(
    draftRootLicenseClasses.filter(([_, classification]) =>
      classification.startsWith("VBL 0.1300"),
    ).length,
    12,
  );
  assert.deepEqual(
    rootLicenseRows.flatMap((row) => {
      const match = row.match(/^\| \[([^\]]+)\]/u);
      return match?.[1] &&
        match[1] !== "Atmavictu" &&
        match[1] !== "CanvasMinstral" &&
        !draftRepositories.has(match[1]) &&
        row.includes("VBL 0.1300")
        ? [match[1]]
        : [];
    }),
    ["Slovenian-Language-Technologies-Overview", "Podpora"],
  );
});
