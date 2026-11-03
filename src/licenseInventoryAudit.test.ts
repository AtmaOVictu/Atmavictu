import assert from "node:assert/strict";
import test from "node:test";
import {
  compareRepositoryHeads,
  parsePinnedRepositoryHeads,
} from "./licenseInventoryAudit.js";

const firstCommit = "a".repeat(40);
const secondCommit = "b".repeat(40);

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
