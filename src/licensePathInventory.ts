import { execFileSync } from "node:child_process";
import { readFile } from "node:fs/promises";
import { fileURLToPath, pathToFileURL } from "node:url";
import {
  parsePinnedRepositoryFiles,
  parsePinnedRepositoryHeads,
  readRepositoryHeads,
  type PinnedRepositoryFiles,
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

export interface MissingRootLicenseBlobGroup {
  blob: string;
  candidates: LicensePathCandidate[];
}

export interface RootLicenseEvidenceChange {
  repository: string;
  recordedDefaultBranch: string | null;
  recordedCommit: string | null;
  recordedBlob: string | null;
  currentCommit: string;
  currentBlob: string | null;
}

export interface LicensePathAuditReport {
  schemaVersion: 1;
  measured: {
    startedAt: string;
    endedAt: string;
  };
  scan: {
    scannedRepositories: number;
    repositoriesWithoutDefaultBranch: number;
    candidatesFound: number;
  };
  rootLicenseStatus: {
    repositoriesScanned: number;
    presentAtCurrentHeads: number;
    absentAtCurrentHeads: number;
    changedSinceRecordedInventory: number;
  };
  rootLicenseChanges: RootLicenseEvidenceChange[];
  scope: "all-name-matched-paths" | "root-alternatives-without-current-root-license";
  repositoriesWithoutCurrentRootLicense: number;
  summary: MissingRootLicenseSummary;
  candidates: LicensePathCandidate[];
  groups: MissingRootLicenseBlobGroup[];
  limitation: string;
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

export function groupMissingRootLicenseAlternatives(
  candidates: LicensePathCandidate[],
  repositoriesWithoutRootLicense: Set<string>,
): MissingRootLicenseBlobGroup[] {
  const groups = new Map<string, LicensePathCandidate[]>();
  for (const candidate of candidates) {
    if (
      !repositoriesWithoutRootLicense.has(candidate.repository) ||
      candidate.path.includes("/")
    ) {
      continue;
    }
    const matches = groups.get(candidate.blob) ?? [];
    matches.push(candidate);
    groups.set(candidate.blob, matches);
  }
  return [...groups]
    .map(([blob, matches]) => ({
      blob,
      candidates: matches.sort(
        (left, right) =>
          left.repository.localeCompare(right.repository) ||
          left.path.localeCompare(right.path),
      ),
    }))
    .sort((left, right) => left.blob.localeCompare(right.blob));
}

export function summarizeCurrentRootLicenseStatus(
  expectedFiles: Map<string, PinnedRepositoryFiles>,
  scannedHeads: Map<string, string>,
  currentRootBlobs: Map<string, string>,
): LicensePathAuditReport["rootLicenseStatus"] {
  let presentAtCurrentHeads = 0;
  const changes = describeRootLicenseEvidenceChanges(
    expectedFiles,
    scannedHeads,
    currentRootBlobs,
  );
  for (const repository of scannedHeads.keys()) {
    const recorded = expectedFiles.get(repository);
    if (!recorded) {
      throw new Error(`No recorded root-license evidence for ${repository}`);
    }
    if (currentRootBlobs.has(repository)) {
      presentAtCurrentHeads += 1;
    }
  }
  return {
    repositoriesScanned: scannedHeads.size,
    presentAtCurrentHeads,
    absentAtCurrentHeads: scannedHeads.size - presentAtCurrentHeads,
    changedSinceRecordedInventory: changes.length,
  };
}

export function describeRootLicenseEvidenceChanges(
  expectedFiles: Map<string, PinnedRepositoryFiles>,
  scannedHeads: Map<string, string>,
  currentRootBlobs: Map<string, string>,
): RootLicenseEvidenceChange[] {
  const changes: RootLicenseEvidenceChange[] = [];
  for (const [repository, currentCommit] of scannedHeads) {
    const recorded = expectedFiles.get(repository);
    if (!recorded) {
      throw new Error(`No recorded root-license evidence for ${repository}`);
    }
    const currentBlob = currentRootBlobs.get(repository) ?? null;
    if (recorded.rootLicenseBlob === currentBlob) {
      continue;
    }
    changes.push({
      repository,
      recordedDefaultBranch: recorded.defaultBranch,
      recordedCommit: recorded.commit,
      recordedBlob: recorded.rootLicenseBlob,
      currentCommit,
      currentBlob,
    });
  }
  return changes.sort((left, right) =>
    left.repository.localeCompare(right.repository),
  );
}

export function createLicensePathAuditReport(input: {
  startedAt: Date;
  endedAt: Date;
  scannedRepositories: number;
  repositoriesWithoutDefaultBranch: number;
  candidates: LicensePathCandidate[];
  expectedFiles: Map<string, PinnedRepositoryFiles>;
  scannedHeads: Map<string, string>;
  currentRootBlobs: Map<string, string>;
  focused: boolean;
}): LicensePathAuditReport {
  const repositoriesWithoutCurrentRootLicense = new Set(
    [...input.scannedHeads.keys()].filter(
      (repository) => !input.currentRootBlobs.has(repository),
    ),
  );
  const rootLicenseStatus = summarizeCurrentRootLicenseStatus(
    input.expectedFiles,
    input.scannedHeads,
    input.currentRootBlobs,
  );
  const rootLicenseChanges = describeRootLicenseEvidenceChanges(
    input.expectedFiles,
    input.scannedHeads,
    input.currentRootBlobs,
  );
  return {
    schemaVersion: 1,
    measured: {
      startedAt: input.startedAt.toISOString(),
      endedAt: input.endedAt.toISOString(),
    },
    scan: {
      scannedRepositories: input.scannedRepositories,
      repositoriesWithoutDefaultBranch: input.repositoriesWithoutDefaultBranch,
      candidatesFound: input.candidates.length,
    },
    rootLicenseStatus,
    rootLicenseChanges,
    scope: input.focused
      ? "root-alternatives-without-current-root-license"
      : "all-name-matched-paths",
    repositoriesWithoutCurrentRootLicense:
      repositoriesWithoutCurrentRootLicense.size,
    summary: summarizeMissingRootLicenseCandidates(
      input.candidates,
      repositoriesWithoutCurrentRootLicense,
    ),
    candidates: input.focused ? [] : input.candidates,
    groups: input.focused
      ? groupMissingRootLicenseAlternatives(
          input.candidates,
          repositoriesWithoutCurrentRootLicense,
        )
      : [],
    limitation:
      "Current root-path presence and Git object identities are measured at the scanned heads; path-name matches remain review leads only, and this scan does not fetch file contents or determine legal effect.",
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
  const args = process.argv.slice(2);
  if (
    args.some(
      (argument) =>
        argument !== "--focus-missing-root" && argument !== "--json",
    )
  ) {
    throw new Error(
      `Unknown argument: ${args.find((argument) => argument !== "--focus-missing-root" && argument !== "--json")}`,
    );
  }
  const focusMissingRoot = args.includes("--focus-missing-root");
  const jsonOutput = args.includes("--json");
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
  const currentRootBlobs = new Map<string, string>();
  const scannedHeads = new Map<string, string>();
  let scannedRepositories = 0;
  let repositoriesWithoutDefaultBranch = 0;
  for (const head of currentHeads) {
    const repository = head.name;
    if (head.commit === null) {
      repositoriesWithoutDefaultBranch += 1;
      continue;
    }
    const entries = readRepositoryTree(repository, head.commit);
    scannedHeads.set(repository, head.commit);
    const rootLicenseEntry = entries.find(
      (entry) =>
        entry.path === "LICENSE.md" && entry.type === "blob",
    );
    if (rootLicenseEntry) {
      if (
        typeof rootLicenseEntry.sha !== "string" ||
        !/^[a-f0-9]{40}$/iu.test(rootLicenseEntry.sha)
      ) {
        throw new Error(
          `GitHub returned no valid root LICENSE.md blob SHA for ${repository}@${head.commit}`,
        );
      }
      currentRootBlobs.set(repository, rootLicenseEntry.sha);
    }
    for (const candidate of findLicensePathCandidates(entries)) {
      candidates.push({ repository, commit: head.commit, ...candidate });
    }
    scannedRepositories += 1;
  }
  const ended = new Date();

  if (jsonOutput) {
    console.log(
      JSON.stringify(
        createLicensePathAuditReport({
          startedAt: started,
          endedAt: ended,
          scannedRepositories,
          repositoriesWithoutDefaultBranch,
          candidates,
          expectedFiles: fileEvidence,
          scannedHeads,
          currentRootBlobs,
          focused: focusMissingRoot,
        }),
        null,
        2,
      ),
    );
    return;
  }
  console.log(
    `Scanned ${scannedRepositories} current default-branch trees from ${started.toISOString()} to ${ended.toISOString()}; ${repositoriesWithoutDefaultBranch} repositories had no default branch; found ${candidates.length} license-name path candidates.`,
  );
  console.log(
    "Repository names are required to match LICENSE-TONGUES.md; each path row includes the measured head commit SHA and Git blob SHA.",
  );
  console.log(
    "Candidates are path-name matches only; blob SHAs identify exact Git objects but this scan does not fetch file contents or determine legal effect.",
  );
  const rootLicenseStatus = summarizeCurrentRootLicenseStatus(
    fileEvidence,
    scannedHeads,
    currentRootBlobs,
  );
  const rootLicenseChanges = describeRootLicenseEvidenceChanges(
    fileEvidence,
    scannedHeads,
    currentRootBlobs,
  );
  const repositoriesWithoutCurrentRootLicense = new Set(
    [...scannedHeads.keys()].filter(
      (repository) => !currentRootBlobs.has(repository),
    ),
  );
  console.log(
    `Current root LICENSE.md status: ${rootLicenseStatus.presentAtCurrentHeads} present, ${rootLicenseStatus.absentAtCurrentHeads} absent among ${rootLicenseStatus.repositoriesScanned} scanned repositories; ${rootLicenseStatus.changedSinceRecordedInventory} differ from recorded path/blob evidence.`,
  );
  for (const change of rootLicenseChanges) {
    console.log(
      `${change.repository}: recorded ${change.recordedDefaultBranch ?? "no default branch"}@${change.recordedCommit ?? "none"} blob:${change.recordedBlob ?? "absent"}; current ${change.currentCommit} blob:${change.currentBlob ?? "absent"}`,
    );
  }
  const summary = summarizeMissingRootLicenseCandidates(
    candidates,
    repositoriesWithoutCurrentRootLicense,
  );
  console.log(
    `Among ${repositoriesWithoutCurrentRootLicense.size} repositories with no current root LICENSE.md: ${summary.repositoriesWithCandidates} have name-matched candidates (${summary.repositoriesWithRootAlternatives} with root-level alternatives, ${summary.repositoriesWithNestedOnly} with nested candidates only); ${summary.rootAlternativePaths} root-level paths map to ${summary.uniqueRootAlternativeBlobs} unique blobs, alongside ${summary.nestedCandidatePaths} nested paths.`,
  );
  if (focusMissingRoot) {
    console.log(
      "Root-level name matches for repositories without a current root LICENSE.md, grouped by Git blob:",
    );
    for (const group of groupMissingRootLicenseAlternatives(
      candidates,
      repositoriesWithoutCurrentRootLicense,
    )) {
      const locations = group.candidates
        .map(
          (candidate) =>
            `${candidate.repository}@${candidate.commit} ${candidate.path}`,
        )
        .join("; ");
      console.log(`blob:${group.blob} ${locations}`);
    }
  } else {
    for (const candidate of candidates) {
      console.log(
        `${candidate.repository}@${candidate.commit} ${candidate.path} blob:${candidate.blob}`,
      );
    }
  }
}

const invokedPath = process.argv[1];
if (invokedPath && import.meta.url === pathToFileURL(invokedPath).href) {
  main().catch((error: unknown) => {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  });
}
