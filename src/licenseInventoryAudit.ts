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

function readRepositoryHeads(): RepositoryHead[] {
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
  if (expected.size === 0) {
    throw new Error("No repository rows were found in the documented inventory");
  }

  const actual = readRepositoryHeads();
  const end = new Date();
  const mismatches = compareRepositoryHeads(expected, actual);
  console.log(
    `Rechecked ${actual.length} repositories from ${start.toISOString()} to ${end.toISOString()}.`,
  );
  console.log(
    `Inventory snapshot: ${expected.size} repositories; current heads: ${actual.length}; mismatches: ${mismatches.length}.`,
  );
  if (mismatches.length > 0) {
    for (const mismatch of mismatches) {
      console.error(
        `${mismatch.repository}: expected ${mismatch.expected}; current ${mismatch.actual}`,
      );
    }
    process.exitCode = 1;
    return;
  }

  console.log("All repository names, default branches, and pinned commit SHAs match.");
}

const invokedPath = process.argv[1];
if (invokedPath && import.meta.url === pathToFileURL(invokedPath).href) {
  main().catch((error: unknown) => {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  });
}
