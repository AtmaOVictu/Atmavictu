import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import test from "node:test";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

import { parseAtmaCliArgs } from "./atmaCli.js";
import type { WorkbenchManifest } from "./workbenchManifest.js";
import { MANIFEST_FILE_NAME } from "./workbenchManifestRepository.js";

const execFileAsync = promisify(execFile);

test("parseAtmaCliArgs rejects unknown command", () => {
  assert.throws(
    () => parseAtmaCliArgs(["unknown", "C:/temp/project"]),
    /Unknown command: unknown/,
  );
});

test("parseAtmaCliArgs rejects missing projectRoot", () => {
  assert.throws(
    () => parseAtmaCliArgs(["show"]),
    /show requires <projectRoot>/,
  );
});

test("atma CLI capture command prints consequence and persists files", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "atmavictu-cli-capture-"));

  try {
    const cliPath = fileURLToPath(new URL("./atmaCli.js", import.meta.url));
    const title = "Seed text";
    const body = "Prvi vhodni tekst.";
    const { stdout } = await execFileAsync(
      process.execPath,
      [cliPath, "capture", projectRoot, title, body],
      { cwd: projectRoot },
    );

    const manifestPath = join(projectRoot, MANIFEST_FILE_NAME);
    const bodyFilePath = join(projectRoot, "incoming", "incoming-0001.txt");
    const rawManifest = await readFile(manifestPath, "utf8");
    const manifest = JSON.parse(rawManifest) as WorkbenchManifest;
    const bodyContent = await readFile(bodyFilePath, "utf8");

    assert.match(stdout, /^POSLEDICA/m);
    assert.match(stdout, /MANIFEST SLED: incoming\/incoming-0001\.txt/);
    assert.match(stdout, /TRENUTNO STANJE: CAPTURED/);
    assert.equal(bodyContent, body);
    assert.equal(manifest.incomingTexts[0]?.sourcePath, "incoming/incoming-0001.txt");
    assert.equal("body" in (manifest.incomingTexts[0] as unknown as Record<string, unknown>), false);
  } finally {
    await rm(projectRoot, { force: true, recursive: true });
  }
});

test("atma CLI show command prints manifest summary", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "atmavictu-cli-show-"));

  try {
    const cliPath = fileURLToPath(new URL("./atmaCli.js", import.meta.url));
    await execFileAsync(
      process.execPath,
      [cliPath, "capture", projectRoot, "Seed text", "Prvi vhodni tekst."],
      { cwd: projectRoot },
    );

    const { stdout } = await execFileAsync(process.execPath, [cliPath, "show", projectRoot], {
      cwd: projectRoot,
    });

    assert.match(stdout, /^ATMAVICTU WORKBENCH/m);
    assert.match(stdout, /MANIFEST VERSION: 2/);
    assert.match(stdout, /INCOMING TEXTS: 1/);
    assert.match(stdout, /FRAGMENTS: 0/);
    assert.match(stdout, /INSERTIONS: 0/);
    assert.match(stdout, /LAST SOURCE: incoming\/incoming-0001\.txt/);
    assert.match(stdout, /LAST STATUS: new/);
  } finally {
    await rm(projectRoot, { force: true, recursive: true });
  }
});

test("atma CLI verify command prints pass for valid manifest", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "atmavictu-cli-verify-pass-"));

  try {
    const cliPath = fileURLToPath(new URL("./atmaCli.js", import.meta.url));
    await execFileAsync(
      process.execPath,
      [cliPath, "capture", projectRoot, "Seed text", "Prvi vhodni tekst."],
      { cwd: projectRoot },
    );

    const { stdout } = await execFileAsync(process.execPath, [cliPath, "verify", projectRoot], {
      cwd: projectRoot,
    });

    assert.match(stdout, /^VERIFY: PASS/m);
    assert.match(stdout, /ERRORS: 0/);
  } finally {
    await rm(projectRoot, { force: true, recursive: true });
  }
});

test("atma CLI verify command prints fail and validation errors for invalid manifest", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "atmavictu-cli-verify-fail-"));

  try {
    const cliPath = fileURLToPath(new URL("./atmaCli.js", import.meta.url));
    const manifestPath = join(projectRoot, MANIFEST_FILE_NAME);
    const invalidManifest = {
      manifestVersion: "2",
      incomingTexts: [
        {
          id: "incoming-0001",
          sourcePath: "C:/Users/Luka/secret.txt",
          status: "new",
        },
      ],
      fragments: [],
      insertions: [],
    } satisfies WorkbenchManifest;

    await writeFile(manifestPath, `${JSON.stringify(invalidManifest, null, 2)}\n`, "utf8");

    const { stdout } = await execFileAsync(process.execPath, [cliPath, "verify", projectRoot], {
      cwd: projectRoot,
    });

    assert.match(stdout, /^VERIFY: FAIL/m);
    assert.match(stdout, /ERRORS:/);
    assert.match(stdout, /sourcePath must be a relative path/);
  } finally {
    await rm(projectRoot, { force: true, recursive: true });
  }
});
