import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import test from "node:test";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

import type { WorkbenchManifest } from "./workbenchManifest.js";
import { MANIFEST_FILE_NAME } from "./workbenchManifestRepository.js";

const execFileAsync = promisify(execFile);

test("captureIncomingText proof CLI prints consequence and persists files", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "atmavictu-proof-"));

  try {
    const cliPath = fileURLToPath(new URL("./captureIncomingTextProof.js", import.meta.url));
    const title = "Seed text";
    const body = "Prvi vhodni tekst.";
    const { stdout } = await execFileAsync(process.execPath, [cliPath, projectRoot, title, body], {
      cwd: projectRoot,
    });

    const manifestPath = join(projectRoot, MANIFEST_FILE_NAME);
    const bodyFilePath = join(projectRoot, "incoming", "incoming-0001.txt");
    const rawManifest = await readFile(manifestPath, "utf8");
    const manifest = JSON.parse(rawManifest) as WorkbenchManifest;
    const bodyContent = await readFile(bodyFilePath, "utf8");

    assert.match(stdout, /^POSLEDICA/m);
    assert.match(stdout, /ZADNJE DEJANJE: ZAJEMI VNOS/);
    assert.match(stdout, /USTVARJENO: incoming\/incoming-0001\.txt/);
    assert.match(stdout, /MANIFEST SLED: incoming\/incoming-0001\.txt/);
    assert.match(stdout, /TRENUTNO STANJE: CAPTURED/);
    assert.match(stdout, /NASLEDNJI KORAK: RAZREZI/);
    assert.match(stdout, /DOKAZNA MEJA: Fragment se ni ustvarjen\./);
    assert.equal(bodyContent, body);
    assert.equal(manifest.incomingTexts[0]?.sourcePath, "incoming/incoming-0001.txt");
    assert.equal("body" in (manifest.incomingTexts[0] as unknown as Record<string, unknown>), false);
  } finally {
    await rm(projectRoot, { force: true, recursive: true });
  }
});
