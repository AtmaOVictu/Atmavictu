import assert from "node:assert/strict";
import { test } from "node:test";
import { mkdtemp, rm, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import {
  nowIso,
  fourReceipts,
  manifestSha256,
  writeSeal,
  readSeal,
  confirmReceipt,
  type ManifestSeal,
} from "./clocks.js";

test("nowIso returns an ISO-8601 string", () => {
  const iso = nowIso();
  assert.ok(typeof iso === "string" && iso.length > 0);
  assert.ok(/^\d{4}-\d{2}-\d{2}T/.test(iso));
});

test("fourReceipts defaults seal + manifest to true, cli/ci to false", () => {
  const r = fourReceipts();
  assert.equal(r.manifest, true);
  assert.equal(r.seal, true);
  assert.equal(r.cli, false);
  assert.equal(r.ci, false);
  const r2 = fourReceipts({ cli: true, ci: true });
  assert.equal(r2.cli, true);
  assert.equal(r2.ci, true);
});

test("manifestSha256 is deterministic", () => {
  const a = manifestSha256({ foo: "bar" });
  const b = manifestSha256({ foo: "bar" });
  assert.equal(a, b);
  assert.equal(a.length, 64);
});

test("writeSeal then readSeal roundtrips in a temp directory", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "atmavictu-clocks-"));
  try {
    const manifest = { manifestVersion: "2", incomingTexts: [], fragments: [], insertions: [] };
    const seal = await writeSeal(projectRoot, manifest, { cli: true });
    assert.equal(seal.manifestPath.endsWith("book.workbench.json"), true);
    assert.equal(seal.receipts.manifest, true);
    assert.equal(seal.receipts.cli, true);
    assert.equal(typeof seal.clock.sealedAt, "string");
    assert.equal(seal.clock.receivedAt, null);
    assert.equal(seal.manifestSha256.length, 64);

    const readBack = await readSeal(projectRoot);
    assert.ok(readBack);
    assert.equal(readBack!.manifestSha256, seal.manifestSha256);
    assert.equal(readBack!.receipts.cli, true);

    const confirmed = confirmReceipt(seal);
    assert.ok(confirmed.clock.receivedAt);
    assert.notEqual(confirmed.clock.receivedAt, seal.clock.receivedAt);
  } finally {
    await rm(projectRoot, { force: true, recursive: true });
  }
});
