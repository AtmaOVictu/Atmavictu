import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import {
  compareRepositoryFiles,
  compareRepositoryHeads,
  parsePinnedRepositoryFiles,
  parsePinnedRepositoryHeads,
  type RepositoryHead,
} from "./licenseInventoryAudit.js";
import {
  createLicensePathAuditReport,
  describeRootLicenseEvidenceChanges,
  findLicensePathCandidates,
  groupMissingRootLicenseAlternatives,
  requireMatchingRepositoryNames,
  summarizeMissingRootLicenseCandidates,
  summarizeCurrentRootLicenseStatus,
} from "./licensePathInventory.js";

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

test("findLicensePathCandidates selects license-named files, not directories or source files", () => {
  assert.deepEqual(
    findLicensePathCandidates([
      { path: "LICENSE.md", sha: firstCommit, type: "blob" },
      { path: "src/LICENCE-THIRD-PARTY.txt", sha: secondCommit, type: "blob" },
      { path: "vendor/package/COPYING", sha: firstCommit, type: "blob" },
      { path: "vendor/package/LICENSE.vrata.json", sha: secondCommit, type: "blob" },
      { path: "src/license.go", sha: firstCommit, type: "blob" },
      { path: "src/copyright_headers.py", sha: secondCommit, type: "blob" },
      { path: "src/licenseHeader.ts", sha: firstCommit, type: "blob" },
      { path: "LICENSES", type: "tree" },
      { type: "blob" },
    ]),
    [
      { path: "LICENSE.md", blob: firstCommit },
      { path: "src/LICENCE-THIRD-PARTY.txt", blob: secondCommit },
      { path: "vendor/package/COPYING", blob: firstCommit },
      { path: "vendor/package/LICENSE.vrata.json", blob: secondCommit },
    ],
  );
});

test("findLicensePathCandidates rejects candidate entries without a valid blob SHA", () => {
  assert.throws(
    () => findLicensePathCandidates([{ path: "LICENSE.md", type: "blob" }]),
    /no valid blob SHA for LICENSE\.md/u,
  );
});

test("requireMatchingRepositoryNames accepts moving heads but requires an exact repository set", () => {
  const current: RepositoryHead[] = [
    { name: "alpha", defaultBranch: "main", commit: secondCommit },
    { name: "oracle", defaultBranch: null, commit: null },
  ];
  assert.deepEqual(
    requireMatchingRepositoryNames(new Set(["alpha", "oracle"]), current),
    current,
  );
  assert.throws(
    () =>
      requireMatchingRepositoryNames(new Set(["alpha", "oracle"]), [current[0]!]),
    /missing: oracle; unexpected: none/u,
  );
  assert.throws(
    () =>
      requireMatchingRepositoryNames(
        new Set(["alpha", "oracle"]),
        [...current, { name: "new-repository", defaultBranch: "main", commit: firstCommit }],
      ),
    /missing: none; unexpected: new-repository/u,
  );
  assert.throws(
    () =>
      requireMatchingRepositoryNames(
        new Set(["alpha"]),
        [
          current[0]!,
          { name: "alpha", defaultBranch: "main", commit: firstCommit },
        ],
      ),
    /duplicate repository names/u,
  );
});

test("summarizeMissingRootLicenseCandidates separates root alternatives from nested leads", () => {
  assert.deepEqual(
    summarizeMissingRootLicenseCandidates(
      [
        { repository: "root-alt", commit: firstCommit, path: "LICENSE", blob: secondCommit },
        { repository: "root-alt", commit: firstCommit, path: "COPYING", blob: firstCommit },
        { repository: "root-alt", commit: firstCommit, path: "NOTICE", blob: firstCommit },
        { repository: "nested-only", commit: secondCommit, path: "docs/LICENSE.txt", blob: firstCommit },
        { repository: "has-root-license", commit: secondCommit, path: "LICENSE", blob: secondCommit },
      ],
      new Set(["root-alt", "nested-only"]),
    ),
    {
      repositoriesWithCandidates: 2,
      repositoriesWithRootAlternatives: 1,
      repositoriesWithNestedOnly: 1,
      rootAlternativePaths: 3,
      uniqueRootAlternativeBlobs: 2,
      nestedCandidatePaths: 1,
    },
  );
});

test("groupMissingRootLicenseAlternatives deduplicates blobs and excludes nested or unrelated candidates", () => {
  assert.deepEqual(
    groupMissingRootLicenseAlternatives(
      [
        {
          repository: "beta",
          commit: secondCommit,
          path: "COPYING",
          blob: firstCommit,
        },
        {
          repository: "alpha",
          commit: firstCommit,
          path: "LICENSE",
          blob: firstCommit,
        },
        {
          repository: "alpha",
          commit: firstCommit,
          path: "docs/LICENSE",
          blob: secondCommit,
        },
        {
          repository: "has-root-license",
          commit: secondCommit,
          path: "LICENSE",
          blob: secondCommit,
        },
      ],
      new Set(["alpha", "beta"]),
    ),
    [
      {
        blob: firstCommit,
        candidates: [
          {
            repository: "alpha",
            commit: firstCommit,
            path: "LICENSE",
            blob: firstCommit,
          },
          {
            repository: "beta",
            commit: secondCommit,
            path: "COPYING",
            blob: firstCommit,
          },
        ],
      },
    ],
  );
});

test("createLicensePathAuditReport emits a versioned focused JSON shape", () => {
  const candidate = {
    repository: "alpha",
    commit: firstCommit,
    path: "LICENSE",
    blob: secondCommit,
  };
  const report = createLicensePathAuditReport({
    startedAt: new Date("2026-11-03T11:00:00.000Z"),
    endedAt: new Date("2026-11-03T11:01:00.000Z"),
    scannedRepositories: 2,
    repositoriesWithoutDefaultBranch: 1,
    candidates: [candidate],
    expectedFiles: new Map([
      [
        "alpha",
        {
          defaultBranch: "main",
          commit: firstCommit,
          rootLicenseBlob: null,
          draftBlob: null,
        },
      ],
    ]),
    scannedHeads: new Map([["alpha", firstCommit]]),
    currentRootBlobs: new Map(),
    focused: true,
  });

  assert.equal(report.schemaVersion, 1);
  assert.equal(report.scope, "root-alternatives-without-current-root-license");
  assert.equal(report.repositoriesWithoutCurrentRootLicense, 1);
  assert.deepEqual(report.measured, {
    startedAt: "2026-11-03T11:00:00.000Z",
    endedAt: "2026-11-03T11:01:00.000Z",
  });
  assert.equal(report.scan.candidatesFound, 1);
  assert.deepEqual(report.candidates, []);
  assert.deepEqual(report.groups, [
    { blob: secondCommit, candidates: [candidate] },
  ]);
  assert.deepEqual(report.rootLicenseStatus, {
    repositoriesScanned: 1,
    presentAtCurrentHeads: 0,
    absentAtCurrentHeads: 1,
    changedSinceRecordedInventory: 0,
  });
  assert.deepEqual(report.rootLicenseChanges, []);
  assert.match(report.limitation, /does not fetch file contents/u);
});

test("summarizeCurrentRootLicenseStatus compares only scanned heads with recorded path and blob evidence", () => {
  const expectedFiles = new Map([
    [
      "unchanged",
      {
        defaultBranch: "main",
        commit: firstCommit,
        rootLicenseBlob: firstCommit,
        draftBlob: null,
      },
    ],
    [
      "removed",
      {
        defaultBranch: "main",
        commit: firstCommit,
        rootLicenseBlob: secondCommit,
        draftBlob: null,
      },
    ],
    [
      "added",
      {
        defaultBranch: "main",
        commit: firstCommit,
        rootLicenseBlob: null,
        draftBlob: null,
      },
    ],
    [
      "unscanned",
      {
        defaultBranch: null,
        commit: null,
        rootLicenseBlob: null,
        draftBlob: null,
      },
    ],
    [
      "branch-added",
      {
        defaultBranch: null,
        commit: null,
        rootLicenseBlob: null,
        draftBlob: null,
      },
    ],
  ]);
  assert.deepEqual(
    summarizeCurrentRootLicenseStatus(
      expectedFiles,
      new Map([
        ["unchanged", firstCommit],
        ["removed", secondCommit],
        ["added", firstCommit],
        ["branch-added", firstCommit],
      ]),
      new Map([
        ["unchanged", firstCommit],
        ["added", secondCommit],
        ["branch-added", firstCommit],
      ]),
    ),
    {
      repositoriesScanned: 4,
      presentAtCurrentHeads: 3,
      absentAtCurrentHeads: 1,
      changedSinceRecordedInventory: 3,
    },
  );
});

test("describeRootLicenseEvidenceChanges reports added and removed root files with commit and blob identities", () => {
  const expectedFiles = new Map([
    [
      "removed",
      {
        defaultBranch: "main",
        commit: firstCommit,
        rootLicenseBlob: secondCommit,
        draftBlob: null,
      },
    ],
    [
      "added",
      {
        defaultBranch: "master",
        commit: secondCommit,
        rootLicenseBlob: null,
        draftBlob: null,
      },
    ],
  ]);
  assert.deepEqual(
    describeRootLicenseEvidenceChanges(
      expectedFiles,
      new Map([
        ["removed", secondCommit],
        ["added", firstCommit],
      ]),
      new Map([["added", firstCommit]]),
    ),
    [
      {
        repository: "added",
        recordedDefaultBranch: "master",
        recordedCommit: secondCommit,
        recordedBlob: null,
        currentCommit: firstCommit,
        currentBlob: firstCommit,
      },
      {
        repository: "removed",
        recordedDefaultBranch: "main",
        recordedCommit: firstCommit,
        recordedBlob: secondCommit,
        currentCommit: secondCommit,
        currentBlob: null,
      },
    ],
  );
});
