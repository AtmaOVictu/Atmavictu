import { execFileSync } from "node:child_process";
import { readFile } from "node:fs/promises";
import { fileURLToPath, pathToFileURL } from "node:url";
import {
  parsePinnedRepositoryFiles,
  parsePinnedRepositoryHeads,
  readRepositoryHeads,
  type RepositoryHead,
} from "./licenseInventoryAudit.js";

interface GitTreeEntry {
  path?: string;
  sha?: string;
  type?: string;
}

interface GitTreeResponse {
  truncated?: boolean;
  tree?: GitTreeEntry[];
}

export interface LicensePathCandidate {
  repository: string;
  commit: string;
  path: string;
  blob: string;
}

export interface LicensePathMatch {
  path: string;
  blob: string;
}

export interface MissingRootLicenseSummary {
  repositoriesWithCandidates: number;
  repositoriesWithRootAlternatives: number;
  repositoriesWithNestedOnly: number;
  rootAlternativePaths: number;
  uniqueRootAlternativeBlobs: number;
  nestedCandidatePaths: number;
}

const LICENSE_BASENAME_PATTERN =
  /^(?:licen[cs]e(?:e|ing)?|copying|copyright|notice|patents?)(?:[-_.].*)?$/iu;
const SOURCE_EXTENSIONS = new Set([
  "c",
  "cc",
  "cpp",
  "cs",
  "go",
  "h",
  "hpp",
  "java",
  "js",
  "jsx",
  "kt",
  "m",
  "php",
  "py",
  "rb",
  "rs",
  "sh",
  "swift",
  "ts",
  "tsx",
]);

export function findLicensePathCandidates(
  entries: GitTreeEntry[],
): LicensePathMatch[] {
  return entries
    .filter(
      (entry): entry is GitTreeEntry & { path: string; type: string } =>
        entry.type === "blob" && typeof entry.path === "string",
    )
    .flatMap((entry): LicensePathMatch[] => {
      const basename = entry.path.split("/").at(-1) ?? "";
      const extension = basename.match(/\.([^.]+)$/u)?.[1]?.toLowerCase();
      const isCandidate =
        LICENSE_BASENAME_PATTERN.test(basename) &&
        (extension === undefined || !SOURCE_EXTENSIONS.has(extension));
      if (!isCandidate) {
        return [];
      }
      if (typeof entry.sha !== "string" || !/^[a-f0-9]{40}$/iu.test(entry.sha)) {
        throw new Error(`GitHub returned no valid blob SHA for ${entry.path}`);
      }
      return [{ path: entry.path, blob: entry.sha }];
    })
    .sort((left, right) => left.path.localeCompare(right.path));
}

export function requireMatchingRepositoryNames(
  expectedNames: Set<string>,
  current: RepositoryHead[],
): RepositoryHead[] {
  const actualNames = new Set(current.map((repository) => repository.name));
  if (actualNames.size !== current.length) {
    throw new Error("GitHub returned duplicate repository names");
  }
  const missing = [...expectedNames].filter((name) => !actualNames.has(name));
  const unexpected = [...actualNames].filter((name) => !expectedNames.has(name));
  if (missing.length > 0 || unexpected.length > 0) {
    throw new Error(
      `Repository set differs from LICENSE-TONGUES.md; missing: ${missing.join(", ") || "none"}; unexpected: ${unexpected.join(", ") || "none"}`,
    );
  }
  return current;
}

export function summarizeMissingRootLicenseCandidates(
  candidates: LicensePathCandidate[],
  repositoriesWithoutRootLicense: Set<string>,
): MissingRootLicenseSummary {
  const grouped = new Map<string, { root: number; nested: number }>();
  const rootBlobs = new Set<string>();
  for (const candidate of candidates) {
    if (!repositoriesWithoutRootLicense.has(candidate.repository)) {
      continue;
    }
    const counts = grouped.get(candidate.repository) ?? { root: 0, nested: 0 };
    if (candidate.path.includes("/")) {
      counts.nested += 1;
    } else {
      counts.root += 1;
      rootBlobs.add(candidate.blob);
    }
    grouped.set(candidate.repository, counts);
  }

  const counts = [...grouped.values()];
  const withRootAlternatives = counts.filter((entry) => entry.root > 0);
  const nestedOnly = counts.filter(
    (entry) => entry.root === 0 && entry.nested > 0,
  );
  return {
    repositoriesWithCandidates: grouped.size,
    repositoriesWithRootAlternatives: withRootAlternatives.length,
    repositoriesWithNestedOnly: nestedOnly.length,
    rootAlternativePaths: withRootAlternatives.reduce(
      (total, entry) => total + entry.root,
      0,
    ),
    uniqueRootAlternativeBlobs: rootBlobs.size,
    nestedCandidatePaths: counts.reduce(
      (total, entry) => total + entry.nested,
      0,
    ),
  };
}

function readRepositoryTree(repository: string, commit: string): GitTreeEntry[] {
  const response = JSON.parse(
    execFileSync(
      "gh",
      [
        "api",
        `repos/AtmaOVictu/${repository}/git/trees/${commit}?recursive=1`,
      ],
      {
        encoding: "utf8",
        stdio: ["ignore", "pipe", "inherit"],
        maxBuffer: 16 * 1024 * 1024,
      },
    ),
  ) as GitTreeResponse;
  if (response.truncated) {
    throw new Error(`GitHub returned a truncated tree for ${repository}@${commit}`);
  }
  if (!Array.isArray(response.tree)) {
    throw new Error(`GitHub returned no tree entries for ${repository}@${commit}`);
  }
  return response.tree;
}

async function main(): Promise<void> {
  const started = new Date();
  const markdown = await readFile(
    fileURLToPath(new URL("../../LICENSE-TONGUES.md", import.meta.url)),
    "utf8",
  );
  const heads = parsePinnedRepositoryHeads(markdown);
  const fileEvidence = parsePinnedRepositoryFiles(markdown);
  if (heads.size !== 54) {
    throw new Error(`Expected 54 repository rows, found ${heads.size}`);
  }
  const currentHeads = requireMatchingRepositoryNames(
    new Set(heads.keys()),
    readRepositoryHeads(),
  );

  const candidates: LicensePathCandidate[] = [];
  let scannedRepositories = 0;
  let repositoriesWithoutDefaultBranch = 0;
  for (const head of currentHeads) {
    const repository = head.name;
    if (head.commit === null) {
      repositoriesWithoutDefaultBranch += 1;
      continue;
    }
    const entries = readRepositoryTree(repository, head.commit);
    for (const candidate of findLicensePathCandidates(entries)) {
      candidates.push({ repository, commit: head.commit, ...candidate });
    }
    scannedRepositories += 1;
  }
  const ended = new Date();

  console.log(
    `Scanned ${scannedRepositories} current default-branch trees from ${started.toISOString()} to ${ended.toISOString()}; ${repositoriesWithoutDefaultBranch} repositories had no default branch; found ${candidates.length} license-name path candidates.`,
  );
  console.log("Repository names are required to match LICENSE-TONGUES.md; each path row includes the measured head commit SHA and Git blob SHA.");
  console.log("Candidates are path-name matches only; blob SHAs identify exact Git objects but this scan does not fetch file contents or determine legal effect.");
  const repositoriesWithoutRootLicense = new Set(
    [...fileEvidence]
      .filter(
        ([, evidence]) =>
          evidence.commit !== null && evidence.rootLicenseBlob === null,
      )
      .map(([repository]) => repository),
  );
  const summary = summarizeMissingRootLicenseCandidates(
    candidates,
    repositoriesWithoutRootLicense,
  );
  console.log(
    `Among ${repositoriesWithoutRootLicense.size} repositories with no recorded root LICENSE.md: ${summary.repositoriesWithCandidates} have name-matched candidates (${summary.repositoriesWithRootAlternatives} with root-level alternatives, ${summary.repositoriesWithNestedOnly} with nested candidates only); ${summary.rootAlternativePaths} root-level paths map to ${summary.uniqueRootAlternativeBlobs} unique blobs, alongside ${summary.nestedCandidatePaths} nested paths.`,
  );
  for (const candidate of candidates) {
    console.log(
      `${candidate.repository}@${candidate.commit} ${candidate.path} blob:${candidate.blob}`,
    );
  }
}

const invokedPath = process.argv[1];
if (invokedPath && import.meta.url === pathToFileURL(invokedPath).href) {
  main().catch((error: unknown) => {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  });
}
