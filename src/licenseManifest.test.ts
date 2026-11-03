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
