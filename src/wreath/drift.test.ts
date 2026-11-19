import assert from "node:assert/strict";
import { test } from "node:test";
import { mkdtemp, rm, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { createHash } from "node:crypto";
import { detectWreathDrift } from "./drift.js";

function manifestItem(path: string, sha256: string) {
  return { path, sha256, size_bytes: Buffer.byteLength(sha256, "utf8") };
}

async function makeRepo(
  door: string,
  manifestDoorContent: string | null,
  items: Record<string, string>,
): Promise<string> {
  const root = await mkdtemp(join(tmpdir(), "atmavictu-drift-"));
  await writeFile(join(root, "LICENSE.md"), door);
  const doorForManifest = manifestDoorContent ?? door;
  const manifest = {
    license: "VBL",
    items: [
      manifestItem(
        "LICENSE.md",
        createHash("sha256")
          .update(Buffer.from(doorForManifest.replace(/\r\n/g, "\n"), "utf8"))
          .digest("hex"),
      ),
      ...Object.entries(items).map(([name, content]) =>
        manifestItem(name, createHash("sha256").update(Buffer.from(content.replace(/\r\n/g, "\n"), "utf8")).digest("hex"))
      ),
    ],
  };
  await writeFile(join(root, "LICENSE-MANIFEST"), JSON.stringify(manifest, null, 2));
  // zapišemo tudi datoteke same
  await writeFile(join(root, "LICENSE-DE.md"), items["LICENSE-DE.md"] ?? "");
  await writeFile(join(root, "LICENSE-FR.md"), items["LICENSE-FR.md"] ?? "");
  return root;
}

test("detectWreathDrift returns no drift when door hash equals manifest LICENSE.md slot", async () => {
  const root = await makeRepo("telo vrat\n", "telo vrat\n", {
    "LICENSE-DE.md": "telo vrat\n",
    "LICENSE-FR.md": "telo vrat\n",
  });
  try {
    const report = detectWreathDrift(root);
    assert.equal(report.drift, false);
    assert.equal(report.details.length, 0);
    assert.equal(report.doorHash, report.manifestSlotHash);
    for (const c of report.companions) {
      assert.equal(c.hashMatchesManifest, true);
    }
  } finally {
    await rm(root, { force: true, recursive: true });
  }
});

test("detectWreathDrift detects drift when door changes but manifest slot is stale", async () => {
  const root = await makeRepo("telo vrat v2\n", "telo vrat v1\n", {
    "LICENSE-DE.md": "telo vrat v1\n",
    "LICENSE-FR.md": "telo vrat v1\n",
  });
  try {
    const report = detectWreathDrift(root);
    assert.equal(report.drift, true);
    assert.notEqual(report.doorHash, report.manifestSlotHash);
    assert.ok(report.details.some((d) => d.includes("re-izdan v istem dihu")));
    // companion ≠ door je njihova narava (priča), sam po sebi drift ni:
    const fr = report.companions.find((c) => c.path.endsWith("LICENSE-FR.md"));
    assert.ok(fr);
    assert.equal(fr.hashMatchesDoor, false);
  } finally {
    await rm(root, { force: true, recursive: true });
  }
});

test("detectWreathDrift reports drift when LICENSE.md is absent", async () => {
  const root = await mkdtemp(join(tmpdir(), "atmavictu-drift-"));
  await writeFile(join(root, "LICENSE-MANIFEST"), JSON.stringify({ license: "VBL", items: [] }));
  try {
    const report = detectWreathDrift(root);
    assert.equal(report.drift, true);
    assert.equal(report.doorHash, null);
    assert.ok(report.details.some((d) => d.includes("odsotna")));
  } finally {
    await rm(root, { force: true, recursive: true });
  }
});
