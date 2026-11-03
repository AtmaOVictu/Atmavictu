import { execFileSync } from "node:child_process";
import { readFile } from "node:fs/promises";
import { fileURLToPath, pathToFileURL } from "node:url";
import { parsePinnedRepositoryHeads } from "./licenseInventoryAudit.js";

interface GitTreeEntry {
  path?: string;
  type?: string;
}

interface GitTreeResponse {
  truncated?: boolean;
  tree?: GitTreeEntry[];
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

export function findLicensePathCandidates(entries: GitTreeEntry[]): string[] {
  return entries
    .filter(
      (entry): entry is GitTreeEntry & { path: string; type: string } =>
        entry.type === "blob" && typeof entry.path === "string",
    )
    .filter((entry) => {
      const basename = entry.path.split("/").at(-1) ?? "";
      const extension = basename.match(/\.([^.]+)$/u)?.[1]?.toLowerCase();
      return (
        LICENSE_BASENAME_PATTERN.test(basename) &&
        (extension === undefined || !SOURCE_EXTENSIONS.has(extension))
      );
    })
    .map((entry) => entry.path)
    .sort((left, right) => left.localeCompare(right));
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
  if (heads.size !== 54) {
    throw new Error(`Expected 54 repository rows, found ${heads.size}`);
  }

  const candidates: Array<{ repository: string; commit: string; path: string }> = [];
  let scannedRepositories = 0;
  for (const [repository, head] of heads) {
    if (head.commit === null) {
      continue;
    }
    const entries = readRepositoryTree(repository, head.commit);
    for (const path of findLicensePathCandidates(entries)) {
      candidates.push({ repository, commit: head.commit, path });
    }
    scannedRepositories += 1;
  }
  const ended = new Date();

  console.log(
    `Scanned ${scannedRepositories} pinned repository trees from ${started.toISOString()} to ${ended.toISOString()}; found ${candidates.length} license-name path candidates.`,
  );
  console.log(
    "Candidates are path-name matches only; this scan does not read file contents or determine legal effect.",
  );
  for (const candidate of candidates) {
    console.log(
      `${candidate.repository}@${candidate.commit} ${candidate.path}`,
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
