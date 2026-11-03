import { execFileSync } from "node:child_process";
import { readFile } from "node:fs/promises";
import { fileURLToPath, pathToFileURL } from "node:url";

export interface RepositoryHead {
  name: string;
  defaultBranch: string | null;
  commit: string | null;
}

export interface InventoryMismatch {
  repository: string;
  expected: string;
  actual: string;
}

export interface PinnedRepositoryHead {
  defaultBranch: string | null;
  commit: string | null;
}

export interface PinnedRepositoryFiles extends PinnedRepositoryHead {
  rootLicenseBlob: string | null;
  draftBlob: string | null;
}

export interface RepositoryFileObjects {
  rootLicense: string | null;
  draft: string | null;
}

function requiredCapture(value: string | undefined, field: string): string {
  if (value === undefined) {
    throw new Error(`Inventory row is missing ${field}`);
  }
  return value;
}

const GRAPHQL_QUERY = `query {
  user(login: "AtmaOVictu") {
    repositories(first: 100, affiliations: OWNER) {
      pageInfo { hasNextPage }
      nodes {
        name
        defaultBranchRef {
          name
          target { ... on Commit { oid } }
        }
      }
    }
  }
}`;

export function parsePinnedRepositoryHeads(
  markdown: string,
): Map<string, PinnedRepositoryHead> {
  const heads = new Map<string, PinnedRepositoryHead>();

  for (const line of markdown.split(/\r?\n/u)) {
    const match = line.match(
      /^\| \[([^\]]+)\]\(https:\/\/github\.com\/AtmaOVictu\/([^/)`]+)(?:\/(?:blob|tree)\/([a-f0-9]{40})(?:\/[^)]*)?)?\) \| ([^|]+) \|/u,
    );
    if (!match) {
      continue;
    }
    const repository = match[2];
    if (!repository || match[1] !== repository) {
      throw new Error(`Inventory repository label does not match its URL: ${line}`);
    }
    const head = {
      defaultBranch: match[4]?.replaceAll("`", "").trim() === "none"
        ? null
        : (match[4]?.replaceAll("`", "").trim() ?? null),
      commit: match[3] ?? null,
    };
    const previous = heads.get(repository);
    if (
      previous &&
      (previous.defaultBranch !== head.defaultBranch || previous.commit !== head.commit)
    ) {
      throw new Error(`Inventory contains conflicting pinned commits for ${repository}`);
    }
    heads.set(repository, head);
  }

  return heads;
}

export function compareRepositoryHeads(
  expected: Map<string, PinnedRepositoryHead>,
  actual: RepositoryHead[],
): InventoryMismatch[] {
  const current = new Map(actual.map((repository) => [repository.name, repository]));
  const mismatches: InventoryMismatch[] = [];

  for (const [name, expectedHead] of expected) {
    const repository = current.get(name);
    if (!repository) {
      mismatches.push({
        repository: name,
        expected: expectedHead.defaultBranch
          ? `${expectedHead.defaultBranch}: ${expectedHead.commit}`
          : "no default branch",
        actual: "repository not returned by GitHub",
      });
      continue;
    }

    const actualCommit =
      repository.defaultBranch === null || repository.commit === null
        ? null
        : repository.commit;
    if (
      repository.defaultBranch === null &&
      expectedHead.defaultBranch === null &&
      expectedHead.commit === null
    ) {
      continue;
    }
    if (
      expectedHead.defaultBranch !== repository.defaultBranch ||
      expectedHead.commit !== actualCommit
    ) {
      mismatches.push({
        repository: name,
        expected: expectedHead.defaultBranch
          ? `${expectedHead.defaultBranch}: ${expectedHead.commit}`
          : "no default branch",
        actual:
          actualCommit === null
            ? "no default branch"
            : `${repository.defaultBranch}: ${actualCommit}`,
      });
    }
  }

  for (const repository of actual) {
    if (!expected.has(repository.name)) {
      mismatches.push({
        repository: repository.name,
        expected: "repository absent from snapshot",
        actual:
          repository.defaultBranch === null || repository.commit === null
            ? "no default branch"
            : `${repository.defaultBranch}: ${repository.commit}`,
      });
    }
  }

  return mismatches;
}

export function parsePinnedRepositoryFiles(
  markdown: string,
): Map<string, PinnedRepositoryFiles> {
  const files = new Map<string, PinnedRepositoryFiles>();
  const rootHeading = "## Cross-repository release status measured 2026-11-03";
  const inventory = markdown.split(rootHeading, 2)[1];
  if (!inventory) {
    throw new Error("Cross-repository release status section was not found");
  }

  const rootTable = inventory.split(/\r?\n## /u, 1)[0] ?? "";
  for (const line of rootTable.split(/\r?\n/u)) {
    const fileRow = line.match(
      /^\| \[([^\]]+)\]\(https:\/\/github\.com\/AtmaOVictu\/([^/)`]+)\/blob\/([a-f0-9]{40})\/LICENSE\.md\) \| `([^`]+)` \| [^|]+ \| `([a-f0-9]{40})`\s+\| `([a-f0-9]{40})` \|$/u,
    );
    if (fileRow) {
      const label = requiredCapture(fileRow[1], "repository label");
      const repository = requiredCapture(fileRow[2], "repository name");
      const commit = requiredCapture(fileRow[3], "linked commit");
      const defaultBranch = requiredCapture(fileRow[4], "default branch");
      const blob = requiredCapture(fileRow[5], "license blob");
      const measuredCommit = requiredCapture(fileRow[6], "measured commit");
      if (label !== repository || commit !== measuredCommit) {
        throw new Error(`Root LICENSE.md evidence is inconsistent: ${line}`);
      }
      files.set(repository, {
        defaultBranch,
        commit,
        rootLicenseBlob: blob,
        draftBlob: null,
      });
      continue;
    }

    const missingRow = line.match(
      /^\| \[([^\]]+)\]\(https:\/\/github\.com\/AtmaOVictu\/([^/)`]+)\/tree\/([a-f0-9]{40})\) \| `([^`]+)` \| No readable root file at this path\s+\| `([a-f0-9]{40})` \|$/u,
    );
    if (missingRow) {
      const label = requiredCapture(missingRow[1], "repository label");
      const repository = requiredCapture(missingRow[2], "repository name");
      const commit = requiredCapture(missingRow[3], "linked commit");
      const defaultBranch = requiredCapture(missingRow[4], "default branch");
      const measuredCommit = requiredCapture(missingRow[5], "measured commit");
      if (label !== repository || commit !== measuredCommit) {
        throw new Error(`Missing root LICENSE.md evidence is inconsistent: ${line}`);
      }
      if (files.has(repository)) {
        throw new Error(`Duplicate root LICENSE.md status for ${repository}`);
      }
      files.set(repository, {
        defaultBranch,
        commit,
        rootLicenseBlob: null,
        draftBlob: null,
      });
      continue;
    }

    const noBranchRow = line.match(
      /^\| \[([^\]]+)\]\(https:\/\/github\.com\/AtmaOVictu\/([^/)`]+)\) \| none \| No default branch; root-file check unavailable \| none \|$/u,
    );
    if (noBranchRow) {
      const label = requiredCapture(noBranchRow[1], "repository label");
      const repository = requiredCapture(noBranchRow[2], "repository name");
      if (label !== repository || files.has(repository)) {
        throw new Error(`No-default-branch evidence is inconsistent: ${line}`);
      }
      files.set(repository, {
        defaultBranch: null,
        commit: null,
        rootLicenseBlob: null,
        draftBlob: null,
      });
    }
  }

  const draftTableHeading = "| Repository | Default ref | Measured draft path | Git blob | Measured commit |";
  const draftTable = inventory.split(draftTableHeading, 2)[1]?.split(/\r?\n/u).slice(2);
  if (!draftTable) {
    throw new Error("Measured draft inventory table was not found");
  }
  let draftRows = 0;
  for (const line of draftTable) {
    const draftRow = line.match(
      /^\| \[([^\]]+)\]\(https:\/\/github\.com\/AtmaOVictu\/([^/)`]+)\/blob\/([a-f0-9]{40})\/VBL-10\.5\.1-KOMPIL-A-DRAFT-NOT-RELEASED\.md\) \| `([^`]+)` \| `VBL-10\.5\.1-KOMPIL-A-DRAFT-NOT-RELEASED\.md` \| `([a-f0-9]{40})`\s+\| `([a-f0-9]{40})` \|$/u,
    );
    if (!draftRow) {
      if (line.startsWith("| ")) {
        break;
      }
      continue;
    }
    const label = requiredCapture(draftRow[1], "repository label");
    const repository = requiredCapture(draftRow[2], "repository name");
    const linkedCommit = requiredCapture(draftRow[3], "linked commit");
    const defaultBranch = requiredCapture(draftRow[4], "default branch");
    const blob = requiredCapture(draftRow[5], "draft blob");
    const measuredCommit = requiredCapture(draftRow[6], "measured commit");
    const entry = files.get(repository);
    if (
      label !== repository ||
      linkedCommit !== measuredCommit ||
      !entry ||
      entry.commit !== measuredCommit ||
      entry.defaultBranch !== defaultBranch ||
      entry.draftBlob !== null
    ) {
      throw new Error(`Measured draft evidence is inconsistent: ${line}`);
    }
    entry.draftBlob = blob;
    draftRows += 1;
  }
  if (files.size === 0 || draftRows === 0) {
    throw new Error("Repository or draft evidence tables are incomplete");
  }

  return files;
}

export function compareRepositoryFiles(
  expected: Map<string, PinnedRepositoryFiles>,
  actual: Map<string, RepositoryFileObjects>,
): InventoryMismatch[] {
  const mismatches: InventoryMismatch[] = [];

  for (const [repository, expectedFiles] of expected) {
    if (expectedFiles.commit === null) {
      continue;
    }
    const actualFiles = actual.get(repository);
    if (!actualFiles) {
      mismatches.push({
        repository,
        expected: "file objects at pinned commit",
        actual: "repository object not returned by GitHub",
      });
      continue;
    }
    if (expectedFiles.rootLicenseBlob !== actualFiles.rootLicense) {
      mismatches.push({
        repository,
        expected: expectedFiles.rootLicenseBlob ?? "no root LICENSE.md object",
        actual: actualFiles.rootLicense ?? "no root LICENSE.md object",
      });
    }
    if (
      expectedFiles.draftBlob !== null &&
      expectedFiles.draftBlob !== actualFiles.draft
    ) {
      mismatches.push({
        repository,
        expected: `draft blob ${expectedFiles.draftBlob}`,
        actual: actualFiles.draft ? `draft blob ${actualFiles.draft}` : "no draft object",
      });
    }
  }

  return mismatches;
}

function readRepositoryFiles(
  expected: Map<string, PinnedRepositoryFiles>,
): Map<string, RepositoryFileObjects> {
  const repositories = [...expected].filter(([, entry]) => entry.commit !== null);
  const fields = repositories.map(([name, entry], index) => {
    const commit = entry.commit;
    if (!commit) {
      throw new Error(`Missing pinned commit for ${name}`);
    }
    const repositoryAlias = `repo${index}`;
    const rootAlias = `root${index}`;
    const draftAlias = entry.draftBlob === null ? null : `draft${index}`;
    return {
      name,
      repositoryAlias,
      rootAlias,
      draftAlias,
      query: `${repositoryAlias}: repository(owner: "AtmaOVictu", name: ${JSON.stringify(name)}) {
        ${rootAlias}: object(expression: "${commit}:LICENSE.md") { oid }
        ${draftAlias ? `${draftAlias}: object(expression: "${commit}:VBL-10.5.1-KOMPIL-A-DRAFT-NOT-RELEASED.md") { oid }` : ""}
      }`,
    };
  });
  const query = `query {\n${fields.map((field) => field.query).join("\n")}\n}`;
  const response = JSON.parse(
    execFileSync("gh", ["api", "graphql", "-f", `query=${query}`], {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "inherit"],
      maxBuffer: 1024 * 1024,
    }),
  ) as {
    data?: Record<string, Record<string, { oid?: string } | null> | null>;
  };
  if (!response.data) {
    throw new Error("GitHub file-object response was incomplete");
  }

  const objects = new Map<string, RepositoryFileObjects>();
  for (const field of fields) {
    const repository = response.data[field.repositoryAlias];
    if (!repository) {
      throw new Error(`GitHub did not return repository ${field.name} for the pinned file check`);
    }
    const root = repository[field.rootAlias];
    const draft = field.draftAlias ? repository[field.draftAlias] : null;
    if (
      (root !== null && typeof root?.oid !== "string") ||
      (draft !== null && typeof draft?.oid !== "string")
    ) {
      throw new Error(`GitHub returned an invalid Git object for ${field.name}`);
    }
    objects.set(field.name, {
      rootLicense: root?.oid ?? null,
      draft: draft?.oid ?? null,
    });
  }

  return objects;
}

export function readRepositoryHeads(): RepositoryHead[] {
  const response = JSON.parse(
    execFileSync("gh", ["api", "graphql", "-f", `query=${GRAPHQL_QUERY}`], {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "inherit"],
    }),
  ) as {
    data?: {
      user?: {
        repositories?: {
          pageInfo?: { hasNextPage?: boolean };
          nodes?: Array<{
            name?: string;
            defaultBranchRef?: {
              name?: string;
              target?: { oid?: string };
            } | null;
          }>;
        };
      };
    };
  };
  const repositoryConnection = response.data?.user?.repositories;
  if (!repositoryConnection?.nodes || repositoryConnection.pageInfo?.hasNextPage) {
    throw new Error("GitHub repository response was incomplete; expected at most 100 repositories");
  }

  return repositoryConnection.nodes.map((repository) => {
    if (!repository.name) {
      throw new Error("GitHub repository response contained an unnamed repository");
    }
    const branch = repository.defaultBranchRef;
    if (!branch) {
      return { name: repository.name, defaultBranch: null, commit: null };
    }
    if (!branch.name || !branch.target?.oid) {
      throw new Error(`GitHub did not return a commit for ${repository.name}'s default branch`);
    }
    return {
      name: repository.name,
      defaultBranch: branch.name,
      commit: branch.target.oid,
    };
  });
}

async function main(): Promise<void> {
  const start = new Date();
  const markdown = await readFile(
    fileURLToPath(new URL("../../LICENSE-TONGUES.md", import.meta.url)),
    "utf8",
  );
  const expected = parsePinnedRepositoryHeads(markdown);
  const expectedFiles = parsePinnedRepositoryFiles(markdown);
  if (expected.size !== 54 || expectedFiles.size !== 54) {
    throw new Error(
      `Expected 54 matching head and file-status rows, found ${expected.size} and ${expectedFiles.size}`,
    );
  }
  for (const [repository, expectedHead] of expected) {
    const fileEvidence = expectedFiles.get(repository);
    if (
      !fileEvidence ||
      expectedHead.defaultBranch !== fileEvidence.defaultBranch ||
      expectedHead.commit !== fileEvidence.commit
    ) {
      throw new Error(`Head and file evidence disagree for ${repository}`);
    }
  }

  const actual = readRepositoryHeads();
  const headMismatches = compareRepositoryHeads(expected, actual);
  const actualFiles = readRepositoryFiles(expectedFiles);
  const end = new Date();
  const fileMismatches = compareRepositoryFiles(expectedFiles, actualFiles);
  console.log(
    `Rechecked ${actual.length} repositories from ${start.toISOString()} to ${end.toISOString()}.`,
  );
  console.log(
    `Inventory snapshot: ${expected.size} repositories; current heads: ${actual.length}; head mismatches: ${headMismatches.length}.`,
  );
  console.log(
    `Pinned root LICENSE.md objects: ${[...expectedFiles.values()].filter((entry) => entry.commit !== null && entry.rootLicenseBlob !== null).length} present, ${[...expectedFiles.values()].filter((entry) => entry.commit !== null && entry.rootLicenseBlob === null).length} absent; mismatches: ${fileMismatches.length}.`,
  );
  console.log(
    `Recorded draft objects checked: ${[...expectedFiles.values()].filter((entry) => entry.draftBlob !== null).length}.`,
  );
  const mismatches = [...headMismatches, ...fileMismatches];
  if (mismatches.length > 0) {
    for (const mismatch of mismatches) {
      console.error(
        `${mismatch.repository}: expected ${mismatch.expected}; current ${mismatch.actual}`,
      );
    }
    process.exitCode = 1;
    return;
  }

  console.log(
    "All repository names, default branches, pinned commit SHAs, and recorded Git object IDs match.",
  );
}

const invokedPath = process.argv[1];
if (invokedPath && import.meta.url === pathToFileURL(invokedPath).href) {
  main().catch((error: unknown) => {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  });
}
