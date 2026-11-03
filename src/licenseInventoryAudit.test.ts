import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import {
  compareRepositoryFiles,
  compareRepositoryHeads,
  parsePinnedRepositoryFiles,
  parsePinnedRepositoryHeads,
} from "./licenseInventoryAudit.js";

const firstCommit = "a".repeat(40);
const secondCommit = "b".repeat(40);

test("the documented inventory has consistent head and file evidence for every repository", async () => {
  const markdown = await readFile(
    new URL("../../LICENSE-TONGUES.md", import.meta.url),
    "utf8",
  );
  const heads = parsePinnedRepositoryHeads(markdown);
  const files = parsePinnedRepositoryFiles(markdown);

  assert.equal(heads.size, 54);
  assert.equal(files.size, 54);
  assert.equal(
    [...files.values()].filter((entry) => entry.rootLicenseBlob !== null).length,
    19,
  );
  assert.equal(
    [...files.values()].filter(
      (entry) => entry.commit !== null && entry.rootLicenseBlob === null,
    ).length,
    34,
  );
  assert.equal(
    [...files.values()].filter((entry) => entry.draftBlob !== null).length,
    14,
  );
  for (const [repository, head] of heads) {
    const evidence = files.get(repository);
    assert.ok(evidence, `${repository} must have file evidence`);
    assert.deepEqual(
      { defaultBranch: evidence.defaultBranch, commit: evidence.commit },
      head,
    );
  }
});

test("parsePinnedRepositoryHeads reads pinned rows and the no-branch row", () => {
  const markdown = [
    "| Repository | Default ref | Status |",
    "|---|---|---|",
    `| [alpha](https://github.com/AtmaOVictu/alpha/blob/${firstCommit}/LICENSE.md) | \`main\` | present |`,
    `| [alpha](https://github.com/AtmaOVictu/alpha/tree/${firstCommit}) | \`main\` | absent |`,
    "| [oracle](https://github.com/AtmaOVictu/oracle) | none | unavailable |",
  ].join("\n");

  assert.deepEqual(
    [...parsePinnedRepositoryHeads(markdown)],
    [
      ["alpha", { defaultBranch: "main", commit: firstCommit }],
      ["oracle", { defaultBranch: null, commit: null }],
    ],
  );
});

test("parsePinnedRepositoryHeads rejects conflicting commits and mislabeled repositories", () => {
  assert.throws(
    () =>
      parsePinnedRepositoryHeads(
        [
          `| [alpha](https://github.com/AtmaOVictu/alpha/blob/${firstCommit}/LICENSE.md) | \`main\` |`,
          `| [alpha](https://github.com/AtmaOVictu/alpha/tree/${secondCommit}) | \`main\` |`,
        ].join("\n"),
      ),
    /conflicting pinned commits for alpha/u,
  );
  assert.throws(
    () =>
      parsePinnedRepositoryHeads(
        `| [alpha](https://github.com/AtmaOVictu/beta/tree/${firstCommit}) | \`main\` |`,
      ),
    /label does not match its URL/u,
  );
});

test("compareRepositoryHeads detects ref, commit, and repository-set drift", () => {
  const expected = new Map([
    ["alpha", { defaultBranch: "main", commit: firstCommit }],
    ["beta", { defaultBranch: "master", commit: secondCommit }],
    ["oracle", { defaultBranch: null, commit: null }],
  ]);
  const actual = [
    { name: "alpha", defaultBranch: "main", commit: firstCommit },
    { name: "beta", defaultBranch: "main", commit: secondCommit },
    { name: "new-repository", defaultBranch: "main", commit: firstCommit },
  ];

  assert.deepEqual(
    compareRepositoryHeads(expected, actual),
    [
      {
        repository: "beta",
        expected: `master: ${secondCommit}`,
        actual: `main: ${secondCommit}`,
      },
      {
        repository: "oracle",
        expected: "no default branch",
        actual: "repository not returned by GitHub",
      },
      {
        repository: "new-repository",
        expected: "repository absent from snapshot",
        actual: `main: ${firstCommit}`,
      },
    ],
  );
});

test("parsePinnedRepositoryFiles reads root status, draft blobs, and missing-branch rows", () => {
  const markdown = [
    "## Cross-repository release status measured 2026-11-03",
    "| Repository | Default ref | Measured root `LICENSE.md` | Git blob | Measured commit |",
    "|---|---|---|---|---|",
    `| [alpha](https://github.com/AtmaOVictu/alpha/blob/${firstCommit}/LICENSE.md) | \`main\` | VBL 0.1410 | \`${secondCommit}\`  | \`${firstCommit}\` |`,
    `| [beta](https://github.com/AtmaOVictu/beta/tree/${secondCommit}) | \`master\` | No readable root file at this path  | \`${secondCommit}\` |`,
    "| [oracle](https://github.com/AtmaOVictu/oracle) | none | No default branch; root-file check unavailable | none |",
    "",
    "| Repository | Default ref | Measured draft path | Git blob | Measured commit |",
    "|---|---|---|---|---|",
    `| [alpha](https://github.com/AtmaOVictu/alpha/blob/${firstCommit}/VBL-10.5.1-KOMPIL-A-DRAFT-NOT-RELEASED.md) | \`main\` | \`VBL-10.5.1-KOMPIL-A-DRAFT-NOT-RELEASED.md\` | \`${secondCommit}\`  | \`${firstCommit}\` |`,
    "",
    "Further notes.",
  ].join("\n");

  assert.deepEqual(
    [...parsePinnedRepositoryFiles(markdown)],
    [
      [
        "alpha",
        {
          defaultBranch: "main",
          commit: firstCommit,
          rootLicenseBlob: secondCommit,
          draftBlob: secondCommit,
        },
      ],
      [
        "beta",
        {
          defaultBranch: "master",
          commit: secondCommit,
          rootLicenseBlob: null,
          draftBlob: null,
        },
      ],
      [
        "oracle",
        {
          defaultBranch: null,
          commit: null,
          rootLicenseBlob: null,
          draftBlob: null,
        },
      ],
    ],
  );
});

test("compareRepositoryFiles detects root and draft Git object drift", () => {
  const expected = new Map([
    [
      "alpha",
      {
        defaultBranch: "main",
        commit: firstCommit,
        rootLicenseBlob: secondCommit,
        draftBlob: firstCommit,
      },
    ],
    [
      "beta",
      {
        defaultBranch: "main",
        commit: secondCommit,
        rootLicenseBlob: null,
        draftBlob: null,
      },
    ],
  ]);
  const actual = new Map([
    ["alpha", { rootLicense: firstCommit, draft: null }],
    ["beta", { rootLicense: firstCommit, draft: firstCommit }],
  ]);

  assert.deepEqual(
    compareRepositoryFiles(expected, actual),
    [
      {
        repository: "alpha",
        expected: secondCommit,
        actual: firstCommit,
      },
      {
        repository: "alpha",
        expected: `draft blob ${firstCommit}`,
        actual: "no draft object",
      },
      {
        repository: "beta",
        expected: "no root LICENSE.md object",
        actual: firstCommit,
      },
    ],
  );
});
