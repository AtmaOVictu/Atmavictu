import assert from "node:assert/strict";
import { test } from "node:test";
import { mkdtemp, rm } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { readReviewStatus, allReviewedNone } from "./review.js";

async function tempRootWithoutRegister(): Promise<string> {
  const root = await mkdtemp(join(tmpdir(), "atmavictu-review-"));
  await rm(join(root, "REGISTER-PREVERJANJ.jsonl"), { force: true });
  return root;
}

test("readReviewStatus returns stage 'none' when no review register exists", async () => {
  const root = await tempRootWithoutRegister();
  try {
    const status = readReviewStatus(root, "LICENSE-DE.md");
    assert.equal(status.slot, "LICENSE-DE.md");
    assert.equal(status.stage, "none");
  } finally {
    await rm(root, { force: true, recursive: true });
  }
});

test("allReviewedNone returns 'none' for every slot", async () => {
  const root = await tempRootWithoutRegister();
  try {
    const statuses = allReviewedNone(root, [
      "LICENSE-DE.md",
      "LICENSE-FR.md",
      "LICENSE-SLO.md",
    ]);
    assert.equal(statuses.length, 3);
    for (const s of statuses) {
      assert.equal(s.stage, "none");
    }
  } finally {
    await rm(root, { force: true, recursive: true });
  }
});

test("readReviewStatus maps PASS with independent reviewer to 'second'", () => {
  const status = readReviewStatus(process.cwd(), "LICENSE-SLO.md");
  assert.equal(status.slot, "LICENSE-SLO.md");
  assert.equal(status.stage, "second");
  assert.ok(status.reviewer);
  assert.ok(status.reviewedAt);
});

test("readReviewStatus maps PASS with executor reviewer to 'first'", () => {
  const status = readReviewStatus(process.cwd(), "LICENSE.md");
  assert.equal(status.slot, "LICENSE.md");
  assert.equal(status.stage, "first");
});

test("readReviewStatus returns 'none' for slot without register entry", () => {
  const status = readReviewStatus(process.cwd(), "LICENSE-JA.md");
  assert.equal(status.slot, "LICENSE-JA.md");
  assert.equal(status.stage, "none");
});

test("allReviewedNone returns mixed stages for real register", () => {
  const statuses = allReviewedNone(process.cwd(), [
    "LICENSE-SLO.md",
    "LICENSE-DE.md",
    "LICENSE-JA.md",
  ]);
  assert.equal(statuses.length, 3);
  const bySlot = Object.fromEntries(statuses.map((s) => [s.slot, s.stage]));
  assert.equal(bySlot["LICENSE-SLO.md"], "second");
  assert.equal(bySlot["LICENSE-DE.md"], "second");
  assert.equal(bySlot["LICENSE-JA.md"], "none");
});
