import assert from "node:assert/strict";
import { execFile, execFileSync } from "node:child_process";
import { existsSync } from "node:fs";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
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

test("atma CLI full ninefold path runs headless: capture-to-insert with verify", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "atmavictu-cli-walk-"));
  try {
    const cliPath = fileURLToPath(new URL("./atmaCli.js", import.meta.url));
    const { stdout } = await execFileAsync(
      process.execPath,
      [cliPath, "walk", projectRoot, "Naslov", "Vsebina vira.", "Odlomek iz vira.", "poglavja/01-uvod.md"],
      { cwd: projectRoot },
    );
    assert.match(stdout, /^POSLEDICA/m);
    assert.match(stdout, /STATUS: processing/);
    assert.match(stdout, /TARGET: poglavja\/01-uvod\.md/);
    assert.match(stdout, /^VERIFY: PASS/m);
    const rawManifest = await readFile(join(projectRoot, MANIFEST_FILE_NAME), "utf8");
    const manifest = JSON.parse(rawManifest) as WorkbenchManifest;
    assert.equal(manifest.incomingTexts[0]?.status, "used");
    assert.equal(manifest.fragments[0]?.status, "inserted");
    assert.equal(manifest.insertions.length, 1);
  } finally {
    await rm(projectRoot, { force: true, recursive: true });
  }
});

test("atma CLI start-processing and archives run headless", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "atmavictu-cli-nine-"));
  try {
    const cliPath = fileURLToPath(new URL("./atmaCli.js", import.meta.url));
    const run = (args: string[]) =>
      execFileAsync(process.execPath, [cliPath, ...args], { cwd: projectRoot });
    await run(["walk", projectRoot, "Naslov", "Vsebina vira.", "Odlomek.", "poglavja/uvod.md"]);
    const rawWalk = await readFile(join(projectRoot, MANIFEST_FILE_NAME), "utf8");
    const walked = JSON.parse(rawWalk) as WorkbenchManifest;
    const fragmentId = walked.fragments[0]?.id ?? "";
    const incomingId = walked.incomingTexts[0]?.id ?? "";
    const archivedFragment = await run(["archive-fragment", projectRoot, fragmentId]);
    assert.match(archivedFragment.stdout, /STATUS: archived/);
    const archivedIncoming = await run(["archive-incoming", projectRoot, incomingId]);
    assert.match(archivedIncoming.stdout, /STATUS: archived/);
    const verify = await run(["verify", projectRoot]);
    assert.match(verify.stdout, /^VERIFY: PASS/m);
  } finally {
    await rm(projectRoot, { force: true, recursive: true });
  }
});

test("atma CLI update commands and add-concept run headless", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "atmavictu-cli-update-"));
  try {
    const cliPath = fileURLToPath(new URL("./atmaCli.js", import.meta.url));
    const run = (args: string[]) =>
      execFileAsync(process.execPath, [cliPath, ...args], { cwd: projectRoot });
    await run(["walk", projectRoot, "Naslov", "Vsebina vira.", "Odlomek.", "poglavja/uvod.md"]);
    const rawWalk = await readFile(join(projectRoot, MANIFEST_FILE_NAME), "utf8");
    const walked = JSON.parse(rawWalk) as WorkbenchManifest;
    const fragmentId = walked.fragments[0]?.id ?? "";
    const incomingId = walked.incomingTexts[0]?.id ?? "";
    const insertionId = walked.insertions[0]?.id ?? "";
    const updIncoming = await run(["update-incoming", projectRoot, incomingId, "--note", "Opomba."]);
    assert.match(updIncoming.stdout, /NOTE: Opomba\./);
    const added = await run(["add-concept", projectRoot, "Pojem"]);
    assert.match(added.stdout, /CONCEPT: concept-/);
    const updFragment = await run(["update-fragment", projectRoot, fragmentId, "--text", "Novi odlomek."]);
    assert.match(updFragment.stdout, /TEXT: Novi odlomek\./);
    const updInsertion = await run(["update-insertion", projectRoot, insertionId, "--target", "poglavja/02.md"]);
    assert.match(updInsertion.stdout, /TARGET: poglavja\/02\.md/);
    const verify = await run(["verify", projectRoot]);
    assert.match(verify.stdout, /^VERIFY: PASS/m);
  } finally {
    await rm(projectRoot, { force: true, recursive: true });
  }
});

test("atma CLI bulk-insert lands two insertions atomically", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "atmavictu-cli-bulk-"));
  try {
    const cliPath = fileURLToPath(new URL("./atmaCli.js", import.meta.url));
    const run = (args: string[]) =>
      execFileAsync(process.execPath, [cliPath, ...args], { cwd: projectRoot });
    const first = await run(["capture", projectRoot, "Naslov", "Vsebina vira."]);
    assert.match(first.stdout, /^POSLEDICA/m);
    const rawCapture = await readFile(join(projectRoot, MANIFEST_FILE_NAME), "utf8");
    const captured = JSON.parse(rawCapture) as WorkbenchManifest;
    const incomingId = captured.incomingTexts[0]?.id ?? "";
    await run(["start-processing", projectRoot, incomingId]);
    await run(["create-fragment", projectRoot, incomingId, "Prvi odlomek."]);
    await run(["create-fragment", projectRoot, incomingId, "Drugi odlomek."]);
    const rawFragments = await readFile(join(projectRoot, MANIFEST_FILE_NAME), "utf8");
    const withFragments = JSON.parse(rawFragments) as WorkbenchManifest;
    const pairArgs = withFragments.fragments.map((f, i) => f.id + "=poglavja/bulk-0" + (i + 1) + ".md");
    const bulk = await run(["bulk-insert", projectRoot, ...pairArgs]);
    assert.match(bulk.stdout, /TARGET: poglavja\/bulk-01\.md/);
    assert.match(bulk.stdout, /TARGET: poglavja\/bulk-02\.md/);
    const verify = await run(["verify", projectRoot]);
    assert.match(verify.stdout, /^VERIFY: PASS/m);
    const rawFinal = await readFile(join(projectRoot, MANIFEST_FILE_NAME), "utf8");
    const final = JSON.parse(rawFinal) as WorkbenchManifest;
    assert.equal(final.insertions.length, 2);
    assert.equal(final.incomingTexts[0]?.status, "used");
  } finally {
    await rm(projectRoot, { force: true, recursive: true });
  }
});

test("atma exe path stays whole: sea-config, thin entry and headless walk", () => {
  const here = dirname(fileURLToPath(import.meta.url));
  const repoRoot = dirname(dirname(here));
  const seaConfig = join(repoRoot, "atma", "sea-config.json");
  const thinEntry = join(repoRoot, "atma", "atma-exe.cjs");
  const cliPath = join(repoRoot, "build", "src", "atmaCli.js");
  assert.ok(existsSync(seaConfig), "manjka atma/sea-config.json");
  assert.ok(existsSync(thinEntry), "manjka atma/atma-exe.cjs");
  assert.ok(existsSync(cliPath), "manjka build/src/atmaCli.js (pozheni npm test)");
  const blobPath = join(repoRoot, "atma", "atma.blob");
  const before = existsSync(blobPath) ? "obstaja" : "manjka";
  execFileSync(process.execPath, ["--experimental-sea-config", "sea-config.json"], {
    cwd: join(repoRoot, "atma"),
    encoding: "utf8",
  });
  assert.ok(existsSync(blobPath), "atma.blob se ni zgradil (prej: " + before + ")");
});
